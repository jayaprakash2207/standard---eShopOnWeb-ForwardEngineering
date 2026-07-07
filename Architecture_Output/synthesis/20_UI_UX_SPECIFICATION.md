=== DOCUMENT: 20_UI_UX_SPECIFICATION.md ===

# UI/UX Specification — eShopOnWeb

---

## 1. Overview

This specification covers the user interface and user experience design requirements for eShopOnWeb. Content is classified by evidence confidence: **CONFIRMED** (direct code evidence), **INFERRED** (deduced from architecture), and **REQUIRED** (must be defined before generation can complete for that page).

---

## 2. Design System

### 2.1 Current Framework

| Attribute | Current Value | Status |
|-----------|--------------|--------|
| CSS Framework | Bootstrap 3.4.1 | ⚠️ EOL July 2019 — must upgrade (TD-13) |
| Typography | Bootstrap 3 defaults | Inherited |
| Icons | Glyphicons (Bootstrap 3 bundled) | Will be removed in Bootstrap 5 upgrade |
| Color scheme | Bootstrap 3 default | No custom brand palette found |
| JS Framework | jQuery 3.6.3 | Keep or remove with Bootstrap 5 upgrade |
| Notifications (Web) | toastr.js 2.1.4 | Keep |
| Notifications (Admin) | Custom ToastService (Blazor) | 3-second dismiss delay confirmed |
| Validation (Web) | jquery-validation + ASP.NET MVC unobtrusive | Keep |
| Responsive target | Mobile + Desktop | Bootstrap 3 responsive grid |

### 2.2 Layout Template (INFERRED)

```
_Layout.cshtml — Shared shell for all Web pages
┌─────────────────────────────────────────────────────────────┐
│  [Logo/Brand]  [Catalog]  [Basket (N)]  [Login/Username]    │  ← Header / Navbar
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                    @RenderBody()                            │  ← Page Content
│                                                             │
├─────────────────────────────────────────────────────────────┤
│           Footer — copyright, links                         │  ← Footer
└─────────────────────────────────────────────────────────────┘
```

**Basket badge:** Nav bar shows item count. Populated by `IBasketViewModelService.GetOrCreateBasketForUser()`.

**Auth state:** `_LoginPartial.cshtml` renders Login/Register links (anonymous) or username + Logout link (authenticated).

---

## 3. Page Specifications

### 3.1 Catalog Browse Page

**Route:** `/` or `/Catalog/Index` (INFERRED)
**Auth required:** No (anonymous)
**Confidence:** INFERRED (MIS-004 — page source not extracted)

#### Layout

```
┌───────────────────────────────────────────────────────────────┐
│  Filter by Brand: [Dropdown ▼]   Filter by Type: [Dropdown ▼] │  ← Filter bar
├───────────────────────────────────────────────────────────────┤
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐                      │
│  │ Img  │  │ Img  │  │ Img  │  │ Img  │                      │
│  │Name  │  │Name  │  │Name  │  │Name  │   ← Product grid      │
│  │$0.00 │  │$0.00 │  │$0.00 │  │$0.00 │                      │
│  │[Add] │  │[Add] │  │[Add] │  │[Add] │                      │
│  └──────┘  └──────┘  └──────┘  └──────┘                      │
├───────────────────────────────────────────────────────────────┤
│  [← Prev]  Page 1 of N  [Next →]                              │  ← Pagination
└───────────────────────────────────────────────────────────────┘
```

#### Data bindings

| UI Element | Data Source | Service | Spec |
|------------|------------|---------|------|
| Brand dropdown | CatalogBrands | CachedCatalogViewModelService | CatalogFilterSpecification |
| Type dropdown | CatalogTypes | CachedCatalogViewModelService | CatalogFilterSpecification |
| Product grid | CatalogItems (filtered, paginated) | CachedCatalogViewModelService | CatalogFilterPaginatedSpecification |
| Pagination | Total count / page size | CachedCatalogViewModelService | skip/take |
| "Add to basket" | POST (basket item) | BasketService.AddItemToBasket | — |

#### URL query parameters (INFERRED)

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `brandId` | int? | null (all brands) | Filter |
| `typeId` | int? | null (all types) | Filter |
| `page` | int | 1 | Pagination |
| `pageSize` | int | (configurable) | Items per page |

---

### 3.2 Basket Page

**Route:** `/Basket/Index` (INFERRED)
**Auth required:** No (anonymous users supported via GUID cookie)
**Confidence:** INFERRED (MIS-004)

#### Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Your Shopping Basket                                        │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ [Img] Name | Qty: [___] | Unit: $X.XX | Total: $X.XX│   │
│  │       Brand/Type                             [Remove]│   │
│  └─────────────────────────────────────────────────────┘   │
│  ... (one row per basket item)                              │
│                                                             │
│  Subtotal: $XX.XX                        [Update Basket]    │
│                                          [Checkout →]       │
└─────────────────────────────────────────────────────────────┘
```

#### Behavior

| Action | Handler | Business Rule |
|--------|---------|--------------|
| Update quantities | BasketService.SetQuantities() | RemoveEmptyItems() when qty=0 (BR-16) |
| Remove item | Set quantity to 0 → RemoveEmptyItems | BR-16 |
| Checkout button | Redirect to /Basket/Checkout | Requires [Authorize] — login redirect |
| Anonymous basket | Cookie `BASKET_COOKIENAME` | 10-year expiry confirmed (Checkout.cshtml.cs:95) |
| Transfer on login | BasketService.TransferBasketAsync() | Triggered by Login.cshtml.cs on POST |

---

### 3.3 Checkout Page

**Route:** `/Basket/Checkout`
**Auth required:** Yes (`[Authorize]`)
**Confidence:** PARTIAL — page model confirmed; address form REQUIRED (MIS-007)

#### Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Checkout                                                    │
│                                                             │
│  Order Summary                    Shipping Address           │
│  ┌──────────────────────┐        ┌────────────────────────┐ │
│  │ [Item 1] × Qty $X.XX │        │ Street:  [__________]  │ │
│  │ [Item 2] × Qty $X.XX │        │ City:    [__________]  │ │
│  │ ...                  │        │ State:   [__________]  │ │
│  │ Total: $XX.XX        │        │ Country: [__________]  │ │
│  └──────────────────────┘        │ Zip:     [__________]  │ │
│                                  └────────────────────────┘ │
│                                  [Place Order]               │
└─────────────────────────────────────────────────────────────┘
```

#### Form Fields (REQUIRED — resolves TD-09, MIS-007)

| Field | Input Type | Max Length | Required | Validation |
|-------|-----------|-----------|----------|-----------|
| Street | text | 180 | Yes | Not empty |
| City | text | 100 | Yes | Not empty |
| State | text | 60 | Yes | Not empty |
| Country | text | 90 | Yes | Not empty |
| ZipCode | text | 18 | Yes | Not empty |

#### Behavior

| Step | Action | Service |
|------|--------|---------|
| 1 | Load basket items + prices | BasketService |
| 2 | User fills address form | Client-side validation |
| 3 | POST /Basket/Checkout | OrderService.CreateOrderAsync(basketId, address) |
| 4 | Order created | Order saved to DB; basket NOT cleared (BR-26) |
| 5 | Redirect | To confirmation page or order history (INFERRED) |

> **TD-09 CRITICAL:** Current source has `new Address("123 Main St.", "Kent", "OH", "United States", "44240")` hardcoded. This form **must** replace that constant before generation is complete.

---

### 3.4 Login Page

**Route:** `/Account/Login`
**Auth required:** No
**Confidence:** HIGH

#### Layout

```
┌───────────────────────────────────────────┐
│  Sign in                                  │
│                                           │
│  Email:    [___________________________]  │
│  Password: [___________________________]  │
│                                           │
│  [Sign in]         [Register as new user] │
│                                           │
│  [Forgot your password?]                  │
└───────────────────────────────────────────┘
```

#### Behavior

| Action | Implementation |
|--------|---------------|
| POST | SignInManager.PasswordSignInAsync(isPersistent:false, lockoutOnFailure:false) |
| On success | TransferAnonymousBasketToUserAsync() → Redirect(returnUrl) |
| Anonymous basket transfer | Read BASKET_COOKIENAME cookie → IBasketService.TransferBasketAsync → Delete cookie |
| On failure | Return page with ModelState error |
| No lockout | Web login does NOT lock out on failure (unlike API) |

---

### 3.5 Register Page

**Route:** `/Account/Register`
**Auth required:** No
**Confidence:** HIGH

#### Layout

```
┌───────────────────────────────────────────┐
│  Create a new account                     │
│                                           │
│  Email:            [_________________]    │
│  Password:         [_________________]    │
│  Confirm Password: [_________________]    │
│                                           │
│  [Register]                               │
└───────────────────────────────────────────┘
```

#### Behavior

| Action | Implementation | Gap |
|--------|---------------|-----|
| POST | UserManager.CreateAsync(user, password) | — |
| Email confirmation | GenerateEmailConfirmationTokenAsync → SendEmailAsync | ⚠️ TD-08: EmailSender stub; no email sent |
| Auto-signin after register | INFERRED | MIS-004 |

