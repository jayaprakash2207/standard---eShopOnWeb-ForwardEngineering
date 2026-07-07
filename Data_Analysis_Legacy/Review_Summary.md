# DA Agent 2 — Review Summary
> eShopOnWeb | Reviewed: 2026-07-06 | DB connection: CODE-ONLY (SQL Server not running)

---

## 1. Overview

| Item | Count |
|------|-------|
| Output files reviewed | 13 of 13 |
| ADDED changes | 2 (BR-19 new business rule; DQ-13 new data quality issue) |
| CORRECTED changes | 1 (DQ-12 qualifier: PublicApiIntegrationTests may use real localdb) |
| ENRICHED changes | 9 (BR-18, BR-07, BR-05, DS-05 cookie IsEssential, IMemoryCache confirmation, basket transfer merge logic, dead code confirmation, project purpose context, ProductName nullability note) |
| **Total changes** | **12** |

Test files scanned: 49 `.cs` files across 4 test projects (UnitTests/xUnit, IntegrationTests/xUnit, FunctionalTests/xUnit, PublicApiIntegrationTests/MSTest).
Documentation reviewed: `README.md` (no `docs/` folder exists).
Spot-check source files: `CacheHelpers.cs`, `OrderItemConfiguration.cs`, `CatalogContextSeed.cs`, `Index.cshtml.cs`, both `HealthChecks/` files, `Dependencies.cs`.

**Validation queue from Agent 1 — resolution:**

| VQ-ID | Status | Finding |
|-------|--------|---------|
| VQ-01 (PaymentMethod dead code) | RESOLVED ✅ | Confirmed — 0 test files reference BuyerAggregate. Confidence raised to 0.98. |
| VQ-02 (RESTRICT scenario tested?) | RESOLVED ✅ | Confirmed NOT tested. In-memory DB silently ignores RESTRICT. No Order delete test exists. |
| VQ-03 (CatalogItemId guard at checkout) | RESOLVED ✅ | No defensive null-check at `OrderService.CreateOrderAsync:catalogItems.First(...)`. Risk stands. |
| VQ-04 (UNIQUE index on Catalog.Name) | RESOLVED ✅ | Confirmed NO unique index in any migration. Concurrent create race condition is real. |
| VQ-05 (Cookie Secure/HttpOnly flags) | RESOLVED ✅ | `Index.cshtml.cs:94` — IsEssential=true IS set; Secure and HttpOnly are NOT set. |
| VQ-06 (Partial transfer failure tested?) | RESOLVED ✅ | Tests mock the repository — no failure path for DeleteAsync tested. Non-atomic risk stands. |

---

## 2. Quality Scores

| File | Before Review | After Review |
|------|:---:|:---:|
| schema-catalogue.json | 0.90 | 0.95 |
| erd.md | 0.90 | 0.90 |
| data-source-inventory.json | 0.90 | 0.92 |
| data-flow-map.md | 0.80 | 0.92 |
| pii-inventory.json | 0.90 | 0.95 |
| data-quality-report.md | 0.90 | 0.93 |
| migration-complexity.json | 0.90 | 0.90 |
| hidden-business-rules.json | 0.90 | 0.97 |
| storage-pattern-analysis.md | 0.90 | 0.97 |
| redundancy-analysis.json | 0.90 | 0.97 |
| data-dictionary.md | 0.90 | 0.90 |
| conceptual-data-model.md | 0.90 | 0.95 |
| access-control-matrix.md | 0.90 | 0.90 |
| **Overall** | **0.89** | **0.93** |

---

## 3. Key Corrections

### RC-08 / DQ-13 — OrderItemConfiguration vs. Migration Nullability Conflict (CORRECTED finding)
`OrderItemConfiguration.cs:16` calls `.IsRequired()` on `ItemOrdered_ProductName`, but `InitialModel` migration creates it `nullable: true`. The actual SQL schema is nullable — migration governs DDL, not ORM config. The application guards (`CatalogItemOrdered` constructor) prevent null in practice, but any raw SQL bypass would expose the gap. Invisible to all test suites (in-memory ignores this constraint).
- **Files updated:** `schema-catalogue.json`, `data-quality-report.md` (new DQ-13)

