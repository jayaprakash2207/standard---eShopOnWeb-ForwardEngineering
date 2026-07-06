## 🔍 Agent 1 — Chunk 0 of 6 — Project-Wide Structural Scan

---

### Project Scan Summary

- **Language(s):** C# / .NET 6+
- **Framework(s):** ASP.NET Core, Blazor WebAssembly, Entity Framework Core, ASP.NET Core Identity, JWT Bearer, Ardalis.Specification, Ardalis.GuardClauses
- **Architecture Style:** Modular Monolith — Clean Architecture / DDD layering within a single solution (multiple projects, not microservices)
- **Solution Layout:** 6 source projects + 1 infrastructure folder + 1 shared library

---

### Folder Structure (Top-Level → One Level Down)

```
src/
├── ApplicationCore/          ← Domain layer (entities, services, interfaces, specs)
│   ├── Entities/
│   │   ├── BasketAggregate/  (Basket, BasketItem)
│   │   ├── BuyerAggregate/   (Buyer, PaymentMethod)
│   │   └── OrderAggregate/   (Order, OrderItem, Address, CatalogItemOrdered)
│   ├── Constants/
│   ├── Exceptions/
│   ├── Extensions/
│   ├── Interfaces/
│   ├── Services/
│   └── Specifications/
├── Infrastructure/           ← Infrastructure layer (EF, Identity, Logging, Email)
│   ├── Data/
│   │   └── Queries/
│   ├── Identity/
│   ├── Logging/
│   └── Services/
├── PublicApi/                ← REST API project (Minimal API endpoints)
│   ├── AuthEndpoints/
│   ├── CatalogBrandEndpoints/
│   ├── CatalogItemEndpoints/
│   ├── CatalogTypeEndpoints/
│   └── Middleware/
├── Web/                      ← Customer-facing MVC/Razor Pages web app
│   └── Areas/Identity/Pages/Account/
├── BlazorAdmin/              ← Admin SPA (Blazor WebAssembly)
│   ├── Helpers/
│   ├── JavaScript/
│   ├── Pages/CatalogItemPage/
│   ├── Services/
│   └── Shared/
└── BlazorShared/             ← Shared library (BlazorAdmin ↔ Web)
    ├── Attributes/
    ├── Authorization/
    ├── Interfaces/
    └── Models/

infra/                        ← Azure deployment infrastructure (Bicep/ARM) — excluded from business analysis
```

---

### File Inventory by Type

| Artifact Type | Paths |
|---|---|
| **Entity / Model files** | `src/ApplicationCore/Entities/BaseEntity.cs`, `CatalogItem.cs`, `CatalogBrand.cs`, `CatalogType.cs`, `BasketAggregate/Basket.cs`, `BasketAggregate/BasketItem.cs`, `BuyerAggregate/Buyer.cs`, `BuyerAggregate/PaymentMethod.cs`, `OrderAggregate/Order.cs`, `OrderAggregate/OrderItem.cs`, `OrderAggregate/Address.cs`, `OrderAggregate/CatalogItemOrdered.cs` |
| **API route files** | `src/PublicApi/AuthEndpoints/AuthenticateEndpoint.cs`, `PublicApi/CatalogBrandEndpoints/CatalogBrandListEndpoint.cs`, `PublicApi/CatalogItemEndpoints/CatalogItemGetByIdEndpoint.cs`, `PublicApi/CatalogItemEndpoints/CatalogItemListPagedEndpoint.cs`, `PublicApi/CatalogItemEndpoints/CreateCatalogItemEndpoint.cs`, `PublicApi/CatalogItemEndpoints/DeleteCatalogItemEndpoint.cs`, `PublicApi/CatalogItemEndpoints/UpdateCatalogItemEndpoint.cs`, `PublicApi/CatalogTypeEndpoints/CatalogTypeListEndpoint.cs` |
| **Config / env files** | `src/PublicApi/appsettings.json`, `appsettings.Development.json`, `appsettings.Docker.json`, `src/Web/appsettings.Development.json`, `src/Web/appsettings.Docker.json`, `src/BlazorAdmin/wwwroot/appsettings.json`, `infra/main.parameters.json` |
| **Integration client files** | `src/Infrastructure/Services/EmailSender.cs`, `src/BlazorAdmin/Services/HttpService.cs`, `src/Infrastructure/Identity/IdentityTokenClaimService.cs` |
| **Service files** | `src/ApplicationCore/Services/BasketService.cs`, `OrderService.cs`, `UriComposer.cs`, `src/Infrastructure/Data/Queries/BasketQueryService.cs`, `src/Infrastructure/Identity/IdentityTokenClaimService.cs` |
| **DB / EF context** | `src/Infrastructure/Data/CatalogContext.cs`, `src/Infrastructure/Data/EfRepository.cs`, `src/Infrastructure/Data/CatalogContextSeed.cs`, `src/Infrastructure/Identity/AppIdentityDbContextSeed.cs` |
| **Authorization constants** | `src/ApplicationCore/Constants/AuthorizationConstants.cs`, `src/BlazorShared/Authorization/Constants.cs` |
| **Specification files** | `src/ApplicationCore/Specifications/` (6 spec files) |

---

### Domains Identified

| # | Domain | Primary Projects | Notes |
|---|---|---|---|
| 1 | **Catalog** | ApplicationCore, PublicApi, BlazorAdmin | CatalogItem, CatalogBrand, CatalogType — full CRUD API |
| 2 | **Basket** | ApplicationCore, Infrastructure, Web | Basket + BasketItem aggregates, anonymous → user transfer |
| 3 | **Order** | ApplicationCore, Web | Order + OrderItem aggregate, checkout flow |
| 4 | **Buyer / Identity** | ApplicationCore, Infrastructure | Buyer, PaymentMethod, ASP.NET Core Identity, JWT |
| 5 | **Admin UI** | BlazorAdmin, BlazorShared | Blazor WASM SPA calling PublicApi |
| 6 | **Web (Customer-Facing)** | Web | MVC/Razor Pages, login/register, basket UI |

---

### Chunk Plan (Ordered: Highest Complexity First)

| Chunk | Domain | Reason for Priority |
|---|---|---|
| **Chunk 1** | Catalog Domain (ApplicationCore entities + PublicApi endpoints) | Highest entity density; full CRUD surface; most API routes; role-gated mutations |
| **Chunk 2** | Basket & Order Domain (ApplicationCore) | Core transaction domain; two DDD aggregates; complex checkout sequence; cross-domain state dependencies |
| **Chunk 3** | Buyer, Identity & Auth (ApplicationCore + Infrastructure) | JWT token issuance; role seeding; access control boundary; cross-cutting to all domains |
| **Chunk 4** | Infrastructure (Data, Repos, Logging, Email) | EF entity mapping, seed data, repository pattern — confirms entity field ground truth |
| **Chunk 5** | BlazorAdmin + BlazorShared | Admin SPA service layer; caching decorators; shared DTO contracts; UI-facing API surface |
| **Chunk 6** | Web (Customer-Facing MVC) | Login/register/basket transfer flows; limited source data available from extraction |

