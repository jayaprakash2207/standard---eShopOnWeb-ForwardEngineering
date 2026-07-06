| 3 | System triggers anonymous basket merge (🔗 cross-domain to Basket) | Successful sign-in only | — |
| 4 | Customer redirected to intended destination | — | — |

**Terminal outcomes:** Customer logged in with session cookie; anonymous basket merged to account

---

### Process 12: New User Registration
**Domain:** Identity/Auth | **Trigger:** New visitor submits registration form | **Initiating Actor:** New User

| Step | Description | Condition (if any) | Exception Path (if any) |
|---|---|---|---|
| 1 | Visitor submits email and password | — | — |
| 2 | System creates the account | — | Email already registered → error returned |
| 3 | System attempts to send a confirmation email | — | 〰️ ASSUMED — email sender is a stub; no email is actually delivered |
| 4 | System signs the new user in immediately without waiting for email confirmation | — | — |

**Terminal outcomes:** Account created; user logged in; confirmation email not delivered in current implementation

---

## OUTPUT 3 — Business Rules Catalog

| ID | Rule | Domain | Type | Severity | Confidence | Source |
|---|---|---|---|---|---|---|
| BR-01 | A product's name must not be blank when updating its details. | Catalog | Hard Constraint | High | ✅ HIGH | CatalogItem.UpdateDetails |
| BR-02 | A product's description must not be blank when updating its details. | Catalog | Hard Constraint | High | ✅ HIGH | CatalogItem.UpdateDetails |
| BR-03 | A product's price must be greater than zero when updating its details. | Catalog | Hard Constraint | High | ✅ HIGH | CatalogItem.UpdateDetails |
| BR-04 | A product's brand must be specified as a valid selection when changing its brand. | Catalog | Hard Constraint | High | ✅ HIGH | CatalogItem.UpdateBrand |
| BR-05 | A product's type must be specified as a valid selection when changing its type. | Catalog | Hard Constraint | High | ✅ HIGH | CatalogItem.UpdateType |
| BR-06 | A product's price must be between 0.01 and 1000 (inclusive) when submitted through the admin interface. | Catalog | Threshold | High | ✅ HIGH | CatalogItem DTO `[Range(0.01, 1000)]` |
| BR-07 | A product name is required when creating or editing a product via the admin interface. | Catalog | Hard Constraint | High | ✅ HIGH | CatalogItem DTO `[Required]` |
| BR-08 | A product description is required when creating or editing a product via the admin interface. | Catalog | Hard Constraint | High | ✅ HIGH | CatalogItem DTO `[Required]` |
| BR-09 | An uploaded product image must not exceed 512 kilobytes in file size. | Catalog | Hard Constraint | High | ✅ HIGH | CatalogItem.IsValidImage — `ImageMaximumBytes = 512000` |
| BR-10 | An uploaded product image must be in one of the following formats: .jpg, .jpeg, .png, or .gif. All other file types are rejected. | Catalog | Hard Constraint | High | ✅ HIGH | CatalogItem.IsExtensionValid |
| BR-11 | Only users in the Administrators role may create, update, or delete products. Browsing the catalog requires no authentication. | Catalog | Approval Gate | High | ✅ HIGH | PublicApi endpoint `[Authorize(Roles = "Administrators")]` |
| BR-12 | A product name must be unique. A new product cannot be created with the same name as an existing product. | Catalog | Hard Constraint | High | ✅ HIGH | CreateCatalogItemEndpoint — DuplicateException |
| BR-13 | A basket item's quantity must be zero or greater; negative quantities are not permitted. | Basket | Hard Constraint | High | ✅ HIGH | BasketItem.AddQuantity and SetQuantity |
| BR-14 | When basket item quantities are updated, any item set to a quantity of zero is automatically removed from the basket. | Basket | Hard Constraint | High | ✅ HIGH | Basket.RemoveEmptyItems called after SetQuantities |
| BR-15 | A basket must exist to update item quantities. If the basket cannot be found, the update returns "not found" and no changes are made. | Basket | Hard Constraint | Medium | ✅ HIGH | BasketService.SetQuantities |
| BR-16 | When a shopper logs in, all items from their anonymous shopping basket are merged into their registered account basket. The anonymous basket is then permanently deleted. | Basket / Identity | Hard Constraint | High | ✅ HIGH | BasketService.TransferBasketAsync |
| BR-17 | If a product already exists as a line in the basket, adding it again increases the quantity of that line rather than creating a second line for the same product. | Basket | Hard Constraint | High | ✅ HIGH | Basket.AddItem |
| BR-18 | The price recorded on a basket item is the price at the time the item was added to the basket. It does not automatically update if the catalog price changes later. | Basket / Catalog | Hard Constraint | High | ✅ HIGH | BasketItem.UnitPrice set at construction; no refresh mechanism |
| BR-19 | An order cannot be created if the basket cannot be found. | Order | Hard Constraint | High | ✅ HIGH | OrderService.CreateOrderAsync — `Guard.Against.Null(basket)` |
| BR-20 | A basket must contain at least one item to proceed to checkout. An empty basket cannot generate an order. | Order | Hard Constraint | High | ✅ HIGH | GuardExtensions.EmptyBasketOnCheckout |
| BR-21 | The product name and image recorded on an order line are a permanent snapshot taken at the time of ordering. Subsequent catalog changes do not affect historical orders. | Order / Catalog | Hard Constraint | High | ✅ HIGH | CatalogItemOrdered — immutable after construction |
| BR-22 | The price charged on each order line is the price that was in effect when the item was added to the basket, not the price at the time of checkout. | Order / Basket | Hard Constraint | High | ✅ HIGH | OrderService.CreateOrderAsync — uses `basketItem.UnitPrice` |
| BR-23 | An order must be associated with a non-empty customer identifier. Orders cannot be created anonymously. | Order | Hard Constraint | High | ✅ HIGH | Order constructor — `Guard.Against.NullOrEmpty(buyerId)` |
| BR-24 | An ordered product snapshot must reference a valid product (ID of 1 or greater), and both product name and picture must be provided. | Order | Hard Constraint | High | ✅ HIGH | CatalogItemOrdered constructor — three Guard clauses |
| BR-25 | An order's total value is the sum of each line's locked unit price multiplied by the quantity ordered on that line. | Order | Hard Constraint | High | ✅ HIGH | Order.Total() |
| BR-26 | Repeated failed login attempts via the API are counted toward account lockout. An account exceeding the lockout threshold will be temporarily prevented from signing in. | Identity/Auth | Hard Constraint | High | ✅ HIGH | AuthenticateEndpoint — `lockoutOnFailure: true` |
| BR-27 | A JWT access token is valid for exactly 7 days from the time it is issued. After 7 days the holder must re-authenticate. | Identity/Auth | SLA | High | ✅ HIGH | IdentityTokenClaimService — `Expires = DateTime.UtcNow.AddDays(7)` |
| BR-28 | A JWT token encodes the user's username and all roles assigned at the time of issuance. Role changes after issuance are not reflected until re-authentication. | Identity/Auth | Hard Constraint | High | ✅ HIGH | IdentityTokenClaimService — claims loop |
| BR-29 | The admin interface treats authentication state as valid for up to 60 seconds without re-checking the server. A deactivated user may retain access for up to 60 seconds after deactivation. | Identity/Auth | SLA | Medium | ✅ HIGH | CustomAuthStateProvider — `TimeSpan.FromSeconds(60)` |
| BR-30 | A user must exist in the system to be issued an access token. An unrecognised username results in a failure. | Identity/Auth | Hard Constraint | High | ✅ HIGH | IdentityTokenClaimService — UserNotFoundException |
| BR-31 | Two default accounts are seeded into every fresh deployment: a demo user with no administrative access and an admin user with full Administrators access, both using the same hardcoded default password. These are development accounts and represent a security risk if not replaced before production deployment. | Identity/Auth | Compliance | High | ✅ HIGH — ⚠️ SECURITY RISK | AppIdentityDbContextSeed — `DEFAULT_PASSWORD = "Pass@word1"` |
| BR-32 | A buyer record must be linked to a valid, non-empty user identity when created. | Buyer | Hard Constraint | Low | 〰️ ASSUMED — constructor enforces this but no code path currently creates a Buyer record | Buyer constructor |

