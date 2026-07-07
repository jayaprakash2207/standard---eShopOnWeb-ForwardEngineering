# Architecture Inventory

> ⚠️ **DISC-001 (verified 2026-06-25):** `CatalogItem` stock fields — `AvailableStock`,
> `RestockThreshold`, `MaxStockThreshold`, `OnReorder` — are a **verified discrepancy**: they do NOT
> exist in the real source (`github.com/dotnet-architecture/eShopOnWeb`, `main`, `CatalogItem.cs`, which
> declares only Name, Description, Price, PictureUri, CatalogTypeId, CatalogBrandId). Do **not** generate
> them; the derived reorder event (EVT-12) and any reorder capability/process are invalid. See
> [`../EVIDENCE_VERIFICATION_REPORT.md`](../EVIDENCE_VERIFICATION_REPORT.md).

> Source of truth: `ENTERPRISE_KNOWLEDGE_GRAPH.json` (schema 1.0, generated 2026-06-23).
> System: **eShopOnWeb (authoritative name 'unknown' in source evidence)** | Source project: `eShopOnWeb` | Evidence root: `bussiness-architecture 1/bussiness-architecture/output/eShopOnWeb`
>
> Evidence-only consolidation. Confidence/status signals (HIGH/MEDIUM/LOW, ACTIVE/DORMANT, implemented/aspirational-unimplemented, INFERRED, VERSION UNKNOWN, soft-reference, RC-002 dead code) are preserved verbatim from source fragments. No forward engineering; no new capabilities/entities/APIs invented. Cross-links are emitted only where a source file supports them.

This is a **foundation package**: a flat, countable inventory of every node in the canonical knowledge graph. Each row keeps its graph `id` so this document cross-references the JSON. It describes the **current + canonical** state only; it proposes no code or new designs.

## Summary Counts

| # | Category | Count |
|---|----------|-------|
| 1 | Business Capabilities | 39 |
| 2 | Actors | 5 |
| 3 | Business Processes | 10 |
| 4 | Data Entities | 15 |
| 5 | Data Relationships | 12 |
| 6 | Aggregates | 4 |
| 7 | Repositories | 4 |
| 8 | Application Services | 47 |
| 9 | Interfaces | 13 |
| 10 | APIs | 55 |
| 11 | Application Dependencies | 19 |
| 12 | Current Stack | 26 |
| 13 | Target Stack | 0 |
| 14 | Infrastructure | 8 |
| 15 | Security | 17 |
| | **Total nodes** | **274** |

## 1. Business Capabilities

