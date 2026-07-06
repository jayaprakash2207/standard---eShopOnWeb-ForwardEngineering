# Data Dictionary — eShopOnWeb
> Source: Migration files (confidence 0.9), EF entity and configuration code (0.8). DB not connected.
> Every table in schema-catalogue.json is represented below.
> Extraction date: 2026-07-06

---

## Database: CatalogDB (CatalogContext)

---

### Table: Baskets

**Business meaning:** A shopping session container. One basket per buyer identity at a time (enforced at the application layer, not the database). Destroyed after successful checkout.

| Column | Type | Nullable | Business Meaning |
|--------|------|----------|-----------------|
| Id | int (IDENTITY 1,1) | NOT NULL | System-generated basket identifier. |
| BuyerId | nvarchar(256) | NOT NULL | Identity of the basket owner. For authenticated users: their email address (matches AspNetUsers.UserName). For anonymous users: a GUID string issued via browser cookie with a 10-year TTL. Originally nvarchar(40) in the initial migration; widened to nvarchar(256) in FixBuyerId (2021-10-26) to accommodate email addresses. |

---

### Table: BasketItems

**Business meaning:** A single product line item in a shopping basket with its price locked at add-time.

| Column | Type | Nullable | Business Meaning |
|--------|------|----------|-----------------|
| Id | int (IDENTITY 1,1) | NOT NULL | System-generated line item identifier. |
| BasketId | int (FK → Baskets.Id CASCADE) | NOT NULL | Parent basket. Cascade delete — deleting the basket removes all its items. |
| CatalogItemId | int (soft ref → Catalog.Id) | NOT NULL | The product this line item represents. No FK constraint — a CatalogItem can be deleted without cascading to BasketItems, leaving a dangling reference. |
| UnitPrice | decimal(18,2) | NOT NULL | Price of the product **at the time it was added to the basket**. Not updated if the catalog price changes later. Copied to OrderItem.UnitPrice at checkout. |
| Quantity | int | NOT NULL | Number of units selected. Must be ≥ 0. Zero-quantity items are removed by `Basket.RemoveEmptyItems()`. |

---

### Table: Catalog  *(EF entity: CatalogItem — mapped via `.ToTable("Catalog")` in CatalogItemConfiguration)*

**Business meaning:** The master product catalogue. Source of truth for current product details. Managed exclusively by administrators.

| Column | Type | Nullable | Business Meaning |
|--------|------|----------|-----------------|
| Id | int (HiLo: catalog_hilo, increment 10) | NOT NULL | System-generated product identifier. Uses HiLo for batch insert efficiency — IDs increment by 10. |
| Name | nvarchar(50) | NOT NULL | Product display name. Must be ≤ 50 characters. Application-level uniqueness check in CreateCatalogItemEndpoint (no DB UNIQUE index). |
| Description | nvarchar(max) | nullable | Long-form product description. |
| Price | decimal(18,2) | NOT NULL | Current selling price. Domain entity guards against negative or zero. DTO enforces Range(0.01, 1000). |
| PictureUri | nvarchar(max) | nullable | Template URI for product image. Raw value stored as `http://catalogbaseurltobereplaced/images/products/{n}.png`; resolved at read time by `UriComposer` using `CatalogSettings.CatalogBaseUrl`. New items use `eCatalog-item-default.png` (image upload disabled). |
| CatalogTypeId | int (FK → CatalogTypes.Id CASCADE) | NOT NULL | Product category (e.g. Mug, T-Shirt). |
| CatalogBrandId | int (FK → CatalogBrands.Id CASCADE) | NOT NULL | Product brand (e.g. .NET, Azure). |

---

### Table: CatalogBrands

**Business meaning:** Reference data for product brand labels.

| Column | Type | Nullable | Business Meaning |
|--------|------|----------|-----------------|
| Id | int (HiLo: catalog_brand_hilo, increment 10) | NOT NULL | System-generated brand identifier. |
| Brand | nvarchar(100) | NOT NULL | Brand name. Seed data: Azure, .NET, Visual Studio, SQL Server, Other. Mapped to field `Name` in CatalogBrandDto via AutoMapper. |

---

### Table: CatalogTypes

**Business meaning:** Reference data for product type/category classifications.

| Column | Type | Nullable | Business Meaning |
|--------|------|----------|-----------------|
| Id | int (HiLo: catalog_type_hilo, increment 10) | NOT NULL | System-generated type identifier. |
| Type | nvarchar(100) | NOT NULL | Product type/category name. Seed data: Mug, T-Shirt, Sheet, USB Memory Stick. **Note:** mapped to field `Name` in CatalogTypeDto via AutoMapper — the field name in the API response differs from the column name. |

---

### Table: Orders

**Business meaning:** A completed purchase transaction. Captures the buyer, shipping destination, date, and all items at the time of purchase. Immutable historical record.

