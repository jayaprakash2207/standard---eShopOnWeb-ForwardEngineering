# Strangler Candidate Report — eShopOnWeb

## Purpose

This report identifies modules and components that are candidates for extraction via the Strangler Fig pattern — incrementally replacing legacy monolith functionality with new services without a full rewrite.

---

## Extraction Priority Summary

| Module | Extraction Candidate | Priority | Risk | Notes |
|---|---|---|---|---|
| Catalog (Read) | Yes — REST API already exists | High | Low | PublicApi already exposes catalog read endpoints |
| Identity | Yes — clearly bounded | Medium | Medium | Auth already isolated; BlazorAdmin uses it independently |
| Basket | Partial — service boundary clear | Medium | Medium | Depends on CatalogContext — needs DbContext split first |
| Order | Partial — service boundary clear | Low | High | High cross-module coupling (Basket + Catalog reads) |
| Admin (BlazorAdmin) | No — UI layer only | N/A | N/A | Already a separate SPA project |
| CrossCutting | No — infrastructure glue | N/A | N/A | Should be a shared library, not extracted |

---

## Candidate 1: Catalog Read API

**Module:** Catalog
**Sub-scope:** Read-only catalog operations (browse, filter, lookup brands/types)
**Extraction type:** Extract to standalone read-optimized microservice or API

**Rationale:**
- PublicApi already exposes `GET api/catalog-brands`, `GET api/catalog-items`, `GET api/catalog-types` as well-defined REST endpoints
- BlazorAdmin exclusively uses these read endpoints with no direct DB coupling
- CatalogItem, CatalogBrand, CatalogType entities are read-heavy, write-seldom
- UriComposer already abstracts catalog image URL construction

**Strangler pattern approach:**
1. Create a new `CatalogReadService` project (e.g., standalone ASP.NET Core minimal API)
2. Route `GET api/catalog-*` through API Gateway or reverse proxy to new service
3. New service reads from read replica or a separate Catalog database
4. Retire corresponding PublicApi endpoints once traffic fully migrated

**Blockers:**
- CatalogContext must be split — Catalog entities share a single DbContext with Basket and Order entities
- AutoMapper profiles need to be migrated to the new service

**Confidence:** 0.88

---

## Candidate 2: Authentication / Identity Service

**Module:** Identity
**Sub-scope:** Authentication, JWT issuance, user management
**Extraction type:** Extract to standalone identity provider or integrate with external IdP (Azure Entra ID, Auth0)

**Rationale:**
- AuthenticateEndpoint (`POST api/authenticate`) and related infrastructure are already isolated in `PublicApi/AuthEndpoints/`
- AppIdentityDbContext is fully separate from CatalogContext
- JWT generation (IdentityTokenClaimService) has a clean interface boundary (ITokenClaimsService)
- BlazorAdmin already uses this endpoint independently via HTTP

**Strangler pattern approach:**
1. Extract AuthenticateEndpoint + IdentityTokenClaimService into a new `IdentityService` microservice
2. Both Web (MVC cookie auth) and PublicApi can delegate authentication to the new service
3. Long-term: replace with managed IdP (Azure Entra External ID, Auth0) to eliminate JWT secret management entirely

**Blockers:**
- Web project cookie-based auth not visible in Layer 1 — needs investigation before extraction
- JWT_SECRET_KEY must be externalized first (see RISK-001) before any identity extraction is safe

**Confidence:** 0.85

---

## Candidate 3: Catalog Admin (Write Operations)

**Module:** Catalog
**Sub-scope:** Admin CRUD for catalog items
**Extraction type:** Extract to a dedicated Catalog Management Service with its own write model

**Rationale:**
- BlazorAdmin exclusively performs catalog write operations via PublicApi
- Read (browse) and Write (admin) have distinct actors and SLAs — admin writes are low-volume; public reads are high-volume
- Separating read and write models enables CQRS at the service level

**Strangler pattern approach:**
1. Extract catalog write endpoints into a `CatalogCommandService`
2. Catalog read API remains on current PublicApi
3. Catalog commands publish events (CatalogItemCreated, CatalogItemUpdated) consumed by read service

**Blockers:**
- Catalog mutation endpoint source (POST/PUT/DELETE catalog-items) not fully visible in Layer 1 — implementation must be reviewed before extraction planning
- Event infrastructure (message bus) does not exist in current codebase — would need to be introduced

**Confidence:** 0.75

---

## Candidate 4: Basket Service

**Module:** Basket
**Sub-scope:** Basket lifecycle management
**Extraction type:** Extract to standalone stateful basket service (could use Redis instead of SQL Server)

**Rationale:**
- BasketService and Basket aggregate have a clean interface boundary (IBasketService)
- Basket operations are write-heavy and ephemeral — SQL Server is suboptimal for basket storage
- IBasketQueryService (CountTotalBasketItems) already hints at read/write separation within basket

**Strangler pattern approach:**
1. Replace SQL basket storage with Redis or in-memory store in a new `BasketService` microservice
2. Web project calls BasketService via HTTP (not direct DI injection)
3. TransferBasketAsync becomes an event-driven flow triggered by Identity login events

**Blockers:**
- BasketItem references CatalogItemId — extraction requires a catalog lookup at basket API level
- CatalogContext must be split before Basket has its own schema
- Web project basket controller unknown — extraction complexity cannot be fully assessed

**Confidence:** 0.70

---

## Non-Candidates

### OrderService
**Reason:** OrderService.CreateOrderAsync reads from both Basket and Catalog aggregates in a single transaction. Extracting Order without co-locating Basket and Catalog read access requires distributed transactions or eventual consistency — a significant complexity jump. Should be the last module extracted after Catalog and Basket are already separate services.

### CrossCutting (ApplicationCore interfaces, EfRepository, LoggerAdapter)
**Reason:** These are shared library components, not service-worthy bounded contexts. They should be published as NuGet packages (or kept as project references) rather than extracted as services.

### Web (MVC)
**Reason:** Web project is the primary user-facing application. Its controllers/pages are not visible in Layer 1, so extraction risk cannot be assessed. It also orchestrates multiple services (Basket, Order, Identity) — extracting it would require all downstream services to exist first.

---

## Recommended Extraction Order

1. **Externalize JWT secret and implement real EmailSender** (pre-requisites, not extractions)
2. **Split CatalogContext** into Catalog / Basket / Order DbContexts (enabling prerequisite for all extractions)
3. **Extract Identity Service** (lowest coupling, cleanest boundary)
4. **Extract Catalog Read API** (highest demand, lowest coupling)
5. **Extract Catalog Admin (Write)** (lower volume, builds on read extraction)
6. **Extract Basket Service** (mid complexity)
7. **Extract Order Service** (highest complexity, last in sequence)
