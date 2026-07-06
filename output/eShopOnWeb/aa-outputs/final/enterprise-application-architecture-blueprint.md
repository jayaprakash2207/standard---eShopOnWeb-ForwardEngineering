# Enterprise Application Architecture Blueprint

## 1. Purpose

This document is the implementation-oriented Application Architecture blueprint for forward engineering this repository. It is written as if a team were rebuilding the application from scratch, but every major input is derived from generated reverse-engineering evidence.

The goal is not to copy the legacy code line-for-line. The goal is to preserve externally visible behavior and proven architectural responsibilities while redesigning weak boundaries, high coupling, and violations.

Source artifacts used:

- architecture-output/inventory/project-inventory.json
- architecture-output/final/system-inventory.json
- architecture-output/final/module-boundary-map.json
- architecture-output/final/component-registry.json
- architecture-output/final/dependency-graph.json
- architecture-output/final/application-interface-catalogue.json
- architecture-output/final/call-flow-map.json
- architecture-output/final/architecture-violation-register.json
- architecture-output/final/application-risk-register.json
- architecture-output/final/business-capability-map.json
- architecture-output/final/module-consolidation-map.json
- architecture-output/final/api-contract-preservation-map.json
- architecture-output/final/test-runtime-evidence-map.json
- architecture-output/evidence-packs/layering-pattern-pack.json
- architecture-output/evidence-packs/external-boundary-pack.json
- architecture-output/evidence-packs/frontend-application-pack.json

## 2. Architecture Vision

Architecture type: `Application Architecture`

Detected system name: `unknown`

Detected application shape: 6 application/support project records with 2 deployable unit candidates.

Forward-engineering outcome: Preserve externally visible behavior and implementation-critical flows while redesigning weak boundaries, high coupling, and detected architecture violations.

System name remains `unknown` because no authoritative source-backed system-name artifact was found.

## 3. Application Design Overview

Design narrative:

- The application is organized as a layered .NET solution with web-facing deployables and supporting libraries. Detected deployable candidates are PublicApi, Web; supporting project candidates include ApplicationCore, BlazorShared, Infrastructure, BlazorAdmin.
- Invocation enters through HTTP APIs, MVC/Razor-style web routes, frontend routes, and executable bootstrap Program.cs files. The target build should keep these invocation adapters thin and move workflow orchestration into application services, handlers, or explicitly reviewed module APIs.
- Domain and application concerns are primarily represented through entity, service, handler, specification, repository-interface, and shared-contract components. Infrastructure concerns are represented through EF Core/data configuration, repository implementation, identity/token services, and external or frontend API clients.
- The legacy evidence shows useful patterns that should influence the target design, but weak boundaries, direct endpoint-to-repository dependencies, and module cycles should be redesigned rather than copied.

Target design posture:

- Preserve public contracts and behavior before changing implementation internals.
- Use the detected layered architecture as the first target decomposition model.
- Treat modules as candidate boundaries until data ownership and coupling questions are reviewed.
- Keep UI/API adapters thin; place business workflow in application/domain services or handlers.
- Isolate persistence and integrations behind interfaces/adapters.

Technology/style clues found in project evidence:

- Ardalis.ApiEndpoints
- Ardalis.Specification
- Ardalis.Specification.EntityFrameworkCore
- Azure.Identity
- BlazorInputFile
- Blazored.LocalStorage
- FluentValidation
- MediatR
- Microsoft.AspNetCore.Authentication.JwtBearer
- Microsoft.AspNetCore.Components.Authorization
- Microsoft.AspNetCore.Components.WebAssembly
- Microsoft.AspNetCore.Components.WebAssembly.Authentication
- Microsoft.AspNetCore.Components.WebAssembly.DevServer
- Microsoft.AspNetCore.Components.WebAssembly.Server
- Microsoft.AspNetCore.Diagnostics.EntityFrameworkCore
- Microsoft.AspNetCore.Identity.EntityFrameworkCore
- Microsoft.AspNetCore.Identity.UI
- Microsoft.EntityFrameworkCore.InMemory
- Microsoft.EntityFrameworkCore.SqlServer
- Microsoft.EntityFrameworkCore.Tools
- Microsoft.Extensions.Identity.Core
- MinimalApi.Endpoint
- Npgsql.EntityFrameworkCore.PostgreSQL
- Swashbuckle.AspNetCore.SwaggerUI
- System.IdentityModel.Tokens.Jwt

## 4. Pattern And Style Catalogue

This catalogue is the main design interpretation layer. It explains the implementation styles found in the legacy code and how they should influence a new build.

