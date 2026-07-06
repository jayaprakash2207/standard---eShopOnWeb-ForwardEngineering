=== DOCUMENT: 14_NFR_SPECIFICATION.md ===

# Non-Functional Requirements Specification — eShopOnWeb

---

## 1. Performance

| ID | Requirement | Target | Current State | Gap? |
|----|-------------|--------|--------------|------|
| NFR-PERF-01 | Catalog list API response time (P95) | < 200ms | +1,000ms artificial delay (TD-07) | **CRITICAL — remove Task.Delay(1000)** |
| NFR-PERF-02 | Order creation end-to-end latency | < 500ms | Not measured; no instrumentation | Unknown |
| NFR-PERF-03 | Basket add-item latency | < 100ms | Not measured | Unknown |
| NFR-PERF-04 | Server-side catalog cache hit ratio | > 80% (estimated) | 30s sliding IMemoryCache | Satisfied |
| NFR-PERF-05 | Client-side catalog cache (BlazorAdmin) | 1-minute TTL | Blazored.LocalStorage 60s | Satisfied |
| NFR-PERF-06 | Health check endpoint response time | < 5s | Content-based HTTP check; no timeout declared | Gap — non-pooled HttpClient risk |

---

## 2. Availability

| ID | Requirement | Target | Current State | Gap? |
|----|-------------|--------|--------------|------|
| NFR-AVAIL-01 | Web application uptime | 99.5% (Azure App Service B1 SLA) | B1 SKU has no SLA guarantee | Gap — B1 has no uptime SLA |
| NFR-AVAIL-02 | SQL Server availability | 99.99% (Azure SQL Basic SLA) | Provisioned via Azure SQL | OK |
| NFR-AVAIL-03 | SQL retry on transient failure | Max 6 retries, 30s max delay | EnableRetryOnFailure() — Web production only | Gap — missing in PublicApi and dev/Docker |
| NFR-AVAIL-04 | Application auto-restart on crash | Yes | Azure App Service auto-restart | OK |
| NFR-AVAIL-05 | Token validity period | 7 days | NFR-03 confirmed | Satisfied |
| NFR-AVAIL-06 | Cookie session validity | 60 minutes | NFR-04 confirmed | Satisfied |

---

## 3. Scalability

| ID | Requirement | Target | Current State | Gap? |
|----|-------------|--------|--------------|------|
| NFR-SCALE-01 | Horizontal scaling | Stateless web tier | IMemoryCache revocation is in-process — NOT shareable across instances | Gap — revocation cache breaks on scale-out |
| NFR-SCALE-02 | Database connection pool | Max 100 connections (SQL Server default) | No MaxPoolSize declared | Unknown — defaults apply |
| NFR-SCALE-03 | Rate limiting | Protect /api/authenticate from brute force | No rate limiting middleware found | Gap — brute force risk |
| NFR-SCALE-04 | Request timeouts | HttpClient default 100s | No timeout configured on HttpService or health checks | Gap |

**Scale-out blocker:** The in-process `IMemoryCache` used for cookie token revocation (AP-09) cannot be shared across multiple App Service instances. If the web application is scaled to 2+ instances, a revoked token would still be accepted by instances that haven't seen the revocation. Migration to Azure Cache for Redis or distributed cache is required before horizontal scaling.

---

## 4. Reliability

| ID | Requirement | Target | Current State | Gap? |
|----|-------------|--------|--------------|------|
| NFR-REL-01 | Database startup retry | 10 attempts | CatalogContextSeed retry loop (BR-39) | Satisfied |
| NFR-REL-02 | Basket transfer atomicity | All-or-nothing | 3 separate SaveChanges (DQ-002) | Gap — partial failure creates orphaned data |
| NFR-REL-03 | Order-basket consistency | Basket cleared after order | NOT cleared — BR-26 | By design; operational risk |
| NFR-REL-04 | Graceful shutdown | Drain in-flight requests | No graceful shutdown handler found | Gap |
| NFR-REL-05 | Health check for traffic routing | Liveness + readiness | Content-based /health (Web only) | Partial |

---

## 5. Security

| ID | Requirement | Target | Current State | Gap? |
|----|-------------|--------|--------------|------|
| NFR-SEC-01 | JWT signing key entropy | ≥ 256-bit random key | Hardcoded ASCII string (TD-01) | **CRITICAL BLOCKER** |
| NFR-SEC-02 | JWT token validation | Issuer + audience validated | ValidateIssuer=false, ValidateAudience=false (TD-03) | **CRITICAL BLOCKER** |
| NFR-SEC-03 | Admin account initial password | Environment-specific random | Hardcoded "Pass@word1" (TD-02) | **CRITICAL BLOCKER** |
| NFR-SEC-04 | TLS minimum version | TLS 1.2 | Enforced on App Service + Azure SQL | Satisfied |
| NFR-SEC-05 | HTTPS enforcement | Required | httpsOnly:true on App Service | Satisfied |
| NFR-SEC-06 | Cookie security attributes | HttpOnly, Secure, SameSite | HttpOnly=true, SecurePolicy=Always, SameSite=Lax | Mostly satisfied |
| NFR-SEC-07 | Secret management | Key Vault (production) | Web: Key Vault ✅; PublicApi: ❌ none | Partial |
| NFR-SEC-08 | SQL access restriction | Firewall whitelist | All IPs open (TD-11) | Gap |
| NFR-SEC-09 | JWT token lifetime | ≤ 7 days | 7 days exactly (NFR-03) | Satisfied |
| NFR-SEC-10 | Account lockout on failed login | Yes | lockoutOnFailure=true on API; web login does NOT lock out | Partial |

