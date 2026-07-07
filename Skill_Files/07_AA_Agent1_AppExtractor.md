# SKILL FILE: AA Agent 1 — Application Extractor

> Skill ID: `SKL-AA1` | Version: `1.0.0` | Status: `ACTIVE`
> SDLC Phase: `Analysis`
> Domain: `Reverse Engineering` | Sub-Domain: `Code Analysis`
> Owner: `[Team / Member]` | Last Updated: `2026-06-01`

---

## BLOCK 1 — IDENTITY

### 1.1 Skill Metadata

| Field | Value |
|-------|-------|
| Skill ID | `SKL-AA1` |
| Skill Name | AA Agent 1 — Application Extractor |
| Version | `1.0.0` |
| SDLC Phase | `Analysis` |
| Domain | `Reverse Engineering` |
| Sub-Domain | `Code Analysis` |
| Owner | `[Team / Member]` |
| Tags | `application-architecture`, `module-boundaries`, `dependency-graph`, `call-flow`, `strangler-migration`, `agent-1-of-2` |
| Status | `Active` |
| Paired With | `SKL-AA2` (AA Agent 2 — Quality Review) — hard dependency, `SKL-AA2` reviews this skill's complete output set |

### 1.2 Goal & Success Criteria

**Primary Goal:**
> Analyze a legacy application codebase and produce a production-grade Application Architecture output — explaining the internal software structure (modules, layers, components, dependencies, call flows, patterns, violations, and migration candidates) — that supports both SDLC reverse engineering and forward engineering.

**Secondary Goals:**
- Answer, with evidence: what is this application; what applications/projects exist in the repo; what are the deployable units; what are the modules and what does each own; what are the layers; what components exist and how do they depend on each other; what are the entry points; what are the important call flows; what architecture pattern does the application follow; where are the architecture violations; what migration risks exist; which modules are better strangler/forward-engineering candidates; what open questions require human review
- Document the actual legacy architecture exactly as it is — messy parts, violations, weak boundaries, tight coupling, unclear ownership, risky flows, migration blockers, and unknowns included — never make it look cleaner than it is

**Success Definition:**
> A run is successful when all 14 required output files (13 named files + the `diagrams/` folder with 5 Mermaid diagrams) exist under `OUTPUT_ROOT/D1-application-architecture/`, every major finding cites source evidence (file path, line number where available, class/function/component name, confidence score), no fabricated module ownership/call flows/technology details/business rules/deployment details/security details/data ownership appear anywhere, and the run scores an average ≥ 4.0 out of 5 across the 10 Quality Parameters (§4.2) with no single parameter below 3.0.

**What This Skill Does NOT Do:**
> This is Application Architecture only.
- Does not perform Business Architecture, Data Architecture, Technology Architecture, a security deep dive, QA test generation, or BRD generation unless explicitly requested later
- Does not modify, refactor, rename, delete, format, or generate production code inside the legacy repo
- Does not send the entire raw repository into the model — parses structured evidence first, reasons second
- Does not make the architecture look cleaner than it actually is

---

## BLOCK 2 — ACTIVATION

### 2.1 Trigger Conditions

**Explicit Triggers** _(user states these directly)_:
- A request to analyze/document/reverse-engineer the "application architecture" or "internal software structure" of a legacy codebase
- Providing `LEGACY_REPO_PATH`, `OUTPUT_ROOT`, and (optionally) `LAYER1_PATH` and asking for an application architecture extraction

**Implicit Signals** _(infer from conversation context or orchestrator routing)_:
- The orchestrator has classified the request as belonging to the Application Architecture reverse-engineering pipeline (as opposed to Business, Data, or Technology Architecture)
- The user wants module boundaries, a dependency graph, call-flow traces, or strangler/migration candidates identified

**Activation Keywords / Patterns:**
```
"application architecture" | "internal software structure" | "module boundaries" |
"dependency graph" | "call flow" | "strangler candidates" | "migration candidates"
```

### 2.2 Pre-conditions & Guards

**Must Be True Before Activation:**
- [ ] `LEGACY_REPO_PATH` (the codebase root) is provided
- [ ] `OUTPUT_ROOT` (where outputs should be written) is provided
- [ ] This skill runs inside a coding agent (Claude Code, or similar) with file read/write access to `OUTPUT_ROOT`

**Disqualifiers** _(do NOT activate if any of these are true)_:
- [ ] No `LEGACY_REPO_PATH` is provided
- [ ] The request is for Business, Data, Technology Architecture, a security deep dive, QA test generation, or BRD generation without an explicit, separate follow-up request for those
- [ ] The user is asking to modify or refactor the legacy source code itself — that is out of scope; this is a read-only reverse-engineering task

---

## BLOCK 3 — CONTEXT

> _Block 3 is the most critical block for Reverse Engineering skills. Precision here directly determines output accuracy._

### 3.1 Environment Context

| Dimension | Details |
|-----------|---------|
| Target Language(s) | Language-agnostic — any repo with recognizable project/solution/package files |
| Framework(s) | Any — detected during Stage 1 System Discovery |
| Platform / OS | Runs inside a coding agent (Claude Code, Codex, or similar) with file system access |
| Database Type | Detected via `database.json` (Layer 1) for data-access dependency evidence (Stage 5); schema itself is `SKL-DA1`'s domain |
| Architecture Pattern | Detected in Stage 7, not assumed in advance |
| Available Tools | Read access to `LEGACY_REPO_PATH`; write access limited to `OUTPUT_ROOT` |
| Repository Access | `Read-Write` (write scoped to `OUTPUT_ROOT` only — the legacy repo itself is strictly read-only, §5.1) |
| Authentication Level | None required |
| **Layer 1 JSON (accelerator, partial exception for Stages 6 & 8)** | `source_code.json` (classes, methods, fields, constructor dependencies, namespaces), `database.json` (tables/columns/relationships), `config.json` (config keys/values), `logs.json` (log patterns) are the PRIMARY input, used instead of raw source reads wherever they cover the needed evidence. **Exception:** Stage 6 (Call Flow Tracing) requires method bodies to trace actual call chains — raw source files are read directly for this stage. Stage 8 (Violation Detection) requires line-level verification of constructor injection patterns — raw source files are read directly for this stage too. Any item marked `unknown` or missing from Layer 1 JSON is also read directly. Entity files, service class signatures, and config files already fully represented in Layer 1 JSON are never re-read. |

### 3.2 Artifact Taxonomy

> _Which artifact types can this skill ingest and analyze?_

| Artifact Type | Supported | Accepted Formats | Notes |
|---------------|-----------|-----------------|-------|
| Source Code | ✓ | Any — via `source_code.json` (Layer 1) primarily; raw reads for Stage 6/8 and `unknown` gaps | Classes, methods, fields, constructor dependencies |
| Database Schema | ✓ (dependency evidence only) | Via `database.json` (Layer 1) | Used for Stage 5 data-access dependencies, not schema documentation itself |
| API Contracts | ✓ | Route/controller declarations, GraphQL resolvers, SOAP/WCF endpoints | Stage 4 Interface/Entry Point Discovery |
| Configuration Files | ✓ | Via `config.json` (Layer 1) | Stage 1 system discovery, entry points |
| UI Wireframes / Designs | ✗ | — | Out of scope |
| Application Logs / Traces | ✓ (limited) | `logs.json` (Layer 1) | Stage 6 call flow tracing signals |
| Test Cases | ✓ (limited, as `test_project` type) | Any test framework | Classified as a project type in Stage 1; not a primary evidence source otherwise |
| Documentation | ✗ | — | Not a primary input for this skill |
| Infrastructure as Code | ✗ | — | Out of scope — belongs to `SKL-TA1` |
| Binary / Compiled Code | ✗ | — | Cannot be scanned |
| Solution/Project/Package Manifests | ✓ | `*.sln`, `*.csproj`, `pom.xml`, `build.gradle`, `settings.gradle`, `package.json`, `angular.json`, `vite.config.*`, `webpack.config.*`, `requirements.txt`, `pyproject.toml`, `composer.json` | Stage 1 System Discovery's primary search targets |

