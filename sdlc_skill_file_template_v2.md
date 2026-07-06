# SKILL FILE: [Skill Name]

> Skill ID: `SKL-XXX` | Version: `1.0.0` | Status: `DRAFT`
> SDLC Phase: `[Analysis / Design / Development / Testing / Deployment / Maintenance]`
> Domain: `Reverse Engineering` | Sub-Domain: `[Code Analysis / DB Schema / API Discovery / UI Flow / Business Logic / Data Flow]`
> Owner: `[Team / Member]` | Last Updated: `YYYY-MM-DD`

---

## BLOCK 1 — IDENTITY

### 1.1 Skill Metadata

| Field | Value |
|-------|-------|
| Skill ID | `SKL-XXX` |
| Skill Name | |
| Version | `1.0.0` |
| SDLC Phase | |
| Domain | `Reverse Engineering` |
| Sub-Domain | |
| Owner | |
| Tags | |
| Status | `Draft / Review / Active / Deprecated` |
| Paired With | `[SKL-YYY if this is one of an agent pair]` |

### 1.2 Goal & Success Criteria

**Primary Goal:**
> _One sentence: what does this skill accomplish?_

**Secondary Goals:**
-
-

**Success Definition:**
> _How do you know this skill ran successfully? Be specific and measurable._
> _Example: "Output contains a complete entity-relationship map with ≥90% coverage of tables identified in the schema, with all foreign key relationships resolved and tagged EXTRACTED or PARTIAL."_

**What This Skill Does NOT Do:**
> _Explicitly list what is out of scope — especially work that belongs to a paired agent._
-
-

---

## BLOCK 2 — ACTIVATION

### 2.1 Trigger Conditions

**Explicit Triggers** _(user states these directly)_:
-
-

**Implicit Signals** _(infer from conversation context or orchestrator routing)_:
-
-

**Activation Keywords / Patterns:**
```
[list keywords, phrases, or intent signals the orchestrator detects to route here]
```

### 2.2 Pre-conditions & Guards

**Must Be True Before Activation:**
- [ ]
- [ ]

**Disqualifiers** _(do NOT activate if any of these are true)_:
- [ ] Paired agent has not yet completed its run (if this is Agent 2 of a pair)
- [ ]

---

## BLOCK 3 — CONTEXT

> _Block 3 is the most critical block for Reverse Engineering skills. Precision here directly determines output accuracy._

### 3.1 Environment Context

| Dimension | Details |
|-----------|---------|
| Target Language(s) | |
| Framework(s) | |
| Platform / OS | |
| Database Type | |
| Architecture Pattern | `Monolith / Microservices / Event-driven / Serverless / Hybrid` |
| Available Tools | |
| Repository Access | `Read-only / Read-Write` |
| Authentication Level | |

### 3.2 Artifact Taxonomy

> _Which artifact types can this skill ingest and analyze?_

| Artifact Type | Supported | Accepted Formats | Notes |
|---------------|-----------|-----------------|-------|
| Source Code | ✓ / ✗ | `.java`, `.py`, `.cs`, `.ts`, etc. | |
| Database Schema | ✓ / ✗ | DDL, `.sql`, ERD export | |
| API Contracts | ✓ / ✗ | OpenAPI, WSDL, Swagger | |
| Configuration Files | ✓ / ✗ | `.yaml`, `.json`, `.env`, `.xml` | |
| UI Wireframes / Designs | ✓ / ✗ | Figma export, screenshots | |
| Application Logs / Traces | ✓ / ✗ | `.log`, structured JSON, APM exports | |
| Test Cases | ✓ / ✗ | JUnit, pytest, Cucumber | |
| Documentation | ✓ / ✗ | `.md`, `.pdf`, wiki pages | |
| Infrastructure as Code | ✓ / ✗ | Terraform, CloudFormation, Helm | |
| Binary / Compiled Code | ✓ / ✗ | `.jar`, `.dll`, `.exe` | |

### 3.3 Domain Knowledge References

**Architectural Patterns to Recognise:**
-

**Design Patterns to Detect** _(e.g. Repository, CQRS, Singleton, Saga)_:
-

**Standards & Protocols:**
-

**Domain Glossary:**

| Term | Definition |
|------|-----------|
| | |

**RE Checklist for This Sub-Domain:**
> _Specific things this skill must look for in this sub-domain._
- [ ]
- [ ]

---

## BLOCK 4 — INTERFACE

