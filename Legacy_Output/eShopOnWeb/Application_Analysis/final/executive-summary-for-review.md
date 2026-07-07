# Executive Summary For Review

## 1. Application Structure Detected

The repository contains 6 detected application/project records and 2 deployable candidates. The extracted architecture keeps the system name as `unknown` because the final inventory did not identify an authoritative product/system-name artifact.

Source-backed project structure:

- `src/PublicApi`: PublicApi (backend_web_api).
- `src/Web`: Web (backend_web_api).
- `src/BlazorAdmin`: BlazorAdmin (frontend_spa).
- `src/Infrastructure`: Infrastructure (database_project).
- `src/ApplicationCore`: ApplicationCore (library).
- `src/BlazorShared`: BlazorShared (library).

## 2. Main Deployable Units

Detected deployable units:

- `PublicApi`: backend_web_api, source `src/PublicApi`.
- `Web`: backend_web_api, source `src/Web`.

## 3. Main Modules

The extraction identified 13 module candidates. These are evidence-derived candidates, not confirmed business-owned bounded contexts.

Main/high-impact modules by component count and coupling include Catalog, Identity, Verification, Basket, Admin, Web, Order, ApplicationCore, SharedContracts, CrossCutting. Lower-coupled candidates include none detected.

## 4. Main Layers

Detected layers and component counts:

- API: 17
- Application: 69
- CrossCutting: 62
- DataAccess: 15
- Domain: 18
- Infrastructure: 9
- Integration: 2
- Presentation/UI: 115
- Unknown: 3

The Unknown count is material and should be reviewed before finalizing modernization boundaries.

## 5. Detected Architecture Pattern

Detected pattern: Layered Monolith.

Evidence:

- Deployable candidates: src/PublicApi, src/Web.
- Layer/component evidence: API=17, Application=69, CrossCutting=62, DataAccess=15, Domain=18, Infrastructure=9, Integration=2, Presentation/UI=115, and 1 more.
- Module evidence: Catalog, Identity, Verification, Basket, Admin, Web, Order, ApplicationCore, SharedContracts, CrossCutting.

Architecture style claims are limited to the generated source-backed artifacts; no future platform or deployment model is assumed.

## 6. Main Dependencies

The dependency graph contains 534 edges.

Highest-coupling modules: Catalog, Basket, Identity, Web, ApplicationCore, DataAccess, CrossCutting, Infrastructure, and 2 more.

Highest-coupling components: EfRepository, UriComposer.

Detected module cycles: 1.

## 7. Major Risks

- APP-RISK-001: Module candidate Catalog has weak or uncertain boundary evidence with coupling score 13.
- APP-RISK-002: Module dependency cycle detected: Admin -> ApplicationCore -> Basket -> Catalog -> DataAccess -> Identity -> Order -> Web
- APP-RISK-003: High-coupling module candidates include Catalog, Basket, Identity, Web, ApplicationCore.
- APP-RISK-004: EfRepository is a high-coupling component candidate with total coupling 16.
- APP-RISK-005: 0 call flows are partial because parsed evidence did not fully resolve runtime dispatch and downstream calls.
- APP-RISK-006: Frontend application evidence contains 11 API call mappings from BlazorAdmin.
- APP-RISK-007: Controller-like component CatalogBrandListEndpoint depends directly on repository EfRepository.
- APP-RISK-008: 0 components have unknown module ownership and 40 components have unknown type classification.

## 8. Best Migration Candidates

Best early candidates from current evidence: none detected.

These are better starting points because they have lower coupling and observable interfaces.

## 9. Poor Migration Candidates

Poor first candidates: Admin, ApplicationCore, Basket, Catalog, DataAccess, Identity, Order, Web.

These should be deferred until dependency direction, repository ownership, and call-flow gaps are clarified.

## 10. Key Open Questions

1. Confirm the authoritative system name; evidence packs leave system_name as unknown.
2. Confirm ownership and boundaries for weak or unknown module candidates: Admin, ApplicationCore, Basket, Catalog, DataAccess, Identity, Order, Web.
3. Review the 0 components with unknown module ownership before finalizing module boundaries.
4. Review the 40 components with Unknown type/layer classification to decide whether they are architecture-significant.
5. Review 0 partial call flows before using them as behavior-preservation contracts.
6. Confirm whether detected module cycles are real architecture cycles or artifacts of static dependency resolution: Admin -> ApplicationCore -> Basket -> Catalog -> DataAccess -> Identity -> Order -> Web.
7. Confirm deployment ownership for detected frontend applications: BlazorAdmin.
8. Confirm whether detected database/infrastructure services are development-only or production-relevant external boundaries.
9. Confirm the target systems and purposes behind configured HTTP/API base URLs and health-check dependencies: sqlserver, catalog-items, catalog-items/{id}, catalog-items?PageSize=10, {_apiUrl}{uri}.
10. Confirm whether no scheduled jobs/message consumers exist; none were detected in parsed facts.

## 11. How This Supports SDLC Reverse Engineering

This output gives SDLC teams a source-backed architecture baseline for the existing application:

- Identifies applications/projects and deployable units.
- Maps candidate modules, components, entry points, dependencies, call flows, and layers.
- Shows architecture risks, violations, coupling, cycles, and unknowns.
- Provides evidence-backed JSON artifacts suitable for downstream analysis and review tooling.
- Keeps uncertainty explicit in `open-questions.md` instead of converting gaps into assumptions.

## 12. How This Supports Forward Engineering

This output gives forward-engineering teams practical modernization input:

- Preserve or explicitly redesign detected APIs, frontend routes, bootstrap entry points, and partial call flows.
- Start modernization review with lower-coupled candidates such as none detected.
- Defer high-coupling/cyclic areas such as Admin, ApplicationCore, Basket, Catalog, DataAccess, Identity, Order, Web.
- Avoid carrying forward detected layer violations, unresolved module cycles, and unclear module boundaries.
- Resolve partial call flows, shared data-access ownership, and external boundary ownership before committing to future service boundaries.
