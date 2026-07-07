# Business Process Models
## eShopOnWeb

---
### Process: Add Item to Basket
**Trigger:** Customer (or anonymous user) selects a catalog item to purchase
**Actors:** Customer, System
**End Result:** Basket contains the requested item with correct quantity

**Steps:**
1. System — Retrieve the customer's existing basket, or create a new one if none exists
   - Decision: Does a basket already exist for this user?
     - YES -> Use existing basket
     - NO  -> Create a new basket for the user
2. System — Add the item to the basket, consolidating quantity if the item is already present
   - Decision: Is the catalog item already in the basket?
     - YES -> Increase quantity of existing basket item
     - NO  -> Add a new basket line item
3. System — Persist the updated basket

**Business Rules Applied:** BR005

---
### Process: Transfer Anonymous Basket to Registered User
**Trigger:** An anonymous user logs in or registers
**Actors:** Customer, System
**End Result:** Registered user's basket contains all items from their anonymous session

**Steps:**
1. System — Retrieve the anonymous user's basket
   - Decision: Does the anonymous basket exist?
     - YES -> Continue transfer
     - NO  -> End process - nothing to transfer
2. System — Retrieve or create a basket for the now-registered user
   - Decision: Does the registered user already have a basket?
     - YES -> Merge items into existing basket
     - NO  -> Create a new basket for the user
3. System — Copy each item from the anonymous basket into the user's basket

**Business Rules Applied:** BR005

---
### Process: Checkout / Place Order
**Trigger:** Customer initiates checkout from their basket
**Actors:** Customer, System
**End Result:** Order is created from the basket contents with a calculated total and shipping address

**Steps:**
1. System — Retrieve the customer's basket with items
2. System — Verify the basket exists and is not empty
   - Decision: Is the basket empty?
     - YES -> Block checkout and raise an empty-basket error
     - NO  -> Continue to order creation
3. System — Retrieve full catalog item details for each basket item
4. System — Create a snapshot of each ordered item (name, picture, price) for the order record
5. System — Create the order with the buyer ID, shipping address, and order items
6. System — Calculate the order total from item prices and quantities

**Business Rules Applied:** BR009, BR010, BR011, BR012

---
### Process: Catalog Item Administration
**Trigger:** Administrator manages catalog items via the admin (Blazor) interface
**Actors:** Administrator, System
**End Result:** Catalog item data is updated and reflected in the admin UI

**Steps:**
1. Administrator — View the list of catalog items, types, and brands
2. Administrator — Create a new catalog item
3. Administrator — Delete an existing catalog item
4. System — Refresh the cached local catalog item list after create/delete

**Business Rules Applied:** BR001, BR002, BR003, BR004

---
### Process: User Authentication
**Trigger:** User submits login credentials via the API
**Actors:** Customer, Administrator, System
**End Result:** User receives a JWT token containing their identity and role claims for subsequent API access

**Steps:**
1. Customer — Submit username and password to the authentication endpoint
2. System — Validate credentials against identity store
   - Decision: Are the credentials valid and is the account not locked out?
     - YES -> Issue authentication token with success result
     - NO  -> Return failed result with lockout/not-allowed status
3. System — Generate a signed JWT token containing user identity and role claims

**Business Rules Applied:** None identified

---