### 3.3 Domain Knowledge References

**Architectural Patterns to Recognise** _(Stage 7)_:
- Layered Monolith, N-tier Architecture, Clean Architecture, Hexagonal/Ports and Adapters, Modular Monolith, Microservices, Big Ball of Mud, Anemic Domain Model, Rich Domain Model/DDD, Unknown

**Design Patterns to Detect** _(component types, Stage 3)_:
- Controller, Service, Repository, Entity, DTO, ViewModel, Mapper, Validator, Handler, Command, Query, Gateway, Client, Middleware, Filter, FrontendComponent, FrontendService, RouteGuard, StateStore, BatchJob, ScheduledJob, MessageConsumer, Unknown

**Standards & Protocols:**
- Layer classification: Presentation/UI, API, Application Service, Domain, Infrastructure, Data Access, Integration, Cross-cutting, Test, Unknown
- Coupling metrics: Efferent coupling (how many other modules this module depends on — high efferent = risky to extract early, needs many others) and Afferent coupling (how many modules depend on this module — high afferent = risky to change, many others depend on it)

**Domain Glossary:**

| Term | Definition |
|------|-----------|
| Deployable unit | An application/project in the repo that can be independently deployed (backend API, frontend SPA, worker, batch job) as opposed to a shared library |
| Module boundary quality | Strong (clear ownership, clear entry points, limited dependencies, few cross-module leaks) / Moderate (mostly clear, some shared components or unclear dependencies) / Weak (heavy cross-module dependencies, unclear ownership, circular dependencies, shared services/data everywhere) / Unknown (insufficient evidence) |
| Strangler candidate | A module assessed for how good a first-migration-target it is, ranked Good Early Candidate / Possible Candidate With Refactoring / Poor Candidate / Blocked / Unknown |
| Open question | Any item this skill could not determine from the codebase — must be logged, never fabricated |

**RE Checklist for This Sub-Domain:**
> _Specific things this skill must look for in this sub-domain._
- [ ] Every deployable unit and supporting project is identified with type, framework, and evidence
- [ ] Every module has its boundary quality assessed with multiple corroborating signals, not folder names alone
- [ ] Every component is classified by both type and layer
- [ ] Every entry point (HTTP API, frontend route, scheduled job, message consumer, batch job, CLI, webhook) is catalogued
- [ ] Every dependency edge, cycle, and high-coupling node is captured in the dependency graph
- [ ] At least the most important call flows are traced end-to-end from entry point to persistence/integration
- [ ] The architecture pattern is stated with evidence and confidence, including competing possible patterns
- [ ] Every violation category is checked, not just the obvious ones
- [ ] Every module is classified for strangler/migration suitability with reasoning
- [ ] All 5 required Mermaid diagrams are generated, best-effort, with an "unknown items marked as unknown" note

---

## BLOCK 4 — INTERFACE

### 4.1 Input Specification

#### Required Inputs

| Field | Type | Format / Example | Description |
|-------|------|-----------------|-------------|
| `LEGACY_REPO_PATH` | string | Absolute path | The legacy codebase root to analyze |
| `OUTPUT_ROOT` | string | Absolute path | Where architecture outputs should be written |

#### Optional Inputs

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `LAYER1_PATH` | string | none | Absolute path to Layer 1 JSON output folder (`source_code.json`, `database.json`, `config.json`, `logs.json`) — if absent, falls back to raw source scanning throughout |

#### Input Validation Rules
- `LEGACY_REPO_PATH` must contain at least one recognizable project/solution/package file (§3.1 System Discovery search list)
- `OUTPUT_ROOT` must be writable and must NOT be inside `LEGACY_REPO_PATH` (this skill never writes into the legacy repo)

#### Input Rejection Criteria
- `LEGACY_REPO_PATH` is absent or contains no recognizable project structure
- `OUTPUT_ROOT` is not writable

### 4.2 Output Specification

#### Standard Output Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `skill_id` | string | ✓ | `SKL-AA1` |
| `run_id` | string | ✓ | `RUN-YYYYMMDD-HHMMSS` |
| `confidence_score` | float 0–1 | ✓ | Computed per §6.2 formula |
| `analysis_depth` | string | ✓ | `module` for Stages 1-5, 7-13; `function` for Stage 6 (Call Flow Tracing) and Stage 8 (Violation Detection), which read raw source directly |
| `coverage_pct` | float 0–1 | ✓ | Files/artifacts produced with meaningful content, out of the 14 required (13 files + diagrams folder) — mirrors Quality Parameter 1 (Completeness) |
| `findings` | object | ✓ | Maps each required output filename to a short description of its top-level shape (not full contents — full contents are written to disk under `OUTPUT_ROOT/D1-application-architecture/`) |
| `gaps` | array | ✓ | All `open_questions` entries across every stage output |
| `recommendations` | array | | Top 5 architecture findings and top 5 risks, per the Final Response format |
| `handoff_context` | object | | Forward Engineering Input Map contents, packaged for `SKL-AA2` and `SKL-FOUNDATION` |

#### Required Output Folder Structure

```text
OUTPUT_ROOT/
  D1-application-architecture/
    application-architecture-summary.md
    system-inventory.json
    module-boundary-map.json
    component-registry.json
    application-interface-catalogue.json
    dependency-graph.json
    call-flow-map.json
    architecture-pattern-report.md
    architecture-violation-register.json
    application-risk-register.json
    strangler-candidate-report.md
    forward-engineering-input-map.md
    open-questions.md
    extraction-audit.md
    diagrams/
      system-context.mmd
      container-view.mmd
      component-view.mmd
      dependency-view.mmd
      call-flow-view.mmd
```

> If a file cannot be fully produced, it is still created with `Status: incomplete`, `Reason: <why>`, `Open questions: <questions>` — never silently omitted.

#### `findings` Object Structure _(skill-specific — maps to the files above)_

```json
{
  "skill_id": "SKL-AA1",
  "run_id": "RUN-20260601-200000",
  "confidence_score": 0.84,
  "analysis_depth": "module",
  "coverage_pct": 1.0,
  "findings": {
    "system-inventory.json": "system_name, repo_root, applications[] (name, type, framework, deployable, evidence[], confidence), supporting_projects[], open_questions[]",
    "module-boundary-map.json": "modules[] (module_id, name, responsibility, source_folders[], main_components[], entry_points[], depends_on_modules[], used_by_modules[], afferent/efferent coupling, boundary_quality, confidence, evidence[], open_questions[])",
    "component-registry.json": "components[] (component_id, name, type, layer, module, file, start/end_line, public_methods[], dependencies[], called_by[], risk_flags[], confidence, evidence[])",
    "application-interface-catalogue.json": "interfaces[] (interface_id, type, method, path_or_name, owner_module, entry_component, called_service, visibility, evidence[], confidence, open_questions[])",
    "dependency-graph.json": "nodes[], edges[] (from, to, relationship, evidence[]), cycles[] (cycle, severity, impact), high_coupling_components[], high_coupling_modules[]",
    "call-flow-map.json": "flows[] (flow_id, name, entry_point, steps[] (step, component, layer, module, operation), modules_touched[], external_systems_touched[], data_access_components[], risk_flags[], confidence, open_questions[])",
    "architecture-pattern-report.md": "detected pattern, confidence score, evidence, why selected, competing possible patterns, architecture violations, forward engineering implications",
    "architecture-violation-register.json": "violations[] (violation_id, type, description, affected_module, affected_components[], evidence[], severity, migration_impact, recommendation, confidence)",
    "application-risk-register.json": "risks[] (risk_id, category, description, affected_modules[], affected_components[], severity, forward_engineering_impact, evidence[], recommendation, confidence)",
    "strangler-candidate-report.md": "module ranking, reason for ranking, risks, recommended migration sequencing, human review questions",
    "forward-engineering-input-map.md": "candidate future modules/services, APIs to preserve/redesign, important call flows to preserve, modules requiring deeper review, violations not to copy, migration blockers, recommended modernization sequence",
    "open-questions.md": "consolidated list of every open_questions[] entry across all stage outputs",
    "extraction-audit.md": "record of what was read via Layer 1 JSON vs raw source, and why",
    "diagrams/*.mmd": "5 Mermaid diagrams: system-context, container-view, component-view, dependency-view, call-flow-view"
  },
  "gaps": [
    { "area": "OrderService coupling", "reason": "constructor dependencies could not be fully resolved from source_code.json alone; raw source needed for confirmation", "severity": "Med" }
  ],
  "recommendations": [
    "Top finding: modular monolith with 4 clear domain modules and 1 shared-kernel module",
    "Top risk: circular dependency between Ordering and Catalog modules (ARCH-VIOL-003)"
  ],
  "handoff_context": {
    "candidate_future_services": ["Ordering", "Catalog"],
    "migration_blockers": ["Shared database table between Ordering and Payments"]
  }
}
```

