All 19 output files are now complete. Here is the full inventory of what was produced:

---

## Extraction Complete — All 19 Files Written

**Output directory:** `results/aa-outputs/D1-application-architecture/`

### JSON Files (Stages 1–9)
| File | Stage | Contents |
|---|---|---|
| `system-inventory.json` | 1 | 6 apps/libraries, 3 Docker units, Azure deployment |
| `module-boundary-map.json` | 2 | 6 modules with coupling scores |
| `component-registry.json` | 3 | 27 components with risk flags |
| `application-interface-catalogue.json` | 4 | 12 interfaces (8 REST, 2 Blazor, 2 inferred) |
| `dependency-graph.json` | 5 | 18 nodes, 24 edges, 1 cross-module cycle |
| `call-flow-map.json` | 6 | 6 end-to-end call flows |
| `architecture-violation-register.json` | 8 | 9 violations (1 Critical, 4 High) |
| `application-risk-register.json` | 9 | 10 risks (1 Critical, 4 High, 3 prod blockers) |

### Markdown Files (Stages 7, 10–13)
| File | Contents |
|---|---|
| `architecture-pattern-report.md` | Clean Architecture + 6 patterns + 7 anti-patterns |
| `strangler-candidate-report.md` | 4 extraction candidates with ordered migration plan |
| `forward-engineering-input-map.md` | 15 confirmed facts, 7 decision points, gap analysis |
| `open-questions.md` | 22 open questions across 6 categories |
| `extraction-audit.md` | Source coverage map, stage completion, rules compliance |
| `application-architecture-summary.md` | Final summary |

### Mermaid Diagrams
| File | Type |
|---|---|
| `diagrams/system-context.mmd` | C4 Context |
| `diagrams/container-view.mmd` | C4 Container |
| `diagrams/component-view.mmd` | Component graph with risk annotations |
| `diagrams/dependency-view.mmd` | Project + package dependency graph |
| `diagrams/call-flow-view.mmd` | Sequence: Auth + Catalog list + Checkout |

### Top 3 Production Blockers Found
1. **RISK-001** — Hardcoded `JWT_SECRET_KEY` and `DEFAULT_PASSWORD` in `AuthorizationConstants.cs` — any repo reader can forge admin JWT tokens
2. **RISK-002** — `EmailSender` is a stub (`Task.CompletedTask`) — all emails silently dropped
3. **RISK-008** — Admin catalog mutation endpoints (POST/PUT/DELETE) — authorization enforcement unknown (source not in Layer 1)