---

✅ **Chunk 0 Complete.**
Proceeding to Chunk 1 — Catalog Domain.

---

## 📥 Agent 1 — Chunk 1 of 6 — Catalog Domain

**Carried Forward from Prior Chunks:**
- Entities: *(none yet — this is the first entity chunk)*
- States: *(none yet)*
- Roles: *(none yet)*

---

### Entities

**CatalogItem** — `src/ApplicationCore/Entities/CatalogItem.cs`

| Field | Type |
|---|---|
| Id | int (inherited from BaseEntity) |
| Name | string |
| Description | string |
| Price | decimal |
| PictureUri | string |
| CatalogTypeId | int (FK) |
| CatalogType | CatalogType? (nav) |
| CatalogBrandId | int (FK) |
| CatalogBrand | CatalogBrand? (nav) |

Methods (signatures only): `UpdateDetails(CatalogItemDetails)`, `UpdateBrand(int)`, `UpdateType(int)`, `UpdatePictureUri(string)`
Inner record: `CatalogItemDetails { Name?, Description?, Price }`
Implements: `IAggregateRoot`

**CatalogBrand** — `src/ApplicationCore/Entities/CatalogBrand.cs`

| Field | Type |
|---|---|
| Id | int (inherited) |
| Brand | string |

Implements: `IAggregateRoot`

**CatalogType** — `src/ApplicationCore/Entities/CatalogType.cs`

| Field | Type |
|---|---|
| Id | int (inherited) |
| Name (via LookupData) | — |
| Type | string |

Implements: `IAggregateRoot`

---

### API Routes (PublicApi — Catalog)

| HTTP Verb | Route | Handler | Role Guard |
|---|---|---|---|
| GET | `api/catalog-brands` | `CatalogBrandListEndpoint.HandleAsync` | None |
| GET | `api/catalog-items` | `CatalogItemListPagedEndpoint.HandleAsync` | None |
| GET | `api/catalog-items/{catalogItemId}` | `CatalogItemGetByIdEndpoint.HandleAsync` | None |
| POST | `api/catalog-items` | `CreateCatalogItemEndpoint.HandleAsync` | `ADMINISTRATORS` (JWT) |
| DELETE | `api/catalog-items/{catalogItemId}` | `DeleteCatalogItemEndpoint.HandleAsync` | `ADMINISTRATORS` (JWT) |
| PUT | `api/catalog-items` | `UpdateCatalogItemEndpoint.HandleAsync` | `ADMINISTRATORS` (JWT) |
| GET | `api/catalog-types` | `CatalogTypeListEndpoint.HandleAsync` | None |

---

### Specifications (Catalog)

| Spec Class | Purpose (name only) | File |
|---|---|---|
| `CatalogFilterSpecification` | Filter by brandId + typeId | `src/ApplicationCore/Specifications/CatalogFilterSpecification.cs` |
| `CatalogFilterPaginatedSpecification` | Filter + paginate (skip/take) | `src/ApplicationCore/Specifications/CatalogFilterPaginatedSpecification.cs` |
| `CatalogItemNameSpecification` | Filter by exact name | `src/ApplicationCore/Specifications/CatalogItemNameSpecification.cs` |
| `CatalogItemsSpecification` | Filter by array of IDs | `src/ApplicationCore/Specifications/CatalogItemsSpecification.cs` |

---

### Roles (Catalog-Scoped)

| Role | Gated Actions |
|---|---|
| `ADMINISTRATORS` | `POST api/catalog-items`, `DELETE api/catalog-items/{id}`, `PUT api/catalog-items` |

Auth scheme: `JwtBearerDefaults.AuthenticationScheme`
Role constant: `BlazorShared.Authorization.Constants.Roles.ADMINISTRATORS = "Administrators"`

---

### Integrations (Catalog)

- `IUriComposer.ComposePicUri()` — transforms stored PictureUri template using `CatalogBaseUrl` from `CatalogSettings.CatalogBaseUrl` config
- `IRepository<CatalogItem>` / `IRepository<CatalogBrand>` / `IRepository<CatalogType>` — EF-backed via `EfRepository`

---

### 📦 Chunk Inventory — Catalog Domain

- **Entities found this chunk:** CatalogItem, CatalogBrand, CatalogType
- **States found this chunk:** None (no lifecycle state enum on catalog entities)
- **Roles found this chunk:** `ADMINISTRATORS`
- **Services / capabilities detected:**
  - `CreateCatalogItemEndpoint` → `HandleAsync(CreateCatalogItemRequest, IRepository<CatalogItem>): Task<IResult>` — Catalog Item Creation
  - `DeleteCatalogItemEndpoint` → `HandleAsync(DeleteCatalogItemRequest, IRepository<CatalogItem>): Task<IResult>` — Catalog Item Deletion
  - `UpdateCatalogItemEndpoint` → `HandleAsync(UpdateCatalogItemRequest, IRepository<CatalogItem>): Task<IResult>` — Catalog Item Update
  - `CatalogItemGetByIdEndpoint` → `HandleAsync(GetByIdCatalogItemRequest, IRepository<CatalogItem>): Task<IResult>` — Catalog Item Retrieval
  - `CatalogItemListPagedEndpoint` → `HandleAsync(ListPagedCatalogItemRequest, IRepository<CatalogItem>): Task<IResult>` — Paged Catalog Listing
  - `CatalogBrandListEndpoint` → `HandleAsync(IRepository<CatalogBrand>): Task<IResult>` — Brand Listing
  - `CatalogTypeListEndpoint` → `HandleAsync(IRepository<CatalogType>): Task<IResult>` — Type Listing
- **Integrations detected:** IUriComposer (CatalogBaseUrl), EF Core repositories
- **Cross-domain dependencies flagged:** CatalogItem → referenced by OrderAggregate (CatalogItemOrdered), BasketAggregate (BasketItem.CatalogItemId), and OrderService — 🔗 SHARED ENTITY
- **Newly flagged as SHARED ENTITY:** CatalogItem (referenced in Basket, Order, and Admin domains)
- **LOW CONFIDENCE items raised:** None

---

## 📥 Agent 1 — Chunk 2 of 6 — Basket & Order Domain

**Carried Forward from Prior Chunks:**
- Entities: CatalogItem 🔗 SHARED, CatalogBrand, CatalogType
- States: *(none)*
- Roles: `ADMINISTRATORS`

---

### Entities

**Basket** — `src/ApplicationCore/Entities/BasketAggregate/Basket.cs`

| Field | Type |
|---|---|
| Id | int (inherited) |
| BuyerId | string |
| Items | IReadOnlyCollection\<BasketItem\> |
| TotalItems | int (computed) |

Methods: `AddItem(int, decimal, int)`, `RemoveEmptyItems()`, `SetNewBuyerId(string)`
Implements: `IAggregateRoot`

**BasketItem** — `src/ApplicationCore/Entities/BasketAggregate/BasketItem.cs`

