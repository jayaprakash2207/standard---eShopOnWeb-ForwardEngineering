# Traceability Matrix — eShopOnWeb Enterprise Foundation Package

> **Source of truth:** `ENTERPRISE_KNOWLEDGE_GRAPH.json` (schema_version 1.0). Generated 2026-06-23.  
> **System:** eShopOnWeb (authoritative name 'unknown' in source evidence).  
> **Evidence root:** `bussiness-architecture 1/bussiness-architecture/output/eShopOnWeb`.

This document renders the **verified canonical knowledge graph** as an end-to-end traceability view across the four architecture layers (Business → Data → Application → Technology). It carries **only** content present in the graph; every node and link keeps its graph **id** so this document cross-references the JSON directly. Confidence (`HIGH`/`MEDIUM`/`LOW` or numeric) and status signals are preserved verbatim. This is a **foundation package**: it describes the current + canonical state and the verified inputs for future forward engineering. It proposes no code and no new designs.

Evidence-only consolidation. Confidence/status signals (HIGH/MEDIUM/LOW, ACTIVE/DORMANT, implemented/aspirational-unimplemented, INFERRED, VERSION UNKNOWN, soft-reference, RC-002 dead code) are preserved verbatim from source fragments. No forward engineering; no new capabilities/entities/APIs invented. Cross-links are emitted only where a source file supports them.

## 1. How to read the traceability chain

The canonical chain is:

```
Capability  →  Process  →  Entity  →  Service  →  API
 (BIZ-CAP)     (BIZ-PROC)  (DATA-ENT) (APP-SVC)   (APP-API)
```

Each hop is a separately evidenced cross-link in the graph (`capability_to_process`, `process_to_entity`, `entity_to_service`, `service_to_api`). A chain row below is the transitive join of these links. Where the graph carries **no** link for a hop, the cell shows `—` with a footnote explaining the missing/unverified relationship.

**Topology note (important for the Service → API hop):** in this graph the **entity-owning services** are the domain/component modules — `APP-SVC-001 Catalog`, `APP-SVC-002 Identity`, `APP-SVC-003 Basket`, `APP-SVC-004 Order`, `APP-SVC-008 DataAccess` — whereas the **API-hosting services** are the deployable runtime units — `APP-SVC-006 Web`, `APP-SVC-011 PublicApi`, `APP-SVC-016 BlazorAdmin`. The graph's `service_to_api` links attach APIs to the deployable host (derived from each interface's `source_file` path, per ASSUMP-004), **not** to the domain module that owns the entity. Consequently the Service → API hop does **not** continue from the entity-owning service in any primary chain; this is recorded as a structural gap (see footnote [^svcapi] and §5).

## 2. Primary traceability matrix (Capability → Process → Entity → Service → API)

One row per traceable chain. IDs and names are shown for each hop. `—` marks a hop the graph does not link, footnoted below the table.

