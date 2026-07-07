# Business Capability Model — eShopOnWeb

**Date:** 2026-07-06

---

## Level 0 — Business Domain

```
eShopOnWeb Online Retail Platform
```

---

## Level 1 — Capability Areas

| ID | Area | Status |
|----|------|--------|
| BCA-01 | Product Management | ACTIVE |
| BCA-02 | Customer Acquisition | ACTIVE |
| BCA-03 | Transaction Processing | PARTIAL |
| BCA-04 | Fulfillment | NOT IMPLEMENTED |
| BCA-05 | Customer Management | PARTIAL |
| BCA-06 | Platform Operations | PARTIAL |

---

## Level 2 — Capabilities by Area

### BCA-01 — Product Management

| ID | Capability | Status | Bounded Context | API Surface |
|----|-----------|--------|-----------------|-------------|
| CAP-001 | Catalog Browsing | ACTIVE | Catalog | GET /api/catalog-items, /api/catalog-brands, /api/catalog-types |
| CAP-002 | Catalog Administration | ACTIVE | Catalog | POST/PUT/DELETE /api/catalog-items (ADMINISTRATORS only) |
| CAP-101 | Product Image Management | ACTIVE | Catalog | Image upload via DTO PictureBase64; 512 KB max, .jpg/.jpeg/.png/.gif |
| CAP-102 | Brand Management | ACTIVE (read-only API) | Catalog | GET /api/catalog-brands; create/update via seeding only |
| CAP-103 | Product Type Management | ACTIVE (read-only API) | Catalog | GET /api/catalog-types; create/update via seeding only |

### BCA-02 — Customer Acquisition

| ID | Capability | Status | Bounded Context | Handler |
|----|-----------|--------|-----------------|---------|
| CAP-005 | User Authentication | ACTIVE | Identity | POST /authenticate (JWT); Login.cshtml.cs (Cookie) |
| CAP-006 | User Registration | ACTIVE (email unconfirmed) | Identity | Register.cshtml.cs |
| CAP-007 | Anonymous-to-Authenticated Basket Transfer | ACTIVE | Basket/Identity | BasketService.TransferBasketAsync |
| CAP-201 | Account Lockout Protection | ACTIVE | Identity | lockoutOnFailure:true in AuthenticateEndpoint |
| CAP-202 | Email Confirmation | STUB — NOT FUNCTIONAL | Identity | EmailSender stub |

### BCA-03 — Transaction Processing

| ID | Capability | Status | Bounded Context | Handler |
|----|-----------|--------|-----------------|---------|
| CAP-003 | Basket Management | ACTIVE | Basket | BasketService (no REST API; Web Razor Pages) |
| CAP-004 | Order Checkout | ACTIVE (no payment) | Order | OrderService.CreateOrderAsync; Web checkout page |
| CAP-008 | Payment Processing | NOT IMPLEMENTED | Buyer | No service; Stripe intent in comment only |
| CAP-301 | Price Lock at Basket Add | ACTIVE | Basket | BasketItem.UnitPrice at construction |
| CAP-302 | Order Line Snapshot | ACTIVE | Order | CatalogItemOrdered value object |

### BCA-04 — Fulfillment

| ID | Capability | Status | Bounded Context | Handler |
|----|-----------|--------|-----------------|---------|
| CAP-401 | Order Status Tracking | NOT IMPLEMENTED | Order | No status field on Order entity |
| CAP-402 | Order Dispatch Notification | NOT IMPLEMENTED | Order/Identity | No email; no status transitions |
| CAP-403 | Delivery Confirmation | NOT IMPLEMENTED | Order | — |

### BCA-05 — Customer Management

| ID | Capability | Status | Bounded Context | Handler |
|----|-----------|--------|-----------------|---------|
| CAP-009 | Order History Retrieval | UNCONFIRMED | Order | Specification exists; no confirmed UI |
| CAP-501 | Saved Payment Methods | NOT IMPLEMENTED | Buyer | Buyer/PaymentMethod dormant |
| CAP-502 | GDPR Data Erasure | NOT IMPLEMENTED | All PII entities | No erasure mechanism found |

### BCA-06 — Platform Operations

| ID | Capability | Status | Component | Notes |
|----|-----------|--------|-----------|-------|
| CAP-601 | Infrastructure as Code | ACTIVE | infra/ Bicep | Azure App Service, SQL, Key Vault |
| CAP-602 | Build and Test CI | ACTIVE | GitHub Actions | dotnet build + dotnet test |
| CAP-603 | Automated Deployment | NOT WIRED | azure.yaml + Bicep | IaC complete; no pipeline step |
| CAP-604 | Health Monitoring | PARTIAL | /health endpoints | Content assertion — fragile |
| CAP-605 | APM Telemetry | NOT IMPLEMENTED | App Insights ref only | No SDK; no resource provisioned |
| CAP-606 | Secrets Management | ACTIVE (production) | Azure Key Vault | Hardcoded in source for dev |

---

## Capability Heat Map

| Capability Area | Completeness | Business Risk | Forward Engineering Priority |
|-----------------|-------------|--------------|------------------------------|
| Product Management | 90% | Low | Low — minor gaps only |
| Customer Acquisition | 70% | Medium | Medium — email stub |
| Transaction Processing | 40% | CRITICAL | CRITICAL — no payment |
| Fulfillment | 0% | HIGH | HIGH — orders untrackable |
| Customer Management | 10% | HIGH | HIGH — GDPR exposure |
| Platform Operations | 60% | HIGH | HIGH — no deploy pipeline; no APM |