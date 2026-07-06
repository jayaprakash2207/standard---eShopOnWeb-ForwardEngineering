# Data Flow Map — eShopOnWeb
> Source: Phase 1 code discovery (entity/ORM code + service layer + specifications)
> Confidence: 0.8
> Extraction date: 2026-07-06

---

## System Overview

```
┌─────────────┐    HTTP/REST     ┌──────────────────┐    EF Core    ┌──────────────┐
│ BlazorAdmin │ ──────────────► │   PublicApi       │ ────────────► │  CatalogDB   │
│  (WASM)     │    JWT Bearer    │  (Minimal API)    │               │  SQL Server  │
└─────────────┘                  └──────────────────┘               └──────────────┘
      │                                   │
      │ LocalStorage cache                │ EF Core
      │ (1 min TTL)                       ▼
                                  ┌──────────────────┐
                                  │   IdentityDB     │
                                  │  (ASP.NET        │
                                  │   Identity)      │
                                  └──────────────────┘

┌─────────────┐    Cookie/Session  ┌──────────────────┐    EF Core    ┌──────────────┐
│  Browser    │ ◄────────────────► │   Web MVC         │ ────────────► │  CatalogDB   │
│  (Shopper)  │    Cookie basket   │  (Razor Pages)    │               │              │
└─────────────┘                    └──────────────────┘               └──────────────┘
                                          │
                                          │ IMemoryCache (30s sliding)
                                          │ Brands, Types, CatalogItems
```

---

## Flow 1 — Browse Catalog (anonymous or authenticated)

```
Browser GET /
  → Web MVC Index.cshtml.cs
    → CachedCatalogViewModelService.GetCatalogItems(pageIndex, itemsPage, brandId?, typeId?)
      [Cache HIT  — 30s sliding]  → return cached CatalogIndexViewModel
      [Cache MISS]                 → CatalogViewModelService.GetCatalogItems()
                                       → IReadRepository<CatalogItem>.ListAsync(CatalogFilterPaginatedSpecification)
                                           → EF Core SELECT FROM Catalog WHERE brandId/typeId SKIP/TAKE
                                       → IReadRepository<CatalogBrand>.ListAsync()
                                       → IReadRepository<CatalogType>.ListAsync()
                                     → cache result (sliding 30s)
  ← HTML paginated catalog grid
```

---

## Flow 2 — Add to Basket

```
Browser POST /basket/add
  → Web MVC BasketViewModelService (or basket page handler)
    → BasketService.AddItemToBasket(username, catalogItemId, price, quantity)
      → IRepository<Basket>.FirstOrDefaultAsync(BasketWithItemsSpecification(username))
        [NULL]  → new Basket(username); IRepository<Basket>.AddAsync()
        [FOUND] → basket.AddItem(catalogItemId, price, quantity)
                    [item exists] → existingItem.AddQuantity(quantity)
                    [new item]    → _items.Add(new BasketItem(catalogItemId, quantity, unitPrice))
      → IRepository<Basket>.UpdateAsync()
          → EF Core INSERT/UPDATE Baskets + BasketItems

Anonymous user: BuyerId = GUID from 10-year browser cookie
Authenticated user: BuyerId = User.Identity.Name (email address)
```

---

## Flow 3 — Checkout (Basket → Order)

```
Browser POST /basket/checkout
  → CheckoutModel.OnPost(items)
    1. BasketService.SetQuantities(basketId, quantities)
         → UPDATE BasketItems.Quantity; Basket.RemoveEmptyItems() removes zero-qty
    2. OrderService.CreateOrderAsync(basketId, shippingAddress)
         → IRepository<Basket>.FirstOrDefaultAsync(BasketWithItemsSpecification(basketId))
             → Guard.Against.EmptyBasketOnCheckout(basket.Items)  [throws if 0 items]
         → IRepository<CatalogItem>.ListAsync(CatalogItemsSpecification(catalogItemIds[]))
             → EF Core SELECT FROM Catalog WHERE Id IN (...)
         → foreach basket item:
             → new CatalogItemOrdered(catalogItem.Id, catalogItem.Name, uriComposer.ComposePicUri(...))
             → new OrderItem(itemOrdered, basketItem.UnitPrice, basketItem.Quantity)
               *** UnitPrice taken from BasketItem, NOT current Catalog.Price ***
         → new Order(basket.BuyerId, shippingAddress, items)
         → IRepository<Order>.AddAsync(order)
             → EF Core INSERT Orders + INSERT OrderItems (single SaveChanges — EF tracks graph)
    3. BasketService.DeleteBasketAsync(basketId)
         → IRepository<Basket>.DeleteAsync()
             → EF Core DELETE BasketItems (CASCADE) + DELETE Baskets
    4. Redirect → /basket/success
```

**Key data invariant:** UnitPrice on OrderItem is copied from BasketItem.UnitPrice (price when item was added to basket), NOT the current CatalogItem.Price. Price changes after adding to basket do not affect order total.

---

## Flow 4 — Admin: Create/Edit/Delete Catalog Item (BlazorAdmin → PublicApi)

