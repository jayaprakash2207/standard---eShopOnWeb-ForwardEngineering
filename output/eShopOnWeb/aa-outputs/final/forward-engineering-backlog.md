# Forward Engineering Backlog

This backlog converts architecture evidence into planning tasks. It is not an implementation task list yet.

| ID | Priority | Title | Source | Acceptance / Done When |
|---|---|---|---|---|
| FE-001 | High | Confirm authoritative system name and deployment ownership | open-questions.md | System name and deployable ownership are confirmed or intentionally kept unknown. |
| FE-002 | High | Review future boundary for CAP-001 Catalog | business-capability-map.json | Architect records preserve/merge/extract decision with data ownership and API impact. |
| FE-003 | High | Review future boundary for CAP-002 Identity | business-capability-map.json | Architect records preserve/merge/extract decision with data ownership and API impact. |
| FE-004 | High | Review future boundary for CAP-004 Admin | business-capability-map.json | Architect records preserve/merge/extract decision with data ownership and API impact. |
| FE-005 | High | Review future boundary for CAP-005 Basket | business-capability-map.json | Architect records preserve/merge/extract decision with data ownership and API impact. |
| FE-006 | High | Review future boundary for CAP-006 Controllers | business-capability-map.json | Architect records preserve/merge/extract decision with data ownership and API impact. |
| FE-007 | High | Review future boundary for CAP-007 Order | business-capability-map.json | Architect records preserve/merge/extract decision with data ownership and API impact. |
| FE-008 | High | Review future boundary for CAP-013 Data | business-capability-map.json | Architect records preserve/merge/extract decision with data ownership and API impact. |
| FE-009 | High | Resolve architecture risk APP-RISK-001 | application-risk-register.json | Risk is accepted, mitigated, or converted into implementation constraints. |
| FE-010 | High | Resolve architecture risk APP-RISK-002 | application-risk-register.json | Risk is accepted, mitigated, or converted into implementation constraints. |
| FE-011 | High | Resolve architecture risk APP-RISK-003 | application-risk-register.json | Risk is accepted, mitigated, or converted into implementation constraints. |
| FE-012 | High | Resolve architecture risk APP-RISK-004 | application-risk-register.json | Risk is accepted, mitigated, or converted into implementation constraints. |
| FE-013 | Medium | Resolve architecture risk APP-RISK-005 | application-risk-register.json | Risk is accepted, mitigated, or converted into implementation constraints. |
| FE-014 | Medium | Resolve architecture risk APP-RISK-006 | application-risk-register.json | Risk is accepted, mitigated, or converted into implementation constraints. |
| FE-015 | Medium | Resolve architecture risk APP-RISK-007 | application-risk-register.json | Risk is accepted, mitigated, or converted into implementation constraints. |
| FE-016 | Medium | Resolve architecture risk APP-RISK-008 | application-risk-register.json | Risk is accepted, mitigated, or converted into implementation constraints. |
| FE-017 | Medium | Create contract test for API-CONTRACT-001 POST /api/authenticate | api-contract-preservation-map.json | Forward implementation can prove behavioral compatibility or intentional redesign. |
| FE-018 | Medium | Create contract test for API-CONTRACT-002 GET /api/catalog-brands | api-contract-preservation-map.json | Forward implementation can prove behavioral compatibility or intentional redesign. |
| FE-019 | Medium | Create contract test for API-CONTRACT-003 GET /api/catalog-items/{catalogItemId} | api-contract-preservation-map.json | Forward implementation can prove behavioral compatibility or intentional redesign. |
| FE-020 | Medium | Create contract test for API-CONTRACT-004 GET /api/catalog-items | api-contract-preservation-map.json | Forward implementation can prove behavioral compatibility or intentional redesign. |
| FE-021 | Medium | Create contract test for API-CONTRACT-005 POST /api/catalog-items | api-contract-preservation-map.json | Forward implementation can prove behavioral compatibility or intentional redesign. |
| FE-022 | Medium | Create contract test for API-CONTRACT-006 DELETE /api/catalog-items/{catalogItemId} | api-contract-preservation-map.json | Forward implementation can prove behavioral compatibility or intentional redesign. |
| FE-023 | Medium | Create contract test for API-CONTRACT-007 PUT /api/catalog-items | api-contract-preservation-map.json | Forward implementation can prove behavioral compatibility or intentional redesign. |
| FE-024 | Medium | Create contract test for API-CONTRACT-008 GET /api/catalog-types | api-contract-preservation-map.json | Forward implementation can prove behavioral compatibility or intentional redesign. |
| FE-025 | Medium | Review API contract API-CONTRACT-009 unknown /{controller:slugify=Home}/{action:slugify=Index}/{id?} | api-contract-preservation-map.json | Contract is classified as preserve, redesign, or retire with owner approval. |
| FE-026 | Medium | Review API contract API-CONTRACT-010 unknown ASP.NET Razor Pages route registration | api-contract-preservation-map.json | Contract is classified as preserve, redesign, or retire with owner approval. |
| FE-027 | Medium | Review API contract API-CONTRACT-011 unknown /index.html | api-contract-preservation-map.json | Contract is classified as preserve, redesign, or retire with owner approval. |
| FE-028 | Medium | Review API contract API-CONTRACT-039 unknown /logout | api-contract-preservation-map.json | Contract is classified as preserve, redesign, or retire with owner approval. |
| FE-029 | Medium | Review API contract API-CONTRACT-040 unknown /admin | api-contract-preservation-map.json | Contract is classified as preserve, redesign, or retire with owner approval. |
| FE-030 | Medium | Review API contract API-CONTRACT-051 GET /{handler?} | api-contract-preservation-map.json | Contract is classified as preserve, redesign, or retire with owner approval. |
| FE-031 | Medium | Review API contract API-CONTRACT-053 unknown .NET application bootstrap Program.cs | api-contract-preservation-map.json | Contract is classified as preserve, redesign, or retire with owner approval. |
| FE-032 | Medium | Review API contract API-CONTRACT-054 unknown .NET application bootstrap Program.cs | api-contract-preservation-map.json | Contract is classified as preserve, redesign, or retire with owner approval. |
| FE-033 | Medium | Resolve open architecture question | open-questions.md | Confirm the authoritative system name; evidence packs leave system_name as unknown. |
| FE-034 | Medium | Resolve open architecture question | open-questions.md | Confirm ownership and boundaries for weak or unknown module candidates: Admin, ApplicationCore, Basket, Catalog, DataAccess, Identity, Order, Web. |
| FE-035 | Medium | Resolve open architecture question | open-questions.md | Review the 0 components with unknown module ownership before finalizing module boundaries. |
| FE-036 | Medium | Resolve open architecture question | open-questions.md | Review the 40 components with Unknown type/layer classification to decide whether they are architecture-significant. |
| FE-037 | Medium | Resolve open architecture question | open-questions.md | Review 0 partial call flows before using them as behavior-preservation contracts. |
| FE-038 | Medium | Resolve open architecture question | open-questions.md | Confirm whether detected module cycles are real architecture cycles or artifacts of static dependency resolution: Admin -> ApplicationCore -> Basket -> Catalog -> DataAccess -> Identity -> Order -> Web. |
