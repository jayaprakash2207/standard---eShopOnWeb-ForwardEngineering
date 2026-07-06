# Stakeholder Map
## eShopOnWeb

### Internal Stakeholders (System Users)

#### Customer / Buyer
- **Responsibilities:** Browse catalog items, types, and brands; manage shopping basket (add items, adjust quantities); transfer anonymous basket to account on login; place orders and view order history; manage payment methods and shipping address
- **System Access:** Catalog browsing endpoints, Basket management, Order management, Authentication
- **Key Processes:** Add Item to Basket, Transfer Anonymous Basket to Registered User, Checkout / Place Order, User Authentication
- **Permission Level:** Standard

#### Administrator
- **Responsibilities:** Create, update, and delete catalog items; manage catalog brands and types; view and manage application data via the admin interface
- **System Access:** Admin catalog management interface, cached catalog data services, catalog lookup data
- **Key Processes:** Catalog Item Administration, User Authentication
- **Permission Level:** Admin

#### System / Service Account
- **Responsibilities:** Seed initial catalog and identity data on startup; issue authentication tokens; compose image URIs and compute basket/order totals; send notification emails (not yet implemented)
- **System Access:** Catalog and identity data seeding components, token issuance service, image path composition, email sending component
- **Key Processes:** Supports all processes via background/system operations (seeding, token issuance, calculations)
- **Permission Level:** Elevated

### External Stakeholders

- **Customers (public-facing):** End users of the storefront who browse products, build baskets, and place orders — represented in-system by the Customer/Buyer role
- **Notification Recipients:** Customers expected to receive order/email notifications via the Email Sender component (present in code but not yet implemented, suggesting a planned but incomplete capability)

---
> Note: Influence levels and org hierarchy require business validation.