the updated basket | — | — |

**Terminal outcomes:** Basket updated; zero-quantity items removed

---

### Process: Transfer Anonymous Basket at Login
**Domain:** Basket → Web
**Trigger:** Customer successfully logs in
**Initiating Actor:** System (automatic on login success)

| Step | Description | Condition (if any) | Exception Path (if any) |
|---|---|---|---|
| 1 | System reads anonymous session identifier from browser cookie | — | If no cookie: process ends immediately |
| 2 | System looks up the anonymous basket | — | If no anonymous basket: process ends immediately |
| 3 | System looks up or creates the customer's authenticated basket | — | — |
| 4 | System copies all items from the anonymous basket into the authenticated basket; matching products have quantities combined | — | — |
| 5 | System saves the authenticated basket | — | — |
| 6 | System permanently deletes the anonymous basket | — | — |
| 7 | System deletes the anonymous session cookie from the browser | — | — |

**Terminal outcomes:** Anonymous items merged into account basket; anonymous basket and cookie destroyed; OR no-op if no anonymous basket existed

---

### Process: Place Order at Checkout
**Domain:** Basket → Order
**Trigger:** Customer submits checkout form with shipping address
**Initiating Actor:** Registered Customer

| Step | Description | Condition (if any) | Exception Path (if any) |
|---|---|---|---|
| 1 | Customer provides shipping address and confirms the order | Customer must be authenticated | — |
| 2 | System retrieves the customer's basket with all items | — | Error if basket not found |
| 3 | System verifies the basket contains at least one item | Basket must not be empty | Checkout blocked; error raised |
| 4 | System retrieves current product details from the catalogue for all items in the basket | Cross-domain read from Catalog | — |
| 5 | System creates a permanent snapshot of each product's name and image as they exist at this moment | Snapshot is immutable; future catalog changes do not affect this order | — |
| 6 | System records each order line using the price captured when the item was added to the basket | Price comes from basket, not current catalog | — |
| 7 | System saves the confirmed order with buyer identity, shipping address, timestamp, and all line items | — | — |
| 8 | Basket remains in place after order creation | Basket is not cleared by the order service | 〰️ ASSUMED — Web layer may clear the basket separately |

**Terminal outcomes:** Order saved permanently; basket not automatically cleared

---

### Process: API Authentication and Token Issuance
**Domain:** Identity
**Trigger:** API caller submits username and password
**Initiating Actor:** Administrator (via admin portal) or any API consumer

| Step | Description | Condition (if any) | Exception Path (if any) |
|---|---|---|---|
| 1 | Caller submits username and password | — | — |
| 2 | System validates credentials; failed attempts count toward account lockout | — | Account locked out: lockout response returned; no token issued |
| 3 | If sign-in not permitted (e.g. unconfirmed email): not-allowed response returned | — | No token issued |
| 4 | If account requires two-factor authentication: two-factor response returned | — | No token issued |
| 5 | On success, system retrieves all roles assigned to the user | — | User not found in database: error |
| 6 | System creates a signed JWT token containing the username and all role memberships | Signed with HMAC-SHA256 | — |
| 7 | Token is set to expire 7 days from issuance | — | — |
| 8 | Token returned to caller | — | — |

**Terminal outcomes:** Token issued (success) OR lockout / not-allowed / two-factor required (failure)

---

### Process: Customer Registration
**Domain:** Web → Identity
**Trigger:** Visitor submits registration form
**Initiating Actor:** Prospective Customer

| Step | Description | Condition (if any) | Exception Path (if any) |
|---|---|---|---|
| 1 | Visitor provides email address and password | — | — |
| 2 | System creates the account | Email must not already be registered | Duplicate email: error returned |
| 3 | System generates a one-time email confirmation token | — | — |
| 4 | System attempts to send a confirmation email | — | ⚠️ Email is never delivered — stub only |
| 5 | 〰️ ASSUMED — Customer directed to confirmation waiting page | Source not available | — |
| 6 | Customer clicks confirmation link | Requires email delivery — currently broken | Unreachable in current implementation |
| 7 | System confirms the email address; account becomes fully active | — | — |

**Terminal outcomes:** Account created immediately; email confirmation permanently blocked by stub

---

### Process: Database Initialisation on Startup
**Domain:** Infrastructure
**Trigger:** Application starts
**Initiating Actor:** System (automatic)

