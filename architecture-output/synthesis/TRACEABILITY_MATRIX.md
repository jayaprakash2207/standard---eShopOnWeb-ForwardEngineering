# Traceability Matrix — eShopOnWeb

> Columns: Capability → Process → Entity/Aggregate → Service → API → Database → Confidence
> Each row = one business capability traced end-to-end through every architecture layer.

---

## Reading Guide

- **ASSUMED** = behavior inferred from service interfaces; source not extracted
- **STUB** = code exists but does not function
- **DEAD** = code exists but is not persisted or called
- Confidence is the lowest-confidence link in the chain (weakest-link rule)

---

## Capability Traceability Rows

### CAP-001 — Product Catalog Management

| Dimension | Value | Confidence |
|-----------|-------|------------|
| **Capability** | Product Catalog Management | HIGH |
| **Process** | PROC-008: Catalog Administration (Create/Update/Delete) | HIGH |
| **Entities** | CatalogItem (ENT-001), CatalogBrand (ENT-002), CatalogType (ENT-003) | HIGH |
| **Domain Service** | UriComposer (SVC-003) for image URI composition | HIGH |
| **Application Service** | CatalogItemService/BlazorAdmin (SVC-011), CachedCatalogItemServiceDecorator (SVC-012) | HIGH |
| **API Endpoints** | POST /api/catalog-items (API-003), PUT /api/catalog-items (API-004), DELETE /api/catalog-items/{id} (API-005), GET /api/catalog-items (API-001), GET /api/catalog-items/{id} (API-002), GET /api/catalog-brands (API-006), GET /api/catalog-types (API-007) | HIGH |
| **Database** | CatalogDB: CatalogItems (HiLo), CatalogBrands, CatalogTypes | HIGH |
| **Auth Gate** | JWT Bearer + Administrators role on writes; anonymous reads | HIGH |
| **UI** | BlazorAdmin (DEP-001 hosted) — List/Create/Edit/Delete pages | HIGH |
| **Business Rules** | BR-01 to BR-12 (name/price/brand/type validation); BR-07 (admin-only writes) | HIGH |
| **Overall Confidence** | **HIGH** |

---

### CAP-002 — Shopping Basket Management

| Dimension | Value | Confidence |
|-----------|-------|------------|
| **Capability** | Shopping Basket Management | HIGH |
| **Process** | PROC-002 (Add Item), PROC-003 (Update Quantities) | HIGH |
| **Entities** | Basket (ENT-004), BasketItem (ENT-005), CatalogItem (ENT-001, ref by ID) | HIGH |
| **Domain Service** | BasketService (SVC-001): AddItemToBasket, SetQuantities, DeleteBasketAsync | HIGH |
| **Application Service** | BasketQueryService (SVC-006): CountTotalBasketItems (bypasses IRepository) | HIGH |
| **API Endpoints** | No dedicated REST API for basket — served via Web MVC pages (ASSUMED) | ASSUMED |
| **Database** | CatalogDB: Baskets, BasketItems | HIGH |
| **Auth Gate** | None for anonymous basket; Cookie auth for authenticated basket operations | HIGH |
| **UI** | Web MVC basket pages (ASSUMED — source not extracted) | ASSUMED |
| **Business Rules** | BR-13 (auto-create), BR-14 (merge duplicate), BR-15 (no negative qty), BR-16 (remove zero-qty) | HIGH |
| **Overall Confidence** | **MEDIUM** (Web basket pages ASSUMED) |

---

### CAP-003 — Order Placement & History

| Dimension | Value | Confidence |
|-----------|-------|------------|
| **Capability** | Order Placement & History | HIGH |
| **Process** | PROC-005: Place Order at Checkout | HIGH |
| **Entities** | Order (ENT-006), OrderItem (ENT-007), Address (ENT-008 VO), CatalogItemOrdered (ENT-009 VO), Basket (ENT-004, read), CatalogItem (ENT-001, snapshot source) | HIGH |
| **Domain Service** | OrderService (SVC-002): CreateOrderAsync(basketId, address); reads IRepository\<Basket\> + IRepository\<CatalogItem\> | HIGH |
| **Application Service** | GetMyOrdersHandler (SVC-010, MediatR), GetOrderDetailsHandler | HIGH |
| **API Endpoints** | No REST API for orders — Web MVC only (ASSUMED for display); order creation is server-side | ASSUMED |
| **Database** | CatalogDB: Orders, OrderItems (with embedded Address + CatalogItemOrdered) | HIGH |
| **Auth Gate** | [Authorize] on checkout page — registered customers only | HIGH |
| **UI** | Web MVC checkout page, order history page (ASSUMED — source not extracted) | ASSUMED |
| **Business Rules** | BR-20 (empty basket blocks), BR-21 (product snapshot), BR-22 (price frozen), BR-23 (total calc), BR-24 (buyer required), BR-25 (valid line items), BR-26 (basket NOT cleared) | HIGH |
| **Gap** | Order has no status field — no fulfilment workflow (Pain Point PP-01) | HIGH |
| **Overall Confidence** | **MEDIUM** (Web checkout/history pages ASSUMED) |