### 4.1 Input Specification

#### Required Inputs

| Field | Type | Format / Example | Description |
|-------|------|-----------------|-------------|
| | | | |

#### Optional Inputs

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| | | | |

#### Input Validation Rules
-
-

#### Input Rejection Criteria
-
-

### 4.2 Output Specification

#### Standard Output Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `skill_id` | string | ✓ | Executing skill identifier |
| `run_id` | string | ✓ | Unique run identifier (`RUN-YYYYMMDD-HHMMSS`) |
| `confidence_score` | float 0–1 | ✓ | Overall confidence in output quality |
| `analysis_depth` | string | ✓ | Level performed: `system / module / class / function / line` |
| `coverage_pct` | float 0–1 | ✓ | % of input artifact analysed |
| `findings` | object | ✓ | Primary output artifact — structure defined below |
| `gaps` | array | ✓ | Unresolved items — must not be empty if coverage < 100% |
| `recommendations` | array | | Suggested next steps |
| `handoff_context` | object | | Context package for the downstream skill |

#### `findings` Object Structure _(skill-specific — define for this skill)_

```json
{
  "skill_id": "SKL-XXX",
  "run_id": "RUN-YYYYMMDD-HHMMSS",
  "confidence_score": 0.85,
  "analysis_depth": "module",
  "coverage_pct": 0.92,
  "findings": {
    // define the specific structure this skill produces
    // every field should carry a confidence_tag (see section 4.3)
  },
  "gaps": [
    { "area": "", "reason": "", "severity": "High / Med / Low" }
  ],
  "recommendations": [],
  "handoff_context": {}
}
```

#### Quality Criteria
-
-

### 4.3 Confidence & Evidence Tagging Schema

> _Every finding in the output must carry a tag declaring how it was obtained. This is the core quality signal for RE work — it tells downstream agents and human reviewers how much to trust each finding._

#### Tag Taxonomy

| Tag | Symbol | Definition | Downstream Action |
|-----|--------|-----------|------------------|
| EXTRACTED | `✅` | Found directly and unambiguously in source (code, schema, config, live DB) | Proceed; no review needed unless conflicted |
| PARTIAL | `⚠️` | Some evidence exists but not complete — e.g. field defined but no usage found | Include with warning flag; surface in `gaps` |
| INFERRED | `〰️` | Reasoned from context, naming, or patterns — not directly coded | Mark as inferred; require human confirmation before use in downstream decisions |
| UNKNOWN | `❓` | Cannot be determined from available artifacts | Escalate; populate `gaps`; do NOT fabricate |

#### Mandatory Tagging Rules

- Every finding in the `findings` object that involves a claim about business logic, a state, a relationship, or a rule **must** carry a `confidence_tag`
- The overall `confidence_score` is derived from the distribution of tags across findings — define the calculation method in section 6.2
- `INFERRED` and `UNKNOWN` findings must always appear in `gaps` with a reason
- Findings marked `UNKNOWN` must never be included in documents presented to stakeholders without explicit human sign-off

#### Display Convention

```
✅ HIGH     — EXTRACTED from source — [source file:line]
⚠️ PARTIAL  — Partial evidence — [what was found vs what's missing]
〰️ INFERRED — Reasoned from [context/pattern/naming] — requires validation
❓ UNKNOWN  — Cannot determine from available artifacts
```

---

## BLOCK 5 — EXECUTION

### 5.1 Constraints & Guardrails

**Hard Constraints _(MUST NOT do these under any circumstances)_:**
-
-

**Soft Constraints _(PREFER NOT TO — may override with justification)_:**
-
-

**Scope Boundaries:**

| IN Scope | OUT of Scope |
|----------|-------------|
| | |

**Data Sensitivity Rules:**

| Data Type | Rule |
|-----------|------|
| PII (names, emails, IDs) | |
| Credentials / Secrets | |
| Confidential Business Logic | |
| Third-party IP / Licensed Code | |

**Exclusion List** _(never scan these)_:
```
[directories, file types, patterns to always skip]
e.g. node_modules/, .git/, dist/, build/, *.min.js, *.lock, __pycache__/
```

### 5.2 Process & Methodology

> _The ordered steps this skill executes. Each step must have a clear input, action, and output._

**Step 1 — [Name]**
- Input:
- Action:
- Output:
- Decision Point: _(if applicable)_

**Step 2 — [Name]**
- Input:
- Action:
- Output:

> _Add steps as needed._

