# 03 — Use Case Specification

**System:** eShopOnWeb (authoritative name "unknown" in source evidence; labeled eShopOnWeb per OQ-007)
**Single source of truth:** `ENTERPRISE_KNOWLEDGE_GRAPH.json`
**Date:** 2026-06-23

---

## 1. Purpose & Scope

This document specifies use cases for every capability in the Enterprise Knowledge Graph that has behavioral evidence. It is grounded **exclusively** in graph node ids — capabilities (BIZ-CAP), actors (BIZ-ACT), processes (BIZ-PROC), business rules (BR0xx), entities (DATA-ENT), services/modules (APP-SVC), interfaces (APP-IF) and APIs (APP-API) — and the cross-links between them (`capability_to_process`, `process_to_entity`, `entity_to_service`, `service_to_api`). No capability, actor, flow, rule, entity, service or API outside the graph is invented.

**Coverage rule applied:**
- **L1 / L2 capabilities** are summarized (they aggregate their L3 leaves; no independent behavioral flow of their own).
- **L3 leaf capabilities (the 20 functional leaves)** receive full use-case specifications.
- Where a capability has **no step-level process evidence** (Browse Catalog, Adjust Basket value-stream stages; the zero-step seeding/buyer processes), this is stated explicitly and a minimal evidence-bounded flow is given with a gap flag.
- **INFERRED / aspirational** capabilities (Payment branch BIZ-CAP-027/028; Buyer profile branch) are noted, not specified as discovered behavior.

**Status flags honored (HARD RULES):**
- Buyer (DATA-ENT-010) and PaymentMethod (DATA-ENT-011) are `persisted=false`, `status=aspirational/unimplemented` (RC-002).
- Payment capabilities BIZ-CAP-027 / BIZ-CAP-028 are `inferred`, confidence `LOW`.
- `target_stack` is EMPTY (0 nodes); no target technology is asserted. Where the legacy stack appears it is labeled **Current (legacy)**.

### 1.1 Technology neutrality

This document is behavioral and technology-neutral. Implementation realization of these use cases is a forward-engineering choice. **No target technology is asserted by this specification**: the graph `target_stack` is EMPTY (0 nodes) and contains no mandate, ASMP or OQ node selecting a target stack. Any concrete target technologies (for example a backend framework, frontend framework, database engine or container runtime) are **externally-supplied generation options not derived from the graph** and must be sourced from a forward-engineering decision at generation time; they are deliberately not enumerated here so that none is implied to be discovered evidence. The Current (legacy) stack realizing these flows today is .NET 8 / ASP.NET Core (TECH-CUR-001/002), Blazor WASM (TECH-CUR-003), EF Core (TECH-CUR-005) over PostgreSQL/SQL Server (TECH-CUR-006/007, per-environment per OQ-003), with JWT + ASP.NET Core Identity (TECH-SEC-001/002).

---

## 2. Actors

| Actor id | Name | Type | Role in use cases |
|---|---|---|---|
| BIZ-ACT-001 | Customer / Buyer | human | Browses catalog, manages own basket, places orders, views order history. Permission: Standard. |
| BIZ-ACT-002 | Anonymous Shopper | human | Unauthenticated visitor; browses and builds an anonymous basket that is merged on login. |
| BIZ-ACT-003 | Administrator | human | Back-office catalog maintenance via the Blazor admin interface. Permission: Admin. |
| BIZ-ACT-004 | System / Service Account | system | Startup seeding, token issuance, image-path composition, total calculation. Permission: Elevated. |
| BIZ-ACT-005 | Notification Recipients | external | Recipients of order/email notifications via IEmailSender (APP-IF-008) — **present in code, not yet implemented**. |

---

## 3. Business Rule Catalog (evidence-anchored)

These rules drive the alternative/exception flows below. All are quoted from the graph `business.processes[].business_rules` anchors.

| Rule | Statement (evidence anchor) | Source entity |
|---|---|---|
| BR001 | Catalog item name / description / price validation | CatalogItem.cs |
| BR002 | Brand id must not equal 0 | CatalogItem.cs |
| BR003 | Type id must not equal 0 | CatalogItem.cs |
| BR004 | Image path generation for product picture | CatalogItem.cs |
| BR005 | IF item already in basket THEN increase the existing line quantity; ELSE add a new basket line | Basket.cs |
| BR006 | Zero-quantity basket line is removed | Basket.cs |
| BR007 | Negative basket quantity rejected | BasketItem.cs |
| BR008 | IF buyer record created without a valid identity reference THEN reject buyer creation | Buyer.cs (aspirational) |
| BR009 | Order line requires valid catalog item id / name / picture | CatalogItemOrdered.cs |
| BR010 | Order total = sum(unit price × quantity) | Order.cs |
| BR011 | Order requires a buyer id | Order.cs |
| BR012 | Block checkout for an empty basket | GuardExtensions.cs |

---

## 4. Capability → Use Case Index

| Capability | Level | Status | Process | Use Case |
|---|---|---|---|---|
| BIZ-CAP-001 Catalog Management | L1 | ACTIVE | — | Summary §5.1 |
| BIZ-CAP-002 Product Information Management | L2 | ACTIVE | BIZ-PROC-001 | Summary §5.1 |
| BIZ-CAP-003 Catalog Item Details Maintenance | L3 | ACTIVE | BIZ-PROC-006 | UC-01 |
| BIZ-CAP-004 Product Classification | L3 | ACTIVE | BIZ-PROC-006 | UC-02 |
| BIZ-CAP-005 Product Image Management | L3 | ACTIVE | BIZ-PROC-006 | UC-03 |
| BIZ-CAP-006 Catalog Reference Data | L2 | ACTIVE | — | Summary §5.1 |
| BIZ-CAP-007 Brand Management | L3 | ACTIVE | BIZ-PROC-006 / -009 | UC-04 |
| BIZ-CAP-008 Type Management | L3 | ACTIVE | BIZ-PROC-006 / -009 | UC-05 |
| BIZ-CAP-009 Catalog Seeding | L3 | ACTIVE | BIZ-PROC-009 | UC-06 |
| BIZ-CAP-010 Basket / Shopping Cart Management | L1 | ACTIVE | — | Summary §5.2 |
| BIZ-CAP-011 Basket Maintenance | L2 | ACTIVE | — | Summary §5.2 |
| BIZ-CAP-012 Add Item to Basket | L3 | ACTIVE | BIZ-PROC-002 | UC-07 |
| BIZ-CAP-013 Quantity Adjustment | L3 | ACTIVE | BIZ-PROC-004 | UC-08 |
| BIZ-CAP-014 Basket Cleanup | L3 | ACTIVE | BIZ-PROC-004 | UC-09 |
| BIZ-CAP-015 Session Continuity | L2 | ACTIVE | — | Summary §5.2 |
| BIZ-CAP-016 Anonymous-to-Registered Basket Transfer | L3 | ACTIVE | BIZ-PROC-003 | UC-10 |
| BIZ-CAP-017 Order Management | L1 | ACTIVE | — | Summary §5.3 |
| BIZ-CAP-018 Order Creation | L2 | ACTIVE | BIZ-PROC-005 | Summary §5.3 |
| BIZ-CAP-019 Checkout Processing | L3 | ACTIVE | BIZ-PROC-005 | UC-11 |
| BIZ-CAP-020 Empty Basket Protection | L3 | ACTIVE | BIZ-PROC-005 | UC-12 |
| BIZ-CAP-021 Ordered Item Snapshot | L3 | ACTIVE | BIZ-PROC-005 | UC-13 |
| BIZ-CAP-022 Order Calculation | L2 | ACTIVE | BIZ-PROC-005 | Summary §5.3 |
| BIZ-CAP-023 Order Total Calculation | L3 | ACTIVE | BIZ-PROC-005 | UC-14 |
| BIZ-CAP-024 Buyer / Customer Profile Management | L1 | ACTIVE (MED) | — | Summary §5.4 |
| BIZ-CAP-025 Buyer Identity | L2 | ACTIVE (MED) | — | Summary §5.4 |
| BIZ-CAP-026 Buyer Record Creation | L3 | ACTIVE (MED) | BIZ-PROC-008 | UC-15 |
| BIZ-CAP-027 Payment Information | L2 | inferred (LOW) | — | Noted §5.4 |
| BIZ-CAP-028 Payment Method Management | L3 | inferred (LOW) | — | Noted §5.4 |
| BIZ-CAP-029 Identity & Authentication | L1 | ACTIVE | — | Summary §5.5 |
| BIZ-CAP-030 Access Control | L2 | ACTIVE | BIZ-PROC-007 | Summary §5.5 |
| BIZ-CAP-031 User Login | L3 | ACTIVE | BIZ-PROC-007 | UC-16 |
| BIZ-CAP-032 Token Issuance | L3 | ACTIVE | BIZ-PROC-007 | UC-17 |
| BIZ-CAP-033 Identity Seeding | L2 | ACTIVE | — | Summary §5.5 |
| BIZ-CAP-034 Identity Data Seeding | L3 | ACTIVE | BIZ-PROC-010 | UC-18 |
| BIZ-CAP-035 Admin Catalog Operations (Blazor) | L1 | ACTIVE | — | Summary §5.6 |
| BIZ-CAP-036 Administrative Catalog Interface | L2 | ACTIVE | BIZ-PROC-006 | Summary §5.6 |
| BIZ-CAP-037 Catalog Item List View | L3 | ACTIVE | BIZ-PROC-006 | UC-19 |
| BIZ-CAP-038 Catalog Item Create/Delete | L3 | ACTIVE | BIZ-PROC-006 | UC-20 |
| BIZ-CAP-039 Cached Data Refresh | L3 | ACTIVE | BIZ-PROC-006 | UC-21 |

