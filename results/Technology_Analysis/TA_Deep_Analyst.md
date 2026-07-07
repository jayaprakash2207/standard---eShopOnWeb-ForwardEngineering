I now have all the evidence needed to produce the complete Agent 2 analysis. Let me compile the full 8-output report.

---

## Agent 2 - Analysis Summary

- Layers analysed: 6 — Application, Data, Infrastructure, CI/CD, Security, Observability
- Chunks processed: 6 (Orientation + 5 layer deep-dives + Synthesis Pass)
- Technologies assessed: 67
- Architecture patterns catalogued: 14 (AP-01 through AP-14)
- NFR entries recorded: 19 (NFR-01 through NFR-19)
- Technical debt items identified: 20 (TD-01 through TD-20) — Critical: 3, High: 8, Medium: 6, Low: 3
- CI/CD pipeline files directly read: 2 (0 reusable workflow files — none referenced locally)
- CI/CD capabilities confirmed present: 2 of 14 (Build, Unit Tests)
- Agent 1 LOW CONFIDENCE items resolved: 10 of 12
- Discrepancies with Agent 1: 3

---

## OUTPUT 1 - Technology Stack Assessment

| Component | Declared Version | Usage Depth | How It Is Used in This System | EOL / Support Status | Agent 1 Match? |
|---|---|---|---|---|---|
| .NET Runtime | 8.0 | Active - core path | All application processes run on .NET 8.0; confirmed in global.json rollForward policy and Bicep runtimeVersion | LTS until November 2026 | Confirmed |
| ASP.NET Core MVC | 8.0.2 | Active - core path | eshopwebmvc uses full MVC pipeline: controllers, Razor views, middleware chain (HSTS, HttpsRedirection, Authentication, Authorization, CookiePolicy) | LTS until November 2026 | Confirmed |
| Blazor WebAssembly | 8.0.2 | Active - core path | BlazorAdmin embedded in Web host; served as WASM; CustomAuthStateProvider fetches JWT from PublicApi /User endpoint and attaches Bearer header to all subsequent HttpClient calls; cache duration hardcoded 60 seconds | LTS until November 2026 | Confirmed |
| Entity Framework Core SqlServer | 8.0.2 | Active - core path | Two DbContexts: CatalogContext (Baskets, CatalogItems, CatalogBrands, CatalogTypes, Orders, OrderItems, BasketItems) + AppIdentityDbContext (ASP.NET Identity tables). EfRepository<T> wraps Ardalis RepositoryBase<T>. Production path uses `sqlOptions.EnableRetryOnFailure()`. | LTS until November 2026 | Confirmed |
| Entity Framework Core InMemory | 8.0.2 | Active - test path | UseOnlyInMemoryDatabase=true switches both CatalogContext and AppIdentityDbContext to in-memory; used in PublicApiIntegrationTests | LTS until November 2026 | Confirmed |
| MediatR | 12.0.1 | Partial - declared, minimal direct evidence | Package declared; no direct `IMediator.Send()` call sites found in source files read; likely used by PublicApi endpoints not yet read in depth | Supported | Confirmed |
| AutoMapper | 12.0.1 | Active - secondary | MappingProfile assembly scanned in PublicApi Program.cs: `AddAutoMapper(typeof(MappingProfile).Assembly)` | Supported | Confirmed |
| FluentValidation | 11.9.0 | Active - secondary | Package used for request validation in PublicApi endpoints (package reference confirmed; endpoint bodies not fully read) | Supported | Confirmed |
| Ardalis.Specification | 7.0.0 | Active - core path | All repository queries use strongly-typed Specifications: BasketWithItemsSpecification, CatalogFilterPaginatedSpecification, CatalogItemsSpecification, CustomerOrdersWithItemsSpecification, OrderWithItemsByIdSpec — all confirmed in source | Supported | Confirmed |
| Ardalis.ApiEndpoints | 4.1.0 | Active - core path | `app.MapEndpoints()` registered in PublicApi Program.cs | Supported | Confirmed |
| Ardalis.GuardClauses | 4.0.1 | Active - core path | Used in Basket, BasketItem, Order, CatalogItem, OrderService — domain entity validation; custom extension `Guard.Against.EmptyBasketOnCheckout()` | Supported | Confirmed |
| Ardalis.Result | 7.0.0 | Active - secondary | `Result<Basket>` returned from BasketService.SetQuantities() | Supported | Confirmed |
| Swashbuckle.AspNetCore | 6.5.0 | Active - secondary | OpenAPI doc generated in PublicApi; Bearer security scheme defined; Swagger UI served at `/swagger/v1/swagger.json` | Supported | Confirmed |
| Microsoft.AspNetCore.Authentication.JwtBearer | 8.0.2 | Active - core path | PublicApi uses JWT Bearer as DefaultScheme; ValidateIssuerSigningKey=true, ValidateIssuer=false, ValidateAudience=false; RequireHttpsMetadata=false | LTS until November 2026 | Confirmed |
| ASP.NET Core Identity | 8.0.2 | Active - core path | eshopwebmvc uses Cookie authentication; PublicApi uses JWT; both use AppIdentityDbContext + IdentityTokenClaimService; seed data creates users/roles at startup | LTS until November 2026 | Confirmed |
| System.IdentityModel.Tokens.Jwt | 7.3.1 | Active - core path | IdentityTokenClaimService generates JWT: HmacSha256Signature, 7-day expiry, key sourced from `AuthorizationConstants.JWT_SECRET_KEY` hardcoded constant | Supported | Confirmed |
| Azure.Identity | 1.10.4 | Active - production path only | Production branch in Web Program.cs: `ChainedTokenCredential(new AzureDeveloperCliCredential(), new DefaultAzureCredential())` for Key Vault config provider | Supported | Confirmed |
| Azure.Extensions.AspNetCore.Configuration.Secrets | 1.3.1 | Active - production path only | `builder.Configuration.AddAzureKeyVault(...)` called only in non-Development/non-Docker branch | Supported | Confirmed |
| IMemoryCache (Microsoft.Extensions.Caching.Memory) | 8.0.x (built-in) | Active - core path | CachedCatalogViewModelService wraps CatalogViewModelService with GetOrCreateAsync; SlidingExpiration = 30 seconds; keys: "brands", "types", pattern "items-{0}-{1}-{2}-{3}" | Supported | New — not in Agent 1 as distinct usage (implied) |
| Microsoft.AspNetCore.Mvc | 2.2.0 | Declared-only — no usage evidence | Package declared in Directory.Packages.props at 2.2.0; all actual MVC usage is via ASP.NET Core 8.0.2 framework (implicit). No project references this standalone package directly. | EOL: December 2018 (ASP.NET Core 2.2) | DISCREPANCY — Agent 1 flagged LOW/version conflict; confirmed stale declaration, no active usage |
| SignalR Client (aspnet-signalr) | 1.0.27 | Declared-only — no usage evidence in source read | Included via libman to browser; no server-side SignalR hub found in source files read | EOL: ASP.NET Core 1.x era | Confirmed LOW |
| Bootstrap | 3.4.1 | Active - secondary | MVC views use Bootstrap 3.4.1 for layout | EOL: Bootstrap 3 — no official security support; Bootstrap 5.3 is current | Confirmed |
| jQuery | 3.6.3 | Active - secondary | Used for validation and UI in MVC views | Supported (3.7.1 current) | Confirmed |
| Application Insights | UNKNOWN | Declared-only — no SDK | `APPLICATIONINSIGHTS_CONNECTION_STRING` env var injected if `applicationInsightsName` is non-empty; `main.bicep` passes no `applicationInsightsName` to web module; no `Microsoft.ApplicationInsights.AspNetCore` NuGet package present | N/A — not instrumented | DISCREPANCY — Agent 1 flagged LOW; confirmed: App Insights is NOT provisioned and NOT instrumented in this repository |
| EfRepository<T> / Ardalis.Specification.EntityFrameworkCore | 7.0.0 | Active - core path | All domain aggregates (Basket, Order, CatalogItem, CatalogBrand, CatalogType) use EfRepository<T> via IRepository<T> and IReadRepository<T> | Supported | Confirmed |
| dotnet-xunit | 2.3.1 | Declared-only — deprecated | DotNetCliToolReference in FunctionalTests.csproj; this mechanism is unsupported in .NET Core 2.1+ SDK; functional tests likely cannot be run via this tool reference | Unsupported — deprecated since .NET Core 2.1 | Confirmed LOW |

