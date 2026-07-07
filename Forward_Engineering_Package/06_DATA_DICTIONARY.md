# 06 — Data Dictionary

> ⚠️ **DISC-001 (verified 2026-06-25):** The `CatalogItem` attributes `AvailableStock`, `RestockThreshold`,
> `MaxStockThreshold`, `OnReorder` listed below are a **verified discrepancy** — absent from the real
> source (`eShopOnWeb` `main`, `CatalogItem.cs` has only Name, Description, Price, PictureUri,
> CatalogTypeId, CatalogBrandId). **Do not generate** these columns, any `CK_CatalogItem_Stock` constraint,
> or the derived reorder event. See [`../EVIDENCE_VERIFICATION_REPORT.md`](../EVIDENCE_VERIFICATION_REPORT.md).

> **Single source of truth:** `ENTERPRISE_KNOWLEDGE_GRAPH.json`. Every attribute, type, constraint, PII flag and ownership statement below is traced to graph node ids (`DATA-ENT-###`, `DATA-REL-###`, `DATA-AGG-###`, `DATA-REPO-###`, `APP-SVC-###`) and cross-links. No attributes, types or relationships have been invented.
>
> **Scope:** All 15 `DATA-ENT` entities, each with an attribute table. Logical data types are **technology-neutral** (Identifier, ShortText, LongText, Money/Decimal, Integer, Boolean, ImageURI, Timestamp, Enum). Where the graph records only `key_attributes`, the table is limited to those attributes and any unknowns are explicitly flagged as a gap.
>
> **Status flags honoured (HARD RULE):** `Buyer` (DATA-ENT-010) and `PaymentMethod` (DATA-ENT-011) are `persisted=false`, `status=aspirational/unimplemented` (RC-002) and are marked accordingly. `CatalogItemDetails` (DATA-ENT-014) is also `persisted=false`. `BaseEntity` (DATA-ENT-015) is `persisted=false` (abstract base, no table of its own).

---

## How to read the type and constraint columns

| Logical Data Type | Meaning (technology-neutral) |
|---|---|
| Identifier | Surrogate or natural key value; opaque, system-assigned. |
| ShortText | Bounded single-line text (name, label, code). |
| LongText | Unbounded / large free text (description). |
| Money/Decimal | Fixed-precision monetary or decimal amount. |
| Integer | Whole number (counts, quantities, thresholds, FKs to integer keys). |
| Boolean | True/false flag. |
| ImageURI | Reference (path/URL) to an image asset, not the binary. |
| Timestamp | Point in time (date + time). |
| Enum | Constrained set of named values. |

**PII** is taken directly from `entity.pii`. **Ownership** is the bounded context / owning service from the `entity_to_service` cross-links and the DDD aggregate (`DATA-AGG-###`) the entity belongs to.

**Owning-service map (from `entity_to_service` cross-links):**

| Bounded Context (owning service) | Entities (DATA-ENT) |
|---|---|
| Catalog — `APP-SVC-001` (also data-access adapter `APP-SVC-008`) | 001, 002, 003, 012, 014 |
| Basket — `APP-SVC-003` | 004, 005 |
| Order — `APP-SVC-004` | 006, 007, 013, 010, 011 |
| Identity — `APP-SVC-002` | 008, 009 |
| ApplicationCore (shared kernel) — `APP-SVC-007` | 015 |

---

## DATA-ENT-001 — CatalogItem

A product offered for sale, with name, description, price, image, brand and type classification, plus stock-management fields. Canonical source of truth for live product data. Aggregate root of `DATA-AGG-004` (CatalogItem). PII: **No**. Persisted: **Yes** (`status=implemented`, confidence 0.8).

