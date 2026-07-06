# Architecture Pattern Report — eShopOnWeb

## 1. Primary Architecture Pattern

**Pattern:** Clean Architecture (Onion Architecture / DDD Layered Monolith)

**Confidence:** 0.97

**Evidence:**
- `src/ApplicationCore/` contains only domain entities, interfaces, and services with zero infrastructure dependencies — the innermost ring.
- `src/Infrastructure/` implements all ApplicationCore interfaces (`IRepository<T>`, `ITokenClaimsService`, `IEmailSender`, `IAppLogger`) — outer ring depends inward.
- `src/Infrastructure/Data/EfRepository.cs` implements `IRepository<T>` defined in ApplicationCore, never the reverse.
- `src/ApplicationCore/Interfaces/IAppLogger.cs` comment: _"eliminates need to depend directly on ASP.NET Core logging types"_ — explicit decoupling design intent documented in code.
- Dependency inversion observed: `BasketService` depends on `IRepository<Basket>` (ApplicationCore interface), resolved at runtime via `EfRepository<Basket>` (Infrastructure). Service layer never imports `Microsoft.EntityFrameworkCore` directly.

**Layers identified:**

| Layer | Project | Allowed Dependencies |
|---|---|---|
| Domain | ApplicationCore (Entities, Specifications, Interfaces) | None (only BCL + Ardalis.GuardClauses) |
| Application Service | ApplicationCore (Services) | Domain interfaces only |
| Infrastructure | Infrastructure | ApplicationCore interfaces, EF Core, ASP.NET Identity |
| API | PublicApi | ApplicationCore, Infrastructure (DI wiring) |
| Presentation (MVC) | Web | ApplicationCore, Infrastructure (DI wiring) |
| Presentation (SPA) | BlazorAdmin | BlazorShared, HTTP (no direct ApplicationCore reference) |
| Shared DTOs | BlazorShared | None (pure DTOs) |

---

## 2. Secondary Patterns Identified

### 2.1 Repository Pattern (Generic)

**Pattern:** Generic Repository with Specification pattern

**Implementation:** `EfRepository<T>` extends `Ardalis.Specification.EntityFrameworkCore.RepositoryBase<T>`, implementing both `IRepository<T>` (read/write) and `IReadRepository<T>` (read-only) from ApplicationCore.

**Evidence:** `src/Infrastructure/Data/EfRepository.cs` — single class handles all 7 domain aggregate types (Basket, Order, CatalogItem, CatalogBrand, CatalogType, and inferred others).

**Variant:** `BasketQueryService` bypasses `EfRepository` for a performance-critical SUM query using raw `DbContext` directly — a known pragmatic deviation documented in code.

---

### 2.2 Decorator Pattern (Caching)

**Pattern:** Transparent decorator wrapping domain services for browser-side caching

**Implementations:**
- `CachedCatalogItemServiceDecorator` wraps `ICatalogItemService` — adds 1-minute localStorage TTL for catalog items
- `CachedCatalogLookupDataServiceDecorator` wraps `ICatalogLookupDataService<T>` — same pattern for brands/types

**Evidence:** `src/BlazorAdmin/Services/CachedCatalogItemServiceDecorator.cs` — constructor takes `ICatalogItemService _catalogItemService` and delegates all calls, intercepting cache read/write around `List()` and `GetById()`.

**Cache tier:** Browser `localStorage` via `Blazored.LocalStorage`. Cache cleared on BlazorAdmin startup (`src/BlazorAdmin/Program.cs` — `await localStorage.ClearAsync()`).

---

### 2.3 Specification Pattern

**Pattern:** Encapsulated query criteria as objects

**Implementation:** Ardalis.Specification library; specifications in `src/ApplicationCore/Specifications/`

**Specifications identified:**
- `BasketWithItemsSpecification` — loads Basket with Include(BasketItems)
- `CatalogItemsSpecification` — bulk-loads CatalogItems by ID list (used in checkout)
- `CatalogFilterSpecification` — paginated catalog filter with brand/type predicates
- `CustomerOrdersSpecification` / `CustomerOrdersWithItemsSpecification` — orders by buyer
- `OrderWithItemsByIdSpec` — single order with items by ID

**Value:** Query logic never leaks into controllers/services; all filtering, includes, and ordering are encapsulated and reusable.

---

### 2.4 Domain-Driven Design (DDD)

**Pattern:** DDD tactical patterns — Aggregates, Value Objects, Domain Services, Guard Clauses

