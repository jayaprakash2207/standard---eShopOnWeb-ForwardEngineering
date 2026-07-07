=== DOCUMENT: 03_USE_CASE_SPECIFICATION.md ===

# Use Case Specification — eShopOnWeb

---

## UC-001: Browse Product Catalog

**Actor:** Anonymous Visitor, Registered Customer
**Confidence:** MEDIUM (Web browse pages not extracted; inferred from service layer)

**Preconditions:** None

**Main Flow:**
1. Actor navigates to storefront
2. System displays paginated product listing (default page size)
3. Actor optionally filters by Brand and/or Type using dropdowns
4. System applies CatalogFilterPaginatedSpecification and returns filtered, paged results
5. System composes image URIs via UriComposer.ComposePicUri()
6. Server-side cache (CachedCatalogViewModelService) serves results for up to 30 seconds before re-querying DB
7. Actor selects a product to view details

**Alternate Flow A — Page size 0:**
- At step 2, if page size = 0, system returns all matching products on a single page (BR-10)

**Postconditions:** Product list or detail displayed

---

## UC-002: Add Item to Basket

**Actor:** Anonymous Visitor, Registered Customer
**Confidence:** HIGH (BasketService.AddItemToBasket confirmed; Web UI ASSUMED)

**Preconditions:** Product catalog is browsable

**Main Flow:**
1. Actor selects a product and chooses a quantity
2. System calls BasketService.AddItemToBasket(userId, catalogItemId, price, quantity)
3. If no basket exists for the user, system creates one (BR-13)
4. If basket already contains the product, system increments existing quantity (BR-14)
5. System saves basket via EfRepository
6. System returns updated basket with new TotalItems count

**Exception Flow E1 — Negative quantity:**
- System raises validation error; quantity must be ≥ 0 (BR-15)

**Postconditions:** Basket created or updated; TotalItems reflects new total

---

## UC-003: Update Basket Quantities

**Actor:** Registered Customer, Anonymous Visitor
**Confidence:** HIGH (BasketService.SetQuantities confirmed)

**Preconditions:** Basket exists with at least one item

**Main Flow:**
1. Actor adjusts item quantities in basket view
2. System calls BasketService.SetQuantities(basketId, {itemId: newQty, ...})
3. For each item: system calls BasketItem.SetQuantity(qty)
4. After all updates, Basket.RemoveEmptyItems() removes any items with qty = 0 (BR-16)
5. System saves updated basket

**Postconditions:** Basket updated; zero-quantity items removed

---

## UC-004: Transfer Anonymous Basket on Login

**Actor:** System (triggered automatically on login)
**Confidence:** HIGH (Login.cshtml.cs + BasketService.TransferBasketAsync confirmed)

**Preconditions:** Customer successfully authenticates via web login form

**Main Flow:**
1. Login page reads BASKET_COOKIENAME cookie from browser
2. If cookie absent: process ends with no changes (BR-19)
3. System calls BasketService.TransferBasketAsync(anonymousId, userName)
4. System retrieves anonymous basket by BuyerId = anonymousId
5. If no anonymous basket: process ends
6. System retrieves or creates authenticated basket for userName
7. System copies all items; matching CatalogItemIds have quantities combined (BR-17)
8. System saves authenticated basket
9. System deletes anonymous basket
10. Login page deletes BASKET_COOKIENAME cookie from browser (BR-18, BR-46)

**Postconditions:** Authenticated basket contains merged items; anonymous basket and cookie deleted

**Risk:** Three separate SaveChangesAsync calls — non-atomic (DQ-002). Partial failure leaves orphaned data.

---

## UC-005: Place Order at Checkout

**Actor:** Registered Customer
**Confidence:** HIGH (OrderService.CreateOrderAsync confirmed; Web checkout form ASSUMED)

**Preconditions:** Customer is authenticated; basket is non-empty

**Main Flow:**
1. Customer provides shipping address on checkout form (**ASSUMED — form not extracted; currently hardcoded TD-09**)
2. System calls OrderService.CreateOrderAsync(basketId, shippingAddress)
3. OrderService calls Guard.Against.EmptyBasketOnCheckout — throws if basket has 0 items (BR-20)
4. OrderService reads IRepository\<CatalogItem\> to retrieve product details for all basket items
5. For each basket item, OrderService creates CatalogItemOrdered snapshot (ProductName, PictureUri, CatalogItemId) (BR-21)
6. OrderService creates Order with BuyerId, OrderDate=now, ShipToAddress, and all OrderItems
7. Each OrderItem.UnitPrice = BasketItem.UnitPrice (frozen at basket-add time, not current catalog price) (BR-22)
8. System saves Order via EfRepository
9. Basket is NOT cleared (BR-26) — caller must explicitly delete basket separately

**Exception Flow E1 — Empty basket:**
- Step 3 throws EmptyBasketOnCheckoutException; checkout blocked (BR-20)

**Exception Flow E2 — Unauthenticated:**
- [Authorize] on checkout page redirects to login before step 1 (BR-24)

**Postconditions:** Order saved permanently with frozen prices and product snapshots; basket persists unchanged

---

