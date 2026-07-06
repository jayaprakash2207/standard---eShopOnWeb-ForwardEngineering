=== DOCUMENT: 06_DATA_DICTIONARY.md ===

# Data Dictionary — eShopOnWeb

**Source:** DA Agent 1+2; EF migrations; entity source files; fluent configuration in Infrastructure/Data/Config/

---

## CatalogDB — Table: CatalogItems

| Column | Data Type | Nullable | Constraints | Description |
|--------|-----------|----------|-------------|-------------|
| Id | int | NOT NULL | PK, HiLo sequence (catalog_hilo) | Surrogate key; generated server-side via hi-lo algorithm |
| Name | nvarchar(max) | NOT NULL | — | Product display name; no DB UNIQUE index (DQ-001 — enforced at API layer only) |
| Description | nvarchar(max) | NOT NULL | — | Product description text |
| Price | decimal(18,2) | NOT NULL | — | Unit selling price; validated 0.01–1000.00 at application layer |
| PictureUri | nvarchar(max) | NOT NULL | — | Relative URI template; composed with CatalogSettings.CatalogBaseUrl by UriComposer |
| CatalogTypeId | int | NOT NULL | FK → CatalogTypes.Id | References the product type classification |
| CatalogBrandId | int | NOT NULL | FK → CatalogBrands.Id | References the product brand |

**PII:** None directly. Image URI is non-personal.
**Notes:** HiLo key generation reserves blocks of IDs server-side (catalog_hilo sequence). Cascade delete behavior on FK references: RESTRICT (default EF Core SQL Server behavior — parent cannot be deleted if children exist).

---

## CatalogDB — Table: CatalogBrands

| Column | Data Type | Nullable | Constraints | Description |
|--------|-----------|----------|-------------|-------------|
| Id | int | NOT NULL | PK, identity | Surrogate key |
| Brand | nvarchar(max) | NOT NULL | — | Brand display name (e.g., "Azure", ".NET") |

---

## CatalogDB — Table: CatalogTypes

| Column | Data Type | Nullable | Constraints | Description |
|--------|-----------|----------|-------------|-------------|
| Id | int | NOT NULL | PK, identity | Surrogate key |
| Type | nvarchar(max) | NOT NULL | — | Type/category display name (e.g., "T-Shirt", "Mug") |

---

## CatalogDB — Table: Baskets

| Column | Data Type | Nullable | Constraints | Description |
|--------|-----------|----------|-------------|-------------|
| Id | int | NOT NULL | PK, identity | Surrogate key |
| BuyerId | nvarchar(max) | NOT NULL | — | **PII** — For authenticated users: email address. For anonymous: GUID string from browser cookie. |

**PII:** BuyerId contains email address for authenticated users.
**Notes:** No expiry or TTL column. Anonymous baskets persist indefinitely (PP-08). Basket remains after order creation (BR-26).

---

## CatalogDB — Table: BasketItems

| Column | Data Type | Nullable | Constraints | Description |
|--------|-----------|----------|-------------|-------------|
| Id | int | NOT NULL | PK, identity | Surrogate key |
| UnitPrice | decimal(18,2) | NOT NULL | — | Price frozen at basket-add time (BR-22); never recalculated |
| Quantity | int | NOT NULL | ≥ 0 (application constraint) | Item quantity; 0-qty items removed by RemoveEmptyItems() (BR-16) |
| CatalogItemId | int | NOT NULL | No FK constraint in EF — soft reference only | Reference to CatalogItems.Id; **no enforced FK** (DA Agent 1) — can reference deleted products |
| BasketId | int | NOT NULL | FK → Baskets.Id | Owning basket |

**Notes:** CatalogItemId has no EF FK constraint declared — EF InMemory tests would never catch an orphaned reference. EF Core SQL Server will infer the FK constraint from navigation property conventions unless explicitly removed.

---

## CatalogDB — Table: Orders

| Column | Data Type | Nullable | Constraints | Description |
|--------|-----------|----------|-------------|-------------|
| Id | int | NOT NULL | PK, identity | Surrogate key |
| BuyerId | nvarchar(max) | NOT NULL | Guard.Against.NullOrEmpty | **PII** — authenticated user's email address |
| OrderDate | datetimeoffset(7) | NOT NULL | Default: DateTimeOffset.Now | Timestamp of order creation; immutable after save |
| ShipToAddress_Street | nvarchar(180) | NOT NULL | Max 180 chars | **PII** — physical delivery address |
| ShipToAddress_City | nvarchar(100) | NOT NULL | Max 100 chars | **PII** |
| ShipToAddress_State | nvarchar(60) | NOT NULL | Max 60 chars | **PII** |
| ShipToAddress_Country | nvarchar(90) | NOT NULL | Max 90 chars | **PII** |
| ShipToAddress_ZipCode | nvarchar(18) | NOT NULL | Max 18 chars | **PII** |

**PII:** BuyerId (email), all ShipToAddress columns.
**Notes:** No OrderStatus column. Orders are a terminal write — no lifecycle state machine. ShipToAddress columns are EF owned entity columns (not a separate table).

---

## CatalogDB — Table: OrderItems

