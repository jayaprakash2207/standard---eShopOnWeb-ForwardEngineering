# Entity Relationship Diagram — eShopOnWeb

`db_connection: CODE-ONLY — no live DB session in extraction (db_connection_results: [])`

> **RC-001 (CORRECTED)**: Both databases run on **PostgreSQL via Npgsql**, not SQL Server/Azure SQL Edge as originally stated — confirmed via `src/Infrastructure/Dependencies.cs` (`UseNpgsql`) and `src/Web/appsettings.json` (`Host=localhost;Port=5432;Database=eShopCatalog` / `eShopIdentity`). `appsettings.Docker.json` still has stale SQL Server connection strings. See schema-catalogue.json.

## CatalogDb

```
CatalogBrand (CatalogBrands)
  Id (PK)
  Brand
        ▲
        │ 1
        │
        │ *
CatalogItem (Catalog) ───────────────* CatalogType (CatalogTypes)
  Id (PK)                                Id (PK)
  Name                                   Type
  Description
  Price
  PictureUri
  CatalogTypeId (FK -> CatalogTypes.Id)
  CatalogBrandId (FK -> CatalogBrands.Id)
  AvailableStock
  RestockThreshold
  MaxStockThreshold
  OnReorder

Basket (Baskets)
  Id (PK)
  BuyerId  ~~~> AspNetUsers.Id   [SOFT REFERENCE — see WARNINGS]
        │ 1
        │
        │ *
BasketItem (BasketItems)
  Id (PK)
  BasketId (FK -> Baskets.Id)
  CatalogItemId (FK -> Catalog.Id)
  UnitPrice
  Quantity

Order (Orders)
  Id (PK)
  BuyerId  ~~~> AspNetUsers.Id   [SOFT REFERENCE — see WARNINGS]
  OrderDate
  ShipToAddress_* (owned type Address, flattened)
        │ 1
        │
        │ *
OrderItem (OrderItems)
  Id (PK)
  OrderId (FK -> Orders.Id)
  ItemOrdered_* (owned type CatalogItemOrdered — denormalized snapshot of CatalogItem)
  UnitPrice
  Units
```

## IdentityDb (INFERRED — standard ASP.NET Core Identity, confidence 0.7)

```
AspNetUsers
  Id (PK, string/GUID)
  UserName
  Email
  PasswordHash
  ... standard Identity columns
        │ *           │ *
        │             │
AspNetUserRoles ──── AspNetRoles
  UserId (FK)           Id (PK)
  RoleId (FK)           Name (e.g. "Administrators")
```

## ⚠️ WARNINGS — Soft / Unenforced References

1. **`Baskets.BuyerId` → `AspNetUsers.Id`** — cross-database reference (CatalogDb → IdentityDb). No DB-level FK possible since these are two separate databases/contexts. Enforced only in application code (BasketService / OrderService). confidence 0.8.
2. **`Orders.BuyerId` → `AspNetUsers.Id`** — same cross-database soft reference as above. confidence 0.8.
3. **`OrderItems.ItemOrdered_*` (CatalogItemOrdered)** — denormalized/duplicated snapshot of `Catalog` columns (Id, ProductName, PictureUri) at time of order. Not a live FK to `Catalog.Id` — by design, to preserve order history if catalog item changes/is removed later. This is an intentional historical-snapshot pattern, not a data-quality defect. confidence 0.8 — see redundancy-analysis.json.
4. **`Buyer` / `PaymentMethod` entities** (src/ApplicationCore/Entities/BuyerAggregate/) — RESOLVED (RC-002): **CONFIRMED dead/unmapped code**. `CatalogContext.cs` declares exactly 7 DbSets (Baskets, CatalogItems, CatalogBrands, CatalogTypes, Orders, OrderItems, BasketItems) and `AppIdentityDbContext.OnModelCreating` only calls `base.OnModelCreating` — no Buyer/PaymentMethod mapping exists anywhere. These entities are not part of the live schema. confidence 0.9 — see redundancy-analysis.json.
