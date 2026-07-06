# Canonical Enterprise Model — eShopOnWeb

> Human-readable rendering of the VERIFIED canonical knowledge graph
> (`ENTERPRISE_KNOWLEDGE_GRAPH.json`, schema version 1.0). Every node retains its
> graph ID so this document cross-references the source of truth. Content is
> evidence-grounded only; confidence and status signals are preserved verbatim.
> This is a **foundation package** describing the current and canonical state plus
> inputs for future forward engineering. It does **not** propose code or new designs.

---

## 1. Overview

| Field | Value |
|---|---|
| System name | eShopOnWeb (authoritative name flagged **`unknown`** in source business evidence; see OQ-007 / ASSUMP-007) |
| Source project | `eShopOnWeb` |
| Evidence root | `bussiness-architecture 1/bussiness-architecture/output/eShopOnWeb` |
| Generated | 2026-06-23 |
| Schema version | 1.0 |
| Domains | business, data, application, technology |

**Confidence note (verbatim from graph):** Evidence-only consolidation.
Confidence/status signals (HIGH/MEDIUM/LOW, ACTIVE/DORMANT,
implemented/aspirational-unimplemented, INFERRED, VERSION UNKNOWN, soft-reference,
RC-002 dead code) are preserved from source fragments. No forward engineering; no
new capabilities/entities/APIs invented. Cross-links are emitted only where a
source file supports them.

**Domain inventory at a glance:**

| Domain | Node groups (counts) |
|---|---|
| Business | 39 capabilities, 5 actors, 10 processes |
| Data | 15 entities, 4 aggregates, 12 relationships, 4 repositories |
| Application | 47 services/modules, 13 interfaces, 55 API endpoints, 19 dependencies |
| Technology | 26 current-stack items, 0 target-stack items, 8 infrastructure items, 17 security entries |
| Cross-links | 17 capability→process, 29 process→entity, 16 entity→service, 55 service→api |

---

## 2. Business Architecture

### 2.1 Capability Map (L1 / L2 / L3)

All capabilities carry `status` and `confidence` from the graph. Payment-related
capabilities are explicitly **inferred** at **LOW** confidence.

| ID | Level | Capability | Parent | Status | Confidence |
|---|---|---|---|---|---|
| BIZ-CAP-001 | L1 | Catalog Management | — | ACTIVE | HIGH |
| BIZ-CAP-002 | L2 | Product Information Management | BIZ-CAP-001 | ACTIVE | HIGH |
| BIZ-CAP-003 | L3 | Catalog Item Details Maintenance | BIZ-CAP-002 | ACTIVE | HIGH |
| BIZ-CAP-004 | L3 | Product Classification | BIZ-CAP-002 | ACTIVE | HIGH |
| BIZ-CAP-005 | L3 | Product Image Management | BIZ-CAP-002 | ACTIVE | HIGH |
| BIZ-CAP-006 | L2 | Catalog Reference Data | BIZ-CAP-001 | ACTIVE | HIGH |
| BIZ-CAP-007 | L3 | Brand Management | BIZ-CAP-006 | ACTIVE | HIGH |
| BIZ-CAP-008 | L3 | Type Management | BIZ-CAP-006 | ACTIVE | HIGH |
| BIZ-CAP-009 | L3 | Catalog Seeding | BIZ-CAP-006 | ACTIVE | HIGH |
| BIZ-CAP-010 | L1 | Basket / Shopping Cart Management | — | ACTIVE | HIGH |
| BIZ-CAP-011 | L2 | Basket Maintenance | BIZ-CAP-010 | ACTIVE | HIGH |
| BIZ-CAP-012 | L3 | Add Item to Basket | BIZ-CAP-011 | ACTIVE | HIGH |
| BIZ-CAP-013 | L3 | Quantity Adjustment | BIZ-CAP-011 | ACTIVE | HIGH |
| BIZ-CAP-014 | L3 | Basket Cleanup | BIZ-CAP-011 | ACTIVE | HIGH |
| BIZ-CAP-015 | L2 | Session Continuity | BIZ-CAP-010 | ACTIVE | HIGH |
| BIZ-CAP-016 | L3 | Anonymous-to-Registered Basket Transfer | BIZ-CAP-015 | ACTIVE | HIGH |
| BIZ-CAP-017 | L1 | Order Management | — | ACTIVE | HIGH |
| BIZ-CAP-018 | L2 | Order Creation | BIZ-CAP-017 | ACTIVE | HIGH |
| BIZ-CAP-019 | L3 | Checkout Processing | BIZ-CAP-018 | ACTIVE | HIGH |
| BIZ-CAP-020 | L3 | Empty Basket Protection | BIZ-CAP-018 | ACTIVE | HIGH |
| BIZ-CAP-021 | L3 | Ordered Item Snapshot | BIZ-CAP-018 | ACTIVE | HIGH |
| BIZ-CAP-022 | L2 | Order Calculation | BIZ-CAP-017 | ACTIVE | HIGH |
| BIZ-CAP-023 | L3 | Order Total Calculation | BIZ-CAP-022 | ACTIVE | HIGH |
| BIZ-CAP-024 | L1 | Buyer / Customer Profile Management | — | ACTIVE | MEDIUM |
| BIZ-CAP-025 | L2 | Buyer Identity | BIZ-CAP-024 | ACTIVE | MEDIUM |
| BIZ-CAP-026 | L3 | Buyer Record Creation | BIZ-CAP-025 | ACTIVE | MEDIUM |
| BIZ-CAP-027 | L2 | Payment Information | BIZ-CAP-024 | **inferred** | LOW |
| BIZ-CAP-028 | L3 | Payment Method Management | BIZ-CAP-027 | **inferred** | LOW |
| BIZ-CAP-029 | L1 | Identity & Authentication | — | ACTIVE | HIGH |
| BIZ-CAP-030 | L2 | Access Control | BIZ-CAP-029 | ACTIVE | HIGH |
| BIZ-CAP-031 | L3 | User Login | BIZ-CAP-030 | ACTIVE | HIGH |
| BIZ-CAP-032 | L3 | Token Issuance | BIZ-CAP-030 | ACTIVE | HIGH |
| BIZ-CAP-033 | L2 | Identity Seeding | BIZ-CAP-029 | ACTIVE | HIGH |
| BIZ-CAP-034 | L3 | Identity Data Seeding | BIZ-CAP-033 | ACTIVE | HIGH |
| BIZ-CAP-035 | L1 | Admin Catalog Operations (Blazor) | — | ACTIVE | HIGH |
| BIZ-CAP-036 | L2 | Administrative Catalog Interface | BIZ-CAP-035 | ACTIVE | HIGH |
| BIZ-CAP-037 | L3 | Catalog Item List View | BIZ-CAP-036 | ACTIVE | HIGH |
| BIZ-CAP-038 | L3 | Catalog Item Create/Delete | BIZ-CAP-036 | ACTIVE | HIGH |
| BIZ-CAP-039 | L3 | Cached Data Refresh | BIZ-CAP-036 | ACTIVE | HIGH |

