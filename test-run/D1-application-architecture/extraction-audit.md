# Extraction Audit — Self-Review Checklist

Agent: Application Architecture Extraction Agent
Output directory: test-run/D1-application-architecture/
Date: 2026-07-06

---

## Phase Completion

| Phase | Status | Notes |
|---|---|---|
| Phase 1: System Inventory | Complete | system-inventory.json |
| Phase 2: Module Boundary Detection | Complete | module-boundary-map.json |
| Phase 3: Component Discovery | Complete | component-registry.json |
| Phase 4: Interface / Entry Point Discovery | Complete | application-interface-catalogue.json |
| Phase 5: Dependency Analysis | Complete | dependency-graph.json |
| Phase 6: Call Flow Tracing | Complete | call-flow-map.json |
| Phase 7: Architecture Pattern Detection | Complete | architecture-pattern-report.md |
| Phase 8: Architecture Violation Detection | Complete | architecture-violation-register.json |
| Phase 9: Application Risk Register | Complete | application-risk-register.json |
| Phase 10: Strangler / Migration Candidate Analysis | Complete | strangler-candidate-report.md |
| Phase 11: Forward Engineering Input Map | Complete | forward-engineering-input-map.md |
| Phase 12: Diagrams | Complete | diagrams/system-context.mmd, container-view.mmd, component-view.mmd, dependency-view.mmd, call-flow-view.mmd |
| Phase 13: Final Summary | Complete | application-architecture-summary.md |

---

## Output File Checklist

| File | Exists | Evidence-Backed |
|---|---|---|
| system-inventory.json | Yes | azure.yaml, docker-compose.yml, launchSettings.json cited |
| module-boundary-map.json | Yes | Namespace + service + DbSet evidence per module |
| component-registry.json | Yes | Source files cited per component |
| application-interface-catalogue.json | Yes | Source endpoints and inferred endpoints distinguished |
| dependency-graph.json | Yes | 27 nodes, 23 edges, 1 cycle identified |
| call-flow-map.json | Yes | 5 flows, file + line reasoning per step |
| architecture-pattern-report.md | Yes | 6 evidence items for Clean Architecture |
| architecture-violation-register.json | Yes | 9 violations, each with source file evidence |
| application-risk-register.json | Yes | 10 risks, each with severity + evidence |
| strangler-candidate-report.md | Yes | 5 modules ranked, migration sequence proposed |
| forward-engineering-input-map.md | Yes | 7 sections, source-grounded recommendations |
| open-questions.md | Yes | 12 questions with blocking impact |
| extraction-audit.md | Yes | This file |
| diagrams/system-context.mmd | Yes | C4 context view |
| diagrams/container-view.mmd | Yes | C4 container + component view |
| diagrams/component-view.mmd | Yes | Flowchart, components with violations marked |
| diagrams/dependency-view.mmd | Yes | Module-level dependencies, violations marked with dashed lines |
| diagrams/call-flow-view.mmd | Yes | Sequence diagrams for FLOW-001, FLOW-003, FLOW-005 |
| application-architecture-summary.md | Yes | 15-section master summary |

---

## Quality Checks

### No Hallucination Check

| Area | Verdict |
|---|---|
| Source file paths cited | All citations reference files from Layer 1 extraction data or azure.yaml/docker-compose.yml |
| Line number claims | Line numbers provided where source was available in extraction; omitted where not confirmed |
| Endpoint claims | Confirmed endpoints (authenticated, catalog-brands) distinguished from inferred endpoints with [inferred] labels |
| Missing sources acknowledged | Web project not in extraction — flagged as APP-RISK-005 and OQ-001; not guessed |
| Unknowns marked | All FLOW-002, FLOW-003, FLOW-004 entry points marked as "unknown — not in extraction" |
| Confidence scores | All findings include confidence scores (0.75–0.99 range) |

### Do Not Modify Legacy Code Check

