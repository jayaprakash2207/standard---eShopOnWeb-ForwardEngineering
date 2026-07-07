# Forward-Engineering Input Map

**System:** eShopOnWeb (authoritative name flagged `unknown` in source evidence — see `OQ-007` / `ASSUMP-007`)
**Source project:** eShopOnWeb
**Generated:** 2026-06-23
**Schema version:** 1.0
**Canonical source:** [`ENTERPRISE_KNOWLEDGE_GRAPH.json`](./ENTERPRISE_KNOWLEDGE_GRAPH.json)

> This document is a **view** over the verified canonical knowledge graph. It contains **no code and no new/target design**. It maps the already-evidence-grounded foundation graph to the inputs a future forward-engineering (FE) stage will consume. Every claim carries the graph node IDs so this document cross-references the JSON. Confidence/status signals (HIGH/MEDIUM/LOW, ACTIVE, implemented/aspirational, INFERRED, VERSION UNKNOWN) are preserved verbatim from the graph and are **not** elevated here.

---

## 1. Purpose & How to Consume This Package

This is a **foundation package**. It describes the current + canonical state of the system and the inputs a future forward-engineering stage will consume. It does **not** propose code, target architecture, or new designs beyond what the evidence already names.

**Canonical vs. views.** The JSON is the single source of truth; the Markdown documents are read-only projections of it.

| Artifact | Role | Notes |
| --- | --- | --- |
| `ENTERPRISE_KNOWLEDGE_GRAPH.json` | **Canonical source of truth** | All facts, IDs, confidence and status live here. Top-level sections: `metadata`, `business`, `data`, `application`, `technology`, `cross_links`, `assumptions`, `normalization_log`, `open_questions`. |
| `FORWARD_ENGINEERING_INPUT_MAP.md` (this doc) | **View** — FE input catalog | Maps graph sections/IDs to the inputs a future FE stage needs. |
| Other per-domain Markdown views | **Views** | Business / Data / Application / Technology narrative renderings of the same graph. |

**How to consume:**

1. Treat the JSON as authoritative. Where this doc and the JSON disagree, the JSON wins.
2. Use the node IDs (e.g. `DATA-ENT-001`, `APP-SVC-011`, `TECH-SEC-010`) to navigate back into the graph.
3. Respect the recorded **confidence** (HIGH/MEDIUM/LOW) and **status** (ACTIVE, implemented, aspirational/unimplemented, INFERRED). Low-confidence and inferred items are inputs that require human review, not decisions.
4. Consult `assumptions` (`ASSUMP-001..007`), `normalization_log`, and `open_questions` (`OQ-001..009`) before acting on any merged/normalized node.

The graph spans 4 domains: `business`, `data`, `application`, `technology`.
**Evidence note (verbatim from `metadata.confidence_note`):** Evidence-only consolidation; confidence/status signals preserved verbatim; no forward engineering; no new capabilities/entities/APIs invented; cross-links emitted only where a source file supports them.

---

## 2. Forward-Engineering Input Catalog

Each row maps an FE input artifact to the graph section(s)/IDs that provide it. Counts reflect node totals in the graph.

