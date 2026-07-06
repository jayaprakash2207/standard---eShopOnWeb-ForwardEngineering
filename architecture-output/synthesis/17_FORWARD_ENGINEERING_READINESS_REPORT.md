=== DOCUMENT: 17_FORWARD_ENGINEERING_READINESS_REPORT.md ===

# Forward Engineering Readiness Report — eShopOnWeb
## Scored Assessment for Code Generation

---

## 1. Executive Summary

| Metric | Value |
|--------|-------|
| Total capabilities assessed | 8 |
| Capabilities READY for generation | 4 (50%) |
| Capabilities PARTIAL | 3 (37.5%) |
| Capabilities BLOCKED | 1 (12.5%) |
| Critical blockers (must resolve before any generation) | 3 |
| Total artifact count (Document 16) | 54 |
| Artifacts with HIGH confidence | 40 (74%) |
| Artifacts INFERRED | 10 (19%) |
| Artifacts BLOCKED | 4 (7%) |
| Estimated generation effort with current knowledge | 7–9 engineer-days |
| Estimated effort after resolving all blockers | 12–15 engineer-days |

**Overall readiness score: 71 / 100**

Generation can begin on the domain core (Phase 1–5 of Document 16) immediately. PublicApi, Azure IaC, and email functionality require blocker resolution before those phases complete.

---

## 2. Pre-Generation Blocker Checklist

These three items BLOCK all production generation. They must be resolved in this order:

| Priority | Blocker | ID | Resolution Action | Estimated Effort |
|----------|---------|-----|------------------|-----------------|
| P0 | JWT signing key hardcoded in source | MIS-001 + TD-01 | Generate 256-bit random key; store in Azure Key Vault under `jwt-signing-key`; remove `AuthorizationConstants.JWT_SECRET_KEY` from source | 1 day |
| P0 | Admin password hardcoded in source | MIS-002 + TD-02 | Remove `DEFAULT_PASSWORD` from `AppIdentityDbContextSeed.cs`; read from Key Vault; add forced password-reset on first login | 1 day |
| P0 | JWT issuer/audience not validated | MIS-003 + TD-03 | Define production URI values; set `ValidateIssuer=true`, `ValidateAudience=true` in `PublicApi/Program.cs` | 2 hours |

> **Rule:** Any generated file that touches JWT configuration, authentication, or database seeding must pass validation gates G-SEC-01, G-SEC-02, G-SEC-03 before being committed.

---

## 3. Capability Readiness Scores

### CAP-001 — Catalog Browsing

| Dimension | Score | Notes |
|-----------|-------|-------|
| Domain model | 10/10 | CatalogItem, CatalogBrand, CatalogType fully mapped |
| Data schema | 10/10 | All 3 tables + HiLo sequence confirmed |
| Application service | 10/10 | CatalogViewModelService, CachedCatalogViewModelService confirmed |
| API endpoints | 10/10 | GET /api/catalog-items, /brands, /types fully specified |
| Web pages | 5/10 | Catalog list page INFERRED; source not extracted |
| NFRs | 9/10 | 30s cache confirmed; Task.Delay must be removed |
| Security | 9/10 | Anonymous access correct; [AllowAnonymous] confirmed |
| **Total** | **63/70 = 90%** | **READY** |

---

### CAP-002 — Basket Management

| Dimension | Score | Notes |
|-----------|-------|-------|
| Domain model | 10/10 | Basket aggregate, BasketItem, all methods confirmed |
| Data schema | 10/10 | Baskets + BasketItems tables confirmed |
| Application service | 10/10 | BasketService fully specified (GEN-SVC-01) |
| API endpoints | N/A | No basket REST API; Web-only |
| Web pages | 4/10 | Basket page INFERRED; only cookie management confirmed |
| NFRs | 8/10 | 10-year anonymous cookie confirmed; non-atomic transfer gap |
| Security | 8/10 | Anonymous basket cookie missing HttpOnly flag (TD-10) |
| **Total** | **50/60 = 83%** | **READY** |

---

### CAP-003 — Checkout and Order Placement