> Browse Catalog (BIZ-PROC-001) underpins L2 BIZ-CAP-002 but has **no L3 functional leaf** mapped to it and **no step-level breakdown** (value-stream stage only). It is covered as a minimal evidence-bounded use case **UC-00** under §5.1 with a gap flag.

---

## 5. Use Cases by L1 Capability

### 5.1 BIZ-CAP-001 — Catalog Management (L1, ACTIVE)

**Summary.** Manage the store product catalog: product information (BIZ-CAP-002) and catalog reference data (BIZ-CAP-006). Live product master data is owned by the Catalog context (BC-01) in DATA-ENT-001 CatalogItem, classified by DATA-ENT-002 CatalogBrand and DATA-ENT-003 CatalogType (DATA-REL-001/002), persisted via CatalogContext (DATA-REPO-003) and served by APP-SVC-001 Catalog. Functional behavior is expressed through its L3 leaves (UC-01..UC-06) and, for browsing, UC-00.

**L2 BIZ-CAP-002 — Product Information Management** aggregates UC-01 (details), UC-02 (classification), UC-03 (images). **L2 BIZ-CAP-006 — Catalog Reference Data** aggregates UC-04 (brands), UC-05 (types), UC-06 (seeding).

---

#### UC-00 — Browse Catalog (minimal, evidence-bounded; GAP)

| Field | Value |
|---|---|
| **UC id** | UC-00 |
| **Title** | Browse the catalog and filter by brand or type |
| **Capability** | underpins BIZ-CAP-002 (no functional L3 mapped) |
| **Process** | BIZ-PROC-001 (confidence MEDIUM, **1 step only**) |
| **Primary actor** | BIZ-ACT-001 Customer / Buyer; BIZ-ACT-002 Anonymous Shopper |
| **Secondary actor** | BIZ-ACT-004 System / Service Account |

**GAP:** BIZ-PROC-001 is a value-stream stage with **no step-level breakdown in evidence** (graph note: "not detailed in the process models document"). Flow below is the single evidenced step only. See **ASMP-FE-010**.

**Preconditions:** Catalog data has been seeded (UC-06). Catalog read APIs are reachable.

**Main flow:**
1. The actor requests the catalog listing. The system returns catalog items, optionally filtered by brand or type (`process_to_entity`: BIZ-PROC-001 → DATA-ENT-001/002/003).

**Alternative / exception flow:** None in evidence.

**Postconditions:** The actor has viewed available catalog items. No state change.

**Related services:** APP-SVC-001 Catalog; read decorators APP-SVC-044/045 (ICatalogItemService / ICatalogLookupDataService, APP-IF-010/011); APP-SVC-050 List.
**Related entities:** DATA-ENT-001 CatalogItem, DATA-ENT-002 CatalogBrand, DATA-ENT-003 CatalogType.
**Related APIs:** APP-API-004 `GET /api/catalog-items`, APP-API-003 `GET /api/catalog-items/{catalogItemId}`, APP-API-002 `GET /api/catalog-brands`, APP-API-008 `GET /api/catalog-types` (all `unit=PublicApi`, handler endpoints APP-SVC-030/031/032/036).

---

#### UC-01 — Maintain Catalog Item Details

| Field | Value |
|---|---|
| **UC id** | UC-01 |
| **Title** | Maintain product name, description, price, and image |
| **Capability** | BIZ-CAP-003 (L3, ACTIVE, HIGH) |
| **Process** | BIZ-PROC-006 Catalog Item Administration (4 steps, HIGH) |
| **Primary actor** | BIZ-ACT-003 Administrator |
| **Secondary actor** | BIZ-ACT-004 System / Service Account |

**Preconditions:** Administrator is authenticated (UC-16/UC-17); reference brands and types exist (UC-04/UC-05).

**Main flow (from BIZ-PROC-006 steps + BR001/BR004):**
1. Administrator selects a catalog item to edit (or initiates create — see UC-20).
2. Administrator submits name, description, and price.
3. System validates name / description / price (**BR001**).
4. System generates the image path for the product picture (**BR004**).
5. System persists the updated CatalogItem (DATA-ENT-001) via APP-SVC-001 / CatalogContext (DATA-REPO-003).
6. System refreshes the cached catalog list (UC-21).

**Alternative / exception flow:**
- **3a (BR001 fails):** name, description, or price invalid → system rejects the change; item not persisted.

**Postconditions:** CatalogItem details updated and persisted; image path set; admin cache refreshed.

**Related services:** APP-SVC-001 Catalog; APP-SVC-035 UpdateCatalogItemEndpoint; APP-SVC-020 UriComposer (IUriComposer, APP-IF-004, image-path composition); APP-SVC-023 CatalogContext.
**Related entities:** DATA-ENT-001 CatalogItem (`process_to_entity` BIZ-PROC-006 → DATA-ENT-001; `entity_to_service` → APP-SVC-001).
**Related APIs:** APP-API-007 `PUT /api/catalog-items` (handler APP-SVC-035); APP-API-048 `GET /Admin/EditCatalogItem`.

---

#### UC-02 — Classify Product (Brand & Type)

| Field | Value |
|---|---|
| **UC id** | UC-02 |
| **Title** | Assign a product to a brand and a type |
| **Capability** | BIZ-CAP-004 (L3, ACTIVE, HIGH) |
| **Process** | BIZ-PROC-006 (HIGH) |
| **Primary actor** | BIZ-ACT-003 Administrator |

**Preconditions:** Target CatalogItem exists; the chosen brand (DATA-ENT-002) and type (DATA-ENT-003) exist.

