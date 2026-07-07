=== DOCUMENT: 18_DEPLOYMENT_ARCHITECTURE.md ===

# Deployment Architecture — eShopOnWeb

---

## 1. Deployable Units

| ID | Service | Runtime | Hosts | Azure SKU | Confidence |
|----|---------|---------|-------|-----------|-----------|
| DEP-001 | eshopwebmvc | ASP.NET Core 8.0 | Web MVC + BlazorAdmin + /User endpoint | Azure App Service B1 Linux | HIGH |
| DEP-002 | eshoppublicapi | ASP.NET Core 8.0 | REST API (catalog CRUD, authenticate) | **NOT DEPLOYED TO AZURE (TD-12)** | HIGH |
| DEP-003 | sqlserver | Azure SQL Edge (Docker) / Azure SQL v12 | CatalogDB + IdentityDB | Azure SQL (dev: Docker port 1433) | HIGH |

> Evidence: TA Agent 1 + TA Agent 2; azure.yaml; docker-compose.yml; DEP-002 explicitly absent from azure.yaml

---

## 2. Azure Production Topology

```
                         Internet
                            │
                     HTTPS (TLS 1.2+)
                            │
                            ▼
          ┌─────────────────────────────────────┐
          │  Azure App Service — eshopwebmvc     │
          │  Plan: AppServicePlan-B1 (Linux)     │
          │  Runtime: dotnetcore|8.0             │
          │  httpsOnly: true                     │
          │  ftpsState: FtpsOnly                 │
          │  alwaysOn: true                      │
          │  Identity: SystemAssigned            │
          │  CORS: portal.azure.com              │
          └───────────┬────────────┬─────────────┘
                      │            │
              get+list│            │connections
                      ▼            ▼
          ┌───────────────┐  ┌──────────────────────────────┐
          │ Azure Key     │  │ Azure SQL Server — CatalogDB  │
          │ Vault         │  │ Version: v12.0, TLS 1.2       │
          │ (standard)    │  │ Database: catalogDatabase     │
          │               │  │ ⚠️ Firewall: 0.0.0.1–         │
          │ Secrets:       │  │ 255.255.255.254 (ALL IPs)    │
          │ - catalog-conn │  └──────────────────────────────┘
          │ - identity-conn│
          │ - sqlAdmin     │  ┌──────────────────────────────┐
          │ - appUser      │  │ Azure SQL Server — IdentityDB │
          └───────────────┘  │ Version: v12.0, TLS 1.2       │
                             │ Database: identityDatabase     │
                             │ ⚠️ Firewall: 0.0.0.1–          │
                             │ 255.255.255.254 (ALL IPs)      │
                             └──────────────────────────────┘

⚠️ PublicApi: NO Azure deployment (TD-12)
   eshoppublicapi is absent from azure.yaml.
   It runs in Docker development only.
   See OQ-006 for resolution options.
```

---

## 3. Docker Development Topology

```
localhost
    │
    ├──── Port 5106 ──► eshopwebmvc:8080
    │                    ASPNETCORE_ENVIRONMENT=Docker
    │                    ConnectionStrings from environment
    │                    Volumes: ~/.microsoft/usersecrets
    │                             ~/.aspnet/https
    │
    ├──── Port 5200 ──► eshoppublicapi:8080
    │                    ASPNETCORE_ENVIRONMENT=Docker
    │                    ConnectionStrings from environment
    │
    └──── Port 1433 ──► sqlserver:1433
                         Image: mcr.microsoft.com/azure-sql-edge (⚠️ no tag — TD-17)
                         SA_PASSWORD: hardcoded in docker-compose.yml (TD-02)

Networks: default (implicit compose)
No explicit health checks in docker-compose.yml
No container restart policy
```

---

## 4. Environment Matrix

| Environment | Database | Auth Secret | JWT Key | Secrets | EnableRetry | Health |
|-------------|----------|-------------|---------|---------|-------------|--------|
| Development (local) | EF InMemory (tests) or Docker SQL | User Secrets | **Hardcoded** (TD-01) | dotnet user-secrets | ❌ | /health |
| Docker | Docker SQL Server container | docker-compose env vars | **Hardcoded** (TD-01) | docker-compose.yml | ❌ | /health |
| Production (Azure) | Azure SQL (Key Vault conn string) | Azure Key Vault | **Hardcoded** (TD-01) | Key Vault | ✅ Web only | /health |

