# Storage Pattern Analysis — eShopOnWeb
> Source: Phase 1 — Config, Extensions, Cache, Background, HealthChecks files
> Extraction date: 2026-07-06

---

## 1. Primary Relational Storage (SQL Server)

**Pattern:** Entity Framework Core with Ardalis Specification library and Repository pattern

| Aspect | Detail |
|--------|--------|
| Engine | SQL Server / Azure SQL Edge (docker-compose: mcr.microsoft.com/azure-sql-edge, port 1433) |
| ORM | EF Core (net8.0 target) |
| Repository abstraction | `IRepository<T>` / `IReadRepository<T>` → `EfRepository<T>` (Ardalis.Specification.EntityFrameworkCore) |
| ID generation | Mixed: IDENTITY (Baskets, Orders, BasketItems, OrderItems) + HiLo sequences (Catalog, CatalogBrands, CatalogTypes) |
| In-memory fallback | `UseOnlyInMemoryDatabase=true` config flag enables full in-memory mode for dev/test |
| Transaction scope | EF `SaveChanges()` — one DbContext per request (scoped DI) |
| Contexts | Two: `CatalogContext` (CatalogConnection) and `AppIdentityDbContext` (IdentityConnection) |
| Migration tool | EF Core CLI Migrations |

Two separate DbContext instances — `CatalogContext` and `AppIdentityDbContext`. In Docker both share one SQL Server instance (`sqlserver` service). In production they could be fully separated databases.

---

## 2. Server-Side Memory Cache (ASP.NET Core IMemoryCache)

**Pattern:** Decorator — `CachedCatalogViewModelService` wraps `CatalogViewModelService`

| Aspect | Detail |
|--------|--------|
| Provider | `IMemoryCache` (in-process, per server instance) |
| Scope | Web MVC server only |
| Cached data | CatalogItems paginated (brand/type filtered), CatalogBrands, CatalogTypes |
| TTL | **30 seconds sliding expiration** (`CacheHelpers.DefaultCacheDuration = TimeSpan.FromSeconds(30)`) |
| Invalidation | **None** — TTL-only. Admin writes via PublicApi do NOT invalidate this cache. |
| Cache keys | `items-{pageIndex}-{itemsPage}-{brandId}-{typeId}`, `brands`, `types` |
| Registered | `builder.Services.AddMemoryCache()` in both Web and PublicApi Program.cs |
| Scale risk | In-process — not shared across Web instances. Each instance has its own independent cache. |

**Business rule (BR-08):** Catalog data shown to shoppers in the Web storefront may be up to 30 seconds stale after an admin update via BlazorAdmin/PublicApi.

---

## 3. Browser LocalStorage Cache (Blazor WASM)

**Pattern:** Decorator — `CachedCatalogItemServiceDecorator` and `CachedCatalogLookupDataServiceDecorator<T>` wrap HTTP service classes

| Aspect | Detail |
|--------|--------|
| Provider | `Blazored.LocalStorage` (browser localStorage API) |
| Scope | Per-browser session, BlazorAdmin only |
| Cached data | CatalogItems (key: `items`), CatalogBrand (key: `CatalogBrand`), CatalogType (key: `CatalogType`) |
| TTL | **1 minute absolute** (`CacheEntry.DateCreated.AddMinutes(1) > DateTime.UtcNow`) |
| Invalidation on CatalogItem write | `RefreshLocalStorageList()` removes `items` key and re-fetches immediately |
| Invalidation on startup | `ClearLocalStorageCache()` in BlazorAdmin Program.cs removes `CatalogBrand` and `CatalogType` keys on every app load |
| Write-through gap | Create/Edit/Delete operations refresh `items` only. Brand and Type lists are NOT invalidated on item mutations — only TTL refreshes them. |

**Business rule (BR-09):** BlazorAdmin catalog item list is at most 1 minute stale. Brand/type lists are at most 1 minute stale but NOT invalidated on item write operations.

---

## 4. HTTP Cookie Storage (Anonymous Basket Identity)

**Pattern:** Server-issued GUID cookie used as basket identity for anonymous shoppers

| Aspect | Detail |
|--------|--------|
| Cookie name | `Constants.BASKET_COOKIENAME` (defined in `src/Web/Constants.cs`) |
| Content | GUID string (anonymous BuyerId) |
| TTL | **10 years** (`DateTime.Today.AddYears(10)`) |
| Scope | Web MVC only |
| Security | No `Secure` or `HttpOnly` flags confirmed in code review |
| DB persistence | GUID stored as `BuyerId` in Baskets table indefinitely |
| Cleanup | No background job or TTL-based cleanup of stale anonymous Baskets rows observed |

**Risk:** The Baskets table may accumulate many abandoned anonymous rows over time with no cleanup mechanism.

---

## 5. File System Storage (Product Images)

**Pattern:** Static files served via ASP.NET Core static files middleware