| Attribute | Definition | Logical Data Type | Constraints | PII | Ownership |
|---|---|---|---|---|---|
| Id | Surrogate key uniquely identifying the catalog item | Identifier | PK; required | No | Catalog (`APP-SVC-001` / `APP-SVC-008`) |
| Name | Product display name | ShortText | required | No | Catalog (`APP-SVC-001`) |
| Description | Long-form product description | LongText | optional | No | Catalog (`APP-SVC-001`) |
| Price | Selling price of the product | Money/Decimal | required; Price >= 0 (non-negative monetary value — see ASMP-DD-001) | No | Catalog (`APP-SVC-001`) |
| PictureUri | Reference to the product image asset | ImageURI | optional | No | Catalog (`APP-SVC-001`) |
| CatalogTypeId | Classification (category) the product belongs to | Integer | FK -> CatalogType.Id (`DATA-REL-002`); required | No | Catalog (`APP-SVC-001`) |
| CatalogBrandId | Brand/label the product belongs to | Integer | FK -> CatalogBrand.Id (`DATA-REL-001`); required | No | Catalog (`APP-SVC-001`) |
| AvailableStock | Units currently available to sell | Integer | AvailableStock >= 0 (ASMP-DD-001) | No | Catalog (`APP-SVC-001`) |
| RestockThreshold | Stock level that triggers reorder | Integer | RestockThreshold >= 0; RestockThreshold <= MaxStockThreshold (ASMP-DD-001) | No | Catalog (`APP-SVC-001`) |
| MaxStockThreshold | Maximum stock the item may hold | Integer | MaxStockThreshold >= 0 (ASMP-DD-001) | No | Catalog (`APP-SVC-001`) |
| OnReorder | Whether the item is currently flagged for reorder | Boolean | required | No | Catalog (`APP-SVC-001`) |

Attributes are the full `key_attributes` set per evidence. Stock-threshold range constraints (`>= 0`, `Restock <= Max`) are asserted under **ASMP-DD-001** (the graph names the fields but does not record numeric ranges).

---

## DATA-ENT-002 — CatalogBrand

A manufacturer or label that groups products together (e.g. "Adventure Works"). PII: **No**. Persisted: **Yes** (`status=implemented`).

| Attribute | Definition | Logical Data Type | Constraints | PII | Ownership |
|---|---|---|---|---|---|
| Id | Surrogate key of the brand | Identifier | PK; required | No | Catalog (`APP-SVC-001`) |
| Brand | Brand / label display name | ShortText | required | No | Catalog (`APP-SVC-001`) |

Attributes are the full `key_attributes` set per evidence. Referenced by CatalogItem via `DATA-REL-001`.

---

## DATA-ENT-003 — CatalogType

A classification grouping products by type/category (e.g. Mugs, T-Shirts, Stickers). PII: **No**. Persisted: **Yes** (`status=implemented`).

| Attribute | Definition | Logical Data Type | Constraints | PII | Ownership |
|---|---|---|---|---|---|
| Id | Surrogate key of the type/category | Identifier | PK; required | No | Catalog (`APP-SVC-001`) |
| Type | Category / type display name | ShortText | required | No | Catalog (`APP-SVC-001`) |

Attributes are the full `key_attributes` set per evidence. Referenced by CatalogItem via `DATA-REL-002`.

---

## DATA-ENT-004 — Basket

A temporary collection of products a customer intends to purchase; belongs to one customer, keyed by BuyerId (soft, cross-database reference to ApplicationUser.Id, realised as the `AspNetUsers.Id` column per the INFERRED ASP.NET Core Identity schema, confidence 0.7). Aggregate root of `DATA-AGG-001` (BasketAggregate). PII: **No**. Persisted: **Yes** (`status=implemented`).

| Attribute | Definition | Logical Data Type | Constraints | PII | Ownership |
|---|---|---|---|---|---|
| Id | Surrogate key of the basket | Identifier | PK; required | No | Basket (`APP-SVC-003`) |
| BuyerId | Owner of the basket | Identifier | Soft (app-enforced) cross-database reference to ApplicationUser.Id, realised as the `AspNetUsers.Id` column (INFERRED Identity schema, confidence 0.7) (`DATA-REL-008`); no DB-level FK; required | No | Basket (`APP-SVC-003`) |

