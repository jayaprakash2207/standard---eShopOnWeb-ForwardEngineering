=== DOCUMENT: 15_FORWARD_ENGINEERING_SPECIFICATION.md ===

# Forward Engineering Specification — eShopOnWeb
## Generation Rules, Templates, and Validation Gates

---

## 1. Purpose

This specification defines the rules for regenerating eShopOnWeb from its reverse-engineered model. It is the executable contract between the knowledge graph (Document 1) and the generation manifest (Document 16). Every generation rule maps to a KNOWN, INFERRED, or MISSING classification from Document 5.

---

## 2. Generation Principles

| Principle | Rule |
|-----------|------|
| No fabrication | Every generated artifact must trace to at minimum one KNOWN or INFERRED evidence item |
| Fail explicitly | If a required input is MISSING, generation halts with an error; it does not assume a default |
| Security by default | Generated security config uses secure defaults; never copies hardcoded secrets from source |
| Idempotency | All database and seed operations must be idempotent (check before insert) |
| Test-first | Generate unit tests alongside every domain service and API endpoint |
| Dependency inversion | Generated code follows Clean Architecture layer dependencies (ApplicationCore has no Infrastructure references) |

---

## 3. Generation Rules by Layer

### 3.1 Domain Layer (ApplicationCore)

**Rule GEN-DOM-01: Entity Generation**
```
For each entity in ENT-001 through ENT-009:
  - Generate C# class with properties matching data dictionary (Document 6)
  - Inherit from BaseEntity (Id: int, protected set)
  - Apply IAggregateRoot on aggregate roots
  - Apply [required] / validation attributes per field constraints
  - Generate private backing collection fields for child collections
  - Expose collections as IReadOnlyCollection<T>
  - Generate domain methods matching confirmed method signatures
```

**Rule GEN-DOM-02: Value Object Generation**
```
For Address and CatalogItemOrdered:
  - Generate as C# record or sealed class (immutable)
  - All properties init-only
  - Apply Guard.Against.* in constructor matching confirmed constraint rules
  - No database ID; no IAggregateRoot
```

**Rule GEN-DOM-03: Guard Clause Application**
```
For each constructor and mutation method:
  - Apply Guard.Against.Null() on reference types
  - Apply Guard.Against.NullOrEmpty() on string fields
  - Apply Guard.Against.OutOfRange() on Quantity (0–max int)
  - Apply Guard.Against.NegativeOrZero() on UnitPrice
  - Apply Guard.Against.Zero() on CatalogItemId, CatalogBrandId, CatalogTypeId
  - Generate custom GuardExtensions.EmptyBasketOnCheckout()
```

**Rule GEN-DOM-04: Specification Generation**
```
For each of 8 confirmed specification classes:
  - Inherit from Specification<T> (Ardalis)
  - Implement constructor taking filter parameters
  - Use .Where(), .Include(), .OrderBy(), .Skip(), .Take() as confirmed
  - Generate matching unit tests
```

**Rule GEN-DOM-05: Domain Exception Generation**
```
Generate: BasketNotFoundException, EmptyBasketOnCheckoutException, DuplicateException
All inherit from Exception; include message constructor
```

---

### 3.2 Application Services

**Rule GEN-SVC-01: BasketService**
```
Implement IBasketService:
  - AddItemToBasket(string username, int catalogItemId, decimal price, int quantity)
    └── Auto-create basket if absent (BR-13); AddItem() merges duplicates (BR-14)
  - DeleteBasketAsync(int basketId)
  - SetQuantities(int basketId, Dictionary<string,int> quantities)
    └── Call SetQuantity per item; call RemoveEmptyItems() (BR-16)
    └── Return Result<Basket> (.NotFound if missing)
  - TransferBasketAsync(string anonymousId, string userName)
    └── No-op if no anonymous basket (BR-19)
    └── ⚠️ Note: 3 separate SaveChanges — flag for future atomicity improvement

Validation: all parameters Guard.Against.NullOrEmpty
```

**Rule GEN-SVC-02: OrderService**
```
Implement IOrderService:
  - CreateOrderAsync(int basketId, Address shippingAddress)
    └── Guard.Against.EmptyBasketOnCheckout
    └── Read IRepository<CatalogItem> for all basket CatalogItemIds
    └── Build CatalogItemOrdered snapshots (BR-21)
    └── Use BasketItem.UnitPrice for order line prices (BR-22) — NOT catalog price
    └── Save via IRepository<Order>
    └── DO NOT clear basket (BR-26)
```

**Rule GEN-SVC-03: Identity Services**
```
Implement ITokenClaimsService:
  - GetTokenAsync(string userName)
    └── Read roles via UserManager.GetRolesAsync()
    └── Build JWT with HMAC-SHA256
    └── Token lifetime: 7 days (NFR-03)
    └── Signing key: READ FROM CONFIGURATION — never hardcode
    └── Validate: set ValidateIssuer=true, ValidateAudience=true (fix TD-03)
```

---

### 3.3 Infrastructure Layer

