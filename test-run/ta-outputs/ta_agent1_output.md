- `sqlAdminPassword` → stored by sqlserver.bicep (×2 modules)
- `appUserPassword` → stored by sqlserver.bicep (×2 modules)
- `AZURE-SQL-CATALOG-CONNECTION-STRING` → stored by sql-catalog module
- `AZURE-SQL-IDENTITY-CONNECTION-STRING` → stored by sql-identity module

### TLS & Network Security (Bicep declarations)

- App Service: `minTlsVersion: '1.2'`, `httpsOnly: true`, `ftpsState: 'FtpsOnly'`
- SQL Server: `minimalTlsVersion: '1.2'`, `publicNetworkAccess: 'Enabled'`
- Firewall: 0.0.0.1–255.255.255.254 (all IPs — see LOW note below)
- CORS (App Service): `https://portal.azure.com`, `https://ms.portal.azure.com` + additional via `allowedOrigins` param

### Application-Level CORS / Config

- `AllowedHosts: *` — declared in appsettings.json for both Web and PublicApi

---

### Chunk Inventory - Security Layer
- Technology components: Microsoft.AspNetCore.Authentication.JwtBearer 8.0.2, System.IdentityModel.Tokens.Jwt 7.3.1, Microsoft.AspNetCore.Identity.EntityFrameworkCore 8.0.2, Azure.Identity 1.10.4, Azure.Extensions.AspNetCore.Configuration.Secrets 1.3.1, System.Security.Claims 4.3.0
- Data stores: Microsoft.eShopOnWeb.Identity (SHARED — identity store for ASP.NET Core Identity)
- Integrations: Azure Key Vault (runtime config provider, Web only); User Secrets (dev only, both services)
- Infrastructure resources: Azure Key Vault standard, Managed Identity SystemAssigned on App Service, Key Vault access policy (secrets: get+list)
- Environments identified: Development (User Secrets), Docker (volume-mounted usersecrets), Production (Key Vault)
- CI/CD tool invocations: None
- Reusable workflows followed: None
- Cross-layer dependencies flagged: JWT config keys (issuer/audience) not found in any config file — likely in User Secrets or Program.cs; Agent 2 to resolve
- Newly flagged as SHARED COMPONENT: ASP.NET Core Identity (Web + PublicApi share IdentityDb); JWT bearer auth (Web + PublicApi + Infrastructure)
- VERSION CONFLICTS: None new
- LOW CONFIDENCE items raised this chunk:
  - SQL Server firewall `0.0.0.1–255.255.255.254` = all IPs allowed; comment in Bicep acknowledges this is for developer debugging — production exposure risk; Agent 2 to flag
  - JWT signing key / issuer / audience not found in any scanned config file — configuration source unknown

---

## Agent 1 - Chunk 6 of 6 - Observability Layer

**Carried Forward:**
- Technology components: All prior
- Data stores: CatalogDb, IdentityDb, InMemory
- Integrations: Azure Key Vault, Azure App Insights (LOW), GitHub Actions
- LOW CONFIDENCE items: 13

---

### Application Insights (Bicep reference)

- `applicationInsights` resource reference in appservice.bicep: `Microsoft.Insights/components@2020-02-02` declared as `existing` — not provisioned in scanned Bicep files
- App settings key: `APPLICATIONINSIGHTS_CONNECTION_STRING` — conditionally injected when `applicationInsightsName` param non-empty
- No Application Insights Bicep module found in `infra/` tree

### Logging Configuration

**Web `appsettings.json`:**
- LogLevel.Default: Warning; LogLevel.Microsoft: Warning; LogLevel.System: Warning; IncludeScopes: false; AllowedHosts: *

**Web `appsettings.Development.json`:**
- LogLevel.Default: Debug; LogLevel.System: Information; LogLevel.Microsoft: Information

**Web `appsettings.Docker.json`:**
- LogLevel.Default: Debug; LogLevel.System: Information; LogLevel.Microsoft: Information

**PublicApi `appsettings.json`:**
- LogLevel.Default: Warning; LogLevel.Microsoft: Warning; LogLevel.System: Warning

**PublicApi `appsettings.Development.json`:**
- LogLevel.Default: Information; LogLevel.Microsoft: Warning; LogLevel.Hosting.Lifetime: Information

**App Service log config (Bicep):**
- applicationLogs.fileSystem.level: Verbose
- detailedErrorMessages.enabled: true
- failedRequestsTracing.enabled: true
- httpLogs.fileSystem.enabled: true, retentionInDays: 1, retentionInMb: 35

### SignalR Client (libman.json)

- `aspnet-signalr@1.0.27` declared as client-side library — server-side SignalR hub configuration not detectable from scanned files

### VSCode Extensions (observability-adjacent)

- `formulahendry.dotnet-test-explorer` — test runner UI
- `ms-kubernetes-tools.vscode-kubernetes-tools` — Kubernetes tooling present in recommendations; no k8s manifests found

---