| # | Capability | Process | Entity | Service (entity owner) | API |
|---|------------|---------|--------|------------------------|-----|
| 1 | `BIZ-CAP-002` Product Information Management | `BIZ-PROC-001` Browse Catalog | `DATA-ENT-001` CatalogItem | `APP-SVC-001` Catalog | — [^svcapi] |
| 2 | `BIZ-CAP-002` Product Information Management | `BIZ-PROC-001` Browse Catalog | `DATA-ENT-001` CatalogItem | `APP-SVC-008` DataAccess | — [^svcapi] |
| 3 | `BIZ-CAP-002` Product Information Management | `BIZ-PROC-001` Browse Catalog | `DATA-ENT-002` CatalogBrand | `APP-SVC-001` Catalog | — [^svcapi] |
| 4 | `BIZ-CAP-002` Product Information Management | `BIZ-PROC-001` Browse Catalog | `DATA-ENT-003` CatalogType | `APP-SVC-001` Catalog | — [^svcapi] |
| 5 | `BIZ-CAP-009` Catalog Seeding | `BIZ-PROC-009` Catalog Seeding | `DATA-ENT-001` CatalogItem | `APP-SVC-001` Catalog | — [^svcapi] |
| 6 | `BIZ-CAP-009` Catalog Seeding | `BIZ-PROC-009` Catalog Seeding | `DATA-ENT-001` CatalogItem | `APP-SVC-008` DataAccess | — [^svcapi] |
| 7 | `BIZ-CAP-009` Catalog Seeding | `BIZ-PROC-009` Catalog Seeding | `DATA-ENT-002` CatalogBrand | `APP-SVC-001` Catalog | — [^svcapi] |
| 8 | `BIZ-CAP-009` Catalog Seeding | `BIZ-PROC-009` Catalog Seeding | `DATA-ENT-003` CatalogType | `APP-SVC-001` Catalog | — [^svcapi] |
| 9 | `BIZ-CAP-012` Add Item to Basket | `BIZ-PROC-002` Add Item to Basket | `DATA-ENT-004` Basket | `APP-SVC-003` Basket | — [^svcapi] |
| 10 | `BIZ-CAP-012` Add Item to Basket | `BIZ-PROC-002` Add Item to Basket | `DATA-ENT-005` BasketItem | `APP-SVC-003` Basket | — [^svcapi] |
| 11 | `BIZ-CAP-012` Add Item to Basket | `BIZ-PROC-002` Add Item to Basket | `DATA-ENT-001` CatalogItem | `APP-SVC-001` Catalog | — [^svcapi] |
| 12 | `BIZ-CAP-012` Add Item to Basket | `BIZ-PROC-002` Add Item to Basket | `DATA-ENT-001` CatalogItem | `APP-SVC-008` DataAccess | — [^svcapi] |
| 13 | `BIZ-CAP-013` Quantity Adjustment | `BIZ-PROC-004` Adjust Basket | `DATA-ENT-005` BasketItem | `APP-SVC-003` Basket | — [^svcapi] |
| 14 | `BIZ-CAP-013` Quantity Adjustment | `BIZ-PROC-004` Adjust Basket | `DATA-ENT-004` Basket | `APP-SVC-003` Basket | — [^svcapi] |
| 15 | `BIZ-CAP-014` Basket Cleanup | `BIZ-PROC-004` Adjust Basket | `DATA-ENT-005` BasketItem | `APP-SVC-003` Basket | — [^svcapi] |
| 16 | `BIZ-CAP-014` Basket Cleanup | `BIZ-PROC-004` Adjust Basket | `DATA-ENT-004` Basket | `APP-SVC-003` Basket | — [^svcapi] |
| 17 | `BIZ-CAP-016` Anonymous-to-Registered Basket Transfer | `BIZ-PROC-003` Transfer Anonymous Basket to Registered User | `DATA-ENT-004` Basket | `APP-SVC-003` Basket | — [^svcapi] |
| 18 | `BIZ-CAP-016` Anonymous-to-Registered Basket Transfer | `BIZ-PROC-003` Transfer Anonymous Basket to Registered User | `DATA-ENT-005` BasketItem | `APP-SVC-003` Basket | — [^svcapi] |
| 19 | `BIZ-CAP-016` Anonymous-to-Registered Basket Transfer | `BIZ-PROC-003` Transfer Anonymous Basket to Registered User | `DATA-ENT-008` ApplicationUser | `APP-SVC-002` Identity | — [^svcapi] |
| 20 | `BIZ-CAP-019` Checkout Processing | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-004` Basket | `APP-SVC-003` Basket | — [^svcapi] |
| 21 | `BIZ-CAP-019` Checkout Processing | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-006` Order | `APP-SVC-004` Order | — [^svcapi] |
| 22 | `BIZ-CAP-019` Checkout Processing | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-007` OrderItem | `APP-SVC-004` Order | — [^svcapi] |
| 23 | `BIZ-CAP-019` Checkout Processing | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-012` CatalogItemOrdered | `APP-SVC-001` Catalog | — [^svcapi] |
| 24 | `BIZ-CAP-019` Checkout Processing | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-013` Address | `APP-SVC-004` Order | — [^svcapi] |
| 25 | `BIZ-CAP-019` Checkout Processing | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-001` CatalogItem | `APP-SVC-001` Catalog | — [^svcapi] |
| 26 | `BIZ-CAP-019` Checkout Processing | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-001` CatalogItem | `APP-SVC-008` DataAccess | — [^svcapi] |
| 27 | `BIZ-CAP-020` Empty Basket Protection | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-004` Basket | `APP-SVC-003` Basket | — [^svcapi] |
| 28 | `BIZ-CAP-020` Empty Basket Protection | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-006` Order | `APP-SVC-004` Order | — [^svcapi] |
| 29 | `BIZ-CAP-020` Empty Basket Protection | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-007` OrderItem | `APP-SVC-004` Order | — [^svcapi] |
| 30 | `BIZ-CAP-020` Empty Basket Protection | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-012` CatalogItemOrdered | `APP-SVC-001` Catalog | — [^svcapi] |
| 31 | `BIZ-CAP-020` Empty Basket Protection | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-013` Address | `APP-SVC-004` Order | — [^svcapi] |
| 32 | `BIZ-CAP-020` Empty Basket Protection | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-001` CatalogItem | `APP-SVC-001` Catalog | — [^svcapi] |
| 33 | `BIZ-CAP-020` Empty Basket Protection | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-001` CatalogItem | `APP-SVC-008` DataAccess | — [^svcapi] |
| 34 | `BIZ-CAP-021` Ordered Item Snapshot | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-004` Basket | `APP-SVC-003` Basket | — [^svcapi] |
| 35 | `BIZ-CAP-021` Ordered Item Snapshot | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-006` Order | `APP-SVC-004` Order | — [^svcapi] |
| 36 | `BIZ-CAP-021` Ordered Item Snapshot | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-007` OrderItem | `APP-SVC-004` Order | — [^svcapi] |
| 37 | `BIZ-CAP-021` Ordered Item Snapshot | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-012` CatalogItemOrdered | `APP-SVC-001` Catalog | — [^svcapi] |
| 38 | `BIZ-CAP-021` Ordered Item Snapshot | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-013` Address | `APP-SVC-004` Order | — [^svcapi] |
| 39 | `BIZ-CAP-021` Ordered Item Snapshot | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-001` CatalogItem | `APP-SVC-001` Catalog | — [^svcapi] |
| 40 | `BIZ-CAP-021` Ordered Item Snapshot | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-001` CatalogItem | `APP-SVC-008` DataAccess | — [^svcapi] |
| 41 | `BIZ-CAP-023` Order Total Calculation | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-004` Basket | `APP-SVC-003` Basket | — [^svcapi] |
| 42 | `BIZ-CAP-023` Order Total Calculation | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-006` Order | `APP-SVC-004` Order | — [^svcapi] |
| 43 | `BIZ-CAP-023` Order Total Calculation | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-007` OrderItem | `APP-SVC-004` Order | — [^svcapi] |
| 44 | `BIZ-CAP-023` Order Total Calculation | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-012` CatalogItemOrdered | `APP-SVC-001` Catalog | — [^svcapi] |
| 45 | `BIZ-CAP-023` Order Total Calculation | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-013` Address | `APP-SVC-004` Order | — [^svcapi] |
| 46 | `BIZ-CAP-023` Order Total Calculation | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-001` CatalogItem | `APP-SVC-001` Catalog | — [^svcapi] |
| 47 | `BIZ-CAP-023` Order Total Calculation | `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-001` CatalogItem | `APP-SVC-008` DataAccess | — [^svcapi] |
| 48 | `BIZ-CAP-026` Buyer Record Creation | `BIZ-PROC-008` Buyer Record Creation | `DATA-ENT-010` Buyer | `APP-SVC-004` Order | — [^svcapi] |
| 49 | `BIZ-CAP-026` Buyer Record Creation | `BIZ-PROC-008` Buyer Record Creation | `DATA-ENT-008` ApplicationUser | `APP-SVC-002` Identity | — [^svcapi] |
| 50 | `BIZ-CAP-031` User Login | `BIZ-PROC-007` User Authentication | `DATA-ENT-008` ApplicationUser | `APP-SVC-002` Identity | — [^svcapi] |
| 51 | `BIZ-CAP-031` User Login | `BIZ-PROC-007` User Authentication | `DATA-ENT-009` Role | `APP-SVC-002` Identity | — [^svcapi] |
| 52 | `BIZ-CAP-032` Token Issuance | `BIZ-PROC-007` User Authentication | `DATA-ENT-008` ApplicationUser | `APP-SVC-002` Identity | — [^svcapi] |
| 53 | `BIZ-CAP-032` Token Issuance | `BIZ-PROC-007` User Authentication | `DATA-ENT-009` Role | `APP-SVC-002` Identity | — [^svcapi] |
| 54 | `BIZ-CAP-034` Identity Data Seeding | `BIZ-PROC-010` Identity Data Seeding | `DATA-ENT-008` ApplicationUser | `APP-SVC-002` Identity | — [^svcapi] |
| 55 | `BIZ-CAP-034` Identity Data Seeding | `BIZ-PROC-010` Identity Data Seeding | `DATA-ENT-009` Role | `APP-SVC-002` Identity | — [^svcapi] |
| 56 | `BIZ-CAP-037` Catalog Item List View | `BIZ-PROC-006` Catalog Item Administration | `DATA-ENT-001` CatalogItem | `APP-SVC-001` Catalog | — [^svcapi] |
| 57 | `BIZ-CAP-037` Catalog Item List View | `BIZ-PROC-006` Catalog Item Administration | `DATA-ENT-001` CatalogItem | `APP-SVC-008` DataAccess | — [^svcapi] |
| 58 | `BIZ-CAP-037` Catalog Item List View | `BIZ-PROC-006` Catalog Item Administration | `DATA-ENT-002` CatalogBrand | `APP-SVC-001` Catalog | — [^svcapi] |
| 59 | `BIZ-CAP-037` Catalog Item List View | `BIZ-PROC-006` Catalog Item Administration | `DATA-ENT-003` CatalogType | `APP-SVC-001` Catalog | — [^svcapi] |
| 60 | `BIZ-CAP-038` Catalog Item Create/Delete | `BIZ-PROC-006` Catalog Item Administration | `DATA-ENT-001` CatalogItem | `APP-SVC-001` Catalog | — [^svcapi] |
| 61 | `BIZ-CAP-038` Catalog Item Create/Delete | `BIZ-PROC-006` Catalog Item Administration | `DATA-ENT-001` CatalogItem | `APP-SVC-008` DataAccess | — [^svcapi] |
| 62 | `BIZ-CAP-038` Catalog Item Create/Delete | `BIZ-PROC-006` Catalog Item Administration | `DATA-ENT-002` CatalogBrand | `APP-SVC-001` Catalog | — [^svcapi] |
| 63 | `BIZ-CAP-038` Catalog Item Create/Delete | `BIZ-PROC-006` Catalog Item Administration | `DATA-ENT-003` CatalogType | `APP-SVC-001` Catalog | — [^svcapi] |
| 64 | `BIZ-CAP-039` Cached Data Refresh | `BIZ-PROC-006` Catalog Item Administration | `DATA-ENT-001` CatalogItem | `APP-SVC-001` Catalog | — [^svcapi] |
| 65 | `BIZ-CAP-039` Cached Data Refresh | `BIZ-PROC-006` Catalog Item Administration | `DATA-ENT-001` CatalogItem | `APP-SVC-008` DataAccess | — [^svcapi] |
| 66 | `BIZ-CAP-039` Cached Data Refresh | `BIZ-PROC-006` Catalog Item Administration | `DATA-ENT-002` CatalogBrand | `APP-SVC-001` Catalog | — [^svcapi] |
| 67 | `BIZ-CAP-039` Cached Data Refresh | `BIZ-PROC-006` Catalog Item Administration | `DATA-ENT-003` CatalogType | `APP-SVC-001` Catalog | — [^svcapi] |

_Total traceable chains: **67**._

[^svcapi]: **Service → API not linked for entity-owning services.** The graph's `service_to_api` links attach all 55 APIs to the three deployable hosts (`APP-SVC-006 Web`, `APP-SVC-011 PublicApi`, `APP-SVC-016 BlazorAdmin`), derived from each interface's `source_file` path (ASSUMP-004). No `service_to_api` link exists from the domain/component services (`APP-SVC-001 Catalog`, `-002 Identity`, `-003 Basket`, `-004 Order`, `-008 DataAccess`) that own the entities. The API column therefore terminates at `—`; the full Service → API mapping is given in §3.4 against the deployable hosts. Bridging entity-owning module → deployable-host API is an open structural question (see ARCH-VIOL-001 / `APP-DEP-002`, where an endpoint reaches a repository directly) and is left for forward engineering.

## 3. Per cross-link-type tables

Each table lists every link of one type with its evidence and confidence, exactly as carried in the graph's `cross_links`.

### 3.1 `capability_to_process`

_17 links._

| Capability | → Process | Confidence | Evidence | Note |
|------------|-----------|------------|----------|------|
| `BIZ-CAP-002` Product Information Management | `BIZ-PROC-001` Browse Catalog | MEDIUM | ba_documents/02_value_stream.md :: Stage 1 Browse Catalog (Product Information / catalog viewing) | Browse Catalog stage exercises Product Information Management; not a step-level process in evidence. |
| `BIZ-CAP-012` Add Item to Basket | `BIZ-PROC-002` Add Item to Basket | HIGH | ba_documents/03_process_models.md :: Process: Add Item to Basket; ba_documents/01_capability_map.md :: L3: Add Item to Basket [ACTIVE] |  |
| `BIZ-CAP-016` Anonymous-to-Registered Basket Transfer | `BIZ-PROC-003` Transfer Anonymous Basket to Registered User | HIGH | ba_documents/03_process_models.md :: Process: Transfer Anonymous Basket to Registered User; ba_documents/01_capability_map.md :: L3: Anonymous-to-Registered Basket Transfer [ACTIVE] |  |
| `BIZ-CAP-013` Quantity Adjustment | `BIZ-PROC-004` Adjust Basket | MEDIUM | ba_documents/02_value_stream.md :: Stage 4 Adjust Basket (quantity adjustment / cleanup); ba_documents/04_business_rules.md :: BR006/BR007 basket quantity rules |  |
| `BIZ-CAP-014` Basket Cleanup | `BIZ-PROC-004` Adjust Basket | MEDIUM | ba_documents/04_business_rules.md :: BR006: zero-quantity basket line removed (Basket.cs) |  |
| `BIZ-CAP-019` Checkout Processing | `BIZ-PROC-005` Checkout / Place Order | HIGH | ba_documents/03_process_models.md :: Process: Checkout / Place Order; ba_documents/01_capability_map.md :: L3: Checkout Processing [ACTIVE] |  |
| `BIZ-CAP-020` Empty Basket Protection | `BIZ-PROC-005` Checkout / Place Order | HIGH | ba_documents/03_process_models.md :: Checkout step 2: block checkout if basket empty (BR012) |  |
| `BIZ-CAP-021` Ordered Item Snapshot | `BIZ-PROC-005` Checkout / Place Order | HIGH | ba_documents/03_process_models.md :: Checkout step 4: snapshot ordered item (name, picture, price) |  |
| `BIZ-CAP-023` Order Total Calculation | `BIZ-PROC-005` Checkout / Place Order | HIGH | ba_documents/03_process_models.md :: Checkout step 6: calculate order total (BR010) |  |
| `BIZ-CAP-038` Catalog Item Create/Delete | `BIZ-PROC-006` Catalog Item Administration | HIGH | ba_documents/03_process_models.md :: Process: Catalog Item Administration (create/delete item); ba_documents/01_capability_map.md :: L3: Catalog Item Create/Delete [ACTIVE] |  |
| `BIZ-CAP-037` Catalog Item List View | `BIZ-PROC-006` Catalog Item Administration | HIGH | ba_documents/03_process_models.md :: Catalog Item Administration step 1: view list of items, types, brands |  |
| `BIZ-CAP-039` Cached Data Refresh | `BIZ-PROC-006` Catalog Item Administration | HIGH | ba_documents/03_process_models.md :: Catalog Item Administration step 4: refresh cached catalog list |  |
| `BIZ-CAP-031` User Login | `BIZ-PROC-007` User Authentication | HIGH | ba_documents/03_process_models.md :: Process: User Authentication step 2 (validate credentials/lockout); ba_documents/01_capability_map.md :: L3: User Login [ACTIVE] |  |
| `BIZ-CAP-032` Token Issuance | `BIZ-PROC-007` User Authentication | HIGH | ba_documents/03_process_models.md :: User Authentication step 3: generate signed JWT token; ba_documents/01_capability_map.md :: L3: Token Issuance [ACTIVE] |  |
| `BIZ-CAP-026` Buyer Record Creation | `BIZ-PROC-008` Buyer Record Creation | LOW | ba_documents/01_capability_map.md :: L3: Buyer Record Creation [ACTIVE]; ba_documents/04_business_rules.md :: BR008 reject buyer creation without valid identity | Buyer Record Creation is tagged ACTIVE in the capability map, but the underlying Buyer entity is CONFIRMED dead/unimplemented code (RC-002; DATA-ENT-010 status=aspirational/unimplemented). Treat as aspirational, consistent with the entity_to_service / process_to_entity Buyer links. |
| `BIZ-CAP-009` Catalog Seeding | `BIZ-PROC-009` Catalog Seeding | MEDIUM | ba_documents/01_capability_map.md :: L3: Catalog Seeding [ACTIVE] |  |
| `BIZ-CAP-034` Identity Data Seeding | `BIZ-PROC-010` Identity Data Seeding | MEDIUM | ba_documents/01_capability_map.md :: L3: Identity Data Seeding [ACTIVE] |  |

### 3.2 `process_to_entity`

_29 links._

| Process | → Entity | Confidence | Evidence | Note |
|---------|----------|------------|----------|------|
| `BIZ-PROC-001` Browse Catalog | `DATA-ENT-001` CatalogItem | MEDIUM | ba_documents/02_value_stream.md :: Browse Catalog: views catalog items filtered by brand/type |  |
| `BIZ-PROC-001` Browse Catalog | `DATA-ENT-002` CatalogBrand | LOW | ba_documents/02_value_stream.md :: Browse Catalog: filter by brand |  |
| `BIZ-PROC-001` Browse Catalog | `DATA-ENT-003` CatalogType | LOW | ba_documents/02_value_stream.md :: Browse Catalog: filter by type |  |
| `BIZ-PROC-002` Add Item to Basket | `DATA-ENT-004` Basket | HIGH | ba_documents/03_process_models.md :: Add Item to Basket: retrieve/create the basket, persist; ba_documents/04_business_rules.md :: BR005 (Basket.cs) |  |
| `BIZ-PROC-002` Add Item to Basket | `DATA-ENT-005` BasketItem | HIGH | ba_documents/04_business_rules.md :: BR005 add/increase basket line item (BasketItem) |  |
| `BIZ-PROC-002` Add Item to Basket | `DATA-ENT-001` CatalogItem | MEDIUM | ba_documents/03_process_models.md :: Add Item to Basket trigger: selects a catalog item |  |
| `BIZ-PROC-003` Transfer Anonymous Basket to Registered User | `DATA-ENT-004` Basket | HIGH | ba_documents/03_process_models.md :: Transfer Anonymous Basket: retrieve/merge baskets |  |
| `BIZ-PROC-003` Transfer Anonymous Basket to Registered User | `DATA-ENT-005` BasketItem | HIGH | ba_documents/03_process_models.md :: Transfer Anonymous Basket step 3: copy each item |  |
| `BIZ-PROC-003` Transfer Anonymous Basket to Registered User | `DATA-ENT-008` ApplicationUser | MEDIUM | ba_documents/03_process_models.md :: Transfer to now-registered user (ApplicationUser identity) |  |
| `BIZ-PROC-004` Adjust Basket | `DATA-ENT-005` BasketItem | MEDIUM | ba_documents/04_business_rules.md :: BR007 negative basket quantity rejected (BasketItem.cs) |  |
| `BIZ-PROC-004` Adjust Basket | `DATA-ENT-004` Basket | MEDIUM | ba_documents/04_business_rules.md :: BR006 zero-quantity basket line removed (Basket.cs) |  |
| `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-004` Basket | HIGH | ba_documents/03_process_models.md :: Checkout step 1-2: retrieve basket, verify non-empty |  |
| `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-006` Order | HIGH | ba_documents/03_process_models.md :: Checkout step 5: create the order with buyer ID, address, items; ba_documents/04_business_rules.md :: BR010/BR011 (Order.cs) |  |
| `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-007` OrderItem | HIGH | ba_documents/03_process_models.md :: Checkout: create order items (OrderItem) |  |
| `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-012` CatalogItemOrdered | HIGH | ba_documents/03_process_models.md :: Checkout step 4: snapshot ordered item (CatalogItemOrdered); ba_documents/04_business_rules.md :: BR009 order line requires catalog item id/name/picture (CatalogItemOrdered.cs) |  |
| `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-013` Address | HIGH | ba_documents/03_process_models.md :: Checkout step 5: order with shipping address (Address owned type) |  |
| `BIZ-PROC-005` Checkout / Place Order | `DATA-ENT-001` CatalogItem | MEDIUM | ba_documents/03_process_models.md :: Checkout step 3: retrieve full catalog item details for each basket item |  |
| `BIZ-PROC-006` Catalog Item Administration | `DATA-ENT-001` CatalogItem | HIGH | ba_documents/03_process_models.md :: Catalog Item Administration: create/delete catalog item; ba_documents/04_business_rules.md :: BR001/BR004 (CatalogItem.cs) |  |
| `BIZ-PROC-006` Catalog Item Administration | `DATA-ENT-002` CatalogBrand | MEDIUM | ba_documents/03_process_models.md :: Admin views/uses brands; ba_documents/04_business_rules.md :: BR002 brand ID != 0 |  |
| `BIZ-PROC-006` Catalog Item Administration | `DATA-ENT-003` CatalogType | MEDIUM | ba_documents/03_process_models.md :: Admin views/uses types; ba_documents/04_business_rules.md :: BR003 type ID != 0 |  |
| `BIZ-PROC-007` User Authentication | `DATA-ENT-008` ApplicationUser | HIGH | ba_documents/03_process_models.md :: User Authentication step 2: validate credentials against identity store |  |
| `BIZ-PROC-007` User Authentication | `DATA-ENT-009` Role | MEDIUM | ba_documents/03_process_models.md :: User Authentication step 3: JWT contains role claims |  |
| `BIZ-PROC-008` Buyer Record Creation | `DATA-ENT-010` Buyer | LOW | ba_documents/04_business_rules.md :: BR008 buyer record creation (Buyer.cs); ba_documents/01_capability_map.md :: Buyer Record Creation linked to identity account | Buyer (DATA-ENT-010) is aspirational/unimplemented (RC-002); the process is rule-described but not a live persisted flow. |
| `BIZ-PROC-008` Buyer Record Creation | `DATA-ENT-008` ApplicationUser | LOW | ba_documents/04_business_rules.md :: BR008 reject buyer without valid identity reference | BIZ-PROC-008 (Buyer Record Creation) is a business-rule-described but unimplemented flow (RC-002); the ApplicationUser association is theoretical (rule BR008) rather than an observed runtime persistence path. |
| `BIZ-PROC-009` Catalog Seeding | `DATA-ENT-001` CatalogItem | MEDIUM | ba_documents/01_capability_map.md :: Catalog Seeding: populate initial catalog data |  |
| `BIZ-PROC-009` Catalog Seeding | `DATA-ENT-002` CatalogBrand | LOW | ba_documents/01_capability_map.md :: Catalog Reference Data seeding (brands) |  |
| `BIZ-PROC-009` Catalog Seeding | `DATA-ENT-003` CatalogType | LOW | ba_documents/01_capability_map.md :: Catalog Reference Data seeding (types) |  |
| `BIZ-PROC-010` Identity Data Seeding | `DATA-ENT-008` ApplicationUser | MEDIUM | ba_documents/01_capability_map.md :: Identity Data Seeding: populate initial user accounts |  |
| `BIZ-PROC-010` Identity Data Seeding | `DATA-ENT-009` Role | MEDIUM | ba_documents/01_capability_map.md :: Identity Data Seeding: populate roles |  |

### 3.3 `entity_to_service`

_16 links._

| Entity | → Service | Confidence | Evidence | Note |
|--------|-----------|------------|----------|------|
| `DATA-ENT-001` CatalogItem | `APP-SVC-001` Catalog | HIGH | aa-outputs/final/data-ownership-map.md :: CatalogItem \| COMP-0005 \| Catalog \| CAP-001 Catalog |  |
| `DATA-ENT-002` CatalogBrand | `APP-SVC-001` Catalog | HIGH | aa-outputs/final/data-ownership-map.md :: CatalogBrand \| COMP-0004 \| Catalog |  |
| `DATA-ENT-003` CatalogType | `APP-SVC-001` Catalog | HIGH | aa-outputs/final/data-ownership-map.md :: CatalogType \| COMP-0007 \| Catalog |  |
| `DATA-ENT-014` CatalogItemDetails | `APP-SVC-001` Catalog | MEDIUM | aa-outputs/final/data-ownership-map.md :: CatalogItemDetails \| COMP-0006 \| Catalog |  |
| `DATA-ENT-012` CatalogItemOrdered | `APP-SVC-001` Catalog | MEDIUM | aa-outputs/final/data-ownership-map.md :: CatalogItemOrdered \| COMP-0013 \| Catalog \| CAP-001 Catalog | Ownership map assigns CatalogItemOrdered to Catalog module though it is physically an owned type of OrderAggregate (DATA-AGG-002). |
| `DATA-ENT-004` Basket | `APP-SVC-003` Basket | HIGH | aa-outputs/final/data-ownership-map.md :: Basket \| COMP-0008 \| Basket \| CAP-005 Basket |  |
| `DATA-ENT-005` BasketItem | `APP-SVC-003` Basket | HIGH | aa-outputs/final/data-ownership-map.md :: BasketItem \| COMP-0009 \| Basket |  |
| `DATA-ENT-006` Order | `APP-SVC-004` Order | HIGH | aa-outputs/final/data-ownership-map.md :: Order \| COMP-0014 \| Order \| CAP-007 Order |  |
| `DATA-ENT-007` OrderItem | `APP-SVC-004` Order | HIGH | aa-outputs/final/data-ownership-map.md :: OrderItem \| COMP-0015 \| Order |  |
| `DATA-ENT-013` Address | `APP-SVC-004` Order | HIGH | aa-outputs/final/data-ownership-map.md :: Address \| COMP-0012 \| Order |  |
| `DATA-ENT-010` Buyer | `APP-SVC-004` Order | LOW | aa-outputs/final/data-ownership-map.md :: Buyer \| COMP-0010 \| Order \| CAP-007 Order | Buyer is owned (per ownership map) by Order module but is aspirational/unimplemented dead code (RC-002). |
| `DATA-ENT-011` PaymentMethod | `APP-SVC-004` Order | LOW | aa-outputs/final/data-ownership-map.md :: PaymentMethod \| COMP-0011 \| Order \| CAP-007 Order | PaymentMethod owned (per ownership map) by Order module but aspirational/unimplemented dead code (RC-002). |
| `DATA-ENT-008` ApplicationUser | `APP-SVC-002` Identity | HIGH | aa-outputs/final/data-ownership-map.md :: ApplicationUser \| COMP-0099 \| Identity \| CAP-002 Identity |  |
| `DATA-ENT-009` Role | `APP-SVC-002` Identity | MEDIUM | da-outputs/data-dictionary.md :: AspNetRoles in IdentityDb (AppIdentityDbContext, Identity module); aa-outputs/final/data-ownership-map.md :: AppIdentityDbContext \| COMP-0097 \| Identity |  |
| `DATA-ENT-015` BaseEntity | `APP-SVC-007` ApplicationCore | HIGH | aa-outputs/final/data-ownership-map.md :: BaseEntity \| COMP-0003 \| ApplicationCore \| CAP-008 Application |  |
| `DATA-ENT-001` CatalogItem | `APP-SVC-008` DataAccess | MEDIUM | da-outputs/data-flow-map.md :: IRepository<CatalogItem> (CatalogContext) via EfRepository; aa-outputs/final/data-ownership-map.md :: EfRepository \| COMP-0087 \| DataAccess | Persistence is mediated by DataAccess (EfRepository) over CatalogContext; logical capability ownership remains Catalog. |

### 3.4 `service_to_api`

_55 links. APIs are attached to deployable hosts (Web / PublicApi / BlazorAdmin)._

| Service (host) | → API | Confidence | Evidence | Note |
|----------------|-------|------------|----------|------|
| `APP-SVC-011` PublicApi | `APP-API-001` POST /api/authenticate | HIGH | aa-outputs/final/application-interface-catalogue.json :: INT-001 source_file=src/PublicApi/AuthEndpoints/AuthenticateEndpoint.cs (owner_module=Identity, entry_component=AuthenticateEndpoint) | Handler AuthenticateEndpoint attributed to Identity module; hosted in PublicApi deployable. |
| `APP-SVC-011` PublicApi | `APP-API-002` GET /api/catalog-brands | HIGH | aa-outputs/final/application-interface-catalogue.json :: INT-002 CatalogBrandListEndpoint (PublicApi, Catalog module) |  |
| `APP-SVC-011` PublicApi | `APP-API-003` GET /api/catalog-items/{catalogItemId} | HIGH | aa-outputs/final/application-interface-catalogue.json :: INT-003 CatalogItemGetByIdEndpoint (PublicApi) |  |
| `APP-SVC-011` PublicApi | `APP-API-004` GET /api/catalog-items | HIGH | aa-outputs/final/application-interface-catalogue.json :: INT-004 CatalogItemListPagedEndpoint (PublicApi) |  |
| `APP-SVC-011` PublicApi | `APP-API-005` POST /api/catalog-items | HIGH | aa-outputs/final/application-interface-catalogue.json :: INT-005 CreateCatalogItemEndpoint (PublicApi) |  |
| `APP-SVC-011` PublicApi | `APP-API-006` DELETE /api/catalog-items/{catalogItemId} | HIGH | aa-outputs/final/application-interface-catalogue.json :: INT-006 DeleteCatalogItemEndpoint (PublicApi) |  |
| `APP-SVC-011` PublicApi | `APP-API-007` PUT /api/catalog-items | HIGH | aa-outputs/final/application-interface-catalogue.json :: INT-007 UpdateCatalogItemEndpoint (PublicApi) |  |
| `APP-SVC-011` PublicApi | `APP-API-008` GET /api/catalog-types | HIGH | aa-outputs/final/application-interface-catalogue.json :: INT-008 CatalogTypeListEndpoint (PublicApi) |  |
| `APP-SVC-011` PublicApi | `APP-API-054` CLI .NET application bootstrap Program.cs (PublicApi) | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-054 PublicApi Program.cs bootstrap |  |
| `APP-SVC-006` Web | `APP-API-009` ROUTE /{controller:slugify=Home}/{action:slugify=Index}/{id?} | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-009 source_file=src/Web/Program.cs (owner_module=CrossCutting, entry_component=Program) |  |
| `APP-SVC-006` Web | `APP-API-010` ROUTE ASP.NET Razor Pages route registration | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-010 source_file=src/Web/Program.cs (owner_module=CrossCutting, entry_component=Program) |  |
| `APP-SVC-006` Web | `APP-API-011` ROUTE /index.html | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-011 source_file=src/Web/Program.cs (owner_module=CrossCutting, entry_component=Program) |  |
| `APP-SVC-006` Web | `APP-API-012` GET /home_page_health_check | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-012 source_file=src/Web/Program.cs (owner_module=CrossCutting, entry_component=Program) |  |
| `APP-SVC-006` Web | `APP-API-013` GET /api_health_check | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-013 source_file=src/Web/Program.cs (owner_module=CrossCutting, entry_component=Program) |  |
| `APP-SVC-006` Web | `APP-API-014` GET /Manage/MyAccount | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-014 source_file=src/Web/Controllers/ManageController.cs (owner_module=Identity, entry_component=ManageController) |  |
| `APP-SVC-006` Web | `APP-API-015` POST /Manage/MyAccount | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-015 source_file=src/Web/Controllers/ManageController.cs (owner_module=Identity, entry_component=ManageController) |  |
| `APP-SVC-006` Web | `APP-API-016` POST /Manage/SendVerificationEmail | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-016 source_file=src/Web/Controllers/ManageController.cs (owner_module=Identity, entry_component=ManageController) |  |
| `APP-SVC-006` Web | `APP-API-017` GET /Manage/ChangePassword | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-017 source_file=src/Web/Controllers/ManageController.cs (owner_module=Identity, entry_component=ManageController) |  |
| `APP-SVC-006` Web | `APP-API-018` POST /Manage/ChangePassword | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-018 source_file=src/Web/Controllers/ManageController.cs (owner_module=Identity, entry_component=ManageController) |  |
| `APP-SVC-006` Web | `APP-API-019` GET /Manage/SetPassword | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-019 source_file=src/Web/Controllers/ManageController.cs (owner_module=Identity, entry_component=ManageController) |  |
| `APP-SVC-006` Web | `APP-API-020` POST /Manage/SetPassword | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-020 source_file=src/Web/Controllers/ManageController.cs (owner_module=Identity, entry_component=ManageController) |  |
| `APP-SVC-006` Web | `APP-API-021` GET /Manage/ExternalLogins | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-021 source_file=src/Web/Controllers/ManageController.cs (owner_module=Identity, entry_component=ManageController) |  |
| `APP-SVC-006` Web | `APP-API-022` POST /Manage/LinkLogin | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-022 source_file=src/Web/Controllers/ManageController.cs (owner_module=Identity, entry_component=ManageController) |  |
| `APP-SVC-006` Web | `APP-API-023` GET /Manage/LinkLoginCallback | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-023 source_file=src/Web/Controllers/ManageController.cs (owner_module=Identity, entry_component=ManageController) |  |
| `APP-SVC-006` Web | `APP-API-024` POST /Manage/RemoveLogin | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-024 source_file=src/Web/Controllers/ManageController.cs (owner_module=Identity, entry_component=ManageController) |  |
| `APP-SVC-006` Web | `APP-API-025` GET /Manage/TwoFactorAuthentication | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-025 source_file=src/Web/Controllers/ManageController.cs (owner_module=Identity, entry_component=ManageController) |  |
| `APP-SVC-006` Web | `APP-API-026` GET /Manage/Disable2faWarning | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-026 source_file=src/Web/Controllers/ManageController.cs (owner_module=Identity, entry_component=ManageController) |  |
| `APP-SVC-006` Web | `APP-API-027` POST /Manage/Disable2fa | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-027 source_file=src/Web/Controllers/ManageController.cs (owner_module=Identity, entry_component=ManageController) |  |
| `APP-SVC-006` Web | `APP-API-028` GET /Manage/EnableAuthenticator | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-028 source_file=src/Web/Controllers/ManageController.cs (owner_module=Identity, entry_component=ManageController) |  |
| `APP-SVC-006` Web | `APP-API-029` GET /Manage/ShowRecoveryCodes | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-029 source_file=src/Web/Controllers/ManageController.cs (owner_module=Identity, entry_component=ManageController) |  |
| `APP-SVC-006` Web | `APP-API-030` POST /Manage/EnableAuthenticator | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-030 source_file=src/Web/Controllers/ManageController.cs (owner_module=Identity, entry_component=ManageController) |  |
| `APP-SVC-006` Web | `APP-API-031` GET /Manage/ResetAuthenticatorWarning | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-031 source_file=src/Web/Controllers/ManageController.cs (owner_module=Identity, entry_component=ManageController) |  |
| `APP-SVC-006` Web | `APP-API-032` POST /Manage/ResetAuthenticator | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-032 source_file=src/Web/Controllers/ManageController.cs (owner_module=Identity, entry_component=ManageController) |  |
| `APP-SVC-006` Web | `APP-API-033` POST /Manage/GenerateRecoveryCodes | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-033 source_file=src/Web/Controllers/ManageController.cs (owner_module=Identity, entry_component=ManageController) |  |
| `APP-SVC-006` Web | `APP-API-034` GET /Manage/GenerateRecoveryCodesWarning | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-034 source_file=src/Web/Controllers/ManageController.cs (owner_module=Identity, entry_component=ManageController) |  |
| `APP-SVC-006` Web | `APP-API-035` GET /Order/MyOrders | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-035 source_file=src/Web/Controllers/OrderController.cs (owner_module=Order, entry_component=OrderController) |  |
| `APP-SVC-006` Web | `APP-API-036` GET /Order/Detail/{orderId} | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-036 source_file=src/Web/Controllers/OrderController.cs (owner_module=Order, entry_component=OrderController) |  |
| `APP-SVC-006` Web | `APP-API-037` GET /User | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-037 source_file=src/Web/Controllers/UserController.cs (owner_module=Identity, entry_component=UserController) |  |
| `APP-SVC-006` Web | `APP-API-038` POST /User/Logout | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-038 source_file=src/Web/Controllers/UserController.cs (owner_module=Identity, entry_component=UserController) |  |
| `APP-SVC-006` Web | `APP-API-041` GET /Account/ConfirmEmail | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-041 source_file=src/Web/Areas/Identity/Pages/Account/ConfirmEmail.cshtml (owner_module=Identity, entry_component=ConfirmEmail) |  |
| `APP-SVC-006` Web | `APP-API-042` GET /Account/Login | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-042 source_file=src/Web/Areas/Identity/Pages/Account/Login.cshtml (owner_module=Identity, entry_component=Login) |  |
| `APP-SVC-006` Web | `APP-API-043` GET /Account/Logout | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-043 source_file=src/Web/Areas/Identity/Pages/Account/Logout.cshtml (owner_module=Identity, entry_component=Logout) |  |
| `APP-SVC-006` Web | `APP-API-044` GET /Account/Register | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-044 source_file=src/Web/Areas/Identity/Pages/Account/Register.cshtml (owner_module=Identity, entry_component=Register) |  |
| `APP-SVC-006` Web | `APP-API-045` GET /Error | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-045 source_file=src/Web/Pages/Error.cshtml (owner_module=Web, entry_component=Error) |  |
| `APP-SVC-006` Web | `APP-API-046` GET / | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-046 source_file=src/Web/Pages/Index.cshtml (owner_module=Web, entry_component=Index) |  |
| `APP-SVC-006` Web | `APP-API-047` GET /Privacy | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-047 source_file=src/Web/Pages/Privacy.cshtml (owner_module=Web, entry_component=Privacy) |  |
| `APP-SVC-006` Web | `APP-API-048` GET /Admin/EditCatalogItem | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-048 source_file=src/Web/Pages/Admin/EditCatalogItem.cshtml (owner_module=Catalog, entry_component=EditCatalogItem) |  |
| `APP-SVC-006` Web | `APP-API-049` GET /Admin | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-049 source_file=src/Web/Pages/Admin/Index.cshtml (owner_module=Admin, entry_component=Index) |  |
| `APP-SVC-006` Web | `APP-API-050` GET /Basket/Checkout | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-050 source_file=src/Web/Pages/Basket/Checkout.cshtml (owner_module=Basket, entry_component=Checkout) |  |
| `APP-SVC-006` Web | `APP-API-051` GET /{handler?} | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-051 source_file=src/Web/Pages/Basket/Index.cshtml (owner_module=Basket, entry_component=Index) |  |
| `APP-SVC-006` Web | `APP-API-052` GET /Basket/Success | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-052 source_file=src/Web/Pages/Basket/Success.cshtml (owner_module=Basket, entry_component=Success) |  |
| `APP-SVC-006` Web | `APP-API-055` CLI .NET application bootstrap Program.cs (Web) | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-055 source_file=src/Web/Program.cs (owner_module=CrossCutting, entry_component=Program) |  |
| `APP-SVC-016` BlazorAdmin | `APP-API-039` ROUTE /logout | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-039 source_file=src/BlazorAdmin/Pages/Logout.razor (owner_module=Identity, entry_component=Logout) |  |
| `APP-SVC-016` BlazorAdmin | `APP-API-040` ROUTE /admin | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-040 source_file=src/BlazorAdmin/Pages/CatalogItemPage/List.razor (owner_module=Catalog, entry_component=List) |  |
| `APP-SVC-016` BlazorAdmin | `APP-API-053` CLI .NET application bootstrap Program.cs (BlazorAdmin) | MEDIUM | aa-outputs/final/application-interface-catalogue.json :: INT-053 source_file=src/BlazorAdmin/Program.cs (owner_module=Admin, entry_component=Program) |  |

## 4. Evidence index (node → origin evidence)

Every node in the graph, grouped by domain/kind, mapped to the source evidence file(s) it was derived from. This makes each id traceable to its origin. Confidence/status are shown where the graph carries them.

### 4.1 Business / Capabilities (39)

| ID | Name | Conf. | Status | Source evidence file(s) |
|----|------|-------|--------|--------------------------|
| `BIZ-CAP-001` | Catalog Management | HIGH | ACTIVE | `ba_documents/01_capability_map.md`, `aa-outputs/final/business-capability-map.md` |
| `BIZ-CAP-002` | Product Information Management | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-003` | Catalog Item Details Maintenance | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-004` | Product Classification | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-005` | Product Image Management | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-006` | Catalog Reference Data | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-007` | Brand Management | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-008` | Type Management | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-009` | Catalog Seeding | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-010` | Basket / Shopping Cart Management | HIGH | ACTIVE | `ba_documents/01_capability_map.md`, `aa-outputs/final/business-capability-map.md` |
| `BIZ-CAP-011` | Basket Maintenance | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-012` | Add Item to Basket | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-013` | Quantity Adjustment | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-014` | Basket Cleanup | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-015` | Session Continuity | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-016` | Anonymous-to-Registered Basket Transfer | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-017` | Order Management | HIGH | ACTIVE | `ba_documents/01_capability_map.md`, `aa-outputs/final/business-capability-map.md` |
| `BIZ-CAP-018` | Order Creation | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-019` | Checkout Processing | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-020` | Empty Basket Protection | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-021` | Ordered Item Snapshot | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-022` | Order Calculation | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-023` | Order Total Calculation | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-024` | Buyer / Customer Profile Management | MEDIUM | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-025` | Buyer Identity | MEDIUM | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-026` | Buyer Record Creation | MEDIUM | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-027` | Payment Information | LOW | inferred | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-028` | Payment Method Management | LOW | inferred | `ba_documents/01_capability_map.md`, `aa-outputs/final/business-capability-map.md` |
| `BIZ-CAP-029` | Identity & Authentication | HIGH | ACTIVE | `ba_documents/01_capability_map.md`, `aa-outputs/final/business-capability-map.md` |
| `BIZ-CAP-030` | Access Control | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-031` | User Login | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-032` | Token Issuance | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-033` | Identity Seeding | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-034` | Identity Data Seeding | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-035` | Admin Catalog Operations (Blazor) | HIGH | ACTIVE | `ba_documents/01_capability_map.md`, `aa-outputs/final/business-capability-map.md` |
| `BIZ-CAP-036` | Administrative Catalog Interface | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-037` | Catalog Item List View | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-038` | Catalog Item Create/Delete | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |
| `BIZ-CAP-039` | Cached Data Refresh | HIGH | ACTIVE | `ba_documents/01_capability_map.md` |