Attributes are the full `key_attributes` set per evidence. `BuyerId` itself is not flagged PII at entity level; the entity owns child `BasketItem` records (`DATA-REL-003`).

> **Note (gap):** `BuyerId` is an unenforced cross-database link (`DATA-REL-008`, confidence 0.8) from CatalogDb to the IdentityDb `AspNetUsers.Id` column. Referential integrity is application-enforced only — see **ASMP-DD-002**. (No open question on cross-database BuyerId/identity ownership exists in the graph; none is asserted here.)

---

## DATA-ENT-005 — BasketItem

A single line in a basket referencing a CatalogItem, with unit price captured at time of adding and a quantity. Member of `DATA-AGG-001` (BasketAggregate). PII: **No**. Persisted: **Yes** (`status=implemented`).

| Attribute | Definition | Logical Data Type | Constraints | PII | Ownership |
|---|---|---|---|---|---|
| Id | Surrogate key of the basket line | Identifier | PK; required | No | Basket (`APP-SVC-003`) |
| BasketId | Parent basket this line belongs to | Integer | FK -> Basket.Id (`DATA-REL-003`); required | No | Basket (`APP-SVC-003`) |
| CatalogItemId | Catalog product this line references | Integer | FK -> CatalogItem.Id (`DATA-REL-004`); required | No | Basket (`APP-SVC-003`) |
| UnitPrice | Price per unit captured at time of adding | Money/Decimal | UnitPrice >= 0 (ASMP-DD-001) | No | Basket (`APP-SVC-003`) |
| Quantity | Number of units of the catalog item in this line | Integer | Quantity >= 0 (basket cleanup removes zero-quantity lines per BIZ-CAP-014; ASMP-DD-001) | No | Basket (`APP-SVC-003`) |

Attributes are the full `key_attributes` set per evidence.

---

## DATA-ENT-006 — Order

A confirmed purchase made by a customer; records OrderDate, a flattened owned-type shipping Address, and BuyerId (soft cross-database reference to ApplicationUser.Id, realised as the `AspNetUsers.Id` column per the INFERRED ASP.NET Core Identity schema, confidence 0.7). Aggregate root of `DATA-AGG-002` (OrderAggregate). PII: **Yes**. Persisted: **Yes** (`status=implemented`).

| Attribute | Definition | Logical Data Type | Constraints | PII | Ownership |
|---|---|---|---|---|---|
| Id | Surrogate key of the order | Identifier | PK; required | No | Order (`APP-SVC-004`) |
| BuyerId | Customer who placed the order | Identifier | Soft (app-enforced) cross-database reference to ApplicationUser.Id, realised as the `AspNetUsers.Id` column (INFERRED Identity schema, confidence 0.7) (`DATA-REL-009`); no DB-level FK; required | Yes (links to an identifiable person) | Order (`APP-SVC-004`) |
| OrderDate | Date/time the order was placed | Timestamp | required | No | Order (`APP-SVC-004`) |
| ShipToAddress_Street | Street line of the shipping address | ShortText | required; owned-type Address column (`DATA-REL-007`) | Yes | Order (`APP-SVC-004`) |
| ShipToAddress_City | City of the shipping address | ShortText | required; owned-type Address column | Yes | Order (`APP-SVC-004`) |
| ShipToAddress_State | State/region of the shipping address | ShortText | optional; owned-type Address column | Yes | Order (`APP-SVC-004`) |
| ShipToAddress_Country | Country of the shipping address | ShortText | required; owned-type Address column | Yes | Order (`APP-SVC-004`) |
| ShipToAddress_ZipCode | Postal/zip code of the shipping address | ShortText | required; owned-type Address column | Yes | Order (`APP-SVC-004`) |

Attributes are the full `key_attributes` set per evidence. The `ShipToAddress_*` columns are the **flattened owned-type Address** (`DATA-ENT-013`, `DATA-REL-007`); they are catalogued here because they physically reside on the Orders table and are PII-bearing. The entity owns child `OrderItem` records (`DATA-REL-005`).