| Column | Type | Nullable | Business Meaning |
|--------|------|----------|-----------------|
| Id | int (IDENTITY 1,1) | NOT NULL | System-generated order identifier. |
| BuyerId | nvarchar(256) | NOT NULL | Email address of the customer who placed the order. Stored as plain string — no FK to IdentityDB. If the Identity account is deleted, the order record is retained with the email address. |
| OrderDate | datetimeoffset | NOT NULL | Date and time when the order was created. Set by the application server clock (`DateTimeOffset.Now` in the Order constructor), not a DB default. |
| ShipToAddress_Street | nvarchar(180) | NOT NULL | Shipping street address. Owned value object column. Made NOT NULL in FixShipToAddress migration (2021-12-31). |
| ShipToAddress_City | nvarchar(100) | NOT NULL | Shipping city. Made NOT NULL in FixShipToAddress migration. |
| ShipToAddress_State | nvarchar(60) | nullable | Shipping state or province. **Intentionally nullable** — not all international addresses have a state. Only nullable ShipToAddress column. |
| ShipToAddress_Country | nvarchar(90) | NOT NULL | Shipping country. Made NOT NULL in FixShipToAddress migration. |
| ShipToAddress_ZipCode | nvarchar(18) | NOT NULL | Shipping postal/zip code. Made NOT NULL in FixShipToAddress migration. |

---

### Table: OrderItems

**Business meaning:** An immutable line-item record of what was purchased, at what price. All `ItemOrdered_*` columns are a snapshot of the product at the moment of purchase and preserve order history even if the catalogue later changes.

| Column | Type | Nullable | Business Meaning |
|--------|------|----------|-----------------|
| Id | int (IDENTITY 1,1) | NOT NULL | System-generated order line item identifier. |
| OrderId | int (FK → Orders.Id RESTRICT) | nullable | Parent order. **ON DELETE RESTRICT** — an order cannot be deleted while it has items. **Nullable in schema** (see DQ-06), though always set in practice. |
| ItemOrdered_CatalogItemId | int (soft ref → Catalog.Id) | nullable | The catalog product ID **at time of purchase**. Preserved in history even if the catalog item is later deleted. No FK — intentional snapshot design. |
| ItemOrdered_ProductName | nvarchar(50) | nullable | Product name **at time of purchase**. Snapshot — preserved even if product is later renamed. |
| ItemOrdered_PictureUri | nvarchar(max) | nullable | Product image URI **at time of purchase**. Snapshot. |
| UnitPrice | decimal(18,2) | NOT NULL | Price paid per unit. Copied from `BasketItem.UnitPrice` at checkout — not the current `Catalog.Price`. |
| Units | int | NOT NULL | Number of units ordered. |

---

## Database: IdentityDB (AppIdentityDbContext)

---

### Table: AspNetUsers

**Business meaning:** Registered members of the store. Manages authentication credentials, lockout state, and role membership.

| Column | Type | Nullable | Business Meaning |
|--------|------|----------|-----------------|
| Id | nvarchar(450) | NOT NULL (PK) | ASP.NET Identity GUID string identifier. |
| UserName | nvarchar(256) | nullable | The user's email address used as their login username (e.g. `demouser@microsoft.com`). Referenced in CatalogDB as `Baskets.BuyerId` and `Orders.BuyerId`. |
| NormalizedUserName | nvarchar(256) | nullable | Uppercase UserName for case-insensitive lookups. Unique index (filtered). |
| Email | nvarchar(256) | nullable | User's email address — same value as UserName in this application. PII. |
| NormalizedEmail | nvarchar(256) | nullable | Uppercase Email. Non-unique index. PII. |
| EmailConfirmed | bit | NOT NULL | Whether the email has been verified via confirmation link. |
| PasswordHash | nvarchar(max) | nullable | PBKDF2 hashed password (ASP.NET Identity). Not plaintext. |
| SecurityStamp | nvarchar(max) | nullable | Random value regenerated on password/security change. Used to invalidate auth tokens. |
| ConcurrencyStamp | nvarchar(max) | nullable | Optimistic concurrency token. |
| PhoneNumber | nvarchar(max) | nullable | Optional phone number. Not collected in the demo UI. |
| PhoneNumberConfirmed | bit | NOT NULL | Whether phone number is verified. |
| TwoFactorEnabled | bit | NOT NULL | Whether two-factor authentication is enabled. |
| LockoutEnd | datetimeoffset | nullable | When the account lockout ends. NULL if not locked out. |
| LockoutEnabled | bit | NOT NULL | Whether lockout is enabled for this account. |
| AccessFailedCount | int | NOT NULL | Consecutive failed login attempts. Increments on failure; resets on success. |

**Seed data:** `demouser@microsoft.com` (no roles), `admin@microsoft.com` (Administrators role). Both use `DEFAULT_PASSWORD` ("Pass@word1") — see DQ-09.

---

### Tables: AspNetRoles, AspNetUserRoles, AspNetUserClaims, AspNetUserLogins, AspNetUserTokens, AspNetRoleClaims

Standard ASP.NET Identity 6 schema. `ApplicationUser` adds no custom columns beyond `IdentityUser`. `AspNetRoles` contains one seeded record: `Administrators`. All related tables (claims, logins, tokens, role assignments) use standard Identity structure with cascade-delete FKs back to AspNetUsers and AspNetRoles.

---

## Sequences (CatalogDB)

| Sequence | Increment | Used By | Business Meaning |
|----------|-----------|---------|-----------------|
| catalog_hilo | 10 | Catalog.Id | HiLo strategy for product IDs. Allows batch inserts without round-trips. IDs skip by 10 (e.g. 1, 11, 21…). |
| catalog_brand_hilo | 10 | CatalogBrands.Id | HiLo for brand IDs. |
| catalog_type_hilo | 10 | CatalogTypes.Id | HiLo for type IDs. |
