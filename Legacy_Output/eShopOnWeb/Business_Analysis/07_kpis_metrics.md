# KPIs & Metrics
## eShopOnWeb

### Operational Metrics (extracted from code/config)
| Metric | Source | Current Threshold | Business Meaning |
|---|---|---|---|
| Minimum catalog item price | BR001 | Greater than zero | Ensures no product can be sold or listed at zero/negative price |
| Minimum basket item quantity | BR007 | Zero (cannot go negative) | Ensures basket quantities never become invalid |
| Minimum basket size for checkout | BR012 | At least 1 item | Ensures no orders are created from empty baskets |

### Process Metrics
| Process | Metric | How Measured |
|---|---|---|
| Add Item to Basket | Basket consolidation rate | Proportion of "add item" actions that increase an existing line vs. create a new line (BR005) |
| Checkout / Place Order | Order total accuracy | Sum of unit price x quantity across order items (BR010) |
| Checkout / Place Order | Empty basket checkout attempts | Count of checkout attempts blocked due to empty basket (BR012) |
| Catalog Item Administration | Catalog update rejection rate | Count of catalog item updates rejected due to invalid name, description, price, brand, or type (BR001-BR003) |

### Business Health Indicators
- **Catalog Data Quality:** Frequency of rejected catalog updates (BR001-BR003) indicates how often administrators submit incomplete or invalid product data
- **Basket Hygiene:** Frequency of empty basket line removals (BR006) indicates how often customers reduce items to zero rather than removing them directly
- **Checkout Friction:** Frequency of empty-basket checkout blocks (BR012) may indicate UX issues prompting customers to attempt checkout prematurely
- **Order Integrity:** Rejection rate for incomplete order line items (BR009) and missing buyer references (BR008, BR011) indicates data integrity in the order pipeline

---
> Note: Target values and benchmarks require business input.