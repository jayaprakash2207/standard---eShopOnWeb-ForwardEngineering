# Data Flow Map — eShopOnWeb

## Major Flows

### 1. Catalog Browsing (Read)
`Web (MVC/Razor) / PublicApi` → `IRepository<CatalogItem>` (CatalogContext) → `CatalogDb.Catalog` (joined with `CatalogBrands`, `CatalogTypes`)
- Read-heavy. CachedCatalogItemServiceDecorator and CachedCatalogLookupDataServiceDecorator (BlazorAdmin) sit in front of catalog lookups to reduce DB round-trips. confidence 0.75

### 2. Basket Management
`Web/PublicApi` → `IBasketService` (BasketService.cs) → `IRepository<Basket>` → `CatalogDb.Baskets` / `BasketItems`
- `BasketService` enforces guard clauses (`BasketGuards` in GuardExtensions.cs) — e.g. throwing `BasketNotFoundException` if basket id invalid. confidence 0.8
- Basket is keyed by `BuyerId`, which is a soft reference to `AspNetUsers.Id` in IdentityDb (cross-DB, app-enforced only). confidence 0.8

### 3. Checkout / Order Creation
`Web/PublicApi` (checkout endpoint) → `IOrderService` (OrderService.cs) →
1. Reads `Basket` + `BasketItems` for the buyer
2. Validates basket is non-empty — throws `EmptyBasketOnCheckoutException` if empty (src/ApplicationCore/Exceptions/EmptyBasketOnCheckoutException.cs)
3. Snapshots each `CatalogItem` into a `CatalogItemOrdered` owned-type record (denormalization for historical accuracy)
4. Writes `Order` + `OrderItems` to `CatalogDb`
5. CORRECTED (RC-007): does **not** clear/empty the `Basket` after order creation — `OrderService.CreateOrderAsync` (src/ApplicationCore/Services/OrderService.cs) only reads the basket, validates it, snapshots items, and saves the new `Order`/`OrderItems`. No call to delete/empty the basket was found in this method. confidence 0.85. The basket remains in `Baskets`/`BasketItems` after checkout unless cleared by a caller not covered here.

### 4. Authentication / Identity
`Web/PublicApi` → ASP.NET Core Identity middleware → `IdentityDb.AspNetUsers` / `AspNetRoles` / `AspNetUserRoles`
- `ITokenClaimsService` (src/ApplicationCore/Interfaces/ITokenClaimsService.cs) issues claims/tokens for API auth (likely JWT for PublicApi — confidence 0.7, UNKNOWN exact mechanism without reading the implementation).
- CORRECTED: role name `"Administrators"` is defined in `BlazorShared.Authorization.Constants.Roles` (src/BlazorShared/Authorization/Constants.cs), referenced by `[Authorize]` attributes — see access-control-matrix.md. `AuthorizationConstants` (src/ApplicationCore/Constants/AuthorizationConstants.cs) does **not** contain role names; it holds hardcoded auth secrets (AUTH_KEY, JWT_SECRET_KEY, DEFAULT_PASSWORD) — see pii-inventory.json RC-006.

### 5. BlazorAdmin Management UI
`BlazorAdmin` (WASM client) → `HttpService` → `PublicApi` (HTTP/JSON) → `CatalogContext` → `CatalogDb`
- `CatalogItemService` / `CatalogLookupDataService` call PublicApi endpoints to list/update catalog items, brands, types.
- Decorated by cache layer (see storage-pattern-analysis.md) before hitting the network/API.
- `RefreshBroadcast` (src/BlazorAdmin/Helpers/RefreshBroadcast.cs) appears to be a pub/sub mechanism to invalidate cached data across components after a write — confidence 0.7, INFERRED from naming.

### 6. Notifications
- `IEmailSender` interface (src/ApplicationCore/Interfaces/IEmailSender.cs) — used for order confirmation or account emails. Implementation/trigger point not visible in supplied extraction. UNKNOWN, confidence < 0.7.

## Cross-Database Boundary

```
┌────────────────┐        soft FK (BuyerId)        ┌──────────────────┐
│   CatalogDb     │  <───────────────────────────── │   IdentityDb      │
│ Baskets, Orders │                                  │   AspNetUsers      │
└────────────────┘                                  └──────────────────┘
```
No DB-enforced referential integrity across this boundary — see erd.md WARNINGS.

## Change Records
- **RC-007** (CORRECTED): Checkout flow item 5 — basket is not cleared by `OrderService.CreateOrderAsync`; previously marked "inferred, clears basket" at confidence 0.7, now corrected to "not observed" at confidence 0.85. Evidence: src/ApplicationCore/Services/OrderService.cs.
- **RC-008** (ENRICHED): Authentication/Identity flow item 4 — confirmed literal role name `"Administrators"` and clarified that `AuthorizationConstants.cs` holds secrets, not role names. Evidence: src/BlazorShared/Authorization/Constants.cs; src/ApplicationCore/Constants/AuthorizationConstants.cs.
