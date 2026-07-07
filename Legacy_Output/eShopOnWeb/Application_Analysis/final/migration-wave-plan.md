# Migration Wave Plan

This is a planning sequence derived from architecture evidence. It is not an implementation schedule.

## Wave 0 - Architecture Stabilization

Goals:

- confirm open questions
- review 0 partial call flows
- confirm external boundary ownership
- decide whether test-project components remain in final architecture views
- add contract tests for preserved APIs

API contracts to stabilize first:

- POST /api/authenticate (API-CONTRACT-001, owner COMP-0221 AuthenticateEndpoint)
- GET /api/catalog-brands (API-CONTRACT-002, owner COMP-0118 CatalogBrandListEndpoint)
- GET /api/catalog-items/{catalogItemId} (API-CONTRACT-003, owner COMP-0122 CatalogItemGetByIdEndpoint)
- GET /api/catalog-items (API-CONTRACT-004, owner COMP-0223 CatalogItemListPagedEndpoint)
- POST /api/catalog-items (API-CONTRACT-005, owner COMP-0128 CreateCatalogItemEndpoint)
- DELETE /api/catalog-items/{catalogItemId} (API-CONTRACT-006, owner COMP-0131 DeleteCatalogItemEndpoint)
- PUT /api/catalog-items (API-CONTRACT-007, owner COMP-0134 UpdateCatalogItemEndpoint)
- GET /api/catalog-types (API-CONTRACT-008, owner COMP-0137 CatalogTypeListEndpoint)
- GET /home_page_health_check (API-CONTRACT-012, owner COMP-0140 Program)
- GET /api_health_check (API-CONTRACT-013, owner COMP-0140 Program)
- GET /Manage/MyAccount (API-CONTRACT-014, owner COMP-0153 ManageController)
- POST /Manage/MyAccount (API-CONTRACT-015, owner COMP-0153 ManageController)

## Wave 1 - Low-Coupling Capability Modernization

Candidate capabilities:

- none detected

## Wave 2 - Shared Contract And UI/API Alignment

Goals:

- preserve or explicitly redesign frontend/API contracts
- map UI flows to preserved API contracts
- review all `review` API contracts before implementation

Review contracts:

API-CONTRACT-009 /{controller:slugify=Home}/{action:slugify=Index}/{id?}, API-CONTRACT-010 ASP.NET Razor Pages route registration, API-CONTRACT-011 /index.html, API-CONTRACT-039 /logout, API-CONTRACT-040 /admin, API-CONTRACT-051 /{handler?}, API-CONTRACT-053 .NET application bootstrap Program.cs, API-CONTRACT-054 .NET application bootstrap Program.cs, API-CONTRACT-055 .NET application bootstrap Program.cs

## Wave 3 - Data Ownership And Infrastructure Refactoring

Goals:

- identify entities and repositories shared across capabilities
- avoid extracting services with unresolved data ownership
- clarify persistence ownership before choosing service boundaries

## Wave 4 - High-Risk Capability Extraction Or Redesign

Defer until after earlier waves:

- CAP-001 Catalog: risks 3, weak modules 1, coupling 13
- CAP-002 Identity: risks 1, weak modules 1, coupling 8
- CAP-004 Admin: risks 1, weak modules 1, coupling 3
- CAP-005 Basket: risks 1, weak modules 1, coupling 9
- CAP-006 Controllers: risks 1, weak modules 1, coupling 7
- CAP-007 Order: risks 1, weak modules 1, coupling 4
- CAP-013 Data: risks 3, weak modules 1, coupling 5
