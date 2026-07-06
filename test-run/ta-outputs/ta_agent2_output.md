I now have all the evidence needed. Producing the full 8-output analysis.

---

## Agent 2 - Analysis Summary
- **Layers analysed:** 6 — Application, Security, Data, Infrastructure, CI/CD, Observability
- **Chunks processed:** 6 (Orientation + 5 layer deep-dives, collapsed into single synthesis given source evidence was read in parallel)
- **Technologies assessed:** 52
- **Architecture patterns catalogued:** 18 (AP-01 through AP-18)
- **NFR entries recorded:** 14 (NFR-01 through NFR-14)
- **Technical debt items identified:** 19 (TD-01 through TD-19) — Critical: 3, High: 9, Medium: 5, Low: 2
- **CI/CD pipeline files directly read:** 2 (0 reusable workflow files; no local `uses:` references found)
- **CI/CD capabilities confirmed present:** 3 of 14 (Build, Unit Tests, Dependency Scan via Dependabot)
- **Agent 1 LOW CONFIDENCE items resolved:** 8 of 13
- **Discrepancies with Agent 1:** 4

---

## ⚠️ CRITICAL SECURITY ESCALATION — Read Before Any Other Output

**Three hardcoded secrets committed to source control in `src/ApplicationCore/Constants/AuthorizationConstants.cs`:**

1. `JWT_SECRET_KEY = "SecretKeyOfDoomThatMustBeAMinimumNumberOfBytes"` — used LIVE at line 54 of `src/PublicApi/Program.cs` and line 26 of `src/Infrastructure/Identity/IdentityTokenClaimService.cs` to sign and validate all JWT tokens issued by the system.
2. `AUTH_KEY = "AuthKeyOfDoomThatMustBeAMinimumNumberOfBytes"` — declared in constants, available to any code referencing this class.
3. `DEFAULT_PASSWORD = "Pass@word1"` — used in `src/Infrastructure/Identity/AppIdentityDbContextSeed.cs` to create `demouser@microsoft.com` and `admin@microsoft.com` on every startup that runs the seeder against a real SQL Server.

**Impact:** Any developer, contributor, or attacker with repo access can forge valid JWT tokens accepted by the PublicApi. The `admin@microsoft.com` account (with Administrators role) is created on every fresh deployment with the publicly known password `Pass@word1`. These TODO comments acknowledge the risk but the code ships with live credentials.

**Required action before any production deployment:** Rotate all three values; move `JWT_SECRET_KEY` to Azure Key Vault; remove `DEFAULT_PASSWORD` from source entirely.

---

## OUTPUT 1 - Technology Stack Assessment

| Component | Declared Version | Usage Depth | How It Is Used in This System | EOL / Support Status | Agent 1 Match? |
|---|---|---|---|---|---|
| .NET SDK | 8.0.x (rollForward: latestFeature) | Active - core path | All projects target net8.0; rollForward allows patch-level advancement | LTS until November 2026 | Confirmed |
| ASP.NET Core | 8.0.2 | Active - core path | MVC + Razor Pages (Web); Minimal API (PublicApi); middleware pipeline for both services | LTS until November 2026 | Confirmed |
| Blazor WebAssembly | 8.0.2 | Active - core path | BlazorAdmin WASM panel hosted inside Web; custom AuthStateProvider; client-side rendering | LTS until November 2026 | Confirmed |
| Entity Framework Core (SqlServer) | 8.0.2 | Active - core path | `CatalogContext` (Baskets, CatalogItems, Orders, OrderItems, BasketItems, CatalogBrands, CatalogTypes); `AppIdentityDbContext` (ASP.NET Identity tables); `EnableRetryOnFailure()` in production path only | Supported | Confirmed |
| Entity Framework Core (InMemory) | 8.0.2 | Active - secondary | `Dependencies.ConfigureServices()` branches on `UseOnlyInMemoryDatabase` config flag; used by FunctionalTests and PublicApiIntegrationTests | Supported | Confirmed |
| MediatR | 12.0.1 | Partial | Used only in Web project for read-side queries: `GetMyOrdersHandler`, `GetOrderDetailsHandler`; NOT used for write operations (BasketService, OrderService bypass MediatR) | Supported | Confirmed |
| FluentValidation | 11.9.0 | Active - secondary | Declared in central props; used by PublicApi request validation; not directly evidenced in scanned endpoints but consistent with MinimalApi.Endpoint pattern | Supported | Confirmed |
| AutoMapper | 12.0.1 | Partial | Used in `CatalogItemListPagedEndpoint` to map `CatalogItem` → `CatalogItemDto`; `MappingProfile` registered in PublicApi; not present in Web | Supported | Confirmed |
| Ardalis.Specification | 7.0.0 | Active - core path | 8 specification classes used for ALL entity queries; `IReadRepositoryBase<T>` consumed throughout | Supported | Confirmed |
| Ardalis.Specification.EntityFrameworkCore | 7.0.0 | Active - core path | `EfRepository<T>` extends `RepositoryBase<T>`; single repository implementation for all aggregates | Supported | Confirmed |
| Ardalis.ApiEndpoints | 4.1.0 | Active - core path | `AuthenticateEndpoint` uses `EndpointBaseAsync`; mixed with MinimalApi.Endpoint pattern in same service | Supported | Confirmed |
| Ardalis.GuardClauses | 4.0.1 | Active - core path | Used in `BasketItem`, `Basket`, `Buyer`, `Order`, `CatalogItem`, `OrderService`, `CheckoutModel`; custom extension `Guard.Against.EmptyBasketOnCheckout` | Supported | Confirmed |
| Ardalis.Result | 7.0.0 | Partial | Used in `IBasketService.SetQuantities` return type; `BasketService` returns `Result<Basket>.NotFound()`; not pervasive | Supported | Confirmed |
| Ardalis.ListStartupServices | 1.1.4 | Active - secondary | `app.UseShowAllServicesMiddleware()` registered in Development/Docker only | Supported | Confirmed |
| MinimalApi.Endpoint | 1.3.0 | Active - core path | All catalog, brand, type endpoints in PublicApi use `IEndpoint<TResult, TRequest, TService>` pattern; `app.MapEndpoints()` at startup | Supported | Confirmed |
| Swashbuckle.AspNetCore | 6.5.0 | Active - secondary | OpenAPI spec at `/swagger/v1/swagger.json`; SwaggerUI at `/swagger`; Bearer security definition added; enabled only in PublicApi | Supported | Confirmed |
| Microsoft.AspNetCore.Authentication.JwtBearer | 8.0.2 | Active - core path | JWT Bearer configured in `PublicApi/Program.cs` with HMAC-SHA256 signing key from `AuthorizationConstants.JWT_SECRET_KEY` | Supported | Confirmed |
| Microsoft.AspNetCore.Identity.EntityFrameworkCore | 8.0.2 | Active - core path | `AppIdentityDbContext : IdentityDbContext<ApplicationUser>`; seeded with admin/demo users on startup | Supported | Confirmed |
| System.IdentityModel.Tokens.Jwt | 7.3.1 | Active - core path | `JwtSecurityTokenHandler.CreateToken()` in `IdentityTokenClaimService`; 7-day token expiry; HMAC-SHA256 | Supported | Confirmed |
| Azure.Identity | 1.10.4 | Partial | Used in Web/Program.cs production branch only: `new ChainedTokenCredential(new AzureDeveloperCliCredential(), new DefaultAzureCredential())`; NOT used in PublicApi at all | Supported | Confirmed |
| Azure.Extensions.AspNetCore.Configuration.Secrets | 1.3.1 | Partial | `builder.Configuration.AddAzureKeyVault(...)` in Web/Program.cs production branch only; PublicApi has no Key Vault integration | Supported | Confirmed |
| Microsoft.AspNetCore.Diagnostics.EntityFrameworkCore | 8.0.2 | Active - secondary | `app.UseMigrationsEndPoint()` registered in Development/Docker only | Supported | Confirmed |
| Microsoft.Extensions.Logging.Configuration | 8.0.0 | Active - core path | `builder.Logging.AddConsole()` in both Web and PublicApi Program.cs; log levels configured per environment in appsettings | Supported | Confirmed |
| Blazored.LocalStorage | 4.5.0 | Active - core path | Used by `CachedCatalogItemServiceDecorator` and `CachedCatalogLookupDataServiceDecorator` to cache catalog data in browser localStorage; 1-minute TTL | Supported | Confirmed |
| Bootstrap | 3.4.1 | Active - secondary | CSS framework delivered via cdnjs; Bootstrap 3 series | EOL: 2019 (Bootstrap 3 unmaintained; Bootstrap 5 current) | Confirmed |
| aspnet-signalr (client) | 1.0.27 | Declared-only — no server usage found | Client JS library declared in libman.json; no `app.MapHub<T>()` or `builder.Services.AddSignalR()` found in either Program.cs | LOW - no server-side hub registration found | Confirmed - LOW |
| Microsoft.AspNetCore.Mvc | 2.2.0 | Declared-only — no usage evidence | In Directory.Packages.props but no PackageReference found in any .csproj scanned | EOL: April 2022 (ASP.NET Core 2.2) | Confirmed - LOW, DISCREPANCY: version incompatible with net8.0 |
| Azure Application Insights | v2020-02-02 (existing ref) | Partial | `APPLICATIONINSIGHTS_CONNECTION_STRING` env key injected conditionally by Bicep; no provisioning Bicep module found; no SDK usage found in application source | LOW - env key only; no provisioning found | Confirmed - LOW |
| dotnet-xunit | 2.3.1 | Declared-only | DotNetCliToolReference in FunctionalTests.csproj; deprecated format | LOW - deprecated format | Confirmed - LOW |
| coverlet.collector | 6.0.2 | Declared-only in CI context | Declared in central props; `dotnet test` in CI does NOT include `--collect:"XPlat Code Coverage"` flag | Active in local dev; Declared-only in CI (no coverage gate) | Confirmed |
| EmailSender (IEmailSender) | N/A | Declared-only — stub | `EmailSender.SendEmailAsync()` returns `Task.CompletedTask`; TODO comment present; no SMTP/SendGrid integration | N/A - stub | New - not in Agent 1 |
| Azure SQL Server | v12.0 | Active - core path | Two databases: `catalogDatabase` (CatalogContext) and `identityDatabase` (AppIdentityDbContext); `EnableRetryOnFailure()` in production path | Supported | Confirmed |
| Azure App Service | dotnetcore\|8.0, B1 Linux | Active - core path | Web service only deployed here per azure.yaml; `alwaysOn: true`; SystemAssigned Managed Identity | Supported | Confirmed |
| Azure Key Vault | standard SKU | Partial | Web service reads secrets at startup (production only); PublicApi has NO Key Vault integration | Supported | Confirmed |