---

### CAP-004 — Customer Identity & Authentication

| Dimension | Value | Confidence |
|-----------|-------|------------|
| **Capability** | Customer Identity & Authentication | HIGH |
| **Process** | PROC-006: API Authentication and Token Issuance; PROC-007: Customer Registration | HIGH |
| **Entities** | ApplicationUser (ENT-012); Buyer (ENT-010 — DEAD CODE) | HIGH (ApplicationUser); LOW (Buyer) |
| **Domain Service** | IdentityTokenClaimService (SVC-004): GetTokenAsync(userName) | HIGH |
| **Application Service** | ASP.NET Core Identity (UserManager, SignInManager, RoleManager) | HIGH |
| **API Endpoints** | POST /api/authenticate (API-008); Web: Login/Register/ConfirmEmail Razor pages | HIGH |
| **Database** | IdentityDB: AspNetUsers, AspNetRoles, AspNetUserRoles | HIGH |
| **Auth Gate** | ASP.NET Identity validates credentials; JWT issued on success | HIGH |
| **UI** | Web MVC Login/Register/ConfirmEmail pages (confirmed source) | HIGH |
| **Business Rules** | BR-27 (7-day token), BR-28 (user must exist), BR-29 (roles in claims), BR-30 (lockout), BR-31 (non-persistent API login), BR-32 (seeded accounts), BR-33 (hardcoded credentials — CRITICAL) | HIGH |
| **Gap** | EmailSender stub breaks registration confirmation (BR-34); Buyer not persisted | HIGH |
| **Overall Confidence** | **HIGH** |

---

### CAP-005 — Admin Catalog Portal

| Dimension | Value | Confidence |
|-----------|-------|------------|
| **Capability** | Admin Catalog Portal | HIGH |
| **Process** | PROC-008: Catalog Administration | HIGH |
| **Entities** | CatalogItem DTO (BlazorShared), CatalogBrand DTO, CatalogType DTO | HIGH |
| **Domain Service** | (Mediated through PublicApi — no direct domain service call from BlazorAdmin) | HIGH |
| **Application Service** | CatalogItemService (SVC-011), CachedCatalogItemServiceDecorator (SVC-012), CatalogLookupDataService, HttpService (SVC-015) | HIGH |
| **API Endpoints** | All 8 PublicApi catalog endpoints (API-001 through API-008) | HIGH |
| **Database** | CatalogDB (via PublicApi → EfRepository) | HIGH |
| **Auth Gate** | JWT obtained from Web /User endpoint; Bearer token on mutating calls | HIGH |
| **UI** | BlazorAdmin WASM SPA — List/Create/Edit/Delete/Details pages | HIGH |
| **Business Rules** | BR-41 (10 items/page), BR-42 (1-min cache), BR-43 (immediate cache invalidation on write), BR-44 (3s toast dismiss) | HIGH |
| **Overall Confidence** | **HIGH** |

---

### CAP-006 — Customer Storefront Browsing

| Dimension | Value | Confidence |
|-----------|-------|------------|
| **Capability** | Customer Storefront Browsing | ASSUMED |
| **Process** | PROC-001: Browse and Filter Products | ASSUMED |
| **Entities** | CatalogItem (ENT-001), CatalogBrand (ENT-002), CatalogType (ENT-003) | HIGH |
| **Domain Service** | UriComposer (SVC-003) for image URIs | HIGH |
| **Application Service** | CachedCatalogViewModelService (SVC-009): 30s server-side cache | HIGH |
| **API Endpoints** | None — served directly via Web MVC Razor Pages | ASSUMED |
| **Database** | CatalogDB: CatalogItems, CatalogBrands, CatalogTypes | HIGH |
| **Auth Gate** | None — anonymous browsing permitted | HIGH |
| **UI** | Web MVC catalog index/detail pages (ASSUMED — source not extracted) | ASSUMED |
| **Business Rules** | BR-07 (reads anonymous), BR-10 (page size 0 = all), BR-11 (1s delay on API list — not on Web catalog) | MEDIUM |
| **Overall Confidence** | **ASSUMED** |