### 2.2 Actors

| ID | Actor | Type | Summary (from graph) |
|---|---|---|---|
| BIZ-ACT-001 | Customer / Buyer | human | Self-service storefront user: browses catalog, manages own basket, transfers anonymous basket on login, places/views orders, manages payment + shipping. Permission level Standard. Canonical merge of "Customer", "Buyer". |
| BIZ-ACT-002 | Anonymous Shopper | human | Unauthenticated visitor / anonymous session. Canonical merge of "anonymous user/shopper/session". |
| BIZ-ACT-003 | Administrator | human | Manages catalog items via the admin (Blazor) interface. |
| BIZ-ACT-004 | System / Service Account | system | Automated actor (incl. Seeder). Permission level Elevated. Canonical merge of "System", "Seeder". |
| BIZ-ACT-005 | Notification Recipients | external | External recipients of notifications. |

### 2.3 Business Processes

Triggers, rule references (BRxxx) and confidence are carried from the graph.
Several processes are value-stream stages only (no step-level breakdown in evidence)
and are therefore MEDIUM confidence — see ASSUMP-005.

| ID | Process | Trigger | Business rules | Confidence |
|---|---|---|---|---|
| BIZ-PROC-001 | Browse Catalog | Customer chooses to view available catalog items | — | MEDIUM |
| BIZ-PROC-002 | Add Item to Basket | Customer (or anonymous user) selects a catalog item to purchase | BR005 | HIGH |
| BIZ-PROC-003 | Transfer Anonymous Basket to Registered User | An anonymous user logs in or registers | BR005 | HIGH |
| BIZ-PROC-004 | Adjust Basket | Customer reviews their merged/finalized basket before checkout | BR006, BR007 | MEDIUM |
| BIZ-PROC-005 | Checkout / Place Order | Customer initiates checkout from their basket | BR009, BR010, BR011, BR012 | HIGH |
| BIZ-PROC-006 | Catalog Item Administration | Administrator manages catalog items via the admin (Blazor) interface | BR001, BR002, BR003, BR004 | HIGH |
| BIZ-PROC-007 | User Authentication | User submits login credentials via the API | — | HIGH |
| BIZ-PROC-008 | Buyer Record Creation | A buyer record needs creation against a valid identity account (no explicit trigger in evidence) | BR008 | MEDIUM |
| BIZ-PROC-009 | Catalog Seeding | System startup | — | MEDIUM |
| BIZ-PROC-010 | Identity Data Seeding | System startup | — | MEDIUM |

---

## 3. Data Architecture

### 3.1 Entities

`persisted` and `pii` flags, status and confidence are from the graph. Three nodes
are **aspirational/unimplemented** (Buyer, PaymentMethod, CatalogItemDetails);
Buyer/PaymentMethod are CONFIRMED dead/unmapped code (RC-002).