> Gap: `EnableRetryOnFailure()` is only configured in Web/Program.cs production path. PublicApi and Docker environments have no retry on transient SQL failures.

---

## 5. Network Configuration

### TLS Configuration

| Component | Min TLS Version | HTTPS Enforced | Notes |
|-----------|----------------|----------------|-------|
| Azure App Service | 1.2 | ✅ httpsOnly:true | FtpsOnly also enforced |
| Azure SQL CatalogDB | 1.2 | N/A (TCP) | minTlsVersion: "1.2" confirmed |
| Azure SQL IdentityDB | 1.2 | N/A (TCP) | minTlsVersion: "1.2" confirmed |
| Docker (dev) | None | ❌ HTTP only | Development purpose only |

### Firewall Configuration

**Current (insecure — TD-11):**
```bicep
// sqlserver.bicep — current state
resource symbolicname 'Microsoft.Sql/servers/firewallRules@2022-08-01-preview' = {
  name: 'AllowAllWindowsAzureIps'   // approximation
  properties: {
    startIpAddress: '0.0.0.1'
    endIpAddress: '255.255.255.254'  // ALL internet IPs can connect
  }
}
```

**Recommended fix options (pick one):**

| Option | Description | Effort | Security Level |
|--------|-------------|--------|---------------|
| A — Service Endpoint | Enable VNet Service Endpoint; restrict SQL to App Service subnet | Medium | High |
| B — Private Endpoint | SQL accessible only from private VNet | High | Highest |
| C — IP Whitelist | Restrict to App Service outbound IP list | Low | Medium |

Option A is recommended for a B1-tier App Service (no VNet injection required; service endpoints suffice).

### CORS Configuration

| Service | AllowedHosts | CORS Policy | Risk |
|---------|-------------|-------------|------|
| Web appsettings.json | `*` | All hosts | Medium — lock down in production |
| PublicApi appsettings.json | `*` | All hosts | Medium — lock down in production |
| Azure App Service | portal.azure.com, ms.portal.azure.com | Bicep `corsAllowOrigins` param | Low |

---

## 6. Azure Resource Inventory

Evidence: TA Agent 1 full Bicep analysis; TA Agent 2 confirmation

| Resource Type | Name Pattern | Config | Notes |
|--------------|-------------|--------|-------|
| App Service Plan | AppServicePlan-{env} | B1, Linux | Shared between Web (and future PublicApi) |
| App Service | eshopwebmvc-{env} | dotnetcore|8.0, alwaysOn | DEP-001 |
| App Service | eshoppublicapi-{env} | **Not provisioned** | TD-12 — missing |
| Azure SQL Server | sqlserver-{env} | v12.0 | Shared for both databases |
| SQL Database | catalogDatabase | Basic SKU (inferred) | CatalogDB |
| SQL Database | identityDatabase | Basic SKU (inferred) | IdentityDB |
| Key Vault | keyvault-{env} | standard | Web Managed Identity access |
| App Insights | **Not provisioned** | — | OQ-007 |

---

## 7. Secrets and Configuration Mapping

### Azure Key Vault → Application Configuration

| Key Vault Secret | App Setting Name | Consumer | Status |
|-----------------|-----------------|---------|--------|
| AZURE-SQL-CATALOG-CONNECTION-STRING | ConnectionStrings:CatalogConnection | Web | ✅ Confirmed |
| AZURE-SQL-IDENTITY-CONNECTION-STRING | ConnectionStrings:IdentityConnection | Web | ✅ Confirmed |
| sqlAdminPassword | (Bicep-only) | sqlserver Bicep | ✅ Confirmed |
| appUserPassword | (Bicep-only) | sqlserver Bicep | ✅ Confirmed |
| jwt-signing-key | **MISSING** (TD-01) | PublicApi + Web | ❌ Must add |
| admin-initial-password | **MISSING** (TD-02) | Seed on startup | ❌ Must add |

