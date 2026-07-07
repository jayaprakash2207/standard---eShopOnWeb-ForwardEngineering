=== DOCUMENT: 19_FRONTEND_ARCHITECTURE.md ===

# Frontend Architecture — eShopOnWeb

---

## 1. Frontend Surfaces

eShopOnWeb has three distinct frontend surfaces that share the same domain core and HTTP session, but use different rendering technologies and authentication mechanisms:

| Surface | Technology | Auth Mechanism | Deployed With | Users | Confidence |
|---------|-----------|----------------|--------------|-------|-----------|
| Web (MVC + Razor Pages) | ASP.NET Core MVC, Razor Pages, Bootstrap 3.4.1 | Cookie (EshopIdentifier) | eshopwebmvc | Customers | HIGH |
| BlazorAdmin | Blazor WebAssembly (WASM) | JWT Bearer (relay from Web /User) | eshopwebmvc (hosted) | Administrators | HIGH |
| PublicApi Swagger UI | Swashbuckle — browser-rendered OpenAPI | JWT Bearer (manual entry) | eshoppublicapi | Developers / Admins | HIGH |

---

## 2. Web Application (MVC + Razor Pages)

### 2.1 Rendering Architecture

```
Customer Browser
    │
    │  HTTP Request (Cookie: EshopIdentifier)
    ▼
ASP.NET Core Web Application (eshopwebmvc)
    │
    ├── Areas/Identity/Pages/Account/ (Razor Pages — scaffold)
    │       Login.cshtml / Register.cshtml / ConfirmEmail.cshtml
    │
    ├── Pages/ (Razor Pages — application)
    │       Basket/Checkout.cshtml     ← INFERRED (MIS-004, MIS-007)
    │       Catalog/Index.cshtml       ← INFERRED (MIS-004)
    │       Orders/MyOrders.cshtml     ← INFERRED (MIS-004)
    │
    ├── Controllers/
    │       UserController.cs          ← GET /User (BlazorAdmin auth relay)
    │
    └── Server-side rendered HTML → Browser
            Bootstrap 3.4.1 (⚠️ EOL)
            jQuery 3.6.3
            jquery-validation 1.19.5
            jquery-validation-unobtrusive 4.0.0
            toastr.js 2.1.4
```

### 2.2 Confirmed Web Pages

| Page | Path | Auth Required | Confirmed | Notes |
|------|------|---------------|-----------|-------|
| Login | /Account/Login | No | HIGH | basket transfer on login confirmed |
| Register | /Account/Register | No | HIGH | email confirmation flow confirmed |
| ConfirmEmail | /Account/ConfirmEmail | No | HIGH | ConfirmEmailAsync on GET |
| Checkout | /Basket/Checkout | ✅ [Authorize] | INFERRED | address hardcoded — TD-09 |
| Catalog browse | /Catalog/Index (assumed) | No | INFERRED | MIS-004 |
| Basket view | /Basket/Index (assumed) | No (anon supported) | INFERRED | MIS-004 |
| Order history | /Orders/MyOrders (assumed) | ✅ [Authorize] | INFERRED | MIS-004 |

### 2.3 View Model Services

| Service | Interface | Implementation | Notes |
|---------|-----------|---------------|-------|
| ICatalogViewModelService | ICatalogViewModelService | CatalogViewModelService | INFERRED — builds page view models |
| ICachedCatalogViewModelService | (same interface) | CachedCatalogViewModelService | CONFIRMED; 30s sliding IMemoryCache |

### 2.4 Client-Side Libraries (delivered via libman.json)

| Library | Version | Status |
|---------|---------|--------|
| Bootstrap | 3.4.1 | ⚠️ EOL July 2019 (TD-13) — must upgrade |
| jQuery | 3.6.3 | Active |
| jquery-validation | 1.19.5 | Active |
| jquery-validation-unobtrusive | 4.0.0 | Active |
| toastr.js | 2.1.4 | Active |
| aspnet-signalr | 1.0.27 | ⚠️ Dead — no SignalR hub (TD-16) — remove |

### 2.5 Web Layout Structure (INFERRED)

```
_Layout.cshtml
    ├── Header: site logo, nav links, basket count, user auth state
    ├── Main: @RenderBody()
    └── Footer: site info

_ValidationScriptsPartial.cshtml
    └── jquery-validation + jquery-validation-unobtrusive scripts

_LoginPartial.cshtml
    └── Login / Register links when anonymous
    └── Username + Logout when authenticated
```

---

## 3. BlazorAdmin (Blazor WebAssembly)

### 3.1 Architecture

BlazorAdmin is a Blazor WASM application hosted inside the `eshopwebmvc` ASP.NET Core app as a `RazorClassLibrary` project. It is NOT a standalone Blazor-hosted app — it runs in the browser as WebAssembly but is served through the Web application's pipeline.