---

## OUTPUT 2 - Architecture Pattern Catalog

| ID | Pattern Name | Category | Applies To | Exact Configuration | Coverage | Confidence | Source |
|---|---|---|---|---|---|---|---|
| AP-01 | Ardalis Specification / Repository Query Object | Data Access | All domain aggregate queries (Basket, CatalogItem, CatalogBrand, CatalogType, Order) via EfRepository | 8 specification classes: `BasketWithItemsSpecification`, `CatalogFilterPaginatedSpecification`, `CatalogFilterSpecification`, `CatalogItemNameSpecification`, `CatalogItemsSpecification`, `CustomerOrdersSpecification`, `CustomerOrdersWithItemsSpecification`, `OrderWithItemsByIdSpec` | Applied everywhere it should be for reads and writes | HIGH | `src/ApplicationCore/Specifications/` (all files), `src/Infrastructure/Data/EfRepository.cs` |
| AP-02 | Generic Repository Pattern | Data Access | All `IAggregateRoot`-implementing entities: Basket, CatalogItem, CatalogBrand, CatalogType, Order, Buyer | Single implementation `EfRepository<T> : RepositoryBase<T>, IReadRepository<T>, IRepository<T>` backed by `CatalogContext` only; `IReadRepository<T>` for read-only access; `IRepository<T>` for full CRUD | Applied everywhere; `Buyer` aggregate has no `DbSet<Buyer>` in CatalogContext — persistence gap | HIGH | `src/Infrastructure/Data/EfRepository.cs`, `src/Web/Configuration/ConfigureCoreServices.cs:15-16` |
| AP-03 | Mediator Pattern (Command/Query via MediatR) | Application | Web project read path only: `GetMyOrdersHandler`, `GetOrderDetailsHandler` | `AddMediatR(cfg => cfg.RegisterServicesFromAssembly(...))` in `ConfigureWebServices.cs`; `IRequestHandler<GetMyOrders, IEnumerable<OrderViewModel>>`; write path (BasketService, OrderService) does NOT use MediatR | Partial — read queries only in Web; PublicApi and all writes bypass MediatR | HIGH | `src/Web/Configuration/ConfigureWebServices.cs:11`, `src/Web/Features/MyOrders/GetMyOrdersHandler.cs` |
| AP-04 | DDD Aggregate Root Pattern | Data Access | `Basket`, `Order`, `Buyer` (all implement `IAggregateRoot`) | Private backing collections (`_items`, `_orderItems`, `_paymentMethods`) exposed as `IReadOnlyCollection<T>`; all mutation through Aggregate methods only (`AddItem`, `RemoveEmptyItems`, `SetQuantity`); `BuyerId` string (email) as cross-context identity link | Applied to all three aggregates; `CatalogItem`, `CatalogBrand`, `CatalogType` also implement `IAggregateRoot` as single-entity roots | HIGH | `src/ApplicationCore/Entities/BasketAggregate/Basket.cs`, `src/ApplicationCore/Entities/OrderAggregate/Order.cs` |
| AP-05 | Value Object Pattern (EF Owned Entity) | Data Access | `Address` (owned by `Order`), `CatalogItemOrdered` (owned by `OrderItem`) | `builder.OwnsOne(o => o.ShipToAddress)` with nested column constraints: ZipCode max 18, Street max 180, State max 60, Country max 90, City max 100; `builder.Navigation(x => x.ShipToAddress).IsRequired()` | Applied to Address and CatalogItemOrdered consistently | HIGH | `src/Infrastructure/Data/Config/OrderConfiguration.cs:19-43` |
| AP-06 | Guard Clause Pattern | Application | All domain entity constructors, service methods, page models | Ardalis.GuardClauses: `Guard.Against.Null`, `Guard.Against.NullOrEmpty`, `Guard.Against.OutOfRange`, `Guard.Against.NegativeOrZero`, `Guard.Against.Zero`, `Guard.Against.EmptyBasketOnCheckout` (custom extension in `GuardExtensions.cs`) | Applied throughout domain and service layer | HIGH | `src/ApplicationCore/Extensions/GuardExtensions.cs`, `src/ApplicationCore/Entities/BasketAggregate/BasketItem.cs`, `src/ApplicationCore/Services/OrderService.cs` |
| AP-07 | Cache-Aside with Decorator Pattern (Server-side) | Caching | `ICatalogViewModelService` in Web project | `CachedCatalogViewModelService` wraps `CatalogViewModelService`; uses `IMemoryCache.GetOrCreateAsync()`; sliding expiration: **30,000ms (30s)** (`CacheHelpers.DefaultCacheDuration = TimeSpan.FromSeconds(30)`); 3 cache keys: `"brands"`, `"types"`, `"items-{pageIndex}-{itemsPage}-{brandId}-{typeId}"` | Applied to catalog read path only in Web; write-through invalidation absent (cache expires naturally) | HIGH | `src/Web/Services/CachedCatalogViewModelService.cs`, `src/Web/Extensions/CacheHelpers.cs:7` |
| AP-08 | Cache-Aside with Decorator Pattern (Client-side Browser) | Caching | `ICatalogItemService`, `ICatalogLookupDataService<T>` in BlazorAdmin | `CachedCatalogItemServiceDecorator` and `CachedCatalogLookupDataServiceDecorator` wrap HTTP services; cache in `Blazored.LocalStorage`; TTL: **60,000ms (1 min)** (`DateCreated.AddMinutes(1)`); write operations trigger explicit cache refresh via `RefreshLocalStorageList()`; fixed cache key `"items"` for all catalog items | Applied to all BlazorAdmin read operations; write path invalidates and re-populates correctly | HIGH | `src/BlazorAdmin/Services/CachedCatalogItemServiceDecorator.cs:34`, `src/BlazorAdmin/Services/CachedCatalogLookupDataServiceDecorator.cs:38` |
| AP-09 | Cookie Authentication with Token Revocation | Security | Web project session management | `CookieAuthenticationDefaults.AuthenticationScheme`; `HttpOnly=true`; `SecurePolicy=Always`; `SameSite=Lax`; cookie name `EshopIdentifier`; expiry: **60 minutes** (`ValidityMinutesPeriod = 60`); revocation: `UserController.Logout()` stores `{userId}:{identityKey}` in `IMemoryCache` with absolute expiry matching cookie validity; `RevokeAuthenticationEvents` checks this on each request | Applied only to Web; PublicApi uses JWT only | HIGH | `src/Web/Program.cs:47-53`, `src/Web/Configuration/ConfigureCookieSettings.cs`, `src/Web/Controllers/UserController.cs:44-56` |
| AP-10 | JWT Bearer Authentication with RBAC | Security | PublicApi — all mutation endpoints | `JwtBearerDefaults.AuthenticationScheme`; key: `AuthorizationConstants.JWT_SECRET_KEY` (HMAC-SHA256 hardcoded); `ValidateIssuerSigningKey=true`; `ValidateIssuer=false`; `ValidateAudience=false`; `RequireHttpsMetadata=false`; token lifetime: **7 days**; roles enforced via `[Authorize(Roles = "Administrators", AuthenticationSchemes = JwtBearerDefaults.AuthenticationScheme)]` on CreateCatalogItem, DeleteCatalogItem, UpdateCatalogItem; READ endpoints (`GET catalog-items`, `GET catalog-items/{id}`, brand list, type list) have NO authorization | Partial — RBAC on writes only; reads are open; issuer/audience not validated | HIGH | `src/PublicApi/Program.cs:54-70`, `src/PublicApi/CatalogItemEndpoints/CreateCatalogItemEndpoint.cs:30`, `src/PublicApi/CatalogItemEndpoints/DeleteCatalogItemEndpoint.cs:21` |
| AP-11 | Custom Auth State Provider (Blazor Token Relay) | Security | BlazorAdmin ↔ Web ↔ PublicApi | `CustomAuthStateProvider` fetches `UserInfo` (including JWT token) from Web's `/User` endpoint; caches `ClaimsPrincipal` for **60,000ms (60s)**; attaches token as `Authorization: Bearer {token}` header on all subsequent `HttpClient` calls to PublicApi; `UserCacheRefreshInterval = TimeSpan.FromSeconds(60)` hardcoded (TODO comment acknowledges this) | Applied to BlazorAdmin only | HIGH | `src/BlazorAdmin/CustomAuthStateProvider.cs:10,34-35,59` |
| AP-12 | SQL Retry on Failure (EF Core Resilience) | Resilience | Web (production path) → Azure SQL connections | `sqlOptions.EnableRetryOnFailure()` with default configuration (EF Core default: max 6 attempts, 30s max delay, transient SQL error codes) on BOTH `CatalogContext` and `AppIdentityDbContext`; ONLY in the production/Azure branch of `Web/Program.cs` (inside `else` block); Development/Docker and PublicApi have NO retry configured | Partial — production Web only; PublicApi and development paths have no retry | HIGH | `src/Web/Program.cs:36,41` |
| AP-13 | HiLo Key Generation | Data Access | `CatalogItem` entity | `builder.Property(ci => ci.Id).UseHiLo("catalog_hilo")` — server-side hi-lo sequence named `catalog_hilo`; other entities use default EF Core identity generation | Applied to CatalogItem only; Basket, Order, OrderItem use default identity | HIGH | `src/Infrastructure/Data/Config/CatalogItemConfiguration.cs:14-15` |
| AP-14 | Exception Middleware Pattern | Application | PublicApi global error handling | `ExceptionMiddleware` catches all unhandled exceptions; `DuplicateException` → HTTP 409 Conflict with `ErrorDetails` JSON body; all other exceptions → HTTP 500 with `exception.Message` exposed in response body (information leakage risk) | Applied to PublicApi only; Web uses `app.UseExceptionHandler("/Error")` in production | HIGH | `src/PublicApi/Middleware/ExceptionMiddleware.cs` |
| AP-15 | Content-Based Health Checks | Observability | Web project — 2 health check endpoints | `ApiHealthCheck`: HTTP GET to `{apiBase}catalog-items`, checks response body contains `.NET Bot Black Sweatshirt`; `HomePageHealthCheck`: HTTP GET to `{scheme}://{host}`, checks response body for same string; both exposed at `/health` (aggregate), `home_page_health_check`, `api_health_check`; BOTH instantiate `new HttpClient()` per invocation (no HttpClientFactory) | Applied to Web only; PublicApi has no health endpoint | HIGH | `src/Web/HealthChecks/ApiHealthCheck.cs`, `src/Web/HealthChecks/HomePageHealthCheck.cs`, `src/Web/Program.cs:87-89` |
| AP-16 | Account Lockout on Authentication Endpoint | Security | PublicApi `/api/authenticate` | `_signInManager.PasswordSignInAsync(username, password, isPersistent: false, lockoutOnFailure: true)` — account lockout IS enabled on failed login attempts | Applied to PublicApi authenticate endpoint only | HIGH | `src/PublicApi/AuthEndpoints/AuthenticateEndpoint.cs:44` |
| AP-17 | Basket Cookie (Anonymous Shopping) | Application | Web basket management for unauthenticated users | `Checkout.cshtml.cs` uses cookie key `Constants.BASKET_COOKIENAME`; anonymous basket ID: `Guid.NewGuid().ToString()`; cookie expiry: **10 years** (`DateTime.Today.AddYears(10)`); no `HttpOnly` flag set on basket cookie; transfers to user basket on login | Applied to Web basket flow | HIGH | `src/Web/Pages/Basket/Checkout.cshtml.cs:92-96` |
| AP-18 | Parallel Async Fan-Out (Client-side Read) | Application | BlazorAdmin CatalogItemService | `CatalogItemService.GetById()` and `List()` methods use `Task.WhenAll(brandListTask, typeListTask, itemGetTask)` to fire all three API calls concurrently; result enrichment done in-memory after all complete | Applied in BlazorAdmin service layer | HIGH | `src/BlazorAdmin/Services/CatalogItemService.cs:49-51, 63-66` |