| Dimension | Score | Notes |
|-----------|-------|-------|
| Domain model | 10/10 | Order aggregate, Address VO, CatalogItemOrdered VO confirmed |
| Data schema | 10/10 | Orders + OrderItems tables confirmed; column constraints confirmed |
| Application service | 10/10 | OrderService fully specified (GEN-SVC-02) |
| API endpoints | N/A | No order REST API; Web-only |
| Web pages | 3/10 | Checkout.cshtml.cs partially confirmed; address HARDCODED (TD-09) |
| NFRs | 7/10 | No order status field; basket not cleared after order |
| Security | 9/10 | [Authorize] confirmed; cookie auth |
| **Total** | **49/60 = 82%** | **PARTIAL — blocked on MIS-007** |

---

### CAP-004 — Identity and Authentication

| Dimension | Score | Notes |
|-----------|-------|-------|
| Domain model | 10/10 | ApplicationUser confirmed; Buyer confirmed as dead code |
| Data schema | 10/10 | ASP.NET Identity tables confirmed |
| Application service | 8/10 | IdentityTokenClaimService confirmed; key hardcoded (TD-01) |
| API endpoints | 10/10 | POST /api/authenticate fully specified |
| Web pages | 9/10 | Login, Register, ConfirmEmail confirmed; basket transfer on login confirmed |
| NFRs | 8/10 | Cookie validity 60min confirmed; JWT 7-day confirmed |
| Security | 4/10 | 3 critical security gaps (TD-01, TD-02, TD-03) — all PRE-GENERATION BLOCKERS |
| **Total** | **59/70 = 84%** | **PARTIAL — 3 P0 blockers** |

---

### CAP-005 — Catalog Administration (BlazorAdmin)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Domain model | 10/10 | CatalogItem CRUD operations confirmed |
| Data schema | 10/10 | Full CatalogDB schema confirmed |
| Application service | 10/10 | CatalogItemService, CachedCatalogItemServiceDecorator confirmed |
| API endpoints | 10/10 | POST, PUT, DELETE /api/catalog-items fully specified |
| UI components | 8/10 | List.razor, Create/Edit/Delete modals confirmed; items-per-page=10 confirmed |
| NFRs | 9/10 | 60s cache, immediate invalidation, 3s toast confirmed |
| Security | 8/10 | JWT Bearer, Administrators role enforced; no timeout on BlazorAdmin HTTP calls |
| **Total** | **65/70 = 93%** | **READY** |

---

### CAP-006 — Order History

| Dimension | Score | Notes |
|-----------|-------|-------|
| Domain model | 10/10 | Order aggregate with OrderItems confirmed |
| Data schema | 10/10 | CustomerOrdersWithItemsSpecification confirmed |
| Application service | 10/10 | GetMyOrdersHandler (MediatR) + OrderViewModelService confirmed |
| API endpoints | N/A | No order history REST API |
| Web pages | 4/10 | Order history page INFERRED; source not extracted |
| NFRs | 8/10 | No pagination on order history noted |
| Security | 9/10 | [Authorize] confirmed (INFERRED for order history page) |
| **Total** | **51/60 = 85%** | **PARTIAL — Web page INFERRED** |

---

### CAP-007 — User Registration

| Dimension | Score | Notes |
|-----------|-------|-------|
| Domain model | 9/10 | ApplicationUser confirmed; email confirmation confirmed |
| Data schema | 10/10 | IdentityDB tables confirmed |
| Application service | 10/10 | UserManager operations confirmed |
| API endpoints | N/A | No registration REST API |
| Web pages | 10/10 | Register.cshtml.cs confirmed |
| NFRs | 5/10 | Email sender is a complete stub (TD-08); blocked on MIS-006 |
| Security | 9/10 | Password hashing confirmed (PBKDF2); TwoFactorEnabled=false by default |
| **Total** | **53/60 = 88%** | **PARTIAL — email sender stub (MIS-006)** |

---

### CAP-008 — Anonymous Basket Transfer