### 4.2 Business / Actors (5)

| ID | Name | Conf. | Status | Source evidence file(s) |
|----|------|-------|--------|--------------------------|
| `BIZ-ACT-001` | Customer / Buyer |  |  | `ba_documents/06_stakeholder_map.md`, `ba_documents/09_operating_model.md`, `ba_documents/02_value_stream.md` |
| `BIZ-ACT-002` | Anonymous Shopper |  |  | `ba_documents/03_process_models.md`, `ba_documents/01_capability_map.md` |
| `BIZ-ACT-003` | Administrator |  |  | `ba_documents/06_stakeholder_map.md`, `ba_documents/09_operating_model.md`, `ba_documents/02_value_stream.md` |
| `BIZ-ACT-004` | System / Service Account |  |  | `ba_documents/06_stakeholder_map.md`, `ba_documents/09_operating_model.md`, `ba_documents/02_value_stream.md` |
| `BIZ-ACT-005` | Notification Recipients |  |  | `ba_documents/06_stakeholder_map.md` |

### 4.3 Business / Processes (10)

| ID | Name | Conf. | Status | Source evidence file(s) |
|----|------|-------|--------|--------------------------|
| `BIZ-PROC-001` | Browse Catalog | MEDIUM |  | `ba_documents/02_value_stream.md` |
| `BIZ-PROC-002` | Add Item to Basket | HIGH |  | `ba_documents/03_process_models.md`, `ba_documents/04_business_rules.md` |
| `BIZ-PROC-003` | Transfer Anonymous Basket to Registered User | HIGH |  | `ba_documents/03_process_models.md`, `ba_documents/02_value_stream.md` |
| `BIZ-PROC-004` | Adjust Basket | MEDIUM |  | `ba_documents/02_value_stream.md`, `ba_documents/04_business_rules.md` |
| `BIZ-PROC-005` | Checkout / Place Order | HIGH |  | `ba_documents/03_process_models.md`, `ba_documents/04_business_rules.md` |
| `BIZ-PROC-006` | Catalog Item Administration | HIGH |  | `ba_documents/03_process_models.md`, `ba_documents/02_value_stream.md`, `ba_documents/04_business_rules.md` |
| `BIZ-PROC-007` | User Authentication | HIGH |  | `ba_documents/03_process_models.md`, `ba_documents/01_capability_map.md` |
| `BIZ-PROC-008` | Buyer Record Creation | MEDIUM |  | `ba_documents/01_capability_map.md`, `ba_documents/04_business_rules.md` |
| `BIZ-PROC-009` | Catalog Seeding | MEDIUM |  | `ba_documents/01_capability_map.md`, `ba_documents/06_stakeholder_map.md` |
| `BIZ-PROC-010` | Identity Data Seeding | MEDIUM |  | `ba_documents/01_capability_map.md`, `ba_documents/06_stakeholder_map.md` |