| Pattern / Style | What It Means In This Application | Target Implementation Guidance | Evidence | Confidence |
|---|---|---|---|---:|
| Layered Monolith / Layered Application | The application is organized into API/UI, Application, Domain, Infrastructure/DataAccess, Integration, and CrossCutting concerns inside one repository/solution. | Use layered boundaries as the implementation baseline, then remove direct API/UI-to-data access dependencies before target sign-off. | Multiple projects/layers detected within one solution/repository and shared deployable units. | 0.78 |
| Clean Architecture influence | Core/domain abstractions are separated from infrastructure implementations, although evidence shows some boundary weakness. | Keep domain/application contracts inward-facing and make infrastructure implement adapters; review violations before copying structure. | Projects/layers include ApplicationCore, Infrastructure, Domain, Application, DataAccess, and Integration evidence. | 0.72 |
| Repository Pattern | Persistence access is represented through repository components/interfaces and shared repository implementations. | Preserve repository/query abstractions, but avoid direct endpoint-to-repository coupling in the target design. | IReadRepository (Repository) [src/ApplicationCore/Interfaces/IReadRepository.cs], IRepository (Repository) [src/ApplicationCore/Interfaces/IRepository.cs], BasketWithItemsSpecification (Repository) [src/ApplicationCore/Specifications/BasketWithItemsSpecification.cs], and 2 more | 0.86 |
| Specification Pattern | Query/filter rules are expressed as reusable specification components or supported by the Ardalis.Specification package. | Use specifications for reusable query intent, but keep them owned by the module/data model they describe. | BasketWithItemsSpecification (Repository) [src/ApplicationCore/Specifications/BasketWithItemsSpecification.cs], CatalogFilterPaginatedSpecification (Repository) [src/ApplicationCore/Specifications/CatalogFilterPaginatedSpecification.cs], CatalogFilterSpecification (Repository) [src/ApplicationCore/Specifications/CatalogFilterSpecification.cs], and 2 more | 0.84 |
| Endpoint / Handler-style API | Some API routes are implemented as endpoint classes with HandleAsync/AddRoute-style behavior instead of only conventional MVC controllers. | Model target APIs as explicit request handlers/endpoints with thin mapping and application-service delegation. | AuthenticateEndpoint (Controller) [src/PublicApi/AuthEndpoints/AuthenticateEndpoint.cs], CatalogBrandListEndpoint (Controller) [src/PublicApi/CatalogBrandEndpoints/CatalogBrandListEndpoint.cs], CatalogItemGetByIdEndpoint (Controller) [src/PublicApi/CatalogItemEndpoints/CatalogItemGetByIdEndpoint.cs], and 2 more | 0.86 |
| MVC / Razor Pages Web UI | Web-facing routes include controller/page-style components, especially around account/manage and web storefront behavior. | Preserve user-visible routes or intentionally remap them; keep controllers/page models thin. | AuthenticateEndpoint (Controller) [src/PublicApi/AuthEndpoints/AuthenticateEndpoint.cs], CatalogBrandListEndpoint (Controller) [src/PublicApi/CatalogBrandEndpoints/CatalogBrandListEndpoint.cs], CatalogItemGetByIdEndpoint (Controller) [src/PublicApi/CatalogItemEndpoints/CatalogItemGetByIdEndpoint.cs], and 2 more | 0.78 |
| Blazor frontend component/service style | Frontend behavior is represented through Blazor/Razor components and frontend services that call backend APIs. | Preserve route/API contracts and rebuild frontend state/API service patterns explicitly. | BlazorComponent (FrontendComponent) [src/BlazorAdmin/Helpers/BlazorComponent.cs], BlazorLayoutComponent (FrontendComponent) [src/BlazorAdmin/Helpers/BlazorLayoutComponent.cs], ToastComponent (FrontendComponent) [src/BlazorAdmin/Helpers/ToastComponent.cs], and 2 more | 0.82 |
| Dependency Injection and Constructor Injection | Components express dependencies through constructors, DI registrations, and injected Razor/frontend services. | Use DI as the composition mechanism, but keep dependency direction aligned with target layers. | CatalogBrand (Entity) [src/ApplicationCore/Entities/CatalogBrand.cs], CatalogItem (Entity) [src/ApplicationCore/Entities/CatalogItem.cs], CatalogItemDetails (Entity) [src/ApplicationCore/Entities/CatalogItem.cs], and 2 more | 0.9 |
| EF Core Data Access / ORM Configuration | Persistence is implemented through EF Core-style contexts, entity configurations, repositories, and database support. | Keep EF Core in infrastructure/data-access adapters and confirm data ownership before service/module extraction. | CatalogContext (Repository) [src/Infrastructure/Data/CatalogContext.cs], CatalogContextSeed (BatchJob) [src/Infrastructure/Data/CatalogContextSeed.cs], BasketConfiguration (Configuration) [src/Infrastructure/Data/Config/BasketConfiguration.cs], and 2 more | 0.86 |
| Configuration / Options / Cross-cutting constants | Configuration and constants are explicit components that support authentication, catalog behavior, routing, options, and shared behavior. | Move cross-cutting configuration into explicit options/policies and avoid hidden module coupling through shared constants. | CatalogSettings (Configuration) [src/ApplicationCore/CatalogSettings.cs], AuthorizationConstants (Configuration) [src/ApplicationCore/Constants/AuthorizationConstants.cs], Program (Configuration) [src/BlazorAdmin/Program.cs], and 2 more | 0.77 |
| MediatR / CQRS-style handlers | Handler components and MediatR clues indicate command/query or request-handler style behavior in parts of the application. | Use handlers for use-case isolation where they already exist; do not force CQRS everywhere unless justified by module complexity. | GetMyOrders (Handler) [src/Web/Features/MyOrders/GetMyOrders.cs], GetMyOrdersHandler (Handler) [src/Web/Features/MyOrders/GetMyOrdersHandler.cs], GetOrderDetails (Handler) [src/Web/Features/OrderDetails/GetOrderDetails.cs], and 1 more | 0.68 |
| Health Check / Operational Endpoint style | Runtime health endpoints are exposed as operational entry points. | Preserve health/readiness endpoints or provide target equivalents in the deployment platform. | GET /home_page_health_check [src/Web/Program.cs:196], GET /api_health_check [src/Web/Program.cs:197] | 0.8 |

## 5. Applications And Deployable Units

Detected application/support records: 6

Deployable unit candidates: PublicApi, Web

| Unit | Type | Source Path | Framework | Evidence Confidence |
|---|---|---|---|---:|
| PublicApi | backend_web_api | src/PublicApi | unknown | 0.92 |
| Web | backend_web_api | src/Web | unknown | 0.92 |

Implementation meaning:

- Treat deployable units as runtime entry containers until deployment ownership is confirmed.
- Keep support/test projects separate from production module ownership.
- Do not infer cloud platform or production topology unless deployment evidence proves it.

## 6. Architecture Style And Pattern

Primary detected pattern: `Layered Monolith` with confidence `0.78`.

Pattern evidence: Multiple projects/layers detected within one solution/repository and shared deployable units.

Target style guidance: Use the detected layered application style as the baseline behavior model, but do not blindly preserve weak module boundaries or layer violations.

Secondary candidates: Clean Architecture, Modular Monolith

## 7. Layer Model To Implement

| Layer | Component Count | Evidence Examples |
|---|---:|---|
| API | 17 | src/PublicApi/AuthEndpoints/AuthenticateEndpoint.cs, src/PublicApi/CatalogBrandEndpoints/CatalogBrandListEndpoint.cs, src/PublicApi/CatalogItemEndpoints/CatalogItemGetByIdEndpoint.cs, and 5 more |
| Application | 69 | src/ApplicationCore/Interfaces/IAppLogger.cs, src/ApplicationCore/Interfaces/IBasketQueryService.cs, src/ApplicationCore/Interfaces/IBasketService.cs, and 5 more |
| CrossCutting | 62 | src/ApplicationCore/CatalogSettings.cs, src/ApplicationCore/Constants/AuthorizationConstants.cs, src/ApplicationCore/Exceptions/BasketNotFoundException.cs, and 5 more |
| DataAccess | 15 | src/ApplicationCore/Interfaces/IReadRepository.cs, src/ApplicationCore/Interfaces/IRepository.cs, src/ApplicationCore/Specifications/BasketWithItemsSpecification.cs, and 5 more |
| Domain | 18 | src/ApplicationCore/Entities/BaseEntity.cs, src/ApplicationCore/Entities/BasketAggregate/Basket.cs, src/ApplicationCore/Entities/BasketAggregate/BasketItem.cs, and 5 more |
| Infrastructure | 9 | src/Infrastructure/Data/Config/BasketConfiguration.cs, src/Infrastructure/Data/Config/BasketItemConfiguration.cs, src/Infrastructure/Data/Config/CatalogBrandConfiguration.cs, and 5 more |
| Integration | 2 | src/ApplicationCore/Interfaces/IEmailSender.cs, src/BlazorAdmin/CustomAuthStateProvider.cs |
| Presentation/UI | 115 | src/BlazorAdmin/App.razor, src/BlazorAdmin/Helpers/BlazorComponent.cs, src/BlazorAdmin/Helpers/BlazorLayoutComponent.cs, and 5 more |
| Unknown | 3 | src/BlazorAdmin/JavaScript/Cookies.cs, src/BlazorAdmin/JavaScript/Css.cs, src/BlazorAdmin/JavaScript/Route.cs |