| Field | Type |
|---|---|
| Id | int (inherited) |
| UnitPrice | decimal |
| Quantity | int |
| CatalogItemId | int (FK → CatalogItem) |
| BasketId | int (FK → Basket) |

Methods: `AddQuantity(int)`, `SetQuantity(int)`

**Order** — `src/ApplicationCore/Entities/OrderAggregate/Order.cs`

| Field | Type |
|---|---|
| Id | int (inherited) |
| BuyerId | string |
| OrderDate | DateTimeOffset (default: now) |
| ShipToAddress | Address (value object) |
| OrderItems | IReadOnlyCollection\<OrderItem\> |

Methods: `Total(): decimal`
Implements: `IAggregateRoot`

**OrderItem** — `src/ApplicationCore/Entities/OrderAggregate/OrderItem.cs`

| Field | Type |
|---|---|
| Id | int (inherited) |
| ItemOrdered | CatalogItemOrdered (value object, snapshot) |
| UnitPrice | decimal |
| Units | int |

**Address** — `src/ApplicationCore/Entities/OrderAggregate/Address.cs` *(Value Object)*

| Field | Type |
|---|---|
| Street | string |
| City | string |
| State | string |
| Country | string |
| ZipCode | string |

**CatalogItemOrdered** — `src/ApplicationCore/Entities/OrderAggregate/CatalogItemOrdered.cs` *(Value Object — snapshot)*

| Field | Type |
|---|---|
| CatalogItemId | int |
| ProductName | string |
| PictureUri | string |

**Basket & Order Services**

`BasketService` — `src/ApplicationCore/Services/BasketService.cs`
- `AddItemToBasket(string username, int catalogItemId, decimal price, int quantity): Task<Basket>`
- `DeleteBasketAsync(int basketId): Task`
- `SetQuantities(int basketId, Dictionary<string, int> quantities): Task<Result<Basket>>`
- `TransferBasketAsync(string anonymousId, string userName): Task`

`OrderService` — `src/ApplicationCore/Services/OrderService.cs`
- `CreateOrderAsync(int basketId, Address shippingAddress): Task`

---

### Specifications (Basket & Order)

| Spec Class | Purpose (name only) | File |
|---|---|---|
| `BasketWithItemsSpecification` | Basket by ID or BuyerId, includes Items | `src/ApplicationCore/Specifications/BasketWithItemsSpecification.cs` |
| `CustomerOrdersSpecification` | Orders by BuyerId, includes OrderItems | `src/ApplicationCore/Specifications/CustomerOrdersSpecification.cs` |
| `CustomerOrdersWithItemsSpecification` | Orders by BuyerId, includes OrderItems + ItemOrdered | `src/ApplicationCore/Specifications/CustomerOrdersWithItemsSpecification.cs` |
| `OrderWithItemsByIdSpec` | Order by Id, includes OrderItems + ItemOrdered | `src/ApplicationCore/Specifications/OrderWithItemsByIdSpec.cs` |

---

### States (Basket & Order)

No explicit lifecycle state enum found on Basket or Order entities in the provided source data. Order has `OrderDate` (timestamp) but no status field declared.

⚠️ ARCHITECTURE NOTE: `Order` entity has no `Status` or `OrderStatus` field in the declared properties. Either order lifecycle states are not modelled in this version, or they exist outside the provided extraction scope. Agent 2 to verify from full source scan.

---

### Exceptions (Domain)

| Exception | Trigger Condition |
|---|---|
| `BasketNotFoundException` | Basket not found by ID |
| `EmptyBasketOnCheckoutException` | Basket has zero items at checkout |
| `DuplicateException` | Catalog item with same name already exists |

---

### 📦 Chunk Inventory — Basket & Order Domain

- **Entities found this chunk:** Basket, BasketItem, Order, OrderItem, Address (ValueObject), CatalogItemOrdered (ValueObject)
- **States found this chunk:** None declared on domain entities
- **Roles found this chunk:** None new
- **Services / capabilities detected:**
  - `BasketService` → `AddItemToBasket(...)`, `DeleteBasketAsync(...)`, `SetQuantities(...)`, `TransferBasketAsync(...)` — Basket Management
  - `OrderService` → `CreateOrderAsync(int, Address)` — Order Creation
- **Integrations detected:** `IRepository<Basket>`, `IRepository<Order>`, `IRepository<CatalogItem>` (cross-domain read), `IUriComposer` (pic URI composition during order creation)
- **Cross-domain dependencies flagged:** OrderService reads `IRepository<CatalogItem>` — 🔗 Cross-domain dependency: Order domain reads Catalog domain at order creation time
- **Newly flagged as SHARED ENTITY:** Basket (referenced by Web login flow `TransferBasketAsync`), Order (referenced by Web customer order history pages)
- **LOW CONFIDENCE items raised:**
  - ⚠️ LOW — `Order` has no status/lifecycle field visible in extraction; order state machine may be absent or out of extraction scope

---

## 📥 Agent 1 — Chunk 3 of 6 — Buyer, Identity & Auth Domain

**Carried Forward from Prior Chunks:**
- Entities: CatalogItem 🔗 SHARED, CatalogBrand, CatalogType, Basket 🔗 SHARED, BasketItem, Order 🔗 SHARED, OrderItem, Address, CatalogItemOrdered
- States: *(none domain-level)*
- Roles: `ADMINISTRATORS`

---

### Entities

**Buyer** — `src/ApplicationCore/Entities/BuyerAggregate/Buyer.cs`

| Field | Type |
|---|---|
| Id | int (inherited) |
| IdentityGuid | string |
| PaymentMethods | IEnumerable\<PaymentMethod\> |

Implements: `IAggregateRoot`

**PaymentMethod** — `src/ApplicationCore/Entities/BuyerAggregate/PaymentMethod.cs`

| Field | Type |
|---|---|
| Id | int (inherited) |
| Alias | string? |
| CardId | string? (⚠️ NOTE: comment says actual card data must be in PCI-compliant system like Stripe) |
| Last4 | string? |

⚠️ ARCHITECTURE NOTE: `PaymentMethod.CardId` has a code comment explicitly noting PCI compliance — actual card data is NOT stored here; this is a reference/token only. Agent 2 to flag in security/compliance section.

---

### Auth Constants

**AuthorizationConstants** — `src/ApplicationCore/Constants/AuthorizationConstants.cs`

| Constant | Value |
|---|---|
| `AUTH_KEY` | `"AuthKeyOfDoomThatMustBeAMinimumNumberOfBytes"` ⚠️ TODO comment present |
| `DEFAULT_PASSWORD` | `"Pass@word1"` ⚠️ TODO: "Don't use in production" |
| `JWT_SECRET_KEY` | `"SecretKeyOfDoomThatMustBeAMinimumNumberOfBytes"` ⚠️ TODO: "Change to environment variable" |

⚠️ ARCHITECTURE NOTE: Three hardcoded security constants carry explicit TODO comments warning against production use. These are demo/sample values. Agent 2 to flag as critical security findings.

**BlazorShared Authorization Constants** — `src/BlazorShared/Authorization/Constants.cs`

