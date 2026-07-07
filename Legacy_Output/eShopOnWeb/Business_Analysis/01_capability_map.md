# Business Capability Map
## eShopOnWeb

> Extracted from legacy codebase. Status: Active/Dormant per code evidence.

### L1: Catalog Management
#### L2: Product Information Management
- **L3: Catalog Item Details Maintenance** — Maintain product name, description, price, and image for items in the store catalog `[ACTIVE]`
- **L3: Product Classification** — Assign products to a brand and a type for organization and filtering `[ACTIVE]`
- **L3: Product Image Management** — Generate and maintain image paths for product pictures `[ACTIVE]`

#### L2: Catalog Reference Data
- **L3: Brand Management** — Maintain the list of manufacturers/brands available for product classification `[ACTIVE]`
- **L3: Type Management** — Maintain the list of product categories/types `[ACTIVE]`
- **L3: Catalog Seeding** — Populate initial catalog data on system startup `[ACTIVE]`

### L1: Basket / Shopping Cart Management
#### L2: Basket Maintenance
- **L3: Add Item to Basket** — Add a product to a customer's basket, consolidating quantity if already present `[ACTIVE]`
- **L3: Quantity Adjustment** — Adjust the quantity of an item in the basket, preventing negative values `[ACTIVE]`
- **L3: Basket Cleanup** — Remove basket lines that have a zero quantity `[ACTIVE]`

#### L2: Session Continuity
- **L3: Anonymous-to-Registered Basket Transfer** — Merge an anonymous shopper's basket into their account basket upon login `[ACTIVE]`

### L1: Order Management
#### L2: Order Creation
- **L3: Checkout Processing** — Convert a customer's basket into a confirmed order `[ACTIVE]`
- **L3: Empty Basket Protection** — Prevent checkout when the basket contains no items `[ACTIVE]`
- **L3: Ordered Item Snapshot** — Capture product name, picture, and price at the time of order `[ACTIVE]`

#### L2: Order Calculation
- **L3: Order Total Calculation** — Calculate the order total from item prices and quantities `[ACTIVE]`

### L1: Buyer / Customer Profile Management
#### L2: Buyer Identity
- **L3: Buyer Record Creation** — Create a buyer record linked to a valid identity account `[ACTIVE]`

#### L2: Payment Information
- **L3: Payment Method Management** — Associate payment methods with a buyer `[ACTIVE - inferred from data model]`

### L1: Identity & Authentication
#### L2: Access Control
- **L3: User Login** — Validate user credentials and report lockout/permission status `[ACTIVE]`
- **L3: Token Issuance** — Generate signed JWT tokens containing identity and role claims `[ACTIVE]`

#### L2: Identity Seeding
- **L3: Identity Data Seeding** — Populate initial user accounts and roles on startup `[ACTIVE]`

### L1: Admin Catalog Operations (Blazor)
#### L2: Administrative Catalog Interface
- **L3: Catalog Item List View** — Display catalog items, types, and brands to administrators `[ACTIVE]`
- **L3: Catalog Item Create/Delete** — Allow administrators to create or remove catalog items `[ACTIVE]`
- **L3: Cached Data Refresh** — Refresh locally cached catalog lists after changes `[ACTIVE]`

---
**Summary**
| Level | Count |
|---|---|
| L1 Capabilities | 6 |
| L2 Sub-Capabilities | 12 |
| L3 Functions | 20 |