#### Quality Criteria _(the 10 Quality Parameters used to judge production-grade output — reused in Block 6.1 and Block 8.2)_

| # | Parameter | What "5 = production-grade" looks like |
|---|---|---|
| 1 | Completeness | All 14 required files present and meaningful (not just all present but shallow) |
| 2 | Source Traceability | Nearly every finding has a file path, line number where possible, class/method/component name, and an evidence explanation |
| 3 | No Hallucination | `unknown` used honestly when evidence is missing; open questions created; confidence scores included; no invented Kubernetes/microservices/domain-ownership/cloud-provider/API-gateway claims without file evidence |
| 4 | Module Boundary Quality | `module-boundary-map.json` modules are clearly justified with evidence — name, responsibility, source folders, main components, entry points, dependencies, coupling scores, boundary quality, confidence |
| 5 | Component Classification Quality | `component-registry.json` accurately classifies controllers, services, repositories, entities, DTOs, validators, handlers, clients, gateways, frontend components, jobs/consumers |
| 6 | Dependency Graph Usefulness | `dependency-graph.json` identifies component/module dependencies, cycles, high-coupling modules/components, and layer violations in a way that supports real migration decisions |
| 7 | Call Flow Quality | `call-flow-map.json` shows entry point, ordered steps, component/layer/module per step, external systems touched, data access touched, risk flags — clear flows from entry to persistence/integration |
| 8 | Architecture Pattern Accuracy | `architecture-pattern-report.md` pattern is evidence-backed and nuanced, with violations and competing patterns considered |
| 9 | Risk Register Quality | `application-risk-register.json` risks are actionable: risk id, category, severity, affected module/component, evidence, forward engineering impact, recommendation, confidence |
| 10 | Forward Engineering Usefulness | `forward-engineering-input-map.md` and the strangler report are directly useful for modernization planning: which modules can become future services, which shouldn't migrate first, which APIs/flows must be preserved, which violations shouldn't be copied, what migration sequence is recommended |

### 4.3 Confidence & Evidence Tagging Schema

> _Every finding in the output must carry a tag declaring how it was obtained._

#### Tag Taxonomy

| Tag | Symbol | Definition | Downstream Action |
|-----|--------|-----------|------------------|
| EXTRACTED | `✅` | Directly evidenced by file+line+class/function/component name, with a stated confidence ≥ 0.85 | Proceed; no review needed unless conflicted |
| PARTIAL | `⚠️` | Evidenced but with a stated confidence in the 0.60–0.84 range — real evidence, some uncertainty | Include with warning flag; surface in `gaps`/`open_questions` |
| INFERRED | `〰️` | Evidenced only weakly (naming/pattern inference), stated confidence 0.40–0.59 | Mark as inferred; `SKL-AA2` to verify |
| UNKNOWN | `❓` | The literal `unknown` value used per this skill's own Non-Negotiable Rule 2.1, or confidence < 0.40 | Escalate; populate `open_questions`; do NOT fabricate |