### Chunk Inventory - Observability Layer
- Technology components found: Application Insights (`Microsoft.Insights/components@2020-02-02` — referenced existing, not provisioned), Microsoft.Extensions.Logging.Configuration 8.0.0
- Data stores: None
- Integrations: Azure Application Insights (APPLICATIONINSIGHTS_CONNECTION_STRING env key — conditional; LOW — provisioning not found)
- Infrastructure resources: None new
- Environments identified: None new
- CI/CD tool invocations: None
- Reusable workflows followed: None
- Cross-layer dependencies: App Insights → App Service (env key injection at deploy time)
- Newly flagged as SHARED COMPONENT: None
- VERSION CONFLICTS: None
- LOW CONFIDENCE items raised:
  - Application Insights referenced as `existing` in Bicep but no provisioning resource in scanned files — may exist outside this repo, or manually provisioned pre-deployment
  - SignalR server-side hub config not detectable from current scan scope

---

## Agent 1 - Project Scan Summary

- **Language(s):** C# / .NET SDK 8.0.x (rollForward: latestFeature)
- **Framework(s):** ASP.NET Core 8.0.2, Blazor WebAssembly 8.0.2, EF Core 8.0.2
- **Architecture style:** Modular Monolith — HIGH confidence (two deployable services sharing common ApplicationCore + Infrastructure projects; single SQL Server; single repo; shared solution file)
- **Deployment target:** Azure App Service (Linux, dotnetcore\|8.0, B1 SKU) + Docker Compose (local dev)
- **Total files scanned:** 38
- **Technology layers found:** 6 — Application, Data, Infrastructure, CI/CD, Security, Observability
- **Chunks processed:** 6
- **External integrations found:** 5 (Azure Key Vault, Azure App Service, Azure SQL, Azure Application Insights [LOW], GitHub Actions)
- **Data stores identified:** 3 (CatalogDb, IdentityDb, InMemory/test)
- **Services / components found:** 5 (eshopwebmvc, eshoppublicapi, sqlserver, App Service, Key Vault)
- **CI/CD pipeline files read:** 2 (0 reusable workflow files followed)
- **CI/CD tool invocations found:** dotnet build, dotnet test

---

## OUTPUT 1 - Technology Stack Inventory

