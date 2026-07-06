# Forward Engineering Input Map — eShopOnWeb

> This document classifies every piece of knowledge about the system into three buckets:
> KNOWN (safe to regenerate from), INFERRED (regenerate with validation gate), MISSING (must resolve before generation).

---

## KNOWN — High confidence; regenerate directly

### Domain Model

| Item | Evidence | Source |
|------|----------|--------|
| CatalogItem entity (all fields, methods, constraints) | Full entity source confirmed | ApplicationCore/Entities/CatalogItem.cs |
| CatalogBrand entity | Full entity source confirmed | ApplicationCore/Entities/CatalogBrand.cs |
| CatalogType entity | Full entity source confirmed | ApplicationCore/Entities/CatalogType.cs |
| Basket aggregate (BuyerId, Items, AddItem, RemoveEmptyItems, SetNewBuyerId) | Full source confirmed | ApplicationCore/Entities/BasketAggregate/Basket.cs |
| BasketItem entity (UnitPrice, Quantity, CatalogItemId, AddQuantity, SetQuantity) | Full source confirmed | ApplicationCore/Entities/BasketAggregate/BasketItem.cs |
| Order aggregate (BuyerId, OrderDate, ShipToAddress, OrderItems, Total()) | Full source confirmed | ApplicationCore/Entities/OrderAggregate/Order.cs |
| OrderItem entity (ItemOrdered, UnitPrice, Units) | Full source confirmed | ApplicationCore/Entities/OrderAggregate/OrderItem.cs |
| Address value object (Street, City, State, Country, ZipCode) | Full source confirmed | ApplicationCore/Entities/OrderAggregate/Address.cs |
| CatalogItemOrdered value object (CatalogItemId, ProductName, PictureUri) | Full source confirmed | ApplicationCore/Entities/OrderAggregate/CatalogItemOrdered.cs |
| BaseEntity (Id: int, virtual protected set) | Full source confirmed | ApplicationCore/Entities/BaseEntity.cs |
| All 8 Specification classes | All confirmed | ApplicationCore/Specifications/*.cs |
| Guard clause extensions (EmptyBasketOnCheckout) | Confirmed | ApplicationCore/Extensions/GuardExtensions.cs |
| All 3 domain exceptions (BasketNotFoundException, EmptyBasketOnCheckoutException, DuplicateException) | Confirmed | ApplicationCore/Exceptions/*.cs |

### Application Services

| Item | Evidence | Source |
|------|----------|--------|
| BasketService (all 4 methods with signatures) | Confirmed | ApplicationCore/Services/BasketService.cs |
| OrderService.CreateOrderAsync(int basketId, Address address) | Confirmed | ApplicationCore/Services/OrderService.cs |
| UriComposer.ComposePicUri(string) | Confirmed | ApplicationCore/Services/UriComposer.cs |
| IdentityTokenClaimService.GetTokenAsync(string) | Confirmed | Infrastructure/Identity/IdentityTokenClaimService.cs |
| EfRepository\<T\> (generic CRUD + spec-based queries) | Confirmed | Infrastructure/Data/EfRepository.cs |
| BasketQueryService.CountTotalBasketItems(string) | Confirmed | Infrastructure/Data/Queries/BasketQueryService.cs |
| LoggerAdapter\<T\> | Confirmed | Infrastructure/Logging/LoggerAdapter.cs |
| CatalogContextSeed (brand/type/item seed data logic) | Confirmed | Infrastructure/Data/CatalogContextSeed.cs |
| AppIdentityDbContextSeed (role + user seeding logic) | Confirmed | Infrastructure/Identity/AppIdentityDbContextSeed.cs |

### API Contracts (PublicApi)

| Item | Evidence | Source |
|------|----------|--------|
| All 8 REST endpoints (method, route, auth, request/response types) | Confirmed | PublicApi/**Endpoints/*.cs |
| ExceptionMiddleware (DuplicateException → 409, others → 500) | Confirmed | PublicApi/Middleware/ExceptionMiddleware.cs |
| Swagger/OpenAPI v1 registration | Confirmed | PublicApi/Program.cs |
| JWT Bearer configuration (HMAC-SHA256, ValidateIssuerSigningKey=true) | Confirmed | PublicApi/Program.cs:54-70 |
| MappingProfile (CatalogItem → CatalogItemDto via AutoMapper) | Confirmed | PublicApi/MappingProfile.cs |

### Database Schema

| Item | Evidence | Source |
|------|----------|--------|
| CatalogDB schema (all 7 tables, columns, types, constraints) | EF migrations + fluent config confirmed | Infrastructure/Data/Migrations/, Config/*.cs |
| IdentityDB schema (7 standard ASP.NET Identity tables) | EF migration confirmed | Infrastructure/Identity/ |
| CatalogItem HiLo key sequence (catalog_hilo) | Confirmed | Infrastructure/Data/Config/CatalogItemConfiguration.cs:14-15 |
| Address owned entity column constraints | Confirmed | Infrastructure/Data/Config/OrderConfiguration.cs:19-43 |
| CatalogItemOrdered owned entity in OrderItem | Confirmed | Infrastructure/Data/Config/OrderConfiguration.cs |

### Security Model

| Item | Evidence | Source |
|------|----------|--------|
| Roles: Administrators (only role) | Confirmed | BlazorShared/Authorization/Constants.cs |
| Cookie auth: HttpOnly=true, SecurePolicy=Always, SameSite=Lax, 60min | Confirmed | Web/Configuration/ConfigureCookieSettings.cs |
| Token revocation via IMemoryCache | Confirmed | Web/Controllers/UserController.cs:44-56 |
| Anonymous basket cookie: Guid ID, 10-year expiry, NO HttpOnly | Confirmed | Web/Pages/Basket/Checkout.cshtml.cs:92-96 |
| Account lockout on failed API login | Confirmed | PublicApi/AuthEndpoints/AuthenticateEndpoint.cs:44 |
| Azure Key Vault integration (Web, production only) | Confirmed | Web/Program.cs |
| Azure Managed Identity (SystemAssigned, Web App Service) | Confirmed | infra/core/host/appservice.bicep |

### Infrastructure and Deployment

| Item | Evidence | Source |
|------|----------|--------|
| Docker Compose topology (3 containers, ports) | Confirmed | docker-compose.yml |
| Azure App Service B1 Linux (Web only) | Confirmed | infra/core/host/appservice.bicep |
| Azure SQL Server v12.0, TLS 1.2 | Confirmed | infra/core/database/sqlserver/sqlserver.bicep |
| Azure Key Vault standard SKU | Confirmed | infra/core/security/keyvault.bicep |
| Environment matrix: Development/Docker/Production | Confirmed | appsettings.*.json, azure.yaml |
| GitHub Actions: build + test on all branches | Confirmed | .github/workflows/dotnetcore.yml |
| Connection strings: CatalogConnection + IdentityConnection | Confirmed | appsettings.*.json |

### BlazorAdmin

| Item | Evidence | Source |
|------|----------|--------|
| All BlazorAdmin service interfaces and implementations | Confirmed | BlazorAdmin/Services/*.cs |
| Blazored.LocalStorage cache: 1-min TTL, immediate mutation invalidation | Confirmed | CachedCatalogItemServiceDecorator.cs |
| CustomAuthStateProvider: 60s poll, JWT relay | Confirmed | BlazorAdmin/CustomAuthStateProvider.cs |
| All BlazorShared DTO models | Confirmed | BlazorShared/Models/*.cs |

### NFRs (Exact Values Known)

| NFR | Value | Source |
|-----|-------|--------|
| Server-side catalog cache TTL | 30 seconds (sliding) | CacheHelpers.cs:7 |
| Client-side catalog cache TTL | 60 seconds | CachedCatalogItemServiceDecorator.cs:34 |
| JWT token lifetime | 7 days | IdentityTokenClaimService.cs:38 |
| Auth cookie validity | 60 minutes | ConfigureCookieSettings.cs:10 |
| BlazorAdmin auth poll interval | 60 seconds | CustomAuthStateProvider.cs:10 |
| Anonymous basket cookie lifetime | 10 years | Checkout.cshtml.cs:95 |

---

## INFERRED — Regenerate with validation gate required

| Item | Inference Basis | Validation Gate | Confidence |
|------|----------------|----------------|------------|
| Web catalog browse pages (route, filter, pagination) | CachedCatalogViewModelService, CatalogFilterPaginatedSpecification, SlugifyParameterTransformer exist | Read src/Web/Pages/Catalog/ | MEDIUM |
| Web basket management pages (add, update, view) | BasketService methods fully documented; BASKET_COOKIENAME cookie pattern confirmed | Read src/Web/Pages/Basket/ | MEDIUM |
| Web checkout page (form fields, address collection) | Checkout.cshtml.cs:57 hardcoded address reveals page exists; [Authorize] confirmed | Read src/Web/Pages/Basket/Checkout.cshtml.cs fully | MEDIUM |
| Web order history page | CustomerOrdersSpecification, GetMyOrdersHandler, GetOrderDetailsHandler exist | Read src/Web/Pages/Order/ | MEDIUM |
| DuplicateException enforcement call site for catalog name uniqueness | DuplicateException class exists; ExceptionMiddleware handles it as 409 | Grep for new DuplicateException() in full source | MEDIUM |
| Basket cookie name constant value | Used in Login.cshtml.cs; definition file not extracted | Read src/Web/Constants.cs | HIGH |
| AutoMapper MappingProfile full contents | CatalogItemListPagedEndpoint uses AutoMapper; MappingProfile class exists | Read src/PublicApi/MappingProfile.cs | HIGH |
| FluentValidation rule classes for API requests | FluentValidation declared; validation wired in PublicApi; individual rule files not extracted | Read src/PublicApi/**/*Validator.cs | MEDIUM |
| Order lifecycle after creation (email, fulfilment status) | No status field in Order; OrderService has no post-creation workflow | Business decision required — PP-01 | LOW |
| Payment capture flow | PaymentMethod entity exists but not persisted; no payment SDK found | Business decision required — AO-03 | LOW |
| Buyer-to-ApplicationUser linkage activation | IdentityGuid field present; not wired; Buyer not persisted | Business decision required — OQ-005 | LOW |