### Pattern Coverage Gaps

| Gap | Affected Integration / Component | Severity | Recommendation |
|---|---|---|---|
| No retry / timeout on any database call in Development, Docker, or PublicApi paths | PublicApi → CatalogDb; PublicApi → IdentityDb; Web (Dev/Docker) → sqlserver | High | Add `EnableRetryOnFailure(maxRetryCount: 5, maxRetryDelay: TimeSpan.FromSeconds(30), errorNumbersToAdd: null)` to all `UseSqlServer()` calls in `Dependencies.ConfigureServices()` |
| JWT token issuer and audience not validated | PublicApi — all authenticated endpoints | Critical | Set `ValidateIssuer = true`, `ValidateAudience = true` with explicit `ValidIssuers` and `ValidAudiences` in `AddJwtBearer()` |
| No retry, timeout, or circuit breaker on outbound HTTP calls (health checks, BlazorAdmin API calls) | `ApiHealthCheck`, `HomePageHealthCheck`, `HttpService` in BlazorAdmin | High | Register typed `HttpClient` via `IHttpClientFactory` with `AddTransientHttpErrorPolicy` using Polly; add request timeouts |
| No structured/correlation-ID logging | All services — all request paths | Medium | Implement `ILogger<T>` structured logging with `{CorrelationId}` scope throughout; use `LoggerAdapter<T>` which is already wired |
| No cache invalidation on catalog writes (server-side) | `CachedCatalogViewModelService` — catalog items and brands written via PublicApi | Medium | Web's 30s cache will serve stale data after PublicApi mutations; implement eviction signal or shorten TTL further |
| No outbox / at-least-once delivery on order creation | `OrderService.CreateOrderAsync()` | Medium | No transactional outbox pattern; if email/notification fails after order save there is no retry |

### Declared-But-Unused Libraries

| Library | Declared In | No Usage Found In | Risk |
|---|---|---|---|
| `aspnet-signalr@1.0.27` | `src/Web/libman.json` | No `AddSignalR()`, `MapHub<T>()`, or hub class in any scanned `.cs` file | Dead client dependency; false signal that real-time is operational |
| `Microsoft.AspNetCore.Mvc 2.2.0` | `Directory.Packages.props` | No `<PackageReference Include="Microsoft.AspNetCore.Mvc">` in any `.csproj` | Vestigial / version conflict with net8.0 ecosystem; net8.0 includes ASP.NET Core MVC as part of framework |
| `EmailSender` / `IEmailSender` | Wired in DI (`ConfigureCoreServices.cs:26`) | `SendEmailAsync()` returns `Task.CompletedTask` — no outbound email logic | False signal: email notifications appear wired but silently no-op |

---

