# Security Architecture Assessment

> Built from Agent 1's Security & Configuration Snapshot, cross-checked against all 6 reviewed
> `appsettings*.json` files (Web x3, PublicApi x3), `docker-compose.yml`,
> `docker-compose.override.yml`, and `infra/main.parameters.json`. **Two critical hardcoded-secret
> findings below were directly confirmed during this pass** (see Secrets Posture).

## Authentication & Authorisation Implementation

| Mechanism | Declared (Agent 1) | Implemented How | Validation Completeness | Gaps | Severity |
|---|---|---|---|---|---|
| ASP.NET Core Identity (cookie-based) | HIGH - `IdentityConnection` present in Web/PublicApi | EF Core Identity store (`Microsoft.AspNetCore.Identity.EntityFrameworkCore` + `.UI`) backed by `IdentityConnection`; provider switches Postgres (default) / SQL Server (Docker) per AP-08 | Partial - connection and package evidence is HIGH, but password policy, lockout settings, 2FA configuration, and cookie security options (`SecurePolicy`, `SameSite`, expiry) are configured in `Program.cs`/`Startup.cs`, which was not provided | Cannot confirm whether `RequireConfirmedAccount`, password complexity, or account lockout are enabled; cannot confirm cookie is `SecurePolicy = Always` for the Docker environment which serves over plain HTTP (`ASPNETCORE_URLS=http://+:8080`) | Medium - escalate to High if cookie auth is confirmed to run over HTTP in any reachable environment |
| JWT Bearer Authentication | LOW (Agent 1) - inferred from package references only | **Unresolved** - `Microsoft.AspNetCore.Authentication.JwtBearer` and `System.IdentityModel.Tokens.Jwt` are referenced in Web, PublicApi, and Infrastructure, but none of the 6 appsettings files reviewed contain an `Authentication`, `Jwt`, `Authority`, `Audience`, `Issuer`, or signing-key configuration block | Minimal - no configuration evidence at all | If PublicApi endpoints are intended to be protected by JWT bearer tokens (plausible, since it is the "public API" with Swagger UI), the **authorization may not actually be enforced**, or the configuration lives in user-secrets/environment variables not in scope. Either way this is currently unverifiable and represents a documentation/configuration gap on a security-critical control | **High** - an API described as "public" with no confirmed authentication enforcement is a high-severity unknown until resolved |
| Blazor WebAssembly Authentication | LOW (Agent 1) - inferred from package references only | **Unresolved** - `Microsoft.AspNetCore.Components.WebAssembly.Authentication`, `Microsoft.Extensions.Identity.Core`, `Microsoft.AspNetCore.Components.Authorization` referenced in BlazorAdmin; no OIDC authority/client ID found in any of BlazorAdmin's 3 `wwwroot/appsettings*.json` files | Minimal - no configuration evidence | Cannot confirm how (or whether) BlazorAdmin authenticates its calls to PublicApi/Web; if BlazorAdmin calls PublicApi unauthenticated, combined with the JWT gap above this could mean the admin UI's backing API has no enforced authorization | High - admin-facing UI with unconfirmed auth wiring to its backing API |
| Authorization Components (role/claims-based) | LOW (Agent 1) - package reference only | Same as above - `Microsoft.AspNetCore.Components.Authorization` provides `AuthorizeView`/`CascadingAuthenticationState` primitives only; no role/policy definitions visible | Minimal | Cannot confirm role-to-page mapping for BlazorAdmin (e.g., is catalog editing restricted to an "Administrator" role?) | Medium |

---

## Secrets Posture