### RC-03 — Basket Item Price Lock Is Stronger Than Documented (ADDED, BR-19)
Agent 1 documented price lock at basket-add time (BR-05). Tests reveal a stronger invariant: adding the same item a second time at a *different* price does not update `UnitPrice` — only `Quantity` accumulates. A shopper who sees a price drop cannot benefit from it by "re-adding" the item; the original price is permanent for that basket session.
- **Files updated:** `hidden-business-rules.json` (new BR-19)

### RC-01 — PublicApiIntegrationTests May Hit Real LocalDB (ENRICHED/CORRECTED qualifier)
BR-18 claimed "ALL automated tests run exclusively against in-memory databases." This is 75% accurate. `PublicApiIntegrationTests` (MSTest) uses `WebApplicationFactory<Program>` with no `ConfigureServices` DB override. `appsettings.json` points to `(localdb)\mssqllocaldb`. This suite may validate real FK/constraint behaviour — which is actually better than in-memory, not worse.
- **Files updated:** `hidden-business-rules.json` (BR-18 qualifier)

---

## 4. Cross-File Consistency Results

| Check | Files | Result |
|-------|-------|--------|
| Same table count | `schema-catalogue.json` ↔ `erd.md` | ✅ PASS — 7 CatalogDB + 7 IdentityDB = 14 in both |
| PII columns match | `pii-inventory.json` ↔ `schema-catalogue.json` | ✅ PASS — all PII-flagged columns present in schema |
| Row counts match | `schema-catalogue.json` ↔ `migration-complexity.json` | ✅ PASS — both UNKNOWN (CODE-ONLY) |
| Business rules in flow map | `hidden-business-rules.json` ↔ `data-flow-map.md` | ✅ PASS — BR-07 (transfer), BR-05 (price lock) both in Flow 3 & 5 |
| Cache in both places | `data-source-inventory.json` ↔ `storage-pattern-analysis.md` | ✅ PASS — DS-03, DS-04 consistent |
| FK delete rules consistent | `schema-catalogue.json` ↔ `migration-complexity.json` | ✅ PASS — CASCADE and RESTRICT match |
| Canonical entity claims match | `redundancy-analysis.json` ↔ `schema-catalogue.json` | ✅ PASS — CANONICAL entities exist as tables; SHADOW_UNUSED absent from migrations |
| Data dictionary completeness | `data-dictionary.md` ↔ `schema-catalogue.json` | ✅ PASS — all 14 tables have entries; no invented meanings |
| Conceptual model traces to aggregates | `conceptual-data-model.md` ↔ `schema-catalogue.json` | ✅ PASS — all 5 conceptual entities trace to real table/aggregate |
| PII tables in access matrix | `access-control-matrix.md` ↔ `pii-inventory.json` | ✅ PASS — AspNetUsers, Baskets, Orders all covered in matrix |

**All 10 cross-file checks passed. No contradictions found.**

---

## 5. Open Questions for Gate G1