---

## MISSING — Must resolve before code generation; generation blocked

### Critical Blockers (Block ALL generation)

| ID | Missing Item | Impact | Resolution Path |
|----|-------------|--------|----------------|
| MIS-001 | JWT_SECRET_KEY — must be replaced before any deployment generation | All JWT auth is broken/exploitable | Move to Azure Key Vault; generate new 256-bit key |
| MIS-002 | DEFAULT_PASSWORD — must be replaced before any deployment | Admin account compromised on every deploy | Generate random initial password via Key Vault secret |
| MIS-003 | JWT ValidateIssuer/ValidateAudience values — issuer and audience URIs not defined anywhere | Forward-engineering cannot write correct JWT validation config | Architecture decision: define issuer URI (e.g., "https://yourdomain.com") and audience |

### High-Priority Gaps (Block specific capability generation)

| ID | Missing Item | Blocked Capability | Resolution Path |
|----|-------------|-------------------|----------------|
| MIS-004 | Web Razor pages: Catalog browse, Basket, Checkout, Order history | CAP-002, CAP-003, CAP-006 partially blocked | Extract full source of src/Web/Pages/ |
| MIS-005 | PublicApi Azure deployment path | Cannot generate production deployment for PublicApi | Architecture decision: separate App Service, or merge into Web (OQ-006) |
| MIS-006 | Email provider configuration (SendGrid/SMTP credentials and service class) | CAP-007 permanently blocked (email confirmation never works) | Implement real EmailSender with SendGrid or Azure Communication Services |
| MIS-007 | Shipping address form in Web checkout | CAP-003 checkout is non-functional (hardcoded address TD-09) | Implement address form in Checkout.cshtml; bind to CreateOrderAsync |
| MIS-008 | Order status field and fulfilment workflow | CAP-003 has no post-creation state | Business decision: define order status enum and workflow states |
| MIS-009 | Payment processing integration | No payment capture before order creation | Business decision + Stripe/Adyen integration (AO-03) |
| MIS-010 | Database backup and DR configuration | Cannot generate production Bicep without backup policy | Business decision: define RTO/RPO (OQ-010, OQ-011) |