Layer rules:

- Presentation/UI and API components should invoke application/use-case services, handlers, or gateways instead of directly owning persistence logic.
- Domain components should remain independent of Presentation/UI, API, Integration, Infrastructure, and DataAccess concerns unless an explicit reviewed exception exists.
- Infrastructure and DataAccess should implement persistence/integration abstractions and must not become the owner of user-facing workflow orchestration.
- CrossCutting concerns should be shared through explicit configuration, middleware, policies, or adapters rather than hidden module-to-module dependencies.

Do not blindly carry forward:

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

## 8. Module Blueprint

These are evidence-derived module candidates, not automatically confirmed future bounded contexts.

| ID | Module | Boundary | Migration Readiness | Components | Entry Points | Depends On |
|---|---|---|---|---:|---:|---|
| MOD-001 | Admin | Weak | Blocked | 23 | 2 | Identity |
| MOD-002 | ApplicationCore | Weak | Blocked | 13 | 0 | Catalog |
| MOD-003 | Basket | Weak | Blocked | 23 | 3 | Admin, ApplicationCore, Catalog, DataAccess, and 3 more |
| MOD-004 | Catalog | Weak | Blocked | 66 | 9 | Admin, ApplicationCore, DataAccess, PublicApi, and 2 more |
| MOD-005 | CrossCutting | Medium | Needs Refactoring | 10 | 7 | ApplicationCore, Catalog, Identity, Infrastructure, and 1 more |
| MOD-006 | DataAccess | Weak | Blocked | 2 | 0 | Catalog |
| MOD-007 | Identity | Weak | Blocked | 66 | 20 | ApplicationCore, Basket, Catalog, Infrastructure, and 2 more |
| MOD-008 | Infrastructure | Medium | Needs Refactoring | 3 | 0 | none detected |
| MOD-009 | Order | Weak | Blocked | 21 | 2 | ApplicationCore, Catalog, DataAccess, Verification |
| MOD-010 | PublicApi | Medium | Needs Refactoring | 5 | 0 | none detected |
| MOD-011 | SharedContracts | Medium | Needs Refactoring | 12 | 0 | none detected |
| MOD-012 | Verification | Medium | Needs Refactoring | 45 | 0 | ApplicationCore, DataAccess, Identity, Order, and 1 more |
| MOD-013 | Web | Weak | Blocked | 21 | 3 | Basket, Catalog, DataAccess, Infrastructure |

Module implementation guidance:

- Admin: Preserve externally visible interfaces and behavior where this module owns APIs or frontend routes., Keep module ownership aligned to the listed source folders and component evidence until a human architect confirms revised boundaries., Implement entry-point components as thin orchestration/adaptation layers., and 3 more
- ApplicationCore: Preserve externally visible interfaces and behavior where this module owns APIs or frontend routes., Keep module ownership aligned to the listed source folders and component evidence until a human architect confirms revised boundaries., Place workflow/use-case coordination in application services or handlers., and 3 more
- Basket: Preserve externally visible interfaces and behavior where this module owns APIs or frontend routes., Keep module ownership aligned to the listed source folders and component evidence until a human architect confirms revised boundaries., Implement entry-point components as thin orchestration/adaptation layers., and 4 more
- Catalog: Preserve externally visible interfaces and behavior where this module owns APIs or frontend routes., Keep module ownership aligned to the listed source folders and component evidence until a human architect confirms revised boundaries., Implement entry-point components as thin orchestration/adaptation layers., and 4 more
- CrossCutting: Preserve externally visible interfaces and behavior where this module owns APIs or frontend routes., Keep module ownership aligned to the listed source folders and component evidence until a human architect confirms revised boundaries.
- DataAccess: Preserve externally visible interfaces and behavior where this module owns APIs or frontend routes., Keep module ownership aligned to the listed source folders and component evidence until a human architect confirms revised boundaries., Separate persistence access from API/UI entry points and keep entity ownership explicit., and 2 more
- Identity: Preserve externally visible interfaces and behavior where this module owns APIs or frontend routes., Keep module ownership aligned to the listed source folders and component evidence until a human architect confirms revised boundaries., Implement entry-point components as thin orchestration/adaptation layers., and 4 more
- Infrastructure: Preserve externally visible interfaces and behavior where this module owns APIs or frontend routes., Keep module ownership aligned to the listed source folders and component evidence until a human architect confirms revised boundaries., Place workflow/use-case coordination in application services or handlers.
- Order: Preserve externally visible interfaces and behavior where this module owns APIs or frontend routes., Keep module ownership aligned to the listed source folders and component evidence until a human architect confirms revised boundaries., Implement entry-point components as thin orchestration/adaptation layers., and 4 more
- PublicApi: Preserve externally visible interfaces and behavior where this module owns APIs or frontend routes., Keep module ownership aligned to the listed source folders and component evidence until a human architect confirms revised boundaries.
- SharedContracts: Preserve externally visible interfaces and behavior where this module owns APIs or frontend routes., Keep module ownership aligned to the listed source folders and component evidence until a human architect confirms revised boundaries., Implement entry-point components as thin orchestration/adaptation layers., and 1 more
- Verification: Preserve externally visible interfaces and behavior where this module owns APIs or frontend routes., Keep module ownership aligned to the listed source folders and component evidence until a human architect confirms revised boundaries., Implement entry-point components as thin orchestration/adaptation layers., and 2 more
- Web: Preserve externally visible interfaces and behavior where this module owns APIs or frontend routes., Keep module ownership aligned to the listed source folders and component evidence until a human architect confirms revised boundaries., Implement entry-point components as thin orchestration/adaptation layers., and 3 more

Module design contracts:

- MOD-001 Admin: Business capability module spanning invocation, workflow, domain/data evidence, or shared UI/API behavior. Target contract: Admin should preserve or explicitly redesign the listed route/API contracts; expose use-case operations through application services or handlers; map UI routes and components to stable API/client-service calls. Patterns: Controller/API endpoint pattern, Frontend component pattern, Shared configuration/cross-cutting style
- MOD-002 ApplicationCore: Domain and persistence-adjacent module with entity ownership and data-access concerns that need separation in the target design. Target contract: ApplicationCore should expose use-case operations through application services or handlers; preserve domain invariants and entity relationships during redesign; hide persistence behind repository/query abstractions. Patterns: Repository pattern, Domain entity/aggregate style, Shared configuration/cross-cutting style
- MOD-003 Basket: Business capability module spanning invocation, workflow, domain/data evidence, or shared UI/API behavior. Target contract: Basket should preserve or explicitly redesign the listed route/API contracts; expose use-case operations through application services or handlers; preserve domain invariants and entity relationships during redesign; hide persistence behind repository/query abstractions; map UI routes and components to stable API/client-service calls. Patterns: Controller/API endpoint pattern, Frontend component pattern, Repository pattern, Specification pattern, Domain entity/aggregate style, and 2 more
- MOD-004 Catalog: Business capability module spanning invocation, workflow, domain/data evidence, or shared UI/API behavior. Target contract: Catalog should preserve or explicitly redesign the listed route/API contracts; expose use-case operations through application services or handlers; preserve domain invariants and entity relationships during redesign; hide persistence behind repository/query abstractions; map UI routes and components to stable API/client-service calls. Patterns: Controller/API endpoint pattern, Frontend component pattern, Repository pattern, Specification pattern, Domain entity/aggregate style, and 2 more
- MOD-005 CrossCutting: Invocation/API module that owns externally visible routes and maps requests into application behavior. Target contract: CrossCutting should preserve or explicitly redesign the listed route/API contracts. Patterns: Shared configuration/cross-cutting style
- MOD-006 DataAccess: Data-access adapter module that should implement persistence contracts rather than own business workflow. Target contract: DataAccess should hide persistence behind repository/query abstractions. Patterns: Repository pattern
- MOD-007 Identity: Business capability module spanning invocation, workflow, domain/data evidence, or shared UI/API behavior. Target contract: Identity should preserve or explicitly redesign the listed route/API contracts; expose use-case operations through application services or handlers; preserve domain invariants and entity relationships during redesign; hide persistence behind repository/query abstractions; map UI routes and components to stable API/client-service calls. Patterns: Controller/API endpoint pattern, Frontend component pattern, Repository pattern, Domain entity/aggregate style, EF Core context/configuration style, and 1 more
- MOD-008 Infrastructure: Shared/cross-cutting support module for configuration, constants, shared contracts, or platform concerns. Target contract: Infrastructure should expose use-case operations through application services or handlers. Patterns: Shared configuration/cross-cutting style
- MOD-009 Order: Business capability module spanning invocation, workflow, domain/data evidence, or shared UI/API behavior. Target contract: Order should preserve or explicitly redesign the listed route/API contracts; expose use-case operations through application services or handlers; preserve domain invariants and entity relationships during redesign; hide persistence behind repository/query abstractions; map UI routes and components to stable API/client-service calls. Patterns: Controller/API endpoint pattern, Frontend component pattern, Repository pattern, Specification pattern, Domain entity/aggregate style, and 2 more
- MOD-010 PublicApi: Supporting module candidate whose target role requires human boundary review. Target contract: PublicApi should confirm whether this candidate remains a separate target module. Patterns: none detected
- MOD-011 SharedContracts: User-interface or frontend-facing module that adapts user actions to API/application calls. Target contract: SharedContracts should expose use-case operations through application services or handlers; map UI routes and components to stable API/client-service calls. Patterns: Frontend component pattern, Shared configuration/cross-cutting style
- MOD-012 Verification: Business capability module spanning invocation, workflow, domain/data evidence, or shared UI/API behavior. Target contract: Verification should expose use-case operations through application services or handlers; preserve domain invariants and entity relationships during redesign. Patterns: Controller/API endpoint pattern, Specification pattern, Domain entity/aggregate style, Shared configuration/cross-cutting style
- MOD-013 Web: Business capability module spanning invocation, workflow, domain/data evidence, or shared UI/API behavior. Target contract: Web should preserve or explicitly redesign the listed route/API contracts; expose use-case operations through application services or handlers; map UI routes and components to stable API/client-service calls. Patterns: Controller/API endpoint pattern, Frontend component pattern, Shared configuration/cross-cutting style

## 9. Component Model

Total components: 310

Components by type: `{"BatchJob": 2, "Configuration": 27, "Controller": 32, "DTO": 58, "Entity": 19, "ExternalClient": 2, "FrontendComponent": 68, "FrontendService": 8, "Handler": 4, "Mapper": 1, "Middleware": 1, "Repository": 13, "Service": 34, "Unknown": 40, "Validator": 1}`

Components by layer: `{"API": 17, "Application": 69, "CrossCutting": 62, "DataAccess": 15, "Domain": 18, "Infrastructure": 9, "Integration": 2, "Presentation/UI": 115, "Unknown": 3}`

Components with Roslyn semantic symbol evidence: 247

Implementation meaning:

- Controllers/API endpoints and frontend components should be treated as invocation adapters.
- Services and handlers should own use-case orchestration.
- Repositories, DbContexts, and external clients should be adapters behind explicit contracts.
- Unknown components should be reviewed before deciding whether they are architecture-significant.

## 10. Implementation Architecture By Concern

### API and Invocation

Legacy design: HTTP routes are owned by endpoint/controller/page components and executable Program.cs bootstrap files.

Target implementation design: Create thin route adapters that validate/map requests, invoke application services or handlers, and return stable response contracts.

Evidence:

- POST /api/authenticate [src/PublicApi/AuthEndpoints/AuthenticateEndpoint.cs:36]
- GET /api/catalog-brands [src/PublicApi/CatalogBrandEndpoints/CatalogBrandListEndpoint.cs:27]
- GET /api/catalog-items/{catalogItemId} [src/PublicApi/CatalogItemEndpoints/CatalogItemGetByIdEndpoint.cs:25]
- GET /api/catalog-items [src/PublicApi/CatalogItemEndpoints/CatalogItemListPagedEndpoint.cs:31]
- POST /api/catalog-items [src/PublicApi/CatalogItemEndpoints/CreateCatalogItemEndpoint.cs:29]
- DELETE /api/catalog-items/{catalogItemId} [src/PublicApi/CatalogItemEndpoints/DeleteCatalogItemEndpoint.cs:20]
- PUT /api/catalog-items [src/PublicApi/CatalogItemEndpoints/UpdateCatalogItemEndpoint.cs:27]
- GET /api/catalog-types [src/PublicApi/CatalogTypeEndpoints/CatalogTypeListEndpoint.cs:27]

### Application Workflow

Legacy design: Services, handlers, DTOs, specifications, and shared contracts represent use-case and workflow boundaries.

Target implementation design: Implement workflows as application services or handlers that coordinate domain rules, persistence abstractions, and integrations.

Evidence:

- BasketGuards (Service) [src/ApplicationCore/Extensions/GuardExtensions.cs]
- JsonExtensions (Service) [src/ApplicationCore/Extensions/JsonExtensions.cs]
- IAppLogger (Service) [src/ApplicationCore/Interfaces/IAppLogger.cs]
- IBasketQueryService (Service) [src/ApplicationCore/Interfaces/IBasketQueryService.cs]
- IBasketService (Service) [src/ApplicationCore/Interfaces/IBasketService.cs]

### Domain Model

Legacy design: Domain entities and aggregate-style folders represent Basket, Catalog, Order, Buyer, and related business concepts.

Target implementation design: Preserve domain concepts and invariants; keep domain types independent of UI/API/infrastructure dependencies.

