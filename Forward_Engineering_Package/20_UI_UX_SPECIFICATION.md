# 20 — UI/UX Specification

> **Single source of truth:** `ENTERPRISE_KNOWLEDGE_GRAPH.json`. Every page, flow, actor, capability, and field below is traced to graph node ids. No screen, field, or interaction has been invented beyond what the evidence supports.
>
> **Confidence posture:** The legacy system is server-rendered Razor Pages + a Blazor WASM admin SPA. No design system, wireframes, or UX assets exist in the evidence. This document derives UI/UX requirements **strictly from business capabilities (BIZ-CAP)**, **processes (BIZ-PROC)**, **actors (BIZ-ACT)**, **API surfaces (APP-API)**, and **business rules (BR001–BR012)**. Where a UI detail is not in evidence it is marked ⚠ DERIVED or 🟦 REQUIRES HUMAN DECISION.
>
> **Status flags honored:** BC-06 Buyer/Customer Profile is aspirational (RC-002); no payment/buyer UI is specified. Payment capabilities BIZ-CAP-027/028 are INFERRED/LOW; excluded.

---

## 1. Purpose

This document specifies the UI/UX requirements — page inventory, user flows, field-level requirements, validation behavior, error states, authorization guards, and accessibility baseline — that an AI generator or development team must honor when building the frontend.

---

## 2. Actors & their primary surfaces

| Actor | Node | Primary surfaces |
|---|---|---|
| Anonymous Shopper | BIZ-ACT-002 | Catalog browse, Basket (read/add), Login/Register |
| Customer / Buyer | BIZ-ACT-001 | All anonymous surfaces + Checkout, Order history, Account/profile management |
| Administrator | BIZ-ACT-003 | Admin SPA (catalog CRUD), Admin Razor Pages |
| System / Service Account | BIZ-ACT-004 | No UI (seeding only — BIZ-PROC-009/010) |

---

## 3. Page Inventory & Requirements

### 3.1 Catalog Browse — `/` (APP-API-046)

**Capability:** BIZ-CAP-001 Browse Catalog, BIZ-CAP-002 Filter by Brand, BIZ-CAP-003 Filter by Type, BIZ-CAP-005 Page Results
**Actor:** BIZ-ACT-001, BIZ-ACT-002 (anonymous)
**Process:** BIZ-PROC-001

| Requirement | Detail | Source |
|---|---|---|
| Display product list | CatalogItem: Name, Price, PictureUri | DATA-ENT-001 |
| Filter by Brand | Dropdown bound to CatalogBrand list (APP-API-002) | BIZ-CAP-002, DATA-ENT-002 |
| Filter by Type | Dropdown bound to CatalogType list (APP-API-008) | BIZ-CAP-003, DATA-ENT-003 |
| Pagination | pageIndex / pageSize controls; display total count | API-06, APP-API-004 |
| Add to Basket button | Per item; triggers add-to-basket flow (§3.3) | BIZ-CAP-012 |
| No price currency symbol | Amount-only display (VO-05 — no currency in evidence) | ASMP-FE-001 |
| No stock level display | AvailableStock **DISC-001** — absent from real source; **do not display** | DISC-001 |

### 3.2 Catalog Item Detail — (no dedicated route in evidence)

> No dedicated item-detail page is evidenced in the 55 APIs. `APP-API-003 GET /api/catalog-items/{id}` is a PublicApi endpoint; there is no corresponding Razor Page route. 🟦 A detail page is a **human decision** if desired.

### 3.3 Basket — `/{handler?}` (APP-API-051)

**Capability:** BIZ-CAP-010 View Basket, BIZ-CAP-012 Add Item to Basket, BIZ-CAP-013 Remove Item, BIZ-CAP-014 Update Quantity
**Actor:** BIZ-ACT-001, BIZ-ACT-002
**Process:** BIZ-PROC-002, BIZ-PROC-004

