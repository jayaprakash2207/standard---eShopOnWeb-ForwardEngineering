# Business Motivation Model
## eShopOnWeb

> INFERRED from code analysis — requires business validation

### Mission (inferred)
eShopOnWeb exists to provide an online storefront where customers can browse a catalog of products organized by brand and type, build a shopping basket (as anonymous or registered users), and complete purchases through a checkout process that produces a confirmed order with an accurate total and shipping destination. The system also provides administrators with tools to maintain the product catalog and supports secure, role-based access for both customers and staff.

### Business Drivers (inferred)
- **Frictionless Shopping Experience:** Evidence — basket consolidation logic (BR005) and anonymous-to-registered basket transfer process ensure customers don't lose cart contents or end up with duplicate lines
- **Data Integrity for Transactions:** Evidence — multiple validation rules (BR008, BR009, BR011) prevent orders or buyers from being created with missing critical references
- **Accurate Order Pricing:** Evidence — order-time snapshot of item details (Catalog Item Ordered) and total calculation (BR010) ensure price changes after purchase don't retroactively affect existing orders
- **Catalog Quality Control:** Evidence — validation on catalog item name, description, price, brand, and type (BR001-BR003) prevents incomplete product listings
- **Secure, Role-Based Access:** Evidence — Identity & Authentication capability issues JWT tokens with role claims for differentiated Customer/Administrator access

### Goals (inferred from processes)
| Goal | Evidence | Process |
|---|---|---|
| Ensure customers never lose basket contents when logging in | Anonymous-to-registered basket merge logic | Transfer Anonymous Basket to Registered User |
| Prevent invalid or empty orders from being created | BR011, BR012 guard checks | Checkout / Place Order |
| Maintain a clean, accurate product catalog | BR001-BR004 validation on catalog item fields | Catalog Item Administration |
| Provide secure access differentiated by role | JWT token issuance with role claims | User Authentication |

### Constraints (extracted from rules)
| Constraint | Source Rule | Business Impact |
|---|---|---|
| Catalog items must have a name, description, and positive price | BR001 | Prevents publishing incomplete or free/negative-priced products |
| Catalog items must reference a valid brand and type | BR002, BR003 | Ensures every product is classifiable for browsing/filtering |
| Basket item quantities cannot go negative | BR007 | Prevents invalid basket states that could affect order totals |
| Orders cannot be created without a buyer or with incomplete line items | BR008, BR009, BR011 | Ensures every order is traceable to a valid customer with complete product detail |
| Checkout is blocked for empty baskets | BR012 | Prevents creation of zero-value or meaningless orders |