# Conceptual Data Model — eShopOnWeb

*Business language only — no table names, data types, or FK syntax.*

## Core Business Concepts

**Customer**
A person who can log in, browse products, hold a shopping basket, and place orders. Customers have an identity (login credentials, email, roles such as Administrator) and may store one or more payment methods for checkout.

**Product**
An item offered for sale. Each product belongs to a Brand and a Category (Type), has a name, description, price, and an image. Each product also tracks how many units are currently available, and the warehouse rules for when to reorder more stock (a low-stock threshold, a maximum stock level, and whether a reorder is currently underway).

**Brand**
A manufacturer or label that groups products together (e.g. a clothing brand).

**Category**
A classification grouping products by type (e.g. mugs, t-shirts, stickers).

**Shopping Basket**
A temporary collection of products a customer intends to purchase, along with the quantity and price of each. A basket belongs to exactly one customer and exists until checkout (or abandonment).

**Order**
A confirmed purchase made by a customer. An order records when it was placed, where it should be shipped (a shipping address consisting of street, city, state, country, and postal code), and a list of the products purchased — each captured as it appeared *at the time of purchase* (name, price, image), so that historical orders remain accurate even if the product catalog changes later.

**Payment Method**
A way for a customer to pay for an order. Associated with a customer's account. **RC-002 (CORRECTED)**: this concept exists only as unused/aspirational source code (`BuyerAggregate/Buyer.cs`, `PaymentMethod.cs`) and is **not currently implemented** in the persisted schema — no checkout flow or table backs it today.

**Role / Permission**
Customers (and staff) are assigned roles (e.g. "Administrator") that determine what parts of the system they can access — notably the catalog-management admin tools.

## Relationships (in business terms)

- A **Customer** has **one Shopping Basket** at a time.
- A **Shopping Basket** contains **many Basket Lines**, each referring to one **Product** with a quantity and price.
- A **Customer** can place **many Orders** over time.
- An **Order** contains **many Order Lines**, each describing one **Product** as it was at the time of purchase, with quantity and price paid.
- A **Product** belongs to **one Brand** and **one Category**.
- A **Brand** can have **many Products**.
- A **Category** can have **many Products**.
- A **Customer** may have **one or more Payment Methods**. *(RC-002: CONFIRMED not implemented in the current persisted schema — Buyer/PaymentMethod are unused code, not mapped tables. See redundancy-analysis.json.)*
- A **Customer** has **one or more Roles** governing system access (confirmed role: `"Administrators"`, RC-008).

## Change Records
- **RC-002** (CORRECTED): Payment Method concept confirmed not implemented in persisted schema (was "unconfirmed").
- **RC-008** (ENRICHED): Confirmed role name "Administrators".

## Business Lifecycle Notes
- Products have a **stock replenishment lifecycle**: available stock depletes as orders are placed; when it falls below a restock threshold, a reorder process is signaled (`OnReorder`); stock is replenished up to a maximum threshold.
- An **Order cannot be created from an empty Basket** — this is an enforced business rule, not just a UI restriction.
- Once an **Order** is placed, the product details on that order are **frozen in time** — later changes to a product's name, price, or image do not retroactively change historical orders.