| Requirement | Detail | Source |
|---|---|---|
| Display basket lines | Item name, unit price, quantity, line total | DATA-ENT-004/005, VO-02 |
| Add item | From catalog page; consolidates quantity if item already in basket | BR005 |
| Update quantity | Inline quantity control; 0 removes line | BR006 |
| Reject negative quantity | Show validation error | BR007 |
| Display basket total | Derived `Σ(UnitPrice × Quantity)` — no stored total | BR010 |
| Anonymous basket | Keyed by session/cookie; no login required | BIZ-ACT-002, ASMP-FE-005 |
| Anonymous-to-registered transfer | On login, merge anonymous basket into user basket | BIZ-PROC-003 / EVT-03 |
| Proceed to Checkout button | Links to `/Basket/Checkout`; requires authenticated user | APP-API-050 |

### 3.4 Checkout — `/Basket/Checkout` (APP-API-050)

**Capability:** BIZ-CAP-019 Initiate Checkout, BIZ-CAP-020 Block Empty Basket, BIZ-CAP-021 Place Order
**Actor:** BIZ-ACT-001 (authenticated)
**Process:** BIZ-PROC-005

| Requirement | Detail | Source |
|---|---|---|
| Require authentication | Redirect to login if anonymous | BR011, SR-02 |
| Block empty basket | Show error message; prevent submission | BR012 / EVT-06 |
| Shipping address form | Street (required), City (required), State (optional), Country (required), ZipCode (required) | DATA-ENT-013 Address VO-01 (PII) |
| Order summary | List basket items with snapshot name/price/qty; derived total | VO-03, BR010 |
| Submit order | POST checkout; handle success → `/Basket/Success` (APP-API-052) | BIZ-PROC-005 |
| Error states | Empty basket (409), missing address (400), unauthenticated (401) | API-04 |
| No payment fields | BC-06 aspirational; **no card/payment UI** | RC-002, SR-09 |

### 3.5 Order Success — `/Basket/Success` (APP-API-052)

| Requirement | Detail | Source |
|---|---|---|
| Confirmation message | Order placed successfully | BIZ-CAP-021 |
| Link to order history | → `/Order/MyOrders` | APP-API-035 |

### 3.6 Order History — `/Order/MyOrders` (APP-API-035)

**Capability:** BIZ-CAP-022 View Order History
**Actor:** BIZ-ACT-001 (authenticated, own orders only)

| Requirement | Detail | Source |
|---|---|---|
| Require authentication | Redirect to login if anonymous | SR-02, BR011 |
| List orders | OrderDate, total (derived), item count | DATA-ENT-006 |
| Row-level ownership | Only show orders where `Order.BuyerId == token.sub` | DATA-REL-009 |
| Link to order detail | → `/Order/Detail/{orderId}` | APP-API-036 |

### 3.7 Order Detail — `/Order/Detail/{orderId}` (APP-API-036)

| Requirement | Detail | Source |
|---|---|---|
| Display order lines | Snapshot: product name, picture, unit price, units | DATA-ENT-007, VO-03 |
| Display shipping address | Street, City, State, Country, ZipCode (PII) | DATA-ENT-013 |
| Row-level ownership | Return 403/404 if `Order.BuyerId ≠ token.sub` | DATA-REL-009, SR-02 |
| No live catalog link | Ordered snapshot is historical; do not link to current CatalogItem | DR-06 |

### 3.8 Login — `/Account/Login` (APP-API-042)

**Capability:** BIZ-CAP-031 User Login
**Process:** BIZ-PROC-007

| Requirement | Detail | Source |
|---|---|---|
| Email + Password fields | Standard credential form | DATA-ENT-008 |
| Submit → JWT issuance | POST /api/authenticate (APP-API-001) → JWT | BIZ-PROC-007, EVT-07 |
| Lockout handling | Show lockout message; `AccessFailedCount` + `LockoutEnabled` | DATA-ENT-008 |
| Redirect after login | Return to previous page or catalog | BIZ-PROC-007 |
| Anonymous basket merge | Trigger BIZ-PROC-003 on successful login | EVT-03 |

### 3.9 Register — `/Account/Register` (APP-API-044)

**Capability:** BIZ-CAP-030 User Registration

