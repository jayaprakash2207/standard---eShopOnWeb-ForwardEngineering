## Integration & Dependency Graph

### External Integrations

| Integration Name | Category | Protocol / Interface | Direction | Config Key / Env Var | Source File | Confidence |
|---|---|---|---|---|---|---|
| actions/checkout | CI-CD Action | GitHub Actions | CI-CD Pipeline | N/A | .github/workflows/dotnetcore.yml, .github/workflows/richnav.yml | HIGH |
| actions/setup-dotnet | CI-CD Action | GitHub Actions | CI-CD Pipeline | N/A (dotnet-version: '8.0.x') | .github/workflows/dotnetcore.yml, .github/workflows/richnav.yml | HIGH |
| microsoft/RichCodeNavIndexer | CI-CD Action (code indexing) | GitHub Actions | CI-CD Pipeline | repo-token: `${{ github.token }}`; languages: 'csharp'; environment: 'internal' | .github/workflows/richnav.yml | HIGH |
| Dependabot (NuGet) | Dependency Management | GitHub native integration | Inbound (automated PRs) | N/A | .github/dependabot.yml | HIGH |
| Azure Key Vault | Secrets Management / Cloud Service | Azure SDK (Azure.Identity, Azure.Extensions.AspNetCore.Configuration.Secrets) | Outbound | `AZURE_KEY_VAULT_NAME` (referenced for `sqlAdminPassword`, `appUserPassword`) | infra/main.parameters.json, src/Web/Web.csproj | LOW - referenced via env var / package reference only; no Key Vault resource declaration found |
| host.docker.internal (Web service) | Internal Cross-Container Reference | HTTP | Outbound | `baseUrls.webBase` | src/BlazorAdmin/wwwroot/appsettings.Docker.json | LOW - referenced via config key only; no explicit network/DNS declaration |

---

### Internal Service Dependencies (for multi-service / microservice projects)

| Caller Service | Target Service | Protocol | Dependency Type | Config Key / Env Var | Source File |
|---|---|---|---|---|---|
| BlazorAdmin | eshoppublicapi (PublicApi) | HTTP/HTTPS | Synchronous | `baseUrls.apiBase` | src/BlazorAdmin/wwwroot/appsettings.json, appsettings.Development.json, appsettings.Docker.json |
| BlazorAdmin | eshopwebmvc (Web) | HTTP/HTTPS | Synchronous | `baseUrls.webBase` | src/BlazorAdmin/wwwroot/appsettings.json, appsettings.Development.json, appsettings.Docker.json |
| eshopwebmvc (Web) | sqlserver / PostgreSQL (catalog data) | TCP / SQL | Synchronous | `ConnectionStrings:CatalogConnection` | src/Web/appsettings.json, src/Web/appsettings.Docker.json |
| eshopwebmvc (Web) | sqlserver / PostgreSQL (identity data) | TCP / SQL | Synchronous | `ConnectionStrings:IdentityConnection` | src/Web/appsettings.json, src/Web/appsettings.Docker.json |
| eshoppublicapi (PublicApi) | sqlserver / PostgreSQL (catalog data) | TCP / SQL | Synchronous | `ConnectionStrings:CatalogConnection` | src/PublicApi/appsettings.json, src/PublicApi/appsettings.Docker.json |
| eshoppublicapi (PublicApi) | sqlserver / PostgreSQL (identity data) | TCP / SQL | Synchronous | `ConnectionStrings:IdentityConnection` | src/PublicApi/appsettings.json, src/PublicApi/appsettings.Docker.json |
| eshopwebmvc | sqlserver | TCP | Synchronous (compose `depends_on`) | N/A | docker-compose.yml |
| eshoppublicapi | sqlserver | TCP | Synchronous (compose `depends_on`) | N/A | docker-compose.yml |
| eshopwebmvc (Web) | eshoppublicapi (PublicApi) | HTTP/HTTPS | Synchronous | `baseUrls.apiBase` | src/Web/appsettings.json, appsettings.Development.json, appsettings.Docker.json |