## UC-006: Authenticate via API (Admin Login)

**Actor:** Catalog Administrator
**Confidence:** HIGH (AuthenticateEndpoint.HandleAsync confirmed)

**Preconditions:** Valid credentials exist in IdentityDB

**Main Flow:**
1. Client sends POST /api/authenticate with {userName, password}
2. System calls SignInManager.PasswordSignInAsync(username, password, isPersistent:false, lockoutOnFailure:true)
3. On success: system calls IdentityTokenClaimService.GetTokenAsync(userName)
4. Service retrieves user's role memberships from UserManager
5. Service creates JWT with {username, roles} claims, HMAC-SHA256 signature, 7-day expiry (NFR-03)
6. System returns {IsAuthenticated:true, Token:"{jwt}", Username:"{name}"}

**Alternate Flow A — Failed credentials:**
- System increments lockout counter (BR-30)
- Returns {IsLockedOut:true} if lockout threshold exceeded
- Returns {IsNotAllowed:true} if account not permitted (e.g., unconfirmed email)
- Returns {RequiresTwoFactor:true} if 2FA required

**Postconditions:** JWT token issued (7-day validity) OR failure response returned

---

## UC-007: Register Customer Account

**Actor:** Prospective Customer
**Confidence:** HIGH (Register.cshtml.cs confirmed; email confirmation BROKEN)

**Preconditions:** Email address not already registered

**Main Flow:**
1. Visitor submits registration form with email and password
2. System calls UserManager.CreateAsync(newUser, password)
3. System generates email confirmation token
4. System calls EmailSender.SendEmailAsync(**no email sent — stub**)
5. Account is created in IdentityDB; email confirmation token generated but never delivered (BR-34)
6. Account remains in unconfirmed state until confirmation email is clicked (currently impossible)

**Exception Flow E1 — Duplicate email:**
- Step 2 returns error; registration form shows error message

**Postconditions:** Account created (unconfirmed state); confirmation email NOT delivered in current implementation

---

## UC-008: Administer Product Catalog

**Actor:** Catalog Administrator
**Confidence:** HIGH (BlazorAdmin + PublicApi fully confirmed)

**Preconditions:** Administrator authenticated via JWT (UC-006 completed)

**Sub-cases:**

### UC-008a: Create Product
1. Admin fills product form (Name, Description, Price, Brand, Type, optional image)
2. System validates: name not blank (BR-01), description not blank (BR-02), price 0.01–1000 (BR-03/04), brand ≠ 0 (BR-05), type ≠ 0 (BR-06)
3. If image provided: validates JPG/PNG/GIF/JPEG format and ≤ 512 KB (BR-08/09)
4. BlazorAdmin calls POST /api/catalog-items with JWT Bearer
5. PublicApi [Authorize(Roles="Administrators")] gate validates token and role
6. CreateCatalogItemEndpoint saves new CatalogItem via IRepository\<CatalogItem\>
7. BlazorAdmin cache immediately invalidated and refreshed (BR-43)
8. Success toast displayed for 3 seconds (BR-44)

### UC-008b: Update Product
1. Admin selects product from list and edits fields
2. Same validation as UC-008a
3. BlazorAdmin calls PUT /api/catalog-items; same auth gate
4. Cache invalidated; toast shown

### UC-008c: Delete Product
1. Admin clicks delete; confirmation required
2. BlazorAdmin calls DELETE /api/catalog-items/{id}; same auth gate
3. Cache invalidated; toast shown

**Postconditions:** Product created/updated/deleted in CatalogDB; BlazorAdmin cache refreshed

---

## UC-009: View Customer Order History

**Actor:** Registered Customer
**Confidence:** ASSUMED (GetMyOrdersHandler confirmed; Web order history pages not extracted)

**Preconditions:** Customer is authenticated

**Main Flow:**
1. Customer navigates to "My Orders" section
2. System executes GetMyOrdersHandler (MediatR query)
3. Handler uses CustomerOrdersWithItemsSpecification to retrieve all orders for current user
4. System maps Orders to OrderViewModels
5. System displays order list with date, items, and total

**Postconditions:** Customer's order history displayed

---

## Use Case Summary Matrix

| UC | Name | Actor | Auth Required | Confidence | Status |
|----|------|-------|--------------|------------|--------|
| UC-001 | Browse Product Catalog | Any | None | MEDIUM | Partial |
| UC-002 | Add Item to Basket | Any | None | HIGH | Confirmed |
| UC-003 | Update Basket Quantities | Any | None | HIGH | Confirmed |
| UC-004 | Transfer Anonymous Basket on Login | System | Cookie login | HIGH | Confirmed |
| UC-005 | Place Order at Checkout | Registered Customer | Cookie session | HIGH | Partial (address form missing) |
| UC-006 | Authenticate via API | Administrator | Credentials | HIGH | Confirmed |
| UC-007 | Register Customer Account | Prospective Customer | None | HIGH | Partial (email broken) |
| UC-008 | Administer Product Catalog | Administrator | JWT Admin role | HIGH | Confirmed |
| UC-009 | View Customer Order History | Registered Customer | Cookie session | ASSUMED | Assumed |