| Component Name | Version | Category | Layer | Package Manager / Source | Source File | Confidence |
|---|---|---|---|---|---|---|
| .NET SDK | 8.0.x (rollForward: latestFeature) | Runtime / SDK | Application | global.json | global.json | HIGH |
| ASP.NET Core | 8.0.2 | Web Framework | Application | NuGet (central props) | Directory.Packages.props | HIGH |
| Blazor WebAssembly | 8.0.2 | UI Framework | Application | NuGet | Directory.Packages.props | HIGH |
| Entity Framework Core (SqlServer) | 8.0.2 | ORM | Data | NuGet | Directory.Packages.props | HIGH |
| Entity Framework Core (InMemory) | 8.0.2 | ORM / Test | Data | NuGet | Directory.Packages.props | HIGH |
| MediatR | 12.0.1 | Mediator / CQRS | Application | NuGet | Directory.Packages.props | HIGH |
| FluentValidation | 11.9.0 | Validation | Application | NuGet | Directory.Packages.props | HIGH |
| AutoMapper | 12.0.1 | Object Mapping | Application | NuGet | Directory.Packages.props | HIGH |
| Ardalis.Specification | 7.0.0 | Repository Pattern | Application | NuGet | Directory.Packages.props | HIGH |
| Ardalis.Specification.EntityFrameworkCore | 7.0.0 | Repository / ORM | Data | NuGet | Directory.Packages.props | HIGH |
| Ardalis.ApiEndpoints | 4.1.0 | API Framework | Application | NuGet | Directory.Packages.props | HIGH |
| Ardalis.GuardClauses | 4.0.1 | Guard Utility | Application | NuGet | Directory.Packages.props | HIGH |
| Ardalis.Result | 7.0.0 | Result Utility | Application | NuGet | Directory.Packages.props | HIGH |
| Ardalis.ListStartupServices | 1.1.4 | Dev Diagnostic | Application | NuGet | Directory.Packages.props | HIGH |
| MinimalApi.Endpoint | 1.3.0 | Minimal API Framework | Application | NuGet | Directory.Packages.props | HIGH |
| Swashbuckle.AspNetCore | 6.5.0 | OpenAPI / Swagger | Application | NuGet | Directory.Packages.props | HIGH |
| Swashbuckle.AspNetCore.SwaggerUI | 6.5.0 | OpenAPI / Swagger | Application | NuGet | Directory.Packages.props | HIGH |
| Swashbuckle.AspNetCore.Annotations | 6.5.0 | OpenAPI / Swagger | Application | NuGet | Directory.Packages.props | HIGH |
| Microsoft.AspNetCore.Authentication.JwtBearer | 8.0.2 | Auth Middleware | Security | NuGet | Directory.Packages.props | HIGH |
| Microsoft.AspNetCore.Identity.EntityFrameworkCore | 8.0.2 | Identity / ORM | Security | NuGet | Directory.Packages.props | HIGH |
| Microsoft.AspNetCore.Identity.UI | 8.0.2 | Identity UI | Security | NuGet | Directory.Packages.props | HIGH |
| Microsoft.Extensions.Identity.Core | 8.0.0 | Identity Core | Security | NuGet | Directory.Packages.props | HIGH |
| Microsoft.AspNetCore.Components.WebAssembly.Authentication | 8.0.2 | Auth / Blazor | Security | NuGet | Directory.Packages.props | HIGH |
| System.IdentityModel.Tokens.Jwt | 7.3.1 | JWT Library | Security | NuGet | Directory.Packages.props | HIGH |
| System.Security.Claims | 4.3.0 | Security Claims | Security | NuGet | Directory.Packages.props | HIGH |
| Azure.Identity | 1.10.4 | Azure SDK / Auth | Security | NuGet | Directory.Packages.props | HIGH |
| Azure.Extensions.AspNetCore.Configuration.Secrets | 1.3.1 | Azure SDK / Config | Security | NuGet | Directory.Packages.props | HIGH |
| Microsoft.AspNetCore.Diagnostics.EntityFrameworkCore | 8.0.2 | Diagnostics | Observability | NuGet | Directory.Packages.props | HIGH |
| Microsoft.Extensions.Logging.Configuration | 8.0.0 | Logging | Observability | NuGet | Directory.Packages.props | HIGH |
| Blazored.LocalStorage | 4.5.0 | Blazor Component | Application | NuGet | Directory.Packages.props | HIGH |
| BlazorInputFile | 0.2.0 | Blazor Component | Application | NuGet | Directory.Packages.props | HIGH |
| System.Net.Http.Json | 8.0.0 | HTTP Client | Application | NuGet | Directory.Packages.props | HIGH |
| System.Text.Json | 8.0.3 | JSON Serialization | Application | NuGet | Directory.Packages.props | HIGH |
| Microsoft.AspNetCore.Components.WebAssembly.Server | 8.0.2 | Blazor Server Host | Application | NuGet | Directory.Packages.props | HIGH |
| Microsoft.Web.LibraryManager.Build | 2.1.175 | Client Library Build | Build | NuGet | Directory.Packages.props | HIGH |
| BuildBundlerMinifier | 3.2.449 | Build / Minifier | Build | NuGet | Directory.Packages.props | HIGH |
| Microsoft.VisualStudio.Azure.Containers.Tools.Targets | 1.19.6 | Docker Build Tool | Build | NuGet | Directory.Packages.props | HIGH |
| Microsoft.VisualStudio.Web.CodeGeneration.Design | 8.0.0 | Scaffolding Tool | Build | NuGet | Directory.Packages.props | HIGH |
| dotnet-ef | 8.0.0 | DB Migration Tool | Build | dotnet tools | src/Web/.config/dotnet-tools.json | HIGH |
| xunit | 2.7.0 | Test Framework | Build | NuGet | Directory.Packages.props | HIGH |
| xunit.runner.visualstudio | 2.5.6 | Test Runner | Build | NuGet | Directory.Packages.props | HIGH |
| xunit.runner.console | 2.7.0 | Test Runner | Build | NuGet | Directory.Packages.props | HIGH |
| MSTest.TestAdapter | 3.2.2 | Test Framework | Build | NuGet | Directory.Packages.props | HIGH |
| MSTest.TestFramework | 3.2.2 | Test Framework | Build | NuGet | Directory.Packages.props | HIGH |
| NSubstitute | 5.1.0 | Test Mocking | Build | NuGet | Directory.Packages.props | HIGH |
| NSubstitute.Analyzers.CSharp | 1.0.17 | Test Analyzer | Build | NuGet | Directory.Packages.props | HIGH |
| Microsoft.AspNetCore.Mvc.Testing | 8.0.2 | Integration Test | Build | NuGet | Directory.Packages.props | HIGH |
| Microsoft.NET.Test.Sdk | 17.9.0 | Test SDK | Build | NuGet | Directory.Packages.props | HIGH |
| coverlet.collector | 6.0.2 | Code Coverage | Build | NuGet | Directory.Packages.props | HIGH |
| jQuery | 3.6.3 | Client JS Library | Application | cdnjs (libman) | src/Web/libman.json | HIGH |
| Bootstrap | 3.4.1 | CSS Framework | Application | cdnjs (libman) | src/Web/libman.json | HIGH |
| jquery-validation-unobtrusive | 4.0.0 | Client Validation | Application | cdnjs (libman) | src/Web/libman.json | HIGH |
| jquery-validate | 1.19.5 | Client Validation | Application | cdnjs (libman) | src/Web/libman.json | HIGH |
| toastr.js | 2.1.4 | UI Notification | Application | cdnjs (libman) | src/Web/libman.json | HIGH |
| aspnet-signalr (client) | 1.0.27 | Real-time Client | Application | cdnjs (libman) | src/Web/libman.json | HIGH |
| Azure SQL Edge | tag UNKNOWN | Container DB Image | Data | Docker Hub / MCR | docker-compose.yml | LOW - no image tag declared |
| Azure SQL Server | v12.0 | Relational Database | Data | Azure / Bicep | infra/core/database/sqlserver/sqlserver.bicep | HIGH |
| Azure App Service | dotnetcore\|8.0, B1 Linux | Hosting Platform | Infrastructure | Bicep | infra/core/host/appservice.bicep | HIGH |
| Azure App Service Plan | B1 | Compute Plan | Infrastructure | Bicep | infra/core/host/appserviceplan.bicep | HIGH |
| Azure Key Vault | standard SKU | Secrets Management | Security | Bicep | infra/core/security/keyvault.bicep | HIGH |
| Azure Managed Identity | SystemAssigned | Identity | Security | Bicep | infra/core/host/appservice.bicep | HIGH |
| Azure Application Insights | v2020-02-02 (existing ref) | Observability | Observability | Bicep (existing ref only) | infra/core/host/appservice.bicep | LOW - referenced as existing; no provisioning found |
| Azure Developer CLI (azd) | unversioned | Deployment Tool | CI-CD | azure.yaml | azure.yaml | HIGH |
| actions/checkout | v2 | CI/CD Action | CI-CD | GitHub Actions | .github/workflows/dotnetcore.yml | HIGH |
| actions/setup-dotnet | v1 | CI/CD Action | CI-CD | GitHub Actions | .github/workflows/dotnetcore.yml | HIGH |
| microsoft/RichCodeNavIndexer | v0.1 | CI/CD Action | CI-CD | GitHub Actions | .github/workflows/richnav.yml | HIGH |
| GitHub Dependabot | v2 | Dependency Scanner | CI-CD | GitHub | .github/dependabot.yml | HIGH |
| Microsoft.AspNetCore.Mvc | 2.2.0 | Web Framework | Application | NuGet | Directory.Packages.props | LOW - declared in central props but no PackageReference found in any csproj; may be vestigial |
| dotnet-xunit | 2.3.1 | Test Runner (legacy) | Build | DotNetCliToolReference | tests/FunctionalTests/FunctionalTests.csproj | LOW - deprecated DotNetCliToolReference format; not in central props |