### Medium-Priority Gaps (Affect quality of generated output)

| ID | Missing Item | Impact | Resolution Path |
|----|-------------|--------|----------------|
| MIS-011 | Azure Application Insights provisioning status | Observability Bicep incomplete | Check Azure subscription; add provisioning to infra/ if absent (OQ-007) |
| MIS-012 | Azure SQL firewall IP restriction list | Security Bicep uses open-all rule | Define App Service outbound IPs or use private endpoints |
| MIS-013 | Connection pool and command timeout configuration | NFR spec incomplete | Business decision: set MaxPoolSize, CommandTimeout per load expectations |
| MIS-014 | RTO and RPO targets | NFR spec incomplete | Business decision (OQ-011) |
| MIS-015 | Rate limiting configuration | PublicApi unprotected from flooding | Business decision: define per-IP or per-user rate limits |
| MIS-016 | Buyer/PaymentMethod persistence decision | ENT-010/ENT-011 scope uncertain | Business decision: remove dead code or wire up for payment integration |
| MIS-017 | Dockerfile contents (base images, ENTRYPOINT, EXPOSE port) | Container generation incomplete | Read src/Web/Dockerfile and src/PublicApi/Dockerfile |

---

## Generation Readiness by Capability

| Capability | Readiness | Blockers | Notes |
|------------|-----------|----------|-------|
| CAP-001 Product Catalog Management | **READY** | None | All API, entity, DB confirmed |
| CAP-002 Shopping Basket Management | **PARTIAL** | MIS-004 (Web basket pages) | Domain layer complete; Web pages ASSUMED |
| CAP-003 Order Placement & History | **PARTIAL** | MIS-004, MIS-007 (hardcoded address), MIS-008 (no order status) | Core domain complete; checkout page gap |
| CAP-004 Customer Identity & Auth | **PARTIAL** | MIS-001/002/003 (hardcoded creds), MIS-006 (email stub) | Auth logic complete; security blockers |
| CAP-005 Admin Catalog Portal | **READY** | None | Full BlazorAdmin + API confirmed |
| CAP-006 Customer Storefront | **PARTIAL** | MIS-004 | Domain + cache confirmed; pages ASSUMED |
| CAP-007 Account Registration | **PARTIAL** | MIS-006 (email stub) | Form confirmed; email permanently broken |
| CAP-008 Basket Transfer | **READY** | None | Full flow confirmed |