| # | Question | Category | Who to Assign |
|---|----------|----------|---------------|
| G1-01 | Is this application being migrated to production as-is, or used only as a reference? README explicitly states it is a demo/reference app, not a production ecommerce platform. If migrating to production, DQ-01 through DQ-13 all require remediation plans before go-live. | Business intent | Product Owner / Architecture Lead |
| G1-02 | What is the data retention policy for anonymous basket rows? No cleanup job exists. Over time `Baskets` accumulates rows for 10-year GUID cookies, with no TTL-based pruning. A policy (e.g., purge baskets older than 90 days with no order) is required. | Legal / Privacy | Data Privacy Officer |
| G1-03 | Right-to-erasure (GDPR Art. 17): deleting a user from IdentityDB does NOT remove their email from `CatalogDB.Baskets.BuyerId` or `CatalogDB.Orders.BuyerId`. Orders are immutable by design. Must business confirm whether erasure requires anonymisation or deletion of order history? | Legal / Compliance | Legal / DPO |
| G1-04 | JWT token lifetime: `AuthenticateEndpoint` does not set `Expires` on the `SecurityTokenDescriptor`. Tests set 1-hour expiry but the live endpoint has no explicit lifetime. What is the intended BlazorAdmin session duration? | Security policy | Security Architect |
| G1-05 | Infrastructure sizing: all row counts unknown. At production scale, `IMemoryCache` is per-process — in a multi-instance deployment behind a load balancer, each instance has a separate cache, causing inconsistent catalog views. Is horizontal scaling required? If yes, a distributed cache (Redis) must replace in-process IMemoryCache. | Infrastructure | Infrastructure / DevOps |

---

## 6. Gate G1 Recommendation

### READY

The 13 output files are internally consistent, well-evidenced (migration-confirmed 0.9+, test-confirmed where tested), and accurately describe the codebase from code alone. All 10 cross-file consistency checks passed. No fundamental architecture misunderstandings were found.

**Conditions before using outputs for production go/no-go decisions (not blockers for G1 review meeting):**

1. **Connect DB** to resolve row counts and confirm sequence current values. Run: `docker-compose up sqlserver` then re-run migration/schema queries.
2. **Acknowledge demo-app scope** (G1-01): This is a reference implementation. DQ-09 (hardcoded credentials/JWT key), DQ-01 (RESTRICT blocks Order deletion), and DQ-02 (no FK on BasketItems.CatalogItemId) must be remediated before production use.
3. **G1-03 (GDPR erasure)** is the highest-risk open question if real user data will ever be processed.

The DA outputs are of sufficient quality to brief stakeholders, identify migration risks, and begin forward-engineering design decisions.

---

## Appendix: All Change Records

| Change ID | Type | File | Summary |
|-----------|------|------|---------|
| RC-01 | ENRICHED | hidden-business-rules.json | BR-18 qualifier: PublicApiIntegrationTests may hit localdb, not in-memory |
| RC-02 | ENRICHED | hidden-business-rules.json | BR-07: transfer merge confirmed — same-item quantities accumulate |
| RC-03 | ADDED | hidden-business-rules.json | BR-19: basket UnitPrice locked at first-add; never updated by re-add |
| RC-04 | ENRICHED | storage-pattern-analysis.md | Cookie IsEssential=true confirmed; Secure/HttpOnly absent confirmed |
| RC-05 | ENRICHED | storage-pattern-analysis.md | CacheHelpers.DefaultCacheDuration=30s confirmed directly from source |
| RC-06 | ADDED | data-quality-report.md | DQ-13: OrderItemConfiguration IsRequired vs migration nullable:true conflict |
| RC-07 | ENRICHED | data-quality-report.md | DQ-12 qualifier: MSTest suite may use real localdb |
| RC-08 | CORRECTED | schema-catalogue.json | ItemOrdered_ProductName nullability discrepancy noted in column entry |
| RC-09 | ENRICHED | conceptual-data-model.md | README confirms reference/demo purpose, not production ecommerce |
| RC-10 | ENRICHED | redundancy-analysis.json | Buyer/PaymentMethod dead code confirmed by test scan (0 references in 49 files) |
| RC-11 | ENRICHED | pii-inventory.json | Hardcoded demo credentials in functional/integration tests; IsEssential confirmed |
| RC-12 | ENRICHED | data-flow-map.md | Basket transfer quantity-accumulation behaviour confirmed by test |

---

*DA Reverse Engineering System — Agent 2 of 2 | v2 | 2026-07-06*
