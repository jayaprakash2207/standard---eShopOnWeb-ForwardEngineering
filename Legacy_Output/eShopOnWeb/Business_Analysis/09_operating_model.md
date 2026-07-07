# Operating Model
## eShopOnWeb

> INFERRED from code analysis — requires business validation

### Organizational Roles Identified
- **Customer / Buyer:** Self-service role — browses the catalog, manages their own basket, and places their own orders. No oversight of other users' data.
- **Administrator:** Back-office role — maintains the product catalog (items, brands, types) through a dedicated admin interface, separate from the customer-facing storefront.
- **System / Service Account:** Automated role — performs startup data seeding, token issuance, image path composition, and total calculations on behalf of the application itself, with no human operator.

### Decision Authority (inferred)
| Decision | Who Decides | Rule Reference |
|---|---|---|
| Whether a catalog item update is valid (name/description/price) | System (automatic validation) | BR001 |
| Whether a brand/type assignment is valid | System (automatic validation) | BR002, BR003 |
| Whether a basket quantity adjustment is allowed | System (automatic validation) | BR007 |
| Whether a checkout can proceed | System (automatic validation) | BR012 |
| Whether a buyer/order record can be created | System (automatic validation) | BR008, BR011 |
| Whether a user is granted access (login) | System / Identity store | User Authentication process |

### Process Ownership (inferred)
| Process | Owner Role | Supporting Roles |
|---|---|---|
| Add Item to Basket | Customer / Buyer | System |
| Transfer Anonymous Basket to Registered User | System | Customer / Buyer |
| Checkout / Place Order | Customer / Buyer | System |
| Catalog Item Administration | Administrator | System |
| User Authentication | System / Service Account | Customer / Buyer, Administrator |

---
> Note: Org chart and reporting lines require HR/business input.