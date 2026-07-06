# SKILL FILE: TA Agent 2 — Deep Analyst

> Skill ID: `SKL-TA2` | Version: `2.0.0` | Status: `ACTIVE`
> SDLC Phase: `Analysis`
> Domain: `Reverse Engineering` | Sub-Domain: `Technology & Infrastructure Discovery`
> Owner: `[Team / Member]` | Last Updated: `2026-06-01`

---

## BLOCK 1 — IDENTITY

### 1.1 Skill Metadata

| Field | Value |
|-------|-------|
| Skill ID | `SKL-TA2` |
| Skill Name | TA Agent 2 — Deep Analyst |
| Version | `2.0.0` |
| SDLC Phase | `Analysis` |
| Domain | `Reverse Engineering` |
| Sub-Domain | `Technology & Infrastructure Discovery` |
| Owner | `[Team / Member]` |
| Tags | `technology-architecture`, `deep-analysis`, `nfr-extraction`, `ci-cd-maturity`, `risk-register`, `agent-2-of-2` |
| Status | `Active` |
| Paired With | `SKL-TA1` (TA Agent 1 — Stack Scout) — hard dependency, this skill cannot begin without `SKL-TA1`'s 6 output files |

### 1.2 Goal & Success Criteria

**Primary Goal:**
> Transform `SKL-TA1`'s structural inventory into precise, evidence-based Technology Architecture documentation — reading deep into method bodies, configuration logic, infrastructure declarations, and full CI/CD pipeline files — extracting architectural patterns, NFRs, security implementations, and technical risks from what the code and configuration actually do, not from what they are named.

**Secondary Goals:**
- Preserve exact configuration values (timeouts, pool sizes, retry counts, TTLs) — these values ARE the architectural specification, never paraphrased
- Assess CI/CD pipeline maturity from direct evidence (tool/action names found in full pipeline reads) — never from stage names alone
- Reconcile every discrepancy found between `SKL-TA1`'s inventory and what implementation actually shows, without silently overwriting the agreed naming baseline

**Success Definition:**
> A run is successful when all 8 outputs (Technology Stack Assessment, Architecture Pattern Catalog, Component Interaction & Contract Map, Data Architecture Assessment, Security Architecture Assessment, NFR Registry, Technical Debt & Risk Register, Operational Architecture Assessment) are produced with every numeric threshold preserved exactly, every CI/CD capability assessment backed by a specific tool/action name and file/job reference (never a bare stage name), and every discrepancy with `SKL-TA1`'s inventory captured in the Agent 1 Discrepancy Log rather than silently resolved.

**What This Skill Does NOT Do:**
> Everything `SKL-TA1` already established as ground truth is inherited, not re-derived.
- Does not re-derive the Technology Stack Inventory, Data Store Registry, or Component Map from scratch
- Does not run Stage 6 (Architecture Pattern Catalog Final), Stage 7 (Component Interaction Map), or Stage 8 (Operational Assessment) per-chunk — all three require the full cross-layer picture and run once, in the Synthesis Pass
- Does not assess CI/CD pipeline maturity from stage/job names alone — every capability claim must cite a specific tool invocation or action name
- Does not mark a finding `HIGH` confidence without a direct code or config reference

---

## BLOCK 2 — ACTIVATION

### 2.1 Trigger Conditions

**Explicit Triggers** _(user states these directly)_:
- "run agent 2"
- "deep analysis"
- "continue"
- "finalise the documentation"

**Implicit Signals** _(infer from conversation context or orchestrator routing)_:
- `SKL-TA1`'s 6 output files are present in the session and the user's next message implies moving forward rather than re-scanning
- The orchestrator routes here immediately after `SKL-TA1` completes

**Activation Keywords / Patterns:**
```
"run agent 2" | "deep analysis" | "continue" | "finalise the documentation" |
"architecture patterns" | "NFRs" | "technical debt" | "CI/CD maturity"
```

### 2.2 Pre-conditions & Guards

**Must Be True Before Activation:**
- [ ] `SKL-TA1`'s output files are available — pasted in, uploaded, or produced in the same session
- [ ] The original project codebase is still accessible — needed for deep reads into method bodies, full CI/CD pipeline files, and configuration logic
- [ ] At minimum, `SKL-TA1`'s OUTPUT 1 (Technology Stack Inventory), OUTPUT 2 (Component & Service Map), and OUTPUT 3 (Data Store Registry) are present

**Disqualifiers** _(do NOT activate if any of these are true)_:
- [ ] Paired agent (`SKL-TA1`) has not yet completed its run and none of its 6 outputs exist
- [ ] Fewer than 3 of `SKL-TA1`'s outputs are available and the 3 minimum-required ones are not among them
- [ ] `SKL-TA1`'s Component Map contains only 1 component with no data store or integration — likely a scanning failure or a library project; confirm with the user before proceeding
- [ ] More than 50% of `SKL-TA1`'s items are flagged low confidence — the scaffolding is too unreliable to build on without human triage first

---

## BLOCK 3 — CONTEXT

> _Block 3 is the most critical block for Reverse Engineering skills. Precision here directly determines output accuracy._

### 3.1 Environment Context

| Dimension | Details |
|-----------|---------|
| Target Language(s) | Same as `SKL-TA1` — inherited, not re-detected |
| Framework(s) | Any — inherited from `SKL-TA1`'s Chunk 0 detection |
| Platform / OS | Any — static source/config-read skill |
| Database Type | Inherited from `SKL-TA1`'s Data Store Registry; this skill traces access patterns, not schema |
| Architecture Pattern | Confirmed/corrected by this skill in Stage 6, not re-detected from scratch |
| Available Tools | Read-only file/codebase access, same as `SKL-TA1`, PLUS `SKL-TA1`'s 6 completed output files as required input |
| Repository Access | `Read-only` |
| Authentication Level | None required — this skill never connects to a live system |
| **CI/CD note (v2)** | `SKL-TA1`'s OUTPUT 4 CI/CD Pipeline Inventory already includes tool invocations and action names — used as the starting point, but this skill MUST also directly read the full pipeline files during the CI/CD layer chunk; `SKL-TA1`'s list is a fast-scan summary, this skill's direct read is the authoritative source for Stage 8 |

### 3.2 Artifact Taxonomy

> _Which artifact types can this skill ingest and analyze?_

| Artifact Type | Supported | Accepted Formats | Notes |
|---------------|-----------|-----------------|-------|
| Source Code | ✓ (deep) | Any language `SKL-TA1` scanned | Full method bodies read for resilience/security/transaction logic — the key difference from `SKL-TA1` |
| Database Schema | ✗ (not re-read) | — | Access patterns traced through repository/DAO code, not schema itself |
| API Contracts | ✓ | OpenAPI, Proto, GraphQL schema | Used for API Contract Inventory (Stage 7) |
| Configuration Files | ✓ (deep) | Any config format | Connection pool, cache, queue, security filter chain configuration read in full — these ARE the NFRs |
| UI Wireframes / Designs | ✗ | — | Out of scope |
| Application Logs / Traces | ✗ | — | Out of scope |
| Test Cases | ✓ (limited) | Any test framework | Read only if a specific architectural pattern is ambiguous and test config clarifies intent |
| Documentation | ✗ | — | Not a primary source in the source prompt |
| Infrastructure as Code | ✓ (deep) | Dockerfiles, compose, K8s, Terraform | Read for deployment safety, DR posture, environment parity |
| Binary / Compiled Code | ✗ | — | Cannot be scanned |
| **CI/CD Pipeline Files (full read, v2)** | ✓ (mandatory, primary evidence for this layer) | GitHub Actions, Jenkinsfile, GitLab CI, Azure Pipelines, CircleCI, Bitbucket Pipelines | Every `run:` block read in FULL (not first-word-only like `SKL-TA1`); every local `uses:` reference followed and read with the same depth |
| **`SKL-TA1` Output Files** | ✓ (required) | The 6 outputs from `SKL-TA1` | Treated as ground truth for naming/inventory; traced deep into implementation, never replaced |

### 3.3 Domain Knowledge References