| FE input artifact | Graph section → IDs | Coverage / confidence signal |
| --- | --- | --- |
| Domain entities | `data.entities` → `DATA-ENT-001 … DATA-ENT-015` | 15 entities; per-node `persisted`, `pii`, `status`, `confidence` (0.7–0.9). |
| Aggregates & aggregate roots | `data.aggregates` → `DATA-AGG-001 … DATA-AGG-004` | 4 aggregates; `DATA-AGG-003 BuyerAggregate` is aspirational/unimplemented. |
| Entity relationships (cardinality) | `data.relationships` → 12 relationship nodes | Each carries `from`/`to`/`cardinality`/`status`. |
| Repositories & persistence boundaries | `data.repositories` → `DATA-REPO-001 … DATA-REPO-004` | Interfaces + EF DbContexts; `entities_served` vs `entities_served_inferred` distinguished (`OQ-008`). |
| API contracts to preserve | `application.apis` → `APP-API-001 … APP-API-055` + `cross_links.service_to_api` (55) | `preserve_redesign_review` flags `preserve` vs `review`; `confidence` HIGH→LOW. |
| Interface/port abstractions to preserve | `application.interfaces` → `APP-IF-001 … APP-IF-013` | 13 abstractions/ports; some have empty `implemented_by` (no concrete impl in evidence). |
| Bounded-context / service decomposition candidates | `application.services` → `APP-SVC-001 … APP-SVC-052` + `application.dependencies` + `cross_links.entity_to_service` | Module candidates, components, coupling and migration-readiness labels. See §3. |
| Dependency structure & cycle | `application.dependencies` → `APP-DEP-001 … APP-DEP-019` | `APP-DEP-001` records the module cycle; `APP-DEP-002..008` record layering violations. |
| Capability backlog drivers | `business.capabilities` → `BIZ-CAP-001 … (39 nodes, L1–L3)` + `cross_links.capability_to_process` (17) | 37 ACTIVE, 2 inferred; 6 L1 capabilities anchor the backlog. |
| Business processes / behavior to preserve | `business.processes` → `BIZ-PROC-001 … BIZ-PROC-010` + `cross_links.process_to_entity` (29) | 10 processes with `trigger`, `steps`, `business_rules`; confidence HIGH/MEDIUM. |
| Actors / roles | `business.actors` → `BIZ-ACT-001 … BIZ-ACT-005` | 5 actors (human/system/external). |
| NFRs / security baseline | `technology.security` → `TECH-SEC-001 … TECH-SEC-017` | 4 auth/authz controls, 3 secrets mechanisms, 10 findings. See §5. |
| Current technology stack (preserve/replace inputs) | `technology.current_stack` → `TECH-CUR-001 … TECH-CUR-026` | 26 nodes; many versions `(not declared)` / `unknown` — see §5 gaps. |
| Infrastructure & deployment topology | `technology.infrastructure` → `TECH-INF-001 … TECH-INF-008` | 3 containers, compose orchestration, CI/CD, Dependabot, Azure targets (referenced). |
| Target stack | `technology.target_stack` → **empty (0 nodes)** | No target stack recorded — intentionally out of scope for this foundation package (§6). |
| Assumptions / normalization to honor | `assumptions` (`ASSUMP-001..007`), `normalization_log` | Merged-node provenance; split using `merged_from` facets if needed. |
| Open questions feeding FE | `open_questions` → `OQ-001 … OQ-009` | Unresolved decisions and disagreements. See §5. |

---

## 3. Bounded-Context / Service Decomposition INPUTS (candidates only)

> These are **candidates derived strictly from evidence** (module nodes + the dependency cycle + data-ownership facts). They are **inputs, not decomposition decisions**. Coupling/boundary/migration-readiness labels are carried verbatim from `application.services`.

### 3.1 Module candidates and their evidence-recorded posture