**Rule GEN-INFRA-01: EF Context**
```
Generate CatalogContext : DbContext:
  - DbSet<CatalogItem> CatalogItems
  - DbSet<CatalogBrand> CatalogBrands
  - DbSet<CatalogType> CatalogTypes
  - Register Basket, Order, BasketItem, OrderItem via ApplyConfigurationsFromAssembly
  - EnableRetryOnFailure() on ALL environments (fix TD-05)

Generate AppIdentityDbContext : IdentityDbContext<ApplicationUser>
```

**Rule GEN-INFRA-02: EF Configurations**
```
CatalogItemConfiguration:
  - UseHiLo("catalog_hilo") on Id
  - HasForeignKey on CatalogBrandId, CatalogTypeId

OrderConfiguration:
  - OwnsOne(ShipToAddress) with all column length constraints
  - Navigation(ShipToAddress).IsRequired()
  - OwnsOne(OrderItem.ItemOrdered)

NEW — Add UNIQUE index on CatalogItems.Name (fix DQ-001):
  - builder.HasIndex(ci => ci.Name).IsUnique()
```

**Rule GEN-INFRA-03: Repository**
```
Generate EfRepository<T> : RepositoryBase<T>, IRepository<T>, IReadRepository<T>
  - Constructor: (CatalogContext context)
  - No additional methods — Ardalis.Specification.EntityFrameworkCore handles all CRUD
```

**Rule GEN-INFRA-04: Email Sender**
```
DO NOT regenerate the stub implementation.
Generate interface IEmailSender with SendEmailAsync signature.
Generate SendGridEmailSender : IEmailSender as the real implementation:
  - Read SendGrid API key from configuration (Key Vault)
  - Required input: MIS-006 (SendGrid API key)
  - BLOCK generation if MIS-006 not resolved
```

---

### 3.4 API Layer (PublicApi)

**Rule GEN-API-01: Endpoint Generation**
```
For each of 8 confirmed REST endpoints:
  - Generate MinimalApi.Endpoint implementing IEndpoint<TResult, TRequest, TService>
  - Apply [Authorize] / [AllowAnonymous] per confirmed auth matrix
  - Apply FluentValidation validator class per request type
  - Remove Task.Delay(1000) from CatalogItemListPagedEndpoint (fix TD-07)

For AuthenticateEndpoint:
  - Use EndpointBaseAsync (Ardalis.ApiEndpoints)
  - lockoutOnFailure: true
  - Return AuthenticateResponse with all fields
```

**Rule GEN-API-02: JWT Bearer Configuration**
```
In PublicApi/Program.cs AddJwtBearer():
  - ValidateIssuerSigningKey: true
  - IssuerSigningKey: read from configuration (Key Vault / env var) — NEVER hardcode
  - ValidateIssuer: true
  - ValidIssuer: from configuration
  - ValidateAudience: true
  - ValidAudience: from configuration
  - RequireHttpsMetadata: true (production) / false (development)
  - BLOCK generation if MIS-001 not resolved
```

**Rule GEN-API-03: Exception Middleware**
```
Generate ExceptionMiddleware:
  - DuplicateException → 409 Conflict
  - For all other exceptions in production:
    └── Return generic "An error occurred" message (fix TD-04)
    └── Log full exception with ILogger
  - In development: may include exception details
```

**Rule GEN-API-04: OpenAPI Configuration**
```
Register Swashbuckle:
  - Title: "My API V1"
  - Version: "v1"
  - Add Bearer security scheme definition
  - app.UseSwagger() and app.UseSwaggerUI() unconditionally
```

---

### 3.5 Web Application

**Rule GEN-WEB-01: Identity Pages**
```
Generate Login.cshtml + Login.cshtml.cs:
  - OnGetAsync(returnUrl?)
  - OnPostAsync(returnUrl?):
    └── SignInManager.PasswordSignInAsync(isPersistent:false, lockoutOnFailure:false)
    └── On success: call TransferAnonymousBasketToUserAsync()
    └── Read BASKET_COOKIENAME cookie
    └── Call IBasketService.TransferBasketAsync(anonymousId, userName)
    └── Delete cookie

Generate Register.cshtml + Register.cshtml.cs:
  - OnPostAsync(returnUrl?): CreateAsync → generate token → SendEmailAsync
  
Generate ConfirmEmail.cshtml + ConfirmEmail.cshtml.cs:
  - OnGetAsync(userId, code): ConfirmEmailAsync
```

**Rule GEN-WEB-02: Checkout Page**
```
BLOCKED: MIS-007 (hardcoded address TD-09)
Generate Checkout.cshtml with:
  - Shipping address form fields: Street, City, State, Country, ZipCode
  - [Authorize] on OnPost
  - OnPostAsync: bind Address from form; call IOrderService.CreateOrderAsync(basketId, address)
  - Optionally: call IBasketService.DeleteBasketAsync after order creation (AO-04)
```

