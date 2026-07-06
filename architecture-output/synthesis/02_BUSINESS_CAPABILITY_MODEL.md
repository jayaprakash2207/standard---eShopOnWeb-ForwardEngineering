=== DOCUMENT: 02_BUSINESS_CAPABILITY_MODEL.md ===

# Business Capability Model — eShopOnWeb

---

## Capability Map (Level 0 → Level 2)

```
eShopOnWeb
├── 1. CATALOG MANAGEMENT
│   ├── 1.1 Product Catalog Maintenance
│   │   ├── 1.1.1 Create Product
│   │   ├── 1.1.2 Update Product (details, price, image, brand, type)
│   │   └── 1.1.3 Delete Product
│   ├── 1.2 Catalog Browsing
│   │   ├── 1.2.1 Paginated Product Listing
│   │   ├── 1.2.2 Filter by Brand and Type
│   │   └── 1.2.3 Product Detail View
│   └── 1.3 Reference Data Management
│       ├── 1.3.1 Brand Management
│       └── 1.3.2 Type Management
│
├── 2. CUSTOMER ENGAGEMENT
│   ├── 2.1 Shopping Basket
│   │   ├── 2.1.1 Add Item to Basket
│   │   ├── 2.1.2 Update Basket Quantities
│   │   ├── 2.1.3 Remove Items from Basket
│   │   └── 2.1.4 View Basket Summary
│   ├── 2.2 Anonymous Shopping
│   │   ├── 2.2.1 Anonymous Basket Creation (cookie-based)
│   │   └── 2.2.2 Anonymous-to-Authenticated Basket Transfer
│   └── 2.3 Checkout & Order Placement
│       ├── 2.3.1 Shipping Address Entry  ← MISSING (TD-09)
│       ├── 2.3.2 Order Validation
│       ├── 2.3.3 Order Creation with Price Snapshot
│       └── 2.3.4 Order History View
│
├── 3. IDENTITY & ACCESS
│   ├── 3.1 Customer Account Management
│   │   ├── 3.1.1 Customer Registration
│   │   ├── 3.1.2 Email Confirmation  ← BROKEN (TD-08 stub)
│   │   ├── 3.1.3 Login (Cookie Session)
│   │   └── 3.1.4 Logout
│   ├── 3.2 API Authentication
│   │   ├── 3.2.1 JWT Token Issuance
│   │   └── 3.2.2 Token Revocation (server-side cache)
│   └── 3.3 Access Control
│       ├── 3.3.1 Role Assignment (Administrators)
│       └── 3.3.2 RBAC Enforcement on Catalog Mutations
│
└── 4. PLATFORM OPERATIONS
    ├── 4.1 Data Initialization
    │   ├── 4.1.1 Catalog Seed Data
    │   └── 4.1.2 Identity Seed Data (users + roles)
    ├── 4.2 Observability
    │   ├── 4.2.1 Console Logging  ← plain text, no correlation IDs
    ├── 4.3 Health Monitoring
    │   └── 4.3.1 Health Endpoint (content-based, Web only)
    └── 4.4 Admin Portal
        ├── 4.4.1 Catalog Admin UI (Blazor WASM)
        └── 4.4.2 Admin Session Management
```

---

## Capability Details

### 1.1 Product Catalog Maintenance

| Attribute | Value |
|-----------|-------|
| Owner | Catalog Administrator |
| System Support | PublicApi REST + BlazorAdmin SPA |
| Auth Required | JWT — Administrators role |
| Maturity | Full (all CRUD operations implemented and tested) |
| Risks | Single admin role — no granular permissions |

**Sub-capabilities:**

| Sub-Capability | API | Auth | Business Rule |
|----------------|-----|------|---------------|
| Create Product | POST /api/catalog-items | Administrators | BR-01 to BR-09 |
| Update Product | PUT /api/catalog-items | Administrators | BR-01 to BR-09 |
| Delete Product | DELETE /api/catalog-items/{id} | Administrators | BR-07 |

### 1.2 Catalog Browsing

| Attribute | Value |
|-----------|-------|
| Owner | All users (including anonymous) |
| System Support | Web MVC (via CachedCatalogViewModelService) + PublicApi GET endpoints |
| Auth Required | None |
| Maturity | API confirmed; Web browse pages ASSUMED (source not extracted) |
| NFRs | Server-side cache: 30s; API list includes 1s artificial delay (TD-07 — remove) |

### 2.1 Shopping Basket