| Service node | Module | Layer | Coupling / boundary / migration-readiness (verbatim) | Confidence |
| --- | --- | --- | --- | --- |
| `APP-SVC-001` Catalog | Catalog | mixed | HIGH (coupling 13); boundary Weak; readiness Blocked | MEDIUM |
| `APP-SVC-002` Identity | Identity | mixed | HIGH (coupling 8); boundary Weak; readiness Blocked | MEDIUM |
| `APP-SVC-003` Basket | Basket | mixed | HIGH (coupling 9); boundary Weak; readiness Blocked; depends on Admin, ApplicationCore, Catalog, DataAccess +3 | MEDIUM |
| `APP-SVC-004` Order | Order | mixed | coupling 4; boundary Weak; readiness Blocked; depends on ApplicationCore, Catalog, DataAccess, Verification | MEDIUM |
| `APP-SVC-005` Admin | Admin | Presentation/UI | coupling 3; boundary Weak; readiness Blocked; depends on Identity | MEDIUM |
| `APP-SVC-006` Web | Web | mixed | HIGH (high-coupling module); boundary Weak; readiness Blocked | HIGH |
| `APP-SVC-007` ApplicationCore | ApplicationCore | Application/Domain | HIGH (high-coupling module); boundary Weak; readiness Blocked; depends on Catalog | HIGH |
| `APP-SVC-008` DataAccess | DataAccess | DataAccess | coupling 5; boundary Weak; readiness Blocked; high-coupling component EfRepository (16) | MEDIUM |
| `APP-SVC-009` Infrastructure | Infrastructure | Infrastructure | boundary Medium; readiness Needs Refactoring; depends on none detected | HIGH |
| `APP-SVC-010` CrossCutting | CrossCutting | CrossCutting | boundary Medium; readiness Needs Refactoring; high-coupling module per blueprint | MEDIUM |
| `APP-SVC-011` PublicApi | PublicApi | API | boundary Medium; readiness Needs Refactoring; depends on none detected | HIGH |
| `APP-SVC-012` SharedContracts | SharedContracts | Application | boundary Medium; readiness Needs Refactoring; depends on none detected | HIGH |
| `APP-SVC-013` Verification | Verification | mixed | boundary Medium; readiness Needs Refactoring; depends on ApplicationCore, DataAccess, Identity, Order +1 | LOW |

Deployable/frontend artifacts of note: `APP-SVC-016` BlazorAdmin (non-deployable frontend SPA; 11 API call mappings — `APP-RISK-006`). High-coupling components flagged as decomposition obstacles: `APP-SVC-022` EfRepository (coupling 16) and `APP-SVC-020` UriComposer (coupling 8).

### 3.2 Data-ownership inputs (which context owns which entity)

From `data.repositories` and `cross_links.entity_to_service` (16 links):

| DbContext / repository | Owns (evidence-cited) | Inferred (review) |
| --- | --- | --- |
| `DATA-REPO-003` CatalogContext | CatalogItem, CatalogBrand, CatalogType, Basket, BasketItem, Order, OrderItem | — |
| `DATA-REPO-004` AppIdentityDbContext | ApplicationUser, Role | Role ownership inferred via Identity schema (`ASSUMP-006`, conf 0.7) |
| `DATA-REPO-001` IRepository<T> | CatalogItem, Basket | Order (`entities_served_inferred`, `OQ-008`) |
| `DATA-REPO-002` IReadRepository<T> | — | CatalogItem (`entities_served_inferred`, `OQ-008`) |

> **Caveat for FE:** `CatalogContext` (`DATA-REPO-003`) currently persists entities spanning Catalog, Basket, and Order — a single physical DbContext crossing three candidate contexts. This is a data-ownership input to any decomposition, not a recommendation.

### 3.3 The dependency cycle as a decomposition input

`APP-DEP-001` records a **module dependency cycle**: Admin → ApplicationCore → Basket → Catalog → DataAccess → Identity → Order → Web → (back to Admin). Whether this is a true runtime cycle or a static-resolution artifact is **unresolved** (`OQ-004`). Any context boundary proposal must account for or first resolve this cycle.

---

## 4. Contracts to Preserve & Data to Migrate

### 4.1 API contracts (from `application.apis` + `cross_links.service_to_api`)

55 API nodes (`APP-API-001..055`). Each carries `deployable_unit`, `handler`, `preserve_redesign_review`, and `confidence`.

**PublicApi REST contracts — flagged `preserve`, HIGH confidence (strongest preservation inputs):**