| Step | Description | Condition (if any) | Exception Path (if any) |
|---|---|---|---|
| 1 | System applies database schema changes | SQL Server only | Retries up to 10 times on failure |
| 2 | If no brands exist, inserts pre-configured brand list | Empty database only | Retries up to 10 times |
| 3 | If no types exist, inserts pre-configured type list | Empty database only | Retries up to 10 times |
| 4 | If no products exist, inserts pre-configured product list | Empty database only | Retries up to 10 times |
| 5 | Creates Administrators role if it does not exist | Identity database | — |
| 6 | Creates demo and admin user accounts if they do not exist | Identity database | — |
| 7 | Assigns admin account to the Administrators role | — | — |

**Terminal outcomes:** Database migration-current; reference data and default accounts present

---

## OUTPUT 3 — Business Rules Catalog

| ID | Rule | Domain | Type | Severity | Confidence |
|---|---|---|---|---|---|
| BR-01 | A product name cannot be empty when creating or updating a product. | Catalog | Hard Constraint | High | ✅ HIGH |
| BR-02 | A product description cannot be empty when creating or updating a product. | Catalog | Hard Constraint | High | ✅ HIGH |
| BR-03 | A product price must be greater than zero when creating or updating a product. | Catalog | Hard Constraint | High | ✅ HIGH |
| BR-04 | A product price must be between 0.01 and 1,000 and may have at most two decimal places. | Catalog | Threshold | High | ✅ HIGH |
| BR-05 | A product's brand assignment cannot be set to an unrecognised (zero) identifier. | Catalog | Hard Constraint | High | ✅ HIGH |
| BR-06 | A product's type assignment cannot be set to an unrecognised (zero) identifier. | Catalog | Hard Constraint | High | ✅ HIGH |
| BR-07 | Only users with the Administrator role may create, update, or delete catalog products. All users — including unauthenticated visitors — may browse and view products. | Catalog | Approval Gate | High | ✅ HIGH |
| BR-08 | A product image upload must be in JPG, PNG, GIF, or JPEG format. | Catalog | Hard Constraint | Medium | ✅ HIGH |
| BR-09 | A product image upload must not exceed 512 KB in size. | Catalog | Threshold | Medium | ✅ HIGH |
| BR-10 | A product listing request with a page size of 0 returns all matching products on a single page. | Catalog | Soft Constraint | Low | ✅ HIGH |
| BR-11 | The paged product catalog API includes a fixed 1-second delay on every request. This is a demo artefact and must be removed before production use. | Catalog | SLA | High | ✅ HIGH |
| BR-12 | A duplicate product name cannot be created in the catalog. | Catalog | Hard Constraint | High | ⚠️ LOW — enforcement point not in extracted source |
| BR-13 | A shopping basket is automatically created for a user when they first add an item, if no basket already exists. | Basket | Soft Constraint | Medium | ✅ HIGH |
| BR-14 | Adding a product already in the basket increases the existing quantity rather than creating a duplicate entry. | Basket | Hard Constraint | Medium | ✅ HIGH |
| BR-15 | Basket item quantities must be zero or greater; negative quantities are not permitted. | Basket | Hard Constraint | High | ✅ HIGH |
| BR-16 | Items with a quantity of zero are automatically removed from the basket whenever the basket is updated. | Basket | Hard Constraint | Medium | ✅ HIGH |
| BR-17 | When a customer logs in, all items from their anonymous basket are merged into their authenticated account basket. If the same product exists in both, quantities are combined. | Basket | Hard Constraint | High | ✅ HIGH |
| BR-18 | After a basket transfer on login, the anonymous basket is permanently deleted and the anonymous session cookie is removed from the browser. | Basket | Hard Constraint | High | ✅ HIGH |
| BR-19 | If a customer has no anonymous basket at login, the transfer process ends immediately with no changes. | Basket | Soft Constraint | Low | ✅ HIGH |
| BR-20 | An order cannot be placed if the basket contains no items. | Order | Hard Constraint | High | ✅ HIGH |
| BR-21 | When an order is created, each product's name and image are captured as a permanent historical record. Future catalog changes do not alter completed order records. | Order | Hard Constraint | High | ✅ HIGH |
| BR-22 | Each order line item records the price from the basket at the time the item was added — not the current catalog price. The price is frozen at basket-add time. | Order | Hard Constraint | High | ✅ HIGH |
| BR-23 | An order total is calculated as the sum of (quantity × unit price) for every line item. | Order | Hard Constraint | Medium | ✅ HIGH |
| BR-24 | An order requires a valid buyer identifier. An order cannot be created without identifying the purchaser. | Order | Hard Constraint | High | ✅ HIGH |
| BR-25 | Each order line item must reference a valid product (ID greater than zero) with a non-empty product name and non-empty image address captured at order time. | Order | Hard Constraint | High | ✅ HIGH |
| BR-26 | The shopping basket is NOT automatically cleared when an order is placed. The basket persists after checkout. | Order / Basket | Soft Constraint | Medium | ✅ HIGH |
| BR-27 | Access tokens are valid for 7 days from issuance. After 7 days the user must re-authenticate. | Identity | SLA | High | ✅ HIGH |
| BR-28 | A token can only be issued for a user that exists in the identity database. | Identity | Hard Constraint | High | ✅ HIGH |
| BR-29 | Access tokens embed the user's username and all assigned roles as verifiable claims. | Identity | Hard Constraint | High | ✅ HIGH |
| BR-30 | Failed login attempts count toward account lockout. Repeated incorrect passwords lock the account. | Identity | Hard Constraint | High | ✅ HIGH |
| BR-31 | Login sessions via the API are not persistent. "Remember me" is always disabled. | Identity | Hard Constraint | Medium | ✅ HIGH |
| BR-32 | Two default user accounts (demouser@microsoft.com and admin@microsoft.com) and one Administrator role are seeded at startup with a shared default password. These must be replaced before production deployment. | Identity | Compliance | Critical | ✅ HIGH |
| BR-33 | **[CRITICAL SECURITY]** Three authentication credentials are hardcoded in source code: the authentication key, the JWT signing secret, and the default password. All carry explicit developer warnings against production use. Deployment without replacing these values is a critical security vulnerability. | Identity | Compliance | Critical | ✅ HIGH |
| BR-34 | New registrations require email address confirmation. The confirmation email is currently never delivered — the email service is a non-functional stub. | Identity | Hard Constraint | High | ✅ HIGH (rule exists); ⚠️ LOW (enforcement broken) |
| BR-35 | A buyer record must be linked to a valid identity reference. Cannot be created without a non-empty identity link. NOTE: Buyer entity is not currently persisted to any database. | Buyer | Hard Constraint | Medium | ✅ HIGH (rule in code); ⚠️ LOW (entity unused) |
| BR-36 | The admin portal refreshes the user's authentication state every 60 seconds. | Identity | SLA | Low | ✅ HIGH |
| BR-37 | Product reference data is seeded on first startup only if the database is empty. Existing data is never overwritten. | Infrastructure | Hard Constraint | Medium | ✅ HIGH |
| BR-38 | Database schema changes are applied automatically at startup when running on SQL Server. | Infrastructure | Hard Constraint | Medium | ✅ HIGH |
| BR-39 | The startup data seeding process retries up to 10 times on failure before halting. | Infrastructure | Hard Constraint | High | ✅ HIGH |
| BR-40 | The basket item count displayed in navigation reflects total units across all products — not the number of distinct product types. | Infrastructure | Hard Constraint | Low | ✅ HIGH |
| BR-41 | The admin portal displays catalog items in pages of 10 items per page when loading the paged view. | BlazorAdmin | Threshold | Low | ✅ HIGH |
| BR-42 | The admin portal's local cache of product data expires after 1 minute. | BlazorAdmin | SLA | Low | ✅ HIGH |
| BR-43 | After any product creation, update, or deletion, the admin portal cache is immediately cleared and refreshed — regardless of the 1-minute TTL. | BlazorAdmin | Hard Constraint | Medium | ✅ HIGH |
| BR-44 | Admin portal status notifications auto-dismiss after 3 seconds. | BlazorAdmin | SLA | Low | ✅ HIGH |
| BR-45 | When a customer logs in, the system reads an anonymous session identifier from a browser cookie to locate any anonymous basket items. | Web / Basket | Hard Constraint | High | ✅ HIGH |
| BR-46 | After successfully transferring anonymous basket items on login, the anonymous session cookie is deleted from the browser. | Web / Basket | Hard Constraint | High | ✅ HIGH |