| ID | Entity | Persisted | PII | Status | Conf |
|---|---|---|---|---|---|
| DATA-ENT-001 | CatalogItem | yes | no | implemented | 0.80 |
| DATA-ENT-002 | CatalogBrand | yes | no | implemented | 0.80 |
| DATA-ENT-003 | CatalogType | yes | no | implemented | 0.80 |
| DATA-ENT-004 | Basket | yes | no | implemented | 0.80 |
| DATA-ENT-005 | BasketItem | yes | no | implemented | 0.80 |
| DATA-ENT-006 | Order | yes | **yes** | implemented | 0.80 |
| DATA-ENT-007 | OrderItem | yes | no | implemented | 0.80 |
| DATA-ENT-008 | ApplicationUser | yes | **yes** | implemented | 0.70 |
| DATA-ENT-009 | Role | yes | no | implemented | 0.70 |
| DATA-ENT-010 | Buyer | no | no | **aspirational/unimplemented** (RC-002 dead code) | 0.90 |
| DATA-ENT-011 | PaymentMethod | no | no | **aspirational/unimplemented** (RC-002 dead code) | 0.90 |
| DATA-ENT-012 | CatalogItemOrdered | yes | no | implemented (owned/value type, ItemOrdered_* snapshot) | 0.78 |
| DATA-ENT-013 | Address | yes | **yes** | implemented (owned/value type, ShipToAddress_* flattened) | 0.75 |
| DATA-ENT-014 | CatalogItemDetails | no | no | **aspirational/unimplemented** (likely DTO/read-model) | 0.72 |
| DATA-ENT-015 | BaseEntity | no | no | implemented (abstract base, no own table) | 0.80 |

### 3.2 Aggregates (root + members)

| ID | Aggregate | Root | Member entities | Status |
|---|---|---|---|---|
| DATA-AGG-001 | BasketAggregate | Basket | Basket, BasketItem | implemented |
| DATA-AGG-002 | OrderAggregate | Order | Order, OrderItem, Address, CatalogItemOrdered | implemented |
| DATA-AGG-003 | BuyerAggregate | Buyer | Buyer, PaymentMethod | **aspirational/unimplemented** (RC-002) |
| DATA-AGG-004 | CatalogItem | CatalogItem | CatalogItem (single-entity aggregate) | implemented |

> Note (OQ-006): DATA-AGG-004 (CatalogItem aggregate) and DATA-ENT-001 (CatalogItem
> entity) share a name but are kept **separate** — different node kinds.

### 3.3 Key Relationships

Cardinality and status from the graph. Cross-database links via `BuyerId` are
**soft (app-enforced, no DB FK)** references between CatalogDb and IdentityDb.

| ID | From → To | Cardinality | Status / note |
|---|---|---|---|
| DATA-REL-001 | CatalogItem → CatalogBrand | *..1 | implemented (CatalogBrandId FK) |
| DATA-REL-002 | CatalogItem → CatalogType | *..1 | implemented (CatalogTypeId FK) |
| DATA-REL-003 | Basket → BasketItem | 1..* | implemented |
| DATA-REL-004 | BasketItem → CatalogItem | *..1 | implemented |
| DATA-REL-005 | Order → OrderItem | 1..* | implemented |
| DATA-REL-006 | OrderItem → CatalogItemOrdered | 1..1 | implemented (owned type) |
| DATA-REL-007 | Order → Address | 1..1 | implemented (owned type) |
| DATA-REL-008 | Basket → ApplicationUser | *..1 | **implemented-soft-reference** (BuyerId cross-DB, app-enforced) |
| DATA-REL-009 | Order → ApplicationUser | *..1 | implemented-soft-reference (BuyerId cross-DB) |
| DATA-REL-010 | ApplicationUser → Role | *..* | implemented (Identity schema, INFERRED) |
| DATA-REL-011 | Basket → Order | 1..1 | implemented (basket converts to order at checkout) |
| DATA-REL-012 | Buyer → PaymentMethod | 1..* | aspirational/unimplemented |

### 3.4 Repositories

| ID | Repository | Kind | Entities served (cited) | Entities served (inferred) | Conf |
|---|---|---|---|---|---|
| DATA-REPO-001 | `IRepository<T>` | interface | CatalogItem, Basket | Order (OQ-008) | 0.85 |
| DATA-REPO-002 | `IReadRepository<T>` | interface | — | CatalogItem (OQ-008) | 0.80 |
| DATA-REPO-003 | CatalogContext | ef-dbcontext | CatalogItem, CatalogBrand, CatalogType, Basket, BasketItem, Order, OrderItem (7 DbSets) | — | 0.90 |
| DATA-REPO-004 | AppIdentityDbContext | ef-dbcontext | ApplicationUser, Role | — | 0.70 (Identity schema INFERRED) |

> Note (OQ-008): For DATA-REPO-001 the Order binding and for DATA-REPO-002 the
> CatalogItem binding are **inferences** (generic Repository+Specification pattern);
> not directly evidenced. Checkout persists Order via `IOrderService` (OrderService.cs).

---

## 4. Application Architecture

### 4.1 Modules and Deployable Services

47 services span logical module candidates, deployable runtime units, app-services,
EF contexts, seeders, endpoints, controllers, Razor PageModels, Blazor components and
decorators. Several module-candidate / deployable duplicates were merged (ASSUMP-001..003).

**Module candidates and deployable units (top level):**

