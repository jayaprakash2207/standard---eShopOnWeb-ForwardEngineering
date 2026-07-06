=== DOCUMENT: 01_BRD.md ===

# Business Requirements Document
## eShopOnWeb — .NET 8 Reference E-Commerce Platform

**Version:** 1.0 (Reverse-Engineered)
**Confidence:** HIGH for confirmed capabilities; ASSUMED for Web pages not in extraction
**Source:** BA Agent 1+2 outputs, all business rules BR-01 through BR-46

---

## 1. Executive Summary

eShopOnWeb is a modular monolith e-commerce platform built on ASP.NET Core 8. It supports a customer-facing storefront, an API-driven administrator portal, and a shared domain core. The system manages a product catalog, customer shopping baskets, and order placement. Authentication is provided via ASP.NET Core Identity with cookie-based sessions for web customers and JWT tokens for the admin API. The system is deployed as two services sharing one database: a web application (eshopwebmvc) and a public REST API (eshoppublicapi).

---

## 2. Business Objectives

| ID | Objective | Priority |
|----|-----------|----------|
| OBJ-001 | Enable customers to browse and purchase physical goods online without creating an account | High |
| OBJ-002 | Allow registered customers to maintain a persistent shopping basket across sessions | High |
| OBJ-003 | Enable checkout with shipping address and create immutable order records | High |
| OBJ-004 | Provide administrators with a secure portal to manage the product catalog | High |
| OBJ-005 | Support customer self-registration with email-based account confirmation | High |
| OBJ-006 | Maintain historical order records with price and product snapshots that cannot be altered retroactively | High |

---

## 3. Stakeholders

| Role | System Role | Access Method |
|------|-------------|---------------|
| Catalog Administrator | Manages products (CRUD), prices, images, brands, types | BlazorAdmin SPA via JWT |
| Registered Customer | Browses, adds to basket, checks out, views orders | Web MVC via cookie session |
| Anonymous Visitor | Browses products, maintains temporary basket | Web MVC, no account required |
| Prospective Customer | Self-registers for an account | Web MVC registration form |
| Automated System | DB seeding, basket transfer, order assembly | Server-side, no human actor |

---

## 4. Functional Requirements

### FR-01: Product Catalog

| ID | Requirement | Priority | Confidence |
|----|-------------|----------|------------|
| FR-01-01 | System SHALL display paginated product listings filterable by brand and type | Must Have | HIGH |
| FR-01-02 | System SHALL allow administrators to create products with name, description, price, brand, type, and optional image | Must Have | HIGH |
| FR-01-03 | System SHALL allow administrators to update any product field | Must Have | HIGH |
| FR-01-04 | System SHALL allow administrators to delete products | Must Have | HIGH |
| FR-01-05 | System SHALL reject product names that are blank or duplicate an existing name | Must Have | HIGH |
| FR-01-06 | System SHALL reject prices outside the range 0.01–1000.00 with no more than 2 decimal places | Must Have | HIGH |
| FR-01-07 | System SHALL restrict create/update/delete operations to the Administrators role | Must Have | HIGH |
| FR-01-08 | System SHALL accept image uploads in JPG, PNG, GIF, or JPEG format up to 512 KB | Should Have | HIGH |
| FR-01-09 | System SHALL associate each product with exactly one brand and one type | Must Have | HIGH |
| FR-01-10 | System SHALL compose product image URIs from a configurable base URL template | Must Have | HIGH |

### FR-02: Shopping Basket

| ID | Requirement | Priority | Confidence |
|----|-------------|----------|------------|
| FR-02-01 | System SHALL automatically create a basket when a visitor first adds an item | Must Have | HIGH |
| FR-02-02 | System SHALL merge quantities when the same product is added to a basket that already contains it | Must Have | HIGH |
| FR-02-03 | System SHALL prevent basket item quantities from being set below zero | Must Have | HIGH |
| FR-02-04 | System SHALL automatically remove items from the basket when their quantity is set to zero | Must Have | HIGH |
| FR-02-05 | System SHALL persist anonymous baskets using a browser cookie session identifier | Must Have | HIGH |
| FR-02-06 | System SHALL assign a new GUID as the basket identifier for each anonymous session | Must Have | HIGH |
| FR-02-07 | System SHALL persist the anonymous session cookie for 10 years | Should Have | HIGH |
| FR-02-08 | System SHALL display the total unit count (not distinct product count) in basket navigation | Should Have | HIGH |

### FR-03: Anonymous Basket Transfer

| ID | Requirement | Priority | Confidence |
|----|-------------|----------|------------|
| FR-03-01 | On successful login, system SHALL detect whether an anonymous basket cookie is present | Must Have | HIGH |
| FR-03-02 | System SHALL transfer all items from the anonymous basket into the authenticated customer's basket | Must Have | HIGH |
| FR-03-03 | System SHALL combine quantities when the same product exists in both baskets | Must Have | HIGH |
| FR-03-04 | System SHALL delete the anonymous basket after transfer | Must Have | HIGH |
| FR-03-05 | System SHALL delete the anonymous basket cookie from the browser after transfer | Must Have | HIGH |
| FR-03-06 | System SHALL take no action if no anonymous basket exists at login time | Must Have | HIGH |