| Constant | Value |
|---|---|
| `Roles.ADMINISTRATORS` | `"Administrators"` |

---

### Identity Services

**IdentityTokenClaimService** — `src/Infrastructure/Identity/IdentityTokenClaimService.cs`
- `GetTokenAsync(string userName): Task<string>`
- Issues JWT tokens; 7-day expiry; HMAC-SHA256; roles embedded as claims

**AppIdentityDbContextSeed** — `src/Infrastructure/Identity/AppIdentityDbContextSeed.cs`
- Seeds: role `Administrators`, user `demouser@microsoft.com`, admin `admin@microsoft.com`
- Both users seeded with `AuthorizationConstants.DEFAULT_PASSWORD`

---

### API Routes (Auth)

| HTTP Verb | Route | Handler | Role Guard |
|---|---|---|---|
| POST | *(inferred: `api/authenticate`)* | `AuthenticateEndpoint.HandleAsync` | None (public) |

`AuthenticateEndpoint.HandleAsync` returns: `Result`, `IsLockedOut`, `IsNotAllowed`, `RequiresTwoFactor`, `Username`, `Token`

---

### 📦 Chunk Inventory — Buyer, Identity & Auth Domain

- **Entities found this chunk:** Buyer, PaymentMethod
- **States found this chunk:** None
- **Roles found this chunk:** `ADMINISTRATORS` (confirmed seeded; already carried from Chunk 1)
- **Services / capabilities detected:**
  - `IdentityTokenClaimService` → `GetTokenAsync(string): Task<string>` — JWT Token Issuance
  - `AuthenticateEndpoint` → `HandleAsync(AuthenticateRequest, CancellationToken): Task<ActionResult<AuthenticateResponse>>` — API Authentication
- **Integrations detected:** ASP.NET Core Identity (`UserManager`, `SignInManager`, `RoleManager`), JWT (`JwtSecurityTokenHandler`, `HmacSha256`), `AppIdentityDbContext` (separate from `CatalogContext`)
- **Cross-domain dependencies flagged:** Buyer entity exists in ApplicationCore but is not confirmed as an EF-tracked entity in `CatalogContext` — 🔗 Cross-domain note: Buyer/PaymentMethod may use a separate identity DB context or may be unused in this sample version. Agent 2 to verify.
- **Newly flagged as SHARED ENTITY:** None
- **LOW CONFIDENCE items raised:**
  - ⚠️ LOW — `Buyer` entity not found in `CatalogContext` EF entity list; may be defined in `AppIdentityDbContext` or unused in current sample scope
  - ⚠️ LOW — `PaymentMethod` fields (CardId, Alias, Last4) suggest Stripe integration intent but no Stripe client/SDK reference found in extracted source; payment processing may be a stub

---

## 📥 Agent 1 — Chunk 4 of 6 — Infrastructure Domain

**Carried Forward from Prior Chunks:**
- Entities: CatalogItem 🔗 SHARED, CatalogBrand, CatalogType, Basket 🔗 SHARED, BasketItem, Order 🔗 SHARED, OrderItem, Address, CatalogItemOrdered, Buyer, PaymentMethod
- States: *(none domain-level)*
- Roles: `ADMINISTRATORS`

---

### EF Entities (CatalogContext)

Confirmed tracked in `src/Infrastructure/Data/CatalogContext.cs`:

| Entity | DbSet Property |
|---|---|
| CatalogBrand | `DbSet<CatalogBrand> CatalogBrands` |
| BasketItem | `DbSet<BasketItem>` |
| Basket | `DbSet<Basket>` |
| CatalogItem | `DbSet<CatalogItem> CatalogItems` |
| Order | `DbSet<Order>` |
| CatalogType | `DbSet<CatalogType> CatalogTypes` |
| OrderItem | `DbSet<OrderItem>` |

⚠️ ARCHITECTURE NOTE: `Buyer` and `PaymentMethod` entities are NOT in `CatalogContext`. They are either tracked in `AppIdentityDbContext` or unused/stubbed in this sample. Agent 2 to confirm.

---

### Repository

**EfRepository** — `src/Infrastructure/Data/EfRepository.cs`
- Implements `IRepository<T>` and `IReadRepository<T>` for all `IAggregateRoot` entities
- Generic EF Core-backed implementation (Ardalis.Specification pattern)

---

### Query Services

**BasketQueryService** — `src/Infrastructure/Data/Queries/BasketQueryService.cs`
- `CountTotalBasketItems(string username): Task<int>`
- Direct `_dbContext` query (bypasses repository) — sum of quantities across all basket items for a user

---

### Data Seeding

**CatalogContextSeed** — seeds CatalogBrands, CatalogTypes, CatalogItems on startup if empty; runs EF migrations automatically on SQL Server

**AppIdentityDbContextSeed** — seeds `Administrators` role, `demouser@microsoft.com`, `admin@microsoft.com`

---

### Services (Infrastructure)

**EmailSender** — `src/Infrastructure/Services/EmailSender.cs`
- `SendEmailAsync(string email, string subject, string message): Task`
- ⚠️ STUB: body is `return Task.CompletedTask` — no actual email sending logic wired

**LoggerAdapter** — `src/Infrastructure/Logging/LoggerAdapter.cs`
- `LogInformation(string message, params object[] args): void`
- `LogWarning(string message, params object[] args): void`
- Wraps ASP.NET Core `ILogger<T>` to implement `IAppLogger<T>`

---

### Config Keys

| Key | Value | Source |
|---|---|---|
| `CatalogSettings.CatalogBaseUrl` | *(from appsettings — value not in extraction)* | appsettings.json |
| `BaseUrlConfiguration.ApiBase` | *(from appsettings)* | appsettings.json |
| `BaseUrlConfiguration.WebBase` | *(from appsettings)* | appsettings.json |
| `parameters.sqlAdminPassword` | ***REDACTED*** | `infra/main.parameters.json` |

---

### 📦 Chunk Inventory — Infrastructure Domain

- **Entities found this chunk:** No new entities; confirmed EF mapping for CatalogBrand, BasketItem, Basket, CatalogItem, Order, CatalogType, OrderItem
- **States found this chunk:** None
- **Roles found this chunk:** None new
- **Services / capabilities detected:**
  - `EfRepository` — Generic Repository (all aggregate roots)
  - `BasketQueryService` → `CountTotalBasketItems(string): Task<int>` — Basket Item Count Query
  - `EmailSender` → `SendEmailAsync(string, string, string): Task` — Email Notification (STUB)
  - `LoggerAdapter` → `LogInformation(...)`, `LogWarning(...)` — Logging Abstraction
  - `IdentityTokenClaimService` → `GetTokenAsync(string): Task<string>` — JWT Issuance (confirmed here)
- **Integrations detected:** SQL Server (EF Core, `IsSqlServer()` check), ASP.NET Core Identity (`AppIdentityDbContext` separate DB), SendGrid/SMTP (TODO comment — not implemented)
- **Cross-domain dependencies flagged:** `BasketQueryService` accesses `_dbContext` directly — bypasses `IRepository` abstraction; 🔗 Architecture note for Agent 2
- **Newly flagged as SHARED ENTITY:** None
- **LOW CONFIDENCE items raised:**
  - ⚠️ LOW — `EmailSender` is a confirmed stub; no real email integration exists in this codebase version