**Main flow (BIZ-PROC-006 + BR002/BR003):**
1. Administrator selects a brand and a type for the catalog item.
2. System validates the brand id is not 0 (**BR002**).
3. System validates the type id is not 0 (**BR003**).
4. System sets CatalogBrandId / CatalogTypeId on the CatalogItem (DATA-REL-001/002) and persists.

**Alternative / exception flow:**
- **2a (BR002 fails):** brand id = 0 → reject; classification not applied.
- **3a (BR003 fails):** type id = 0 → reject; classification not applied.

**Postconditions:** CatalogItem associated with a valid brand and type (candidate value object VO-06 ProductClassification).

**Related services:** APP-SVC-001 Catalog; APP-SVC-033/035 (create/update endpoints).
**Related entities:** DATA-ENT-001 CatalogItem, DATA-ENT-002 CatalogBrand, DATA-ENT-003 CatalogType.
**Related APIs:** APP-API-005 `POST /api/catalog-items`, APP-API-007 `PUT /api/catalog-items`.

---

#### UC-03 — Manage Product Image Path

| Field | Value |
|---|---|
| **UC id** | UC-03 |
| **Title** | Generate and maintain the product image path |
| **Capability** | BIZ-CAP-005 (L3, ACTIVE, HIGH) |
| **Process** | BIZ-PROC-006 (HIGH) |
| **Primary actor** | BIZ-ACT-004 System / Service Account |
| **Secondary actor** | BIZ-ACT-003 Administrator |

**Preconditions:** A catalog item is being created or updated (UC-01 / UC-20).

**Main flow (BIZ-PROC-006 + BR004):**
1. On create/update of a CatalogItem, the system generates the image path for the product picture (**BR004**) via APP-SVC-020 UriComposer (IUriComposer, APP-IF-004).
2. System stores PictureUri on DATA-ENT-001 CatalogItem and persists.

**Alternative / exception flow:** None step-level in evidence beyond BR004.

**Postconditions:** CatalogItem.PictureUri reflects the composed image path.

**Related services:** APP-SVC-020 UriComposer; APP-SVC-001 Catalog. (Note: APP-DEP-010 records UriComposer as a high-coupling component to resolve at carve-out.)
**Related entities:** DATA-ENT-001 CatalogItem.
**Related APIs:** APP-API-005 `POST /api/catalog-items`, APP-API-007 `PUT /api/catalog-items` (image path set as part of create/update).

---

#### UC-04 — Manage Brands

| Field | Value |
|---|---|
| **UC id** | UC-04 |
| **Title** | Maintain the list of brands available for classification |
| **Capability** | BIZ-CAP-007 (L3, ACTIVE, HIGH) |
| **Process** | BIZ-PROC-006 (list/use); BIZ-PROC-009 (seed) |
| **Primary actor** | BIZ-ACT-003 Administrator; BIZ-ACT-004 System (seeding) |

**Preconditions:** Catalog reference store available.

**Main flow (evidence-bounded — list & reference; GAP on create/edit/delete of brands):**
1. System provides the list of brands for selection/display (BIZ-PROC-006 step "View the list of catalog items, types, and brands").
2. Brands are populated at startup by catalog seeding (UC-06, BIZ-PROC-009).

**GAP:** The graph exposes brand **listing/reference and seeding** only; there is **no brand create/update/delete process step or API** in evidence (only `GET /api/catalog-brands`). See **ASMP-FE-011**.

**Alternative / exception flow:** None in evidence.

**Postconditions:** Brand reference data available for classification (UC-02) and display.

**Related services:** APP-SVC-001 Catalog; APP-SVC-030 CatalogBrandListEndpoint; APP-SVC-025 CatalogContextSeed.
**Related entities:** DATA-ENT-002 CatalogBrand.
**Related APIs:** APP-API-002 `GET /api/catalog-brands` (handler APP-SVC-030).

---

#### UC-05 — Manage Types

| Field | Value |
|---|---|
| **UC id** | UC-05 |
| **Title** | Maintain the list of product types/categories |
| **Capability** | BIZ-CAP-008 (L3, ACTIVE, HIGH) |
| **Process** | BIZ-PROC-006 (list/use); BIZ-PROC-009 (seed) |
| **Primary actor** | BIZ-ACT-003 Administrator; BIZ-ACT-004 System (seeding) |

**Preconditions:** Catalog reference store available.

**Main flow (evidence-bounded — list & reference; GAP on create/edit/delete of types):**
1. System provides the list of types for selection/display (BIZ-PROC-006 step).
2. Types are populated at startup by catalog seeding (UC-06, BIZ-PROC-009).

**GAP:** Only type **listing/reference and seeding** are evidenced; **no type create/update/delete process or API** exists (only `GET /api/catalog-types`). See **ASMP-FE-011**.

**Alternative / exception flow:** None in evidence.

**Postconditions:** Type reference data available for classification (UC-02) and display.

**Related services:** APP-SVC-001 Catalog; APP-SVC-036 CatalogTypeListEndpoint; APP-SVC-025 CatalogContextSeed.
**Related entities:** DATA-ENT-003 CatalogType.
**Related APIs:** APP-API-008 `GET /api/catalog-types` (handler APP-SVC-036).

---

#### UC-06 — Seed Catalog Data

| Field | Value |
|---|---|
| **UC id** | UC-06 |
| **Title** | Populate initial catalog data on startup |
| **Capability** | BIZ-CAP-009 (L3, ACTIVE, HIGH) |
| **Process** | BIZ-PROC-009 Catalog Seeding (confidence MEDIUM, **0 steps**) |
| **Primary actor** | BIZ-ACT-004 System / Service Account |

**GAP:** BIZ-PROC-009 has **0 step-level steps in evidence** (capability/responsibility only). Flow below is the minimal evidence-bounded behavior from the trigger + `process_to_entity`. See **ASMP-FE-012**.

**Preconditions:** System startup; catalog persistence store reachable.

**Main flow (minimal, trigger-bounded):**
1. On system startup, the System / Service Account seeds initial CatalogItem, CatalogBrand, and CatalogType data (`process_to_entity`: BIZ-PROC-009 → DATA-ENT-001/002/003).
2. Seeded data is persisted via CatalogContext (DATA-REPO-003).

**Alternative / exception flow:** None in evidence (idempotency / re-seed behavior not evidenced — gap).

**Postconditions:** Catalog reference and item data exist, enabling UC-00..UC-05.

**Related services:** APP-SVC-025 CatalogContextSeed (BatchJob); APP-SVC-023 CatalogContext; APP-SVC-001 Catalog.
**Related entities:** DATA-ENT-001 CatalogItem, DATA-ENT-002 CatalogBrand, DATA-ENT-003 CatalogType.
**Related APIs:** None (startup batch job, not an HTTP API). Bootstrap occurs under APP-API-054 / APP-API-055 (Program.cs hosts).

---

### 5.2 BIZ-CAP-010 — Basket / Shopping Cart Management (L1, ACTIVE)

**Summary.** Manage the shopping basket lifecycle. L2 **BIZ-CAP-011 Basket Maintenance** covers add/adjust/cleanup (UC-07..UC-09); L2 **BIZ-CAP-015 Session Continuity** covers anonymous-to-registered transfer (UC-10). The consistency boundary is DATA-AGG-001 BasketAggregate (root DATA-ENT-004 Basket, member DATA-ENT-005 BasketItem, DATA-REL-003), persisted via CatalogContext (DATA-REPO-003) and served by APP-SVC-003 Basket. Basket references the user via a soft BuyerId reference to ApplicationUser (DATA-REL-008) — a cross-context identifier to Identity (BC-04), not a hard FK.