## OUTPUT 3 - Component Interaction & Contract Map

| Caller | Target | Protocol | Interaction Type | Coupling Strength | Contract | Timeout Declared? | Error Handling | Notes |
|---|---|---|---|---|---|---|---|---|
| eshopwebmvc (Web) | Azure SQL (catalogDatabase) | ADO.NET / EF Core TCP | Sync Request-Response | Tight — direct DbContext; no interface abstraction above EfRepository | Undocumented — EF migrations only | No — DEFAULT, RISK | EF exception propagates; `UseMigrationsEndPoint()` in dev | Shared schema with PublicApi; `EnableRetryOnFailure()` in prod only |
| eshopwebmvc (Web) | Azure SQL (identityDatabase) | ADO.NET / EF Core TCP | Sync Request-Response | Tight — direct DbContext | Undocumented — EF migrations only | No — DEFAULT, RISK | EF exception propagates | `EnableRetryOnFailure()` in prod only |
| eshopwebmvc (Web) | Azure Key Vault | HTTPS / Azure SDK | Sync (startup config read) | Loose — configuration provider abstraction | Azure SDK contract | Yes — Azure SDK default | `ChainedTokenCredential` with fallback | Production only; startup blocking |
| BlazorAdmin (WASM) | eshopwebmvc `/User` endpoint | HTTP | Sync Request-Response | Tight — URL-coupled; no contract document | Undocumented | No — DEFAULT, RISK | Try/catch in `FetchUser()` logs warning; returns anonymous principal | JWT token relayed from Web to Blazor |
| BlazorAdmin (WASM) | eshoppublicapi | HTTP (Bearer JWT) | Sync Request-Response | Loose — via HTTP interface | OpenAPI v1 (Swagger) at `/swagger/v1/swagger.json` | No — DEFAULT, RISK | `HttpService` wraps calls; no timeout; errors surface to UI | JWT from Web `/User` endpoint used as Bearer |
| eshoppublicapi (PublicApi) | sqlserver / Azure SQL (catalogDatabase) | ADO.NET / EF Core TCP | Sync Request-Response | Tight — direct DbContext | Undocumented — same EF migrations | No — DEFAULT, RISK | Exception propagated to `ExceptionMiddleware` | NO `EnableRetryOnFailure()`; NO Key Vault; always reads local connection strings |
| eshoppublicapi (PublicApi) | sqlserver / Azure SQL (identityDatabase) | ADO.NET / EF Core TCP | Sync Request-Response | Tight — direct DbContext | Undocumented — EF migrations | No — DEFAULT, RISK | Exception propagated | NO `EnableRetryOnFailure()` |
| Web | cdnjs | HTTPS (build-time libman) | Build-time Download | Loose — build tool fetches | Versioned package names in libman.json | N/A — build tool | Build fails on CDN unavailability | 6 client libraries fetched at build time |
| GitHub Actions CI | GitHub (actions/checkout, setup-dotnet) | HTTPS / GitHub API | CI/CD Pipeline | Loose — pinned action versions | GitHub Actions interface | N/A | Workflow fails on action error | Pinned to outdated v2/v1 |

### Coupling Hotspots

| Component | Inbound Dependencies | Outbound Dependencies | Coupling Risk |
|---|---|---|---|
| CatalogContext (shared DbContext) | eshopwebmvc (Web), eshoppublicapi (PublicApi), Infrastructure (EfRepository for ALL aggregates) | Azure SQL catalogDatabase | High — both deployable services write to the same shared CatalogContext; no bounded context separation; Baskets, Orders, and Catalog all share one context |
| ApplicationCore (class library) | Web, PublicApi, FunctionalTests, UnitTests, Infrastructure | None (pure domain) | Medium — SHARED COMPONENT used by all; changes break all consumers simultaneously |
| Infrastructure (class library) | Web, PublicApi, IntegrationTests | CatalogContext, AppIdentityDbContext, Azure SDK | High — contains all EF contexts and identity; both services depend on it; no abstraction boundary between Web-specific and API-specific infra |
| AuthorizationConstants | Infrastructure.Identity.IdentityTokenClaimService, PublicApi.Program | None | Critical — hardcoded JWT signing key shared across token issuer (Infrastructure) and token validator (PublicApi); if either is compromised, both are |

### API Contract Inventory

| Boundary | Contract Type | Version | Location | Breaking Change Risk |
|---|---|---|---|---|
| PublicApi public REST endpoints | OpenAPI / Swagger | v1 ("My API V1") | `/swagger/v1/swagger.json` (runtime); no static spec file committed | High — version is "v1" string only; no semver; no versioning strategy; breaking changes undetectable |
| Web internal `/User` endpoint | Undocumented | UNVERSIONED | `src/Web/Controllers/UserController.cs` | High — consumed by BlazorAdmin; any signature change breaks Blazor auth silently |
| Web `/api/authenticate` (actually PublicApi) | OpenAPI (Swagger) | v1 | PublicApi Swagger | Medium — operationId `auth.authenticate` established |
| Web health endpoint `/health` | JSON custom format | UNVERSIONED | `src/Web/Program.cs:151-168` | Low — internal monitoring only |

---

## OUTPUT 4 - Data Architecture Assessment

### Data Store Deep Dive

| Store | Access Pattern | ORM / Query Style | Transaction Scope | Consistency Model | Connection Pool Config | Migration State | Agent 1 Match? |
|---|---|---|---|---|---|---|---|
| CatalogDb (Azure SQL / local sqlserver) — accessed via `CatalogContext` | Repository via Ardalis.Specification + EfRepository; `BasketQueryService` uses raw LINQ to EF for aggregate query (`SumAsync`) | EF Core 8 — code-first; fluent API configuration; all entities via `ApplyConfigurationsFromAssembly` | Method-level (implicit EF transaction per `SaveChangesAsync()`); no explicit `BeginTransaction()` calls found in scanned code | Strong — SQL Server ACID via EF Core SaveChanges | DEFAULT — not declared; EF Core uses SQL Server default pool (min 0, max 100) | 3 migrations present and current (InitialModel 2020-12, FixBuyerId 2021-10, FixShipToAddress 2021-12); snapshot up to date | Confirmed |
| IdentityDb (Azure SQL / local sqlserver) — accessed via `AppIdentityDbContext` | ASP.NET Core Identity framework access only; `identityDbContext.Database.Migrate()` called on seeder startup | EF Core 8 — IdentityDbContext scaffold; default Identity tables | Method-level (Identity framework manages internally) | Strong — SQL Server ACID | DEFAULT — not declared | 1 migration (InitialIdentityModel 2020-12); `Database.Migrate()` auto-applies on startup when SQL Server | Confirmed |
| InMemory DB — CatalogContext | EF Core InMemory via `UseInMemoryDatabase("Catalog")` | EF Core InMemory | None (InMemory has no transactions) | Eventual (no durability guarantees) | N/A | N/A — ephemeral | Confirmed |
| InMemory DB — AppIdentityDbContext | EF Core InMemory via `UseInMemoryDatabase("Identity")` | EF Core InMemory | None | Eventual | N/A | N/A — ephemeral | Confirmed |

### Data Ownership Map

| Entity / Table | Owning Service | Other Services With Access | Access Type | Coupling Risk |
|---|---|---|---|---|
| Basket, BasketItem | eshopwebmvc (Web) — primary writer | eshoppublicapi (PublicApi) — shares same CatalogContext connection string | Read-write (both services can access) | ANTIPATTERN — shared database with no service boundary; both services connect directly to CatalogDb |
| CatalogItem, CatalogBrand, CatalogType | eshoppublicapi (PublicApi) — admin write path | eshopwebmvc (Web) — read path (via CachedCatalogViewModelService) | Read (Web) / Read-write (PublicApi admin) | Tight — shared schema; Web reads from same tables PublicApi writes to |
| Order, OrderItem | eshopwebmvc (Web) — sole writer (`OrderService`) | eshoppublicapi — NOT observed to access orders; BlazorAdmin has no order management | Write (Web only) | Low — effectively single writer |
| ASP.NET Identity (Users, Roles, Claims) | eshopwebmvc (Web) — primary Identity management | eshoppublicapi (PublicApi) — reads for JWT token generation (`UserManager.FindByNameAsync`, `GetRolesAsync`) | Read (PublicApi) / Read-write (Web) | Tight — shared IdentityDb schema; both connect directly |

### Data Flow & Consistency Notes

