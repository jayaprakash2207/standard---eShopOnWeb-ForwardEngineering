# 19 — Frontend Architecture

> **Single source of truth:** `ENTERPRISE_KNOWLEDGE_GRAPH.json`. Every surface, component, route, and service mapping below is traced to graph node ids (`APP-SVC-###`, `APP-API-###`, `APP-IF-###`, `TECH-CUR-###`, `BIZ-CAP-###`). No frontend surface, component, or route has been invented.
>
> **Technology neutrality:** `target_stack` is **empty (0 nodes)**. Every target frontend technology (React, Angular, Vue, Next.js, etc.) is a **[NEUTRAL-OPTION] not in legacy evidence**. Only the current Blazor WASM / Razor MVC surfaces are labeled **Current (legacy)**. Target options are offered per the mandated set; none is recommended over another.
>
> **Status flags honored:** BC-06 Buyer/Customer Profile is aspirational (RC-002); no frontend surface is designed for it. Payment capabilities BIZ-CAP-027/028 are INFERRED/LOW; no payment UI is generated.

---

## 1. Purpose

This document specifies the frontend architecture — surfaces, rendering models, component decomposition, routing, data-fetch patterns, auth wiring, and technology options — for forward engineering. It is the frontend companion to doc 11 (API Contracts) and doc 13 (Security Architecture).

---

## 2. Current (Legacy) Frontend Surfaces

The legacy system has **two distinct frontend surfaces** hosted in three deployable units:

| Surface | Deployable unit | Node(s) | Technology (legacy) | Rendering |
|---|---|---|---|---|
| **Storefront** — catalog browse, basket, checkout, orders, account/identity | Web (`eshopwebmvc`, TECH-INF-001) | APP-SVC-006 | ASP.NET Core MVC + Razor Pages | **Server-rendered (SSR)** |
| **Admin SPA** — catalog CRUD, cache refresh | Web (hosted inside eshopwebmvc) | APP-SVC-016 (BlazorAdmin), APP-SVC-005 (Admin module) | **Blazor WebAssembly** (TECH-CUR-003) | **Client-side SPA (WASM)** |

> ⚠️ Open evidence item: `TECH-CUR-003` is labeled **Blazor WebAssembly** but `APP-SVC-006` evidence describes the Web host as "ASP.NET Core MVC + Razor Pages + **Blazor Server** host". This tension is unresolved (doc 12 §2.1 note). Blueprint follows `TECH-CUR-003` (WebAssembly); confirm against source before generating.

---

## 3. Storefront Surface — Current (Legacy) Page Inventory

All 43 Web-served routes (`APP-API-009…052, 055`, owner `APP-SVC-006`), grouped by functional area.

### 3.1 Public / Catalog (BC-01)

| API | Method | Route | Page / Handler | Capability | Auth |
|---|---|---|---|---|---|
| APP-API-046 | GET | `/` | Index (catalog listing) | BIZ-CAP-001 Browse Catalog | anonymous |
| APP-API-047 | GET | `/Privacy` | Privacy | — | anonymous |
| APP-API-045 | GET | `/Error` | Error | — | anonymous |
| APP-API-009 | ROUTE† | `{controller}/{action}/{id?}` | Conventional MVC route | — | — |
| APP-API-010 | ROUTE† | Razor Pages route registration | — | — | — |
| APP-API-011 | ROUTE† | `/index.html` | SPA fallback | — | — |

### 3.2 Basket & Checkout (BC-02 / BC-03)

| API | Method | Route | Page / Handler | Capability | Auth |
|---|---|---|---|---|---|
| APP-API-051 | GET† | `/{handler?}` | Basket Index (Razor Page) | BIZ-CAP-012 Add to Basket | anonymous / Customer |
| APP-API-050 | GET | `/Basket/Checkout` | Checkout (Razor Page) | BIZ-CAP-019 Checkout | Customer (authenticated) |
| APP-API-052 | GET | `/Basket/Success` | Order Success (Razor Page) | BIZ-CAP-021 Place Order | Customer |

### 3.3 Orders (BC-03)

| API | Method | Route | Page / Handler | Auth |
|---|---|---|---|---|
| APP-API-035 | GET | `/Order/MyOrders` | GetMyOrders handler (MediatR, APP-SVC-041/042) | Customer (own orders) |
| APP-API-036 | GET | `/Order/Detail/{orderId}` | GetOrderDetails handler (APP-SVC-043) | Customer (own, row-level) |

