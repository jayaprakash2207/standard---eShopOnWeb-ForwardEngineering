# TA Review Summary - eShopOnWeb

## Agent 2 - Analysis Summary

- **Layers analysed**: 6 - Application/Technology Stack, Security, Data, Component Interaction,
  CI/CD & Deployment, Operational (Observability/Deployment Safety/DR)
- **Technologies assessed**: ~38 (full breakdown in `technology-stack-assessment.md`)
- **Architecture patterns catalogued**: 19 (AP-01 through AP-19)
- **NFR entries recorded**: 28 (NFR-01 through NFR-28)
- **Technical debt items identified**: 22 (TD-01 through TD-22) - Critical: 3, High: 6, Medium: 8,
  Low: 5
- **CI/CD pipeline files directly read**: 3 (`.github/workflows/dotnetcore.yml`,
  `.github/workflows/richnav.yml`, `.github/dependabot.yml`); 0 reusable workflow files
  referenced
- **CI/CD capabilities confirmed present**: 2 of 14 (Build, Unit Tests) fully present; 1 of 14
  (Integration Tests) Partial; 11 of 14 Absent
- **Agent 1 LOW CONFIDENCE items resolved**: 1 of several (the Postgres vs SQL Server data-store
  conflict - see Discrepancy Log)
- **Discrepancies with Agent 1**: 2

---

## Evidence Scope Caveat (applies to all 9 output files)

This pass had access to: Agent 1's 6 inventory files, solution files (`Everything.sln`,
`eShopOnWeb.sln`), `docker-compose.yml`/`docker-compose.override.yml`, both Dockerfiles, all 6
src-project `.csproj` files, all reviewed `appsettings*.json` files (Web x3, PublicApi x3,
BlazorAdmin x3), `infra/main.parameters.json`, `infra/abbreviations.json`,
`.github/workflows/dotnetcore.yml`, `.github/workflows/richnav.yml`, `.github/dependabot.yml`,
and all 4 test-project `.csproj` files.

**No `.cs` application source files were provided** (no `Program.cs`, controllers, endpoint
classes, specification classes, `DbContext`, mapping profiles, or Razor components). As a
result:
- Architecture Pattern Catalog entries are predominantly Priority 5 evidence (library presence in
  manifest) rather than Priority 1-3 (annotations/code), and are marked LOW/ASSUMED accordingly.
- Several security-critical configuration questions (JWT issuer/audience, CORS policy, Identity
  cookie security options, BlazorAdmin OIDC authority) could not be resolved and are carried to
  the Validation Queue below as **High-priority follow-up items for a source-code pass**.

---

## Validation Queue