| Column | Data Type | Nullable | Constraints | Description |
|--------|-----------|----------|-------------|-------------|
| Id | int | NOT NULL | PK, identity | Surrogate key |
| OrderId | int | NOT NULL | FK → Orders.Id | Owning order |
| ItemOrdered_CatalogItemId | int | NOT NULL | Guard.Against.Zero | Original product ID (for reference; not an active FK) |
| ItemOrdered_ProductName | nvarchar(max) | NOT NULL | Guard.Against.NullOrEmpty | **Snapshot** — product name at time of order; immutable (BR-21) |
| ItemOrdered_PictureUri | nvarchar(max) | NOT NULL | Guard.Against.NullOrEmpty | **Snapshot** — product image URI at time of order; immutable (BR-21) |
| UnitPrice | decimal(18,2) | NOT NULL | Guard.Against.NegativeOrZero | Price at basket-add time (BR-22); immutable |
| Units | int | NOT NULL | Guard.Against.OutOfRange (≥ 1) | Quantity ordered |

**Notes:** ItemOrdered_* columns are EF owned entity columns. The ProductName and PictureUri are snapshots — future catalog changes do not affect historical orders. This is the correct pattern per BR-21.

---

## IdentityDB — Table: AspNetUsers

| Column | Data Type | Nullable | Description |
|--------|-----------|----------|-------------|
| Id | nvarchar(450) | NOT NULL PK | GUID string — ApplicationUser.Id |
| UserName | nvarchar(256) | NULL | Username (used as login; same as Email in this system) |
| NormalizedUserName | nvarchar(256) | NULL | Uppercase normalized for queries |
| Email | nvarchar(256) | NULL | **PII** — email address |
| NormalizedEmail | nvarchar(256) | NULL | Uppercase normalized |
| EmailConfirmed | bit | NOT NULL | False until email confirmation; confirmation currently broken (TD-08) |
| PasswordHash | nvarchar(max) | NULL | **Sensitive** — PBKDF2 hash (ASP.NET Identity default) |
| SecurityStamp | nvarchar(max) | NULL | Invalidation stamp for credential rotation |
| ConcurrencyStamp | nvarchar(max) | NULL | Optimistic concurrency |
| PhoneNumber | nvarchar(max) | NULL | Optional; not used in current system |
| PhoneNumberConfirmed | bit | NOT NULL | Not used |
| TwoFactorEnabled | bit | NOT NULL | Two-factor auth flag; handled in AuthenticateEndpoint |
| LockoutEnd | datetimeoffset(7) | NULL | Lockout expiry; set on account lockout (BR-30) |
| LockoutEnabled | bit | NOT NULL | Whether lockout is allowed for this user |
| AccessFailedCount | int | NOT NULL | Incremented on failed login; reset on success |

**Seeded rows:**
- `demouser@microsoft.com` / Pass@word1 (BR-33 — CRITICAL: hardcoded password)
- `admin@microsoft.com` / Pass@word1, Administrators role (BR-33 — CRITICAL)

---

## IdentityDB — Table: AspNetRoles

| Column | Data Type | Description |
|--------|-----------|-------------|
| Id | nvarchar(450) PK | Role GUID |
| Name | nvarchar(256) | Role name: "Administrators" |
| NormalizedName | nvarchar(256) | "ADMINISTRATORS" |
| ConcurrencyStamp | nvarchar(max) | Optimistic concurrency |

**Seeded roles:** "Administrators" only.

---

## IdentityDB — Table: AspNetUserRoles

| Column | Data Type | Description |
|--------|-----------|-------------|
| UserId | nvarchar(450) PK, FK | FK → AspNetUsers.Id |
| RoleId | nvarchar(450) PK, FK | FK → AspNetRoles.Id |

**Seeded:** admin@microsoft.com → Administrators role.

---

## Conceptual Entity Glossary

| Term | Definition |
|------|------------|
| **Product / CatalogItem** | A physical good available for purchase; has name, description, price, image, brand, and type. |
| **Brand** | A manufacturer or label associated with one or more products (e.g., "Azure"). |
| **Type** | A product category or classification (e.g., "T-Shirt", "Mug"). |
| **Basket** | A temporary collection of products a user intends to purchase; can be anonymous or authenticated. |
| **Basket Item** | A single product line in a basket with a price (frozen at add time) and quantity. |
| **Order** | An immutable record of a completed purchase transaction with buyer, date, shipping address, and line items. |
| **Order Item** | A line in an order capturing product snapshot, price, and quantity — immutable after creation. |
| **Address** | A shipping destination with street, city, state, country, and zip code. |
| **Product Snapshot (CatalogItemOrdered)** | An immutable copy of product name and image URI captured at order creation time. |
| **BuyerId** | A string identifier linking baskets and orders to a user. Contains email for authenticated users; GUID for anonymous. |
| **Administrator** | A system role granting catalog management rights via the BlazorAdmin portal and PublicApi. |
| **Buyer** | A domain entity representing a customer profile with saved payment methods (currently not persisted). |
| **PaymentMethod** | A tokenized payment instrument associated with a Buyer (PCI reference token; currently not persisted). |
