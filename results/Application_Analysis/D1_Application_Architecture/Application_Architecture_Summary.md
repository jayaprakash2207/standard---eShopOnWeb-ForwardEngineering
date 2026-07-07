# Application Architecture Summary — eShopOnWeb

**Extraction date:** 2026-07-06
**Codebase:** eShopOnWeb (.NET 8 Reference Application — Microsoft / ardalis)
**Extraction confidence:** Overall 0.88 (high for ApplicationCore + Infrastructure layers; medium for Web/PublicApi catalog endpoints due to Layer 1 gaps)

---

## 1. What This System Is

eShopOnWeb is a .NET 8 e-commerce reference application demonstrating Clean Architecture, Domain-Driven Design, and layered monolith patterns. It consists of a public-facing web storefront (ASP.NET Core MVC), a REST API for catalog/auth data, and a Blazor WebAssembly admin UI for catalog management. The system is deployable to Azure App Service via `azd` or locally via Docker Compose.

---

## 2. Architecture Pattern

**Clean Architecture (Onion / Ports & Adapters)**

- `ApplicationCore` is the innermost layer — domain entities, interfaces, application services. Zero infrastructure dependencies.
- `Infrastructure` is the outer layer — implements all ApplicationCore interfaces (EfRepository, IdentityTokenClaimService, EmailSender, LoggerAdapter).
- `Web` and `PublicApi` depend on ApplicationCore (for business logic) and Infrastructure (for DI wiring) but never the reverse.
- `BlazorAdmin` is entirely HTTP-driven — calls PublicApi endpoints; shares DTOs via `BlazorShared` library. No direct ApplicationCore or Infrastructure reference.

**Secondary patterns confirmed:**
- Repository + Specification pattern (Ardalis.Specification)
- Decorator pattern for browser-side caching (CachedCatalogItemServiceDecorator)
- DDD Aggregates (Basket, Order, CatalogItem with encapsulated invariants)
- Value Objects (Address, CatalogItemOrdered price snapshot)
- Endpoint-per-handler (MinimalApi.Endpoint + Ardalis.ApiEndpoints — inconsistently mixed)

---

## 3. Modules

| Module | Responsibility | Boundary Quality |
|---|---|---|
| Catalog | Product data (items, brands, types); CRUD via PublicApi | Moderate |
| Basket | Shopping basket lifecycle; anonymous-to-auth transfer | Strong |
| Order | Checkout orchestration; immutable order with price snapshot | Strong |
| Identity | ASP.NET Identity; JWT issuance; user management | Moderate |
| Admin | BlazorAdmin SPA; catalog CRUD via HTTP to PublicApi | Moderate |
| CrossCutting | IRepository, IAppLogger, UriComposer, EmailSender (stub) | Strong |

---

## 4. Key Components

| Component | Type | Risk |
|---|---|---|
| CatalogContext | EF DbContext | God context — 7 DbSets across 3 bounded contexts |
| OrderService | Application Service | High coupling — reads Basket + Catalog in one transaction |
| IdentityTokenClaimService | Infrastructure | Hardcoded JWT_SECRET_KEY — **production blocker** |
| AuthorizationConstants | Domain Constants | Hardcoded JWT_SECRET_KEY + DEFAULT_PASSWORD |
| EmailSender | Infrastructure | Stub — Task.CompletedTask — all emails silently dropped |
| CachedCatalogItemServiceDecorator | Blazor Service | localStorage cache — per-tab, non-shared, cleared on startup |
| BasketQueryService | Infrastructure Query | Bypasses EfRepository — direct DbContext SUM query |
| Buyer / PaymentMethod | Domain Entities | Dead code candidates — no visible service consumers |

---

## 5. Data Architecture

- **Two connection strings:** `CatalogConnection` (all domain data) and `IdentityConnection` (ASP.NET Identity tables)
- **Two DbContexts:** `CatalogContext` (Catalog + Basket + Order tables — violation: spans 3 BCs) and `AppIdentityDbContext` (Identity)
- **No separate databases per bounded context** — Catalog, Basket, and Order all share `CatalogConnection`
- **No caching layer** beyond browser localStorage in BlazorAdmin
- **No message bus or event-driven integration**

---

## 6. API Surface

| Endpoint | Type | Confidence |
|---|---|---|
| POST api/authenticate | REST | 0.99 |
| GET api/catalog-brands | REST | 0.99 |
| GET api/catalog-types | REST | 0.82 (inferred) |
| GET api/catalog-items | REST | 0.90 (inferred) |
| GET api/catalog-items/{id} | REST | 0.88 (inferred) |
| POST api/catalog-items | REST (admin) | 0.88 (inferred) |
| PUT api/catalog-items | REST (admin) | 0.85 (inferred) |
| DELETE api/catalog-items/{id} | REST (admin) | 0.85 (inferred) |
| Web MVC routes (catalog browse, basket, checkout) | HTTP/HTML | 0.70 (unknown — source not in Layer 1) |