---

## OUTPUT 4 — Stakeholder & Role Matrix

| Technical Role ID | Plain English Name | Responsibilities | Actions They Can Trigger | Data They Can Access | Domain(s) Active In |
|---|---|---|---|---|---|
| ADMINISTRATORS | System Administrator | Manages the product catalog and has full access to the admin interface. Authenticates via JWT token. The only role that can modify catalog content. | Authenticate via API; Create products; Edit product details, price, or image; Delete products; View brand and type lists; Browse full product catalog | All product records (read and write); brand and type lists; own authentication token and identity | Catalog, Identity/Auth |
| Anonymous (unauthenticated) | Anonymous Shopper | Browses the publicly available product catalog and adds items to a temporary basket tracked by a browser cookie. Has no persistent account. | Browse and filter products; View product details; Retrieve brand and type lists; Add items to anonymous basket | Product name, description, price, picture URL, brand name, type name — read only; own basket contents by cookie ID | Catalog, Basket |
| Authenticated User | Registered Customer | Has a persistent account enabling basket persistence, order history, and checkout. Can log in via the website. Switches from anonymous shopper to registered customer at login, at which point any anonymous basket is merged. | Log in (web); Register new account; Add items to basket; Adjust basket quantities; Proceed to checkout; Provide shipping address and confirm order; 〰️ ASSUMED — view order history | Own basket contents; own order records and order line details; public catalog (read) | Identity/Auth, Basket, Order, Catalog |

