# Canonical Enterprise Model — eShopOnWeb

> Every row traces to the Enterprise Knowledge Graph. Confidence: HIGH=direct code evidence | MEDIUM=inferred | LOW=assumed | ASSUMED=no evidence.

---

## LAYER 1 — BUSINESS

### Business Capabilities

| ID | Name | Description | Confidence |
|----|------|-------------|------------|
| CAP-001 | Product Catalog Management | Full CRUD on catalog items, brands, and types. Mutations restricted to Administrators role via JWT. | HIGH |
| CAP-002 | Shopping Basket Management | Add, update, remove, and transfer basket items for both anonymous and authenticated users. | HIGH |
| CAP-003 | Order Placement & History | Checkout creates immutable order with price-frozen line items and product snapshots. | HIGH |
| CAP-004 | Customer Identity & Authentication | ASP.NET Core Identity + JWT token issuance for API clients; cookie-based sessions for web. | HIGH |
| CAP-005 | Admin Catalog Portal | Blazor WASM SPA for administrators to manage the product catalog with local storage caching. | HIGH |
| CAP-006 | Customer Storefront Browsing | Customer-facing product browse, filter, basket, checkout, and order history pages. | ASSUMED |
| CAP-007 | Customer Account Registration | Self-service registration with email confirmation flow (email delivery currently broken). | HIGH |
| CAP-008 | Anonymous Basket & Session Transfer | Browser-cookie-tracked anonymous basket that merges into authenticated basket on login. | HIGH |

### Business Processes

| ID | Name | Domain | Trigger | Terminal Outcomes | Confidence |
|----|------|--------|---------|-------------------|------------|
| PROC-001 | Browse and Filter Products | Catalog | Visitor accesses storefront | Products listed with brand/type filtering | ASSUMED |
| PROC-002 | Add Item to Basket | Basket | Customer selects product | Basket created or updated; duplicate items merged by quantity | HIGH |
| PROC-003 | Update Basket Quantities | Basket | Customer edits basket | Basket updated; zero-quantity items removed (BR-16) | HIGH |
| PROC-004 | Transfer Anonymous Basket on Login | Basket→Web | Successful login with cookie | Anonymous items merged into account basket; cookie deleted | HIGH |
| PROC-005 | Place Order at Checkout | Basket→Order | Customer submits checkout form | Order saved with frozen prices and product snapshots | HIGH |
| PROC-006 | API Authentication and Token Issuance | Identity | API credential submission | JWT token (7 days) issued OR lockout/not-allowed/2FA response | HIGH |
| PROC-007 | Customer Registration with Email Confirmation | Web→Identity | Visitor submits registration | Account created; confirmation email NOT delivered (stub) | HIGH |
| PROC-008 | Catalog Administration | BlazorAdmin→PublicApi | Admin acts on product | Product created/updated/deleted; admin cache refreshed | HIGH |
| PROC-009 | Database Initialization on Startup | Infrastructure | Application starts | Migrations applied; reference data seeded; default accounts created | HIGH |

### Business Rules (Critical)

| ID | Rule | Severity | Confidence |
|----|------|----------|------------|
| BR-07 | Only Administrators may create, update, or delete catalog items | High | HIGH |
| BR-17 | Anonymous basket items merge into authenticated basket on login | High | HIGH |
| BR-20 | Order cannot be placed if basket is empty | High | HIGH |
| BR-21 | Product name and image are snapshot-immutable in orders | High | HIGH |
| BR-22 | Price frozen at basket-add time; not recalculated at checkout | High | HIGH |
| BR-26 | Basket is NOT auto-cleared after order placement | Medium | HIGH |
| BR-33 | **CRITICAL**: Three hardcoded credentials in source (JWT key, auth key, default password) | Critical | HIGH |
| BR-34 | Email confirmation permanently broken — EmailSender is a no-op stub | High | HIGH |

### Roles

| ID | Role | Actions Permitted | Auth Mechanism |
|----|------|-------------------|----------------|
| ROLE-001 | Catalog Administrator (Administrators) | Create/Update/Delete catalog items; all catalog reads | JWT Bearer + Role claim |
| ROLE-002 | Registered Customer | Basket management; checkout; order history; own profile | ASP.NET Identity cookie |
| ROLE-003 | Anonymous Visitor | Browse catalog; maintain anonymous basket | None (cookie session) |