---

## DATA-ENT-007 — OrderItem

A single purchased line within an order. Embeds a `CatalogItemOrdered` owned-type snapshot of the catalog item at time of order, plus UnitPrice and Units. Snapshot is intentional historical denormalization, not a live FK. Member of `DATA-AGG-002` (OrderAggregate). PII: **No**. Persisted: **Yes** (`status=implemented`).

| Attribute | Definition | Logical Data Type | Constraints | PII | Ownership |
|---|---|---|---|---|---|
| Id | Surrogate key of the order line | Identifier | PK; required | No | Order (`APP-SVC-004`) |
| OrderId | Parent order this line belongs to | Integer | FK -> Order.Id (`DATA-REL-005`); required | No | Order (`APP-SVC-004`) |
| ItemOrdered_CatalogItemId | Snapshot of the catalog item id at time of order | Integer | owned-type CatalogItemOrdered column (`DATA-REL-006`); **snapshot, not a live FK** | No | Order (`APP-SVC-004`) |
| ItemOrdered_ProductName | Snapshot of the product name at time of order | ShortText | owned-type CatalogItemOrdered column; required | No | Order (`APP-SVC-004`) |
| ItemOrdered_PictureUri | Snapshot of the product image reference at time of order | ImageURI | owned-type CatalogItemOrdered column; optional | No | Order (`APP-SVC-004`) |
| UnitPrice | Price per unit captured at time of order | Money/Decimal | UnitPrice >= 0 (ASMP-DD-001) | No | Order (`APP-SVC-004`) |
| Units | Number of units ordered for this line | Integer | Units >= 1 (ASMP-DD-001) | No | Order (`APP-SVC-004`) |

Attributes are the full `key_attributes` set per evidence. The `ItemOrdered_*` columns are the **flattened owned-type CatalogItemOrdered** (`DATA-ENT-012`, `DATA-REL-006`) — an intentional point-in-time snapshot, deliberately decoupled from live CatalogItem data.

---

## DATA-ENT-008 — ApplicationUser

The identity/account of a customer or staff member (login credentials, email, roles). Canonical source of truth for identity. IdentityDb schema is **INFERRED** standard ASP.NET Core Identity (confidence 0.7). PII: **Yes**. Persisted: **Yes** (`status=implemented`).

| Attribute | Definition | Logical Data Type | Constraints | PII | Ownership |
|---|---|---|---|---|---|
| Id | Surrogate key of the user/account | Identifier | PK; required | Yes | Identity (`APP-SVC-002`) |
| UserName | Login user name | ShortText | required; unique (ASMP-DD-003) | Yes | Identity (`APP-SVC-002`) |
| Email | User email address | ShortText | required; unique (ASMP-DD-003) | Yes | Identity (`APP-SVC-002`) |
| PasswordHash | Hashed password credential (never plaintext) | ShortText | required; security-sensitive | Yes | Identity (`APP-SVC-002`) |
| PhoneNumber | User phone number | ShortText | optional | Yes | Identity (`APP-SVC-002`) |

> **Inference flag (gap):** The IdentityDb schema is INFERRED standard ASP.NET Core Identity (confidence 0.7). The listed attributes are per evidence; **additional standard Identity fields (e.g. security stamps, lockout, two-factor) are unknown / not catalogued** — see ASMP-DD-003. Uniqueness of `UserName`/`Email` is asserted under ASMP-DD-003 as standard Identity behaviour, not explicitly recorded in the graph.

---

## DATA-ENT-009 — Role

A role assigned to users governing system access; confirmed role name "Administrators" (RC-008). IdentityDb schema is **INFERRED** standard ASP.NET Core Identity (confidence 0.7). PII: **No**. Persisted: **Yes** (`status=implemented`).

