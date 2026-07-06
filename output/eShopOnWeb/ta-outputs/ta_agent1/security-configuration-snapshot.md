## Security & Configuration Snapshot

### Authentication & Authorisation Mechanisms

| Mechanism Name | Type | Provider / Library | Scope | Config Key / Annotation | Source File | Confidence |
|---|---|---|---|---|---|---|
| JWT Bearer Tokens | Authentication | Microsoft.AspNetCore.Authentication.JwtBearer, System.IdentityModel.Tokens.Jwt | API (PublicApi), Web | N/A - package reference only, no issuer/audience/secret config keys found in provided appsettings | src/PublicApi/PublicApi.csproj, src/Web/Web.csproj | LOW - inferred from package references; no explicit JWT configuration block found |
| ASP.NET Core Identity | Authentication / Authorisation (Both) | Microsoft.AspNetCore.Identity.EntityFrameworkCore, Microsoft.AspNetCore.Identity.UI | All (Web, PublicApi - identity store) | `ConnectionStrings:IdentityConnection` | src/Web/Web.csproj, src/PublicApi/PublicApi.csproj, src/Web/appsettings.json, src/PublicApi/appsettings.json | HIGH |
| Blazor WebAssembly Authentication | Authentication | Microsoft.AspNetCore.Components.WebAssembly.Authentication, Microsoft.Extensions.Identity.Core | Frontend (BlazorAdmin) | N/A - package reference only, no provider/authority config found | src/BlazorAdmin/BlazorAdmin.csproj | LOW - inferred from package references; no explicit auth provider/authority configuration found |
| Authorization Components | Authorisation | Microsoft.AspNetCore.Components.Authorization | Frontend (BlazorAdmin) | N/A | src/BlazorAdmin/BlazorAdmin.csproj | LOW - inferred from package reference only |

---

### Secrets & Configuration Management

| Approach | Tool / Service | Scope | Config Key / Reference | Source File | Confidence |
|---|---|---|---|---|---|
| .NET User Secrets | dotnet user-secrets (local dev) | Application (PublicApi) | `UserSecretsId: 5b662463-1efd-4bae-bde4-befe0be3e8ff` | src/PublicApi/PublicApi.csproj | HIGH |
| .NET User Secrets | dotnet user-secrets (local dev) | Application (Web) | `UserSecretsId: aspnet-Web2-1FA3F72E-E7E3-4360-9E49-1CCCD7FE85F7` | src/Web/Web.csproj | HIGH |
| Docker-mounted host secrets | Volume mount (read-only) | Infrastructure / Application | volumes: `~/.aspnet/https:/root/.aspnet/https:ro`, `~/.microsoft/usersecrets:/root/.microsoft/usersecrets:ro` | docker-compose.override.yml | HIGH |
| Azure Key Vault (referenced) | Azure.Extensions.AspNetCore.Configuration.Secrets, Azure.Identity | Application / Infrastructure | `AZURE_KEY_VAULT_NAME` (used by `secretOrRandomPassword` for `sqlAdminPassword`, `appUserPassword`) | infra/main.parameters.json, src/Web/Web.csproj | LOW - referenced via package + deployment parameter only; no Key Vault resource declaration or vault name found |
| Plaintext credentials in source-controlled config | Environment Variables / appsettings (hardcoded) | Infrastructure (Docker) / Application | `SA_PASSWORD` (docker-compose.yml); `ConnectionStrings:CatalogConnection` / `ConnectionStrings:IdentityConnection` password components (src/Web/appsettings.json, src/PublicApi/appsettings.json, src/Web/appsettings.Docker.json, src/PublicApi/appsettings.Docker.json) | docker-compose.yml; src/Web/appsettings*.json; src/PublicApi/appsettings*.json | HIGH - SECRETS MANAGEMENT PATTERN DETECTED: database credentials and `SA_PASSWORD` are committed in plaintext within source-controlled compose/config files (values not reproduced here); Agent 2 to assess risk |

---

### Network Security Declarations

| Declaration | Type | Value (non-secret only) | Source File | Confidence |
|---|---|---|---|---|
| AllowedHosts | Host Filtering | `"*"` | src/Web/appsettings.json, src/PublicApi/appsettings.json | HIGH |
| TLS (Development) | TLS | `https://localhost:44315`, `https://localhost:5099`, `https://localhost:5001` (dev certs via mounted `~/.aspnet/https`) | src/Web/appsettings.Development.json, src/PublicApi/appsettings.Development.json, docker-compose.override.yml | HIGH |
| TLS (Docker) | TLS | `ASPNETCORE_URLS=http://+:8080` - plain HTTP, no TLS termination declared | docker-compose.override.yml, src/Web/appsettings.Docker.json, src/PublicApi/appsettings.Docker.json | HIGH |
| TrustServerCertificate | TLS (DB connection) | `TrustServerCertificate=true` | src/Web/appsettings.Docker.json, src/PublicApi/appsettings.Docker.json | HIGH |
| CORS policy | CORS | Not declared in any provided config file | N/A | LOW - VALUE NOT FOUND - no CORS policy configuration present in scanned appsettings/csproj files |
| CSP / HSTS headers | CSP / HSTS | Not declared in any provided config file | N/A | LOW - VALUE NOT FOUND |

---

### Compliance & Audit Flags

| Item | Type | Detail | Source File |
|---|---|---|---|
| LAYER NOT FOUND | Audit Logging / Data Retention / GDPR / PCI / HIPAA / SOC2 / RBAC | No audit logging configuration keys, data retention settings, or compliance-related annotations found in any provided manifest, config, or IaC file | N/A |

---

### Chunk Inventory - Security Layer
- Technology components found this chunk: None new (JWT, Identity, Azure.Identity, Azure.Extensions.AspNetCore.Configuration.Secrets previously catalogued in Technology Stack Inventory)
- Data stores found this chunk: None new
- Integrations found this chunk: Azure Key Vault (referenced) - carried forward from Integration & Dependency Graph
- Infrastructure resources found: None new
- Environments identified: None new
- CI/CD tool invocations found (this chunk): None
- Reusable workflows followed: None
- Cross-layer dependencies flagged: Identity data store (`ConnectionStrings:IdentityConnection`) shared between Web and PublicApi (Data layer); Azure Key Vault parameter referenced from both Web project (Application) and azd deployment parameters (Infrastructure)
- Newly flagged as SHARED COMPONENT: ASP.NET Core Identity (Web + PublicApi), `ConnectionStrings:IdentityConnection` / `ConnectionStrings:CatalogConnection` config keys (Web + PublicApi)
- VERSION CONFLICTS detected: None new this chunk
- LOW CONFIDENCE items raised this chunk:
  - No JWT issuer/audience/signing-key configuration found despite JWT package references
  - No CORS, CSP, or HSTS configuration found in any provided file
  - Plaintext DB credentials and `SA_PASSWORD` present in source-controlled config files (values withheld from this report per scanning policy)
  - Azure Key Vault referenced by name placeholder only (`AZURE_KEY_VAULT_NAME`); no vault resource or actual name declared