1. **Basket-to-Order conversion** is a synchronous in-process operation: `OrderService.CreateOrderAsync()` reads basket (CatalogContext), creates order (CatalogContext), caller then calls `BasketService.DeleteBasketAsync()` — these are two separate `SaveChangesAsync()` calls with no wrapping transaction. If the basket delete fails after order creation, the basket persists as an orphan.
2. **Catalog item snapshot on order**: `CatalogItemOrdered` is an owned entity (value object) capturing `ProductName` and `PictureUri` at time of order — correct immutable snapshot pattern.
3. **Database seeding on every startup**: Both `CatalogContextSeed.SeedAsync()` and `AppIdentityDbContextSeed.SeedAsync()` run on every startup against SQL Server; Identity seeder calls `Database.Migrate()` inline — schema migrations run in the application process, not a separate migration job.
4. **No outbox, event log, or saga**: Order creation is fire-and-forget after the final DB write; no domain events published; no compensation mechanism.

---

## OUTPUT 5 - Security Architecture Assessment

### Authentication & Authorisation Implementation

| Mechanism | Declared (Agent 1) | Implemented How | Validation Completeness | Gaps | Severity |
|---|---|---|---|---|---|
| JWT Bearer Tokens (PublicApi) | HIGH — package declared | `AuthorizationConstants.JWT_SECRET_KEY` (hardcoded string) converted to `byte[]` via `Encoding.ASCII.GetBytes()`; `SymmetricSecurityKey`; `HmacSha256Signature`; token lifetime: 7 days; issued by `IdentityTokenClaimService.GetTokenAsync()` | Partial — `ValidateIssuerSigningKey=true` only; `ValidateIssuer=false`; `ValidateAudience=false`; `RequireHttpsMetadata=false` | No issuer/audience validation (any token signed with same key accepted); HTTPS not required for token submission; 7-day lifetime with no refresh or revocation for JWT path | Critical |
| ASP.NET Core Identity (Web + PublicApi) | HIGH | `AddIdentity<ApplicationUser, IdentityRole>()` with `AppIdentityDbContext`; seeded with `demouser@microsoft.com` (Buyers role) and `admin@microsoft.com` (Administrators role); passwords from `AuthorizationConstants.DEFAULT_PASSWORD = "Pass@word1"` | Full Identity framework implementation; account lockout on API login (`lockoutOnFailure: true`) | Seed passwords are hardcoded well-known values; both accounts created on every fresh SQL deployment | Critical |
| Cookie Authentication (Web) | HIGH (inferred) | `CookieAuthenticationDefaults.AuthenticationScheme`; `HttpOnly=true`; `SecurePolicy=Always`; `SameSite=Lax`; `ExpireTimeSpan = 60 min`; revocation via `IMemoryCache` with `RevokeAuthenticationEvents` | Full | Cookie SameSite=Lax (not Strict) permits some cross-site requests | Low |
| Blazor WASM Auth (BlazorAdmin) | HIGH | `CustomAuthStateProvider` calls Web `/User` endpoint; caches principal 60s; attaches JWT Bearer on HttpClient | Partial — 60s staleness window for auth state; no token expiry check during cache window | `UserCacheRefreshInterval` hardcoded; TODO comment present | Medium |
| Azure Managed Identity (Web→KeyVault) | HIGH | `ChainedTokenCredential(new AzureDeveloperCliCredential(), new DefaultAzureCredential())` in production branch; `builder.Configuration.AddAzureKeyVault(...)` | Full for production Web path | No equivalent in PublicApi — PublicApi cannot access Key Vault | Medium |
| RBAC (Role-based) | Not explicitly in Agent 1 | `[Authorize(Roles = "Administrators", AuthenticationSchemes = JwtBearerDefaults.AuthenticationScheme)]` on `CreateCatalogItemEndpoint`, `DeleteCatalogItemEndpoint`, `UpdateCatalogItemEndpoint` (PublicApi); Web Checkout: `[Authorize]` (any authenticated user) | Partial — write endpoints protected; ALL READ endpoints on PublicApi are anonymous | `GET /api/catalog-items`, `GET /api/catalog-items/{id}`, brand list, type list — unauthenticated | Low (by design for public catalog) |

### Secrets Posture

| Item | Finding | Severity | Evidence |
|---|---|---|---|
| JWT signing key | Hardcoded: `AuthorizationConstants.JWT_SECRET_KEY = "SecretKeyOfDoomThatMustBeAMinimumNumberOfBytes"` — committed to source, used live in production code | Critical | `src/ApplicationCore/Constants/AuthorizationConstants.cs:10`, `src/PublicApi/Program.cs:54`, `src/Infrastructure/Identity/IdentityTokenClaimService.cs:26` |
| Auth key constant | Hardcoded: `AuthorizationConstants.AUTH_KEY = "AuthKeyOfDoomThatMustBeAMinimumNumberOfBytes"` — committed to source | High | `src/ApplicationCore/Constants/AuthorizationConstants.cs:7` |
| Default seed passwords | Hardcoded: `AuthorizationConstants.DEFAULT_PASSWORD = "Pass@word1"` used to create both `admin@microsoft.com` and `demouser@microsoft.com` on every fresh deployment | Critical | `src/Infrastructure/Identity/AppIdentityDbContextSeed.cs:21,25` |
| Docker SA_PASSWORD | `SA_PASSWORD=@someThingComplicated1234` hardcoded in docker-compose.yml; dev-only but committed to repo | High | `docker-compose.yml` |
| Azure SQL connection strings (Docker) | Connection strings including passwords committed in `appsettings.Docker.json` for both Web and PublicApi (redacted in pipeline output but present in source tree) | High | `src/Web/appsettings.Docker.json`, `src/PublicApi/appsettings.Docker.json` |
| Azure SQL admin passwords (production) | Sourced via `$(secretOrRandomPassword ${AZURE_KEY_VAULT_NAME} sqlAdminPassword)` azd function — properly externalized for production | OK | `infra/main.parameters.json` |
| Key Vault secrets (production) | `AZURE-SQL-CATALOG-CONNECTION-STRING`, `AZURE-SQL-IDENTITY-CONNECTION-STRING` stored in Key Vault; accessed via Managed Identity | OK | `infra/core/security/keyvault.bicep`, `infra/main.bicep` |

### Attack Surface Summary

| Surface | Exposure | Mitigations Found | Gaps |
|---|---|---|---|
| PublicApi REST endpoints | 10+ endpoints; `POST /api/authenticate`, `POST/DELETE/PUT /api/catalog-items` require JWT Administrators role; `GET /api/catalog-items`, `GET /api/catalog-items/{id}`, brand/type lists — anonymous | JWT RBAC on writes; account lockout on authenticate; CORS scoped to `baseUrlConfig.WebBase`; Swagger UI enabled always | `RequireHttpsMetadata=false`; JWT issuer/audience not validated; exception message leaked in 500 responses via `ExceptionMiddleware` |
| Web MVC + Razor Pages | Public catalog browsing anonymous; basket requires cookie; checkout requires `[Authorize]`; admin pages require Administrators role | Cookie auth with HttpOnly, SecurePolicy=Always; HSTS in production; CSRF protection via Razor Pages antiforgery by default | `AllowedHosts: *` in appsettings; hardcoded default admin password; `RequireConsent = false` in cookie policy (TODO comment present) |
| BlazorAdmin WASM panel | Requires authentication (JWT forwarded from Web); admin-only CRUD on catalog | JWT Bearer on all mutating calls | 60-second auth state cache window; no explicit token expiry validation during cache period |
| Azure SQL databases | `publicNetworkAccess: Enabled`; firewall `0.0.0.1–255.255.255.254` (all IPs allowed) | TLS 1.2 enforced; SQL admin credentials in Key Vault for production | All-IP firewall rule in production Bicep; commented as developer convenience, not hardened for production |
| Azure App Service | HTTPS only, TLS 1.2 min, FTPS only | `httpsOnly: true`; `ftpsState: FtpsOnly`; SystemAssigned Managed Identity | CORS allows `portal.azure.com` and `ms.portal.azure.com` as additional origins |

---

## OUTPUT 6 - NFR Registry

