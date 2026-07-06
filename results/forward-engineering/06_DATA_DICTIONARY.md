# Data Dictionary — eShopOnWeb

**Date:** 2026-07-06
**Database:** CatalogDb (primary) + IdentityDb (identity)
**ORM:** Entity Framework Core 8.0.2

---

## CatalogDb Entities

### CatalogItem (table: Catalog)

| Field | C# Type | SQL Type | Nullable | Constraints | Notes |
|-------|---------|---------|---------|-------------|-------|
| Id | int | INT IDENTITY(1,1) | NO | PK | Inherited from BaseEntity |
| Name | string | NVARCHAR | NO | NOT NULL; referenced by uniqueness check | Guard: non-blank |
| Description | string | NVARCHAR | NO | NOT NULL | Guard: non-blank |
| Price | decimal | DECIMAL | NO | NOT NULL | Guard: > 0; DTO range 0.01–1000 |
| PictureUri | string | NVARCHAR | YES | — | Updated via UpdatePictureUri; cache-busting broken |
| CatalogTypeId | int | INT | NO | FK → CatalogTypes.Id; ON DELETE RESTRICT* | Guard: valid |
| CatalogBrandId | int | INT | NO | FK → CatalogBrands.Id; ON DELETE RESTRICT* | Guard: valid |

*ON DELETE RESTRICT never tested by any test suite — DA_Agent2_VQ-02

### CatalogBrand (table: CatalogBrands)

| Field | C# Type | SQL Type | Nullable | Constraints |
|-------|---------|---------|---------|-------------|
| Id | int | INT IDENTITY | NO | PK |
| Brand | string | NVARCHAR | NO | NOT NULL |

### CatalogType (table: CatalogTypes)

| Field | C# Type | SQL Type | Nullable | Constraints |
|-------|---------|---------|---------|-------------|
| Id | int | INT IDENTITY | NO | PK |
| Type | string | NVARCHAR | NO | NOT NULL |

### Basket (table: Baskets)

| Field | C# Type | SQL Type | Nullable | Constraints | Notes |
|-------|---------|---------|---------|-------------|-------|
| Id | int | INT IDENTITY | NO | PK | |
| BuyerId | string | NVARCHAR | NO | NOT NULL | Either username (auth) or GUID string (anon) |

### BasketItem (table: BasketItems)

| Field | C# Type | SQL Type | Nullable | Constraints | Notes |
|-------|---------|---------|---------|-------------|-------|
| Id | int | INT IDENTITY | NO | PK | |
| UnitPrice | decimal | DECIMAL | NO | NOT NULL | Locked at add time — never updated |
| Quantity | int | INT | NO | NOT NULL; >= 0 | |
| CatalogItemId | int | INT | NO | FK → Catalog.Id | No navigation property across context |
| BasketId | int | INT | NO | FK → Baskets.Id | |

### Order (table: Orders)

| Field | C# Type | SQL Type | Nullable | Constraints | Notes |
|-------|---------|---------|---------|-------------|-------|
| Id | int | INT IDENTITY | NO | PK | |
| BuyerId | string | NVARCHAR | NO | NOT NULL | Username of authenticated buyer |
| OrderDate | DateTimeOffset | DATETIMEOFFSET | NO | NOT NULL; default = now | |
| ShipToAddress_Street | string | NVARCHAR | YES | Owned entity columns | |
| ShipToAddress_City | string | NVARCHAR | YES | Owned entity columns | |
| ShipToAddress_State | string | NVARCHAR | YES | Owned entity columns | |
| ShipToAddress_Country | string | NVARCHAR | YES | Owned entity columns | |
| ShipToAddress_ZipCode | string | NVARCHAR | YES | Owned entity columns | |

**PII:** ShipToAddress_Street, ShipToAddress_City, BuyerId contain personal data — GDPR erasure obligation.

### OrderItem (table: OrderItems)

| Field | C# Type | SQL Type | Nullable | Constraints | Notes |
|-------|---------|---------|---------|-------------|-------|
| Id | int | INT IDENTITY | NO | PK | |
| UnitPrice | decimal | DECIMAL | NO | NOT NULL | Price at basket-add time |
| Units | int | INT | NO | NOT NULL | Quantity ordered |
| ItemOrdered_CatalogItemId | int | INT | NO | NOT NULL | Snapshot — reference only; not FK |
| ItemOrdered_ProductName | string | NVARCHAR | YES | nullable:true IN MIGRATION despite IsRequired() in config | ⚠️ DISCREPANCY RC-08 / OQ-018 |
| ItemOrdered_PictureUri | string | NVARCHAR | YES | Nullable in migration | |
| OrderId | int | INT | NO | FK → Orders.Id | |

---

## IdentityDb Entities (ASP.NET Identity Standard Schema)

| Table | Key Columns | Notes |
|-------|------------|-------|
| AspNetUsers | Id (NVARCHAR PK), UserName, NormalizedUserName, Email, NormalizedEmail, EmailConfirmed, PasswordHash, SecurityStamp, ConcurrencyStamp, PhoneNumber, TwoFactorEnabled, LockoutEnd, LockoutEnabled, AccessFailedCount | Standard Identity schema |
| AspNetRoles | Id, Name, NormalizedName, ConcurrencyStamp | One seeded role: "Administrators" |
| AspNetUserRoles | UserId FK + RoleId FK | Many-to-many bridge |
| AspNetUserClaims | Id, UserId, ClaimType, ClaimValue | |
| AspNetRoleClaims | Id, RoleId, ClaimType, ClaimValue | |
| AspNetUserLogins | LoginProvider + ProviderKey + UserId | External login support |
| AspNetUserTokens | UserId + LoginProvider + Name + Value | Token storage |

---

## Indexes and Constraints (Confirmed + Gaps)

| Table | Index/Constraint | Status | Risk |
|-------|-----------------|--------|------|
| Catalog | PK on Id | Confirmed | — |
| Catalog | FK to CatalogBrands | Confirmed | ON DELETE RESTRICT untested |
| Catalog | FK to CatalogTypes | Confirmed | ON DELETE RESTRICT untested |
| Catalog | UNIQUE on Name | **ABSENT** — no UNIQUE index found | Race condition — two concurrent creates can insert same name (DA_Agent2_VQ-04) |
| Baskets | PK on Id | Confirmed | — |
| BasketItems | FK to Baskets | Confirmed | — |
| BasketItems | FK to Catalog (CatalogItemId) | Confirmed | — |
| Orders | PK on Id | Confirmed | — |
| OrderItems | FK to Orders | Confirmed | — |
| OrderItems | ItemOrdered_ProductName | nullable:true in migration — CONFLICT with EF IsRequired() | OQ-018 |

Continue with prompt "next" for documents 07–11.