---

## OUTPUT 4 — Stakeholder & Role Matrix

| Technical Role ID | Plain English Name | Responsibilities | Actions They Can Trigger | Data They Can Access | Domain(s) Active In |
|---|---|---|---|---|---|
| ADMINISTRATORS | Catalog Administrator | Maintains the full product catalog — adding new products, updating details and pricing, uploading images, removing discontinued products. Accesses the system via the browser-based admin portal using JWT-authenticated API calls. | Add new product, Update product details / price / image / brand / type, Delete product, View all products | All product fields; own admin session state | Catalog, BlazorAdmin, Identity |
| *(Cookie-Authenticated User)* | Registered Customer | Manages their own shopping basket and places orders through the customer-facing website. Authenticates via email and password. Can view their own order history. | Log in, Add items to basket, Update basket quantities, Remove basket items, Submit checkout with shipping address, View order history | Own basket items and prices, own order history (items, totals, dates, shipping address), product catalog (read-only) | Basket, Order, Web, Identity |
| *(Anonymous / Unauthenticated)* | Unregistered Visitor | Browses products and builds an anonymous basket without creating an account. Cannot place orders. Session tracked via browser cookie. | Browse product catalog, View product details, Add items to anonymous basket, Adjust anonymous basket quantities | Product catalog (read-only), own anonymous basket | Catalog, Basket, Web |
| *(Pre-Registration)* | Prospective Customer | A new visitor initiating account creation. Can register with email and password. Currently cannot complete email confirmation due to broken email delivery. | Register for an account, Submit email confirmation (currently unreachable) | Registration form fields only | Web, Identity |
| *(System — Automatic)* | Automated System Process | Executes background and triggered operations with no human actor: basket transfer on login, order assembly at checkout, database seeding on startup, cache refresh after admin mutations. | Transfer anonymous basket on login, Assemble and save order at checkout, Seed database on startup, Refresh admin browser cache after product changes | Full read/write access to all data stores within each operation's scope | All domains |

