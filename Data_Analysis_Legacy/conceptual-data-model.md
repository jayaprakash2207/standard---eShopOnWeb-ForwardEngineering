# Conceptual Data Model — eShopOnWeb
> Business language only. No table names, column types, or technical FK syntax.
> This describes what the business cares about, not how the database stores it.
> Extraction date: 2026-07-06
> **RC-09 (ENRICHED — Phase 2 README):** This is a **reference/demo application**, not a production ecommerce system. Per README: "It is not meant to be an eCommerce reference application, and as such it does not implement many features that would be obvious and/or essential to a real eCommerce application." Purpose: illustrates ASP.NET Core architectural patterns for the eBook "Architecting Modern Web Applications with ASP.NET Core and Azure". Active development has moved to https://github.com/dotnet/eShop. This context informs why features like payment processing, inventory management, and shipping integrations are absent — they are out of scope by design, not gaps.

---

## Core Business Concepts

### Shopper
A person who browses and buys products from the store. A shopper may visit anonymously (tracked by a long-lived browser session marker) or as a registered member. When a registered member logs in, any products they placed in their cart while browsing anonymously are automatically carried over to their account cart.

---

### Product
A specific item available for purchase. Every product belongs to one **Brand** and one **Category**. A product has a current selling price and a photo. Products are managed exclusively by store administrators. The product catalogue is the authoritative list of what the store currently sells and at what prices.

---

### Brand
A manufacturer or label associated with products — for example ".NET", "Azure", "Visual Studio", "SQL Server", or "Other". One brand may be associated with many products.

---

### Category
A product type classification — for example Mug, T-Shirt, Sheet, or USB Memory Stick. One category may contain many products.

---

### Cart
A temporary collection of products a shopper intends to purchase. A cart belongs to one shopper and a shopper has one active cart at a time. Each item in the cart records the price at the moment it was added — this price is preserved even if the store subsequently changes the product price. The cart is destroyed once the shopper completes a purchase.

---

### Purchase
A completed transaction. A purchase permanently records:
- Which shopper bought the products
- The shipping address provided at the time of the transaction
- The date and time of purchase
- Each product line: a frozen copy of the product's details as they appeared at purchase time (name, image, identifier), the price paid per unit, and the quantity

A purchase is an immutable historical record. If a product is later renamed, repriced, or removed from the catalogue, the purchase record retains the original details exactly as they were at purchase time.

---

### Purchase Line
A single product entry within a Purchase. Each line captures a frozen snapshot of the product's details at the moment of purchase alongside the quantity and price paid. This snapshot persists independently of any future changes to the product catalogue.

---

### Registered Member
A shopper who has created an account. Members log in with an email address and password. Members may be assigned the **Administrator** role, which grants full control over the product catalogue.

---

### Administrator
A registered member with elevated permissions. Administrators can add, edit, and remove products from the catalogue via a dedicated management interface. All catalogue write operations require administrator credentials.

---

## Relationships Between Concepts

```
  Brand ─── associated with ───► Product ◄─── associated with ─── Category
                                     │
                           added to  │  (price locked at add-time)
                                     ▼
  Shopper ─── has one active ─► Cart ──── contains ──────► Cart Line Item
     │                             │                              │
     │ places                      │ converted to at checkout     │ price locked when added
     │                             ▼
     └──── places ─────────► Purchase ──── contains ──────► Purchase Line
                                 │                                │
                                 │ shipped to                     │ captures frozen snapshot of
                                 ▼                                ▼
                         Shipping Address                  Product Snapshot
                                                      (name, image, identifier
                                                       frozen at purchase time)

  Registered Member ─── may hold ───► Administrator role
           │
           └── has one active ─────► Cart (identified by email)
```

---

## Key Business Invariants (plain language)

1. **A cart cannot be empty at checkout.** Attempting to complete a purchase from an empty cart is rejected by the system.

2. **Cart prices are locked.** The price shown in the cart at the moment the customer added a product is the price they pay — even if the store changes the product price before the customer completes their purchase.

3. **Purchase records are immutable.** Once a purchase is recorded, its product details (names, images, prices paid, quantities) cannot be changed retroactively, even if the store later updates or removes those products.

4. **Only administrators can manage products.** Browsing, adding to cart, and purchasing are open to all shoppers (including anonymous). Creating, editing, or deleting products requires authenticated administrator credentials.

5. **One active cart per shopper.** If an anonymous shopper creates an account and logs in, their anonymous cart is merged into their member cart.

6. **Product names should be unique.** Two products cannot be created with the same name (enforced when creating new products — not enforced during edits).
