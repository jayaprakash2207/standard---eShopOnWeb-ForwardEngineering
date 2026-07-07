# Open Questions — eShopOnWeb Architecture Extraction

Items below require human review or additional extraction before the architecture can be considered complete. Each item lists the blocking impact if left unresolved.

---

## Category A — Missing Source Coverage

### OQ-001: Web Project Source Not Extracted
**Priority: High**
**Status: Unresolved**

The primary deployable unit (`src/Web`) — an ASP.NET Core MVC / Razor Pages application — was not included in the Layer 1 extraction. This is the application's main user-facing entry point.

**What is missing:**
- Basket controller/page (Add to basket, view basket, remove item)
- Checkout controller/page (enters OrderService.CreateOrderAsync)
- Order history controller/page
- Catalog browsing pages (HomeController, CatalogController if present)
- Authentication login/logout handlers (cookie-based)
- Any middleware in Program.cs / Startup configuration
- Whether Buyer aggregate is used anywhere

**Blocking impact:**
- FLOW-002 (Add to Basket) and FLOW-003 (Checkout) are incomplete
- FLOW-004 (Basket Transfer) — unknown trigger
- Module boundary map for Basket and Order modules is incomplete
- Migration sequence cannot be finalized without knowing Web project structure

**Resolution:** Run Layer 1 extraction again targeting `src/Web/**/*.cs`

---

### OQ-002: Test Project Coverage Unknown
**Priority: Medium**
**Status: Unresolved**

The solution likely contains test projects (standard for eShopOnWeb). If test coverage exists for domain services, it affects migration safety and confidence.

**What is missing:**
- Unit tests for BasketService, OrderService, domain entities
- Integration tests for PublicApi endpoints
- E2E tests (if any)

**Blocking impact:** Cannot assess migration regression risk. Before extracting services, must know which behavior is covered by tests.

**Resolution:** Run extraction on test projects; or human verifies test project existence and coverage level.

---

### OQ-003: BlazorAdmin Hosting Model Unknown
**Priority: Medium**
**Status: Unresolved**

It is unclear whether BlazorAdmin Blazor WASM is:
- (a) Hosted by the Web project (embedded as a subdirectory / middleware)
- (b) Deployed as a standalone static site
- (c) Deployed as part of the PublicApi project

**Blocking impact:** Affects deployment plan. If BlazorAdmin is embedded in Web, extracting Web as separate services requires BlazorAdmin to also move to a standalone deployment (Azure Static Web Apps or equivalent).

**Resolution:** Check `src/Web/Program.cs` or `Startup.cs` for WASM hosting middleware.

---

## Category B — Security Questions

### OQ-004: JWT Secret Rotation Status
**Priority: Critical**
**Status: Requires Action**

`AuthorizationConstants.JWT_SECRET_KEY` is hardcoded as `"SecretKeyOfDoomThatMustBeAMinimumNumberOfBytes"` in source. A TODO comment exists acknowledging this.

**Question:** Has this secret been rotated in the production environment? Or is the same hardcoded value in use?

**Blocking impact:** If the hardcoded key is in production, all JWT tokens are forgeable by anyone with source access. Critical security risk.

**Resolution:** Security team confirms rotation status. Engineering rotates and moves to Key Vault before any migration work.

---

### OQ-005: DEFAULT_PASSWORD in Seed Data
**Priority: Critical**
**Status: Requires Action**

`AuthorizationConstants.DEFAULT_PASSWORD = "Pass@word1"` is hardcoded. This appears to be used in database seed operations.

**Question:** Are production database accounts seeded with this default password? Have the passwords been changed post-seeding?

**Blocking impact:** If default password is in production use, privileged accounts may be compromised.

**Resolution:** Audit Identity DB for accounts using this password. Enforce password rotation.

---

## Category C — Architecture Questions

### OQ-006: Buyer Aggregate Status — Dead Code or Planned Feature?
**Priority: Medium**
**Status: Unresolved**

`Buyer` and `PaymentMethod` aggregate roots exist in ApplicationCore with `IAggregateRoot` marker but are not wired to any service, DbContext, or API endpoint. `PaymentMethod.cs` has a comment: "actual card data must be stored in PCI compliant system like Stripe."

**Question:** Is Buyer aggregate:
- (a) Dead code — safe to remove?
- (b) Used in Web project controllers not in extraction?
- (c) Planned future payment module?

**Blocking impact:** If (c), forward engineering must account for a payment service and associated PCI compliance decisions. If (a), removing reduces confusion during migration.

**Resolution:** Human decision required. Check git log for Buyer aggregate history; check Web project for Buyer service usage.