---

## OUTPUT 5 — Value Stream Maps

*(Full text as produced in Stage 6 above — reproduced here for completeness.)*

### Value Stream 1: Customer Shopping Journey

**Trigger:** A visitor arrives at the online shop
**Actors Involved:** Anonymous Shopper, Registered Customer, System
**Terminal Outcomes:** Order successfully placed and permanently recorded; or shopper exits at any stage without purchasing

| # | Stage Name | Actor | Business Action | Entry Condition | Exit Output | Stage Type |
|---|---|---|---|---|---|---|
| 1 | Product Discovery | Anonymous Shopper | Browse, filter, and explore available products by brand and type | No account required; any visitor may begin | Filtered, paginated product list with names, descriptions, prices, and images | Value-Adding |
| 2 | Product Selection | Anonymous Shopper | View the full details of a product of interest | Visitor selects a product | Full product detail displayed | Value-Adding |
| 3 | Basket Building | Anonymous Shopper | Add one or more products to basket; adjust quantities | Shopper selects a product to purchase | Basket created or updated; price locked to catalog price at time of add | Value-Adding |
| 4 | Account Sign-In | Anonymous Shopper | Authenticate with registered credentials | Shopper initiates login or checkout | Session established; anonymous basket merged into account basket and deleted | Handoff |
| 5 | Basket Review | Registered Customer | Review basket contents and adjust quantities if needed | Shopper is authenticated | Basket confirmed; zero-quantity items removed | Verification |
| 6 | Checkout | Registered Customer | Provide shipping address and confirm the order | Basket contains at least one item; shopper is authenticated | Permanent order record created; product names, images, and prices frozen at basket-add values | Value-Adding |
| 7 | Order Confirmed | System | Record the completed order | Order service confirms successful save | Order stored under shopper's account; basket cleared (〰️ ASSUMED — performed by Web layer) | Value-Adding |