| ID | Name | Kind | Owning module | Coupling / boundary | Conf |
|---|---|---|---|---|---|
| APP-SVC-001 | Catalog | module | Catalog | HIGH (score 13); Weak; migration Blocked | MEDIUM |
| APP-SVC-002 | Identity | module | Identity | — | MEDIUM |
| APP-SVC-003 | Basket | module | Basket | — | MEDIUM |
| APP-SVC-004 | Order | module | Order | — | MEDIUM |
| APP-SVC-005 | Admin | module | Admin | (logical module; see OQ-001) | MEDIUM |
| APP-SVC-006 | Web | module + deployable-service (`eshopwebmvc`) | Web | HIGH; Weak; Blocked | HIGH |
| APP-SVC-007 | ApplicationCore | module + library component | ApplicationCore | — | HIGH |
| APP-SVC-008 | DataAccess | module | DataAccess | — | MEDIUM |
| APP-SVC-009 | Infrastructure | module + library component | Infrastructure | — | HIGH |
| APP-SVC-010 | CrossCutting | module | CrossCutting | — | MEDIUM |
| APP-SVC-011 | PublicApi | module + deployable-service (`eshoppublicapi`) | PublicApi | — | HIGH |
| APP-SVC-012 | SharedContracts (= BlazorShared) | module + library component | SharedContracts | — | HIGH |
| APP-SVC-013 | Verification | module | Verification | — | LOW |
| APP-SVC-016 | BlazorAdmin | app-service (frontend SPA, **non-deployable**, served via Web host) | Admin | 11 API call mappings (APP-RISK-006) | HIGH |

**Notable component-level services** (selection; full list in JSON):
UriComposer (APP-SVC-020), IdentityTokenClaimService (APP-SVC-021), EfRepository
(APP-SVC-022, high coupling), CatalogContext (APP-SVC-023), AppIdentityDbContext
(APP-SVC-024), CatalogContextSeed (APP-SVC-025), AppIdentityDbContextSeed
(APP-SVC-026), the eight PublicApi endpoints (APP-SVC-029..036), MVC controllers
ManageController/OrderController/UserController (APP-SVC-037..039), cached catalog
decorators (APP-SVC-044/045), Blazor components (APP-SVC-046..051) and the host
bootstrap `Program` (APP-SVC-052).

### 4.2 Interfaces (ports / abstractions)

| ID | Interface | Kind | Implemented by / note |
|---|---|---|---|
| APP-IF-001 | `IRepository<T>` | abstraction | EfRepository (Repository pattern, 0.86) |
| APP-IF-002 | `IReadRepository<T>` | abstraction | read side of repository pattern |
| APP-IF-003 | `ITokenClaimsService` | port | IdentityTokenClaimService |
| APP-IF-004 | `IUriComposer` | abstraction | UriComposer |
| APP-IF-005 | `IAppLogger<T>` | abstraction | logging adapter |
| APP-IF-006 | `IBasketService` | abstraction | basket operations |
| APP-IF-007 | `IBasketQueryService` | abstraction | basket queries |
| APP-IF-008 | `IEmailSender` | port | email notification port |
| APP-IF-009 | `IAggregateRoot` | abstraction | aggregate-root marker |
| APP-IF-010 | `ICatalogItemService` | abstraction | catalog item ops (consumed by BlazorAdmin) |
| APP-IF-011 | `ICatalogLookupDataService` | abstraction | brand/type lookup |
| APP-IF-012 | `IMediator` | external | MediatR mediator |
| APP-IF-013 | `CustomAuthStateProvider` | UI | Blazor auth-state provider |

### 4.3 API Surface Summary

55 endpoints total. Counts by deployable unit (deployable assignment derived from
`source_file`, ASSUMP-004):

| Deployable unit | Endpoint count |
|---|---|
| Web (`eshopwebmvc`) | 43 |
| PublicApi (`eshoppublicapi`) | 9 |
| BlazorAdmin (frontend SPA) | 3 |
| **Total** | **55** |

Methods (graph-normalized; ROUTE/CLI are **synthetic** classifications per OQ-009,
not extracted HTTP verbs): GET 32, POST 13, ROUTE 5, CLI 3, DELETE 1, PUT 1.

**Representative endpoints (full list in JSON):**

PublicApi (REST, src/PublicApi):

| ID | Method | Path | Handler | Auth | Conf |
|---|---|---|---|---|---|
| APP-API-001 | POST | `/api/authenticate` | AuthenticateEndpoint | issues JWT (ITokenClaimsService + SignInManager) | HIGH |
| APP-API-002 | GET | `/api/catalog-brands` | CatalogBrandListEndpoint | not noted | HIGH |
| APP-API-003 | GET | `/api/catalog-items/{catalogItemId}` | CatalogItemGetByIdEndpoint | not noted | HIGH |
| APP-API-004 | GET | `/api/catalog-items` | CatalogItemListPagedEndpoint | not noted | HIGH |
| APP-API-005 | POST | `/api/catalog-items` | CreateCatalogItemEndpoint | not noted | HIGH |
| APP-API-006 | DELETE | `/api/catalog-items/{catalogItemId}` | DeleteCatalogItemEndpoint | not noted | HIGH |
| APP-API-007 | PUT | `/api/catalog-items` | UpdateCatalogItemEndpoint | not noted | HIGH |
| APP-API-008 | GET | `/api/catalog-types` | CatalogTypeListEndpoint | not noted | HIGH |
| APP-API-054 | CLI | Program.cs bootstrap (PublicApi) | Program | internal | MEDIUM |

Web (MVC + Razor Pages + Blazor Server host, src/Web — selection):