### 4.4 Data / Entities (15)

| ID | Name | Conf. | Status | Source evidence file(s) |
|----|------|-------|--------|--------------------------|
| `DATA-ENT-001` | CatalogItem | 0.8 | implemented | `da-outputs/schema-catalogue.json`, `da-outputs/data-dictionary.md`, `da-outputs/erd.md`, `da-outputs/conceptual-data-model.md` |
| `DATA-ENT-002` | CatalogBrand | 0.8 | implemented | `da-outputs/schema-catalogue.json`, `da-outputs/data-dictionary.md`, `da-outputs/conceptual-data-model.md` |
| `DATA-ENT-003` | CatalogType | 0.8 | implemented | `da-outputs/schema-catalogue.json`, `da-outputs/data-dictionary.md`, `da-outputs/conceptual-data-model.md` |
| `DATA-ENT-004` | Basket | 0.8 | implemented | `da-outputs/schema-catalogue.json`, `da-outputs/data-dictionary.md`, `da-outputs/erd.md`, `da-outputs/conceptual-data-model.md` |
| `DATA-ENT-005` | BasketItem | 0.8 | implemented | `da-outputs/schema-catalogue.json`, `da-outputs/data-dictionary.md`, `da-outputs/conceptual-data-model.md` |
| `DATA-ENT-006` | Order | 0.8 | implemented | `da-outputs/schema-catalogue.json`, `da-outputs/data-dictionary.md`, `da-outputs/erd.md`, `da-outputs/conceptual-data-model.md` |
| `DATA-ENT-007` | OrderItem | 0.8 | implemented | `da-outputs/schema-catalogue.json`, `da-outputs/data-dictionary.md`, `da-outputs/erd.md`, `da-outputs/conceptual-data-model.md` |
| `DATA-ENT-008` | ApplicationUser | 0.7 | implemented | `da-outputs/schema-catalogue.json`, `da-outputs/data-dictionary.md`, `da-outputs/redundancy-analysis.json`, `da-outputs/conceptual-data-model.md` |
| `DATA-ENT-009` | Role | 0.7 | implemented | `da-outputs/schema-catalogue.json`, `da-outputs/data-dictionary.md`, `da-outputs/conceptual-data-model.md` |
| `DATA-ENT-010` | Buyer | 0.9 | aspirational/unimplemented | `da-outputs/schema-catalogue.json`, `da-outputs/data-dictionary.md`, `da-outputs/redundancy-analysis.json`, `da-outputs/conceptual-data-model.md`, `da-outputs/erd.md` |
| `DATA-ENT-011` | PaymentMethod | 0.9 | aspirational/unimplemented | `da-outputs/schema-catalogue.json`, `da-outputs/data-dictionary.md`, `da-outputs/conceptual-data-model.md` |
| `DATA-ENT-012` | CatalogItemOrdered | 0.78 | implemented | `da-outputs/schema-catalogue.json`, `da-outputs/erd.md`, `da-outputs/redundancy-analysis.json` |
| `DATA-ENT-013` | Address | 0.75 | implemented | `da-outputs/schema-catalogue.json`, `da-outputs/erd.md`, `da-outputs/data-dictionary.md` |
| `DATA-ENT-014` | CatalogItemDetails | 0.72 | aspirational/unimplemented | `da-outputs/schema-catalogue.json`, `da-outputs/data-dictionary.md`, `da-outputs/redundancy-analysis.json` |
| `DATA-ENT-015` | BaseEntity | 0.8 | implemented | `da-outputs/schema-catalogue.json` |

