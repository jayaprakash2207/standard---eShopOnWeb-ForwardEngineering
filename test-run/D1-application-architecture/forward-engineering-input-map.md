# Forward Engineering Input Map — eShopOnWeb

This document translates reverse-engineering findings into structured inputs for forward engineering agents. Each section maps a discovered system aspect to the forward-engineering decision it informs.

---

## Section 1 — Domain Model Inputs

### 1.1 Confirmed Aggregate Roots (carry forward as-is)

| Aggregate | Source File | Key Behavior | Value Objects | Status |
|---|---|---|---|---|
| Basket | src/ApplicationCore/Entities/BasketAggregate/Basket.cs | AddItem, RemoveEmptyItems, SetNewBuyerId | (none explicit) | Keep — strong model |
| Order | src/ApplicationCore/Entities/OrderAggregate/Order.cs | Total(), private _orderItems | Address, CatalogItemOrdered | Keep — DDD-complete |
| CatalogItem | src/ApplicationCore/Entities/CatalogItem.cs | UpdateDetails, UpdateBrand, UpdateType | (none) | Keep |
| CatalogBrand | src/ApplicationCore/Entities | (data entity) | (none) | Keep |
| CatalogType | src/ApplicationCore/Entities | (data entity) | (none) | Keep |
| Buyer | src/ApplicationCore/Entities/BuyerAggregate/Buyer.cs | (none wired) | PaymentMethod | Requires human decision — see open-questions.md |

### 1.2 Value Objects to Preserve

| Value Object | Source | Purpose |
|---|---|---|
| Address | src/ApplicationCore/Entities/OrderAggregate/Address.cs | Shipping address on Order — immutable value |
| CatalogItemOrdered | src/ApplicationCore/Entities/OrderAggregate/CatalogItemOrdered.cs | Snapshot of catalog item at order time — preserves price/name |

**Forward engineering note:** CatalogItemOrdered is a critical pattern — it prevents retroactive price changes from corrupting order history. Preserve in new Order service.

### 1.3 Domain Validations (via Ardalis.GuardClauses)

CatalogItem uses Guard.Against for property validation:
- `Guard.Against.Null(name)`, `Guard.Against.NullOrEmpty(description)`, `Guard.Against.OutOfRange(price)`
- Evidence: `src/ApplicationCore/Entities/CatalogItem.cs`

Forward engineering input: all new domain entities should use Guard.Against (or equivalent) for invariant enforcement at the domain boundary.

---

## Section 2 — Interface / API Contract Inputs

### 2.1 Confirmed PublicApi Endpoints (with evidence)

| Endpoint | Method | Source | Auth Required | DTO |
|---|---|---|---|---|
| /api/authenticate | POST | src/PublicApi/AuthEndpoints/AuthenticateEndpoint.cs | No | AuthenticateRequest → AuthenticateResponse (JWT) |
| /api/catalog-brands | GET | src/PublicApi/CatalogBrandEndpoints/CatalogBrandListEndpoint.cs | Unknown | CatalogBrandListResponse |
| /api/catalog-items | GET | Inferred from BlazorAdmin CatalogItemService | Unknown | CatalogListResponse (paginated) |
| /api/catalog-items/{id} | PUT | Inferred from BlazorAdmin CatalogItemService | Unknown | (unknown) |
| /api/catalog-items | POST | Inferred from BlazorAdmin CatalogItemService | Unknown | CreateCatalogItemRequest |
| /api/catalog-items/{id} | DELETE | Inferred from BlazorAdmin CatalogItemService | Unknown | (none) |
| /api/catalog-types | GET | Inferred from BlazorAdmin CatalogItemService | Unknown | CatalogTypeListResponse |
| /User | GET | Inferred from CustomAuthStateProvider | JWT | UserInfo response |

### 2.2 Forward Engineering API Design Recommendations