| API ID | Method / path | Handler | Notes |
| --- | --- | --- | --- |
| `APP-API-001` | POST `/api/authenticate` | AuthenticateEndpoint | issues JWT; ITokenClaimsService + SignInManager |
| `APP-API-002` | GET `/api/catalog-brands` | CatalogBrandListEndpoint | |
| `APP-API-003` | GET `/api/catalog-items/{catalogItemId}` | CatalogItemGetByIdEndpoint | |
| `APP-API-004` | GET `/api/catalog-items` | CatalogItemListPagedEndpoint | |
| `APP-API-005` | POST `/api/catalog-items` | CreateCatalogItemEndpoint | |
| `APP-API-006` | DELETE `/api/catalog-items/{catalogItemId}` | DeleteCatalogItemEndpoint | |
| `APP-API-007` | PUT `/api/catalog-items` | UpdateCatalogItemEndpoint | |
| `APP-API-008` | GET `/api/catalog-types` | CatalogTypeListEndpoint | |

**Web (MVC/Razor) user-facing contracts — `preserve`, HIGH confidence:** `/Manage/*` identity flows (`APP-API-014..034`), `/Order/MyOrders` & `/Order/Detail/{orderId}` (`APP-API-035`, `APP-API-036`), `/User` & `/User/Logout` (`APP-API-037`, `APP-API-038`).

**Flagged `review` (LOW/MEDIUM confidence — verify before preserving):** conventional/route/SPA-fallback and CLI bootstrap entries `APP-API-009`, `APP-API-010`, `APP-API-011`, `APP-API-051`, `APP-API-053`, `APP-API-054`, `APP-API-055`; BlazorAdmin routes `APP-API-039` (`/logout`), `APP-API-040` (`/admin`). Razor Page GETs `APP-API-041..052` are `preserve` but LOW confidence. See `OQ-009`: ROUTE/CLI method labels are synthetic classifications (`method_note`), not extracted HTTP verbs.

### 4.2 Interface/port abstractions to preserve (from `application.interfaces`)

| Interface ID | Name | Kind | Implemented by (evidence) |
| --- | --- | --- | --- |
| `APP-IF-001` | IRepository<T> | abstraction | EfRepository |
| `APP-IF-002` | IReadRepository<T> | abstraction | EfRepository |
| `APP-IF-003` | ITokenClaimsService | port | IdentityTokenClaimService |
| `APP-IF-004` | IUriComposer | abstraction | UriComposer |
| `APP-IF-005` | IAppLogger<T> | abstraction | (none in evidence) |
| `APP-IF-006` | IBasketService | abstraction | (none in evidence) |
| `APP-IF-007` | IBasketQueryService | abstraction | (none in evidence) |
| `APP-IF-008` | IEmailSender | port | (none in evidence) |
| `APP-IF-009` | IAggregateRoot | abstraction (DDD marker) | (none in evidence) |
| `APP-IF-010` | ICatalogItemService | abstraction | CachedCatalogItemServiceDecorator |
| `APP-IF-011` | ICatalogLookupDataService | abstraction | CachedCatalogLookupDataServiceDecorator |
| `APP-IF-012` | IMediator | external (MediatR) | (external) |
| `APP-IF-013` | CustomAuthStateProvider | UI | CustomAuthStateProvider |

> Empty `implemented_by` entries indicate the abstraction is declared but no concrete implementation was found in evidence — an input requiring verification, not a gap to fill blindly.

### 4.3 Data to migrate (from `data.entities` + `data.aggregates`)

**Persisted / implemented entities (migration candidates):**

| Entity ID | Name | PII | Confidence |
| --- | --- | --- | --- |
| `DATA-ENT-001` | CatalogItem | no | 0.8 |
| `DATA-ENT-002` | CatalogBrand | no | 0.8 |
| `DATA-ENT-003` | CatalogType | no | 0.8 |
| `DATA-ENT-004` | Basket | no | 0.8 |
| `DATA-ENT-005` | BasketItem | no | 0.8 |
| `DATA-ENT-006` | Order | **yes** | 0.8 |
| `DATA-ENT-007` | OrderItem | no | 0.8 |
| `DATA-ENT-008` | ApplicationUser | **yes** | 0.7 |
| `DATA-ENT-009` | Role | no | 0.7 |
| `DATA-ENT-012` | CatalogItemOrdered (owned) | no | 0.78 |
| `DATA-ENT-013` | Address (owned) | **yes** | 0.75 |
| `DATA-ENT-015` | BaseEntity | no | 0.8 (base class, not persisted) |