| Dimension | Score | Notes |
|-----------|-------|-------|
| Domain model | 10/10 | Basket.SetNewBuyerId(), TransferBasketAsync() confirmed |
| Data schema | 10/10 | Baskets.BuyerId transition confirmed |
| Application service | 10/10 | BasketService.TransferBasketAsync fully specified |
| API endpoints | N/A | Web-only |
| Web pages | 10/10 | Login.cshtml.cs basket transfer on login confirmed |
| NFRs | 6/10 | Non-atomic 3-SaveChanges flow — known gap (DQ-002) |
| Security | 8/10 | GUID cookie generation; anonymousId validated |
| **Total** | **54/60 = 90%** | **READY** |

---

## 4. Generation Phase Readiness

| Phase | Name | Status | Readiness | Blockers |
|-------|------|--------|-----------|---------|
| 1 | Domain Core | READY | 97% | None |
| 2 | Specifications | READY | 98% | None |
| 3 | Application Services | READY | 95% | None |
| 4 | Infrastructure | READY | 90% | None |
| 5 | PublicApi | READY_WITH_CONDITIONS | 82% | G-SEC-01, G-SEC-02, G-SEC-03 must pass first |
| 6 | Web Application | PARTIAL | 68% | MIS-004, MIS-007 |
| 7 | BlazorAdmin | READY | 92% | None |
| 8 | Infrastructure as Code | PARTIAL | 65% | MIS-005 (PublicApi Azure), MIS-012 (firewall) |

---

## 5. Knowledge Gap Impact Analysis

### Critical Gaps (block generation or produce incorrect output)

| Gap | Impact | Affected Artifacts | Resolution |
|-----|--------|--------------------|-----------|
| MIS-001: JWT key | Generated JWT config would hardcode insecure key | ART-027, ART-040 | Key Vault secret |
| MIS-002: Admin password | Seeding would use insecure default | ART-030 | Key Vault secret |
| MIS-003: JWT issuer/audience | Token validation misconfigured | ART-040 | Architecture decision |
| MIS-007: Address form | Checkout generates hardcoded address | ART-044 | UI form design |

### High-Priority Gaps (incomplete feature generation)

| Gap | Impact | Affected Artifacts | Resolution |
|-----|--------|--------------------|-----------|
| MIS-004: Web pages | Catalog, basket, order pages are INFERRED | ART-044, catalog/basket pages | Extract src/Web/Pages/ |
| MIS-005: PublicApi Azure | No Azure deployment for PublicApi | ART-053 | OQ-006 decision |
| MIS-006: Email provider | Registration email non-functional | ART-028 | SendGrid API key |
| MIS-008: Order status | No order fulfilment workflow | Multiple | Business decision |

### Medium-Priority Gaps (quality improvements)

| Gap | Impact | Resolution |
|-----|--------|-----------|
| MIS-009: Unique index migration | DQ-001 duplicates possible | Add to EF config |
| MIS-010: EnableRetryOnFailure all envs | Docker/PublicApi have no retry | Fix GEN-INFRA-01 |
| MIS-011: HTTP timeout | Unbounded BlazorAdmin HTTP calls | Configure HttpClient |
| MIS-012: SQL firewall | All IPs can access SQL | Restrict in Bicep |

---

## 6. Technical Debt Paydown Priority

Technical debt items must be resolved during or before generation (not after):

| Priority | ID | Item | When to Resolve |
|----------|----|------|-----------------|
| P0 | TD-01 | JWT key hardcoded | Before Phase 5 |
| P0 | TD-02 | DEFAULT_PASSWORD hardcoded | Before Phase 4 |
| P0 | TD-03 | JWT validation flags | During Phase 5 |
| P1 | TD-04 | exception.Message in 500 responses | During Phase 5 |
| P1 | TD-05 | EnableRetryOnFailure missing in Docker/PublicApi | During Phase 4 |
| P1 | TD-07 | Task.Delay(1000) in catalog endpoint | During Phase 5 |
| P1 | TD-08 | EmailSender stub | During Phase 6 |
| P1 | TD-09 | Hardcoded shipping address | During Phase 6 |
| P1 | TD-10 | [Authorize]+[AllowAnonymous] conflict on UserController | During Phase 6 |
| P1 | TD-11 | SQL firewall open to all IPs | During Phase 8 |
| P1 | TD-12 | PublicApi has no Azure deployment | During Phase 8 |
| P2 | TD-13 | Bootstrap 3.4.1 EOL | Phase 6 (or separate sprint) |
| P2 | TD-14/15 | Outdated GitHub Actions v1/v2 | During Phase 8 |
| P3 | TD-16 | Dead SignalR client reference | During Phase 6 |