Evidence:

- BaseEntity (Entity) [src/ApplicationCore/Entities/BaseEntity.cs]
- CatalogBrand (Entity) [src/ApplicationCore/Entities/CatalogBrand.cs]
- CatalogItem (Entity) [src/ApplicationCore/Entities/CatalogItem.cs]
- CatalogItemDetails (Entity) [src/ApplicationCore/Entities/CatalogItem.cs]
- CatalogType (Entity) [src/ApplicationCore/Entities/CatalogType.cs]

### Persistence and Data Access

Legacy design: Repository, EF Core context/configuration, and data-access components provide persistence behavior.

Target implementation design: Keep persistence behind repository/query abstractions; remove direct endpoint-to-repository access where flagged.

Evidence:

- IReadRepository (Repository) [src/ApplicationCore/Interfaces/IReadRepository.cs]
- IRepository (Repository) [src/ApplicationCore/Interfaces/IRepository.cs]
- BasketWithItemsSpecification (Repository) [src/ApplicationCore/Specifications/BasketWithItemsSpecification.cs]
- CatalogFilterPaginatedSpecification (Repository) [src/ApplicationCore/Specifications/CatalogFilterPaginatedSpecification.cs]
- CatalogFilterSpecification (Repository) [src/ApplicationCore/Specifications/CatalogFilterSpecification.cs]

### Frontend / Admin UI

Legacy design: Frontend components and services represent admin/user-facing UI routes and API client behavior.

Target implementation design: Preserve route intent and API calls while making state, auth, and API service boundaries explicit.

Evidence:

- BlazorComponent (FrontendComponent) [src/BlazorAdmin/Helpers/BlazorComponent.cs]
- BlazorLayoutComponent (FrontendComponent) [src/BlazorAdmin/Helpers/BlazorLayoutComponent.cs]
- ToastComponent (FrontendComponent) [src/BlazorAdmin/Helpers/ToastComponent.cs]
- List (FrontendComponent) [src/BlazorAdmin/Pages/CatalogItemPage/List.razor.cs]
- CustomInputSelect (FrontendComponent) [src/BlazorAdmin/Shared/CustomInputSelect.cs]

### Cross-cutting and Configuration

Legacy design: Configuration, constants, middleware, and shared contracts cut across modules.

Target implementation design: Centralize cross-cutting policies as explicit options, middleware, adapters, or shared contracts with clear ownership.

Evidence:

- CatalogSettings (Configuration) [src/ApplicationCore/CatalogSettings.cs]
- AuthorizationConstants (Configuration) [src/ApplicationCore/Constants/AuthorizationConstants.cs]
- Program (Configuration) [src/BlazorAdmin/Program.cs]
- ServicesConfiguration (Configuration) [src/BlazorAdmin/ServicesConfiguration.cs]
- JSInteropConstants (Configuration) [src/BlazorAdmin/JavaScript/JSInteropConstants.cs]

### Module Boundary Governance

Legacy design: Module candidates are evidence-derived and several are weak or cyclic.

Target implementation design: Finalize module boundaries only after resolving ownership, data ownership, cycles, and high coupling.

Evidence:

- MOD-001 Admin boundary=Weak
- MOD-002 ApplicationCore boundary=Weak
- MOD-003 Basket boundary=Weak
- MOD-004 Catalog boundary=Weak
- MOD-005 CrossCutting boundary=Medium
- MOD-006 DataAccess boundary=Weak
- MOD-007 Identity boundary=Weak
- MOD-008 Infrastructure boundary=Medium


## 11. Invocation Model

Entry point count: 55

Entry points by type: `{"CLI": 3, "FrontendRoute": 3, "HTTP_API": 49}`

HTTP methods: `{"DELETE": 1, "GET": 32, "POST": 13, "PUT": 1, "unknown": 8}`

Entry points by module: `{"Admin": 2, "Basket": 3, "Catalog": 9, "CrossCutting": 7, "Identity": 29, "Order": 2, "Web": 3}`

Implementation rules:

- Every HTTP_API interface listed here must either be preserved, explicitly versioned, or retired with product-owner approval.
- Every FrontendRoute must be mapped to a frontend route/component responsibility or marked for redesign.
- Program.cs/CLI bootstrap entries represent executable startup surfaces, not user-facing business commands unless human review confirms otherwise.
- Call-flow steps with Roslyn semantic evidence can be used as stronger behavior-preservation anchors than heuristic-only steps.

Representative API contracts to preserve or review:

- INT-001: POST /api/authenticate -> AuthenticateEndpoint (Identity) [src/PublicApi/AuthEndpoints/AuthenticateEndpoint.cs:36]
- INT-002: GET /api/catalog-brands -> CatalogBrandListEndpoint (Catalog) [src/PublicApi/CatalogBrandEndpoints/CatalogBrandListEndpoint.cs:27]
- INT-003: GET /api/catalog-items/{catalogItemId} -> CatalogItemGetByIdEndpoint (Catalog) [src/PublicApi/CatalogItemEndpoints/CatalogItemGetByIdEndpoint.cs:25]
- INT-004: GET /api/catalog-items -> CatalogItemListPagedEndpoint (Catalog) [src/PublicApi/CatalogItemEndpoints/CatalogItemListPagedEndpoint.cs:31]
- INT-005: POST /api/catalog-items -> CreateCatalogItemEndpoint (Catalog) [src/PublicApi/CatalogItemEndpoints/CreateCatalogItemEndpoint.cs:29]
- INT-006: DELETE /api/catalog-items/{catalogItemId} -> DeleteCatalogItemEndpoint (Catalog) [src/PublicApi/CatalogItemEndpoints/DeleteCatalogItemEndpoint.cs:20]
- INT-007: PUT /api/catalog-items -> UpdateCatalogItemEndpoint (Catalog) [src/PublicApi/CatalogItemEndpoints/UpdateCatalogItemEndpoint.cs:27]
- INT-008: GET /api/catalog-types -> CatalogTypeListEndpoint (Catalog) [src/PublicApi/CatalogTypeEndpoints/CatalogTypeListEndpoint.cs:27]
- INT-009: unknown /{controller:slugify=Home}/{action:slugify=Index}/{id?} -> Program (CrossCutting) [src/Web/Program.cs:194]
- INT-010: unknown ASP.NET Razor Pages route registration -> Program (CrossCutting) [src/Web/Program.cs:195]
- INT-012: GET /home_page_health_check -> Program (CrossCutting) [src/Web/Program.cs:196]
- INT-013: GET /api_health_check -> Program (CrossCutting) [src/Web/Program.cs:197]
- INT-014: GET /Manage/MyAccount -> ManageController (Identity) [src/Web/Controllers/ManageController.cs:47]
- INT-015: POST /Manage/MyAccount -> ManageController (Identity) [src/Web/Controllers/ManageController.cs:69]
- INT-016: POST /Manage/SendVerificationEmail -> ManageController (Identity) [src/Web/Controllers/ManageController.cs:108]
- INT-017: GET /Manage/ChangePassword -> ManageController (Identity) [src/Web/Controllers/ManageController.cs:137]
- INT-018: POST /Manage/ChangePassword -> ManageController (Identity) [src/Web/Controllers/ManageController.cs:157]
- INT-019: GET /Manage/SetPassword -> ManageController (Identity) [src/Web/Controllers/ManageController.cs:186]
- INT-020: POST /Manage/SetPassword -> ManageController (Identity) [src/Web/Controllers/ManageController.cs:207]
- INT-021: GET /Manage/ExternalLogins -> ManageController (Identity) [src/Web/Controllers/ManageController.cs:234]