| id | name | level / parent | status / confidence | evidence file(s) |
|----|------|----------------|---------------------|------------------|
| BIZ-CAP-001 | Catalog Management | L1 / — | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md`; `aa-outputs/final/business-capability-map.md` |
| BIZ-CAP-002 | Product Information Management | L2 / BIZ-CAP-001 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-003 | Catalog Item Details Maintenance | L3 / BIZ-CAP-002 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-004 | Product Classification | L3 / BIZ-CAP-002 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-005 | Product Image Management | L3 / BIZ-CAP-002 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-006 | Catalog Reference Data | L2 / BIZ-CAP-001 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-007 | Brand Management | L3 / BIZ-CAP-006 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-008 | Type Management | L3 / BIZ-CAP-006 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-009 | Catalog Seeding | L3 / BIZ-CAP-006 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-010 | Basket / Shopping Cart Management | L1 / — | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md`; `aa-outputs/final/business-capability-map.md` |
| BIZ-CAP-011 | Basket Maintenance | L2 / BIZ-CAP-010 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-012 | Add Item to Basket | L3 / BIZ-CAP-011 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-013 | Quantity Adjustment | L3 / BIZ-CAP-011 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-014 | Basket Cleanup | L3 / BIZ-CAP-011 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-015 | Session Continuity | L2 / BIZ-CAP-010 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-016 | Anonymous-to-Registered Basket Transfer | L3 / BIZ-CAP-015 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-017 | Order Management | L1 / — | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md`; `aa-outputs/final/business-capability-map.md` |
| BIZ-CAP-018 | Order Creation | L2 / BIZ-CAP-017 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-019 | Checkout Processing | L3 / BIZ-CAP-018 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-020 | Empty Basket Protection | L3 / BIZ-CAP-018 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-021 | Ordered Item Snapshot | L3 / BIZ-CAP-018 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-022 | Order Calculation | L2 / BIZ-CAP-017 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-023 | Order Total Calculation | L3 / BIZ-CAP-022 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-024 | Buyer / Customer Profile Management | L1 / — | ACTIVE / conf MEDIUM | `ba_documents/01_capability_map.md` |
| BIZ-CAP-025 | Buyer Identity | L2 / BIZ-CAP-024 | ACTIVE / conf MEDIUM | `ba_documents/01_capability_map.md` |
| BIZ-CAP-026 | Buyer Record Creation | L3 / BIZ-CAP-025 | ACTIVE / conf MEDIUM | `ba_documents/01_capability_map.md` |
| BIZ-CAP-027 | Payment Information | L2 / BIZ-CAP-024 | inferred / conf LOW | `ba_documents/01_capability_map.md` |
| BIZ-CAP-028 | Payment Method Management | L3 / BIZ-CAP-027 | inferred / conf LOW | `ba_documents/01_capability_map.md`; `aa-outputs/final/business-capability-map.md` |
| BIZ-CAP-029 | Identity & Authentication | L1 / — | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md`; `aa-outputs/final/business-capability-map.md` |
| BIZ-CAP-030 | Access Control | L2 / BIZ-CAP-029 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-031 | User Login | L3 / BIZ-CAP-030 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-032 | Token Issuance | L3 / BIZ-CAP-030 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-033 | Identity Seeding | L2 / BIZ-CAP-029 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-034 | Identity Data Seeding | L3 / BIZ-CAP-033 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-035 | Admin Catalog Operations (Blazor) | L1 / — | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md`; `aa-outputs/final/business-capability-map.md` |
| BIZ-CAP-036 | Administrative Catalog Interface | L2 / BIZ-CAP-035 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-037 | Catalog Item List View | L3 / BIZ-CAP-036 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-038 | Catalog Item Create/Delete | L3 / BIZ-CAP-036 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |
| BIZ-CAP-039 | Cached Data Refresh | L3 / BIZ-CAP-036 | ACTIVE / conf HIGH | `ba_documents/01_capability_map.md` |

## 2. Actors

| id | name | type | description | evidence file(s) |
|----|------|------|-------------|------------------|
| BIZ-ACT-001 | Customer / Buyer | human | Self-service storefront user who browses the catalog (items, types, brands), manages their own shopping basket (add ite… | `ba_documents/06_stakeholder_map.md`; `ba_documents/09_operating_model.md`; `ba_documents/02_value_stream.md` |
| BIZ-ACT-002 | Anonymous Shopper | human | Unauthenticated storefront visitor who can browse the catalog and build an anonymous basket prior to login. The anonymo… | `ba_documents/03_process_models.md`; `ba_documents/01_capability_map.md` |
| BIZ-ACT-003 | Administrator | human | Back-office role who creates, updates, and deletes catalog items, manages catalog brands and types, and views/manages a… | `ba_documents/06_stakeholder_map.md`; `ba_documents/09_operating_model.md`; `ba_documents/02_value_stream.md` |
| BIZ-ACT-004 | System / Service Account | system | Automated role performing startup data seeding, token issuance, image path composition, and basket/order total calculat… | `ba_documents/06_stakeholder_map.md`; `ba_documents/09_operating_model.md`; `ba_documents/02_value_stream.md` |
| BIZ-ACT-005 | Notification Recipients | external | Customers expected to receive order/email notifications via the Email Sender component. Noted as present in code but no… | `ba_documents/06_stakeholder_map.md` |

## 3. Business Processes

| id | name | trigger | steps / rules | status / confidence | evidence file(s) |
|----|------|---------|---------------|---------------------|------------------|
| BIZ-PROC-001 | Browse Catalog | Customer chooses to view available catalog items | 1 steps | conf MEDIUM | `ba_documents/02_value_stream.md` |
| BIZ-PROC-002 | Add Item to Basket | Customer (or anonymous user) selects a catalog item to purchase | 3 steps, 1 rules | conf HIGH | `ba_documents/03_process_models.md`; `ba_documents/04_business_rules.md` |
| BIZ-PROC-003 | Transfer Anonymous Basket to Registered User | An anonymous user logs in or registers | 3 steps, 1 rules | conf HIGH | `ba_documents/03_process_models.md`; `ba_documents/02_value_stream.md` |
| BIZ-PROC-004 | Adjust Basket | Customer reviews their merged/finalized basket before checkout | 1 steps, 2 rules | conf MEDIUM | `ba_documents/02_value_stream.md`; `ba_documents/04_business_rules.md` |
| BIZ-PROC-005 | Checkout / Place Order | Customer initiates checkout from their basket | 6 steps, 4 rules | conf HIGH | `ba_documents/03_process_models.md`; `ba_documents/04_business_rules.md` |
| BIZ-PROC-006 | Catalog Item Administration | Administrator manages catalog items via the admin (Blazor) interface | 4 steps, 4 rules | conf HIGH | `ba_documents/03_process_models.md`; `ba_documents/02_value_stream.md`; `ba_documents/04_business_rules.md` |
| BIZ-PROC-007 | User Authentication | User submits login credentials via the API | 3 steps | conf HIGH | `ba_documents/03_process_models.md`; `ba_documents/01_capability_map.md` |
| BIZ-PROC-008 | Buyer Record Creation | A buyer record needs to be created against a valid identity account (no explici… | 0 steps, 1 rules | conf MEDIUM | `ba_documents/01_capability_map.md`; `ba_documents/04_business_rules.md` |
| BIZ-PROC-009 | Catalog Seeding | System startup | 0 steps | conf MEDIUM | `ba_documents/01_capability_map.md`; `ba_documents/06_stakeholder_map.md` |
| BIZ-PROC-010 | Identity Data Seeding | System startup | 0 steps | conf MEDIUM | `ba_documents/01_capability_map.md`; `ba_documents/06_stakeholder_map.md` |

## 4. Data Entities

| id | name | key attributes | persisted / PII | status / confidence | evidence file(s) |
|----|------|----------------|-----------------|---------------------|------------------|
| DATA-ENT-001 | CatalogItem | Id, Name, Description, Price, PictureUri, CatalogTypeId, CatalogBrandId, AvailableStock,… | True / PII=False | implemented / conf 0.8 | `da-outputs/schema-catalogue.json`; `da-outputs/data-dictionary.md`; `da-outputs/erd.md` |
| DATA-ENT-002 | CatalogBrand | Id, Brand | True / PII=False | implemented / conf 0.8 | `da-outputs/schema-catalogue.json`; `da-outputs/data-dictionary.md`; `da-outputs/conceptual-data-model.md` |
| DATA-ENT-003 | CatalogType | Id, Type | True / PII=False | implemented / conf 0.8 | `da-outputs/schema-catalogue.json`; `da-outputs/data-dictionary.md`; `da-outputs/conceptual-data-model.md` |
| DATA-ENT-004 | Basket | Id, BuyerId | True / PII=False | implemented / conf 0.8 | `da-outputs/schema-catalogue.json`; `da-outputs/data-dictionary.md`; `da-outputs/erd.md` |
| DATA-ENT-005 | BasketItem | Id, BasketId, CatalogItemId, UnitPrice, Quantity | True / PII=False | implemented / conf 0.8 | `da-outputs/schema-catalogue.json`; `da-outputs/data-dictionary.md`; `da-outputs/conceptual-data-model.md` |
| DATA-ENT-006 | Order | Id, BuyerId, OrderDate, ShipToAddress_Street, ShipToAddress_City, ShipToAddress_State, Sh… | True / PII=True | implemented / conf 0.8 | `da-outputs/schema-catalogue.json`; `da-outputs/data-dictionary.md`; `da-outputs/erd.md` |
| DATA-ENT-007 | OrderItem | Id, OrderId, ItemOrdered_CatalogItemId, ItemOrdered_ProductName, ItemOrdered_PictureUri,… | True / PII=False | implemented / conf 0.8 | `da-outputs/schema-catalogue.json`; `da-outputs/data-dictionary.md`; `da-outputs/erd.md` |
| DATA-ENT-008 | ApplicationUser | Id, UserName, Email, PasswordHash, PhoneNumber | True / PII=True | implemented / conf 0.7 | `da-outputs/schema-catalogue.json`; `da-outputs/data-dictionary.md`; `da-outputs/redundancy-analysis.json` |
| DATA-ENT-009 | Role | Id, Name | True / PII=False | implemented / conf 0.7 | `da-outputs/schema-catalogue.json`; `da-outputs/data-dictionary.md`; `da-outputs/conceptual-data-model.md` |
| DATA-ENT-010 | Buyer |  | False / PII=False | aspirational/unimplemented / conf 0.9 | `da-outputs/schema-catalogue.json`; `da-outputs/data-dictionary.md`; `da-outputs/redundancy-analysis.json` |
| DATA-ENT-011 | PaymentMethod |  | False / PII=False | aspirational/unimplemented / conf 0.9 | `da-outputs/schema-catalogue.json`; `da-outputs/data-dictionary.md`; `da-outputs/conceptual-data-model.md` |
| DATA-ENT-012 | CatalogItemOrdered | ItemOrdered_CatalogItemId, ItemOrdered_ProductName, ItemOrdered_PictureUri | True / PII=False | implemented / conf 0.78 | `da-outputs/schema-catalogue.json`; `da-outputs/erd.md`; `da-outputs/redundancy-analysis.json` |
| DATA-ENT-013 | Address | ShipToAddress_Street, ShipToAddress_City, ShipToAddress_State, ShipToAddress_Country, Shi… | True / PII=True | implemented / conf 0.75 | `da-outputs/schema-catalogue.json`; `da-outputs/erd.md`; `da-outputs/data-dictionary.md` |
| DATA-ENT-014 | CatalogItemDetails |  | False / PII=False | aspirational/unimplemented / conf 0.72 | `da-outputs/schema-catalogue.json`; `da-outputs/data-dictionary.md`; `da-outputs/redundancy-analysis.json` |
| DATA-ENT-015 | BaseEntity | Id | False / PII=False | implemented / conf 0.8 | `da-outputs/schema-catalogue.json` |

## 5. Data Relationships

| id | from → to | cardinality | description | status | evidence file(s) |
|----|-----------|-------------|-------------|--------|------------------|
| DATA-REL-001 | CatalogItem → CatalogBrand | *..1 | A CatalogItem belongs to one CatalogBrand; a Brand can have many Products (Cata… | implemented | `da-outputs/erd.md`; `da-outputs/conceptual-data-model.md`; `da-outputs/data-dictionary.md` |
| DATA-REL-002 | CatalogItem → CatalogType | *..1 | A CatalogItem belongs to one CatalogType (category); a Category can have many P… | implemented | `da-outputs/erd.md`; `da-outputs/conceptual-data-model.md`; `da-outputs/data-dictionary.md` |
| DATA-REL-003 | Basket → BasketItem | 1..* | A Basket contains many BasketItems (BasketItem.BasketId FK -> Baskets.Id). | implemented | `da-outputs/erd.md`; `da-outputs/conceptual-data-model.md`; `da-outputs/data-dictionary.md` |
| DATA-REL-004 | BasketItem → CatalogItem | *..1 | A BasketItem references one CatalogItem (BasketItem.CatalogItemId FK -> Catalog… | implemented | `da-outputs/erd.md`; `da-outputs/data-dictionary.md`; `da-outputs/ba_documents/05_data_model.md` |
| DATA-REL-005 | Order → OrderItem | 1..* | An Order contains many OrderItems (OrderItem.OrderId FK -> Orders.Id). | implemented | `da-outputs/erd.md`; `da-outputs/conceptual-data-model.md`; `da-outputs/data-dictionary.md` |
| DATA-REL-006 | OrderItem → CatalogItemOrdered | 1..1 | An OrderItem embeds one CatalogItemOrdered owned-type snapshot (ItemOrdered_*)… | implemented | `da-outputs/erd.md`; `da-outputs/conceptual-data-model.md`; `da-outputs/ba_documents/05_data_model.md` |
| DATA-REL-007 | Order → Address | 1..1 | An Order ships to one Address (owned type ShipToAddress_* flattened into Orders… | implemented | `da-outputs/erd.md`; `da-outputs/data-dictionary.md`; `da-outputs/ba_documents/05_data_model.md` |
| DATA-REL-008 | Basket → ApplicationUser | *..1 | A Basket belongs to one customer via Basket.BuyerId, a SOFT (unenforced) cross-… | implemented-soft-reference | `da-outputs/erd.md`; `da-outputs/data-flow-map.md`; `da-outputs/conceptual-data-model.md` |
| DATA-REL-009 | Order → ApplicationUser | *..1 | An Order belongs to one customer via Order.BuyerId, a SOFT (unenforced) cross-d… | implemented-soft-reference | `da-outputs/erd.md`; `da-outputs/conceptual-data-model.md`; `da-outputs/data-dictionary.md` |
| DATA-REL-010 | ApplicationUser → Role | *..* | Users are assigned roles governing system access via the AspNetUserRoles join (… | implemented-inferred | `da-outputs/erd.md`; `da-outputs/data-dictionary.md`; `da-outputs/conceptual-data-model.md` |
| DATA-REL-011 | Basket → Order | 1..1 | A Basket is converted into an Order at checkout (one-to-one). An Order cannot b… | implemented | `da-outputs/ba_documents/05_data_model.md`; `da-outputs/conceptual-data-model.md`; `da-outputs/data-flow-map.md` |
| DATA-REL-012 | Buyer → PaymentMethod | 1..* | A Buyer may have one or more Payment Methods. ASPIRATIONAL ONLY (RC-002): both… | aspirational/unimplemented | `da-outputs/conceptual-data-model.md`; `da-outputs/ba_documents/05_data_model.md`; `da-outputs/schema-catalogue.json` |

## 6. Aggregates

| id | name | root entity | member entities | status | evidence file(s) |
|----|------|-------------|-----------------|--------|------------------|
| DATA-AGG-001 | BasketAggregate | Basket | Basket, BasketItem | implemented | `da-outputs/schema-catalogue.json`; `da-outputs/conceptual-data-model.md` |
| DATA-AGG-002 | OrderAggregate | Order | Order, OrderItem, Address, CatalogItemOrdered | implemented | `da-outputs/schema-catalogue.json`; `da-outputs/erd.md` |
| DATA-AGG-003 | BuyerAggregate | Buyer | Buyer, PaymentMethod | aspirational/unimplemented | `da-outputs/conceptual-data-model.md`; `da-outputs/schema-catalogue.json`; `da-outputs/redundancy-analysis.json` |
| DATA-AGG-004 | CatalogItem | CatalogItem | CatalogItem | implemented | `da-outputs/schema-catalogue.json`; `da-outputs/redundancy-analysis.json` |

## 7. Repositories

| id | name | kind | entities served (inferred) | confidence | evidence file(s) |
|----|------|------|----------------------------|------------|------------------|
| DATA-REPO-001 | IRepository<T> | interface | CatalogItem, Basket (inferred: Order) | 0.85 | `da-outputs/storage-pattern-analysis.md`; `da-outputs/data-flow-map.md` |
| DATA-REPO-002 | IReadRepository<T> | interface | (inferred: CatalogItem) | 0.8 | `da-outputs/storage-pattern-analysis.md` |
| DATA-REPO-003 | CatalogContext | ef-dbcontext | CatalogItem, CatalogBrand, CatalogType, Basket, BasketItem, Order, OrderItem | 0.9 | `da-outputs/schema-catalogue.json`; `da-outputs/storage-pattern-analysis.md`; `da-outputs/data-flow-map.md` |
| DATA-REPO-004 | AppIdentityDbContext | ef-dbcontext | ApplicationUser, Role | 0.7 | `da-outputs/schema-catalogue.json`; `da-outputs/storage-pattern-analysis.md` |

## 8. Application Services

| id | name | kind | layer / owning module | confidence | evidence file(s) |
|----|------|------|-----------------------|------------|------------------|
| APP-SVC-001 | Catalog | module | mixed / Catalog | MEDIUM | `aa-outputs/final/enterprise-application-architecture-blueprint.md`; `aa-outputs/final/application-architecture-summary.md`; `aa-outputs/final/service-boundary-options.md` |
| APP-SVC-002 | Identity | module | mixed / Identity | MEDIUM | `aa-outputs/final/enterprise-application-architecture-blueprint.md`; `aa-outputs/final/application-architecture-summary.md`; `aa-outputs/final/service-boundary-options.md` |
| APP-SVC-003 | Basket | module | mixed / Basket | MEDIUM | `aa-outputs/final/enterprise-application-architecture-blueprint.md`; `aa-outputs/final/service-boundary-options.md`; `aa-outputs/final/data-ownership-map.md` |
| APP-SVC-004 | Order | module | mixed / Order | MEDIUM | `aa-outputs/final/enterprise-application-architecture-blueprint.md`; `aa-outputs/final/service-boundary-options.md`; `aa-outputs/final/data-ownership-map.md` |
| APP-SVC-005 | Admin | module | Presentation/UI / Admin | MEDIUM | `aa-outputs/final/enterprise-application-architecture-blueprint.md`; `aa-outputs/final/service-boundary-options.md` |
| APP-SVC-006 | Web | module+deployable-service | mixed / Web | HIGH | `aa-outputs/final/enterprise-application-architecture-blueprint.md`; `aa-outputs/final/application-architecture-summary.md`; `aa-outputs/final/system-inventory.json` |
| APP-SVC-007 | ApplicationCore | module+component | Application/Domain / ApplicationCore | HIGH | `aa-outputs/final/enterprise-application-architecture-blueprint.md`; `aa-outputs/final/system-inventory.json`; `ta-outputs/ta_agent1/component-service-map.md` |
| APP-SVC-008 | DataAccess | module | DataAccess / DataAccess | MEDIUM | `aa-outputs/final/enterprise-application-architecture-blueprint.md`; `aa-outputs/final/service-boundary-options.md` |
| APP-SVC-009 | Infrastructure | module+component | Infrastructure / Infrastructure | HIGH | `aa-outputs/final/enterprise-application-architecture-blueprint.md`; `aa-outputs/final/system-inventory.json`; `ta-outputs/ta_agent1/component-service-map.md` |
| APP-SVC-010 | CrossCutting | module | CrossCutting / CrossCutting | MEDIUM | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-SVC-011 | PublicApi | module+deployable-service | API / PublicApi | HIGH | `aa-outputs/final/enterprise-application-architecture-blueprint.md`; `aa-outputs/final/system-inventory.json`; `ta-outputs/ta_agent1/component-service-map.md` |
| APP-SVC-012 | SharedContracts | module+component | Application / SharedContracts | HIGH | `aa-outputs/final/enterprise-application-architecture-blueprint.md`; `ta-outputs/ta_agent1/component-service-map.md`; `aa-outputs/final/system-inventory.json` |
| APP-SVC-013 | Verification | module | mixed / Verification | LOW | `aa-outputs/final/enterprise-application-architecture-blueprint.md`; `aa-outputs/final/application-architecture-summary.md` |
| APP-SVC-016 | BlazorAdmin | app-service | Presentation/UI / Admin | HIGH | `aa-outputs/final/system-inventory.json`; `ta-outputs/ta_agent1/component-service-map.md` |
| APP-SVC-020 | UriComposer | domain-service | Application / ApplicationCore | HIGH | `aa-outputs/final/enterprise-application-architecture-blueprint.md`; `aa-outputs/final/application-architecture-summary.md` |
| APP-SVC-021 | IdentityTokenClaimService | app-service | Application / Identity | HIGH | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-SVC-022 | EfRepository | component | DataAccess / DataAccess | HIGH | `aa-outputs/final/enterprise-application-architecture-blueprint.md`; `aa-outputs/final/data-ownership-map.md` |
| APP-SVC-023 | CatalogContext | component | DataAccess / Catalog | HIGH | `aa-outputs/final/data-ownership-map.md`; `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-SVC-024 | AppIdentityDbContext | component | DataAccess / Identity | HIGH | `aa-outputs/final/data-ownership-map.md` |
| APP-SVC-025 | CatalogContextSeed | component | DataAccess / Catalog | HIGH | `aa-outputs/final/system-inventory.json`; `aa-outputs/final/data-ownership-map.md` |
| APP-SVC-026 | AppIdentityDbContextSeed | component | DataAccess / Identity | HIGH | `aa-outputs/final/system-inventory.json`; `aa-outputs/final/data-ownership-map.md` |
| APP-SVC-027 | BasketGuards | domain-service | Application / ApplicationCore | MEDIUM | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-SVC-028 | JsonExtensions | domain-service | CrossCutting / ApplicationCore | MEDIUM | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-SVC-029 | AuthenticateEndpoint | component | API / Identity | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-SVC-030 | CatalogBrandListEndpoint | component | API / Catalog | HIGH | `aa-outputs/final/application-interface-catalogue.json`; `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-SVC-031 | CatalogItemGetByIdEndpoint | component | API / Catalog | HIGH | `aa-outputs/final/application-interface-catalogue.json`; `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-SVC-032 | CatalogItemListPagedEndpoint | component | API / Catalog | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-SVC-033 | CreateCatalogItemEndpoint | component | API / Catalog | HIGH | `aa-outputs/final/application-interface-catalogue.json`; `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-SVC-034 | DeleteCatalogItemEndpoint | component | API / Catalog | HIGH | `aa-outputs/final/application-interface-catalogue.json`; `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-SVC-035 | UpdateCatalogItemEndpoint | component | API / Catalog | HIGH | `aa-outputs/final/application-interface-catalogue.json`; `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-SVC-036 | CatalogTypeListEndpoint | component | API / Catalog | HIGH | `aa-outputs/final/application-interface-catalogue.json`; `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-SVC-037 | ManageController | component | API / Identity | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-SVC-038 | OrderController | component | API / Order | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-SVC-039 | UserController | component | API / Identity | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-SVC-040 | IndexModel | component | Presentation/UI / Web | MEDIUM | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-SVC-041 | GetMyOrders | component | Application / Web | MEDIUM | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-SVC-042 | GetMyOrdersHandler | component | Application / Web | MEDIUM | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-SVC-043 | GetOrderDetails | component | Application / Web | MEDIUM | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-SVC-044 | CachedCatalogItemServiceDecorator | component | Presentation/UI / Catalog | MEDIUM | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-SVC-045 | CachedCatalogLookupDataServiceDecorator | component | Presentation/UI / Catalog | MEDIUM | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-SVC-046 | BlazorComponent | component | Presentation/UI / Admin | MEDIUM | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-SVC-047 | BlazorLayoutComponent | component | Presentation/UI / Admin | MEDIUM | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-SVC-048 | ToastComponent | component | Presentation/UI / Admin | MEDIUM | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-SVC-049 | RefreshBroadcast | component | Presentation/UI / Admin | MEDIUM | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-SVC-050 | List | component | Presentation/UI / Catalog | HIGH | `aa-outputs/final/enterprise-application-architecture-blueprint.md`; `aa-outputs/final/application-interface-catalogue.json` |
| APP-SVC-051 | CustomAuthStateProvider | component | Integration / Admin | MEDIUM | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-SVC-052 | Program | component | CrossCutting / CrossCutting | HIGH | `aa-outputs/final/application-interface-catalogue.json` |

