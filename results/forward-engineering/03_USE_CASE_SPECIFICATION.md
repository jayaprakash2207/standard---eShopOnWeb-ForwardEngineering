# Use Case Specification — eShopOnWeb

**Date:** 2026-07-06

---

## UC-001: Browse Product Catalog

**Actor:** Anonymous Shopper (primary), Registered Customer
**Precondition:** None — publicly accessible
**Trigger:** User navigates to catalog page

| Step | Actor | System Response |
|------|-------|----------------|
| 1 | Actor requests catalog page (optional: filter by brand/type, page number) | System checks IMemoryCache (30s TTL); serves from cache or queries CatalogDb |
| 2 | — | System returns paginated list (10 items/page) with Name, Description, Price, PictureUri, Brand, Type |
| 3 | Actor selects a product | System calls GET /api/catalog-items/{id}; returns full product detail |

**Postcondition:** Product details displayed
**Exceptions:** Product not found → 404 response
**Business Rules:** NFR-04 (10/page), NFR-01 (30s cache)
**Known Issue:** Task.Delay(1000) in API-002 adds 1 second artificial latency (TD-21)

---

## UC-002: Add Product to Basket

**Actor:** Anonymous Shopper
**Precondition:** Product exists in catalog; UC-001 completed
**Trigger:** Actor clicks "Add to Cart"

| Step | Actor | System Response |
|------|-------|----------------|
| 1 | Actor clicks add; quantity defaults to 1 | System reads current catalog price for this product |
| 2 | — | System calls BasketService.AddItemToBasket(username/cookie-GUID, catalogItemId, price, quantity) |
| 3 | — | If item already in basket: BasketItem.SetQuantity(existing + new); BR-017 |
| 4 | — | BasketItem.UnitPrice locked at this catalog price; BR-018 |
| 5 | — | System persists Basket and BasketItem to CatalogDb |

**Postcondition:** Basket updated; item quantity and locked price recorded
**Exceptions:** CatalogItem not found → error; negative quantity → guard violation
**Business Rules:** BR-013, BR-017, BR-018

---

## UC-003: Update Basket Quantities

**Actor:** Registered Customer (or Anonymous Shopper)
**Precondition:** Basket exists with at least one item
**Trigger:** Actor adjusts quantities on basket page

| Step | Actor | System Response |
|------|-------|----------------|
| 1 | Actor submits updated quantities per item | System calls BasketService.SetQuantities(basketId, {itemId: qty, ...}) |
| 2 | — | For each item: BasketItem.SetQuantity(qty); validates qty >= 0 (BR-013) |
| 3 | — | Basket.RemoveEmptyItems() — removes any item where qty = 0 (BR-014) |
| 4 | — | Returns Result<Basket>; Ardalis.Result pattern |

**Postcondition:** Basket updated; zero-qty items removed
**Exceptions:** Basket not found → Result.NotFound (BR-015)

---

## UC-004: Login with Basket Merge

**Actor:** Anonymous Shopper with basket
**Precondition:** Actor has anonymous basket; valid account credentials
**Trigger:** Actor submits login form

| Step | Actor | System Response |
|------|-------|----------------|
| 1 | Actor submits email + password | System calls SignInManager.PasswordSignInAsync(lockoutOnFailure:true) |
| 2 | — | On success: establish cookie session |
| 3 | — | System calls TransferAnonymousBasketToUserAsync → BasketService.TransferBasketAsync(anonymousGuid, username) |
| 4 | — | Anonymous basket items merged into user basket; anonymous basket deleted (BR-016) |
| 5 | — | Redirect to intended destination |

**Postcondition:** User authenticated; anonymous basket merged
**Exceptions:** Invalid credentials → error; account locked → IsLockedOut=true (BR-026)
**Business Rules:** BR-016, BR-026

---

## UC-005: Checkout (Place Order)

**Actor:** Registered Customer
**Precondition:** Basket has ≥1 item; actor authenticated
**Trigger:** Actor submits checkout form with shipping address

