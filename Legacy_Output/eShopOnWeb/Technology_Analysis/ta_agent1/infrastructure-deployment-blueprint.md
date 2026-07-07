## Infrastructure & Deployment Blueprint

### Compute & Container Resources

| Resource Name | Resource Type | Platform / Provider | Image / Runtime Version | Environments Declared | Key Configuration (non-secret) | Source File | Confidence |
|---|---|---|---|---|---|---|---|
| eshopwebmvc | Container (Docker Compose service) | Docker | Build: mcr.microsoft.com/dotnet/sdk:8.0; Runtime: mcr.microsoft.com/dotnet/aspnet:8.0 | Docker (ASPNETCORE_ENVIRONMENT=Docker) | env: ASPNETCORE_ENVIRONMENT, ASPNETCORE_URLS; ports: 5106:8080; volumes: ~/.aspnet/https:/root/.aspnet/https:ro, ~/.microsoft/usersecrets:/root/.microsoft/usersecrets:ro | docker-compose.yml, docker-compose.override.yml, src/Web/Dockerfile | HIGH |
| eshoppublicapi | Container (Docker Compose service) | Docker | Build: mcr.microsoft.com/dotnet/sdk:8.0; Runtime: mcr.microsoft.com/dotnet/aspnet:8.0 | Docker (ASPNETCORE_ENVIRONMENT=Docker) | env: ASPNETCORE_ENVIRONMENT, ASPNETCORE_URLS; ports: 5200:8080; volumes: ~/.aspnet/https:/root/.aspnet/https:ro, ~/.microsoft/usersecrets:/root/.microsoft/usersecrets:ro; Dockerfile EXPOSE 80, EXPOSE 443 | docker-compose.yml, docker-compose.override.yml, src/PublicApi/Dockerfile | HIGH |
| sqlserver | Container (Docker Compose service) | Docker | mcr.microsoft.com/azure-sql-edge (no tag declared) | Docker | env: SA_PASSWORD, ACCEPT_EULA=Y; ports: 1433:1433 | docker-compose.yml | HIGH |
| Azure deployment environment (azd) | Resource Group / Subscription scope (parameters only) | Azure (via azd / Bicep, main.bicep not provided) | N/A | environmentName = `${AZURE_ENV_NAME}` | parameters: environmentName, location (`${AZURE_LOCATION}`), principalId (`${AZURE_PRINCIPAL_ID}`), sqlAdminPassword, appUserPassword (sourced via `secretOrRandomPassword` from `${AZURE_KEY_VAULT_NAME}`) | infra/main.parameters.json | LOW - parameters file present but no resource-defining Bicep/ARM template (main.bicep) provided in scan input |
| Azure resource naming convention map | Reference / Convention file | Azure (azd abbreviations) | N/A | N/A | Maps ~80 Azure resource type abbreviations (e.g. `kv-` Key Vault, `aks-` AKS, `redis-` Cache for Redis, `cosmos-` Cosmos DB, `app-` App Service, `sql-` SQL) - none of these resource types have corresponding resource declarations in the provided files | infra/abbreviations.json | LOW - inferred from naming convention reference only; no actual resource declarations found for any listed type |

---

### Environments Identified

| Environment Name | Trigger / Target | Source File |
|---|---|---|
| Development | Local development run (ASPNETCORE_ENVIRONMENT=Development, implicit) | src/Web/appsettings.Development.json, src/PublicApi/appsettings.Development.json, src/BlazorAdmin/wwwroot/appsettings.Development.json |
| Docker | Container run via docker-compose (ASPNETCORE_ENVIRONMENT=Docker) | docker-compose.override.yml, src/Web/appsettings.Docker.json, src/PublicApi/appsettings.Docker.json, src/BlazorAdmin/wwwroot/appsettings.Docker.json |
| Default / Production-like | Default config loaded when no environment-specific override applies | src/Web/appsettings.json, src/PublicApi/appsettings.json, src/BlazorAdmin/wwwroot/appsettings.json |
| CI (build) | push, pull_request, workflow_dispatch (any branch) | .github/workflows/dotnetcore.yml |
| CI (code index, manual) | workflow_dispatch only | .github/workflows/richnav.yml |
| Azure (azd environment) | `${AZURE_ENV_NAME}` - deployment-time parameter, target undeclared | infra/main.parameters.json |
| Test (in-memory) | `UseOnlyInMemoryDatabase: true` | tests/PublicApiIntegrationTests/appsettings.test.json |

---

### CI/CD Pipeline Inventory

