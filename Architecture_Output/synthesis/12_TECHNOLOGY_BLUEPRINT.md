=== DOCUMENT: 12_TECHNOLOGY_BLUEPRINT.md ===

# Technology Blueprint — eShopOnWeb

---

## 1. Technology Stack Summary

### Core Runtime

| Layer | Technology | Version | Role | Status |
|-------|-----------|---------|------|--------|
| Runtime | .NET SDK | 8.0.x (rollForward: latestFeature) | All projects | LTS Nov 2026 ✅ |
| Web Framework | ASP.NET Core | 8.0.2 | MVC + Minimal API | Supported ✅ |
| SPA Framework | Blazor WebAssembly | 8.0.2 | Admin portal | Supported ✅ |
| ORM | Entity Framework Core | 8.0.2 | Data access | Supported ✅ |
| Database | SQL Server / Azure SQL | v12.0 | Persistence | Supported ✅ |

### Application Libraries

| Library | Version | Purpose | Maturity |
|---------|---------|---------|---------|
| MediatR | 12.0.1 | CQRS (read-side only) | Partial use — writes bypass |
| FluentValidation | 11.9.0 | API request validation | Supported |
| AutoMapper | 12.0.1 | DTO mapping | Supported |
| Ardalis.Specification | 7.0.0 | Repository query objects | Core pattern ✅ |
| Ardalis.ApiEndpoints | 4.1.0 | Endpoint base class | Used for AuthEndpoint |
| Ardalis.GuardClauses | 4.0.1 | Guard clauses | Core pattern ✅ |
| Ardalis.Result | 7.0.0 | Result type | Partial use |
| MinimalApi.Endpoint | 1.3.0 | Catalog API endpoints | Core pattern ✅ |
| Swashbuckle.AspNetCore | 6.5.0 | OpenAPI / Swagger | PublicApi only |
| Blazored.LocalStorage | 4.5.0 | Browser cache (60s TTL) | BlazorAdmin ✅ |
| System.IdentityModel.Tokens.Jwt | 7.3.1 | JWT creation | Core security |
| Azure.Identity | 1.10.4 | Managed Identity (Web prod) | Partial |
| Azure.Extensions.AspNetCore.Configuration.Secrets | 1.3.1 | Key Vault config provider | Web prod only |

### Security Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| Microsoft.AspNetCore.Authentication.JwtBearer | 8.0.2 | JWT validation (PublicApi) |
| Microsoft.AspNetCore.Identity.EntityFrameworkCore | 8.0.2 | Identity store |
| Microsoft.AspNetCore.Identity.UI | 8.0.2 | Identity scaffold pages |
| Microsoft.AspNetCore.Components.WebAssembly.Authentication | 8.0.2 | Blazor auth |
| System.Security.Claims | 4.3.0 | Claims primitives |

### Frontend Libraries (CDN via libman)

| Library | Version | Purpose | Status |
|---------|---------|---------|--------|
| Bootstrap | 3.4.1 | CSS framework | **EOL July 2019 — TD-13** |
| jQuery | 3.6.3 | DOM manipulation | In use |
| jquery-validation | 1.19.5 | Client-side validation | In use |
| jquery-validation-unobtrusive | 4.0.0 | MVC unobtrusive validation | In use |
| toastr.js | 2.1.4 | Toast notifications | In use |
| aspnet-signalr | 1.0.27 | Real-time client | **Dead — no server hub (TD-16)** |

### Test Stack

| Library | Version | Purpose | Note |
|---------|---------|---------|------|
| xunit | 2.7.0 | Unit + functional tests | Primary |
| MSTest.TestFramework | 3.2.2 | Integration tests | Secondary |
| NSubstitute | 5.1.0 | Mocking | Used |
| Microsoft.AspNetCore.Mvc.Testing | 8.0.2 | Integration test host | Used |
| EF Core InMemory | 8.0.2 | Test database | **No FK/UNIQUE enforcement (DA-Agent-2)** |
| coverlet.collector | 6.0.2 | Coverage | **Not wired in CI** |

---

## 2. Infrastructure Blueprint

### Azure Production Topology

```
Internet
    │
    ▼ HTTPS (TLS 1.2 min)
Azure App Service (B1 Linux, dotnetcore|8.0)
    │  Name: eshopwebmvc
    │  httpsOnly: true
    │  ftpsState: FtpsOnly
    │  alwaysOn: true
    │  SystemAssigned Managed Identity
    │  CORS: portal.azure.com, ms.portal.azure.com
    │
    ├──► Azure Key Vault (standard)
    │      Secrets: AZURE-SQL-CATALOG-CONNECTION-STRING
    │               AZURE-SQL-IDENTITY-CONNECTION-STRING
    │               sqlAdminPassword, appUserPassword
    │      Access: get+list via Managed Identity
    │
    ├──► Azure SQL Server — CatalogDB (v12.0, TLS 1.2)
    │      Database: catalogDatabase
    │      Firewall: 0.0.0.1-255.255.255.254 ← ALL IPs OPEN (TD-11)
    │      publicNetworkAccess: Enabled
    │
    └──► Azure SQL Server — IdentityDB (v12.0, TLS 1.2)
           Database: identityDatabase
           Firewall: 0.0.0.1-255.255.255.254 ← ALL IPs OPEN (TD-11)
           publicNetworkAccess: Enabled

⚠️ PublicApi (eshoppublicapi): NOT DEPLOYED TO AZURE (TD-12)
   PublicApi has no App Service, no azure.yaml entry, no Key Vault integration.
   Decision required: see OQ-006.
```

### Docker Compose Development Topology