1. **Eliminate client-side joins** — `/api/catalog-items` response should embed brand and type names in the response DTO, not require client to join separately.
2. **Add pagination contract** — catalog-items endpoint appears to be paginated (based on CatalogItemService page number parameter). Standardize pagination shape: `{ items: [], pageIndex, pageSize, totalCount }`.
3. **Standardize authentication** — all admin endpoints should require JWT Bearer in Authorization header. Currently not all endpoints have explicit auth documented.
4. **Version the API** — as services are extracted, `/api/v1/` prefix avoids client breakage during migration.

---

## Section 3 — Data Model Inputs

### 3.1 CatalogContext Entities (ALL in single context — must split)

| Entity | Target Context (after split) | Key Fields |
|---|---|---|
| CatalogItem | CatalogContext | Id, Name, Description, Price, PictureUri, CatalogTypeId, CatalogBrandId |
| CatalogBrand | CatalogContext | Id, Brand |
| CatalogType | CatalogContext | Id, Type |
| Basket | BasketContext | Id, BuyerId, Items (BasketItem) |
| BasketItem | BasketContext (owned by Basket) | Id, UnitPrice, Quantity, CatalogItemId |
| Order | OrderContext | Id, BuyerId, ShipToAddress, OrderDate, OrderItems |
| OrderItem | OrderContext (owned by Order) | ItemOrdered (CatalogItemOrdered snapshot), UnitPrice, Units |

### 3.2 Identity Entities (AppIdentityDbContext — already separate, no split needed)

- ApplicationUser (extends IdentityUser) — IdentityConnection database
- Standard ASP.NET Identity tables (AspNetUsers, AspNetRoles, AspNetUserRoles, etc.)

### 3.3 Context Split Design

```
Before (current):
  CatalogConnection database:
    Baskets, BasketItems
    Catalog (items), CatalogBrands, CatalogTypes
    Orders, OrderItems

After (recommended):
  CatalogConnection database:
    Catalog, CatalogBrands, CatalogTypes

  BasketConnection database (new):
    Baskets, BasketItems

  OrderConnection database (new):
    Orders, OrderItems
    (CatalogItemOrdered snapshot — no FK to Catalog, by design)

  IdentityConnection database (unchanged):
    ASP.NET Identity tables
```

### 3.4 CatalogItemId Cross-Context Reference

BasketItem.CatalogItemId and CatalogItemOrdered are soft references to Catalog. There is no DB-level foreign key enforcement across bounded contexts. This is correct — maintain as soft references with periodic validation.

---

## Section 4 — Infrastructure Pattern Inputs

### 4.1 Repository Pattern

- Generic `EfRepository<T>` extends `Ardalis.Specification.RepositoryBase<T>`
- Per-module extraction: each new service gets its own `EfRepository<T>` backed by that module's DbContext
- Specification pattern should be preserved — `Ardalis.Specification` is portable and eliminates leaky query logic

### 4.2 Caching Pattern

- Server-side: `CachedCatalogItemServiceDecorator` and `CachedCatalogLookupDataServiceDecorator` in BlazorAdmin (client-side LocalStorage, 1-min TTL)
- Evidence: `src/BlazorAdmin/Services/CachedCatalogItemServiceDecorator.cs`
- Forward engineering note: server-side Redis or memory cache should replace client-side LocalStorage caching in a production-grade catalog service. Client-side TTL cache is appropriate only for static lookup data (brands, types).

### 4.3 Dependency Injection Registration Pattern

- Infrastructure registered via `Dependencies.AddInfrastructureServices(config)` static method
- `USE_ONLY_IN_MEMORY_DATABASE` environment variable triggers InMemory switch for testing
- Evidence: `src/Infrastructure/Dependencies.cs`
- Forward engineering note: preserve this env-var toggle for test environments. New services should support `IN_MEMORY_MODE=true` for integration testing without SQL Server.

### 4.4 Configuration Inputs

| Config Key | Source | Forward Engineering Action |
|---|---|---|
| CatalogConnection | appsettings.json | Split into per-module connection strings |
| IdentityConnection | appsettings.json | Keep as-is for auth service |
| CatalogBaseUrl | appsettings.json | Move to catalog service config |
| BaseApiUrl (Blazor) | src/BlazorAdmin | Move to admin app config; point to new catalog service URL |

