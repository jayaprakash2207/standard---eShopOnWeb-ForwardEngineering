# Application Architecture Summary

## 1. System Overview

The repository contains 6 detected application/support project records and 2 deployable unit candidates. The authoritative system name is unknown in the evidence, so final artifacts keep `system_name` as `unknown`.

Evidence: `system-inventory-pack.json` detects 6 projects and deployable units PublicApi, Web.

Source anchors: src/PublicApi/PublicApi.csproj, src/Web/Web.csproj, src/BlazorAdmin/BlazorAdmin.csproj, src/ApplicationCore/ApplicationCore.csproj, src/BlazorShared/BlazorShared.csproj, src/Infrastructure/Infrastructure.csproj.

## 2. Detected Application Style

Detected style: Layered Monolith. Secondary candidates: Clean Architecture, Modular Monolith. The pattern statement is based on project/deployable evidence and detected component layers.

## 3. Deployable Units

Deployable units detected: PublicApi, Web. Deployment/build clues are retained in `system-inventory.json` and `system-inventory-pack.json`.

## 4. Main Modules

Module candidates are evidence-derived, not final business-owned bounded contexts. Largest candidates by component count:

- Catalog: 25 components, 9 entry points, boundary Weak
- Identity: 25 components, 29 entry points, boundary Weak
- Verification: 25 components, 0 entry points, boundary Medium
- Admin: 23 components, 2 entry points, boundary Weak
- Basket: 23 components, 3 entry points, boundary Weak
- Order: 21 components, 2 entry points, boundary Weak
- Web: 21 components, 3 entry points, boundary Weak
- ApplicationCore: 13 components, 0 entry points, boundary Weak

Representative module evidence: Catalog uses src/ApplicationCore/CatalogSettings.cs, Identity uses src/ApplicationCore/Constants/AuthorizationConstants.cs, Verification uses tests/FunctionalTests/PublicApi/ApiTestFixture.cs, Admin uses src/BlazorAdmin/App.razor, Basket uses src/ApplicationCore/Entities/BasketAggregate/Basket.cs.

## 5. Main Layers

Detected layer counts: {"API": 17, "Application": 69, "CrossCutting": 62, "DataAccess": 15, "Domain": 18, "Infrastructure": 9, "Integration": 2, "Presentation/UI": 115, "Unknown": 3}.

## 6. Main Interfaces

Entry points detected: {"CLI": 3, "FrontendRoute": 3, "HTTP_API": 49}. Representative HTTP APIs: POST /api/authenticate, GET /api/catalog-brands, GET /api/catalog-items/{catalogItemId}, GET /api/catalog-items, POST /api/catalog-items, DELETE /api/catalog-items/{catalogItemId}, PUT /api/catalog-items, GET /api/catalog-types. Representative frontend routes: /index.html, /logout, /admin.

Representative interface evidence is retained in `application-interface-catalogue.json` and `entry-point-pack.json`.

## 7. Major Dependencies

Dependency evidence contains 534 graph edges. High-coupling modules include Catalog, Basket, Identity, Web, ApplicationCore, DataAccess. High-coupling components include EfRepository, UriComposer.

## 8. Architecture Pattern

Primary pattern: Layered Monolith with confidence 0.78. Service separation is not claimed unless deployable and dependency evidence supports it.

Pattern evidence anchors: src/PublicApi/PublicApi.csproj, src/Web/Web.csproj, src/BlazorAdmin/BlazorAdmin.csproj, src/ApplicationCore/ApplicationCore.csproj, src/BlazorShared/BlazorShared.csproj, src/Infrastructure/Infrastructure.csproj.

## 9. Architecture Risks

Top risks:

- APP-RISK-001: Module candidate Catalog has weak or uncertain boundary evidence with coupling score 13.
- APP-RISK-002: Module dependency cycle detected: Admin -> ApplicationCore -> Basket -> Catalog -> DataAccess -> Identity -> Order -> Web
- APP-RISK-003: High-coupling module candidates include Catalog, Basket, Identity, Web, ApplicationCore.
- APP-RISK-004: EfRepository is a high-coupling component candidate with total coupling 16.
- APP-RISK-005: 0 call flows are partial because parsed evidence did not fully resolve runtime dispatch and downstream calls.
- APP-RISK-006: Frontend application evidence contains 11 API call mappings from BlazorAdmin.

## 10. Migration/Forward-Engineering Implications

Start with lower-coupled candidates: none detected. Defer blocked or unknown-readiness candidates until module boundaries, dependency direction, and call-flow gaps are reviewed: Admin, ApplicationCore, Basket, Catalog, DataAccess, Identity, Order, Web.

## 11. Open Questions Summary

There are 13 open questions. The most important are system name, candidate module boundaries, route/call-flow coverage, partial call flows, module cycles, and external boundary ownership.