---

### CAP-007 — Customer Account Registration

| Dimension | Value | Confidence |
|-----------|-------|------------|
| **Capability** | Customer Account Registration | HIGH |
| **Process** | PROC-007: Customer Registration with Email Confirmation | HIGH |
| **Entities** | ApplicationUser (ENT-012) | HIGH |
| **Domain Service** | (None — handled by Identity framework) | HIGH |
| **Application Service** | UserManager.CreateAsync, EmailConfirmation token generation | HIGH |
| **API Endpoints** | Web: Register.cshtml.cs OnPostAsync (no REST API) | HIGH |
| **Database** | IdentityDB: AspNetUsers | HIGH |
| **Auth Gate** | None — registration is public | HIGH |
| **UI** | Web MVC Register page | HIGH |
| **Business Rules** | BR-34 (email confirmation — **BROKEN due to stub**); duplicate email rejected | HIGH |
| **Critical Gap** | Email confirmation permanently blocked; no workaround in current code | HIGH |
| **Overall Confidence** | **HIGH** (capability exists and partially works; confirmation broken) |

---

### CAP-008 — Anonymous Basket & Session Transfer

| Dimension | Value | Confidence |
|-----------|-------|------------|
| **Capability** | Anonymous Basket & Session Transfer | HIGH |
| **Process** | PROC-004: Transfer Anonymous Basket on Login | HIGH |
| **Entities** | Basket (ENT-004), BasketItem (ENT-005) | HIGH |
| **Domain Service** | BasketService.TransferBasketAsync(anonymousId, userName) (SVC-001) | HIGH |
| **Application Service** | Login.cshtml.cs TransferAnonymousBasketToUserAsync reads BASKET_COOKIENAME cookie | HIGH |
| **API Endpoints** | None — triggered by Web login form post | HIGH |
| **Database** | CatalogDB: Baskets, BasketItems | HIGH |
| **Auth Gate** | Cookie auth — triggered on successful login | HIGH |
| **UI** | Web MVC Login page | HIGH |
| **Business Rules** | BR-17 (merge on login), BR-18 (delete anon basket + cookie), BR-19 (no-op if no anon basket), BR-45 (read cookie), BR-46 (delete cookie) | HIGH |
| **Data Risk** | TransferBasketAsync has 3 separate SaveChanges (non-atomic — DQ-002) | HIGH |
| **Overall Confidence** | **HIGH** |

---

## Coverage Summary

| Capability | Traced? | Weakest Link | Priority Gap |
|------------|---------|--------------|--------------|
| CAP-001 Product Catalog Management | Full | HIGH | None |
| CAP-002 Shopping Basket Management | Partial | ASSUMED (Web pages) | Extract Web basket pages |
| CAP-003 Order Placement & History | Partial | ASSUMED (Web pages) | Extract Web checkout/history pages |
| CAP-004 Customer Identity & Auth | Full | HIGH | EmailSender stub |
| CAP-005 Admin Catalog Portal | Full | HIGH | None |
| CAP-006 Customer Storefront Browsing | Minimal | ASSUMED | Extract Web browse pages |
| CAP-007 Customer Account Registration | Full | HIGH | Fix EmailSender |
| CAP-008 Anonymous Basket Transfer | Full | HIGH | None |

---

## Cross-Capability Dependency Map

```
CAP-006 (Browse) ──────────────────────────────► CAP-002 (Basket)
                                                        │
                                               CAP-007 (Register)
                                               CAP-004 (Login/Auth)
                                                        │
                                                        ▼
                                               CAP-008 (Basket Transfer)
                                                        │
                                                        ▼
                                               CAP-003 (Order Placement)
                                                        │
                                               CAP-001 (Catalog) ─── CAP-005 (Admin Portal)
```

Every customer purchase journey traverses: Browse → Basket → (Register+Login) → Transfer → Checkout → Order.
All paths depend on CAP-001 (catalog data source) and CAP-004 (identity).