---

## 📥 Agent 1 — Chunk 5 of 6 — BlazorAdmin + BlazorShared Domain

**Carried Forward from Prior Chunks:**
- Entities: CatalogItem 🔗 SHARED, CatalogBrand, CatalogType, Basket 🔗 SHARED, BasketItem, Order 🔗 SHARED, OrderItem, Address, CatalogItemOrdered, Buyer, PaymentMethod
- States: *(none domain-level)*
- Roles: `ADMINISTRATORS`

---

### Shared Models (BlazorShared — DTOs)

| Model | Key Fields | File |
|---|---|---|
| `CatalogItem` (DTO) | Id, CatalogTypeId, CatalogType (string), CatalogBrandId, CatalogBrand (string), Name, Description, Price, PictureUri, PictureBase64, PictureName | `src/BlazorShared/Models/CatalogItem.cs` |
| `CatalogBrand` (DTO) | Id, Name (via LookupData) | `src/BlazorShared/Models/CatalogBrand.cs` |
| `CatalogType` (DTO) | Id, Name (via LookupData) | `src/BlazorShared/Models/CatalogType.cs` |
| `LookupData` (abstract) | Id: int, Name: string | `src/BlazorShared/Models/LookupData.cs` |
| `CreateCatalogItemRequest` | CatalogTypeId, CatalogBrandId, Name, Description, Price, PictureUri, PictureBase64, PictureName | `src/BlazorShared/Models/CreateCatalogItemRequest.cs` |
| `PagedCatalogItemResponse` | CatalogItems: List\<CatalogItem\>, PageCount: int | `src/BlazorShared/Models/PagedCatalogItemResponse.cs` |
| `UserInfo` | IsAuthenticated, NameClaimType, RoleClaimType, Token, Claims | `src/BlazorShared/Authorization/UserInfo.cs` |
| `ErrorDetails` | StatusCode: int, Message: string | `src/BlazorShared/Models/ErrorDetails.cs` |

---

### State & Status (BlazorAdmin — UI Level)

**ToastLevel** — `src/BlazorAdmin/Services/ToastService.cs`

| Values (verbatim) |
|---|
| `Info`, `Success`, `Warning`, `Error` |

⚠️ NOTE: This is a UI notification severity enum, not a domain lifecycle state.

---

### BlazorAdmin Services

| Service | Method Signatures | Capability Label |
|---|---|---|
| `CatalogItemService` | `Create(CreateCatalogItemRequest): Task<CatalogItem>`, `Edit(CatalogItem): Task<CatalogItem>`, `Delete(int): Task<string>`, `GetById(int): Task<CatalogItem>`, `ListPaged(int): Task<List<CatalogItem>>`, `List(): Task<List<CatalogItem>>` | Catalog Item HTTP Client |
| `CachedCatalogItemServiceDecorator` | Same interface as above + `RefreshLocalStorageList()` | Cached Catalog Item Service (Local Storage) |
| `CatalogLookupDataService<T,R>` | `List(): Task<List<TLookupData>>` | Catalog Lookup (Brand/Type) HTTP Client |
| `CachedCatalogLookupDataServiceDecorator<T,R>` | `List(): Task<List<TLookupData>>` | Cached Catalog Lookup (Local Storage) |
| `HttpService` | `HttpGet<T>(string): Task<T>`, `HttpDelete<T>(string, int): Task<T>`, `HttpPost<T>(string, object): Task<T>`, `HttpPut<T>(string, object): Task<T>` | HTTP API Client Wrapper |
| `ToastService` | `ShowToast(string, ToastLevel): void` | UI Toast Notification |

---

### Authorization (BlazorShared)

| Constant | Value | File |
|---|---|---|
| `Constants.Roles.ADMINISTRATORS` | `"Administrators"` | `src/BlazorShared/Authorization/Constants.cs` |

`UserInfo` carries: `IsAuthenticated`, `Token`, `Claims (IEnumerable<ClaimValue>)`, `NameClaimType`, `RoleClaimType`

`CustomAuthStateProvider` (BlazorAdmin) — polls `/User` endpoint every 60 seconds to refresh authentication state; injects Bearer token into `HttpClient.DefaultRequestHeaders`

---

### Admin Page Components (CatalogItemPage)

| Component | Actions Exposed |
|---|---|
| `List.razor.cs` | `CreateClick()`, `EditClick(int)`, `DeleteClick(int)`, `DetailsClick(int)`, `ReloadCatalogItems()` |

---

### 📦 Chunk Inventory — BlazorAdmin + BlazorShared Domain

- **Entities found this chunk:** CatalogItem (DTO variant) 🔗 SHARED, CatalogBrand (DTO) 🔗 SHARED, CatalogType (DTO) 🔗 SHARED
- **States found this chunk:** `ToastLevel` { Info, Success, Warning, Error } — UI notification severity only
- **Roles found this chunk:** `ADMINISTRATORS` (confirmed in BlazorShared Constants — same value as ApplicationCore)
- **Services / capabilities detected:** (listed in table above)
- **Integrations detected:** `Blazored.LocalStorage` (local browser cache for catalog data, 1-minute TTL), `HttpClient` (calls PublicApi via `BaseUrlConfiguration.ApiBase`), `IJSRuntime` (cookie read/delete, routing, CSS body overflow)
- **Cross-domain dependencies flagged:** BlazorAdmin `CatalogItemService` calls `api/catalog-items`, `api/catalog-brands`, `api/catalog-types` — 🔗 Consumes PublicApi Catalog endpoints directly
- **Newly flagged as SHARED ENTITY:** None new
- **LOW CONFIDENCE items raised:**
  - ⚠️ LOW — `CatalogItem` (BlazorShared DTO) and `CatalogItem` (ApplicationCore entity) are distinct classes with the same name; Agent 2 to clearly distinguish these in documentation

---

## 📥 Agent 1 — Chunk 6 of 6 — Web (Customer-Facing) Domain

**Carried Forward from Prior Chunks:**
- Entities: CatalogItem 🔗 SHARED, CatalogBrand, CatalogType, Basket 🔗 SHARED, BasketItem, Order 🔗 SHARED, OrderItem, Address, CatalogItemOrdered, Buyer, PaymentMethod
- States: *(none domain-level)*
- Roles: `ADMINISTRATORS`

---

### Web Layer — Identity Pages (from extraction)

| Page | Handler Methods | Capability |
|---|---|---|
| `Login.cshtml.cs` | `OnGetAsync(returnUrl?)`, `OnPostAsync(returnUrl?)` | Cookie-based login; on success calls `TransferAnonymousBasketToUserAsync` |
| `Register.cshtml.cs` | `OnPostAsync(returnUrl?)` | Creates `ApplicationUser`, generates email confirmation token, sends confirmation email |
| `ConfirmEmail.cshtml.cs` | `OnGetAsync(userId, code)` | Confirms user email via token |