| Requirement | Detail | Source |
|---|---|---|
| Email + Password + Confirm fields | Standard registration form | DATA-ENT-008 |
| Email confirmation flow | Trigger ConfirmEmail (APP-API-041) | BIZ-PROC-007 |
| Redirect to login or home | Post-registration | BIZ-CAP-030 |

### 3.10 Account Management — `/Manage/*` (APP-API-014..034)

**Capability:** BIZ-CAP-029 Identity & Authentication management
**Actor:** BIZ-ACT-001 (authenticated, own account only)

Sub-pages covered by ManageController (APP-SVC-037) — 21 routes:

| Sub-area | Routes | Fields |
|---|---|---|
| My Account / Profile | `/Manage` | UserName, Email, PhoneNumber (PII) |
| Change Password | `/Manage/ChangePassword` | Current + New password |
| Set Password (external login) | `/Manage/SetPassword` | New password |
| Two-Factor Auth (2FA) | `/Manage/TwoFactorAuthentication`, `/Manage/EnableAuthenticator`, `/Manage/ResetAuthenticator`, `/Manage/GenerateRecoveryCodes`, `/Manage/ShowRecoveryCodes` | TOTP setup; `TwoFactorEnabled` flag |
| External logins | `/Manage/ExternalLogins` | OAuth provider management |

> All `/Manage/*` routes require authenticated user; enforce row-level ownership (`token.sub` = user being managed).

### 3.11 Logout — `/Account/Logout` (APP-API-043) + `/User/Logout` (APP-API-038)

| Requirement | Detail |
|---|---|
| Clear session / token | SignInManager.SignOutAsync |
| Redirect to catalog | BIZ-CAP-031 |

---

## 4. Admin SPA Pages (BC-05 — BlazorAdmin)

### 4.1 Catalog Item List — `/admin` (APP-API-040)

**Capability:** BIZ-CAP-035 View Catalog Admin, BIZ-CAP-037 List Items, BIZ-CAP-039 Cache Refresh
**Actor:** BIZ-ACT-003 (Administrators)

| Requirement | Detail | Source |
|---|---|---|
| Require Administrators role | Redirect/401 if not admin | SR-02 / §13.11 |
| Display item list | Name, Price, Brand, Type, PictureUri | DATA-ENT-001 via APP-API-004 |
| Filter by Brand / Type | Dropdowns bound to APP-API-002 / APP-API-008 | BIZ-CAP-002/003 |
| Pagination | pageIndex / pageSize | API-06 |
| Create item button | Opens create form (§4.2) | BIZ-CAP-038 |
| Delete item | Per-row delete; confirm dialog; calls APP-API-006 | BIZ-CAP-038 / EVT-09 |
| Cache refresh | Trigger refresh after create/delete; toast notification | APP-SVC-049 / EVT-10 / APP-SVC-048 |
| No stock columns | DISC-001 — do not display AvailableStock / RestockThreshold / MaxStockThreshold / OnReorder | DISC-001 |

### 4.2 Create / Edit Catalog Item — `/Admin/EditCatalogItem` (APP-API-048) + Admin SPA create form

**Capability:** BIZ-CAP-038 Manage Catalog Items
**Process:** BIZ-PROC-006

| Field | Type | Validation | Source |
|---|---|---|---|
| Name | Text (required) | BR001 — name required | DATA-ENT-001 |
| Description | Textarea (required) | BR001 — description required | DATA-ENT-001 |
| Price | Decimal (required, ≥ 0) | BR001 — price valid | DATA-ENT-001, VO-05 |
| PictureUri / Picture | File upload or URL | BR004 — image path generated | DATA-ENT-001 |
| CatalogBrand | Dropdown (required, ≠ 0) | BR002 | DATA-REL-001, DATA-ENT-002 |
| CatalogType | Dropdown (required, ≠ 0) | BR003 | DATA-REL-002, DATA-ENT-003 |

> **No stock fields (AvailableStock / RestockThreshold / MaxStockThreshold / OnReorder)** — DISC-001 verified absent from real source.

