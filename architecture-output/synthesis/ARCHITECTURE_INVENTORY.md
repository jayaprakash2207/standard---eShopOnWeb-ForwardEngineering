# Architecture Inventory — eShopOnWeb

---

## 1. DEPLOYABLE UNITS

| ID | Name | Type | Runtime | Port | Deployment Target | Azure Deploy Path | Confidence |
|----|------|------|---------|------|-------------------|-------------------|------------|
| DEP-001 | eshopwebmvc | Web Application | ASP.NET Core 8 + Blazor WASM | 5106:8080 (Docker) / 443 (Azure) | Docker Compose (dev) + Azure App Service B1 Linux (prod) | azure.yaml → infra/main.bicep | HIGH |
| DEP-002 | eshoppublicapi | REST API | ASP.NET Core 8 Minimal API | 5200:8080 (Docker) | Docker Compose (dev) only | **NOT in azure.yaml — no Azure deployment path (TD-12)** | HIGH |
| DEP-003 | sqlserver | Container DB | Azure SQL Edge (no tag) | 1433:1433 | Docker Compose (dev) only | Azure SQL via Bicep (prod) | LOW |

### Shared Class Libraries (not independently deployable)

| Library | Referenced By | Role |
|---------|--------------|------|
| ApplicationCore | Web, PublicApi, FunctionalTests, UnitTests | Domain layer — entities, services, interfaces, specs |
| Infrastructure | Web, PublicApi, IntegrationTests | EF contexts, repositories, identity, logging, email |
| BlazorAdmin | Web (host) | Blazor WASM SPA (served by Web) |
| BlazorShared | Web, BlazorAdmin, ApplicationCore | Shared DTOs, authorization constants |

---

## 2. DATABASES

| ID | Name | Engine | Version | Tables | Access From | Migrations | PII Stored | Confidence |
|----|------|--------|---------|--------|-------------|------------|------------|------------|
| DB-001 | CatalogDB (Microsoft.eShopOnWeb.CatalogDb) | SQL Server / Azure SQL | v12.0 | CatalogBrands, CatalogTypes, CatalogItems, Baskets, BasketItems, Orders, OrderItems (7 tables) | Web, PublicApi | 3 applied | Email (BuyerId in Basket/Order), Shipping Address (Orders) | HIGH |
| DB-002 | IdentityDB (Microsoft.eShopOnWeb.Identity) | SQL Server / Azure SQL | v12.0 | AspNetUsers, AspNetRoles, AspNetUserRoles, AspNetUserClaims, AspNetUserLogins, AspNetUserTokens, AspNetRoleClaims (7 tables) | Web (primary), PublicApi (read for JWT) | 1 applied | Email, PasswordHash, SecurityStamp | HIGH |

---

## 3. APIs

| ID | Method | Route | Auth | Response | Description | OpenAPI Documented | Confidence |
|----|--------|-------|------|----------|-------------|-------------------|------------|
| API-001 | GET | /api/catalog-items | None | PagedCatalogItemResponse | Paged catalog with brand/type filter; **1-second artificial delay** | Yes — /swagger | HIGH |
| API-002 | GET | /api/catalog-items/{catalogItemId} | None | CatalogItemDto | Single item by ID | Yes | HIGH |
| API-003 | POST | /api/catalog-items | JWT Administrators | Created CatalogItem | Create new catalog item with optional image | Yes | HIGH |
| API-004 | PUT | /api/catalog-items | JWT Administrators | Updated CatalogItem | Update existing catalog item | Yes | HIGH |
| API-005 | DELETE | /api/catalog-items/{catalogItemId} | JWT Administrators | 204 No Content | Delete catalog item by ID | Yes | HIGH |
| API-006 | GET | /api/catalog-brands | None | List\<CatalogBrand\> | All brands | Yes | HIGH |
| API-007 | GET | /api/catalog-types | None | List\<CatalogType\> | All types | Yes | HIGH |
| API-008 | POST | /api/authenticate | None | AuthenticateResponse (token, flags) | Issue JWT; lockout on failed attempts | Yes | HIGH |
| API-009 | GET | /User | Cookie (Web session) | UserInfo (claims, token) | Web endpoint serving user state to BlazorAdmin; consumed every 60s | **No — undocumented** | HIGH |
| API-010 | GET | /health | None | JSON health report | Aggregate health; content-based checks for API and homepage | No | HIGH |

---

