=== DOCUMENT: 08_ERD.md ===

# Entity Relationship Diagram — eShopOnWeb

---

## CatalogDB — Entity Relationship Diagram (Mermaid)

```mermaid
erDiagram
    CatalogBrands {
        int Id PK
        nvarchar Brand
    }

    CatalogTypes {
        int Id PK
        nvarchar Type
    }

    CatalogItems {
        int Id PK "HiLo: catalog_hilo"
        nvarchar Name
        nvarchar Description
        decimal Price
        nvarchar PictureUri
        int CatalogTypeId FK
        int CatalogBrandId FK
    }

    Baskets {
        int Id PK
        nvarchar BuyerId "PII: email or GUID"
    }

    BasketItems {
        int Id PK
        decimal UnitPrice "Frozen at add time"
        int Quantity
        int CatalogItemId "Soft ref — no FK"
        int BasketId FK
    }

    Orders {
        int Id PK
        nvarchar BuyerId "PII: email"
        datetimeoffset OrderDate
        nvarchar ShipToAddress_Street "PII, max 180"
        nvarchar ShipToAddress_City "PII, max 100"
        nvarchar ShipToAddress_State "PII, max 60"
        nvarchar ShipToAddress_Country "PII, max 90"
        nvarchar ShipToAddress_ZipCode "PII, max 18"
    }

    OrderItems {
        int Id PK
        int OrderId FK
        int ItemOrdered_CatalogItemId "Snapshot ref"
        nvarchar ItemOrdered_ProductName "Snapshot: immutable"
        nvarchar ItemOrdered_PictureUri "Snapshot: immutable"
        decimal UnitPrice "Frozen at basket-add time"
        int Units
    }

    %% Relationships
    CatalogItems }o--|| CatalogBrands : "CatalogBrandId"
    CatalogItems }o--|| CatalogTypes : "CatalogTypeId"
    BasketItems }o--|| Baskets : "BasketId (cascade delete)"
    OrderItems }o--|| Orders : "OrderId (cascade delete)"

    %% Soft reference (no FK constraint)
    BasketItems ..o| CatalogItems : "CatalogItemId (soft ref)"
    OrderItems ..o| CatalogItems : "ItemOrdered_CatalogItemId (snapshot, soft ref)"
```

---

## IdentityDB — Entity Relationship Diagram (Mermaid)

```mermaid
erDiagram
    AspNetUsers {
        nvarchar450 Id PK
        nvarchar256 UserName
        nvarchar256 NormalizedUserName "UNIQUE index"
        nvarchar256 Email "PII"
        nvarchar256 NormalizedEmail
        bit EmailConfirmed "false until confirmed — BROKEN"
        nvarchar PasswordHash "PBKDF2 hash"
        nvarchar SecurityStamp
        nvarchar ConcurrencyStamp
        bit TwoFactorEnabled
        datetimeoffset LockoutEnd
        bit LockoutEnabled
        int AccessFailedCount
    }

    AspNetRoles {
        nvarchar450 Id PK
        nvarchar256 Name "Administrators (only role seeded)"
        nvarchar256 NormalizedName "UNIQUE index"
        nvarchar ConcurrencyStamp
    }

    AspNetUserRoles {
        nvarchar450 UserId PK_FK
        nvarchar450 RoleId PK_FK
    }

    AspNetUserClaims {
        int Id PK
        nvarchar450 UserId FK
        nvarchar ClaimType
        nvarchar ClaimValue
    }

    AspNetUserLogins {
        nvarchar450 LoginProvider PK
        nvarchar450 ProviderKey PK
        nvarchar450 UserId FK
        nvarchar ProviderDisplayName
    }

    AspNetUserTokens {
        nvarchar450 UserId PK_FK
        nvarchar450 LoginProvider PK
        nvarchar450 Name PK
        nvarchar Value "Email confirmation token stored here"
    }

    AspNetRoleClaims {
        int Id PK
        nvarchar450 RoleId FK
        nvarchar ClaimType
        nvarchar ClaimValue
    }

    %% Relationships
    AspNetUsers ||--o{ AspNetUserRoles : "has roles"
    AspNetRoles ||--o{ AspNetUserRoles : "assigned to users"
    AspNetUsers ||--o{ AspNetUserClaims : "has claims"
    AspNetUsers ||--o{ AspNetUserLogins : "external logins"
    AspNetUsers ||--o{ AspNetUserTokens : "tokens (email confirm)"
    AspNetRoles ||--o{ AspNetRoleClaims : "role claims"
```

---

## Cross-Database Conceptual Linkage

```
CatalogDB.Baskets.BuyerId (string)
    └──► IdentityDB.AspNetUsers.Email (for authenticated users)
         └── No enforced FK — application-layer join only

CatalogDB.Orders.BuyerId (string)
    └──► IdentityDB.AspNetUsers.Email
         └── No enforced FK — application-layer join only

ApplicationCore.Buyer.IdentityGuid (DEAD CODE — not persisted)
    └── Intended to link to IdentityDB.AspNetUsers.Id
```

**Note:** The cross-database BuyerId linkage is enforced only at the application layer. There are no database-level foreign key constraints between CatalogDB and IdentityDB. BuyerId in baskets and orders equals the user's email address (not the AspNetUsers.Id GUID). This creates a data consistency risk if users change their email address (not currently supported).

---

## Key Relationship Notes

| Relationship | Type | FK Enforcement | Cascade | Notes |
|-------------|------|---------------|---------|-------|
| CatalogItem → CatalogBrand | Many-to-one | Enforced FK | RESTRICT | Brand cannot be deleted if products reference it |
| CatalogItem → CatalogType | Many-to-one | Enforced FK | RESTRICT | Type cannot be deleted if products reference it |
| BasketItem → Basket | Many-to-one (owned) | Enforced FK | CASCADE DELETE | Items deleted when basket deleted |
| OrderItem → Order | Many-to-one (owned) | Enforced FK | CASCADE DELETE | Items deleted when order deleted |
| BasketItem → CatalogItem | Many-to-one | **NO FK** | None | Soft reference — orphaned basket items possible after product deletion |
| OrderItem → CatalogItem | Snapshot | **NO FK** | None | Historical snapshot — intentionally no FK; product can be deleted without affecting order history |
| Basket.BuyerId → AspNetUsers.Email | Cross-DB join | **NO FK** | None | Application-layer only |
| Order.BuyerId → AspNetUsers.Email | Cross-DB join | **NO FK** | None | Application-layer only |
