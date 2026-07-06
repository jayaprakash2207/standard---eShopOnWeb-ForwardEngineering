I now have all data needed. Producing the full Agent 1 output.

---

## Agent 1 - Chunk 0 of 6 - Project-Wide Structural Scan

**Directory structure (top-level + 2 levels):**
```
eShopOnWeb/
├── src/
│   ├── ApplicationCore/       (domain model, no framework deps)
│   ├── BlazorAdmin/           (Blazor WebAssembly admin panel)
│   ├── BlazorShared/          (shared Blazor DTOs/models)
│   ├── Infrastructure/        (EF Core data access)
│   ├── PublicApi/             (ASP.NET Core REST API)
│   └── Web/                   (ASP.NET Core MVC host app)
├── tests/
│   ├── FunctionalTests/
│   ├── IntegrationTests/
│   ├── PublicApiIntegrationTests/
│   └── UnitTests/
├── infra/
│   ├── core/database/sqlserver/
│   ├── core/host/
│   └── core/security/
└── .github/workflows/
```

**Project Scan Summary (Chunk 0):**
- Language: C# / .NET 8.0 (SDK 8.0.x, rollForward: latestFeature)
- Framework: ASP.NET Core 8.0 (MVC + Blazor WebAssembly + Minimal/Endpoint API)
- Architecture style: Modular Monolith - HIGH (single solution, Clean Architecture layering, single DB server, two deployable containers)
- Deployment target: Azure App Service (azure.yaml declares `host: appservice`); Docker Compose for local development
- Technology layers found: 6 — Application, Data, Infrastructure, CI/CD, Security, Observability
- Deployable services: 2 (eshopwebmvc, eshoppublicapi)
- Data stores: 2 logical SQL databases (CatalogDb, Identity)
- External integrations: Azure App Service, Azure SQL, Azure Key Vault, Application Insights (Bicep reference), GitHub Actions (checkout, setup-dotnet, RichCodeNavIndexer)

**All manifest / config / pipeline files located:**
- Package manifests: `Directory.Packages.props`, `src/ApplicationCore/ApplicationCore.csproj`, `src/BlazorAdmin/BlazorAdmin.csproj`, `src/BlazorShared/BlazorShared.csproj`, `src/Infrastructure/Infrastructure.csproj`, `src/PublicApi/PublicApi.csproj`, `src/Web/Web.csproj`, `tests/FunctionalTests/FunctionalTests.csproj`, `tests/IntegrationTests/IntegrationTests.csproj`, `tests/PublicApiIntegrationTests/PublicApiIntegrationTests.csproj`, `tests/UnitTests/UnitTests.csproj`
- Container configs: `docker-compose.yml`, `docker-compose.override.yml`, `src/Web/Dockerfile`, `src/PublicApi/Dockerfile`
- IaC (Bicep): `infra/main.bicep`, `infra/main.parameters.json`, `infra/core/database/sqlserver/sqlserver.bicep`, `infra/core/host/appservice.bicep`, `infra/core/host/appserviceplan.bicep`, `infra/core/security/keyvault-access.bicep`, `infra/core/security/keyvault.bicep`
- CI/CD pipelines: `.github/workflows/dotnetcore.yml` (entry point), `.github/workflows/richnav.yml` (entry point); no reusable workflow templates
- Config files: `global.json`, `azure.yaml`, `src/Web/appsettings.json`, `src/Web/appsettings.Docker.json`, `src/Web/appsettings.Development.json`, `src/PublicApi/appsettings.json`, `src/PublicApi/appsettings.Docker.json`, `src/PublicApi/appsettings.Development.json`, `tests/PublicApiIntegrationTests/appsettings.test.json`
- Frontend library manager: `src/Web/libman.json`
- Local tooling: `src/Web/.config/dotnet-tools.json`

