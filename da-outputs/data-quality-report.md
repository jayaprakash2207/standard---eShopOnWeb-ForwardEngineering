# Data Quality Report — eShopOnWeb
> Source: Code-only (migration files + EF configuration + service layer). DB not connected.
> Confidence: 0.9 (migration file evidence)
> Extraction date: 2026-07-06

---

## DQ-01 — ON DELETE RESTRICT on OrderItems → Orders

| Attribute | Value |
|-----------|-------|
| Table | OrderItems |
| Column | OrderId (FK) |
| Constraint | FK_OrderItems_Orders_OrderId — ON DELETE RESTRICT |
| Risk | HIGH |
| Status | ⚠️ FLAGGED |

**Detail:** The FK from `OrderItems.OrderId` to `Orders.Id` uses `ReferentialAction.Restrict`. Attempting to DELETE an Orders row that still has child OrderItems will raise a database error. There is no soft-delete mechanism and no code in the current codebase deletes Orders. However this constraint blocks any future data archiving, order cancellation, or admin-delete functionality. Any safe deletion path must either delete OrderItems first or use EF with navigation properties fully loaded.

---

## DQ-02 — No FK: BasketItems.CatalogItemId → Catalog.Id

| Attribute | Value |
|-----------|-------|
| Table | BasketItems |
| Column | CatalogItemId |
| Expected FK | Catalog.Id |
| Actual | No FK constraint |
| Risk | MEDIUM |
| Status | ⚠️ FLAGGED |

**Detail:** A catalog item can be deleted from the Catalog table while still referenced in active BasketItems. If the user then checks out, `OrderService.CreateOrderAsync` calls `.First(c => c.Id == basketItem.CatalogItemId)` — if the item is gone this throws `InvalidOperationException`. No defensive null-check exists at that call site.

**Recommendation:** Add a guard in `OrderService.CreateOrderAsync` to handle missing catalog items, or add an FK with appropriate ON DELETE behaviour.

---

## DQ-03 — OrderDate Set by Application Clock, Not DB Default

| Attribute | Value |
|-----------|-------|
| Table | Orders |
| Column | OrderDate |
| Issue | `DateTimeOffset.Now` set in C# constructor — not a DB server default |
| Risk | LOW |
| Status | ℹ️ NOTED |

**Detail:** `Order.OrderDate` is set in the entity constructor. In a multi-instance deployment, clock drift between app servers could produce non-monotonic `OrderDate` values.

---

## DQ-04 — CatalogItem Name Uniqueness Enforced at Application Layer Only

| Attribute | Value |
|-----------|-------|
| Table | Catalog |
| Column | Name |
| DB Constraint | None |
| App-level check | CatalogItemNameSpecification count in CreateCatalogItemEndpoint only |
| Risk | MEDIUM |
| Status | ⚠️ FLAGGED |

**Detail:** The uniqueness of `CatalogItem.Name` is enforced only in `CreateCatalogItemEndpoint.HandleAsync` via a count query. No UNIQUE index on `Catalog.Name` in any migration. Under concurrent create requests, both could pass the check and insert duplicate names. `UpdateCatalogItemEndpoint` does NOT check name uniqueness at all.

---

## DQ-05 — ShipToAddress_State is Nullable (Intentional Inconsistency)

| Attribute | Value |
|-----------|-------|
| Table | Orders |
| Column | ShipToAddress_State |
| Constraint | nullable: true — nvarchar(60) |
| Risk | LOW |
| Status | ℹ️ NOTED |

**Detail:** The `FixShipToAddress` migration made all other `ShipToAddress_*` columns NOT NULL, but `State` remains nullable. `OrderConfiguration.cs` does not call `.IsRequired()` for State. Likely intentional (international addresses may omit state/province).

---

## DQ-06 — OrderItems.OrderId is Nullable

| Attribute | Value |
|-----------|-------|
| Table | OrderItems |
| Column | OrderId |
| Constraint | nullable: true (migration) |
| Risk | MEDIUM |
| Status | ⚠️ FLAGGED |