---

## Section 5 — Security Inputs

### 5.1 JWT Authentication

- Algorithm: HMAC SHA256
- Secret: HARDCODED in `AuthorizationConstants.JWT_SECRET_KEY` — **MUST be rotated**
- Claims: username + roles (from Identity)
- Token usage: Set as `HttpClient.DefaultRequestHeaders.Authorization` in BlazorAdmin
- Evidence: `src/Infrastructure/Identity/IdentityTokenClaimService.cs`, `src/BlazorAdmin/CustomAuthStateProvider.cs`

**Forward engineering input:**
1. JWT secret must be stored in Azure Key Vault / environment variable
2. Token must include expiry claim — current code sets expiry but must be verified in forward-engineered service
3. Blazor client must NOT mutate `DefaultRequestHeaders` on a shared `HttpClient` — use `HttpRequestMessage` with per-request auth headers

### 5.2 Authorization

- `Roles.ADMINISTRATORS` constant used for admin-only endpoints
- Standard ASP.NET Identity role-based auth
- Evidence: `src/ApplicationCore/Constants/AuthorizationConstants.cs`

**Forward engineering input:** Preserve role-based authorization model. In microservices, roles should be embedded in JWT claims — services should not call identity DB to validate roles.

### 5.3 Known Security Gaps (must address before production)

| Gap | Severity | Action Required |
|---|---|---|
| Hardcoded JWT_SECRET_KEY | Critical | Rotate; move to Key Vault |
| Hardcoded DEFAULT_PASSWORD | Critical | Remove from source; use seeding from env |
| EmailSender not implemented | Medium | Implement before enabling account confirmation |
| HttpService null return on GET errors | Medium | Add error observability before production |
| CustomAuthStateProvider shares HttpClient headers | Medium | Use per-request auth headers |

---

## Section 6 — Deployment Inputs

### 6.1 Current Topology

| Service | Deployment | Evidence |
|---|---|---|
| Web (MVC) | Azure App Service | azure.yaml: services.web |
| PublicApi | Docker container | docker-compose.yml: eshoppublicapi |
| BlazorAdmin | Hosted in Web or standalone (unknown) | ServicesConfiguration.cs registers services |
| SQL Server | Docker (azure-sql-edge) | docker-compose.yml: sqlserver |

### 6.2 Forward Engineering Deployment Design

```
Recommended target (per strangler sequence):
  auth-service        → Azure Container App (stateless, JWT issuer)
  catalog-read-service → Azure Container App (read-only, cacheable)
  catalog-admin-service → Azure Container App (admin, JWT-protected)
  basket-service       → Azure Container App (session-scoped writes)
  order-service        → Azure Container App (transactional writes, saga)
  blazor-admin (SPA)   → Azure Static Web Apps (decoupled from backend)
  API Gateway          → Azure API Management (route /api/* to services)
```

### 6.3 InMemory Database Toggle

`USE_ONLY_IN_MEMORY_DATABASE` environment variable in `src/Infrastructure/Dependencies.cs` enables EF InMemory mode for testing. All forward-engineered services should preserve an equivalent test-mode flag.

---

## Section 7 — Missing Information (Requires Extraction)

The following areas have insufficient evidence for forward engineering input and require human review or additional extraction:

| Area | Gap | Impact |
|---|---|---|
| Web project controllers | Not in Layer 1 extraction | Cannot design Basket or Order API contracts |
| Checkout flow entry point | Unknown endpoint | Cannot design checkout saga |
| Basket cleanup after order | Whether Web controller calls DeleteBasketAsync | Risk of orphan baskets in new order service |
| /User endpoint | Which project serves it | Cannot design user profile service |
| BlazorAdmin hosting | Embedded in Web or standalone | Affects static web app vs. hosted WASM deployment |
| Buyer aggregate intent | Dead code or planned module | Cannot scope payment service design |
| Test project coverage | Not extracted | Cannot assess migration safety |
