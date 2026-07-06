# Operational Architecture Assessment

> CI/CD maturity below is **evidence-based only** per the v2 rules: every "Present" row cites a
> specific tool/action invocation, file, and job. Pipeline files directly read in full this pass:
> `.github/workflows/dotnetcore.yml`, `.github/workflows/richnav.yml`, `.github/dependabot.yml`.
> No `.circleci/`, `bitbucket-pipelines.yml`, `azure-pipelines.yml`, or `Jenkinsfile` were found in
> the provided file set. No local `uses:` references to reusable workflow files exist in either
> workflow (both jobs use only marketplace actions: `actions/checkout`, `actions/setup-dotnet`,
> `microsoft/RichCodeNavIndexer`).

## CI/CD Pipeline Maturity

| Capability | Present? | Evidence (tool / action name + file + job) | Runs On | Gap Severity |
|---|---|---|---|---|
| Build | Present | `dotnet build ./eShopOnWeb.sln --configuration Release` - .github/workflows/dotnetcore.yml, `build` job, step 3 | All branches (`on: [push, pull_request, workflow_dispatch]`) | - |
| Unit Tests | Present | `dotnet test ./eShopOnWeb.sln --configuration Release` - .github/workflows/dotnetcore.yml, `build` job, step 4 | All branches | - |
| Integration Tests | Partial | Same `dotnet test ./eShopOnWeb.sln` command implicitly includes `tests/IntegrationTests`, `tests/FunctionalTests`, and `tests/PublicApiIntegrationTests` (all are part of the solution), but there is no dedicated job/step, no `ASPNETCORE_ENVIRONMENT=Docker` setup, and no `docker-compose up` step to provide a real database for integration scenarios - tests presumably rely on the InMemory provider | All branches, but coverage of "real" integration scenarios (Postgres/SQL Server) is unverified | Medium |
| Code Coverage Gate | Absent | `coverlet.collector` is referenced in tests/PublicApiIntegrationTests/PublicApiIntegrationTests.csproj, but no `--collect:"XPlat Code Coverage"`, `--collect "Code Coverage"`, or coverage-report-publishing step found in dotnetcore.yml | - | Low |
| SAST (Static Security) | Absent | No `sonar`, `sonarcloud`, `sonarqube`, `semgrep`, `codeql`, `snyk code`, or analyzer-gate step found in either workflow file | - | High |
| Dependency Scan | Absent | No `snyk test`, `npm audit`, `dotnet list package --vulnerable`, `owasp dependency-check`, or `govulncheck`-equivalent step found. **Dependabot is configured** (.github/dependabot.yml, `package-ecosystem: nuget`, daily) but this is an out-of-band PR-creation mechanism, not an in-pipeline scan/gate | Dependabot: repo-wide, daily (outside CI runs) | High |
| Container / Image Scan | Absent | No `trivy image`, `snyk container`, `grype`, `docker scout`, or `dockle` step found, despite both `src/Web/Dockerfile` and `src/PublicApi/Dockerfile` existing and being buildable via docker-compose | - | High |
| Secret / Credential Scan | Absent | No `trufflehog`, `gitleaks`, `detect-secrets`, `git-secrets`, or `ggshield` step found in either workflow file. **This directly correlates with TD-01/TD-02** - the two hardcoded-credential findings would not be caught | - | High |
| Lint / Code Quality | Absent | No `dotnet format --verify-no-changes`, `eslint`, or equivalent step found | - | Medium |
| Infrastructure Scan (IaC) | Absent | No `tfsec`, `checkov`, `terrascan`, or `trivy config` step found, despite `infra/main.parameters.json` existing | - | Low (infra is parameters-only, no resource templates to scan yet) |
| Automated Deploy | Absent | No `azd deploy`, `az webapp deploy`, `kubectl apply`, `helm upgrade`, `terraform apply`, or similar deploy step found in either workflow file | - | High |
| Smoke / Health Check Post-Deploy | Absent | No `curl`/`wget` against a health endpoint, no `k6`/`artillery`/`newman` post-deploy step found (consistent with Automated Deploy being Absent) | - | High |
| Auto Rollback | Absent | No `kubectl rollout undo`, `helm rollback`, deployment-slot-swap-rollback, or `--rollback-on-failure` found (consistent with Automated Deploy being Absent) | - | High |
| Manual Approval Gate | Absent | No `environment:` block with required reviewers found in either workflow job | - | Low |
| Release / Versioning Automation | Absent | No `semantic-release`, `standard-version`, `git tag`, `gh release create`, or `dotnet-gitversion` step found in either workflow file | - | Low |

**Additional capability identified (not in the standard 14-item table):**

| Capability | Present? | Evidence | Runs On | Note |
|---|---|---|---|---|
| Code Navigation Indexing | Present | `microsoft/RichCodeNavIndexer@v0.1` - .github/workflows/richnav.yml, `build` job, after `dotnet build ./Everything.sln --configuration Release /bl` | Manual (`workflow_dispatch` only), `windows-latest` | Developer-experience tooling (code search/navigation index), not a build-quality or security gate; included here for completeness since it is a distinct, directly-evidenced pipeline capability |

**Pipeline files directly read this pass:** `.github/workflows/dotnetcore.yml`,
`.github/workflows/richnav.yml`, `.github/dependabot.yml`.

