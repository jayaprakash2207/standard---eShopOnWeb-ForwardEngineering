# Business Rules Inventory
## eShopOnWeb

> Total Rules: 12 | Critical: 5 | High: 2 | Medium: 3 | Low: 1

### Validation Rules
| Rule ID | Business Statement | Priority | Source |
|---|---|---|---|
| BR001 | IF a catalog item's name, description, or price is missing or the price is zero/negative THEN reject the update to catalog item details | High | CatalogItem.cs |
| BR002 | IF a catalog brand ID of zero is provided THEN reject the brand assignment for the catalog item | Medium | CatalogItem.cs |
| BR003 | IF a catalog type ID of zero is provided THEN reject the type assignment for the catalog item | Medium | CatalogItem.cs |
| BR007 | IF a quantity adjustment to a basket item would result in a negative value THEN reject the quantity update | High | BasketItem.cs |
| BR008 | IF a buyer record is created without a valid identity reference THEN reject buyer creation | Critical | Buyer.cs |
| BR009 | IF an order line item is created without a valid catalog item ID, product name, or picture URI THEN reject creation of that order line item | Critical | CatalogItemOrdered.cs |
| BR011 | IF an order is created without a buyer ID THEN reject order creation | Critical | Order.cs |

### Calculation Rules
| Rule ID | Business Statement | Priority | Source |
|---|---|---|---|
| BR004 | IF a picture file name is provided for a catalog item THEN generate a unique image path under images/products; IF no picture name is provided THEN clear the picture URI | Low | CatalogItem.cs |
| BR005 | IF a customer adds a catalog item already present in their basket THEN increase the quantity of the existing basket line instead of creating a new line; ELSE add a new basket line item | Critical | Basket.cs |
| BR010 | An order's total is calculated as the sum of each ordered item's unit price multiplied by its quantity | Critical | Order.cs |

### Approval Rules
| Rule ID | Business Statement | Priority | Source |
|---|---|---|---|
| _None identified_ | | | |

### Restriction Rules
| Rule ID | Business Statement | Priority | Source |
|---|---|---|---|
| BR006 | IF a basket line item has a quantity of zero THEN remove it from the basket | Medium | Basket.cs |
| BR012 | IF a customer attempts checkout with no items in their basket THEN block the checkout and raise an empty-basket error | Critical | GuardExtensions.cs |

---
### Config-Driven Rules
Rules whose values come from configuration (can be changed without code deployment):
| Rule ID | Parameter | Current Value | Effect |
|---|---|---|---|
| _None identified_ | All extracted rules are hard-coded in application logic, not driven by configuration | — | — |