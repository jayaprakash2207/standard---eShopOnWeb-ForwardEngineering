---

**Application Architecture extraction completed.**

**Output location:** `test-run/D1-application-architecture/`

**Files generated (19 total):**
- `system-inventory.json`, `module-boundary-map.json`, `component-registry.json`, `application-interface-catalogue.json`, `dependency-graph.json`, `call-flow-map.json`
- `architecture-pattern-report.md`, `architecture-violation-register.json`, `application-risk-register.json`
- `strangler-candidate-report.md`, `forward-engineering-input-map.md`, `open-questions.md`, `extraction-audit.md`
- `diagrams/system-context.mmd`, `diagrams/container-view.mmd`, `diagrams/component-view.mmd`, `diagrams/dependency-view.mmd`, `diagrams/call-flow-view.mmd`
- `application-architecture-summary.md`

---

**Top 5 Architecture Findings:**

1. **Clean Architecture with DDD-Lite** (confidence 0.90) — strict dependency inversion, IAggregateRoot-constrained repository, rich domain entities with Guard.Against validation, Ardalis.Specification for query encapsulation
2. **Shared CatalogContext spans 3 domain boundaries** — Basket, Order, and Catalog all live in one EF DbContext; this is the #1 technical migration blocker
3. **OrderService reads Basket internals directly** — cross-aggregate coupling in `CreateOrderAsync` prevents independent Order and Basket service extraction
4. **Decorator pattern in BlazorAdmin** — `CachedCatalogItemServiceDecorator` wraps catalog services with 1-minute LocalStorage TTL; client-side join of brands/types/items on every page load
5. **Two separate DbContexts** — CatalogContext (business) and AppIdentityDbContext (identity) are already isolated — this is an architectural strength that makes auth service extraction straightforward

---

**Top 5 Risks:**

1. **APP-RISK-002 (Critical):** `JWT_SECRET_KEY` and `DEFAULT_PASSWORD` are hardcoded in source — blocks any production deployment
2. **APP-RISK-001 (High):** Shared CatalogContext — cannot extract Basket, Order, or Catalog as independent services without splitting this context first
3. **APP-RISK-003 (High):** OrderService→Basket coupling — requires CheckoutDTO design before Order extraction
4. **APP-RISK-005 (High):** Web project not extracted — basket, checkout, and order entry points are unknown; architecture map is incomplete
5. **APP-RISK-009 (Medium):** `TransferBasketAsync` is effectively a 2-record transaction — becomes a distributed transaction problem when Basket is extracted

---

**Open Questions Requiring Human Review:**

- **OQ-004/OQ-005 (Critical):** Has the JWT secret been rotated in production? Are accounts still using the hardcoded DEFAULT_PASSWORD?
- **OQ-001 (High):** Web project source must be extracted to complete the architecture map
- **OQ-007 (Medium):** Which project serves `GET /User`? Required for auth service design
- **OQ-008 (Medium):** Does the checkout controller delete the basket after order creation?
- **OQ-006 (Medium):** Is the Buyer aggregate dead code or a planned payment module?