---

### Build & Developer Toolchain

| Tool | Version | Purpose | Source File |
|---|---|---|---|
| dotnet build | 8.0.x (SDK) | Build | .github/workflows/dotnetcore.yml |
| dotnet test | 8.0.x (SDK) | Test | .github/workflows/dotnetcore.yml |
| dotnet build (/bl flag) | 8.0.x (SDK) | Build (binary log for code indexing) | .github/workflows/richnav.yml |
| dotnet restore / publish | 8.0.x (SDK) | Build/Packaging (container image build) | src/Web/Dockerfile, src/PublicApi/Dockerfile |
| xunit | (not declared) | Test Framework | tests/FunctionalTests, tests/IntegrationTests, tests/UnitTests (*.csproj) |
| xunit.runner.visualstudio | (not declared) | Test Runner | tests/FunctionalTests, tests/IntegrationTests, tests/UnitTests (*.csproj) |
| xunit.runner.console | (not declared) | Test Runner (console) | tests/UnitTests/UnitTests.csproj |
| dotnet-xunit | 2.3.1 | Test CLI Tool | tests/FunctionalTests/FunctionalTests.csproj |
| NSubstitute | (not declared) | Mocking | tests/IntegrationTests/IntegrationTests.csproj, tests/UnitTests/UnitTests.csproj |
| MSTest.TestAdapter / MSTest.TestFramework | (not declared) | Test Framework | tests/PublicApiIntegrationTests/PublicApiIntegrationTests.csproj |
| coverlet.collector | (not declared) | Code Coverage | tests/PublicApiIntegrationTests/PublicApiIntegrationTests.csproj |
| CodeCoverage.runsettings | (referenced, not provided) | Code Coverage Configuration | eShopOnWeb.sln (Solution Items: tests folder) |
| Microsoft.EntityFrameworkCore.Tools | (not declared) | DB Migration / Scaffolding | src/PublicApi/PublicApi.csproj, src/Web/Web.csproj |
| Microsoft.VisualStudio.Web.CodeGeneration.Design | (not declared) | Code Generation / Scaffolding | src/PublicApi/PublicApi.csproj, src/Web/Web.csproj |
| BuildBundlerMinifier | (not declared) | CSS/JS Bundling & Minification (Release builds only) | src/Web/Web.csproj |
| Microsoft.Web.LibraryManager.Build (libman) | (not declared) | Client-side Library Management | src/Web/Web.csproj |
| Microsoft.VisualStudio.Azure.Containers.Tools.Targets | (not declared) | Container Build Tooling (VS) | src/PublicApi/PublicApi.csproj |

---

### Chunk Inventory - Integration & Dependency Graph
- Technology components found this chunk: None new (all previously catalogued)
- Data stores found this chunk: None new (see Data Store Registry)
- Integrations found this chunk: actions/checkout, actions/setup-dotnet, microsoft/RichCodeNavIndexer, Dependabot (NuGet), Azure Key Vault, host.docker.internal
- Infrastructure resources found: None new
- Environments identified: None new
- CI/CD tool invocations found (this chunk): "build (dotnetcore.yml): dotnet build, dotnet test"; "build (richnav.yml): dotnet build /bl" (carried forward from Infrastructure chunk)
- Reusable workflows followed: None
- Cross-layer dependencies flagged: BlazorAdmin (Application) -> PublicApi & Web (Application/Infrastructure); Web/PublicApi (Application) -> sqlserver/PostgreSQL (Data); Azure Key Vault (Security) <- Web project + azd parameters (Infrastructure)
- Newly flagged as SHARED COMPONENT: None new this chunk
- VERSION CONFLICTS detected: None new this chunk
- LOW CONFIDENCE items raised this chunk:
  - Azure Key Vault integration referenced only via package + parameter placeholder, no Key Vault resource or vault name declared
  - `host.docker.internal` cross-container reference has no corresponding Docker network declaration in docker-compose.yml