## 12. Behavior And Scenario Model

Call flows detected: 55

Semantic trace flows: 43

Flows with data access: 22

Flows with external systems: 2

### SC-READ_PATH: GET /api/catalog-brands

Type: `READ_PATH`  
Status: `traced_from_dependency_candidates`  
Entry point: `GET /api/catalog-brands`  
Confidence: `0.74`

Implementation contract: Implement this scenario so the entry point invokes the listed components in the observed layer/module order, or document an intentional redesign with equivalent behavior.

Flow narrative: The flow starts at GET /api/catalog-brands. The observed implementation chain is CatalogBrandListEndpoint (API/Catalog) -> EfRepository (DataAccess/DataAccess) -> CatalogContext (DataAccess/Catalog). Semantic evidence is present on 0 step(s). Data-access components touched: CatalogContext, EfRepository. External systems touched: none detected.

| Step | Component | Layer | Module | Action | Source |
|---:|---|---|---|---|---|
| 1 | CatalogBrandListEndpoint | API | Catalog | /api/catalog-brands | src/PublicApi/CatalogBrandEndpoints/CatalogBrandListEndpoint.cs |
| 2 | EfRepository | DataAccess | DataAccess | ListAsync | src/Infrastructure/Data/EfRepository.cs |
| 3 | CatalogContext | DataAccess | Catalog | resolves_to | src/Infrastructure/Data/CatalogContext.cs |

### SC-WRITE_PATH: POST /api/catalog-items

Type: `WRITE_PATH`  
Status: `traced_from_dependency_candidates`  
Entry point: `POST /api/catalog-items`  
Confidence: `0.82`

Implementation contract: Implement this scenario so the entry point invokes the listed components in the observed layer/module order, or document an intentional redesign with equivalent behavior.

Flow narrative: The flow starts at POST /api/catalog-items. The observed implementation chain is CreateCatalogItemEndpoint (API/Catalog) -> BaseMessage (Application/PublicApi) -> UriComposer (Application/ApplicationCore) -> EfRepository (DataAccess/DataAccess) -> CatalogSettings (CrossCutting/Catalog) -> CatalogContext (DataAccess/Catalog) -> CreateCatalogItemRequest (Application/Catalog). Semantic evidence is present on 2 step(s). Data-access components touched: CatalogContext, EfRepository. External systems touched: none detected.

| Step | Component | Layer | Module | Action | Source |
|---:|---|---|---|---|---|
| 1 | CreateCatalogItemEndpoint | API | Catalog | /api/catalog-items | src/PublicApi/CatalogItemEndpoints/CreateCatalogItemEndpoint.cs |
| 2 | BaseMessage | Application | PublicApi | CorrelationId | src/PublicApi/BaseMessage.cs |
| 3 | UriComposer | Application | ApplicationCore | ComposePicUri | src/ApplicationCore/Services/UriComposer.cs |
| 4 | EfRepository | DataAccess | DataAccess | CountAsync | src/Infrastructure/Data/EfRepository.cs |
| 5 | CatalogSettings | CrossCutting | Catalog | injects | src/ApplicationCore/CatalogSettings.cs |
| 6 | CatalogContext | DataAccess | Catalog | resolves_to | src/Infrastructure/Data/CatalogContext.cs |
| 7 | CreateCatalogItemRequest | Application | Catalog | CreateCatalogItemRequest.CorrelationId | src/BlazorShared/Models/CreateCatalogItemRequest.cs |

### SC-AUTH_PATH: POST /api/authenticate

Type: `AUTH_PATH`  
Status: `traced_from_dependency_candidates`  
Entry point: `POST /api/authenticate`  
Confidence: `0.74`

Implementation contract: Implement this scenario so the entry point invokes the listed components in the observed layer/module order, or document an intentional redesign with equivalent behavior.

Flow narrative: The flow starts at POST /api/authenticate. The observed implementation chain is AuthenticateEndpoint (API/Identity) -> BaseMessage (Application/PublicApi) -> IdentityTokenClaimService (Application/Identity). Semantic evidence is present on 2 step(s). Data-access components touched: none detected. External systems touched: none detected.

| Step | Component | Layer | Module | Action | Source |
|---:|---|---|---|---|---|
| 1 | AuthenticateEndpoint | API | Identity | /api/authenticate | src/PublicApi/AuthEndpoints/AuthenticateEndpoint.cs |
| 2 | BaseMessage | Application | PublicApi | CorrelationId | src/PublicApi/BaseMessage.cs |
| 3 | IdentityTokenClaimService | Application | Identity | GetTokenAsync | src/Infrastructure/Identity/IdentityTokenClaimService.cs |

### SC-ADMIN_PATH: unknown /admin

Type: `ADMIN_PATH`  
Status: `frontend_route_mapped`  
Entry point: `unknown /admin`  
Confidence: `0.74`

Implementation contract: Implement this scenario so the entry point invokes the listed components in the observed layer/module order, or document an intentional redesign with equivalent behavior.

Flow narrative: The flow starts at unknown /admin. The observed implementation chain is List (Presentation/UI/Catalog) -> ICatalogItemService (Application/SharedContracts) -> CachedCatalogItemServiceDecorator (Presentation/UI/Catalog) -> CachedCatalogLookupDataServiceDecorator (Presentation/UI/Catalog) -> BlazorComponent (Presentation/UI/Admin) -> ICatalogLookupDataService (Application/SharedContracts) -> RefreshBroadcast (Presentation/UI/Admin). Semantic evidence is present on 5 step(s). Data-access components touched: none detected. External systems touched: none detected.

| Step | Component | Layer | Module | Action | Source |
|---:|---|---|---|---|---|
| 1 | List | Presentation/UI | Catalog | /admin | src/BlazorAdmin/Pages/CatalogItemPage/List.razor.cs |
| 2 | ICatalogItemService | Application | SharedContracts | List | src/BlazorShared/Interfaces/ICatalogItemService.cs |
| 3 | CachedCatalogItemServiceDecorator | Presentation/UI | Catalog | List | src/BlazorAdmin/Services/CachedCatalogItemServiceDecorator.cs |
| 4 | CachedCatalogLookupDataServiceDecorator | Presentation/UI | Catalog | List | src/BlazorAdmin/Services/CachedCatalogLookupDataServiceDecorator .cs |
| 5 | BlazorComponent | Presentation/UI | Admin | CallRequestRefresh | src/BlazorAdmin/Helpers/BlazorComponent.cs |
| 6 | ICatalogLookupDataService | Application | SharedContracts | List | src/BlazorShared/Interfaces/ICatalogLookupDataService.cs |
| 7 | RefreshBroadcast | Presentation/UI | Admin | CallRequestRefresh | src/BlazorAdmin/Helpers/RefreshBroadcast.cs |

