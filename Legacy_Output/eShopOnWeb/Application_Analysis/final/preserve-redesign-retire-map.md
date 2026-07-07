# Preserve / Redesign / Retire Map

## Preserve

Preserve behavior or provide explicit compatibility plans for these detected interfaces:

- API-CONTRACT-001: POST /api/authenticate owned by COMP-0221 AuthenticateEndpoint in CAP-002 Identity
- API-CONTRACT-002: GET /api/catalog-brands owned by COMP-0118 CatalogBrandListEndpoint in CAP-001 Catalog
- API-CONTRACT-003: GET /api/catalog-items/{catalogItemId} owned by COMP-0122 CatalogItemGetByIdEndpoint in CAP-001 Catalog
- API-CONTRACT-004: GET /api/catalog-items owned by COMP-0223 CatalogItemListPagedEndpoint in CAP-001 Catalog
- API-CONTRACT-005: POST /api/catalog-items owned by COMP-0128 CreateCatalogItemEndpoint in CAP-001 Catalog
- API-CONTRACT-006: DELETE /api/catalog-items/{catalogItemId} owned by COMP-0131 DeleteCatalogItemEndpoint in CAP-001 Catalog
- API-CONTRACT-007: PUT /api/catalog-items owned by COMP-0134 UpdateCatalogItemEndpoint in CAP-001 Catalog
- API-CONTRACT-008: GET /api/catalog-types owned by COMP-0137 CatalogTypeListEndpoint in CAP-001 Catalog
- API-CONTRACT-012: GET /home_page_health_check owned by COMP-0140 Program in CAP-010 Cross
- API-CONTRACT-013: GET /api_health_check owned by COMP-0140 Program in CAP-010 Cross
- API-CONTRACT-014: GET /Manage/MyAccount owned by COMP-0153 ManageController in CAP-002 Identity
- API-CONTRACT-015: POST /Manage/MyAccount owned by COMP-0153 ManageController in CAP-002 Identity
- API-CONTRACT-016: POST /Manage/SendVerificationEmail owned by COMP-0153 ManageController in CAP-002 Identity
- API-CONTRACT-017: GET /Manage/ChangePassword owned by COMP-0153 ManageController in CAP-002 Identity
- API-CONTRACT-018: POST /Manage/ChangePassword owned by COMP-0153 ManageController in CAP-002 Identity

## Redesign

Do not blindly carry these issues forward:

- APP-RISK-001: Module candidate Catalog has weak or uncertain boundary evidence with coupling score 13.
- APP-RISK-002: Module dependency cycle detected: Admin -> ApplicationCore -> Basket -> Catalog -> DataAccess -> Identity -> Order -> Web
- APP-RISK-003: High-coupling module candidates include Catalog, Basket, Identity, Web, ApplicationCore.
- APP-RISK-004: EfRepository is a high-coupling component candidate with total coupling 16.
- APP-RISK-005: 0 call flows are partial because parsed evidence did not fully resolve runtime dispatch and downstream calls.
- APP-RISK-006: Frontend application evidence contains 11 API call mappings from BlazorAdmin.
- APP-RISK-007: Controller-like component CatalogBrandListEndpoint depends directly on repository EfRepository.
- APP-RISK-008: 0 components have unknown module ownership and 40 components have unknown type classification.
- APP-RISK-009: External dependency candidates include sqlserver, catalog-items, catalog-items/{id}, catalog-items?PageSize=10, {_apiUrl}{uri}; target purposes may require review.

Architecture violations:

- ARCH-VIOL-001: Controller-like component CatalogBrandListEndpoint depends directly on repository EfRepository.
- ARCH-VIOL-002: Controller-like component CatalogItemGetByIdEndpoint depends directly on repository EfRepository.
- ARCH-VIOL-003: Controller-like component CreateCatalogItemEndpoint depends directly on repository EfRepository.
- ARCH-VIOL-004: Controller-like component DeleteCatalogItemEndpoint depends directly on repository EfRepository.
- ARCH-VIOL-005: Controller-like component UpdateCatalogItemEndpoint depends directly on repository EfRepository.
- ARCH-VIOL-006: Controller-like component CatalogTypeListEndpoint depends directly on repository EfRepository.
- ARCH-VIOL-007: Controller-like component IndexModel depends directly on repository EfRepository.
- ARCH-VIOL-008: Module dependency cycle detected: Admin -> ApplicationCore -> Basket -> Catalog -> DataAccess -> Identity -> Order -> Web
- ARCH-VIOL-009: Component EfRepository has high coupling score 16.
- ARCH-VIOL-010: Component UriComposer has high coupling score 8.

## Review

Review these before treating them as stable future design inputs:

- API-CONTRACT-009: unknown /{controller:slugify=Home}/{action:slugify=Index}/{id?} (Review before treating as a stable future contract.)
- API-CONTRACT-010: unknown ASP.NET Razor Pages route registration (Review before treating as a stable future contract.)
- API-CONTRACT-011: unknown /index.html (Review before treating as a stable future contract.)
- API-CONTRACT-039: unknown /logout (Review before treating as a stable future contract.)
- API-CONTRACT-040: unknown /admin (Review before treating as a stable future contract.)
- API-CONTRACT-051: GET /{handler?} (Review before treating as a stable future contract.)
- API-CONTRACT-053: unknown .NET application bootstrap Program.cs (Review before treating as a stable future contract.)
- API-CONTRACT-054: unknown .NET application bootstrap Program.cs (Review before treating as a stable future contract.)
- API-CONTRACT-055: unknown .NET application bootstrap Program.cs (Review before treating as a stable future contract.)

Capability boundaries needing review:

- CAP-001 Catalog: decision review_before_extraction, risks 3, weak modules 1
- CAP-002 Identity: decision review_before_extraction, risks 1, weak modules 1
- CAP-004 Admin: decision review_before_extraction, risks 1, weak modules 1
- CAP-005 Basket: decision review_before_extraction, risks 1, weak modules 1
- CAP-006 Controllers: decision review_before_extraction, risks 1, weak modules 1
- CAP-007 Order: decision review_before_extraction, risks 1, weak modules 1
- CAP-013 Data: decision review_before_extraction, risks 3, weak modules 1

## Retire

No component or API is marked for retirement from static architecture evidence alone. Retirement requires usage, telemetry, production logs, or explicit product-owner confirmation.