```
Browser (WASM runtime)
    │
    │  loads from: /BlazorAdmin (served by eshopwebmvc)
    ▼
BlazorAdmin WASM Application
    │
    ├── CustomAuthStateProvider
    │       Polls GET /User every 60s
    │       Sets ClaimsPrincipal from token
    │
    ├── CatalogItemService
    │       HTTP calls to eshoppublicapi
    │       Authorization: Bearer {token}
    │
    ├── CachedCatalogItemServiceDecorator
    │       Wraps CatalogItemService
    │       Blazored.LocalStorage cache: 60s TTL
    │       Immediate cache invalidation on write
    │
    └── Pages/
            CatalogItemPage/
                List.razor        → paginated item list (10 items/page)
                Create.razor      → create item modal
                Edit.razor        → edit item modal
                Delete.razor      → delete confirmation modal
```

### 3.2 Authentication Flow

```
1. Admin navigates to /BlazorAdmin
2. CustomAuthStateProvider initializes
3. GET /User → UserController.GetCurrentUser()
       Returns: { IsAuthenticated, Token, Claims }
4. If not authenticated: redirect to /Account/Login (Web)
5. After Web Cookie login (via web browser):
       Admin must re-authenticate via BlazorAdmin UI
       POST /api/authenticate {username, password} → JWT token
6. Token stored in-memory (BlazorAdmin state)
7. All HttpClient calls: Authorization: Bearer {token}
8. Every 60s: re-poll GET /User to validate session
```

**Gap:** The JWT Bearer token obtained at step 5 expires in 7 days. The cookie session expires in 60 minutes. If the cookie expires, GET /User returns `IsAuthenticated=false` and BlazorAdmin clears the token — effective maximum session = 60 minutes per login.

### 3.3 Service Layer

| Service | Confirmed | Key Behavior |
|---------|-----------|-------------|
| CatalogItemService | HIGH | CRUD operations via HttpClient; parallel async fan-out for List (ART-048) |
| CachedCatalogItemServiceDecorator | HIGH | Decorator; 60s LocalStorage cache; invalidates on Create/Edit/Delete |
| CustomAuthStateProvider | HIGH | 60s poll; Bearer token attachment; NotifyAuthenticationStateChanged on change |
| HttpService | INFERRED | Generic HTTP wrapper (Get/Post/Put/Delete); no timeout (MIS-011) |
| ToastService | HIGH | 3s dismiss delay confirmed |

### 3.4 Component Catalog (Confirmed)

| Component | Path | Confirmed | Notes |
|-----------|------|-----------|-------|
| List.razor | Pages/CatalogItemPage/List.razor | HIGH | 10 items per page; pagination controls |
| Create.razor / CreateModal | Pages/CatalogItemPage/ | HIGH | Form fields: Name, Description, Price, PictureUri, Brand, Type |
| Edit.razor / EditModal | Pages/CatalogItemPage/ | HIGH | Same fields as Create |
| Delete.razor / DeleteModal | Pages/CatalogItemPage/ | HIGH | Confirmation dialog before delete |
| NavMenu.razor | Shared/NavMenu.razor | INFERRED | Navigation sidebar |
| LoginDisplay.razor | Shared/LoginDisplay.razor | INFERRED | Auth state display |

### 3.5 BlazorShared Class Library

Shared between Web and BlazorAdmin. Contains DTOs used across both surfaces:

| Type | Kind | Purpose | Confidence |
|------|------|---------|-----------|
| CatalogItem | DTO class | BlazorAdmin catalog item view model | HIGH |
| CatalogBrand | DTO class | Brand selector | HIGH |
| CatalogType | DTO class | Type selector | HIGH |
| PaginationInfoViewModel | DTO class | Page controls | HIGH |
| CreateCatalogItemRequest | DTO | Create API payload | HIGH |
| UpdateCatalogItemRequest | DTO | Update API payload | HIGH |

> Note: `BlazorShared.Models.CatalogItem` is a DTO — distinct from `ApplicationCore.Entities.CatalogItem` aggregate root. Same name, different namespace, different purpose. See DISC-001.

---

## 4. PublicApi Swagger UI

Swashbuckle provides an auto-generated API documentation UI available at `/swagger`.

| Attribute | Value | Confidence |
|-----------|-------|-----------|
| Path | /swagger/index.html | HIGH |
| API Title | "My API V1" | HIGH |
| API Version | "v1" | HIGH |
| Security Scheme | JWT Bearer (Authorization: Bearer {token}) | HIGH |
| Availability | Always on (development + production) | HIGH |

---

## 5. Frontend Routing Summary

### Web Application Routes (confirmed + inferred)