| ID | NFR Name | Value | Category | Source | Confidence |
|---|---|---|---|---|---|
| NFR-01 | Server-side catalog cache sliding expiration | 30,000ms (30s) | Data Freshness | `src/Web/Extensions/CacheHelpers.cs:7` — `TimeSpan.FromSeconds(30)` | HIGH |
| NFR-02 | Client-side browser localStorage catalog cache TTL | 60,000ms (1 min) | Data Freshness | `src/BlazorAdmin/Services/CachedCatalogItemServiceDecorator.cs:34` — `DateCreated.AddMinutes(1)` | HIGH |
| NFR-03 | JWT token lifetime | 7 days (604,800s) | Availability / Security | `src/Infrastructure/Identity/IdentityTokenClaimService.cs:38` — `DateTime.UtcNow.AddDays(7)` | HIGH |
| NFR-04 | Authentication cookie validity period | 60 min (3,600s) | Availability / Security | `src/Web/Configuration/ConfigureCookieSettings.cs:10` — `ValidityMinutesPeriod = 60` | HIGH |
| NFR-05 | BlazorAdmin user claims cache refresh interval | 60,000ms (60s) | Data Freshness | `src/BlazorAdmin/CustomAuthStateProvider.cs:10` — `TimeSpan.FromSeconds(60)` | HIGH |
| NFR-06 | Anonymous basket cookie expiry | 10 years | Data Freshness / Resource Management | `src/Web/Pages/Basket/Checkout.cshtml.cs:95` — `DateTime.Today.AddYears(10)` | HIGH |
| NFR-07 | Token revocation cache absolute expiry | 60 min (3,600s) | Availability / Security | `src/Web/Controllers/UserController.cs:52` — `DateTime.Now.AddMinutes(ConfigureCookieSettings.ValidityMinutesPeriod)` | HIGH |
| NFR-08 | Artificial catalog list API delay | 1,000ms (1s) per request | Latency | `src/PublicApi/CatalogItemEndpoints/CatalogItemListPagedEndpoint.cs:42` — `await Task.Delay(1000)` | HIGH |
| NFR-09 | App Service HTTP log retention | 1 day / 35MB | Resource Management | `infra/core/host/appservice.bicep` — `retentionInDays: 1, retentionInMb: 35` | HIGH |
| NFR-10 | SQL deployment script resource retention | 3,600s (1 hour) | Resource Management | `infra/core/database/sqlserver/sqlserver.bicep` — `retentionInterval: PT1H` | HIGH |
| NFR-11 | App Service minimum TLS version | TLS 1.2 | Availability / Security | `infra/core/host/appservice.bicep` — `minTlsVersion: '1.2'` | HIGH |
| NFR-12 | Azure SQL minimum TLS version | TLS 1.2 | Availability / Security | `infra/core/database/sqlserver/sqlserver.bicep` — `minimalTlsVersion: '1.2'` | HIGH |
| NFR-13 | App Service compute plan | B1 SKU, 1 core, 1.75GB RAM, Linux | Throughput / Resource Management | `infra/core/host/appserviceplan.bicep` — `sku: B1` | HIGH |
| NFR-14 | EF Core SQL retry policy (production Web only) | Default: max 6 retries, max 30s delay, transient error codes | Reliability | `src/Web/Program.cs:36,41` — `EnableRetryOnFailure()` with no custom parameters | LOW — default values assumed; no explicit parameters declared |

**NFR categories with no declared values:**
- **Connection pool configuration:** No `MaxPoolSize`, `MinPoolSize`, `ConnectionTimeout`, or `CommandTimeout` in any connection string or DbContext configuration — system uses SQL Server ADO.NET defaults (max 100 connections, 15s command timeout). These defaults represent an unbound concurrency and latency risk on B1 compute.
- **Rate limiting:** No rate limiting declarations found in any middleware, action filter, or Bicep resource. PublicApi is unprotected from request flooding.
- **Request timeouts:** No `HttpClient.Timeout` declared in `ApiHealthCheck`, `HomePageHealthCheck`, or `HttpService`. Default .NET `HttpClient.Timeout` is 100 seconds.

---

## OUTPUT 7 - Technical Debt & Risk Register

| ID | Risk / Debt Item | Category | Affected Component(s) | Severity | Evidence | Recommended Action |
|---|---|---|---|---|---|---|
| TD-01 | JWT signing key hardcoded in source control | Security Vulnerability | PublicApi (token validator), Infrastructure.Identity (token issuer), AuthorizationConstants | Critical | `src/ApplicationCore/Constants/AuthorizationConstants.cs:10` — `JWT_SECRET_KEY = "SecretKeyOfDoomThatMustBeAMinimumNumberOfBytes"` used live at `PublicApi/Program.cs:54` and `IdentityTokenClaimService.cs:26` | Move to Azure Key Vault secret; read at startup via config provider; rotate key immediately in any environment where this repo is accessible |
| TD-02 | Hardcoded default admin and user passwords seeded to production database | Security Vulnerability | AppIdentityDbContextSeed, all deployed environments | Critical | `src/ApplicationCore/Constants/AuthorizationConstants.cs:12` — `DEFAULT_PASSWORD = "Pass@word1"` used in `AppIdentityDbContextSeed.cs:21,25` to create `admin@microsoft.com` and `demouser@microsoft.com` on every startup | Remove seeded accounts from production flow; generate random initial passwords via Key Vault; require forced password reset on first login |
| TD-03 | JWT bearer token validates neither issuer nor audience | Security Vulnerability | PublicApi — all authenticated endpoints | Critical | `src/PublicApi/Program.cs:65-66` — `ValidateIssuer = false`, `ValidateAudience = false` | Set `ValidateIssuer = true`, `ValidIssuer = "<your-issuer>"`, `ValidateAudience = true`, `ValidAudience = "<your-audience>"` to prevent cross-service token acceptance |
| TD-04 | Exception message exposed verbatim in PublicApi 500 responses | Security Vulnerability | PublicApi — ExceptionMiddleware | High | `src/PublicApi/Middleware/ExceptionMiddleware.cs:47` — `Message = exception.Message` for all unhandled exceptions → HTTP 500 body | Return generic error message in production; log full exception server-side; consider environment-conditional detail level |
| TD-05 | No SQL retry on failure in PublicApi or Development/Docker paths | Scalability Constraint | PublicApi (always), Web + PublicApi (Development/Docker) | High | `src/Infrastructure/Dependencies.cs:33,37` — bare `UseSqlServer(connectionString)` with no `sqlOptions => sqlOptions.EnableRetryOnFailure()` | Add `EnableRetryOnFailure()` to all `UseSqlServer()` calls in `Dependencies.ConfigureServices()` |
| TD-06 | Health checks use non-pooled `HttpClient` (socket exhaustion risk) | Scalability Constraint | Web — `ApiHealthCheck`, `HomePageHealthCheck` | High | `src/Web/HealthChecks/ApiHealthCheck.cs:25` and `HomePageHealthCheck.cs:26` — `var client = new HttpClient()` per invocation; health checks called on every health poll | Replace with `IHttpClientFactory`-typed client injected via constructor; avoids socket exhaustion under frequent polling |
| TD-07 | Hardcoded 1-second artificial delay on catalog item listing | Operational Risk | PublicApi — `CatalogItemListPagedEndpoint` | High | `src/PublicApi/CatalogItemEndpoints/CatalogItemListPagedEndpoint.cs:42` — `await Task.Delay(1000)` present in production code path; adds 1,000ms to every `GET /api/catalog-items` call | Remove `await Task.Delay(1000)` entirely; this is a demo artifact shipped to production |
| TD-08 | Email sender is a no-op stub — account confirmation and password reset silently fail | Operational Risk | Infrastructure.Services.EmailSender, Web identity flows | High | `src/Infrastructure/Services/EmailSender.cs:10-12` — `return Task.CompletedTask` with TODO comment | Integrate SendGrid, Azure Communication Services, or SMTP; `EmailSender.SendEmailAsync()` must send real email in production |
| TD-09 | Checkout uses hardcoded shipping address — not collected from user | Architecture Anti-pattern | Web — `CheckoutModel.OnPost()` | High | `src/Web/Pages/Basket/Checkout.cshtml.cs:57` — `new Address("123 Main St.", "Kent", "OH", "United States", "44240")` | Implement shipping address form and bind user-supplied address to `CreateOrderAsync()`; current implementation cannot be used in production |
| TD-10 | Both `[Authorize]` and `[AllowAnonymous]` applied simultaneously to UserController methods | Architecture Anti-pattern | Web — `UserController.GetCurrentUser()`, `UserController.Logout()` | High | `src/Web/Controllers/UserController.cs:36-38, 42-45` — both attributes on same method; `[AllowAnonymous]` overrides `[Authorize]` in ASP.NET Core, making these methods effectively unauthenticated | Remove `[AllowAnonymous]` from both methods if auth is intended; or document the intentional public exposure of user state endpoint |
| TD-11 | Azure SQL firewall open to all IPs in production Bicep | Security Vulnerability | infra — `sqlserver.bicep`, both Azure SQL instances | High | `infra/core/database/sqlserver/sqlserver.bicep` — firewall `0.0.0.1–255.255.255.254` with comment acknowledging it is for developer debugging | Replace with App Service outbound IP whitelist or Azure Service Endpoints; enable private endpoint; remove public network access entirely |
| TD-12 | PublicApi has no Azure deployment path — missing from azure.yaml and Bicep | Operational Risk | eshoppublicapi | High | `azure.yaml` declares only `web` service; no Bicep module for PublicApi App Service; `PublicApi/Program.cs` always calls `Dependencies.ConfigureServices()` with local connection strings (no Key Vault branch) | Decide: deploy PublicApi to its own App Service with Key Vault integration, or merge into Web; current state means PublicApi cannot run in Azure |
| TD-13 | Bootstrap 3.4.1 — end of life since 2019 | EOL Technology | Web — all MVC views using Bootstrap CSS | Medium | `src/Web/libman.json` — `twitter-bootstrap@3.4.1`; Bootstrap 3 reached EOL in July 2019; Bootstrap 5.3 is current | Upgrade to Bootstrap 5; requires HTML markup changes for renamed utility classes and component restructuring |
| TD-14 | `actions/checkout@v2`, `actions/setup-dotnet@v1` — outdated CI/CD action versions | CI-CD Risk | `.github/workflows/dotnetcore.yml`, `.github/workflows/richnav.yml` | Medium | `.github/workflows/dotnetcore.yml:7,8` — `actions/checkout@v2` (current: v4), `actions/setup-dotnet@v1` (current: v4); v1/v2 use deprecated Node.js 12/16 runners being retired by GitHub | Pin to `actions/checkout@v4`, `actions/setup-dotnet@v4` |
| TD-15 | No secret scanning, SAST, dependency scan, or container scan in CI pipeline | CI-CD Risk | GitHub Actions CI pipeline | High | `.github/workflows/dotnetcore.yml` — only `dotnet build` and `dotnet test`; no `trufflehog`, `snyk`, `semgrep`, `trivy`, or equivalent found | Add at minimum: `trufflehog` or `gitleaks` for secret scanning; `snyk test` or `dotnet list package --vulnerable` for dependency scan; SAST via `dotnet-security-guard` or CodeQL |
| TD-16 | aspnet-signalr@1.0.27 declared but no server-side hub registered | Operational Risk | Web — libman.json, all pages loading SignalR client JS | Medium | `src/Web/libman.json` — `aspnet-signalr@1.0.27`; no `AddSignalR()`, `MapHub<T>()`, or hub class found | Remove dead client library or implement server-side hub; current state adds 44KB+ of unused JS to every page load |
| TD-17 | `Microsoft.AspNetCore.Mvc 2.2.0` declared in central props — version incompatible with net8.0 | Configuration Risk | Directory.Packages.props | Medium | `Directory.Packages.props` — no `PackageReference` in any csproj but central version declared for a framework package that is now included in ASP.NET Core 8 SDK | Remove the version entry from `Directory.Packages.props` to avoid accidental resolution |
| TD-18 | Azure SQL Edge container has no image tag — implicit `latest` | Configuration Risk | docker-compose.yml — `sqlserver` service | Medium | `docker-compose.yml` — `image: mcr.microsoft.com/azure-sql-edge` (no tag); `latest` resolves to different versions over time | Pin to a specific tag e.g. `mcr.microsoft.com/azure-sql-edge:1.0.7` |
| TD-19 | `dotnet-xunit 2.3.1` in FunctionalTests — deprecated DotNetCliToolReference format | EOL Technology | `tests/FunctionalTests/FunctionalTests.csproj` | Low | `DotNetCliToolReference` format was deprecated in .NET Core 2.1; may fail to resolve on modern SDK | Remove `DotNetCliToolReference` and use `xunit.runner.console` from central props instead |

