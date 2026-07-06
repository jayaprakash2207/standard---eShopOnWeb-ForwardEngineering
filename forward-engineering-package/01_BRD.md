# Business Requirements Document (BRD)

> ⚠️ **DISC-001 (verified 2026-06-25):** Any reference to `CatalogItem` stock/reorder fields or a stock-reorder
> behavior is a **verified discrepancy** — those fields are absent from the real `eShopOnWeb` source. See
> [`../EVIDENCE_VERIFICATION_REPORT.md`](../EVIDENCE_VERIFICATION_REPORT.md).

**System:** eShopOnWeb (authoritative system name flagged **"unknown"** in source evidence — see OQ-007 / ASSUMP-007)
**Source of truth:** `ENTERPRISE_KNOWLEDGE_GRAPH.json`
**Date:** 2026-06-23
**Status:** Forward-engineering input baseline. Every requirement traces to graph node ids; no capabilities, actors, entities, or rules are invented.

> **Technology note.** This document is **technology-neutral**. Where a stack is named it is labelled **Current (legacy)**. The graph's `target_stack` is **empty (0 nodes)**, so any target technology referenced later in the programme is a **neutral option** ("not in legacy evidence"), never an asserted discovery.

---

## 1. Executive Summary

eShopOnWeb is a reference e-commerce storefront whose business capability model, as consolidated in the Enterprise Knowledge Graph, comprises **39 capabilities**, **10 business processes**, **5 actors**, **15 data entities**, **47 application services/modules**, **13 interfaces**, **55 APIs**, and **26 current-stack technologies**. The platform enables an online retail value stream that takes a shopper from catalog browsing through basket management to a confirmed, priced order, supported by an administrative catalog back-office and an identity/authentication foundation.

Functionally, the implemented system delivers five top-level (L1) capabilities: **Catalog Management** (BIZ-CAP-001), **Basket / Shopping Cart Management** (BIZ-CAP-010), **Order Management** (BIZ-CAP-017), **Identity & Authentication** (BIZ-CAP-029), and **Admin Catalog Operations (Blazor)** (BIZ-CAP-035). A sixth L1 capability, **Buyer / Customer Profile Management** (BIZ-CAP-024), is only partially realised: its **Buyer** (DATA-ENT-010) and **PaymentMethod** (DATA-ENT-011) entities are `persisted=false`, `status=aspirational/unimplemented` (RC-002), and the payment sub-capabilities (BIZ-CAP-027/028) are `inferred`, confidence `LOW`.

This BRD captures the business goals, drivers, scope, stakeholders, assumptions, constraints, and measurable success criteria that govern the forward-engineering (modernisation / re-platforming) of the system. Goals and drivers are **derived strictly from the graph's capabilities, processes, actor and value-stream evidence** — the graph contains no separate `motivation_model` node, so motivation is inferred from this evidence base and gaps are flagged with assumptions (ASMP-FE-###). The defining engineering constraints are a **module dependency cycle** (APP-DEP-001), **weak bounded-context boundaries** with several **high-coupling** modules, a **shared persistence context** crossing three contexts (DATA-REPO-003), pervasive **version-unknown** technology nodes, and an **unknown authoritative system name** (OQ-007).

---

## 2. Business Goals

Goals are derived from the capability hierarchy, process models, and the two value streams evidenced in the graph (Customer Browse-to-Order and Catalog Content Management). Each goal aggregates a set of capabilities; full traceability is in Section 10.