**Detail:** The migration created `OrderId` as `nullable: true`. In practice `OrderService` always creates OrderItems as part of an Order graph. However the schema permits orphaned OrderItem rows. A future code change creating OrderItems before their Order could silently produce NULL OrderId rows.

---

## DQ-07 — Non-Atomic Basket Transfer

| Attribute | Value |
|-----------|-------|
| Operation | TransferBasketAsync |
| Service | BasketService.cs |
| Risk | MEDIUM |
| Status | ⚠️ FLAGGED |

**Detail:** `TransferBasketAsync` in `BasketService.cs` makes two separate EF `SaveChanges` calls:
1. `UpdateAsync(userBasket)` — merges anonymous items into user basket
2. `DeleteAsync(anonymousBasket)` — deletes the anonymous basket

If `DeleteAsync` fails after `UpdateAsync` succeeds, both baskets will contain the same items. There is no transaction wrapping these operations.

---

## DQ-08 — Price Divergence (Basket vs. Order — By Design)

| Attribute | Value |
|-----------|-------|
| Tables | BasketItems.UnitPrice, OrderItems.UnitPrice, Catalog.Price |
| Risk | LOW (intentional design) |
| Status | ℹ️ NOTED — intended behaviour |

**Detail:** `BasketItems.UnitPrice` is captured at basket-add time. `OrderItems.UnitPrice` is copied from `BasketItem.UnitPrice` at checkout — not from the current `Catalog.Price`. A catalog price change between basket-add and checkout will not affect the order total. There is no UI notification if a price drops after the shopper added to cart.

---

## DQ-09 — Hardcoded Default Password and JWT Key

| Attribute | Value |
|-----------|-------|
| File | src/ApplicationCore/Constants/AuthorizationConstants.cs |
| Risk | CRITICAL (for production) |
| Status | ⚠️ FLAGGED |

**Detail:** Both `DEFAULT_PASSWORD` ("Pass@word1") and `JWT_SECRET_KEY` ("SecretKeyOfDoomThatMustBeAMinimumNumberOfBytes") are hardcoded string constants with TODO comments. These values are committed to source control. In production: (a) both seeded accounts share this password, (b) the JWT signing key is known — any party with source access can forge admin tokens. Automated tests depend on both values, so they cannot be changed without also updating tests.

---

## DQ-10 — Image Upload Disabled (Security Risk Mitigated)

| Attribute | Value |
|-----------|-------|
| File | CreateCatalogItemEndpoint.cs |
| Risk | LOW (mitigated) |
| Status | ℹ️ NOTED |