| Pipeline File | Job / Stage Name | Tool Invocations (first word per run: command) | Actions Used (uses: references) | Runs On Condition | Source |
|---|---|---|---|---|---|
| .github/workflows/dotnetcore.yml | build | dotnet (build ./eShopOnWeb.sln --configuration Release), dotnet (test ./eShopOnWeb.sln --configuration Release) | actions/checkout@v2, actions/setup-dotnet@v1 | push, pull_request, workflow_dispatch (all branches) | .github/workflows/dotnetcore.yml |
| .github/workflows/richnav.yml | build | dotnet (build ./Everything.sln --configuration Release /bl) | actions/checkout@v2, actions/setup-dotnet@v1, microsoft/RichCodeNavIndexer@v0.1 | workflow_dispatch (manual only) | .github/workflows/richnav.yml |

**Additional CI/CD-related config (non-pipeline):**
- `.github/dependabot.yml` - package-ecosystem: "nuget", directory: "/", schedule.interval: "daily" - automated dependency-update bot, not a build pipeline.

**Reusable workflows followed:** None - both workflow files contain only remote `uses:` references (actions/checkout, actions/setup-dotnet, microsoft/RichCodeNavIndexer); no local `./` workflow references found.

**Runner platforms:** `dotnetcore.yml` runs on `ubuntu-latest`; `richnav.yml` runs on `windows-latest`.

---

### Network Topology (declared configuration only - no inference)

- No ingress controller, load balancer, reverse proxy, or API gateway configuration found in provided files.
- No VPC / subnet / security group / network policy declarations found in provided files.
- Internal cross-container reference: `host.docker.internal` used by BlazorAdmin (Docker env) to reach the Web service (`webBase: http://host.docker.internal:5106/`) - src/BlazorAdmin/wwwroot/appsettings.Docker.json.
- TLS termination: Development environments use `https://localhost:*` endpoints with local dev certificates mounted via `~/.aspnet/https` volume (docker-compose.override.yml); Docker environment endpoints are declared as plain `http://` (ASPNETCORE_URLS=http://+:8080) - no TLS termination point declared for Docker/container traffic.
- `TrustServerCertificate=true` declared on SQL Server connection strings in Docker config (src/Web/appsettings.Docker.json, src/PublicApi/appsettings.Docker.json).
- ARCHITECTURE NOTE: No infrastructure-as-code resource definitions (e.g. Bicep `main.bicep`, Terraform, ARM templates, Kubernetes manifests) found - only an azd parameters file (`infra/main.parameters.json`) and an Azure resource-naming abbreviations reference (`infra/abbreviations.json`) are present. Actual cloud resource topology may be defined in files/templates not included in this scan.

---

### Chunk Inventory - Infrastructure & Deployment Blueprint
- Technology components found this chunk: mcr.microsoft.com/dotnet/sdk:8.0, mcr.microsoft.com/dotnet/aspnet:8.0, mcr.microsoft.com/azure-sql-edge, actions/checkout@v2, actions/setup-dotnet@v1, microsoft/RichCodeNavIndexer@v0.1
- Data stores found this chunk: sqlserver (Azure SQL Edge) - see Data Store Registry
- Integrations found this chunk: actions/checkout@v2, actions/setup-dotnet@v1, microsoft/RichCodeNavIndexer@v0.1, dependabot (nuget)
- Infrastructure resources found: eshopwebmvc container, eshoppublicapi container, sqlserver container, Azure azd environment (parameters only)
- Environments identified: Development, Docker, Default/Production-like, CI (build), CI (code index), Azure (azd), Test (in-memory)
- CI/CD tool invocations found (this chunk): "build (dotnetcore.yml): dotnet build, dotnet test"; "build (richnav.yml): dotnet build /bl"
- Reusable workflows followed: None
- Cross-layer dependencies flagged: CI/CD `dotnet build`/`dotnet test` targets `./eShopOnWeb.sln` and `./Everything.sln` (Application layer solutions); Azure azd parameters reference Key Vault for `sqlAdminPassword`/`appUserPassword` (Security layer)
- Newly flagged as SHARED COMPONENT: None new this chunk
- VERSION CONFLICTS detected: None new this chunk (see Data Store Registry for primary DB engine conflict)
- LOW CONFIDENCE items raised this chunk:
  - `infra/main.parameters.json` and `infra/abbreviations.json` present but no Bicep/Terraform/ARM resource template provided - actual Azure resource topology unknown
  - Azure SQL Edge image tag not declared (defaults to `latest`)
  - PublicApi Dockerfile EXPOSE (80/443) vs compose port mapping (8080) discrepancy (also flagged in Component & Service Map)