## 4. SERVICES (APPLICATION + DOMAIN)

| ID | Name | Layer | Type | Description | Confidence |
|----|------|-------|------|-------------|------------|
| SVC-001 | BasketService | ApplicationCore | Domain Service | Add/remove/update basket items; anonymous→authenticated transfer | HIGH |
| SVC-002 | OrderService | ApplicationCore | Domain Service | Create order from basket with price+product snapshots | HIGH |
| SVC-003 | UriComposer | ApplicationCore | Domain Service | Compose catalog image URIs from template and base URL config | HIGH |
| SVC-004 | IdentityTokenClaimService | Infrastructure | Identity Service | Issue HMAC-SHA256 JWT tokens with role claims; 7-day expiry | HIGH |
| SVC-005 | EfRepository\<T\> | Infrastructure | Repository | Generic EF Core repository for all IAggregateRoot entities | HIGH |
| SVC-006 | BasketQueryService | Infrastructure | Query Service | CountTotalBasketItems via direct EF LINQ (performance optimization) | HIGH |
| SVC-007 | EmailSender | Infrastructure | Notification Service | **STUB — returns Task.CompletedTask; no email sent** | HIGH |
| SVC-008 | LoggerAdapter\<T\> | Infrastructure | Cross-cutting | Wraps ILogger\<T\>; implements IAppLogger\<T\> | HIGH |
| SVC-009 | CachedCatalogViewModelService | Web | Application Service | IMemoryCache decorator; 30s sliding expiry; 3 cache keys | HIGH |
| SVC-010 | GetMyOrdersHandler | Web | Application Query | MediatR handler for customer order history | HIGH |
| SVC-011 | CatalogItemService | BlazorAdmin | API Client | HTTP client wrapper for PublicApi catalog endpoints | HIGH |
| SVC-012 | CachedCatalogItemServiceDecorator | BlazorAdmin | Cache Decorator | 1-minute localStorage cache; immediate mutation invalidation | HIGH |
| SVC-013 | CustomAuthStateProvider | BlazorAdmin | Auth Service | Polls /User every 60s; provides ClaimsPrincipal to Blazor components | HIGH |
| SVC-014 | ExceptionMiddleware | PublicApi | Middleware | DuplicateException→409; all others→500 with message leak | HIGH |
| SVC-015 | HttpService | BlazorAdmin | HTTP Client | Generic HttpGet/Post/Put/Delete wrapper for PublicApi calls | HIGH |

---

## 5. ENTITIES / AGGREGATES

| ID | Name | Type | Domain | DB Table | Status | Confidence |
|----|------|------|--------|----------|--------|------------|
| ENT-001 | CatalogItem | AggregateRoot | Catalog | CatalogItems (HiLo sequence) | Active | HIGH |
| ENT-002 | CatalogBrand | AggregateRoot | Catalog | CatalogBrands | Active | HIGH |
| ENT-003 | CatalogType | AggregateRoot | Catalog | CatalogTypes | Active | HIGH |
| ENT-004 | Basket | AggregateRoot | Basket | Baskets | Active | HIGH |
| ENT-005 | BasketItem | Entity (child) | Basket | BasketItems | Active | HIGH |
| ENT-006 | Order | AggregateRoot | Order | Orders | Active — no status field | HIGH |
| ENT-007 | OrderItem | Entity (child) | Order | OrderItems | Active | HIGH |
| ENT-008 | Address | Value Object | Order | Embedded in Orders | Active | HIGH |
| ENT-009 | CatalogItemOrdered | Value Object | Order | Embedded in OrderItems | Active | HIGH |
| ENT-010 | Buyer | AggregateRoot | Buyer | **NOT PERSISTED** | Dead code | LOW |
| ENT-011 | PaymentMethod | Entity (child) | Buyer | **NOT PERSISTED** | Dead code | LOW |
| ENT-012 | ApplicationUser | External Entity | Identity | AspNetUsers | Active | HIGH |

---

## 6. TECHNOLOGY STACK

### Runtime / Frameworks

| Component | Version | Used In | EOL / Support |
|-----------|---------|---------|---------------|
| .NET SDK | 8.0.x rollForward:latestFeature | All | LTS Nov 2026 |
| ASP.NET Core | 8.0.2 | Web, PublicApi | LTS Nov 2026 |
| Blazor WebAssembly | 8.0.2 | BlazorAdmin | LTS Nov 2026 |
| Entity Framework Core + SqlServer | 8.0.2 | Infrastructure | Supported |
| Entity Framework Core + InMemory | 8.0.2 | Tests only | Supported |

