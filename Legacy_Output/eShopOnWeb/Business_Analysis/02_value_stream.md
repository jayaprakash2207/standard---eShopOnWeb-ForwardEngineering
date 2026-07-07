# Value Stream Map
## eShopOnWeb

### Value Stream: Customer Browse-to-Order

| Stage | Actor | Description | Value-Add |
|---|---|---|---|
| 1. Browse Catalog | Customer | Customer views available catalog items, filtering by brand or type | Yes |
| 2. Build Basket | Customer | Customer adds desired items to their basket; system consolidates duplicate items | Yes |
| 3. Authenticate (if needed) | Customer | Customer logs in; anonymous basket is transferred to their account | No |
| 4. Adjust Basket | Customer | Customer adjusts quantities or removes items before checkout | Yes |
| 5. Checkout | Customer | Customer initiates checkout; system validates basket is not empty | Yes |
| 6. Order Creation | System | System snapshots ordered item details and creates the order with shipping address | Yes |
| 7. Order Total Calculation | System | System calculates the total order value | Yes |

**Handoff Points:**
- Stage 1 -> Stage 2: Selected catalog item is handed to the basket-building process
- Stage 2 -> Stage 3: Basket contents (as anonymous session) are handed to the authentication process
- Stage 3 -> Stage 4: Merged basket is handed back to the customer for review
- Stage 4 -> Stage 5: Finalized basket is handed to the checkout process
- Stage 5 -> Stage 6: Validated basket contents are handed to order creation
- Stage 6 -> Stage 7: Created order is handed to the total calculation step

---

### Value Stream: Catalog Content Management

| Stage | Actor | Description | Value-Add |
|---|---|---|---|
| 1. Review Catalog | Administrator | Administrator views current catalog items, brands, and types | Yes |
| 2. Create/Update Item | Administrator | Administrator creates or updates a catalog item's details, brand, type, and image | Yes |
| 3. Validate Item Details | System | System rejects updates with missing name, description, invalid price, or invalid brand/type IDs | Yes |
| 4. Refresh Cache | System | System refreshes the locally cached catalog list so the admin UI reflects changes | No |

**Handoff Points:**
- Stage 1 -> Stage 2: Administrator selects an item to create or modify
- Stage 2 -> Stage 3: Submitted item details are handed to validation logic
- Stage 3 -> Stage 4: Validated changes are handed to the cache refresh process