**Additional tools found vs Agent 1's CI/CD inventory:**
- `include-prerelease: true` flag on `actions/setup-dotnet` in both workflows (TD-13) - not
  itemised as a distinct tool by Agent 1, but materially affects build reproducibility.
- `/bl` (MSBuild binary log) flag on the `dotnet build ./Everything.sln` step in richnav.yml -
  diagnostic artifact generation, consumed by the RichCodeNavIndexer action.

---

## Observability Coverage

| Concern | Component | Present? | Tool / Library | Gap? |
|---|---|---|---|---|
| Structured Logging | Web | Partial | Default ASP.NET Core `ILogger` with `Logging.LogLevel` configuration in appsettings (NFR-09 through NFR-11); no `Serilog`, `NLog`, or `Microsoft.Extensions.Logging.ApplicationInsights` package found in Web.csproj | GAP - logs are framework-default console/debug sinks, not structured JSON or shipped to a log aggregator |
| Structured Logging | PublicApi | Partial | Same as Web - `Logging.LogLevel` configuration present (NFR-12, NFR-13); no structured-logging package found in PublicApi.csproj | GAP |
| Structured Logging | BlazorAdmin | Partial | `Microsoft.Extensions.Logging.Configuration` referenced, `Logging.LogLevel` configured in `wwwroot/appsettings*.json` - this is browser-console logging only | GAP - no client-side telemetry shipping (e.g. Application Insights JS SDK) found |
| Distributed Tracing | Web, PublicApi, BlazorAdmin | Absent | No `OpenTelemetry`, `Microsoft.ApplicationInsights`, `Jaeger`, or `Zipkin` package found in any `.csproj` | GAP - given BlazorAdmin -> PublicApi/Web are separate HTTP hops with no correlation mechanism, diagnosing cross-service issues has no tracing support |
| Metrics Export | Web, PublicApi | Absent | No `prometheus-net`, `App.Metrics`, or `Microsoft.Extensions.Diagnostics.Metrics`-based exporter package found | GAP |
| Correlation ID Propagation | Web, PublicApi, BlazorAdmin | Absent | No custom correlation-id middleware or `Microsoft.AspNetCore.HeaderPropagation` package found | GAP - compounds the Distributed Tracing gap above |
| Health / Readiness Endpoints | Web, PublicApi | Absent | No `Microsoft.Extensions.Diagnostics.HealthChecks`-family package found in either `.csproj`; no `/health`-style route evidence | GAP - blocks both container health checks (TD-14) and any future orchestrator readiness/liveness probes |
| Alerting Rules | (platform-wide) | Absent | No monitoring IaC (Alertmanager rules, Azure Monitor alert definitions, CloudWatch alarms) found - `infra/` contains only `main.parameters.json` and `abbreviations.json` | GAP |

---

## Deployment Safety

| Practice | Present? | Evidence | Risk If Absent |
|---|---|---|---|
| Graceful Shutdown | No | No explicit `IHostApplicationLifetime`/`ApplicationStopping` handling evidence; no `Program.cs` provided to confirm either way - marked No based on absence of any related package or config | In-flight requests may be dropped during container restarts/redeploys |
| Readiness Probe | No | No k8s manifests provided; no Dockerfile `HEALTHCHECK`; no `/health` route evidence (NFR-26) | Traffic could be routed to a container before it is ready to serve (relevant if/when an orchestrator is introduced) |
| Liveness Probe | No | Same as above | Hung containers would not be automatically restarted |
| Blue-Green / Canary | No | No deployment pipeline exists at all (Automated Deploy = Absent above), so no progressive-delivery configuration is possible to find | Every future deploy (once one exists) would expose 100% of traffic immediately with no rollback window |
| Feature Flags | No | No feature-flag SDK/package (`Microsoft.FeatureManagement`, LaunchDarkly, etc.) found in any `.csproj` | No ability to decouple code deployment from feature release |

---

## Disaster Recovery Posture

| Item | Declared? | Detail | Source |
|---|---|---|---|
| Database backup configuration | No | Not declared anywhere - `docker-compose.yml`'s `sqlserver` service has no volume for persistent data and no backup script/cron; `infra/` has no resource template defining backup policy | NOT FOUND (docker-compose.yml; infra/main.parameters.json) |
| Multi-region / multi-AZ config | No | `infra/main.parameters.json` declares a single `location` parameter (`${AZURE_LOCATION}`) with no secondary-region parameter; no resource template to confirm topology | NOT FOUND |
| Database replication | No | No replica connection strings, no read-replica configuration, single `sqlserver` compose service with no replica | NOT FOUND (docker-compose.yml; all appsettings) |
| RTO / RPO declarations | No | No documentation, IaC comments, or configuration values found relating to recovery time/point objectives | NOT FOUND |

> **Note on `docker-compose.yml` data persistence**: the `sqlserver` service declares no named
> volume, meaning database data is stored in the container's writable layer and is lost on
> `docker-compose down` (or container recreation). For a local/Docker-based development
> environment this is typically acceptable, but it underscores that this compose file is not a
> production deployment topology - the production data path is presumably the (currently
> undefined) Azure resources referenced by `infra/main.parameters.json`.