### Key Libraries

| Library | Version | Purpose | Notes |
|---------|---------|---------|-------|
| MediatR | 12.0.1 | CQRS reads (Web only) | Writes bypass MediatR |
| FluentValidation | 11.9.0 | API request validation | PublicApi |
| AutoMapper | 12.0.1 | DTO mapping | CatalogItem → CatalogItemDto in PublicApi |
| Ardalis.Specification | 7.0.0 | Query objects | 8 spec classes |
| Ardalis.ApiEndpoints | 4.1.0 | Endpoint base class | AuthenticateEndpoint |
| Ardalis.GuardClauses | 4.0.1 | Guard clauses | Domain constructors + services |
| Ardalis.Result | 7.0.0 | Result type | BasketService.SetQuantities |
| MinimalApi.Endpoint | 1.3.0 | Catalog endpoints | PublicApi |
| Swashbuckle.AspNetCore | 6.5.0 | OpenAPI / Swagger | PublicApi only |
| Blazored.LocalStorage | 4.5.0 | Browser cache | BlazorAdmin 1-min TTL |
| System.IdentityModel.Tokens.Jwt | 7.3.1 | JWT creation | IdentityTokenClaimService |
| Azure.Identity | 1.10.4 | Managed Identity | Web production only |
| Azure.Extensions.AspNetCore.Configuration.Secrets | 1.3.1 | Key Vault config | Web production only |
| Bootstrap | **3.4.1** | CSS framework | **EOL July 2019 — TD-13** |
| jQuery | 3.6.3 | Client JS | libman.json |
| aspnet-signalr (client) | 1.0.27 | Real-time client | **Declared but unused — TD-16** |

### Test Stack

| Library | Version | Purpose |
|---------|---------|---------|
| xunit | 2.7.0 | Unit + functional tests |
| MSTest.TestFramework | 3.2.2 | Integration tests |
| NSubstitute | 5.1.0 | Mocking |
| Microsoft.AspNetCore.Mvc.Testing | 8.0.2 | Integration test host |
| Microsoft.EntityFrameworkCore.InMemory | 8.0.2 | Test database (**NO FK/UNIQUE constraint enforcement**) |
| coverlet.collector | 6.0.2 | Coverage (not wired in CI) |

---

## 7. SECURITY FINDINGS

| ID | Finding | Severity | Location | Status |
|----|---------|----------|----------|--------|
| SEC-F01 | JWT_SECRET_KEY hardcoded: "SecretKeyOfDoomThatMustBeAMinimumNumberOfBytes" | **CRITICAL** | src/ApplicationCore/Constants/AuthorizationConstants.cs:10 | Open |
| SEC-F02 | DEFAULT_PASSWORD hardcoded: "Pass@word1" — seeded to admin account on startup | **CRITICAL** | src/ApplicationCore/Constants/AuthorizationConstants.cs:12 | Open |
| SEC-F03 | AUTH_KEY hardcoded: "AuthKeyOfDoomThatMustBeAMinimumNumberOfBytes" | **HIGH** | src/ApplicationCore/Constants/AuthorizationConstants.cs:7 | Open |
| SEC-F04 | JWT ValidateIssuer=false, ValidateAudience=false | **CRITICAL** | src/PublicApi/Program.cs:65-66 | Open |
| SEC-F05 | RequireHttpsMetadata=false on JWT bearer | HIGH | src/PublicApi/Program.cs | Open |
| SEC-F06 | Exception.Message leaked in 500 responses (ExceptionMiddleware) | HIGH | src/PublicApi/Middleware/ExceptionMiddleware.cs:47 | Open |
| SEC-F07 | Azure SQL firewall open to all IPs (0.0.0.1-255.255.255.254) | HIGH | infra/core/database/sqlserver/sqlserver.bicep | Open |
| SEC-F08 | Docker SA_PASSWORD hardcoded in docker-compose.yml | HIGH | docker-compose.yml (dev only, but committed) | Open |
| SEC-F09 | Anonymous basket cookie has no HttpOnly flag | MEDIUM | src/Web/Pages/Basket/Checkout.cshtml.cs:95 | Open |
| SEC-F10 | AllowedHosts:* in all appsettings.json | MEDIUM | src/Web/appsettings.json, src/PublicApi/appsettings.json | Open |
| SEC-F11 | [Authorize] + [AllowAnonymous] on same UserController methods | HIGH | src/Web/Controllers/UserController.cs:36-38, 42-45 | Open |
| SEC-F12 | Cookie SameSite=Lax (not Strict) | LOW | src/Web/Configuration/ConfigureCookieSettings.cs | Open |
| SEC-F13 | No secret scanning in CI pipeline | HIGH | .github/workflows/ | Open |
| SEC-F14 | PaymentMethod.CardId: PCI data in non-persisted entity; no payment processor wired | HIGH | src/ApplicationCore/Entities/BuyerAggregate/PaymentMethod.cs | Open |