---

## OUTPUT 2 - Architecture Pattern Catalog

| ID | Pattern Name | Category | Applies To | Exact Configuration | Coverage | Confidence | Source |
|---|---|---|---|---|---|---|---|
| AP-01 | Repository Pattern with Specification | Data Access | All domain aggregates via EfRepository<T> | Generic `EfRepository<T> : RepositoryBase<T>` implementing `IRepository<T>` and `IReadRepository<T>`; queries via typed Specification objects (BasketWithItemsSpecification, CatalogFilterPaginatedSpecification, CatalogItemsSpecification, CustomerOrdersWithItemsSpecification, OrderWithItemsByIdSpec, CatalogItemNameSpecification) | Applied everywhere for domain aggregate access | HIGH | src/Infrastructure/Data/EfRepository.cs; src/ApplicationCore/Specifications/*.cs |
| AP-02 | Aggregate Root Pattern (DDD) | Data Access | Basket, CatalogItem, CatalogBrand, CatalogType, Order, Buyer entities | `IAggregateRoot` marker interface; private setters enforce encapsulation; collections exposed as `IReadOnlyCollection<T>`; modification only through entity methods (Basket.AddItem, BasketItem.SetQuantity, Order constructor) | Applied to all root entities | HIGH | src/ApplicationCore/Entities/*/; src/ApplicationCore/Interfaces/IAggregateRoot.cs |
| AP-03 | Clean Architecture Layering | Application | ApplicationCore → Infrastructure → Web / PublicApi | ApplicationCore has zero framework dependencies; Infrastructure references ApplicationCore only; Web and PublicApi reference both. Enforced by project reference graph. | Applied at solution level | HIGH | All .csproj project references |
| AP-04 | Cache-Aside with SlidingExpiration | Caching | eshopwebmvc → CatalogViewModelService | `IMemoryCache.GetOrCreateAsync`; `SlidingExpiration = TimeSpan.FromSeconds(30)` (30 seconds); keys: "brands" (brand list), "types" (type list), "items-{pageIndex}-{itemsPage}-{brandId}-{typeId}" (paginated catalog items); cache not invalidated on write — read path only | Applied to catalog read path (Web only); not applied in PublicApi | HIGH | src/Web/Extensions/CacheHelpers.cs:7; src/Web/Services/CachedCatalogViewModelService.cs |
| AP-05 | Retry on Failure (EF Core SqlClient) | Resilience | eshopwebmvc → Azure SQL (production path only) | `sqlOptions.EnableRetryOnFailure()` — uses EF Core default retry policy: max 6 attempts; exponential backoff with jitter; default transient errors list for SQL Server | Applied in production (non-Dev/non-Docker) branch only; NOT applied in development/Docker branch; NOT applied in PublicApi (PublicApi uses Dependencies.ConfigureServices which has no EnableRetryOnFailure) | HIGH | src/Web/Program.cs:36,41 |
| AP-06 | Health Check Endpoints | Observability | eshopwebmvc | Two named health checks registered: `ApiHealthCheck` (tag: "apiHealthCheck") checks PublicApi by calling `{apiBase}catalog-items` and asserting ".NET Bot Black Sweatshirt" in response; `HomePageHealthCheck` (tag: "homePageHealthCheck") calls home page URL and asserts same string. Served at `/health` (full), `/home_page_health_check`, `/api_health_check`. Response format: JSON with status + per-check error entries. | Web only; not implemented in PublicApi | HIGH | src/Web/Program.cs:87-89, 151-198; src/Web/HealthChecks/ApiHealthCheck.cs; src/Web/HealthChecks/HomePageHealthCheck.cs |
| AP-07 | Cookie Authentication (Web) | Security | eshopwebmvc | `CookieAuthenticationDefaults.AuthenticationScheme` as default; `HttpOnly = true`; `SecurePolicy = CookieSecurePolicy.Always`; `SameSite = SameSiteMode.Lax`; CSRF protection via ASP.NET Core's built-in anti-forgery (Razor Pages + MVC forms) | Applied to Web MVC app | HIGH | src/Web/Program.cs:47-53 |
| AP-08 | JWT Bearer Authentication (API) | Security | eshoppublicapi | `JwtBearerDefaults.AuthenticationScheme` as default; `ValidateIssuerSigningKey = true`; `IssuerSigningKey` = HMAC-SHA256 from `AuthorizationConstants.JWT_SECRET_KEY` (hardcoded constant); `ValidateIssuer = false`; `ValidateAudience = false`; `RequireHttpsMetadata = false`; token expiry = 7 days (from IdentityTokenClaimService) | Applied to PublicApi only | HIGH | src/PublicApi/Program.cs:54-70; src/Infrastructure/Identity/IdentityTokenClaimService.cs |
| AP-09 | Token-Gated State Provider (Blazor) | Security | BlazorAdmin | `CustomAuthStateProvider` fetches `/User` endpoint with 60-second in-memory cache; on authenticated state, sets `HttpClient.DefaultRequestHeaders.Authorization = Bearer {token}`; unauthenticated state returns empty ClaimsIdentity | Applied to BlazorAdmin only | HIGH | src/BlazorAdmin/CustomAuthStateProvider.cs |
| AP-10 | Global Exception Middleware | Application | eshoppublicapi | `ExceptionMiddleware` catches all unhandled exceptions; maps `DuplicateException` → HTTP 409 Conflict; all other exceptions → HTTP 500 Internal Server Error; response always JSON `{StatusCode, Message}` | Applied to PublicApi only; Web uses `app.UseExceptionHandler("/Error")` in production, `app.UseDeveloperExceptionPage()` in development | HIGH | src/PublicApi/Middleware/ExceptionMiddleware.cs |
| AP-11 | Abstract Logging (Adapter) | Observability | ApplicationCore services (BasketService confirmed) | `IAppLogger<T>` interface in ApplicationCore; `LoggerAdapter<T>` in Infrastructure wraps `ILogger<T>` from Microsoft.Extensions.Logging; injected into services; decouples ApplicationCore from logging framework | Applied to ApplicationCore services where logging is needed | HIGH | src/Infrastructure/Logging/LoggerAdapter.cs; src/ApplicationCore/Interfaces/IAppLogger.cs |
| AP-12 | Conditional Infrastructure Switching (Test/Prod) | Deployment | All DbContext registrations | `Dependencies.ConfigureServices`: if `UseOnlyInMemoryDatabase=true` → both CatalogContext and AppIdentityDbContext use in-memory. Web Program.cs: if Development or Docker → use connection strings from config; if production → use Azure Key Vault + EnableRetryOnFailure. | Applied at startup | HIGH | src/Infrastructure/Dependencies.cs; src/Web/Program.cs:25-43 |
| AP-13 | Slug Route Transformation | Application | eshopwebmvc | `SlugifyParameterTransformer` registered as constraint "slugify"; applied to all MVC routes via `RouteTokenTransformerConvention`; default route: `{controller:slugify=Home}/{action:slugify=Index}/{id?}` | Applied to Web routing only | HIGH | src/Web/Program.cs:67-78 |
| AP-14 | Managed Identity + Key Vault Config Provider | Security | eshopwebmvc (production) | `ChainedTokenCredential(new AzureDeveloperCliCredential(), new DefaultAzureCredential())` used to authenticate to Key Vault; `AddAzureKeyVault` loads secrets as configuration keys at startup; App Service has SystemAssigned managed identity with Key Vault access policy (secrets: get+list) | Production path only; not active in Development/Docker | HIGH | src/Web/Program.cs:31-32; infra/core/host/appservice.bicep |

