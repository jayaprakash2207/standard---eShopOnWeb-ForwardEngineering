# Executive Summary — eShopOnWeb Architecture Extraction

**Prepared for:** Architecture Review Board / Engineering Leadership
**Source:** Agent 1 Application Architecture Extraction — `results/aa-outputs/D1-application-architecture/`
**Quality review verdict:** PARTIAL (usable with three noted defects)
**Date:** 2026-07-06

---

## What Was Done

Agent 1 performed a full reverse-engineering extraction of the eShopOnWeb codebase. It produced 19 structured artifacts — 8 JSON data files, 6 Markdown reports, and 5 Mermaid diagrams — covering system inventory, module boundaries, component registry, API contracts, dependency graph, call flows, architecture violations, risk register, migration candidate ranking, and forward engineering inputs.

The extraction covered four of the six projects in depth: `ApplicationCore`, `Infrastructure`, `PublicApi`, and `BlazorAdmin`. The primary user-facing application (`src/Web` — MVC/Razor Pages) was not available in the extraction data and is the single largest gap.

---

## What the Codebase Actually Is

eShopOnWeb is a reference e-commerce application on ASP.NET Core 8. It is a **modular monolith** — not yet microservices — structured using Clean Architecture (strict dependency inversion: interfaces in the core, infrastructure at the edge) with DDD-Lite practices (aggregate roots, value objects, specifications, Guard.Against validation).

Three deployable units run today:

| Unit | What it does |
|---|---|
| Web (MVC) | Shopper UI — catalog browsing, basket, checkout, order history |
| PublicApi (Minimal API) | REST API — authentication + admin catalog endpoints |
| BlazorAdmin (Blazor WASM) | Admin SPA — catalog item management (calls PublicApi) |

One SQL Server database instance serves all business data via `CatalogConnection`. ASP.NET Identity uses a logically separate `IdentityConnection`. Both connections are configured in `src/PublicApi/appsettings.json` and `src/Web` startup (inferred). All runs on Azure App Service (production) and Docker Compose (local dev), provisioned with Azure Developer CLI + Bicep.

---

## The Two Decisions That Block Everything Else

**1. Security hardening must happen before any deployment.**

The JWT signing secret is hardcoded in source (`src/ApplicationCore/Constants/AuthorizationConstants.cs`: `JWT_SECRET_KEY`). The default admin seed password is also in the same file (`DEFAULT_PASSWORD`). Any forward-engineered service deployed today carries a known-compromised authentication key. This is a deployment blocker, not a debt item.

*Required action before migration sprint 1:* Rotate JWT secret to Azure Key Vault or environment variable; remove `DEFAULT_PASSWORD` from source; audit Identity DB for accounts still using the seed password.

**2. The shared database context must be split before service extraction.**

A single EF `CatalogContext` (`src/Infrastructure/Data/CatalogContext.cs`) owns seven DbSets covering all business entities: Baskets, BasketItems, CatalogItems, CatalogBrands, CatalogTypes, Orders, OrderItems. No module can be independently deployed while they share one schema and one migration chain.

*Required action before any module extraction:* Design and execute a schema split into CatalogContext, BasketContext, and OrderContext. This is the primary technical prerequisite for the entire strangler sequence.

---

## Module Readiness at a Glance

| Module | Extraction Coverage | Migration Readiness | Blocker |
|---|---|---|---|
| Identity (Auth) | High | Good early candidate | Rotate JWT secret first |
| Catalog (read) | High | Good early candidate | Split CatalogContext first |
| Catalog (admin write) | Partial (endpoint source not available) | After read extraction | CatalogItemEndpoints source missing; auth enforcement unknown |
| Basket | High | Possible with refactoring | Context split + Web project basket controller unknown |
| Order | High | Last in sequence | Basket + Catalog must be extracted first; checkout transaction gap must be resolved |
| Buyer/PaymentMethod | Partial (entity only) | Unknown | Dead code or planned payment module — human decision needed |
| Web project | None | N/A | Source not in extraction — critical gap; cannot finalize migration sequence |

---

## Recommended Migration Sequence (Summary)

Based on the extraction, the strangler-candidate-report.md proposes:

```
Phase 0 — Pre-migration hardening (blockers, not extractions)
  · Rotate JWT secret → Azure Key Vault
  · Remove DEFAULT_PASSWORD from source
  · Extract and analyse src/Web controllers/pages (fill the primary source gap)
  · Resolve Buyer/PaymentMethod fate (dead code removal or feature tracking item)

Phase 1 — Low-risk extractions
  · Extract Identity Service (already has separate AppIdentityDbContext and clean HTTP interface)
  · Extract Catalog Read API (highest demand, lowest coupling; GET endpoints already exist)

Phase 2 — Database context split (prerequisite for all remaining phases)
  · Split CatalogContext → CatalogContext + BasketContext + OrderContext
  · Run schema migrations per bounded context; use separate connection strings

Phase 3 — Module extractions
  · Extract Basket Service (replace SQL basket with Redis)
  · Extract Catalog Admin Service (write operations; add event publication)

Phase 4 — Order and orchestration
  · Design checkout saga spanning Basket + Order + Payment
  · Extract Order Service
  · Design Payment Service (net-new; PaymentMethod entity already in domain model)

Phase 5 — Web decomposition
  · Decompose Web MVC into BFF layers or micro-frontends
  · Retire monolith
```