**Notable: `TransferAnonymousBasketToUserAsync`** (in `Login.cshtml.cs`):
- Reads `BASKET_COOKIENAME` cookie
- Calls `IBasketService.TransferBasketAsync(anonymousId, userName)`
- Deletes cookie after transfer
- 🔗 Cross-domain: Web Identity page directly calls BasketService

---

### SlugifyParameterTransformer

`src/Web/SlugifyParameterTransformer.cs` — transforms route parameter values to kebab-case (e.g., `CatalogItem` → `catalog-item`)

---

### Constants Referenced

| Constant | Source |
|---|---|
| `Constants.BASKET_COOKIENAME` | Web project constants (file not in extraction — path inferred from usage) |

⚠️ LOW — `Constants.BASKET_COOKIENAME` value not available in extraction data; used in Login page basket transfer logic

---

### 📦 Chunk Inventory — Web Domain

- **Entities found this chunk:** No new entities; Web layer uses ApplicationUser (ASP.NET Core Identity — string Id, UserName, Email)
- **States found this chunk:** None
- **Roles found this chunk:** None new
- **Services / capabilities detected:**
  - `Login` page → `OnGetAsync`, `OnPostAsync`, `TransferAnonymousBasketToUserAsync` — Customer Login + Basket Transfer
  - `Register` page → `OnPostAsync` — Customer Registration + Email Confirmation Flow
  - `ConfirmEmail` page → `OnGetAsync` — Email Confirmation
- **Integrations detected:** ASP.NET Core Identity (`_signInManager`, `_userManager`), `IBasketService` (basket transfer on login), `IEmailSender` (registration confirmation — stub)
- **Cross-domain dependencies flagged:** 🔗 Web Login page calls `IBasketService.TransferBasketAsync` — cross-domain dependency on Basket domain
- **Newly flagged as SHARED ENTITY:** None
- **LOW CONFIDENCE items raised:**
  - ⚠️ LOW — Web domain has limited coverage in extraction; catalog browse pages, basket pages, order history pages, and checkout page are referenced in specs but source not in extraction payload. Agent 2 should scan `src/Web/Pages/` and `src/Web/Controllers/` directly.

---

---

## 🔍 Agent 1 — Final Consolidated Output

---

### Project Scan Summary

- **Language(s):** C# / .NET 6+
- **Framework(s):** ASP.NET Core, Blazor WebAssembly, Entity Framework Core, ASP.NET Core Identity, JWT Bearer, Ardalis.Specification, Ardalis.GuardClauses, Blazored.LocalStorage
- **Architecture style:** Modular Monolith — Clean Architecture (Domain → Application → Infrastructure → Presentation layers; DDD aggregate pattern)
- **Total files scanned:** ~90 source files (from extraction payload)
- **Domains identified:** 6 — Catalog, Basket & Order, Buyer/Identity/Auth, Infrastructure, BlazorAdmin/BlazorShared, Web
- **Chunks processed:** 6

---

## OUTPUT 1 — Domain Architecture Map

| Domain | Sub-domains | Key Modules / Folders | Architecture Role | Notes |
|---|---|---|---|---|
| Catalog | — | `src/ApplicationCore/Entities/` (CatalogItem, CatalogBrand, CatalogType), `src/PublicApi/CatalogItemEndpoints/`, `src/PublicApi/CatalogBrandEndpoints/`, `src/PublicApi/CatalogTypeEndpoints/` | Core | Primary product data domain; full CRUD via REST API |
| Basket | — | `src/ApplicationCore/Entities/BasketAggregate/`, `src/ApplicationCore/Services/BasketService.cs`, `src/Infrastructure/Data/Queries/BasketQueryService.cs` | Core | Shopping basket aggregate; supports anonymous + authenticated users |
| Order | — | `src/ApplicationCore/Entities/OrderAggregate/`, `src/ApplicationCore/Services/OrderService.cs` | Core | Order creation from basket; immutable snapshot pattern (CatalogItemOrdered) |
| Buyer / Identity | BuyerAggregate, Auth | `src/ApplicationCore/Entities/BuyerAggregate/`, `src/Infrastructure/Identity/`, `src/PublicApi/AuthEndpoints/` | Core / Gateway | Identity management; JWT token issuance; role-based access |
| Infrastructure | Data, Logging, Email | `src/Infrastructure/Data/`, `src/Infrastructure/Logging/`, `src/Infrastructure/Services/` | Support | EF Core persistence; generic repository; logging adapter; email stub |
| BlazorAdmin | Admin UI, Shared | `src/BlazorAdmin/`, `src/BlazorShared/` | Gateway | Blazor WASM admin SPA; consumes PublicApi; local storage caching of catalog data |
| Web | Customer UI | `src/Web/` | Gateway | ASP.NET Core MVC/Razor Pages customer-facing app; login/register/order flows |

### Domain Relationships

- Catalog → Basket: BasketItem holds `CatalogItemId` (FK reference, not navigation)
- Catalog → Order: `OrderService` reads `IRepository<CatalogItem>` to build `CatalogItemOrdered` snapshot at order creation time
- Basket → Order: `OrderService` reads basket by ID to create order; basket is not deleted automatically by OrderService
- Web → Basket: Login page calls `IBasketService.TransferBasketAsync` (anonymous → authenticated basket transfer)
- Web → Identity: Uses ASP.NET Core Identity cookie auth (`SignInManager`)
- BlazorAdmin → PublicApi: HTTP calls to `api/catalog-items`, `api/catalog-brands`, `api/catalog-types`; JWT Bearer auth for mutations
- PublicApi → Identity: `AuthenticateEndpoint` calls `ITokenClaimsService.GetTokenAsync` for JWT issuance

---

## OUTPUT 2 — Entity Inventory