---

## 7. Deployment

- **Azure:** `azure.yaml` + Bicep — 2 App Service deployments (`eshopwebmvc`, `eshoppublicapi`) + SQL Server
- **Docker:** `docker-compose.yml` — 3 containers (`eshopwebmvc`, `eshoppublicapi`, `sqlserver` using `azure-sql-edge` image)
- **Ports (local):** Web → 5001/5002; PublicApi → 5099/5100; SQL → 1433

---

## 8. Security Findings (Critical First)

| ID | Finding | Severity | Production Blocker |
|---|---|---|---|
| RISK-001 / VIO-001 | Hardcoded JWT_SECRET_KEY + DEFAULT_PASSWORD in source | **Critical** | **Yes** |
| RISK-008 | Admin catalog mutation endpoints — authorization unknown | **High** | **Yes** |
| RISK-002 / VIO-002 | EmailSender stub — all emails silently dropped | **High** | **Yes** |
| RISK-003 / VIO-007 | 7-day JWT tokens, no revocation mechanism | High | No |
| RISK-006 | Price parameter in AddItemToBasket — potential manipulation if Web passes user-supplied price | Medium | No |
| RISK-004 / VIO-006 | No transaction boundary in checkout — duplicate order risk | Medium | No |

**Three production blockers must be resolved before any production deployment.**

---

## 9. Architecture Violations Summary

9 violations identified. Critical:
- VIO-001: Hardcoded secrets
- VIO-002: Stub email in DI
- VIO-003: God DbContext
- VIO-007: Long-lived JWT tokens

---

## 10. Strangler Fig Extraction Readiness

| Module | Extractable Now? | Blockers |
|---|---|---|
| Catalog (read API) | Partial — API exists | DbContext split required |
| Identity Service | Partial | Secret externalization required; Web auth unknown |
| Basket Service | No | DbContext split; Web basket controller unknown |
| Order Service | No | Highest coupling (reads Basket + Catalog); must go last |

**Recommended order:** Externalize secrets → split DbContext → extract Identity → extract Catalog read → extract Catalog admin → extract Basket → extract Order.

---

## 11. Key Open Questions (Top 5)

1. **Web project controllers/pages not available** — primary user flows (browse, basket, checkout) are unknown (22 open questions in open-questions.md)
2. **Admin endpoint authorization** — POST/PUT/DELETE catalog-items authorization enforcement unknown (RISK-008)
3. **Basket cleanup after order** — is the basket deleted after successful checkout? (RISK-004)
4. **BlazorAdmin hosting** — embedded in Web or standalone? Affects deployment architecture
5. **Buyer/PaymentMethod dead code** — need Web project scan to confirm no active consumers

---

## 12. Output Files

| File | Stage | Description |
|---|---|---|
| system-inventory.json | 1 | 6 apps/libraries, 3 Docker units, 1 Azure deployment |
| module-boundary-map.json | 2 | 6 modules with coupling scores and evidence |
| component-registry.json | 3 | 27 components with dependencies and risk flags |
| application-interface-catalogue.json | 4 | 12 interfaces (8 REST, 2 Blazor routes, 2 inferred) |
| dependency-graph.json | 5 | 18 nodes, 24 edges, 1 cross-module cycle |
| call-flow-map.json | 6 | 6 traced call flows (auth, catalog list, basket, checkout, transfer, admin create) |
| architecture-pattern-report.md | 7 | Clean Architecture confirmed; 6 patterns; 7 anti-patterns |
| architecture-violation-register.json | 8 | 9 violations (1 Critical, 4 High, 3 Medium, 1 Low) |
| application-risk-register.json | 9 | 10 risks (1 Critical, 4 High, 4 Medium, 1 Low) |
| strangler-candidate-report.md | 10 | 4 extraction candidates with ordered migration plan |
| forward-engineering-input-map.md | 11 | 15 confirmed facts, 5 inferred facts, 7 decision points, 4 gap areas |
| open-questions.md | 12 | 22 open questions across 6 categories |
| extraction-audit.md | — | Coverage map, rules compliance, stage completion |
| application-architecture-summary.md | 13 | This file |
| diagrams/system-context.mmd | — | C4 Context diagram |
| diagrams/container-view.mmd | — | C4 Container diagram |
| diagrams/component-view.mmd | — | Component graph with risk annotations |
| diagrams/dependency-view.mmd | — | Project + package dependency graph |
| diagrams/call-flow-view.mmd | — | Sequence diagram: Auth + Catalog list + Checkout |