### SC-ERROR_OR_RESILIENCE_PATH: GET /home_page_health_check

Type: `ERROR_OR_RESILIENCE_PATH`  
Status: `traced_from_dependency_candidates`  
Entry point: `GET /home_page_health_check`  
Confidence: `0.82`

Implementation contract: Implement this scenario so the entry point invokes the listed components in the observed layer/module order, or document an intentional redesign with equivalent behavior.

Flow narrative: The flow starts at GET /home_page_health_check. The observed implementation chain is Program (CrossCutting/CrossCutting) -> CatalogContextSeed (DataAccess/Catalog) -> AppIdentityDbContextSeed (DataAccess/Identity) -> JsonExtensions (CrossCutting/ApplicationCore) -> CatalogContext (DataAccess/Catalog) -> AppIdentityDbContext (DataAccess/Identity). Semantic evidence is present on 3 step(s). Data-access components touched: AppIdentityDbContext, AppIdentityDbContextSeed, CatalogContext, CatalogContextSeed. External systems touched: none detected.

| Step | Component | Layer | Module | Action | Source |
|---:|---|---|---|---|---|
| 1 | Program | CrossCutting | CrossCutting | /home_page_health_check | src/PublicApi/Program.cs |
| 2 | CatalogContextSeed | DataAccess | Catalog | SeedAsync | src/Infrastructure/Data/CatalogContextSeed.cs |
| 3 | AppIdentityDbContextSeed | DataAccess | Identity | SeedAsync | src/Infrastructure/Identity/AppIdentityDbContextSeed.cs |
| 4 | JsonExtensions | CrossCutting | ApplicationCore | ToJson | src/ApplicationCore/Extensions/JsonExtensions.cs |
| 5 | CatalogContext | DataAccess | Catalog | SaveChangesAsync | src/Infrastructure/Data/CatalogContext.cs |
| 6 | AppIdentityDbContext | DataAccess | Identity | uses | src/Infrastructure/Identity/AppIdentityDbContext.cs |


## 13. Data Access And Persistence Model

Repository candidates: 13

Entity candidates: 19

Database context/session candidates: 6

Database/infrastructure boundaries: sqlserver

Implementation rules:

- Treat repository/data-access components as infrastructure adapters behind application/domain-facing abstractions.
- Do not let API/UI entry points call shared repositories directly in the target design unless explicitly accepted as an architecture exception.
- Confirm true data ownership with database/schema review before splitting modules or services.

## 14. Frontend Architecture Model

Frontend status: `frontend_detected`

Frontend apps detected: BlazorAdmin

Implementation rules:

- Preserve detected frontend routes or map them to equivalent navigation routes in the target UI.
- Keep frontend API call contracts aligned with the API contract preservation map.
- State management and authentication-state clues require human review before target UI design is finalized.

## 15. Dependency And Integration Model

Dependency graph nodes: 374

Dependency graph edges: 534

Module cycle count: 1

High-coupling modules: Catalog, Basket, Identity, Web, ApplicationCore, DataAccess, CrossCutting, Infrastructure, and 2 more

High-coupling components: EfRepository, UriComposer

External boundaries: sqlserver, catalog-items, catalog-items, catalog-items, catalog-items/{id}, catalog-items?PageSize=10, catalog-items, {_apiUrl}{uri}, and 41 more

Integration rules:

- External targets inferred only from static evidence must be confirmed before target integration design.
- High-coupling components should become explicit adapters, services, or module APIs in the target design.
- Detected cycles must be broken or intentionally accepted before module/service extraction.

## 16. Forward Engineering Contract

Preserve these behavior/API contracts unless an explicit replacement plan exists:

- none detected

Redesign before carrying forward:

- APP-RISK-001: Module candidate Catalog has weak or uncertain boundary evidence with coupling score 13.
- APP-RISK-002: Module dependency cycle detected: Admin -> ApplicationCore -> Basket -> Catalog -> DataAccess -> Identity -> Order -> Web
- APP-RISK-003: High-coupling module candidates include Catalog, Basket, Identity, Web, ApplicationCore.
- APP-RISK-004: EfRepository is a high-coupling component candidate with total coupling 16.
- APP-RISK-005: 0 call flows are partial because parsed evidence did not fully resolve runtime dispatch and downstream calls.
- APP-RISK-006: Frontend application evidence contains 11 API call mappings from BlazorAdmin.
- APP-RISK-007: Controller-like component CatalogBrandListEndpoint depends directly on repository EfRepository.
- APP-RISK-008: 0 components have unknown module ownership and 40 components have unknown type classification.
- APP-RISK-009: External dependency candidates include sqlserver, catalog-items, catalog-items/{id}, catalog-items?PageSize=10, {_apiUrl}{uri}; target purposes may require review.

Do not blindly carry forward architecture violations:

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

Review before final target design:

- none detected

## 17. Enterprise Governance And Stakeholders

This section explains who should use this blueprint and what each stakeholder should validate.

| Stakeholder | Use | Primary Sections |
|---|---|---|
| Enterprise / Solution Architect | Validate application style, module boundaries, dependency direction, and redesign decisions. | Architecture Style, Layer Model, Module Blueprint, Forward Engineering Contract |
| Engineering Manager | Plan implementation waves, review risks, and track human-review decisions. | Forward Engineering Contract, Human Review Required, Acceptance Criteria |
| Backend / API Engineers | Implement preserved APIs, services, handlers, repositories, and dependency contracts. | Invocation Model, Behavior Model, Data Access Model, Module Blueprint |
| Frontend Engineers | Rebuild or preserve UI routes, frontend services, API call contracts, and state/auth clues. | Frontend Architecture Model, Invocation Model, Forward Engineering Contract |
| QA / Test Engineers | Create contract, scenario, integration, and regression tests from preserved flows and APIs. | Behavior And Scenario Model, Invocation Model, Runtime Evidence |
| Security / Compliance Reviewer | Review identity, exposed interfaces, PII/data ownership questions, and avoid-carry-forward violations. | Security And Compliance Baseline, Human Review Required |

## 18. Architecture Decisions Required Before Build

These are not optional documentation items. They are decisions that should be closed before treating this as a final target architecture.