| Entity Name | Domain | Key Fields | Relationships | Source File(s) | Shared Across Domains? |
|---|---|---|---|---|---|
| CatalogItem | Catalog | Id: int, Name: string, Description: string, Price: decimal, PictureUri: string, CatalogTypeId: int, CatalogBrandId: int | CatalogType (FK), CatalogBrand (FK), BasketItem (1-many via CatalogItemId), CatalogItemOrdered (snapshot copy) | `src/ApplicationCore/Entities/CatalogItem.cs` | Yes — Catalog, Basket, Order, BlazorAdmin |
| CatalogBrand | Catalog | Id: int, Brand: string | CatalogItem (1-many) | `src/ApplicationCore/Entities/CatalogBrand.cs` | Yes — Catalog, BlazorAdmin |
| CatalogType | Catalog | Id: int, Type: string | CatalogItem (1-many) | `src/ApplicationCore/Entities/CatalogType.cs` | Yes — Catalog, BlazorAdmin |
| Basket | Basket | Id: int, BuyerId: string, Items: IReadOnlyCollection\<BasketItem\>, TotalItems: int (computed) | BasketItem (1-many, owned collection) | `src/ApplicationCore/Entities/BasketAggregate/Basket.cs` | Yes — Basket, Order, Web |
| BasketItem | Basket | Id: int, UnitPrice: decimal, Quantity: int, CatalogItemId: int, BasketId: int | Basket (FK), CatalogItem (FK — ID only) | `src/ApplicationCore/Entities/BasketAggregate/BasketItem.cs` | No |
| Order | Order | Id: int, BuyerId: string, OrderDate: DateTimeOffset, ShipToAddress: Address | OrderItem (1-many, owned collection) | `src/ApplicationCore/Entities/OrderAggregate/Order.cs` | Yes — Order, Web |
| OrderItem | Order | Id: int, ItemOrdered: CatalogItemOrdered, UnitPrice: decimal, Units: int | Order (FK), CatalogItemOrdered (embedded value object) | `src/ApplicationCore/Entities/OrderAggregate/OrderItem.cs` | No |
| Address | Order | Street: string, City: string, State: string, Country: string, ZipCode: string | Order (value object — embedded) | `src/ApplicationCore/Entities/OrderAggregate/Address.cs` | No |
| CatalogItemOrdered | Order | CatalogItemId: int, ProductName: string, PictureUri: string | OrderItem (value object — snapshot of CatalogItem at time of order) | `src/ApplicationCore/Entities/OrderAggregate/CatalogItemOrdered.cs` | No |
| Buyer | Buyer | Id: int, IdentityGuid: string, PaymentMethods: IEnumerable\<PaymentMethod\> | PaymentMethod (1-many) | `src/ApplicationCore/Entities/BuyerAggregate/Buyer.cs` | ⚠️ LOW — Not confirmed in CatalogContext EF mapping; may be unused in this sample |
| PaymentMethod | Buyer | Id: int, Alias: string?, CardId: string?, Last4: string? | Buyer (FK) | `src/ApplicationCore/Entities/BuyerAggregate/PaymentMethod.cs` | ⚠️ LOW — Same as Buyer above; PCI note in code |
| ApplicationUser | Identity | UserName: string, Email: string (ASP.NET Core Identity base fields) | Identity DB (separate context) | `src/Infrastructure/Identity/AppIdentityDbContextSeed.cs` | Yes — Identity, Web, PublicApi |
| BaseEntity | All | Id: int (virtual, protected set) | Base class for all entities | `src/ApplicationCore/Entities/BaseEntity.cs` | Yes — all domains |

---

## OUTPUT 3 — State & Status Registry

| Entity / Context | Field Name | States Found (verbatim) | Inferred Lifecycle Order | Source File |
|---|---|---|---|---|
| ToastService (UI) | ToastLevel (enum) | `Info`, `Success`, `Warning`, `Error` | ⚠️ ORDER UNCLEAR — these are notification severity levels, not a lifecycle sequence | `src/BlazorAdmin/Services/ToastService.cs` |
| Order | *(status field)* | *(none found in extraction)* | ⚠️ ORDER UNCLEAR — No `Status` or `OrderStatus` field found on `Order` entity; Agent 2 to verify from full source | `src/ApplicationCore/Entities/OrderAggregate/Order.cs` |
| AuthenticateResponse | result fields | `result.Succeeded`, `result.IsLockedOut`, `result.IsNotAllowed`, `result.RequiresTwoFactor` | ⚠️ ORDER UNCLEAR — these are discrete outcome states of a login attempt, not a sequential lifecycle | `src/PublicApi/AuthEndpoints/AuthenticateEndpoint.cs` |

---

## OUTPUT 4 — Role & Permission Snapshot

| Role Name | Permission Scopes / Annotations | Gated Actions (from route/method names only) | Source File |
|---|---|---|---|
| `ADMINISTRATORS` | `[Authorize(Roles = "Administrators", AuthenticationSchemes = JwtBearerDefaults.AuthenticationScheme)]` | `CreateCatalogItemEndpoint.HandleAsync`, `DeleteCatalogItemEndpoint.HandleAsync`, `UpdateCatalogItemEndpoint.HandleAsync` | `src/PublicApi/CatalogItemEndpoints/CreateCatalogItemEndpoint.cs`, `DeleteCatalogItemEndpoint.cs`, `UpdateCatalogItemEndpoint.cs` |
| *(Anonymous / unauthenticated)* | No auth required | `CatalogItemListPagedEndpoint`, `CatalogItemGetByIdEndpoint`, `CatalogBrandListEndpoint`, `CatalogTypeListEndpoint`, `AuthenticateEndpoint` | `src/PublicApi/` |
| *(Cookie-authenticated user)* | ASP.NET Core Identity cookie | Web login, register, order history (inferred) | `src/Web/Areas/Identity/Pages/Account/` |

---

## OUTPUT 5 — Capability & Service Skeleton

| Domain | Service / Class Name | Method Signatures | Rough Capability Label | Source File |
|---|---|---|---|---|
| Basket | `BasketService` | `AddItemToBasket(string, int, decimal, int): Task<Basket>`, `DeleteBasketAsync(int): Task`, `SetQuantities(int, Dictionary<string,int>): Task<Result<Basket>>`, `TransferBasketAsync(string, string): Task` | Basket Management | `src/ApplicationCore/Services/BasketService.cs` |
| Order | `OrderService` | `CreateOrderAsync(int, Address): Task` | Order Creation | `src/ApplicationCore/Services/OrderService.cs` |
| Catalog | `UriComposer` | `ComposePicUri(string): string` | Catalog Picture URI Composition | `src/ApplicationCore/Services/UriComposer.cs` |
| Basket | `BasketQueryService` | `CountTotalBasketItems(string): Task<int>` | Basket Item Count Query | `src/Infrastructure/Data/Queries/BasketQueryService.cs` |
| Identity | `IdentityTokenClaimService` | `GetTokenAsync(string): Task<string>` | JWT Token Issuance | `src/Infrastructure/Identity/IdentityTokenClaimService.cs` |
| Infrastructure | `EfRepository` | (generic: AddAsync, UpdateAsync, DeleteAsync, GetByIdAsync, ListAsync, FirstOrDefaultAsync, CountAsync) | Generic EF Repository | `src/Infrastructure/Data/EfRepository.cs` |
| Infrastructure | `EmailSender` | `SendEmailAsync(string, string, string): Task` | Email Notification (STUB) | `src/Infrastructure/Services/EmailSender.cs` |
| Infrastructure | `LoggerAdapter` | `LogInformation(string, object[]): void`, `LogWarning(string, object[]): void` | Logging Abstraction | `src/Infrastructure/Logging/LoggerAdapter.cs` |
| BlazorAdmin | `CatalogItemService` | `Create(CreateCatalogItemRequest): Task<CatalogItem>`, `Edit(CatalogItem): Task<CatalogItem>`, `Delete(int): Task<string>`, `GetById(int): Task<CatalogItem>`, `ListPaged(int): Task<List<CatalogItem>>`, `List(): Task<List<CatalogItem>>` | Catalog Item HTTP Client (Admin) | `src/BlazorAdmin/Services/CatalogItemService.cs` |
| BlazorAdmin | `CachedCatalogItemServiceDecorator` | Same as `CatalogItemService` + cache invalidation | Cached Catalog Item Service | `src/BlazorAdmin/Services/CachedCatalogItemServiceDecorator.cs` |
| BlazorAdmin | `CatalogLookupDataService<T,R>` | `List(): Task<List<TLookupData>>` | Catalog Lookup (Brand/Type) HTTP Client | `src/BlazorAdmin/Services/CatalogLookupDataService.cs` |
| BlazorAdmin | `HttpService` | `HttpGet<T>(string): Task<T>`, `HttpDelete<T>(string, int): Task<T>`, `HttpPost<T>(string, object): Task<T>`, `HttpPut<T>(string, object): Task<T>` | HTTP API Client Wrapper | `src/BlazorAdmin/Services/HttpService.cs` |
| PublicApi | `AuthenticateEndpoint` | `HandleAsync(AuthenticateRequest, CancellationToken): Task<ActionResult<AuthenticateResponse>>` | API Authentication | `src/PublicApi/AuthEndpoints/AuthenticateEndpoint.cs` |
| PublicApi | `ExceptionMiddleware` | `InvokeAsync(HttpContext): Task` | API Exception Handling | `src/PublicApi/Middleware/ExceptionMiddleware.cs` |