---

## OUTPUT 2 - Component & Service Map

| Service / Component Name | Type | Exposed Port(s) | Communication Protocol(s) | Primary Technology | Source File | Notes |
|---|---|---|---|---|---|---|
| eshopwebmvc | Frontend Web App | 5106 (host) → 8080 (container) | HTTP | ASP.NET Core 8.0.2 + Blazor WebAssembly 8.0.2 | docker-compose.yml | Dockerfile content not scanned; depends_on sqlserver |
| eshoppublicapi | API Service | 5200 (host) → 8080 (container) | HTTP | ASP.NET Core 8.0.2 (MinimalApi + Ardalis.ApiEndpoints + Swagger) | docker-compose.yml | Dockerfile content not scanned; depends_on sqlserver; NOT declared in azure.yaml |
| sqlserver | Relational Database | 1433:1433 | TCP | Azure SQL Edge (tag UNKNOWN) | docker-compose.yml | Local dev only; SA_PASSWORD hardcoded |
| web (Azure App Service) | Frontend Web App | 443 (HTTPS) | HTTPS | dotnetcore\|8.0 on App Service Linux B1 | infra/main.bicep | httpsOnly:true; SystemAssigned Managed Identity; only service declared in azure.yaml |
| Azure SQL (catalog) | Relational Database | N/A | TCP | Azure SQL Server v12.0, minTLS 1.2 | infra/main.bicep | DB name: catalogDatabase; firewall all IPs open |
| Azure SQL (identity) | Relational Database | N/A | TCP | Azure SQL Server v12.0, minTLS 1.2 | infra/main.bicep | DB name: identityDatabase; firewall all IPs open |
| Azure Key Vault | Secrets Management | N/A | HTTPS / Azure SDK | Azure Key Vault standard | infra/core/security/keyvault.bicep | App Service has get+list on secrets via managed identity |
| ApplicationCore | Class Library | N/A | N/A | C# / .NET 8 | src/ApplicationCore/ApplicationCore.csproj | SHARED COMPONENT — referenced by Web, PublicApi, FunctionalTests, UnitTests |
| Infrastructure | Class Library | N/A | N/A | C# / .NET 8 + EF Core | src/Infrastructure/Infrastructure.csproj | SHARED COMPONENT — referenced by Web, PublicApi, IntegrationTests |
| BlazorAdmin | Blazor WASM Component | N/A | N/A | Blazor WebAssembly 8.0.2 | src/BlazorAdmin/BlazorAdmin.csproj | Hosted within Web project |
| BlazorShared | Class Library | N/A | N/A | C# / .NET 8 | src/BlazorShared/BlazorShared.csproj | SHARED COMPONENT — referenced by Web, BlazorAdmin, ApplicationCore |