---

## OUTPUT 5 — Value Stream Maps

*(Full maps produced in Synthesis Pass — reproduced here for completeness)*

### Value Stream: Customer Purchase Journey

**Trigger:** Visitor arrives at website
**Actors Involved:** Unregistered Visitor, Registered Customer, System
**Terminal Outcomes:** Order placed and recorded | Checkout blocked (empty basket) | Customer abandons

| # | Stage Name | Actor | Business Action | Entry Condition | Exit Output | Stage Type |
|---|---|---|---|---|---|---|
| 1 | Anonymous Browsing | Unregistered Visitor | Browse and filter products; view product details | Visitor accesses the website | Products viewed | Value-Adding |
| 2 | Add to Anonymous Basket | Unregistered Visitor | Select a product and add it with desired quantity | Product identified | Basket created or updated; anonymous session cookie written | Value-Adding |
| 3 | Adjust Basket | Any user | Review basket, change quantities, remove items | At least one basket item | Basket updated; zero-quantity items removed | Value-Adding |
| 4 | Customer Authentication | Unregistered Visitor | Log in to an existing account | Customer wishes to checkout | Authenticated session established | Handoff |
| 5 | Anonymous Basket Transfer | System | Merge anonymous basket into authenticated account basket | Successful login AND anonymous basket cookie exists | Anonymous basket deleted; items merged; cookie deleted | Handoff |
| 6 | Checkout — Shipping Details | Registered Customer | Provide delivery address and confirm order | Basket not empty AND customer authenticated | Shipping address captured; checkout submitted | Value-Adding |
| 7 | Order Validation & Assembly | System | Verify basket not empty; fetch product details; assemble order lines with price snapshots | Checkout submitted | Order items assembled with frozen prices and product snapshots | Verification |
| 8 | Order Creation | System | Record confirmed order permanently | Basket passes validation | Order saved; prices and product details frozen | Value-Adding |
| 9 | Post-Order Basket | System / Customer | 〰️ ASSUMED — basket reviewed or cleared | Order placed | Basket state unresolved — not auto-cleared | Wait-Queue |

**Handoff Points:**
- Stage 4 → 5: System takes over automatically on login success
- Stage 6 → 7–8: System executes checkout logic; no further customer action needed

**Wait States:**
- Stage 9: No SLA or trigger defined for post-checkout basket clearing