| Attribute | Value |
|-----------|-------|
| Owner | Any user (anonymous or authenticated) |
| System Support | BasketService (ApplicationCore) + Web MVC basket pages (ASSUMED) |
| Auth Required | None for anonymous; Cookie session for authenticated |
| Maturity | Domain service fully confirmed; Web pages ASSUMED |
| Key Behavior | Auto-create on first add; merge duplicates; remove zero-qty items |

### 2.2 Anonymous Shopping

| Attribute | Value |
|-----------|-------|
| Owner | System (automatic) |
| System Support | BasketService.TransferBasketAsync; Login.cshtml.cs |
| Auth Required | N/A — triggered by successful login |
| Maturity | Full (transfer flow confirmed end-to-end) |
| Key Behavior | 3 separate SaveChanges calls — non-atomic (DQ-002) |

### 2.3 Checkout & Order Placement

| Attribute | Value |
|-----------|-------|
| Owner | Registered Customer + System |
| System Support | OrderService.CreateOrderAsync; Web checkout page |
| Auth Required | Cookie session ([Authorize]) |
| Maturity | Domain service confirmed; Web checkout page partially confirmed (hardcoded address TD-09) |
| Key Behavior | Price snapshot from basket; product name/image snapshot; basket NOT cleared |
| Critical Gap | Shipping address form not implemented (TD-09); no order status field |

### 3.1 Customer Account Management

| Attribute | Value |
|-----------|-------|
| Owner | Prospective Customer + System |
| System Support | ASP.NET Core Identity; Web Register/Login/ConfirmEmail pages |
| Auth Required | None for registration; credentials for login |
| Maturity | Registration + Login confirmed; Email confirmation BROKEN (EmailSender stub) |
| Critical Gap | EmailSender.SendEmailAsync is a no-op — confirmation permanently blocked |

### 3.2 API Authentication

| Attribute | Value |
|-----------|-------|
| Owner | Administrator (primary consumer via BlazorAdmin) |
| System Support | IdentityTokenClaimService; AuthenticateEndpoint |
| Auth Required | Valid credentials (with lockout on failure) |
| Maturity | Full (confirmed with lockout, 7-day token, role claims) |
| Critical Risk | JWT_SECRET_KEY hardcoded (TD-01); issuer/audience not validated (TD-03) |

---

## Capability Maturity Assessment

| Capability | Maturity Level | Notes |
|------------|----------------|-------|
| 1.1 Product Catalog Maintenance | **5/5 — Full** | Complete CRUD, validation, role gate |
| 1.2 Catalog Browsing | **4/5 — Partial** | API confirmed; Web pages assumed |
| 1.3 Reference Data Management | **5/5 — Full** | Brand/type list confirmed |
| 2.1 Shopping Basket | **4/5 — Partial** | Domain layer full; Web UI assumed |
| 2.2 Anonymous Shopping | **5/5 — Full** | Transfer flow confirmed |
| 2.3 Checkout & Order Placement | **3/5 — Partial** | Core logic confirmed; address form missing |
| 3.1 Customer Account Management | **3/5 — Partial** | Registration works; confirmation broken |
| 3.2 API Authentication | **4/5 — Partial** | Works; hardcoded key is critical debt |
| 3.3 Access Control | **4/5 — Partial** | Single-role RBAC; no granular permissions |
| 4.1 Data Initialization | **5/5 — Full** | Seeding with retry confirmed |
| 4.2 Observability | **2/5 — Minimal** | Plain console log; no tracing/metrics |
| 4.3 Health Monitoring | **3/5 — Partial** | Web only; content-based checks |
| 4.4 Admin Portal | **5/5 — Full** | Full Blazor WASM admin confirmed |

---

## Capability Gap Heat Map

| Capability | Current State | Target State | Gap |
|------------|--------------|-------------|-----|
| Order Status/Fulfilment | Not implemented | Confirmed → Processing → Shipped → Delivered | **HIGH** |
| Email Notifications | Stub (no-op) | Transactional email (registration, order confirm, shipping) | **HIGH** |
| Payment Processing | Not implemented | Capture payment before order creation | **HIGH** |
| Shipping Address Collection | Hardcoded | Customer-supplied address form at checkout | **HIGH** |
| Buyer Profile Persistence | Dead code | Saved payment methods, purchase history | **MEDIUM** |
| Observability | Console log only | Structured logs + distributed traces + metrics | **MEDIUM** |
| Security Posture | Hardcoded keys | Externalized secrets, issuer validation | **CRITICAL** |