---

#### UC-07 — Add Item to Basket

| Field | Value |
|---|---|
| **UC id** | UC-07 |
| **Title** | Add a catalog item to the basket, consolidating quantity |
| **Capability** | BIZ-CAP-012 (L3, ACTIVE, HIGH) |
| **Process** | BIZ-PROC-002 Add Item to Basket (3 steps, HIGH) |
| **Primary actor** | BIZ-ACT-001 Customer / Buyer; BIZ-ACT-002 Anonymous Shopper |
| **Secondary actor** | BIZ-ACT-004 System / Service Account |

**Preconditions:** The catalog item exists and is browsable (UC-00).

**Main flow (BIZ-PROC-002 steps + BR005):**
1. Customer (or anonymous user) selects a catalog item to purchase.
2. System retrieves the user's existing basket, or creates a new one if none exists (Decision: basket exists? YES → use existing; NO → create new — DATA-ENT-004 Basket).
3. System adds the item to the basket: if the catalog item is already present, increase the existing line quantity; else add a new basket line (**BR005**, DATA-ENT-005 BasketItem).
4. System persists the updated basket.

**Alternative / exception flow:**
- **2a:** No existing basket → create a new Basket, then continue.
- **3a (BR005):** Item already present → consolidate by incrementing quantity on the existing line rather than creating a duplicate line.

**Postconditions:** Basket contains the requested item at the correct quantity; basket persisted. Candidate domain event **EVT-01 ItemAddedToBasket** (INFERRED).

**Related services:** APP-SVC-003 Basket; APP-SVC-027 BasketGuards.
**Related entities:** DATA-ENT-004 Basket, DATA-ENT-005 BasketItem, DATA-ENT-001 CatalogItem (soft ref DATA-REL-004) — `process_to_entity` BIZ-PROC-002 → DATA-ENT-004/005/001; `entity_to_service` DATA-ENT-004/005 → APP-SVC-003.
**Related APIs:** APP-API-051 `GET /{handler?}` (Basket Razor Page; physically hosted by Web shell APP-SVC-006, functionally Basket per ASMP-FE-004). No dedicated REST basket API exists in evidence (gap — basket behavior is page/handler-served).

---

#### UC-08 — Adjust Basket Quantity

| Field | Value |
|---|---|
| **UC id** | UC-08 |
| **Title** | Adjust the quantity of a basket line, preventing negative values |
| **Capability** | BIZ-CAP-013 (L3, ACTIVE, HIGH) |
| **Process** | BIZ-PROC-004 Adjust Basket (confidence MEDIUM, **1 step**) |
| **Primary actor** | BIZ-ACT-001 Customer / Buyer |

**GAP:** BIZ-PROC-004 is a value-stream stage with a **single step** ("Customer adjusts quantities or removes items before checkout"); no detailed sub-steps in evidence. Flow is bounded to that step plus its governing rules BR006/BR007. See **ASMP-FE-013**.

**Preconditions:** Basket exists and contains at least one line (DATA-ENT-005 BasketItem).

**Main flow (BIZ-PROC-004 + BR007):**
1. Customer reviews the basket before checkout.
2. Customer changes the quantity of a basket line.
3. System validates the quantity is not negative (**BR007**) and updates the line.
4. System persists the basket.

**Alternative / exception flow:**
- **3a (BR007):** Requested quantity is negative → rejected; quantity unchanged.
- **3b → UC-09:** If the new quantity is zero, the line is removed (**BR006**, see UC-09 Basket Cleanup).

**Postconditions:** Basket line reflects the adjusted (non-negative) quantity. Candidate domain event **EVT-02 BasketQuantityAdjusted** (INFERRED).

**Related services:** APP-SVC-003 Basket; APP-SVC-027 BasketGuards (negative-quantity guard).
**Related entities:** DATA-ENT-005 BasketItem, DATA-ENT-004 Basket (`process_to_entity` BIZ-PROC-004 → DATA-ENT-005/004).
**Related APIs:** APP-API-051 `GET /{handler?}` (Basket page handler; Web shell APP-SVC-006). No dedicated REST API in evidence.

---

#### UC-09 — Basket Cleanup (Remove Zero-Quantity Lines)

| Field | Value |
|---|---|
| **UC id** | UC-09 |
| **Title** | Remove basket lines with zero quantity |
| **Capability** | BIZ-CAP-014 (L3, ACTIVE, HIGH) |
| **Process** | BIZ-PROC-004 Adjust Basket (1 step) |
| **Primary actor** | BIZ-ACT-001 Customer / Buyer |
| **Secondary actor** | BIZ-ACT-004 System / Service Account |

**Preconditions:** Basket exists; a line quantity has been set to zero (via UC-08) or an item removed.

**Main flow (BIZ-PROC-004 + BR006):**
1. During basket adjustment, a line's quantity becomes zero (or the customer removes it).
2. System removes the zero-quantity basket line (**BR006**, DATA-ENT-005 BasketItem).
3. System persists the updated basket.

**Alternative / exception flow:** None beyond BR006 in evidence.

**Postconditions:** Basket contains no zero-quantity lines. Contributes to candidate event **EVT-02 BasketQuantityAdjusted** (INFERRED).

**Related services:** APP-SVC-003 Basket; APP-SVC-027 BasketGuards.
**Related entities:** DATA-ENT-004 Basket, DATA-ENT-005 BasketItem.
**Related APIs:** APP-API-051 `GET /{handler?}` (Basket page handler; Web shell APP-SVC-006).

---

#### UC-10 — Transfer Anonymous Basket to Registered User

| Field | Value |
|---|---|
| **UC id** | UC-10 |
| **Title** | Merge an anonymous basket into the registered user's basket on login |
| **Capability** | BIZ-CAP-016 (L3, ACTIVE, HIGH) |
| **Process** | BIZ-PROC-003 Transfer Anonymous Basket to Registered User (3 steps, HIGH) |
| **Primary actor** | BIZ-ACT-002 Anonymous Shopper (transitioning to BIZ-ACT-001) |
| **Secondary actor** | BIZ-ACT-004 System / Service Account |

**Preconditions:** An anonymous session basket may exist; the user logs in or registers (UC-16).

**Main flow (BIZ-PROC-003 steps + BR005):**
1. (Trigger) An anonymous user logs in or registers.
2. System retrieves the anonymous user's basket (Decision: anonymous basket exists? YES → continue; NO → end, nothing to transfer).
3. System retrieves or creates a basket for the now-registered user (Decision: registered user already has a basket? YES → merge into existing; NO → create new).
4. System copies each item from the anonymous basket into the user's basket, consolidating quantities (**BR005**); the basket is linked to the user via BuyerId (DATA-REL-008 soft ref to DATA-ENT-008 ApplicationUser).

**Alternative / exception flow:**
- **2a:** No anonymous basket → end; nothing to transfer.
- **3a:** Registered user already has a basket → merge anonymous items into the existing basket.
- **4a (BR005):** Item already present in target basket → increase quantity instead of duplicating.

**Postconditions:** Registered user's basket contains all items from the anonymous session. Candidate domain event **EVT-03 AnonymousBasketTransferred** (INFERRED).

**Related services:** APP-SVC-003 Basket; APP-SVC-027 BasketGuards.
**Related entities:** DATA-ENT-004 Basket, DATA-ENT-005 BasketItem, DATA-ENT-008 ApplicationUser (`process_to_entity` BIZ-PROC-003 → DATA-ENT-004/005/008).
**Related APIs:** Triggered at login (APP-API-001 `POST /api/authenticate` / identity login pages APP-API-042/044). No dedicated transfer API in evidence (page/handler orchestrated).