| Goal ID | Business Goal | Derived From (evidence) |
|---------|---------------|--------------------------|
| **G-01** | **Enable self-service product discovery** — let customers and anonymous shoppers browse and find products by brand and type. | BIZ-CAP-001/002/003/004/005/006/007/008; BIZ-PROC-001 (Browse Catalog); value stream "Customer Browse-to-Order" stage 1. |
| **G-02** | **Provide a reliable shopping basket** — allow items to be added, quantities adjusted, and carts cleaned up with session continuity across anonymous-to-registered transitions. | BIZ-CAP-010/011/012/013/014/015/016; BIZ-PROC-002/003/004; business rules BR005/BR006/BR007. |
| **G-03** | **Convert baskets into confirmed, correctly-priced orders** — perform checkout with item snapshotting, shipping address capture, empty-basket protection, and total calculation. | BIZ-CAP-017/018/019/020/021/022/023; BIZ-PROC-005; business rules BR009/BR010/BR011/BR012. |
| **G-04** | **Secure access through identity and authentication** — authenticate users, issue tokens, enforce role-based access, and seed identity data. | BIZ-CAP-029/030/031/032/033/034; BIZ-PROC-007/010. |
| **G-05** | **Empower back-office catalog administration** — let administrators list, create, and delete catalog items with cache refresh, separate from the storefront. | BIZ-CAP-035/036/037/038/039; BIZ-PROC-006; business rules BR001/BR002/BR003/BR004; value stream "Catalog Content Management". |
| **G-06** | **(Future) Manage buyer profile and payment information** — maintain a buyer record distinct from authentication identity and capture payment methods. | BIZ-CAP-024/025/026/027/028; BIZ-PROC-008; DATA-ENT-010/011 (aspirational/unimplemented, RC-002). **OUT of current scope** — see Section 4. |
| **G-07** | **Modernise the platform into independently evolvable bounded contexts** — re-engineer the implemented capabilities into the seven decided contexts (BC-01..BC-07) with clean boundaries, while preserving observable behaviour. | DECISIONS.json `bounded_contexts`; coupling risks RISK-CYCLE-001 / RISK-SHARED-DBCTX-001 / RISK-EFREPO-001; APP-DEP-001. |

> **Gap flagged.** The graph has **no `motivation_model` / strategy node**; goals G-01..G-05 are inferred from capability + process + value-stream evidence and G-07 from the decided contexts. See **ASMP-FE-005**.

---

## 3. Business Drivers

Drivers explain *why* the goals matter; they are inferred from operating-model and value-stream evidence and from the engineering risks recorded in the graph.

| Driver ID | Driver | Evidence basis |
|-----------|--------|----------------|
| **D-01** | **Self-service customer experience.** The operating model assigns customers a self-service role spanning browse, basket, and order. | Actor BIZ-ACT-001 (operating model: "Self-service role — browses the catalog, manages their own basket, places their own orders"); BIZ-ACT-002 anonymous shopper. |
| **D-02** | **Frictionless conversion from anonymous to registered shopping.** Anonymous baskets must survive login/registration to avoid losing carts at the point of conversion. | BIZ-CAP-015/016; BIZ-PROC-003; BIZ-ACT-002. |
| **D-03** | **Order integrity and pricing correctness.** Orders must capture an immutable snapshot of what was bought and compute totals deterministically, independent of later catalog changes. | BR009 (valid item id/name/picture), BR010 (total = Σ unit price × qty), BR011 (buyer id required), BR012 (block empty-basket checkout); BIZ-PROC-005; VO-03 snapshot. |
| **D-04** | **Trusted access control.** Authentication, token issuance, and role/claims-based authorization are prerequisites for basket transfer, order buyer-id, and admin operations. | BIZ-CAP-029..034; BIZ-PROC-007; security TECH-SEC-001/002/003/004. |
| **D-05** | **Operational catalog agility.** Administrators need a dedicated back-office to keep product content current, with cache refresh so changes are reflected. | BIZ-CAP-035..039; BIZ-PROC-006; BIZ-ACT-003 (operating model: "Back-office role — maintains the product catalog"); value stream "Catalog Content Management". |
| **D-06** | **Automated, hands-off operations.** A system/service account performs seeding, token issuance, URI composition, and total calculation without a human operator. | BIZ-ACT-004 (operating model: "Automated role — startup data seeding, token issuance, image path composition, total calculations"); BIZ-PROC-009/010. |
| **D-07** | **Architectural debt remediation.** A module dependency cycle, weak boundaries, high-coupling components, and a shared DbContext block independent deployability and raise change risk. | APP-DEP-001 (cycle), APP-SVC-001 coupling 13 / APP-SVC-022 EfRepository coupling 16 (APP-DEP-009), DATA-REPO-003 shared context; RISK-CYCLE-001 / RISK-SHARED-DBCTX-001 / RISK-EFREPO-001. |
| **D-08** | **Security and compliance hardening.** Multiple High-severity findings (hardcoded credentials, unconfirmed JWT/CORS enforcement, no scanning, no audit/compliance controls) must be addressed during modernisation. | TECH-SEC-008..017; OQ-005. |

---

## 4. Scope

### 4.1 In Scope