```
localhost
    ├── 5106 → eshopwebmvc:8080 (ASP.NET Core, ASPNETCORE_ENVIRONMENT=Docker)
    ├── 5200 → eshoppublicapi:8080 (ASP.NET Core, ASPNETCORE_ENVIRONMENT=Docker)
    └── 1433 → sqlserver:1433 (Azure SQL Edge, SA_PASSWORD=hardcoded)

Volumes:
    - ~/.microsoft/usersecrets (for dev secrets)
    - ~/.aspnet/https (for dev HTTPS certs)

Networks: implicit compose default
```

### Environment Matrix

| Environment | Database | Secrets | Auth Key | Retry | Health |
|-------------|----------|---------|---------|-------|--------|
| Development | EF InMemory (test) or Docker SQL | User Secrets | **Hardcoded** | ❌ | /health |
| Docker | Docker sqlserver container | docker-compose.yml env vars | **Hardcoded** | ❌ | /health |
| Production | Azure SQL (Key Vault conn string) | Azure Key Vault | **Hardcoded (TD-01)** | ✅ Web only | /health |

---

## 3. CI/CD Pipeline Blueprint

### Current State

```
GitHub Repository
    │
    ├── .github/workflows/dotnetcore.yml  [ALL branches — push/PR]
    │       Steps:
    │       1. actions/checkout@v2  ← OUTDATED (current: v4)
    │       2. actions/setup-dotnet@v1  ← OUTDATED (current: v4)
    │       3. dotnet build ./eShopOnWeb.sln --configuration Release
    │       4. dotnet test ./eShopOnWeb.sln --configuration Release
    │
    ├── .github/workflows/richnav.yml  [workflow_dispatch only]
    │       Steps:
    │       1. dotnet build /bl (binary log)
    │       2. microsoft/RichCodeNavIndexer@v0.1
    │
    └── .github/dependabot.yml
            Schedule: daily
            Ecosystem: nuget
            Raises: version-update PRs (non-blocking)
```

### CI/CD Gap Assessment

| Gap | Severity |
|-----|---------|
| No SAST / static security analysis | HIGH |
| No secret / credential scanning in pipeline | HIGH |
| No automated deployment step | HIGH |
| No post-deploy smoke test or health check | HIGH |
| No container image scanning | MEDIUM |
| No code coverage gate | MEDIUM |
| CI actions pinned to deprecated v1/v2 | MEDIUM |
| No integration tests against real SQL Server | MEDIUM |

### Target CI/CD Pipeline (Recommended)

```
Stage 1: Quality Gates
    ├── actions/checkout@v4
    ├── actions/setup-dotnet@v4
    ├── dotnet build --configuration Release
    ├── dotnet test --collect:"XPlat Code Coverage" (min 70% gate)
    ├── gitleaks/trufflehog (secret scan — catches TD-01 immediately)
    └── dotnet list package --vulnerable (dependency scan)

Stage 2: Security Scan
    ├── CodeQL analysis (SAST)
    └── trivy (container image scan on Dockerfile build)

Stage 3: Deploy (main branch only)
    ├── azd deploy (Web service to Azure)
    └── Health check: curl /health after deploy

Stage 4: PublicApi Deploy (after OQ-006 resolved)
    └── az webapp deploy (PublicApi App Service)
```

---

## 4. Version Compatibility Assessment

| Component | Current | Current Status | Action |
|-----------|---------|---------------|--------|
| .NET SDK | 8.0.x | LTS to Nov 2026 | ✅ No action |
| Bootstrap | 3.4.1 | EOL July 2019 | 🔴 Upgrade to Bootstrap 5.3 |
| actions/checkout | v2 | Deprecated (Node.js 16 EOL) | 🟡 Upgrade to v4 |
| actions/setup-dotnet | v1 | Deprecated | 🟡 Upgrade to v4 |
| dotnet-xunit | 2.3.1 | Deprecated DotNetCliToolReference | 🟡 Remove; use xunit.runner.console |
| Microsoft.AspNetCore.Mvc | 2.2.0 | EOL + vestigial in central props | 🟡 Remove from Directory.Packages.props |
| aspnet-signalr | 1.0.27 | Dead/unused | 🟡 Remove from libman.json |
| Azure SQL Edge (Docker) | no tag | Unpinned latest | 🟡 Pin to specific tag |

---

## 5. Technology Decisions (Confirmed from Source)

| Decision | Choice | Rationale (from code) |
|----------|--------|----------------------|
| Architecture style | Clean Architecture (DDD-Lite) | IAggregateRoot, IRepository\<T\>, Ardalis.Specification |
| Query objects | Ardalis.Specification | 8 specification classes; EfRepository<T> via RepositoryBase<T> |
| Key generation | HiLo (CatalogItem), Identity (others) | CatalogItemConfiguration.cs UseHiLo("catalog_hilo") |
| Token signing | HMAC-SHA256 | IdentityTokenClaimService.cs — HS256 algorithm |
| Cookie auth | SameSite=Lax, HttpOnly, SecurePolicy=Always | ConfigureCookieSettings.cs |
| WASM hosting | Blazor hosted in ASP.NET Core (not standalone) | BlazorAdmin is a RazorClassLibrary inside Web |
| API documentation | Swashbuckle/Swagger | PublicApi only; Bearer security definition added |
| Client-side cache | Blazored.LocalStorage | BlazorAdmin; 60s TTL; immediate invalidation on write |
| Server-side cache | IMemoryCache | Web catalog view model service; 30s sliding |
| Error handling | Middleware (PublicApi) + UseExceptionHandler (Web) | ExceptionMiddleware for DuplicateException → 409 |