**Decision Tree:**

| Condition | Branch A | Branch B | Default |
|-----------|----------|----------|---------|
| | | | |

**Iteration / Retry Rules:**

| Trigger | Max Retries | Strategy |
|---------|------------|---------|
| | | |

### 5.3 Analysis Depth & Granularity

| Level | Description | When to Activate | Typical Output Artifact |
|-------|-------------|-----------------|------------------------|
| System | Full system / portfolio overview | Initial discovery, migration scoping | Architecture diagram, component map |
| Module / Service | Component-level analysis | Service dependency mapping | Component catalogue |
| Class / Entity | Object-level analysis | Domain model extraction | Class / entity model |
| Function / Method | Procedural analysis | Business logic extraction | Function catalogue, pseudocode |
| Line / Statement | Detailed code inspection | Security audit, compliance check | Annotated code listing |

**Default Depth Level for This Skill:**

**Coverage Threshold:**
> _Minimum % of the artifact that must be analysed before output is emitted._

**Action if Coverage Threshold Not Met:**

**Reading Depth Rules** _(what to read deep vs skim vs skip)_:

| File / Artifact Type | Reading Rule | Reason |
|---------------------|--------------|--------|
| Validation / conditional logic | Read in full | Contains business rules |
| State transition methods | Read in full | Defines lifecycle |
| Utility / mapping methods | Skim (first + last 20 lines) | No decision logic |
| Test files | Skip unless rule is unclear | Use only to clarify intent |
| Migration files | Field names only | Entity structure — not logic |

### 5.4 Chunking & Context Management

> _Critical for RE on large codebases. This section defines how the skill handles inputs that exceed a single context window and how state is maintained across chunks._

#### Chunking Strategy

| Dimension | Rule | Default |
|-----------|------|---------|
| Chunk unit | What is one "chunk"? (file / class / domain / method batch) | |
| Max chunk size | Maximum lines or characters per chunk | |
| Chunk ordering | How to order chunks for processing (complexity-first / dependency-first / alphabetical) | |

#### Context Window Caps

> _Hard limits applied before building the LLM prompt. These prevent token overflow and force prioritisation._

| Item Type | Cap | Selection Strategy When Over Cap |
|-----------|-----|----------------------------------|
| Business methods / functions | | e.g. prioritise by business keyword score |
| Method body length (chars) | | e.g. truncate to N chars |
| Config parameters | | e.g. keep business-tagged only |
| DB tables | | e.g. keep tables with FK relationships first |
| Log events | | e.g. keep most frequent sequences |

#### Cross-Chunk Continuity Rules

> _What must be carried forward across chunks to maintain consistency._

- **Carried registries:** [list what accumulates across chunks — entity list, rule catalog, role list, etc.]
- **SHARED entity rule:** If an entity appears in more than one chunk → mark `🔗 SHARED ENTITY`; carry in every subsequent "Carried Forward" block
- **ID continuity:** [e.g. BR-IDs never reset between chunks — sequential across all chunks]
- **Registry reset rule:** Never reset cumulative registries between chunks

#### Multi-Run / Incremental Analysis

| Scenario | Behaviour |
|----------|-----------|
| Re-running on same codebase after a code change | |
| Running on a subset of the codebase first | |
| Resuming after a failed run mid-chunk | |

---

## BLOCK 6 — INTELLIGENCE

> _Block 6 transforms a scripted tool into an intelligent agent. The richer this block, the less human correction the output needs._

### 6.1 Decision Rules & Heuristics

> _Rules the agent applies autonomously during execution._

| ID | Trigger Condition | Agent Action | Rationale |
|----|-------------------|--------------|-----------|
| H-001 | | | |
| H-002 | | | |

**Pattern Recognition Catalog:**

| Pattern Name | Signature / Indicator | RE Significance | Action |
|--------------|----------------------|-----------------|--------|
| | | | |

**Ambiguity Resolution Strategy:**

| Ambiguity Type | Resolution Strategy |
|----------------|-------------------|
| Conflicting naming conventions | |
| Undocumented magic values | |
| Implicit business rules in code | |
| Entity defined but never instantiated | |

**Prioritisation Logic:**
> _When context window or time is constrained, analyze in this order:_
1.
2.
3.

### 6.2 Confidence & Uncertainty Handling