---

### OQ-007: Where Is /User Endpoint Served?
**Priority: Medium**
**Status: Unresolved**

`CustomAuthStateProvider.cs` makes an HTTP GET to `/User` to retrieve user information after authentication. The endpoint is not in the PublicApi project (no UserEndpoint found).

**Question:** Which project serves GET /User?
- (a) Web project (serves both MVC pages and this API endpoint)
- (b) PublicApi project (not in extraction)
- (c) A separate user service not visible in extraction

**Blocking impact:** Affects auth service extraction design. The auth service must know what user profile data is served and from where.

**Resolution:** Check `src/Web/Controllers/` and `src/PublicApi/` for a UserController or UserEndpoint.

---

### OQ-008: Basket Cleanup After Checkout
**Priority: Medium**
**Status: Unresolved**

FLOW-003 (Checkout/Place Order) traces `OrderService.CreateOrderAsync` which does NOT delete the basket. The basket remains after an order is placed.

**Question:** Does the checkout controller (in Web project) call `BasketService.DeleteBasketAsync` after order creation?

**Blocking impact:** If no basket cleanup, every completed checkout leaves an orphan basket in the database. This becomes a data hygiene and functional bug in the forward-engineered order service.

**Resolution:** Check Web project checkout controller.

---

### OQ-009: Payment Processing
**Priority: Medium**
**Status: Unresolved**

No payment gateway call exists in the traced FLOW-003 checkout flow. The order is placed without any payment processing.

**Question:** Is this intentional demo simplification (the application is a reference sample), or is payment processing implemented elsewhere (Web project, or a third-party webhook)?

**Blocking impact:** If forward-engineered system requires payment, checkout saga must include a payment step. Stripe, PayPal, or Azure Payment Service design needed.

**Resolution:** Product owner confirmation. Check Web project for any Stripe.net, PayPal, or payment-related packages.

---

### OQ-010: Web Project Authentication — Cookie or JWT or Both?
**Priority: Medium**
**Status: Unresolved**

PublicApi uses JWT Bearer authentication. BlazorAdmin uses JWT. But the Web project (MVC/Razor Pages) likely uses ASP.NET Core cookie-based authentication.

**Question:** Does the Web project use:
- (a) Cookie-based auth only
- (b) JWT auth only (unlikely for MVC)
- (c) Both (hybrid — cookies for MVC, JWT for API endpoints)

**Blocking impact:** If Web uses both auth mechanisms, extracting auth-service requires handling both token issuance (JWT) and session management (cookies). Complicates auth service design.

**Resolution:** Check `src/Web/Program.cs` or Startup auth configuration.

---

## Category D — Infrastructure Questions

### OQ-011: Docker Compose vs. Azure Topology for BlazorAdmin
**Priority: Low**
**Status: Unresolved**

`docker-compose.yml` defines `eshopwebmvc` and `eshoppublicapi` services but BlazorAdmin is not listed as a separate container.

**Question:** Is BlazorAdmin served as static files from within the Web or PublicApi container, or is it a separate deployment unit?

**Resolution:** Check docker-compose.yml in detail; check if Web project serves WASM static files.

---

### OQ-012: UseOnlyInMemoryDatabase Toggle — Test Environments
**Priority: Low**
**Status: Informational**

`USE_ONLY_IN_MEMORY_DATABASE` in `src/Infrastructure/Dependencies.cs` is a known toggle for switching to EF InMemory.

**Question:** Is this toggle currently used in any CI environment or only for local development?

**Resolution:** Check CI pipeline configuration (GitHub Actions, Azure DevOps) for environment variable.

---

## Summary Table

| ID | Category | Priority | Status | Blocking |
|---|---|---|---|---|
| OQ-001 | Missing Source | High | Unresolved | Migration sequence |
| OQ-002 | Missing Source | Medium | Unresolved | Migration safety |
| OQ-003 | Architecture | Medium | Unresolved | Deployment plan |
| OQ-004 | Security | Critical | Requires Action | Production deployment |
| OQ-005 | Security | Critical | Requires Action | Production deployment |
| OQ-006 | Architecture | Medium | Unresolved | Payment service design |
| OQ-007 | Architecture | Medium | Unresolved | Auth service design |
| OQ-008 | Architecture | Medium | Unresolved | Order service design |
| OQ-009 | Architecture | Medium | Unresolved | Checkout saga design |
| OQ-010 | Architecture | Medium | Unresolved | Auth service design |
| OQ-011 | Infrastructure | Low | Unresolved | Deployment plan |
| OQ-012 | Infrastructure | Low | Informational | None |
