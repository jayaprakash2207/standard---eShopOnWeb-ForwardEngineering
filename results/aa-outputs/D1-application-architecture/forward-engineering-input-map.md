# Forward Engineering Input Map — eShopOnWeb

## Purpose

This document maps extracted architecture facts to forward-engineering decisions. It is consumed by the forward-engineering phase to generate target architecture designs, migration plans, and modernization recommendations. All facts come from the Layer 1 source extraction — no invention.

---

## Section 1: Confirmed Architecture Facts (High Confidence ≥ 0.90)

| Fact ID | Fact | Source | Confidence |
|---|---|---|---|
| FA-001 | Framework: .NET 8, ASP.NET Core, Entity Framework Core, Blazor WASM | azure.yaml, docker-compose.yml, Program.cs files | 0.99 |
| FA-002 | Architecture pattern: Clean Architecture (Dependency Inversion, layered) | ApplicationCore has no infra deps; Infrastructure implements ApplicationCore interfaces | 0.97 |
| FA-003 | Database: SQL Server, two connection strings — CatalogConnection, IdentityConnection | appsettings.json (Web, PublicApi) | 0.99 |
| FA-004 | Two separate DbContexts — CatalogContext (domain data), AppIdentityDbContext (identity) | CatalogContext.cs, AppIdentityDbContext.cs | 0.99 |
| FA-005 | CatalogContext spans 3 bounded contexts (Catalog, Basket, Order) in one DbContext | CatalogContext: 7 DbSets | 0.97 |
| FA-006 | Basket and Order data are stored in SQL Server (same DB as Catalog via CatalogConnection) | CatalogContext DbSets | 0.95 |
| FA-007 | JWT authentication used by PublicApi; 7-day token expiry; secret hardcoded | IdentityTokenClaimService.cs, AuthorizationConstants.cs | 0.99 |
| FA-008 | BlazorAdmin is a WASM SPA deployed separately from Web MVC | docker-compose.yml separate containers; Program.cs WebAssemblyHostBuilder | 0.95 |
| FA-009 | Deployment target: Azure App Service (eshopwebmvc, eshoppublicapi), plus SQL Server container | azure.yaml, docker-compose.yml | 0.95 |
| FA-010 | Ardalis.Specification used for query encapsulation in all domain modules | EfRepository.cs, Specifications/ folder | 0.99 |
| FA-011 | No message bus, no event-driven integration, no background job processor visible | Codebase scan — no IHostedService, no queue, no pub/sub | 0.90 |
| FA-012 | No caching infrastructure (Redis, IMemoryCache) other than BlazorAdmin browser localStorage | Dependencies.cs scope, no Redis package references | 0.90 |
| FA-013 | EmailSender is a stub — no email is ever sent | EmailSender.cs: Task.CompletedTask | 0.99 |
| FA-014 | No inventory/stock control on CatalogItem | CatalogItem entity has no stock quantity field | 0.97 |
| FA-015 | Buyer and PaymentMethod entities defined but have no active service references | CatalogContext DbSets, no service consumers visible | 0.75 |

---

## Section 2: Inferred Architecture Facts (Medium Confidence 0.70–0.89)

| Fact ID | Fact | Source | Confidence |
|---|---|---|---|
| FI-001 | Web MVC project uses cookie-based ASP.NET Identity authentication | Presence of AppIdentityDbContext; separate from JWT-based PublicApi auth | 0.85 |
| FI-002 | Web project orchestrates Basket and Order services (not visible in Layer 1) | IBasketService, IOrderService have Web-facing interfaces | 0.82 |
| FI-003 | Catalog item images may use Azure Blob Storage (PictureUri placeholder pattern) | UriComposer replaces 'catalogbaseurltobereplaced' placeholder | 0.75 |
| FI-004 | BlazorAdmin embedded in Web project for production (baseUrls.apiBase suggests co-hosting) | BlazorAdmin wwwroot/appsettings.json baseUrls.webBase = '/' | 0.72 |
| FI-005 | PublicApi has catalog item CRUD endpoints (Create, Read, Update, Delete) | BlazorAdmin HTTP calls to 'catalog-items' for all CRUD ops | 0.88 |

---

## Section 3: Forward Engineering Decision Points

### 3.1 Security Remediation (Immediate)

| Decision Point | Current State | Target State | Blocking Fact |
|---|---|---|---|
| JWT secret management | Hardcoded in AuthorizationConstants.cs | Environment variable / Azure Key Vault | FA-007 |
| Token TTL and refresh | 7-day access token, no refresh | 15-60 min access + refresh token | FA-007 |
| Email stub replacement | Task.CompletedTask stub | Real email provider (SendGrid, ACS) | FA-013 |
| Admin endpoint authorization | Unknown | [Authorize(Roles=Administrators)] on all write endpoints | FI-005 |