**Aggregate Roots identified:**
- `Basket` — encapsulates `BasketItem` list; no direct access to items
- `Order` — encapsulates `OrderItem` list; enforces invariant (no empty orders via constructor guard)
- `CatalogItem` — rich domain methods (`UpdateDetails`, `UpdateBrand`, `UpdatePrice`, etc.)
- `CatalogBrand`, `CatalogType` — simpler aggregates

**Value Objects identified:**
- `Address` — immutable, passed to Order constructor
- `CatalogItemOrdered` — price snapshot value object; comment in code explicitly documents temporal decoupling intent

**Domain Services:**
- `BasketService` — cross-aggregate operations (basket items, transfer, checkout guard)
- `OrderService` — checkout orchestration across 3 aggregates

**Guard Clauses:** `Ardalis.GuardClauses` + custom `GuardExtensions.cs` (`Guard.Against.EmptyBasketOnCheckout`)

---

### 2.5 Minimal API / Endpoint-per-Handler Pattern

**Pattern:** Single-responsibility API endpoint classes (REPR — Request-Endpoint-Response)

**Implementations:**
- `CatalogBrandListEndpoint` — `MinimalApi.Endpoint` base class; `MapEndpoint(IEndpointRouteBuilder app)` wires route
- `AuthenticateEndpoint` — `Ardalis.ApiEndpoints.EndpointBase` base class; `[HttpPost]` attribute

**Note:** Two different base class libraries are used — `MinimalApi.Endpoint` (newer pattern) and `Ardalis.ApiEndpoints` (older). Both follow the same single-responsibility intent but with different mechanisms, creating inconsistency in the API layer.

---

### 2.6 Service Collection Extension Pattern (DI Wiring)

**Pattern:** Infrastructure dependencies registered via static extension methods

**Implementation:** `src/Infrastructure/Dependencies.cs` (inferred from layer context) — AddInfrastructure() / AddApplicationCore() extension methods on IServiceCollection.

**Confidence:** 0.82 (file not directly in Layer 1, inferred from service registrations seen in PublicApi and BlazorAdmin startup)

---

## 3. Anti-Patterns and Pattern Deviations

| Deviation | Location | Severity | Description |
|---|---|---|---|
| God DbContext | `CatalogContext` | Medium | Single EF DbContext for 7 entity types across 3 bounded contexts (Catalog, Basket, Order). Violates aggregate boundary isolation. |
| Bypass of Repository | `BasketQueryService` | Low | Injects `CatalogContext` directly for SUM query, bypassing `EfRepository<T>` abstraction. Pragmatic but inconsistent. |
| Mixed API endpoint libraries | `PublicApi/` | Low | `CatalogBrandListEndpoint` uses `MinimalApi.Endpoint`; `AuthenticateEndpoint` uses `Ardalis.ApiEndpoints`. Should standardize. |
| Hardcoded secret in domain constant | `AuthorizationConstants` | Critical | JWT_SECRET_KEY hardcoded as a C# constant, not read from config/secrets. |
| Stub infrastructure in production path | `EmailSender` | Medium | `IEmailSender` registered in DI but implementation does nothing — silently drops all emails. No configuration flag or warning. |
| Browser cache as infrastructure | `CachedCatalogItemServiceDecorator` | Low | Uses browser localStorage as a cache tier for API responses. Not appropriate for multi-user scenarios and invisible to server-side observability. |
| Dead code aggregates | `Buyer`, `PaymentMethod` | Low | Entities and DbSet registered; no visible service or repository references — potential abandoned feature. |

---

## 4. Architecture Pattern Fitness Assessment

| Concern | Rating | Notes |
|---|---|---|
| Testability | High | ApplicationCore has zero infrastructure dependencies — unit testing domain logic requires no EF mocking |
| Separation of concerns | High | Clean layer boundaries maintained for domain + infrastructure |
| Domain cohesion | High | Aggregates properly encapsulate invariants |
| Scalability | Low | Single SQL Server, single process (MVC monolith) — no horizontal scaling mechanism |
| Observability | Low | IAppLogger abstraction exists but no structured logging, no distributed tracing, no health check endpoints visible |
| Security | Low | Hardcoded JWT secret is a production blocker; EmailSender stub could mask account verification failures silently |
| API consistency | Medium | Two endpoint patterns in use; catalog CRUD endpoints not fully visible |
| Caching strategy | Low | Only browser localStorage — no server-side caching (Redis/Memory); vulnerable to cache stampede on cold start |