---

## Recommended Generation Sequence

```
Phase 1 (Safe to generate now — all KNOWN):
  → Domain model (all entities, value objects, specs, guard extensions)
  → Application services (BasketService, OrderService, UriComposer)
  → Infrastructure (EfRepository, contexts, migrations, seed)
  → PublicApi (all 8 endpoints, middleware, Swagger config)
  → BlazorAdmin (all services, cache decorators, auth state provider)
  → Security config (cookie auth, JWT bearer template — with placeholder for MIS-001/002/003)
  → Database DDL (all tables, indexes, sequences)
  → Azure Bicep (App Service, Key Vault, SQL Server — with MIS-012 firewall placeholder)
  → GitHub Actions (build + test — upgrade to v4 actions)

Phase 2 (After business decisions — INFERRED + MISSING resolved):
  → Web Razor pages (catalog browse, basket, checkout, order history) — after MIS-004
  → Real EmailSender implementation — after MIS-006
  → Checkout shipping address form — after MIS-007
  → JWT issuer/audience configuration — after MIS-003
  → PublicApi Azure App Service Bicep — after OQ-006

Phase 3 (Feature enhancements — new development):
  → Order status workflow + email notifications — after MIS-008
  → Payment gateway integration + Buyer persistence — after MIS-009/016
  → Observability: structured logging + distributed tracing + metrics
  → Rate limiting on PublicApi
  → Multi-region deployment with DR configuration
```