### FR-04: Order Placement

| ID | Requirement | Priority | Confidence |
|----|-------------|----------|------------|
| FR-04-01 | System SHALL prevent order placement from an empty basket | Must Have | HIGH |
| FR-04-02 | System SHALL require a valid shipping address to place an order | Must Have | HIGH |
| FR-04-03 | System SHALL capture a permanent snapshot of each product's name and image URI at order time | Must Have | HIGH |
| FR-04-04 | System SHALL record the price from the basket (set at add-to-basket time), not the current catalog price | Must Have | HIGH |
| FR-04-05 | System SHALL calculate order total as sum of (unit price × quantity) for all line items | Must Have | HIGH |
| FR-04-06 | System SHALL require a buyer identifier on every order | Must Have | HIGH |
| FR-04-07 | System SHALL NOT automatically clear the basket after order placement | Must Have | HIGH |
| FR-04-08 | System SHALL require the customer to be authenticated to place an order | Must Have | HIGH |

### FR-05: Identity and Authentication

| ID | Requirement | Priority | Confidence |
|----|-------------|----------|------------|
| FR-05-01 | System SHALL issue JWT tokens valid for 7 days on successful API authentication | Must Have | HIGH |
| FR-05-02 | System SHALL embed the user's username and all role memberships as JWT claims | Must Have | HIGH |
| FR-05-03 | System SHALL count failed login attempts and lock accounts after repeated failures | Must Have | HIGH |
| FR-05-04 | System SHALL NOT create persistent sessions for API authentication ("remember me" disabled) | Must Have | HIGH |
| FR-05-05 | System SHALL use cookie-based sessions of 60-minute validity for web customers | Must Have | HIGH |
| FR-05-06 | System SHALL support token revocation for cookie sessions via server-side cache | Must Have | HIGH |
| FR-05-07 | System SHALL create a new customer account with email and password on registration | Must Have | HIGH |
| FR-05-08 | System SHALL require email confirmation before a registered account is considered active | Must Have | HIGH |

### FR-06: Admin Portal

| ID | Requirement | Priority | Confidence |
|----|-------------|----------|------------|
| FR-06-01 | Admin portal SHALL display catalog items in pages of 10 items | Should Have | HIGH |
| FR-06-02 | Admin portal SHALL cache catalog data locally for 1 minute | Should Have | HIGH |
| FR-06-03 | Admin portal SHALL immediately invalidate cache after any create, update, or delete operation | Must Have | HIGH |
| FR-06-04 | Admin portal SHALL display a dismissing notification (3 seconds) on every operation result | Should Have | HIGH |
| FR-06-05 | Admin portal SHALL refresh authentication state every 60 seconds | Should Have | HIGH |

---

## 5. Non-Functional Requirements Summary

| Category | Requirement | Value | Status |
|----------|-------------|-------|--------|
| Performance | Catalog list API response time | Remove 1s artificial delay; target <200ms P95 | **BLOCKED — TD-07** |
| Security | JWT signing key | Must be externalized to Key Vault; never hardcoded | **BLOCKED — TD-01** |
| Security | Default admin password | Must be environment-specific; never hardcoded | **BLOCKED — TD-02** |
| Availability | App Service compute | B1 (1 core, 1.75GB RAM, Linux) | Current |
| TLS | Minimum version | TLS 1.2 | Satisfied |
| Data Freshness | Server-side catalog cache | 30 seconds sliding | Satisfied |
| Data Freshness | Client-side catalog cache | 60 seconds | Satisfied |
| Token Lifetime | JWT | 7 days | Satisfied |

---

## 6. Constraints

| Constraint | Detail |
|------------|--------|
| C-001 | Both deployable services share a single CatalogDB SQL Server database (VIO-001) |
| C-002 | PublicApi has no Azure deployment path in current configuration (TD-12) |
| C-003 | Email confirmation is permanently non-functional; requires real EmailSender implementation |
| C-004 | Payment processing is not implemented; orders have no financial transaction capture |
| C-005 | Order lifecycle has no status field; no fulfilment workflow exists |
| C-006 | Checkout hardcodes a shipping address; address collection form is missing |
| C-007 | Buyer and PaymentMethod domain entities are not persisted |

---

## 7. Out of Scope (Current Version)

- Payment processing and PCI-compliant card storage
- Order fulfilment workflow and status tracking
- Shipping carrier integration
- Product inventory tracking and stock levels
- Promotional codes, discounts, and pricing rules
- Multi-currency support
- Product reviews and ratings
- Wishlists
- Returns and refunds
- Tax calculation