**External Dependencies:**
- Stages 1–3, 7–8: SQL Server (product and order data)
- Stage 4: Identity database (credential validation)

**States Accounted For:** No Order status states exist (confirmed absent); AuthenticateResponse outcomes map to Stage 4; ToastLevel excluded (UI-only)

---

### Value Stream: Product Catalog Management

**Trigger:** Administrator logs in to the admin portal
**Actors Involved:** Administrator, System
**Terminal Outcomes:** Product created / updated / deleted | Action rejected (validation or authorisation failure)

| # | Stage Name | Actor | Business Action | Entry Condition | Exit Output | Stage Type |
|---|---|---|---|---|---|---|
| 1 | Admin Authentication | Administrator | Submit credentials to the API | Valid administrator credentials exist | JWT token issued (7-day validity) | Verification |
| 2 | Product List Review | Administrator | View paginated product list (10 per page) | Valid token with Administrator role | Current product list displayed | Value-Adding |
| 3 | Action Selection | Administrator | Choose to create, edit, or delete a product | Product list loaded | Relevant form opened | Handoff |
| 4a | Product Creation | Administrator | Provide all required product fields including optional image | Administrator role confirmed | New product saved; admin cache refreshed | Value-Adding |
| 4b | Product Update | Administrator | Modify one or more fields of an existing product | Product exists; Administrator role confirmed | Product updated; admin cache refreshed | Value-Adding |
| 4c | Product Deletion | Administrator | Permanently remove a product | Product exists; Administrator role confirmed | Product deleted; admin cache refreshed | Exception |
| 5 | Result Notification | System | Display success or error notification | API responds | Toast notification shown for 3 seconds | Verification |

**External Dependencies:** All stages: SQL Server (catalog data); Stage 1: Identity database; Stages 2–4: PublicApi REST

---

### Value Stream: Customer Account Registration

**Trigger:** New visitor decides to create an account
**Actors Involved:** Prospective Customer, System
**Terminal Outcomes:** Account active (requires functional email) | Account created but email confirmation permanently blocked (current state)

| # | Stage Name | Actor | Business Action | Entry Condition | Exit Output | Stage Type |
|---|---|---|---|---|---|---|
| 1 | Registration Submission | Prospective Customer | Provide email and password | Visitor on registration page | Registration submitted | Value-Adding |
| 2 | Account Creation | System | Create account in identity database | Email not already registered | Account record created; confirmation token generated | Value-Adding |
| 3 | Confirmation Email Dispatch | System | Attempt to send confirmation email | Account created | ⚠️ Email never sent — stub; stage is a no-op | Exception |
| 4 | Email Confirmation | Prospective Customer | Click confirmation link | Email received (currently impossible) | Email confirmed; account fully active | Verification |
| 5 | Account Active | Registered Customer | Log in and use all features | Email confirmed | Full access to basket, checkout, order history | Value-Adding |

**Wait States:** Stage 3–4: Process permanently blocked — email never delivered in current implementation

---

## OUTPUT 6 — Domain Architecture Map (Refined)

| Domain | Sub-domains | Key Modules | Architecture Role | Refinements from Deep Analysis |
|---|---|---|---|---|
| Catalog | — | Product API endpoints, Product entities, Product specifications | Core | Full CRUD confirmed; role-gated mutations (Administrators only); image validation in BlazorShared DTO layer; artificial 1-second delay on list endpoint (demo artefact) |
| Basket | — | Basket aggregate, Basket service, Basket query service | Core | Anonymous + authenticated basket support confirmed; basket transfer on login confirmed; basket NOT cleared on order placement (confirmed gap); basket item count uses direct DB query for performance |
| Order | — | Order aggregate, Order service, Order specifications | Core | No order status/lifecycle states — order is a single terminal write. Price snapshot from basket confirmed. Product name/image snapshot confirmed immutable. No post-checkout workflow exists. |
| Buyer / Identity | Buyer aggregate, Auth | Buyer entity, PaymentMethod entity, Identity services, JWT auth endpoint | Core / Gateway | Buyer and PaymentMethod confirmed as unused stubs — not persisted to any database. Three hardcoded security credentials confirmed (critical). Two default seeded accounts confirmed. JWT 7-day expiry confirmed. Account lockout on failed login confirmed. |
| Infrastructure | Data, Logging, Email | EF repository, DB seeding, Logger adapter, Email sender | Support | EF context confirmed for all business entities except Buyer/PaymentMethod. Email sender confirmed full stub. Startup seeding idempotent with 10-retry resilience. BasketQueryService direct-DB bypass confirmed as intentional performance optimisation. |
| BlazorAdmin | Admin UI, Shared | Admin SPA, Cached service decorators, Shared DTO models | Gateway | 1-minute browser cache with immediate invalidation on mutation confirmed. Admin portal authentication polling every 60 seconds confirmed. CatalogItem DTO and domain entity confirmed as intentionally separate objects (DTO adds image upload fields and UI validation). |
| Web | Customer UI | Login/Register/ConfirmEmail pages | Gateway | Login → basket transfer confirmed. Registration → email confirmation broken (stub). Customer-facing Razor pages for browse/basket/checkout/order history not available in source extraction — 4 capabilities marked as ASSUMED. |