**Detail:** Image upload was intentionally disabled after a community-reported security concern (GitHub issue #537). All new catalog items receive `eCatalog-item-default.png`. The PictureUri column still exists and stores the placeholder path.

---

## DQ-11 — Create Catalog Item Uses Two SaveChanges Calls (Non-Atomic)

| Attribute | Value |
|-----------|-------|
| File | src/PublicApi/CatalogItemEndpoints/CreateCatalogItemEndpoint.cs |
| Risk | LOW |
| Status | ⚠️ FLAGGED |

**Detail:** `CreateCatalogItemEndpoint.HandleAsync` calls `itemRepository.AddAsync(newItem)` to obtain the new Id, then calls `itemRepository.UpdateAsync(newItem)` to set the placeholder `PictureUri`. If the second call fails, a catalog item will exist with no `PictureUri` set.

---

## DQ-12 — All Tests Run Against In-Memory Database (SQL Constraints Untested)

| Attribute | Value |
|-----------|-------|
| Component | All test suites |
| Risk | HIGH (for production deployment validation) |
| Status | ⚠️ FLAGGED |

**Detail:** Every test fixture in the codebase substitutes the SQL Server DbContext with `UseInMemoryDatabase(...)`. EF's in-memory provider does NOT enforce FK constraints, UNIQUE constraints, NULL constraints, or HiLo sequence behaviour. This means all DQ issues in this report (DQ-01 RESTRICT, DQ-02 no FK, DQ-04 no UNIQUE index, DQ-06 nullable OrderId) are currently invisible to the automated test suite.

**Recommendation:** Before production migration, run at minimum one integration test suite against a real SQL Server (or SQLite with FK pragma enabled) to validate constraint behaviour.

---

## DQ-13 — OrderItemConfiguration: ItemOrdered_ProductName Marked IsRequired But Migration Has It Nullable

| Attribute | Value |
|-----------|-------|
| Table | OrderItems |
| Column | ItemOrdered_ProductName |
| EF Config | `io.Property(cio => cio.ProductName).HasMaxLength(50).IsRequired()` |
| Migration | `nullable: true` (InitialModel, line 136) |
| Risk | LOW |
| Status | ⚠️ DISCREPANCY NOTED |

**Detail:** `OrderItemConfiguration.cs` calls `.IsRequired()` on `ItemOrdered_ProductName`, but the InitialModel migration generated `nullable: true`. The ORM config and migration are inconsistent. In a real SQL Server deployment, the migration column definition (nullable) governs actual schema. The IsRequired() in code adds model validation but does not retroactively update SQL. This discrepancy means the application layer expects non-null but the database allows null. In practice all order creation paths set ProductName (via `CatalogItemOrdered` constructor, which guards NullOrEmpty), so orphaned nulls are unlikely — but the schema gap exists.

---

## Agent 2 Review Changes

```json
[
  {
    "change_id": "RC-06",
    "type": "ADDED",
    "finding_id": "data-quality-report.md — DQ-13 (new)",
    "what": "OrderItemConfiguration marks ItemOrdered_ProductName as IsRequired() but migration created it nullable: true. EF config and migration disagree. In-memory tests won't catch this.",
    "evidence_source": "Phase 4 spot check / cross-file consistency",
    "evidence_detail": "src/Infrastructure/Data/Config/OrderItemConfiguration.cs:16-17 — .IsRequired(). Migration 20201202111507_InitialModel.cs:136 — nullable: true.",
    "confidence_before": 0.0,
    "confidence_after": 0.95,
    "phase_found": "Phase 4 spot check"
  },
  {
    "change_id": "RC-07",
    "type": "ENRICHED",
    "finding_id": "data-quality-report.md — DQ-12",
    "what": "Qualifier added: PublicApiIntegrationTests MSTest suite does NOT override DbContext and may hit localdb. The 'all tests in-memory' claim is 95% accurate but not 100%. Three of four test projects are confirmed in-memory.",
    "evidence_source": "Phase 1 test review",
    "evidence_detail": "tests/PublicApiIntegrationTests/ProgramTest.cs — WebApplicationFactory<Program> with no DB override. src/PublicApi/appsettings.json — CatalogConnection points to localdb, no UseOnlyInMemoryDatabase flag.",
    "confidence_before": 0.9,
    "confidence_after": 0.9,
    "phase_found": "Phase 1 test review"
  }
]
```

## Summary Table

| ID | Issue | Table / Component | Severity |
|----|-------|-------------------|----------|
| DQ-01 | ON DELETE RESTRICT blocks Order deletion | OrderItems | HIGH |
| DQ-02 | No FK: BasketItems.CatalogItemId → Catalog | BasketItems | MEDIUM |
| DQ-03 | OrderDate uses app server clock | Orders | LOW |
| DQ-04 | No UNIQUE index on Catalog.Name | Catalog | MEDIUM |
| DQ-05 | ShipToAddress_State nullable (intentional) | Orders | LOW |
| DQ-06 | OrderItems.OrderId nullable | OrderItems | MEDIUM |
| DQ-07 | Non-atomic basket transfer (2 SaveChanges) | BasketService | MEDIUM |
| DQ-08 | Price divergence basket→order (by design) | BasketItems/OrderItems | LOW/Intended |
| DQ-09 | Hardcoded credentials in source | AuthorizationConstants.cs | CRITICAL (prod) |
| DQ-10 | Image upload disabled | CreateCatalogItemEndpoint | LOW (mitigated) |
| DQ-11 | Create catalog item — 2 SaveChanges calls | CreateCatalogItemEndpoint | LOW |
| DQ-12 | All tests use in-memory DB — constraints untested | All test suites | HIGH |