### 3.4 Identity & Account (BC-04)

| API | Method | Route | Page / Handler | Auth |
|---|---|---|---|---|
| APP-API-042 | GET | `/Account/Login` | Login Razor Page | anonymous |
| APP-API-044 | GET | `/Account/Register` | Register Razor Page | anonymous |
| APP-API-041 | GET | `/Account/ConfirmEmail` | ConfirmEmail Razor Page | anonymous |
| APP-API-043 | GET | `/Account/Logout` | Logout Razor Page | authenticated |
| APP-API-037 | GET | `/User` | UserController (APP-SVC-039) | authenticated |
| APP-API-038 | POST | `/User/Logout` | UserController.Logout | authenticated |
| APP-API-014..034 | GET/POST | `/Manage/*` | ManageController (APP-SVC-037) — 21 account/2FA/password/external-login routes | authenticated (own account) |

### 3.5 Admin (BC-05 — via Web shell Razor Pages)

| API | Method | Route | Page / Handler | Auth |
|---|---|---|---|---|
| APP-API-049 | GET | `/Admin` | Admin Index Razor Page | **Administrators** |
| APP-API-048 | GET | `/Admin/EditCatalogItem` | EditCatalogItem Razor Page | **Administrators** |

### 3.6 Health checks

| API | Method | Route | Auth |
|---|---|---|---|
| APP-API-012 | GET | `/home_page_health_check` | anonymous |
| APP-API-013 | GET | `/api_health_check` | anonymous |

---

## 4. Admin SPA Surface — Current (Legacy) BlazorAdmin

| API | Method | Route | Component | Auth |
|---|---|---|---|---|
| APP-API-040 | ROUTE† | `/admin` | List.razor (APP-SVC-050) — catalog item list + CRUD | **Administrators** |
| APP-API-039 | ROUTE† | `/logout` | Logout.razor (APP-SVC-046) | **Administrators** |
| APP-API-053 | CLI† | Bootstrap | BlazorAdmin Program.cs | internal |

**BlazorAdmin component inventory (APP-SVC-016 / BC-05):**

| Node | Component | Role |
|---|---|---|
| APP-SVC-046 | BlazorComponent | Base component (CallRequestRefresh hook) |
| APP-SVC-047 | BlazorLayoutComponent | Shell layout for all BlazorAdmin pages |
| APP-SVC-048 | ToastComponent | Toast notification |
| APP-SVC-049 | RefreshBroadcast | Broadcast helper for catalog list refresh (EVT-10 CatalogCacheRefreshed) |
| APP-SVC-050 | List | Catalog item list page; consumes ICatalogItemService / ICatalogLookupDataService (APP-IF-010/011) |
| APP-SVC-051 | CustomAuthStateProvider | WASM auth state; implements APP-IF-013 |
| APP-SVC-044 | CachedCatalogItemServiceDecorator | In-memory cache decorator for catalog items | 
| APP-SVC-045 | CachedCatalogLookupDataServiceDecorator | In-memory cache decorator for brands/types |

**Runtime HTTP dependencies (BlazorAdmin ← → backends):**

| Dependency | Source | Target | Note |
|---|---|---|---|
| APP-DEP-017 | BlazorAdmin (APP-SVC-016) | PublicApi (APP-SVC-011) | Catalog CRUD calls (APP-API-002..008) |
| APP-DEP-018 | BlazorAdmin (APP-SVC-016) | Web (APP-SVC-006) | Supplementary Web calls |

> `OQ-001` — whether to **merge** Admin module (APP-SVC-005) with BlazorAdmin (APP-SVC-016) is **UNRESOLVED**. Keep separate until a human decides.

---

## 5. Frontend Data-Fetch Patterns (Current / Legacy)

| Pattern | Where used | Evidence |
|---|---|---|
| **EF Core direct** (server-side) | Storefront Razor Pages — IndexModel (APP-SVC-040) fetches catalog via EfRepository directly | APP-DEP-002..009 (layer violations — MUST be fixed in target) |
| **MediatR handler** (server-side) | Order history / detail — APP-SVC-041/042/043 mediate between Razor Page and Order aggregate | TECH-CUR-011 MediatR |
| **HTTP/JSON fetch** (client-side) | BlazorAdmin → PublicApi (APP-DEP-017) via ICatalogItemService/ICatalogLookupDataService | APP-IF-010/011 |
| **Local storage** | BlazorAdmin session state | Blazored.LocalStorage (TECH-CUR-017) |
| **In-memory cache** | BlazorAdmin catalog list via decorator pattern (APP-SVC-044/045) | CachedCatalogItemServiceDecorator |

