# Forward Engineering Input Map

Generated from evidence packs only. This is application-architecture input for future design, not a future technology decision.

## 1. Candidate Future Modules/Services

Ready or lower-risk candidates from current evidence: none detected.

Modules needing refactoring or review before becoming separate services: MOD-001 Admin, MOD-002 ApplicationCore, MOD-003 Basket, MOD-004 Catalog, MOD-006 DataAccess, MOD-007 Identity, MOD-009 Order, MOD-013 Web.

## 2. Existing APIs To Preserve Or Redesign

Preserve behavior or explicitly redesign these detected interfaces:

- POST /api/authenticate (owner: COMP-0221 AuthenticateEndpoint; module: MOD-007 Identity; file: src/PublicApi/AuthEndpoints/AuthenticateEndpoint.cs)
- GET /api/catalog-brands (owner: COMP-0118 CatalogBrandListEndpoint; module: MOD-004 Catalog; file: src/PublicApi/CatalogBrandEndpoints/CatalogBrandListEndpoint.cs)
- GET /api/catalog-items/{catalogItemId} (owner: COMP-0122 CatalogItemGetByIdEndpoint; module: MOD-004 Catalog; file: src/PublicApi/CatalogItemEndpoints/CatalogItemGetByIdEndpoint.cs)
- GET /api/catalog-items (owner: COMP-0223 CatalogItemListPagedEndpoint; module: MOD-004 Catalog; file: src/PublicApi/CatalogItemEndpoints/CatalogItemListPagedEndpoint.cs)
- POST /api/catalog-items (owner: COMP-0128 CreateCatalogItemEndpoint; module: MOD-004 Catalog; file: src/PublicApi/CatalogItemEndpoints/CreateCatalogItemEndpoint.cs)
- DELETE /api/catalog-items/{catalogItemId} (owner: COMP-0131 DeleteCatalogItemEndpoint; module: MOD-004 Catalog; file: src/PublicApi/CatalogItemEndpoints/DeleteCatalogItemEndpoint.cs)
- PUT /api/catalog-items (owner: COMP-0134 UpdateCatalogItemEndpoint; module: MOD-004 Catalog; file: src/PublicApi/CatalogItemEndpoints/UpdateCatalogItemEndpoint.cs)
- GET /api/catalog-types (owner: COMP-0137 CatalogTypeListEndpoint; module: MOD-004 Catalog; file: src/PublicApi/CatalogTypeEndpoints/CatalogTypeListEndpoint.cs)
- unknown /{controller:slugify=Home}/{action:slugify=Index}/{id?} (owner: COMP-0140 Program; module: MOD-005 CrossCutting; file: src/Web/Program.cs)
- unknown ASP.NET Razor Pages route registration (owner: COMP-0140 Program; module: MOD-005 CrossCutting; file: src/Web/Program.cs)
- GET /home_page_health_check (owner: COMP-0140 Program; module: MOD-005 CrossCutting; file: src/Web/Program.cs)
- GET /api_health_check (owner: COMP-0140 Program; module: MOD-005 CrossCutting; file: src/Web/Program.cs)
- GET /Manage/MyAccount (owner: COMP-0153 ManageController; module: MOD-007 Identity; file: src/Web/Controllers/ManageController.cs)
- POST /Manage/MyAccount (owner: COMP-0153 ManageController; module: MOD-007 Identity; file: src/Web/Controllers/ManageController.cs)
- POST /Manage/SendVerificationEmail (owner: COMP-0153 ManageController; module: MOD-007 Identity; file: src/Web/Controllers/ManageController.cs)
- GET /Manage/ChangePassword (owner: COMP-0153 ManageController; module: MOD-007 Identity; file: src/Web/Controllers/ManageController.cs)
- POST /Manage/ChangePassword (owner: COMP-0153 ManageController; module: MOD-007 Identity; file: src/Web/Controllers/ManageController.cs)
- GET /Manage/SetPassword (owner: COMP-0153 ManageController; module: MOD-007 Identity; file: src/Web/Controllers/ManageController.cs)
- POST /Manage/SetPassword (owner: COMP-0153 ManageController; module: MOD-007 Identity; file: src/Web/Controllers/ManageController.cs)
- GET /Manage/ExternalLogins (owner: COMP-0153 ManageController; module: MOD-007 Identity; file: src/Web/Controllers/ManageController.cs)

## 3. Call Flows To Preserve Behaviorally

Evidence contains 55 traced-from-dependency-candidate flows and 0 partial flows.

Traced flows with evidence:

- POST /api/authenticate (status: traced_from_dependency_candidates; confidence: 0.74)
- GET /api/catalog-brands (status: traced_from_dependency_candidates; confidence: 0.74)
- GET /api/catalog-items/{catalogItemId} (status: traced_from_dependency_candidates; confidence: 0.82)
- GET /api/catalog-items (status: traced_from_dependency_candidates; confidence: 0.82)
- POST /api/catalog-items (status: traced_from_dependency_candidates; confidence: 0.82)
- DELETE /api/catalog-items/{catalogItemId} (status: traced_from_dependency_candidates; confidence: 0.82)
- PUT /api/catalog-items (status: traced_from_dependency_candidates; confidence: 0.82)
- GET /api/catalog-types (status: traced_from_dependency_candidates; confidence: 0.74)
- unknown /{controller:slugify=Home}/{action:slugify=Index}/{id?} (status: traced_from_dependency_candidates; confidence: 0.82)
- unknown ASP.NET Razor Pages route registration (status: framework_route_coverage_marker; confidence: 0.7799999999999999)

## 4. Architecture Violations Not To Carry Forward

Do not blindly carry forward these risk-backed concerns:

- APP-RISK-001: Module candidate Catalog has weak or uncertain boundary evidence with coupling score 13.
- APP-RISK-002: Module dependency cycle detected: Admin -> ApplicationCore -> Basket -> Catalog -> DataAccess -> Identity -> Order -> Web
- APP-RISK-003: High-coupling module candidates include Catalog, Basket, Identity, Web, ApplicationCore.
- APP-RISK-004: EfRepository is a high-coupling component candidate with total coupling 16.
- APP-RISK-005: 0 call flows are partial because parsed evidence did not fully resolve runtime dispatch and downstream calls.
- APP-RISK-006: Frontend application evidence contains 11 API call mappings from BlazorAdmin.

## 5. Risks To Resolve Before Implementation

- APP-RISK-001: Module candidate Catalog has weak or uncertain boundary evidence with coupling score 13. (module: Catalog; components: unknown; dependency refs: DEP-0001, DEP-0002, DEP-0007, DEP-0008; evidence: architecture-output/evidence-packs/module-boundary-pack.json)
- APP-RISK-002: Module dependency cycle detected: Admin -> ApplicationCore -> Basket -> Catalog -> DataAccess -> Identity -> Order -> Web (module: Admin, ApplicationCore, Basket, Catalog, DataAccess, Identity, Order, Web; components: unknown; dependency refs: DEP-0001, DEP-0002, DEP-0003, DEP-0004; evidence: architecture-output/evidence-packs/dependency-pack.json)
- APP-RISK-003: High-coupling module candidates include Catalog, Basket, Identity, Web, ApplicationCore. (module: multiple; components: unknown; dependency refs: DEP-0001, DEP-0002, DEP-0003, DEP-0004; evidence: architecture-output/evidence-packs/dependency-pack.json)
- APP-RISK-004: EfRepository is a high-coupling component candidate with total coupling 16. (module: unknown; components: COMP-0087 EfRepository; dependency refs: DEP-0001, DEP-0002, DEP-0003, DEP-0004; evidence: architecture-output/evidence-packs/dependency-pack.json)
- APP-RISK-005: 0 call flows are partial because parsed evidence did not fully resolve runtime dispatch and downstream calls. (module: multiple; components: unknown; dependency refs: DEP-0001, DEP-0002, DEP-0003, DEP-0004; evidence: architecture-output/evidence-packs/call-flow-pack.json)
- APP-RISK-006: Frontend application evidence contains 11 API call mappings from BlazorAdmin. (module: multiple; components: unknown; dependency refs: DEP-0001, DEP-0002, DEP-0003, DEP-0004; evidence: architecture-output/evidence-packs/frontend-application-pack.json)
- APP-RISK-007: Controller-like component CatalogBrandListEndpoint depends directly on repository EfRepository. (module: DataAccess, Catalog; components: COMP-0118 CatalogBrandListEndpoint, COMP-0087 EfRepository; dependency refs: DEP-0001, DEP-0002, DEP-0007, DEP-0008; evidence: src/PublicApi/CatalogBrandEndpoints/CatalogBrandListEndpoint.cs)
- APP-RISK-008: 0 components have unknown module ownership and 40 components have unknown type classification. (module: unknown; components: unknown; dependency refs: DEP-0001, DEP-0002, DEP-0003, DEP-0004; evidence: architecture-output/evidence-packs/component-registry-pack.json)

## 6. Modules Needing Deeper Review

MOD-001 Admin, MOD-002 ApplicationCore, MOD-003 Basket, MOD-004 Catalog, MOD-006 DataAccess, MOD-007 Identity, MOD-009 Order, MOD-013 Web

## 7. Suggested First Modernization Candidates

Start with low-coupled, evidence-backed candidates: none detected. Defer blocked or unknown-readiness modules until cycles, shared dependencies, and call-flow gaps are reviewed.