**Architectural Patterns to Recognise:**
- Resilience: Retry (backoff params), Circuit Breaker (threshold/window), Bulkhead, Timeout, Fallback, Rate Limiting
- Data Access: Repository, Unit of Work, CQRS, Event Sourcing, Outbox, N+1 detection, transaction boundaries, locking
- Caching: Cache-Aside, Read-Through, Write-Through, invalidation, TTL, eviction policy
- Communication: Sync REST, gRPC, async messaging, WebSocket, event publishing, GraphQL
- Security: OAuth2/OIDC, JWT validation, API Key, mTLS, RBAC, ABAC, token refresh
- Scalability: horizontal scaling config, connection pooling, read replicas, async offload
- Observability: structured logging, distributed tracing, metric export, health checks, correlation IDs
- Deployment: blue-green/canary, feature flags, sidecar, health/readiness probes, graceful shutdown

**Design Patterns to Detect** _(e.g. Repository, CQRS, Singleton, Saga)_:
- All patterns in the "Pattern categories to scan for" table (§5.2 Stage 3) — Resilience, Data Access, Caching, Communication, Security, Scalability, Observability, Deployment

**Standards & Protocols:**
- Evidence-to-Capability Mapping for CI/CD (§5.2 CI/CD Deep-Read Sub-Procedure) — 14 pipeline capabilities, each requiring a specific tool/action name as proof

**Domain Glossary:**

| Term | Definition |
|------|-----------|
| AP-ID | Architecture Pattern identifier, sequential (AP-01, AP-02, …) across the entire analysis; never resets |
| NFR-ID | Non-Functional Requirement identifier, sequential across the entire analysis; never resets |
| TD-ID | Technical Debt/Risk identifier, sequential across the entire analysis; never resets |
| Evidence-based CI/CD assessment | A capability is Present ONLY when a specific tool invocation or action name is found — never inferred from a stage/job name alone |
| Coverage gap | A pattern applied inconsistently across the system (present in some places, missing in others where it should be) |

**RE Checklist for This Sub-Domain:**
> _Specific things this skill must look for in this sub-domain._
- [ ] Every architecture pattern instance records its exact configuration values, never paraphrased
- [ ] Every CI/CD capability claim cites a specific tool/action name + file + job
- [ ] Every NFR is a single discrete numeric value — never combined
- [ ] Every technology's EOL/support status is assessed, not just its version
- [ ] Every component interaction records its coupling strength with a specific reason
- [ ] Plaintext secrets committed to source control trigger immediate escalation (§8.1), never quiet documentation

---

## BLOCK 4 — INTERFACE

### 4.1 Input Specification

#### Required Inputs

| Field | Type | Format / Example | Description |
|-------|------|-----------------|-------------|
| `ta1_outputs` | object (6 files) | `SKL-TA1`'s Technology Stack Inventory, Component & Service Map, Data Store Registry, Infrastructure & Deployment Blueprint, Integration & Dependency Graph, Security & Configuration Snapshot | Ground truth for naming/inventory; required before Chunk 0 can begin |
| `project_source` | file tree / zip / pasted code | Same project `SKL-TA1` scanned | Needed for deep reads — `SKL-TA1`'s inventory alone is insufficient |

#### Optional Inputs

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `ta1_validation_queue` | array | empty | `SKL-TA1`'s low-confidence/`ARCHITECTURE NOTE` items — used as priority Resolution Targets in Chunk 0 |
| `prior_chunk_plan` | object | none | If resuming a run, the Chunk Plan, AP/NFR/TD-ID counters, and cumulative registries from the point of interruption |

#### Input Validation Rules
- At minimum, `SKL-TA1`'s OUTPUT 1, OUTPUT 2, and OUTPUT 3 must be present
- The original project source must still be accessible, including full CI/CD pipeline files

#### Input Rejection Criteria
- `SKL-TA1`'s output is entirely absent
- Fewer than 3 of `SKL-TA1`'s outputs are present and the 3 minimum-required ones are not among them
- `SKL-TA1`'s Component Map contains only 1 component with no data store or integration

### 4.2 Output Specification

#### Standard Output Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `skill_id` | string | ✓ | `SKL-TA2` |
| `run_id` | string | ✓ | `RUN-YYYYMMDD-HHMMSS` |
| `confidence_score` | float 0–1 | ✓ | Computed per §6.2 formula |
| `analysis_depth` | string | ✓ | `function` — this skill reads method bodies, configuration logic, and full CI/CD pipeline files, unlike `SKL-TA1`'s `module` depth |
| `coverage_pct` | float 0–1 | ✓ | % of the 6 fixed layers fully processed through Stage 5, weighted with CI/CD capabilities confirmed / 14 total |
| `findings` | object | ✓ | The 8 final outputs, keyed as below |
| `gaps` | array | ✓ | All unresolved `LOW`/`ASSUMED`/`DISCREPANCY` items |
| `recommendations` | array | | Highest-priority Critical/High technical debt item, or "None" |
| `handoff_context` | object | | Full cumulative registries + Agent 1 Discrepancy Log, packaged for `SKL-FOUNDATION` |

#### `findings` Object Structure _(skill-specific)_

```json
{
  "skill_id": "SKL-TA2",
  "run_id": "RUN-20260601-190000",
  "confidence_score": 0.89,
  "analysis_depth": "function",
  "coverage_pct": 0.93,
  "findings": {
    "technology_stack_assessment": [
      { "component": "express", "declared_version": "4.18.2", "usage_depth": "Active - core path", "eol_status": "Supported", "confidence_tag": "EXTRACTED" }
    ],
    "architecture_pattern_catalog": [
      { "id": "AP-01", "pattern": "Retry with Exponential Backoff", "category": "Resilience", "applies_to": "PaymentService -> External Payment Gateway", "exact_configuration": "Max 3 attempts; initial delay 1000ms; multiplier 2.0x; max delay 8000ms", "coverage": "Applied everywhere it should be", "confidence_tag": "EXTRACTED", "source": "PaymentService.processPayment()" }
    ],
    "component_interaction_contract_map": [],
    "data_architecture_assessment": { "data_store_deep_dive": [], "data_ownership_map": [], "data_flow_notes": [] },
    "security_architecture_assessment": { "auth_implementation": [], "secrets_posture": [], "attack_surface_summary": [] },
    "nfr_registry": [
      { "id": "NFR-03", "name": "Database connection acquisition timeout", "value": "30000ms (30s)", "category": "Latency / Availability", "source": "application.yml (Hikari)", "confidence_tag": "EXTRACTED" }
    ],
    "technical_debt_risk_register": [],
    "operational_architecture_assessment": { "cicd_pipeline_maturity": [], "observability_coverage": [], "deployment_safety": [], "disaster_recovery_posture": [] }
  },
  "gaps": [
    { "area": "Auto Rollback CI/CD capability", "reason": "no kubectl rollout undo / helm rollback / deployment slot swap found in any pipeline file", "severity": "High" }
  ],
  "recommendations": [
    "Highest-priority action item: TD-04 (Spring Boot 2.7 EOL, Critical severity)"
  ],
  "handoff_context": {
    "ap_id_counter": 18,
    "nfr_id_counter": 27,
    "td_id_counter": 11,
    "discrepancy_log": []
  }
}
```

#### Quality Criteria
- No numeric threshold, version number, or configuration parameter is paraphrased anywhere in final OUTPUT text
- No CI/CD capability is marked `Present` without a specific tool/action name + file + job reference
- No architecture pattern is invented without direct code/config evidence — unevidenced expectations are marked `ASSUMED`
- Every discrepancy with `SKL-TA1` is logged, never silently resolved

### 4.3 Confidence & Evidence Tagging Schema

> _Every finding in the output must carry a tag declaring how it was obtained._

#### Tag Taxonomy