**Domain Relationships (confirmed and refined):**
- Catalog → Basket: BasketItem stores CatalogItemId only (reference, no navigation). Price passed by Web layer at add-to-basket time.
- Catalog → Order: OrderService reads IRepository\<CatalogItem\> to build product snapshot at order creation. Cross-domain read confirmed.
- Basket → Order: OrderService reads basket by ID. Basket is not modified or deleted by OrderService after order creation.
- Web → Basket: Login page calls BasketService.TransferBasketAsync. Cookie-based anonymous identity.
- Web → Identity: Cookie-based sign-in via ASP.NET Core Identity SignInManager.
- BlazorAdmin → PublicApi: HTTP REST calls with JWT Bearer token. All catalog mutations require Administrator role.
- PublicApi → Identity: AuthenticateEndpoint calls ITokenClaimsService.GetTokenAsync for JWT issuance.
- Buyer → Identity: IdentityGuid links Buyer to ApplicationUser conceptually; linkage not active (Buyer not persisted).

---

## OUTPUT 7 — Pain Point Report

| # | Pain Point | Domain(s) | Severity | Evidence | Automation Opportunity |
|---|---|---|---|---|---|
| PP-01 | Orders have no status tracking. Once placed, there is no way for customers to track fulfilment, and administrators have no workflow to progress orders through processing or shipping. | Order | High | Order entity has no status field (confirmed); no lifecycle states in registry; no post-order workflow exists | Yes — Add order status workflow with automated transitions and customer email notifications |
| PP-02 | Email delivery is completely non-functional. Registration confirmation emails are never sent. No order confirmation or shipping notifications can be sent. | Identity, Web | High | EmailSender.SendEmailAsync confirmed stub — returns Task.CompletedTask with no email sent (BR-34) | Yes — Wire in SendGrid or SMTP; add order and registration email triggers |
| PP-03 | Payment processing is not implemented. Orders are created without any payment capture. The system cannot process real commercial transactions. | Buyer, Order | High | PaymentMethod entity not persisted; no payment processor SDK in codebase; PCI compliance note present (BR-35) | Yes — Integrate a payment gateway (e.g. Stripe) at checkout; automate payment capture before order creation |
| PP-04 | Three hardcoded security credentials are in source code with explicit warnings they must not be used in production. Two default accounts with a known shared password are seeded to the database at startup. | Identity | Critical | AuthorizationConstants.cs — AUTH_KEY, JWT_SECRET_KEY, DEFAULT_PASSWORD (BR-33); seeded accounts (BR-32) | Yes — Replace with environment variables / secrets manager; deployment pipeline gate blocking deployment with default values |
| PP-05 | Baskets are not cleared after an order is placed. Customers see ordered items still in their basket after purchasing, risking confusion and duplicate orders. | Order, Basket | Medium | BR-26 — no basket.DeleteAsync() in OrderService; basket persists post-checkout | Yes — Automatically clear the basket immediately after successful order creation |
| PP-06 | A 1-second artificial delay is hardcoded into every product catalog list request. Every customer page load that shows products is delayed by 1 full second unnecessarily. | Catalog | Medium | BR-11 — Task.Delay(1000) confirmed in paged catalog endpoint | Yes — Remove the delay; add real performance monitoring |
| PP-07 | The customer profile (Buyer) aggregate is defined in the business domain but not connected to any database. Saved payment methods and customer purchase profiles cannot function. | Buyer | Medium | BR-35 — Buyer not in CatalogContext or AppIdentityDbContext; entity is unused in all workflows | Yes — Add Buyer to an EF context; link to ApplicationUser via IdentityGuid |
| PP-08 | Shopping baskets have no expiry. Anonymous baskets created during browsing sessions persist indefinitely, causing database accumulation over time with no cleanup. | Basket | Medium | No expiry rule or scheduled cleanup found in any part of the codebase or Business Rules Catalog | Yes — Scheduled background job to expire anonymous baskets older than a configurable threshold |
| PP-09 | Customer-facing Razor pages for product browsing, basket management, checkout, and order history were not available for analysis. Business rules and error handling for these critical paths are unverified. | Web | Medium | Validation Queue items #7 and #8 unresolved; four Web capabilities marked ASSUMED | No automation applicable — requires source access to complete |
| PP-10 | All administrative access is controlled by a single "Administrators" role with no granular sub-permissions. No read-only admin, no category-scoped editing, no role hierarchy. | Catalog, Identity | Low | BR-07 — single ADMINISTRATORS role; no secondary roles found in any source | Yes — Introduce policy-based authorisation with scoped roles (e.g. Catalog Viewer, Catalog Editor) |
| PP-11 | The admin portal authentication polling interval (60 seconds) is hardcoded and cannot be changed without a code deployment. | BlazorAdmin | Low | BR-36 — UserCacheRefreshInterval hardcoded in CustomAuthStateProvider | No — Move to configuration value; low business impact |

