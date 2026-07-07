# Application Architecture Summary — eShopOnWeb

**Extraction agent:** Application Architecture Extraction Agent
**Output directory:** test-run/D1-application-architecture/
**Date:** 2026-07-06
**Coverage:** ApplicationCore, Infrastructure, PublicApi, BlazorAdmin (Web project NOT extracted — see Section 15)

---

## 1. System Overview

eShopOnWeb is a reference e-commerce application built on ASP.NET Core 8. It demonstrates Clean Architecture / Onion Architecture patterns and DDD-Lite practices on the .NET platform.

**Deployable units:**
| Unit | Technology | Role |
|---|---|---|
| Web | ASP.NET Core 8 MVC + Razor Pages | Primary shopper-facing UI — catalog browsing, basket, checkout, orders |
| PublicApi | ASP.NET Core 8 Minimal API (Ardalis.ApiEndpoints) | REST API — authentication + catalog admin |
| BlazorAdmin | Blazor WebAssembly | Admin SPA for catalog item management |

**Shared libraries:** ApplicationCore (domain + services + interfaces), Infrastructure (EF Core + repositories + identity), BlazorShared (DTOs shared between Blazor + PublicApi).

**Evidence:** `azure.yaml`, `docker-compose.yml`, `src/*/launchSettings.json`

---

## 2. Architecture Pattern

**Primary: Clean Architecture (confidence: 0.90)**

The codebase follows Clean Architecture with strict dependency inversion:
- ApplicationCore has zero dependencies on Infrastructure or UI layers
- Infrastructure implements ApplicationCore interfaces (IRepository, ITokenClaimService, IEmailSender)
- No direct EF Core references appear in ApplicationCore services
- `IAppLogger<T>` wraps `Microsoft.Extensions.Logging` — core is decoupled from logging framework

**Secondary: Decorator Pattern** in BlazorAdmin caching layer
- `CachedCatalogItemServiceDecorator` and `CachedCatalogLookupDataServiceDecorator` wrap Blazor services
- 1-minute TTL client-side cache via Blazored.LocalStorage

**DDD-Lite patterns observed:**
- IAggregateRoot marker constrains IRepository<T> to aggregate roots
- Rich domain entities (Basket.AddItem, Order.Total(), CatalogItem.UpdateDetails)
- Value Objects: Address, CatalogItemOrdered (order-time snapshot)
- Specifications: Ardalis.Specification for query encapsulation
- Guard.Against validation in domain entity methods

---

## 3. Module Inventory

| Module | Boundary Quality | Artifacts | Status |
|---|---|---|---|
| Catalog | Moderate | CatalogItem, CatalogBrand, CatalogType, PublicApi endpoints | Active |
| Basket | Strong | Basket, BasketItem, BasketService, IBasketService | Active |
| Order | Strong | Order, OrderItem, OrderService, IOrderService | Active |
| Authentication | Moderate | AppIdentityDbContext, IdentityTokenClaimService, AuthenticateEndpoint | Active |
| Buyer | Weak | Buyer, PaymentMethod entities only | Dead code candidate — no service, no DbSet |
| Infrastructure-Cross-Cutting | Strong | EfRepository<T>, CatalogContext, DISetup | Active — shared violation |

---

## 4. Component Inventory (Key)

20 components discovered. Key high-risk entries:

| Component | Type | Risk |
|---|---|---|
| CatalogContext | EF DbContext | SHARED_CONTEXT — 3 domains in 1 context — #1 migration blocker |
| EfRepository<T> | Repository | SHARED_INFRASTRUCTURE — used across all modules |
| OrderService | Application Service | HIGH_EFFERENT_COUPLING — reads Basket, Catalog, writes Order |
| HttpService (Blazor) | HTTP Gateway | RETURNS_NULL_ON_ERROR — silent failures on GET/DELETE |
| CachedCatalogItemServiceDecorator | Decorator | CACHE_INVALIDATION risk on catalog writes |
| AuthorizationConstants | Constants | HARDCODED_SECRETS — Critical security violation |
| IdentityTokenClaimService | Auth Service | Issues JWT with hardcoded key |

---

## 5. API Surface (Discovered)