**Handoff Points:**
- Stage 3 → Stage 4: Anonymous basket preserved through login; all items merged into account basket at this transition
- Stage 6 → Stage 7: Order service records the order; the calling web page is responsible for clearing the basket

**Wait States:**
- Stage 4: Shopper must actively choose to log in; no time limit
- Stage 5: Shopper reviews basket before committing; no time limit enforced

**External Dependencies:**
- Stage 4: ASP.NET Core Identity — credential verification and session establishment
- Stage 6: Entity Framework Core (CatalogContext) — reads catalog and basket; writes order

**States Accounted For:**

| Implicit State | Stage |
|---|---|
| Basket does not exist | Pre-Stage 3 |
| Basket exists (anonymous) | Stage 3 |
| Basket exists (account-linked) | Stages 4–5 |
| Basket cleared | Post-Stage 7 (〰️ ASSUMED) |
| Order created (terminal) | Stage 7 |

**Unaccounted States:** Order fulfillment states (Confirmed / Shipped / Delivered / Cancelled) — not present in codebase; outside scope of this implementation.

---

### Value Stream 2: Product Catalog Management (Admin)

**Trigger:** An administrator needs to add, update, or remove a product
**Actors Involved:** System Administrator, System
**Terminal Outcomes:** Catalog updated and changes visible to shoppers immediately; or action rejected due to validation failure

| # | Stage Name | Actor | Business Action | Entry Condition | Exit Output | Stage Type |
|---|---|---|---|---|---|---|
| 1 | Admin Authentication | System Administrator | Enter credentials to access the admin interface | Administrator navigates to admin interface | JWT token issued; valid for 7 days; admin interface unlocked | Verification |
| 2 | Catalog Review | System Administrator | View the current product catalog (loaded from browser cache if less than 1 minute old) | Administrator is authenticated | Product list displayed with all details | Value-Adding |
| 3a | Create Product | System Administrator | Enter product details and submit | No product with the same name already exists; price between 0.01 and 1000; image ≤ 512 KB in accepted format | Product saved; cache refreshed; visible to shoppers immediately | Value-Adding |
| 3b | Update Product | System Administrator | Modify product details and submit | Product exists; name not blank; description not blank; price > 0; valid brand and type selected | Product updated; cache refreshed; changes visible immediately | Value-Adding |
| 3c | Delete Product | System Administrator | Confirm product deletion | Product exists; administrator authenticated | Product permanently removed; cache refreshed | Value-Adding |

**Handoff Points:**
- Stage 1 → Stage 2: JWT issued by PublicApi; Blazor admin interface uses it to authorise all subsequent requests

**Wait States:**
- Stage 1: Administrator must re-authenticate when the 7-day token expires

**External Dependencies:**
- Stage 1: ASP.NET Core Identity — credential verification; JWT signing
- Stages 3a–3c: Entity Framework Core (CatalogContext) — all product persistence

**States Accounted For:**

| Implicit State | Stage |
|---|---|
| Product does not exist | Pre-Stage 3a |
| Product exists | Stages 2, 3b, 3c |
| Product created | Stage 3a exit |
| Product updated | Stage 3b exit |
| Product deleted (terminal) | Stage 3c exit |

---

## OUTPUT 6 — Domain Architecture Map (Refined)