---

### 3.2 Database Architecture (Medium Term)

| Decision Point | Current State | Target State | Blocking Fact |
|---|---|---|---|
| DbContext consolidation | 1 CatalogContext for 3 bounded contexts | 3 separate DbContexts (CatalogContext, BasketContext, OrderContext) | FA-005 |
| Basket storage | SQL Server via CatalogContext | Redis (cache) or separate SQL schema | FA-006 |
| Connection string naming | CatalogConnection used for all domain data | Separate connection strings per bounded context | FA-003 |

---

### 3.3 Service Extraction Readiness

| Decision Point | Current State | Target State | Blocking Fact |
|---|---|---|---|
| Catalog read API | Exposed in PublicApi; coupled to CatalogContext | Standalone CatalogReadService | FA-005, FI-005 |
| Identity service | AuthenticateEndpoint in PublicApi | Standalone IdentityService or managed IdP | FA-007 |
| Basket service | ApplicationCore service + CatalogContext storage | Standalone BasketService with Redis | FA-005, FA-006 |
| Order service | ApplicationCore service; reads Basket + Catalog | Standalone OrderService (event-driven after Basket/Catalog extracted) | FA-011, FA-005 |

---

### 3.4 Missing Infrastructure (Gap Analysis)

| Gap | Impact | Recommended Pattern |
|---|---|---|
| No message bus | Services cannot communicate async; all calls are synchronous | Introduce Azure Service Bus or RabbitMQ; start with domain events within monolith |
| No server-side caching | Cold-start API latency; no cache for catalog reads | Add IMemoryCache or Redis for catalog items and brands |
| No distributed tracing | Cannot trace requests across Web → PublicApi → DB | Add OpenTelemetry with Azure Monitor |
| No health check endpoints | Cannot verify service availability | Add ASP.NET Core health checks (/health, /ready) |
| No background processing | Long-running tasks (email, order fulfillment) block web threads | Add IHostedService or Azure Functions for async tasks |
| No rate limiting | PublicApi has no visible rate limiting | Add ASP.NET Core rate limiting middleware on public endpoints |

---

### 3.5 Domain Model Gaps

| Gap | Description | Forward Engineering Action |
|---|---|---|
| Buyer/PaymentMethod dead code | Entities defined, no callers | Remove or implement; create explicit tracking item |
| No order status lifecycle | Orders are created only; no fulfillment/cancellation state machine | Add OrderStatus enum and status transition logic |
| No inventory tracking | CatalogItem has no stock quantity | Add AvailableStock field and stock reservation in checkout |
| No product categories hierarchy | CatalogType/CatalogBrand are flat single-level | Consider hierarchical category support if domain expands |

---

## Section 4: Module-to-Microservice Mapping

If the application is to be evolved towards microservices, the following mapping is recommended based on current bounded contexts:

```
Current Monolith Module    →    Target Microservice
─────────────────────────────────────────────────────
Catalog (read)             →    catalog-service (read model)
Catalog (write/admin)      →    catalog-management-service
Basket                     →    basket-service (Redis-backed)
Order                      →    order-service
Identity                   →    identity-service (or managed IdP)
BlazorAdmin                →    admin-portal (already SPA; point at new services)
Web (MVC)                  →    storefront (BFF pattern calling downstream services)
CrossCutting               →    shared-libs (NuGet packages per platform standard)
```

**Note:** This mapping requires the DbContext split (Section 3.2) as a pre-requisite for all service extractions.

---

## Section 5: Open Questions Requiring Resolution Before Forward Engineering

| ID | Question | Impact if Unresolved |
|---|---|---|
| OQ-001 | Does the Web project use cookie-based auth separately from JWT? | Identity service extraction plan cannot finalize |
| OQ-002 | Are catalog mutation endpoints protected by admin role? | Security posture of admin extraction is unknown |
| OQ-003 | Is BlazorAdmin embedded in Web or served separately in production? | Admin portal deployment architecture unknown |
| OQ-004 | What triggers basket deletion after order? | Data integrity of checkout flow unknown |
| OQ-005 | Are there Web project controllers for Basket, Order, Catalog browse? | Primary user flow entry points unknown |
| OQ-006 | How are catalog images stored (local vs. Azure Blob)? | Catalog read service media handling approach unclear |
| OQ-007 | Is there an Azure DevOps / GitHub Actions CI pipeline? | Deployment modernization planning requires CI knowledge |