```
BlazorAdmin (WASM)
  → Authenticates via POST /api/authenticate (returns JWT)
  → CachedCatalogItemServiceDecorator.Create/Edit/Delete(...)
      [checks LocalStorage 'items' cache — 1-min TTL]
      → CatalogItemService.Create/Edit/Delete(...)
          → HttpService.HttpPost/Put/Delete("catalog-items", ...)
              → PublicApi CreateCatalogItemEndpoint / UpdateCatalogItemEndpoint / DeleteCatalogItemEndpoint
                  [Authorize(Roles="Administrators", JWT Bearer)]
                  → IRepository<CatalogItem>.AddAsync/UpdateAsync/DeleteAsync()
                      → EF Core INSERT/UPDATE/DELETE Catalog
      → RefreshLocalStorageList() — removes LocalStorage 'items' key and re-fetches from API

NOTE: Web MVC IMemoryCache (30s sliding) is NOT invalidated by PublicApi writes.
Catalog changes will appear in Web MVC storefront within 30 seconds maximum.
```

---

## Flow 5 — Anonymous to Authenticated Basket Transfer (on login)

```
User logs in (POST /account/login)
  → SignInManager.PasswordSignInAsync()
  → BasketService.TransferBasketAsync(anonymousGUID, userEmail)
      → IRepository<Basket>.FirstOrDefaultAsync(BasketWithItemsSpecification(anonymousGUID))
          [NULL] → return (nothing to transfer)
          [FOUND] →
      → IRepository<Basket>.FirstOrDefaultAsync(BasketWithItemsSpecification(userEmail))
          [NULL]  → new Basket(userEmail); IRepository<Basket>.AddAsync(userBasket)
          [FOUND] → use existing user basket
      → foreach item in anonymousBasket:
           → userBasket.AddItem(item.CatalogItemId, item.UnitPrice, item.Quantity)
      → IRepository<Basket>.UpdateAsync(userBasket)   [SaveChanges #1]
      → IRepository<Basket>.DeleteAsync(anonymousBasket) [SaveChanges #2, cascades BasketItems]

⚠️ NON-ATOMIC: Two separate SaveChanges calls. If DeleteAsync fails after UpdateAsync succeeds,
   both anonymous and user baskets will contain the same items.
```

---

## Flow 6 — JWT Authentication (PublicApi / BlazorAdmin)

```
BlazorAdmin POST /api/authenticate { username, password }
  → AuthenticateEndpoint
      → SignInManager.PasswordSignInAsync()
      → UserManager.GetRolesAsync(user)   [reads AspNetUserRoles + AspNetRoles]
      → Builds JWT (HS256, key: AuthorizationConstants.JWT_SECRET_KEY — hardcoded)
      → Returns { token, username, isAuthenticated, claims[] }

BlazorAdmin:
  → Stores Bearer token in HttpClient.DefaultRequestHeaders.Authorization (in-memory)
  → CustomAuthStateProvider caches user state for 60 seconds (hardcoded — TODO: make configurable)
```

---

## Flow 7 — Basket Item Count (DB-side aggregation)

```
Web MVC basket icon counter
  → BasketQueryService.CountTotalBasketItems(username)
      → EF Core LINQ (runs as SQL, not in-memory):
         SELECT SUM(bi.Quantity)
         FROM Baskets b
         JOIN BasketItems bi ON bi.BasketId = b.Id
         WHERE b.BuyerId = @username
```

---

## Data Mutation Summary

| Operation | Tables Written | SaveChanges Calls | Atomic? |
|-----------|---------------|-------------------|---------|
| Add to basket | Baskets, BasketItems | 1 | ✅ Yes |
| Set basket quantities | BasketItems | 1 | ✅ Yes |
| Delete basket | BasketItems (CASCADE), Baskets | 1 | ✅ Yes |
| Create order | Orders, OrderItems | 1 (EF tracks full graph) | ✅ Yes |
| Transfer basket (anonymous → user) | Baskets, BasketItems | 2 | ❌ No — non-atomic |
| Create catalog item | Catalog | 2 (add + update pictureUri) | ⚠️ Two calls |
| Update catalog item | Catalog | 1 | ✅ Yes |
| Delete catalog item | Catalog | 1 | ✅ Yes |

**⚠️ Non-atomic basket transfer:** If the `DeleteAsync(anonymousBasket)` call fails after `UpdateAsync(userBasket)` succeeds, both baskets will contain the same items.

**⚠️ Create catalog item — two SaveChanges:** `CreateCatalogItemEndpoint` calls `AddAsync` to get the Id, then `UpdateAsync` to set the placeholder PictureUri. If the second call fails, a catalog item exists with no PictureUri.

---

## Agent 2 Review Changes

```json
[
  {
    "change_id": "RC-12",
    "type": "ENRICHED",
    "finding_id": "data-flow-map.md — Flow 5 basket transfer",
    "what": "Test confirms that when both anonymous and user baskets have the same CatalogItemId, Transfer accumulates quantities (not deduplicates). Anon qty=1 + user qty=4 → user qty=5 after transfer.",
    "evidence_source": "Phase 1 test review",
    "evidence_detail": "tests/UnitTests/ApplicationCore/Services/BasketServiceTests/TransferBasket.cs:68-71 — TransferAnonymousBasketItemsWhilePreservingExistingUserBasketItems.",
    "confidence_before": 0.9,
    "confidence_after": 1.0,
    "phase_found": "Phase 1 test review"
  }
]
```