| ID | Method | Path | Handler |
|---|---|---|---|
| APP-API-012 | GET | `/home_page_health_check` | Program (health check) |
| APP-API-013 | GET | `/api_health_check` | Program (health check) |
| APP-API-014 | GET | `/Manage/MyAccount` | ManageController.MyAccount |
| APP-API-035 | GET | `/Order/MyOrders` | OrderController.MyOrders (IMediator.Send) |
| APP-API-036 | GET | `/Order/Detail/{orderId}` | OrderController.Detail (IMediator.Send) |
| APP-API-048 | GET | `/Admin/EditCatalogItem` | EditCatalogItem (Razor Page) |
| APP-API-050 | GET | `/Basket/Checkout` | Checkout (Razor Page) |
| APP-API-052 | GET | `/Basket/Success` | Success (Razor Page) |
| APP-API-009 | ROUTE | conventional MVC route registration | Program (synthetic, OQ-009) |

BlazorAdmin (frontend SPA, src/BlazorAdmin):

| ID | Method | Path | Handler |
|---|---|---|---|
| APP-API-039 | ROUTE | `/logout` | Logout.razor |
| APP-API-040 | ROUTE | `/admin` | List.razor (ICatalogItemService / ICatalogLookupDataService) |
| APP-API-053 | CLI | Program.cs bootstrap (BlazorAdmin) | Program |

### 4.4 Notable Dependencies (incl. the dependency cycle)

**Module dependency CYCLE — APP-DEP-001** (ARCH-VIOL-008 / APP-RISK-002):

```
Admin -> ApplicationCore -> Basket -> Catalog -> DataAccess -> Identity -> Order -> Web -> (back to Admin)
```

One module cycle detected. Whether this is a real runtime cycle or a
static-resolution artifact is **unresolved** (OQ-004) and flagged for human review.

**Layering violations — endpoints/PageModels calling EfRepository directly:**

| ID | From → To | Note |
|---|---|---|
| APP-DEP-002 | CatalogBrandListEndpoint → EfRepository | ARCH-VIOL-001 |
| APP-DEP-003 | CatalogItemGetByIdEndpoint → EfRepository | ARCH-VIOL-002 |
| APP-DEP-004 | CreateCatalogItemEndpoint → EfRepository | ARCH-VIOL-003 |
| APP-DEP-005 | DeleteCatalogItemEndpoint → EfRepository | ARCH-VIOL-004 |
| APP-DEP-006 | UpdateCatalogItemEndpoint → EfRepository | ARCH-VIOL-005 |
| APP-DEP-007 | CatalogTypeListEndpoint → EfRepository | ARCH-VIOL-006 |
| APP-DEP-008 | IndexModel → EfRepository | ARCH-VIOL-007 (Razor PageModel) |

**High-coupling components:** EfRepository (APP-DEP-009, coupling score 16,
ARCH-VIOL-009 / APP-RISK-004); UriComposer (APP-DEP-010, score 8, ARCH-VIOL-010).

**Project / runtime dependencies:** Web → ApplicationCore, BlazorAdmin, BlazorShared,
Infrastructure (APP-DEP-013); PublicApi → ApplicationCore, Infrastructure
(APP-DEP-012); Infrastructure → ApplicationCore (APP-DEP-014); ApplicationCore →
BlazorShared (APP-DEP-015, flagged unusual: domain → shared contracts); BlazorAdmin →
BlazorShared (APP-DEP-016). **No** project reference Web → PublicApi (APP-DEP-011).
Runtime HTTP: BlazorAdmin → PublicApi (`apiBase`, APP-DEP-017) and BlazorAdmin → Web
(`webBase`, APP-DEP-018). Runtime TCP/SQL: Web, PublicApi → sqlserver (APP-DEP-019).

---

## 5. Technology Architecture

### 5.1 Current Stack (grouped)

Versions largely **not declared** in evidence (VERSION UNKNOWN preserved).

**Runtime / frameworks**

| ID | Item | Version |
|---|---|---|
| TECH-CUR-001 | .NET SDK / Runtime | 8.0.x |
| TECH-CUR-002 | ASP.NET Core (Microsoft.NET.Sdk.Web) | 8.0 (SDK; no version declared) |
| TECH-CUR-003 | Blazor WebAssembly | 8.0 (SDK; package versions not declared) |
| TECH-CUR-004 | AspNetCore.Components.WebAssembly.Server | not declared |

**Data access / ORM**

| ID | Item | Version |
|---|---|---|
| TECH-CUR-005 | Entity Framework Core (ORM) | not declared |
| TECH-CUR-006 | EFCore.SqlServer (provider) | not declared |
| TECH-CUR-007 | Npgsql.EFCore.PostgreSQL (provider) | not declared |
| TECH-CUR-008 | EFCore.InMemory (provider) | not declared |
| TECH-CUR-009 | Ardalis.Specification (+ EntityFrameworkCore evaluator) | not declared |

**Application pattern / utility libraries**

| ID | Item |
|---|---|
| TECH-CUR-010 | Ardalis Guard/Result/ApiEndpoints |
| TECH-CUR-011 | MediatR |
| TECH-CUR-012 | AutoMapper (DI extensions) |
| TECH-CUR-013 | MinimalApi.Endpoint |
| TECH-CUR-014 | Swashbuckle.AspNetCore (+ SwaggerUI, + Annotations) |
| TECH-CUR-015 | FluentValidation |
| TECH-CUR-016 | System.Text.Json / System.Net.Http.Json |
| TECH-CUR-017 | Blazor client libs (Blazored.LocalStorage, BlazorInputFile, Extensions.Identity.Core) |
| TECH-CUR-018 | Extensions.Logging.Configuration |
| TECH-CUR-019 | AspNetCore.Diagnostics.EntityFrameworkCore |