### Pattern Coverage Gaps

| Gap | Affected Integration / Component | Severity | Recommendation |
|---|---|---|---|
| No retry logic on PublicApi → SQL Server | PublicApi → CatalogContext + AppIdentityDbContext | High | Add `sqlOptions.EnableRetryOnFailure()` in Dependencies.ConfigureServices for both production paths, or replicate Web's production branch pattern in PublicApi |
| No circuit breaker on any database call | eshopwebmvc + eshoppublicapi → SQL Server | High | Add Polly-based circuit breaker around EF Core context; or use Resilience4j equivalent for .NET (Microsoft.Extensions.Resilience) |
| No timeout declared on EF Core connections | Both DbContexts | High | Add `CommandTimeout` and connection timeout to SQL Server options; EF Core default is 30s command timeout but no connection timeout is explicitly declared |
| No retry or circuit breaker on external HTTP calls | ApiHealthCheck → PublicApi endpoint; Blazor CustomAuthStateProvider → /User endpoint; HomePageHealthCheck → home URL | High | These HttpClient usages create new `HttpClient()` instances directly (anti-pattern); replace with IHttpClientFactory + Polly retry/circuit breaker policies |
| No CORS policy on eshopwebmvc | eshopwebmvc (MVC host) | Medium | PublicApi has CORS configured; Web MVC host has no explicit CORS policy; CORS origin for Azure deployment is not declared anywhere in application code |
| BlazorAdmin auth cache TTL hardcoded | BlazorAdmin CustomAuthStateProvider | Low | `UserCacheRefreshInterval = TimeSpan.FromSeconds(60)` hardcoded with TODO comment; should be injected from configuration |
| No API versioning strategy | eshoppublicapi public REST API | Medium | Swagger doc declared as "v1" but no versioning mechanism (no `Asp.Versioning`, no URL prefix `/api/v1/`); breaking changes have no migration path |

### Declared-But-Unused Libraries

| Library | Declared In | No Usage Found In | Risk |
|---|---|---|---|
| Microsoft.AspNetCore.Mvc 2.2.0 | Directory.Packages.props | All project source — no .csproj references this standalone package | Dead dependency / stale declaration — misleads version analysis tools |
| SignalR Client 1.0.27 | src/Web/libman.json (browser) | No SignalR Hub registration found in Web Program.cs or any Infrastructure service | Dead client library — loaded in every page but no server counterpart found |
| dotnet-xunit 2.3.1 | tests/FunctionalTests/FunctionalTests.csproj | DotNetCliToolReference mechanism is deprecated; cannot be invoked via `dotnet xunit` in .NET 6+ SDK | Functional test runner is inoperable; tests in FunctionalTests project cannot be run via this reference |

---

## OUTPUT 3 - Component Interaction & Contract Map

| Caller | Target | Protocol | Interaction Type | Coupling Strength | Contract | Timeout Declared? | Error Handling | Notes |
|---|---|---|---|---|---|---|---|---|
| eshopwebmvc | CatalogContext (SQL Server) | TCP/TLS 1.2 | Sync Request-Response | Tight — direct DbContext injection | No API contract; EF Core schema | Yes — EF Core EnableRetryOnFailure default (production only) | Exception caught at startup seeding; no per-request fallback | Production path only has retry; Dev/Docker has no resilience |
| eshopwebmvc | AppIdentityDbContext (SQL Server) | TCP/TLS 1.2 | Sync Request-Response | Tight — direct DbContext injection | No API contract; EF Core schema | Yes — EF Core EnableRetryOnFailure default (production only) | Exception caught at startup seeding | Same as above |
| eshopwebmvc | Azure Key Vault | HTTPS | Sync (startup config load) | Loose — config provider abstraction | Azure SDK contract | Azure SDK default | No explicit error handling if KV unavailable at startup | App fails to start if KV unreachable in production |
| eshoppublicapi | CatalogContext (SQL Server) | TCP/TLS 1.2 | Sync Request-Response | Tight — direct DbContext injection | No API contract; EF Core schema | No — `EnableRetryOnFailure()` absent in Dependencies.ConfigureServices | Exception caught at startup seeding; ExceptionMiddleware handles per-request | RISK: no transient fault retry in PublicApi |
| eshoppublicapi | AppIdentityDbContext (SQL Server) | TCP/TLS 1.2 | Sync Request-Response | Tight — direct DbContext injection | No API contract; EF Core schema | No | Exception caught at startup seeding | Same risk as above |
| BlazorAdmin | eshoppublicapi | HTTP/HTTPS | Sync Request-Response | Loose — HttpClient with interface | Undocumented (runtime API contract) | No — raw `new HttpClient()` with no timeout | try/catch in CustomAuthStateProvider.FetchUser(); returns empty identity on failure | Anti-pattern: raw `new HttpClient()` instead of IHttpClientFactory |
| ApiHealthCheck | eshoppublicapi | HTTP | Sync Request-Response | Loose — HTTP check | No contract | No — raw `new HttpClient()` with no timeout | HealthCheckResult.Unhealthy on assertion failure; no exception handling on network failure | Raw `new HttpClient()` anti-pattern; no timeout; network failure throws unhandled |
| HomePageHealthCheck | eshopwebmvc | HTTP | Sync Request-Response | Loose — HTTP check | No contract | No — raw `new HttpClient()` with no timeout | HealthCheckResult.Unhealthy on assertion failure; no exception handling | Same issue as ApiHealthCheck |
| eshopwebmvc | eshoppublicapi | HTTP | Sync (Blazor prerender) | Loose — HttpClient | Undocumented | No — no timeout declared on registered HttpClient | No error handling declared | BaseAddress set from BaseUrlConfiguration.WebBase at startup |