**Legacy tag mapping** _(this skill's original per-finding numeric `confidence` field, mapped onto the taxonomy above)_:

| Original value | Maps to |
|---|---|
| `confidence` ≥ 0.85, with file+line+name evidence cited | `EXTRACTED` |
| `confidence` 0.60–0.84 | `PARTIAL` |
| `confidence` 0.40–0.59 | `INFERRED` |
| Literal string `"unknown"` (for module ownership, call flows, technology details, API behavior, business rules, deployment details, security details, data ownership per Non-Negotiable Rule 2.1) or `confidence` < 0.40 | `UNKNOWN` |

#### Mandatory Tagging Rules

- Every entry in every JSON output's array carries (or implies, via its numeric `confidence` field) a `confidence_tag` per the mapping above
- `confidence_score` (overall) is computed per §6.2
- `INFERRED` and `UNKNOWN` findings always appear in `open-questions.md`
- Per Non-Negotiable Rule 2.1: module ownership, call flows, technology details, API behavior, business rules, deployment details, security details, and data ownership are NEVER invented — if undeterminable, the literal value is `unknown`, not a guess

#### Display Convention

```
✅ EXTRACTED — confidence ≥ 0.85, evidence: [file:line, class/function/component]
⚠️ PARTIAL  — confidence 0.60-0.84, evidence: [file:line, class/function/component]
〰️ INFERRED — confidence 0.40-0.59, weak/naming-based evidence only
❓ UNKNOWN  — literal "unknown" value; added to open-questions.md
```

---

## BLOCK 5 — EXECUTION

### 5.1 Constraints & Guardrails

**Hard Constraints _(MUST NOT do these under any circumstances — Non-Negotiable Rules 2.1–2.5)_:**
- **2.1 Do not hallucinate.** If something cannot be determined from the codebase, write `unknown` and add it to `open-questions.md`. Never invent: module ownership, call flows, technology details, API behavior, business rules, deployment details, security details, data ownership.
- **2.2 Source evidence is mandatory.** Every important finding must include: source file path, line number if available, class/function/component name, reasoning summary, confidence score.
- **2.3 Do not modify legacy source code.** This is a reverse-engineering task — never change, refactor, rename, delete, format, or generate production code inside the legacy repo. All generated outputs go into `OUTPUT_ROOT`.
- **2.4 Do not scan junk folders.** Exclude unless explicitly needed: `.git/`, `node_modules/`, `bin/`, `obj/`, `target/`, `dist/`, `build/`, `coverage/`, `.vscode/`, `.idea/`, `*.min.js`, `*.map`, `*.lock` (when not needed for dependency analysis), large generated files, compiled binaries, logs.
- **2.5 Parse first, reason second.** Do not send the entire raw repo into the LLM. First extract structured evidence (files, projects, classes, functions, components, routes, dependencies, entry points, call chains), then use that evidence to produce architecture judgments.

**Soft Constraints _(PREFER NOT TO — may override with justification)_:**
- Prefer Layer 1 JSON over raw reads wherever it covers the needed evidence — override for Stage 6 (Call Flow Tracing) and Stage 8 (Violation Detection), which need method-body/line-level detail Layer 1 doesn't provide

**Scope Boundaries:**

| IN Scope | OUT of Scope |
|----------|-------------|
| System/module/component/interface discovery | Business Architecture, Data Architecture, Technology Architecture |
| Dependency graph and call flow tracing | Security deep dive |
| Architecture pattern and violation detection | QA test generation |
| Application risk register | BRD generation |
| Strangler/migration candidate analysis | Modifying, refactoring, or generating legacy source code |
| Forward engineering input map + diagrams | Sending the entire raw repo into the model without structured pre-extraction |

**Data Sensitivity Rules:**

| Data Type | Rule |
|-----------|------|
| PII (names, emails, IDs) | Not a focus of this skill; if encountered in code/config, field/class names only, never sample values |
| Credentials / Secrets | Never captured; this skill reads structure, not runtime secrets |
| Confidential Business Logic | Not interpreted by this skill (out of scope — Business Architecture is `SKL-BA1`/`SKL-BA2`'s job); component/call-flow structure only |
| Third-party IP / Licensed Code | Component/dependency names only, as declared in imports/manifests |

**Exclusion List** _(never scan these unless explicitly needed)_:
```
.git/            node_modules/    bin/             obj/
target/          dist/            build/           coverage/
.vscode/         .idea/           *.min.js         *.map
*.lock (when not needed for dependency analysis)
large generated files, compiled binaries, logs
```

### 5.2 Process & Methodology

> _13 sequential stages. Each stage's input, action, and output are defined below. This skill's chunking axis is stage-based, not domain/layer-based (§5.4) — a deliberate divergence from the BA/DA/TA pairs._

**Stage 1 — System Discovery**
- Input: repo root, solution/project/package/build files, folder structure. Search for: `*.sln`, `*.csproj`, `pom.xml`, `build.gradle`, `settings.gradle`, `package.json`, `angular.json`, `vite.config.*`, `webpack.config.*`, `requirements.txt`, `pyproject.toml`, `composer.json`
- Action: extract all projects/apps in the repo — backend projects, frontend projects, shared libraries, test projects, database/infrastructure projects, possible deployable units, supporting libraries
- Output: `system-inventory.json` — `{ system_name, repo_root, applications: [{ name, type: backend_api|frontend_spa|web_app|worker|batch_job|library|test_project|unknown, framework, deployable, evidence: [{file, reason}], confidence }], supporting_projects: [], open_questions: [] }`

**Stage 2 — Module Boundary Detection**
- Input: folder structure, namespaces/packages, controllers, services, entities, frontend routes, feature folders
- Action: identify application modules (e.g. Customer, Order, Payment, Catalog, Basket, Admin, Report, Notification, Authentication, Claim, Loan, Policy, Invoice). Do NOT assume folder names are always correct — use multiple corroborating signals: folder names, namespace/package prefixes, controller names, service names, entity names, route prefixes, frontend feature folders, shared dependencies
- Output: `module-boundary-map.json` — `{ modules: [{ module_id, name, responsibility, source_folders, main_components, entry_points, depends_on_modules, used_by_modules, afferent_coupling, efferent_coupling, boundary_quality: Strong|Moderate|Weak|Unknown, confidence, evidence, open_questions }] }`
- Boundary quality rules: **Strong** = clear folder/namespace ownership, clear entry points, limited dependencies, few cross-module leaks. **Moderate** = mostly clear but some shared components or unclear dependencies. **Weak** = heavy cross-module dependencies, unclear ownership, circular dependencies, shared services/data models everywhere. **Unknown** = insufficient evidence.

**Stage 3 — Component Discovery**
- Input: `source_code.json` (Layer 1) as primary input for class names, types, method signatures, constructor dependencies; raw source files only for items missing/marked `unknown` in Layer 1
- Action: classify each component by TYPE (Controller, Service, Repository, Entity, DTO, ViewModel, Mapper, Validator, Handler, Command, Query, Gateway, Client, Middleware, Filter, FrontendComponent, FrontendService, RouteGuard, StateStore, BatchJob, ScheduledJob, MessageConsumer, Unknown) and LAYER (Presentation/UI, API, Application Service, Domain, Infrastructure, Data Access, Integration, Cross-cutting, Test, Unknown)
- Output: `component-registry.json` — `{ components: [{ component_id, name, type, layer, module, file, start_line, end_line, public_methods, dependencies, called_by, risk_flags, confidence, evidence }] }`

**Stage 4 — Interface / Entry Point Discovery**
- Input: backend controllers, REST routes, GraphQL resolvers, SOAP/WCF endpoints, frontend routes, message listeners, scheduled jobs, batch scripts, CLI commands
- Action: extract HTTP APIs, frontend routes, scheduled jobs, message consumers, batch jobs, CLI commands, webhook handlers, public/internal interfaces
- Output: `application-interface-catalogue.json` — `{ interfaces: [{ interface_id, type: HTTP_API|FrontendRoute|ScheduledJob|BatchJob|MessageConsumer|CLI|Webhook|Unknown, method: GET|POST|PUT|DELETE|PATCH|unknown, path_or_name, owner_module, entry_component, called_service, visibility: external|internal|user_facing|admin|unknown, evidence, confidence, open_questions }] }`

**Stage 5 — Dependency Analysis**
- Input: imports, constructor injection, project references, method calls, service calls, repository calls, frontend API calls
- Action: extract component dependencies, module dependencies, project dependencies, layer dependencies, cycles, high-coupling components, cross-module references
- Output: `dependency-graph.json` — `{ nodes: [{id, type: component|module|external|project, module, layer}], edges: [{from, to, relationship: calls|imports|injects|references|reads|writes|publishes|consumes|unknown, evidence}], cycles: [{cycle, severity: Low|Medium|High, impact}], high_coupling_components: [], high_coupling_modules: [] }`
- Coupling rules: efferent coupling = how many other modules this module depends on (high = risky to extract early, needs many others); afferent coupling = how many modules depend on this module (high = risky to change, many others depend on it)

**Stage 6 — Call Flow Tracing** _(reads raw source directly — Layer 1 JSON insufficient, needs method bodies)_
- Input: interfaces, component registry, dependency graph, method call chains, repository calls, external calls
- Action: trace important flows from entry point to downstream components — e.g. `POST /api/orders/checkout → OrderController.Checkout → OrderService.PlaceOrder → BasketService.GetBasket → PaymentGateway.Charge → OrderRepository.Save`. If a full call flow cannot be traced, produce a partial flow and add an open question — never fabricate the missing steps.
- Output: `call-flow-map.json` — `{ flows: [{ flow_id, name, entry_point, steps: [{step, component, layer, module, operation}], modules_touched, external_systems_touched, data_access_components, risk_flags, confidence, open_questions }] }`

**Stage 7 — Architecture Pattern Detection**
- Input: system inventory, module map, component registry, dependency graph, call flows, layering evidence
- Action: detect the pattern from: Layered Monolith, N-tier Architecture, Clean Architecture, Hexagonal/Ports and Adapters, Modular Monolith, Microservices, Big Ball of Mud, Anemic Domain Model, Rich Domain Model/DDD, Unknown
- Output: `architecture-pattern-report.md` — must include detected pattern, confidence score, evidence, why this pattern was selected, competing possible patterns, architecture violations, forward engineering implications

**Stage 8 — Architecture Violation Detection** _(reads raw source directly for line-level constructor injection verification)_
- Input: component registry, dependency graph, call flows, component metrics, layering rules
- Action: detect: God Class, Fat Controller, Circular Dependency, Layer Violation, Controller directly accessing Repository, Service depending on UI layer, Domain depending on Infrastructure, Shared Utility Overuse, Shotgun Surgery Risk, Feature Envy, Dead Code Candidate, Cross-Module Leakage, Frontend-Backend Tight Coupling, Unknown Ownership
- Output: `architecture-violation-register.json` — `{ violations: [{ violation_id, type, description, affected_module, affected_components, evidence, severity: Low|Medium|High|Critical, migration_impact, recommendation, confidence }] }`

**Stage 9 — Application Risk Register**
- Input: all previous stage outputs
- Action: assess risks in categories: High Coupling, Unclear Module Boundary, Circular Dependency, Shared Data Model, Shared Service, Integration Scatter, Large Component, Layer Violation, Unknown Entry Point, Unclear Ownership, Migration Blocker, Forward Engineering Risk
- Output: `application-risk-register.json` — `{ risks: [{ risk_id, category, description, affected_modules, affected_components, severity: Low|Medium|High|Critical, forward_engineering_impact, evidence, recommendation, confidence }] }`

**Stage 10 — Strangler / Migration Candidate Analysis**
- Input: `module-boundary-map.json`, `dependency-graph.json`, `application-risk-register.json`, `architecture-violation-register.json`, `call-flow-map.json`
- Action: classify each module — Good Early Candidate (clear boundary, low efferent coupling, clear public interfaces, few external dependencies, no circular dependency, limited shared ownership) / Possible Candidate With Refactoring / Poor Candidate (high coupling, unclear ownership, many external dependencies, central workflow orchestration, shared data model, many violations) / Blocked / Unknown
- Output: `strangler-candidate-report.md` — must include module ranking, reason for ranking, risks, recommended migration sequencing, human review questions

**Stage 11 — Forward Engineering Input Map**
- Input: all previous stage outputs
- Action: convert architecture findings into useful input for future forward engineering
- Output: `forward-engineering-input-map.md` — must include candidate future modules/services, current APIs to preserve or redesign, important call flows to preserve, modules requiring deeper review, architecture violations not to copy, migration blockers, recommended modernization sequence

**Stage 12 — Diagrams**
- Input: all previous stage outputs
- Action: generate Mermaid diagrams, best-effort if full details are not available; every diagram must include the note "Generated from source evidence. Unknown items are marked as unknown."
- Output: `diagrams/system-context.mmd`, `diagrams/container-view.mmd`, `diagrams/component-view.mmd`, `diagrams/dependency-view.mmd`, `diagrams/call-flow-view.mmd`

**Stage 13 — Final Summary**
- Input: all previous stage outputs
- Action: assemble the summary
- Output: `application-architecture-summary.md` — must include: 1. System Overview, 2. Applications/Projects Detected, 3. Deployable Units, 4. Main Modules, 5. Layered Structure, 6. Component Summary, 7. Interfaces/Entry Points, 8. Dependency Summary, 9. Key Call Flows, 10. Detected Architecture Pattern, 11. Architecture Violations, 12. Application Risks, 13. Migration/Strangler Candidates, 14. Forward Engineering Guidance, 15. Open Questions

**Decision Tree:**

| Condition | Branch A | Branch B | Default |
|-----------|----------|----------|---------|
| An item cannot be determined from the codebase | Write `unknown`, add to `open-questions.md` | — | Never invent module ownership, call flows, tech details, API behavior, business rules, deployment details, security details, data ownership |
| A file cannot be fully produced | Still create it with `Status: incomplete`, `Reason:`, `Open questions:` | — | Never silently omit a required file |
| A full call flow cannot be traced | Produce a partial flow | Add an open question | Never fabricate missing steps |
| Stage 6 or Stage 8 evidence is needed | Read raw source directly | — | Layer 1 JSON is insufficient for method-body/line-level detail in these two stages only |

**Iteration / Retry Rules:**

| Trigger | Max Retries | Strategy |
|---------|------------|---------|
| A module's boundary signal is ambiguous (folder name vs. namespace vs. dependency evidence disagree) | 1 | Check all corroborating signals (§3.3); if still ambiguous, mark `boundary_quality: Unknown` and add an open question |
| A component's layer classification is unclear | 0 | Mark `layer: Unknown`; never guess a layer without at least one corroborating signal |

### 5.3 Analysis Depth & Granularity

| Level | Description | When to Activate | Typical Output Artifact |
|-------|-------------|-----------------|------------------------|
| System | Full system / portfolio overview | Stage 1 System Discovery | `system-inventory.json` |
| Module / Service | Component-level analysis | Stages 2, 5, 7, 9, 10 | `module-boundary-map.json`, `dependency-graph.json` |
| Class / Entity | Object-level analysis | Stage 3 Component Discovery | `component-registry.json` |
| Function / Method | Procedural analysis | Stage 6 (Call Flow Tracing) — raw source read | `call-flow-map.json` |
| Line / Statement | Detailed code inspection | Stage 8 (Violation Detection) — constructor injection line-level verification | `architecture-violation-register.json` |

**Default Depth Level for This Skill:** `Module / Service` for most stages, deliberately descending to `Function / Method` (Stage 6) and `Line / Statement` (Stage 8) where Layer 1 JSON cannot supply the needed detail.

**Coverage Threshold:**
> All 14 required output artifacts (13 files + `diagrams/` with 5 `.mmd` files) exist, per Quality Parameter 1 (Completeness) scored ≥ 4/5.

**Action if Coverage Threshold Not Met:**
> Still create every file, even incomplete ones, with `Status: incomplete`, `Reason:`, and `Open questions:` populated — never silently omit a required output file.

**Reading Depth Rules** _(what to read deep vs skim vs skip)_:

| File / Artifact Type | Reading Rule | Reason |
|---------------------|--------------|--------|
| `source_code.json` (Layer 1) | Primary input for Stages 1-5, 7, 9-13 | Classes, methods, fields, constructor dependencies already extracted |
| Raw source files (Stage 6 only) | Read method bodies in full for the flows being traced | Call chains require actual code, not just signatures |
| Raw source files (Stage 8 only) | Read constructor injection patterns at line level | Violation detection needs line-level verification |
| Items marked `unknown` or missing from Layer 1 JSON | Read directly, any stage | Fills genuine gaps in the accelerator |
| Junk folders (§5.1 exclusion list) | Never read unless explicitly needed | No architectural evidence; wastes context |

### 5.4 Chunking & Context Management

> _Critical for RE on large codebases. This skill's chunking axis is stage-based (13 fixed processing stages), NOT domain/layer-based like the BA/DA/TA pairs — a deliberate divergence._

#### Chunking Strategy

| Dimension | Rule | Default |
|-----------|------|---------|
| Chunk unit | One processing stage (1 through 13), each with its own input/action/output — not a domain or technology layer | Stage-based |
| Max chunk size | No fixed line cap; each stage's scope is bounded by its own required output shape | Stage-scoped |
| Chunk ordering | Fixed: Stage 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → 11 → 12 → 13, strictly sequential — later stages consume earlier stages' outputs as their own input | Sequential, non-negotiable |

#### Context Window Caps

| Item Type | Cap | Selection Strategy When Over Cap |
|-----------|-----|----------------------------------|
| Raw repo dump into the LLM | Never — parse structured evidence first (Non-Negotiable Rule 2.5) | Extract files/projects/classes/functions/components/routes/dependencies/entry points/call chains first, reason from that evidence |
| Call flows traced (Stage 6) | Trace the "important" flows, not exhaustively every possible path | Prioritize flows starting from the entry points found most central in the dependency graph (highest afferent coupling on the touched components) |
| Method bodies read (Stage 6/8) | Read only what's needed for the specific flow/violation being verified | Do not read entire files when only one method's body is relevant |

#### Cross-Chunk Continuity Rules

- **Carried registries:** cumulative `system-inventory.json` → `module-boundary-map.json` → `component-registry.json` → `application-interface-catalogue.json` → `dependency-graph.json`, each stage building on all prior stages' outputs
- **ID continuity:** `MOD-XXX`, `COMP-XXX`, `INT-XXX`, `FLOW-XXX`, `ARCH-VIOL-XXX`, `APP-RISK-XXX` are all sequential within their own series across the whole run — never reset mid-run
- **open_questions propagation:** every stage's `open_questions` array feeds the consolidated `open-questions.md` in Stage 13 — never dropped between stages
- **Registry reset rule:** never reset any ID series or registry between stages — this is a single continuous run, not chunked by domain

#### Multi-Run / Incremental Analysis

| Scenario | Behaviour |
|----------|-----------|
| Re-running on same codebase after a code change | Re-run all 13 stages — this skill's stages are sequentially dependent (each consumes the prior stage's output), so a partial re-run risks stale intermediate artifacts; full re-run is the safe default |
| Running on a subset of the codebase first | Scope `LEGACY_REPO_PATH` to the subset; note in `open-questions.md` that other areas were out of scope for this run |
| Resuming after a failed run mid-stage | Resume from the last fully-completed stage's output files; do not re-run completed stages, but verify their outputs are non-`incomplete` before trusting them as input to the next stage |

---

## BLOCK 6 — INTELLIGENCE

### 6.1 Decision Rules & Heuristics

| ID | Trigger Condition | Agent Action | Rationale |
|----|-------------------|--------------|-----------|
| H-001 | Something cannot be determined from the codebase | Write `unknown`; add to `open-questions.md` | Non-Negotiable Rule 2.1 — never invent |
| H-002 | A module's folder name might not reflect its true boundary | Cross-check namespace/package prefixes, controller/service/entity names, route prefixes, frontend feature folders, shared dependencies | Folder names alone are an unreliable single signal |
| H-003 | Stage 6 (Call Flow) or Stage 8 (Violation Detection) needs evidence Layer 1 JSON doesn't have | Read raw source directly for that stage only | These two stages need method-body/line-level detail that structured pre-extraction doesn't capture |
| H-004 | A full call flow cannot be traced to completion | Produce a partial flow; add an open question | Never fabricate the missing steps |
| H-005 | A file cannot be fully produced | Create it anyway with `Status: incomplete`, `Reason:`, `Open questions:` | Never silently omit a required output file |

**Pattern Recognition Catalog** _(Stage 7 Architecture Pattern Detection)_:

| Pattern Name | Signature / Indicator | RE Significance | Action |
|--------------|----------------------|-----------------|--------|
| Layered Monolith / N-tier | Clear Presentation → Application → Domain → Data Access layering, single deployable | Baseline for most legacy enterprise apps | Record with evidence; note any layer-skipping violations |
| Clean Architecture / Hexagonal | Domain has no dependency on Infrastructure; ports/adapters or interfaces at boundaries | Indicates deliberate dependency-inversion discipline | Record; cross-check Stage 8 for Domain-depends-on-Infrastructure violations that would contradict this |
| Modular Monolith | Multiple modules with strong boundaries (§3.3), single deployable | Good strangler-migration foundation | Record; feeds Stage 10 candidate analysis directly |
| Microservices | Multiple independently deployable units, each with its own data store, communicating over network | Already decomposed — different risk profile than a monolith | Record; note any shared-database anti-patterns across "services" that would suggest a distributed monolith instead |
| Big Ball of Mud | Widespread cross-module leakage, circular dependencies, unclear ownership everywhere | High migration risk | Record; expect many Stage 8 violations and Stage 9 risks to corroborate |
| Anemic vs. Rich Domain Model | Entities with only getters/setters and no behavior (anemic) vs. entities enforcing their own invariants (rich/DDD) | Affects where business rules actually live — relevant to `SKL-BA2`'s handoff too | Record with evidence from Stage 3 component classification |

**Ambiguity Resolution Strategy:**

| Ambiguity Type | Resolution Strategy |
|----------------|-------------------|
| Two or more patterns seem to fit equally well | Record BOTH in "competing possible patterns" with evidence for each — do not force a single answer when evidence is genuinely mixed |
| A component's type is ambiguous (e.g. a class that's both a mapper and a validator) | Classify by its PRIMARY responsibility; note the secondary responsibility in `risk_flags` or evidence, don't invent a new type |
| A module's boundary quality signals conflict (clear folder ownership but heavy cross-module calls) | Weigh dependency evidence (Stage 5) more heavily than folder structure alone — coupling is the more reliable signal; mark `Moderate`, not `Strong`, when in doubt |