| Band | Score | Label | Agent Behaviour |
|------|-------|-------|----------------|
| High | 0.85 – 1.00 | Confident | Proceed; tag `✅ EXTRACTED`; include in output |
| Medium | 0.60 – 0.84 | Review advised | Tag `⚠️ PARTIAL`; include with warning; surface in `gaps` |
| Low | 0.40 – 0.59 | Uncertain | Tag `〰️ INFERRED`; pause; attempt disambiguation |
| Very Low | 0.00 – 0.39 | Cannot determine | Tag `❓ UNKNOWN`; escalate; do NOT fabricate |

**Confidence Score Calculation:**
> _How is the overall `confidence_score` computed from individual finding tags?_
- Method: `Rule-based / LLM self-assessed / Hybrid`
- Formula:
  > _Example: (count of EXTRACTED × 1.0 + PARTIAL × 0.7 + INFERRED × 0.4 + UNKNOWN × 0) / total findings_

**Disambiguation Strategies** _(attempt in order before escalating)_:
1.
2.
3.

### 6.3 Evidence Hierarchy

> _When multiple sources provide conflicting information about the same fact, this ranking determines which source wins. Critical for RE work where code, migrations, tests, docs, and live databases can disagree._

#### Source Reliability Ranking

| Rank | Source Type | Reliability | Notes |
|------|-------------|-------------|-------|
| 1 — Highest | Live database (queried directly) | Definitive | What the system actually contains at runtime |
| 2 | Migration files (chronological) | Very High | Ground truth for schema evolution |
| 3 | ORM entity / model class | High | Declared structure — may lag behind DB |
| 4 | Repository / query layer | High | Shows what data is actually read/written |
| 5 | Service / business logic layer | Medium | Shows intent, may have bugs |
| 6 | Test files | Medium | Shows expected behaviour — may be incomplete |
| 7 | Configuration files | Medium | Runtime parameters — may differ per environment |
| 8 | Documentation / comments | Low | Often stale — verify against code |
| 9 — Lowest | Naming conventions alone | Very Low | Inference only — must be flagged INFERRED |

> _Add or adjust rows for your specific technology stack._

#### Conflict Resolution Rule

When two sources disagree:
1. The higher-ranked source wins
2. Document both sides in the output: `"code says X, live DB says Y — live DB wins per evidence hierarchy"`
3. Tag the winning value with the source that provided it
4. Add the conflict to the `gaps` array with both values and the resolution applied

#### Common RE Conflict Patterns

| Conflict | Typical Cause | Resolution |
|----------|--------------|------------|
| Entity in ORM but not in DB | Migration not run or entity deleted | Live DB wins; flag gap |
| Field in migration but not in ORM entity | ORM entity not updated after migration | Migration wins; flag for developer review |
| Business rule in test but not in production code | Rule removed from code but test not updated | Flag as discrepancy; mark PARTIAL |
| Config value differs between environments | Environment-specific override | Document all values; do not pick one |

---

## BLOCK 7 — INTEGRATION

### 7.1 Tools & Integrations

| Tool / API / MCP Server | Purpose | Access Method | Required |
|-------------------------|---------|---------------|---------|
| | | | ✓ / ✗ |

**File Operation Permissions:**

| Operation | Permitted Paths | Restrictions |
|-----------|----------------|-------------|
| Read | | |
| Write | | |
| Execute | `None` | Execution prohibited unless explicitly listed |

### 7.2 Dependencies

**Upstream Skills** _(must complete before this skill runs)_:

| Skill ID | Skill Name | Output Consumed | Dependency Type |
|----------|------------|-----------------|--------------------|
| | | | `Hard / Soft` |