| Route | Handler | Auth | Confidence |
|-------|---------|------|-----------|
| GET /Account/Login | Pages/Account/Login.cshtml | Anonymous | HIGH |
| POST /Account/Login | Pages/Account/Login.cshtml | Anonymous | HIGH |
| GET /Account/Register | Pages/Account/Register.cshtml | Anonymous | HIGH |
| POST /Account/Register | Pages/Account/Register.cshtml | Anonymous | HIGH |
| GET /Account/ConfirmEmail | Pages/Account/ConfirmEmail.cshtml | Anonymous | HIGH |
| GET /Basket/Checkout | Pages/Basket/Checkout.cshtml | Authorized | INFERRED |
| POST /Basket/Checkout | Pages/Basket/Checkout.cshtml | Authorized | INFERRED |
| GET /User | Controllers/UserController.cs | Authorized | HIGH |
| POST /User/Logout | Controllers/UserController.cs | Authorized | HIGH |
| GET /health | Health check middleware | Anonymous | HIGH |
| GET /BlazorAdmin/* | Blazor WASM SPA | Varies | HIGH |
| GET /swagger | Swashbuckle UI (PublicApi only) | Anonymous | HIGH |

---

## 6. Frontend Gaps and Generation Instructions

### Gap 1: Catalog Browse Page (MIS-004)

- **What is INFERRED:** The catalog list page renders CatalogItems with filter dropdowns for Brand and Type; uses CachedCatalogViewModelService; pagination with configurable page size.
- **What is MISSING:** Exact Razor template, page model bindings, URL query parameters.
- **Generation instruction:** Generate based on CatalogFilterPaginatedSpecification and CatalogViewModelService interface. Expose: `?brandId=&typeId=&page=&pageSize=10`.

### Gap 2: Basket Page (MIS-004)

- **What is INFERRED:** Lists basket items with quantities; allows quantity update; allows item removal; shows total. Supports anonymous users.
- **What is MISSING:** Exact form structure, AJAX vs full-page submit.
- **Generation instruction:** Use BasketService.SetQuantities() for update; BasketService.DeleteBasketAsync() or RemoveEmptyItems() for removal. Anonymous basket cookie: `BASKET_COOKIENAME`.

### Gap 3: Checkout Page (MIS-007)

- **What is CONFIRMED:** `Checkout.cshtml.cs:95` — 10-year anonymous basket cookie creation. `CheckoutPage.OnPostAsync` calls `IOrderService.CreateOrderAsync`.
- **What is MISSING:** Shipping address form fields.
- **What is HARDCODED (must replace):** `new Address("123 Main St.", "Kent", "OH", "United States", "44240")` (TD-09)
- **Generation instruction:** Add form fields: Street (max 180), City (max 100), State (max 60), Country (max 90), ZipCode (max 18). Bind to Address value object. Apply client-side validation.

### Gap 4: Order History Page (MIS-004)

- **What is INFERRED:** Lists authenticated user's past orders. Shows OrderDate, Total, and order items with snapshots.
- **What is MISSING:** Exact Razor template; pagination.
- **Generation instruction:** Use GetMyOrdersHandler (MediatR query) returning IEnumerable<OrderViewModel>. Route: /Orders/MyOrders. Requires [Authorize].

---

## 7. Frontend Technology Decisions (Confirmed from Source)

| Decision | Choice | Evidence |
|----------|--------|---------|
| MVC rendering | Server-side Razor Pages + MVC | ASP.NET Core MVC confirmed |
| Admin SPA | Blazor WASM (hosted, not standalone) | BlazorAdmin project; RazorClassLibrary |
| CSS framework | Bootstrap 3.4.1 (⚠️ EOL) | libman.json; TD-13 |
| DOM manipulation | jQuery 3.6.3 | libman.json |
| Notifications (Web) | toastr.js 2.1.4 | libman.json |
| Notifications (Admin) | Custom ToastService (Blazor) | ToastService.cs; 3s dismiss |
| Client-side validation | jquery-validation + ASP.NET unobtrusive | libman.json |
| Client cache (Admin) | Blazored.LocalStorage | 60s TTL; immediate invalidation |
| Real-time (Web) | Not implemented | aspnet-signalr present but no hub — TD-16 |

---

## 8. Bootstrap Upgrade Path (TD-13)

Bootstrap 3.4.1 reached end-of-life in July 2019. The Web application uses Bootstrap 3-specific class names in Razor templates. Migration to Bootstrap 5.3 requires:

1. Update `libman.json` Bootstrap version from `3.4.1` to `5.3.x`
2. Update layout templates — key breaking changes:
   - `col-xs-*` → `col-*`
   - `pull-left`/`pull-right` → `float-start`/`float-end`
   - `hidden-xs` → `d-none d-sm-block`
   - Panel/well components removed — use Cards
   - Glyphicons removed — switch to Bootstrap Icons or Font Awesome
3. Test all pages visually — Bootstrap 3→5 is not a drop-in upgrade
4. Remove jQuery dependency if Bootstrap JS components are migrated to pure Bootstrap 5

**Confidence:** INFERRED — Bootstrap 3 class names deduced from web pages not extracted; actual template content unavailable (MIS-004).