| Domain | Sub-domains | Key Modules | Architecture Role | Refinements from Deep Analysis |
|---|---|---|---|---|
| Catalog | Brands, Types, Items | PublicApi catalog endpoints; ApplicationCore entities; BlazorAdmin UI and services | Core | Two `CatalogItem` classes confirmed as intentional: domain entity (persistence + domain rules) vs Blazor DTO (display + UI validation). `Task.Delay(1000)` confirmed as dev artifact — no business purpose. Image validation logic exists in DTO static methods, not in the domain entity. Picture cache-busting uses `DateTime.MinValue.Ticks` and is permanently broken. |
| Basket | — | BasketAggregate entities; BasketService; BasketQueryService | Core | Basket lifecycle is fully implicit: create-on-first-add, merge-at-login, clear-at-checkout (Web layer responsibility). `BuyerId` dual-use confirmed: username string (authenticated) or GUID string (anonymous). Basket deletion at checkout is NOT performed by OrderService — must be performed by the Web checkout page. `SetNewBuyerId` method exists on Basket but has no confirmed calling code in extracted source. |
| Order | — | OrderAggregate entities and value objects; OrderService; Specification classes | Core | No order lifecycle states — confirmed intentional scope boundary. Basket is read but not deleted by OrderService. Order history lookup Specifications exist (CustomerOrdersWithItemsSpecification, OrderWithItemsByIdSpec) but no confirmed front-end entry point found in extraction. Price-locking at basket-add time is the key business invariant. |
| Identity/Auth | JWT, Roles, Sessions | Infrastructure/Identity; PublicApi/AuthEndpoints; Web/Identity pages; BlazorShared/Authorization | Cross-cutting | Account lockout confirmed enabled (`lockoutOnFailure: true`). JWT valid for 7 days. Auth state cached for 60 seconds in admin client. `/User` endpoint called by Blazor admin client not found in extraction. `ApplicationUser` appears to be a vanilla IdentityUser extension with no custom fields. Hardcoded `JWT_SECRET_KEY` and `DEFAULT_PASSWORD` confirmed as production security risks. |
| Buyer | Payment Methods | BuyerAggregate entities | Support | Confirmed fully dormant: not in CatalogContext, no service, no repository, no API surface. Buyer constructor has one guard clause. Stripe referenced only in a source comment. No active payment processing of any kind exists in the system. |

**Cross-Domain Flow Evidence (confirmed from method bodies):**
- Catalog → Basket: Price passed from Web layer (not looked up inside basket service); BasketItem locks catalog price at add time
- Basket → Order: OrderService reads basket by ID; basket deletion is a Web layer responsibility post-checkout
- Catalog → Order: OrderService reads CatalogItem records to build CatalogItemOrdered snapshots (name + picture URI)
- Identity → Basket: Login.cshtml.cs calls BasketService.TransferBasketAsync on successful sign-in
- Identity → Catalog (Admin): JWT bearer token with ADMINISTRATORS role required for all catalog write operations
- BlazorAdmin → PublicApi: HttpService wrapper sends all API calls with Bearer token attached

---

## OUTPUT 7 — Pain Point Report

