# Confidence Report

## Confidence Summary

| Area | Confidence | Evidence |
|---|---|---|
| Project/deployable inventory | High | `system-inventory.json` and inventory outputs identify project files and deployable candidates. |
| Component detection | Medium/High | 310 components detected; 0 major production components have Unknown type/layer; 40 total Unknown including support/test artifacts. |
| API/interface detection | Medium/High | 55 interfaces detected; 33 API contracts have confidence >= 0.85. |
| Dependency graph shape | High | 534 edges; invalid graph endpoints after normalization: 0. |
| Capability grouping | Medium | 13 capability candidates; average capability confidence 0.8. |
| Call flows | Medium | 55 flows detected; 55 traced/coverage-marker flows and 0 partial flows. |
| Test/runtime evidence | Medium/High | Static test-source evidence is captured; runtime status: not_run; runtime projects: 0. |
| External boundary purpose | Medium/Low | External targets are detected as candidates; purpose/ownership still needs confirmation. |

## Why Confidence Is Lower In Some Areas

- Static parsing cannot prove complete runtime route coverage where framework conventions expand routes dynamically.
- Dynamic dispatch and framework conventions can still limit call-flow completeness.
- Capability grouping is inferred from names, folders, modules, routes, components, and dependencies.
- Unknown component classifications may hide support classes or architecture-significant pieces.

## How To Increase Confidence

1. Confirm open questions with application owners.
2. Add contract tests for preserved API contracts.
3. Add parser support for language/framework-specific call graphs.
4. Review any remaining major Unknown components and test-project inclusion policy.
5. Validate external dependency purpose from runtime config and deployment knowledge.