| Area | Capabilities / Processes (ids) |
|------|-------------------------------|
| Catalog browsing, classification, reference data, seeding | BIZ-CAP-001..009; BIZ-PROC-001, BIZ-PROC-009 |
| Basket lifecycle, quantity rules, cleanup, session continuity, anonymous transfer | BIZ-CAP-010..016; BIZ-PROC-002, BIZ-PROC-003, BIZ-PROC-004 |
| Checkout, order creation, item snapshot, empty-basket protection, total calculation, order history | BIZ-CAP-017..023; BIZ-PROC-005 |
| Authentication, token issuance, access control, identity seeding | BIZ-CAP-029..034; BIZ-PROC-007, BIZ-PROC-010 |
| Administrative catalog operations (list / create / delete / cache refresh) | BIZ-CAP-035..039; BIZ-PROC-006 |
| Re-engineering implemented capabilities into bounded contexts BC-01..BC-05 and the cross-cutting shell BC-07, breaking APP-DEP-001 and splitting DATA-REPO-003 | DECISIONS.json contexts; coupling risks RISK-CYCLE-001/-SHARED-DBCTX-001/-EFREPO-001 |
| Preservation of the 55 evidenced APIs and 13 interfaces during modernisation (functional vs physical ownership per ASMP-FE-004) | APP-API-001..055; APP-IF-001..013 |

### 4.2 Out of Scope (current) / Future

| Item | Reason / status (ids) |
|------|------------------------|
| **Buyer / Customer Profile context (BC-06)** — buyer record and its lifecycle | `aspirational/unimplemented` (RC-002); BIZ-CAP-024/025/026; BIZ-PROC-008 has 0 detailed steps; DATA-ENT-010 **Buyer** `persisted=false`. Today the buyer reference is satisfied by **ApplicationUser** (BC-04). **OUT — future, ASMP-FE-003.** |
| **Payment Method Management** — payment information capture/storage | BIZ-CAP-027/028 `inferred`, confidence `LOW`; DATA-ENT-011 **PaymentMethod** `persisted=false`; DATA-REL-012 (Buyer 1..* PaymentMethod) aspirational; DATA-AGG-003 BuyerAggregate aspirational. **OUT — future.** |
| **Email / order notifications** | BIZ-ACT-005 Notification Recipients and IEmailSender (APP-IF-008) noted "present in code but not yet implemented." **OUT — future.** |
| **Stock reorder workflow** | No process/business-rule node exists; EVT-12 inferred only from CatalogItem stock attributes. **OUT — confirm before any work (ASMP-FE-002).** |
| **CatalogItemDetails (DATA-ENT-014)** | `persisted=false`, aspirational/unimplemented — design input only. **OUT.** |
| **Multi-currency pricing** | No currency attribute on any entity; a Money VO with currency would be a NEW design element (ASMP-FE-001). **OUT unless explicitly mandated.** |
| **Target technology selection** | `target_stack` is empty (0 nodes). Stack choice is a downstream decision, offered as neutral options, not part of this BRD. |

---

## 5. Stakeholders

