=== DOCUMENT: 09_DATA_FLOW_DIAGRAM.md ===

# Data Flow Diagram — eShopOnWeb

---

## DFD Level 0 — System Context

```
                    ┌─────────────────────────────────────┐
                    │         eShopOnWeb System           │
                    │                                     │
 [Anonymous Visitor]│──── Browse/Basket requests ────────►│
                    │◄─── Product listings, basket state──│
                    │                                     │
 [Registered Customer]──── Login, Checkout, Orders ──────►│
                    │◄─── Session cookie, order confirm───│
                    │                                     │
 [Administrator]────│──── JWT + Catalog mutations ────────►│
                    │◄─── Catalog data, admin state ──────│
                    │                                     │
                    │──── Product reads/writes ───────────►[CatalogDB / Azure SQL]
                    │◄─── Entity data ────────────────────│
                    │                                     │
                    │──── Identity reads/writes ──────────►[IdentityDB / Azure SQL]
                    │◄─── User/role data ─────────────────│
                    │                                     │
                    │──── Key Vault reads (startup) ──────►[Azure Key Vault]
                    │◄─── Connection strings, secrets ────│
                    │                                     │
                    │──── Email send (STUB — no-op) ──────►[Email Provider]
                    └─────────────────────────────────────┘
```

---

## DFD Level 1 — Internal Data Flows

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            Web (eshopwebmvc)                                │
│                                                                             │
│  [Login.cshtml]                                                             │
│    │── credentials ──► SignInManager.PasswordSignInAsync()                  │
│    │                    └──► IdentityDB read/write                          │
│    │── on success ──► TransferAnonymousBasketToUserAsync()                  │
│    │                    └──► BasketService.TransferBasketAsync()            │
│    │                           └──► CatalogDB: Baskets, BasketItems (R/W)  │
│    │                                                                        │
│  [Register.cshtml]                                                          │
│    │── new user ──► UserManager.CreateAsync() ──► IdentityDB write         │
│    │── token gen ──► EmailSender.SendEmailAsync() ──► STUB (no-op)         │
│    │                                                                        │
│  [Catalog Pages] (ASSUMED)                                                  │
│    │── page request ──► CachedCatalogViewModelService (30s IMemoryCache)    │
│    │                    └──► EfRepository<CatalogItem> ──► CatalogDB read   │
│    │                                                                        │
│  [Basket Pages] (ASSUMED)                                                   │
│    │── add/update ──► BasketService ──► EfRepository<Basket> ──► CatalogDB │
│    │── count query ──► BasketQueryService.CountTotalBasketItems()           │
│    │                    └──► CatalogDB direct LINQ (bypasses repository)    │
│    │                                                                        │
│  [Checkout Page] (ASSUMED)                                                  │
│    │── submit ──► OrderService.CreateOrderAsync(basketId, address)          │
│    │              ├──► IRepository<Basket> ──► CatalogDB read               │
│    │              ├──► IRepository<CatalogItem> ──► CatalogDB read          │
│    │              └──► IRepository<Order>.AddAsync() ──► CatalogDB write    │
│    │                                                                        │
│  [/User endpoint]                                                           │
│    │── GET ──► UserManager ──► IdentityDB read                              │
│    │◄── UserInfo { Token, Claims, IsAuthenticated }                         │
│                                                                             │
│  [MediatR Queries — Order History]                                          │
│    │── GetMyOrders ──► CustomerOrdersWithItemsSpecification                 │
│    │                    └──► EfRepository<Order> ──► CatalogDB read         │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                          PublicApi (eshoppublicapi)                         │
│                                                                             │
│  POST /api/authenticate                                                     │
│    │── credentials ──► SignInManager ──► IdentityDB read                    │
│    │── on success ──► IdentityTokenClaimService.GetTokenAsync()             │
│    │                    ├──► UserManager.GetRolesAsync() ──► IdentityDB     │
│    │                    └──► JwtSecurityTokenHandler.CreateToken()          │
│    │◄── JWT token (7-day, HMAC-SHA256)                                      │
│                                                                             │
│  GET /api/catalog-items (paged)                                             │
│    │── request ──► [1s artificial delay — TD-07 REMOVE]                    │
│    │── filter ──► CatalogFilterPaginatedSpecification                       │
│    │               └──► EfRepository<CatalogItem> ──► CatalogDB read       │
│    │── map ──► AutoMapper: CatalogItem → CatalogItemDto                    │
│    │◄── PagedCatalogItemResponse                                            │
│                                                                             │
│  POST/PUT /api/catalog-items [JWT Administrators required]                  │
│    │── validate ──► FluentValidation rules                                   │
│    │── mutate ──► IRepository<CatalogItem>.AddAsync/UpdateAsync()           │
│    │               └──► CatalogDB write                                     │
│                                                                             │
│  DELETE /api/catalog-items/{id} [JWT Administrators required]               │
│    │── find ──► IRepository<CatalogItem>.GetByIdAsync()                     │
│    │── delete ──► IRepository<CatalogItem>.DeleteAsync()                    │
│    │               └──► CatalogDB write                                     │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         BlazorAdmin (WASM in browser)                      │
│                                                                             │
│  Startup:                                                                   │
│    │── GET /User ──► Web /User endpoint ──► JWT token received              │
│    │── token stored in memory; attached as Bearer on all PublicApi calls    │
│    │── repeated every 60s (UserCacheRefreshInterval)                        │
│                                                                             │
│  Catalog List Page:                                                         │
│    │── CachedCatalogItemServiceDecorator: check localStorage (60s TTL)      │
│    │── cache miss ──► HttpService.HttpGet ──► GET /api/catalog-items        │
│    │── parallel: GET /api/catalog-brands + GET /api/catalog-types           │
│    │── join results in-memory; enrich items with brand/type names           │
│    │── store in localStorage with DateCreated timestamp                     │
│                                                                             │
│  Catalog Mutation (Create/Edit/Delete):                                     │
│    │── HttpService.HttpPost/HttpPut/HttpDelete ──► PublicApi (JWT Bearer)   │
│    │── on response: RefreshLocalStorageList() ──► invalidate + re-fetch     │
│    │── ToastService.ShowToast() ──► 3-second UI notification                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## DFD Level 2 — Order Creation Data Flow (Detailed)