---

## OUTPUT 3 - Data Store Registry

| Store Name | Category | Engine / Technology | Version | Declared Database / Collection Name | Connected Services (if detectable) | Source File | Confidence |
|---|---|---|---|---|---|---|---|
| sqlserver (compose) | Relational Database | Azure SQL Edge | UNKNOWN (no tag) | Microsoft.eShopOnWeb.CatalogDb; Microsoft.eShopOnWeb.Identity | eshopwebmvc, eshoppublicapi | docker-compose.yml | LOW - no image tag declared |
| Azure SQL (catalog) | Relational Database | Azure SQL Server | v12.0 | catalogDatabase (param; default value) | web (App Service) | infra/main.bicep, infra/core/database/sqlserver/sqlserver.bicep | HIGH |
| Azure SQL (identity) | Relational Database | Azure SQL Server | v12.0 | identityDatabase (param; default value) | web (App Service) | infra/main.bicep, infra/core/database/sqlserver/sqlserver.bicep | HIGH |
| InMemory DB | In-Memory / Test | EF Core InMemory | 8.0.2 | (not declared) | FunctionalTests, PublicApiIntegrationTests, Infrastructure | Directory.Packages.props, tests/PublicApiIntegrationTests/appsettings.test.json | HIGH — test-only; UseOnlyInMemoryDatabase: true |

---

## OUTPUT 4 - Infrastructure & Deployment Blueprint

### Compute & Container Resources

| Resource Name | Resource Type | Platform / Provider | Image / Runtime Version | Environments Declared | Key Configuration (non-secret) | Source File | Confidence |
|---|---|---|---|---|---|---|---|
| eshopwebmvc | Container | Docker Compose | src/Web/Dockerfile (content unknown) | Docker | ASPNETCORE_ENVIRONMENT, ASPNETCORE_URLS=http://+:8080, port 5106:8080, usersecrets + https volumes | docker-compose.yml + override | HIGH |
| eshoppublicapi | Container | Docker Compose | src/PublicApi/Dockerfile (content unknown) | Docker | ASPNETCORE_ENVIRONMENT, ASPNETCORE_URLS=http://+:8080, port 5200:8080, usersecrets + https volumes | docker-compose.yml + override | HIGH |
| sqlserver | Container | Docker Compose | mcr.microsoft.com/azure-sql-edge (no tag) | Docker | SA_PASSWORD (env), ACCEPT_EULA, port 1433:1433 | docker-compose.yml | LOW - no image tag |
| web (App Service) | Azure App Service | Azure / Bicep | dotnetcore\|8.0 | Production | httpsOnly:true, minTlsVersion:1.2, ftpsState:FtpsOnly, alwaysOn:true, B1 SKU, SystemAssigned identity, CORS: portal.azure.com, AZURE_SQL_*_CONNECTION_STRING_KEY, AZURE_KEY_VAULT_ENDPOINT, APPLICATIONINSIGHTS_CONNECTION_STRING | infra/core/host/appservice.bicep, infra/main.bicep | HIGH |
| appserviceplan | Azure App Service Plan | Azure / Bicep | B1 | Production | reserved:true (Linux), kind:'' | infra/core/host/appserviceplan.bicep | HIGH |
| sql-catalog | Azure SQL Server | Azure / Bicep | SQL Server v12.0, minTLS 1.2 | Production | publicNetworkAccess:Enabled, firewall 0.0.0.1–255.255.255.254, deployment script azCliVersion:2.37.0 | infra/core/database/sqlserver/sqlserver.bicep | HIGH |
| sql-identity | Azure SQL Server | Azure / Bicep | SQL Server v12.0, minTLS 1.2 | Production | publicNetworkAccess:Enabled, firewall 0.0.0.1–255.255.255.254, deployment script azCliVersion:2.37.0 | infra/core/database/sqlserver/sqlserver.bicep | HIGH |
| keyvault | Azure Key Vault | Azure / Bicep | standard SKU | Production | tenantId from subscription(), secrets: get+list for principalId | infra/core/security/keyvault.bicep | HIGH |

### Environments Identified

| Environment Name | Trigger / Target | Source File |
|---|---|---|
| Development | Local run / ASPNETCORE_ENVIRONMENT=Development, launchSettings | .vscode/launch.json, appsettings.Development.json |
| Docker | ASPNETCORE_ENVIRONMENT=Docker, docker-compose up | docker-compose.override.yml |
| Production | azd up / Azure deployment | azure.yaml, infra/main.bicep |

### CI/CD Pipeline Inventory