---

## 8. PII INVENTORY

| Field | Entity/Table | Sensitivity | Purpose | Encryption at Rest |
|-------|-------------|-------------|---------|-------------------|
| Email (as BuyerId) | Basket.BuyerId, Order.BuyerId | PII — identifies individual | Links basket/order to account | Azure SQL TDE (if enabled in Azure) |
| Email | ApplicationUser.Email | PII — contact info | Account login identifier | Azure SQL TDE |
| PasswordHash | ApplicationUser.PasswordHash | Sensitive — hashed credential | Authentication | ASP.NET Identity PBKDF2 hash |
| ShipToAddress.Street/City/State/Country/ZipCode | Orders (embedded) | PII — physical location | Order fulfillment | Azure SQL TDE |
| ProductName, PictureUri | CatalogItemOrdered (embedded) | Non-PII | Historical order record | Azure SQL TDE |
| CardId, Alias, Last4 | PaymentMethod (NOT PERSISTED) | PCI-sensitive / reference token | Payment token (stub) | N/A — dead code |

---

## 9. TECHNICAL DEBT REGISTER

| ID | Item | Category | Severity | Evidence |
|----|------|----------|----------|---------|
| TD-01 | JWT_SECRET_KEY hardcoded | Security | CRITICAL | AuthorizationConstants.cs:10 → PublicApi/Program.cs:54 |
| TD-02 | DEFAULT_PASSWORD hardcoded | Security | CRITICAL | AuthorizationConstants.cs:12 → AppIdentityDbContextSeed.cs:21,25 |
| TD-03 | JWT issuer/audience not validated | Security | CRITICAL | PublicApi/Program.cs:65-66 |
| TD-04 | Exception message in 500 response | Security | HIGH | ExceptionMiddleware.cs:47 |
| TD-05 | No SQL retry in PublicApi or dev/Docker paths | Reliability | HIGH | Dependencies.cs UseSqlServer calls |
| TD-06 | Health checks create new HttpClient per call | Reliability | HIGH | ApiHealthCheck.cs:25, HomePageHealthCheck.cs:26 |
| TD-07 | 1-second artificial delay in catalog list endpoint | Performance | HIGH | CatalogItemListPagedEndpoint.cs:42 |
| TD-08 | EmailSender is a complete stub | Operational | HIGH | EmailSender.cs:10-12 |
| TD-09 | Checkout uses hardcoded shipping address | Functional | HIGH | Checkout.cshtml.cs:57 |
| TD-10 | [Authorize]+[AllowAnonymous] on same methods | Security | HIGH | UserController.cs:36-38 |
| TD-11 | Azure SQL firewall open to all IPs | Security | HIGH | sqlserver.bicep |
| TD-12 | PublicApi has no Azure deployment path | Operational | HIGH | azure.yaml (web only) |
| TD-13 | Bootstrap 3.4.1 — EOL since 2019 | EOL Technology | MEDIUM | libman.json |
| TD-14 | CI actions pinned to v1/v2 (deprecated) | CI/CD | MEDIUM | dotnetcore.yml:7,8 |
| TD-15 | No SAST, secret scan, or container scan in CI | CI/CD | HIGH | .github/workflows/ |
| TD-16 | SignalR client declared, no server hub | Operational | MEDIUM | libman.json |
| TD-17 | Microsoft.AspNetCore.Mvc 2.2.0 in central props | Configuration | MEDIUM | Directory.Packages.props |
| TD-18 | Azure SQL Edge container has no image tag | Configuration | MEDIUM | docker-compose.yml |
| TD-19 | dotnet-xunit deprecated DotNetCliToolReference | EOL Technology | LOW | FunctionalTests.csproj |