## 9. Interfaces

| id | name | kind | implemented by | evidence file(s) |
|----|------|------|----------------|------------------|
| APP-IF-001 | IRepository<T> | abstraction | EfRepository | `aa-outputs/final/data-ownership-map.md`; `aa-outputs/final/application-interface-catalogue.json` |
| APP-IF-002 | IReadRepository<T> | abstraction | EfRepository | `aa-outputs/final/data-ownership-map.md`; `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-IF-003 | ITokenClaimsService | port | IdentityTokenClaimService | `aa-outputs/final/application-interface-catalogue.json`; `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-IF-004 | IUriComposer | abstraction | UriComposer | `aa-outputs/final/application-interface-catalogue.json`; `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-IF-005 | IAppLogger<T> | abstraction |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md`; `aa-outputs/final/application-interface-catalogue.json` |
| APP-IF-006 | IBasketService | abstraction |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-IF-007 | IBasketQueryService | abstraction |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-IF-008 | IEmailSender | port |  | `aa-outputs/final/enterprise-application-architecture-blueprint.md`; `aa-outputs/final/application-interface-catalogue.json` |
| APP-IF-009 | IAggregateRoot | abstraction |  | `aa-outputs/final/data-ownership-map.md` |
| APP-IF-010 | ICatalogItemService | abstraction | CachedCatalogItemServiceDecorator | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-IF-011 | ICatalogLookupDataService | abstraction | CachedCatalogLookupDataServiceDecorator | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-IF-012 | IMediator | external |  | `aa-outputs/final/application-interface-catalogue.json`; `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-IF-013 | CustomAuthStateProvider | UI | CustomAuthStateProvider | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |

## 10. APIs

| id | method / path | handler | deployable unit | auth | confidence | evidence file(s) |
|----|---------------|---------|-----------------|------|------------|------------------|
| APP-API-001 | POST /api/authenticate | AuthenticateEndpoint | PublicApi | issues JWT (security/identity clue); ITokenClaimsService + SignInManager.PasswordSignInAsync | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-002 | GET /api/catalog-brands | CatalogBrandListEndpoint | PublicApi | not noted | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-003 | GET /api/catalog-items/{catalogItemId} | CatalogItemGetByIdEndpoint | PublicApi | not noted | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-004 | GET /api/catalog-items | CatalogItemListPagedEndpoint | PublicApi | not noted | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-005 | POST /api/catalog-items | CreateCatalogItemEndpoint | PublicApi | not noted | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-006 | DELETE /api/catalog-items/{catalogItemId} | DeleteCatalogItemEndpoint | PublicApi | not noted | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-007 | PUT /api/catalog-items | UpdateCatalogItemEndpoint | PublicApi | not noted | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-008 | GET /api/catalog-types | CatalogTypeListEndpoint | PublicApi | not noted | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-009 | ROUTE /{controller:slugify=Home}/{action:slugify=Index}/{id?} *(synth… | Program (conventional MVC route registr… | Web | unknown | LOW | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-010 | ROUTE ASP.NET Razor Pages route registration *(synthetic)* | Program (Razor Pages route registration) | Web | unknown | LOW | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-011 | ROUTE /index.html *(synthetic)* | Program (SPA fallback route) | Web | not noted | LOW | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-012 | GET /home_page_health_check | Program (health check route) | Web | not noted | LOW | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-013 | GET /api_health_check | Program (health check route) | Web | not noted | LOW | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-014 | GET /Manage/MyAccount | ManageController.MyAccount | Web | user_facing identity (UserManager) | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-015 | POST /Manage/MyAccount | ManageController.MyAccount | Web | user_facing identity | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-016 | POST /Manage/SendVerificationEmail | ManageController.SendVerificationEmail | Web | user_facing identity; IEmailSender | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-017 | GET /Manage/ChangePassword | ManageController.ChangePassword | Web | user_facing identity | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-018 | POST /Manage/ChangePassword | ManageController.ChangePassword | Web | user_facing identity; SignInManager | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-019 | GET /Manage/SetPassword | ManageController.SetPassword | Web | user_facing identity | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-020 | POST /Manage/SetPassword | ManageController.SetPassword | Web | user_facing identity; SignInManager | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-021 | GET /Manage/ExternalLogins | ManageController.ExternalLogins | Web | user_facing identity | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-022 | POST /Manage/LinkLogin | ManageController.LinkLogin | Web | user_facing identity | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-023 | GET /Manage/LinkLoginCallback | ManageController.LinkLoginCallback | Web | user_facing identity | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-024 | POST /Manage/RemoveLogin | ManageController.RemoveLogin | Web | user_facing identity | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-025 | GET /Manage/TwoFactorAuthentication | ManageController.TwoFactorAuthentication | Web | user_facing identity | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-026 | GET /Manage/Disable2faWarning | ManageController.Disable2faWarning | Web | user_facing identity | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-027 | POST /Manage/Disable2fa | ManageController.Disable2fa | Web | user_facing identity | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-028 | GET /Manage/EnableAuthenticator | ManageController.EnableAuthenticator | Web | user_facing identity | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-029 | GET /Manage/ShowRecoveryCodes | ManageController.ShowRecoveryCodes | Web | user_facing identity | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-030 | POST /Manage/EnableAuthenticator | ManageController.EnableAuthenticator | Web | user_facing identity | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-031 | GET /Manage/ResetAuthenticatorWarning | ManageController.ResetAuthenticatorWarn… | Web | user_facing identity | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-032 | POST /Manage/ResetAuthenticator | ManageController.ResetAuthenticator | Web | user_facing identity | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-033 | POST /Manage/GenerateRecoveryCodes | ManageController.GenerateRecoveryCodes | Web | user_facing identity | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-034 | GET /Manage/GenerateRecoveryCodesWarning | ManageController.GenerateRecoveryCodesW… | Web | user_facing identity | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-035 | GET /Order/MyOrders | OrderController.MyOrders (IMediator.Sen… | Web | user_facing | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-036 | GET /Order/Detail/{orderId} | OrderController.Detail (IMediator.Send) | Web | user_facing | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-037 | GET /User | UserController.GetCurrentUser | Web | user_facing identity (SignInManager) | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-038 | POST /User/Logout | UserController.Logout | Web | user_facing identity; SignInManager.SignOutAsync | HIGH | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-039 | ROUTE /logout *(synthetic)* | Logout (Logout.razor; IJSRuntime, HttpC… | BlazorAdmin | user_facing | MEDIUM | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-040 | ROUTE /admin *(synthetic)* | List (List.razor; calls ICatalogItemSer… | BlazorAdmin | user_facing | MEDIUM | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-041 | GET /Account/ConfirmEmail | ConfirmEmail (Razor Page) | Web | user_facing identity | LOW | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-042 | GET /Account/Login | Login (Razor Page) | Web | user_facing identity | LOW | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-043 | GET /Account/Logout | Logout (Razor Page) | Web | user_facing identity | LOW | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-044 | GET /Account/Register | Register (Razor Page) | Web | user_facing identity | LOW | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-045 | GET /Error | Error (Razor Page) | Web | user_facing | LOW | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-046 | GET / | Index (Razor Page) | Web | user_facing | LOW | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-047 | GET /Privacy | Privacy (Razor Page) | Web | user_facing | LOW | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-048 | GET /Admin/EditCatalogItem | EditCatalogItem (Razor Page) | Web | user_facing (admin) | LOW | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-049 | GET /Admin | Index (Admin Razor Page) | Web | user_facing (admin) | LOW | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-050 | GET /Basket/Checkout | Checkout (Razor Page) | Web | user_facing | LOW | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-051 | GET /{handler?} | Index (Basket Razor Page) | Web | user_facing | MEDIUM | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-052 | GET /Basket/Success | Success (Razor Page) | Web | user_facing | LOW | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-053 | CLI .NET application bootstrap Program.cs (BlazorAdmin) *(synthetic)* | Program | BlazorAdmin | internal | MEDIUM | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-054 | CLI .NET application bootstrap Program.cs (PublicApi) *(synthetic)* | Program | PublicApi | internal | MEDIUM | `aa-outputs/final/application-interface-catalogue.json` |
| APP-API-055 | CLI .NET application bootstrap Program.cs (Web) *(synthetic)* | Program | Web | internal | MEDIUM | `aa-outputs/final/application-interface-catalogue.json` |

## 11. Application Dependencies

| id | from → to | type | note | evidence file(s) |
|----|-----------|------|------|------------------|
| APP-DEP-001 | Admin -> ApplicationCore -> Basket -> Catalog -> DataAccess -> Identity -> Order -> Web → (cycle back to Admin) | module | Module dependency CYCLE (ARCH-VIOL-008 / APP-RISK-002). 1 module cycle detected… | `aa-outputs/final/enterprise-application-architecture-blueprint.md`; `aa-outputs/final/application-architecture-summary.md` |
| APP-DEP-002 | CatalogBrandListEndpoint → EfRepository | component | Direct controller-like-to-repository dependency (ARCH-VIOL-001). Layer violatio… | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-DEP-003 | CatalogItemGetByIdEndpoint → EfRepository | component | Direct endpoint-to-repository dependency (ARCH-VIOL-002). | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-DEP-004 | CreateCatalogItemEndpoint → EfRepository | component | Direct endpoint-to-repository dependency (ARCH-VIOL-003). | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-DEP-005 | DeleteCatalogItemEndpoint → EfRepository | component | Direct endpoint-to-repository dependency (ARCH-VIOL-004). | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-DEP-006 | UpdateCatalogItemEndpoint → EfRepository | component | Direct endpoint-to-repository dependency (ARCH-VIOL-005). | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-DEP-007 | CatalogTypeListEndpoint → EfRepository | component | Direct endpoint-to-repository dependency (ARCH-VIOL-006). | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-DEP-008 | IndexModel → EfRepository | component | Razor PageModel directly depends on repository (ARCH-VIOL-007). | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-DEP-009 | EfRepository → (many consumers) | component | High-coupling component, total coupling score 16 (ARCH-VIOL-009 / APP-RISK-004)… | `aa-outputs/final/enterprise-application-architecture-blueprint.md`; `aa-outputs/final/application-architecture-summary.md` |
| APP-DEP-010 | UriComposer → (catalog endpoints) | component | High-coupling component, coupling score 8 (ARCH-VIOL-010). | `aa-outputs/final/enterprise-application-architecture-blueprint.md` |
| APP-DEP-011 | Web → PublicApi | module | No project reference from Web to PublicApi (Web references ApplicationCore, Bla… | `ta-outputs/ta_agent1/integration-dependency-graph.md` |
| APP-DEP-012 | PublicApi → ApplicationCore, Infrastructure | package | Project references: PublicApi.csproj -> ApplicationCore.csproj, Infrastructure.… | `aa-outputs/final/system-inventory.json` |
| APP-DEP-013 | Web → ApplicationCore, BlazorAdmin, BlazorShared, Infrastructure | package | Project references: Web.csproj -> ApplicationCore, BlazorAdmin, BlazorShared, I… | `aa-outputs/final/system-inventory.json` |
| APP-DEP-014 | Infrastructure → ApplicationCore | package | Project reference: Infrastructure.csproj -> ApplicationCore.csproj. | `aa-outputs/final/system-inventory.json` |
| APP-DEP-015 | ApplicationCore → BlazorShared | package | Project reference: ApplicationCore.csproj -> BlazorShared.csproj. (Unusual: dom… | `aa-outputs/final/system-inventory.json` |
| APP-DEP-016 | BlazorAdmin → BlazorShared | package | Project reference: BlazorAdmin.csproj -> BlazorShared.csproj. | `aa-outputs/final/system-inventory.json` |
| APP-DEP-017 | BlazorAdmin → PublicApi | component | Runtime HTTP/HTTPS synchronous dependency via baseUrls.apiBase. BlazorAdmin SPA… | `ta-outputs/ta_agent1/integration-dependency-graph.md` |
| APP-DEP-018 | BlazorAdmin → Web | component | Runtime HTTP/HTTPS synchronous dependency via baseUrls.webBase. | `ta-outputs/ta_agent1/integration-dependency-graph.md` |
| APP-DEP-019 | Web, PublicApi → sqlserver | component | Runtime TCP/SQL synchronous dependency (ConnectionStrings:CatalogConnection / I… | `ta-outputs/ta_agent1/integration-dependency-graph.md` |

## 12. Current Stack

| id | name | version | category / layer | confidence | evidence / source |
|----|------|---------|------------------|------------|-------------------|
| TECH-CUR-001 | .NET SDK / Runtime | 8.0.x | Runtime / SDK / Runtime / Build | HIGH | `.github/workflows/dotnetcore.yml`; `ta-outputs/technology-stack-assessment.md: 'Active` |
| TECH-CUR-002 | ASP.NET Core (Microsoft.NET.Sdk.Web) | 8.0 (project SDK, no version declared) | Web Application Framework / SDK / Application | HIGH | `src/Web/Web.csproj, src/PublicApi/PublicApi.csproj`; `ta-outputs/technology-stack-assessment.md: 'Active` |
| TECH-CUR-003 | Blazor WebAssembly (Microsoft.NET.Sdk.BlazorWebAssembly + Microsoft.AspNetCore.Components.WebAssembly) | 8.0 (project SDK / package versions not declared) | Frontend Framework / SDK / Application (Frontend) | HIGH | `src/BlazorAdmin/BlazorAdmin.csproj`; `ta-outputs/technology-stack-assessment.md: 'Active` |
| TECH-CUR-004 | Microsoft.AspNetCore.Components.WebAssembly.Server | (not declared) | Blazor WASM Hosting / Application | LOW | `src/Web/Web.csproj`; `ta-outputs/technology-stack-assessment.md: 'Active` |
| TECH-CUR-005 | Entity Framework Core (ORM) | (not declared) | ORM / Data Access / Data | LOW | `src/Infrastructure/Infrastructure.csproj, src/Web/Web.csproj, src/PublicApi/PublicApi.csproj`; `ta-outputs/ta_agent1/data-store-registry.md` |
| TECH-CUR-006 | Microsoft.EntityFrameworkCore.SqlServer | (not declared) | ORM Provider / Database Driver / Data | LOW | `src/Web/Web.csproj, src/PublicApi/PublicApi.csproj (SHARED COMPONENT)`; `ta-outputs/technology-stack-assessment.md: 'Active` |
| TECH-CUR-007 | Npgsql.EntityFrameworkCore.PostgreSQL | (not declared) | ORM Provider / Database Driver / Data | LOW | `src/Infrastructure/Infrastructure.csproj`; `ta-outputs/technology-stack-assessment.md: 'Active` |
| TECH-CUR-008 | Microsoft.EntityFrameworkCore.InMemory | (not declared) | ORM Provider / In-Memory Data Store / Data | LOW | `src/Infrastructure/Infrastructure.csproj, src/PublicApi/PublicApi.csproj, src/Web/Web.csproj + 4 test projects (SHARED COMPONENT)`; `ta-outputs/technology-stack-assessment.md: 'Active in production projects, not just tests ... suggests an UseOnlyInMemoryDatabase-style runtime switch (TD-16)'`; `tests/PublicApiIntegrationTests/appsettings.test.json` |
| TECH-CUR-009 | Ardalis.Specification (+ EntityFrameworkCore evaluator) | (not declared) | Specification Pattern Library / Application / Data | LOW | `src/ApplicationCore/ApplicationCore.csproj, src/Web/Web.csproj; Ardalis.Specification.EntityFrameworkCore in src/Infrastructure/Infrastructure.csproj`; `ta-outputs/technology-stack-assessment.md: 'Active` |
| TECH-CUR-010 | Ardalis Guard/Result/ApiEndpoints libraries | (not declared) | Application Pattern Libraries / Application | LOW | `Ardalis.GuardClauses, Ardalis.Result`; `Ardalis.ApiEndpoints`; `Ardalis.ListStartupServices` |
| TECH-CUR-011 | MediatR | (not declared) | Mediator / CQRS Library / Application | LOW | `src/Web/Web.csproj only`; `ta-outputs/technology-stack-assessment.md: 'Declared-only` |
| TECH-CUR-012 | AutoMapper.Extensions.Microsoft.DependencyInjection | (not declared) | Object Mapping Library / Application | LOW | `src/PublicApi/PublicApi.csproj, src/Web/Web.csproj (SHARED COMPONENT)`; `ta-outputs/technology-stack-assessment.md: 'Active` |
| TECH-CUR-013 | MinimalApi.Endpoint | (not declared) | Minimal API Pattern Library / Application | LOW | `src/PublicApi/PublicApi.csproj`; `ta-outputs/technology-stack-assessment.md: 'Active` |
| TECH-CUR-014 | Swashbuckle.AspNetCore (+ SwaggerUI, + Annotations) | (not declared) | OpenAPI / Swagger Documentation / Application | LOW | `src/PublicApi/PublicApi.csproj`; `ta-outputs/technology-stack-assessment.md: 'Active` |
| TECH-CUR-015 | FluentValidation | (not declared) | Validation Library / Application | LOW | `src/BlazorShared/BlazorShared.csproj`; `ta-outputs/technology-stack-assessment.md: 'Declared-only; shared validation rules ... no validator class evidence provided'` |
| TECH-CUR-016 | System.Text.Json / System.Net.Http.Json | (not declared) | JSON Serialization / HTTP-JSON Client / Application | LOW | `System.Text.Json`; `System.Net.Http.Json` |
| TECH-CUR-017 | Blazor client libraries (Blazored.LocalStorage, BlazorInputFile, Microsoft.Extensions.Identity.Core) | (not declared) | Blazor Client Component Libraries / Application (Frontend) | LOW | `src/BlazorAdmin/BlazorAdmin.csproj, src/BlazorShared/BlazorShared.csproj`; `ta-outputs/technology-stack-assessment.md: BlazorInputFile 'Declared-only ... possible legacy dependency superseded by framework-native InputFile since .NET 5'` |
| TECH-CUR-018 | Microsoft.Extensions.Logging.Configuration | (not declared) | Logging Configuration / Observability | LOW | `src/BlazorAdmin/BlazorAdmin.csproj`; `ta-outputs/technology-stack-assessment.md: 'Active` |
| TECH-CUR-019 | Microsoft.AspNetCore.Diagnostics.EntityFrameworkCore | (not declared) | EF Core Developer Diagnostics / Observability / Data | LOW | `src/Web/Web.csproj, src/PublicApi/PublicApi.csproj (SHARED COMPONENT)`; `ta-outputs/technology-stack-assessment.md: 'Active` |
| TECH-CUR-020 | Azure SQL Edge (sqlserver container) | unknown (no tag declared; defaults to latest) | Relational Database Engine / Data | LOW | `docker-compose.yml`; `ta-outputs/technology-stack-assessment.md: 'EOL` |
| TECH-CUR-021 | PostgreSQL (eShopCatalog, eShopIdentity) | unknown | Relational Database Engine / Data | LOW | `src/Web/appsettings.json, src/PublicApi/appsettings.json (default config)`; `ta-outputs/ta_agent1/data-store-registry.md: 'VERSION UNKNOWN; no IaC declaration found, host=localhost:5432 implies external/local dev instance'` |
| TECH-CUR-022 | EF Core InMemory Database (data store) | unknown | In-Memory / Test Data Store / Data | LOW | `ta-outputs/ta_agent1/data-store-registry.md`; `Provider: Microsoft.EntityFrameworkCore.InMemory (TECH-CUR-008)` |
| TECH-CUR-023 | Docker base images (mcr.microsoft.com/dotnet/sdk:8.0, mcr.microsoft.com/dotnet/aspnet:8.0) | 8.0 | Container Base Images / Build / Infrastructure | HIGH | `src/Web/Dockerfile, src/PublicApi/Dockerfile`; `ta-outputs/technology-stack-assessment.md: 'Active` |
| TECH-CUR-024 | Build & dev tooling (EF Core Tools, CodeGeneration.Design, Containers.Tools.Targets, BuildBundlerMinifier, LibraryManager, WebAssembly.DevServer) | (not declared; dotnet-xunit 2.3.1) | Build / Developer Tooling / Build | LOW | `Microsoft.EntityFrameworkCore.Tools, Microsoft.VisualStudio.Web.CodeGeneration.Design`; `Microsoft.VisualStudio.Azure.Containers.Tools.Targets`; `BuildBundlerMinifier (Release-only), Microsoft.Web.LibraryManager.Build` |
| TECH-CUR-025 | Test tooling (xUnit, MSTest, NSubstitute, coverlet, Microsoft.NET.Test.Sdk, Mvc.Testing) | (not declared; dotnet-xunit 2.3.1) | Test Frameworks & Tooling / Build / Test | LOW | `xunit, xunit.runner.visualstudio, xunit.runner.console`; `MSTest.TestAdapter/TestFramework, coverlet.collector`; `NSubstitute(+Analyzers)` |
| TECH-CUR-026 | GitHub Actions (actions/checkout@v2, actions/setup-dotnet@v1, microsoft/RichCodeNavIndexer@v0.1) | checkout@v2, setup-dotnet@v1, RichCodeNavIndexer@v0.1 | CI/CD Actions / CI-CD | HIGH | `.github/workflows/dotnetcore.yml, .github/workflows/richnav.yml`; `ta-outputs/ta_agent1/infrastructure-deployment-blueprint.md` |