| Pipeline File | Job / Stage Name | Tool Invocations | Actions Used | Runs On Condition | Source |
|---|---|---|---|---|---|
| .github/workflows/dotnetcore.yml | build | dotnet build, dotnet test | actions/checkout@v2, actions/setup-dotnet@v1 | push, pull_request, workflow_dispatch (all branches) | .github/workflows/dotnetcore.yml |
| .github/workflows/richnav.yml | build | dotnet build | actions/checkout@v2, actions/setup-dotnet@v1, microsoft/RichCodeNavIndexer@v0.1 | workflow_dispatch only | .github/workflows/richnav.yml |
| .github/dependabot.yml | N/A (scheduled scan) | N/A | N/A | daily schedule, nuget ecosystem | .github/dependabot.yml |

### Network Topology

- No ingress / load balancer declarations found (Azure Front Door, Application Gateway, or Nginx not provisioned in scanned Bicep)
- No internal service mesh or DNS declarations found
- No VPC / subnet / NSG declarations found in scanned files (abbreviations.json contains naming prefixes for these but no provisioning)
- TLS termination: App Service (`minTlsVersion: 1.2`, `httpsOnly: true`); SQL Server (`minimalTlsVersion: 1.2`)
- Docker network: implicit compose default network (no explicit network block declared)

---

## OUTPUT 5 - Integration & Dependency Graph

### External Integrations

| Integration Name | Category | Protocol / Interface | Direction | Config Key / Env Var | Source File | Confidence |
|---|---|---|---|---|---|---|
| Azure Key Vault | Secrets Management | Azure SDK (HTTPS) | Inbound (config read at startup) | AZURE_KEY_VAULT_ENDPOINT | infra/main.bicep, infra/core/security/keyvault.bicep, src/Web/Web.csproj | HIGH |
| Azure App Service | Hosting Platform | Azure ARM / azd | Outbound (deploy target) | AZURE_ENV_NAME, AZURE_LOCATION | azure.yaml, infra/main.bicep | HIGH |
| Azure SQL Server (catalog) | Relational Database | ADO.NET / EF Core | Outbound | AZURE_SQL_CATALOG_CONNECTION_STRING_KEY, ConnectionStrings.CatalogConnection | infra/main.bicep, appsettings.json | HIGH |
| Azure SQL Server (identity) | Relational Database | ADO.NET / EF Core | Outbound | AZURE_SQL_IDENTITY_CONNECTION_STRING_KEY, ConnectionStrings.IdentityConnection | infra/main.bicep, appsettings.json | HIGH |
| Azure Application Insights | Observability | Azure SDK | Outbound | APPLICATIONINSIGHTS_CONNECTION_STRING | infra/core/host/appservice.bicep | LOW - env key declared; provisioning resource not found in scanned files |
| actions/checkout | CI/CD Action | GitHub Actions | CI-CD Pipeline | N/A | .github/workflows/dotnetcore.yml | HIGH |
| actions/setup-dotnet | CI/CD Action | GitHub Actions | CI-CD Pipeline | dotnet-version: 8.0.x | .github/workflows/dotnetcore.yml | HIGH |
| microsoft/RichCodeNavIndexer | Code Indexing Action | GitHub Actions | CI-CD Pipeline | repo-token, languages, environment | .github/workflows/richnav.yml | HIGH |
| GitHub Dependabot | Dependency Scanning | GitHub | Inbound (PRs raised) | N/A | .github/dependabot.yml | HIGH |
| cdnjs | Client Library CDN | HTTPS (libman at build) | Outbound (build time) | N/A | src/Web/libman.json | HIGH |

### Internal Service Dependencies