**Downstream Skills** _(receive this skill's output)_:

| Skill ID | Skill Name | What This Skill Provides | Trigger Condition |
|----------|------------|--------------------------|--------------------|
| | | | |

**External Systems:**

| System | Purpose | Data Flow | Connection Type |
|--------|---------|-----------|----------------|
| | | `→ / ← / ↔` | `Sync / Async` |

### 7.3 Context Propagation & Handoff Protocol

**Context to Carry Forward** _(always pass to all downstream skills)_:
-
-

**State to Persist** _(store across sessions / incremental runs)_:
-
-

**Handoff Artifact Format:**

```json
{
  "source_skill": "SKL-XXX",
  "run_id": "RUN-YYYYMMDD-HHMMSS",
  "target_skill": "SKL-YYY",
  "confidence_score": 0.85,
  "context": {
    // fields the downstream skill needs to continue
  },
  "artifacts": {
    // produced artifacts passed forward
  },
  "validation_queue": [
    // unresolved LOW/UNKNOWN items for the downstream skill to investigate
  ]
}
```

**Recommended Starting Point for Downstream Agent:**
> _When this handoff arrives, which domain / entity / area should the next agent investigate first, and why?_

---

## BLOCK 8 — RELIABILITY

### 8.1 Error Handling & Fallbacks

| Failure Mode | Likelihood | Detection | Fallback Strategy | Escalation Rule |
|--------------|-----------|-----------|------------------|----------------|
| | `H / M / L` | | | |

**Human Review Triggers** _(mandatory escalation conditions)_:
- [ ] Overall `confidence_score` below 0.60
- [ ] `gaps` list contains more than `N` items
- [ ] More than `X%` of findings tagged `INFERRED` or `UNKNOWN`
- [ ] Evidence hierarchy conflict found that cannot be resolved automatically
- [ ]

**Escalation Path:**
1.
2.
3.

**Partial Output Policy:**
> _Under what conditions is a partial output acceptable? Is it better than no output?_

### 8.2 Validation & QA Checklist

**Agent Self-Check** _(run before emitting any output)_:
- [ ] All required output schema fields are populated
- [ ] Every finding carries a `confidence_tag` from the taxonomy in section 4.3
- [ ] `confidence_score` calculated per the method in section 6.2
- [ ] `gaps` populated for all `INFERRED`, `UNKNOWN`, and below-threshold items
- [ ] `handoff_context` package is well-formed and includes the `validation_queue`
- [ ] No PII or credentials in output (unless explicitly in scope)
- [ ] No fabricated entities, relationships, or business rules
- [ ] Evidence hierarchy applied to all conflicting signals (section 6.3)
- [ ] Chunking registries are cumulative — no resets between chunks (section 5.4)
- [ ]

**Human Review Checklist:**
- [ ] Findings align with known system behaviour
- [ ] `INFERRED` findings are plausible and flagged for confirmation
- [ ] `UNKNOWN` findings are genuinely unresolvable from available artifacts
- [ ] No `EXTRACTED` findings that appear to be fabricated
- [ ] Coverage meets the threshold defined in section 5.3
- [ ]

**Automated Test Cases:**

| Test ID | Scenario | Input | Expected Output | Pass Criteria |
|---------|----------|-------|-----------------|---------------|
| T-001 | | | | |

---

## BLOCK 9 — REFERENCE

### 9.1 Examples

#### Canonical Example (Standard Case)

**Scenario:**
> _Brief description — the "happy path."_

**Input:**
```json
{
}
```

**Expected Output:**
```json
{
  "confidence_score": 0.87,
  "findings": {
    // show confidence_tag on each finding
  },
  "gaps": []
}
```

**Notes:**
> _What makes this the canonical case?_

#### Edge Cases

| ID | Description | Input Pattern | Expected Behaviour | Risk if Mishandled |
|----|-------------|--------------|-------------------|-------------------|
| E-001 | Entity defined but never queried | | Tag PARTIAL; flag in gaps | Phantom entity appears in domain model |
| E-002 | Business rule in test only, not in production code | | Tag INFERRED; flag discrepancy | Rule treated as active when it isn't |
| E-003 | Context window cap reached mid-domain | | Emit partial output; mark coverage_pct; note in gaps | Silent truncation misrepresents coverage |

#### Anti-Patterns _(What NOT to Do)_

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|---------------|-----------------|
| Fabricating business logic from variable names alone | Creates EXTRACTED findings that are actually INFERRED | Mark as INFERRED; flag for human review |
| Resetting ID counters (BR-IDs, chunk registries) between chunks | Breaks traceability and creates duplicate IDs | Keep all registries cumulative across chunks |
| Treating all `if/else` branches as separate business rules | Inflates rule count; obscures actual policy | Group by business intent, not code branching |
| Silently overriding an upstream agent's named artifact | Makes the output diverge from the agreed naming baseline | Log as DISCREPANCY; never silently update |
| Skipping the Evidence Hierarchy when sources conflict | Arbitrary resolution; inconsistent output quality | Always rank sources and document which won |

### 9.2 Changelog & Version Notes

| Version | Date | Author | Change Description |
|---------|------|--------|--------------------|
| 1.0.0 | YYYY-MM-DD | | Initial draft |

---

_Template v2.0 · 9 Blocks · 24 Sections · SDLC Agentic AI Platform · RE-optimised_