---

## OUTPUT 8 - Operational Architecture Assessment

### CI/CD Pipeline Maturity

> Evidence-based assessment per v2 protocol. Present requires a specific tool invocation found in a pipeline file. Absent means no matching evidence in any scanned pipeline file.

| Capability | Present? | Evidence (tool / action name + file + job) | Runs On | Gap Severity |
|---|---|---|---|---|
| Build | Present | `dotnet build ./eShopOnWeb.sln --configuration Release` — `.github/workflows/dotnetcore.yml`, `build` job, step 3 | All branches (push, pull_request, workflow_dispatch) | - |
| Unit Tests | Present | `dotnet test ./eShopOnWeb.sln --configuration Release` — `.github/workflows/dotnetcore.yml`, `build` job, step 4 | All branches | - |
| Integration Tests | Absent | No `testcontainers`, `docker-compose up` + test, `newman`, or equivalent found in any pipeline file | - | Medium |
| Code Coverage Gate | Absent | `dotnet test` runs WITHOUT `--collect:"XPlat Code Coverage"` flag; `coverlet.collector` is declared in packages but not invoked in CI | - | Medium |
| SAST (Static Security) | Absent | No `sonar`, `semgrep`, `codeql`, `snyk code`, `bandit`, `security-code-scan` found in any pipeline file | - | High |
| Dependency Scan | Partial | GitHub Dependabot configured (`.github/dependabot.yml`) — `nuget` ecosystem, `daily` schedule; raises PRs for outdated packages; NOT an in-pipeline blocking gate; no `snyk test`, `dotnet list package --vulnerable`, or `owasp dependency-check` found in workflow files | Daily PR creation (not blocking gate) | Medium |
| Container / Image Scan | Absent | No `trivy image`, `snyk container`, `docker scout`, or equivalent found | - | Medium |
| Secret / Credential Scan | Absent | No `trufflehog`, `gitleaks`, `detect-secrets`, or `git-secrets` found in any pipeline file; ironic given hardcoded secrets confirmed in source | - | High |
| Infrastructure Scan (IaC) | Absent | No `tfsec`, `checkov`, `terrascan` found; Bicep files not scanned | - | Medium |
| Lint / Code Quality | Absent | No `dotnet format --verify-no-changes`, `eslint`, or equivalent found | - | Low |
| Automated Deploy | Absent | No `az webapp deploy`, `azd deploy`, `kubectl apply`, or equivalent found in any pipeline file; deployment is manual via `azd up` | - | High |
| Smoke / Health Check Post-Deploy | Absent | No `curl` health endpoint, `newman`, or equivalent post-deploy check found | - | High |
| Auto Rollback | Absent | No `az webapp deployment slot swap --rollback`, `helm rollback`, or equivalent found | - | High |
| Manual Approval Gate | Absent | No `environment: production` with `required reviewers` configuration found | - | Low |
| Release / Versioning Automation | Absent | No `semantic-release`, `gh release create`, `git tag` automation found | - | Low |

**CI/CD pipeline files directly read:** 2 (`dotnetcore.yml`, `richnav.yml`) + 1 configuration file (`dependabot.yml`). No reusable workflow files (`uses:` pointing to local paths) found.

**Additional tools found vs Agent 1 inventory:** None — Agent 1's inventory was complete for these files.

### Observability Coverage