| Attribute | Definition | Logical Data Type | Constraints | PII | Ownership |
|---|---|---|---|---|---|
| Id | Surrogate key of the role | Identifier | PK; required | No | Identity (`APP-SVC-002`) |
| Name | Role name (e.g. "Administrators") | ShortText | required; unique (ASMP-DD-003) | No | Identity (`APP-SVC-002`) |

Attributes are the full `key_attributes` set per evidence. Associated to ApplicationUser many-to-many via the inferred `AspNetUserRoles` join (`DATA-REL-010`, confidence 0.7).

---

## DATA-ENT-010 — Buyer  *(ASPIRATIONAL / UNIMPLEMENTED)*

Aspirational customer aggregate that would store payment methods. **CONFIRMED dead/unmapped code (RC-002):** not a DbSet on CatalogContext, no EF configuration, no repository usage. PII: **No**. Persisted: **No** (`status=aspirational/unimplemented`, confidence 0.9). Aspirational aggregate root of `DATA-AGG-003` (BuyerAggregate, also aspirational).

| Attribute | Definition | Logical Data Type | Constraints | PII | Ownership |
|---|---|---|---|---|---|
| *(none recorded)* | No `key_attributes` are recorded in the graph for this aspirational entity | — | — | No | Order context (`APP-SVC-004`) per `entity_to_service` — **aspirational only** |

> **ASPIRATIONAL / UNIMPLEMENTED (RC-002):** No attributes are recorded; the entity has no persisted schema, no table, no checkout flow backing it. Any attribute set is **unknown** and must not be assumed. If a future target design re-introduces a Buyer aggregate, attributes would need to be defined fresh — flagged as a gap (see ASMP-DD-004). Aspirational relationship to PaymentMethod: `DATA-REL-012` (1..*).

---

## DATA-ENT-011 — PaymentMethod  *(ASPIRATIONAL / UNIMPLEMENTED)*

A way for a customer to pay, associated with a Buyer. **CONFIRMED dead/unmapped code (RC-002):** exists only as a class referenced from Buyer; no DbSet / EntityTypeConfiguration / repository. PII: **No** (per `entity.pii`). Persisted: **No** (`status=aspirational/unimplemented`, confidence 0.9). **Not currently in PCI-DSS scope.**

| Attribute | Definition | Logical Data Type | Constraints | PII | Ownership |
|---|---|---|---|---|---|
| *(none recorded)* | No `key_attributes` are recorded in the graph for this aspirational entity | — | — | No | Order context (`APP-SVC-004`) per `entity_to_service` — **aspirational only** |

> **ASPIRATIONAL / UNIMPLEMENTED (RC-002):** No attributes are recorded; the entity is dead/unmapped code. Attribute set is **unknown** — flagged as a gap (see ASMP-DD-004). **Caution:** if a future target design implements real payment data, PII / PCI-DSS classification would change materially; the current `pii=false` reflects the *unimplemented* state only and must be re-assessed before any implementation.

---

## DATA-ENT-012 — CatalogItemOrdered

Owned/value type embedded into the OrderItems table — an intentional historical **snapshot** of CatalogItem (id, product name, picture) at time of order. Not its own table. Member of `DATA-AGG-002` (OrderAggregate). PII: **No**. Persisted: **Yes** (embedded; `status=implemented`, confidence 0.78).

| Attribute | Definition | Logical Data Type | Constraints | PII | Ownership |
|---|---|---|---|---|---|
| ItemOrdered_CatalogItemId | Snapshot of the catalog item id at time of order | Integer | embedded owned-type column on OrderItems; **snapshot, not a live FK** (`DATA-REL-006`) | No | Order (`APP-SVC-004`) — modelled in Catalog context per `entity_to_service` (`APP-SVC-001`) |
| ItemOrdered_ProductName | Snapshot of the product name at time of order | ShortText | embedded owned-type column; required | No | Order (`APP-SVC-004`) |
| ItemOrdered_PictureUri | Snapshot of the product image reference at time of order | ImageURI | embedded owned-type column; optional | No | Order (`APP-SVC-004`) |

