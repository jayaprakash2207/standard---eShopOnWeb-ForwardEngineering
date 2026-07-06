## Data Store Registry

| Store Name | Category | Engine / Technology | Version | Declared Database / Collection Name | Connected Services (if detectable) | Source File | Confidence |
|---|---|---|---|---|---|---|---|
| sqlserver | Relational Database | Azure SQL Edge (SQL Server-compatible) | (not declared / latest) | Microsoft.eShopOnWeb.CatalogDb, Microsoft.eShopOnWeb.Identity | eshopwebmvc (Web), eshoppublicapi (PublicApi) | docker-compose.yml; src/Web/appsettings.Docker.json; src/PublicApi/appsettings.Docker.json | HIGH - image/service declared in compose; DB names from Docker connection strings |
| PostgreSQL (eShopCatalog) | Relational Database | PostgreSQL (via Npgsql.EntityFrameworkCore.PostgreSQL) | (not declared) | eShopCatalog | Web (CatalogConnection), PublicApi (CatalogConnection) | src/Web/appsettings.json; src/PublicApi/appsettings.json; src/Infrastructure/Infrastructure.csproj | LOW - VERSION UNKNOWN; no IaC declaration found, host=localhost:5432 implies external/local dev instance |
| PostgreSQL (eShopIdentity) | Relational Database | PostgreSQL (via Npgsql.EntityFrameworkCore.PostgreSQL) | (not declared) | eShopIdentity | Web (IdentityConnection), PublicApi (IdentityConnection) | src/Web/appsettings.json; src/PublicApi/appsettings.json; src/Infrastructure/Infrastructure.csproj | LOW - VERSION UNKNOWN; no IaC declaration found, host=localhost:5432 implies external/local dev instance |
| EF Core InMemory Database | In-Memory / Key-Value Store (test & fallback) | Microsoft.EntityFrameworkCore.InMemory | (not declared) | (not declared - provider only) | Infrastructure, PublicApi, Web, FunctionalTests, IntegrationTests, PublicApiIntegrationTests (`UseOnlyInMemoryDatabase: true`) | src/Infrastructure/Infrastructure.csproj; src/PublicApi/PublicApi.csproj; src/Web/Web.csproj; tests/PublicApiIntegrationTests/appsettings.test.json | LOW - VERSION UNKNOWN; SHARED COMPONENT across Application and Test layers |

---

### VERSION / TECHNOLOGY CONFLICT
- **Primary relational database technology conflict**: `src/Web/appsettings.json` and `src/PublicApi/appsettings.json` (default config) declare PostgreSQL connection strings (`Host=localhost;Port=5432;...`) for `CatalogConnection` and `IdentityConnection`, while `src/Web/appsettings.Docker.json` and `src/PublicApi/appsettings.Docker.json` declare SQL Server connection strings for the same keys (`CatalogConnection`, `IdentityConnection`) pointing at the `sqlserver` (Azure SQL Edge) container declared in `docker-compose.yml`. `src/Infrastructure/Infrastructure.csproj` references both `Npgsql.EntityFrameworkCore.PostgreSQL` and (via PublicApi/Web) `Microsoft.EntityFrameworkCore.SqlServer`. Agent 2 to determine which engine is authoritative per environment (default/local vs Docker) and whether this is intentional dual-provider support or drift.

---

### Chunk Inventory - Data Store Registry
- Technology components found this chunk: Npgsql.EntityFrameworkCore.PostgreSQL, Microsoft.EntityFrameworkCore.SqlServer, Microsoft.EntityFrameworkCore.InMemory, Azure SQL Edge
- Data stores found this chunk: sqlserver (Azure SQL Edge / SQL Server), PostgreSQL (eShopCatalog, eShopIdentity), EF Core InMemory
- Integrations found this chunk: None
- Infrastructure resources found: sqlserver container (docker-compose.yml)
- Environments identified: default/Production-like (PostgreSQL), Docker (SQL Server / Azure SQL Edge)
- Cross-layer dependencies flagged: Data layer connection strings consumed by both Web and PublicApi (Application layer) - SHARED COMPONENT
- Newly flagged as SHARED COMPONENT: EF Core InMemory provider (Infrastructure, PublicApi, Web, multiple test projects)
- VERSION CONFLICTS detected: Primary database engine conflict between default appsettings (PostgreSQL) and Docker appsettings (SQL Server / Azure SQL Edge) - see above
- LOW CONFIDENCE items raised this chunk:
  - PostgreSQL version not declared anywhere (package reference has no version pin)
  - Azure SQL Edge image has no tag declared in docker-compose.yml (defaults to `latest`)
  - PostgreSQL host (`localhost:5432`) has no corresponding IaC/container declaration in provided files - may be expected to run externally or in a separate compose file not provided