---

### 5.3 BIZ-CAP-017 — Order Management (L1, ACTIVE)

**Summary.** Create orders from baskets and calculate totals. L2 **BIZ-CAP-018 Order Creation** covers checkout (UC-11), empty-basket protection (UC-12) and ordered-item snapshot (UC-13). L2 **BIZ-CAP-022 Order Calculation** covers total calculation (UC-14). All four leaves map to the single end-to-end process BIZ-PROC-005 Checkout / Place Order (6 steps, HIGH). The consistency boundary is DATA-AGG-002 OrderAggregate (root DATA-ENT-006 Order; members DATA-ENT-007 OrderItem, DATA-ENT-013 Address, DATA-ENT-012 CatalogItemOrdered; DATA-REL-005/006/007). Order references the buyer via a soft BuyerId reference (DATA-REL-009). Order history is queried via APP-SVC-041/042/043 (GetMyOrders / handler / GetOrderDetails).

---

#### UC-11 — Checkout / Place Order

| Field | Value |
|---|---|
| **UC id** | UC-11 |
| **Title** | Convert the basket into a confirmed order |
| **Capability** | BIZ-CAP-019 (L3, ACTIVE, HIGH) |
| **Process** | BIZ-PROC-005 Checkout / Place Order (6 steps, HIGH) |
| **Primary actor** | BIZ-ACT-001 Customer / Buyer |
| **Secondary actor** | BIZ-ACT-004 System / Service Account |

**Preconditions:** Customer authenticated (UC-16/UC-17) with a valid buyer id (BR011); basket exists.

**Main flow (BIZ-PROC-005 steps + BR009/BR010/BR011/BR012):**
1. Customer initiates checkout from their basket.
2. System retrieves the customer's basket with items (DATA-ENT-004 Basket).
3. System verifies the basket exists and is not empty (**BR012**; Decision in UC-12).
4. System retrieves full catalog item details for each basket item (DATA-ENT-001 CatalogItem).
5. System creates a snapshot of each ordered item — name, picture, price (**BR009**; UC-13, DATA-ENT-012 CatalogItemOrdered).
6. System creates the order with the buyer id, shipping address, and order items (**BR011**; DATA-ENT-006 Order, DATA-ENT-013 Address, DATA-ENT-007 OrderItem). Basket→Order transition is DATA-REL-011.
7. System calculates the order total from item prices and quantities (**BR010**; UC-14).

**Alternative / exception flow:**
- **3a (BR012):** Basket is empty → block checkout and raise an empty-basket error (UC-12). Candidate event **EVT-06 CheckoutRejectedEmptyBasket** (INFERRED).
- **6a (BR011):** No valid buyer id → order creation rejected.
- **5a (BR009):** Ordered-item snapshot missing valid catalog item id / name / picture → order line invalid.

**Postconditions:** A confirmed Order exists with snapshotted line items, shipping address, buyer id and a calculated total; basket consumed. Candidate domain event **EVT-04 OrderPlaced** (INFERRED).

**Related services:** APP-SVC-004 Order; APP-SVC-038 OrderController (uses MediatR / IMediator APP-IF-012); APP-SVC-027 BasketGuards (empty-basket guard).
**Related entities:** DATA-ENT-004 Basket, DATA-ENT-006 Order, DATA-ENT-007 OrderItem, DATA-ENT-012 CatalogItemOrdered, DATA-ENT-013 Address, DATA-ENT-001 CatalogItem (`process_to_entity` BIZ-PROC-005 → these).
**Related APIs:** APP-API-050 `GET /Basket/Checkout`, APP-API-052 `GET /Basket/Success` (Basket Razor pages; Web shell APP-SVC-006, functionally Ordering/Basket per ASMP-FE-004); order history APP-API-035 `GET /Order/MyOrders`, APP-API-036 `GET /Order/Detail/{orderId}` (handlers via APP-SVC-038/041/043).

---

#### UC-12 — Empty Basket Protection

| Field | Value |
|---|---|
| **UC id** | UC-12 |
| **Title** | Prevent checkout when the basket is empty |
| **Capability** | BIZ-CAP-020 (L3, ACTIVE, HIGH) |
| **Process** | BIZ-PROC-005 (step 2 / BR012) |
| **Primary actor** | BIZ-ACT-004 System / Service Account |
| **Secondary actor** | BIZ-ACT-001 Customer / Buyer |

**Preconditions:** Checkout has been initiated (UC-11 step 1).

**Main flow (BIZ-PROC-005 step "Verify the basket exists and is not empty" + BR012):**
1. System retrieves the basket and evaluates whether it is empty.
2. If the basket is **not** empty, checkout continues (UC-11 step 4 onward).

**Alternative / exception flow:**
- **1a (BR012):** Basket is empty → system blocks checkout and raises an empty-basket error (enforced by GuardExtensions.cs / APP-SVC-027 BasketGuards). No order is created. Candidate event **EVT-06 CheckoutRejectedEmptyBasket** (INFERRED).

**Postconditions:** Checkout proceeds only for a non-empty basket; otherwise no state change.

**Related services:** APP-SVC-027 BasketGuards; APP-SVC-004 Order.
**Related entities:** DATA-ENT-004 Basket, DATA-ENT-005 BasketItem.
**Related APIs:** APP-API-050 `GET /Basket/Checkout` (Web shell APP-SVC-006).

---

#### UC-13 — Capture Ordered-Item Snapshot

| Field | Value |
|---|---|
| **UC id** | UC-13 |
| **Title** | Snapshot product name, picture, and price at order time |
| **Capability** | BIZ-CAP-021 (L3, ACTIVE, HIGH) |
| **Process** | BIZ-PROC-005 (steps 3–4 / BR009) |
| **Primary actor** | BIZ-ACT-004 System / Service Account |

**Preconditions:** Checkout in progress; basket non-empty (UC-12 passed).

**Main flow (BIZ-PROC-005 + BR009):**
1. System retrieves full catalog item details for each basket item (DATA-ENT-001).
2. System creates an ordered-item snapshot — catalog item id, product name, picture (DATA-ENT-012 CatalogItemOrdered; DATA-REL-006 OrderItem 1..1 CatalogItemOrdered).
3. System validates each snapshot has a valid catalog item id / name / picture (**BR009**).

**Alternative / exception flow:**
- **3a (BR009):** Snapshot missing valid id / name / picture → the order line is invalid and is rejected.

**Postconditions:** Each OrderItem carries an immutable CatalogItemOrdered snapshot (candidate value object **VO-03**), decoupling the order from later catalog changes.

**Related services:** APP-SVC-004 Order.
**Related entities:** DATA-ENT-012 CatalogItemOrdered, DATA-ENT-007 OrderItem, DATA-ENT-001 CatalogItem.
> **Boundary note:** DATA-ENT-012 is physically catalog-owned in evidence (`entity_to_service` DATA-ENT-012 → APP-SVC-001) yet conceptually a member of OrderAggregate (DATA-AGG-002); resolved as a copied-at-checkout value object in BC-03 (see DECISIONS VO-03).
**Related APIs:** APP-API-050 `GET /Basket/Checkout` (snapshot produced during checkout; Web shell APP-SVC-006).

---

#### UC-14 — Calculate Order Total

| Field | Value |
|---|---|
| **UC id** | UC-14 |
| **Title** | Calculate the order total from item prices and quantities |
| **Capability** | BIZ-CAP-023 (L3, ACTIVE, HIGH) |
| **Process** | BIZ-PROC-005 (step 6 / BR010) |
| **Primary actor** | BIZ-ACT-004 System / Service Account |