**Rule GEN-WEB-03: Cache Configuration**
```
Generate CachedCatalogViewModelService:
  - Decorator over ICatalogViewModelService
  - IMemoryCache.GetOrCreateAsync with sliding expiration
  - Cache duration: read from configuration (default: 30 seconds)
  - Cache keys: "brands", "types", "items-{pageIndex}-{itemsPage}-{brandId}-{typeId}"
```

**Rule GEN-WEB-04: Auth Configuration**
```
Generate ConfigureCookieSettings:
  - CookieName: "EshopIdentifier"
  - HttpOnly: true
  - SecurePolicy: Always
  - SameSite: Lax
  - ExpireTimeSpan: 60 minutes
  - SlidingExpiration: true

Generate RevokeAuthenticationEvents:
  - Check IMemoryCache on each ValidatePrincipal
  - Key: "{userId}:{securityStamp}"
```

---

### 3.6 BlazorAdmin

**Rule GEN-BLAZOR-01: Services**
```
Generate CatalogItemService, CachedCatalogItemServiceDecorator:
  - CachedCatalogItemServiceDecorator:
    └── Cache TTL: 60 seconds (read from config; default 60s)
    └── Cache key: "items"
    └── Immediate invalidation on Create/Edit/Delete (BR-43)
    └── RefreshLocalStorageList() after any mutation

Generate CustomAuthStateProvider:
  - Poll /User endpoint every UserCacheRefreshInterval (default 60s)
  - Move interval to configuration (fix TD-11 hardcoded poll interval)
  - Attach Bearer token on HttpClient DefaultRequestHeaders

Generate HttpService:
  - HttpGet<T>, HttpPost<T>, HttpPut<T>, HttpDelete<T>
  - Add timeout: configurable (default 30s) to fix missing timeout gap
```

---

### 3.7 Infrastructure (Azure)

**Rule GEN-AZURE-01: Bicep**
```
Generate infra/main.bicep with:
  - Azure App Service (Web) — confirmed configuration
  - Azure App Service (PublicApi) — NEW (fix TD-12; blocked on OQ-006)
  - Azure SQL Server (×2)
  - Azure Key Vault
  - Managed Identity for both App Services

Generate sqlserver.bicep with FIXED firewall (fix TD-11):
  - Replace open-all rule with App Service outbound IP whitelist
  - Or: use privateEndpoint module

Generate appservice.bicep:
  - Add APPLICATIONINSIGHTS_CONNECTION_STRING (when OQ-007 resolved)
```

**Rule GEN-AZURE-02: CI/CD**
```
Generate .github/workflows/dotnetcore.yml:
  - Upgrade: actions/checkout@v4, actions/setup-dotnet@v4
  - Add: gitleaks secret scan (detect TD-01 pattern before it reaches prod)
  - Add: dotnet test --collect:"XPlat Code Coverage"
  - Add: dotnet list package --vulnerable
  - Add: azd deploy on main branch push (after OQ-006 resolved)
```

---

## 4. Validation Gates

Gates that MUST pass before generation proceeds to next phase:

| Gate | Condition | Blocking? |
|------|-----------|-----------|
| G-SEC-01 | JWT signing key sourced from configuration; AuthorizationConstants.JWT_SECRET_KEY absent | BLOCK ALL |
| G-SEC-02 | DEFAULT_PASSWORD absent from source; admin password in Key Vault | BLOCK ALL |
| G-SEC-03 | ValidateIssuer=true, ValidateAudience=true with non-empty values | BLOCK PublicApi |
| G-DB-01 | EF migrations compile; dotnet ef database update succeeds on real SQL Server | BLOCK Deploy |
| G-DB-02 | At least one integration test runs against SQL Server (not InMemory) | BLOCK Deploy |
| G-DB-03 | Unique index on CatalogItems.Name exists in migration | BLOCK CATALOG |
| G-EMAIL-01 | IEmailSender has a real implementation (SendGrid/SMTP); SendEmailAsync is not a stub | BLOCK Registration |
| G-CHECKOUT-01 | Checkout page collects shipping address from form; hardcoded address removed | BLOCK ORDER |
| G-CI-01 | Secret scanning passes with no JWT_SECRET_KEY found in source | BLOCK Deploy |
| G-HEALTH-01 | Health checks use IHttpClientFactory (no new HttpClient()) | WARN |

---

## 5. Regeneration Order (Dependency-Safe Sequence)

```
1. BlazorShared (no dependencies)
2. ApplicationCore/Entities (domain primitives)
3. ApplicationCore/Specifications
4. ApplicationCore/Services (depends on entities + specs)
5. Infrastructure/Data (depends on entities + EF Core)
6. Infrastructure/Identity (depends on Identity packages)
7. Infrastructure/Services (depends on service interfaces)
8. PublicApi (depends on ApplicationCore + Infrastructure)
9. Web (depends on ApplicationCore + Infrastructure)
10. BlazorAdmin (depends on BlazorShared + calls PublicApi)
11. Tests (depends on all above)
12. Infrastructure as Code (independent of application layers)
```
