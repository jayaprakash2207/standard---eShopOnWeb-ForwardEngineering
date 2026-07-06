# NFR Registry

> Every distinct numeric or threshold value found across all layers (Application, Data, CI/CD,
> Infrastructure, Security) is listed as its own row, per the "never collapse distinct
> configuration values" rule. Where a category has **no declared values**, this is logged
> explicitly as its own finding, since the absence of configuration means framework defaults
> (often unbounded or unsuitable for production) apply.

## NFR Registry

| ID | NFR Name | Value | Category | Source | Confidence |
|---|---|---|---|---|---|
| NFR-01 | eshopwebmvc (Web) container internal listen address/port | `http://+:8080` (via `ASPNETCORE_URLS`) | Availability | docker-compose.override.yml | HIGH |
| NFR-02 | eshopwebmvc (Web) host-to-container port mapping | `5106:8080` | Availability | docker-compose.override.yml | HIGH |
| NFR-03 | eshoppublicapi (PublicApi) container internal listen address/port | `http://+:8080` (via `ASPNETCORE_URLS`) | Availability | docker-compose.override.yml | HIGH |
| NFR-04 | eshoppublicapi (PublicApi) host-to-container port mapping | `5200:8080` | Availability | docker-compose.override.yml | HIGH |
| NFR-05 | eshoppublicapi (PublicApi) Dockerfile declared exposed ports | `80`, `443` | Availability | src/PublicApi/Dockerfile | HIGH - but **DISCREPANCY** vs NFR-03 (actual runtime binding is 8080, not 80/443) - carried forward from Agent 1 |
| NFR-06 | sqlserver (Azure SQL Edge) host-to-container port mapping | `1433:1433` | Availability | docker-compose.yml | HIGH |
| NFR-07 | Database connection pool size (Catalog/Identity, both Postgres and SQL Server providers, both Web and PublicApi) | **None declared** - Npgsql default `Maximum Pool Size=100`, `Minimum Pool Size=0`; Microsoft.Data.SqlClient default `Max Pool Size=100`, `Min Pool Size=0` apply | Resource Management | Not found in any of the 6 reviewed appsettings files (connection strings contain no `Pooling`/`Maximum Pool Size`/`Minimum Pool Size`/`Min Pool Size`/`Max Pool Size` parameters) | LOW - framework default assumed; ASSUMED category per Decision Rules ("None declared - system using framework defaults; defaults may be unbounded and represent a scalability or reliability risk") |
| NFR-08 | Database connection/command timeout (Catalog/Identity, both providers) | **None declared** - Npgsql default command timeout 30s / connection timeout 15s; SqlClient default connection timeout 15s apply | Latency | Not found in any reviewed connection string (no `Timeout`/`Command Timeout`/`Connect Timeout` parameter) | LOW - framework default assumed |
| NFR-09 | Web - default (non-environment-specific) logging minimum level | `Default: Warning` | Data Freshness (Observability) | src/Web/appsettings.json (`Logging.LogLevel.Default`) | HIGH |
| NFR-10 | Web - Development logging minimum level | `Default: Debug`, `System: Information`, `Microsoft: Information` | Data Freshness (Observability) | src/Web/appsettings.Development.json | HIGH |
| NFR-11 | Web - Docker logging minimum level | `Default: Debug`, `System: Information`, `Microsoft: Information` (identical to Development) | Data Freshness (Observability) | src/Web/appsettings.Docker.json | HIGH |
| NFR-12 | PublicApi - default (non-environment-specific) logging minimum level | `Default: Warning`, `Microsoft: Warning`, `System: Warning` | Data Freshness (Observability) | src/PublicApi/appsettings.json (`Logging.LogLevel`) | HIGH |
| NFR-13 | PublicApi - Development/Docker logging minimum level | `Default: Information`, `Microsoft: Warning`, `Microsoft.Hosting.Lifetime: Information` (identical in both files) | Data Freshness (Observability) | src/PublicApi/appsettings.Development.json, src/PublicApi/appsettings.Docker.json | HIGH |
| NFR-14 | Web - `AllowedHosts` configuration | `*` (wildcard - all hosts allowed) | Availability / Security boundary | src/Web/appsettings.json (`AllowedHosts`) | HIGH - **note**: wildcard `AllowedHosts` is a permissive default; combined with no CORS policy found (TD-17), this widens the host-header attack surface |
| NFR-15 | PublicApi - `AllowedHosts` configuration | `*` (wildcard - all hosts allowed) | Availability / Security boundary | src/PublicApi/appsettings.json (`AllowedHosts`) | HIGH |
| NFR-16 | BlazorAdmin (Development) - API base URL target | `https://localhost:5099/api/` | Availability (service discovery) | src/BlazorAdmin/wwwroot/appsettings.Development.json, appsettings.json | HIGH |
| NFR-17 | BlazorAdmin (Development) - Web base URL target | `https://localhost:44315/` | Availability (service discovery) | src/BlazorAdmin/wwwroot/appsettings.Development.json, appsettings.json | HIGH |
| NFR-18 | BlazorAdmin (Docker) - API base URL target | `http://localhost:5200/api/` | Availability (service discovery) | src/BlazorAdmin/wwwroot/appsettings.Docker.json | HIGH |
| NFR-19 | BlazorAdmin (Docker) - Web base URL target | `http://host.docker.internal:5106/` | Availability (service discovery) | src/BlazorAdmin/wwwroot/appsettings.Docker.json | HIGH |
| NFR-20 | Dependency update polling interval (Dependabot, NuGet ecosystem) | `daily` | Data Freshness | .github/dependabot.yml (`schedule.interval`) | HIGH |
| NFR-21 | CI build/test configuration | `Release` (used for both `dotnet build` and `dotnet test`) | Reliability (build fidelity) | .github/workflows/dotnetcore.yml | HIGH |
| NFR-22 | CI .NET SDK version pin | `8.0.x` with `include-prerelease: true` | Reliability (build reproducibility) | .github/workflows/dotnetcore.yml, .github/workflows/richnav.yml | HIGH - **note**: `include-prerelease: true` on a `.x` floating version means the exact SDK patch/preview build used by CI is not pinned and can change between runs (see TD-09) |
| NFR-23 | HTTP retry/circuit breaker policy for inter-service or DB calls | **None declared** anywhere in the codebase | Reliability | Not found in any `.csproj` (no Polly/`Microsoft.Extensions.Http.Resilience` package) or appsettings | LOW - "None declared - system is using framework defaults; defaults may be unbounded and represent a scalability or reliability risk" (no retry = zero resilience to transient faults, which is itself the finding) |
| NFR-24 | Rate limiting (requests-per-period) for PublicApi | **None declared** | Rate | Not found in `PublicApi.csproj` (no `Microsoft.AspNetCore.RateLimiting` usage evidence) or appsettings | LOW - "None declared" |
| NFR-25 | Cache TTL / eviction policy (catalog data or otherwise) | **None declared** | Data Freshness | No caching package (Redis client, `IMemoryCache` config, `IDistributedCache` config) found in any `.csproj` or appsettings, despite `infra/abbreviations.json` listing a `cacheRedis: "redis-"` naming convention | LOW - "None declared"; the `redis-` convention entry in abbreviations.json appears to be an unused boilerplate reference (every Azure resource-type abbreviation in that file is unused per Agent 1) |
| NFR-26 | Container health check interval/timeout/retries (Docker `HEALTHCHECK`) | **None declared** | Availability | Not found in src/Web/Dockerfile or src/PublicApi/Dockerfile (no `HEALTHCHECK` instruction) | LOW - "None declared" |
| NFR-27 | `docker-compose` resource limits (CPU/memory) per service | **None declared** | Resource Management | Not found in docker-compose.yml or docker-compose.override.yml (no `deploy.resources.limits`) | LOW - "None declared" |
| NFR-28 | `docker-compose` service start-order dependency gating | `depends_on: sqlserver` (Web, PublicApi) - **order only, no health condition** | Availability | docker-compose.yml | HIGH - presence confirmed; absence of `condition: service_healthy` is itself the finding (no readiness gating value to record) |

---

### NFR Categories With No Declared Values - Summary

The following categories had **zero declared configuration values** across all reviewed files.
Per the Decision Rules, this is logged as a finding in its own right - these represent either
undocumented reliance on framework defaults or genuine architectural gaps:

- **Reliability**: No retry counts, backoff multipliers, or circuit-breaker thresholds anywhere
  (NFR-23).
- **Rate**: No rate-limiting configuration for the public API (NFR-24).
- **Data Freshness (caching)**: No cache TTL/eviction policy for any data (NFR-25).
- **Resource Management (compute)**: No container CPU/memory limits (NFR-27).
- **Availability (health probing)**: No container health checks, no readiness/liveness probe
  configuration (NFR-26, NFR-28).
- **Throughput (application-level)**: No max request body/upload size, no thread-pool sizing, no
  Kestrel limits (`MaxConcurrentConnections`, `MaxRequestBodySize`) found in any appsettings file.
