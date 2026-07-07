# Extraction Audit — eShopOnWeb Architecture Extraction

## Extraction Metadata

| Field | Value |
|---|---|
| Extraction date | 2026-07-06 |
| Codebase | eShopOnWeb (.NET 8 Reference Application) |
| Extraction agent | Application Architecture Extraction Agent |
| Layer 1 data provided | Yes — JSON-embedded source code artifacts |
| Output directory | results/aa-outputs/D1-application-architecture/ |
| Total output files | 14 JSON/Markdown + 5 Mermaid diagrams |

---

## Layer 1 Source Coverage

### Files Present in Layer 1

| File | Used In Stage |
|---|---|
| src/ApplicationCore/Services/BasketService.cs | Stages 2, 3, 4, 6 |
| src/ApplicationCore/Services/OrderService.cs | Stages 2, 3, 4, 6 |
| src/ApplicationCore/Services/UriComposer.cs | Stages 3, 6 |
| src/ApplicationCore/Entities/BasketAggregate/Basket.cs | Stages 2, 3, 4 |
| src/ApplicationCore/Entities/OrderAggregate/Order.cs | Stages 2, 3, 4 |
| src/ApplicationCore/Constants/AuthorizationConstants.cs | Stages 3, 8, 9 |
| src/Infrastructure/Data/CatalogContext.cs | Stages 2, 3, 5, 8 |
| src/Infrastructure/Data/EfRepository.cs | Stages 2, 3, 5 |
| src/Infrastructure/Data/Queries/BasketQueryService.cs | Stages 3, 8 |
| src/Infrastructure/Identity/IdentityTokenClaimService.cs | Stages 3, 6, 8, 9 |
| src/Infrastructure/Services/EmailSender.cs | Stages 3, 8, 9 |
| src/BlazorAdmin/Program.cs | Stages 1, 3, 8 |
| src/BlazorAdmin/CustomAuthStateProvider.cs | Stages 3, 4, 6 |
| src/BlazorAdmin/Services/CachedCatalogItemServiceDecorator.cs | Stages 3, 4, 6, 7 |
| src/PublicApi/AuthEndpoints/AuthenticateEndpoint.cs | Stages 3, 4, 6 |
| src/PublicApi/CatalogBrandEndpoints/CatalogBrandListEndpoint.cs | Stages 3, 4 |
| src/ApplicationCore/Interfaces/IAppLogger.cs | Stages 2, 7 |
| src/BlazorAdmin/Services/CatalogItemService.cs | Stages 3, 4, 5 |
| src/BlazorAdmin/Pages/CatalogItemPage/List.razor.cs | Stages 3, 4, 6 |
| src/BlazorAdmin/wwwroot/appsettings.json | Stages 1, 2 |
| azure.yaml | Stage 1 |
| docker-compose.yml | Stage 1 |
| src/Web/Properties/launchSettings.json | Stages 1, 4 |

### Files NOT Present in Layer 1 (Gaps)

| Missing File | Impact | Artifacts Affected |
|---|---|---|
| src/Web/Controllers/ (all) | Primary user flow routes unknown | application-interface-catalogue.json (INT-012 confidence 0.70), call-flow-map.json FLOW-003/FLOW-004/FLOW-005 entry points |
| src/Web/Pages/ (all Razor pages) | Web UI patterns unknown | architecture-pattern-report.md |
| src/Web/Program.cs | Web startup, auth config unknown | architecture-pattern-report.md, forward-engineering-input-map.md OQ-002 |
| src/PublicApi/CatalogItemEndpoints/ | Admin CRUD endpoint implementation unknown | application-interface-catalogue.json INT-004 to INT-008 confidence reduced; application-risk-register.json RISK-008 |
| src/ApplicationCore/Entities/BuyerAggregate/ | Buyer/PaymentMethod entity fullness unknown | component-registry.json (dead code flag), architecture-violation-register.json VIO-008 confidence 0.75 |
| tests/ (any test projects) | Test coverage unknown | extraction-audit.md only |
| infra/ (Bicep files) | Azure infrastructure baseline unknown | forward-engineering-input-map.md OQ-017 |
| .github/workflows/ or .azure/pipelines/ | CI/CD pipeline unknown | forward-engineering-input-map.md OQ-015 |

---

## Stage Completion Summary

| Stage | Output File | Status | Completeness | Confidence |
|---|---|---|---|---|
| Stage 1 — System Inventory | system-inventory.json | Complete | High | 0.95 |
| Stage 2 — Module Boundary Map | module-boundary-map.json | Complete | High | 0.90 |
| Stage 3 — Component Registry | component-registry.json | Complete | High | 0.88 |
| Stage 4 — Interface Catalogue | application-interface-catalogue.json | Complete | Medium (Web routes unknown) | 0.83 |
| Stage 5 — Dependency Graph | dependency-graph.json | Complete | High | 0.90 |
| Stage 6 — Call Flow Map | call-flow-map.json | Complete | Medium (Web entry points unknown) | 0.86 |
| Stage 7 — Architecture Pattern Report | architecture-pattern-report.md | Complete | High | 0.92 |
| Stage 8 — Architecture Violation Register | architecture-violation-register.json | Complete | High | 0.93 |
| Stage 9 — Application Risk Register | application-risk-register.json | Complete | High | 0.91 |
| Stage 10 — Strangler Candidate Report | strangler-candidate-report.md | Complete | Medium | 0.82 |
| Stage 11 — Forward Engineering Input Map | forward-engineering-input-map.md | Complete | Medium | 0.85 |
| Stage 12 — Diagrams | diagrams/*.mmd | Complete | High | 0.88 |
| Stage 13 — Summary | application-architecture-summary.md | Complete | High | 0.90 |

---

## Evidence Quality Assessment

### Verified (direct source evidence)
- Clean Architecture pattern (no infra deps in ApplicationCore)
- JWT secret hardcoded in AuthorizationConstants.cs
- EmailSender stub returning Task.CompletedTask
- CatalogContext spanning 3 bounded contexts (7 DbSets)
- Decorator pattern in BlazorAdmin (CachedCatalogItemServiceDecorator)
- 7-day JWT token TTL in IdentityTokenClaimService
- localStorage cache cleared on BlazorAdmin startup
- Ardalis.Specification and Guard Clauses usage
- Docker Compose deployment with eshopwebmvc, eshoppublicapi, sqlserver containers
- Azure deployment via azure.yaml targeting App Service

### Inferred (logical deduction from available artifacts)
- Web project uses cookie-based authentication (inferred from AppIdentityDbContext separation)
- PublicApi has 5 additional catalog item endpoints (inferred from BlazorAdmin HTTP calls)
- BlazorAdmin may be embedded in Web project (inferred from baseUrls.webBase = '/')
- Price manipulation risk in basket add flow (inferred from IBasketService.AddItemToBasket signature)
- Buyer/PaymentMethod entities are dead code (inferred from absence of callers in visible artifacts)

### Not Determinable from Layer 1
- Web project route structure
- Checkout controller implementation
- Catalog item endpoint authorization
- Order post-creation basket cleanup
- CI/CD pipeline details
- Azure Blob Storage vs. local image storage

---

## Rules Compliance Check

| Rule | Compliant |
|---|---|
| No source code modified | Yes — all outputs are analysis documents only |
| No facts invented without evidence | Yes — all inferences marked with confidence score and evidence |
| Unknown items marked "unknown" or with open questions | Yes — 22 open questions documented |
| Confidence scores on all evidence claims | Yes |
| Security findings documented | Yes — 4 security risks, 3 security violations |
| Dead code flagged with confidence | Yes — VIO-008 confidence 0.75 |