| Caller Service | Target Service | Protocol | Dependency Type | Config Key / Env Var | Source File |
|---|---|---|---|---|---|
| eshopwebmvc | sqlserver | TCP | Synchronous | ConnectionStrings.CatalogConnection, ConnectionStrings.IdentityConnection | docker-compose.yml, appsettings.Docker.json |
| eshoppublicapi | sqlserver | TCP | Synchronous | ConnectionStrings.CatalogConnection, ConnectionStrings.IdentityConnection | docker-compose.yml, appsettings.Docker.json |
| eshopwebmvc | eshoppublicapi | HTTP | Synchronous | baseUrls.apiBase | appsettings.Docker.json (apiBase: http://localhost:5200/api/) |
| web (App Service) | Azure SQL catalog | TCP | Synchronous | AZURE_SQL_CATALOG_CONNECTION_STRING_KEY → Key Vault secret | infra/main.bicep |
| web (App Service) | Azure SQL identity | TCP | Synchronous | AZURE_SQL_IDENTITY_CONNECTION_STRING_KEY → Key Vault secret | infra/main.bicep |

### Build & Developer Toolchain

| Tool | Version | Purpose | Source File |
|---|---|---|---|
| dotnet CLI | 8.0.x | Build, test, run, publish, watch | .vscode/tasks.json, .github/workflows/ |
| dotnet-ef | 8.0.0 | EF Core migrations | src/Web/.config/dotnet-tools.json |
| MSBuild | (bundled with .NET SDK) | Solution build (/bl binary log in richnav) | .github/workflows/richnav.yml |
| BuildBundlerMinifier | 3.2.449 | CSS/JS bundle + minify (Release only) | src/Web/Web.csproj |
| Microsoft.Web.LibraryManager.Build | 2.1.175 | Client library restore at build | src/Web/Web.csproj |
| Azure Developer CLI (azd) | unversioned | Provision + deploy to Azure | azure.yaml |
| coverlet.collector | 6.0.2 | Code coverage collection | Directory.Packages.props |

---

## OUTPUT 6 - Security & Configuration Snapshot

### Authentication & Authorisation Mechanisms

| Mechanism Name | Type | Provider / Library | Scope | Config Key / Annotation | Source File | Confidence |
|---|---|---|---|---|---|---|
| JWT Bearer Tokens | Authentication | Microsoft.AspNetCore.Authentication.JwtBearer 8.0.2 + System.IdentityModel.Tokens.Jwt 7.3.1 | API (PublicApi) + Web | JWT signing key / issuer / audience NOT in scanned config files | Directory.Packages.props, src/Infrastructure/Infrastructure.csproj | HIGH — package declared; LOW - JWT config keys not found in any appsettings file |
| ASP.NET Core Identity | Authentication / Authorisation | Microsoft.AspNetCore.Identity.EntityFrameworkCore 8.0.2 | Web + PublicApi | ConnectionStrings.IdentityConnection | Directory.Packages.props | HIGH |
| Blazor WebAssembly Authentication | Authentication | Microsoft.AspNetCore.Components.WebAssembly.Authentication 8.0.2 | BlazorAdmin | N/A | src/BlazorAdmin/BlazorAdmin.csproj | HIGH |
| Azure Managed Identity | Authentication (service-to-Azure) | Azure.Identity 1.10.4 / SystemAssigned | App Service → Key Vault | AZURE_KEY_VAULT_ENDPOINT | infra/core/host/appservice.bicep, src/Web/Web.csproj | HIGH |
| ASP.NET Core User Secrets | Secrets (dev) | .NET User Secrets | Development only | UserSecretsId (Web + PublicApi) | src/Web/Web.csproj, src/PublicApi/PublicApi.csproj | HIGH |

### Secrets & Configuration Management

| Approach | Tool / Service | Scope | Config Key / Reference | Source File | Confidence |
|---|---|---|---|---|---|
| Azure Key Vault | Azure Key Vault standard | Application (production Web) + Infrastructure | AZURE_KEY_VAULT_ENDPOINT, AZURE-SQL-CATALOG-CONNECTION-STRING, AZURE-SQL-IDENTITY-CONNECTION-STRING, sqlAdminPassword, appUserPassword | infra/core/security/keyvault.bicep, infra/main.bicep | HIGH |
| ASP.NET Core User Secrets | Built-in .NET | Development (Web + PublicApi) | UserSecretsId mount in docker-compose override | src/Web/Web.csproj, src/PublicApi/PublicApi.csproj, docker-compose.override.yml | HIGH |
| Environment Variables | Docker Compose | Docker dev environment | ASPNETCORE_ENVIRONMENT, ASPNETCORE_URLS, SA_PASSWORD, ACCEPT_EULA | docker-compose.yml + override | HIGH |
| Hardcoded dev credentials | N/A | Docker environment only | SA_PASSWORD + connection string passwords in appsettings.Docker.json | docker-compose.yml, appsettings.Docker.json (Web + PublicApi) | HIGH — SECRETS MANAGEMENT PATTERN DETECTED: dev-only but hardcoded values present |
| Azure ARM parameters (@secure) | Azure Bicep | Infrastructure provisioning | sqlAdminPassword, appUserPassword sourced from `$(secretOrRandomPassword ...)` | infra/main.parameters.json | HIGH |

### Network Security Declarations

| Declaration | Type | Value (non-secret only) | Source File | Confidence |
|---|---|---|---|---|
| App Service TLS minimum version | TLS | 1.2 | infra/core/host/appservice.bicep | HIGH |
| App Service HTTPS only | TLS | true | infra/core/host/appservice.bicep | HIGH |
| App Service FTPS state | TLS | FtpsOnly | infra/core/host/appservice.bicep | HIGH |
| SQL Server TLS minimum version | TLS | 1.2 | infra/core/database/sqlserver/sqlserver.bicep | HIGH |
| SQL Server firewall rule | Firewall | 0.0.0.1–255.255.255.254 (all IPs) | infra/core/database/sqlserver/sqlserver.bicep | HIGH — intentionally open per Bicep comment; production risk |
| App Service CORS origins | CORS | https://portal.azure.com, https://ms.portal.azure.com (+ allowedOrigins param) | infra/core/host/appservice.bicep | HIGH |
| Application AllowedHosts | CORS | * (all hosts) | src/Web/appsettings.json, src/PublicApi/appsettings.json | HIGH |
| Key Vault access policy | Access Control | secrets: [get, list] for principalId | infra/core/security/keyvault.bicep, keyvault-access.bicep | HIGH |

### Compliance & Audit Flags

| Item | Type | Detail | Source File |
|---|---|---|---|
| App Service application logs | Audit Logging | fileSystem level Verbose; retentionInDays:1, retentionInMb:35 | infra/core/host/appservice.bicep |
| App Service detailed error messages | Audit Logging | enabled:true | infra/core/host/appservice.bicep |
| App Service failed request tracing | Audit Logging | enabled:true | infra/core/host/appservice.bicep |
| App Service HTTP logs | Audit Logging | fileSystem enabled, 1-day retention | infra/core/host/appservice.bicep |
| SQL deployment script retention | Data Retention | retentionInterval: PT1H (script resource, not data) | infra/core/database/sqlserver/sqlserver.bicep |

---

## Validation Queue

| # | Item | Chunk | Reason |
|---|---|---|---|
| 1 | `Microsoft.AspNetCore.Mvc 2.2.0` in Directory.Packages.props | 1 | Declared in central package management but no PackageReference found in any csproj; may be vestigial; version conflicts with net8.0 ecosystem |
| 2 | `dotnet-xunit 2.3.1` in FunctionalTests.csproj | 1 | Deprecated DotNetCliToolReference format; not in Directory.Packages.props; may not resolve correctly on modern SDK |
| 3 | `azure-sql-edge` — no image tag | 2 | docker-compose.yml uses implicit latest; production-grade pinning absent; actual version unknown |
| 4 | `SA_PASSWORD` + connection string passwords hardcoded | 2 | Present in docker-compose.yml and appsettings.Docker.json; dev-only but committed to repo; SECRETS MANAGEMENT PATTERN DETECTED |
| 5 | JWT signing key / issuer / audience not in any config file | 5 | JwtBearer + IdentityModel.Tokens.Jwt declared; configuration source unknown — likely User Secrets or Program.cs; Agent 2 to resolve via source code scan |
| 6 | SQL Server firewall 0.0.0.1–255.255.255.254 | 5 | All IPs allowed to Azure SQL; comment in Bicep acknowledges this is a developer convenience, not production-hardened |
| 7 | Application Insights — no provisioning resource | 6 | Referenced as `existing` in appservice.bicep; no `Microsoft.Insights/components` Bicep module found; may be manually provisioned or in a missing file |
| 8 | PublicApi deployment to Azure undeclared | 3 | Only `web` service in azure.yaml; no Bicep module for PublicApi; how/whether PublicApi deploys to production is unknown |
| 9 | src/Web/Dockerfile and src/PublicApi/Dockerfile not provided | 3 | Referenced in docker-compose.yml; base images, exposed ports, ENTRYPOINT unknown |
| 10 | SignalR client declared; server-side hub config unknown | 6 | aspnet-signalr@1.0.27 in libman.json; no server-side hub registration detectable from scanned config files |
| 11 | `actions/checkout@v2` and `actions/setup-dotnet@v1` pinned to old versions | 4 | v2/v1 are outdated; v4 is current for both actions; security and compatibility implications for Agent 2 to assess |
| 12 | No deployment step in CI/CD | 4 | Neither workflow contains az deploy, azd deploy, docker push, or equivalent; deployment to Azure appears to be manual (azd up) |
| 13 | `KubernetesTools` VSCode extension recommended | 6 | Present in .vscode/extensions.json but no k8s manifests found anywhere in scanned files |

---

## Handoff Note to Agent 2

eShopOnWeb is a **modular monolith** built on ASP.NET Core 8.0.2 with two deployable surfaces: `Web` (MVC + Blazor WASM admin panel) and `PublicApi` (minimal API + Swagger). Both share `ApplicationCore` and `Infrastructure` class libraries and connect to two SQL Server databases — `CatalogDb` and `IdentityDb` — using EF Core 8.0.2. Production infrastructure is Azure App Service (B1, Linux, dotnetcore\|8.0) provisioned via Bicep; secrets flow through Azure Key Vault via a SystemAssigned Managed Identity on the web service only.

**Start with the Application layer** (highest dependency density): the Ardalis Specification + MediatR + FluentValidation combination signals a deliberate domain architecture worth mapping before the data layer. The Data layer second priority: two separate SQL Server instances in production but a single `sqlserver` container in Docker with shared credentials is an architecture inconsistency Agent 2 should resolve. The most significant unresolved items are: (1) JWT configuration source missing from all config files; (2) PublicApi has no declared Azure deployment path; (3) both Dockerfiles are unscanned; (4) the open SQL Server firewall rule is a production risk requiring explicit assessment.

---
*Agent 1 Scan Complete.*
*Agent 2 may now begin deep analysis using the 6 output files above.*
*Recommended starting point: Application Layer — reason: highest dependency density; Ardalis + MediatR + FluentValidation pattern signals deliberate architectural structure that must be understood before data and infrastructure layers can be accurately assessed.*