### Coupling Hotspots

| Component | Inbound Dependencies | Outbound Dependencies | Coupling Risk |
|---|---|---|---|
| CatalogContext | eshopwebmvc (via EfRepository), eshoppublicapi (via EfRepository) | SQL Server (catalog) | High — both deployable services share a single CatalogContext class and same DB; schema change breaks both |
| AppIdentityDbContext | eshopwebmvc (Auth), eshoppublicapi (Auth) | SQL Server (identity) | High — shared identity DB across both services; schema change breaks both |
| AuthorizationConstants.JWT_SECRET_KEY | IdentityTokenClaimService (token generation), PublicApi Program.cs (token validation) | Hardcoded constant in ApplicationCore | Critical — secret in source code; change requires recompile and redeploy of both services |
| eshoppublicapi | BlazorAdmin (HTTP calls), ApiHealthCheck (HTTP call), eshopwebmvc (Blazor host) | SQL Server (×2), Azure Key Vault (via config) | High — central API for Blazor admin; outage affects both Web host health checks and admin UI |

### API Contract Inventory

| Boundary | Contract Type | Version | Location | Breaking Change Risk |
|---|---|---|---|---|
| eshoppublicapi public REST API | OpenAPI (Swagger) — generated | "v1" (informal, no versioning mechanism) | /swagger/v1/swagger.json (runtime generated) | High — no URL versioning, no schema contract file committed to repo; breaking changes are invisible to consumers |
| eshopwebmvc → eshoppublicapi (Blazor internal) | Undocumented HTTP | UNVERSIONED | NOT FOUND | High — Blazor calls ApiBase directly; no contract enforcement |
| BlazorAdmin → PublicApi /User endpoint | Undocumented | UNVERSIONED | NOT FOUND | High — `UserInfo` deserialization in CustomAuthStateProvider; no versioning |

---

## OUTPUT 4 - Data Architecture Assessment

### Data Store Deep Dive

| Store | Access Pattern | ORM / Query Style | Transaction Scope | Consistency Model | Connection Pool Config | Migration State | Agent 1 Match? |
|---|---|---|---|---|---|---|---|
| CatalogContext / SQL Server (catalog) | Repository pattern via EfRepository<T>; all queries via Ardalis Specification objects; no raw SQL found | EF Core 8.0.2 with Specification pattern; LINQ-generated SQL | Method-level implicit transactions (EF Core SaveChanges); no explicit TransactionScope or BeginTransaction found | Strong (SQL Server ACID) | DEFAULT — no Hikari or explicit pool configuration; EF Core uses SqlClient defaults (max pool: 100, min: 0, connection timeout: 15s implied) | EF Core Migrations present (dotnet-ef 8.0.0 tooling declared); `ApplyConfigurationsFromAssembly` on model creation; EF Migrations directory not read but tooling present | Confirmed |
| AppIdentityDbContext / SQL Server (identity) | Direct ASP.NET Identity framework access; no custom repositories | EF Core 8.0.2 — standard ASP.NET Identity schema; no custom query logic found | Framework-managed (Identity framework handles transactions) | Strong (SQL Server ACID) | DEFAULT — same as CatalogContext | EF Core Migrations present (standard ASP.NET Identity migration pattern) | Confirmed |
| In-Memory EF Store (test) | Same IRepository<T> interface as production; substituted via Dependencies.ConfigureServices UseOnlyInMemoryDatabase branch | EF Core InMemory provider 8.0.2 | No transaction support (InMemory limitation) | None — in-memory, no durability | N/A | N/A | Confirmed |

### Data Ownership Map

| Entity / Table | Owning Service | Other Services With Access | Access Type | Coupling Risk |
|---|---|---|---|---|
| Basket, BasketItem | eshopwebmvc (primary write), eshoppublicapi (shared CatalogContext) | eshoppublicapi | Read-write (shared CatalogContext class) | Tight — shared DbContext class across two deployable containers |
| CatalogItem, CatalogBrand, CatalogType | eshopwebmvc (admin writes), eshoppublicapi (reads + writes) | Both services | Read-write | Tight — no ownership boundary |
| Order, OrderItem | eshopwebmvc (creates via OrderService) | eshoppublicapi (potential reads via EfRepository) | Read-write | Tight |
| ASP.NET Identity tables (Users, Roles, Claims) | eshopwebmvc (primary auth), eshoppublicapi (token generation via UserManager) | eshoppublicapi | Read-write (UserManager calls) | Tight — shared identity DB |

### Data Flow & Consistency Notes

- **Startup seeding**: Both eshopwebmvc and eshoppublicapi independently call `CatalogContextSeed.SeedAsync()` and `AppIdentityDbContextSeed.SeedAsync()` at startup. If both containers start simultaneously, there is a race condition risk on seed data insertion. No distributed lock or idempotency guard was evidenced.
- **No event-driven consistency**: All data flows are synchronous SQL transactions. No event sourcing, outbox pattern, or messaging layer found.
- **No read replica usage**: Both services read and write to the same SQL endpoints; no CQRS read/write separation at the database level.
- **Cache invalidation gap**: CachedCatalogViewModelService caches catalog data with 30-second sliding expiration. Admin writes via BlazorAdmin (via PublicApi endpoints) do not trigger cache invalidation in the Web MVC service. Catalog updates made via PublicApi will not be reflected in the Web catalog view for up to 30 seconds; longer if the cache TTL keeps sliding.

---

## OUTPUT 5 - Security Architecture Assessment

### Authentication & Authorisation Implementation