| Aspect | Detail |
|--------|--------|
| Path pattern | `images/products/{n}.png` |
| Base URL config | `CatalogSettings.CatalogBaseUrl` (injected into `UriComposer`) |
| DB storage | `Catalog.PictureUri` stores template URL `http://catalogbaseurltobereplaced/images/products/{n}.png` |
| Runtime resolution | `UriComposer.ComposePicUri()` replaces the placeholder at read time |
| Upload | **DISABLED** — security concern (GitHub issue #537). New items use `eCatalog-item-default.png` |
| Production recommendation | Code comment: "upload to blob storage and deliver via CDN after verification process" |

---

## 6. JWT Token Storage (Authentication)

**Pattern:** JWT Bearer tokens issued by PublicApi, held in-memory by BlazorAdmin per session

| Aspect | Detail |
|--------|--------|
| Token type | JWT (HS256) |
| Signing key | `AuthorizationConstants.JWT_SECRET_KEY` — hardcoded constant (see DQ-09) |
| Client storage | `HttpClient.DefaultRequestHeaders.Authorization` (in-memory per session — not persisted to LocalStorage) |
| Audience/Issuer validation | **Disabled** (`ValidateIssuer = false`, `ValidateAudience = false`) |
| Token lifetime | Not explicitly configured in PublicApi — uses JWT default |
| Revocation | No revocation mechanism. Compromised token remains valid until natural expiry. |

---

## 7. No Background Workers / No Message Queue

Scanned for `*/Background*`, `*/Workers*`, `*/Jobs*`, `*/Queue*`, `*/Hosted*` — none found.

There are no background processing jobs, message queues, event buses, scheduled tasks, or hosted services in this codebase. All data operations are synchronous request/response.

---

## 8. Health Checks

**Pattern:** Application-level HTTP health checks (not direct DB pings)

| Check | Behaviour |
|-------|-----------|
| ApiHealthCheck | HTTP GET to `catalog-items` endpoint; verifies `.NET Bot Black Sweatshirt` in response body |
| HomePageHealthCheck | HTTP GET to app homepage; verifies `.NET Bot Black Sweatshirt` in response body |

**Note:** Neither check directly pings the database. DB health is inferred from API response content. If the DB is down but a cached response is returned, the health check could report healthy while the DB is unavailable.

---

## 9. Cookie Security Flags (Basket Cookie)

**Pattern:** Browser cookie set by `Index.cshtml.cs:GetOrSetBasketCookieAndUserName()`

| Aspect | Detail |
|--------|--------|
| `IsEssential` | **true** — set in cookie options (GDPR lawful basis) |
| `Secure` | **NOT set** — not in CookieOptions in `Index.cshtml.cs:94-96` |
| `HttpOnly` | **NOT set** — not in CookieOptions |
| Expiry | 10 years (`DateTime.Today.AddYears(10)`) |

**RC-04 (CORRECTED):** Agent 1 stated "No Secure or HttpOnly flags confirmed" which is accurate. Agent 2 confirms via direct reading of the cookie-write call. `IsEssential = true` *is* set (GDPR) but `Secure` and `HttpOnly` are absent — the GUID can be read by JS and transmitted over plain HTTP.

---

## Storage Architecture Summary

## Agent 2 Review Changes

```json
[
  {
    "change_id": "RC-04",
    "type": "ENRICHED",
    "finding_id": "storage-pattern-analysis.md — Section 4: HTTP Cookie Storage",
    "what": "Confirmed IsEssential=true IS set (GDPR essential cookie). Secure and HttpOnly remain absent. Agent 1 was directionally correct; adding confirmation of IsEssential.",
    "evidence_source": "Phase 1 spot check",
    "evidence_detail": "src/Web/Pages/Basket/Index.cshtml.cs:94 — 'var cookieOptions = new CookieOptions { IsEssential = true }; cookieOptions.Expires = DateTime.Today.AddYears(10); Response.Cookies.Append(...)'. No Secure or HttpOnly properties set.",
    "confidence_before": 0.8,
    "confidence_after": 0.95,
    "phase_found": "Phase 1 test review / spot check"
  },
  {
    "change_id": "RC-05",
    "type": "ENRICHED",
    "finding_id": "storage-pattern-analysis.md — Section 2: IMemoryCache",
    "what": "Confirmed CacheHelpers.DefaultCacheDuration = TimeSpan.FromSeconds(30) directly from source. Cache key formats confirmed: 'items-{pageIndex}-{itemsPage}-{brandId}-{typeId}', 'brands', 'types'. Seed item '.NET Bot Black Sweatshirt' is the health-check target.",
    "evidence_source": "Phase 4 spot check",
    "evidence_detail": "src/Web/Extensions/CacheHelpers.cs:7 — TimeSpan.FromSeconds(30). tests/UnitTests/Web/Extensions/CacheHelpersTests/GenerateCatalogItemCacheKey.cs confirms key format 'items-0-10--'.",
    "confidence_before": 0.9,
    "confidence_after": 1.0,
    "phase_found": "Phase 4 spot check"
  }
]
```

```
Shopper Request Lifecycle (Web MVC):
  Browser
  → Web MVC
    → IMemoryCache (30s sliding TTL)
      [MISS] → CatalogViewModelService
               → EfRepository<CatalogItem/Brand/Type>
               → CatalogDB (SQL Server)
  Anonymous: BuyerId = GUID cookie (10yr)
  Authenticated: BuyerId = email (ASP.NET Identity cookie)

Admin Request Lifecycle (BlazorAdmin → PublicApi):
  Browser
  → BlazorAdmin WASM
    → LocalStorage cache (1 min TTL)
      [MISS] → HttpService
               → PublicApi (JWT Bearer auth)
               → EfRepository<CatalogItem>
               → CatalogDB (SQL Server)
  Auth: JWT token from /api/authenticate (held in-memory)

Identity:
  Web MVC / PublicApi
  → ASP.NET Identity
  → AppIdentityDbContext
  → IdentityDB (SQL Server)
```
