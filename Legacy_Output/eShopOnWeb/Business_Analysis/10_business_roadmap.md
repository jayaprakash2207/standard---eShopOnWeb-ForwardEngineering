# Business Roadmap
## eShopOnWeb

> INFERRED from code analysis — requires business strategy input

### Current State Summary
- **Capabilities working well:** Basket / Shopping Cart Management (consolidation, cleanup, and session transfer logic are well-defined with clear rules); Order Management (strong validation and total calculation logic ensures order integrity)
- **Capabilities needing improvement:** Catalog Management (validation exists but is limited to basic field presence and price positivity — no rules around inventory levels, stock availability, or pricing tiers); Identity & Authentication (no business rules identified, suggesting authorization/role logic may be under-specified)
- **Missing capabilities (gaps):**
  - Inventory/stock management — no entity or rule tracks product availability or stock levels
  - Order fulfillment/shipping status tracking — Order entity has no lifecycle states (e.g., Pending, Shipped, Delivered)
  - Customer notifications — Email Sender component exists but is "not yet implemented"
  - Payment processing — Payment Methods are stored on Buyer, but no rules govern payment validation or processing
  - Discounts/promotions — no rules or entities related to pricing adjustments at checkout

### Recommended Upgrade Priorities
| Priority | Capability | Reason | Complexity |
|---|---|---|---|
| 1 | Order Fulfillment & Status Tracking | Orders currently have no lifecycle states, limiting visibility into fulfillment for customers and staff | High |
| 2 | Inventory / Stock Management | No stock-level rules exist; customers could order out-of-stock items | High |
| 3 | Customer Notifications | Email Sender exists but is incomplete — completing this closes a known gap | Medium |
| 4 | Payment Processing Validation | Payment Methods exist on Buyer but lack associated business rules | Medium |
| 5 | Catalog Management Enhancements | Add rules for stock-aware catalog display and richer pricing rules (e.g., discounts) | Medium |

### Quick Wins (Low effort, high value)
- No config-driven rules were identified in this codebase, so there are no "flip a setting" quick wins at this time
- Completing the existing Email Sender implementation (referenced but not implemented) would close a known functional gap with relatively low new-design effort

### Technical Debt Identified
- Entities lack defined lifecycle/state fields (e.g., Order has no status field), which limits process visibility and may require schema changes to address
- No business rules exist for the Identity & Authentication and Admin Catalog Operations capabilities, suggesting either under-documentation or under-developed business logic in these areas
- Email notification capability is referenced in code but not implemented, indicating incomplete feature delivery

---
> Note: Timeline and investment decisions require business leadership input.