## 13. Target Stack

_No target-stack nodes are present in the graph (count = 0). This foundation package records current + canonical state only; the target stack is an input deferred to future forward engineering._

## 14. Infrastructure

| id | name | type | description | evidence file(s) |
|----|------|------|-------------|------------------|
| TECH-INF-001 | eshopwebmvc container | Docker Compose service / container | Web (MVC + Razor + hosted Blazor WASM) container. Build image mcr.microsoft.com/dotnet/sdk:8.0; run… | `ta-outputs/ta_agent1/infrastructure-deployment-blueprint.md`; `docker-compose.yml, docker-compose.override.yml, src/Web/Dockerfile`; `ta-outputs/nfr-registry.md NFR-01/NFR-02/NFR-28` |
| TECH-INF-002 | eshoppublicapi container | Docker Compose service / container | PublicApi (public REST API + Swagger UI) container. Build image mcr.microsoft.com/dotnet/sdk:8.0; r… | `ta-outputs/ta_agent1/infrastructure-deployment-blueprint.md`; `docker-compose.yml, docker-compose.override.yml, src/PublicApi/Dockerfile`; `ta-outputs/nfr-registry.md NFR-03/NFR-04/NFR-05` |
| TECH-INF-003 | sqlserver container (Azure SQL Edge) | Docker Compose service / database container | mcr.microsoft.com/azure-sql-edge image (no tag, defaults to latest). env: SA_PASSWORD, ACCEPT_EULA=… | `ta-outputs/ta_agent1/infrastructure-deployment-blueprint.md`; `ta-outputs/ta_agent1/data-store-registry.md, ta-outputs/technology-stack-assessment.md (EOL)`; `ta-outputs/operational-architecture-assessment.md` |
| TECH-INF-004 | docker-compose orchestration (local/Docker environment) | Container orchestration / compose | docker-compose.yml + docker-compose.override.yml define the three-service local Docker topology (es… | `ta-outputs/ta_agent1/infrastructure-deployment-blueprint.md`; `ta-outputs/nfr-registry.md NFR-27 (no resource limits), NFR-28 (depends_on order only)` |
| TECH-INF-005 | GitHub Actions CI/CD pipelines | CI/CD pipeline | Two workflows: dotnetcore.yml (build + test on push/PR/dispatch, all branches, ubuntu-latest; dotne… | `ta-outputs/ta_agent1/infrastructure-deployment-blueprint.md`; `ta-outputs/operational-architecture-assessment.md` |
| TECH-INF-006 | Dependabot (NuGet) | Dependency-management automation | Automated NuGet dependency-update bot. package-ecosystem: nuget, directory: /, schedule.interval: d… | `.github/dependabot.yml`; `ta-outputs/ta_agent1/infrastructure-deployment-blueprint.md`; `ta-outputs/nfr-registry.md NFR-20` |
| TECH-INF-007 | Azure deployment environment (azd / parameters-only) | Cloud deployment target (declared, parameters only) | Azure azd deployment scope referenced via infra/main.parameters.json (environmentName, location, pr… | `ta-outputs/ta_agent1/infrastructure-deployment-blueprint.md`; `ta-outputs/security-architecture-assessment.md` |
| TECH-INF-008 | Azure Key Vault (referenced) | Secrets management cloud service (referenced) | Referenced via Azure.Identity + Azure.Extensions.AspNetCore.Configuration.Secrets packages and the… | `ta-outputs/ta_agent1/infrastructure-deployment-blueprint.md / ta-outputs/ta_agent1/integration-dependency-graph.md`; `src/Web/Web.csproj, infra/main.parameters.json` |

## 15. Security

| id | name | type | severity | description | evidence file(s) |
|----|------|------|----------|-------------|------------------|
| TECH-SEC-001 | ASP.NET Core Identity (cookie-based auth + user store) | auth |  | ASP.NET Core Identity backed by EF Core (Microsoft.AspNetCore.Identity.EntityFrameworkCor… | `ta-outputs/ta_agent1/security-configuration-snapshot.md`; `ta-outputs/security-architecture-assessment.md` |
| TECH-SEC-002 | JWT Bearer Authentication | auth | High | Microsoft.AspNetCore.Authentication.JwtBearer + System.IdentityModel.Tokens.Jwt reference… | `ta-outputs/ta_agent1/security-configuration-snapshot.md`; `ta-outputs/security-architecture-assessment.md` |
| TECH-SEC-003 | Blazor WebAssembly Authentication (BlazorAdmin) | auth | High | Microsoft.AspNetCore.Components.WebAssembly.Authentication + Microsoft.Extensions.Identit… | `ta-outputs/ta_agent1/security-configuration-snapshot.md`; `ta-outputs/security-architecture-assessment.md` |
| TECH-SEC-004 | Authorization Components (role/claims-based) | authz | Medium | Microsoft.AspNetCore.Components.Authorization in BlazorAdmin supplies AuthorizeView / Cas… | `ta-outputs/ta_agent1/security-configuration-snapshot.md`; `ta-outputs/security-architecture-assessment.md`; `ta-outputs/ta_agent1/technology-stack-inventory.md` |
| TECH-SEC-005 | .NET User Secrets (local dev) | secrets |  | dotnet user-secrets used for local secret overrides. UserSecretsId present for Web (aspne… | `ta-outputs/ta_agent1/security-configuration-snapshot.md`; `ta-outputs/security-architecture-assessment.md` |
| TECH-SEC-006 | Azure Key Vault secrets integration (referenced) | secrets | Medium | Azure.Extensions.AspNetCore.Configuration.Secrets + Azure.Identity packages and AZURE_KEY… | `ta-outputs/ta_agent1/security-configuration-snapshot.md`; `ta-outputs/security-architecture-assessment.md` |
| TECH-SEC-007 | Docker-mounted host secrets (read-only bind mounts) | secrets |  | Read-only bind mounts ~/.aspnet/https:/root/.aspnet/https:ro (HTTPS dev certs) and ~/.mic… | `ta-outputs/ta_agent1/security-configuration-snapshot.md`; `ta-outputs/security-architecture-assessment.md` |
| TECH-SEC-008 | Hardcoded PostgreSQL credentials in source-controlled config | finding | Critical | Plaintext PostgreSQL credentials (Username=postgres;Password=Clarium123) committed to sou… | `ta-outputs/security-architecture-assessment.md`; `ta-outputs/ta_agent1/security-configuration-snapshot.md` |
| TECH-SEC-009 | Hardcoded SQL Server / Azure SQL Edge SA password in source-controlled config | finding | Critical | Plaintext SA password (SA_PASSWORD=@someThingComplicated1234) committed in docker-compose… | `ta-outputs/security-architecture-assessment.md` |
| TECH-SEC-010 | No JWT/authentication enforcement configured for PublicApi | finding | High | No confirmed JWT/authentication enforcement configuration for PublicApi despite it being… | `ta-outputs/security-architecture-assessment.md` |
| TECH-SEC-011 | No CORS policy found despite required cross-origin calls | finding | High | No CORS policy in any provided config file, yet BlazorAdmin calls PublicApi/Web from a di… | `ta-outputs/ta_agent1/security-configuration-snapshot.md`; `ta-outputs/security-architecture-assessment.md` |
| TECH-SEC-012 | No secret scanning in CI/CD | finding | High | No trufflehog/gitleaks/detect-secrets/git-secrets/ggshield step in either workflow; the t… | `ta-outputs/security-architecture-assessment.md`; `ta-outputs/operational-architecture-assessment.md` |
| TECH-SEC-013 | SQL Server port 1433 published directly to host network | finding | Medium | sqlserver container publishes 1433:1433 directly to the host with no network restriction.… | `ta-outputs/security-architecture-assessment.md` |
| TECH-SEC-014 | No TLS termination for Docker/container traffic | finding | Medium | Docker environment endpoints declared as plain HTTP (ASPNETCORE_URLS=http://+:8080); no T… | `ta-outputs/ta_agent1/infrastructure-deployment-blueprint.md`; `ta-outputs/ta_agent1/security-configuration-snapshot.md` |
| TECH-SEC-015 | AllowedHosts wildcard + TrustServerCertificate=true | finding | Medium | AllowedHosts set to '*' (all hosts) in Web and PublicApi appsettings.json - permissive ho… | `ta-outputs/ta_agent1/security-configuration-snapshot.md`; `ta-outputs/nfr-registry.md NFR-14` |
| TECH-SEC-016 | No SAST / dependency / container vulnerability scanning in CI/CD | finding | High | No SAST (sonar/codeql/semgrep/snyk), no in-pipeline dependency vulnerability scan (dotnet… | `ta-outputs/operational-architecture-assessment.md`; `ta-outputs/security-architecture-assessment.md` |
| TECH-SEC-017 | No audit logging / compliance controls (RBAC, GDPR, PCI, retention) found | finding | Medium | No audit logging configuration keys, data-retention settings, or compliance-related annot… | `ta-outputs/ta_agent1/security-configuration-snapshot.md` |

## Status Legend

Values below are surfaced exactly as the graph carries them on each node (`status`, `confidence`, `severity`).

| Marker | Meaning |
|--------|---------|
| `ACTIVE` | Node is part of the current canonical state of the system. |
| `INFERRED` | Node/attribute derived (e.g. ASP.NET Identity schema, generic Repository binding) rather than directly cited; treat with care. |
| confidence `HIGH` | Strongly evidence-grounded; multiple corroborating sources. |
| confidence `MEDIUM` | Single source or partial corroboration. |
| confidence `LOW` | Weak / assumption-backed link (see assumptions log). |
| confidence `0.xx` | Numeric confidence score carried on data / application / stack nodes. |
| severity `High` / `Medium` / `Low` | Security finding severity as recorded in the source assessment. |
| `*(synthetic)*` (APIs) | `method` value (ROUTE / CLI) is a normalized classification, not an extracted HTTP verb (see OQ-009). |

## Consolidation Note

The canonical graph is the result of de-duplicating overlapping source artifacts. The `normalization_log` records **15 canonicalization rules**, and the `assumptions` log records **7 merge / scoping assumptions**.

Duplicates merged (per `normalization_log`):

| canonical node | variants merged | rule |
|----------------|-----------------|------|
| Customer / Buyer (BIZ-ACT-001) | Customer; Buyer; Customer / Buyer | Collapse human storefront user variants to a single canonical actor; record originals. |
| Anonymous Shopper (BIZ-ACT-002) | anonymous user; anonymous shopper; anonymous session | Single canonical unauthenticated-visitor actor. |
| System / Service Account (BIZ-ACT-004) | System; System / Service Account; Seeder | Single canonical automated actor. |
| CatalogItem (DATA-ENT-001) | Catalog (table); Catalog Item; Product | Use the C# entity class name as canonical; table name and conceptual 'Product' recorded a… |
| CatalogBrand (DATA-ENT-002) | CatalogBrands (table); Catalog Brand; Brand | Entity class name canonical; table/conceptual names as aliases. |
| CatalogType (DATA-ENT-003) | CatalogTypes (table); Catalog Type; Category; Type | Entity class name canonical; table/conceptual 'Category' names as aliases. |
| ApplicationUser (DATA-ENT-008) | AspNetUsers (table); Customer; User | Entity/identity class canonical; table name + conceptual 'Customer'/'User' as aliases. |
| CatalogItemOrdered (DATA-ENT-012) | ItemOrdered (owned type) | Owned-type class name canonical; flattened column-prefix alias recorded. |
| Address (DATA-ENT-013) | ShipToAddress (owned type) | Owned-type class name canonical; ShipToAddress_* flattened alias recorded. |
| Web (APP-SVC-006) | MOD-013 Web; CAP-006 Controllers; eshopwebmvc | Merge module candidate + deployable runtime service of the same Web unit into one node. |
| PublicApi (APP-SVC-011) | MOD-010 PublicApi; eshoppublicapi | Merge module candidate + deployable runtime service eshoppublicapi. |
| ApplicationCore (APP-SVC-007) | MOD-002 ApplicationCore; CAP-008 Application; ApplicationCore (component) | Merge module candidate + class-library component. |
| Infrastructure (APP-SVC-009) | MOD-008 Infrastructure; Infrastructure (component) | Merge module candidate + class-library component. |
| SharedContracts (APP-SVC-012) | MOD-011 SharedContracts; BlazorShared | Merge module candidate SharedContracts with the BlazorShared class library it maps to. |
| Ardalis.Specification (+ EntityFrameworkCore evaluator) (TECH-CUR-009) | Ardalis.Specification; Ardalis.Specification.EntityFrameworkCore | The Ardalis.Specification.EntityFrameworkCore evaluator lives under the umbrella node TEC… |

Notable application-layer merges (module-candidate + deployable / component collapsed into one node), per assumptions ASSUMP-001..003:

- **Web** (`APP-SVC-006`) ← MOD-013 Web + deployable `eshopwebmvc` (ASSUMP-001)
- **PublicApi** (`APP-SVC-011`) ← MOD-010 PublicApi + deployable `eshoppublicapi` (ASSUMP-002)
- **ApplicationCore** (`APP-SVC-007`) ← MOD-002 + class-library component (ASSUMP-003)
- **Infrastructure** (`APP-SVC-009`) ← MOD-008 + class-library component (ASSUMP-003)
- **SharedContracts / BlazorShared** (`APP-SVC-012`) ← MOD-011 + BlazorShared library (ASSUMP-003)

In total, the 15 normalization rules collapse **38 source variant labels** into canonical nodes. Items deliberately **kept separate** pending human review are tracked as open questions (`OQ-001` Admin vs BlazorAdmin; `OQ-006` CatalogItem aggregate vs entity) — there are **9 open questions** total. Merged facets are preserved on each node's `merged_from` field so a reviewer can split them back out if needed.

