# Strangler / Migration Candidate Report — eShopOnWeb

Generated from source evidence. Unknown items are marked as unknown.

---

## Module Migration Ranking

### Rank 1 — Authentication Module
**Classification: Good Early Candidate**

| Criterion | Assessment |
|---|---|
| Boundary clarity | Strong — AppIdentityDbContext already separate from CatalogContext |
| Efferent coupling | Low — depends only on ASP.NET Identity + JWT libraries |
| Public interfaces | Clear — POST /api/authenticate; GET /User |
| External dependencies | SQL Server (Identity DB) only |
| Circular dependencies | None |
| Architecture violations | Hardcoded JWT secret (must fix first, then extract) |

**Recommended action:** Extract as an `auth-service` after rotating the JWT secret. This service already has a separate DbContext and well-defined HTTP interface. Can be deployed as a standalone minimal API behind a shared token issuer.

**Risks:**
- JWT secret rotation must happen before extraction
- Web project's cookie-based auth flow needs verification (not in extraction)
- /User endpoint needs investigation — which project currently serves it?

---

### Rank 2 — Catalog Module (Read-Only First)
**Classification: Good Early Candidate (read path) / Possible Candidate With Refactoring (write path)**

| Criterion | Assessment |
|---|---|
| Boundary clarity | Moderate — Catalog entities well-defined; client-side join coupling in BlazorAdmin |
| Efferent coupling | Low for reads; write path needs CQRS design |
| Public interfaces | GET /api/catalog-brands, GET /api/catalog-items, GET /api/catalog-types |
| External dependencies | CatalogContext (shared — must split first) |
| Architecture violations | Client-side join in BlazorAdmin; shared CatalogContext |

**Recommended action (Phase 1):** Extract catalog read endpoints as a standalone `catalog-read-service`. Expose GET endpoints from a dedicated database read replica or separate read model. BlazorAdmin can point to new URL.

**Recommended action (Phase 2):** Extract catalog admin write operations (Create, Update, Delete catalog items) after designing a proper catalog-admin API with events.

**Risks:**
- CatalogContext must be split before database-level isolation
- BlazorAdmin client-side join must be redesigned to use enriched catalog item DTO

---

### Rank 3 — Basket Module
**Classification: Possible Candidate With Refactoring**

| Criterion | Assessment |
|---|---|
| Boundary clarity | Strong domain model; basket transfer is a complex stateful operation |
| Efferent coupling | Medium — anonymous-to-auth transfer is a 2-record transaction |
| Public interfaces | Unknown (Web project not extracted) |
| External dependencies | CatalogContext (shared); anonymous session management |
| Circular dependencies | None in code; data-level dependency with Catalog (CatalogItemId FK) |
| Architecture violations | CatalogContext shared; TransferBasketAsync transactional risk |

**Recommended action:** Extract after CatalogContext split and after defining the basket-checkout contract with Order. BasketService's core domain model is clean and portable.

**Risks:**
- TransferBasketAsync requires distributed transaction or eventual consistency design
- Basket depends on CatalogItemId reference — need to decide if Catalog item validation happens in Basket or Order service
- Web project basket controllers unknown — need extraction

---

### Rank 4 — Order Module
**Classification: Poor Candidate (until Basket and Catalog are resolved)**

| Criterion | Assessment |
|---|---|
| Boundary clarity | Strong within domain; but cross-module dependency on Basket and Catalog at runtime |
| Efferent coupling | High — OrderService depends on Basket + Catalog + Infrastructure simultaneously |
| Public interfaces | Unknown (Web project not extracted) |
| External dependencies | CatalogContext (shared) |
| Architecture violations | Cross-aggregate read in OrderService.CreateOrderAsync |

**Recommended action:** Migrate Order LAST in the sequence. Before extraction: (a) split CatalogContext, (b) extract Basket with checkout DTO, (c) design checkout saga or workflow. Only then can OrderService be redesigned to consume a checkout request rather than reading basket directly.

**Risks:**
- Direct dependency on IRepository<Basket> in OrderService is a hard coupling
- CatalogItemOrdered snapshot pattern is good — preserve it in forward engineering
- No payment processing exists — forward-engineered Order service will need payment integration design

---

### Rank 5 — Buyer Module
**Classification: Unknown**

| Criterion | Assessment |
|---|---|
| Boundary clarity | Entity exists; no service or API surface |
| Efferent coupling | Unknown — not wired |
| Public interfaces | None visible |
| External dependencies | Unknown — not in DbContext |
| Architecture violations | Dead code candidate |

**Recommended action:** Requires human review before classification. If Buyer is dead code, remove. If it is intended as a future payment/profile module, design it as a new service from scratch rather than migrating the stub.

---

## Recommended Migration Sequence

```
Phase 0 (Pre-migration hardening):
  1. Rotate JWT secret — move to env/Key Vault
  2. Complete extraction of Web project controllers/pages (fill coverage gap)
  3. Clarify Buyer module status
  4. Add missing Web project source to architecture extraction

Phase 1 (Low-risk extractions):
  5. Extract Authentication service (standalone auth-service)
  6. Extract Catalog read API (catalog-read-service, read-only first)

Phase 2 (Context splitting):
  7. Split CatalogContext into CatalogContext, BasketContext, OrderContext
  8. Run schema migrations per bounded context

Phase 3 (Module extractions):
  9. Extract Basket service (basket-service) with new checkout contract
  10. Extract Catalog write operations (catalog-admin-service)

Phase 4 (Order and orchestration):
  11. Design checkout workflow / saga (spans Basket + Order + Payment)
  12. Extract Order service (order-service) with saga pattern
  13. Design and integrate payment service (net-new, using Stripe or equivalent)

Phase 5 (Web decommission):
  14. Decompose Web project by feature into micro-frontends or dedicated BFF layers
  15. Retire Web monolith after all features migrated
```

---

## Human Review Questions

1. What does the Web project (src/Web) expose? Basket, order, and catalog browsing controllers must be analyzed before finalizing migration sequence.
2. Is the Buyer aggregate in use anywhere not captured? Dead code vs. planned payment feature?
3. How does the Web project authenticate? Cookie-based or JWT? If both patterns exist, the auth service extraction is more complex.
4. What serves the /User endpoint consumed by BlazorAdmin? Web project? A separate user profile service?
5. Is BlazorAdmin hosted as part of the Web project (embedded WASM) or deployed standalone?
6. Is there an existing payment processing integration not visible in extracted files?
7. What is the expected production load profile? Catalog (read-heavy) vs. Basket/Order (write-transaction-heavy) may drive different deployment priorities.
8. Are there test projects in the solution? Test coverage affects migration safety.