Attributes are the full `key_attributes` set per evidence. This is a value object: it has no independent identity/PK and is co-located with `OrderItem` (`DATA-ENT-007`). Ownership note: `entity_to_service` links it to Catalog (`APP-SVC-001`) as the conceptual origin, but it is physically persisted and managed within the Order aggregate.

---

## DATA-ENT-013 — Address

Owned/value type embedded (flattened) into the Orders table as `ShipToAddress_*` columns. Not its own table. Member of `DATA-AGG-002` (OrderAggregate). PII: **Yes**. Persisted: **Yes** (embedded; `status=implemented`, confidence 0.75).

| Attribute | Definition | Logical Data Type | Constraints | PII | Ownership |
|---|---|---|---|---|---|
| ShipToAddress_Street | Street line of the shipping address | ShortText | embedded owned-type column on Orders; required | Yes | Order (`APP-SVC-004`) |
| ShipToAddress_City | City of the shipping address | ShortText | embedded owned-type column; required | Yes | Order (`APP-SVC-004`) |
| ShipToAddress_State | State/region of the shipping address | ShortText | embedded owned-type column; optional | Yes | Order (`APP-SVC-004`) |
| ShipToAddress_Country | Country of the shipping address | ShortText | embedded owned-type column; required | Yes | Order (`APP-SVC-004`) |
| ShipToAddress_ZipCode | Postal/zip code of the shipping address | ShortText | embedded owned-type column; required | Yes | Order (`APP-SVC-004`) |

Attributes are the full `key_attributes` set per evidence. This is a value object with no independent identity/PK; the same fields are catalogued on `DATA-ENT-006` (Order) because they physically reside on the Orders table.

---

## DATA-ENT-014 — CatalogItemDetails  *(NON-PERSISTED DTO / VALUE OBJECT)*

A struct co-located with CatalogItem; likely a non-persisted DTO/projection/value object (read-model), not its own table. PII: **No**. Persisted: **No** (`status=aspirational/unimplemented`, confidence 0.72).

| Attribute | Definition | Logical Data Type | Constraints | PII | Ownership |
|---|---|---|---|---|---|
| *(none recorded)* | No `key_attributes` are recorded in the graph for this struct/DTO | — | — | No | Catalog (`APP-SVC-001`) |

> **Gap:** No attributes are recorded. The entity is a likely read-model/DTO/value object, **not independently persisted (to be confirmed)**. Attribute set is **unknown** — flagged as a gap (see ASMP-DD-005). It carries no table and no PK of its own.

---

## DATA-ENT-015 — BaseEntity  *(ABSTRACT BASE — NON-PERSISTED)*

Abstract base class providing the `Id` property to entities. Not its own table (no persistence on its own). PII: **No**. Persisted: **No** (`status=implemented` as a code construct, but `persisted=false`). Owned by the shared kernel ApplicationCore (`APP-SVC-007`).

| Attribute | Definition | Logical Data Type | Constraints | PII | Ownership |
|---|---|---|---|---|---|
| Id | Surrogate identity inherited by all derived entities | Identifier | PK on the **derived** entity; required | No | ApplicationCore shared kernel (`APP-SVC-007`) |

Attributes are the full `key_attributes` set per evidence. `BaseEntity` itself maps to no table; the `Id` is realised as the primary key on each concrete persisted entity that inherits it.

---

## Cross-entity glossary of shared terms

Terms that recur across multiple entities, with their canonical meaning and the node ids where they appear. Use this to resolve naming overlaps consistently.

