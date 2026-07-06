=== DOCUMENT: 04_BUSINESS_PROCESS_MODEL.md ===

# Business Process Model — eShopOnWeb

---

## BPM-001: Customer Purchase Journey (End-to-End Value Stream)

**Trigger:** Visitor arrives at storefront
**Termination:** Order placed OR customer abandons

```
[Anonymous Visitor]                [System]                    [Registered Customer]
       │                              │                                │
       ▼                              │                                │
  Browse Catalog ─────── CachedCatalogViewModelService ───────────────┤
  (30s server cache)                  │                                │
       │                              │                                │
       ▼                              │                                │
  Add to Anonymous Basket ─── BasketService.AddItemToBasket() ────────┤
  (BASKET_COOKIENAME cookie)          │                                │
       │                              │                                │
       ▼                              │                                │
  [Decide to Purchase?] ──No──► [Abandon]                             │
       │                              │                                │
      Yes                             │                                │
       │                              │                                │
       ▼                              │                                │
  Login / Register ────── SignInManager.PasswordSignInAsync() ────────►
       │                              │                                │
       │                   TransferAnonymousBasketToUserAsync()        │
       │                   (3 SaveChanges — non-atomic DQ-002)         │
       │                              │                                │
       │                              │◄───────────────────────────────┤
       │                              │                                │
       │                              │                           Checkout Form
       │                              │                           [ASSUMED — TD-09]
       │                              │                                │
       │                    OrderService.CreateOrderAsync()            │
       │                    ├── Guard.Against.EmptyBasket              │
       │                    ├── Read IRepository<CatalogItem>          │
       │                    ├── Build CatalogItemOrdered snapshots      │
       │                    ├── Freeze prices from BasketItem.UnitPrice│
       │                    └── Save Order to CatalogDB                │
       │                              │                                │
       │                              │                           Order Saved ✓
       │                              │                                │
       │                    Basket NOT cleared (BR-26)                 │
       │                              │                                │
       └──────────────────────────────┴────────────────────────────────┘
```

**Wait States:**
- Post-checkout basket: no trigger for basket clearing; customer must manually clear or basket persists (ASMP-001)

---

## BPM-002: Product Catalog Administration

**Trigger:** Administrator opens BlazorAdmin portal
**Termination:** Product created / updated / deleted OR operation rejected

```
[Administrator]              [BlazorAdmin]              [PublicApi]           [CatalogDB]
      │                           │                          │                     │
      ▼                           │                          │                     │
  Open Admin Portal               │                          │                     │
      │                           │                          │                     │
      ▼                           │                          │                     │
  Authenticate ──────POST /api/authenticate──────────────────►                    │
      │                           ◄── JWT Token (7 days) ────┤                     │
      │                           │                          │                     │
      ▼                           │                          │                     │
  View Product List ────── GET /api/catalog-items ───────────►──── SELECT ──────► │
      │                    [1-second artificial delay TD-07]  │◄── Results ────────│
      │                    [LocalStorage cache 60s AP-08]     │                     │
      │                           │                          │                     │
  Select Action                   │                          │                     │
      │                           │                          │                     │
  ┌──┼──────────────────────────┐ │                          │                     │
  │  ▼                          │ │                          │                     │
  │ CREATE ──────────────────── POST /api/catalog-items ──── ►── INSERT ─────────► │
  │ UPDATE ──────────────────── PUT /api/catalog-items ───── ►── UPDATE ─────────► │
  │ DELETE ──────────────────── DELETE /api/catalog-items/{id}►── DELETE ─────────► │
  └──────────────────────────── │ │                          │◄── Confirm ──────── │
                                 │ │                          │                     │
      │                    Cache Invalidated + Refreshed      │                     │
      │                    (BR-43: immediate on mutation)      │                     │
      │                           │                          │                     │
      ▼                           │                          │                     │
  Toast Notification (3s)         │                          │                     │
```

**Auth Gate:** Every mutation requires JWT Bearer with `Administrators` role claim. All read operations are anonymous-accessible.

---