---

## Key Architecture Findings

| Finding | Confidence | Impact |
|---|---|---|
| Clean Architecture with DDD-Lite — strong foundation for extraction | 0.97 | Positive: ApplicationCore has zero infrastructure deps; portable |
| Shared CatalogContext spans Catalog, Basket, and Order | 0.97 | Blocker: #1 technical prerequisite for any microservice extraction |
| OrderService reads Basket and Catalog repos in one call | 0.98 | Complicates Order extraction; requires checkout saga design |
| JWT secret and default password hardcoded in source | 0.99 | Critical security blocker; must fix before any deployment |
| AppIdentityDbContext already separate from CatalogContext | 0.99 | Positive: Auth service extraction is the most straightforward |
| EmailSender is a stub — all emails silently dropped | 0.99 | Production blocker: account recovery, password reset, and order confirmation non-functional |
| Admin catalog mutation endpoint authorization unknown | 0.85 | Security risk: POST/PUT/DELETE catalog-items source not available; role enforcement unverified |
| Basket transfer has no explicit transaction scope | 0.87 | Data integrity risk: anonymousBasket delete and userBasket update are separate calls |
| 7-day JWT TTL with no revocation mechanism | 0.97 | Security debt: stolen tokens valid 7 days with no server-side revocation path |

---

## Production Blockers (Must Fix Before Go-Live)

Three items are flagged `"production_blocker": true` in the risk register:

| Blocker | Location | Fix Effort |
|---|---|---|
| RISK-001: JWT_SECRET_KEY + DEFAULT_PASSWORD hardcoded | `AuthorizationConstants.cs` | Low — environment variable wiring |
| RISK-002: EmailSender stub — all emails silently dropped | `EmailSender.cs` | Medium — real email provider integration |
| RISK-008: Admin catalog endpoint authorization unknown | `PublicApi/CatalogItemEndpoints/` (not in extraction) | Low once source is obtained — add [Authorize(Roles=Administrators)] |

---

## Open Questions Requiring Human Response

Documented in `open-questions.md` (22 total); the highest-priority items for forward engineering decisions:

| Question | Priority | Why It Matters |
|---|---|---|
| What controllers/pages does src/Web expose? | Critical | Cannot finalize migration sequence; basket, checkout, order flows are architecturally incomplete |
| Are catalog mutation endpoints protected by admin role? | Critical | Security posture of the admin API is unknown |
| Has the JWT secret been rotated in production environments? | Critical | Determines whether existing sessions are already compromised |
| Is BlazorAdmin embedded in Web (hosted mode) or standalone? | High | Admin portal deployment architecture affects extraction planning |
| What triggers basket deletion after a successful order? | High | Checkout data integrity (RISK-004) impact cannot be scoped |
| Is the Buyer/PaymentMethod aggregate dead code or a planned feature? | Medium | Determines whether payment is in extraction scope |
| What does GET /User serve, and from which project? | Medium | Required for auth service API contract design |

---

## What Was Not Covered

| Gap | Impact |
|---|---|
| `src/Web` (MVC/Razor Pages) — not extracted | Basket, Order, and catalog browsing entry points undocumented; 5 call flows have unknown entry points |
| `src/PublicApi/CatalogItemEndpoints/` — not extracted | Admin CRUD endpoint authorization unverifiable; INT-004 to INT-008 are inferred, not confirmed |
| Test projects — not extracted | Cannot quantify migration regression risk; test coverage baseline unknown |
| `infra/` Bicep files — not extracted | Azure infrastructure baseline unknown beyond what azure.yaml declares |
| BlazorAdmin Create/Edit/Delete pages — only List.razor.cs available | Admin write-path Blazor UI not analysed |

These gaps do not invalidate the findings above. They bound the extraction confidence (overall 0.88) and define the scope of a follow-up extraction run.

---

## Quality Review Note

The extracted artifacts are substantively correct, well-evidenced, and safe for downstream planning. Three defects were found (see `quality-review.md` for details):

- **QR-001 (Medium):** "Infrastructure", "Web", and "PublicApi" used as module names in coupling fields but not declared as modules — causes resolution failures in programmatic module joins
- **QR-002 (Low):** "List (Blazor Page)" referenced in call flows but absent from component-registry.json
- **QR-003 (Low):** Three call flows (Add to Basket, Basket Transfer, Admin Create Item) not diagrammed in the sequence view

None of these defects affect the migration sequence, the security findings, or the production blocker identification.
