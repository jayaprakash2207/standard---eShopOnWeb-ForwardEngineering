=== DOCUMENT: 10_SERVICE_CATALOG.md ===

# Service Catalog — eShopOnWeb

---

## Deployable Services

### SRV-001: eshopwebmvc (Web Application)

| Attribute | Value |
|-----------|-------|
| Type | ASP.NET Core 8 MVC + Blazor WASM host |
| Runtime | dotnetcore\|8.0 |
| Port (Docker) | 5106 → 8080 |
| Port (Azure) | 443 (HTTPS, httpsOnly:true) |
| Deployment | Azure App Service B1 Linux (production); Docker Compose (dev) |
| Azure Deploy | ✅ Declared in azure.yaml |
| Key Vault | ✅ Connected (Managed Identity, production only) |
| Auth | ASP.NET Core Identity cookies (60min); forwards JWT to BlazorAdmin |
| Databases | CatalogDB (RW), IdentityDB (RW) |
| SQL Retry | ✅ EnableRetryOnFailure() in production path only |
| Health Endpoint | /health (content-based) |
| Logging | Console (plain text, Warning in prod, Debug in dev) |
| Entry Points | Razor Pages (catalog/basket/checkout/orders — ASSUMED), Login/Register/ConfirmEmail (confirmed) |
| Hosts | BlazorAdmin WASM SPA |

**Capabilities served:**
- CAP-002 Shopping Basket Management
- CAP-003 Order Placement & History
- CAP-004 Customer Identity (web sessions)
- CAP-006 Customer Storefront Browsing
- CAP-007 Customer Account Registration
- CAP-008 Anonymous Basket & Session Transfer

---

### SRV-002: eshoppublicapi (Public REST API)

| Attribute | Value |
|-----------|-------|
| Type | ASP.NET Core 8 Minimal API |
| Runtime | dotnetcore\|8.0 |
| Port (Docker) | 5200 → 8080 |
| Port (Azure) | **Not deployed — no azure.yaml entry (TD-12)** |
| Deployment | Docker Compose (dev) only |
| Azure Deploy | ❌ NOT declared in azure.yaml |
| Key Vault | ❌ No Key Vault integration |
| Auth | JWT Bearer (HMAC-SHA256, Administrators role for mutations) |
| Databases | CatalogDB (RW), IdentityDB (R for token issuance) |
| SQL Retry | ❌ No EnableRetryOnFailure() |
| OpenAPI | ✅ Swagger at /swagger/v1/swagger.json |
| Logging | Console (plain text) |

**Capabilities served:**
- CAP-001 Product Catalog Management (primary API surface)
- CAP-005 Admin Catalog Portal (backend for BlazorAdmin)
- CAP-004 Customer Identity (JWT token issuance)

---

## Application Services

### Domain Services (ApplicationCore)

| ID | Service | Interface | Methods | Consumers |
|----|---------|-----------|---------|-----------|
| SVC-001 | BasketService | IBasketService | AddItemToBasket, DeleteBasketAsync, SetQuantities, TransferBasketAsync | Web (Login, Checkout pages) |
| SVC-002 | OrderService | IOrderService | CreateOrderAsync(basketId, address) | Web (Checkout page) |
| SVC-003 | UriComposer | IUriComposer | ComposePicUri(pictureUri) | Web, PublicApi endpoints |

### Infrastructure Services

| ID | Service | Interface | Methods | Consumers |
|----|---------|-----------|---------|-----------|
| SVC-004 | IdentityTokenClaimService | ITokenClaimsService | GetTokenAsync(userName) | PublicApi AuthenticateEndpoint |
| SVC-005 | EfRepository\<T\> | IRepository\<T\>, IReadRepository\<T\> | AddAsync, UpdateAsync, DeleteAsync, GetByIdAsync, ListAsync, CountAsync, FirstOrDefaultAsync | All domain services + endpoints |
| SVC-006 | BasketQueryService | IBasketQueryService | CountTotalBasketItems(username) | Web navigation basket count |
| SVC-007 | EmailSender (**STUB**) | IEmailSender | SendEmailAsync(email, subject, body) → Task.CompletedTask | Web Register page, Forgot password |
| SVC-008 | LoggerAdapter\<T\> | IAppLogger\<T\> | LogInformation, LogWarning | Domain services |