---

## LAYER 2 — DATA

### Aggregates and Entities

| ID | Name | Type | Domain | Key Fields | Persistence | Confidence |
|----|------|------|--------|------------|-------------|------------|
| ENT-001 | CatalogItem | AggregateRoot | Catalog | Id(int/HiLo), Name, Description, Price(decimal), PictureUri, CatalogTypeId, CatalogBrandId | CatalogDB.CatalogItems | HIGH |
| ENT-002 | CatalogBrand | AggregateRoot | Catalog | Id(int), Brand(string) | CatalogDB.CatalogBrands | HIGH |
| ENT-003 | CatalogType | AggregateRoot | Catalog | Id(int), Type(string) | CatalogDB.CatalogTypes | HIGH |
| ENT-004 | Basket | AggregateRoot | Basket | Id(int), BuyerId(string/email), Items(collection), TotalItems(computed) | CatalogDB.Baskets | HIGH |
| ENT-005 | BasketItem | Entity | Basket | Id(int), UnitPrice(decimal), Quantity(int), CatalogItemId(int FK), BasketId(int FK) | CatalogDB.BasketItems | HIGH |
| ENT-006 | Order | AggregateRoot | Order | Id(int), BuyerId(string), OrderDate(DateTimeOffset), ShipToAddress(Address VO), OrderItems(collection) | CatalogDB.Orders | HIGH |
| ENT-007 | OrderItem | Entity | Order | Id(int), ItemOrdered(CatalogItemOrdered VO), UnitPrice(decimal), Units(int) | CatalogDB.OrderItems | HIGH |
| ENT-008 | Address | ValueObject | Order | Street, City, State, Country, ZipCode (all string, EF owned) | Embedded in Orders table | HIGH |
| ENT-009 | CatalogItemOrdered | ValueObject | Order | CatalogItemId(int), ProductName(string), PictureUri(string) — immutable snapshot | Embedded in OrderItems table | HIGH |
| ENT-010 | Buyer | AggregateRoot | Buyer | Id(int), IdentityGuid(string), PaymentMethods(collection) | **NOT PERSISTED — DEAD CODE** | LOW |
| ENT-011 | PaymentMethod | Entity | Buyer | Id(int), Alias(string?), CardId(string?/PCI token), Last4(string?) | **NOT PERSISTED — DEAD CODE** | LOW |
| ENT-012 | ApplicationUser | ExternalEntity | Identity | Id(string/GUID), UserName, Email, PasswordHash, etc. | IdentityDB (ASP.NET Identity tables) | HIGH |

### Databases

| ID | Name | Engine | Tables | Connection | Confidence |
|----|------|--------|--------|------------|------------|
| DB-001 | CatalogDB | SQL Server / Azure SQL | CatalogBrands, CatalogTypes, CatalogItems, Baskets, BasketItems, Orders, OrderItems | ConnectionStrings.CatalogConnection | HIGH |
| DB-002 | IdentityDB | SQL Server / Azure SQL | AspNetUsers, AspNetRoles, AspNetUserRoles, + 4 standard Identity tables | ConnectionStrings.IdentityConnection | HIGH |

### EF Migrations

| Migration | Date | Change |
|-----------|------|--------|
| InitialModel | 2020-12 | All catalog, basket, order tables |
| FixBuyerId | 2021-10 | Buyer identity field adjustment |
| FixShipToAddress | 2021-12 | Address owned entity column updates |
| InitialIdentityModel | 2020-12 | All Identity tables |

### Specifications (Query Objects)

| Class | Domain | Purpose |
|-------|--------|---------|
| CatalogFilterSpecification | Catalog | Filter by brandId + typeId |
| CatalogFilterPaginatedSpecification | Catalog | Filter + paginate (skip/take) |
| CatalogItemNameSpecification | Catalog | Filter by exact name |
| CatalogItemsSpecification | Catalog | Filter by array of IDs |
| BasketWithItemsSpecification | Basket | Basket by ID or BuyerId with Items |
| CustomerOrdersSpecification | Order | Orders by BuyerId with OrderItems |
| CustomerOrdersWithItemsSpecification | Order | Orders by BuyerId, Items + ItemOrdered |
| OrderWithItemsByIdSpec | Order | Order by Id with Items + ItemOrdered |