| Tag | Symbol | Definition | Downstream Action |
|-----|--------|-----------|------------------|
| EXTRACTED | `✅` | Directly and explicitly evidenced by a line of code, annotation, configuration value, or a matching CI/CD tool/action name | Proceed; no review needed unless conflicted |
| PARTIAL | `⚠️` | Inferred from naming patterns, partial code evidence, or ambiguous config — some real evidence exists | Include with warning flag; surface in `gaps` |
| INFERRED | `〰️` | A pattern or NFR implied by context but with no direct code evidence (`ASSUMED` in this skill's own vocabulary) | Mark as inferred; never state as confirmed fact |
| UNKNOWN | `❓` | Cannot be determined even after deep read; or a direct contradiction with `SKL-TA1`'s inventory that cannot be resolved | Escalate via `gaps` / Discrepancy Log; do NOT fabricate |

**Legacy tag mapping** _(this skill's original scale, mapped onto the taxonomy above)_:

| Original label | Maps to |
|---|---|
| `HIGH` | `EXTRACTED` |
| `LOW — [specific reason]` | `PARTIAL` |
| `ASSUMED — [reason]` | `INFERRED` |
| `DISCREPANCY — [what SKL-TA1 said vs what code shows]` | `UNKNOWN` until resolved, then re-tagged per resolution; always logged in the Agent 1 Discrepancy Log regardless of final tag |
| `RESOLVED — [what code confirmed]` | `EXTRACTED` (and removed from the Validation Queue inherited from `SKL-TA1`) |
| CI/CD `HIGH — [tool name] found in [file]:[job]` | `EXTRACTED` (the tool name IS the evidence, per the v2 rule) |

#### Mandatory Tagging Rules

- Every row in every one of the 8 `findings` structures carries a `confidence_tag`
- `confidence_score` is computed per §6.2
- `INFERRED` and `UNKNOWN` findings always appear in `gaps` with a reason
- No finding is ever marked `EXTRACTED`/`HIGH` without a direct code, config, or tool/action-name reference (this skill's own Constraint, §5.1)

#### Display Convention

```
✅ EXTRACTED — [tool name] found in [file]:[job], OR directly evidenced by [code/config reference]
⚠️ PARTIAL  — inferred from [naming/partial evidence] — [specific reason]
〰️ INFERRED — ASSUMED: [reason this pattern/NFR is architecturally expected but not found in code]
❓ UNKNOWN  — DISCREPANCY: [what SKL-TA1 said] vs [what the code/config shows] — unresolved
```

---

## BLOCK 5 — EXECUTION

### 5.1 Constraints & Guardrails

**Hard Constraints _(MUST NOT do these under any circumstances)_:**
- NEVER begin without `SKL-TA1`'s minimum required outputs (OUTPUT 1, 2, 3)
- NEVER re-derive the Technology Stack Inventory, Data Store Registry, or Component Map from scratch
- NEVER silently override `SKL-TA1`'s named artifacts — every discrepancy must be logged
- NEVER run Stage 6 (Architecture Pattern Catalog Final), Stage 7 (Component Interaction Map), or Stage 8 (Operational Assessment) per-chunk — all three run once, in the Synthesis Pass
- NEVER reset the NFR Registry or Technical Debt Register between chunks
- NEVER reset NFR-ID or TD-ID numbering between chunks — sequential across the entire analysis
- NEVER collapse distinct configuration values into a single entry — each timeout, pool size, retry count, and TTL is a discrete NFR
- NEVER invent architecture patterns not evidenced in code or configuration — mark `ASSUMED — [reason]` instead
- NEVER paraphrase exact configuration values, version numbers, or threshold values
- NEVER assess CI/CD pipeline maturity from stage names alone — every capability claim requires a specific tool invocation or action name
- NEVER rely solely on `SKL-TA1`'s CI/CD summary for the Operational Assessment — must directly read the full pipeline files during the CI/CD layer chunk
- NEVER use vague language in final output artifacts
- NEVER mark a finding `HIGH`/`EXTRACTED` confidence without a direct code or config reference

**Soft Constraints _(PREFER NOT TO — may override with justification)_:**
- Prefer not to read test files unless a specific architectural pattern is ambiguous and test config clarifies intent
- Prefer not to read past the first 30 / last 20 lines of a method body exceeding 80 lines unless the skipped middle contains nested conditionals or additional retry/DB call logic

**Scope Boundaries:**

| IN Scope | OUT of Scope |
|----------|-------------|
| Method-body-level architecture pattern extraction | Re-scanning folder/module structure (SKL-TA1's job) |
| Full CI/CD pipeline file reads | Business rule extraction (BA pair's job) |
| NFR extraction with exact values | Data schema / ERD construction (DA pair's job) |
| Technical debt and risk identification | Application call-flow tracing (AA pair's job) |
| Component interaction and coupling analysis | Discovering new technology components not in SKL-TA1's inventory (confirm/correct only) |

**Data Sensitivity Rules:**

| Data Type | Rule |
|-----------|------|
| PII (names, emails, IDs) | Not typically encountered; if found, field names only |
| Credentials / Secrets | If plaintext secrets are found committed to source control, record the LOCATION only, never the secret value — and escalate immediately (§8.1) |
| Confidential Business Logic | Not this skill's focus — technology/architecture facts only |
| Third-party IP / Licensed Code | Library/framework names and versions only |

**Exclusion List** _(never scan these)_:
```
Same exclusion list as SKL-TA1: node_modules/, .git/, dist/, build/, out/,
.next/, .nuxt/, __pycache__/, *.min.js, *.bundle.js, *.map, coverage/,
.cache/, vendor/, bin/, *.compiled.*
Plus, specific to this skill: test files (unless clarifying an ambiguous
pattern), UI render components/view templates, database migration files
(SKL-TA1 already extracted table names), and auto-generated code files
(marked `// Generated`, `/* @generated */`, or in a `generated/` folder).
```

### 5.2 Process & Methodology

**Step 1 — Chunk 0: Orientation Pass**
- Input: `SKL-TA1`'s 6 output files
- Action: re-read all available outputs in full; list every `LOW`/`ARCHITECTURE NOTE` item as priority Resolution Targets; confirm Layer Processing Order (§6.1); note all CI/CD tool invocations `SKL-TA1` already captured as the starting point for this skill's direct-read expansion; identify expected architectural patterns from the stack (e.g. Resilience4j in stack → expect circuit breaker patterns; Kafka → expect event-driven patterns); identify expected NFR categories from the Data Store Registry and Integration Graph
- Output: **Orientation Summary** + **Chunk Plan** + **Resolution Targets list** + **Expected Pattern Checklist**
- Decision Point: if `SKL-TA1`'s minimum required outputs are missing → apply Escalation Triggers (§8.1) instead of proceeding

**Step 2 — Chunks 1–N: Layer Deep Dives (Stages 2–5, per chunk, in sequence)**
- Input: one technology layer, in the priority order from §6.1 Layer Processing Order
- Action:
  1. **Stage 2 — Technology Usage Analysis**: for each major technology in `SKL-TA1`'s OUTPUT 1 for this layer, read class declarations, config blocks, injection points to determine actual usage depth (fully integrated / partially integrated / declared but no usage evidence); confirm or correct version records — flag `DISCREPANCY` if implementation shows a different version; flag `LOW — declared in manifest but no usage evidence found` for unused declarations
  2. **Stage 3 — Architecture Pattern Extraction**: read all method bodies per the Reading Strategy (§5.3); identify every pattern with exact location, exact configuration, and confidence; for the CI/CD & Deployment Layer, apply the **CI/CD Deep-Read Sub-Procedure** instead of the standard code read (see below)
  3. **Stage 4 — NFR Extraction**: read all numeric-value-bearing configuration blocks and annotated parameters; translate every threshold/timeout/pool-size/retry-count/TTL/rate-limit/concurrency-setting into its own discrete NFR row; include all `NFR CANDIDATE` items from Stage 3; convert all time values to dual format (`30000ms (30s)`)
  4. **Stage 5 — Technical Risk & Debt Identification**: assess version currency against EOL/support calendars; identify anti-patterns from Stages 2-4 evidence; assign severity (Critical/High/Medium/Low)
  5. Apply Cross-Chunk Continuity Rules (§5.4)
- Output: a **Layer Summary block** (exact format in this section's "Chunk Response Format" below) before proceeding to the next chunk

**CI/CD Deep-Read Sub-Procedure** _(replaces the standard Stage 3 code read for the CI/CD & Deployment Layer — v2 addition)_:
1. Read every pipeline file listed in `SKL-TA1`'s OUTPUT 4 CI/CD Pipeline Inventory — do not skip any
2. Also scan CI/CD directories directly (`.github/workflows/`, `.circleci/`, `bitbucket-pipelines.yml`, `azure-pipelines.yml`, `Jenkinsfile`, etc.) for files `SKL-TA1` may have missed
3. For every `uses:` reference to a local file → open and read it with the same depth
4. For every `run:` block → read the FULL script content (unlike `SKL-TA1`'s first-word-only read); extract every tool invocation; record step name, job name, file
5. For every `if:` condition on a job/step → record what branch/event/variable controls execution — this determines actual coverage of each capability
6. Map every tool invocation and action to a pipeline capability using the Evidence-to-Capability Mapping table (§6.1)
7. Note capabilities that are **conditionally excluded** (e.g. security scans that run only on `main`, not on PRs)

**Step 3 — Synthesis Pass: Stages 6, 7 & 8 (run once, after all layer chunks complete)**
- Input: all completed Layer Summaries, the full Architecture Pattern findings, NFR Registry, Technical Debt Register
- Action:
  1. **Stage 6 — Architecture Pattern Catalog (Final)**: consolidate all Stage 3 findings across chunks into a single, deduplicated catalog; for each pattern, confirm consistent application or identify coverage gaps; identify patterns declared in libraries but unused; identify patterns critically absent given the integration profile
  2. **Stage 7 — Component Interaction & Contract Map**: use `SKL-TA1`'s Component Map and Integration Graph as the starting point; trace actual communication patterns from code (HTTP calls, pub/sub, gRPC stubs, event dispatchers); classify coupling strength (Tight/Loose with reason); identify missing API contracts, versioning strategy, breaking-change risk
  3. **Stage 8 — Operational Architecture Assessment**: evidence-based CI/CD Maturity assessment (Present only with a matching tool/action + file + job; Absent when no matching evidence anywhere; Partial when evidence exists only under an excluding condition); Deployment Safety (blue-green/canary/feature flags/graceful shutdown/readiness probes per service); Observability Coverage (structured logging/tracing/metrics/alerting/health endpoints per service, gaps are findings); Disaster Recovery Posture (backup/multi-region/replication declarations in IaC or absent); Environment Parity (environment count, shared vs. divergent build paths)
- Output: OUTPUT 2 (final), OUTPUT 3, OUTPUT 8

**Step 4 — Final Response Assembly**
- Input: all 8 outputs, the Validation Queue, the Agent 1 Discrepancy Log
- Action: consolidate everything into the exact structure shown in §9.1
- Output: the Final Response Assembly block

**Decision Tree:**

| Condition | Branch A | Branch B | Default |
|-----------|----------|----------|---------|
| Fewer than 6 of `SKL-TA1`'s outputs available | Proceed if the 3 minimum-required outputs are present | Stop if they are not | Flag every missing output at the top of Chunk 0 |
| A CI/CD capability's evidence exists only under a conditional (e.g. `if: github.ref == 'refs/heads/main'`) | Mark `Partial` | — | Never mark `Present` if PRs/other branches are excluded |
| A method body exceeds 80 lines | Read first 30 + last 20 lines | Read the skipped middle only if it contains nested conditionals or additional retry/DB call logic | Never read repetitive boilerplate |

**Iteration / Retry Rules:**

| Trigger | Max Retries | Strategy |
|---------|------------|---------|
| A technology's usage evidence is genuinely ambiguous even after reading the full relevant code | 1 | Mark `LOW — [specific reason]`; do not retry indefinitely — surface it and move on |
| No CI/CD pipeline files found during the direct read | 0 | Flag `CI/CD LAYER: No pipeline files found in expected locations; Stage 8 CI/CD Maturity will be assessed as all Absent with Critical severity gaps`; continue |

**Chunk Response Format:**

```
## Agent 2 - Chunk [N] of [Total] - [Layer Name]

**Agent 1 Input This Chunk:**
- Technologies being analysed:          [list from Agent 1's OUTPUT 1 for this layer]
- Components being traced:              [list from Agent 1's OUTPUT 2 for this layer]
- Data stores being traced:             [list from Agent 1's OUTPUT 3, if Data layer]
- CI/CD tool invocations from Agent 1:  [list from OUTPUT 4, if CI/CD layer - "will verify and expand by direct read"]
- LOW CONFIDENCE items to resolve:      [list from Agent 1's Validation Queue, or "None"]

**Carried Forward from Prior Chunks:**
- Validated technologies:               [cumulative list]
- NFR entries catalogued so far:        [NFR-01 through NFR-XX - count and range]
- Technical debt entries catalogued:    [TD-01 through TD-XX - count and range]
- Unresolved Validation Queue items:    [count]

---
[Stages 2-5 output for this layer; CI/CD layer uses the Deep-Read Sub-Procedure for Stage 3]
---

### Layer Summary - [Layer Name]
- Technologies confirmed this chunk:               [list with usage depth: Active / Partial / Declared-only]
- Patterns found this chunk:                       [AP-XX through AP-YY]
- NFR entries added this chunk:                    [NFR-XX through NFR-YY - count]
- Technical debt entries added this chunk:         [TD-XX through TD-YY - count]
- [CI/CD layer only] Pipeline files directly read: [list]
- [CI/CD layer only] Additional tools found vs Agent 1: [list, or "None"]
- Agent 1 LOW CONFIDENCE items resolved:           [list with resolution detail]
- New LOW CONFIDENCE items raised:                 [list with reason, or "None"]
- DISCREPANCIES with Agent 1 found:                [list, or "None"]
- Cross-layer dependencies to carry to Synthesis:  [list, or "None"]
```

### 5.3 Analysis Depth & Granularity

| Level | Description | When to Activate | Typical Output Artifact |
|-------|-------------|-----------------|------------------------|
| System | Full system / portfolio overview | Not used directly — OUTPUT 3/8 refine `SKL-TA1`'s system-level view rather than rebuilding it | Component Interaction & Contract Map |
| Module / Service | Component-level analysis | Inherited starting point from `SKL-TA1` | Technology Stack Assessment |
| Class / Entity | Object-level analysis | Data access pattern tracing | Data Architecture Assessment |
| Function / Method | Procedural analysis | **This skill's default and defining depth** — every chunk reads method bodies and config blocks | Architecture Pattern Catalog, NFR Registry |
| Line / Statement | Detailed code inspection | Exact numeric value extraction from config; full CI/CD `run:` block reads | NFR Registry values, CI/CD Pipeline Maturity evidence |

**Default Depth Level for This Skill:** `Function / Method`, with `Line / Statement` precision for exact configuration values and full CI/CD script reads — this is the key divergence from `SKL-TA1`'s `Module / Service` depth.

**Reading Strategy** _(what to read deep vs skim vs skip)_:

**Read in full:**
- Retry, circuit breaker, timeout, and rate limiting logic — any method body with these annotations or manual implementations
- State transition and workflow orchestration methods
- Authentication and authorisation enforcement logic (`@PreAuthorize`, middleware, guard functions, filter chains)
- Data access methods with transaction annotations or explicit transaction management
- Error handling and fallback paths — frequently contain implicit resilience policies
- Connection pool, cache, and queue configuration blocks — these ARE the NFRs
- Security filter chains and middleware registration — filter ORDER is architecturally significant
- Any method body in a class flagged as a cross-service integration client in `SKL-TA1`'s Integration Graph
- CI/CD pipeline files — every step's `run:` block and `uses:` reference in full during the CI/CD layer chunk (v2)
- All reusable workflow files referenced by primary pipeline files — follow every local `uses:` reference (v2)

**Skim (first and last 20 lines only):**
- Service class methods with no resilience annotations and no transaction scope — check entry conditions and return types only
- DTO mapping/serialisation methods — confirm field names, skip mapping logic
- Repository/DAO implementations with no custom query logic — confirm target store, skip boilerplate

**Skip entirely:**
- Test files — unless a specific architectural pattern is ambiguous and test config clarifies intent
- UI render components and view templates
- Database migration files — `SKL-TA1` already extracted table names
- Auto-generated code files
- Any file type/directory on `SKL-TA1`'s exclusion list

**Token efficiency rule:** if a method body exceeds 80 lines → read first 30 lines, jump to last 20 lines; if the skipped middle contains nested conditionals or additional retry/DB call logic, read it. Never read repetitive boilerplate.

**Coverage Threshold:**
> 100% of `SKL-TA1`'s minimum-required layers processed through Stage 5 before the Synthesis Pass begins; all 14 CI/CD capabilities assessed with evidence-based Present/Absent/Partial before Stage 8 is considered complete.

**Action if Coverage Threshold Not Met:**
> Emit the Final Response Assembly anyway with `coverage_pct` reflecting the shortfall; list every unprocessed layer and every un-assessed CI/CD capability in `gaps` with a specific reason.

### 5.4 Chunking & Context Management

> _Critical for RE on large codebases._

#### Chunking Strategy

| Dimension | Rule | Default |
|-----------|------|---------|
| Chunk unit | One technology layer, inherited from `SKL-TA1`'s 6-layer boundary — not redefined | Same 6 layers as `SKL-TA1` |
| Max chunk size | No hard line cap on the layer; per-method reading depth capped at 80 lines before the skim rule applies; CI/CD `run:` blocks read in FULL (unlike `SKL-TA1`'s first-word-only cap) | 80 lines before first/last-20 skim rule triggers (non-CI/CD layers) |
| Chunk ordering | Priority order (§6.1 Layer Processing Order): most external integrations first, then Security, Application, Data, CI/CD & Deployment (direct pipeline read), Infrastructure, Observability last | Integration-density-first, Security-early |

#### Context Window Caps

| Item Type | Cap | Selection Strategy When Over Cap |
|-----------|-----|----------------------------------|
| Method body length (non-CI/CD) | 80 lines before triggering skim rule | Read first 30 + last 20 lines; read middle only if nested conditionals/retry logic present |
| CI/CD `run:` block | NO cap — read in full (v2 deliberate divergence from `SKL-TA1`'s first-word-only rule) | This is the primary architectural evidence for the CI/CD layer; truncating it reproduces the v1 accuracy problem |
| Utility/mapping method | First + last 20 lines | Skip further reading |
| Layers per Synthesis Pass | All layers — Synthesis Pass never runs per-chunk | Wait for all chunks to complete before Stage 6/7/8 |

#### Cross-Chunk Continuity Rules

- **Carried registries:** cumulative NFR Registry (NFR-ID sequential, never reset), cumulative Technical Debt & Risk Register (TD-ID sequential, never reset), cumulative validated-technologies list
- **Cross-chunk dependency rule:** if implementation in Chunk B depends on patterns/constraints found in Chunk A → note `Cross-chunk dependency: [detail]` in that chunk's Layer Summary
- **SHARED COMPONENT rule:** if a component is marked `SHARED COMPONENT` by `SKL-TA1` → cross-reference it in every chunk where it appears; note all new usage evidence
- **NFR CANDIDATE rule:** an NFR value spotted while tracing a pattern in Stage 3 is logged immediately as `NFR CANDIDATE [NFR-XX]` inline, then formalized in Stage 4 of the same chunk
- **RISK CANDIDATE rule:** a technical debt/risk item spotted while reading any stage is logged immediately as `RISK CANDIDATE [TD-XX]` inline, then formalized in Stage 5
- **ID continuity:** AP-IDs, NFR-IDs, and TD-IDs never reset — sequential across all chunks
- **Registry reset rule:** never reset cumulative registries between chunks

#### Multi-Run / Incremental Analysis

| Scenario | Behaviour |
|----------|-----------|
| Re-running on same codebase after a code change | Re-run only the layers whose files or `SKL-TA1` inventory changed; carry forward AP/NFR/TD-ID counters and unaffected layers' findings |
| Running on a subset of the codebase first | Treat the subset's layers as the full Chunk Plan; Synthesis Pass runs only across layers actually processed, noted as partial |
| Resuming after a failed run mid-chunk | Resume from `prior_chunk_plan` with all ID counters and completed chunks' registries intact |

---

## BLOCK 6 — INTELLIGENCE

### 6.1 Decision Rules & Heuristics

| ID | Trigger Condition | Agent Action | Rationale |
|----|-------------------|--------------|-----------|
| H-001 | A finding is directly and explicitly evidenced by a line of code, annotation, or configuration value | Mark `HIGH` (→ `EXTRACTED`) | Confirms direct evidence |
| H-002 | A finding is inferred from naming patterns, partial code evidence, or ambiguous config | Mark `LOW — [specific reason]` (→ `PARTIAL`); never omit | Preserves visibility of uncertain-but-real findings |
| H-003 | A pattern/NFR is implied by context but has no direct code evidence | Mark `ASSUMED — [reason]` (→ `INFERRED`) | Prevents fabricated patterns from being stated as fact |
| H-004 | Deep analysis contradicts `SKL-TA1`'s inventory | Mark `DISCREPANCY — [what SKL-TA1 said vs what code shows]`; add to Discrepancy Log; never silently update | Preserves traceability and the shared naming baseline |
| H-005 | An `SKL-TA1` low-confidence item is confirmed/resolved by implementation evidence | Mark `RESOLVED — [what code confirmed]`; remove from Validation Queue | Retires risk as evidence accumulates |
| H-006 | A CI/CD capability is confirmed by a tool invocation found in a pipeline file | Mark `HIGH — [tool name] found in [file]:[job]` | The tool name IS the evidence (v2 rule) — job/stage names alone prove nothing |

**Layer Processing Order** _(priority table)_:

| Priority | Layer | Rationale |
|---|---|---|
| 1 | Layer with the most external integrations in `SKL-TA1`'s Integration Graph | Highest coupling risk |
| 2 | Security layer | Highest risk surface — resolve early to flag critical issues |
| 3 | Application layer | Core logic and patterns |
| 4 | Data layer | — |
| 5 | CI/CD & Deployment layer | Read pipeline files directly in this chunk, not from `SKL-TA1` summary alone |
| 6 | Infrastructure layer | — |
| 7 | Observability layer (last) | Informs the Operational Assessment in the Synthesis Pass |

**How to Use Agent 1's Output:**

| Agent 1 Output | How You Use It | What You Add |
|---|---|---|
| Technology Stack Inventory | Anchor for every component — confirm version currency, EOL status, usage depth | Actual usage patterns, deprecation evidence, version risk |
| Component & Service Map | Starting list for interaction tracing and coupling analysis | Actual communication patterns, contract types, coupling strength, data ownership |
| Data Store Registry | Ground truth for persistence technology — trace connection config, access patterns, consistency model | Access patterns, transaction boundaries, consistency model, migration state |
| Infrastructure & Deployment Blueprint | Deployment topology baseline | Resource limit sufficiency, environment parity gaps, scaling posture |
| Integration & Dependency Graph | External integration list | Error handling depth, contract version, auth method, timeout/retry posture |
| Security & Configuration Snapshot | Security mechanism declarations | Implementation quality, secret rotation evidence, RBAC enforcement depth |

**Evidence-to-Capability Mapping Table** _(CI/CD Deep-Read Sub-Procedure, §5.2)_:

| Pipeline Capability | Tool Invocations / Action Names That Confirm It |
|---|---|
| Build | `docker build`, `mvn package`, `gradle build`, `dotnet build`, `npm run build`, `go build`, `cargo build`, `pip wheel`, `gem build`, `make`, `msbuild` |
| Unit Tests | `jest`, `pytest`, `dotnet test`, `go test`, `mvn test`, `gradle test`, `xunit`, `mocha`, `karma`, `rspec`, `phpunit`, `nunit`, `vitest`, `jasmine` |
| Integration Tests | `testcontainers`, `docker-compose up` + test command, `newman`, `supertest`, `pytest-django`, `playwright`, `cypress` (CI context, before deploy) |
| Code Coverage | `--collect:"XPlat Code Coverage"`, `--coverage`, `coverage run`, `jacoco`, `istanbul`, `nyc`, `lcov` |
| SAST (Static Security) | `sonar`, `sonarcloud`, `sonarqube`, `semgrep`, `codeql`, `snyk code`, `bandit`, `brakeman`, `gosec`, `spotbugs`, `pmd`, `checkmarx`, `veracode`, `eslint`/`pylint` with security plugin |
| Dependency Scan | `snyk test`, `npm audit`, `safety check`, `owasp dependency-check`, `bundle audit`, `trivy fs`, `grype`, `pip-audit`, `audit-ci`, `govulncheck` |
| Container / Image Scan | `trivy image`, `snyk container`, `grype`, `anchore-engine`, `docker scout`, `dockle`, `clair` |
| Secret / Credential Scan | `trufflehog`, `gitleaks`, `detect-secrets`, `git-secrets`, `ggshield` |
| Lint / Code Quality | `eslint`, `pylint`, `flake8`, `rubocop`, `golangci-lint`, `checkstyle`, `ktlint`, `swiftlint`, `prettier --check`, `dotnet format --verify-no-changes` |
| Infrastructure Scan | `tfsec`, `checkov`, `terrascan`, `kube-score`, `kube-linter`, `trivy config` |
| Automated Deploy | `kubectl apply`, `helm upgrade`, `terraform apply`, `aws deploy`, `az webapp deploy`, `gcloud deploy`, `ansible-playbook`, `eb deploy`, `fly deploy`, `heroku deploy` |
| Smoke / Health Check Post-Deploy | `curl`/`wget` on health endpoint, `newman`, `k6`, `artillery`, `playwright` post-deploy job, `httpie` GET on app URL |
| Auto Rollback | `kubectl rollout undo`, `helm rollback`, `az webapp deployment slot swap --rollback`, `--rollback-on-failure` flag, explicit prior-version redeploy `on: failure:` |
| Environment Promotion | Conditional `if: github.ref == 'refs/heads/main'` deploy; separate jobs per environment; manual approval gate |
| Notification | `slack`, `teams`, `sendgrid`, webhook `curl` POST, `actions/github-script` for PR comment on failure |
| Release / Versioning | `semantic-release`, `standard-version`, `git tag`, `gh release create`, `dotnet-gitversion`, `axion-release-plugin` |

**Pattern categories to scan for in non-CI/CD layers:**

| Category | Patterns to Look For |
|---|---|
| Resilience | Retry (backoff params), Circuit Breaker (threshold/window), Bulkhead (concurrency limit), Timeout (exact ms), Fallback, Rate Limiting (requests/period) |
| Data Access | Repository, Unit of Work, CQRS, Event Sourcing, Outbox, N+1 detection, explicit transaction boundaries, Optimistic/Pessimistic locking |
| Caching | Cache-Aside, Read-Through, Write-Through, invalidation, TTL values, eviction policy, cache key strategy |
| Communication | Sync REST (timeout config), gRPC, Async messaging (queue/topic names+concurrency), WebSocket, Event publishing, GraphQL |
| Security | OAuth2/OIDC (provider+scope), JWT validation (algorithm, expiry, audience), API Key, mTLS, RBAC enforcement, ABAC, Token refresh |
| Scalability | Horizontal scaling config (replica count), Connection pooling (pool size), Read replica usage, Async offload to queue |
| Observability | Structured logging (format+fields), Distributed tracing (library+sampling rate), Metric export (names+labels), Health check implementation, Correlation ID propagation |
| Deployment | Blue-green/canary config, Feature flag integration, Sidecar pattern, Health/readiness probe config, Graceful shutdown logic |

**NFR categories:**

| Category | Examples |
|---|---|
| Throughput | Connection pool max size; message consumer concurrency; thread pool size; max upload size |
| Latency | Connection timeout; read timeout; write timeout; circuit breaker open state duration |
| Reliability | Retry max attempts; retry backoff delay+multiplier; circuit breaker failure threshold |
| Data Freshness | Cache TTL; cache max entries; stale-while-revalidate window; polling interval |
| Resource Management | Connection pool min idle; idle timeout; max connection lifetime; memory limits |
| Rate | Rate limit requests-per-period; token bucket refill rate; throttle threshold |
| Availability | Health check interval/threshold; readiness probe timeout; graceful shutdown timeout |

**Risk and debt categories:**

| Category | Signals to Look For |
|---|---|
| EOL / Unsupported Technology | Version past declared EOL date; 2+ major versions behind latest; no recent commits |
| Known CVE Exposure | Declared version range includes versions with known CVEs; library flagged abandoned |
| Architecture Anti-pattern | N+1 query in loop; sync blocking call inside async handler; direct DB access from API controller; shared mutable state across threads |
| Security Vulnerability | JWT decoded but not validated; hardcoded secrets; CORS wildcard origin; no CSRF protection; SQL concatenation |
| Scalability Constraint | Fixed thread pool with no queue limit; sync external API call with no timeout; missing connection pool config (default unbounded) |
| Operational Risk | No health check endpoint; no graceful shutdown; no structured logging; no correlation ID propagation; hardcoded environment values |
| Dependency Coupling | Direct instantiation of external client with no interface; circular module dependency; shared DB table between logically separate services |
| Configuration Risk | Hardcoded magic numbers with no named constant; env-specific config committed to source; no safe default for a critical timeout |
| CI/CD Risk | No secret scanning; security scans conditionally skipped on PRs; no rollback mechanism; no post-deploy health check; deploy runs without test gate |

**Ambiguity Resolution Strategy:**

| Ambiguity Type | Resolution Strategy |
|----------------|-------------------|
| A CI/CD capability's evidence exists only under an excluding condition | Mark `Partial`, not `Present` — the runs-on condition determines actual coverage |
| A technology is declared in the manifest but has no usage evidence | Mark `LOW — declared in manifest but no usage evidence found; possible transitive dependency or unused library` |
| An NFR category has no declared values | Log `[Category] NFRs: None declared — system is using framework defaults; defaults may be unbounded and represent a scalability or reliability risk` |
| A single layer produces no architecture patterns | Note in Layer Summary and continue — normal for some layers |

**Architecture Pattern Signal Priority** _(used in Stage 3)_:

| Priority | Signal | Reliability |
|---|---|---|
| 1 — Highest | Framework annotations directly on the method (`@Retry`, `@CircuitBreaker`, `@Cacheable`, `@Transactional`, `@RateLimit`) | Ground truth — exact config values in the annotation |
| 2 | Configuration file block directly naming the pattern (Hikari pool settings, Resilience4j config, rate limiter config) | High — declarative, exact values readable |
| 3 | Code logic implementing the pattern manually (while-retry loop with backoff, try-catch with fallback) | High — values in code but may require parsing |
| 4 | Infrastructure-level pattern declarations (k8s readiness/liveness probes, Nginx rate limit directives, ALB health checks) | High — operational pattern evidence |
| 5 | Library presence in manifest without usage evidence in code | Medium — available but may not be actively used |
| 6 — Lowest | Folder naming or comments suggesting a pattern | Weak — flag for investigation only, never confirm from this alone |

**Prioritisation Logic:**
> When context window or time is constrained, analyze in this order:
1. Resolution Targets carried over from `SKL-TA1`'s Validation Queue (Chunk 0 priority)
2. Layers in Layer Processing Order (integration density → security → application → data → CI/CD → infrastructure → observability)
3. Within a layer: Stage 2 (Usage) → Stage 3 (Patterns) → Stage 4 (NFRs) → Stage 5 (Risk/Debt)
4. Synthesis Pass (Stages 6-8) only after all layer chunks are complete

### 6.2 Confidence & Uncertainty Handling

| Band | Score | Label | Agent Behaviour |
|------|-------|-------|----------------|
| High | 0.85 – 1.00 | Confident | Proceed; tag `✅ EXTRACTED`; include in output |
| Medium | 0.60 – 0.84 | Review advised | Tag `⚠️ PARTIAL`; include with warning; surface in `gaps` |
| Low | 0.40 – 0.59 | Uncertain | Tag `〰️ INFERRED` (`ASSUMED`); attempt disambiguation before finalizing |
| Very Low | 0.00 – 0.39 | Cannot determine | Tag `❓ UNKNOWN`; escalate via `gaps` / Discrepancy Log; do NOT fabricate |

**Confidence Score Calculation:**
- Method: `Rule-based`
- Formula: `(count(EXTRACTED)×1.0 + count(PARTIAL)×0.7 + count(INFERRED)×0.4 + count(UNKNOWN)×0) / total findings`

**Disambiguation Strategies** _(attempt in order before escalating)_:
1. Re-check the Architecture Pattern Signal Priority table (§6.1) — framework annotations outrank everything else
2. For CI/CD specifically: re-verify with a full pipeline file read (not `SKL-TA1`'s summary) before concluding a capability is Absent
3. If still unresolved, mark `ASSUMED`/`LOW` with a specific reason and move on — never block the chunk indefinitely

### 6.3 Evidence Hierarchy

> _When multiple sources provide conflicting information about the same fact, this ranking determines which source wins. Identical to `SKL-TA1`'s Block 6.3 — both agents in this pair operate on the same static-analysis evidence and must agree on what outranks what._

#### Source Reliability Ranking

| Rank | Source Type | Reliability | Notes |
|------|-------------|-------------|-------|
| 1 — Highest | Primary package/dependency manifest with explicit version pin | Definitive | — |
| 2 | IaC/container/CI-CD declaration — INCLUDING full pipeline file reads at this skill's depth | Very High | This skill reads deeper into rank-2 CI/CD evidence than `SKL-TA1` did |
| 3 | Lock file resolved version | High | — |
| 4 | Application config/env files, INCLUDING deep-read configuration blocks (connection pools, security filter chains) at this skill's depth | Medium-High | Primary evidence source for NFRs |
| 5 | Import/using statements with no manifest entry | Medium | — |
| 6 | Folder/naming conventions alone | Low | Must be flagged `INFERRED`/`ASSUMED` |
| 7 — Lowest | Documentation/README | Very Low | Not a primary source for this skill |

#### Conflict Resolution Rule

When two sources disagree:
1. The higher-ranked source wins
2. Document both sides: `"SKL-TA1's manifest scan says version X, but the class actually imports and uses version Y at runtime — implementation wins per evidence hierarchy"`
3. Tag the winning value with the source that provided it
4. Add the conflict to `gaps` AND the Agent 1 Discrepancy Log if it involves `SKL-TA1`'s inventory

#### Common RE Conflict Patterns

| Conflict | Typical Cause | Resolution |
|----------|--------------|------------|
| Deep analysis shows a different technology version in actual use than `SKL-TA1`'s manifest scan reported | A different version may be resolved at build time, or the manifest may be stale | Flag `DISCREPANCY`; log both; implementation evidence (rank 2-4 depending on source) generally wins over a bare manifest declaration if directly observed in a config block or build output |
| `SKL-TA1`'s CI/CD summary lists a job as present but the direct pipeline read finds no matching tool invocation | `SKL-TA1`'s fast-scan summary may have captured a job name without full step detail, or a step was since removed | The direct full pipeline read (this skill, v2) is authoritative for Stage 8; flag the discrepancy and use the direct-read result |
| An architecture pattern is declared in a config file but no code appears to invoke it | Possible dead configuration, or configuration is picked up by framework auto-wiring not visible in explicit code | Mark `PARTIAL`/`LOW` with the specific gap noted; do not assume either full adoption or complete disuse without further evidence |

---

## BLOCK 7 — INTEGRATION

### 7.1 Tools & Integrations

| Tool / API / MCP Server | Purpose | Access Method | Required |
|-------------------------|---------|---------------|---------|
| Codebase file access (VS Code workspace, uploaded zip, pasted tree/code) | Source of all deep-read input, including full CI/CD pipeline files | Read-only file access | ✓ |
| `SKL-TA1` output files | Ground-truth naming/inventory baseline | Provided as session context | ✓ |

**File Operation Permissions:**

| Operation | Permitted Paths | Restrictions |
|-----------|----------------|-------------|
| Read | Entire provided project source, excluding the exclusion list (§5.1); plus `SKL-TA1`'s 6 output files | Never opens test files (unless clarifying an ambiguous pattern), UI render code, migration files, or auto-generated files |
| Write | None — chat output only | N/A |
| Execute | `None` | Execution prohibited — pure static-read skill |

### 7.2 Dependencies

**Upstream Skills** _(must complete before this skill runs)_:

| Skill ID | Skill Name | Output Consumed | Dependency Type |
|----------|------------|-----------------|--------------------|
| `SKL-TA1` | TA Agent 1 — Stack Scout | All 6 inventory outputs | `Hard` |

**Downstream Skills** _(receive this skill's output)_:

| Skill ID | Skill Name | What This Skill Provides | Trigger Condition |
|----------|------------|--------------------------|--------------------|
| `SKL-FOUNDATION` _(not yet templated)_ | Foundation Layer | All 8 final Technology Architecture outputs, the Validation Queue, and the Agent 1 Discrepancy Log | After all four architecture pairs complete, per `prompts-ready-to-use/00_README.md` |

**External Systems:**

| System | Purpose | Data Flow | Connection Type |
|--------|---------|-----------|----------------|
| None | This skill never connects to a live database, API, or external service | — | — |

### 7.3 Context Propagation & Handoff Protocol

**Context to Carry Forward** _(always pass to all downstream skills)_:
- The full cumulative Architecture Pattern Catalog (AP-01 through AP-N), NFR Registry (NFR-01 through NFR-N), and Technical Debt & Risk Register (TD-01 through TD-N)
- All 8 final outputs
- The complete Validation Queue and the Agent 1 Discrepancy Log

**State to Persist** _(store across sessions / incremental runs)_:
- AP/NFR/TD-ID counters, cumulative registries, and Chunk Plan, to support resuming an interrupted run

**Handoff Artifact Format:**

```json
{
  "source_skill": "SKL-TA2",
  "run_id": "RUN-20260601-190000",
  "target_skill": "SKL-FOUNDATION",
  "confidence_score": 0.89,
  "context": {
    "layers_analysed": ["Application", "Security", "Data", "CI/CD & Deployment", "Infrastructure", "Observability"],
    "technical_debt_range": "TD-01 through TD-11"
  },
  "artifacts": {
    "technology_stack_assessment": "...", "architecture_pattern_catalog": "...",
    "component_interaction_contract_map": "...", "data_architecture_assessment": "...",
    "security_architecture_assessment": "...", "nfr_registry": "...",
    "technical_debt_risk_register": "...", "operational_architecture_assessment": "..."
  },
  "validation_queue": [
    { "item": "Auto Rollback CI/CD capability", "tag": "UNKNOWN", "reason": "no matching tool/action evidence found in any pipeline file" }
  ]
}
```

**Recommended Starting Point for Downstream Agent:**
> Not a fixed value — the Final Response Assembly's "Highest-priority action item" field names the top Critical or High severity Technical Debt entry (or states "None — no critical risks identified"). `SKL-FOUNDATION` should investigate that item first.

---

## BLOCK 8 — RELIABILITY

### 8.1 Error Handling & Fallbacks

| Failure Mode | Likelihood | Detection | Fallback Strategy | Escalation Rule |
|--------------|-----------|-----------|------------------|----------------|
| `SKL-TA1`'s minimum required outputs missing (OUTPUT 1, 2, 3) | L | Checked at Chunk 0 | N/A | Stop; ask the user to run `SKL-TA1` first |
| More than 50% of `SKL-TA1`'s items flagged low confidence | M | Counted at Chunk 0 | N/A | Stop; ask the user to review `SKL-TA1`'s Validation Queue before proceeding |
| `SKL-TA1`'s Component Map has only 1 component, no data store/integration | L | Checked at Chunk 0 | N/A | Stop; confirm with the user whether this is a scanning failure or a genuine library project |
| Deep analysis in Chunk 1 reveals a fundamentally different architecture (event sourcing, CQRS read-model, multi-tenancy, service mesh) | L | Observed during early chunks | N/A | Stop; ask whether `SKL-TA1` should re-run with this knowledge first |
| Security layer analysis reveals plaintext secrets committed to source control | L | Observed during Security layer chunk | N/A | **Stop immediately**; alert the user to this Critical risk before completing any remaining analysis; location only, never the secret value |
| A single layer produces no architecture patterns | M | Observed during Stage 3 | Note in Layer Summary; continue | Continue |
| A technology has no usage evidence in source | M | Observed during Stage 2 | Mark `LOW — declared in manifest but no usage found`; continue | Continue |
| An NFR category has no declared values | M | Observed during Stage 4 | Log "None declared — using framework defaults; may be unbounded risk"; continue | Continue |
| No CI/CD pipeline files found during direct read | L | CI/CD Deep-Read Sub-Procedure step 1-2 | Flag all Stage 8 CI/CD capabilities as Absent with Critical severity | Continue |

**Human Review Triggers** _(mandatory escalation conditions)_:
- [ ] Overall `confidence_score` below 0.60
- [ ] `gaps` list contains more than 10 unresolved items
- [ ] More than 30% of findings tagged `INFERRED` or `UNKNOWN`
- [ ] Evidence hierarchy conflict found that cannot be resolved automatically (§6.3)
- [ ] Any entry in the Agent 1 Discrepancy Log remains unresolved at Final Response Assembly
- [ ] Plaintext secrets found committed to source control (always escalates immediately, regardless of other thresholds)

**Escalation Path:**
1. Flag the item in the Validation Queue or Agent 1 Discrepancy Log with its specific reason
2. Carry it into the Handoff Note to `SKL-FOUNDATION`, marked as the highest-priority action item if it is Critical/High severity
3. Plaintext-secret findings escalate to the user immediately, not deferred to the Final Response Assembly
4. If `SKL-FOUNDATION` also cannot resolve remaining items, they surface to human review at the Gate G1 stakeholder checkpoint

**Partial Output Policy:**
> A partial output (not all 8 outputs fully populated) is acceptable and preferable to no output — every layer and stage reached should be reported in full, with unreached items explicitly listed in `gaps`. The Synthesis Pass should still run on whatever layer chunks did complete, noting that cross-layer coverage is partial.

### 8.2 Validation & QA Checklist

**Agent Self-Check** _(run before emitting any output)_:
- [ ] All required output schema fields are populated
- [ ] Every finding carries a `confidence_tag` from the taxonomy in §4.3
- [ ] `confidence_score` calculated per the method in §6.2
- [ ] `gaps` populated for all `INFERRED`, `UNKNOWN`, and below-threshold items
- [ ] `handoff_context` package is well-formed and includes the Agent 1 Discrepancy Log
- [ ] No secret VALUES in output — locations only
- [ ] No fabricated architecture patterns, NFRs, or risk items — every one is evidenced or explicitly marked `ASSUMED`
- [ ] Evidence hierarchy applied to all conflicting signals (§6.3)
- [ ] Chunking registries (NFR Registry, Technical Debt Register, AP/NFR/TD-ID counters) are cumulative — no resets between chunks (§5.4)
- [ ] Every CI/CD capability claim cites a specific tool/action name + file + job — none claimed from a stage/job name alone
- [ ] No numeric threshold, version number, or configuration parameter is paraphrased

**Human Review Checklist:**
- [ ] Findings align with known system behaviour
- [ ] `INFERRED`/`ASSUMED` findings are plausible and flagged for confirmation
- [ ] `UNKNOWN`/`DISCREPANCY` findings are genuinely unresolvable from available artifacts
- [ ] No `EXTRACTED` findings that appear to be fabricated
- [ ] Coverage meets the threshold defined in §5.3
- [ ] Exact configuration values preserved throughout (no paraphrased thresholds)
- [ ] CI/CD Pipeline Maturity assessment is evidence-based, not name-based

**Automated Test Cases:**

| Test ID | Scenario | Input | Expected Output | Pass Criteria |
|---------|----------|-------|-----------------|---------------|
| T-001 | Standard architecture pattern extraction | `@Retry(maxAttempts=3, backoff=@Backoff(delay=1000, multiplier=2.0, maxDelay=8000))` on a payment method | AP entry with all exact values preserved: 3 attempts, 1000ms delay, 2.0x multiplier, 8000ms max | Exact values present, not paraphrased as "retry logic exists" |
| T-002 | Evidence-based CI/CD maturity (v2) | Pipeline with `run: dotnet test`, `run: snyk test`, `run: trivy fs`, a `sonarcloud-github-action` | Unit Tests, SAST, Dependency Scan, Container Scan all marked Present with specific tool+file+job evidence | Never marked Present from a job named "quality" alone |
| T-003 | NFR extraction from Hikari pool config | `maximum-pool-size: 20`, `minimum-idle: 5`, `connection-timeout: 30000` | 3 separate NFR rows, each with its own ID and exact value | No combining into a single "connection pool configured" row |
| T-004 | Plaintext secret discovered | A hardcoded database password found in a committed config file | Immediate stop and escalation; location recorded, value never repeated | Escalates before continuing with remaining analysis |

---

## BLOCK 9 — REFERENCE

### 9.1 Examples

#### Canonical Example (Standard Case)

**Scenario:**
> Reading `PaymentService.java`'s `processPayment()` method to extract a Retry + Circuit Breaker pattern pair, using `SKL-TA1`'s Component Map as the anchor.

**Input:**
```json
{
  "ta1_outputs": { "component_service_map": ["PaymentService"], "integration_dependency_graph": ["External Payment Gateway"] },
  "project_source": "Java Spring Boot project, PaymentService.java present with @Retry and @CircuitBreaker annotations"
}
```

**Expected Output:**
```json
{
  "confidence_score": 0.95,
  "findings": {
    "architecture_pattern_catalog": [
      { "id": "AP-01", "pattern": "Retry with Exponential Backoff", "category": "Resilience", "applies_to": "PaymentService -> External Payment Gateway", "exact_configuration": "Max 3 attempts; initial delay 1,000ms; multiplier 2.0x; max delay 8,000ms", "confidence_tag": "EXTRACTED", "source": "PaymentService.processPayment()" },
      { "id": "AP-02", "pattern": "Circuit Breaker", "category": "Resilience", "applies_to": "PaymentService -> External Payment Gateway", "exact_configuration": "Named 'paymentGateway'; sliding window 10 calls; opens at 50% failure rate; fallback: fallbackCharge()", "confidence_tag": "EXTRACTED", "source": "PaymentService.processPayment()" }
    ]
  },
  "gaps": []
}
```

**Notes:**
> Canonical because both patterns are read directly from explicit framework annotations with every configuration value preserved verbatim.

#### Edge Cases

| ID | Description | Input Pattern | Expected Behaviour | Risk if Mishandled |
|----|-------------|--------------|-------------------|-------------------|
| E-001 | CI/CD capability evidence exists only under an excluding condition | `snyk test` runs only under `if: github.ref == 'refs/heads/main'` | Marked `Partial`, not `Present` — PRs are excluded from the scan | Marking `Present` overstates actual security coverage on PRs, where vulnerabilities would otherwise ship unreviewed |
| E-002 | NFR category with no declared values | No rate limit config found anywhere in the Application layer | Logged as "Rate NFRs: None declared — system using framework defaults; may be unbounded and represent a scalability/reliability risk" | Silently omitting this hides a real operational risk |
| E-003 | Plaintext secret found in a committed config file | A database password literal in `appsettings.Production.json` | Immediate stop; user alerted; location recorded, value never repeated in output | Continuing analysis without escalating leaves a Critical security exposure undisclosed |

#### Anti-Patterns _(What NOT to Do)_

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|---------------|-----------------|
| Marking a CI/CD "quality" job as SAST-present because the job name suggests it | A job named "quality" could contain only linting — the v1 defect this skill's v2 changes specifically fixed | Always require a specific tool/action name as evidence |
| Writing "some retry logic exists" instead of the exact backoff parameters | Architecturally worthless — not actionable for capacity planning or incident response | Always preserve exact configuration values |
| Combining "connection pool configured" into one NFR row instead of separate max-size/min-idle/timeout rows | Destroys operationally critical information | Each distinct numeric value is its own NFR row |
| Silently overwriting `SKL-TA1`'s version record when implementation shows a different version | Corrupts the shared naming baseline and hides the disagreement from review | Always log to the Agent 1 Discrepancy Log |
| Running Stage 8 (Operational Assessment) per-layer-chunk instead of once in the Synthesis Pass | Produces incomplete cross-layer conclusions that must be redone anyway | Run Stages 6-8 once, after all chunks complete |

### 9.2 Changelog & Version Notes

| Version | Date | Author | Change Description |
|---------|------|--------|--------------------|
| 1.0.0 | (unspecified) | TA Reverse Engineering System | Original v1 — CI/CD maturity assessed by stage/job name matching; low accuracy |
| 2.0.0 | 2026-06-01 | TA Reverse Engineering System | Original `06_TA_Agent2_DeepAnalyst.md` prompt (v2, June 2026). Reading strategy: CI/CD pipeline files now read in full during the CI/CD layer chunk (not inferred from Agent 1 summary) — primary fix for low CI/CD accuracy. Stage 3: dedicated CI/CD deep-read sub-procedure added, mapping tool invocations to pipeline capabilities via an evidence table. Stage 8: evidence-based CI/CD maturity assessment replaces name-based stage matching. |
| 2.0.0 (template conversion) | 2026-07-06 | Skill file conversion pass | Reformatted into the `sdlc_skill_file_template_v2.md` 9-block structure; no behavioral change to the underlying analysis logic — added `confidence_tag` taxonomy mapping (including `ASSUMED`/`DISCREPANCY`/`RESOLVED` legacy labels), the evidence hierarchy (kept identical to `SKL-TA1`'s), a JSON output schema, and explicit chunking caps that were implicit in the original prose. |

---

_Template v2.0 · 9 Blocks · 24 Sections · SDLC Agentic AI Platform · RE-optimised_
_Converted from: `prompts-ready-to-use/06_TA_Agent2_DeepAnalyst.md` · Pair with: `skill-files/05_TA_Agent1_StackScout.md` (`SKL-TA1`)_