### 4.5 Data / Relationships (12)

| ID | Name | Conf. | Status | Source evidence file(s) |
|----|------|-------|--------|--------------------------|
| `DATA-REL-001` | CatalogItem -> CatalogBrand |  | implemented | `da-outputs/erd.md`, `da-outputs/conceptual-data-model.md`, `da-outputs/data-dictionary.md` |
| `DATA-REL-002` | CatalogItem -> CatalogType |  | implemented | `da-outputs/erd.md`, `da-outputs/conceptual-data-model.md`, `da-outputs/data-dictionary.md` |
| `DATA-REL-003` | Basket -> BasketItem |  | implemented | `da-outputs/erd.md`, `da-outputs/conceptual-data-model.md`, `da-outputs/data-dictionary.md` |
| `DATA-REL-004` | BasketItem -> CatalogItem |  | implemented | `da-outputs/erd.md`, `da-outputs/data-dictionary.md`, `da-outputs/ba_documents/05_data_model.md` |
| `DATA-REL-005` | Order -> OrderItem |  | implemented | `da-outputs/erd.md`, `da-outputs/conceptual-data-model.md`, `da-outputs/data-dictionary.md` |
| `DATA-REL-006` | OrderItem -> CatalogItemOrdered |  | implemented | `da-outputs/erd.md`, `da-outputs/conceptual-data-model.md`, `da-outputs/ba_documents/05_data_model.md` |
| `DATA-REL-007` | Order -> Address |  | implemented | `da-outputs/erd.md`, `da-outputs/data-dictionary.md`, `da-outputs/ba_documents/05_data_model.md` |
| `DATA-REL-008` | Basket -> ApplicationUser |  | implemented-soft-reference | `da-outputs/erd.md`, `da-outputs/data-flow-map.md`, `da-outputs/conceptual-data-model.md` |
| `DATA-REL-009` | Order -> ApplicationUser |  | implemented-soft-reference | `da-outputs/erd.md`, `da-outputs/conceptual-data-model.md`, `da-outputs/data-dictionary.md` |
| `DATA-REL-010` | ApplicationUser -> Role |  | implemented-inferred | `da-outputs/erd.md`, `da-outputs/data-dictionary.md`, `da-outputs/conceptual-data-model.md` |
| `DATA-REL-011` | Basket -> Order |  | implemented | `da-outputs/ba_documents/05_data_model.md`, `da-outputs/conceptual-data-model.md`, `da-outputs/data-flow-map.md` |
| `DATA-REL-012` | Buyer -> PaymentMethod |  | aspirational/unimplemented | `da-outputs/conceptual-data-model.md`, `da-outputs/ba_documents/05_data_model.md`, `da-outputs/schema-catalogue.json` |

### 4.6 Data / Aggregates (4)

| ID | Name | Conf. | Status | Source evidence file(s) |
|----|------|-------|--------|--------------------------|
| `DATA-AGG-001` | BasketAggregate |  | implemented | `da-outputs/schema-catalogue.json`, `da-outputs/conceptual-data-model.md` |
| `DATA-AGG-002` | OrderAggregate |  | implemented | `da-outputs/schema-catalogue.json`, `da-outputs/erd.md` |
| `DATA-AGG-003` | BuyerAggregate |  | aspirational/unimplemented | `da-outputs/conceptual-data-model.md`, `da-outputs/schema-catalogue.json`, `da-outputs/redundancy-analysis.json` |
| `DATA-AGG-004` | CatalogItem |  | implemented | `da-outputs/schema-catalogue.json`, `da-outputs/redundancy-analysis.json` |

### 4.7 Data / Repositories (4)

| ID | Name | Conf. | Status | Source evidence file(s) |
|----|------|-------|--------|--------------------------|
| `DATA-REPO-001` | IRepository<T> | 0.85 |  | `da-outputs/storage-pattern-analysis.md`, `da-outputs/data-flow-map.md` |
| `DATA-REPO-002` | IReadRepository<T> | 0.8 |  | `da-outputs/storage-pattern-analysis.md` |
| `DATA-REPO-003` | CatalogContext | 0.9 |  | `da-outputs/schema-catalogue.json`, `da-outputs/storage-pattern-analysis.md`, `da-outputs/data-flow-map.md` |
| `DATA-REPO-004` | AppIdentityDbContext | 0.7 |  | `da-outputs/schema-catalogue.json`, `da-outputs/storage-pattern-analysis.md` |

### 4.8 Application / Services (47)

| ID | Name | Conf. | Status | Source evidence file(s) |
|----|------|-------|--------|--------------------------|
| `APP-SVC-001` | Catalog | MEDIUM |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md`, `aa-outputs/final/application-architecture-summary.md`, `aa-outputs/final/service-boundary-options.md`, `aa-outputs/final/data-ownership-map.md` |
| `APP-SVC-002` | Identity | MEDIUM |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md`, `aa-outputs/final/application-architecture-summary.md`, `aa-outputs/final/service-boundary-options.md` |
| `APP-SVC-003` | Basket | MEDIUM |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md`, `aa-outputs/final/service-boundary-options.md`, `aa-outputs/final/data-ownership-map.md` |
| `APP-SVC-004` | Order | MEDIUM |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md`, `aa-outputs/final/service-boundary-options.md`, `aa-outputs/final/data-ownership-map.md`, `aa-outputs/final/application-interface-catalogue.json` |
| `APP-SVC-005` | Admin | MEDIUM |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md`, `aa-outputs/final/service-boundary-options.md` |
| `APP-SVC-006` | Web | HIGH |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md`, `aa-outputs/final/application-architecture-summary.md`, `aa-outputs/final/system-inventory.json`, `ta-outputs/ta_agent1/component-service-map.md` |
| `APP-SVC-007` | ApplicationCore | HIGH |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md`, `aa-outputs/final/system-inventory.json`, `ta-outputs/ta_agent1/component-service-map.md` |
| `APP-SVC-008` | DataAccess | MEDIUM |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md`, `aa-outputs/final/service-boundary-options.md` |
| `APP-SVC-009` | Infrastructure | HIGH |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md`, `aa-outputs/final/system-inventory.json`, `ta-outputs/ta_agent1/component-service-map.md` |
| `APP-SVC-010` | CrossCutting | MEDIUM |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-SVC-011` | PublicApi | HIGH |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md`, `aa-outputs/final/system-inventory.json`, `ta-outputs/ta_agent1/component-service-map.md` |
| `APP-SVC-012` | SharedContracts | HIGH |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md`, `ta-outputs/ta_agent1/component-service-map.md`, `aa-outputs/final/system-inventory.json` |
| `APP-SVC-013` | Verification | LOW |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md`, `aa-outputs/final/application-architecture-summary.md` |
| `APP-SVC-016` | BlazorAdmin | HIGH |  | `aa-outputs/final/system-inventory.json`, `ta-outputs/ta_agent1/component-service-map.md` |
| `APP-SVC-020` | UriComposer | HIGH |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md`, `aa-outputs/final/application-architecture-summary.md` |
| `APP-SVC-021` | IdentityTokenClaimService | HIGH |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-SVC-022` | EfRepository | HIGH |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md`, `aa-outputs/final/data-ownership-map.md` |
| `APP-SVC-023` | CatalogContext | HIGH |  | `aa-outputs/final/data-ownership-map.md`, `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-SVC-024` | AppIdentityDbContext | HIGH |  | `aa-outputs/final/data-ownership-map.md` |
| `APP-SVC-025` | CatalogContextSeed | HIGH |  | `aa-outputs/final/system-inventory.json`, `aa-outputs/final/data-ownership-map.md` |
| `APP-SVC-026` | AppIdentityDbContextSeed | HIGH |  | `aa-outputs/final/system-inventory.json`, `aa-outputs/final/data-ownership-map.md` |
| `APP-SVC-027` | BasketGuards | MEDIUM |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-SVC-028` | JsonExtensions | MEDIUM |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-SVC-029` | AuthenticateEndpoint | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-SVC-030` | CatalogBrandListEndpoint | HIGH |  | `aa-outputs/final/application-interface-catalogue.json`, `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-SVC-031` | CatalogItemGetByIdEndpoint | HIGH |  | `aa-outputs/final/application-interface-catalogue.json`, `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-SVC-032` | CatalogItemListPagedEndpoint | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-SVC-033` | CreateCatalogItemEndpoint | HIGH |  | `aa-outputs/final/application-interface-catalogue.json`, `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-SVC-034` | DeleteCatalogItemEndpoint | HIGH |  | `aa-outputs/final/application-interface-catalogue.json`, `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-SVC-035` | UpdateCatalogItemEndpoint | HIGH |  | `aa-outputs/final/application-interface-catalogue.json`, `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-SVC-036` | CatalogTypeListEndpoint | HIGH |  | `aa-outputs/final/application-interface-catalogue.json`, `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-SVC-037` | ManageController | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-SVC-038` | OrderController | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-SVC-039` | UserController | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-SVC-040` | IndexModel | MEDIUM |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-SVC-041` | GetMyOrders | MEDIUM |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-SVC-042` | GetMyOrdersHandler | MEDIUM |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-SVC-043` | GetOrderDetails | MEDIUM |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-SVC-044` | CachedCatalogItemServiceDecorator | MEDIUM |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-SVC-045` | CachedCatalogLookupDataServiceDecorator | MEDIUM |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-SVC-046` | BlazorComponent | MEDIUM |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-SVC-047` | BlazorLayoutComponent | MEDIUM |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-SVC-048` | ToastComponent | MEDIUM |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-SVC-049` | RefreshBroadcast | MEDIUM |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-SVC-050` | List | HIGH |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md`, `aa-outputs/final/application-interface-catalogue.json` |
| `APP-SVC-051` | CustomAuthStateProvider | MEDIUM |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-SVC-052` | Program | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |

### 4.9 Application / Interfaces (13)

| ID | Name | Conf. | Status | Source evidence file(s) |
|----|------|-------|--------|--------------------------|
| `APP-IF-001` | IRepository<T> |  |  | `aa-outputs/final/data-ownership-map.md`, `aa-outputs/final/application-interface-catalogue.json` |
| `APP-IF-002` | IReadRepository<T> |  |  | `aa-outputs/final/data-ownership-map.md`, `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-IF-003` | ITokenClaimsService |  |  | `aa-outputs/final/application-interface-catalogue.json`, `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-IF-004` | IUriComposer |  |  | `aa-outputs/final/application-interface-catalogue.json`, `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-IF-005` | IAppLogger<T> |  |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md`, `aa-outputs/final/application-interface-catalogue.json` |
| `APP-IF-006` | IBasketService |  |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-IF-007` | IBasketQueryService |  |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-IF-008` | IEmailSender |  |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md`, `aa-outputs/final/application-interface-catalogue.json` |
| `APP-IF-009` | IAggregateRoot |  |  | `aa-outputs/final/data-ownership-map.md` |
| `APP-IF-010` | ICatalogItemService |  |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-IF-011` | ICatalogLookupDataService |  |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-IF-012` | IMediator |  |  | `aa-outputs/final/application-interface-catalogue.json`, `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-IF-013` | CustomAuthStateProvider |  |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |

### 4.10 Application / APIs (55)

| ID | Name | Conf. | Status | Source evidence file(s) |
|----|------|-------|--------|--------------------------|
| `APP-API-001` | POST /api/authenticate | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-002` | GET /api/catalog-brands | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-003` | GET /api/catalog-items/{catalogItemId} | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-004` | GET /api/catalog-items | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-005` | POST /api/catalog-items | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-006` | DELETE /api/catalog-items/{catalogItemId} | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-007` | PUT /api/catalog-items | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-008` | GET /api/catalog-types | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-009` | ROUTE /{controller:slugify=Home}/{action:slugify=Index}/{id?} | LOW |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-010` | ROUTE ASP.NET Razor Pages route registration | LOW |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-011` | ROUTE /index.html | LOW |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-012` | GET /home_page_health_check | LOW |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-013` | GET /api_health_check | LOW |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-014` | GET /Manage/MyAccount | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-015` | POST /Manage/MyAccount | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-016` | POST /Manage/SendVerificationEmail | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-017` | GET /Manage/ChangePassword | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-018` | POST /Manage/ChangePassword | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-019` | GET /Manage/SetPassword | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-020` | POST /Manage/SetPassword | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-021` | GET /Manage/ExternalLogins | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-022` | POST /Manage/LinkLogin | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-023` | GET /Manage/LinkLoginCallback | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-024` | POST /Manage/RemoveLogin | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-025` | GET /Manage/TwoFactorAuthentication | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-026` | GET /Manage/Disable2faWarning | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-027` | POST /Manage/Disable2fa | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-028` | GET /Manage/EnableAuthenticator | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-029` | GET /Manage/ShowRecoveryCodes | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-030` | POST /Manage/EnableAuthenticator | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-031` | GET /Manage/ResetAuthenticatorWarning | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-032` | POST /Manage/ResetAuthenticator | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-033` | POST /Manage/GenerateRecoveryCodes | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-034` | GET /Manage/GenerateRecoveryCodesWarning | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-035` | GET /Order/MyOrders | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-036` | GET /Order/Detail/{orderId} | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-037` | GET /User | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-038` | POST /User/Logout | HIGH |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-039` | ROUTE /logout | MEDIUM |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-040` | ROUTE /admin | MEDIUM |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-041` | GET /Account/ConfirmEmail | LOW |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-042` | GET /Account/Login | LOW |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-043` | GET /Account/Logout | LOW |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-044` | GET /Account/Register | LOW |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-045` | GET /Error | LOW |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-046` | GET / | LOW |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-047` | GET /Privacy | LOW |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-048` | GET /Admin/EditCatalogItem | LOW |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-049` | GET /Admin | LOW |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-050` | GET /Basket/Checkout | LOW |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-051` | GET /{handler?} | MEDIUM |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-052` | GET /Basket/Success | LOW |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-053` | CLI .NET application bootstrap Program.cs (BlazorAdmin) | MEDIUM |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-054` | CLI .NET application bootstrap Program.cs (PublicApi) | MEDIUM |  | `aa-outputs/final/application-interface-catalogue.json` |
| `APP-API-055` | CLI .NET application bootstrap Program.cs (Web) | MEDIUM |  | `aa-outputs/final/application-interface-catalogue.json` |

