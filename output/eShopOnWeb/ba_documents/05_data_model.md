# Information / Data Model
## eShopOnWeb

### Core Entities

#### Catalog Item
- **Business Definition:** A product available for purchase in the store catalog, including its name, description, price, image, brand, and type classification
- **Key Attributes:** Identifier, Name, Description, Price, Picture (image path), Brand reference, Type reference
- **States/Lifecycle:** No formal lifecycle identified (inferred: items are created, updated, and may be removed by administrators)
- **Relationships:**
  - Belongs to Catalog Brand
  - Belongs to Catalog Type
  - Referenced by Basket Item
  - Referenced by Catalog Item Ordered (order-time snapshot)
- **Business Rules:** BR001, BR002, BR003, BR004

#### Catalog Type
- **Business Definition:** A classification or category of catalog items, used to organize products (e.g., product category)
- **Key Attributes:** Identifier, Type Name
- **States/Lifecycle:** None identified
- **Relationships:**
  - Categorizes Catalog Item
- **Business Rules:** BR003

#### Catalog Brand
- **Business Definition:** The manufacturer or brand associated with a catalog item
- **Key Attributes:** Identifier, Brand Name
- **States/Lifecycle:** None identified
- **Relationships:**
  - Provides branding for Catalog Item
- **Business Rules:** BR002

#### Basket
- **Business Definition:** A shopping cart that holds items a buyer intends to purchase, either as an anonymous or registered user
- **Key Attributes:** Identifier, Buyer reference, list of Basket Items
- **States/Lifecycle:** Anonymous -> Transferred to Registered User -> Converted to Order
- **Relationships:**
  - Belongs to Buyer
  - Contains Basket Items
  - Converted into an Order
- **Business Rules:** BR005, BR006, BR012

#### Basket Item
- **Business Definition:** A single line item in a shopping basket representing a quantity of a catalog item at a given price
- **Key Attributes:** Identifier, Catalog Item reference, Unit Price, Quantity
- **States/Lifecycle:** Added -> Quantity Adjusted -> Removed (when quantity reaches zero)
- **Relationships:**
  - Belongs to Basket
  - References Catalog Item
- **Business Rules:** BR005, BR006, BR007

#### Buyer
- **Business Definition:** A registered customer who places orders and stores payment methods, identified by their identity provider account
- **Key Attributes:** Identifier, Identity reference, Payment Methods
- **States/Lifecycle:** None identified
- **Relationships:**
  - Owns Basket
  - Places Order
  - Has Payment Method(s)
- **Business Rules:** BR008

#### Order
- **Business Definition:** A confirmed purchase placed by a buyer, containing ordered items and a shipping address
- **Key Attributes:** Identifier, Buyer reference, Shipping Address, Order Items, Total (calculated)
- **States/Lifecycle:** Created from Basket -> Total Calculated (no further lifecycle states identified)
- **Relationships:**
  - Belongs to Buyer
  - Contains Order Items
  - Created from Basket
  - Ships to an Address
- **Business Rules:** BR010, BR011, BR012

#### Order Item
- **Business Definition:** A single purchased line within an order, capturing the ordered catalog item, its price at time of purchase, and quantity
- **Key Attributes:** Identifier, Item Ordered (snapshot reference), Unit Price, Units (quantity)
- **States/Lifecycle:** None identified
- **Relationships:**
  - Belongs to Order
  - References Catalog Item Ordered (a point-in-time snapshot of the Catalog Item)
- **Business Rules:** BR009, BR010

---
### Entity Relationship Summary
| Entity | Relates To | Relationship Type |
|---|---|---|
| Catalog Item | Catalog Brand | Belongs to (many-to-one) |
| Catalog Item | Catalog Type | Belongs to (many-to-one) |
| Basket Item | Catalog Item | References (many-to-one) |
| Basket | Basket Item | Contains (one-to-many) |
| Basket | Buyer | Belongs to (many-to-one) |
| Order | Buyer | Belongs to (many-to-one) |
| Order | Order Item | Contains (one-to-many) |
| Order Item | Catalog Item (snapshot) | References (many-to-one) |
| Basket | Order | Converted into (one-to-one, at checkout) |