## BPM-003: Anonymous Basket Transfer on Login

**Trigger:** Customer submits login form with valid credentials
**Termination:** Baskets merged OR no anonymous basket (no-op)

```
Step 1: Read BASKET_COOKIENAME cookie
        └── If absent → END (no-op, BR-19)

Step 2: Look up anonymous basket by BuyerId = cookie value
        └── If not found → END (no-op)

Step 3: Retrieve or create authenticated basket for userName
        └── SaveChanges #1 (if new basket created)

Step 4: For each item in anonymous basket:
        ├── If authenticated basket already has same CatalogItemId:
        │   └── Basket.AddItem() → BasketItem.AddQuantity() (quantities combined, BR-17)
        └── Else: new BasketItem added to authenticated basket
        └── SaveChanges #2

Step 5: Delete anonymous basket
        └── SaveChanges #3

Step 6: Delete BASKET_COOKIENAME cookie from browser (BR-18, BR-46)
```

**Risk (DQ-002):** Steps 3-5 each commit independently. A failure between steps leaves orphaned data. No compensating transaction or saga exists.

---

## BPM-004: Customer Registration

**Trigger:** Visitor submits registration form
**Termination:** Account created (unconfirmed) OR duplicate email error

```
Step 1: Visitor submits {email, password}

Step 2: System → UserManager.CreateAsync(ApplicationUser, password)
        ├── Email already exists → return error to form
        └── Success → account created in IdentityDB (AspNetUsers)

Step 3: System → GenerateEmailConfirmationTokenAsync()
        └── Token generated (but delivery will fail)

Step 4: System → EmailSender.SendEmailAsync(email, subject, body)
        └── ⚠️ STUB: returns Task.CompletedTask immediately
        └── No email sent — confirmation permanently blocked (BR-34, TD-08)

Step 5: Account remains in IsEmailConfirmed=false state
        └── Depending on Identity config, login may or may not be permitted
```

**Gap:** Steps 4-5 are permanently non-functional. Account exists but confirmation is impossible without implementing real EmailSender.

---

## BPM-005: Database Initialization on Application Startup

**Trigger:** Application process starts (Web or PublicApi)
**Termination:** All migrations applied; seed data present

```
Step 1: CatalogContextSeed.SeedAsync()
        ├── If SQL Server: context.Database.Migrate() with retry (up to 10 attempts, BR-39)
        ├── If no CatalogBrands: INSERT seed brands (idempotent, BR-37)
        ├── If no CatalogTypes: INSERT seed types
        └── If no CatalogItems: INSERT seed products

Step 2: AppIdentityDbContextSeed.SeedAsync()
        ├── context.Database.Migrate() (Identity migrations auto-applied)
        ├── If 'Administrators' role missing: CreateAsync role
        ├── If 'demouser@microsoft.com' missing: CreateAsync user (password=DEFAULT_PASSWORD=Pass@word1 — CRITICAL BR-33)
        └── If 'admin@microsoft.com' missing: CreateAsync + assign Administrators role

RETRY POLICY: Up to 10 attempts on transient SQL errors (BR-39)
IDEMPOTENCY: Seed operations check existence before inserting (BR-37)
```

**Critical Risk:** Step 2 always creates admin@microsoft.com with the publicly known password "Pass@word1" on any fresh SQL Server database. Applies to every production deployment.

---

## Process Risk Summary

| Process | Risk | Severity |
|---------|------|----------|
| BPM-001 Order Placement | No order status; no post-order workflow | HIGH |
| BPM-001 Order Placement | Basket not cleared after order (BR-26) | MEDIUM |
| BPM-001 Order Placement | Checkout address hardcoded (TD-09) | HIGH |
| BPM-002 Catalog Admin | 1-second delay on every catalog list load (TD-07) | HIGH |
| BPM-003 Basket Transfer | Non-atomic 3-step transaction (DQ-002) | MEDIUM |
| BPM-004 Registration | Email confirmation permanently non-functional (TD-08) | HIGH |
| BPM-005 Startup | Seeded admin account with known password (BR-33) | CRITICAL |