### 4.11 Application / Dependencies (19)

| ID | Name | Conf. | Status | Source evidence file(s) |
|----|------|-------|--------|--------------------------|
| `APP-DEP-001` | Admin -> ApplicationCore -> Basket -> Catalog -> DataAccess -> Identity -> Order -> Web -> (cycle back to Admin) |  |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md`, `aa-outputs/final/application-architecture-summary.md` |
| `APP-DEP-002` | CatalogBrandListEndpoint -> EfRepository |  |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-DEP-003` | CatalogItemGetByIdEndpoint -> EfRepository |  |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-DEP-004` | CreateCatalogItemEndpoint -> EfRepository |  |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-DEP-005` | DeleteCatalogItemEndpoint -> EfRepository |  |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-DEP-006` | UpdateCatalogItemEndpoint -> EfRepository |  |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-DEP-007` | CatalogTypeListEndpoint -> EfRepository |  |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-DEP-008` | IndexModel -> EfRepository |  |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-DEP-009` | EfRepository -> (many consumers) |  |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md`, `aa-outputs/final/application-architecture-summary.md` |
| `APP-DEP-010` | UriComposer -> (catalog endpoints) |  |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| `APP-DEP-011` | Web -> PublicApi |  |  | `ta-outputs/ta_agent1/integration-dependency-graph.md` |
| `APP-DEP-012` | PublicApi -> ApplicationCore, Infrastructure |  |  | `aa-outputs/final/system-inventory.json` |
| `APP-DEP-013` | Web -> ApplicationCore, BlazorAdmin, BlazorShared, Infrastructure |  |  | `aa-outputs/final/system-inventory.json` |
| `APP-DEP-014` | Infrastructure -> ApplicationCore |  |  | `aa-outputs/final/system-inventory.json` |
| `APP-DEP-015` | ApplicationCore -> BlazorShared |  |  | `aa-outputs/final/system-inventory.json` |
| `APP-DEP-016` | BlazorAdmin -> BlazorShared |  |  | `aa-outputs/final/system-inventory.json` |
| `APP-DEP-017` | BlazorAdmin -> PublicApi |  |  | `ta-outputs/ta_agent1/integration-dependency-graph.md` |
| `APP-DEP-018` | BlazorAdmin -> Web |  |  | `ta-outputs/ta_agent1/integration-dependency-graph.md` |
| `APP-DEP-019` | Web, PublicApi -> sqlserver |  |  | `ta-outputs/ta_agent1/integration-dependency-graph.md` |

### 4.12 Technology / Current Stack (26)

| ID | Name | Conf. | Status | Source evidence file(s) |
|----|------|-------|--------|--------------------------|
| `TECH-CUR-001` | .NET SDK / Runtime | HIGH |  | `.github/workflows/dotnetcore.yml - dotnet build/test on 8.0.x`, `ta-outputs/technology-stack-assessment.md: 'Active - core path; Target framework for all 6 src projects and 4 test projects ... Supported - LTS until 2026-11-10'` |
| `TECH-CUR-002` | ASP.NET Core (Microsoft.NET.Sdk.Web) | HIGH |  | `src/Web/Web.csproj, src/PublicApi/PublicApi.csproj - Microsoft.NET.Sdk.Web`, `ta-outputs/technology-stack-assessment.md: 'Active - core path; Web app SDK for Web.csproj and PublicApi.csproj'` |
| `TECH-CUR-003` | Blazor WebAssembly (Microsoft.NET.Sdk.BlazorWebAssembly + Microsoft.AspNetCore.Components.WebAssembly) | HIGH |  | `src/BlazorAdmin/BlazorAdmin.csproj - Microsoft.NET.Sdk.BlazorWebAssembly, Microsoft.AspNetCore.Components.WebAssembly`, `ta-outputs/technology-stack-assessment.md: 'Active - core path; WASM admin UI, hosted by Web via Microsoft.AspNetCore.Components.WebAssembly.Server'` |
| `TECH-CUR-004` | Microsoft.AspNetCore.Components.WebAssembly.Server | LOW |  | `src/Web/Web.csproj`, `ta-outputs/technology-stack-assessment.md: 'Active - core path; hosts the BlazorAdmin WASM app inside the Web project'` |
| `TECH-CUR-005` | Entity Framework Core (ORM) | LOW |  | `src/Infrastructure/Infrastructure.csproj, src/Web/Web.csproj, src/PublicApi/PublicApi.csproj - EF Core providers + Microsoft.EntityFrameworkCore.Tools`, `ta-outputs/ta_agent1/data-store-registry.md - EF Core providers back Catalog and Identity stores` |
| `TECH-CUR-006` | Microsoft.EntityFrameworkCore.SqlServer | LOW |  | `src/Web/Web.csproj, src/PublicApi/PublicApi.csproj (SHARED COMPONENT)`, `ta-outputs/technology-stack-assessment.md: 'Active - Docker environment only; appsettings.Docker.json declares SQL Server connection strings against the sqlserver compose service'` |
| `TECH-CUR-007` | Npgsql.EntityFrameworkCore.PostgreSQL | LOW |  | `src/Infrastructure/Infrastructure.csproj`, `ta-outputs/technology-stack-assessment.md: 'Active - default environment; src/Web/appsettings.json and src/PublicApi/appsettings.json (the default, non-environment-suffixed config) declare CatalogConnection/IdentityConnection as PostgreSQL'` |
| `TECH-CUR-008` | Microsoft.EntityFrameworkCore.InMemory | LOW |  | `src/Infrastructure/Infrastructure.csproj, src/PublicApi/PublicApi.csproj, src/Web/Web.csproj + 4 test projects (SHARED COMPONENT)`, `ta-outputs/technology-stack-assessment.md: 'Active in production projects, not just tests ... suggests an UseOnlyInMemoryDatabase-style runtime switch (TD-16)'`, `tests/PublicApiIntegrationTests/appsettings.test.json - UseOnlyInMemoryDatabase: true` |
| `TECH-CUR-009` | Ardalis.Specification (+ EntityFrameworkCore evaluator) | LOW |  | `src/ApplicationCore/ApplicationCore.csproj, src/Web/Web.csproj; Ardalis.Specification.EntityFrameworkCore in src/Infrastructure/Infrastructure.csproj`, `ta-outputs/technology-stack-assessment.md: 'Active - secondary; consistent 3-layer reference pattern is strong indirect evidence of an active specification-pattern data-access layer'` |
| `TECH-CUR-010` | Ardalis Guard/Result/ApiEndpoints libraries | LOW |  | `Ardalis.GuardClauses, Ardalis.Result - src/ApplicationCore/ApplicationCore.csproj (Declared-only)`, `Ardalis.ApiEndpoints - src/PublicApi/PublicApi.csproj (Active - core path, REST endpoint-per-class pattern AP-05)`, `Ardalis.ListStartupServices - src/Web/Web.csproj (Declared-only, DI diagnostics)` |
| `TECH-CUR-011` | MediatR | LOW |  | `src/Web/Web.csproj only`, `ta-outputs/technology-stack-assessment.md: 'Declared-only - CQRS/mediator pattern signal ... scoped to the Web project (AP-01)'` |
| `TECH-CUR-012` | AutoMapper.Extensions.Microsoft.DependencyInjection | LOW |  | `src/PublicApi/PublicApi.csproj, src/Web/Web.csproj (SHARED COMPONENT)`, `ta-outputs/technology-stack-assessment.md: 'Active - secondary; DTO <-> domain mapping'` |
| `TECH-CUR-013` | MinimalApi.Endpoint | LOW |  | `src/PublicApi/PublicApi.csproj`, `ta-outputs/technology-stack-assessment.md: 'Active - secondary; minimal-API endpoint pattern, complements Ardalis.ApiEndpoints'` |
| `TECH-CUR-014` | Swashbuckle.AspNetCore (+ SwaggerUI, + Annotations) | LOW |  | `src/PublicApi/PublicApi.csproj`, `ta-outputs/technology-stack-assessment.md: 'Active - core path; OpenAPI/Swagger documentation and UI for PublicApi'` |
| `TECH-CUR-015` | FluentValidation | LOW |  | `src/BlazorShared/BlazorShared.csproj`, `ta-outputs/technology-stack-assessment.md: 'Declared-only; shared validation rules ... no validator class evidence provided'` |
| `TECH-CUR-016` | System.Text.Json / System.Net.Http.Json | LOW |  | `System.Text.Json - src/ApplicationCore/ApplicationCore.csproj (Declared-only)`, `System.Net.Http.Json - src/BlazorAdmin/BlazorAdmin.csproj (Active - secondary; typed JSON HTTP client extensions consistent with BlazorAdmin calling apiBase/webBase REST endpoints)` |
| `TECH-CUR-017` | Blazor client libraries (Blazored.LocalStorage, BlazorInputFile, Microsoft.Extensions.Identity.Core) | LOW |  | `src/BlazorAdmin/BlazorAdmin.csproj, src/BlazorShared/BlazorShared.csproj`, `ta-outputs/technology-stack-assessment.md: BlazorInputFile 'Declared-only ... possible legacy dependency superseded by framework-native InputFile since .NET 5'` |
| `TECH-CUR-018` | Microsoft.Extensions.Logging.Configuration | LOW |  | `src/BlazorAdmin/BlazorAdmin.csproj`, `ta-outputs/technology-stack-assessment.md: 'Active - secondary; binds Logging section of wwwroot/appsettings*.json'` |
| `TECH-CUR-019` | Microsoft.AspNetCore.Diagnostics.EntityFrameworkCore | LOW |  | `src/Web/Web.csproj, src/PublicApi/PublicApi.csproj (SHARED COMPONENT)`, `ta-outputs/technology-stack-assessment.md: 'Active - secondary; EF Core developer exception pages'` |
| `TECH-CUR-020` | Azure SQL Edge (sqlserver container) | LOW |  | `docker-compose.yml - mcr.microsoft.com/azure-sql-edge (no tag), backs eshopwebmvc and eshoppublicapi in Docker env; DB names Microsoft.eShopOnWeb.CatalogDb, Microsoft.eShopOnWeb.Identity`, `ta-outputs/technology-stack-assessment.md: 'EOL - Microsoft retired Azure SQL Edge (end of support 2025-09-30); no tag pin means image resolution will fail or silently fall back ... DISCREPANCY - elevated from tagging hygiene to EOL/availability risk'` |
| `TECH-CUR-021` | PostgreSQL (eShopCatalog, eShopIdentity) | LOW |  | `src/Web/appsettings.json, src/PublicApi/appsettings.json (default config) - CatalogConnection/IdentityConnection PostgreSQL connection strings (Host=localhost;Port=5432)`, `ta-outputs/ta_agent1/data-store-registry.md: 'VERSION UNKNOWN; no IaC declaration found, host=localhost:5432 implies external/local dev instance'` |
| `TECH-CUR-022` | EF Core InMemory Database (data store) | LOW |  | `ta-outputs/ta_agent1/data-store-registry.md - EF Core InMemory store; UseOnlyInMemoryDatabase: true (tests/PublicApiIntegrationTests/appsettings.test.json)`, `Provider: Microsoft.EntityFrameworkCore.InMemory (TECH-CUR-008)` |
| `TECH-CUR-023` | Docker base images (mcr.microsoft.com/dotnet/sdk:8.0, mcr.microsoft.com/dotnet/aspnet:8.0) | HIGH |  | `src/Web/Dockerfile, src/PublicApi/Dockerfile - sdk:8.0 (build stage), aspnet:8.0 (runtime stage)`, `ta-outputs/technology-stack-assessment.md: 'Active - core path ... Supported (tracks .NET 8 LTS)'` |
| `TECH-CUR-024` | Build & dev tooling (EF Core Tools, CodeGeneration.Design, Containers.Tools.Targets, BuildBundlerMinifier, LibraryManager, WebAssembly.DevServer) | LOW |  | `Microsoft.EntityFrameworkCore.Tools, Microsoft.VisualStudio.Web.CodeGeneration.Design - src/Web/Web.csproj, src/PublicApi/PublicApi.csproj`, `Microsoft.VisualStudio.Azure.Containers.Tools.Targets - src/PublicApi/PublicApi.csproj`, `BuildBundlerMinifier (Release-only), Microsoft.Web.LibraryManager.Build - src/Web/Web.csproj`, `Microsoft.AspNetCore.Components.WebAssembly.DevServer - src/BlazorAdmin/BlazorAdmin.csproj` |
| `TECH-CUR-025` | Test tooling (xUnit, MSTest, NSubstitute, coverlet, Microsoft.NET.Test.Sdk, Mvc.Testing) | LOW |  | `xunit, xunit.runner.visualstudio, xunit.runner.console - tests/FunctionalTests, IntegrationTests, UnitTests`, `MSTest.TestAdapter/TestFramework, coverlet.collector - tests/PublicApiIntegrationTests (only project using MSTest)`, `NSubstitute(+Analyzers) - IntegrationTests, UnitTests; Microsoft.AspNetCore.Mvc.Testing, Microsoft.NET.Test.Sdk - multiple test projects`, `dotnet-xunit 2.3.1 (DotNetCliToolReference) - tests/FunctionalTests; ta-outputs/technology-stack-assessment.md: 'legacy DotNetCliToolReference, superseded'` |
| `TECH-CUR-026` | GitHub Actions (actions/checkout@v2, actions/setup-dotnet@v1, microsoft/RichCodeNavIndexer@v0.1) | HIGH |  | `.github/workflows/dotnetcore.yml, .github/workflows/richnav.yml`, `ta-outputs/ta_agent1/infrastructure-deployment-blueprint.md - CI/CD Pipeline Inventory` |

### 4.13 Technology / Infrastructure (8)

| ID | Name | Conf. | Status | Source evidence file(s) |
|----|------|-------|--------|--------------------------|
| `TECH-INF-001` | eshopwebmvc container |  |  | `ta-outputs/ta_agent1/infrastructure-deployment-blueprint.md - 'eshopwebmvc \| Container (Docker Compose service) \| ports 5106:8080'`, `docker-compose.yml, docker-compose.override.yml, src/Web/Dockerfile`, `ta-outputs/nfr-registry.md NFR-01/NFR-02/NFR-28` |
| `TECH-INF-002` | eshoppublicapi container |  |  | `ta-outputs/ta_agent1/infrastructure-deployment-blueprint.md - 'eshoppublicapi \| Container \| ports 5200:8080; Dockerfile EXPOSE 80, EXPOSE 443'`, `docker-compose.yml, docker-compose.override.yml, src/PublicApi/Dockerfile`, `ta-outputs/nfr-registry.md NFR-03/NFR-04/NFR-05` |
| `TECH-INF-003` | sqlserver container (Azure SQL Edge) |  |  | `ta-outputs/ta_agent1/infrastructure-deployment-blueprint.md - 'sqlserver \| Container \| mcr.microsoft.com/azure-sql-edge (no tag); ports 1433:1433'`, `ta-outputs/ta_agent1/data-store-registry.md, ta-outputs/technology-stack-assessment.md (EOL)`, `ta-outputs/operational-architecture-assessment.md - 'sqlserver service declares no named volume ... data is lost on docker-compose down'` |
| `TECH-INF-004` | docker-compose orchestration (local/Docker environment) |  |  | `ta-outputs/ta_agent1/infrastructure-deployment-blueprint.md - Network Topology section; 'No ingress controller, load balancer, reverse proxy, or API gateway configuration found'`, `ta-outputs/nfr-registry.md NFR-27 (no resource limits), NFR-28 (depends_on order only)` |
| `TECH-INF-005` | GitHub Actions CI/CD pipelines |  |  | `ta-outputs/ta_agent1/infrastructure-deployment-blueprint.md - CI/CD Pipeline Inventory`, `ta-outputs/operational-architecture-assessment.md - CI/CD Pipeline Maturity table (Automated Deploy = Absent; SAST/Dependency/Container/Secret scan = Absent)` |
| `TECH-INF-006` | Dependabot (NuGet) |  |  | `.github/dependabot.yml`, `ta-outputs/ta_agent1/infrastructure-deployment-blueprint.md - 'automated dependency-update bot, not a build pipeline'`, `ta-outputs/nfr-registry.md NFR-20` |
| `TECH-INF-007` | Azure deployment environment (azd / parameters-only) |  |  | `ta-outputs/ta_agent1/infrastructure-deployment-blueprint.md - 'parameters file present but no resource-defining Bicep/ARM template (main.bicep) provided'; abbreviations 'none of these resource types have corresponding resource declarations'`, `ta-outputs/security-architecture-assessment.md - 'this whole surface is UNKNOWN, not merely low risk'` |
| `TECH-INF-008` | Azure Key Vault (referenced) |  |  | `ta-outputs/ta_agent1/infrastructure-deployment-blueprint.md / ta-outputs/ta_agent1/integration-dependency-graph.md - 'referenced via env var / package reference only; no Key Vault resource declaration found'`, `src/Web/Web.csproj, infra/main.parameters.json` |

### 4.14 Technology / Security (17)

| ID | Name | Conf. | Status | Source evidence file(s) |
|----|------|-------|--------|--------------------------|
| `TECH-SEC-001` | ASP.NET Core Identity (cookie-based auth + user store) |  |  | `ta-outputs/ta_agent1/security-configuration-snapshot.md - 'ASP.NET Core Identity \| HIGH \| ConnectionStrings:IdentityConnection'`, `ta-outputs/security-architecture-assessment.md - 'EF Core Identity store ... Partial; cannot confirm cookie is SecurePolicy=Always for the Docker environment which serves over plain HTTP'` |
| `TECH-SEC-002` | JWT Bearer Authentication |  |  | `ta-outputs/ta_agent1/security-configuration-snapshot.md - 'JWT Bearer Tokens \| LOW - inferred from package references; no explicit JWT configuration block found'`, `ta-outputs/security-architecture-assessment.md - 'Unresolved ... High - an API described as public with no confirmed authentication enforcement is a high-severity unknown until resolved' (AP-10, TD-12)` |
| `TECH-SEC-003` | Blazor WebAssembly Authentication (BlazorAdmin) |  |  | `ta-outputs/ta_agent1/security-configuration-snapshot.md - 'Blazor WebAssembly Authentication \| LOW - inferred from package references; no explicit auth provider/authority configuration found'`, `ta-outputs/security-architecture-assessment.md - 'Unresolved ... High - admin-facing UI with unconfirmed auth wiring to its backing API'` |
| `TECH-SEC-004` | Authorization Components (role/claims-based) |  |  | `ta-outputs/ta_agent1/security-configuration-snapshot.md - 'Authorization Components \| Microsoft.AspNetCore.Components.Authorization \| LOW - package reference only'`, `ta-outputs/security-architecture-assessment.md - 'no role/policy definitions visible ... Cannot confirm role-to-page mapping for BlazorAdmin'`, `ta-outputs/ta_agent1/technology-stack-inventory.md - System.Security.Claims in src/ApplicationCore/ApplicationCore.csproj` |
| `TECH-SEC-005` | .NET User Secrets (local dev) |  |  | `ta-outputs/ta_agent1/security-configuration-snapshot.md - '.NET User Secrets \| HIGH \| UserSecretsId ...'`, `ta-outputs/security-architecture-assessment.md - 'Correctly used ... but does not mitigate the two Critical findings above'` |
| `TECH-SEC-006` | Azure Key Vault secrets integration (referenced) |  |  | `ta-outputs/ta_agent1/security-configuration-snapshot.md - 'Azure Key Vault (referenced) \| LOW - referenced via package + deployment parameter only; no Key Vault resource declaration or vault name found'`, `ta-outputs/security-architecture-assessment.md - 'Medium ... no Key Vault resource declaration ... no vault name/URI appears in any application appsettings*.json' (TD-13)` |
| `TECH-SEC-007` | Docker-mounted host secrets (read-only bind mounts) |  |  | `ta-outputs/ta_agent1/security-configuration-snapshot.md - 'Docker-mounted host secrets \| Volume mount (read-only) \| HIGH'`, `ta-outputs/security-architecture-assessment.md - 'Informational (good practice for local dev; not a production secret-delivery mechanism)'` |
| `TECH-SEC-008` | Hardcoded PostgreSQL credentials in source-controlled config |  |  | `ta-outputs/security-architecture-assessment.md - 'Hardcoded plaintext credentials committed to source control: Username=postgres;Password=Clarium123 ... Critical' (src/Web/appsettings.json, src/PublicApi/appsettings.json, TD-01)`, `ta-outputs/ta_agent1/security-configuration-snapshot.md - 'SECRETS MANAGEMENT PATTERN DETECTED: database credentials ... committed in plaintext'` |
| `TECH-SEC-009` | Hardcoded SQL Server / Azure SQL Edge SA password in source-controlled config |  |  | `ta-outputs/security-architecture-assessment.md - 'Hardcoded plaintext password committed to source control: SA_PASSWORD=@someThingComplicated1234 ... Critical' (docker-compose.yml; appsettings.Docker.json, TD-02)` |
| `TECH-SEC-010` | No JWT/authentication enforcement configured for PublicApi |  |  | `ta-outputs/security-architecture-assessment.md - 'HIGH - No confirmed JWT/authentication enforcement configuration for PublicApi despite it being the system public-facing API (AP-10, TD-12)'` |
| `TECH-SEC-011` | No CORS policy found despite required cross-origin calls |  |  | `ta-outputs/ta_agent1/security-configuration-snapshot.md - 'CORS policy \| Not declared in any provided config file \| LOW - VALUE NOT FOUND'`, `ta-outputs/security-architecture-assessment.md - 'HIGH - No CORS policy found despite cross-origin calls from BlazorAdmin to PublicApi/Web ... in every environment (TD-17)'` |
| `TECH-SEC-012` | No secret scanning in CI/CD |  |  | `ta-outputs/security-architecture-assessment.md - 'HIGH - No secret scanning in CI/CD; the two Critical hardcoded-credential findings ... would pass the current pipeline undetected (TD-06)'`, `ta-outputs/operational-architecture-assessment.md - 'Secret / Credential Scan \| Absent ... directly correlates with TD-01/TD-02'` |
| `TECH-SEC-013` | SQL Server port 1433 published directly to host network |  |  | `ta-outputs/security-architecture-assessment.md - 'MEDIUM - SQL Server port 1433 published directly to the host network (TD-18)'; attack-surface table 'Direct host exposure of the database port'` |
| `TECH-SEC-014` | No TLS termination for Docker/container traffic |  |  | `ta-outputs/ta_agent1/infrastructure-deployment-blueprint.md - 'Docker environment endpoints are declared as plain http:// ... no TLS termination point declared for Docker/container traffic'`, `ta-outputs/ta_agent1/security-configuration-snapshot.md - 'TLS (Docker) \| ASPNETCORE_URLS=http://+:8080 - plain HTTP, no TLS termination declared'` |
| `TECH-SEC-015` | AllowedHosts wildcard + TrustServerCertificate=true |  |  | `ta-outputs/ta_agent1/security-configuration-snapshot.md - 'AllowedHosts \| Host Filtering \| "*" \| HIGH'; 'TrustServerCertificate \| TrustServerCertificate=true \| HIGH'`, `ta-outputs/nfr-registry.md NFR-14 - 'wildcard AllowedHosts is a permissive default; combined with no CORS policy found (TD-17), this widens the host-header attack surface'` |
| `TECH-SEC-016` | No SAST / dependency / container vulnerability scanning in CI/CD |  |  | `ta-outputs/operational-architecture-assessment.md - 'SAST \| Absent \| High'; 'Dependency Scan \| Absent \| High'; 'Container / Image Scan \| Absent \| High'`, `ta-outputs/security-architecture-assessment.md - 'No SAST, no dependency vulnerability scan beyond Dependabot ... no container image scanning ... no secret scanning'` |
| `TECH-SEC-017` | No audit logging / compliance controls (RBAC, GDPR, PCI, retention) found |  |  | `ta-outputs/ta_agent1/security-configuration-snapshot.md - 'LAYER NOT FOUND \| Audit Logging / Data Retention / GDPR / PCI / HIPAA / SOC2 / RBAC \| No audit logging configuration keys ... found'` |

_Total nodes indexed: **274** across all four domains._

## 5. Coverage & gaps

Computed strictly from the presence/absence of `cross_links` in the graph. A `—` in §2 or an absence here means *no evidenced link exists in the source graph*, not that the relationship is impossible. These are the verified inputs for forward-engineering decisions.

### 5.1 Coverage summary

| Hop | Linked | Total source nodes | Coverage |
|-----|--------|--------------------|----------|
| Capability → Process | 17 capabilities | 39 | 17/39 (44%) |
| Process → Entity | 10 processes | 10 | 10/10 (100%) |
| Entity → Service | 15 entities | 15 | 15/15 (100%) |
| Service → API (hosts) | 3 services host APIs | 47 | 3/47 (6%) |
| API → Service (reverse) | 55 APIs mapped | 55 | 55/55 (100%) |

### 5.2 Capabilities with no linked process

22 of 39 capabilities have **no** `capability_to_process` link. Most are L2/L3 sub-capabilities whose value-stream stages are not broken down to step-level processes in the business evidence (see ASSUMP-005). The 10 processes in the graph cover only the Catalog-browse, Basket, and Order/Checkout value-stream stages plus login/seeding.

| Capability | Linked process? |
|------------|-----------------|
| `BIZ-CAP-001` Catalog Management | — |
| `BIZ-CAP-003` Catalog Item Details Maintenance | — |
| `BIZ-CAP-004` Product Classification | — |
| `BIZ-CAP-005` Product Image Management | — |
| `BIZ-CAP-006` Catalog Reference Data | — |
| `BIZ-CAP-007` Brand Management | — |
| `BIZ-CAP-008` Type Management | — |
| `BIZ-CAP-010` Basket / Shopping Cart Management | — |
| `BIZ-CAP-011` Basket Maintenance | — |
| `BIZ-CAP-015` Session Continuity | — |
| `BIZ-CAP-017` Order Management | — |
| `BIZ-CAP-018` Order Creation | — |
| `BIZ-CAP-022` Order Calculation | — |
| `BIZ-CAP-024` Buyer / Customer Profile Management | — |
| `BIZ-CAP-025` Buyer Identity | — |
| `BIZ-CAP-027` Payment Information | — |
| `BIZ-CAP-028` Payment Method Management | — |
| `BIZ-CAP-029` Identity & Authentication | — |
| `BIZ-CAP-030` Access Control | — |
| `BIZ-CAP-033` Identity Seeding | — |
| `BIZ-CAP-035` Admin Catalog Operations (Blazor) | — |
| `BIZ-CAP-036` Administrative Catalog Interface | — |

### 5.3 Processes with no linked entity

**None.** All 10 processes carry at least one `process_to_entity` link.

### 5.4 Entities with no owning service

**None.** All 15 entities carry an `entity_to_service` ownership link (per the data-ownership map).

### 5.5 APIs with no mapped service

**None.** All 55 APIs are mapped to a deployable host service via `service_to_api`.

### 5.6 Structural gap: entity-owning service → API

The single systemic gap in the end-to-end chain (footnote [^svcapi]): APIs are linked to **deployable hosts** (`APP-SVC-006 Web`, `APP-SVC-011 PublicApi`, `APP-SVC-016 BlazorAdmin`), while entities are owned by **domain modules** (`APP-SVC-001 Catalog`, `-002 Identity`, `-003 Basket`, `-004 Order`, `-008 DataAccess`). The graph carries no link bridging a domain module to the deployable-host API surface, so no primary chain reaches the API column. Related evidence:

- `APP-DEP-002` (ARCH-VIOL-001): `CatalogBrandListEndpoint` depends directly on `EfRepository` — an endpoint bypassing the application service to reach data access, illustrating the missing service layer between host APIs and domain modules.
- `APP-DEP-001` (ARCH-VIOL-008 / `APP-RISK-002`): a module dependency cycle (Admin → ApplicationCore → Basket → Catalog → DataAccess → Identity → Order → Web) whose real-vs-static nature is unresolved (OQ-004).

### 5.7 Confidence-flagged and unresolved links

Links the graph marks below `HIGH`, or tied to an open question / assumption, that warrant human confirmation before relying on the chain:

| Link | Confidence | Reason / reference |
|------|------------|--------------------|
| `BIZ-CAP-002` → `BIZ-PROC-001` (cap→proc) | MEDIUM | Browse Catalog stage exercises Product Information Management; not a step-level process in evidence. |
| `BIZ-CAP-013` → `BIZ-PROC-004` (cap→proc) | MEDIUM | value-stream stage, not step-level (ASSUMP-005) |
| `BIZ-CAP-014` → `BIZ-PROC-004` (cap→proc) | MEDIUM | value-stream stage, not step-level (ASSUMP-005) |
| `BIZ-CAP-026` → `BIZ-PROC-008` (cap→proc) | LOW | Buyer Record Creation is tagged ACTIVE in the capability map, but the underlying Buyer entity is CONFIRMED dead/unimplemented code (RC-002; DATA-ENT-010 status=aspirational/unimplemented). Treat as aspirational, consistent with the entity_to_service / process_to_entity Buyer links. |
| `BIZ-CAP-009` → `BIZ-PROC-009` (cap→proc) | MEDIUM | value-stream stage, not step-level (ASSUMP-005) |
| `BIZ-CAP-034` → `BIZ-PROC-010` (cap→proc) | MEDIUM | value-stream stage, not step-level (ASSUMP-005) |
| `BIZ-PROC-001` → `DATA-ENT-001` (proc→ent) | MEDIUM | ASSUMP-005 |
| `BIZ-PROC-001` → `DATA-ENT-002` (proc→ent) | LOW | ASSUMP-005 |
| `BIZ-PROC-001` → `DATA-ENT-003` (proc→ent) | LOW | ASSUMP-005 |
| `BIZ-PROC-002` → `DATA-ENT-001` (proc→ent) | MEDIUM | ASSUMP-005 |
| `BIZ-PROC-003` → `DATA-ENT-008` (proc→ent) | MEDIUM | ASSUMP-005 |
| `BIZ-PROC-004` → `DATA-ENT-005` (proc→ent) | MEDIUM | ASSUMP-005 |
| `BIZ-PROC-004` → `DATA-ENT-004` (proc→ent) | MEDIUM | ASSUMP-005 |
| `BIZ-PROC-005` → `DATA-ENT-001` (proc→ent) | MEDIUM | ASSUMP-005 |
| `BIZ-PROC-006` → `DATA-ENT-002` (proc→ent) | MEDIUM | ASSUMP-005 |
| `BIZ-PROC-006` → `DATA-ENT-003` (proc→ent) | MEDIUM | ASSUMP-005 |
| `BIZ-PROC-007` → `DATA-ENT-009` (proc→ent) | MEDIUM | ASSUMP-005 |
| `BIZ-PROC-008` → `DATA-ENT-010` (proc→ent) | LOW | Buyer (DATA-ENT-010) is aspirational/unimplemented (RC-002); the process is rule-described but not a live persisted flow. |
| `BIZ-PROC-008` → `DATA-ENT-008` (proc→ent) | LOW | BIZ-PROC-008 (Buyer Record Creation) is a business-rule-described but unimplemented flow (RC-002); the ApplicationUser association is theoretical (rule BR008) rather than an observed runtime persistence path. |
| `BIZ-PROC-009` → `DATA-ENT-001` (proc→ent) | MEDIUM | ASSUMP-005 |
| `BIZ-PROC-009` → `DATA-ENT-002` (proc→ent) | LOW | ASSUMP-005 |
| `BIZ-PROC-009` → `DATA-ENT-003` (proc→ent) | LOW | ASSUMP-005 |
| `BIZ-PROC-010` → `DATA-ENT-008` (proc→ent) | MEDIUM | ASSUMP-005 |
| `BIZ-PROC-010` → `DATA-ENT-009` (proc→ent) | MEDIUM | ASSUMP-005 |
| `DATA-ENT-014` → `APP-SVC-001` (ent→svc) | MEDIUM | see ASSUMP-006 |
| `DATA-ENT-012` → `APP-SVC-001` (ent→svc) | MEDIUM | Ownership map assigns CatalogItemOrdered to Catalog module though it is physically an owned type of OrderAggregate (DATA-AGG-002). |
| `DATA-ENT-010` → `APP-SVC-004` (ent→svc) | LOW | Buyer is owned (per ownership map) by Order module but is aspirational/unimplemented dead code (RC-002). |
| `DATA-ENT-011` → `APP-SVC-004` (ent→svc) | LOW | PaymentMethod owned (per ownership map) by Order module but aspirational/unimplemented dead code (RC-002). |
| `DATA-ENT-009` → `APP-SVC-002` (ent→svc) | MEDIUM | see ASSUMP-006 |
| `DATA-ENT-001` → `APP-SVC-008` (ent→svc) | MEDIUM | Persistence is mediated by DataAccess (EfRepository) over CatalogContext; logical capability ownership remains Catalog. |
| `APP-SVC-011` → `APP-API-054` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-009` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-010` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-011` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-012` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-013` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-014` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-015` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-016` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-017` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-018` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-019` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-020` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-021` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-022` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-023` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-024` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-025` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-026` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-027` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-028` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-029` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-030` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-031` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-032` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-033` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-034` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-035` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-036` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-037` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-038` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-041` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-042` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-043` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-044` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-045` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-046` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-047` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-048` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-049` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-050` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-051` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-052` (svc→api) | MEDIUM |  |
| `APP-SVC-006` → `APP-API-055` (svc→api) | MEDIUM |  |
| `APP-SVC-016` → `APP-API-039` (svc→api) | MEDIUM |  |
| `APP-SVC-016` → `APP-API-040` (svc→api) | MEDIUM |  |
| `APP-SVC-016` → `APP-API-053` (svc→api) | MEDIUM |  |

### 5.8 Related open questions & assumptions

These graph-recorded caveats bear directly on traceability reliability:

- **ASSUMP-004** — `service_to_api` derivation from `source_file` path (the corrected basis; the non-existent `deployable_unit` field was removed during audit).
- **ASSUMP-005** — Browse Catalog / Adjust Basket `process_to_entity` links are value-stream stage inferences carrying LOW/MEDIUM confidence.
- **ASSUMP-006** — `Role` (`DATA-ENT-009`) → Identity ownership is MEDIUM (inferred ASP.NET Identity schema).
- **OQ-004** — module dependency cycle real vs static (`APP-DEP-001`).
- **OQ-008** — repository → entity bindings (`DATA-REPO-001/002`) demoted to inferred.
- **OQ-009** — synthetic `ROUTE`/`CLI` method labels on some `APP-API` nodes are not extracted HTTP verbs.

---

_End of traceability matrix. All ids resolve against `ENTERPRISE_KNOWLEDGE_GRAPH.json`; all assumptions/open-questions resolve against `.work/assumptions.json`._