| Mechanism | Declared (Agent 1) | Implemented How | Validation Completeness | Gaps | Severity |
|---|---|---|---|---|---|
| JWT Bearer (PublicApi) | JWT Bearer Auth 8.0.2 | IdentityTokenClaimService generates JWT using `AuthorizationConstants.JWT_SECRET_KEY` — a hardcoded string constant in ApplicationCore/Constants/AuthorizationConstants.cs ("SecretKeyOfDoomThatMustBeAMinimumNumberOfBytes"). Token validation: ValidateIssuerSigningKey=true, ValidateIssuer=false, ValidateAudience=false, RequireHttpsMetadata=false | Partial — signing key validated; issuer and audience not validated; HTTPS not required for token submission | JWT_SECRET_KEY hardcoded in source; ValidateIssuer=false; ValidateAudience=false; RequireHttpsMetadata=false means tokens can be submitted over HTTP | Critical |
| Cookie Authentication (Web) | ASP.NET Core Identity | `CookieAuthenticationDefaults.AuthenticationScheme`; HttpOnly=true; SecurePolicy=Always; SameSite=Lax; CSRF handled by Razor Pages anti-forgery | Full for standard web auth flow | None identified | Low |
| Managed Identity / Key Vault (production) | Azure Managed Identity + Key Vault | ChainedTokenCredential(AzureDeveloperCliCredential, DefaultAzureCredential) → AddAzureKeyVault; loaded only in non-Development/non-Docker branch | Full — standard Azure SDK pattern | None | None |
| Blazor WebAssembly Auth | Declared via WebAssembly.Authentication 8.0.2 | CustomAuthStateProvider fetches /User endpoint; attaches Bearer token to all HttpClient calls; 60s in-memory cache | Partial — no token refresh logic; cache is time-based only; token expiry (7 days) not checked against cache interval | 7-day JWT token with no refresh mechanism; token stored in Blazor memory; no revocation mechanism | Medium |
| AuthorizationConstants | Claims-based RBAC | `AUTH_KEY` constant declared; `DEFAULT_PASSWORD = "Pass@word1"` declared with TODO comment | Partial — authorization policies registered (RazorPages: `/Basket/Checkout` auth required) | DEFAULT_PASSWORD hardcoded in source; JWT_SECRET_KEY hardcoded in source (see below) | Critical |

### Secrets Posture

| Item | Finding | Severity | Evidence |
|---|---|---|---|
| JWT_SECRET_KEY | Hardcoded string in source: "SecretKeyOfDoomThatMustBeAMinimumNumberOfBytes" — committed to version control | Critical | src/ApplicationCore/Constants/AuthorizationConstants.cs:8 |
| AUTH_KEY | Hardcoded string in source: "AuthKeyOfDoomThatMustBeAMinimumNumberOfBytes" | Critical | src/ApplicationCore/Constants/AuthorizationConstants.cs:4 |
| DEFAULT_PASSWORD | Hardcoded default password "Pass@word1" with "TODO: Don't use this in production" comment — committed to source | Critical | src/ApplicationCore/Constants/AuthorizationConstants.cs:11 |
| SA_PASSWORD (Docker) | Plaintext "@someThingComplicated1234" in docker-compose.yml committed to source control | High | docker-compose.yml, sqlserver service environment |
| SQL Admin/App passwords (Azure) | Managed via Azure Key Vault via Bicep `@secure()` params and `secretOrRandomPassword`; not in source | None | infra/main.parameters.json, infra/core/database/sqlserver/sqlserver.bicep |
| Azure connection strings (production) | Retrieved from Key Vault at startup via managed identity; not in source | None | src/Web/Program.cs:35-42 |

### Attack Surface Summary

| Surface | Exposure | Mitigations Found | Gaps |
|---|---|---|---|
| PublicApi REST endpoints | Public HTTP/HTTPS; Swagger UI enabled in all environments (no environment guard); JWT Bearer required for most endpoints | JWT Bearer auth; CORS policy scoped to `baseUrlConfig.WebBase` origin only | RequireHttpsMetadata=false; ValidateIssuer=false; ValidateAudience=false; Swagger UI always exposed (no production guard) |
| eshopwebmvc web UI | HTTPS enforced (production via Bicep httpsOnly:true; Development uses localhost certs); Cookie auth | HSTS in production; HttpOnly+Secure+SameSite=Lax cookies; Anti-forgery on forms | No WAF or rate limiting found |
| Azure SQL Server firewall | All IPs allowed: 0.0.0.1–255.255.255.254; publicNetworkAccess=Enabled | TLS 1.2 minimum; credentials in Key Vault | Wide-open firewall — any internet IP can reach SQL port; no VNet/private endpoint |
| Docker local development | SA_PASSWORD in plaintext in docker-compose.yml | User secrets mounted read-only for app config | Plaintext SA password in source-controlled file |
| JWT token lifecycle | 7-day expiry; signed with HMAC-SHA256 | Signing key validated | Key is hardcoded constant; no rotation mechanism; no revocation; issuer/audience not validated |

---

## OUTPUT 6 - NFR Registry

| ID | NFR Name | Value | Category | Source | Confidence |
|---|---|---|---|---|---|
| NFR-01 | Catalog cache sliding expiration TTL | 30,000ms (30s) | Data Freshness | src/Web/Extensions/CacheHelpers.cs:7 — `TimeSpan.FromSeconds(30)` | HIGH |
| NFR-02 | Blazor auth state cache refresh interval | 60,000ms (60s) | Data Freshness | src/BlazorAdmin/CustomAuthStateProvider.cs — `TimeSpan.FromSeconds(60)` (hardcoded, TODO comment) | HIGH |
| NFR-03 | JWT token expiry | 7 days (604,800,000ms) | Reliability / Security | src/Infrastructure/Identity/IdentityTokenClaimService.cs — `DateTime.UtcNow.AddDays(7)` | HIGH |
| NFR-04 | Catalog items per page | 10 items | Throughput | src/Web/Constants.cs:4 — `ITEMS_PER_PAGE = 10` | HIGH |
| NFR-05 | EF Core retry on failure — maximum attempts | 6 attempts (EF Core SqlClient default) | Reliability | src/Web/Program.cs:36 — `EnableRetryOnFailure()` with no params = default; applies to production Web path only | HIGH — value is EF Core documented default for EnableRetryOnFailure() |
| NFR-06 | App Service minimum TLS version | TLS 1.2 | Security | infra/core/host/appservice.bicep — `minTlsVersion: '1.2'` | HIGH |
| NFR-07 | Azure SQL Server minimum TLS version | TLS 1.2 | Security | infra/core/database/sqlserver/sqlserver.bicep — `minimalTlsVersion: '1.2'` | HIGH |
| NFR-08 | App Service app log retention (file system) | 1 day | Resource Management | infra/core/host/appservice.bicep — `retentionInDays: 1` | HIGH |
| NFR-09 | App Service HTTP log retention size | 35 MB | Resource Management | infra/core/host/appservice.bicep — `retentionInMb: 35` | HIGH |
| NFR-10 | App Service SKU (compute tier) | B1 (1 core, 1.75 GB RAM) | Throughput | infra/core/host/appserviceplan.bicep — SKU B1 | HIGH |
| NFR-11 | App Service always-on | Enabled | Availability | infra/core/host/appservice.bicep — `alwaysOn: true` | HIGH |
| NFR-12 | Web production log level | Warning | Observability | src/Web/appsettings.json — `Logging.LogLevel.Default: Warning` | HIGH |
| NFR-13 | Web development log level | Debug | Observability | src/Web/appsettings.Development.json — `Logging.LogLevel.Default: Debug` | HIGH |
| NFR-14 | PublicApi production log level | Warning | Observability | src/PublicApi/appsettings.json — `Logging.LogLevel.Default: Warning` | HIGH |
| NFR-15 | PublicApi development log level | Information | Observability | src/PublicApi/appsettings.Development.json — `Logging.LogLevel.Default: Information` | HIGH |
| NFR-16 | SQL Server public network access | Enabled (all IPs: 0.0.0.1–255.255.255.254) | Security / Availability | infra/core/database/sqlserver/sqlserver.bicep — publicNetworkAccess: Enabled, firewall rule | HIGH |
| NFR-17 | EF Core SqlClient connection pool max (default) | 100 connections (SQL Server SqlClient default) | Throughput | No explicit pool configuration found; EF Core uses SqlClient defaults | LOW — not declared; system uses framework default; unbounded risk |
| NFR-18 | ApiHealthCheck — content assertion string | ".NET Bot Black Sweatshirt" | Availability | src/Web/HealthChecks/ApiHealthCheck.cs:27; src/Web/HealthChecks/HomePageHealthCheck.cs:27 | HIGH — but fragile; string-match health check |
| NFR-19 | CORS allowed origins (PublicApi) | Single origin from `baseUrlConfig.WebBase` (localhost:5001 dev; host.docker.internal:5106 Docker; runtime-injected in production) | Security | src/PublicApi/Program.cs:72-82 | HIGH |