**Aspirational / unimplemented (NOT current migration data — design inputs only):** `DATA-ENT-010` Buyer, `DATA-ENT-011` PaymentMethod, `DATA-ENT-014` CatalogItemDetails; and the `DATA-AGG-003` BuyerAggregate.

**Aggregates (migration grouping inputs):** `DATA-AGG-001` BasketAggregate (Basket, BasketItem); `DATA-AGG-002` OrderAggregate (Order, OrderItem, Address, CatalogItemOrdered); `DATA-AGG-004` CatalogItem (single-entity — kept separate from entity `DATA-ENT-001` per `OQ-006`). PII-bearing data (`DATA-ENT-006`, `DATA-ENT-008`, `DATA-ENT-013`) requires migration/compliance handling.

---

## 5. Readiness, Risks & Open Questions Feeding FE

### 5.1 Open questions (from `open_questions`)

| ID | Question | Recorded resolution / status |
| --- | --- | --- |
| `OQ-001` | Merge Admin module (`APP-SVC-005`) with BlazorAdmin deployable (`APP-SVC-016`)? | Kept **separate** pending human review (conservative). |
| `OQ-002` | PublicApi listening port: EXPOSE 80/443 vs compose 8080? | Runtime binding 8080 better-evidenced; EXPOSE 80/443 treated as stale. Both recorded. |
| `OQ-003` | Active EF Core provider: PostgreSQL vs SQL Server / Azure SQL Edge? | Per-environment: Postgres (`TECH-CUR-007`) default/local; SQL Server (`TECH-CUR-006`) Docker-only. Both ACTIVE in scope. |
| `OQ-004` | Is the module cycle (`APP-DEP-001`) real or a static artifact? | **Unresolved** — needs human review. |
| `OQ-005` | Is JWT/auth enforced on PublicApi; is there a CORS policy? | **Unresolved** — kept as High findings `TECH-SEC-010`, `TECH-SEC-011`; not promoted to implemented controls. |
| `OQ-006` | Does aggregate `DATA-AGG-004` duplicate entity `DATA-ENT-001`? | Kept **separate** (different node kinds). |
| `OQ-007` | Authoritative system name? | Use 'eShopOnWeb' label with explicit 'unknown' caveat in metadata. |
| `OQ-008` | Does IRepository<T> serve Order; which entity does IReadRepository<T> serve? | Demoted to inference (`entities_served_inferred`); not directly evidenced. |
| `OQ-009` | Are ROUTE/CLI HTTP-method values evidence-backed verbs? | No — synthetic labels; `method_note` marks them; source records `method=unknown`. |

### 5.2 Application dependency / cycle / violation inputs (from `application.dependencies`)

- `APP-DEP-001` — module dependency **cycle** (see §3.3; `OQ-004`).
- `APP-DEP-002..008` — direct endpoint/PageModel → EfRepository layering violations (ARCH-VIOL-001..007): `CatalogBrandListEndpoint`, `CatalogItemGetByIdEndpoint`, `CreateCatalogItemEndpoint`, `DeleteCatalogItemEndpoint`, `UpdateCatalogItemEndpoint`, `CatalogTypeListEndpoint`, `IndexModel`.
- `APP-DEP-009` — EfRepository high coupling (score 16, ARCH-VIOL-009).
- `APP-DEP-010` — UriComposer high coupling (score 8, ARCH-VIOL-010).
- `APP-DEP-011..019` — project/package/runtime references (e.g. `APP-DEP-011` Web → PublicApi has no project reference; `APP-DEP-019` Web/PublicApi → sqlserver runtime TCP).