---

### 3.6 Order Confirmation / Order History Pages

**Route:** `/Orders/MyOrders` (INFERRED)
**Auth required:** Yes
**Confidence:** INFERRED (MIS-004)

#### Data Source

- Handler: `GetMyOrdersHandler` (MediatR query)
- Specification: `CustomerOrdersWithItemsSpecification(buyerId)`
- Returns: List of orders with OrderItems and CatalogItemOrdered snapshots

#### Expected Layout (INFERRED)

```
┌───────────────────────────────────────────────────────────┐
│  My Orders                                                │
│                                                           │
│  Order #1234  |  Date: 2026-01-15  |  Total: $49.95       │
│    ├── .NET Bot Black Hoodie (1) × $19.50                 │
│    └── .NET Foundation Pin (2) × $9.99                    │
│                                                           │
│  Order #1198  |  Date: 2025-12-01  |  Total: $12.99       │
│    └── .NET Bot White Mug (1) × $12.99                    │
└───────────────────────────────────────────────────────────┘
```

> Note: CatalogItemOrdered is a snapshot (ProductName + PictureUri + CatalogItemId). Product name shows historical name at time of order, not current catalog name.

---

## 4. BlazorAdmin UI

### 4.1 Catalog Item List Page

**Route:** `/BlazorAdmin/CatalogItems` (INFERRED)
**Auth required:** Yes (Administrators role + JWT Bearer)
**Confidence:** HIGH

#### Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Catalog Items Admin              [+ Create New Item]        │
├─────────────────────────────────────────────────────────────┤
│  ID │ Name                  │ Price  │ Brand    │ Type │ Act │
│  1  │ .NET Bot Black Hoodie │ $19.50 │ .NET     │ T-S  │ ✏🗑 │
│  2  │ .NET Black & White    │ $8.50  │ .NET     │ Mug  │ ✏🗑 │
│  ...                                                        │
│  (10 items per page — confirmed)                            │
├─────────────────────────────────────────────────────────────┤
│  [← Prev]  Page 1 of N  [Next →]                            │
└─────────────────────────────────────────────────────────────┘
```

**Items per page:** 10 (confirmed — `BlazorAdmin/Pages/CatalogItemPage/List.razor.cs`)

### 4.2 Create/Edit Catalog Item Modal

**Trigger:** [+ Create New Item] button or ✏ Edit icon
**Confidence:** HIGH (confirmed from AA Agent analysis)

#### Form Fields

| Field | Input Type | Required | Validation |
|-------|-----------|----------|-----------|
| Name | text | Yes | Not empty |
| Description | text area | Yes | Not empty |
| Price | decimal | Yes | > 0 |
| Picture URI | text | No | URL format |
| Catalog Brand | dropdown | Yes | Select from brand list |
| Catalog Type | dropdown | Yes | Select from type list |

**On submit:**
- Create: POST /api/catalog-items → CatalogItemService.CreateAsync()
- Edit: PUT /api/catalog-items → CatalogItemService.UpdateAsync()
- After mutation: immediate cache invalidation (RefreshLocalStorageList)
- Toast notification: success or error (3s dismiss)

### 4.3 Delete Confirmation Modal

**Trigger:** 🗑 Delete icon on list row
**Confidence:** HIGH

```
┌─────────────────────────────────────────────┐
│  Delete Catalog Item                        │
│                                             │
│  Are you sure you want to delete            │
│  ".NET Bot Black Hoodie"?                   │
│                                             │
│  This action cannot be undone.              │
│                                             │
│  [Cancel]                    [Delete]       │
└─────────────────────────────────────────────┘
```

**On confirm:** DELETE /api/catalog-items/{id} → immediate cache invalidation

### 4.4 Authentication State Display

| State | UI Behavior |
|-------|------------|
| Not authenticated | Redirect to Web /Account/Login |
| Authenticated (Admin) | Show admin username + Logout |
| Session expired (60min cookie) | GET /User returns IsAuthenticated=false → clear token → redirect to login |
| Token near expiry | No auto-refresh implemented (OQ-012) |

---

## 5. User Journey Maps

### 5.1 Anonymous Customer Purchase Journey

```
[1] Browse Catalog (anonymous)
    │  Filter by brand/type
    │  View product grid
    │
    ▼
[2] Add to Basket (anonymous)
    │  Basket stored in GUID cookie
    │  Anonymous basket created in CatalogDB
    │
    ▼