```
Customer [authenticated, cookie session]
    │
    │  POST /checkout  {shippingAddress: HARDCODED — TD-09}
    ▼
CheckoutModel.OnPost(BasketService, OrderService)
    │
    ├──[1] BasketService.GetOrCreateBasketForUser(userName)
    │       └──► EfRepository<Basket>.FirstOrDefaultAsync(BasketWithItemsSpecification)
    │               └──► CatalogDB: SELECT * FROM Baskets WHERE BuyerId=@user
    │                              JOIN BasketItems ON BasketId
    │
    ├──[2] OrderService.CreateOrderAsync(basket.Id, shippingAddress)
    │       │
    │       ├──[2a] Guard.Against.EmptyBasketOnCheckout(basket.Items)
    │       │        └── Throws if count == 0 ──► HTTP 400
    │       │
    │       ├──[2b] IRepository<CatalogItem>.ListAsync(CatalogItemsSpecification([ids]))
    │       │        └──► CatalogDB: SELECT * FROM CatalogItems WHERE Id IN @ids
    │       │
    │       ├──[2c] For each BasketItem:
    │       │        catalogItem = catalogItems.First(x => x.Id == item.CatalogItemId)
    │       │        orderItem = new OrderItem(
    │       │            new CatalogItemOrdered(catalogItem.Id, catalogItem.Name, catalogItem.PictureUri),
    │       │            item.UnitPrice,  ← from BasketItem, NOT from catalogItem.Price
    │       │            item.Quantity
    │       │        )
    │       │
    │       └──[2d] IRepository<Order>.AddAsync(new Order(buyerId, address, orderItems))
    │                └──► CatalogDB: INSERT INTO Orders; INSERT INTO OrderItems
    │
    └──[3] Basket NOT cleared (BR-26)
            [Caller must call BasketService.DeleteBasketAsync if desired]
```

---

## Data Retention and Lifecycle

| Data Store | Retention Policy | Cleanup Mechanism | Risk |
|------------|-----------------|-------------------|------|
| CatalogDB — Baskets (anonymous) | **Indefinite — no expiry** | None (manual only) | DB bloat over time (PP-08) |
| CatalogDB — Baskets (authenticated) | **Indefinite** | None | Persist after order (BR-26) |
| CatalogDB — Orders | **Indefinite** | None | Correct — permanent historical record |
| IdentityDB — Users | **Indefinite** | Admin manual delete | Unconfirmed accounts accumulate if email broken |
| Azure App Service HTTP Logs | 1 day / 35 MB | Auto-rotate (NFR-09) | Short retention — limited forensics |
| Token revocation cache (IMemoryCache) | 60 minutes (matching cookie validity) | Automatic expiry | Non-persistent — cleared on app restart |