| Step | Actor | System Response |
|------|-------|----------------|
| 1 | Actor provides shipping address (Street, City, State, Country, ZipCode) | System validates address fields |
| 2 | — | Guard.Against.EmptyBasketOnCheckout → rejects if basket empty (BR-020) |
| 3 | — | OrderService.CreateOrderAsync(basketId, shippingAddress) |
| 4 | — | Loads basket with items; Guard.Against.Null(basket) (BR-019) |
| 5 | — | For each BasketItem: loads CatalogItem; builds CatalogItemOrdered snapshot (BR-021) |
| 6 | — | Creates Order aggregate with OrderItems; uses BasketItem.UnitPrice (BR-022) |
| 7 | — | Persists Order to CatalogDb |
| 8 | — | [Web layer — ASMP-002] Deletes basket |
| 9 | — | [MISSING] Charges payment method — NOT IMPLEMENTED |
| 10 | — | [MISSING] Sends order confirmation email — NOT IMPLEMENTED |

**Postcondition:** Order record created; basket cleared (assumed)
**Exceptions:** Basket not found → BasketNotFoundException; empty basket → EmptyBasketOnCheckoutException
**Business Rules:** BR-019 through BR-025
**Critical Gap:** No payment charging occurs (FE-D-002 decision required)

---

## UC-006: Admin Create Product

**Actor:** System Administrator (authenticated with JWT, ADMINISTRATORS role)
**Precondition:** Actor has valid JWT with Administrators claim
**Trigger:** Admin submits new product form in BlazorAdmin

| Step | Actor | System Response |
|------|-------|----------------|
| 1 | Actor submits product details (name, description, price, brand, type, image) | System validates: name required (BR-007), description required (BR-008), price 0.01–1000 (BR-006) |
| 2 | — | Image validation: size ≤ 512 KB (BR-009), extension .jpg/.jpeg/.png/.gif (BR-010) |
| 3 | — | POST /api/catalog-items with Bearer token |
| 4 | — | PublicApi verifies JWT and ADMINISTRATORS role (BR-011) |
| 5 | — | Checks CatalogItemNameSpecification — rejects if name already exists (BR-012) |
| 6 | — | Creates CatalogItem entity; persists to CatalogDb.Catalog table |
| 7 | — | Returns created CatalogItemDto; BlazorAdmin invalidates LocalStorage cache |

**Postcondition:** Product visible in catalog; admin cache refreshed
**Exceptions:** Unauthorized → 401; duplicate name → 409 (DuplicateException → ExceptionMiddleware)
**Business Rules:** BR-006 through BR-012

---

## UC-007: Admin Update Product

**Actor:** System Administrator
**Precondition:** Product exists; actor authenticated as ADMINISTRATORS
**Trigger:** Admin edits and submits product form

| Step | Actor | System Response |
|------|-------|----------------|
| 1 | Actor modifies product fields | Same validation as UC-006 |
| 2 | — | PUT /api/catalog-items with Bearer token |
| 3 | — | Calls CatalogItem.UpdateDetails(details), .UpdateBrand(id), .UpdateType(id), .UpdatePictureUri(name) as applicable |
| 4 | — | Persists to CatalogDb.Catalog table |

**Business Rules:** BR-001 through BR-005, BR-006, BR-011
**Known Issue:** UpdatePictureUri uses DateTime.MinValue.Ticks → cache-busting broken (TD-22)

---

## UC-008: Register New User

**Actor:** New Visitor
**Precondition:** Email not already registered
**Trigger:** Visitor submits registration form

| Step | Actor | System Response |
|------|-------|----------------|
| 1 | Visitor submits email, password | UserManager.CreateAsync(ApplicationUser, password) |
| 2 | — | Email uniqueness enforced by ASP.NET Identity |
| 3 | — | [STUB] EmailSender.SendEmailAsync → Task.CompletedTask — no email delivered (ASMP-006) |
| 4 | — | SignInManager.SignInAsync — user immediately signed in |

**Postcondition:** Account created; user signed in; confirmation email NOT delivered
**Gap:** FR-AUTH-008 — email confirmation required for production