**Preconditions:** Order lines (DATA-ENT-007 OrderItem) with unit prices and quantities exist (UC-11 step 6).

**Main flow (BIZ-PROC-005 + BR010):**
1. System sums, across order lines, unit price × quantity (**BR010**: order total = Σ(UnitPrice × Units)).
2. System records the calculated total on the order (DATA-ENT-006 Order).

**Alternative / exception flow:** None in evidence.

**Postconditions:** Order carries a calculated total. Candidate domain event **EVT-05 OrderTotalCalculated** (INFERRED).

> **Modeling note (ASMP-FE-001 reused):** Price / UnitPrice appear as bare decimals with **no currency attribute** on any entity; a currency-bearing Money value object (VO-05) is a NEW design element, "not in legacy evidence."

**Related services:** APP-SVC-004 Order.
**Related entities:** DATA-ENT-006 Order, DATA-ENT-007 OrderItem.
**Related APIs:** computed during checkout (APP-API-050); surfaced in order history APP-API-035 / APP-API-036.

---

### 5.4 BIZ-CAP-024 — Buyer / Customer Profile Management (L1, ACTIVE, MEDIUM)

**Summary.** Manage buyer identity records and (aspirationally) payment information. L2 **BIZ-CAP-025 Buyer Identity** covers buyer record creation (UC-15). L2 **BIZ-CAP-027 Payment Information** and L3 **BIZ-CAP-028 Payment Method Management** are **inferred / confidence LOW** and have no behavioral process, service or API — see §5.4.1.

> **Status caveat (RC-002 / ASMP-FE-003):** DATA-ENT-010 Buyer and DATA-ENT-011 PaymentMethod are `persisted=false`, `status=aspirational/unimplemented`; DATA-AGG-003 BuyerAggregate is aspirational; DATA-REL-012 Buyer 1..* PaymentMethod is aspirational. Today the buyer reference is satisfied by DATA-ENT-008 ApplicationUser (BC-04). The use case below is specified as a **design input, not discovered behavior**, and must not drive persistence generation without a deliberate decision.

---

#### UC-15 — Create Buyer Record (design input; ASPIRATIONAL)

| Field | Value |
|---|---|
| **UC id** | UC-15 |
| **Title** | Create a buyer record linked to a valid identity account |
| **Capability** | BIZ-CAP-026 (L3, ACTIVE, MEDIUM) |
| **Process** | BIZ-PROC-008 Buyer Record Creation (confidence MEDIUM, **0 steps**) |
| **Primary actor** | BIZ-ACT-004 System / Service Account |
| **Secondary actor** | BIZ-ACT-001 Customer / Buyer |

**GAP:** BIZ-PROC-008 has **0 step-level steps** and no explicit trigger in evidence; the target entity DATA-ENT-010 Buyer is aspirational/unimplemented. Flow is bounded to the governing rule BR008 + BR011 only. See **ASMP-FE-003** (reused) and **ASMP-FE-014**.

**Preconditions:** A valid identity account (DATA-ENT-008 ApplicationUser) exists (UC-16/UC-18).

**Main flow (rule-bounded; BR008):**
1. The system creates a buyer record (DATA-ENT-010 Buyer) linked to a valid identity reference.

**Alternative / exception flow:**
- **1a (BR008):** Buyer creation attempted without a valid identity reference → reject buyer creation.

**Postconditions (aspirational):** A buyer record linked to an identity account exists, satisfying the buyer-id requirement for orders (BR011). Candidate domain event **EVT-11 BuyerRecordCreated** (INFERRED).

**Related services:** None in evidence (BC-06 has no services). Buyer/Payment entities are mapped to APP-SVC-004 Order in `entity_to_service` (DATA-ENT-010/011 → APP-SVC-004) — physical placement only, not an implemented service flow.
**Related entities:** DATA-ENT-010 Buyer (aspirational), DATA-ENT-008 ApplicationUser (`process_to_entity` BIZ-PROC-008 → DATA-ENT-010/008).
**Related APIs:** None in evidence.

#### 5.4.1 BIZ-CAP-027 / BIZ-CAP-028 — Payment Information & Payment Method Management (INFERRED, LOW — NOT SPECIFIED)

No use case is written. These capabilities are `inferred` with confidence `LOW`, derived **only from the data-model entity** DATA-ENT-011 PaymentMethod (aspirational/unimplemented). There is **no process, no business rule, no service, and no API** in evidence. Relationship DATA-REL-012 (Buyer 1..* PaymentMethod) is aspirational. Any payment behavior is a **future forward-engineering decision**, never asserted as discovered. Gap recorded as **ASMP-FE-015**.

---

### 5.5 BIZ-CAP-029 — Identity & Authentication (L1, ACTIVE)

**Summary.** Validate credentials, issue tokens, and seed identity data. L2 **BIZ-CAP-030 Access Control** covers login (UC-16) and token issuance (UC-17), both mapped to BIZ-PROC-007 User Authentication (3 steps, HIGH). L2 **BIZ-CAP-033 Identity Seeding** covers identity data seeding (UC-18, BIZ-PROC-010). Identity owns DATA-ENT-008 ApplicationUser and DATA-ENT-009 Role via AppIdentityDbContext (DATA-REPO-004), served by APP-SVC-002 Identity. Realized today (Current/legacy) by ASP.NET Core Identity (TECH-SEC-001) + JWT Bearer (TECH-SEC-002).

> **Security caveat (OQ-005):** TECH-SEC-010 records **no confirmed JWT enforcement on PublicApi** and TECH-SEC-011 **no CORS policy** — open findings, not implemented controls.

---

#### UC-16 — User Login (Validate Credentials)

| Field | Value |
|---|---|
| **UC id** | UC-16 |
| **Title** | Validate user credentials and report lockout/permission status |
| **Capability** | BIZ-CAP-031 (L3, ACTIVE, HIGH) |
| **Process** | BIZ-PROC-007 User Authentication (steps 1–2, HIGH) |
| **Primary actor** | BIZ-ACT-001 Customer / Buyer (or BIZ-ACT-003 Administrator) |
| **Secondary actor** | BIZ-ACT-004 System / Service Account |

**Preconditions:** Identity store seeded (UC-18); the user has an account (DATA-ENT-008 ApplicationUser).

**Main flow (BIZ-PROC-007 steps 1–2):**
1. The user submits username and password to the authentication endpoint.
2. System validates credentials against the identity store (DATA-ENT-008 ApplicationUser, DATA-ENT-009 Role). Decision: are credentials valid and the account not locked out? YES → proceed to token issuance (UC-17).

**Alternative / exception flow:**
- **2a (lockout / not-allowed):** Credentials invalid, account locked out, or sign-in not allowed → system returns a failed result with lockout / not-allowed status; no token issued.

**Postconditions:** Valid, non-locked-out credentials are confirmed, enabling UC-17. On failure, the failure status is reported. (No standalone business rule node; behavior is process-step evidenced.)

**Related services:** APP-SVC-002 Identity; APP-SVC-029 AuthenticateEndpoint; APP-SVC-021 IdentityTokenClaimService (ITokenClaimsService, APP-IF-003); APP-SVC-039 UserController.
**Related entities:** DATA-ENT-008 ApplicationUser, DATA-ENT-009 Role (`process_to_entity` BIZ-PROC-007 → DATA-ENT-008/009; `entity_to_service` → APP-SVC-002).
**Related APIs:** APP-API-001 `POST /api/authenticate` (handler APP-SVC-029, PublicApi APP-SVC-011 — issues JWT); login/account pages APP-API-042 `GET /Account/Login`, APP-API-037 `GET /User`, APP-API-038 `POST /User/Logout` (Web shell APP-SVC-006).