### Development Secrets (User Secrets)

```json
{
  "ConnectionStrings:CatalogConnection": "...",
  "ConnectionStrings:IdentityConnection": "...",
  "Jwt:SigningKey": "...",
  "AdminPassword": "..."
}
```

> ⚠️ User Secrets ID: found in src/Web/Web.csproj and src/PublicApi/PublicApi.csproj (both projects share the same development secret store under the shared GUID). Confirm before generation.

---

## 8. Deployment Pipeline (Current and Target)

### Current: GitHub Actions

```yaml
# .github/workflows/dotnetcore.yml (current — gaps highlighted)
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2        # ⚠️ OUTDATED — upgrade to v4
      - uses: actions/setup-dotnet@v1   # ⚠️ OUTDATED — upgrade to v4
      - run: dotnet build ./eShopOnWeb.sln --configuration Release
      - run: dotnet test ./eShopOnWeb.sln --configuration Release
      # Missing: deploy, secret scan, coverage gate
```

### Target: GitHub Actions (generated)

```yaml
# .github/workflows/dotnetcore.yml (target)
on:
  push:
    branches: [main]
  pull_request:

jobs:
  quality-gates:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-dotnet@v4
        with: { dotnet-version: '8.0.x' }
      - run: dotnet build ./eShopOnWeb.sln --configuration Release
      - run: dotnet test ./eShopOnWeb.sln --configuration Release
               --collect:"XPlat Code Coverage"
      - uses: gitleaks/gitleaks-action@v2    # secret scan (G-CI-01)
      - run: dotnet list package --vulnerable

  security-scan:
    needs: quality-gates
    runs-on: ubuntu-latest
    steps:
      - uses: github/codeql-action/init@v3
      - uses: github/codeql-action/analyze@v3

  deploy:
    needs: security-scan
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: azure/login@v1
      - run: azd deploy
      - run: curl --fail https://{hostname}/health
```

---

## 9. Health Check Configuration

| Endpoint | Surface | Check Type | Status |
|----------|---------|-----------|--------|
| GET /health | Web (eshopwebmvc) | Content-based ("Healthy" text) | Confirmed |
| GET /health | PublicApi | Assumed (INFERRED) | Not confirmed — add explicitly |

**Health check implementation gap:** `AddHealthChecks().AddSqlServer()` not found. The existing /health endpoint performs an application-level check but does not verify SQL Server connectivity. A proper liveness + readiness setup should:

1. Liveness: return 200 if app is running
2. Readiness: return 200 only if SQL Server connection is available

```csharp
// Recommended addition to Program.cs:
builder.Services.AddHealthChecks()
    .AddDbContextCheck<CatalogContext>("catalog-db")
    .AddDbContextCheck<AppIdentityDbContext>("identity-db");
```

---

## 10. Deployment Checklist

### Pre-Deployment (must complete)

- [ ] G-SEC-01: JWT signing key removed from source; present in Key Vault
- [ ] G-SEC-02: DEFAULT_PASSWORD removed from source; admin password in Key Vault
- [ ] G-SEC-03: ValidateIssuer=true, ValidateAudience=true with URI values
- [ ] G-DB-01: `dotnet ef database update` succeeds against real Azure SQL
- [ ] G-DB-02: At least one integration test runs against Azure SQL (not InMemory)
- [ ] G-CI-01: gitleaks scan passes with 0 findings
- [ ] TD-11: SQL firewall restricted (not open to all IPs)
- [ ] TD-12: Decision on PublicApi Azure deployment (OQ-006)

### Post-Deployment Verification

- [ ] GET /health returns 200 on both services
- [ ] POST /api/authenticate with admin credentials returns JWT token
- [ ] GET /api/catalog-items returns items (< 200ms — after Task.Delay removed)
- [ ] Web login flow completes; basket transfers on login
- [ ] BlazorAdmin list page loads catalog items (requires JWT from authenticate)
- [ ] Admin can create/update/delete a catalog item via BlazorAdmin