---

## 7. Open Questions Requiring Decisions Before Generation Completes

| ID | Question | Affects | Owner |
|----|----------|---------|-------|
| OQ-001 | Should Buyer/PaymentMethod be removed or retained for future use? | Phase 1 entity list | Architecture |
| OQ-002 | Should MediatR be extended to write-side, or replaced with direct service calls? | Phase 3 services | Architecture |
| OQ-003 | What email provider should replace the stub EmailSender? | Phase 4 infra | Operations |
| OQ-004 | Should basket be cleared after order creation? | Phase 3 OrderService | Business |
| OQ-005 | What RTO/RPO are required? (DR targets) | Phase 8 IaC | Business |
| OQ-006 | Should PublicApi be deployed as a separate Azure App Service or merged with Web? | Phase 8 IaC | Architecture |
| OQ-007 | Should Application Insights be added? What workspace ID? | Phase 8 IaC | Operations |
| OQ-008 | Should OrderStatus enum be added? What states? | Phase 1 domain | Business |
| OQ-009 | What is the correct value for ValidIssuer URI? | Phase 5 PublicApi | Architecture |
| OQ-010 | Should IMemoryCache cookie revocation be migrated to Redis for scale-out? | Phase 6 Web | Architecture |
| OQ-011 | Is the artificial 1,000ms catalog delay needed for any staging/demo purpose? | Phase 5 PublicApi | Product |
| OQ-012 | Should BlazorAdmin auth poll interval be configurable without redeployment? | Phase 7 Blazor | Architecture |

---

## 8. Recommended Generation Sequence

Given current knowledge state, the optimal generation order is:

```
Week 1 — Foundation (no blockers)
    Day 1: Resolve P0 blockers (TD-01, TD-02, TD-03) — PREREQUISITE
    Day 2: Generate Phase 1 (Domain Core) + Phase 2 (Specifications)
    Day 3: Generate Phase 3 (Application Services) + unit tests
    Day 4: Generate Phase 4 (Infrastructure) + EF migrations
    Day 5: Generate Phase 7 (BlazorAdmin) + its service tests

Week 2 — API and Web
    Day 6: Generate Phase 5 (PublicApi) — requires P0 blockers resolved
    Day 7: Generate Phase 6 (Web) — register/login/order history pages
    Day 8: Complete Phase 6 (checkout page) — requires MIS-007 resolution
    Day 9: Generate Phase 8 (IaC — Bicep) — requires OQ-006 decision
    Day 10: Integration testing against real SQL Server + CI/CD pipeline

Post-Week 2 — Remaining gaps
    - Email integration (MIS-006)
    - Web catalog/basket/order pages if MIS-004 not resolved by Week 1
    - Bootstrap upgrade (TD-13)
```

---

## 9. Readiness Score Breakdown

| Category | Score | Max | Percentage |
|----------|-------|-----|-----------|
| Domain knowledge completeness | 38 | 40 | 95% |
| API contract completeness | 18 | 20 | 90% |
| Data model completeness | 19 | 20 | 95% |
| Security architecture completeness | 12 | 20 | 60% |
| Infrastructure completeness | 10 | 16 | 63% |
| Web UI completeness | 5 | 14 | 36% |
| NFR completeness | 14 | 16 | 88% |
| Test coverage knowledge | 5 | 10 | 50% |
| **TOTAL** | **121** | **156** | **77.6%** |

**Adjusted overall readiness (after P0 blocker weight): 71 / 100**

> Score penalizes for security blockers because they affect all generated output, not just security-specific components. Once TD-01, TD-02, and TD-03 are resolved, the adjusted score rises to approximately 84/100.