| ID | Decision | Affected Items | Why It Matters |
|---|---|---|---|
| EA-ADR-001 | Confirm target architecture style and whether the rebuild remains a layered monolith, modular monolith, or moves to separately deployable services. | none detected | This determines deployment, module boundaries, data ownership, and team ownership. |
| EA-ADR-002 | Confirm weak module boundaries before using them as target bounded contexts. | Admin, ApplicationCore, Basket, Catalog, DataAccess, and 3 more | Weak boundaries and cycles can create a poor target design if copied directly. |
| EA-ADR-003 | Decide how to handle direct API/UI-to-repository dependencies. | ARCH-VIOL-001, ARCH-VIOL-002, ARCH-VIOL-003, ARCH-VIOL-004, ARCH-VIOL-005, and 3 more | The target implementation should avoid carrying forward data-access coupling unless explicitly accepted. |
| EA-ADR-004 | Confirm API contract preservation/versioning strategy. | none detected | Forward implementation must not accidentally break externally visible behavior. |
| EA-ADR-005 | Confirm data ownership and database boundary strategy. | none detected | Module/service extraction cannot be finalized without data ownership decisions. |

## 19. NFR And Operational Baseline

Runtime evidence status: `not_run`

Runtime evidence summary: `{}`

Availability/health-check clues:

- INT-012: GET /home_page_health_check [src/Web/Program.cs:196]
- INT-013: GET /api_health_check [src/Web/Program.cs:197]

Security/identity clues:

- INT-001: POST /api/authenticate -> AuthenticateEndpoint [src/PublicApi/AuthEndpoints/AuthenticateEndpoint.cs:36]
- INT-014: GET /Manage/MyAccount -> ManageController [src/Web/Controllers/ManageController.cs:47]
- INT-015: POST /Manage/MyAccount -> ManageController [src/Web/Controllers/ManageController.cs:69]
- INT-016: POST /Manage/SendVerificationEmail -> ManageController [src/Web/Controllers/ManageController.cs:108]
- INT-017: GET /Manage/ChangePassword -> ManageController [src/Web/Controllers/ManageController.cs:137]
- INT-018: POST /Manage/ChangePassword -> ManageController [src/Web/Controllers/ManageController.cs:157]
- INT-019: GET /Manage/SetPassword -> ManageController [src/Web/Controllers/ManageController.cs:186]
- INT-020: POST /Manage/SetPassword -> ManageController [src/Web/Controllers/ManageController.cs:207]
- INT-021: GET /Manage/ExternalLogins -> ManageController [src/Web/Controllers/ManageController.cs:234]
- INT-022: POST /Manage/LinkLogin -> ManageController [src/Web/Controllers/ManageController.cs:254]
- INT-023: GET /Manage/LinkLoginCallback -> ManageController [src/Web/Controllers/ManageController.cs:266]
- INT-024: POST /Manage/RemoveLogin -> ManageController [src/Web/Controllers/ManageController.cs:295]
- INT-025: GET /Manage/TwoFactorAuthentication -> ManageController [src/Web/Controllers/ManageController.cs:319]
- INT-026: GET /Manage/Disable2faWarning -> ManageController [src/Web/Controllers/ManageController.cs:338]
- INT-027: POST /Manage/Disable2fa -> ManageController [src/Web/Controllers/ManageController.cs:356]

NFR requirements to confirm:

- Availability/SLO targets are not derivable from static code and must be supplied by stakeholders.
- Latency, throughput, and scaling targets are not derivable from static code and must be supplied by product/platform owners.
- Observability requirements for logs, metrics, traces, audit events, and dashboards require runtime/platform review.
- Security and compliance posture require a separate specialist review before production implementation.
- Disaster recovery, backup, retention, and restore requirements require operations and data-owner input.

## 20. Target Build Acceptance Criteria

| Area | Criteria | Evidence Inputs |
|---|---|---|
| Interface compatibility | Every preserved API/frontend route has a target implementation decision and contract/regression test. | application-interface-catalogue.json, api-contract-preservation-map.json, call-flow-map.json |
| Module ownership | Every future module/service has confirmed owner, responsibility, data ownership, and allowed dependencies. | module-boundary-map.json, module-consolidation-map.json, open-questions.md |
| Layering | Target implementation documents allowed layer dependencies and explicitly rejects or accepts each detected violation. | architecture-violation-register.json, layering-pattern-pack.json |
| Behavior preservation | Read, write, auth, admin, and reliability/error-path scenarios are implemented or intentionally redesigned with review approval. | call-flow-map.json, enterprise-application-architecture-blueprint.json |
| Risk remediation | Each application risk is accepted, mitigated, redesigned, or converted into backlog work. | application-risk-register.json, forward-engineering-backlog.md |
| Human review closure | Open questions are assigned and resolved before final target architecture sign-off. | open-questions.md, architecture-decision-inputs.md |

## 21. Implementation Inputs For A New Build

Use this package as input to create the target implementation backlog:

- Use `application-interface-catalogue.json` and `api-contract-preservation-map.json` as interface contracts.
- Use `module-boundary-map.json` and this module blueprint as candidate module ownership.
- Use `call-flow-map.json` and the scenario model above as behavior-preservation input.
- Use `dependency-graph.json` to break cycles and reduce coupling before extraction.
- Use `application-risk-register.json` and `architecture-violation-register.json` as avoid-carry-forward controls.
- Use `open-questions.md` as the human review queue.

## 22. Human Review Required

- Confirm the authoritative system name; evidence packs leave system_name as unknown.
- Confirm ownership and boundaries for weak or unknown module candidates: Admin, ApplicationCore, Basket, Catalog, DataAccess, Identity, Order, Web.
- Review the 0 components with unknown module ownership before finalizing module boundaries.
- Review the 40 components with Unknown type/layer classification to decide whether they are architecture-significant.
- Review 0 partial call flows before using them as behavior-preservation contracts.
- Confirm whether detected module cycles are real architecture cycles or artifacts of static dependency resolution: Admin -> ApplicationCore -> Basket -> Catalog -> DataAccess -> Identity -> Order -> Web.
- Confirm deployment ownership for detected frontend applications: BlazorAdmin.
- Confirm whether detected database/infrastructure services are development-only or production-relevant external boundaries.
- Confirm the target systems and purposes behind configured HTTP/API base URLs and health-check dependencies: sqlserver, catalog-items, catalog-items/{id}, catalog-items?PageSize=10, {_apiUrl}{uri}.
- Confirm whether no scheduled jobs/message consumers exist; none were detected in parsed facts.
- Confirm controller and route coverage for convention-based framework routes, because extraction found 49 HTTP APIs, 3 frontend routes, and partial call flows but cannot prove complete runtime route coverage without framework execution.
- Review generated/migration source exclusions before relying on this package for database migration planning.
- Confirm whether test-project components should be retained in final architecture evidence or filtered from enterprise application views.
- Confirm business capability names and ownership with product/domain stakeholders before using this as a target bounded-context model.
- Confirm production deployment topology; static repository evidence may include local-development services.
- Confirm non-functional requirements such as availability, latency, scaling, observability, and recovery objectives from runtime and business sources.
