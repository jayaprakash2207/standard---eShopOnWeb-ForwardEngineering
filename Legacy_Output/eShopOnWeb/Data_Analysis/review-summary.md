# DA Agent 2 — Review Summary — eShopOnWeb

## 1. Overview

Files reviewed: **13 of 13**

Total changes: **10 distinct findings (RC-001 through RC-009, plus RC-001b/c, RC-002b/c/d, RC-004b)** applied across the output files:

| Type | Count | Findings |
|---|---|---|
| CORRECTED | 6 | RC-001 (DB engine), RC-002 (Buyer/PaymentMethod dead code), RC-003 (health checks present), RC-004 (cache mechanism), RC-007 (basket not cleared on checkout), RC-009 (DuplicateException target) |
| ENRICHED | 2 | RC-008 (confirmed "Administrators" role string), RC-004b (cache mechanism enrichment in hidden-business-rules.json) |
| ADDED | 2 | RC-005 (CustomAuthStateProvider 60s refresh interval), RC-006 (hardcoded secrets in AuthorizationConstants.cs) |

Files updated: schema-catalogue.json, data-source-inventory.json, migration-complexity.json, redundancy-analysis.json, pii-inventory.json, hidden-business-rules.json, data-flow-map.md, data-quality-report.md, storage-pattern-analysis.md, access-control-matrix.md, erd.md, data-dictionary.md, conceptual-data-model.md (all 13).

The pre-flight check found `db_connection: "CODE-ONLY"` in schema-catalogue.json. No live DB CLI session was available in this environment, so per the fallback approach, Phase 4 spot-checking of source files (Dependencies.cs, CatalogContext.cs, AppIdentityDbContext.cs, migration files, Program.cs, AuthorizationConstants.cs, CustomAuthStateProvider.cs, CacheEntry.cs, BlazorShared/Authorization/Constants.cs, OrderService.cs, CreateCatalogItemEndpoint.cs, BasketConfiguration.cs, OrderConfiguration.cs) was used to confirm or correct Agent 1's code-derived findings. This is evidence-strength "entity/ORM code" / "migration files" tier — high confidence, but row counts, live FK constraint names, and live data values remain UNKNOWN.

## 2. Quality Scores

| Dimension | Before | After |
|---|---|---|
| Database engine accuracy | 0.8 | 0.9 |
| Shadow-entity (Buyer/PaymentMethod) resolution | 0.6–0.7 | 0.9 |
| Caching layer accuracy | 0.5–0.7 | 0.85 |
| Access control / role names | 0.75 | 0.95 |
| Security findings completeness | n/a (0 findings) | 0.9 (hardcoded secrets documented) |
| Health checks coverage | 0.0 (marked absent) | 0.9 |
| Checkout/basket flow accuracy | 0.7 | 0.85 |
| **Overall** | **~0.72** | **~0.90** |

## 3. Key Corrections