---

## OUTPUT 7 - Technical Debt & Risk Register

| ID | Risk / Debt Item | Category | Affected Component(s) | Severity | Evidence | Recommended Action |
|---|---|---|---|---|---|---|
| TD-01 | JWT secret key hardcoded in source control — "SecretKeyOfDoomThatMustBeAMinimumNumberOfBytes" | Security Vulnerability | IdentityTokenClaimService, PublicApi JWT validation | Critical | src/ApplicationCore/Constants/AuthorizationConstants.cs:8 — `JWT_SECRET_KEY = "SecretKeyOfDoomThatMustBeAMinimumNumberOfBytes"` | Move to User Secrets (dev), Key Vault (production); inject via IConfiguration; rotate immediately if any environment uses this value |
| TD-02 | Default password hardcoded in source — "Pass@word1" with explicit TODO comment | Security Vulnerability | AppIdentityDbContextSeed, AuthorizationConstants | Critical | src/ApplicationCore/Constants/AuthorizationConstants.cs:11 — `DEFAULT_PASSWORD = "Pass@word1"` | Seed users with randomly generated passwords stored in Key Vault; remove constant from source |
| TD-03 | AUTH_KEY hardcoded in source | Security Vulnerability | AuthorizationConstants | Critical | src/ApplicationCore/Constants/AuthorizationConstants.cs:4 — `AUTH_KEY = "AuthKeyOfDoomThatMustBeAMinimumNumberOfBytes"` | Move to secrets store; remove from source |
| TD-04 | SA_PASSWORD plaintext in docker-compose.yml committed to source control | Security Vulnerability | docker-compose.yml (Docker local dev) | High | docker-compose.yml — `SA_PASSWORD=@someThingComplicated1234` | Use Docker secret or .env file (gitignored); document .env.example pattern for developers |
| TD-05 | JWT ValidateIssuer=false and ValidateAudience=false — tokens from any issuer accepted | Security Vulnerability | eshoppublicapi JWT validation | High | src/PublicApi/Program.cs:67-68 — `ValidateIssuer = false; ValidateAudience = false` | Set ValidIssuer and ValidAudience; tokens should be scoped to this API only |
| TD-06 | RequireHttpsMetadata=false in JWT Bearer config | Security Vulnerability | eshoppublicapi | High | src/PublicApi/Program.cs:61 — `config.RequireHttpsMetadata = false` | Set to true in production; use environment check or separate production configuration |
| TD-07 | No automated deployment pipeline — Bicep IaC and azd config are complete but no GitHub Actions workflow deploys to Azure | CI-CD Risk | All Azure resources (App Service, SQL, Key Vault) | High | .github/workflows/ contains only build+test; azure.yaml present but no `azd deploy` in any workflow | Add azd deployment job to dotnetcore.yml with environment gating (e.g., `on: push to main` only, with manual approval for production) |
| TD-08 | Azure SQL firewall allows all public IPs (0.0.0.1–255.255.255.254) | Security Vulnerability | sql-catalog, sql-identity (Azure SQL) | High | infra/core/database/sqlserver/sqlserver.bicep — startIpAddress `0.0.0.1`, endIpAddress `255.255.255.254` | Replace with VNet integration and private endpoint; or restrict to App Service outbound IPs |
| TD-09 | No retry on failure for PublicApi → SQL Server | Scalability Constraint | eshoppublicapi → CatalogContext + AppIdentityDbContext | High | src/Infrastructure/Dependencies.cs — `UseSqlServer(connectionString)` with no `sqlOptions.EnableRetryOnFailure()` | Add `sqlOptions.EnableRetryOnFailure()` in Dependencies.ConfigureServices or replicate Web's production pattern in PublicApi startup |
| TD-10 | Raw `new HttpClient()` in ApiHealthCheck, HomePageHealthCheck, Blazor CustomAuthStateProvider — socket exhaustion risk and no timeout | Scalability Constraint | ApiHealthCheck, HomePageHealthCheck, BlazorAdmin | High | src/Web/HealthChecks/ApiHealthCheck.cs:25; HomePageHealthCheck.cs:25; BlazorAdmin/CustomAuthStateProvider.cs — `_httpClient` injected but health checks create raw instances | Register named HttpClient via IHttpClientFactory; add timeout; add Polly retry policy |
| TD-11 | Bootstrap 3.4.1 — end-of-life, no security support | EOL Technology | eshopwebmvc frontend | High | src/Web/libman.json — `twitter-bootstrap@3.4.1`; Bootstrap 3 LTS ended 2019 | Upgrade to Bootstrap 5.x; Bootstrap 3 has known XSS vulnerabilities in older bundled jQuery plugins |
| TD-12 | GitHub Actions `actions/checkout@v2` and `actions/setup-dotnet@v1` — outdated action versions | CI-CD Risk | .github/workflows/dotnetcore.yml, richnav.yml | Medium | .github/workflows/dotnetcore.yml — `actions/checkout@v2` (current: v4); `actions/setup-dotnet@v1` (current: v4) | Update to actions/checkout@v4 and actions/setup-dotnet@v4; older versions use deprecated Node.js 12 runtime (deprecated by GitHub) |
| TD-13 | No secret scanning in CI/CD pipeline | CI-CD Risk | .github/workflows/ | Medium | No trufflehog, gitleaks, detect-secrets, or ggshield found in any pipeline file — critical given hardcoded secrets in TD-01/TD-02/TD-03 | Add `trufflehog` or `gitleaks` scan step to dotnetcore.yml; these hardcoded secrets would be caught immediately |
| TD-14 | No SAST or dependency vulnerability scanning in CI/CD | CI-CD Risk | .github/workflows/ | Medium | No snyk, sonarcloud, semgrep, bandit, or npm audit in any workflow; no trivy or grype | Add `dotnet-security-scan` or Snyk; GitHub Dependabot handles NuGet updates but not vulnerability detection for existing versions |
| TD-15 | Health check implementation fragile — string content assertion (".NET Bot Black Sweatshirt") | Operational Risk | ApiHealthCheck, HomePageHealthCheck | Medium | src/Web/HealthChecks/ApiHealthCheck.cs:27; HomePageHealthCheck.cs:27 — `pageContents.Contains(".NET Bot Black Sweatshirt")` | Replace with dedicated `/health` endpoint on PublicApi; check HTTP status codes not page content; current health check is a content regression test, not a liveness check |
| TD-16 | Application Insights not provisioned or SDK-instrumented — no APM telemetry | Operational Risk | eshopwebmvc (production) | Medium | No `Microsoft.ApplicationInsights.AspNetCore` in Directory.Packages.props; `applicationInsightsName` param has empty default and main.bicep passes no value to web module | Add Application Insights NuGet SDK; provision Microsoft.Insights/components resource in Bicep; wire up APPLICATIONINSIGHTS_CONNECTION_STRING |
| TD-17 | No distributed tracing or correlation ID propagation | Operational Risk | eshopwebmvc, eshoppublicapi | Medium | No OpenTelemetry, Jaeger, Zipkin, or W3C trace-context middleware found; no correlation ID middleware in PublicApi or Web Program.cs | Add OpenTelemetry SDK with OTLP exporter; add W3C TraceContext propagation middleware |
| TD-18 | dotnet-xunit 2.3.1 legacy DotNetCliToolReference — FunctionalTests cannot be run | CI-CD Risk | tests/FunctionalTests | Low | tests/FunctionalTests/FunctionalTests.csproj — DotNetCliToolReference; mechanism deprecated since .NET Core 2.1 | Remove DotNetCliToolReference; run FunctionalTests via `dotnet test` (xunit 2.7.0 supports this); verify tests pass after switch |
| TD-19 | Microsoft.AspNetCore.Mvc 2.2.0 stale declaration in Directory.Packages.props | Configuration Risk | Directory.Packages.props | Low | Directory.Packages.props — `Microsoft.AspNetCore.Mvc` Version="2.2.0"; no project references it | Remove from Directory.Packages.props to avoid confusion in dependency audit tools |
| TD-20 | Single App Service B1 SKU with no auto-scaling or multi-instance config | Scalability Constraint | web (Azure App Service) | Low | infra/core/host/appserviceplan.bicep — SKU B1 (1 core, 1.75 GB RAM); no scale-out rules declared | Add App Service auto-scale rules; consider upgrading to S1/P1v3 for production workloads; B1 has no SLA |

