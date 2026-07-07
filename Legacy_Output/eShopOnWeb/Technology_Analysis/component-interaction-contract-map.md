# Component Interaction & Contract Map

> Built from Agent 1's Component & Service Map and Integration & Dependency Graph, traced against
> connection strings, project references, and `baseUrls` configuration found in
> `appsettings*.json`. No HTTP client source code (`HttpClient` registrations, message
> contracts) was available, so protocol/contract details beyond configuration-file evidence are
> marked LOW or ASSUMED.

## Component Interaction & Contract Map

| Caller | Target | Protocol | Interaction Type | Coupling Strength | Contract | Timeout Declared? | Error Handling | Notes |
|---|---|---|---|---|---|---|---|---|
| BlazorAdmin | eshoppublicapi (PublicApi) | HTTP/HTTPS | Sync Request-Response | Loose - cross-process, configurable base URL per environment | Swagger/OpenAPI generated at runtime by Swashbuckle (no static spec file checked in) - effectively Undocumented from a contract-versioning standpoint | No - RISK (no `HttpClient` timeout config found in any appsettings; `System.Net.Http.Json` referenced but no policy config) | No error handling evidence found - RISK | `apiBase` differs per environment: `https://localhost:5099/api/` (default/dev), `http://localhost:5200/api/` (Docker) |
| BlazorAdmin | eshopwebmvc (Web) | HTTP/HTTPS | Sync Request-Response | Loose - cross-process, configurable base URL per environment | Undocumented (no OpenAPI/contract file found for Web's API surface, if any) | No - RISK | No error handling evidence found - RISK | `webBase` differs per environment: `https://localhost:44315/` (default/dev), `http://host.docker.internal:5106/` (Docker) |
| eshopwebmvc (Web) | Catalog/Identity data store | TCP/SQL via EF Core | Sync Request-Response (data access) | Tight - direct schema access, shared with PublicApi (see Coupling Hotspots) | EF Core model (code-first, no migration files found in `Data\Migrations\`) | No - connection pool/command timeout NOT declared in any appsettings (NFR gap) | Unknown - EF Core default exception propagation assumed; no retry policy configured | Provider switches: Npgsql (`appsettings.json`) vs SqlServer (`appsettings.Docker.json`) for identical connection-string keys (AP-08) |
| eshoppublicapi (PublicApi) | Catalog/Identity data store | TCP/SQL via EF Core | Sync Request-Response (data access) | Tight - direct schema access, shared with Web | Same EF Core model as Web (both reference Infrastructure) | No - same gap as above | Same as above | Same provider-switch pattern as Web (AP-08) |
| eshopwebmvc (Web) | sqlserver (compose service) | TCP | Infra dependency | Tight - `depends_on` is a startup-order hint only, no health-check gating | N/A | N/A | N/A - `depends_on` without `condition: service_healthy` means Web may start before SQL Server is ready to accept connections | docker-compose.yml |
| eshoppublicapi (PublicApi) | sqlserver (compose service) | TCP | Infra dependency | Tight - same `depends_on` caveat as above | N/A | N/A | N/A | docker-compose.yml |
| Web (BlazorAdmin host) | BlazorAdmin (WASM) | In-process (hosted WASM, static file serving) | N/A (asset hosting, not RPC) | Tight - compiled into the same deployable (AP-11) | N/A | N/A | N/A | `Microsoft.AspNetCore.Components.WebAssembly.Server` in Web.csproj + ProjectReference |
| Web | Azure Key Vault | HTTPS (Azure SDK) | Sync (config-load time, if used) | Loose in principle (external service), but unwired - no vault name configured | N/A | Unknown | Unknown | Declared via `Azure.Extensions.AspNetCore.Configuration.Secrets`/`Azure.Identity`; `infra/main.parameters.json` references `${AZURE_KEY_VAULT_NAME}` but no vault resource declaration found |
| CI (GitHub Actions) | NuGet.org | HTTPS | Async (scheduled PR creation) | Loose | Dependabot manifest-driven | N/A | N/A | `.github/dependabot.yml`, daily schedule |
| CI (GitHub Actions, dotnetcore.yml) | eShopOnWeb.sln (build/test target) | Local process (`dotnet build`/`dotnet test`) | Sync | N/A | N/A | N/A | N/A | Runs on `[push, pull_request, workflow_dispatch]` |
| CI (GitHub Actions, richnav.yml) | Everything.sln + RichCodeNavIndexer service | Local process + GitHub-hosted action | Sync (manual trigger) | Loose | N/A | N/A | N/A | `workflow_dispatch` only - not part of normal build/test flow |

---

### Coupling Hotspots

| Component | Inbound Dependencies | Outbound Dependencies | Coupling Risk |
|---|---|---|---|
| Catalog/Identity data store (Postgres `eShopCatalog`/`eShopIdentity` or SQL Server `Microsoft.eShopOnWeb.CatalogDb`/`Microsoft.eShopOnWeb.Identity`) | 2 (Web, PublicApi - both via Infrastructure/EF Core) | 0 | **High - two independently deployable services (Web, PublicApi) read and write the same schema directly via EF Core with no API boundary between them.** This is a shared-database coupling pattern: a schema change required by one service's EF model can break the other at runtime with no compile-time signal, since both reference the same `Infrastructure` project but are deployed as separate containers |
| Infrastructure (class library) | 2 (Web, PublicApi project references) | 3 (Npgsql, SqlServer, InMemory EF providers) | High - any change to `Infrastructure`'s `DbContext`/migrations affects both deployable services simultaneously; combined with AP-08 (environment-switched providers), this is the single highest-risk shared component in the system |
| ApplicationCore | 3 (Infrastructure, Web, PublicApi via transitive/direct project references) | 1 (BlazorShared) | Medium - typical domain-core fan-in for a layered architecture; risk is acceptable provided ApplicationCore has no external/infra dependencies (confirmed - only BlazorShared + NuGet packages) |
| BlazorShared | 2 (ApplicationCore, BlazorAdmin) | 0 | Low - shared validation/model library, narrow surface (FluentValidation, BlazorInputFile) |
| eshoppublicapi (PublicApi) | 1 (BlazorAdmin via `apiBase`) | 1 (data store) | Medium - single inbound caller currently identified (BlazorAdmin); if PublicApi is intended as the system's primary external API (Swagger-documented, JWT packages present), the lack of a discovered external consumer plus the lack of API versioning is a contract-stability risk going forward |
| eshopwebmvc (Web) | 1 (BlazorAdmin via `webBase`) + end users (MVC/Razor UI, not modelled as a "component" here) | 2 (data store, BlazorAdmin hosting) | Medium - Web is both a UI host and (per `webBase` config) an HTTP target for BlazorAdmin; dual role increases blast radius of any Web outage |

---

### API Contract Inventory

| Boundary | Contract Type | Version | Location | Breaking Change Risk |
|---|---|---|---|---|
| eshoppublicapi (PublicApi) public REST API | OpenAPI (generated at runtime via Swashbuckle) | UNVERSIONED - no API versioning package (`Asp.Versioning.*` or similar) found in `PublicApi.csproj`, no `/v1/` route convention evidence | Generated at runtime (Swagger UI), no static spec file committed to source | **High** - no version segment in routes (assumed) and no static contract artifact means BlazorAdmin (and any future consumer) has no stable contract to pin against; any endpoint signature change is an immediate breaking change for all callers |
| eshopwebmvc (Web) -> BlazorAdmin interaction surface | Undocumented | UNVERSIONED | Not found - `webBase` config exists but no contract artifact located | Medium - lower risk than PublicApi since both are typically deployed together (Web hosts BlazorAdmin), but the Docker-environment config (`http://host.docker.internal:5106/`) implies they CAN run as separate processes, reintroducing the versioning risk |
| Catalog/Identity data schema (Infrastructure EF Core model) | Implicit schema contract (code-first EF model, shared by Web & PublicApi) | UNVERSIONED - `Data\Migrations\` folder declared but empty; no migration history found | src/Infrastructure/Infrastructure.csproj (`Folder Include="Data\Migrations\"`) | **High** - see Coupling Hotspots; combined with an empty migrations folder, there is no recorded schema-evolution history, making it impossible to assess how the shared schema has changed over time or to coordinate changes across Web and PublicApi |

---

### Cross-Layer Notes

- The dual EF Core provider pattern (AP-08) means the **coupling strength between Web/PublicApi
  and the data store differs by environment**: in the Docker environment both services point at
  the single `sqlserver` container (tight, single point of failure); in the default/local
  environment both point at `localhost:5432` Postgres (tight, but to an externally-managed
  instance not declared in any IaC reviewed).
- No message broker, event bus, or queue technology appears anywhere in the stack - all
  inter-component communication identified is synchronous (HTTP or direct DB). This is consistent
  with the absence of async/event-driven architecture patterns noted in the Architecture Pattern
  Catalog.