---

## OUTPUT 8 — Automation Opportunities

| # | Opportunity | Current State | Suggested Approach | Expected Impact |
|---|---|---|---|---|
| AO-01 | Order Status Workflow | Orders are created with no status. No fulfilment workflow exists. | Add an order status field and state-machine-driven workflow (e.g. Confirmed → Processing → Shipped → Delivered). Trigger automated customer email at each transition. | High — Enables end-to-end fulfilment tracking; reduces customer enquiries |
| AO-02 | Transactional Email Notifications | All email sending is a stub. No confirmation, order, or shipping emails are ever sent. | Wire in a transactional email provider (SendGrid, Mailgun, or SMTP relay). Trigger: registration confirmation, order placement confirmation, order status change. | High — Completes the registration flow; provides all post-purchase communication |
| AO-03 | Payment Gateway Integration | No payment processing exists. Orders are recorded without financial transaction. | Integrate a PCI-compliant payment provider (Stripe, Adyen, or Braintree). Automate payment capture at checkout before order creation is committed. Store payment token reference in PaymentMethod entity. | High — Enables real commercial transactions |
| AO-04 | Post-Checkout Basket Clearing | Basket persists after order placement, risking duplicate orders and customer confusion. | Add automatic basket deletion inside OrderService immediately after successful order save. Domain event alternative: OrderCreated event triggers BasketService.DeleteBasketAsync. | Medium — Eliminates post-purchase basket confusion |
| AO-05 | Secrets and Credentials Management | Three hardcoded security values in source. Two default accounts with known passwords seeded at startup. | Replace hardcoded values with environment variable references or a secrets manager (Azure Key Vault, AWS Secrets Manager, or .NET user secrets for development). Add deployment pipeline gate that blocks release if default constants are detected. | Critical — Removes the most significant security vulnerability |
| AO-06 | Stale Basket Expiry | Anonymous baskets persist indefinitely. No expiry or cleanup mechanism exists. | Scheduled background job (Hangfire, .NET BackgroundService, or Azure Functions timer) that deletes anonymous baskets older than a configurable number of days (e.g. 30 days). | Medium — Reduces database bloat; improves data hygiene |
| AO-07 | Remove Artificial Catalog API Delay | A 1-second fixed delay on every product list request degrades all customer page loads. | Remove Task.Delay(1000) from the paged catalog endpoint. Add Application Insights or structured logging to measure real response times. | Medium — Immediate improvement to every customer page load |
| AO-08 | Buyer Profile Persistence | Buyer and PaymentMethod entities defined but not persisted; customer account features unavailable. | Add Buyer and PaymentMethod to an EF DbContext. Link Buyer to ApplicationUser via IdentityGuid. Build a customer account page for saved payment methods and purchase profile. | Medium — Unlocks repeat-purchase convenience and customer account features |

---

## ⚠️ Validation Queue