**Containers / tooling / CI**

| ID | Item |
|---|---|
| TECH-CUR-023 | Docker base images (dotnet/sdk:8.0, dotnet/aspnet:8.0) |
| TECH-CUR-024 | Build & dev tooling (EF Core Tools, CodeGeneration.Design, Containers.Tools.Targets, BundlerMinifier, LibraryManager, WebAssembly.DevServer) |
| TECH-CUR-025 | Test tooling (xUnit, MSTest, NSubstitute, coverlet, NET.Test.Sdk, Mvc.Testing) |
| TECH-CUR-026 | GitHub Actions (checkout@v2, setup-dotnet@v1, RichCodeNavIndexer@v0.1) |

### 5.2 Data Stores

| ID | Store | Version | Note |
|---|---|---|---|
| TECH-CUR-020 | Azure SQL Edge (sqlserver container) | unknown (no tag; latest) | Docker env (OQ-003) |
| TECH-CUR-021 | PostgreSQL (eShopCatalog, eShopIdentity) | unknown | Default/local env (OQ-003) |
| TECH-CUR-022 | EF Core InMemory database | unknown | test/in-memory |

> Active DB provider (OQ-003): PostgreSQL (TECH-CUR-007) is default/local; SQL Server
> (TECH-CUR-006) is Docker-only. Both retained as ACTIVE in their respective scopes.

### 5.3 Infrastructure

| ID | Item | Type |
|---|---|---|
| TECH-INF-001 | `eshopwebmvc` container | Docker Compose service |
| TECH-INF-002 | `eshoppublicapi` container | Docker Compose service (port: see OQ-002, runtime binding 8080) |
| TECH-INF-003 | `sqlserver` container (Azure SQL Edge) | DB container |
| TECH-INF-004 | docker-compose orchestration | Container orchestration (3-service local stack) |
| TECH-INF-005 | GitHub Actions CI/CD | Pipelines (dotnetcore.yml build+test) |
| TECH-INF-006 | Dependabot (NuGet) | Dependency-management automation |
| TECH-INF-007 | Azure deployment (azd / parameters-only) | Cloud deployment target (declared, params only) |
| TECH-INF-008 | Azure Key Vault (referenced) | Secrets management (referenced) |

### 5.4 Security — Controls and Findings

**Implemented / referenced controls** (type = auth/authz/secrets):

| ID | Control | Type | Severity flag |
|---|---|---|---|
| TECH-SEC-001 | ASP.NET Core Identity (cookie auth + user store) | auth | — |
| TECH-SEC-002 | JWT Bearer Authentication | auth | High (enforcement unconfirmed, OQ-005) |
| TECH-SEC-003 | Blazor WASM Authentication (BlazorAdmin) | auth | High |
| TECH-SEC-004 | Authorization Components (role/claims-based) | authz | Medium |
| TECH-SEC-005 | .NET User Secrets (local dev) | secrets | — |
| TECH-SEC-006 | Azure Key Vault integration (referenced) | secrets | Medium |
| TECH-SEC-007 | Docker-mounted host secrets (read-only bind mounts) | secrets | — |

**Findings** (type = finding):

| ID | Finding | Severity |
|---|---|---|
| TECH-SEC-008 | Hardcoded PostgreSQL credentials in source-controlled config | **Critical** |
| TECH-SEC-009 | Hardcoded SQL Server / Azure SQL Edge SA password in config | **Critical** |
| TECH-SEC-010 | No JWT/authentication enforcement configured for PublicApi | High |
| TECH-SEC-011 | No CORS policy found despite required cross-origin calls | High |
| TECH-SEC-012 | No secret scanning in CI/CD | High |
| TECH-SEC-016 | No SAST / dependency / container vulnerability scanning in CI/CD | High |
| TECH-SEC-013 | SQL Server port 1433 published directly to host network | Medium |
| TECH-SEC-014 | No TLS termination for Docker/container traffic | Medium |
| TECH-SEC-015 | AllowedHosts wildcard + TrustServerCertificate=true | Medium |
| TECH-SEC-017 | No audit logging / compliance controls (RBAC, GDPR, PCI, retention) found | Medium |

> TECH-SEC-010 and TECH-SEC-011 remain **High-severity findings**, not promoted to
> implemented controls (OQ-005).

### 5.5 Target Stack

The knowledge graph carries **no target-stack nodes** (`technology.target_stack` is
empty). No target/aspirational technology is named in the evidence. Future forward
engineering must source target-state decisions externally; none can be asserted from
this foundation package.

---

## 6. Cross-Domain Linkage

The graph wires four chains: **capability → process → entity → service → API**.
Cross-links are emitted only where a source file supports them; confidence is carried
through each hop. Below are three worked examples.

### 6.1 Worked example — Checkout / Place Order