---

#### UC-17 — Token Issuance

| Field | Value |
|---|---|
| **UC id** | UC-17 |
| **Title** | Generate a signed JWT token with identity and role claims |
| **Capability** | BIZ-CAP-032 (L3, ACTIVE, HIGH) |
| **Process** | BIZ-PROC-007 User Authentication (step 3, HIGH) |
| **Primary actor** | BIZ-ACT-004 System / Service Account |
| **Secondary actor** | BIZ-ACT-001 Customer / Buyer |

**Preconditions:** Credentials validated and account not locked out (UC-16 step 2 = YES).

**Main flow (BIZ-PROC-007 step 3):**
1. System generates a signed JWT token containing the user's identity and role claims (DATA-ENT-008 ApplicationUser, DATA-ENT-009 Role) via APP-SVC-021 IdentityTokenClaimService.
2. System returns the token with a success result for use on subsequent API access.

**Alternative / exception flow:** Reached only when UC-16 succeeds; on UC-16 failure no token is issued (see UC-16 2a).

**Postconditions:** A signed JWT containing identity/role claims is available to the caller. Candidate domain event **EVT-07 UserAuthenticated** (INFERRED).

**Related services:** APP-SVC-021 IdentityTokenClaimService (APP-IF-003 ITokenClaimsService); APP-SVC-029 AuthenticateEndpoint; APP-SVC-002 Identity.
**Related entities:** DATA-ENT-008 ApplicationUser, DATA-ENT-009 Role.
**Related APIs:** APP-API-001 `POST /api/authenticate` (handler APP-SVC-029, issues JWT — TECH-SEC-002).

---

#### UC-18 — Seed Identity Data

| Field | Value |
|---|---|
| **UC id** | UC-18 |
| **Title** | Populate initial user accounts and roles on startup |
| **Capability** | BIZ-CAP-034 (L3, ACTIVE, HIGH) |
| **Process** | BIZ-PROC-010 Identity Data Seeding (confidence MEDIUM, **0 steps**) |
| **Primary actor** | BIZ-ACT-004 System / Service Account |

**GAP:** BIZ-PROC-010 has **0 step-level steps** in evidence (capability/responsibility only). Flow is minimal/trigger-bounded. See **ASMP-FE-012** (reused).

**Preconditions:** System startup; identity store reachable.

**Main flow (minimal, trigger-bounded):**
1. On system startup, the System / Service Account seeds initial user accounts and roles (`process_to_entity` BIZ-PROC-010 → DATA-ENT-008 ApplicationUser, DATA-ENT-009 Role).
2. Seeded data persisted via AppIdentityDbContext (DATA-REPO-004).

**Alternative / exception flow:** None in evidence (idempotency / re-seed not evidenced — gap).

**Postconditions:** Initial users and roles exist, enabling UC-16/UC-17.

**Related services:** APP-SVC-026 AppIdentityDbContextSeed (BatchJob); APP-SVC-024 AppIdentityDbContext; APP-SVC-002 Identity.
**Related entities:** DATA-ENT-008 ApplicationUser, DATA-ENT-009 Role.
**Related APIs:** None (startup batch job). Bootstrap under APP-API-054 / APP-API-055.

---

### 5.6 BIZ-CAP-035 — Admin Catalog Operations (Blazor) (L1, ACTIVE)

**Summary.** Administrative catalog operations through the Blazor admin SPA. L2 **BIZ-CAP-036 Administrative Catalog Interface** aggregates list view (UC-19), create/delete (UC-20) and cache refresh (UC-21), all mapped to BIZ-PROC-006 Catalog Item Administration (4 steps, HIGH). This is a **behavior-only presentation context** (BC-05) owning **no entities/aggregates**; it consumes BC-01 Catalog through ICatalogItemService / ICatalogLookupDataService (APP-IF-010/011) and the catalog APIs. Delivered by APP-SVC-016 BlazorAdmin (runtime HTTP deps APP-DEP-017 → PublicApi, APP-DEP-018 → Web).

> **Open question OQ-001:** whether to merge the Admin module (APP-SVC-005) with the BlazorAdmin deployable (APP-SVC-016) is **UNRESOLVED**; kept separate (conservative).

---

#### UC-19 — View Catalog Item List

| Field | Value |
|---|---|
| **UC id** | UC-19 |
| **Title** | Display catalog items, types, and brands to administrators |
| **Capability** | BIZ-CAP-037 (L3, ACTIVE, HIGH) |
| **Process** | BIZ-PROC-006 (step 1, HIGH) |
| **Primary actor** | BIZ-ACT-003 Administrator |
| **Secondary actor** | BIZ-ACT-004 System / Service Account |

**Preconditions:** Administrator authenticated (UC-16/UC-17); catalog data seeded (UC-06).

**Main flow (BIZ-PROC-006 step 1):**
1. Administrator opens the admin catalog interface (`/admin`).
2. System retrieves and displays the list of catalog items, types, and brands via ICatalogItemService / ICatalogLookupDataService (APP-IF-010/011), served from the catalog read APIs, optionally from the local cache (APP-SVC-044/045 decorators).

**Alternative / exception flow:** None step-level in evidence.

**Postconditions:** Administrator sees the current catalog list (items + reference brands/types).

**Related services:** APP-SVC-016 BlazorAdmin; APP-SVC-050 List; APP-SVC-044 CachedCatalogItemServiceDecorator; APP-SVC-045 CachedCatalogLookupDataServiceDecorator; APP-SVC-005 Admin.
**Related entities:** None owned (BC-05). Read-projects DATA-ENT-001/002/003 from BC-01 Catalog.
**Related APIs:** APP-API-040 `ROUTE /admin` (List.razor; BlazorAdmin APP-SVC-016); consumes APP-API-004 `GET /api/catalog-items`, APP-API-002 `GET /api/catalog-brands`, APP-API-008 `GET /api/catalog-types`.

---

#### UC-20 — Create / Delete Catalog Item

| Field | Value |
|---|---|
| **UC id** | UC-20 |
| **Title** | Create or remove a catalog item (admin) |
| **Capability** | BIZ-CAP-038 (L3, ACTIVE, HIGH) |
| **Process** | BIZ-PROC-006 (steps 2–3, HIGH) |
| **Primary actor** | BIZ-ACT-003 Administrator |
| **Secondary actor** | BIZ-ACT-004 System / Service Account |

**Preconditions:** Administrator authenticated; reference brands/types exist (UC-04/UC-05).

**Main flow (BIZ-PROC-006 steps 2–3 + BR001/BR002/BR003/BR004):**
1. **Create:** Administrator submits a new catalog item (name, description, price, brand, type).
2. System validates name/description/price (**BR001**), brand id ≠ 0 (**BR002**), type id ≠ 0 (**BR003**), and generates the image path (**BR004**).
3. System persists the new CatalogItem (DATA-ENT-001) via APP-SVC-033 CreateCatalogItemEndpoint.
4. **Delete:** Administrator selects an existing catalog item to delete; system removes it via APP-SVC-034 DeleteCatalogItemEndpoint.
5. System refreshes the cached catalog list (UC-21).

**Alternative / exception flow:**
- **2a (BR001):** name/description/price invalid → create rejected.
- **2b (BR002):** brand id = 0 → create rejected.
- **2c (BR003):** type id = 0 → create rejected.

**Postconditions:** A CatalogItem is created (candidate event **EVT-08 CatalogItemCreated**) or deleted (candidate event **EVT-09 CatalogItemDeleted**); admin cache refreshed. Both events INFERRED.