[3] Login (or Register)
    │  POST /Account/Login
    │  TransferAnonymousBasketToUserAsync()
    │  ─── basket cookie deleted ───
    │  ─── basket BuyerId → username ───
    │
    ▼
[4] Review Basket
    │  Update quantities / remove items
    │
    ▼
[5] Checkout
    │  Enter shipping address ← TD-09 gap
    │  [Place Order]
    │
    ▼
[6] Order Created
    └  Basket NOT cleared (by design — BR-26)
       Redirect to order confirmation / history
```

### 5.2 Admin Catalog Management Journey

```
[1] Navigate to /BlazorAdmin
    │
    ▼
[2] CustomAuthStateProvider polls GET /User
    │  Not authenticated in BlazorAdmin →
    │  Login to Web (/Account/Login) first
    │
    ▼
[3] Authenticate via BlazorAdmin
    │  POST /api/authenticate {email, password}
    │  Returns JWT (7 days)
    │
    ▼
[4] View Catalog Item List
    │  10 items per page (cached 60s)
    │
    ▼
[5] Create / Edit / Delete item
    │  CachedCatalogItemServiceDecorator
    │  Immediate cache invalidation
    │  Toast notification (3s)
    │
    └  Every 60s: CustomAuthStateProvider re-polls /User
       If Web session expires (60min): BlazorAdmin clears token
```

---

## 6. Accessibility and UX Notes

| Category | Current State | Gap / Recommendation |
|----------|--------------|---------------------|
| ARIA labels | INFERRED present (Bootstrap 3 scaffolds) | Verify on page extraction |
| Keyboard navigation | Bootstrap 3 supports basic keyboard nav | Verify on upgrade |
| Screen reader support | Not explicitly configured | Add aria-label to icon-only buttons (✏🗑) |
| Error messages | Model validation messages (Web); toast (Admin) | Ensure error messages are not technical |
| Loading states | Not confirmed | Add loading spinner for BlazorAdmin HTTP calls |
| Empty states | Not confirmed | Define empty basket message; empty order history message |
| Mobile responsiveness | Bootstrap 3 responsive grid | Verify breakpoints on catalog grid |
| Form validation feedback | jquery-validation (Web); FluentValidation (API) | Web: client-side inline errors; Admin: toast on fail |

---

## 7. Generation Instructions for UI

| Page | Instruction | Blocker |
|------|------------|---------|
| Catalog browse | Generate Razor Page with Brand/Type filter dropdowns and paginated grid | MIS-004 — INFERRED template |
| Basket | Generate Razor Page with item list, quantity update form, checkout button | MIS-004 — INFERRED template |
| Checkout | Generate Razor Page with order summary + shipping address form | MIS-007 — form fields REQUIRED |
| Login | Generate from confirmed Login.cshtml.cs; include basket transfer logic | None |
| Register | Generate from confirmed Register.cshtml.cs; wire to real email sender | MIS-006 — email stub |
| Order history | Generate Razor Page using GetMyOrdersHandler | MIS-004 — INFERRED template |
| BlazorAdmin List | Generate from confirmed component shape; 10 items/page | None |
| BlazorAdmin Create/Edit | Generate form with confirmed fields + Brand/Type dropdowns | None |
| BlazorAdmin Delete | Generate confirmation modal | None |
| _Layout.cshtml | Generate Bootstrap 3.4.1 → 5.3 upgrade path | TD-13 |

---

## 8. UI Component Summary

| Component | Surface | Technology | Confidence | Generation Status |
|-----------|---------|-----------|-----------|------------------|
| Product grid | Web | Razor Pages + Bootstrap | INFERRED | Needs template |
| Brand/Type filter | Web | Razor Pages dropdowns | INFERRED | Needs template |
| Pagination controls | Web | Razor Pages | INFERRED | Needs template |
| Basket item list | Web | Razor Pages + form | INFERRED | Needs template |
| Checkout address form | Web | Razor Pages + form | REQUIRED | Needs design |
| Login form | Web | Razor Pages | HIGH | Ready to generate |
| Register form | Web | Razor Pages | HIGH | Ready (email stub) |
| Order history list | Web | Razor Pages | INFERRED | Needs template |
| Admin catalog list | BlazorAdmin | Blazor component | HIGH | Ready to generate |
| Admin create/edit modal | BlazorAdmin | Blazor component | HIGH | Ready to generate |
| Admin delete modal | BlazorAdmin | Blazor component | HIGH | Ready to generate |
| Toast notifications | BlazorAdmin | ToastService | HIGH | Ready to generate |
| Auth state display | BlazorAdmin | CustomAuthStateProvider | HIGH | Ready to generate |