> The direct Razor Page → EfRepository violations (APP-DEP-002..009, APP-DEP-009 coupling 16) **MUST NOT be reproduced** in the target (AR-04, M-4). Storefront data-fetch must go through application service ports (APP-IF-001/002).

---

## 6. Target Frontend Options (Neutral — not in legacy evidence)

### 6.1 Rendering model options

| Option | Description | Best for |
|---|---|---|
| **Server-Side Rendering (SSR)** | Pages rendered on server; closest to current Razor Pages | Low JS complexity; SEO; simple auth |
| **Client-Side SPA** | React/Angular/Vue app; calls JSON APIs | Rich interactivity; separate deploy |
| **Hybrid (SSR + SPA islands)** | SSR storefront + SPA admin (mirrors current split) | Matches legacy topology |
| **Edge SSR / Streaming** | Next.js / Nuxt with streaming | Performance-first storefront |

**Recommended (neutral default, not evidenced):** Hybrid — SSR storefront (Next.js/Nuxt/Blazor Server) + SPA admin (React/Angular/Vue). Mirrors the current proven split; SSR handles catalog SEO; SPA handles admin interactivity.

### 6.2 Target framework options per surface

| Surface | React option | Angular option | Vue option | ASP.NET Core option |
|---|---|---|---|---|
| Storefront | Next.js SSR | Angular Universal | Nuxt SSR | Razor Pages (retained) |
| Admin SPA | React (Vite/CRA) | Angular SPA | Vue (Vite) | Blazor WASM (retained) |
| Auth state | oidc-client-ts + React Context | angular-auth-oidc-client | Pinia auth store | ASP.NET Core Identity |
| Catalog service client | typed fetch/axios | Angular HttpClient | composable axios | ICatalogItemService retained |
| Toast/notifications | react-hot-toast | Material snackbar | vue-toastification | (custom) |
| Local storage | Web Storage / TanStack | Angular storage service | Pinia persist | Blazored.LocalStorage retained |

### 6.3 API consumption (frontend → backend)

All target frontend options consume the **same 8 PublicApi JSON endpoints** (APP-API-001..008) and the page-route surfaces (APP-API-009..052). Under a full SPA migration the storefront Razor Page routes need an **API-first redesign** — today only APP-API-001..008 return pure JSON; all Web routes (APP-API-009..052) are HTML. See ASMP-FE-1201 (doc 12).

---

## 7. Frontend Bounded-Context Ownership

| Surface | Functional BC | Physical host | Data access pattern (target) |
|---|---|---|---|
| Catalog browse (`/`) | BC-01 | Web shell (BC-07) | → GET /api/catalog-items (APP-API-004) |
| Basket (`/Basket`) | BC-02 | Web shell (BC-07) | → Basket application service (APP-IF-006/007) |
| Checkout (`/Basket/Checkout`) | BC-03 | Web shell (BC-07) | → Order application service |
| Order history (`/Order/*`) | BC-03 | Web shell (BC-07) | → GET order endpoints (APP-API-035/036) |
| Identity/Account (`/Account/*`, `/Manage/*`) | BC-04 | Web shell (BC-07) | → Identity service (APP-API-042/044, ManageController) |
| Admin catalog CRUD (`/admin`) | BC-05 | BlazorAdmin / SPA | → PublicApi (APP-API-005/006/007) via APP-IF-010/011 |

> Ownership follows ASMP-FE-004 (doc 11/15): flows are attributed to **functional** bounded context while physical hosting remains with the shell (BC-07). Domain logic lives in the functional context; routing/composition in BC-07.

---

## 8. Frontend Security Requirements