| Check | Verdict |
|---|---|
| No source files modified | PASS — all writes went to test-run/D1-application-architecture/ only |
| No source code generated | PASS — only analysis, documentation, and diagrams produced |
| No rename / refactor | PASS |
| No deletion of source files | PASS |

### Coverage Assessment

| Area | Coverage | Gap |
|---|---|---|
| PublicApi project | High | AuthenticateEndpoint, CatalogBrandListEndpoint fully analyzed |
| ApplicationCore — services | High | BasketService, OrderService, UriComposer fully analyzed |
| ApplicationCore — entities | High | Basket, Order, CatalogItem, Buyer entities analyzed |
| Infrastructure | High | EfRepository, CatalogContext, IdentityTokenClaimService analyzed |
| BlazorAdmin | High | CustomAuthStateProvider, HttpService, CatalogItemService, CachedDecorator analyzed |
| Web project | None | Not in Layer 1 extraction — critical gap |
| Test projects | None | Not in extraction |
| BlazorShared | Partial | Models known via usage; project not directly extracted |

---

## Risk Register Validation

| Risk | Confirmed via Evidence | Confidence |
|---|---|---|
| APP-RISK-001 Shared CatalogContext | Yes — CatalogContext.cs DbSets | 0.99 |
| APP-RISK-002 Hardcoded JWT secret | Yes — AuthorizationConstants.cs | 0.99 |
| APP-RISK-003 OrderService→Basket | Yes — OrderService.cs constructor | 0.95 |
| APP-RISK-004 Generic EfRepository | Yes — EfRepository.cs | 0.90 |
| APP-RISK-005 Web project gap | Yes — azure.yaml, no Web source in extraction | 0.99 |
| APP-RISK-006 Buyer unused | Yes — no DbSet, no service registration | 0.80 |
| APP-RISK-007 Client-side join | Yes — CatalogItemService.cs Task.WhenAll | 0.90 |
| APP-RISK-008 Two DbContexts | Yes — Dependencies.cs dual registration | 0.95 |
| APP-RISK-009 Basket transfer | Yes — BasketService.cs TransferBasketAsync | 0.90 |
| APP-RISK-010 ApplyConfigurationsFromAssembly | Yes — CatalogContext.cs | 0.88 |

---

## Architecture Violation Validation

| Violation | Severity | Evidence | Actionable |
|---|---|---|---|
| ARCH-VIOL-001 Shared context | High | CatalogContext.cs 7 DbSets | Yes — split plan in forward-engineering-input-map.md |
| ARCH-VIOL-002 Order→Basket | Medium | OrderService.cs IRepository<Basket> | Yes — CheckoutDTO recommendation |
| ARCH-VIOL-003 Hardcoded secret | Critical | AuthorizationConstants.cs | Yes — Key Vault migration |
| ARCH-VIOL-004 EmailSender stub | Low | EmailSender.cs | Yes — implement before production |
| ARCH-VIOL-005 Buyer dead code | Low | No service/DbSet found | Requires human verification |
| ARCH-VIOL-006 Fat OrderService | Low | OrderService.cs single method | Yes — saga pattern recommendation |
| ARCH-VIOL-007 Frontend coupling | Medium | CatalogItemService.cs join | Yes — enrich catalog-items response |
| ARCH-VIOL-008 async void | Low | List.razor.cs | Yes — change to async Task |
| ARCH-VIOL-009 HttpService null | Medium | HttpService.cs | Yes — Result<T> pattern |

---

## Open Items Requiring Follow-Up

See open-questions.md for full list. Summary of critical blockers:

1. **OQ-001** — Web project source extraction is required before architecture is complete
2. **OQ-004** — JWT secret rotation required before any migration work
3. **OQ-005** — DEFAULT_PASSWORD audit required before any migration work
4. **OQ-007** — /User endpoint server unknown; affects auth service design
5. **OQ-008** — Basket cleanup after checkout unknown; affects order service design