| Endpoint | Confirmed/Inferred | Source |
|---|---|---|
| POST /api/authenticate | Confirmed | src/PublicApi/AuthEndpoints/AuthenticateEndpoint.cs |
| GET /api/catalog-brands | Confirmed | src/PublicApi/CatalogBrandEndpoints/CatalogBrandListEndpoint.cs |
| GET /api/catalog-items | Inferred | BlazorAdmin CatalogItemService.cs |
| POST /api/catalog-items | Inferred | BlazorAdmin CatalogItemService.cs |
| PUT /api/catalog-items/{id} | Inferred | BlazorAdmin CatalogItemService.cs |
| DELETE /api/catalog-items/{id} | Inferred | BlazorAdmin CatalogItemService.cs |
| GET /api/catalog-types | Inferred | BlazorAdmin CatalogItemService.cs |
| GET /User | Inferred | BlazorAdmin CustomAuthStateProvider.cs |

**Note:** All Web project (MVC) endpoints unknown — not in Layer 1 extraction.

---

## 6. Dependency Graph Summary

- **27 nodes**, **23 edges**, **1 dependency cycle** detected
- Cycle: OrderService → Basket data → CatalogContext (medium severity)
- Highest afferent coupling (most depended upon): CatalogContext (afferent=6), EfRepository<T> (afferent=5)
- Highest efferent coupling (most dependencies): OrderService (efferent=4)

**Full graph:** `dependency-graph.json`

---

## 7. Call Flows Traced

| Flow | Entry Point | Modules Touched | Risk |
|---|---|---|---|
| FLOW-001: Admin Auth | POST /api/authenticate | Authentication | Hardcoded JWT key |
| FLOW-002: Add to Basket | Unknown Web controller | Basket, Infrastructure | Entry point not extracted |
| FLOW-003: Checkout/Place Order | Unknown Web checkout | Order, Basket, Catalog, Infrastructure | Basket not deleted; no payment |
| FLOW-004: Basket Transfer on Login | Unknown Web login handler | Basket, Auth, Infrastructure | 2-record transaction risk |
| FLOW-005: BlazorAdmin Catalog List | List.razor.cs OnAfterRenderAsync | Catalog, Infrastructure, BlazorAdmin | Client-side join; async void bug |

---

## 8. Architecture Violations (Summary)

9 violations detected. Severity breakdown:

| Severity | Count | Key Example |
|---|---|---|
| Critical | 1 | Hardcoded JWT secret + default password in source |
| High | 1 | Shared CatalogContext spans 3 domain boundaries |
| Medium | 3 | Order→Basket cross-module; frontend client-side join; HttpService null returns |
| Low | 4 | Dead code (Buyer, EmailSender stub); async void bug; fat OrderService |

**Full register:** `architecture-violation-register.json`

---

## 9. Application Risk Register (Summary)

10 risks identified. Top risks:

| ID | Severity | Risk |
|---|---|---|
| APP-RISK-002 | Critical | Hardcoded JWT secret — blocks production deployment |
| APP-RISK-001 | High | Shared CatalogContext — #1 migration blocker |
| APP-RISK-003 | High | OrderService→Basket coupling — blocks Order extraction |
| APP-RISK-005 | High | Web project not extracted — architecture incomplete |
| APP-RISK-007 | Medium | BlazorAdmin client-side API fan-out |
| APP-RISK-009 | Medium | Basket transfer is a 2-record transaction |

**Full register:** `application-risk-register.json`

---

## 10. Strangler / Migration Candidate Ranking

| Rank | Module | Classification | Prerequisite |
|---|---|---|---|
| 1 | Authentication | Good Early Candidate | Rotate JWT secret first |
| 2 | Catalog (read path) | Good Early Candidate | Split CatalogContext |
| 3 | Basket | Possible (with refactoring) | Split CatalogContext; define checkout DTO |
| 4 | Order | Poor (last) | Basket + Catalog extracted first; checkout saga design |
| 5 | Buyer | Unknown | Human decision required |

**Recommended migration sequence:** Security hardening → Auth service → Catalog read → Context split → Basket → Catalog write → Order saga

**Full report:** `strangler-candidate-report.md`

---

## 11. Forward Engineering Inputs (Summary)

Key inputs for forward engineering agents:

**Domain model:** Carry Basket, Order, CatalogItem aggregates as-is. Preserve Address and CatalogItemOrdered value objects. Guard.Against validation pattern should be used in all new domain entities.

**Data model:** Split CatalogContext into CatalogContext (catalog), BasketContext (basket), OrderContext (order). IdentityContext stays separate. Maintain soft cross-context references (no FK enforcement across boundaries).