| # | Item | Layer | Reason for Uncertainty |
|---|---|---|---|
| 1 | JWT Bearer configuration (issuer/audience/signing key) for Web and PublicApi | Security | Packages referenced (`Microsoft.AspNetCore.Authentication.JwtBearer`, `System.IdentityModel.Tokens.Jwt`) but no configuration found in any of 6 appsettings files; cannot confirm whether PublicApi endpoints are actually token-protected (TD-08) |
| 2 | CORS policy for PublicApi/Web | Security | BlazorAdmin's `baseUrls` config implies cross-origin calls in every environment, but no CORS configuration found in any appsettings file - likely configured in `Program.cs` (TD-09) |
| 3 | ASP.NET Core Identity cookie security options (SecurePolicy, SameSite, lockout, 2FA) | Security | Cannot confirm from appsettings alone; Docker environment binds plain HTTP (`http://+:8080`), raising the stakes of this unknown |
| 4 | BlazorAdmin WASM authentication provider/authority | Security / Application | `Microsoft.AspNetCore.Components.WebAssembly.Authentication` + `Microsoft.Extensions.Identity.Core` referenced, but no OIDC authority/client ID in any of BlazorAdmin's 3 appsettings files (AP-12) |
| 5 | Azure Key Vault resource and vault name | Infrastructure / Security | `infra/main.parameters.json` references `${AZURE_KEY_VAULT_NAME}`; `Azure.Extensions.AspNetCore.Configuration.Secrets`/`Azure.Identity` referenced in Web; no `main.bicep`/resource template and no vault name in any Web appsettings (TD-16) |
| 6 | EF Core migration strategy (Postgres + SQL Server) | Data | `Data\Migrations\` folder declared in Infrastructure.csproj but empty - cannot confirm whether schema is created via `EnsureCreated()`, an out-of-tree migration process, or is simply unmanaged (TD-18) |
| 7 | `Microsoft.EntityFrameworkCore.InMemory` usage switch in Web/PublicApi | Data / Application | Referenced in both production projects; cannot confirm the conditions under which the InMemory provider is selected at runtime without `Program.cs` (TD-11) |
| 8 | All `Ardalis.*`, `Microsoft.AspNetCore.*` etc. resolved package versions | Application | `Directory.Packages.props` (central package management file, referenced by `eShopOnWeb.sln`'s Solution Items) was not provided - every "not declared" version in the Technology Stack Assessment remains LOW - VERSION UNKNOWN until this file is reviewed |
| 9 | `BlazorInputFile` active usage | Application | Possible legacy dependency superseded by framework-native `InputFile`; no Razor component source provided to confirm (Architecture Pattern Catalog, Declared-But-Unused) |
| 10 | Whether deployment to Azure is performed out-of-band (manual `azd up`) or is simply not yet implemented | CI-CD / Infrastructure | No CD workflow exists despite `infra/` parameters being present (TD-07) |

---

## Agent 1 Discrepancy Log

| # | Agent 1 Finding | What Deep Analysis Showed | Status |
|---|---|---|---|
| 1 | Data Store Registry: flagged a "VERSION / TECHNOLOGY CONFLICT" - default appsettings declare Postgres connection strings while `appsettings.Docker.json` declares SQL Server connection strings for the same keys (`CatalogConnection`, `IdentityConnection`), and asked Agent 2 to determine which engine is authoritative per environment | **RESOLVED** - this is the environment-switched dual-provider pattern AP-08. Postgres (`Npgsql.EntityFrameworkCore.PostgreSQL`) is authoritative for the default/local environment (`appsettings.json`, both Web and PublicApi); SQL Server (`Microsoft.EntityFrameworkCore.SqlServer`, against the `sqlserver`/Azure SQL Edge compose service) is authoritative when `ASPNETCORE_ENVIRONMENT=Docker`. Whether this dual-provider setup is *intentional design* vs *unmanaged drift* remains open (TD-04, Validation Queue item 6) | Partially resolved - mechanism confirmed, intent unconfirmed |
| 2 | Infrastructure & Deployment Blueprint: marked `mcr.microsoft.com/azure-sql-edge` (no tag declared) as LOW confidence solely due to the missing version tag, defaulting to `latest` | **DISCREPANCY/ESCALATION** - the missing tag is a secondary concern; the primary issue is that Azure SQL Edge has been **retired by Microsoft** (end of support 2025-09-30). As of the current analysis date (2026-06-15), this component is past its supported lifecycle regardless of which tag resolves. Severity raised from Agent 1's "LOW - no tag declared" to **Critical - EOL technology** (TD-03) | Escalated, not resolved - requires migration off Azure SQL Edge |

---

## Highest-Priority Action Items (Top 3)

1. **TD-01 / TD-02 (Critical)** - Remove hardcoded PostgreSQL and SQL Server `sa` credentials from
   source control (`appsettings.json`, `appsettings.Docker.json`, `docker-compose.yml`); rotate
   both passwords immediately, as they are currently visible to anyone with repository access.
2. **TD-03 (Critical)** - Replace `mcr.microsoft.com/azure-sql-edge` (retired product, no tag
   pinned) with a supported, version-pinned database container image before the `latest` tag
   becomes unresolvable.
3. **TD-06 (High)** - Add secret scanning and dependency vulnerability scanning to
   `.github/workflows/dotnetcore.yml`; the current pipeline would not have caught TD-01/TD-02 and
   provides no automated signal on vulnerable NuGet packages beyond Dependabot's update cadence.

---

## Output File Index

| # | File | Contents |
|---|---|---|
| 1 | `technology-stack-assessment.md` | Full technology table with usage depth, EOL status, Agent 1 cross-reference |
| 2 | `architecture-pattern-catalog.md` | AP-01 - AP-19, Pattern Coverage Gaps, Declared-But-Unused Libraries |
| 3 | `component-interaction-contract-map.md` | Interaction table, Coupling Hotspots, API Contract Inventory |
| 4 | `data-architecture-assessment.md` | Data Store Deep Dive, Data Ownership Map, Data Flow & Consistency Notes |
| 5 | `security-architecture-assessment.md` | Auth/Authz implementation, Secrets Posture, Attack Surface Summary |
| 6 | `nfr-registry.md` | NFR-01 - NFR-28, plus "no declared values" category summary |
| 7 | `technical-debt-risk-register.md` | TD-01 - TD-22, sorted by severity, with severity summary |
| 8 | `operational-architecture-assessment.md` | Evidence-based CI/CD Maturity, Observability Coverage, Deployment Safety, DR Posture |
| 9 | `ta-review-summary.md` | This file - summary, Validation Queue, Discrepancy Log, priority actions |

---

Agent 2 Analysis Complete.
Documentation is ready for technical review.
Highest-priority action item: **TD-01/TD-02 - hardcoded database credentials committed to source
control (Critical, Security Vulnerability)**.