---

## LAYER 3 — APPLICATION

### Domain Services

| ID | Name | Key Methods | Confidence |
|----|------|-------------|------------|
| SVC-001 | BasketService | AddItemToBasket, DeleteBasketAsync, SetQuantities, TransferBasketAsync | HIGH |
| SVC-002 | OrderService | CreateOrderAsync(basketId, address) — cross-reads Basket+CatalogItem | HIGH |
| SVC-003 | UriComposer | ComposePicUri(template) using CatalogSettings.CatalogBaseUrl | HIGH |
| SVC-004 | IdentityTokenClaimService | GetTokenAsync(userName) — HMAC-SHA256 JWT, 7-day expiry | HIGH |
| SVC-005 | EfRepository\<T\> | AddAsync, UpdateAsync, DeleteAsync, GetByIdAsync, ListAsync, CountAsync | HIGH |
| SVC-006 | BasketQueryService | CountTotalBasketItems(username) — direct EF LINQ, bypasses IRepository | HIGH |
| SVC-007 | EmailSender (**STUB**) | SendEmailAsync — returns Task.CompletedTask; no email sent | HIGH |
| SVC-008 | LoggerAdapter\<T\> | LogInformation, LogWarning — wraps ILogger\<T\> | HIGH |
| SVC-009 | CachedCatalogViewModelService | GetCatalogItems (cached 30s IMemoryCache); decorator over CatalogViewModelService | HIGH |
| SVC-010 | GetMyOrdersHandler | IRequestHandler\<GetMyOrders, IEnumerable\<OrderViewModel\>\> — MediatR read query | HIGH |
| SVC-011 | CatalogItemService (BlazorAdmin) | Create/Edit/Delete/GetById/ListPaged/List — HTTP client to PublicApi | HIGH |
| SVC-012 | CachedCatalogItemServiceDecorator | Same as SVC-011 + Blazored.LocalStorage cache, 1-min TTL, immediate mutation invalidation | HIGH |

### API Endpoints

| ID | Method | Route | Auth | Description | Confidence |
|----|--------|-------|------|-------------|------------|
| API-001 | GET | /api/catalog-items | None | Paged catalog with brand/type filter + **1s artificial delay** | HIGH |
| API-002 | GET | /api/catalog-items/{id} | None | Single catalog item by ID | HIGH |
| API-003 | POST | /api/catalog-items | JWT: Administrators | Create catalog item | HIGH |
| API-004 | PUT | /api/catalog-items | JWT: Administrators | Update catalog item | HIGH |
| API-005 | DELETE | /api/catalog-items/{id} | JWT: Administrators | Delete catalog item | HIGH |
| API-006 | GET | /api/catalog-brands | None | List all brands | HIGH |
| API-007 | GET | /api/catalog-types | None | List all types | HIGH |
| API-008 | POST | /api/authenticate | None | Issue JWT token; lockout on failure | HIGH |

### Architecture Patterns Applied