**API design:** Eliminate client-side join — catalog-items response should embed brand/type names. Add pagination standard. Version all API endpoints (/api/v1/).

**Security:** JWT secret to Azure Key Vault. Remove DEFAULT_PASSWORD from source. Per-request auth headers in Blazor (not shared DefaultRequestHeaders).

**Caching:** Server-side Redis for catalog items in production. Client-side LocalStorage appropriate only for static lookup data.

**Full map:** `forward-engineering-input-map.md`

---

## 12. Security Findings (Summary)

| Finding | Severity | File | Action |
|---|---|---|---|
| Hardcoded JWT_SECRET_KEY | Critical | src/ApplicationCore/Constants/AuthorizationConstants.cs | Rotate; move to Key Vault — must do BEFORE any deployment |
| Hardcoded DEFAULT_PASSWORD | Critical | src/ApplicationCore/Constants/AuthorizationConstants.cs | Remove from source; use secret seeding |
| Shared HttpClient DefaultRequestHeaders | Medium | src/BlazorAdmin/CustomAuthStateProvider.cs | Use per-request headers — thread safety risk |
| EmailSender not implemented | Medium | src/Infrastructure/Services/EmailSender.cs | Implement before enabling account features |
| HttpService null on error | Medium | src/BlazorAdmin/Services/HttpService.cs | Add error observability |

---

## 13. Diagrams Generated

| Diagram | File | Type |
|---|---|---|
| System Context | diagrams/system-context.mmd | C4 Context (Mermaid) |
| Container View | diagrams/container-view.mmd | C4 Container (Mermaid) |
| Component View | diagrams/component-view.mmd | Flowchart (Mermaid) |
| Dependency View | diagrams/dependency-view.mmd | Flowchart with violations (Mermaid) |
| Call Flow View | diagrams/call-flow-view.mmd | Sequence (Mermaid) — 3 key flows |

---

## 14. Open Questions (Summary)

12 open questions requiring human review. Critical subset:

| ID | Question | Priority |
|---|---|---|
| OQ-001 | Web project source not extracted — basket/checkout/order controllers unknown | High |
| OQ-004 | Is JWT secret already rotated in production? | Critical |
| OQ-005 | Are accounts seeded with DEFAULT_PASSWORD still in production DB? | Critical |
| OQ-006 | Buyer aggregate — dead code or planned payment module? | Medium |
| OQ-007 | Which project serves GET /User? | Medium |
| OQ-008 | Does checkout controller delete basket after order? | Medium |
| OQ-009 | Is payment processing intentionally absent? | Medium |

**Full list:** `open-questions.md`

---

## 15. Coverage Gaps and Caveats

The following system areas were NOT covered in this extraction and must be addressed before architecture analysis is complete:

**Web project (src/Web) — Critical Gap**
- The primary user-facing application was not in the Layer 1 extraction data
- Basket management, checkout flow, order history, catalog browsing, and Web-side authentication are all unknown
- Architecture diagrams for Basket and Order modules are incomplete
- Migration sequence cannot be finalized without this analysis
- **Action required:** Re-run Layer 1 extraction targeting `src/Web/**/*.cs`

**Test projects — Medium Gap**
- Test coverage level is unknown
- Migration regression risk cannot be quantified
- **Action required:** Extract and assess test project coverage

**BlazorAdmin Create/Edit/Delete pages — Low Gap**
- Only List.razor.cs was in extraction data
- Create, Edit, Delete catalog item pages presumed to exist based on service methods but not verified
- **Action required:** Include BlazorAdmin pages in Layer 1 extraction

---

## Final Agent Statement

Architecture extraction is **substantively complete** for the source files provided. All 13 processing stages were executed. All 19 output files were generated.

The extraction reveals a well-structured Clean Architecture implementation with DDD-Lite practices. The codebase is migration-ready in terms of layering and interface design. However, **two critical blockers** must be resolved before any forward engineering work begins:

1. **Security:** Rotate the hardcoded JWT secret and remove DEFAULT_PASSWORD from source
2. **Coverage:** Extract the Web project source to complete the architecture map

The shared CatalogContext is the primary technical migration blocker. The recommended migration sequence (Auth → Catalog read → Context split → Basket → Order saga) provides a safe, incremental path to a microservice architecture using the strangler fig pattern.

**Confidence in this extraction: 0.88** (limited by Web project gap and inferred endpoints)