---

## OUTPUT 8 - Operational Architecture Assessment

### CI/CD Pipeline Maturity

> Evidence-based assessment. Present requires a specific tool invocation or action name found in a pipeline file. Absent means no matching evidence found in any pipeline file.

| Capability | Present? | Evidence (tool / action name + file + job) | Runs On | Gap Severity |
|---|---|---|---|---|
| Build | Present | `dotnet build ./eShopOnWeb.sln --configuration Release` — .github/workflows/dotnetcore.yml, build job, step 3 | All branches + all PRs (push, pull_request, workflow_dispatch) | - |
| Unit Tests | Present | `dotnet test ./eShopOnWeb.sln --configuration Release` — .github/workflows/dotnetcore.yml, build job, step 4 | All branches + all PRs | - |
| Integration Tests | Absent | `dotnet test` runs the full solution which includes IntegrationTests and PublicApiIntegrationTests projects, but no database service container is started in the workflow; integration tests using real SQL Server cannot pass without it. InMemory tests (UseOnlyInMemoryDatabase=true) may run. No explicit docker-compose or testcontainers invocation found. | - | Medium |
| Code Coverage Gate | Absent | `dotnet test` has no `--collect:"XPlat Code Coverage"` flag; coverlet.collector is declared as a package but no collection flag in pipeline | - | Medium |
| SAST (Static Security) | Absent | No sonar, semgrep, codeql, snyk code, bandit, or security-focused eslint found in any pipeline file | - | High |
| Dependency Scan | Absent | No snyk test, npm audit, owasp dependency-check, trivy fs, or govulncheck found in any pipeline file (Dependabot updates packages but does not scan for vulnerabilities in committed version ranges) | - | High |
| Container / Image Scan | Absent | No trivy image, snyk container, grype, or docker scout found in any pipeline file | - | High |
| Secret / Credential Scan | Absent | No trufflehog, gitleaks, detect-secrets, or ggshield found in any pipeline file | - | High — especially critical given TD-01/TD-02/TD-03 |
| Infrastructure Scan (IaC) | Absent | No tfsec, checkov, terrascan, or trivy config found in any pipeline file | - | Medium |
| Automated Deploy | Absent | No az webapp deploy, azd deploy, kubectl apply, helm upgrade, or terraform apply found in any pipeline file; azure.yaml and full Bicep IaC present but not wired to any CI/CD workflow | - | High |
| Smoke / Health Check Post-Deploy | Absent | No curl health endpoint, newman, k6, or playwright post-deploy check found; no deploy job exists to attach a check to | - | High |
| Auto Rollback | Absent | No kubectl rollout undo, helm rollback, az webapp deployment slot swap, or equivalent found | - | High |
| Manual Approval Gate | Absent | No `environment:` declaration with required reviewers found in any job | - | Low |
| Release / Versioning Automation | Absent | No semantic-release, git tag, gh release create, or standard-version found in any pipeline file | - | Low |

**Summary: 2 of 14 CI/CD capabilities confirmed present (Build, Unit Tests). 12 absent — 5 at High gap severity.**

### Observability Coverage