| Concern | Component | Present? | Tool / Library | Gap? |
|---|---|---|---|---|
| Structured Logging | eshopwebmvc (Web) | Partial | `builder.Logging.AddConsole()` + `IAppLogger<T>` (wraps `ILogger<T>`) + `LoggerAdapter<T>`; log levels configured per environment; NOT structured JSON format — plain console text; `IncludeScopes: false` in production | GAP — no JSON structured format; no correlation ID propagation; scopes disabled |
| Structured Logging | eshoppublicapi (PublicApi) | Partial | `builder.Logging.AddConsole()` + `LoggerAdapter<T>`; same pattern as Web | GAP — same issues as Web |
| Distributed Tracing | eshopwebmvc | Absent | No OpenTelemetry, Jaeger, Zipkin, or Application Insights SDK usage found in source | GAP |
| Distributed Tracing | eshoppublicapi | Absent | No distributed tracing SDK found | GAP |
| Metrics Export | eshopwebmvc | Absent | No Prometheus, Micrometer, StatsD, or Application Insights SDK usage in source | GAP — `APPLICATIONINSIGHTS_CONNECTION_STRING` env key set but no AI SDK wired in code |
| Metrics Export | eshoppublicapi | Absent | No metrics instrumentation found | GAP |
| Correlation ID Propagation | All services | Absent | No `X-Correlation-Id` header middleware, `IHttpContextAccessor` correlation propagation, or Activity/TraceId usage found | GAP — all requests are untraced |
| Health / Readiness Endpoints | eshopwebmvc (Web) | Present | `/health` (aggregate JSON), `home_page_health_check`, `api_health_check` — content-based custom implementations | Partial GAP — health checks use content matching not status codes; non-pooled HttpClient; no readiness vs liveness distinction |
| Health / Readiness Endpoints | eshoppublicapi (PublicApi) | Absent | No `AddHealthChecks()` or `/health` endpoint found in `PublicApi/Program.cs` | GAP |
| Alerting Rules | N/A | Absent | No Alertmanager rules, CloudWatch alarms, or Azure Monitor alert rules found in Bicep or repo | GAP |
| Application Insights (platform) | eshopwebmvc (Web) | Partial | `APPLICATIONINSIGHTS_CONNECTION_STRING` injected by Bicep when `applicationInsightsName` param non-empty; App Service platform logs capture HTTP/app logs; no AI SDK (`Microsoft.ApplicationInsights.AspNetCore`) found in source | Partial — platform telemetry only if AI resource exists; no custom events, traces, or metrics from application code |

### Deployment Safety

| Practice | Present? | Evidence | Risk If Absent |
|---|---|---|---|
| Graceful Shutdown | No | No `app.Lifetime.ApplicationStopping` handler, no `StopTimeout` configuration, no `IHostedService` shutdown logic found in either Program.cs | Requests in-flight during deploy are dropped; potential data loss on active checkout operations |
| Readiness Probe | No | No Kubernetes manifests found; Azure App Service has no readiness probe equivalent configured in Bicep; `alwaysOn: true` keeps the slot warm but does not gate traffic on application readiness | Traffic routed to App Service before database seeder completes; startup failures invisible to load balancer |
| Liveness Probe | No | No Kubernetes liveness probe; Azure App Service auto-restart on process crash only | Hung process (e.g., deadlocked thread pool) may not be restarted |
| Blue-Green / Canary | No | No Azure App Service deployment slots configured in Bicep; no `az webapp deployment slot` commands found | 100% traffic exposure on every deployment; no rollback path except re-deploy |
| Feature Flags | No | No LaunchDarkly, Azure App Configuration feature flags, or `IFeatureManager` usage found | No decoupled release capability; all changes go live on deploy |

### Disaster Recovery Posture

| Item | Declared? | Detail | Source |
|---|---|---|---|
| Database backup configuration | No | No Azure SQL backup policy, PITR retention, or geo-redundant backup declaration found in Bicep | NOT FOUND in `infra/` tree |
| Multi-region / multi-AZ config | No | Single Azure region deployment; no Traffic Manager, Front Door, or secondary region declared | NOT FOUND |
| Database replication | No | No read replica, active geo-replication, or failover group declaration found | NOT FOUND |
| RTO / RPO declarations | No | No SLA targets declared in any configuration or documentation file | NOT FOUND |

---

## Validation Queue

| # | Item | Layer | Reason |
|---|---|---|---|
| 1 | `Microsoft.AspNetCore.Mvc 2.2.0` in Directory.Packages.props | Application | No PackageReference in any csproj confirmed — remains unresolvable from scanned files; likely vestigial. Status: UNRESOLVED (still flagged as TD-17) |
| 2 | `dotnet-xunit 2.3.1` in FunctionalTests.csproj | Application | Deprecated DotNetCliToolReference; not scanned deeper. Status: CONFIRMED as TD-19 |
| 3 | Azure SQL Edge — no image tag | Infrastructure | `mcr.microsoft.com/azure-sql-edge` confirmed in `docker-compose.yml` with no tag. Status: CONFIRMED as TD-18 |
| 4 | SA_PASSWORD + connection string passwords hardcoded | Security | `SA_PASSWORD=@someThingComplicated1234` confirmed in docker-compose.yml. Status: CONFIRMED as HIGH (part of TD-01 context) |
| 5 | JWT signing key / issuer / audience not in any config file | Security | **RESOLVED** — Key is hardcoded in `AuthorizationConstants.JWT_SECRET_KEY`; issuer/audience not validated by design. Status: RESOLVED → TD-01, TD-03 |
| 6 | SQL Server firewall 0.0.0.1–255.255.255.254 | Security | Confirmed in Bicep as intentional developer convenience. Status: CONFIRMED as TD-11 |
| 7 | Application Insights — no provisioning resource | Observability | Referenced as `existing` in Bicep; no provisioning module found anywhere in repo. Status: UNRESOLVED — may be manually provisioned pre-deployment |
| 8 | PublicApi deployment to Azure undeclared | Infrastructure | **RESOLVED** — Confirmed: `azure.yaml` only declares `web`; `PublicApi/Program.cs` has no Key Vault branch; PublicApi cannot run in Azure as currently configured. Status: CONFIRMED as TD-12 |
| 9 | src/Web/Dockerfile and src/PublicApi/Dockerfile not provided | Infrastructure | Not scanned. Status: UNRESOLVED — Dockerfiles not in provided source files; base images, ENTRYPOINT, EXPOSE port unknown |
| 10 | SignalR server-side hub config unknown | Observability | **RESOLVED** — No `AddSignalR()`, `MapHub<T>()`, or hub class found in any scanned C# file. Status: CONFIRMED as TD-16 |
| 11 | `actions/checkout@v2` and `actions/setup-dotnet@v1` pinned to old versions | CI/CD | Confirmed outdated. Status: CONFIRMED as TD-14 |
| 12 | No deployment step in CI/CD | CI/CD | **RESOLVED** — Confirmed: no deploy step in any pipeline file. Status: CONFIRMED as gap in OUTPUT 8 CI/CD Maturity |
| 13 | `KubernetesTools` VSCode extension recommended, no k8s manifests | Observability | Extension present in `.vscode/extensions.json`; no manifests anywhere in scanned tree. Status: CONFIRMED — extension aspirational only |

---

## Agent 1 Discrepancy Log

| # | What Agent 1 Said | What Deep Analysis Shows | Resolved? |
|---|---|---|---|
| D-01 | JWT signing key / issuer / audience "NOT found in any scanned config file — likely in User Secrets or Program.cs" | JWT_SECRET_KEY is hardcoded as a constant string in `src/ApplicationCore/Constants/AuthorizationConstants.cs:10`; it is NOT in User Secrets or environment config; it is compiled into the binary | RESOLVED — Critical finding; flagged as TD-01 |
| D-02 | Agent 1 implied both services have equivalent Azure deployment paths (both listed in Component Map with App Service) | PublicApi has NO Azure deployment path: not in `azure.yaml`, no Key Vault branch in its Program.cs, always reads local connection strings. In production, only `web` deploys to Azure App Service | RESOLVED — flagged as TD-12 |
| D-03 | Agent 1 classified security layer as: "JWT bearer auth (Web + PublicApi + Infrastructure)" | Web does NOT use JWT bearer authentication at all. Web uses Cookie authentication only (`CookieAuthenticationDefaults.AuthenticationScheme`). JWT is PublicApi-only. Web's `UserController` issues JWT tokens FOR BlazorAdmin, but Web itself validates cookies, not JWT | RESOLVED — corrected in OUTPUT 5 |
| D-04 | Agent 1 listed `Microsoft.eShopWeb.CatalogDb` and `Microsoft.eShopWeb.Identity` as the two databases for both services in Docker compose | `EfRepository<T>` constructor accepts `CatalogContext` only — meaning the generic repository resolves to CatalogDb for ALL aggregates. `AppIdentityDbContext` is a separate, parallel registration. Both services in Docker share the same `sqlserver` container and both connect to both databases independently — confirmed correct. However, the Buyer aggregate exists in the domain model but has NO `DbSet<Buyer>` in CatalogContext and no migration for it — this is an undocumented gap | PARTIAL — Buyer entity persistence gap is new finding not in Agent 1's inventory |

---

**Agent 2 Analysis Complete.**

Documentation is ready for technical review.

**Highest-priority action item:** TD-01 — JWT signing key `"SecretKeyOfDoomThatMustBeAMinimumNumberOfBytes"` is committed to source control and used live; combined with TD-03 (no issuer/audience validation) and TD-02 (hardcoded admin password `Pass@word1` seeded on every deployment), the authentication infrastructure of this system is trivially compromisable by any person with repository read access. All three must be remediated before any production deployment.