### Application Services (Web)

| ID | Service | Pattern | Cache TTL | Consumers |
|----|---------|---------|-----------|-----------|
| SVC-009 | CachedCatalogViewModelService | Decorator over ICatalogViewModelService | 30s IMemoryCache sliding | Web catalog pages |
| SVC-010 | GetMyOrdersHandler | MediatR IRequestHandler | None | Web order history page |

### BlazorAdmin Services

| ID | Service | Pattern | Cache | Consumers |
|----|---------|---------|-------|-----------|
| SVC-011 | CatalogItemService | HTTP client | None | CachedCatalogItemServiceDecorator |
| SVC-012 | CachedCatalogItemServiceDecorator | Decorator + Blazored.LocalStorage | 60s with immediate mutation invalidation | BlazorAdmin catalog pages |
| SVC-013 | CustomAuthStateProvider | AuthenticationStateProvider | 60s principal cache | BlazorAdmin auth state |
| SVC-014 | CatalogLookupDataService\<T,R\> | HTTP client | Via CachedCatalogLookupDataServiceDecorator | Catalog item form dropdowns |
| SVC-015 | HttpService | HTTP wrapper | None | All BlazorAdmin API calls |

### Middleware

| ID | Service | Applied To | Behavior |
|----|---------|-----------|---------|
| SVC-016 | ExceptionMiddleware | PublicApi | DuplicateException → 409; all others → 500 + message leak (TD-04) |
| SVC-017 | RevokeAuthenticationEvents | Web | Checks IMemoryCache on each cookie auth for revoked tokens |

---

## Service Dependency Graph

```
Browser (Anonymous)
    └──► eshopwebmvc:5106
              ├──► CatalogDB (EfRepository)
              ├──► IdentityDB (SignInManager, UserManager)
              └──► [internally hosts] BlazorAdmin WASM
                        └──► eshoppublicapi:5200 (JWT Bearer)
                                  ├──► CatalogDB (EfRepository)
                                  └──► IdentityDB (UserManager for roles)

Production (Azure):
    Browser ──► Azure App Service (eshopwebmvc, port 443)
                     ├──► Azure SQL CatalogDB (via Key Vault conn string)
                     ├──► Azure SQL IdentityDB (via Key Vault conn string)
                     ├──► Azure Key Vault (startup config read)
                     └──► BlazorAdmin WASM ──► PublicApi
                                                 [❌ NOT DEPLOYED in Azure]
```

---

## Service SLAs and NFRs

| Service | Metric | Value | Source | Status |
|---------|--------|-------|--------|--------|
| eshopwebmvc | Catalog cache TTL | 30s sliding | CacheHelpers.cs | OK |
| eshoppublicapi | Catalog list latency penalty | **+1,000ms per request** | CatalogItemListPagedEndpoint.cs:42 | **CRITICAL BUG — TD-07** |
| eshoppublicapi | SQL retry (production) | ❌ None | Dependencies.cs | Gap |
| eshopwebmvc | Auth cookie validity | 60min | ConfigureCookieSettings.cs | OK |
| eshoppublicapi | JWT token validity | 7 days | IdentityTokenClaimService.cs | OK |
| BlazorAdmin | Auth state refresh | 60s | CustomAuthStateProvider.cs | OK |
| BlazorAdmin | Catalog cache (browser) | 60s | CachedCatalogItemServiceDecorator.cs | OK |
| eshopwebmvc | Health check endpoint | /health (content-based) | Web/Program.cs | Partial (non-pooled HttpClient risk) |
| Azure App Service | Compute | B1: 1 core, 1.75GB RAM | appserviceplan.bicep | OK |
| Azure SQL | TLS minimum | 1.2 | sqlserver.bicep | OK |