| Hop | Node(s) | Confidence |
|---|---|---|
| Capability (L3) | BIZ-CAP-019 Checkout Processing, BIZ-CAP-020 Empty Basket Protection, BIZ-CAP-021 Ordered Item Snapshot, BIZ-CAP-023 Order Total Calculation | HIGH |
| Process | BIZ-PROC-005 Checkout / Place Order (rules BR009–BR012) | HIGH |
| Entities | Basket (DATA-ENT-004, H), Order (DATA-ENT-006, H), OrderItem (DATA-ENT-007, H), CatalogItemOrdered (DATA-ENT-012, H), Address (DATA-ENT-013, H), CatalogItem (DATA-ENT-001, M) | HIGH/MEDIUM |
| Services | Order module (APP-SVC-004; persists Order/OrderItem/Address via IOrderService); Basket module (APP-SVC-003); CatalogContext (DATA-REPO-003) | HIGH |
| API | `/Basket/Checkout` (APP-API-050) and `/Basket/Success` (APP-API-052) on Web (`eshopwebmvc`); order views `/Order/MyOrders` (APP-API-035), `/Order/Detail/{orderId}` (APP-API-036) via OrderController → IMediator | — |

Process steps (graph): retrieve basket → verify not empty (block if empty —
empty-basket protection) → retrieve catalog item details → snapshot each ordered item
→ create order with buyer ID + shipping address + items → calculate order total. This
demonstrates the OrderAggregate (DATA-AGG-002) owned-type snapshots (CatalogItemOrdered,
Address) materializing during checkout.

### 6.2 Worked example — Catalog Item Maintenance (Admin, Blazor)

| Hop | Node(s) | Confidence |
|---|---|---|
| Capability (L3) | BIZ-CAP-037 Catalog Item List View, BIZ-CAP-038 Catalog Item Create/Delete, BIZ-CAP-039 Cached Data Refresh | HIGH |
| Process | BIZ-PROC-006 Catalog Item Administration (rules BR001–BR004) | HIGH |
| Entities | CatalogItem (DATA-ENT-001, H), CatalogBrand (DATA-ENT-002, M), CatalogType (DATA-ENT-003, M) | HIGH/MEDIUM |
| Services | Catalog module (APP-SVC-001, owns CatalogItem/Brand/Type + CatalogContext); BlazorAdmin SPA (APP-SVC-016) via ICatalogItemService/ICatalogLookupDataService; cached decorators (APP-SVC-044/045) for refresh | HIGH/MEDIUM |
| API | BlazorAdmin `/admin` (APP-API-040, List.razor) and `/logout` (APP-API-039); REST CRUD on PublicApi — `POST /api/catalog-items` (APP-API-005), `PUT /api/catalog-items` (APP-API-007), `DELETE /api/catalog-items/{id}` (APP-API-006), list/get (APP-API-003/004), brands/types (APP-API-002/008); Web admin Razor page `/Admin/EditCatalogItem` (APP-API-048) | HIGH |

Process steps (graph): admin views list of items/types/brands → creates a new item →
deletes an existing item → System refreshes the cached local catalog item list after
create/delete (Cached Data Refresh, RefreshBroadcast APP-SVC-049). The BlazorAdmin SPA
(non-deployable, served by the Web host) reaches the catalog CRUD endpoints over HTTP
(`apiBase` → PublicApi, APP-DEP-017).

### 6.3 Worked example — User Authentication / Token Issuance

| Hop | Node(s) | Confidence |
|---|---|---|
| Capability (L3) | BIZ-CAP-031 User Login, BIZ-CAP-032 Token Issuance | HIGH |
| Process | BIZ-PROC-007 User Authentication (login via the API) | HIGH |
| Entities | ApplicationUser (DATA-ENT-008, PII, H), Role (DATA-ENT-009, M) | HIGH/MEDIUM |
| Services | Identity module (APP-SVC-002); AuthenticateEndpoint (APP-SVC-029); IdentityTokenClaimService (APP-SVC-021) via ITokenClaimsService (APP-IF-003); AppIdentityDbContext (DATA-REPO-004) | HIGH |
| API | `POST /api/authenticate` (APP-API-001) on PublicApi — issues JWT via ITokenClaimsService + SignInManager.PasswordSignInAsync | HIGH |

Note (ASSUMP-004): the AuthenticateEndpoint handler is attributed to the **Identity**
owner module but is **hosted in the PublicApi** deployable; the service→api link
records both facets. JWT enforcement itself is unconfirmed (OQ-005, TECH-SEC-010).

---

## 7. Assumptions & Normalization

This section is explicit and separate from the canonical model above. It records the
consolidation decisions, the variant-collapse normalization log, and the open
questions still pending human review. All are reproduced from
`.work/assumptions.json`.

### 7.1 Assumptions