### 5.3 Technology version-unknown / undeclared gaps (from `technology.current_stack`)

Most stack nodes carry **undeclared or unknown versions** (LOW confidence) — a precise version baseline is **not** available from evidence:

- Versions `(not declared)`, LOW confidence: `TECH-CUR-004 … TECH-CUR-019`, `TECH-CUR-024`, `TECH-CUR-025` (EF Core, providers, MediatR, AutoMapper, Swashbuckle, FluentValidation, Blazor client libs, tooling, test tooling, etc.).
- Versions `unknown`, LOW confidence: `TECH-CUR-021` PostgreSQL, `TECH-CUR-022` EF Core InMemory.
- Higher-confidence anchors: `TECH-CUR-001` .NET 8.0.x (HIGH), `TECH-CUR-002` ASP.NET Core 8.0 (HIGH), `TECH-CUR-003` Blazor WASM 8.0 (HIGH; package versions not declared).

### 5.4 Security baseline & findings (from `technology.security`)

**Controls present (inputs to preserve):** `TECH-SEC-001` ASP.NET Core Identity (cookie auth), `TECH-SEC-002` JWT Bearer, `TECH-SEC-003` Blazor WASM auth, `TECH-SEC-004` role/claims authorization; secrets mechanisms `TECH-SEC-005` (User Secrets), `TECH-SEC-006` (Azure Key Vault, referenced), `TECH-SEC-007` (Docker bind-mounted secrets).

**Findings to resolve before implementation (`type=finding`):** `TECH-SEC-008` hardcoded PostgreSQL creds; `TECH-SEC-009` hardcoded SQL Server SA password; `TECH-SEC-010` no JWT enforcement confirmed on PublicApi (`OQ-005`); `TECH-SEC-011` no CORS policy found (`OQ-005`); `TECH-SEC-012` no secret scanning in CI/CD; `TECH-SEC-013` SQL Server 1433 published to host; `TECH-SEC-014` no TLS for container traffic; `TECH-SEC-015` AllowedHosts `*` + TrustServerCertificate=true; `TECH-SEC-016` no SAST/dependency/container scanning; `TECH-SEC-017` no audit logging / compliance controls.

### 5.5 Assumptions to honor (from `assumptions`)

Merged/normalized nodes carry `merged_from` facets and can be split if a reviewer disagrees: `ASSUMP-001` (Web module+deployable → `APP-SVC-006`), `ASSUMP-002` (PublicApi → `APP-SVC-011`), `ASSUMP-003` (ApplicationCore/Infrastructure/SharedContracts merges), `ASSUMP-004` (route ownership by `source_file`), `ASSUMP-005` (LOW/MEDIUM process→entity links), `ASSUMP-006` (Role ownership inferred), `ASSUMP-007` (system-name labeling).

---

## 6. Out of Scope for This Package

This foundation package deliberately **excludes**:

- **No code.** No source, snippets, scaffolding, or generated artifacts.
- **No target architecture beyond what evidence names.** `technology.target_stack` is empty (0 nodes); no target stack, no migration design, no new bounded-context decisions. Section 3 lists decomposition **candidates from evidence only**.
- **No new facts.** Nothing is added that is not already in the verified graph; cross-links exist only where a source file supports them.
- **No resolution of open questions.** `OQ-001 … OQ-009` are carried forward as inputs; this document does not decide them.
- **No elevation of confidence/status.** LOW/MEDIUM/inferred/aspirational/version-unknown signals are preserved as recorded; aspirational entities (`DATA-ENT-010/011/014`, `DATA-AGG-003`) and unconfirmed controls (`TECH-SEC-010/011`) are **not** treated as implemented.

Forward-engineering decisions (target stack, decomposition, API redesign, data migration plans) are the responsibility of a later stage that consumes these inputs.
