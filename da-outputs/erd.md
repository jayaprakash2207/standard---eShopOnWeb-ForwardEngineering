# Entity-Relationship Diagram — eShopOnWeb
> Source: Code-only (migration files + EF Core configuration). DB not connected.
> Confidence: 0.9 (migration file evidence)
> Extraction date: 2026-07-06

---

## Database 1: CatalogDB (CatalogContext)

```
┌─────────────────────┐         ┌──────────────────────────────────────────────────┐
│   CatalogBrands     │         │   Catalog  (EF entity: CatalogItem)              │
│─────────────────────│         │──────────────────────────────────────────────────│
│ PK  Id   int HiLo   │◄───────│ PK  Id            int (HiLo: catalog_hilo)       │
│     Brand nvarchar  │  FK     │     Name          nvarchar(50)   NOT NULL         │
│          (100)      │  CASCADE│     Description   nvarchar(max)  nullable         │
└─────────────────────┘         │     Price         decimal(18,2)  NOT NULL         │
                                │     PictureUri    nvarchar(max)  nullable         │
┌─────────────────────┐         │ FK  CatalogBrandId int          NOT NULL ────────┘
│   CatalogTypes      │         │ FK  CatalogTypeId  int          NOT NULL ──┐
│─────────────────────│         └──────────────────────────────────────────  │
│ PK  Id   int HiLo   │◄────────────────────────────────────────────────────┘
│     Type nvarchar   │  FK CASCADE
│          (100)      │
└─────────────────────┘


┌──────────────────────────────────┐       ┌──────────────────────────────────────────┐
│   Baskets                        │       │   BasketItems                            │
│──────────────────────────────────│       │──────────────────────────────────────────│
│ PK  Id      int (IDENTITY)       │◄─────│ PK  Id            int (IDENTITY)         │
│     BuyerId nvarchar(256)        │  FK   │ FK  BasketId      int   NOT NULL         │
│             NOT NULL             │CASCADE│ ~~  CatalogItemId int   NOT NULL  ~~~    │
└──────────────────────────────────┘       │     UnitPrice     decimal(18,2)          │
                                           │     Quantity      int                    │
                                           └──────────────────────────────────────────┘
                                             ~~~ = SOFT REF (no FK to Catalog.Id)


┌──────────────────────────────────────────────────────────────┐
│   Orders                                                     │
│──────────────────────────────────────────────────────────────│
│ PK  Id                    int (IDENTITY)                     │
│     BuyerId               nvarchar(256)  NOT NULL            │
│     OrderDate             datetimeoffset NOT NULL            │
│     ShipToAddress_Street  nvarchar(180)  NOT NULL            │
│     ShipToAddress_City    nvarchar(100)  NOT NULL            │
│     ShipToAddress_State   nvarchar(60)   nullable            │
│     ShipToAddress_Country nvarchar(90)   NOT NULL            │
│     ShipToAddress_ZipCode nvarchar(18)   NOT NULL            │
└──────────────────────────────────────────────────────────────┘
                  │
                  │ 1:N  FK_OrderItems_Orders_OrderId  ON DELETE RESTRICT
                  ▼
┌────────────────────────────────────────────────────────────────────────────┐
│   OrderItems                                                               │
│────────────────────────────────────────────────────────────────────────────│
│ PK  Id                         int (IDENTITY)                              │
│ FK  OrderId                    int           nullable  (RESTRICT)          │
│ ~~  ItemOrdered_CatalogItemId  int           nullable  ~~~                 │
│     ItemOrdered_ProductName    nvarchar(50)  nullable  (price snapshot)    │
│     ItemOrdered_PictureUri     nvarchar(max) nullable  (price snapshot)    │
│     UnitPrice                  decimal(18,2) NOT NULL  (price snapshot)    │
│     Units                      int           NOT NULL                      │
└────────────────────────────────────────────────────────────────────────────┘
  ~~~ = SOFT REF (no FK to Catalog.Id — intentional snapshot design per CatalogItemOrdered XML doc)
```

---

## Database 2: IdentityDB (AppIdentityDbContext)

```
┌─────────────────────────────────────┐
│   AspNetUsers                       │   Standard ASP.NET Identity 6 schema.
│─────────────────────────────────────│   ApplicationUser adds no custom columns.
│ PK  Id                  nvarchar    │   Seed users:
│     UserName            nvarchar    │     demouser@microsoft.com (no role)
│     NormalizedUserName  nvarchar    │     admin@microsoft.com (Administrators)
│     Email               nvarchar    │
│     PasswordHash        nvarchar    │
│     ... (standard Identity cols)    │
└──────────────┬──────────────────────┘
               │ 1:N (CASCADE on delete)
               ▼
  AspNetUserRoles ──► AspNetRoles (1:N, CASCADE)
  AspNetUserClaims   (1:N, CASCADE)
  AspNetUserLogins   (1:N, CASCADE)
  AspNetUserTokens   (1:N, CASCADE)
  AspNetRoleClaims ◄── AspNetRoles (1:N, CASCADE)
```

---

## Cross-Database Soft References

| From | Field | Points To | Type |
|------|-------|-----------|------|
| Baskets.BuyerId | nvarchar(256) | AspNetUsers.UserName (or guest GUID) | Soft ref — no FK across DBs |
| Orders.BuyerId | nvarchar(256) | AspNetUsers.UserName | Soft ref — no FK across DBs |
| BasketItems.CatalogItemId | int | Catalog.Id | Soft ref — no FK within same DB |
| OrderItems.ItemOrdered_CatalogItemId | int | Catalog.Id (at time of order) | Intentional snapshot — no FK |

---

## ⚠️ WARNING — Soft References (No FK Protection)

1. **BasketItems.CatalogItemId → Catalog.Id**: No FK means a CatalogItem can be deleted while still referenced in active baskets. If the user then checks out, `OrderService.CreateOrderAsync` calls `.First(c => c.Id == basketItem.CatalogItemId)` which will throw `InvalidOperationException` if the item is gone.

2. **OrderItems.ItemOrdered_CatalogItemId → Catalog.Id**: Intentional by design (value object snapshot per XML doc comment). Product snapshot preserved even if catalog item is later deleted — this is correct for order history.

3. **Baskets.BuyerId and Orders.BuyerId → AspNetUsers.UserName**: Cross-database soft references. Deleting an Identity user leaves orphaned baskets and orders in CatalogDB. No cascade possible across databases.

4. **OrderItems.OrderId is nullable**: Migration created it as `nullable: true`. Application always creates OrderItems within an Order, but schema permits orphaned rows.

5. **ON DELETE RESTRICT on FK_OrderItems_Orders_OrderId**: Attempting to DELETE an Orders row that still has OrderItems children will raise a database error. No `DELETE` of Orders exists in current code, but this blocks any future data archiving or admin-delete flows.

---

## Unmapped Domain Entities (Dead Code)

| Entity | Location | Status |
|--------|----------|--------|
| Buyer | src/ApplicationCore/Entities/BuyerAggregate/Buyer.cs | NOT in CatalogContext. NOT in any migration. Never constructed or queried. DEAD CODE. |
| PaymentMethod | src/ApplicationCore/Entities/BuyerAggregate/PaymentMethod.cs | NOT in CatalogContext. NOT in any migration. Comment: "actual card data must be stored in a PCI compliant system, like Stripe". DEAD CODE. |