| Term | Canonical meaning | Logical Data Type | Where it appears (DATA-ENT / DATA-REL) | Notes |
|---|---|---|---|---|
| **Id** | System-assigned surrogate primary key of an entity. | Identifier | All persisted entities (001–009, 012*, 013*) inherit it via BaseEntity (015). | `*` = owned types persist the value within the parent table, not as a standalone PK. |
| **BuyerId** | Identifier of the customer who owns a basket/order. | Identifier | Basket (004), Order (006); relationships `DATA-REL-008`, `DATA-REL-009`. | **Soft, app-enforced, cross-database** reference to ApplicationUser.Id (008), realised as the `AspNetUsers.Id` column per the INFERRED Identity schema (confidence 0.7) — no DB-level FK. PII-bearing on Order (006). |
| **CatalogItemId** | Identifier of a catalog product. | Integer | Live FK on BasketItem (005, `DATA-REL-004`); snapshot value `ItemOrdered_CatalogItemId` on OrderItem (007) / CatalogItemOrdered (012, `DATA-REL-006`). | On the order side it is a historical **snapshot, not a live FK** — do not join to live Catalog. |
| **UnitPrice** | Price per single unit, captured at a point in time. | Money/Decimal | BasketItem (005), OrderItem (007). | Captured at add-to-basket / order time; may differ from current CatalogItem.Price (001). |
| **Price** | Current selling price of a catalog product. | Money/Decimal | CatalogItem (001). | Distinct from the captured `UnitPrice` above. |
| **Quantity / Units** | Count of units. | Integer | `Quantity` on BasketItem (005); `Units` on OrderItem (007). | Same concept, different attribute names across basket vs. order contexts. |
| **PictureUri** | Reference (path/URL) to a product image asset. | ImageURI | CatalogItem (001); snapshot `ItemOrdered_PictureUri` on OrderItem (007) / CatalogItemOrdered (012). | Stores a reference, not the image binary. |
| **Name** | Human-readable label. | ShortText | `Name` on CatalogItem (001) and Role (009); `Brand` on CatalogBrand (002); `Type` on CatalogType (003); `ProductName` snapshot on OrderItem (007)/012; `UserName` on ApplicationUser (008). | Context-specific labels; not a single shared attribute. |
| **ShipToAddress_** prefix | Flattened columns of the owned-type Address value object. | ShortText | Order (006) and Address (013), via `DATA-REL-007`. | PII-bearing; physically on the Orders table, conceptually the Address value object. |
| **ItemOrdered_** prefix | Flattened columns of the owned-type CatalogItemOrdered snapshot. | mixed (Integer/ShortText/ImageURI) | OrderItem (007) and CatalogItemOrdered (012), via `DATA-REL-006`. | Intentional historical denormalization. |
| **BasketId / OrderId** | FK to the parent aggregate root. | Integer | BasketItem.BasketId -> Basket (`DATA-REL-003`); OrderItem.OrderId -> Order (`DATA-REL-005`). | Hard, in-database foreign keys (intra-aggregate). |
| **CatalogTypeId / CatalogBrandId** | FK from a product to its classification/brand. | Integer | CatalogItem (001) -> CatalogType (`DATA-REL-002`) / CatalogBrand (`DATA-REL-001`). | Hard, in-database foreign keys. |
| **PII** | Personally identifiable information flag. | Boolean (metadata) | True for Order (006), ApplicationUser (008), Address (013). | Per `entity.pii`. PaymentMethod (011) is currently `pii=false` **only because unimplemented** — re-assess before implementation. |

---

## Data classification summary (PII)

| PII = Yes | PII = No |
|---|---|
| Order (006), ApplicationUser (008), Address (013) | CatalogItem (001), CatalogBrand (002), CatalogType (003), Basket (004), BasketItem (005), OrderItem (007), Role (009), Buyer (010)*, PaymentMethod (011)*, CatalogItemOrdered (012), CatalogItemDetails (014)*, BaseEntity (015) |

`*` = aspirational/unimplemented or non-persisted; classification reflects current state and must be re-assessed if implemented. PaymentMethod (011) in particular would likely become PII / PCI-DSS scope once real payment data is stored.

---

## Assumptions added (data-dictionary local — `ASMP-DD-###` namespace)