| Item | Finding | Severity | Evidence |
|---|---|---|---|
| PostgreSQL credentials (default/local environment) | **Hardcoded plaintext credentials committed to source control**: `Username=postgres;Password=Clarium123` for BOTH `CatalogConnection` and `IdentityConnection`, duplicated identically across Web and PublicApi | **Critical** | src/Web/appsettings.json, src/PublicApi/appsettings.json |
| SQL Server / Azure SQL Edge SA password | **Hardcoded plaintext password committed to source control**: `SA_PASSWORD=@someThingComplicated1234` set as a container environment variable in `docker-compose.yml`, and the same literal password is repeated inside `CatalogConnection`/`IdentityConnection` strings in `appsettings.Docker.json` for both Web and PublicApi | **Critical** | docker-compose.yml; src/Web/appsettings.Docker.json; src/PublicApi/appsettings.Docker.json |
| .NET User Secrets (local dev) | Correctly used for local secret overrides - `UserSecretsId` present for both Web (`aspnet-Web2-1FA3F72E-E7E3-4360-9E49-1CCCD7FE85F7`) and PublicApi (`5b662463-1efd-4bae-bde4-befe0be3e8ff`) | Informational (good practice) - **but does not mitigate the two Critical findings above**, since the committed `appsettings*.json` files contain working default credentials that do not require user-secrets to function | src/Web/Web.csproj, src/PublicApi/PublicApi.csproj |
| Docker-mounted host secrets (HTTPS dev certs, user-secrets) | Read-only bind mounts `~/.aspnet/https:/root/.aspnet/https:ro` and `~/.microsoft/usersecrets:/root/.microsoft/usersecrets:ro` for both app containers | Informational (good practice for local dev; not a production secret-delivery mechanism) | docker-compose.override.yml |
| Azure Key Vault (deployment-time) | `infra/main.parameters.json` references `${AZURE_KEY_VAULT_NAME}` via `secretOrRandomPassword()` for `sqlAdminPassword` and `appUserPassword` - but **no Key Vault resource declaration** (`main.bicep` or equivalent) was found in the provided files, and no vault name/URI appears in any application `appsettings*.json` | Medium | infra/main.parameters.json (no corroborating resource file or app-level config found) |
| CI/CD secret scanning | No `trufflehog`, `gitleaks`, `detect-secrets`, or similar secret-scanning step found in `.github/workflows/dotnetcore.yml` or `.github/workflows/richnav.yml` - the two Critical hardcoded-credential findings above would not be caught by the current pipeline | **High** | .github/workflows/*.yml (absence confirmed by direct read) |

> **Escalation note**: Per the Agent 2 escalation rules, plaintext secrets committed to source
> control were found. Location only is recorded above (no secret values reproduced beyond what
> Agent 1 already surfaced in its inventory pass, which is treated as already-disclosed
> context). **These two findings (Postgres credentials, SQL Server SA password) should be
> rotated and removed from source control as a priority action** - see TD-01 and TD-02 in the
> Technical Debt & Risk Register.

---

## Attack Surface Summary

| Surface | Exposure | Mitigations Found | Gaps |
|---|---|---|---|
| eshoppublicapi (PublicApi) - public REST API with Swagger UI | Container port 8080 internally, host-mapped to 5200 (Docker); dev endpoint `https://localhost:5099` | ASP.NET Core Identity packages present (auth mechanism exists at the framework level) | - JWT bearer configuration not found (see Authentication table above) - cannot confirm endpoints are actually protected<br>- No rate limiting found<br>- No CORS policy found in any appsettings, yet BlazorAdmin calls this API from a different origin/port in every declared environment (`localhost:44315`/`host.docker.internal:5106` vs `localhost:5099`/`localhost:5200`) - a CORS policy must exist somewhere (likely `Program.cs`) but is unverified<br>- Swagger UI (`Swashbuckle.AspNetCore.SwaggerUI`) exposure in non-Development environments not confirmed - if enabled in Docker/production, exposes full API schema to anyone reaching the container |
| eshopwebmvc (Web) - MVC + Razor + hosted Blazor WASM | Container port 8080 internally, host-mapped to 5106 (Docker); dev endpoint `https://localhost:44315` | ASP.NET Core Identity (cookie auth) packages present | - Cookie security configuration (`SecurePolicy`, HTTPS-only) not confirmed for the Docker environment, which binds `http://+:8080` (plain HTTP) - if cookies are not marked `Secure`/`HttpOnly` with appropriate `SameSite`, session cookies could be exposed in the Docker network path |
| sqlserver (Azure SQL Edge container) | Host port 1433 published directly (`1433:1433` in docker-compose.yml) | `ACCEPT_EULA=Y`/`SA_PASSWORD` env vars only - no network restriction visible in compose | - Direct host exposure of the database port increases attack surface beyond what the application services require; combined with the hardcoded SA password (Critical, above), an attacker reaching the Docker host's network can connect directly to the database with `sa` credentials found in source control |
| CI/CD pipeline (GitHub Actions) | Public/internal GitHub Actions runners (`ubuntu-latest`, `windows-latest`) | Dependabot for NuGet dependency currency (daily) | - No SAST, no dependency vulnerability scan beyond Dependabot's update-PR mechanism (no `dotnet list package --vulnerable` or `snyk`/`govulncheck`-equivalent step), no container image scanning of either Dockerfile, no secret scanning - see Operational Architecture Assessment for full CI/CD maturity table |
| Azure deployment target (`infra/`) | Parameters-only - `infra/main.parameters.json` and `infra/abbreviations.json` present, no resource-defining template (`main.bicep`/ARM) found | N/A | Cannot assess the security posture of the actual Azure deployment target (network isolation, managed identity scope, Key Vault access policies, etc.) because no resource definitions are present in the provided files - this whole surface is **UNKNOWN**, not merely "low risk" |

---

## Summary of Critical/High Security Findings

1. **CRITICAL** - PostgreSQL credentials (`postgres`/`Clarium123`) hardcoded in
   `src/Web/appsettings.json` and `src/PublicApi/appsettings.json` (TD-01)
2. **CRITICAL** - SQL Server/Azure SQL Edge SA password (`@someThingComplicated1234`) hardcoded in
   `docker-compose.yml` and both services' `appsettings.Docker.json` (TD-02)
3. **HIGH** - No confirmed JWT/authentication enforcement configuration for PublicApi despite it
   being the system's public-facing API (AP-10, TD-12)
4. **HIGH** - No CORS policy found despite cross-origin calls from BlazorAdmin to PublicApi/Web
   being required by the declared `baseUrls` configuration in every environment (TD-17)
5. **HIGH** - No secret scanning in CI/CD; the two Critical hardcoded-credential findings above
   would pass the current pipeline undetected (TD-06)
6. **MEDIUM** - SQL Server port 1433 published directly to the host network (TD-18)
7. **MEDIUM** - Azure Key Vault referenced at deployment-parameter level with no corroborating
   vault resource or application-level configuration (TD-13)