| ID | Pattern | Scope | Configuration |
|----|---------|-------|---------------|
| AP-001 | Clean Architecture (DDD-Lite) | Entire solution | ApplicationCore ← Infrastructure ← Presentation |
| AP-002 | Generic Repository (Ardalis) | All aggregates | EfRepository\<T\> : RepositoryBase\<T\> |
| AP-003 | Mediator (MediatR) | Web read side only | GetMyOrdersHandler, GetOrderDetailsHandler — writes bypass |
| AP-004 | DDD Aggregate Root | Basket, Order, Buyer | Private collections, mutation via aggregate methods |
| AP-005 | EF Owned Entity (Value Object) | Address, CatalogItemOrdered | OwnsOne with column constraints |
| AP-006 | Guard Clause (Ardalis) | Domain constructors + services | Guard.Against.Null/NullOrEmpty/OutOfRange + custom EmptyBasketOnCheckout |
| AP-007 | Cache-Aside Decorator (Server) | Catalog read — Web | IMemoryCache, 30s sliding, 3 cache keys |
| AP-008 | Cache-Aside Decorator (Client) | Catalog read — BlazorAdmin | Blazored.LocalStorage, 60s TTL, mutation invalidation |
| AP-009 | Cookie Auth + Token Revocation | Web sessions | HttpOnly, SecurePolicy=Always, 60min, IMemoryCache revocation |
| AP-010 | JWT Bearer + RBAC | PublicApi mutations | HMAC-SHA256, 7 days, Administrators role only on writes |
| AP-011 | Custom Blazor Auth State Provider | BlazorAdmin | Polls /User every 60s; relays JWT from Web |
| AP-012 | SQL Retry on Failure | Web production only | EnableRetryOnFailure() on both contexts — NOT in PublicApi |
| AP-013 | HiLo Key Generation | CatalogItem only | catalog_hilo sequence |
| AP-014 | Exception Middleware | PublicApi | DuplicateException → 409; all others → 500 with message leak |
| AP-015 | Content-Based Health Checks | Web | /health endpoint; non-pooled HttpClient (socket exhaustion risk) |
| AP-017 | Anonymous Basket Cookie | Web | Guid basket ID; 10-year cookie; no HttpOnly flag |
| AP-018 | Parallel Async Fan-Out | BlazorAdmin | Task.WhenAll(brandListTask, typeListTask, itemTask) |

### Architecture Violations

| ID | Violation | Impact |
|----|-----------|--------|
| VIO-001 | Shared CatalogContext spans Basket, Order, and Catalog domains | Main blocker for service extraction |
| VIO-002 | OrderService reads Basket aggregate internals cross-domain | Prevents independent Order service without CheckoutDTO |
| VIO-003 | BasketQueryService bypasses IRepository (direct EF) | Inconsistency; acceptable for performance |
| VIO-004 | MediatR applied to reads only; writes bypass entirely | Inconsistent command/query separation |

---

## LAYER 4 — TECHNOLOGY

### Runtime and Framework

| Component | Version | Status |
|-----------|---------|--------|
| .NET SDK | 8.0.x | LTS to Nov 2026 |
| ASP.NET Core | 8.0.2 | LTS to Nov 2026 |
| Blazor WebAssembly | 8.0.2 | LTS to Nov 2026 |
| Entity Framework Core | 8.0.2 | Supported |
| MediatR | 12.0.1 | Supported |
| FluentValidation | 11.9.0 | Supported |
| AutoMapper | 12.0.1 | Supported |
| Ardalis.Specification | 7.0.0 | Supported |
| Bootstrap | 3.4.1 | **EOL — July 2019** |
| aspnet-signalr (client) | 1.0.27 | **Dead/Unused** |

### Infrastructure

| Component | Platform | Notes |
|-----------|----------|-------|
| Azure App Service (B1 Linux) | Azure | Web service only; PublicApi NOT deployed |
| Azure SQL Server v12.0 (×2) | Azure | CatalogDB + IdentityDB; TLS 1.2; firewall open to ALL IPs |
| Azure Key Vault (standard) | Azure | Secrets for Web only; Managed Identity; PublicApi has no access |
| Docker Compose | Local dev | eshopwebmvc:5106, eshoppublicapi:5200, sqlserver:1433 |
| GitHub Actions | CI/CD | Build + test only; no deploy, no SAST, no secret scan |
| Dependabot | CI/CD | Daily NuGet scan; PRs only (non-blocking) |

### Critical Technical Debt (Top 3 — All Blockers for Production)

| ID | Item | Severity |
|----|------|----------|
| TD-01 | JWT_SECRET_KEY = "SecretKeyOfDoomThatMustBeAMinimumNumberOfBytes" hardcoded in source | **CRITICAL** |
| TD-02 | DEFAULT_PASSWORD = "Pass@word1" seeded to admin account on every deployment | **CRITICAL** |
| TD-03 | JWT ValidateIssuer=false, ValidateAudience=false — tokens from any source accepted | **CRITICAL** |