**Prioritisation Logic:**
> When context window or time is constrained, analyze in this order:
1. Stages 1-5 (System → Module → Component → Interface → Dependency) — these are prerequisites for everything downstream
2. Stage 6 (Call Flow) for the entry points with the highest afferent coupling in the dependency graph — these represent the most architecturally significant flows
3. Stages 7-9 (Pattern, Violations, Risks) — synthesis of Stages 1-6's evidence
4. Stages 10-13 (Strangler analysis, Forward Engineering Map, Diagrams, Final Summary) — consumption of all prior stages

### 6.2 Confidence & Uncertainty Handling

| Band | Score | Label | Agent Behaviour |
|------|-------|-------|----------------|
| High | 0.85 – 1.00 | Confident | Proceed; tag `✅ EXTRACTED`; include in output with full evidence |
| Medium | 0.60 – 0.84 | Review advised | Tag `⚠️ PARTIAL`; include with warning; surface in `open_questions` |
| Low | 0.40 – 0.59 | Uncertain | Tag `〰️ INFERRED`; attempt disambiguation via corroborating signals before finalizing |
| Very Low | 0.00 – 0.39 | Cannot determine | Tag `❓ UNKNOWN`; use the literal `unknown` value; escalate via `open-questions.md`; do NOT fabricate |