| Control | Requirement | Source |
|---|---|---|
| AuthN | OIDC Authorization Code + PKCE for interactive users | SR-01 / §13.10.2 |
| Token storage | Access token in memory (not localStorage); refresh via BFF or rotating cookie | TECH-SEC-003; ASMP-FE-001 |
| Admin auth | Admin SPA MUST enforce `Administrators` role before any catalog mutation | SR-02 / §13.11 |
| CORS | Explicit allow-list for BlazorAdmin/SPA origin → PublicApi/Web (APP-DEP-017/018) | TECH-SEC-011; SR-04 |
| Security headers | CSP, X-Content-Type-Options, X-Frame-Options, HSTS at ingress | §13.10.5 |
| Anonymous basket | Session/cookie key for anonymous basket; no user token required | ASMP-FE-005 (doc 09) |
| No PII in frontend logs | Order/User/Address PII must not appear in browser console/telemetry | DB-08 |

---

## 9. Frontend NFR Targets

| Target | Value | Basis |
|---|---|---|
| Catalog page initial load (p95) | ≤ 3 s on 4G | NFR-PERF-001 (industry baseline) ⚠ DERIVED |
| Time to interactive (admin SPA) | ≤ 2 s (cached bundle) | ASMP-FE-1901 ⚠ DERIVED |
| Accessibility | WCAG 2.1 AA | industry standard ⚠ — no evidence in legacy |
| Responsive breakpoints | Mobile / Tablet / Desktop | ⚠ DERIVED — not in legacy evidence |
| Bundle size (SPA) | < 500 KB gzipped initial | ⚠ DERIVED |

> All NFRs above are ⚠ **DERIVED / NEUTRAL DEFAULTS** — no frontend performance metrics exist in the legacy evidence. Re-baseline with real measurements post-launch.

---

## 10. Frontend Generation Rules

| Rule | Constraint |
|---|---|
| FE-GR-01 | Storefront data-fetch MUST NOT call EfRepository directly (AR-04 / M-4) — route through application service ports |
| FE-GR-02 | Admin SPA MUST call PublicApi endpoints only (APP-API-002..008); MUST NOT bypass the API layer |
| FE-GR-03 | Catalog mutations in admin (APP-API-005/006/007) MUST require `Administrators` JWT claim before any UI action (§13.11) |
| FE-GR-04 | Checkout flow MUST enforce authenticated buyer id (BR011) before submitting order |
| FE-GR-05 | Anonymous basket MUST be keyed by session/cookie (ASMP-FE-005); transfer on login (BIZ-PROC-003 / EVT-03) |
| FE-GR-06 | No payment UI generated — BC-06 aspirational (RC-002 / SR-09) |
| FE-GR-07 | OQ-001 (Admin module vs BlazorAdmin merge) MUST be resolved by a human before generating the admin surface |
| FE-GR-08 | All 55 APIs in scope (doc 11) — ROUTE/CLI synthetic labels are host/routing concerns, not new JSON endpoints (OQ-009) |

---

## 11. Open Questions & Assumptions

| ID | Statement |
|---|---|
| `OQ-001` | Admin module (APP-SVC-005) vs BlazorAdmin (APP-SVC-016) merge — **UNRESOLVED**; keep separate |
| `OQ-009` | Synthetic ROUTE/CLI API labels — confirmed host/routing realizations, not RESTful contracts |
| `ASMP-FE-1201` | Razor MVC storefront pages are server-rendered; SPA migration requires API-first redesign of APP-API-009..052 |
| `ASMP-FE-1901` | No frontend performance baselines exist in legacy evidence; all NFRs above are derived/assumed |
| `ASMP-FE-1902` | Blazor WASM vs Blazor Server hosting model is unresolved (TECH-CUR-003 vs APP-SVC-006 description tension) — confirm against source before generating |
| `ASMP-FE-1903` | Anonymous basket session-key mechanism (cookie vs localStorage vs server session) is not specified in evidence (doc 09 ASMP-FE-005) — requires human decision before generating basket persistence |

---

## 12. Traceability Summary

| Frontend artifact | Primary graph anchors |
|---|---|
| Storefront pages | APP-API-009..052, APP-SVC-006, BC-02/03/04/07 |
| Admin SPA | APP-SVC-016/046/047/048/049/050/051, APP-API-039/040/053, BC-05 |
| Cache decorators | APP-SVC-044/045, APP-IF-010/011 |
| Auth state | APP-SVC-051, APP-IF-013, TECH-SEC-001/003 |
| Runtime deps | APP-DEP-017 (BlazorAdmin→PublicApi), APP-DEP-018 (BlazorAdmin→Web) |
| Layer violations to fix | APP-DEP-002..009 (endpoint/PageModel→EfRepository) |
| Security | TECH-SEC-001/002/003/004/010/011, SR-01..04, §13.11 |
