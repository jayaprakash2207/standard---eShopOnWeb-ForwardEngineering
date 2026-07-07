# Architecture Pattern Report — eShopOnWeb

Generated from source evidence. Unknown items are marked as unknown.

---

## Detected Primary Pattern

**Clean Architecture (also called Onion Architecture)**

**Confidence: 0.90**

---

## Evidence

### 1. Dependency Rule — Dependencies point inward

```
Presentation / API Layer  ──►  ApplicationCore (interfaces only)
Infrastructure Layer       ──►  ApplicationCore (implements interfaces)
ApplicationCore            ──►  (nothing external — pure .NET)
```

**Source evidence:**
- `src/ApplicationCore/Interfaces/IRepository.cs` — `IRepository<T>` defined in core; implemented in Infrastructure by `EfRepository<T>`
- `src/ApplicationCore/Interfaces/IBasketService.cs` — service contract defined in core; consumed by Web/PublicApi
- `src/Infrastructure/Data/EfRepository.cs` — Infrastructure implements core interfaces without core knowing about EF
- `src/ApplicationCore/Interfaces/IAppLogger.cs` — comment: "eliminates the need to depend directly on the ASP.NET Core logging types"
- `src/Infrastructure/Logging/LoggerAdapter.cs` — wraps Microsoft.Extensions.Logging; core only knows `IAppLogger<T>`

### 2. Entities with Domain Behavior (not Anemic)

- `src/ApplicationCore/Entities/BasketAggregate/Basket.cs` — `AddItem()`, `RemoveEmptyItems()`, `SetNewBuyerId()` on entity
- `src/ApplicationCore/Entities/OrderAggregate/Order.cs` — `Total()` calculation on entity; DDD comment about private collection
- `src/ApplicationCore/Entities/CatalogItem.cs` — `UpdateDetails()`, `UpdateBrand()`, `UpdateType()`, `UpdatePictureUri()` with Guard validation

### 3. Aggregate Root Pattern (DDD-Lite)

- `IAggregateRoot` marker interface at `src/ApplicationCore/Interfaces/IAggregateRoot.cs`
- `Basket`, `Order`, `CatalogBrand`, `CatalogItem`, `CatalogType` all implement `IAggregateRoot`
- `IRepository<T> where T : IAggregateRoot` constrains the generic repository to aggregate roots only

### 4. Repository Pattern with Specification

- `Ardalis.Specification` used; Specifications defined in `src/ApplicationCore/Specifications/`
- `BasketWithItemsSpecification`, `CatalogItemsSpecification`, `CustomerOrdersSpecification` — encapsulate query logic in ApplicationCore
- `EfRepository<T>` extends `RepositoryBase<T>` — infrastructure detail hidden behind interface

### 5. Application Service Layer

- `BasketService`, `OrderService`, `UriComposer` in `src/ApplicationCore/Services/` — pure application orchestration
- No direct framework references in ApplicationCore services

### 6. Separation of DbContexts

- `CatalogContext` for business domain (`src/Infrastructure/Data/CatalogContext.cs`)
- `AppIdentityDbContext` for identity (`src/Infrastructure/Identity/AppIdentityDbContext.cs`)
- Two connection strings: `CatalogConnection` and `IdentityConnection`

---

## Why This Pattern Was Selected Over Alternatives

| Pattern | Why Rejected |
|---|---|
| Simple N-Tier (3-Tier) | Dependency inversion present; Core has no dependency on Infrastructure |
| Hexagonal / Ports & Adapters | Very similar; could be described as Ports & Adapters but C# community naming for this layout is Clean Architecture |
| Big Ball of Mud | Clear layering, interface abstractions, and aggregate roots rule this out |
| Microservices | Single deployable Web monolith + PublicApi; shared database; no event bus |
| Modular Monolith | Module boundaries are partially logical (namespace-based) not enforced at project level |

---

## Secondary Pattern: Decorator Pattern (Blazor Services)

`CachedCatalogItemServiceDecorator` and `CachedCatalogLookupDataServiceDecorator<TLookupData, TResponse>` implement the Decorator pattern over Blazor catalog services.

**Evidence:** `src/BlazorAdmin/ServicesConfiguration.cs` — `AddScoped<ICatalogItemService, CachedCatalogItemServiceDecorator>` wrapping `CatalogItemService`.

---

## Architecture Violations Against Clean Architecture Rules

### Violation 1 — Single Shared DbContext Crosses Domain Boundaries

**Severity: Medium**

`CatalogContext` owns `Basket`, `Order`, AND `CatalogItem` in a single EF context. In Clean Architecture, each aggregate/domain should ideally own its persistence boundary. This creates infrastructure coupling across the Basket, Order, and Catalog modules.

**File:** `src/Infrastructure/Data/CatalogContext.cs`

### Violation 2 — OrderService Directly Reads Basket Data (Cross-Aggregate Service)

**Severity: Medium**

`OrderService.CreateOrderAsync` directly injects and uses `IRepository<Basket>`. This means Order module depends on Basket module's internal data representation. In stricter DDD, Order should consume a domain event or a dedicated checkout DTO — not directly pull from Basket.

**File:** `src/ApplicationCore/Services/OrderService.cs`

### Violation 3 — Infrastructure Layer Reaches Upward to BlazorShared Models

**Severity: Low**

`BlazorAdmin/Services/CatalogItemService.cs` returns `BlazorShared.Models.CatalogItem` — a shared frontend DTO — rather than mapping from a clean Application-layer response model. The frontend service layer conflates DTO and domain model.

### Violation 4 — Hardcoded Security Constants in ApplicationCore

**Severity: High (Security)**

`AuthorizationConstants.JWT_SECRET_KEY` is a hardcoded string in `src/ApplicationCore/Constants/AuthorizationConstants.cs`. This belongs in environment variables, not source code.

**File:** `src/ApplicationCore/Constants/AuthorizationConstants.cs`

### Violation 5 — EmailSender Stub Not Implemented

**Severity: Low (Completeness)**

`src/Infrastructure/Services/EmailSender.cs` returns `Task.CompletedTask` with a TODO. If account confirmation or password reset is wired, emails silently disappear.

---

## Forward Engineering Implications

1. **Strong foundation** — Clean Architecture layers make it feasible to extract individual modules (Basket, Catalog, Order) into separate services using strangler pattern.
2. **CatalogContext is the migration blocker** — shared DbContext must be split before any microservice extraction.
3. **ApplicationCore is nearly infrastructure-free** — can be directly reused or ported in a new service.
4. **Specification pattern is portable** — `Ardalis.Specification` works with any EF target; re-use in extracted service is low-cost.
5. **BlazorAdmin is tightly coupled to PublicApi URL configuration** — URL-based coupling means extracting catalog API requires updating Blazor config.