**Related services:** APP-SVC-016 BlazorAdmin; APP-SVC-033 CreateCatalogItemEndpoint; APP-SVC-034 DeleteCatalogItemEndpoint; APP-SVC-001 Catalog. (Layering violations APP-DEP-004/005 — endpoints → EfRepository — to be broken at carve-out.)
**Related entities:** DATA-ENT-001 CatalogItem (BC-01, consumed by BC-05).
**Related APIs:** APP-API-005 `POST /api/catalog-items` (handler APP-SVC-033), APP-API-006 `DELETE /api/catalog-items/{catalogItemId}` (handler APP-SVC-034); admin edit page APP-API-048 `GET /Admin/EditCatalogItem`.

---

#### UC-21 — Refresh Cached Catalog Data

| Field | Value |
|---|---|
| **UC id** | UC-21 |
| **Title** | Refresh the locally cached catalog list after changes |
| **Capability** | BIZ-CAP-039 (L3, ACTIVE, HIGH) |
| **Process** | BIZ-PROC-006 (step 4, HIGH) |
| **Primary actor** | BIZ-ACT-004 System / Service Account |
| **Secondary actor** | BIZ-ACT-003 Administrator |

**Preconditions:** A catalog item has been created or deleted (UC-20).

**Main flow (BIZ-PROC-006 step 4):**
1. After a create/delete, the system refreshes the cached local catalog item list so the admin UI reflects the change (APP-SVC-049 RefreshBroadcast; cache decorators APP-SVC-044/045).

**Alternative / exception flow:** None in evidence.

**Postconditions:** Admin UI cache reflects the current catalog state. Candidate domain event **EVT-10 CatalogCacheRefreshed** (INFERRED).

**Related services:** APP-SVC-049 RefreshBroadcast; APP-SVC-044/045 cache decorators; APP-SVC-048 ToastComponent; APP-SVC-016 BlazorAdmin.
**Related entities:** None owned (operates on cached projection of DATA-ENT-001/002/003).
**Related APIs:** Client-side refresh within APP-API-040 `ROUTE /admin` (BlazorAdmin); re-reads APP-API-004/002/008.

---

## 6. Coverage Confirmation (all 39 capabilities)

| Coverage class | Count | Capabilities |
|---|---|---|
| Full L3 use case (functional leaves) | 20 | BIZ-CAP-003,004,005,007,008,009,012,013,014,016,019,020,021,023,031,032,034,037,038,039 |
| L1 summaries | 6 | BIZ-CAP-001,010,017,024,029,035 |
| L2 summaries | 11 | BIZ-CAP-002,006,011,015,018,022,025,027,030,033,036 |
| L3 aspirational (design-input UC, not discovered) | 1 | BIZ-CAP-026 Buyer Record Creation (RC-002; written as UC-15) |
| L3 INFERRED/LOW (noted, not specified) | 1 | BIZ-CAP-028 Payment Method Management (payment branch; BIZ-CAP-027 is its L2 parent, counted in L2 summaries) |

> **Note on the "20 functional leaves":** the 20 functional L3 capabilities receive full discovered-behavior use cases (BIZ-CAP-003, 004, 005, 007, 008, 009, 012, 013, 014, 016, 019, 020, 021, 023, 031, 032, 034, 037, 038, 039). **BIZ-CAP-026 Buyer Record Creation** is an aspirational L3 leaf (RC-002) and is written as a **design-input** use case (UC-15) rather than a discovered functional flow. The payment branch — **BIZ-CAP-027** (L2 Payment Information) and **BIZ-CAP-028** (L3 Payment Method Management) — is `inferred`/`LOW` and is noted only, not specified. All 39 capabilities are accounted for: 6 L1 + 11 L2 + 20 functional L3 + BIZ-CAP-026 (aspirational L3) + BIZ-CAP-028 (inferred L3) = 39 (BIZ-CAP-027 is counted within the 11 L2 summaries).

---

## 7. Assumptions (ASMP-FE-###) and Gaps

| Assumption | Statement | Basis | Impact |
|---|---|---|---|
| ASMP-FE-001 (reused) | A currency-bearing Money VO (VO-05) is NOT derivable; Price/UnitPrice are bare decimals. | key_attributes of DATA-ENT-001/005/007; no currency field; target_stack empty. | Currency is a NEW design element if required; amount-only candidate offered (UC-14). |
| ASMP-FE-003 (reused) | Buyer/Customer Profile (BC-06) is surfaced only from aspirational nodes; today the buyer ref is ApplicationUser. | DATA-ENT-010/011 persisted=false (RC-002); DATA-AGG-003 aspirational; DATA-REL-008/009 soft refs. | Do not generate Buyer/Payment persistence without an explicit decision (UC-15). |
| ASMP-FE-004 (reused) | Web-shell-served routes and the PublicApi authenticate endpoint are attributed to FUNCTIONAL contexts while physical hosting stays with BC-07. | service_to_api maps APP-API-014..052 → APP-SVC-006; APP-API-001 → APP-SVC-011. | Distinguish functional ownership from physical hosting in UC-07..UC-12, UC-16. |
| ASMP-FE-010 | UC-00 Browse Catalog flow is limited to the single evidenced value-stream step. | BIZ-PROC-001 has 1 step, confidence MEDIUM; "not detailed in process models" (graph). | Detailed browse/filter/pagination behavior must be confirmed before generation; minimal flow given. |
| ASMP-FE-011 | Brand (UC-04) and Type (UC-05) management is limited to list/reference + seeding; no create/update/delete process or API exists in evidence. | Only APP-API-002 / APP-API-008 (GET) exist; BIZ-PROC-006 step references listing only. | Brand/type CRUD is a NEW design element if required; do not assert it as discovered. |
| ASMP-FE-012 | Catalog Seeding (UC-06) and Identity Data Seeding (UC-18) flows are minimal/trigger-bounded. | BIZ-PROC-009 and BIZ-PROC-010 both have 0 steps, confidence MEDIUM. | Seed content, ordering and idempotency must be confirmed; minimal flows given. |
| ASMP-FE-013 | Basket adjustment (UC-08) detailed sub-steps are not in evidence; flow bounded to the single step + BR006/BR007. | BIZ-PROC-004 has 1 step, confidence MEDIUM (value-stream stage). | Detailed adjust/remove interaction must be confirmed; minimal flow given. |
| ASMP-FE-014 | UC-15 Buyer Record Creation flow is bounded to BR008/BR011; no step-level process and target entity is aspirational. | BIZ-PROC-008 has 0 steps; DATA-ENT-010 persisted=false. | Buyer creation behavior is a design input; do not generate persistence without a decision. |
| ASMP-FE-015 | No use case is written for the Payment branch (BIZ-CAP-027/028); they are inferred-LOW with no process/service/API. | BIZ-CAP-027/028 status=inferred conf=LOW; DATA-ENT-011 aspirational; DATA-REL-012 aspirational. | Payment behavior is a future forward-engineering decision, never asserted as discovered. |

**Open questions referenced:** OQ-001 (Admin vs BlazorAdmin merge — UC-19/20/21), OQ-005 (JWT enforcement / CORS on PublicApi — UC-16/17), OQ-009 (synthetic ROUTE/CLI method labels — APP-API-040/051).

**Explicitly flagged behavioral gaps:** UC-00 (1-step browse), UC-04/UC-05 (no brand/type CRUD), UC-06/UC-18 (0-step seeding), UC-08 (1-step adjust), UC-15 (0-step aspirational buyer), §5.4.1 (no payment behavior). Basket capabilities (UC-07/08/09/10) and order checkout pages (UC-11/12/13) have **no dedicated REST API** in evidence — they are Razor-page/handler-served via the Web shell (APP-SVC-006), recorded as a hosting gap, not invented APIs.