Derived from `business.actors` (BIZ-ACT-###) with operating-model and stakeholder-map evidence.

| Actor ID | Stakeholder | Type | Role / interest | Permission level |
|----------|-------------|------|------------------|------------------|
| **BIZ-ACT-001** | Customer / Buyer | human | Self-service: browses catalog, manages own basket, transfers anonymous basket on login, places orders, views history. Primary beneficiary of G-01/G-02/G-03. | Standard |
| **BIZ-ACT-002** | Anonymous Shopper | human | Unauthenticated visitor who browses and builds an anonymous basket later merged on login. Drives D-02. | *(unauthenticated)* † |
| **BIZ-ACT-003** | Administrator | human | Back-office: creates/updates/deletes catalog items, manages brands/types via the Blazor admin interface. Owner of G-05. | Admin |
| **BIZ-ACT-004** | System / Service Account | system | Automated: startup seeding, token issuance, URI composition, basket/order total calculation; also listed for notification email (not yet implemented). Owner of D-06. | Elevated |
| **BIZ-ACT-005** | Notification Recipients | external | Customers expected to receive order/email notifications via the Email Sender component — "present in code but not yet implemented." Future stakeholder only. | n/a |

> † **Permission-level provenance.** *Standard* (Customer/Buyer), *Admin* (Administrator), and *Elevated* (System / Service Account) are evidenced explicitly in the graph stakeholder-map anchors (`ba_documents/06_stakeholder_map.md` "Permission Level: …" on each actor node). The *(unauthenticated)* label for the Anonymous Shopper is an **inference** — BIZ-ACT-002 has no permission-level field; the graph describes it only as an "Unauthenticated storefront visitor." Treat that one label as inferred, not evidence-derived.
>
> **Engineering stakeholders** (modernisation programme owners, architects) are implied by the forward-engineering mandate and the recorded open questions (e.g. OQ-001 merge decision, OQ-004 cycle reality, OQ-005 JWT/CORS). They are not actor nodes in the graph; see ASMP-FE-006.

---

## 6. Assumptions

### 6.1 Graph assumptions (reused verbatim — ASSUMP-###)

| ID | Assumption (summary) | Impact |
|----|----------------------|--------|
| **ASSUMP-001** | Web module (APP-SVC-006) and deployable eshopwebmvc are the same unit, merged. | Single canonical Web node; split via merged_from if needed. |
| **ASSUMP-002** | PublicApi module (APP-SVC-011) and deployable eshoppublicapi are the same unit, merged. | API cross-links use APP-SVC-011. |
| **ASSUMP-003** | ApplicationCore, Infrastructure, SharedContracts each appear as both module and component and are merged. | Fewer duplicate nodes; facets preserved. |
| **ASSUMP-004** | Route/endpoint ownership assigned by source-file path (Web / PublicApi / BlazorAdmin). | service_to_api links derive from source_file; handler-module noted separately. |
| **ASSUMP-005** | Browse Catalog (BIZ-PROC-001) touches CatalogItem/CatalogBrand/CatalogType (DATA-ENT-001/002/003) and Adjust Basket (BIZ-PROC-004) touches Basket/BasketItem (DATA-ENT-004/005), though these are value-stream stages, not step-level processes. | Those process_to_entity links carry LOW/MEDIUM confidence. |
| **ASSUMP-006** | Role (DATA-ENT-009) owned by Identity via AppIdentityDbContext, mirroring ApplicationUser. | entity_to_service link MEDIUM confidence (0.7). |
| **ASSUMP-007** | Authoritative product name treated as "eShopOnWeb" while source evidence flagged it "unknown". | Naming only; no node semantics affected. |

### 6.2 Forward-engineering assumptions (reused from DECISIONS.json + new)

| ID | Assumption | Basis | Impact |
|----|------------|-------|--------|
| **ASMP-FE-001** | A Money VO with explicit currency is NOT derivable; Price/UnitPrice are bare decimals. | DATA-ENT-001/005/007 key_attributes; empty target_stack. | Multi-currency is a NEW design element if required; default amount-only. |
| **ASMP-FE-002** | StockReorderTriggered (EVT-12) inferred only from OnReorder/RestockThreshold attributes; no reorder process/rule exists. | DATA-ENT-001 attributes; absence of reorder process. | Confirm with stakeholders before any reorder work. |
| **ASMP-FE-003** | Buyer/Customer Profile (BC-06) surfaced only from aspirational nodes; buyer reference today is ApplicationUser. | DATA-ENT-010/011 persisted=false (RC-002); DATA-REL-008/009 soft refs; BIZ-CAP-027/028 inferred LOW. | Do not generate Buyer/Payment persistence without an explicit decision. |
| **ASMP-FE-004** | Routes served by Web shell (APP-SVC-006) and the authenticate endpoint in PublicApi (APP-SVC-011) are attributed to functional contexts (BC-02/03/04), physical hosting to BC-07. | cross_links.service_to_api; ASSUMP-001/002. | Distinguish functional ownership from physical hosting downstream; honour OQ-009. |
| **ASMP-FE-005** *(new)* | Business goals/drivers (G-01..G-06, D-01..D-08) are inferred from capabilities, processes, actors, and value-stream evidence because the graph has **no motivation_model/strategy node**. | metadata.domains (no motivation node); ba_documents 02_value_stream / 09_operating_model anchors only. | Goals/drivers are evidence-grounded inferences, not asserted strategy; validate with business owners. |
| **ASMP-FE-006** *(new)* | The modernisation programme team (architects, platform owners) is an implicit stakeholder set not represented as a BIZ-ACT node. | No engineering actor in business.actors; forward-engineering mandate + OQ-001/004/005. | Include programme stakeholders in governance; do not treat as a discovered business actor. |
| **ASMP-FE-007** *(new)* | "Success" for modernisation = behaviour-preserving re-engineering of implemented capabilities; aspirational nodes (BC-06, payment, notifications, reorder) are explicitly excluded from acceptance. | RC-002 status flags; DECISIONS.json generation_priorities (BC-06 priority 7, "generated last and only on an explicit decision"). | Acceptance criteria (Section 8) scope to implemented capabilities only. |

---

## 7. Constraints

| ID | Constraint | Evidence (ids) |
|----|------------|-----------------|
| **C-01** | **Module dependency cycle.** Admin → ApplicationCore → Basket → Catalog → DataAccess → Identity → Order → Web → (back to Admin). Spans BC-01..BC-05 and BC-07; must be broken before contexts can deploy independently. Its reality vs static-resolution artifact is **unresolved**. | APP-DEP-001; RISK-CYCLE-001; OQ-004 |
| **C-02** | **High legacy coupling / weak boundaries.** Catalog module coupling 13 (APP-SVC-001, readiness Blocked); EfRepository coupling 16 (APP-SVC-022, APP-DEP-009); direct endpoint/PageModel → repository violations (APP-DEP-002..008); UriComposer high-coupling (APP-DEP-010). | APP-SVC-001/003/006/007/022; APP-DEP-002..010; RISK-EFREPO-001 |
| **C-03** | **Shared persistence boundary.** CatalogContext (DATA-REPO-003) persists Catalog (BC-01), Basket (BC-02) and Order (BC-03) entities in one DbContext — one persistence boundary crossing three contexts; must be split per context. | DATA-REPO-003; RISK-SHARED-DBCTX-001; OQ-008 |
| **C-04** | **Version-unknown technology.** Most current-stack nodes are `(not declared)` / `unknown` version, confidence LOW (e.g. EF Core TECH-CUR-005, providers TECH-CUR-006/007, MediatR TECH-CUR-011, DB engines TECH-CUR-020/021). Modernisation planning cannot assume specific versions. | TECH-CUR-004..022, 024, 025 (version not declared / unknown) |
| **C-05** | **Unknown authoritative system name.** Source business evidence flagged the authoritative system name as "unknown"; the label "eShopOnWeb" is a folder-derived convenience. | OQ-007; ASSUMP-007; metadata.system_name |
| **C-06** | **Aspirational data is not migration data.** Buyer/PaymentMethod/CatalogItemDetails are `persisted=false`; no rows to migrate; design input only. | DATA-ENT-010/011/014; RC-002 |
| **C-07** | **Security findings outstanding.** Hardcoded DB credentials, unconfirmed JWT enforcement, no CORS policy found, port 1433 exposed, no TLS for container traffic, no SAST/secret/dependency scanning, no audit/compliance controls. | TECH-SEC-008..017; OQ-005 |
| **C-08** | **Synthetic interface verbs.** ROUTE/CLI method labels on some APP-API nodes are synthetic (source records method="unknown"); do not treat as evidenced HTTP verbs. | OQ-009; APP-API-009/010/011/039/040/053/054/055 |
| **C-09** | **Technology neutrality mandate.** No single stack may be hard-coded; legacy stack labelled "Current (legacy)"; target_stack is empty (0 nodes). | metadata; empty target_stack |

---

## 8. Success Criteria

Measurable, behaviour-preserving criteria tied to capabilities. Scope is implemented capabilities only (ASMP-FE-007).

| ID | Success Criterion (measurable) | Tied capabilities / processes |
|----|--------------------------------|-------------------------------|
| **SC-01** | 100% of the 55 evidenced APIs (APP-API-001..055) retain equivalent observable behaviour post-modernisation, validated against process flows. | All BIZ-PROC; APP-API-001..055 |
| **SC-02** | Catalog browse and classification return brand/type-filtered results for all seeded items, with 0 regressions against BR001/BR002/BR003/BR004 validation on create. | BIZ-CAP-001..009; BIZ-PROC-001/006/009 |
| **SC-03** | Basket operations honour BR005 (consolidate quantity), BR006 (remove zero-qty line), BR007 (reject negative qty) in 100% of tested cases; anonymous→registered transfer loses 0 basket items. | BIZ-CAP-010..016; BIZ-PROC-002/003/004 |
| **SC-04** | Checkout produces an order only for non-empty baskets (BR012), with an immutable item snapshot (BR009), a buyer id (BR011), and a total equal to Σ(unit price × quantity) (BR010) — 0 calculation discrepancies. | BIZ-CAP-017..023; BIZ-PROC-005 |
| **SC-05** | Authentication issues a signed token with identity + role claims only for valid, non-locked-out credentials; role/claims authorization enforced on all admin operations. | BIZ-CAP-029..034; BIZ-PROC-007/010; TECH-SEC-001/002/004 |
| **SC-06** | Administrators can list/create/delete catalog items with cache refresh reflecting changes within one refresh cycle; 0 stale-cache defects on the admin surface. | BIZ-CAP-035..039; BIZ-PROC-006 |
| **SC-07** | The module dependency cycle (APP-DEP-001) is eliminated — verified by 0 cyclic edges in the target module dependency graph — and each context BC-01..BC-05 deploys independently of the others. | APP-DEP-001; RISK-CYCLE-001 |
| **SC-08** | The shared CatalogContext (DATA-REPO-003) is split so that no single persistence boundary spans BC-01/BC-02/BC-03; AppIdentityDbContext remains isolated to BC-04. | DATA-REPO-003/004; RISK-SHARED-DBCTX-001 |
| **SC-09** | Direct endpoint/PageModel → EfRepository violations (APP-DEP-002..008) are removed; endpoints route through application services; EfRepository coupling materially reduced from the recorded score of 16. | APP-DEP-002..009; RISK-EFREPO-001 |
| **SC-10** | All High-severity security findings (TECH-SEC-008..017) have a confirmed disposition: credentials externalised, JWT/CORS enforcement confirmed (closing OQ-005), scanning enabled, audit logging defined. | TECH-SEC-008..017; OQ-005 |

---

## 9. Traceability to Capabilities

Business goal → BIZ-CAP ids (and supporting processes).

| Goal | BIZ-CAP ids | Supporting BIZ-PROC ids | Bounded context |
|------|-------------|--------------------------|------------------|
| **G-01** Self-service product discovery | BIZ-CAP-001, 002, 003, 004, 005, 006, 007, 008, 009 | BIZ-PROC-001, BIZ-PROC-009 | BC-01 Catalog |
| **G-02** Reliable shopping basket | BIZ-CAP-010, 011, 012, 013, 014, 015, 016 | BIZ-PROC-002, BIZ-PROC-003, BIZ-PROC-004 | BC-02 Basket |
| **G-03** Convert baskets into orders | BIZ-CAP-017, 018, 019, 020, 021, 022, 023 | BIZ-PROC-005 | BC-03 Ordering |
| **G-04** Secure access (identity) | BIZ-CAP-029, 030, 031, 032, 033, 034 | BIZ-PROC-007, BIZ-PROC-010 | BC-04 Identity & Access |
| **G-05** Back-office catalog administration | BIZ-CAP-035, 036, 037, 038, 039 | BIZ-PROC-006 | BC-05 Catalog Administration |
| **G-06** *(Future / OUT)* Buyer profile & payment | BIZ-CAP-024, 025, 026, 027*, 028* | BIZ-PROC-008 | BC-06 (Aspirational) |
| **G-07** Modernise into bounded contexts | *(all implemented capabilities above)* | *(all implemented processes above)* | BC-01..BC-05, BC-07 |

\* BIZ-CAP-027/028 are `inferred`, confidence `LOW`; G-06 is OUT of current scope (Section 4.2, ASMP-FE-003).

> **Confidence note.** BIZ-CAP-024/025/026 are `ACTIVE/MEDIUM`; BIZ-CAP-027/028 `inferred/LOW`. All goals G-01..G-05 capabilities are `ACTIVE/HIGH` except as noted. Generation sequencing for the modernisation programme follows DECISIONS.json `generation_priorities`: BC-04 (1), BC-01 (2), BC-02 (3), BC-03 (4), BC-05 (5), BC-07 (6), BC-06 (7, aspirational — only on explicit decision).

---

## Appendix A — Open Questions Carried into Forward Engineering

| OQ | Question | Status |
|----|----------|--------|
| **OQ-001** | Merge Admin module (APP-SVC-005) with BlazorAdmin deployable (APP-SVC-016)? | Unresolved — kept SEPARATE pending review. |
| **OQ-004** | Is APP-DEP-001 a real runtime cycle or a static-resolution artifact? | Unresolved (affects C-01 / SC-07). |
| **OQ-005** | Is JWT/auth actually enforced on PublicApi, and is there a CORS policy? | Unresolved — High-severity findings TECH-SEC-010/011 (affects SC-10). |
| **OQ-006** | Does DATA-AGG-004 duplicate DATA-ENT-001? | Resolved — kept separate (different node kinds). |
| **OQ-007** | Authoritative system name. | Resolved — "eShopOnWeb" label with "unknown" caveat (C-05). |
| **OQ-008** | Which entities do IRepository<T>/IReadRepository<T> serve? | Resolved to inference (affects C-03 / SC-08). |
| **OQ-009** | Are ROUTE/CLI method labels evidenced verbs? | Resolved — synthetic, source method="unknown" (C-08). |
