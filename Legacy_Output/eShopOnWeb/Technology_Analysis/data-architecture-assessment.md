# Data Architecture Assessment

> Built from Agent 1's Data Store Registry. No `DbContext`, repository, or migration source files
> were available, so access-pattern and transaction-scope findings are largely ASSUMED from the
> package set (EF Core + Ardalis.Specification.EntityFrameworkCore) and the empty
> `Data\Migrations\` folder declaration.

## Data Store Deep Dive

| Store | Access Pattern | ORM / Query Style | Transaction Scope | Consistency Model | Connection Pool Config | Migration State | Agent 1 Match? |
|---|---|---|---|---|---|---|---|
| PostgreSQL `eShopCatalog` (default/local environment, via Npgsql.EntityFrameworkCore.PostgreSQL) | ASSUMED Repository/Specification pattern (Ardalis.Specification.EntityFrameworkCore present in Infrastructure) | EF Core code-first | None found - no explicit `BeginTransaction`/`[Transactional]` evidence; EF Core default per-`SaveChanges()` transaction ASSUMED | Strong (relational, single-instance Postgres assumed - `Host=localhost`) | DEFAULT - not declared (Npgsql default `Maximum Pool Size=100`); see NFR-07 | `Data\Migrations\` folder declared empty in Infrastructure.csproj - **no migration files found** -> schema drift risk / cannot confirm schema is reproducible from source | Confirmed as the default-environment store (Agent 1 had flagged provider ambiguity - resolved: Postgres is default, see AP-08) |
| PostgreSQL `eShopIdentity` (default/local environment) | ASSUMED EF Core Identity store (Microsoft.AspNetCore.Identity.EntityFrameworkCore) | EF Core code-first, ASP.NET Identity schema | None found - ASP.NET Identity's default per-operation `SaveChanges()` ASSUMED | Strong | DEFAULT - not declared; see NFR-07 | Same empty-migrations-folder gap as above | Confirmed as default-environment store |
| SQL Server `Microsoft.eShopOnWeb.CatalogDb` (Docker environment, via Microsoft.EntityFrameworkCore.SqlServer, `sqlserver` compose service / Azure SQL Edge) | Same as Postgres equivalent above - same EF model (Infrastructure project is shared, only the provider/connection string changes) | EF Core code-first | Same as above | Strong, but **collation/isolation-level defaults differ between SQL Server and Postgres** - not verified to be aligned (configuration risk, see TD register) | DEFAULT - not declared (SqlClient default `Max Pool Size=100`); see NFR-07 | Same empty-migrations-folder gap | Confirmed as Docker-environment store; this is the SAME logical database as the Postgres entry above, switched by `ASPNETCORE_ENVIRONMENT` |
| SQL Server `Microsoft.eShopOnWeb.Identity` (Docker environment) | Same as above | EF Core code-first, ASP.NET Identity schema | Same as above | Same caveat as above | DEFAULT - not declared | Same gap | Confirmed as Docker-environment store; same logical database as the Postgres Identity entry |
| EF Core InMemory Database | N/A - test double / potential runtime fallback | EF Core InMemory provider | N/A | None (volatile, in-process) | N/A | N/A | Confirmed SHARED COMPONENT (Agent 1); **new finding**: also referenced directly by `Web.csproj` and `PublicApi.csproj` (not only test projects), suggesting a runtime configuration switch (e.g. `UseOnlyInMemoryDatabase`) exists in `Program.cs` (not provided) - see TD-16 |

---

### Data Ownership Map

| Entity / Table | Owning Service | Other Services With Access | Access Type | Coupling Risk |
|---|---|---|---|---|
| Catalog schema (CatalogBrand, CatalogType, CatalogItem, etc. - inferred from `CatalogConnection` / `CatalogBaseUrl` config keys; exact table names not available without migration files) | Infrastructure (shared library, deployed inside both Web and PublicApi) | Web (read/write, MVC + Blazor admin UI per BlazorAdmin's `Services\CatalogItem\*` files), PublicApi (read/write, REST API) | Shared write | **ANTIPATTERN** - two independently deployable services both have direct EF Core write access to the same catalog schema with no single owning service or API boundary between them |
| Identity schema (ASP.NET Core Identity tables - AspNetUsers, AspNetRoles, etc., inferred from `IdentityConnection`) | Infrastructure (shared library, deployed inside both Web and PublicApi) | Web (read/write - cookie auth UI), PublicApi (read/write - declared JWT packages, unconfigured) | Shared write | **ANTIPATTERN** - same shared-schema concern as Catalog; additionally, if PublicApi is meant to validate JWTs issued via Web's Identity cookie auth, the token-issuance/validation relationship is undocumented (no JWT config found - see AP-10) |

---

### Data Flow & Consistency Notes

- **Provider duality (AP-08) is the dominant data-architecture finding.** The same logical
  databases (Catalog, Identity) are declared against two different RDBMS engines depending on
  `ASPNETCORE_ENVIRONMENT`:
  - Default/local: PostgreSQL, `Host=localhost;Port=5432`, credentials `postgres`/`Clarium123`
    (hardcoded in source - see Security Architecture Assessment, Secrets Posture)
  - Docker: SQL Server-compatible (Azure SQL Edge), `Server=sqlserver,1433`, credentials
    `sa`/`@someThingComplicated1234` (hardcoded in source and in `docker-compose.yml`)

  Because the EF Core model in `Infrastructure` is shared between providers, any
  provider-specific SQL generated by EF Core (e.g. `JSONB` vs `NVARCHAR`, sequence vs identity
  column behaviour, default collation) could behave differently between local development and
  the Docker/CI-adjacent environment. **No evidence was found that this divergence has been
  tested** - the CI pipeline (`dotnetcore.yml`) runs `dotnet test` against the solution but does
  not set `ASPNETCORE_ENVIRONMENT=Docker`, so tests likely execute against whichever provider the
  default `appsettings.json` (Postgres) or the InMemory provider resolves to, not the Docker/SQL
  Server path that is intended for containerised/production-like deployment.

- **No event-driven or eventual-consistency patterns found.** No message broker, outbox table, or
  domain-event-publishing package appears in any `.csproj`. All cross-component data interaction
  identified (Component Interaction & Contract Map) is synchronous EF Core or synchronous HTTP.
  Consistency model for the whole system is therefore **strong/immediate consistency by default**,
  constrained to whatever a single relational engine instance provides per environment.

- **No connection resiliency configuration found** for either provider (no `EnableRetryOnFailure`,
  no Polly policy, no command timeout override) - transient faults against the shared database
  (especially in the Docker environment where `depends_on` does not gate on health) have no
  documented mitigation. See Pattern Coverage Gaps in the Architecture Pattern Catalog and NFR-07.

- **Migration state is the most significant data-architecture risk identified.** The
  `Infrastructure.csproj` explicitly declares a `Data\Migrations\` folder but no migration files
  were found in the provided file set. Combined with two RDBMS providers sharing one EF model,
  this means there is no verifiable, version-controlled record of how the schema is created or
  evolved for either Postgres or SQL Server - schema creation may rely on
  `EnsureCreated()`/`Database.Migrate()` calls in `Program.cs` (not provided) with an
  uninitialised migrations folder, which is itself a common source of "works on my machine"
  schema drift between developers and environments.