**Confidence Score Calculation:**
- Method: `LLM self-assessed` (this skill's own per-finding `confidence` field), aggregated `Rule-based`
- Formula: `(count(EXTRACTED)×1.0 + count(PARTIAL)×0.7 + count(INFERRED)×0.4 + count(UNKNOWN)×0) / total findings`

**Disambiguation Strategies** _(attempt in order before escalating)_:
1. Cross-check multiple corroborating signals (folder name + namespace + controller/service/entity names + dependency evidence) rather than relying on one
2. For call flows: attempt to trace at least a partial path even if the full flow is unclear — partial evidence beats none
3. If still unresolved, write the literal `unknown` value and add a specific open question — never guess a plausible-sounding answer

### 6.3 Evidence Hierarchy

> _When multiple sources provide conflicting information about the same fact, this ranking determines which source wins. Identical to `SKL-AA2`'s Block 6.3 — both agents must agree on what outranks what._

#### Source Reliability Ranking

| Rank | Source Type | Reliability | Notes |
|------|-------------|-------------|-------|
| 1 — Highest | Constructor injection / method-body call evidence in source | Definitive | The actual, executing wiring of the system |
| 2 | Class/interface declarations, DI registration code | Very High | Declared structure — should match runtime wiring but occasionally lags |
| 3 | Config files (routing, DI wiring, appsettings) | High | Declarative but may be overridden at runtime in code |
| 4 | Log/trace evidence of an actual call path (`logs.json`, Layer 1) | Medium-High | Shows what actually ran, but only for logged paths |
| 5 | Test files exercising a call path | Medium | Shows expected behavior — may not reflect current production code |
| 6 | Naming conventions alone (`*Service`, `*Repository` suffixes) | Low | Inference only — must be flagged `INFERRED` |
| 7 — Lowest | Documentation/README | Very Low | Often stale — verify against code |

#### Conflict Resolution Rule

When two sources disagree:
1. The higher-ranked source wins
2. Document both sides in the output: `"DI registration declares OrderService -> IPaymentGateway, but constructor code directly instantiates StripeClient - constructor evidence wins per evidence hierarchy"`
3. Tag the winning value with the source that provided it
4. Add the conflict to `open_questions` with both values and the resolution applied

#### Common RE Conflict Patterns

| Conflict | Typical Cause | Resolution |
|----------|--------------|------------|
| DI registration says one implementation, but constructor/method-body evidence shows a different one used | Registration not updated after a refactor, or conditional/environment-based registration | Constructor/method-body evidence (rank 1) wins; flag the DI registration as stale in `risk_flags` |
| A route is declared in config but no controller/handler is found for it | Route file stale, or handler exists under an unexpected name/location | Config declaration alone is insufficient evidence for an `application-interface-catalogue.json` entry — mark `confidence` low and add an open question rather than fabricating the handler |
| Naming suggests a component is a "Repository" but it contains business validation logic | Naming convention violated by actual implementation | Classify by evidenced behavior (rank 1, method-body evidence), not by name; note the naming/behavior mismatch as a risk flag |

---

## BLOCK 7 — INTEGRATION

### 7.1 Tools & Integrations

| Tool / API / MCP Server | Purpose | Access Method | Required |
|-------------------------|---------|---------------|---------|
| Coding agent runtime (Claude Code, Codex, or similar) | Execution environment with file read/write access | Native file system access | ✓ |
| `LEGACY_REPO_PATH` file access | Source of all extraction input | Read-only | ✓ |
| Layer 1 JSON extraction output (`LAYER1_PATH`) | Pre-extracted `source_code.json`, `database.json`, `config.json`, `logs.json` | Read from disk if present | — (optional accelerator; Stages 6 & 8 always need raw source regardless) |

**File Operation Permissions:**

| Operation | Permitted Paths | Restrictions |
|-----------|----------------|-------------|
| Read | `LEGACY_REPO_PATH` (excluding the junk-folder exclusion list, §5.1); `LAYER1_PATH` if present | Never modifies anything under `LEGACY_REPO_PATH` |
| Write | `OUTPUT_ROOT/D1-application-architecture/` only | Never writes into `LEGACY_REPO_PATH` under any circumstance (Non-Negotiable Rule 2.3) |
| Execute | `None` | This skill does not run, build, or test the legacy application |

### 7.2 Dependencies

**Upstream Skills** _(must complete before this skill runs)_:

| Skill ID | Skill Name | Output Consumed | Dependency Type |
|----------|------------|-----------------|--------------------|
| — | None (no skill file) | — | — |

**External Systems:**

| System | Purpose | Data Flow | Connection Type |
|--------|---------|-----------|----------------|
| Layer 1 Extraction (external, non-skill automated pre-step) | Provides `source_code.json`, `database.json`, `config.json`, `logs.json` as an accelerator for Stages 1-5, 7, 9-13 | → (inbound to this skill) | Async (pre-computed); optional — Stages 6 and 8 always read raw source directly regardless of Layer 1's presence |

**Downstream Skills** _(receive this skill's output)_:

| Skill ID | Skill Name | What This Skill Provides | Trigger Condition |
|----------|------------|--------------------------|--------------------|
| `SKL-AA2` | AA Agent 2 — Quality Review | All 14 output artifacts under `OUTPUT_ROOT/D1-application-architecture/` | Immediately after this skill's Stage 13 Final Summary |
| `SKL-FOUNDATION` _(not yet templated)_ | Foundation Layer | Indirectly, via `SKL-AA2`'s review | After all four architecture pairs complete |

> **Known naming discrepancy (documented, not silently resolved):** this skill's own source states its output root as `OUTPUT_ROOT/D1-application-architecture/` (§4.2), while `SKL-AA2`'s original source states its input path as `architecture-output/final/`. These two paths do not match in the original prompts. This skill file does not silently pick one — see `SKL-AA2`'s Block 7.3 for the same note and a recommendation that both paths be reconciled to a single agreed value before this pair is used in production.

### 7.3 Context Propagation & Handoff Protocol

**Context to Carry Forward** _(always pass to all downstream skills)_:
- All 13 files + the `diagrams/` folder
- The consolidated `open-questions.md`
- `extraction-audit.md` (what was read via Layer 1 JSON vs. raw source, and why)

**State to Persist** _(store across sessions / incremental runs)_:
- All ID series counters (`MOD-`, `COMP-`, `INT-`, `FLOW-`, `ARCH-VIOL-`, `APP-RISK-`) and the stage-completion state, to support resuming an interrupted run

**Handoff Artifact Format:**

```json
{
  "source_skill": "SKL-AA1",
  "run_id": "RUN-20260601-200000",
  "target_skill": "SKL-AA2",
  "confidence_score": 0.84,
  "context": {
    "output_location": "OUTPUT_ROOT/D1-application-architecture/",
    "modules_found": 5,
    "components_found": 62
  },
  "artifacts": {
    "system-inventory.json": "...", "module-boundary-map.json": "...", "...": "... (14 artifacts total)"
  },
  "validation_queue": [
    { "item": "OrderService -> PaymentGateway wiring", "tag": "PARTIAL", "reason": "DI registration and constructor evidence agree, but no integration test found exercising the actual call" }
  ]
}
```

**Recommended Starting Point for Downstream Agent:**
> Not a fixed value — `SKL-AA2` should begin with Quality Parameter 3 (No Hallucination) and Parameter 2 (Source Traceability), since a failure in either invalidates trust in every other parameter's score.

---

## BLOCK 8 — RELIABILITY

### 8.1 Error Handling & Fallbacks

| Failure Mode | Likelihood | Detection | Fallback Strategy | Escalation Rule |
|--------------|-----------|-----------|------------------|----------------|
| `LEGACY_REPO_PATH` absent or unreadable | L | Checked before Stage 1 | N/A | Stop and ask the user to provide a valid path |
| No recognizable project/solution/package files found | L | Stage 1 search returns nothing | N/A | Stop and ask the user to confirm this is a source repository |
| A full call flow cannot be traced (Stage 6) | M | Observed during Stage 6 | Produce a partial flow | Add an open question; never fabricate the missing steps |
| A required output file cannot be fully produced | M | Observed at any stage | Create it anyway with `Status: incomplete` | Document `Reason:` and `Open questions:`; never silently omit |
| Layer 1 JSON is entirely absent | L | Checked at Stage 1 | Fall back to raw source scanning for all stages | Continue — this is a supported, if slower, path |
| Module boundary signals conflict across sources | M | Observed during Stage 2 | Weigh dependency evidence over folder naming (§6.1 H-002) | Mark `Moderate` boundary quality if genuinely unclear; never force `Strong` |

**Human Review Triggers** _(mandatory escalation conditions)_:
- [ ] Overall `confidence_score` below 0.60
- [ ] Average Quality Parameter score < 4.0 out of 5 (Non-Negotiable per §4.2's Overall Acceptance Criteria)
- [ ] Any single Quality Parameter scores below 3.0
- [ ] Any hallucinated critical claim detected (Kubernetes/microservices/domain-ownership/cloud-provider/API-gateway claimed without file evidence)
- [ ] `open-questions.md` contains more items than can reasonably be resolved without stakeholder input

**Overall Acceptance Criteria** _(this skill's own numeric bar, ported verbatim)_:
```
All required files are generated.
Each major conclusion has evidence.
Unknowns are clearly listed.
Module boundaries are usable.
Component registry is meaningful.
Dependency graph shows risks.
Call flows show real execution paths.
Architecture pattern is evidence-backed.
Risk register is actionable.
Forward engineering map is useful.

Minimum acceptable score:
Average score >= 4.0 out of 5
No parameter below 3.0
No hallucinated critical claims
```

**Escalation Path:**
1. Flag the item in `open-questions.md` with its specific reason
2. Carry it into the handoff to `SKL-AA2`, which will independently score it against the same 10 Quality Parameters
3. If `SKL-AA2` also flags it (PARTIAL/FAIL), it surfaces to human review at the Gate G1 stakeholder checkpoint

**Partial Output Policy:**
> A partial output is acceptable — every file that can be produced should be, even if marked `Status: incomplete` for the parts that couldn't be completed. A stalled run producing zero files is the only case where no output should be emitted; ask the user how to proceed instead.

### 8.2 Validation & QA Checklist

**Agent Self-Check** _(run before finishing — ported verbatim from source)_:
- [ ] Did I create all required output files?
- [ ] Did I avoid modifying legacy source code?
- [ ] Did I exclude junk/generated folders?
- [ ] Did I identify deployable units?
- [ ] Did I identify modules with responsibilities?
- [ ] Did I classify components by type and layer?
- [ ] Did I build the dependency graph?
- [ ] Did I identify cycles and high coupling?
- [ ] Did I trace important call flows?
- [ ] Did I classify the architecture pattern with evidence?
- [ ] Did I identify architecture violations?
- [ ] Did I create the application risk register?
- [ ] Did I create the strangler/migration candidate report?
- [ ] Did I create the forward engineering input map?
- [ ] Did I generate Mermaid diagrams?
- [ ] Did I add unknowns to open questions?
- [ ] Did every major finding include evidence?
- [ ] Every finding carries a `confidence_tag` from the taxonomy in §4.3
- [ ] `confidence_score` calculated per the method in §6.2
- [ ] Evidence hierarchy applied to all conflicting signals (§6.3)

**Human Review Checklist** _(the 10 Quality Parameters, each scored 1-5 — see §4.2 for full scoring language)_:
- [ ] Parameter 1 — Completeness (all 14 files present and meaningful)
- [ ] Parameter 2 — Source Traceability (nearly every finding source-backed)
- [ ] Parameter 3 — No Hallucination (unknowns handled honestly, no invented Kubernetes/microservices/ownership/cloud/gateway claims)
- [ ] Parameter 4 — Module Boundary Quality (modules clearly justified with evidence)
- [ ] Parameter 5 — Component Classification Quality (accurate layer/type classification)
- [ ] Parameter 6 — Dependency Graph Usefulness (supports real migration decisions)
- [ ] Parameter 7 — Call Flow Quality (clear operation flows from entry to persistence/integration)
- [ ] Parameter 8 — Architecture Pattern Accuracy (evidence-backed and nuanced)
- [ ] Parameter 9 — Risk Register Quality (actionable migration risks)
- [ ] Parameter 10 — Forward Engineering Usefulness (directly useful for modernization planning)

**Automated Test Cases:**

| Test ID | Scenario | Input | Expected Output | Pass Criteria |
|---------|----------|-------|-----------------|---------------|
| T-001 | Standard .NET solution with clear module folders | `.sln` with `Ordering/`, `Catalog/`, `Payments/` projects | `system-inventory.json` lists all 3 as `backend_api` or `library`; `module-boundary-map.json` identifies 3 modules with `Strong` or `Moderate` boundary quality | Evidence cited for every module; no fabricated responsibility text |
| T-002 | Ambiguous folder structure | A flat `Services/` folder containing classes for 4 different business domains | Modules assessed via namespace/entity/route signals, not folder alone; boundary quality marked accordingly (likely `Weak` or `Unknown`) | Does not blindly report "1 module: Services" |
| T-003 | Call flow cannot be fully traced | An entry point whose downstream call terminates in a dynamically-invoked method | Partial flow produced; open question added | No fabricated final steps |
| T-004 | Circular dependency present | Module A depends on Module B which depends back on Module A | `dependency-graph.json` `cycles[]` populated with severity and impact; `architecture-violation-register.json` includes a Circular Dependency entry | Cycle detected and both artifacts consistent with each other |

---

## BLOCK 9 — REFERENCE

### 9.1 Examples

#### Canonical Example (Standard Case)

**Scenario:**
> A clean call-flow trace for a checkout endpoint — the standard, fully-evidenced case for Stage 6.

**Input:**
```text
POST /api/orders/checkout
  → OrderController.Checkout
  → OrderService.PlaceOrder
  → BasketService.GetBasket
  → PaymentGateway.Charge
  → OrderRepository.Save
```

**Expected Output:**
```json
{
  "confidence_score": 0.92,
  "findings": {
    "call-flow-map.json": {
      "flows": [
        {
          "flow_id": "FLOW-001",
          "name": "Checkout",
          "entry_point": "POST /api/orders/checkout",
          "steps": [
            { "step": 1, "component": "OrderController", "layer": "API", "module": "Ordering", "operation": "Checkout" },
            { "step": 2, "component": "OrderService", "layer": "Application Service", "module": "Ordering", "operation": "PlaceOrder" },
            { "step": 3, "component": "BasketService", "layer": "Application Service", "module": "Basket", "operation": "GetBasket" },
            { "step": 4, "component": "PaymentGateway", "layer": "Integration", "module": "Payments", "operation": "Charge" },
            { "step": 5, "component": "OrderRepository", "layer": "Data Access", "module": "Ordering", "operation": "Save" }
          ],
          "modules_touched": ["Ordering", "Basket", "Payments"],
          "external_systems_touched": ["PaymentGateway"],
          "confidence": 0.92
        }
      ]
    }
  },
  "gaps": []
}
```

**Notes:**
> Canonical because every step is directly evidenced by an actual method call chain traced through raw source, with module/layer correctly attributed at each step.

#### Edge Cases

| ID | Description | Input Pattern | Expected Behaviour | Risk if Mishandled |
|----|-------------|--------------|-------------------|-------------------|
| E-001 | Ambiguous module boundary from folder name alone | A `Services/` folder with mixed-domain classes | Cross-check namespace, entity, and route signals; mark `boundary_quality` accordingly, likely `Weak` | Trusting the folder name alone would report a false "1 clean module" |
| E-002 | Component with dual responsibility (mapper + validator) | A class that both maps a DTO and validates its fields | Classify by primary responsibility; note the secondary one in evidence/risk_flags | Forcing a single type without noting the secondary responsibility loses information `SKL-AA2` needs |
| E-003 | Two architecture patterns both plausible | Evidence for both "Modular Monolith" and "Layered Monolith" is roughly equal | Record both as competing possible patterns with their respective evidence, rather than forcing one answer | Forcing a single pattern when evidence is genuinely mixed misleads the migration-planning consumer of this report |

#### Anti-Patterns _(What NOT to Do)_

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|---------------|-----------------|
| Claiming "microservices architecture" because folders are named like services, with no deployable-unit or network-boundary evidence | Fabricates infrastructure/architecture facts (Non-Negotiable Rule 2.1) | Only claim microservices with evidence of independent deployability; otherwise mark `unknown` or note as a competing pattern |
| Sending the entire raw repository into the model in one shot | Wastes context and skips the required parse-first-reason-second discipline (Rule 2.5) | Extract structured evidence first, then reason from it |
| Skipping a required output file because "there wasn't much to say" | Silently omits a promised artifact | Create it with `Status: incomplete`, `Reason:`, `Open questions:` |
| Reporting the architecture as cleaner than it is (hiding violations, tight coupling, unclear ownership) | Defeats the purpose of a reverse-engineering audit — this skill's own "Important Reminder" is explicit about this | Document messy parts, violations, weak boundaries, tight coupling, unclear ownership, risky flows, migration blockers, and unknowns honestly |
| Marking a CI/CD-style "Present" claim (or any claim) from a name alone, with no file/line/class evidence | Fails Quality Parameter 2 (Source Traceability) and 3 (No Hallucination) | Every finding needs file path, line if available, class/function/component name, and confidence |

### 9.2 Changelog & Version Notes

| Version | Date | Author | Change Description |
|---------|------|--------|--------------------|
| 1.0.0 | 2026-06-01 | AA Reverse Engineering System | Original `07_AA_Agent1_AppExtractor.md` prompt (unversioned in source; treated as 1.0.0) |
| 1.0.0 (template conversion) | 2026-07-06 | Skill file conversion pass | Reformatted into the `sdlc_skill_file_template_v2.md` 9-block structure; no behavioral change to the underlying 13-stage extraction logic — added `confidence_tag` taxonomy mapping, evidence hierarchy, JSON output schema, and explicit chunking notes (stage-based, not domain-based) that were implicit in the original prose. Documented, rather than silently resolved, the output-path naming discrepancy between this file (`OUTPUT_ROOT/D1-application-architecture/`) and `SKL-AA2`'s stated input path (`architecture-output/final/`) — see §7.2. |

---

_Template v2.0 · 9 Blocks · 24 Sections · SDLC Agentic AI Platform · RE-optimised_
_Converted from: `prompts-ready-to-use/07_AA_Agent1_AppExtractor.md` · Pair with: `skill-files/08_AA_Agent2_QualityReview.md` (`SKL-AA2`)_