**Chunk Plan (highest information density first):**
1. Chunk 1 - Application Layer (Directory.Packages.props + all .csproj files — full dependency tree)
2. Chunk 2 - Data Layer (docker-compose services, EF Core contexts, connection string keys, schema entities)
3. Chunk 3 - Infrastructure Layer (Dockerfiles, Bicep IaC — Azure resource types and config)
4. Chunk 4 - CI/CD & Deployment Layer (.github/workflows/*, azure.yaml, dependabot.yml)
5. Chunk 5 - Security Layer (JWT, ASP.NET Identity, Azure Key Vault, TLS, CORS from Bicep)
6. Chunk 6 - Observability Layer (App Insights Bicep reference, logging config in appsettings)

---

## Agent 1 - Chunk 1 of 6 - Application Layer

**Carried Forward from Prior Chunks:**
- Technology components: none yet
- Data stores: none yet
- Integrations: none yet
- LOW CONFIDENCE items: 0

---

**Source: `Directory.Packages.props` (centralized NuGet version management)**

Runtime/SDK:
- TargetFramework: `net8.0`
- AspNetVersion property: `8.0.2`
- SystemExtensionVersion: `8.0.0`
- EntityFramworkCoreVersion (sic): `8.0.2`
- VSCodeGeneratorVersion: `8.0.0`

Core application packages:
- Ardalis.ApiEndpoints 4.1.0
- Ardalis.GuardClauses 4.0.1
- Ardalis.Specification.EntityFrameworkCore 7.0.0
- Ardalis.Result 7.0.0
- Ardalis.Specification 7.0.0
- Ardalis.ListStartupServices 1.1.4
- AutoMapper.Extensions.Microsoft.DependencyInjection 12.0.1
- FluentValidation 11.9.0
- MediatR 12.0.1
- MinimalApi.Endpoint 1.3.0

Blazor / ASP.NET Core:
- Microsoft.AspNetCore.Components.Authorization 8.0.2
- Microsoft.AspNetCore.Components.WebAssembly 8.0.2
- Microsoft.AspNetCore.Components.WebAssembly.Authentication 8.0.2
- Microsoft.AspNetCore.Components.WebAssembly.DevServer 8.0.2 (PrivateAssets=All)
- Microsoft.AspNetCore.Components.WebAssembly.Server 8.0.2
- Microsoft.AspNetCore.Identity.EntityFrameworkCore 8.0.2
- Microsoft.AspNetCore.Authentication.JwtBearer 8.0.2
- Microsoft.AspNetCore.Diagnostics.EntityFrameworkCore 8.0.2
- Microsoft.AspNetCore.Identity.UI 8.0.2
- Microsoft.AspNetCore.Mvc 2.2.0  ← VERSION CONFLICT: 2.2.0 vs all other ASP.NET packages at 8.0.2
- Microsoft.Extensions.Identity.Core 8.0.2
- Microsoft.Extensions.Logging.Configuration 8.0.0
- Microsoft.VisualStudio.Web.CodeGeneration.Design 8.0.0
- Microsoft.Web.LibraryManager.Build 2.1.175

Azure:
- Azure.Extensions.AspNetCore.Configuration.Secrets 1.3.1
- Azure.Identity 1.10.4

UI libraries:
- BlazorInputFile 0.2.0
- Blazored.LocalStorage 4.5.0

Build / Bundling:
- BuildBundlerMinifier 3.2.449

EF Core:
- Microsoft.EntityFrameworkCore.InMemory 8.0.2
- Microsoft.EntityFrameworkCore.SqlServer 8.0.2
- Microsoft.EntityFrameworkCore.Tools 8.0.2

API Documentation:
- Swashbuckle.AspNetCore 6.5.0
- Swashbuckle.AspNetCore.SwaggerUI 6.5.0
- Swashbuckle.AspNetCore.Annotations 6.5.0

Security / Token:
- System.IdentityModel.Tokens.Jwt 7.3.1
- System.Security.Claims 4.3.0
- System.Text.Json 8.0.3
- System.Net.Http.Json 8.0.0

Infrastructure tooling:
- Microsoft.VisualStudio.Azure.Containers.Tools.Targets 1.19.6
- NSubstitute 5.1.0
- NSubstitute.Analyzers.CSharp 1.0.17

Test frameworks:
- Microsoft.AspNetCore.Mvc.Testing 8.0.2
- Microsoft.NET.Test.Sdk 17.9.0
- xunit 2.7.0
- xunit.runner.visualstudio 2.5.6
- xunit.runner.console 2.7.0
- MSTest.TestAdapter 3.2.2
- MSTest.TestFramework 3.2.2
- coverlet.collector 6.0.2

**Source: `src/Web/libman.json` (frontend libraries via cdnjs)**
- jquery 3.6.3
- twitter-bootstrap 3.4.1
- jquery-validation-unobtrusive 4.0.0
- jquery-validate 1.19.5
- toastr.js 2.1.4
- aspnet-signalr 1.0.27

**Source: `src/Web/.config/dotnet-tools.json`**
- dotnet-ef 8.0.0

**Source: `src/Web/bundleconfig.json`**
- CSS bundling: site.min.css (SCSS sources confirmed via compilerconfig.json)
- JS bundling: site.min.js, minify enabled

**Source: FunctionalTests.csproj**
- DotNetCliToolReference dotnet-xunit 2.3.1 (legacy tool reference, LOW — tool references are deprecated in modern .NET SDK)

**Project references graph (from .csproj files):**
- Web → ApplicationCore, BlazorAdmin, BlazorShared, Infrastructure
- PublicApi → ApplicationCore, Infrastructure
- BlazorAdmin → BlazorShared
- Infrastructure → ApplicationCore
- FunctionalTests → ApplicationCore, PublicApi, Web
- IntegrationTests → Infrastructure, UnitTests
- PublicApiIntegrationTests → PublicApi, Web
- UnitTests → ApplicationCore, Web

---

### Chunk Inventory - Application Layer
- Technology components found this chunk: .NET 8.0, ASP.NET Core 8.0 MVC, Blazor WebAssembly 8.0, EF Core 8.0.2, MediatR 12.0.1, AutoMapper 12.0.1, FluentValidation 11.9.0, Ardalis.Specification 7.0.0, Swashbuckle 6.5.0, JWT Bearer 8.0.2, ASP.NET Identity 8.0.2, Azure.Identity 1.10.4, SignalR 1.0.27 (client), jQuery 3.6.3, Bootstrap 3.4.1
- Data stores found this chunk: none (connection keys found; store detail in Chunk 2)
- Integrations found this chunk: none (Azure integration details in Chunk 3)
- Infrastructure resources found: none
- Environments identified: none (detail in Chunks 3/4)
- CI/CD tool invocations found: none (detail in Chunk 4)
- Reusable workflows followed: None
- Cross-layer dependencies flagged: None
- Newly flagged as SHARED COMPONENT: `Microsoft.EntityFrameworkCore.SqlServer` (Application + Data layers), `Azure.Identity` (Application + Security layers), `System.IdentityModel.Tokens.Jwt` (Application + Security layers)
- VERSION CONFLICTS detected: `Microsoft.AspNetCore.Mvc` declared 2.2.0 in Directory.Packages.props; all other `Microsoft.AspNetCore.*` packages at 8.0.2 — Agent 2 to determine if this is intentional or stale
- LOW CONFIDENCE items raised this chunk: `dotnet-xunit 2.3.1` — legacy DotNetCliToolReference in FunctionalTests.csproj; deprecated in .NET SDK; may not function as declared

---

## Agent 1 - Chunk 2 of 6 - Data Layer

**Carried Forward from Prior Chunks:**
- Technology components: .NET 8.0, ASP.NET Core 8.0, EF Core 8.0.2, MediatR, AutoMapper, FluentValidation, Ardalis.Specification, Swashbuckle, JWT Bearer, ASP.NET Identity, Azure.Identity, SignalR client, jQuery, Bootstrap
- Data stores: none confirmed yet
- Integrations: none yet
- LOW CONFIDENCE items: 1 (dotnet-xunit legacy tool ref)

---

**Source: `docker-compose.yml` + `docker-compose.override.yml` — data store services**

- `sqlserver` service: image `mcr.microsoft.com/azure-sql-edge` (no explicit tag — UNKNOWN version tag), port 1433:1433, env key `SA_PASSWORD` (SECRETS MANAGEMENT PATTERN DETECTED — plaintext secret in compose file), `ACCEPT_EULA=Y`

**Source: `src/Web/appsettings.json` + `src/PublicApi/appsettings.json` — connection string key names**
- `ConnectionStrings.CatalogConnection` → local: `Server=(localdb)\\mssqllocaldb; Initial Catalog=Microsoft.eShopOnWeb.CatalogDb`
- `ConnectionStrings.IdentityConnection` → local: `Server=(localdb)\\mssqllocaldb; Initial Catalog=Microsoft.eShopOnWeb.Identity`

**Source: `src/Web/appsettings.Docker.json` + `src/PublicApi/appsettings.Docker.json`**
- CatalogConnection → `Server=sqlserver,1433; Initial Catalog=Microsoft.eShopOnWeb.CatalogDb; User Id=sa` (SECRETS MANAGEMENT PATTERN DETECTED — SA credentials embedded in Docker config files)
- IdentityConnection → `Server=sqlserver,1433; Initial Catalog=Microsoft.eShopOnWeb.Identity; User Id=sa`

**Source: `database.json` — EF Core entities (CatalogContext.cs)**
- EF Entities: CatalogBrand, CatalogType, CatalogItem, Basket, BasketItem, OrderItem, Order — all registered in `src/Infrastructure/Data/CatalogContext.cs`
- Note: No separate IdentityContext entity listing — ASP.NET Identity uses standard schema tables; db_contexts array is empty in database.json (LOW — EF DbContext names not extracted by Layer 1; Agent 2 to resolve from Infrastructure source)

**Source: `tests/PublicApiIntegrationTests/appsettings.test.json`**
- `UseOnlyInMemoryDatabase: true` — in-memory database substitution for integration tests

**Source: `infra/main.bicep` — Azure SQL logical databases declared**
- Catalog database: `catalogDatabase` (param default), connection string key `AZURE-SQL-CATALOG-CONNECTION-STRING`
- Identity database: `identityDatabase` (param default), connection string key `AZURE-SQL-IDENTITY-CONNECTION-STRING`

---

### Chunk Inventory - Data Layer
- Technology components found this chunk: SQL Server (Azure SQL Edge for Docker local dev), SQL Server (Azure SQL via Bicep for cloud), EF Core (SHARED — already in Chunk 1), Microsoft.EntityFrameworkCore.InMemory 8.0.2 (test store)
- Data stores found this chunk:
  - `sqlserver` (Docker local) — Azure SQL Edge, version UNKNOWN (no tag), databases: Microsoft.eShopOnWeb.CatalogDb + Microsoft.eShopOnWeb.Identity
  - `catalogDatabase` (Azure) — Azure SQL, version 12.0 (from Bicep), database name: catalogDatabase
  - `identityDatabase` (Azure) — Azure SQL, version 12.0 (from Bicep), database name: identityDatabase
  - In-memory store (test only) — Microsoft.EntityFrameworkCore.InMemory 8.0.2
- Integrations found this chunk: None
- Infrastructure resources found: None (Azure SQL resource detail in Chunk 3)
- Environments identified: local (localdb/Docker), Azure (Bicep)
- CI/CD tool invocations found: None
- Reusable workflows followed: None
- Cross-layer dependencies flagged: `infra/main.bicep` declares SQL databases (cross-layer: Data ↔ Infrastructure)
- Newly flagged as SHARED COMPONENT: `sqlserver` Docker service (Data + Infrastructure layers)
- VERSION CONFLICTS detected: None
- LOW CONFIDENCE items raised this chunk: `mcr.microsoft.com/azure-sql-edge` — no version tag declared in docker-compose.yml; EF DbContext names not extracted (db_contexts array empty in database.json)

---

## Agent 1 - Chunk 3 of 6 - Infrastructure Layer

**Carried Forward from Prior Chunks:**
- Technology components: .NET 8.0, ASP.NET Core 8.0, EF Core 8.0.2, SQL Server (Azure SQL Edge local + Azure SQL 12.0 cloud), InMemory EF (test), MediatR, AutoMapper, FluentValidation, Ardalis.Specification, Swashbuckle, JWT Bearer, ASP.NET Identity, Azure.Identity, SignalR client, jQuery, Bootstrap
- Data stores: sqlserver (local Docker), catalogDatabase (Azure SQL 12.0), identityDatabase (Azure SQL 12.0), InMemory (test)
- Integrations: none yet
- LOW CONFIDENCE items: 2

---

**Source: `src/Web/Dockerfile`**
- Build stage: `mcr.microsoft.com/dotnet/sdk:8.0`
- Runtime stage: `mcr.microsoft.com/dotnet/aspnet:8.0`
- Build commands: `dotnet restore`, `dotnet publish -c Release -o out`
- ENTRYPOINT: `["dotnet", "Web.dll"]`
- No EXPOSE declared in Dockerfile (port exposed via docker-compose.override.yml: 5106:8080)

**Source: `src/PublicApi/Dockerfile`**
- Base stage: `mcr.microsoft.com/dotnet/aspnet:8.0`, EXPOSE 80, EXPOSE 443
- Build stage: `mcr.microsoft.com/dotnet/sdk:8.0`
- Build commands: `dotnet restore`, `dotnet build`, `dotnet publish -c Release -o /app/publish`
- ENTRYPOINT: `["dotnet", "PublicApi.dll"]`

**Source: `docker-compose.yml` + `docker-compose.override.yml`**
- Compose format version: 3.4
- `eshopwebmvc`: image `${DOCKER_REGISTRY-}eshopwebmvc`, build context `.`, dockerfile `src/Web/Dockerfile`, depends_on `sqlserver`, port 5106:8080, env keys: ASPNETCORE_ENVIRONMENT, ASPNETCORE_URLS, volumes: `~/.aspnet/https`, `~/.microsoft/usersecrets`
- `eshoppublicapi`: image `${DOCKER_REGISTRY-}eshoppublicapi`, build context `.`, dockerfile `src/PublicApi/Dockerfile`, depends_on `sqlserver`, port 5200:8080, env keys: ASPNETCORE_ENVIRONMENT, ASPNETCORE_URLS, volumes: `~/.aspnet/https`, `~/.microsoft/usersecrets`
- `sqlserver`: image `mcr.microsoft.com/azure-sql-edge`, port 1433:1433, env keys: SA_PASSWORD, ACCEPT_EULA

**Source: `azure.yaml`**
- Azure Developer CLI (azd) v1.0 schema
- Service: `web`, project `./src/Web`, language `csharp`, host `appservice`

**Source: `infra/main.bicep`**
- Scope: subscription
- Resource Group: `rg-${environmentName}` (abbrs.resourcesResourceGroups)
- App Service (web): `app-web-${resourceToken}`, dotnetcore|8.0, Linux, App Service Plan B1; managed identity: SystemAssigned; config keys: AZURE_SQL_CATALOG_CONNECTION_STRING_KEY, AZURE_SQL_IDENTITY_CONNECTION_STRING_KEY, AZURE_KEY_VAULT_ENDPOINT, APPLICATIONINSIGHTS_CONNECTION_STRING (if applicationInsightsName provided), SCM_DO_BUILD_DURING_DEPLOYMENT, ENABLE_ORYX_BUILD; httpsOnly: true; minTlsVersion: 1.2; ftpsState: FtpsOnly; alwaysOn: true
- App Service Plan: `plan-${resourceToken}`, SKU B1, Linux (reserved: true)
- SQL Server (catalog): `sql-catalog-${resourceToken}`, SQL version 12.0, minimalTlsVersion 1.2, publicNetworkAccess Enabled, firewall: 0.0.0.1–255.255.255.254
- SQL Server (identity): `sql-identity-${resourceToken}`, same config
- Key Vault: `kv-${resourceToken}`, Standard SKU, secrets: get+list for principalId

**Source: `infra/core/database/sqlserver/sqlserver.bicep`**
- Resource: `Microsoft.Sql/servers@2022-05-01-preview`
- Resource: `Microsoft.Resources/deploymentScripts@2020-10-01` — Azure CLI 2.37.0, downloads go-sqlcmd v0.8.1, creates app user in DB
- Resource: Key Vault secrets — sqlAdminPassword, appUserPassword, AZURE-SQL-CONNECTION-STRING
- Env var keys: APPUSERNAME, APPUSERPASSWORD, DBNAME, DBSERVER, SQLCMDPASSWORD, SQLADMIN

**Source: `infra/core/host/appservice.bicep`**
- Resource: `Microsoft.Web/sites@2022-03-01`
- Config: `Microsoft.Web/sites/config` (appsettings + logs)
- Log retention: 1 day, 35MB file system; application logs verbose; detailed errors enabled; failed request tracing enabled
- CORS: `union(['https://portal.azure.com', 'https://ms.portal.azure.com'], allowedOrigins)`
- Optional integration: Application Insights (`APPLICATIONINSIGHTS_CONNECTION_STRING` added if applicationInsightsName non-empty) — LOW — no Application Insights Bicep resource declared in this repository; referenced as existing resource only

**Source: `infra/core/host/appserviceplan.bicep`**
- Resource: `Microsoft.Web/serverfarms@2022-03-01`, SKU B1, Linux

**Source: `infra/core/security/keyvault.bicep` + `keyvault-access.bicep`**
- Resource: `Microsoft.KeyVault/vaults@2022-07-01`, Standard SKU, secrets: get+list
- AccessPolicy resource: `Microsoft.KeyVault/vaults/accessPolicies@2022-07-01`

**Source: `infra/main.parameters.json`**
- Param env vars: AZURE_ENV_NAME, AZURE_LOCATION, AZURE_PRINCIPAL_ID, AZURE_KEY_VAULT_NAME

---

### Chunk Inventory - Infrastructure Layer
- Technology components found this chunk: Docker (compose v3.4), mcr.microsoft.com/dotnet/sdk:8.0, mcr.microsoft.com/dotnet/aspnet:8.0, Azure App Service (dotnetcore 8.0, Linux, B1), Azure App Service Plan (B1), Azure SQL Server (version 12.0 API 2022-05-01-preview), Azure Key Vault (Standard, API 2022-07-01), Azure CLI 2.37.0, go-sqlcmd v0.8.1, Azure Developer CLI (azd)
- Data stores found this chunk: Azure SQL (SHARED — Chunk 2)
- Integrations found this chunk: Application Insights (LOW — referenced as existing resource; no Bicep module in repo), Azure Key Vault (HIGH)
- Infrastructure resources found: App Service (web), App Service Plan (B1), SQL Server x2 (catalog + identity), Key Vault, Deployment Script (Azure CLI)
- Environments identified: Azure (subscription-scoped, environment name parameterised via AZURE_ENV_NAME), Docker local dev
- CI/CD tool invocations found: None
- Reusable workflows followed: None
- Cross-layer dependencies flagged: App Service config references Key Vault endpoint (Infrastructure ↔ Security); SQL credentials stored in Key Vault (Infrastructure ↔ Security); App Insights connection string app setting (Infrastructure ↔ Observability)
- Newly flagged as SHARED COMPONENT: Azure Key Vault (Infrastructure + Security layers), Application Insights (Infrastructure + Observability layers)
- VERSION CONFLICTS detected: None
- LOW CONFIDENCE items raised this chunk: Application Insights Bicep resource absent from this repository; `mcr.microsoft.com/azure-sql-edge` no version tag (SHARED with Chunk 2); SQL Server firewall rule allows all IPs (0.0.0.1–255.255.255.254) — noted for Agent 2 security assessment

---

## Agent 1 - Chunk 4 of 6 - CI/CD & Deployment Layer

**Carried Forward from Prior Chunks:**
- Technology components: [all prior] + Docker, .NET SDK:8.0, ASP.NET:8.0, Azure App Service B1, Azure SQL 12.0, Azure Key Vault, Azure CLI 2.37.0, go-sqlcmd 0.8.1, azd
- Data stores: sqlserver (local), catalogDatabase + identityDatabase (Azure SQL 12.0), InMemory (test)
- Integrations: Azure Key Vault, Application Insights (LOW)
- LOW CONFIDENCE items: 3

---

**Source: `.github/workflows/dotnetcore.yml` — "eShopOnWeb Build and Test"**
- Trigger: `on: [push, pull_request, workflow_dispatch]` — all branches, all PRs
- Job: `build`, runs-on: `ubuntu-latest`

Step-by-step:
| Step | Type | Detail |
|---|---|---|
| `actions/checkout@v2` | uses | Remote action — code checkout |
| Setup .NET | uses | `actions/setup-dotnet@v1`, dotnet-version: `8.0.x`, include-prerelease: true |
| Build with dotnet | run | `dotnet build ./eShopOnWeb.sln --configuration Release` — tool: `dotnet` |
| Test with dotnet | run | `dotnet test ./eShopOnWeb.sln --configuration Release` — tool: `dotnet` |

No local `uses:` references. No deployment steps. No environment declarations.

**Source: `.github/workflows/richnav.yml` — "eShopOnWeb - Code Index"**
- Trigger: `on: workflow_dispatch` — manual only
- Job: `build`, runs-on: `windows-latest`

Step-by-step:
| Step | Type | Detail |
|---|---|---|
| `actions/checkout@v2` | uses | Remote action |
| Setup .NET Core | uses | `actions/setup-dotnet@v1`, dotnet-version: `8.0.x` |
| Build with dotnet | run | `dotnet build ./Everything.sln --configuration Release /bl` — tools: `dotnet` |
| RichCodeNavIndexer | uses | `microsoft/RichCodeNavIndexer@v0.1`, languages: csharp, environment: internal; repo-token: `${{ github.token }}` |

No local `uses:` references. No deployment steps.

**Source: `.github/dependabot.yml`**
- package-ecosystem: `nuget`, directory: `/`, schedule: `daily`

**Source: `azure.yaml`**
- Azure Developer CLI deployment config — host: `appservice`, service: `web`
- No CI/CD pipeline for azd deployment found in this repository

---

### Chunk Inventory - CI/CD & Deployment Layer
- Technology components found this chunk: GitHub Actions (ubuntu-latest, windows-latest runners), actions/checkout@v2, actions/setup-dotnet@v1, microsoft/RichCodeNavIndexer@v0.1, GitHub Dependabot (NuGet daily), Azure Developer CLI (azd — deployment tool, no pipeline declared)
- Data stores found this chunk: None
- Integrations found this chunk: GitHub Actions (CI), GitHub Dependabot (dependency updates), microsoft/RichCodeNavIndexer@v0.1 (code indexing, internal environment), GitHub token (repo-token)
- Infrastructure resources found: None
- Environments identified: No deployment environment targets declared in either workflow — both are build/test/index only; no deploy-to-Azure CI/CD pipeline found in this repository
- CI/CD tool invocations found:
  - `dotnetcore.yml` / `build` job: `dotnet build`, `dotnet test`
  - `richnav.yml` / `build` job: `dotnet build`
- Reusable workflows followed: None
- Cross-layer dependencies flagged: `actions/setup-dotnet@v1` pins to `8.0.x` matching global.json SDK version (CI ↔ Application layer)
- Newly flagged as SHARED COMPONENT: `dotnet` CLI (Application build + CI/CD layers)
- VERSION CONFLICTS detected: `actions/checkout@v2` and `actions/setup-dotnet@v1` are older action versions (v2/v1 vs current v4/v4); Agent 2 to flag for action version currency assessment
- LOW CONFIDENCE items raised this chunk: No Azure deployment pipeline found — azure.yaml and Bicep IaC are present but no GitHub Actions workflow deploys to Azure App Service; azd CLI commands absent from all workflow files

---

## Agent 1 - Chunk 5 of 6 - Security Layer

**Carried Forward from Prior Chunks:**
- Technology components: [all prior] + GitHub Actions runners + Dependabot
- Data stores: [all prior]
- Integrations: Azure Key Vault, Application Insights (LOW), GitHub Actions, Dependabot, RichCodeNavIndexer
- LOW CONFIDENCE items: 4

---

**Source: `Directory.Packages.props` — security packages**
- `Microsoft.AspNetCore.Authentication.JwtBearer` 8.0.2 (Application layer — SHARED)
- `Microsoft.AspNetCore.Identity.EntityFrameworkCore` 8.0.2
- `Microsoft.AspNetCore.Identity.UI` 8.0.2
- `System.IdentityModel.Tokens.Jwt` 7.3.1
- `System.Security.Claims` 4.3.0
- `Azure.Extensions.AspNetCore.Configuration.Secrets` 1.3.1
- `Azure.Identity` 1.10.4

**Source: `src/PublicApi/PublicApi.csproj`**
- `Microsoft.AspNetCore.Authentication.JwtBearer` (version from Directory.Packages.props: 8.0.2) — JWT bearer authentication in PublicApi
- `UserSecretsId: 5b662463-1efd-4bae-bde4-befe0be3e8ff` — ASP.NET User Secrets configured

**Source: `src/Web/Web.csproj`**
- `Azure.Extensions.AspNetCore.Configuration.Secrets` — Azure Key Vault config provider
- `Azure.Identity` — DefaultAzureCredential / Managed Identity
- `Microsoft.AspNetCore.Authentication.JwtBearer`
- `UserSecretsId: aspnet-Web2-1FA3F72E-E7E3-4360-9E49-1CCCD7FE85F7` — ASP.NET User Secrets configured

**Source: `infra/core/host/appservice.bicep` — network security**
- `minTlsVersion: '1.2'` — TLS 1.2 minimum on App Service
- `ftpsState: 'FtpsOnly'` — FTPS only (FTP disabled)
- `httpsOnly: true` — HTTPS enforced
- `cors.allowedOrigins: union(['https://portal.azure.com', 'https://ms.portal.azure.com'], allowedOrigins)` — Azure Portal plus caller-defined origins

**Source: `infra/core/database/sqlserver/sqlserver.bicep` — database security**
- `minimalTlsVersion: '1.2'` — TLS 1.2 minimum on SQL Server
- `publicNetworkAccess: 'Enabled'` — public network access ON (flagged for Agent 2)
- Firewall: startIpAddress `0.0.0.1`, endIpAddress `255.255.255.254` — all IPs allowed (permissive rule, comment in code acknowledges this)
- SQL Admin credentials: stored in Key Vault via `@secure()` Bicep params
- App user credentials: stored in Key Vault, connection string stored as Key Vault secret `AZURE-SQL-CONNECTION-STRING`

**Source: `infra/core/security/keyvault.bicep` + `keyvault-access.bicep`**
- Key Vault: Standard SKU, tenant-scoped, access policies (not RBAC)
- Access policy: principalId → secrets: `['get', 'list']`
- App Service identity: SystemAssigned managed identity, Key Vault access policy grants secrets get+list

**Source: `docker-compose.yml`**
- SA_PASSWORD: plaintext in compose file (SECRETS MANAGEMENT PATTERN DETECTED — developer credential, not production)
- User secrets volumes mounted in override: `~/.microsoft/usersecrets:/root/.microsoft/usersecrets:ro`

**Source: `src/ApplicationCore/Constants/AuthorizationConstants.cs`**
- Class `AuthorizationConstants` declared — authorization policy names defined (names not visible from source_code.json class declaration alone)

---

### Chunk Inventory - Security Layer
- Technology components found this chunk: ASP.NET Core Identity 8.0.2, JWT Bearer Auth 8.0.2, System.IdentityModel.Tokens.Jwt 7.3.1, Azure Key Vault (Standard SKU), Azure.Identity 1.10.4, Azure.Extensions.AspNetCore.Configuration.Secrets 1.3.1, ASP.NET User Secrets (dev)
- Data stores found this chunk: Azure Key Vault (secrets store — SHARED with Infrastructure)
- Integrations found this chunk: Azure Key Vault (SHARED — Chunk 3)
- Infrastructure resources found: None new
- Environments identified: dev (User Secrets), Docker (docker-compose with plaintext SA_PASSWORD), Azure (Key Vault)
- CI/CD tool invocations found: None
- Reusable workflows followed: None
- Cross-layer dependencies flagged: Key Vault endpoint injected into App Service as env var `AZURE_KEY_VAULT_ENDPOINT` (Security ↔ Infrastructure ↔ Application)
- Newly flagged as SHARED COMPONENT: JWT Bearer / Identity (Application + Security), Azure Key Vault (Infrastructure + Security)
- VERSION CONFLICTS detected: None
- LOW CONFIDENCE items raised this chunk: AuthorizationConstants class found but policy names not visible from Layer 1 extraction alone — Agent 2 to inspect; SA_PASSWORD in docker-compose is developer-only pattern

---

## Agent 1 - Chunk 6 of 6 - Observability Layer

**Carried Forward from Prior Chunks:**
- Technology components: [full cumulative list — all prior chunks]
- Data stores: [all prior]
- Integrations: Azure Key Vault, Application Insights (LOW — no Bicep module), GitHub Actions, Dependabot, RichCodeNavIndexer
- LOW CONFIDENCE items: 5

---

**Source: `infra/core/host/appservice.bicep` — logging config**
- Application logs: fileSystem, level `Verbose`
- Detailed error messages: `enabled: true`
- Failed requests tracing: `enabled: true`
- HTTP logs: fileSystem, enabled, retentionInDays: 1, retentionInMb: 35
- Health check path: param `healthCheckPath` (empty string default — not configured in this repository)
- `APPLICATIONINSIGHTS_CONNECTION_STRING` env var injected when `applicationInsightsName` is non-empty

**Source: `src/Web/appsettings.json` + `src/PublicApi/appsettings.json` — log levels**
- Default log level: `Warning`
- Microsoft namespaces: `Warning`
- System: `Warning`

**Source: `src/Web/appsettings.Development.json`**
- Default log level: `Debug`
- System: `Information`
- Microsoft: `Information`

**Source: `src/PublicApi/appsettings.Development.json`**
- Default log level: `Information`
- Microsoft: `Warning`
- Microsoft.Hosting.Lifetime: `Information`

**Source: `src/ApplicationCore/Interfaces/IAppLogger.cs`**
- Interface `IAppLogger` declared — custom logging abstraction (Application layer)

**Source: `infra/main.bicep`**
- Application Insights resource referenced but no `Microsoft.Insights/components` resource declared in this bicep file — `applicationInsightsName` param passed to app service but no module creates the App Insights instance in this repo (LOW — may exist in a separate deployment or not yet implemented)

No monitoring config files found (no prometheus.yml, grafana.json, alertmanager.yml, otel-collector.yml, or similar).

**LAYER NOTE:** No dedicated observability config files detected. Observability is declared only via App Service log settings in Bicep and appsettings log level configuration. Application Insights referenced but no IaC resource provisioning it in this repository.

---

### Chunk Inventory - Observability Layer
- Technology components found this chunk: ASP.NET Core built-in logging (ILogger/IAppLogger), Application Insights (LOW — referenced by env var key only, no IaC resource found in repo)
- Data stores found this chunk: None
- Integrations found this chunk: Application Insights (LOW — no Bicep module; SHARED with Infrastructure layer via env var injection)
- Infrastructure resources found: None
- Environments identified: Development (Debug logs), Production (Warning logs)
- CI/CD tool invocations found: None
- Reusable workflows followed: None
- Cross-layer dependencies flagged: `APPLICATIONINSIGHTS_CONNECTION_STRING` links Infrastructure (App Service config) to Observability
- Newly flagged as SHARED COMPONENT: Application Insights (Infrastructure + Observability)
- VERSION CONFLICTS detected: None
- LOW CONFIDENCE items raised this chunk: Application Insights resource not provisioned in this repository's Bicep — `applicationInsightsName` is an empty-default parameter; no Application Insights SDK NuGet package (e.g. `Microsoft.ApplicationInsights.AspNetCore`) found in any .csproj or Directory.Packages.props — Agent 2 to investigate whether App Insights is actually instrumented at the SDK level or only configuration-referenced

---

---

## Agent 1 - Project Scan Summary

- Language(s): C# (.NET 8.0, SDK 8.0.x)
- Framework(s): ASP.NET Core 8.0 (MVC + Blazor WebAssembly + Minimal/Endpoint API), Entity Framework Core 8.0.2
- Architecture style: Modular Monolith — HIGH (single solution, Clean Architecture layering: ApplicationCore → Infrastructure → Web/PublicApi; single SQL Server, two deployable containers)
- Deployment target: Azure App Service (Linux, dotnetcore 8.0, B1 SKU) via Azure Developer CLI (azd); Docker Compose for local development
- Total files scanned: ~47
- Technology layers found: 6 — Application, Data, Infrastructure, CI/CD, Security, Observability
- Chunks processed: 6
- External integrations found: 5 (Azure App Service, Azure SQL, Azure Key Vault, Application Insights [LOW], GitHub Actions + Dependabot + RichCodeNavIndexer)
- Data stores identified: 4 (CatalogDb/SQL Server, IdentityDb/SQL Server, Azure SQL x2 cloud-side, InMemory EF test store)
- Services / components found: 3 (eshopwebmvc, eshoppublicapi, sqlserver) + BlazorAdmin embedded in Web host
- CI/CD pipeline files read: 2 (0 reusable workflow files followed — none referenced locally)
- CI/CD tool invocations found: `dotnet build`, `dotnet test` (dotnetcore.yml); `dotnet build` (richnav.yml)

---

## OUTPUT 1 - Technology Stack Inventory

| Component Name | Version | Category | Layer | Package Manager / Source | Source File | Confidence |
|---|---|---|---|---|---|---|
| .NET Runtime | 8.0 | Runtime | Application | global.json / Bicep | global.json, infra/main.bicep | HIGH |
| .NET SDK | 8.0.x (rollForward: latestFeature) | SDK | Build | global.json | global.json | HIGH |
| ASP.NET Core MVC | 8.0.2 | Web Framework | Application | NuGet | Directory.Packages.props | HIGH |
| Blazor WebAssembly | 8.0.2 | Frontend Framework | Application | NuGet | Directory.Packages.props | HIGH |
| ASP.NET Core Components.Authorization | 8.0.2 | Auth UI Library | Application | NuGet | Directory.Packages.props | HIGH |
| ASP.NET Core Components.WebAssembly.Server | 8.0.2 | Blazor Server Host | Application | NuGet | Directory.Packages.props | HIGH |
| Entity Framework Core SqlServer | 8.0.2 | ORM / DB Client | Data | NuGet | Directory.Packages.props | HIGH |
| Entity Framework Core InMemory | 8.0.2 | Test Data Store | Data | NuGet | Directory.Packages.props | HIGH |
| Entity Framework Core Tools | 8.0.2 | DB Migration Tool | Build | NuGet | Directory.Packages.props | HIGH |
| MediatR | 12.0.1 | Mediator / CQRS | Application | NuGet | Directory.Packages.props | HIGH |
| AutoMapper.Extensions.Microsoft.DependencyInjection | 12.0.1 | Object Mapping | Application | NuGet | Directory.Packages.props | HIGH |
| FluentValidation | 11.9.0 | Validation Library | Application | NuGet | Directory.Packages.props | HIGH |
| Ardalis.Specification | 7.0.0 | Repository Pattern | Application | NuGet | Directory.Packages.props | HIGH |
| Ardalis.Specification.EntityFrameworkCore | 7.0.0 | Repository/EF Adapter | Data | NuGet | Directory.Packages.props | HIGH |
| Ardalis.ApiEndpoints | 4.1.0 | API Endpoint Pattern | Application | NuGet | Directory.Packages.props | HIGH |
| Ardalis.GuardClauses | 4.0.1 | Guard/Validation Library | Application | NuGet | Directory.Packages.props | HIGH |
| Ardalis.Result | 7.0.0 | Result Pattern | Application | NuGet | Directory.Packages.props | HIGH |
| Ardalis.ListStartupServices | 1.1.4 | Dev Diagnostics | Application | NuGet | Directory.Packages.props | HIGH |
| MinimalApi.Endpoint | 1.3.0 | Minimal API Endpoint | Application | NuGet | Directory.Packages.props | HIGH |
| Swashbuckle.AspNetCore | 6.5.0 | OpenAPI / Swagger | Application | NuGet | Directory.Packages.props | HIGH |
| Swashbuckle.AspNetCore.SwaggerUI | 6.5.0 | Swagger UI | Application | NuGet | Directory.Packages.props | HIGH |
| Swashbuckle.AspNetCore.Annotations | 6.5.0 | Swagger Annotations | Application | NuGet | Directory.Packages.props | HIGH |
| Microsoft.AspNetCore.Authentication.JwtBearer | 8.0.2 | JWT Authentication | Security | NuGet | Directory.Packages.props | HIGH |
| Microsoft.AspNetCore.Identity.EntityFrameworkCore | 8.0.2 | Identity / Auth Store | Security | NuGet | Directory.Packages.props | HIGH |
| Microsoft.AspNetCore.Identity.UI | 8.0.2 | Identity Razor Pages | Security | NuGet | Directory.Packages.props | HIGH |
| Microsoft.AspNetCore.Diagnostics.EntityFrameworkCore | 8.0.2 | EF Dev Error Pages | Application | NuGet | Directory.Packages.props | HIGH |
| Microsoft.AspNetCore.Mvc | 2.2.0 | MVC Core | Application | NuGet | Directory.Packages.props | LOW — VERSION CONFLICT: 2.2.0 declared while all other ASP.NET Core packages at 8.0.2; may be stale/unused declaration |
| Microsoft.Extensions.Identity.Core | 8.0.2 | Identity Core | Security | NuGet | Directory.Packages.props | HIGH |
| Microsoft.Extensions.Logging.Configuration | 8.0.0 | Logging Config | Observability | NuGet | Directory.Packages.props | HIGH |
| System.IdentityModel.Tokens.Jwt | 7.3.1 | JWT Token Library | Security | NuGet | Directory.Packages.props | HIGH |
| System.Security.Claims | 4.3.0 | Claims Library | Security | NuGet | Directory.Packages.props | HIGH |
| System.Text.Json | 8.0.3 | JSON Serialization | Application | NuGet | Directory.Packages.props | HIGH |
| System.Net.Http.Json | 8.0.0 | HTTP JSON Client | Application | NuGet | Directory.Packages.props | HIGH |
| Azure.Identity | 1.10.4 | Azure Auth / Managed Identity | Security | NuGet | Directory.Packages.props | HIGH |
| Azure.Extensions.AspNetCore.Configuration.Secrets | 1.3.1 | Azure Key Vault Config Provider | Security | NuGet | Directory.Packages.props | HIGH |
| Blazored.LocalStorage | 4.5.0 | Browser Local Storage | Application | NuGet | Directory.Packages.props | HIGH |
| BlazorInputFile | 0.2.0 | Blazor File Input | Application | NuGet | Directory.Packages.props | HIGH |
| BuildBundlerMinifier | 3.2.449 | CSS/JS Bundler | Build | NuGet | Directory.Packages.props | HIGH |
| Microsoft.VisualStudio.Web.CodeGeneration.Design | 8.0.0 | Scaffolding Tool | Build | NuGet | Directory.Packages.props | HIGH |
| Microsoft.Web.LibraryManager.Build | 2.1.175 | Frontend Library Manager | Build | NuGet | Directory.Packages.props | HIGH |
| Microsoft.VisualStudio.Azure.Containers.Tools.Targets | 1.19.6 | VS Container Tooling | Build | NuGet | Directory.Packages.props | HIGH |
| NSubstitute | 5.1.0 | Test Mock Library | Build | NuGet | Directory.Packages.props | HIGH |
| NSubstitute.Analyzers.CSharp | 1.0.17 | Test Mock Analyzer | Build | NuGet | Directory.Packages.props | HIGH |
| Microsoft.AspNetCore.Mvc.Testing | 8.0.2 | Integration Test Host | Build | NuGet | Directory.Packages.props | HIGH |
| Microsoft.NET.Test.Sdk | 17.9.0 | Test SDK | Build | NuGet | Directory.Packages.props | HIGH |
| xunit | 2.7.0 | Test Framework | Build | NuGet | Directory.Packages.props | HIGH |
| xunit.runner.visualstudio | 2.5.6 | Test Runner | Build | NuGet | Directory.Packages.props | HIGH |
| xunit.runner.console | 2.7.0 | Test Runner | Build | NuGet | Directory.Packages.props | HIGH |
| MSTest.TestAdapter | 3.2.2 | Test Adapter | Build | NuGet | Directory.Packages.props | HIGH |
| MSTest.TestFramework | 3.2.2 | Test Framework | Build | NuGet | Directory.Packages.props | HIGH |
| coverlet.collector | 6.0.2 | Code Coverage | Build | NuGet | Directory.Packages.props | HIGH |
| dotnet-ef | 8.0.0 | EF Core CLI Tool | Build | dotnet tool | src/Web/.config/dotnet-tools.json | HIGH |
| dotnet-xunit | 2.3.1 | Legacy Test Runner | Build | DotNetCliToolReference | tests/FunctionalTests/FunctionalTests.csproj | LOW — legacy DotNetCliToolReference; deprecated mechanism |
| jQuery | 3.6.3 | Frontend JS Library | Application | cdnjs / libman | src/Web/libman.json | HIGH |
| Bootstrap | 3.4.1 | CSS Framework | Application | cdnjs / libman | src/Web/libman.json | HIGH |
| jquery-validate | 1.19.5 | Form Validation | Application | cdnjs / libman | src/Web/libman.json | HIGH |
| jquery-validation-unobtrusive | 4.0.0 | Unobtrusive Validation | Application | cdnjs / libman | src/Web/libman.json | HIGH |
| toastr.js | 2.1.4 | Toast Notifications | Application | cdnjs / libman | src/Web/libman.json | HIGH |
| SignalR Client (aspnet-signalr) | 1.0.27 | Real-time Client | Application | cdnjs / libman | src/Web/libman.json | HIGH |
| mcr.microsoft.com/dotnet/sdk | 8.0 | Container Build Image | Infrastructure | Docker Hub (MCR) | src/Web/Dockerfile, src/PublicApi/Dockerfile | HIGH |
| mcr.microsoft.com/dotnet/aspnet | 8.0 | Container Runtime Image | Infrastructure | Docker Hub (MCR) | src/Web/Dockerfile, src/PublicApi/Dockerfile | HIGH |
| mcr.microsoft.com/azure-sql-edge | UNKNOWN (no tag) | Container DB Image | Data | Docker Hub (MCR) | docker-compose.yml | LOW — no version tag declared |
| Azure App Service | dotnetcore 8.0 / Linux / B1 | Cloud PaaS Host | Infrastructure | Bicep / azd | infra/main.bicep, infra/core/host/appservice.bicep | HIGH |
| Azure App Service Plan | B1 | Cloud Compute Plan | Infrastructure | Bicep | infra/core/host/appserviceplan.bicep | HIGH |
| Azure SQL Server | 12.0 (API 2022-05-01-preview) | Relational DB PaaS | Data | Bicep | infra/core/database/sqlserver/sqlserver.bicep | HIGH |
| Azure Key Vault | Standard SKU (API 2022-07-01) | Secrets Management | Security | Bicep | infra/core/security/keyvault.bicep | HIGH |
| Azure Developer CLI (azd) | (version unspecified) | Deployment Orchestration | CI-CD | azure.yaml | azure.yaml | HIGH |
| Azure CLI | 2.37.0 | DB Provisioning Script | Infrastructure | Bicep deploymentScript | infra/core/database/sqlserver/sqlserver.bicep | HIGH |
| go-sqlcmd | 0.8.1 | SQL DB User Setup | Infrastructure | Bicep script download | infra/core/database/sqlserver/sqlserver.bicep | HIGH |
| Application Insights | UNKNOWN | Observability | Observability | Bicep env var ref | infra/core/host/appservice.bicep | LOW — no SDK package; no Bicep provisioning in this repo; referenced as existing resource via env var injection only |
| actions/checkout | v2 | CI/CD Action | CI-CD | GitHub Actions | .github/workflows/dotnetcore.yml, richnav.yml | HIGH |
| actions/setup-dotnet | v1 | CI/CD Action | CI-CD | GitHub Actions | .github/workflows/dotnetcore.yml, richnav.yml | HIGH |
| microsoft/RichCodeNavIndexer | v0.1 | Code Index Action | CI-CD | GitHub Actions | .github/workflows/richnav.yml | HIGH |
| GitHub Dependabot | v2 | Dependency Automation | CI-CD | GitHub | .github/dependabot.yml | HIGH |

---

## OUTPUT 2 - Component & Service Map

| Service / Component Name | Type | Exposed Port(s) | Communication Protocol(s) | Primary Technology | Source File | Notes |
|---|---|---|---|---|---|---|
| eshopwebmvc | Frontend App + API Host | 5106 (Docker local, mapped 8080 internal) | HTTP (Docker local) / HTTPS (Azure) | ASP.NET Core 8.0 MVC + Blazor WebAssembly Server | docker-compose.yml, src/Web/Dockerfile | Hosts BlazorAdmin WebAssembly; depends_on sqlserver; env ASPNETCORE_ENVIRONMENT=Docker |
| eshoppublicapi | API Service | 5200 (Docker local, mapped 8080 internal); 80, 443 (Dockerfile EXPOSE) | HTTP/HTTPS | ASP.NET Core 8.0 Minimal/Endpoint API | docker-compose.yml, src/PublicApi/Dockerfile | REST API with Swagger UI; depends_on sqlserver; JWT Bearer auth |
| sqlserver | Database | 1433 | TCP | Azure SQL Edge (Docker local) | docker-compose.yml | Local dev only; Azure SQL used in cloud deployment; depends_on by both app services |
| BlazorAdmin | Frontend App (embedded) | N/A (served from eshopwebmvc) | HTTP/HTTPS (via host) | Blazor WebAssembly 8.0 | src/BlazorAdmin/BlazorAdmin.csproj | Embedded in Web host; not a separate deployable |
| Azure App Service (web) | Cloud PaaS Host | 443 (HTTPS only) | HTTPS | dotnetcore 8.0 / Linux / B1 | infra/main.bicep | Cloud deployment of eshopwebmvc; SystemAssigned managed identity; Key Vault integration |
| Azure SQL (catalog) | Relational Database | 1433 (SQL port) | TCP/TLS 1.2 | Azure SQL Server 12.0 | infra/main.bicep | Database: catalogDatabase; connection string in Key Vault |
| Azure SQL (identity) | Relational Database | 1433 (SQL port) | TCP/TLS 1.2 | Azure SQL Server 12.0 | infra/main.bicep | Database: identityDatabase; connection string in Key Vault |
| Azure Key Vault | Secrets Store | N/A | HTTPS / Azure SDK | Azure Key Vault Standard | infra/core/security/keyvault.bicep | Stores SQL passwords and connection strings; accessed via managed identity |

---

## OUTPUT 3 - Data Store Registry

| Store Name | Category | Engine / Technology | Version | Declared Database / Collection Name | Connected Services (if detectable) | Source File | Confidence |
|---|---|---|---|---|---|---|---|
| sqlserver (Docker local) | Relational Database | Azure SQL Edge | UNKNOWN — no image tag | Microsoft.eShopOnWeb.CatalogDb; Microsoft.eShopOnWeb.Identity | eshopwebmvc, eshoppublicapi | docker-compose.yml | LOW — no version tag; Agent 2 to confirm Azure SQL Edge version in use |
| catalogDatabase (Azure) | Relational Database | Azure SQL Server | 12.0 (API 2022-05-01-preview) | catalogDatabase (param default) | web (App Service) | infra/main.bicep, infra/core/database/sqlserver/sqlserver.bicep | HIGH |
| identityDatabase (Azure) | Relational Database | Azure SQL Server | 12.0 (API 2022-05-01-preview) | identityDatabase (param default) | web (App Service) | infra/main.bicep, infra/core/database/sqlserver/sqlserver.bicep | HIGH |
| InMemory EF Store (test) | In-Memory Store | Microsoft.EntityFrameworkCore.InMemory | 8.0.2 | UNKNOWN — substitutes CatalogDb + Identity schema | PublicApiIntegrationTests (UseOnlyInMemoryDatabase=true) | tests/PublicApiIntegrationTests/appsettings.test.json, Directory.Packages.props | HIGH |
| Azure Key Vault | Secrets Store | Azure Key Vault | Standard SKU | N/A | web (App Service via managed identity), catalogDb deployment script, identityDb deployment script | infra/core/security/keyvault.bicep | HIGH |

**EF Core Entities registered in CatalogContext (src/Infrastructure/Data/CatalogContext.cs):**
CatalogBrand, CatalogType, CatalogItem, Basket, BasketItem, OrderItem, Order

---

## OUTPUT 4 - Infrastructure & Deployment Blueprint

### Compute & Container Resources

| Resource Name | Resource Type | Platform / Provider | Image / Runtime Version | Environments Declared | Key Configuration (non-secret) | Source File | Confidence |
|---|---|---|---|---|---|---|---|
| eshopwebmvc | Container | Docker Compose | mcr.microsoft.com/dotnet/aspnet:8.0 (runtime) | Docker (local) | Port 5106:8080; ASPNETCORE_ENVIRONMENT=Docker; ASPNETCORE_URLS=http://+:8080; volumes: usersecrets, https certs | docker-compose.yml, src/Web/Dockerfile | HIGH |
| eshoppublicapi | Container | Docker Compose | mcr.microsoft.com/dotnet/aspnet:8.0 (runtime) | Docker (local) | Port 5200:8080; ASPNETCORE_ENVIRONMENT=Docker; ASPNETCORE_URLS=http://+:8080; volumes: usersecrets, https certs | docker-compose.yml, src/PublicApi/Dockerfile | HIGH |
| sqlserver | Container | Docker Compose | mcr.microsoft.com/azure-sql-edge (no tag) | Docker (local) | Port 1433:1433; ACCEPT_EULA=Y | docker-compose.yml | LOW — no version tag |
| web (App Service) | Azure App Service | Azure / Bicep | dotnetcore\|8.0, Linux | Azure (env name parameterised) | SKU B1; alwaysOn: true; httpsOnly: true; minTlsVersion: 1.2; ftpsState: FtpsOnly; managedIdentity: SystemAssigned; AZURE_SQL_CATALOG_CONNECTION_STRING_KEY; AZURE_SQL_IDENTITY_CONNECTION_STRING_KEY; AZURE_KEY_VAULT_ENDPOINT | infra/main.bicep, infra/core/host/appservice.bicep | HIGH |
| appServicePlan | Azure App Service Plan | Azure / Bicep | B1, Linux (reserved: true) | Azure | plan-${resourceToken} | infra/main.bicep, infra/core/host/appserviceplan.bicep | HIGH |
| sql-catalog | Azure SQL Server | Azure / Bicep | SQL version 12.0 | Azure | minimalTlsVersion: 1.2; publicNetworkAccess: Enabled; firewall 0.0.0.1–255.255.255.254; deployment script: Azure CLI 2.37.0 + go-sqlcmd 0.8.1 | infra/main.bicep, infra/core/database/sqlserver/sqlserver.bicep | HIGH |
| sql-identity | Azure SQL Server | Azure / Bicep | SQL version 12.0 | Azure | Same as sql-catalog | infra/main.bicep, infra/core/database/sqlserver/sqlserver.bicep | HIGH |
| keyvault | Azure Key Vault | Azure / Bicep | Standard SKU | Azure | kv-${resourceToken}; access policy: secrets get+list | infra/main.bicep, infra/core/security/keyvault.bicep | HIGH |

### Environments Identified

| Environment Name | Trigger / Target | Source File |
|---|---|---|
| Development | Local run (ASPNETCORE_ENVIRONMENT=Development, VS Code launch.json) | .vscode/launch.json, appsettings.Development.json |
| Docker | Docker Compose local run (ASPNETCORE_ENVIRONMENT=Docker) | docker-compose.override.yml, appsettings.Docker.json |
| Azure (cloud) | Azure Developer CLI (azd) deployment, parameterised by AZURE_ENV_NAME | azure.yaml, infra/main.bicep, infra/main.parameters.json |
| Release | CI trigger (push/PR to any branch) — build and test only, no deploy | .github/workflows/dotnetcore.yml |

### CI/CD Pipeline Inventory

| Pipeline File | Job / Stage Name | Tool Invocations (first word per run: command) | Actions Used (uses: references) | Runs On Condition | Source |
|---|---|---|---|---|---|
| .github/workflows/dotnetcore.yml | build | `dotnet build`, `dotnet test` | actions/checkout@v2, actions/setup-dotnet@v1 (dotnet-version: 8.0.x) | push, pull_request, workflow_dispatch (all branches/PRs) | .github/workflows/dotnetcore.yml |
| .github/workflows/richnav.yml | build | `dotnet build` | actions/checkout@v2, actions/setup-dotnet@v1 (dotnet-version: 8.0.x), microsoft/RichCodeNavIndexer@v0.1 | workflow_dispatch (manual only) | .github/workflows/richnav.yml |

### Network Topology (declared configuration only)

- HTTPS enforced: `httpsOnly: true` on Azure App Service (infra/core/host/appservice.bicep)
- TLS 1.2 minimum: App Service `minTlsVersion: '1.2'`; SQL Server `minimalTlsVersion: '1.2'`
- FTPS: `ftpsState: 'FtpsOnly'` on App Service
- CORS: Declared in App Service Bicep — `union(['https://portal.azure.com', 'https://ms.portal.azure.com'], allowedOrigins)` — runtime allowedOrigins value not declared in this repo
- SQL firewall: All IPs allowed (0.0.0.1–255.255.255.254) — publicly accessible, no VNet declared
- No VNet / subnet / NSG / private endpoint declarations found in this repository
- No reverse proxy / load balancer / CDN / service mesh declared

---

## OUTPUT 5 - Integration & Dependency Graph

### External Integrations

| Integration Name | Category | Protocol / Interface | Direction | Config Key / Env Var | Source File | Confidence |
|---|---|---|---|---|---|---|
| Azure App Service | Cloud PaaS | Azure SDK / azd CLI | Outbound (deploy) | AZURE_ENV_NAME, AZURE_LOCATION | azure.yaml, infra/main.bicep | HIGH |
| Azure SQL Server | Cloud Database | TCP / TDS / TLS 1.2 | Outbound | ConnectionStrings.CatalogConnection, ConnectionStrings.IdentityConnection, AZURE_SQL_CATALOG_CONNECTION_STRING_KEY, AZURE_SQL_IDENTITY_CONNECTION_STRING_KEY | appsettings.json, infra/main.bicep | HIGH |
| Azure Key Vault | Secrets Management | HTTPS / Azure SDK | Outbound | AZURE_KEY_VAULT_ENDPOINT, AZURE_KEY_VAULT_NAME | infra/main.bicep, appsettings (runtime injection) | HIGH |
| Application Insights | Observability / APM | HTTPS / SDK | Outbound | APPLICATIONINSIGHTS_CONNECTION_STRING | infra/core/host/appservice.bicep | LOW — env var key declared in App Service config; no App Insights NuGet SDK package found; no Bicep provisioning resource in this repo |
| actions/checkout | CI/CD Action | GitHub Actions | CI-CD Pipeline | N/A | .github/workflows/dotnetcore.yml, .github/workflows/richnav.yml | HIGH |
| actions/setup-dotnet | CI/CD Action | GitHub Actions | CI-CD Pipeline | N/A (dotnet-version: 8.0.x) | .github/workflows/dotnetcore.yml, .github/workflows/richnav.yml | HIGH |
| microsoft/RichCodeNavIndexer | Code Index Action | GitHub Actions | CI-CD Pipeline | GITHUB_TOKEN | .github/workflows/richnav.yml | HIGH |
| GitHub Dependabot | Dependency Automation | GitHub | Inbound (PRs) | N/A | .github/dependabot.yml | HIGH |
| cdnjs (via libman) | Frontend CDN | HTTPS / libman | Outbound (build time) | N/A | src/Web/libman.json | HIGH |

### Internal Service Dependencies (multi-service)

| Caller Service | Target Service | Protocol | Dependency Type | Config Key / Env Var | Source File |
|---|---|---|---|---|---|
| eshopwebmvc | sqlserver | TCP 1433 | Synchronous | ConnectionStrings.CatalogConnection, ConnectionStrings.IdentityConnection | docker-compose.yml, appsettings.Docker.json |
| eshoppublicapi | sqlserver | TCP 1433 | Synchronous | ConnectionStrings.CatalogConnection, ConnectionStrings.IdentityConnection | docker-compose.yml, appsettings.Docker.json |
| eshopwebmvc | eshoppublicapi | HTTP | Synchronous (client) | baseUrls.apiBase (http://localhost:5200/api/) | src/Web/appsettings.Docker.json |
| eshoppublicapi | eshopwebmvc | HTTP | Synchronous (redirect reference) | baseUrls.webBase (http://host.docker.internal:5106/) | src/PublicApi/appsettings.Docker.json |
| web (App Service) | Azure Key Vault | HTTPS | Synchronous (config read) | AZURE_KEY_VAULT_ENDPOINT | infra/main.bicep |
| web (App Service) | Azure SQL (catalog) | TCP/TLS | Synchronous | AZURE_SQL_CATALOG_CONNECTION_STRING_KEY | infra/main.bicep |
| web (App Service) | Azure SQL (identity) | TCP/TLS | Synchronous | AZURE_SQL_IDENTITY_CONNECTION_STRING_KEY | infra/main.bicep |

### Build & Developer Toolchain

| Tool | Version | Purpose | Source File |
|---|---|---|---|
| dotnet CLI | 8.0.x | Build, Test, Publish, EF migrations | global.json, .vscode/tasks.json |
| dotnet-ef | 8.0.0 | EF Core DB migrations | src/Web/.config/dotnet-tools.json |
| dotnet-xunit | 2.3.1 | Legacy test runner (deprecated) | tests/FunctionalTests/FunctionalTests.csproj |
| BuildBundlerMinifier | 3.2.449 | CSS/JS bundle + minification | Directory.Packages.props |
| Microsoft.Web.LibraryManager.Build | 2.1.175 | Frontend library restore (libman) | Directory.Packages.props |
| Microsoft.VisualStudio.Web.CodeGeneration.Design | 8.0.0 | Scaffolding | Directory.Packages.props |
| coverlet.collector | 6.0.2 | Code coverage collection | Directory.Packages.props |
| Azure Developer CLI (azd) | unspecified | Cloud deployment orchestration | azure.yaml |
| Azure CLI | 2.37.0 | DB user provisioning script | infra/core/database/sqlserver/sqlserver.bicep |
| go-sqlcmd | 0.8.1 | SQL command execution in provisioning | infra/core/database/sqlserver/sqlserver.bicep |

---

## OUTPUT 6 - Security & Configuration Snapshot

### Authentication & Authorisation Mechanisms

| Mechanism Name | Type | Provider / Library | Scope | Config Key / Annotation | Source File | Confidence |
|---|---|---|---|---|---|---|
| ASP.NET Core Identity | Authentication + Authorisation | Microsoft.AspNetCore.Identity.EntityFrameworkCore 8.0.2 + UI | Web app (eshopwebmvc) | ConnectionStrings.IdentityConnection | Directory.Packages.props, src/Web/Web.csproj | HIGH |
| JWT Bearer Authentication | Authentication | Microsoft.AspNetCore.Authentication.JwtBearer 8.0.2 | PublicApi + Web | (JWT secret key — User Secrets / Key Vault) | Directory.Packages.props, src/PublicApi/PublicApi.csproj | HIGH |
| JWT Token Generation | Authentication | System.IdentityModel.Tokens.Jwt 7.3.1 | Infrastructure layer | (key in User Secrets) | Directory.Packages.props, src/Infrastructure/Infrastructure.csproj | HIGH |
| ASP.NET Claims | Authorisation | System.Security.Claims 4.3.0 | Application | AuthorizationConstants (policy names not visible in Layer 1 extraction) | Directory.Packages.props, src/ApplicationCore/Constants/AuthorizationConstants.cs | HIGH — library confirmed; policy names LOW — not extractable from Layer 1 |
| Azure Managed Identity (SystemAssigned) | Authentication | Azure.Identity 1.10.4 | App Service → Key Vault | AZURE_KEY_VAULT_ENDPOINT | infra/core/host/appservice.bicep, src/Web/Web.csproj | HIGH |
| Azure Key Vault Config Provider | Authentication | Azure.Extensions.AspNetCore.Configuration.Secrets 1.3.1 | Web app (Key Vault secret reads at startup) | AZURE_KEY_VAULT_ENDPOINT | src/Web/Web.csproj | HIGH |
| Blazor WebAssembly Authentication | Authentication | Microsoft.AspNetCore.Components.WebAssembly.Authentication 8.0.2 | BlazorAdmin client | (not declared in config files) | Directory.Packages.props, src/BlazorAdmin/BlazorAdmin.csproj | HIGH |
| User Secrets (dev) | Secrets Management | ASP.NET User Secrets | Development only | UserSecretsId (Web, PublicApi) | src/Web/Web.csproj, src/PublicApi/PublicApi.csproj | HIGH |

### Secrets & Configuration Management

| Approach | Tool / Service | Scope | Config Key / Reference | Source File | Confidence |
|---|---|---|---|---|---|
| Azure Key Vault | Azure Key Vault Standard | Application (Azure env) | AZURE_KEY_VAULT_ENDPOINT, AZURE_KEY_VAULT_NAME, sqlAdminPassword, appUserPassword, AZURE-SQL-CATALOG-CONNECTION-STRING, AZURE-SQL-IDENTITY-CONNECTION-STRING | infra/main.bicep, infra/core/security/keyvault.bicep | HIGH |
| ASP.NET User Secrets | User Secrets (dev local) | Development only | UserSecretsId in Web.csproj + PublicApi.csproj | src/Web/Web.csproj, src/PublicApi/PublicApi.csproj | HIGH |
| Docker Compose Environment Variables | docker-compose.yml (plaintext) | Docker local dev only | SA_PASSWORD (SQL SA password inline) | docker-compose.yml | HIGH — SECRETS MANAGEMENT PATTERN DETECTED: SA_PASSWORD stored plaintext in compose file (dev use only per context) |
| Docker User Secrets Volume Mount | Volume mount (read-only) | Docker local dev | ~/.microsoft/usersecrets | docker-compose.override.yml | HIGH |
| Azure Deployment Parameters | Bicep @secure() params + azd secretOrRandomPassword | Azure deployment | sqlAdminPassword, appUserPassword (AZURE_KEY_VAULT_NAME sourced) | infra/main.parameters.json | HIGH |

### Network Security Declarations

| Declaration | Type | Value (non-secret only) | Source File | Confidence |
|---|---|---|---|---|
| HTTPS enforced | HTTPS-only | httpsOnly: true | infra/core/host/appservice.bicep | HIGH |
| TLS minimum version (App Service) | TLS | 1.2 | infra/core/host/appservice.bicep | HIGH |
| TLS minimum version (SQL Server) | TLS | 1.2 | infra/core/database/sqlserver/sqlserver.bicep | HIGH |
| FTPS policy | FTPS | FtpsOnly (plain FTP disabled) | infra/core/host/appservice.bicep | HIGH |
| CORS origins (App Service) | CORS | https://portal.azure.com, https://ms.portal.azure.com (+ runtime-injected allowedOrigins) | infra/core/host/appservice.bicep | HIGH |
| SQL firewall rule | Firewall | All IPs allowed: 0.0.0.1–255.255.255.254 (publicly accessible) | infra/core/database/sqlserver/sqlserver.bicep | HIGH |
| SQL public network access | Network Policy | Enabled | infra/core/database/sqlserver/sqlserver.bicep | HIGH |

### Compliance & Audit Flags

| Item | Type | Detail | Source File |
|---|---|---|---|
| Application log retention | Audit Logging | HTTP logs: 1 day, 35MB; application logs verbose; detailed errors + failed request tracing enabled | infra/core/host/appservice.bicep |
| AuthorizationConstants class | RBAC | Authorization policy names defined; names not visible from Layer 1 extraction | src/ApplicationCore/Constants/AuthorizationConstants.cs |
| SA_PASSWORD in docker-compose | Data Security | Plaintext SQL SA password in source-controlled compose file (developer credential) | docker-compose.yml |
| Azure SQL firewall wide-open | Data Security | Firewall allows all IPs (0.0.0.1–255.255.255.254); comment in Bicep acknowledges this is intentional for developer access | infra/core/database/sqlserver/sqlserver.bicep |

---

## Validation Queue

| # | Item | Chunk | Reason |
|---|---|---|---|
| 1 | `dotnet-xunit 2.3.1` in FunctionalTests.csproj | Chunk 1 | Legacy DotNetCliToolReference mechanism deprecated in .NET SDK; may not function; Agent 2 to assess whether functional tests actually run |
| 2 | `Microsoft.AspNetCore.Mvc 2.2.0` in Directory.Packages.props | Chunk 1 | VERSION CONFLICT: 2.2.0 vs all other ASP.NET Core 8.0.2 packages; likely stale/unused declaration; Agent 2 to confirm which project references it |
| 3 | `mcr.microsoft.com/azure-sql-edge` no version tag | Chunks 2+3 | No image tag pinned in docker-compose.yml; exact version unknown; may float to latest on pull |
| 4 | EF DbContext names not extracted | Chunk 2 | `db_contexts` array is empty in database.json; CatalogContext confirmed by ef_entities but IdentityDbContext not listed; Agent 2 to read Infrastructure source for full context list |
| 5 | Application Insights — no SDK, no Bicep resource | Chunks 3+6 | `APPLICATIONINSIGHTS_CONNECTION_STRING` env var injected in App Service Bicep but: (a) no `Microsoft.ApplicationInsights.AspNetCore` NuGet package found; (b) no `Microsoft.Insights/components` Bicep resource in this repo; Agent 2 to determine if App Insights is actually instrumented |
| 6 | No CI/CD deployment pipeline | Chunk 4 | `azure.yaml` + full Bicep IaC present but no GitHub Actions workflow runs `azd deploy` or equivalent; deployment to Azure not automated in source-controlled pipelines |
| 7 | `actions/checkout@v2` + `actions/setup-dotnet@v1` | Chunk 4 | Older action versions (current: v4 / v4); Agent 2 to flag for action currency assessment |
| 8 | SQL Server firewall: all IPs allowed | Chunks 3+5 | `publicNetworkAccess: Enabled`, firewall 0.0.0.1–255.255.255.254; comment in Bicep acknowledges this is for developer access; Agent 2 to assess production security posture |
| 9 | AuthorizationConstants policy names | Chunk 5 | Class declared but policy name strings not visible from Layer 1 source_code.json extraction; Agent 2 to read source |
| 10 | CORS `allowedOrigins` runtime value | Chunk 5 | Declared in Bicep as a parameter with no default; actual caller-defined origins unknown; Agent 2 to check if passed at deployment time |
| 11 | `applicationInsightsName` parameter | Chunk 3 | Empty default in appservice.bicep; whether it's populated at deployment (via main.bicep) not declared — main.bicep does not pass `applicationInsightsName` to the web module |
| 12 | `baseUrls.apiBase` / `baseUrls.webBase` in appsettings | Chunks 2+5 | Hardcoded localhost URLs in appsettings.json; Docker-specific URLs in appsettings.Docker.json; no production URL config found in this repository — likely injected at runtime or via Key Vault |

---

## Handoff Note to Agent 2

This is a .NET 8.0 ASP.NET Core e-commerce reference application (eShopOnWeb) following Clean Architecture: `ApplicationCore` (domain, no framework deps) → `Infrastructure` (EF Core, SQL Server) → `Web` (MVC + Blazor) + `PublicApi` (Minimal/Endpoint REST). The architecture style is Modular Monolith with two deployable containers (eshopwebmvc, eshoppublicapi) sharing a single SQL Server instance (two logical databases: CatalogDb, IdentityDb). Cloud deployment is via Azure Developer CLI to Azure App Service (B1 Linux) with Azure SQL Server 12.0 and Azure Key Vault Standard, all provisioned via Bicep IaC. CI/CD is GitHub Actions — build and test only (`dotnet build`, `dotnet test`); notably there is **no automated deployment pipeline** in this repository despite complete IaC being present. The highest-priority investigation starting points are: (1) the missing Application Insights SDK — the env var key is declared in Bicep but no SDK package is present and no App Insights resource is provisioned, suggesting observability may be incomplete; (2) the SQL Server wide-open firewall rule (all IPs, publicly accessible) which warrants a security posture assessment; and (3) the absence of a CI/CD deployment workflow despite a complete azd/Bicep setup. Recommended starting layer: **Application Layer** — the Clean Architecture project dependency graph and the `AuthorizationConstants` policy names are the highest-value items not yet resolved by Layer 1 extraction.

---
Agent 1 Scan Complete.
Agent 2 may now begin deep analysis using the 6 output files above.
Recommended starting point: **Application Layer** — reason: Clean Architecture dependency graph fully mapped; `AuthorizationConstants` policy names, full EF DbContext list, and Blazor WebAssembly auth flow are the highest-density unresolved items requiring source-level analysis.