---

## 6. Maintainability

| ID | Requirement | Target | Current State | Gap? |
|----|-------------|--------|--------------|------|
| NFR-MAINT-01 | Code test coverage | ≥ 70% | Unknown — coverlet not wired in CI | Gap |
| NFR-MAINT-02 | Integration tests against real SQL Server | Required before go-live | All tests use EF InMemory (DA Agent 2) | Gap |
| NFR-MAINT-03 | API version strategy | Semantic versioning | v1 string only; no versioning strategy | Gap |
| NFR-MAINT-04 | Dependency vulnerability scanning | Automated in CI | Dependabot PRs (not blocking gate) | Partial |
| NFR-MAINT-05 | Framework EOL risk | All dependencies supported | Bootstrap 3.4.1 EOL (TD-13) | Gap |

---

## 7. Observability

| ID | Requirement | Target | Current State | Gap? |
|----|-------------|--------|--------------|------|
| NFR-OBS-01 | Structured logging format | JSON with correlation ID | Plain console text; no correlation IDs; IncludeScopes=false | Gap |
| NFR-OBS-02 | Distributed tracing | OpenTelemetry or App Insights SDK | No tracing SDK found in application code | Gap |
| NFR-OBS-03 | Metrics export | Request rate, error rate, latency | No metrics instrumentation found | Gap |
| NFR-OBS-04 | Health check endpoint | Liveness + readiness | /health exists (Web only; content-based) | Partial |
| NFR-OBS-05 | Alerting | On error rate spike or health failure | No alert rules in Bicep | Gap |
| NFR-OBS-06 | Log retention | ≥ 30 days | 1 day / 35MB (App Service HTTP logs) | Gap |

---

## 8. Disaster Recovery

| ID | Requirement | Current State | Gap? |
|----|-------------|--------------|------|
| NFR-DR-01 | RTO (Recovery Time Objective) | **Not defined (OQ-011)** | Gap |
| NFR-DR-02 | RPO (Recovery Point Objective) | **Not defined (OQ-011)** | Gap |
| NFR-DR-03 | Database backup | Azure SQL default (7-day retention for Basic/Standard) | Not explicitly configured in Bicep | Partial |
| NFR-DR-04 | Multi-region failover | Not configured | Single region, single App Service | Gap |
| NFR-DR-05 | Database geo-replication | Not configured | No failover group declared in Bicep | Gap |

---

## 9. Confirmed NFR Values (Exact — from source)

| NFR | Value | Source File | Confidence |
|-----|-------|-------------|------------|
| Server-side catalog cache TTL | 30 seconds (sliding) | Web/Extensions/CacheHelpers.cs:7 | HIGH |
| Client-side catalog cache TTL (BlazorAdmin) | 60 seconds | BlazorAdmin/Services/CachedCatalogItemServiceDecorator.cs:34 | HIGH |
| JWT token lifetime | 7 days | Infrastructure/Identity/IdentityTokenClaimService.cs:38 | HIGH |
| Cookie session validity | 60 minutes | Web/Configuration/ConfigureCookieSettings.cs:10 | HIGH |
| BlazorAdmin auth poll interval | 60 seconds | BlazorAdmin/CustomAuthStateProvider.cs:10 | HIGH |
| Anonymous basket cookie lifetime | 10 years | Web/Pages/Basket/Checkout.cshtml.cs:95 | HIGH |
| Token revocation cache expiry | 60 minutes | Web/Controllers/UserController.cs:52 | HIGH |
| Artificial catalog API delay | 1,000ms (REMOVE) | PublicApi/CatalogItemEndpoints/CatalogItemListPagedEndpoint.cs:42 | HIGH |
| App Service HTTP log retention | 1 day / 35 MB | infra/core/host/appservice.bicep | HIGH |
| App Service TLS minimum | TLS 1.2 | infra/core/host/appservice.bicep | HIGH |
| Azure SQL TLS minimum | TLS 1.2 | infra/core/database/sqlserver/sqlserver.bicep | HIGH |
| App Service SKU | B1 (1 core, 1.75GB RAM) | infra/core/host/appserviceplan.bicep | HIGH |
| EF Core SQL retry (production Web) | Default (max 6, 30s) | Web/Program.cs:36,41 | LOW (defaults assumed) |
| Admin portal items per page | 10 | BlazorAdmin/Pages/CatalogItemPage/List.razor.cs | HIGH |
| Admin toast dismiss delay | 3 seconds | BlazorAdmin/Services/ToastService.cs | HIGH |
