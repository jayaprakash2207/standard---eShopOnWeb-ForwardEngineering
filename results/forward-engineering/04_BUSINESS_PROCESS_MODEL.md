# Business Process Model — eShopOnWeb

**Date:** 2026-07-06

---

## BPMN Notation Key

```
[Actor] → (Action) → <Decision> → |Event| → [[System State]]
```

---

## Process 1: Customer Shopping Journey (End-to-End)

**ID:** PROC-001
**Trigger:** Visitor arrives at storefront
**Terminal Outcomes:** Order placed | Visitor exits without purchase

```
START
  │
  ▼
[Anonymous Shopper] → (Browse catalog) → [[Product list displayed]]
  │
  ▼
<Filter by brand/type?>
  │ YES → CatalogFilterSpecification → [[Filtered results]]
  │ NO  → CatalogFilterPaginatedSpecification(pageIndex, pageSize=10)
  │
  ▼
[Anonymous Shopper] → (Select product) → GET /api/catalog-items/{id}
  │
  ▼
[Anonymous Shopper] → (Add to basket) → BasketService.AddItemToBasket
                                       → [[BasketItem.UnitPrice LOCKED]]
  │
  ▼
<More items?>
  │ YES → loop to Browse
  │ NO  ↓
  │
  ▼
<Authenticated?>
  │ NO → [Anonymous Shopper] → (Login) → SignInManager.PasswordSignInAsync
  │                           → BasketService.TransferBasketAsync
  │                           → [[Anonymous basket MERGED + DELETED]]
  │ YES ↓
  │
  ▼
[Registered Customer] → (Review basket) → BasketService.SetQuantities
  │                    → Basket.RemoveEmptyItems
  │
  ▼
[Registered Customer] → (Submit checkout + shipping address)
  │
  ▼
<Basket empty?>
  │ YES → Guard.Against.EmptyBasketOnCheckout → ERROR → loop to Review
  │ NO  ↓
  │
  ▼
OrderService.CreateOrderAsync(basketId, shippingAddress)
  → Load basket; Guard.Against.Null
  → For each BasketItem: load CatalogItem → build CatalogItemOrdered snapshot
  → Create Order + OrderItems (price = BasketItem.UnitPrice)
  → Persist Order to CatalogDb
  │
  ▼
[Web Layer — ASMP-002] → (Delete basket)
  │
  ▼
[[MISSING: Payment processing]]
  │
  ▼
[[MISSING: Order confirmation email]]
  │
  ▼
|Order Created| → END
```

**Handoff Points:**
- Login page → BasketService.TransferBasketAsync (cross-domain: Identity → Basket)
- OrderService.CreateOrderAsync → Web layer basket deletion (not atomic)
- OrderService → Payment provider (NOT IMPLEMENTED)

**States Defined:**

| State | Trigger | Duration |
|-------|---------|---------|
| No basket | Pre-first add | Indefinite |
| Anonymous basket | AddItemToBasket | Until login |
| Account basket | TransferBasketAsync | Until checkout |
| Order created | CreateOrderAsync | Permanent record |
| Basket cleared | Web layer post-checkout | Immediate |

**Missing States:** Payment pending, Payment confirmed, Order confirmed, Packed, Dispatched, Delivered, Cancelled

---

## Process 2: Product Catalog Management

**ID:** PROC-002
**Trigger:** Administrator needs to add/update/remove product
**Terminal Outcomes:** Catalog updated and visible | Validation rejection

```
START
  │
  ▼
[Admin] → (Navigate to BlazorAdmin) → GET /User (OQ-003)
                                     → [[UserInfo loaded; JWT attached to HttpClient]]
  │
  ▼
[Admin] → (View catalog) → CatalogItemService.List() or ListPaged()
                         → [[Cache check: Blazored.LocalStorage 1-min TTL]]
  │
  ▼
<Action?>
  ├─── CREATE ──────────────────────────────────────────────────────┐
  │    [Admin] → (Fill form) → (Submit)                             │
  │    → POST /api/catalog-items (Bearer token)                     │
  │    → [PublicApi] validate JWT + ADMINISTRATORS role             │
  │    → FluentValidation: name required, description required,     │
  │      price 0.01–1000, image 512KB/.jpg/.png/.gif                │
  │    → CatalogItemNameSpecification: check uniqueness             │
  │    → <Duplicate name?> YES → 409 Conflict → END with error      │
  │    → Create CatalogItem → Persist → Return DTO                  │
  │    → BlazorAdmin invalidates LocalStorage cache                  │
  │    → [[Product visible in catalog]]                             │
  │                                                                  │
  ├─── UPDATE ──────────────────────────────────────────────────────┤
  │    Same validation flow; PUT /api/catalog-items                  │
  │    → UpdateDetails / UpdateBrand / UpdateType / UpdatePictureUri │
  │                                                                  │
  └─── DELETE ──────────────────────────────────────────────────────┘
       DELETE /api/catalog-items/{id}
       → Product removed from Catalog table
       → BlazorAdmin invalidates LocalStorage cache
       → [[Product no longer visible]]
```

---

## Process 3: User Login with Basket Merge

**ID:** PROC-003
**Trigger:** Anonymous shopper initiates login

```
START
  │
  ▼
[Anonymous Shopper] → (Submit email + password to Login.cshtml.cs)
  │
  ▼
SignInManager.PasswordSignInAsync(email, password, lockoutOnFailure:true)
  │
  ▼
<Result?>
  ├─ IsLockedOut → ERROR: account locked
  ├─ IsNotAllowed → ERROR: account not allowed
  ├─ RequiresTwoFactor → [STUB — no 2FA flow implemented]
  └─ Succeeded ↓
  │
  ▼
Login.cshtml.cs.TransferAnonymousBasketToUserAsync()
  → BasketService.TransferBasketAsync(anonymousCookieGuid, authenticatedUsername)
  → Load anonymous basket; load user basket (or create)
  → Copy all anonymous basket items to user basket
  → Delete anonymous basket
  │
  ▼
[[Cookie session established; anonymous basket merged]]
  │
  ▼
Redirect to ReturnUrl → END
```

---

## Process 4: New User Registration

**ID:** PROC-004

```
START
  │
  ▼
[New Visitor] → (Submit email + password to Register.cshtml.cs)
  │
  ▼
UserManager.CreateAsync(new ApplicationUser{UserName=email, Email=email}, password)
  │
  ▼
<Email unique?>
  │ NO → Identity error → return form with error message
  │ YES ↓
  │
  ▼
[STUB] EmailSender.SendEmailAsync → Task.CompletedTask
      (No email delivered — ASMP-006 / PP-05)
  │
  ▼
SignInManager.SignInAsync → [[Cookie session established immediately]]
  │
  ▼
Redirect to home → END
```

**Gap:** Email confirmation not enforced — unverified email addresses accepted