- **RC-001 — Database engine is PostgreSQL (Npgsql), not SQL Server/Azure SQL Edge.** `src/Infrastructure/Dependencies.cs` registers `UseNpgsql(...)` for both `CatalogContext` and `AppIdentityDbContext`, and `src/Web/appsettings.json` has Postgres connection strings (`Host=localhost;Port=5432;Database=eShopCatalog` / `eShopIdentity`). Migration history (`20260526102924_InitialPostgres.cs`, `20260526102952_InitialPostgres.Designer.cs`) confirms this. `appsettings.Docker.json` still has SQL Server connection strings — flagged as likely stale config (see Gate G1 #1). This was the single most consequential correction: every file that stated "SQL Server / Azure SQL Edge" (schema-catalogue.json, data-source-inventory.json, storage-pattern-analysis.md, erd.md) was updated.

- **RC-002 — Buyer/PaymentMethod confirmed dead/unmapped code, not "possible shadow entities."** `CatalogContext.cs` declares exactly 7 DbSets (Baskets, CatalogItems, CatalogBrands, CatalogTypes, Orders, OrderItems, BasketItems); `AppIdentityDbContext.OnModelCreating` only calls `base.OnModelCreating()`. No `modelBuilder.Entity<Buyer>()`, `IRepository<Buyer>`, or any reference to these classes exists outside their own files. This resolved an open item that had propagated across 6 files (schema-catalogue.json, redundancy-analysis.json, pii-inventory.json, data-quality-report.md, migration-complexity.json, erd.md, conceptual-data-model.md, data-dictionary.md) — all now consistently marked CONFIRMED at confidence 0.9. The PII/PCI-DSS concern around PaymentMethod is resolved (not currently in scope).

- **RC-003 — Health checks ARE present (storage-pattern-analysis.md previously said "absent, UNKNOWN").** `src/Web/Program.cs` calls `.AddHealthChecks()`, maps `/health`, and registers `home_page_health_check` / `api_health_check` tagged endpoints.

- **RC-004 — BlazorAdmin caching uses browser localStorage (`ILocalStorageService` + `CacheEntry<T>{Value, DateCreated}`), not `IMemoryCache`/`{Value, ExpiresAt}` as guessed.** The exact staleness/expiry comparison logic remains unlocated (open item).

- **RC-007 — `OrderService.CreateOrderAsync` does NOT clear the basket after order creation.** The original data-flow-map.md inferred (confidence 0.7) that the basket is cleared post-checkout; reading the method shows it only reads the basket, validates non-empty, snapshots items into `OrderItem`s, and saves the `Order`. No delete/clear call exists in this method.

- **RC-006 — New security finding: hardcoded secrets in `AuthorizationConstants.cs`.** `AUTH_KEY`, `JWT_SECRET_KEY` (placeholder values), and `DEFAULT_PASSWORD = "Pass@word1"` are hardcoded with `// TODO: don't use in production` comments. Added to pii-inventory.json, data-quality-report.md, access-control-matrix.md.

## 4. Cross-File Consistency Results (Phase 5)

| Check | Files | Result |
|---|---|---|
| Same table count | schema-catalogue.json ↔ erd.md | PASS (7 CatalogDb tables consistent; Buyer/PaymentMethod note now consistent — both say "confirmed not mapped") |
| PII columns match | pii-inventory.json ↔ schema-catalogue.json | PASS — PaymentMethod entry reconciled with RC-002; AuthorizationConstants secrets added to pii-inventory.json |
| Row counts match | schema-catalogue.json ↔ migration-complexity.json | PASS (both still UNKNOWN — no live DB; consistent) |
| Business rules in flow map | hidden-business-rules.json ↔ data-flow-map.md | FIXED — basket-clearing claim (RC-007) and Administrators role / AuthorizationConstants claim (RC-008) were inconsistent between the two files; both now aligned |
| Cache in both places | data-source-inventory.json ↔ storage-pattern-analysis.md | FIXED — both now describe localStorage + CacheEntry<T>{Value,DateCreated} (RC-004) consistently |
| FK delete rules consistent | schema-catalogue.json ↔ migration-complexity.json | PASS — both still note FK delete-behavior for CatalogItem←BasketItem/OrderItem as not confirmed from `OrderConfiguration.cs`/`BasketConfiguration.cs` (no explicit `OnDelete` call found); left as an open item, not contradictory |
| Canonical entity claims match actual table/usage evidence | redundancy-analysis.json ↔ schema-catalogue.json | FIXED — Buyer reclassified from "POSSIBLE SHADOW" to "CONFIRMED DEAD CODE" in both files (RC-002) |
| Every table/column has a dictionary entry, none invent meanings | data-dictionary.md ↔ schema-catalogue.json | PASS — Unmapped Entities section in data-dictionary.md updated to match RC-002 |
| Every concept in conceptual model traces to a real aggregate root | conceptual-data-model.md ↔ schema-catalogue.json | FIXED — "Payment Method" concept now explicitly marked as not implemented in the persisted schema (RC-002) |
| Every PII table/column appears in access matrix with cited evidence | access-control-matrix.md ↔ pii-inventory.json | FIXED — Payment Methods row resolved to N/A (RC-002); AuthorizationConstants hardcoded-secrets finding (RC-006) cross-referenced into access-control-matrix.md |

## 5. Open Questions for Gate G1

1. **Stale SQL Server connection strings in `appsettings.Docker.json`** (Web and PublicApi) coexist with an Npgsql-only provider registration in `Dependencies.cs`. Is this dead config from the original SQL Server template that should be removed, or is there a parallel SQL-Server-based deployment path the team still maintains? — *Requires infrastructure/deployment-ownership input.*
2. **Hardcoded secrets in `AuthorizationConstants.cs`** (`AUTH_KEY`, `JWT_SECRET_KEY`, `DEFAULT_PASSWORD = "Pass@word1"`) are marked `// TODO` as non-production. Are these guaranteed to be overridden via environment/config in every real deployment, or could a misconfiguration ship them as-is? — *Requires security/ops sign-off.*
3. **Cache staleness/expiry logic for `CacheEntry<T>`** — `DateCreated` is recorded but the comparison/expiry check was not located in this pass. If this matters for a Gate G1 demo (stale catalog data in BlazorAdmin), a deeper read of the decorator classes' Get methods is needed. *(Lower priority — code-readable, can be resolved without business input if time permits.)*
4. **1 feature flag** reported in the original extraction summary (`total_feature_flags = 1`) could not be located via a spot-check grep for `FeatureManagement`/`IFeatureManager`/`FeatureFlag`. Either the flag uses a different mechanism (e.g. a simple config bool) or it's in a file outside the areas spot-checked. *(Lower priority — code-readable.)*
5. **Whether Basket is intentionally left un-cleared after checkout (RC-007)** is a genuine UX/business question: should a user's basket be emptied automatically after placing an order? This affects both the data model (orphaned `BasketItems` rows after checkout) and UX. — *Requires product/business input.*

## 6. Gate G1 Recommendation

**READY**, with the five open items above carried forward as discussion points rather than blockers. All 13 documents are now internally consistent, the most significant factual error (database engine) has been corrected across every affected file, the previously-unresolved Buyer/PaymentMethod shadow-entity question is closed, and a new security finding (hardcoded secrets) has been surfaced for stakeholder awareness. None of the remaining open items represent a fundamentally different architecture (no event sourcing, CQRS, or multi-tenancy was found) and none require re-running Agent 1's extraction.