> **Namespace note:** These assumptions use the document-local `ASMP-DD-###` namespace to avoid collision with the shared `ASMP-FE-###` registry in `.work/DECISIONS.json`, which defines `ASMP-FE-001..004` with entirely different meanings (Money VO non-derivable; StockReorderTriggered EVT-12 inferred; Buyer/Customer Profile BC-06 aspirational; routes attributed to functional BCs). Each `ASMP-FE-###` id therefore has exactly one definition across the package; the data-dictionary's own attribute-level assumptions are numbered separately below.

| ID | Assumption | Basis | Impact if wrong |
|---|---|---|---|
| ASMP-DD-001 | Numeric range constraints are applied to quantity/stock/price/monetary fields: `Quantity >= 0`, `Units >= 1`, `Price/UnitPrice >= 0`, stock thresholds `>= 0` with `RestockThreshold <= MaxStockThreshold`, `AvailableStock >= 0`. | The graph names these fields (DATA-ENT-001/005/007) and Basket Cleanup (BIZ-CAP-014) removes zero-quantity lines, but records no explicit numeric ranges. Standard e-commerce domain rules. | Target schema validation rules and check constraints would be mis-specified; could allow negative stock/price or invalid thresholds. |
| ASMP-DD-002 | The `BuyerId` link from Basket (004) and Order (006) targets ApplicationUser.Id (008) — realised as the `AspNetUsers.Id` column per the INFERRED Identity schema — and is enforced only in application code, not at the database level. | `DATA-REL-008` / `DATA-REL-009` are `implemented-soft-reference`, cross-database (CatalogDb -> IdentityDb `AspNetUsers.Id`), confidence 0.8; no DB FK recorded. | If a hard FK is expected, migration/integrity design (e.g. consolidating identity and catalog data stores) would differ. |
| ASMP-DD-003 | ApplicationUser (008) and Role (009) follow standard ASP.NET Core Identity semantics: `UserName`/`Email`/role `Name` are unique, and additional standard Identity columns exist beyond those listed. | Entity descriptions state the IdentityDb schema is INFERRED standard ASP.NET Core Identity (confidence 0.7). Listed `key_attributes` are a subset. | A target identity store designed only from listed attributes would omit required Identity fields (security stamp, lockout, 2FA, concurrency stamp). |
| ASMP-DD-004 | Buyer (010) and PaymentMethod (011) have **no defined attribute set** and must be designed fresh if ever implemented; current `pii=false` for PaymentMethod is provisional. | `key_attributes=[]`, `persisted=false`, `status=aspirational/unimplemented`, RC-002 confirmed dead code (confidence 0.9). | Treating these as ready entities would fabricate schema and mis-classify future PII / PCI-DSS scope. |
| ASMP-DD-005 | CatalogItemDetails (014) is a non-persisted read-model/DTO/value object with no table and no defined attributes. | `persisted=false`, `key_attributes=[]`, confidence 0.72; described as struct "likely a value object/DTO". | Mistakenly persisting it would create a redundant/shadow table. |

---

## Gaps flagged

- **Stock/price/quantity ranges (ASMP-DD-001):** the graph records the fields but no numeric range constraints; ranges asserted as assumptions.
- **ApplicationUser / Role schema is INFERRED (confidence 0.7):** listed attributes are a subset of standard ASP.NET Core Identity; **additional fields unknown** for both DATA-ENT-008 and DATA-ENT-009.
- **Buyer (010) and PaymentMethod (011) attributes are unknown** — `key_attributes=[]`, aspirational/unimplemented (RC-002). No schema may be assumed.
- **CatalogItemDetails (014) attributes are unknown** — non-persisted DTO/value object, `key_attributes=[]`.
- **Cross-database `BuyerId` integrity is application-enforced only** (DATA-REL-008/009, confidence 0.8) — not a DB-level FK.
- **PaymentMethod PII/PCI-DSS classification is provisional** — currently `pii=false` only because unimplemented; must be re-assessed before any implementation.