### 4.3 Admin Logout — `/logout` (APP-API-039)

| Requirement | Detail |
|---|---|
| Clear WASM auth state | CustomAuthStateProvider (APP-SVC-051) |
| Redirect to login | BIZ-CAP-031 |

---

## 5. User Flows

### 5.1 Anonymous Browse & Add to Basket

```
[Anonymous] → / (catalog) → filter/page → Add to Basket
                                              ↓
                                        Basket page — line added (BR005)
                                              ↓
                                        Proceed to Checkout → /Account/Login (redirect)
```

### 5.2 Registered Checkout Flow

```
[Customer] → Login (/Account/Login) → JWT issued (BIZ-PROC-007)
                 ↓
         Anonymous basket merged (BIZ-PROC-003 / EVT-03)
                 ↓
         /Basket — review lines → Checkout (/Basket/Checkout)
                 ↓
         Enter shipping address (VO-01)
                 ↓
         Submit → Order created (BIZ-PROC-005 / EVT-04)
                 ↓
         /Basket/Success → link to /Order/MyOrders
```

### 5.3 Admin Catalog Management Flow

```
[Administrator] → /admin (BlazorAdmin, Administrators role required)
                     ↓
               Catalog list (APP-API-004, cached via APP-SVC-044)
                     ↓
        ┌── Create item → form (BR001-004) → POST APP-API-005 → EVT-08
        │                                         ↓
        │                                  Cache refresh (EVT-10) → toast
        │
        └── Delete item → confirm → DELETE APP-API-006 → EVT-09
                                         ↓
                                  Cache refresh (EVT-10) → toast
```

### 5.4 Account / 2FA Management

```
[Customer] → /Manage (account home)
                ↓
    ┌── Change password → /Manage/ChangePassword
    ├── Enable 2FA → /Manage/TwoFactorAuthentication → /Manage/EnableAuthenticator (TOTP)
    ├── Generate recovery codes → /Manage/GenerateRecoveryCodes
    └── External logins → /Manage/ExternalLogins
```

---

## 6. Validation & Error Behavior

All validation follows doc 15 API-04 and API-05 (enforce at edge, surface via problem-detail). UI must reflect these states:

| Error | HTTP status | UI behavior |
|---|---|---|
| Missing required field | 400 | Inline field error |
| Unauthenticated | 401 | Redirect to `/Account/Login` |
| Unauthorized (not Administrators) | 403 | Show permission-denied message |
| Resource not found | 404 | Not-found page / inline message |
| Empty basket checkout | 409 | Inline basket error — "Basket is empty" (BR012) |
| Business-rule violation (BR001-BR012) | 422 | Inline field/form error with message |
| Server error | 500 | Generic error page (no stack trace) |

---

## 7. Accessibility Baseline (Derived — ⚠ not in legacy evidence)

| Requirement | Target | Note |
|---|---|---|
| WCAG compliance | WCAG 2.1 AA | ⚠ DERIVED — no legacy evidence |
| Keyboard navigation | All interactive elements reachable via keyboard | ⚠ DERIVED |
| Screen reader support | Semantic HTML; ARIA labels on icon buttons | ⚠ DERIVED |
| Color contrast | ≥ 4.5:1 for normal text | WCAG 2.1 AA |
| Form labels | Every form field has an associated `<label>` | ⚠ DERIVED |

> 🟦 Accessibility level is a **human decision** — WCAG 2.1 AA is a neutral industry standard, not derived from evidence.

---

## 8. Responsive Design (Derived — ⚠ not in legacy evidence)

| Breakpoint | Target | Note |
|---|---|---|
| Mobile | ≥ 320px | ⚠ DERIVED |
| Tablet | ≥ 768px | ⚠ DERIVED |
| Desktop | ≥ 1200px | ⚠ DERIVED |

> 🟦 Breakpoints are a **human decision**. No responsive design constraints exist in the legacy evidence.

---

## 9. Design System (🟦 — Not in evidence)

No design tokens, component library, color palette, typography scale, or spacing system exists in the legacy evidence. The following are **neutral defaults requiring human decision**:

| Element | Neutral default | Decision |
|---|---|---|
| Component library | None mandated (Tailwind / MUI / Ant Design / shadcn are options) | 🟦 |
| Color palette | None mandated | 🟦 |
| Typography | None mandated | 🟦 |
| Icon set | None mandated | 🟦 |
| Spacing scale | None mandated | 🟦 |

---

## 10. Internationalization & Localization (⚠ not in evidence)

No i18n framework, locale, or translation evidence exists in the legacy codebase. `VO-05 Money` is amount-only (no currency symbol — ASMP-FE-001). Any localization is a **net-new decision** (🟦).

---

## 11. UI Generation Rules

| Rule | Constraint |
|---|---|
| UI-GR-01 | No stock fields (AvailableStock/RestockThreshold/MaxStockThreshold/OnReorder) on any page — DISC-001 |
| UI-GR-02 | No payment/checkout payment step — BC-06 aspirational (RC-002) |
| UI-GR-03 | All admin pages MUST enforce `Administrators` role before render (§13.11) |
| UI-GR-04 | Order/basket/account pages MUST enforce authenticated user + row-level ownership |
| UI-GR-05 | Checkout address form fields derived from Address VO-01 only — do not invent fields |
| UI-GR-06 | Price displayed as bare decimal amount (no currency symbol — ASMP-FE-001 / VO-05) |
| UI-GR-07 | Basket total is derived client-side `Σ(UnitPrice × Quantity)` — no stored total (BR010) |
| UI-GR-08 | Ordered item snapshots (order detail) MUST NOT link to live CatalogItem — historical copy (DR-06) |
| UI-GR-09 | OQ-001 (Admin module merge) — **do not generate merged admin** until human decides |
| UI-GR-10 | 2FA surfaces (APP-API-025..034) MUST be present if authentication surfaces are generated — evidence of intent exists (`TwoFactorEnabled` column) |

---

## 12. Assumptions & Open Questions

| ID | Statement |
|---|---|
| `ASMP-FE-2001` | No wireframes, mockups, or design artifacts exist in the legacy evidence; all layout/visual decisions are deferred to a human designer or design system choice |
| `ASMP-FE-2002` | The catalog browse page (`/`) is the storefront home; no separate landing page is evidenced |
| `ASMP-FE-2003` | No catalog item detail page route exists in the 55 APIs; a detail page would be a net-new addition requiring a new API endpoint |
| `ASMP-FE-2004` | Anonymous basket key mechanism (cookie vs session vs localStorage) is unspecified in evidence (ASMP-FE-005 from doc 09) — requires human decision |
| `ASMP-FE-2005` | Admin SPA currently lists and deletes catalog items; an "edit/update" SPA page is not evidenced (APP-API-007 PUT exists in PublicApi but no BlazorAdmin route maps to it) — 🟦 add if desired |
| `OQ-001` | Admin module (APP-SVC-005) vs BlazorAdmin (APP-SVC-016) merge — unresolved |

---

## 13. Traceability Summary

| UI artifact | Primary graph anchors |
|---|---|
| Catalog browse | APP-API-046, APP-API-004/002/008, BIZ-CAP-001/002/003/005, DATA-ENT-001/002/003 |
| Basket | APP-API-051, DATA-ENT-004/005, BR005/006/007, BIZ-PROC-002/003/004 |
| Checkout | APP-API-050/052, DATA-ENT-006/007/013, BR009/010/011/012, BIZ-PROC-005 |
| Order history/detail | APP-API-035/036, DATA-ENT-006/007, DATA-REL-009 |
| Login/Register | APP-API-042/044/041/043, DATA-ENT-008, BIZ-PROC-007, EVT-07 |
| Account management | APP-API-014..034, APP-SVC-037, DATA-ENT-008 |
| Admin SPA | APP-API-039/040/048/049, APP-SVC-016/050/046..049, BIZ-CAP-035/037/038/039, BIZ-PROC-006 |
| Auth/security | TECH-SEC-001/003/004, SR-01/02, §13.11 |