---

## OUTPUT 6 — Integration & Dependency Map

| Integration Name | Type | Connected Domain(s) | Direction | Config Key / Env Var | Source File |
|---|---|---|---|---|---|
| SQL Server (EF Core) | Internal DB | Catalog, Basket, Order | Both | `ConnectionStrings` (inferred — not in extraction) | `src/Infrastructure/Data/CatalogContext.cs` |
| ASP.NET Core Identity DB | Internal DB | Identity, Web | Both | `ConnectionStrings` (separate from CatalogContext) | `src/Infrastructure/Identity/AppIdentityDbContextSeed.cs` |
| JWT Bearer | Auth Scheme | PublicApi, Identity | Outbound (issued) / Inbound (validated) | `AuthorizationConstants.JWT_SECRET_KEY` (⚠️ hardcoded) | `src/Infrastructure/Identity/IdentityTokenClaimService.cs` |
| SendGrid / SMTP | External API | Web, Identity | Outbound | *(none — stub only; no config key wired)* | `src/Infrastructure/Services/EmailSender.cs` |
| Blazored.LocalStorage | Browser Cache | BlazorAdmin | Both | *(browser API)* | `src/BlazorAdmin/Services/CachedCatalogItemServiceDecorator.cs` |
| PublicApi REST | Internal API | BlazorAdmin → PublicApi | Outbound | `BaseUrlConfiguration.ApiBase` | `src/BlazorAdmin/Services/HttpService.cs` |
| ASP.NET Core Identity Cookie | Auth Scheme | Web | Both | *(framework managed)* | `src/Web/Areas/Identity/Pages/Account/Login.cshtml.cs` |
| Azure Infrastructure | Cloud Platform | All (deployment) | *(infrastructure only)* | `infra/main.parameters.json` | `infra/abbreviations.json` |
| CatalogBaseUrl | Config | Catalog, BlazorAdmin | Outbound (URI template substitution) | `CatalogSettings.CatalogBaseUrl` | `src/ApplicationCore/CatalogSettings.cs` |

---

## ⚠️ Validation Queue

| # | Item | Chunk | Reason |
|---|---|---|---|
| 1 | `Order` has no `Status` / `OrderStatus` field | Chunk 2 | No lifecycle state enum found on Order entity in extraction; order state machine may be absent in this sample or outside extraction scope |
| 2 | `Buyer` and `PaymentMethod` not in `CatalogContext` EF entity list | Chunks 3, 4 | These entities may be in `AppIdentityDbContext` or effectively unused stubs in this sample version |
| 3 | `PaymentMethod.CardId` — PCI compliance note in code | Chunk 3 | Code comment explicitly flags PCI scope; actual payment processing not implemented; Stripe integration is a stub intent |
| 4 | `AuthorizationConstants` — three hardcoded security values with explicit production-unsafe TODO comments | Chunk 3 | `AUTH_KEY`, `DEFAULT_PASSWORD`, `JWT_SECRET_KEY` are demo/sample values; critical security risk if deployed |
| 5 | `EmailSender.SendEmailAsync` — confirmed stub | Chunks 4, 6 | Body is `return Task.CompletedTask`; no real email sending; registration confirmation email is a no-op |
| 6 | `CatalogItem` name collision — ApplicationCore entity vs BlazorShared DTO | Chunk 5 | Two distinct classes named `CatalogItem` in different namespaces; Agent 2 to clearly distinguish in documentation |
| 7 | Web domain has limited extraction coverage | Chunk 6 | Catalog browse, basket, checkout, and order history Razor pages not present in extraction payload; Agent 2 should read `src/Web/Pages/` and `src/Web/Controllers/` directly |
| 8 | `Constants.BASKET_COOKIENAME` value not in extraction | Chunk 6 | Used in Login page basket transfer; constant definition file not in extraction payload |
| 9 | `BasketQueryService` bypasses `IRepository` abstraction | Chunk 4 | Uses `_dbContext` directly for COUNT query; architecture inconsistency vs repository pattern used elsewhere |
| 10 | `CatalogItemListPagedEndpoint` has `await Task.Delay(1000)` | Chunk 1 | Artificial 1-second delay in paged catalog endpoint — likely a demo artefact; Agent 2 to flag |

---

## 🤝 Handoff Note to Agent 2

This is a clean-architecture .NET e-commerce reference application (Microsoft eShopOnWeb) structured as a modular monolith with three frontends (Web MVC, Blazor Admin SPA, PublicApi) all sharing a single domain core. The **Catalog domain** is the most complete and best-evidenced in the extraction — CatalogItem, CatalogBrand, and CatalogType have full CRUD API coverage with role-gated mutations (`ADMINISTRATORS` only for writes).

The **Basket and Order domains** are the functional core of the purchase flow, but the extraction reveals a notable gap: `Order` has no `Status` field, which means either order lifecycle states are not implemented in this sample version or they exist in files not captured by the extractor — this should be your first verification target. The `Buyer` aggregate also appears partially implemented; it exists in the domain layer but is absent from the EF context.

Three **hardcoded security constants** in `AuthorizationConstants.cs` carry explicit TODO/production-unsafe warnings and must be flagged prominently in any security-facing output. The `EmailSender` is a confirmed stub and `PaymentMethod` carries a PCI compliance note without any real payment processor wired. The Web domain has the weakest coverage in this extraction — the customer-facing Razor pages for catalog browsing, basket management, checkout, and order history are referenced through specifications but not present in the source file payload; direct file reads of `src/Web/Pages/` are strongly recommended before finalising Web domain analysis.

---

✅ **Agent 1 Scan Complete.**
Agent 2 may now begin deep analysis using the 6 output files above.
**Recommended starting point: Basket & Order Domain** — reason: most complex state machine gap (Order with no visible status field), highest cross-domain dependency density, and core checkout business logic that Agent 2 must resolve from direct source reads before value stream mapping can proceed.