| # | Pain Point | Domain(s) | Severity | Evidence | Automation Opportunity |
|---|---|---|---|---|---|
| PP-01 | No order lifecycle tracking exists. Once an order is placed the system cannot track fulfilment, dispatch, or delivery. Operations staff have no visibility into what needs to be processed. | Order | High | Order entity has no status field; CreateOrderAsync is a terminal operation with no subsequent transitions; confirmed across BR-19–BR-25 | Yes — implement order state machine (Confirmed → Packed → Dispatched → Delivered) with notifications at each transition |
| PP-02 | No payment processing capability. Orders are recorded but customers are never charged. The Buyer domain intended to hold payment method data is completely dormant. | Buyer, Order | High | Buyer and PaymentMethod absent from CatalogContext; no Stripe SDK; PaymentMethod.CardId comment references future Stripe intent only | Yes — integrate PCI-compliant payment processor at checkout; implement Buyer domain for saved payment methods |
| PP-03 | Hardcoded security credentials in source code. JWT signing key, auth key, and default account password are literal strings with TODO comments. Any deployment using these values is immediately vulnerable. | Identity/Auth | High | `JWT_SECRET_KEY = "SecretKeyOfDoomThatMustBeAMinimumNumberOfBytes"`, `DEFAULT_PASSWORD = "Pass@word1"` confirmed in source (BR-31) | Yes — environment variable injection or Azure Key Vault; startup validation that rejects known default values |
| PP-04 | Artificial 1-second delay on every public catalog list request. Every page load and filter change for all visitors takes at least 1 second longer than necessary. | Catalog | High | `await Task.Delay(1000)` confirmed as dev artifact with no business purpose — first line of the paged catalog handler | Yes — remove the delay; one-line fix |
| PP-05 | Email confirmation is non-functional. Registration sends no email. Unowned email addresses can be registered without verification. | Identity/Auth | Medium | EmailSender.SendEmailAsync returns Task.CompletedTask; confirmed stub with TODO comment | Yes — wire up SendGrid or SMTP |
| PP-06 | Basket not cleared atomically with order creation. If the web layer fails to clear the basket after calling the order service, customers retain a basket full of already-purchased items. | Order / Basket | Medium | CreateOrderAsync contains no basket deletion call; confirmed by deep analysis (⚠️ DISCREPANCY with Agent 1) | Yes — move basket deletion into the order service as a single atomic transaction |
| PP-07 | Admin browser cache not shared across sessions. Two simultaneous administrators see stale snapshots; one admin's edits can silently overwrite the other's. | Catalog | Medium | CachedCatalogItemServiceDecorator uses per-browser LocalStorage with no cross-session invalidation | Yes — server-side cache with event-based invalidation, or optimistic concurrency (ETags) on write endpoints |
| PP-08 | Product picture cache-busting is permanently broken. Updated product images continue to serve from browser cache because the URL never changes (`?0` always appended). | Catalog | Low | `UpdatePictureUri` uses `new DateTime().Ticks` which equals `DateTime.MinValue.Ticks = 0` | Yes — replace with `DateTimeOffset.UtcNow.Ticks` or a GUID; one-line fix |
| PP-09 | Admin page size hardcoded at 10 items regardless of the requested page size. Large catalogs require many roundtrips. | Catalog | Low | `CatalogItemService.ListPaged` hardcodes `?PageSize=10` in the URL | Yes — pass the pageSize parameter through to the API |
| PP-10 | Buyer domain is an unimplemented stub. Customer profiles and saved payment methods cannot exist in the current system. | Buyer | Medium | Buyer and PaymentMethod have no persistence, no service, and no API surface | Yes — full domain implementation required; Stripe integration for payment methods |
| PP-11 | Single role with no granular permissions. Creating a product and permanently deleting one require identical access. No read-only admin tier exists. | Identity/Auth, Catalog | Low | Only one role defined (`ADMINISTRATORS`); all three write endpoints share the same role check | Yes — introduce policy-based roles (e.g. CatalogEditor, CatalogAdmin) |
| PP-12 | No two-factor authentication for administrators. The 2FA flag is surfaced in the login response but no challenge flow is implemented. Administrator accounts are single-factor only. | Identity/Auth | Medium | `RequiresTwoFactor` flag returned but no subsequent 2FA flow found in extracted source | Yes — implement TOTP challenge via ASP.NET Core Identity |

---

## OUTPUT 8 — Automation Opportunities

