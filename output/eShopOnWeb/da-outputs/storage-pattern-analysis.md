# Storage Pattern Analysis — eShopOnWeb

## 1. Relational Storage (Primary)
- **CatalogDb** (PostgreSQL via Npgsql — CONFIRMED, RC-001) — accessed via EF Core `CatalogContext`, repository pattern (`IRepository<T>`, `IReadRepository<T>` in src/ApplicationCore/Interfaces/). `src/Infrastructure/Dependencies.cs` calls `UseNpgsql(...CatalogConnection)`; `src/Web/appsettings.json` points at `Host=localhost;Port=5432;Database=eShopCatalog`. confidence 0.9
- **IdentityDb** (PostgreSQL via Npgsql — CONFIRMED, RC-001) — ASP.NET Core Identity, standard `UserManager`/`SignInManager` access patterns, `AppIdentityDbContext` registered via `UseNpgsql(...IdentityConnection)`. confidence 0.85
- **NOTE**: `appsettings.Docker.json` (Web and PublicApi) still contains SQL Server-style connection strings (`Server=sqlserver,1433;...`). Since the provider is registered as Npgsql unconditionally in `Dependencies.cs`, these appear to be stale/legacy from the original SQL Server template rather than an active second deployment path. confidence 0.8.

## 2. Caching Layer ⚠️ (mandatory section per Phase 1 step 5)

| Component | File | Pattern | TTL / Eviction |
|---|---|---|---|
| `CachedCatalogItemServiceDecorator` | src/BlazorAdmin/Services/CachedCatalogItemServiceDecorator.cs | Decorator over `ICatalogItemService` — wraps PublicApi calls for catalog item CRUD, persisting results via `ILocalStorageService` (browser localStorage) as `CacheEntry<List<CatalogItem>>` | CONFIRMED storage mechanism = browser localStorage (RC-004); `CacheEntry<T>` records a `DateCreated` timestamp but the expiry/staleness comparison logic was not located in this pass — TTL value itself remains UNKNOWN, confidence < 0.7 |
| `CachedCatalogLookupDataServiceDecorator` | src/BlazorAdmin/Services/CachedCatalogLookupDataServiceDecorator .cs | Decorator over `ICatalogLookupDataService` — caches brand/type lookup lists the same way | same as above |
| `CacheEntry<T>` | src/BlazorAdmin/Services/CacheEntry.cs | `{ T Value, DateTime DateCreated = DateTime.UtcNow }` — CONFIRMED shape (RC-004), not `{ Value, ExpiresAt }` as previously guessed | DateCreated present; no expiry field |

**Caching as a business rule**: see hidden-business-rules.json — the staleness-comparison logic for these decorators still needs to be located to fully document the invalidation policy (open item).

`RefreshBroadcast.cs` (src/BlazorAdmin/Helpers/) appears to be the invalidation-signal mechanism that complements this cache — likely a simple pub/sub (C# event or similar) notifying components to re-fetch after a write. confidence 0.65, UNKNOWN exact implementation.

## 3. Client-Side Storage
- **Browser cookies** via `Cookies.cs` (src/BlazorAdmin/JavaScript/) + `CustomAuthStateProvider.cs` — used to persist auth tokens for the Blazor WASM admin client. confidence 0.75
- **NEW (RC-005)**: `CustomAuthStateProvider.cs` defines `UserCacheRefreshInterval = TimeSpan.FromSeconds(60)` — the client re-validates the cached auth/user state against the server at most once per 60 seconds. confidence 0.9

## 4. Background / Async Writers
- No background DB writer classes (`*/Background*`) were present in the supplied entity extraction, and none were found in a Phase 4 spot check either. **Absence confirmed** — no `*HostedService` for stock-reorder processing exists. confidence 0.75.

## 5. Health Checks — CORRECTED (RC-003)
- Health checks **ARE present and active**: `src/Web/Program.cs` calls `.AddHealthChecks()` (line 87), maps `/health` (line 151), and registers two tagged endpoints — `home_page_health_check` and `api_health_check` (lines 196-197) — used to verify catalog DB connectivity for the home page and API respectively. confidence 0.9. Previously marked "absent / UNKNOWN" — that was incorrect; the health-check files exist under `src/Web/HealthChecks` and are wired into `Program.cs`.

## 6. Configuration-Driven Storage Behavior
- `CatalogSettings` class (src/ApplicationCore/CatalogSettings.cs) — likely binds to an `appsettings` section controlling things like `CatalogBaseUrl` for product images (used by `IUriComposer`/`UriComposer.cs`). confidence 0.75

## Summary
The codebase follows a clean **Repository + Specification pattern** (IRepository/IReadRepository) over two **PostgreSQL** databases (CONFIRMED — RC-001, correcting the earlier SQL Server assumption), with a **localStorage-backed caching layer** on the Blazor admin client (CONFIRMED — RC-004) and active **health checks** at `/health` (CONFIRMED — RC-003, correcting the earlier "absent" finding). The biggest storage-pattern risks remain the **unenforced cross-database BuyerId reference** (see erd.md, data-quality-report.md) and the still-unlocated cache **staleness/expiry comparison logic** for catalog data shown to admins. The stale SQL Server connection strings in `appsettings.Docker.json` are a configuration-drift item for Gate G1.

## Change Records
- **RC-001** (CORRECTED): Relational storage engine — PostgreSQL (Npgsql), not SQL Server/Azure SQL Edge. Evidence: src/Infrastructure/Dependencies.cs, src/Web/appsettings.json. confidence 0.8 → 0.9.
- **RC-003** (CORRECTED): Health checks are present and active in src/Web/Program.cs (`/health`, `home_page_health_check`, `api_health_check`). confidence 0.0 → 0.9.
- **RC-004** (CORRECTED): BlazorAdmin caching is browser localStorage via `ILocalStorageService`/`CacheEntry<T>{Value,DateCreated}`, not IMemoryCache/`{Value,ExpiresAt}`. confidence 0.5 → 0.85.
- **RC-005** (ADDED): CustomAuthStateProvider has a 60-second `UserCacheRefreshInterval`. confidence 0.0 → 0.9.