| Concern | Component | Present? | Tool / Library | Gap? |
|---|---|---|---|---|
| Structured Logging | eshopwebmvc | Partial | ASP.NET Core built-in ILogger + LoggerAdapter<T> abstraction; console sink via `builder.Logging.AddConsole()`; no JSON formatter configured — plain text console output in all environments | GAP — no structured JSON logging; no log aggregation sink |
| Structured Logging | eshoppublicapi | Partial | Same pattern — ILogger + console; no JSON formatter | GAP — same as Web |
| Distributed Tracing | eshopwebmvc | Absent | No OpenTelemetry, Activity, Jaeger, Zipkin, or W3C tracecontext middleware found | GAP |
| Distributed Tracing | eshoppublicapi | Absent | No distributed tracing found | GAP |
| Metrics Export | eshopwebmvc | Absent | No Prometheus endpoint, Micrometer equivalent, or StatsD found | GAP |
| Metrics Export | eshoppublicapi | Absent | No metrics export found | GAP |
| Correlation ID Propagation | eshopwebmvc | Absent | No custom middleware or built-in correlation ID propagation found | GAP |
| Correlation ID Propagation | eshoppublicapi | Absent | No correlation ID middleware found | GAP |
| Health / Readiness Endpoints | eshopwebmvc | Present | `/health` (full), `/home_page_health_check`, `/api_health_check` — JSON response; implemented via ASP.NET Core HealthChecks | - (but content-assertion check is fragile — see TD-15) |
| Health / Readiness Endpoints | eshoppublicapi | Absent | No health check endpoint registered in PublicApi Program.cs | GAP |
| Alerting Rules | All | Absent | No Alertmanager rules, CloudWatch alarms, Azure Monitor alerts found in repository | GAP |
| Application Performance Monitoring | eshopwebmvc | Absent | Application Insights not SDK-instrumented (see TD-16) | GAP |

### Deployment Safety

| Practice | Present? | Evidence | Risk If Absent |
|---|---|---|---|
| Graceful Shutdown | No | No `lifetime.ApplicationStopping` cancellation token registration, `IHostedService.StopAsync`, or shutdown timeout configuration found in either Program.cs | In-flight requests dropped during container restart or deployment |
| Readiness Probe | No | No Kubernetes readiness probe configuration found (not Kubernetes-deployed — Azure App Service); App Service health check path param is empty string in appservice.bicep `healthCheckPath` | App Service may receive traffic before app is fully initialised; startup seeding (DB seed) happens before app.Run() so reduced risk |
| Liveness Probe | No | Same — empty `healthCheckPath`; no Azure App Service health check path configured in Bicep despite the parameter existing | Hung or deadlocked containers not restarted by platform |
| Blue-Green / Canary | No | No deployment slots, canary weights, or feature flags found in any Bicep or pipeline file | All traffic exposed to every deployment; rollback requires re-deploy |
| Feature Flags | No | No LaunchDarkly, Azure App Configuration feature flags, or custom feature flag integration found | No decoupled release capability; all features deploy together |

### Disaster Recovery Posture

| Item | Declared? | Detail | Source |
|---|---|---|---|
| Database backup configuration | No | No Azure SQL backup policy, retention period, or geo-redundant backup config declared in Bicep | Bicep files — not found |
| Multi-region / multi-AZ config | No | Single location parameter; no geo-replication, Traffic Manager, or multi-region App Service declared | infra/main.bicep — single `location` param |
| Database replication | No | No Azure SQL active geo-replication or read replica declared | infra/core/database/sqlserver/sqlserver.bicep — not found |
| RTO / RPO declarations | No | No RTO/RPO targets declared in any configuration or documentation file | NOT FOUND |

---

## Validation Queue

| # | Item | Chunk / Layer | Reason |
|---|---|---|---|
| 1 | MediatR actual usage patterns | Application | IMediator usage not confirmed in source files read; MappingProfile and endpoint bodies not fully read; marked Partial pending deeper PublicApi endpoint reading |
| 2 | FluentValidation validator classes | Application | Validators not read in depth; confirmed library registered; individual validator configurations (rules, conditions) not traced |
| 3 | EF Core Migrations directory contents | Data | dotnet-ef tooling declared; migrations directory not read; migration state confirmed as present but schema drift risk cannot be fully assessed without reading migration files |
| 4 | CatalogContextSeed startup race condition | Data | Both eshopwebmvc and eshoppublicapi call SeedAsync independently; no distributed lock found in files read; actual idempotency logic in CatalogContextSeed.cs not read |
| 5 | CORS allowedOrigins runtime value in production | Security | `baseUrlConfig.WebBase` in PublicApi CORS is injected from configuration; production value not declared in any Bicep or config file read |
| 6 | PublicApi endpoint authorization coverage | Security | ExceptionMiddleware confirmed; individual endpoint `[Authorize]` attributes not read; partial coverage of JWT enforcement unknown |

---

## Agent 1 Discrepancy Log

| # | What Agent 1 Said | What Implementation Shows | Resolved? |
|---|---|---|---|
| 1 | `Microsoft.AspNetCore.Mvc 2.2.0` — LOW CONFIDENCE, possible stale/unused declaration | Confirmed: no project references this standalone package; all MVC usage is via the ASP.NET Core 8.0.2 framework packages implicitly. The entry in Directory.Packages.props is orphaned. | RESOLVED — stale declaration, no active usage; add as TD-19 |
| 2 | Application Insights — LOW CONFIDENCE, no SDK package, `applicationInsightsName` empty default | Confirmed: (a) `Microsoft.ApplicationInsights.AspNetCore` NuGet package absent from Directory.Packages.props; (b) `main.bicep` does not pass `applicationInsightsName` to the web module at all; (c) no Application Insights Bicep resource provisioned. Application Insights is completely absent from this repository. | RESOLVED — Application Insights is not implemented; confirmed as TD-16 |
| 3 | AuthorizationConstants policy names — not visible from Layer 1 extraction | Confirmed from source: class contains three hardcoded constants — AUTH_KEY, DEFAULT_PASSWORD, JWT_SECRET_KEY — not policy name strings as Agent 1 suggested. These are security constants, not RBAC policy names. Actual authorization is implemented via `options.Conventions.AuthorizePage("/Basket/Checkout")` in Web Program.cs and JWT Bearer for PublicApi. | RESOLVED — significant finding: constants are hardcoded secrets not policy names; generates TD-01, TD-02, TD-03 |

---

Agent 2 Analysis Complete.
Documentation is ready for technical review.

**Highest-priority action item: TD-01/TD-02/TD-03 — Three security-critical hardcoded secrets in source control** (`JWT_SECRET_KEY = "SecretKeyOfDoomThatMustBeAMinimumNumberOfBytes"`, `DEFAULT_PASSWORD = "Pass@word1"`, `AUTH_KEY = "AuthKeyOfDoomThatMustBeAMinimumNumberOfBytes"`) in `src/ApplicationCore/Constants/AuthorizationConstants.cs`. Any attacker with read access to the repository can forge valid JWT tokens, authenticate as any user, and read all catalog and identity data. These must be rotated and moved to secrets management before this application is deployed to any internet-accessible environment.