| ID | Statement (summary) | Impact |
|---|---|---|
| ASSUMP-001 | Module candidate `Web` (MOD-013) and deployable `eshopwebmvc` are the same unit, merged into APP-SVC-006. | Fewer nodes; split via `merged_from` if reviewer wants module vs deployable separated. |
| ASSUMP-002 | Module candidate `PublicApi` (MOD-010) and deployable `eshoppublicapi` merged into APP-SVC-011. | API cross-links use APP-SVC-011. |
| ASSUMP-003 | ApplicationCore, Infrastructure and SharedContracts/BlazorShared each merge their module-candidate and class-library facets. | Three fewer duplicates; facets in `merged_from`. |
| ASSUMP-004 | Deployable ownership derived from interface `source_file` (src/Web→Web, src/PublicApi→PublicApi, src/BlazorAdmin→BlazorAdmin), **not** a `deployable_unit` field (which does not exist in the catalogue). 47 service_to_api anchors rewritten to INT-NNN source_file + owner_module. | Handler-module attribution (e.g. AuthenticateEndpoint=Identity) noted via owner_module, not overridden. |
| ASSUMP-005 | Browse Catalog (BIZ-PROC-001) and Adjust Basket (BIZ-PROC-004) touch Catalog/Basket entities though they are value-stream stages, not step-level processes. | Those process→entity links carry LOW/MEDIUM confidence. |
| ASSUMP-006 | Role (DATA-ENT-009) owned by Identity via AppIdentityDbContext, mirroring ApplicationUser. | entity→service link MEDIUM (inferred Identity schema, 0.7). |
| ASSUMP-007 | Product name treated as `eShopOnWeb` for labeling while preserving the `unknown` caveat in metadata. | Naming only; no node semantics affected. |

### 7.2 Normalization Decisions (variant collapse)

| Canonical node | Collapsed variants | Rule |
|---|---|---|
| Customer / Buyer (BIZ-ACT-001) | Customer, Buyer, Customer / Buyer | Single canonical storefront user. |
| Anonymous Shopper (BIZ-ACT-002) | anonymous user / shopper / session | Single unauthenticated-visitor actor. |
| System / Service Account (BIZ-ACT-004) | System, Seeder | Single automated actor. |
| CatalogItem (DATA-ENT-001) | Catalog (table), Catalog Item, Product | C# entity class name canonical. |
| CatalogBrand (DATA-ENT-002) | CatalogBrands (table), Brand | Entity class canonical. |
| CatalogType (DATA-ENT-003) | CatalogTypes (table), Category, Type | Entity class canonical. |
| ApplicationUser (DATA-ENT-008) | AspNetUsers (table), Customer, User | Identity class canonical. |
| CatalogItemOrdered (DATA-ENT-012) | ItemOrdered (owned type) | Owned-type class name canonical. |
| Address (DATA-ENT-013) | ShipToAddress (owned type) | Owned-type class name canonical. |
| Web (APP-SVC-006) | MOD-013 Web, CAP-006 Controllers, eshopwebmvc | Merge module + deployable. |
| PublicApi (APP-SVC-011) | MOD-010 PublicApi, eshoppublicapi | Merge module + deployable. |
| ApplicationCore (APP-SVC-007) | MOD-002, CAP-008 Application, component | Merge module + component. |
| Infrastructure (APP-SVC-009) | MOD-008, component | Merge module + component. |
| SharedContracts (APP-SVC-012) | MOD-011 SharedContracts, BlazorShared | Merge module + BlazorShared library. |
| Ardalis.Specification (TECH-CUR-009) | Ardalis.Specification, ...EntityFrameworkCore | EF evaluator under the umbrella node (audit fix: previously mislinked to TECH-CUR-013). |

### 7.3 Open Questions (pending human review)

| ID | Question | Resolution / status |
|---|---|---|
| OQ-001 | Merge `Admin` module (APP-SVC-005) with deployable `BlazorAdmin` (APP-SVC-016)? | Kept **SEPARATE** (conservative) — logical module vs deployable artifact. |
| OQ-002 | PublicApi port: Dockerfile EXPOSE 80/443 vs compose 8080 (5200:8080). | Runtime binding **8080** (ASPNETCORE_URLS in compose); EXPOSE treated as stale. Both recorded. |
| OQ-003 | Active EF Core provider: PostgreSQL vs SQL Server / Azure SQL Edge. | Resolved per environment: PostgreSQL default/local, SQL Server Docker-only; both ACTIVE in scope. |
| OQ-004 | Is the module dependency cycle (APP-DEP-001) a real runtime cycle or static artifact? | **Unresolved** — recorded with the source's caveat; needs human review. |
| OQ-005 | Is JWT/auth enforced on PublicApi and is there a CORS policy? | **Unresolved** — kept as High-severity findings (TECH-SEC-010, TECH-SEC-011). |
| OQ-006 | Does CatalogItem aggregate (DATA-AGG-004) duplicate the CatalogItem entity (DATA-ENT-001)? | Kept **SEPARATE** — different node kinds. |
| OQ-007 | Authoritative system name. | Use `eShopOnWeb` label with `unknown` caveat in metadata. |
| OQ-008 | Does `IRepository<T>` serve Order, and which entity does `IReadRepository<T>` serve? | Demoted to inference (`entities_served_inferred`): Order on DATA-REPO-001, CatalogItem on DATA-REPO-002. |
| OQ-009 | Treat ROUTE/CLI method values on APP-API nodes as evidence-backed verbs? | Kept normalized ROUTE/CLI label but each carries a `method_note` marking it synthetic, not an extracted HTTP verb. |

---

*End of canonical enterprise model. Source of truth: `ENTERPRISE_KNOWLEDGE_GRAPH.json`
(schema 1.0). Assumptions/normalization/open questions: `.work/assumptions.json`.*