| # | Opportunity | Current State | Suggested Approach | Expected Impact |
|---|---|---|---|---|
| AO-01 | Order Fulfilment Workflow | Orders are created and then untracked. No visibility into what needs picking, packing, or shipping. | Add order status field; implement workflow engine or state machine for Confirmed → Packed → Dispatched → Delivered; trigger email/notification at each stage | High — enables the business to operate as a real fulfilment pipeline |
| AO-02 | Payment Processing Integration | No payments are taken. The system records purchase intent but has no charging mechanism. | Integrate Stripe (referenced in source) at the checkout step before order creation; implement Buyer domain to support saved payment methods | High — without this the store cannot take money |
| AO-03 | Secrets Management | JWT signing key and default passwords are literal strings in source code. | Replace all hardcoded secrets with environment variable lookups or Azure Key Vault references; add a startup assertion that fails fast if known default values are detected | High — closes a critical pre-production security gap |
| AO-04 | Transactional Email | No emails sent for registration confirmation, order confirmation, or shipping updates. | Replace the no-op EmailSender stub with SendGrid or SMTP; send confirmation on registration, on order placement, and at each fulfilment stage | Medium — enables email-verified accounts and customer communication |
| AO-05 | Catalog Browse Performance | Every public catalog request waits 1 full second before responding due to an embedded dev artifact. | Remove `await Task.Delay(1000)` from the paged catalog handler | High — immediate user experience improvement; zero trade-off |
| AO-06 | Basket–Order Atomicity | Basket clearing after checkout is a separate manual step; failure leaves purchased items in the basket. | Move basket deletion inside the order service as part of a single database transaction | Medium — eliminates a class of data consistency bugs |
| AO-07 | Collaborative Catalog Editing | Two admins editing simultaneously see stale data; concurrent edits silently overwrite each other. | Add optimistic concurrency (row version / ETag) to update endpoint; or implement server-side cache with write-triggered invalidation | Medium — protects catalog data integrity in multi-admin deployments |

---

## ⚠️ Validation Queue (Unresolved Items)

| # | Item | Domain | Reason |
|---|---|---|---|
| VQ-01 | AutoMapper mapping profiles not in extraction | Catalog | `_mapper.Map<CatalogBrandDto>` etc. confirmed in PublicApi endpoints; profile configuration files not present in extracted source; field-level DTO mapping cannot be fully verified |
| VQ-02 | `ApplicationUser` full class definition not in extraction | Identity/Auth | Only `UserName` and `Email` referenced in SeedAsync; no custom fields observed; treated as vanilla IdentityUser but not confirmed |
| VQ-03 | `/User` endpoint called by Blazor admin client not found in extraction | Identity/Auth | `CustomAuthStateProvider.FetchUser()` calls `GET /User`; endpoint not present in PublicApi or Web extracted source; Blazor auth state hydration depends on it |
| VQ-04 | `Basket.SetNewBuyerId` method — no confirmed calling code | Basket | Method exists on the Basket entity but no calling code found in extracted source; purpose is unclear |
| VQ-05 | Order history retrieval — no confirmed front-end entry point | Order | `CustomerOrdersWithItemsSpecification` and `OrderWithItemsByIdSpec` exist but no service endpoint or Razor Page that uses them is in the extraction; customer order history may exist but cannot be confirmed |
| VQ-06 | Basket deletion at checkout — Web layer responsibility unconfirmed | Order / Basket | OrderService confirmed to NOT delete the basket; deletion must occur in the Web checkout Razor Page; that file is not in the extraction |

---

## 📋 Agent 1 Discrepancy Log

| # | What Agent 1 Said | What Deep Analysis Shows | Status |
|---|---|---|---|
| D-01 | "Basket consumed at checkout (inferred from service pattern — basket consumed at checkout)" — Agent 1 Chunk 3 cross-domain note | `OrderService.CreateOrderAsync` reads the basket but contains no `_basketRepository.DeleteAsync` call. The basket is NOT deleted by the order service. Deletion must be performed by the calling Web layer (Web checkout Razor Page, not in extracted source). | ⚠️ UNRESOLVED — Web checkout page not in extraction; basket deletion by Web layer is assumed but unconfirmed |
| D-02 | Agent 1 did not capture `Basket.SetNewBuyerId`, `CatalogItem.IsValidImage`, or `CatalogItem.IsExtensionValid` | All three methods exist in the extracted source files and carry business logic (image size/format validation; basket owner reassignment). | Resolved — added to capability map and business rules catalog |

---

✅ **Agent 2 Analysis Complete.**
Documentation is ready for business review.

**Highest-priority validation item:** VQ-06 — Basket deletion at checkout is assumed to be performed by the Web checkout page (outside the extracted source). If this step is absent or fails, customers will retain a basket full of already-purchased items after every order. Recommend confirming the Web checkout Razor Page implementation before considering the checkout flow production-ready.