| # | Item | Chunk | Domain | Reason / Status |
|---|---|---|---|---|
| 1 | Order has no status or lifecycle field | Chunk 2 | Order | ✅ RESOLVED — confirmed absent; order is a single terminal record with no post-creation workflow |
| 2 | Buyer and PaymentMethod not in CatalogContext | Chunks 3, 4 | Buyer | ✅ RESOLVED — confirmed not in CatalogContext or AppIdentityDbContext; entities are unused stubs |
| 3 | PaymentMethod.CardId PCI compliance note | Chunk 3 | Buyer | ✅ RESOLVED — confirmed reference token only; no actual card data; no payment processor connected |
| 4 | Three hardcoded security constants | Chunk 3 | Identity | ✅ RESOLVED — confirmed critical; captured as BR-33 |
| 5 | EmailSender.SendEmailAsync is a stub | Chunks 4, 6 | Infrastructure | ✅ RESOLVED — body confirmed as return Task.CompletedTask; no email ever sent |
| 6 | CatalogItem name collision (entity vs DTO) | Chunk 5 | Catalog / BlazorAdmin | ✅ RESOLVED — intentional separation; domain entity is the persisted record; BlazorShared DTO is the admin form model |
| 7 | Web domain has limited extraction coverage | Chunk 6 | Web | ⚠️ PARTIALLY RESOLVED — Login, Register, ConfirmEmail analysed; browse/basket/checkout/order history pages source not available; 4 capabilities marked ASSUMED |
| 8 | BASKET_COOKIENAME constant value | Chunk 6 | Web | ⚠️ UNRESOLVED — definition file not in extraction payload; business behaviour confirmed (cookie-based anonymous basket); exact cookie name unknown |
| 9 | BasketQueryService bypasses IRepository | Chunk 4 | Infrastructure | ✅ RESOLVED — confirmed intentional performance optimisation; direct COUNT query avoids loading all basket objects into memory |
| 10 | Task.Delay(1000) in catalog list endpoint | Chunk 1 | Catalog | ✅ RESOLVED — confirmed demo artefact; captured as BR-11 (SLA violation) and PP-06 (pain point) |
| 11 | BR-12 duplicate name enforcement point | Chunk 1 | Catalog | ⚠️ UNRESOLVED — DuplicateException exists in codebase but the call site enforcing it for catalog creation is not in the extracted source |
| 12 | Post-checkout basket clearing by Web layer | Chunk 2 | Basket / Web | 〰️ ASSUMED — basket is not cleared by OrderService; whether the Web Razor page clears it separately is unverifiable without Web source |
| 13 | Four Web customer-facing capabilities | Chunk 6 | Web | 〰️ ASSUMED — product browse, basket management, checkout, and order history pages exist (confirmed by specifications and service interfaces) but exact flow steps unverified |

---

## 📋 Agent 1 Discrepancy Log

| # | What Agent 1 Stated | What Deep Analysis Found | Status |
|---|---|---|---|
| 1 | Order entity "may have status field outside extraction scope" | Order entity confirmed to have no status field. No lifecycle states exist for Order anywhere in the system. This is a deliberate simplification in this sample version, not a gap in extraction. | ✅ RESOLVED — Agent 1 was appropriately cautious; deep analysis confirms absence |
| 2 | Buyer entity "may be in AppIdentityDbContext or unused" | Buyer confirmed as unused stub — not in CatalogContext, not in AppIdentityDbContext, not referenced in any active workflow | ✅ RESOLVED — Agent 1's LOW CONFIDENCE assessment was correct |
| 3 | PaymentMethod "Stripe integration intent" | No Stripe SDK, client, or configuration reference found anywhere in codebase. PaymentMethod is a pure stub with a PCI compliance comment and no integration path wired. | ✅ RESOLVED — Agent 1 correctly flagged this as LOW CONFIDENCE |
| 4 | Agent 1 listed "Email Notification (STUB)" as a service capability | Correct — confirmed stub | ✅ No discrepancy |

*No Agent 1 named artifact was contradicted. All discrepancy items were LOW CONFIDENCE flags that deep analysis resolved in the expected direction.*

---

✅ **Agent 2 Analysis Complete.**
Documentation is ready for business review.

**Highest-priority validation item:** PP-04 / BR-33 — Three hardcoded security credentials present in source code with explicit production-unsafe warnings. This must be resolved before any non-development deployment of this system.
