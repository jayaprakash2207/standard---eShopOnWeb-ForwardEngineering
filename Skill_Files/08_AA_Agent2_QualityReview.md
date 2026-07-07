# SKILL FILE: AA Agent 2 — Quality Review

> Skill ID: `SKL-AA2` | Version: `1.0.0` | Status: `ACTIVE`
> SDLC Phase: `Analysis`
> Domain: `Reverse Engineering` | Sub-Domain: `Code Analysis`
> Owner: `[Team / Member]` | Last Updated: `2026-06-01`

---

## BLOCK 1 — IDENTITY

### 1.1 Skill Metadata

| Field | Value |
|-------|-------|
| Skill ID | `SKL-AA2` |
| Skill Name | AA Agent 2 — Quality Review |
| Version | `1.0.0` |
| SDLC Phase | `Analysis` |
| Domain | `Reverse Engineering` |
| Sub-Domain | `Code Analysis` |
| Owner | `[Team / Member]` |
| Tags | `application-architecture`, `quality-review`, `gate-g1`, `agent-2-of-2` |
| Status | `Active` |
| Paired With | `SKL-AA1` (AA Agent 1 — Application Extractor) — hard dependency, this skill reviews `SKL-AA1`'s complete output set |

### 1.2 Goal & Success Criteria

**Primary Goal:**
> Review `SKL-AA1`'s generated Application Architecture outputs for completeness, traceability, consistency, and usefulness — producing a PASS/PARTIAL/FAIL verdict per check, with PARTIAL/FAIL items explained clearly enough to act on.

**Secondary Goals:**
- Verify structural integrity (all required files exist, all JSON is valid, all IDs referenced actually resolve) before assessing quality
- Verify every claim has evidence and every unknown is a logged open question, not a silent gap
- Verify the forward-engineering outputs are concrete enough to actually drive modernization planning, not generic filler

**Success Definition:**
> A run is successful when all 11 checks (§5.2) have been run against `SKL-AA1`'s full output set, each is marked PASS/PARTIAL/FAIL with a clear explanation for anything not PASS, and the 3 required review artifacts (`quality-review.md`, `executive-summary-for-review.md`, `final-sanity-check.md`) are written with a clear overall recommendation for whether the output is ready to feed the Foundation Layer / Gate G1.

**What This Skill Does NOT Do:**
> This is a review skill — it verifies `SKL-AA1`'s output, it does not redo the extraction.
- Does not re-run any of `SKL-AA1`'s 13 stages or regenerate its artifacts
- Does not invent new architecture findings not already present in `SKL-AA1`'s output — a review that adds NEW findings not evidenced in the reviewed files is out of scope for this skill (unlike `SKL-DA2`, which is explicitly an enrichment agent; this skill is explicitly a verification agent — see §9.2 for why this distinction matters)
- Does not mark anything PASS without checking it — a rubber-stamp review with no cited evidence is a failure of this skill's own purpose

---

## BLOCK 2 — ACTIVATION

### 2.1 Trigger Conditions

**Explicit Triggers** _(user states these directly)_:
- "review the architecture output"
- "run quality review"
- "check the AA outputs"
- "is this ready for review"

**Implicit Signals** _(infer from conversation context or orchestrator routing)_:
- `SKL-AA1` has completed and its output files exist at the expected location
- The user wants a PASS/PARTIAL/FAIL verdict before sharing the architecture documentation with stakeholders

**Activation Keywords / Patterns:**
```
"review the architecture output" | "run quality review" | "check the AA outputs" |
"is this ready for review" | "quality gate" | "sanity check"
```

### 2.2 Pre-conditions & Guards

**Must Be True Before Activation:**
- [ ] `SKL-AA1`'s output files exist at the input location (see §7.2 for the path-naming discrepancy this skill inherits from its source prompt)
- [ ] At least the core JSON artifacts (`system-inventory.json`, `module-boundary-map.json`, `component-registry.json`, `dependency-graph.json`) are present

**Disqualifiers** _(do NOT activate if any of these are true)_:
- [ ] `SKL-AA1` has not yet run — no output files exist at all
- [ ] The user is asking for a fresh extraction, not a review — route to `SKL-AA1` instead
- [ ] Fewer than half of the 14 required artifacts exist — too little to meaningfully review; recommend re-running `SKL-AA1` instead

---

## BLOCK 3 — CONTEXT

> _Block 3 is the most critical block for Reverse Engineering skills. Precision here directly determines output accuracy._

### 3.1 Environment Context

| Dimension | Details |
|-----------|---------|
| Target Language(s) | Not applicable — this skill reviews structured JSON/Markdown artifacts, not source code directly |
| Framework(s) | Not applicable |
| Platform / OS | Runs inside the same coding agent environment as `SKL-AA1` |
| Database Type | Not applicable |
| Architecture Pattern | Verifies `SKL-AA1`'s stated pattern is evidence-backed; does not independently re-detect it |
| Available Tools | Read access to `SKL-AA1`'s output folder; write access to the same folder for the 3 review artifacts |
| Repository Access | `Read-Write` (write scoped to the architecture output folder only) |
| Authentication Level | None required |

### 3.2 Artifact Taxonomy

> _Which artifact types can this skill ingest and analyze?_

| Artifact Type | Supported | Accepted Formats | Notes |
|---------------|-----------|-----------------|-------|
| Source Code | ✗ | — | This skill reviews `SKL-AA1`'s output, not the legacy source directly (though it may spot-check the legacy repo to verify a specific evidence citation is accurate) |
| Database Schema | ✗ | — | Out of scope |
| API Contracts | ✗ (reviewed indirectly) | — | Reviewed only as represented in `application-interface-catalogue.json` |
| Configuration Files | ✗ | — | Out of scope |
| **`SKL-AA1` Output Artifacts** | ✓ (required, primary input) | The 13 files + `diagrams/*.mmd` under the architecture output folder | The entire object of this skill's review |
| Documentation | ✗ | — | Out of scope |
| Infrastructure as Code | ✗ | — | Out of scope |
| Binary / Compiled Code | ✗ | — | Out of scope |

### 3.3 Domain Knowledge References

**Architectural Patterns to Recognise:**
- Not independently detected by this skill — verified against `SKL-AA1`'s own Stage 7 findings only

**Standards & Protocols:**
- The same 10 Quality Parameters `SKL-AA1` is scored against internally (§4.2 of `skill-files/07_AA_Agent1_AppExtractor.md`) are this skill's own review rubric — this skill applies them independently rather than trusting `SKL-AA1`'s self-assessment

**Domain Glossary:**

| Term | Definition |
|------|-----------|
| PASS | The check is fully satisfied with no material gap |
| PARTIAL | The check is partially satisfied — some evidence/structure exists but with a specific, named gap |
| FAIL | The check is not satisfied — a required element is missing, broken, or contradicted |
| Sanity check | A narrow, mechanical verification (file exists, JSON parses, an ID reference resolves) as opposed to a judgment-based quality assessment |

**RE Checklist for This Sub-Domain:**
> _Specific things this skill must look for in this sub-domain._
- [ ] Every one of the 11 checks (§5.2) is run and marked PASS/PARTIAL/FAIL
- [ ] Every PARTIAL/FAIL has a specific, actionable explanation — never a bare verdict with no reason
- [ ] Every ID cross-reference (module ↔ component, dependency edge ↔ node, call-flow step ↔ component) is verified to actually resolve, not merely assumed present
- [ ] Every diagram is checked against its corresponding JSON artifact for consistency
- [ ] The output-path discrepancy between this skill's stated input (`architecture-output/final/`) and `SKL-AA1`'s stated output (`OUTPUT_ROOT/D1-application-architecture/`) is checked and flagged, not silently worked around

---

## BLOCK 4 — INTERFACE

### 4.1 Input Specification

#### Required Inputs

| Field | Type | Format / Example | Description |
|-------|------|-----------------|-------------|
| `aa1_outputs` | 13 files + `diagrams/` | `SKL-AA1`'s complete output set | The object of review |

#### Optional Inputs

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `legacy_repo_path` | string | none | If provided, allows this skill to spot-check a specific evidence citation against the actual source, rather than trusting the citation at face value |

#### Input Validation Rules
- At least the 4 core JSON artifacts (`system-inventory.json`, `module-boundary-map.json`, `component-registry.json`, `dependency-graph.json`) must be present
- Files that exist must be readable (not corrupted)

#### Input Rejection Criteria
- `SKL-AA1`'s output location is empty or does not exist
- Fewer than half of the 14 required artifacts exist

### 4.2 Output Specification

#### Standard Output Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `skill_id` | string | ✓ | `SKL-AA2` |
| `run_id` | string | ✓ | `RUN-YYYYMMDD-HHMMSS` |
| `confidence_score` | float 0–1 | ✓ | Overall confidence in the reviewed output's quality (NOT `SKL-AA1`'s own self-assessed confidence — this skill's independent judgment) |
| `analysis_depth` | string | ✓ | `module` for most checks; `line` when spot-checking a specific evidence citation against source |
| `coverage_pct` | float 0–1 | ✓ | Checks completed / 11 |
| `findings` | object | ✓ | The 11 check results, each PASS/PARTIAL/FAIL with explanation |
| `gaps` | array | ✓ | Every PARTIAL/FAIL item, with its specific reason |
| `recommendations` | array | | Overall Gate readiness recommendation |
| `handoff_context` | object | | The 3 review artifacts' contents, packaged for `SKL-FOUNDATION` / human reviewers |

#### `findings` Object Structure _(skill-specific — expanded from the source's 11-item check list; see §9.2 for why this expansion was necessary)_

> The original source for this skill was an 11-item bullet checklist with no defined PASS/PARTIAL/FAIL criteria per item. The criteria below were derived from `SKL-AA1`'s own 10 Quality Parameters (its Block 4.2 / `07_AA_Agent1_AppExtractor.md` §6), since `SKL-AA1`'s scoring rubric already implies what a reviewer should be checking for. This is documented explicitly, not presented as if these criteria were literally spelled out in the 44-line original.

| # | Check | PASS | PARTIAL | FAIL |
|---|---|---|---|---|
| 1 | Required files exist | All 14 artifacts (13 files + `diagrams/` with 5 `.mmd` files) present and non-empty | Most present; 1-3 missing or marked `Status: incomplete` | More than 3 missing, or core JSON files (system-inventory, module-boundary-map, component-registry, dependency-graph) absent |
| 2 | JSON is valid | Every `.json` file parses without error | N/A — JSON validity is binary | Any `.json` file fails to parse |
| 3 | Modules match component registry | Every `module` value referenced in `component-registry.json` exists in `module-boundary-map.json`, and vice versa (no orphaned components or empty modules) | A small number of components reference a module not formally defined, or a defined module has zero components | Widespread mismatch — components reference modules that don't exist, or most modules have no components |
| 4 | Dependency edges resolve to nodes | Every `edges[].from` and `edges[].to` in `dependency-graph.json` matches an entry in `nodes[]` | A few edges reference IDs not in `nodes[]`, likely a transcription gap | Many edges reference nonexistent nodes, making the graph structurally unreliable |
| 5 | Call-flow steps reference components | Every `steps[].component` in `call-flow-map.json` matches a `name` in `component-registry.json` | Some steps reference components not in the registry (possibly components discovered only during Stage 6's raw-source read and not backfilled into Stage 3's registry) | Most call-flow steps reference components that don't exist anywhere else in the output set |
| 6 | Diagrams match JSON artifacts | Every module/component/dependency shown in the Mermaid diagrams has a corresponding entry in the JSON artifacts, and vice versa (no diagram nodes invented, no major JSON entities omitted from diagrams) | Minor omissions — a few components missing from `component-view.mmd`, or a diagram note says "best-effort, partial detail" | Diagrams show entities/relationships not present in any JSON artifact, or omit major structural elements entirely |
| 7 | Claims have evidence | Nearly every finding across all files cites file path + (line where available) + class/function/component name + confidence | Most findings cite evidence; some (especially lower-confidence ones) are thinner | Many findings assert facts with no file/line/component citation at all |
| 8 | Risks have affected module/component | Every entry in `application-risk-register.json` and `architecture-violation-register.json` names a specific `affected_modules`/`affected_module` and, where applicable, `affected_components` | Most risks are attributed; a few are vague ("system-wide") without further breakdown | Risks listed with no attribution to any specific module/component — unactionable |
| 9 | Unknowns are open questions | Every literal `"unknown"` value anywhere in the output set has a corresponding entry in `open-questions.md` | Most `unknown` values are tracked; a few appear without a matching open question | Many `unknown` values exist with no corresponding open question — unknowns are being silently dropped |
| 10 | No invented cloud/platform/runtime assumptions | No claim anywhere (e.g. "runs on Kubernetes", "uses microservices", "deployed on AWS") lacks direct file evidence per `SKL-AA1`'s own Non-Negotiable Rule 2.1 | A claim is stated with weak/inferred evidence but is clearly flagged low-confidence rather than asserted as fact | A claim about infrastructure, platform, or runtime is stated as fact with zero supporting evidence anywhere in the output set |
| 11 | Forward-engineering files are actionable | `forward-engineering-input-map.md` and `strangler-candidate-report.md` name SPECIFIC modules/APIs/flows (not generic advice like "consider microservices") with concrete reasoning tied to the actual dependency graph and risk register | Some sections are specific, others generic/boilerplate | The files could apply to almost any codebase — no specific module names, no reasoning tied to this system's actual evidence |

```json
{
  "skill_id": "SKL-AA2",
  "run_id": "RUN-20260601-210000",
  "confidence_score": 0.86,
  "analysis_depth": "module",
  "coverage_pct": 1.0,
  "findings": {
    "checks": [
      { "check": "Required files exist", "verdict": "PASS", "detail": "All 14 artifacts present" },
      { "check": "Dependency edges resolve to nodes", "verdict": "PARTIAL", "detail": "2 of 47 edges reference a node ID not found in nodes[] — likely a Stage 5 transcription gap in the Payments module" }
    ]
  },
  "gaps": [
    { "area": "Dependency graph edge integrity", "reason": "2 edges reference undefined node IDs", "severity": "Med" }
  ],
  "recommendations": [
    "Gate readiness: READY WITH MINOR FIXES — resolve the 2 orphaned dependency edges before Foundation Layer synthesis"
  ],
  "handoff_context": {
    "quality-review.md": "...", "executive-summary-for-review.md": "...", "final-sanity-check.md": "..."
  }
}
```

#### Quality Criteria
- Every PARTIAL/FAIL verdict is explained clearly enough that `SKL-AA1` (or a human) could act on it directly
- No check is marked PASS without having actually been run against the real output files
- This skill's own findings cite evidence (which file, which entry) exactly as it demands of `SKL-AA1`

### 4.3 Confidence & Evidence Tagging Schema

> _Every finding in the output must carry a tag declaring how it was obtained._

#### Tag Taxonomy

| Tag | Symbol | Definition | Downstream Action |
|-----|--------|-----------|------------------|
| EXTRACTED | `✅` | The check was run directly against the artifacts and the result is unambiguous (e.g. a JSON parse either succeeds or fails) | Record the PASS/FAIL verdict; proceed |
| PARTIAL | `⚠️` | The check required judgment (e.g. "is this forward-engineering advice specific enough?") and the reviewer's assessment, while reasoned, involves some subjectivity | Record the PARTIAL verdict with explicit reasoning; flag for `SKL-AA1` or human confirmation |
| INFERRED | `〰️` | The check could only be partially verified (e.g. spot-checking a sample of citations rather than every single one, for a very large output set) | Record with a note on what was and wasn't sampled |
| UNKNOWN | `❓` | The check cannot be run at all (e.g. a required file is missing, so its internal consistency can't be assessed) | Record as FAIL for that check with the specific missing-file reason; do not skip silently |

#### Mandatory Tagging Rules

- Every one of the 11 checks carries a PASS/PARTIAL/FAIL verdict AND (per §4.3's tag taxonomy) a confidence tag reflecting how the verdict was reached
- `confidence_score` (overall) is computed per §6.2
- Every PARTIAL/FAIL is added to `gaps` with a specific, named reason — never a bare verdict

#### Display Convention

```
✅ PASS    — [check name]: [what was verified, with counts/specifics]
⚠️ PARTIAL — [check name]: [specific gap found, with counts/specifics]
❓ FAIL    — [check name]: [specific reason the check could not be satisfied]
```

---

## BLOCK 5 — EXECUTION

### 5.1 Constraints & Guardrails

**Hard Constraints _(MUST NOT do these under any circumstances)_:**
- NEVER re-run or regenerate any of `SKL-AA1`'s 13 stages — this is a review skill, not an extraction skill
- NEVER invent new architecture findings not already present in `SKL-AA1`'s output — this skill verifies, it does not add new facts about the system
- NEVER mark a check PASS without actually checking it against the real files
- NEVER give a bare PARTIAL/FAIL verdict without a specific, actionable explanation

**Soft Constraints _(PREFER NOT TO — may override with justification)_:**
- Prefer to check every entry for structural checks (dependency edges, call-flow references) rather than sampling — override to sampling only when the output set is large enough that exhaustive checking is impractical, and disclose the sampling in the verdict

**Scope Boundaries:**

| IN Scope | OUT of Scope |
|----------|-------------|
| Structural verification (files exist, JSON valid, IDs resolve) | Re-running the extraction |
| Evidence/traceability verification | Adding new architecture findings |
| Cross-artifact consistency (diagrams vs. JSON, modules vs. components) | Business/Data/Technology Architecture review |
| Actionability assessment of forward-engineering outputs | Modifying the legacy source code |

**Data Sensitivity Rules:**

| Data Type | Rule |
|-----------|------|
| PII (names, emails, IDs) | Not applicable — this skill reviews architecture metadata, not data content |
| Credentials / Secrets | Not applicable |
| Confidential Business Logic | Not applicable — out of scope for this skill and for `SKL-AA1` |
| Third-party IP / Licensed Code | Not applicable |

**Exclusion List** _(never scan these)_:
```
Not applicable in the same sense as the extraction skills — this skill only
reads SKL-AA1's output folder and, optionally, spot-checks the legacy repo
for a specific citation (in which case SKL-AA1's own exclusion list applies:
.git/, node_modules/, bin/, obj/, target/, dist/, build/, coverage/,
.vscode/, .idea/, *.min.js, *.map, *.lock, generated files, binaries, logs).
```

### 5.2 Process & Methodology

> _Unlike `SKL-DA2`'s multi-phase enrichment process, this skill's source describes a single holistic review pass — not itself staged or chunked. This is a deliberate structural difference from the DA pair, noted here rather than papered over._

**Step 1 — Load and validate the input set**
- Input: `SKL-AA1`'s output folder
- Action: confirm which of the 14 required artifacts exist; parse every `.json` file; note any parse failures or missing files immediately
- Output: an inventory of what exists, what's missing, and what's malformed — feeds Check 1 and Check 2 directly

**Step 2 — Run all 11 checks**
- Input: the validated artifact set
- Action: run each of the 11 checks defined in §4.2's table, in the order listed (structural checks 1-6 first, since they gate whether the judgment-based checks 7-11 are even meaningful to run against a structurally broken output)
- Output: 11 PASS/PARTIAL/FAIL verdicts, each with a specific explanation for anything not PASS

**Step 3 — Write the 3 required review artifacts**
- Input: the 11 check results
- Action: write `quality-review.md` (full detail on all 11 checks), `executive-summary-for-review.md` (condensed, stakeholder-facing summary with the overall Gate readiness recommendation), and `final-sanity-check.md` (the narrow structural checks only — 1, 2, 4, 5, 6 — as a quick mechanical pass distinct from the judgment-based checks)
- Output: the 3 files, written to the same output location as `SKL-AA1`'s artifacts

**Decision Tree:**

| Condition | Branch A | Branch B | Default |
|-----------|----------|----------|---------|
| A required file is missing | Mark the file-existence check FAIL | Still attempt the remaining checks against whatever DOES exist | Never stop the entire review because one file is missing — report what can be assessed |
| A structural check (2, 4, 5, 6) fails badly | Note that judgment-based checks (7-11) run against a structurally compromised base and may be less reliable | Still run them | Flag this caveat explicitly in `quality-review.md` |
| The output-path discrepancy (§7.2) means no files are found at the expected input path | Check the alternate path (`SKL-AA1`'s stated `OUTPUT_ROOT/D1-application-architecture/`) before concluding nothing exists | — | Document which path was actually used in `extraction-audit`-style notes within `quality-review.md` |

**Iteration / Retry Rules:**

| Trigger | Max Retries | Strategy |
|---------|------------|---------|
| A judgment-based check's verdict is genuinely borderline (e.g. is this forward-engineering advice "specific enough"?) | 0 | Record PARTIAL with the specific reasoning for why it's borderline — do not force a binary PASS/FAIL when the honest answer is "partially" |

### 5.3 Analysis Depth & Granularity

| Level | Description | When to Activate | Typical Output Artifact |
|-------|-------------|-----------------|------------------------|
| System | Full system / portfolio overview | Executive summary framing | `executive-summary-for-review.md` |
| Module / Service | Component-level analysis | Checks 3, 8 (module/component attribution) | `quality-review.md` |
| Class / Entity | Object-level analysis | Not typically needed — this skill reviews aggregated artifacts, not individual classes | — |
| Function / Method | Procedural analysis | Only when spot-checking a specific call-flow evidence citation against the legacy repo | `quality-review.md` evidence notes |
| Line / Statement | Detailed code inspection | Only when spot-checking a specific file:line citation | `quality-review.md` evidence notes |

**Default Depth Level for This Skill:** `Module / Service` for most checks, descending to `Line / Statement` only when independently spot-checking a specific evidence citation (optional, requires `legacy_repo_path`).

**Coverage Threshold:**
> All 11 checks run to completion with a recorded verdict; all 3 review artifacts written.

**Action if Coverage Threshold Not Met:**
> Write whatever review artifacts can be completed; explicitly list which checks could not be run and why (e.g. "Check 6 (diagrams match JSON) could not be run — `diagrams/` folder is empty").

**Reading Depth Rules** _(what to read deep vs skim vs skip)_:

| File / Artifact Type | Reading Rule | Reason |
|---------------------|--------------|--------|
| All 13 `SKL-AA1` files + `diagrams/*.mmd` | Read in full | Every check needs the complete artifact, not a sample, unless the set is unusually large |
| Legacy source (optional spot-check) | Read only the specific file/line cited | This skill verifies citations, it doesn't re-extract |

### 5.4 Chunking & Context Management

> _This skill's review is a single holistic pass, not chunked by domain, layer, or stage — the smallest meaningful unit of work here is "one check" (§5.2 Step 2), and all 11 fit comfortably in one pass for a typical output set._

#### Chunking Strategy

| Dimension | Rule | Default |
|-----------|------|---------|
| Chunk unit | Not chunked — one holistic review pass over the complete `SKL-AA1` output set | Single pass |
| Max chunk size | Not applicable; if the output set is unusually large, sample judgment-based checks (7-11) and disclose the sampling | Full read by default |
| Chunk ordering | Structural checks (1, 2, 4, 5, 6) before judgment-based checks (3, 7, 8, 9, 10, 11) | Structural-first |

#### Context Window Caps

| Item Type | Cap | Selection Strategy When Over Cap |
|-----------|-----|----------------------------------|
| Findings sampled for evidence-citation verification (Check 7) | No fixed cap for typical output sizes; sample if the finding count is very large | Prioritize higher-impact findings (Critical/High severity risks and violations) for citation verification first |

#### Cross-Chunk Continuity Rules

- Not applicable in the domain/chunk sense used by the other 6 skills — this skill's "carried forward" state is simply the accumulating set of 11 check verdicts within a single pass

#### Multi-Run / Incremental Analysis

| Scenario | Behaviour |
|----------|-----------|
| Re-running after `SKL-AA1` re-extracts due to a code change | Re-run all 11 checks against the new output set — do not assume prior verdicts still apply |
| Running against a partial `SKL-AA1` output (some stages incomplete) | Run every check that CAN be run against what exists; mark checks that depend on missing artifacts as FAIL with the specific missing-file reason |

---

## BLOCK 6 — INTELLIGENCE

### 6.1 Decision Rules & Heuristics

| ID | Trigger Condition | Agent Action | Rationale |
|----|-------------------|--------------|-----------|
| H-001 | A required file is missing | Mark Check 1 FAIL/PARTIAL depending on how many; still attempt remaining checks against what exists | Partial review is more useful than no review |
| H-002 | A structural check (edges, call-flow references, diagram consistency) fails | Flag downstream judgment-based checks as potentially less reliable, but still run them | A structurally broken base doesn't make the judgment-based checks meaningless, just lower-confidence |
| H-003 | A finding lacks any file/line/component citation | Fail Check 7 for that finding specifically, not the whole output set wholesale | Precision in the verdict makes it actionable — "some findings lack evidence" beats "evidence is bad" |
| H-004 | Forward-engineering advice reads as generic/boilerplate | Mark Check 11 PARTIAL/FAIL with a specific example of the generic language found | Concrete counter-examples make the feedback actionable for `SKL-AA1`'s next run |
| H-005 | The stated input path has no files but `SKL-AA1`'s stated output path does | Check the alternate path before concluding `SKL-AA1` hasn't run; document which path was used | Prevents a false "SKL-AA1 has not run" verdict caused only by the path-naming discrepancy (§7.2) |

**Pattern Recognition Catalog:**

| Pattern Name | Signature / Indicator | RE Significance | Action |
|--------------|----------------------|-----------------|--------|
| Rubber-stamp risk | All 11 checks marked PASS with generic, non-specific explanations | Suggests the review wasn't actually performed against the real artifacts | Never accept a PASS verdict without a specific citation (which file, which entry, what was checked) |
| Cascading structural failure | Checks 1, 2, and 4 all fail together | Usually indicates `SKL-AA1`'s run was interrupted or corrupted, not 3 independent problems | Note the likely common cause in `quality-review.md` rather than treating them as 3 unrelated findings |
| Boilerplate forward-engineering language | Advice that could apply to "any" codebase ("consider microservices", "modernize incrementally") with no named modules/APIs | Suggests Stage 11 was completed formulaically rather than from the actual dependency graph and risk register | Mark Check 11 PARTIAL/FAIL; quote the generic language as evidence |

**Ambiguity Resolution Strategy:**

| Ambiguity Type | Resolution Strategy |
|----------------|-------------------|
| A judgment call (e.g. "is this evidence citation specific enough?") has no bright-line rule | Apply the PASS/PARTIAL/FAIL criteria in §4.2's table as written; when still genuinely borderline, choose PARTIAL and explain the specific reasoning — never silently round up to PASS |
| The output-path discrepancy means the review skill can't find `SKL-AA1`'s files at the documented input location | Check both the documented input path and `SKL-AA1`'s documented output path before failing Check 1 outright |

**Prioritisation Logic:**
> When context window or time is constrained, analyze in this order:
1. Structural checks first (1, 2, 4, 5, 6) — these gate whether judgment-based checks are even meaningful
2. Evidence/traceability checks (7, 9, 10) — core to whether the output can be trusted at all
3. Attribution and actionability checks (3, 8, 11) — quality-of-content assessment

### 6.2 Confidence & Uncertainty Handling

| Band | Score | Label | Agent Behaviour |
|------|-------|-------|----------------|
| High | 0.85 – 1.00 | Confident | Verdict is PASS or a clear-cut FAIL (e.g. JSON parse error) with no judgment call involved |
| Medium | 0.60 – 0.84 | Review advised | Verdict is PARTIAL, backed by a specific, reasoned explanation |
| Low | 0.40 – 0.59 | Uncertain | A judgment-based check (e.g. actionability) is genuinely borderline even after applying the §4.2 criteria |
| Very Low | 0.00 – 0.39 | Cannot determine | The check could not be run at all (required artifact missing or unreadable) |

**Confidence Score Calculation:**
- Method: `Hybrid` (structural checks are rule-based/binary; judgment-based checks are LLM self-assessed against the §4.2 criteria)
- Formula: `(count(EXTRACTED)×1.0 + count(PARTIAL)×0.7 + count(INFERRED)×0.4 + count(UNKNOWN)×0) / total findings` — applied across all 11 checks' verdicts

**Disambiguation Strategies** _(attempt in order before escalating)_:
1. Re-apply the specific PASS/PARTIAL/FAIL criteria in §4.2's table literally — most ambiguity resolves once the written criteria are checked against precisely
2. If a specific evidence citation is in question, spot-check it against the legacy repo directly (if `legacy_repo_path` is provided)
3. If still genuinely borderline, record PARTIAL with the specific reasoning — never force a PASS or FAIL that the evidence doesn't clearly support

### 6.3 Evidence Hierarchy

> _When multiple sources provide conflicting information about the same fact, this ranking determines which source wins. Identical to `SKL-AA1`'s Block 6.3 — both agents must agree on what outranks what, since this skill is verifying claims `SKL-AA1` made using this same hierarchy._

#### Source Reliability Ranking

| Rank | Source Type | Reliability | Notes |
|------|-------------|-------------|-------|
| 1 — Highest | Constructor injection / method-body call evidence in source | Definitive | If spot-checking, this is what to verify a citation against |
| 2 | Class/interface declarations, DI registration code | Very High | — |
| 3 | Config files (routing, DI wiring, appsettings) | High | — |
| 4 | Log/trace evidence of an actual call path | Medium-High | — |
| 5 | Test files exercising a call path | Medium | — |
| 6 | Naming conventions alone | Low | A citation resting only on this should already be tagged `INFERRED`/`PARTIAL` by `SKL-AA1` — if it's presented as `EXTRACTED`, that's a Check 7/10 finding for this skill |
| 7 — Lowest | Documentation/README | Very Low | — |

#### Conflict Resolution Rule

When this skill's spot-check of a citation disagrees with what `SKL-AA1` claimed:
1. The higher-ranked source (from direct inspection) wins
2. Document both: `"SKL-AA1 cited OrderService.cs:42 as evidence of X, but that line actually shows Y — flagged in Check 7 as a citation accuracy issue"`
3. This becomes a specific, named finding under Check 7 (claims have evidence) or Check 10 (no invented assumptions), not a silent correction

#### Common RE Conflict Patterns

| Conflict | Typical Cause | Resolution |
|----------|--------------|------------|
| A cited file:line doesn't actually show what the finding claims | Line numbers can drift if the source was analyzed at a different commit than the one being spot-checked, or the citation was mis-transcribed | Flag as a Check 7 finding; note whether it looks like drift (different but related content) or a genuine mis-citation |
| `SKL-AA1`'s stated confidence for a finding seems inconsistent with the evidence rank actually cited (e.g. `EXTRACTED` tag but only naming-convention evidence given) | `SKL-AA1`'s self-scoring may not have applied its own evidence hierarchy consistently | Flag as a Check 10 finding — recommend the confidence tag be reconciled with the actual evidence rank |

---

## BLOCK 7 — INTEGRATION

### 7.1 Tools & Integrations

| Tool / API / MCP Server | Purpose | Access Method | Required |
|-------------------------|---------|---------------|---------|
| File access to `SKL-AA1`'s output location | The object of review | Read-only (plus write for the 3 review artifacts) | ✓ |
| Legacy repo file access (optional) | Spot-checking specific evidence citations | Read-only | — (optional) |

**File Operation Permissions:**

| Operation | Permitted Paths | Restrictions |
|-----------|----------------|-------------|
| Read | `SKL-AA1`'s output location (both the documented input path and, if needed, `SKL-AA1`'s documented output path — see §7.2); optionally the legacy repo for spot-checks | — |
| Write | The same architecture output folder, for the 3 review artifacts only | Never modifies any of `SKL-AA1`'s original 14 artifacts |
| Execute | `None` | This skill does not run, build, or test anything |

### 7.2 Dependencies

**Upstream Skills** _(must complete before this skill runs)_:

| Skill ID | Skill Name | Output Consumed | Dependency Type |
|----------|------------|-----------------|--------------------|
| `SKL-AA1` | AA Agent 1 — Application Extractor | All 14 output artifacts | `Hard` |

> **Known naming discrepancy (documented, not silently resolved):** this skill's own source states its input location as `architecture-output/final/`, while `SKL-AA1`'s own source states its output location as `OUTPUT_ROOT/D1-application-architecture/`. These two paths do not match in the original prompts, and neither original file acknowledges the other's path. This conversion does not silently pick one as "correct" — per §6.1 H-005, this skill checks BOTH locations before concluding `SKL-AA1` has not run, and documents in `quality-review.md` which path actually contained the files. **Recommendation:** reconcile both prompts to a single agreed output path before this pair is used in an automated (non-interactive) pipeline, since a human pasting these prompts manually would naturally adjust the path, but an automated runner would not.

**Downstream Skills** _(receive this skill's output)_:

| Skill ID | Skill Name | What This Skill Provides | Trigger Condition |
|----------|------------|--------------------------|--------------------|
| `SKL-FOUNDATION` _(not yet templated)_ | Foundation Layer | `SKL-AA1`'s 14 artifacts, PASS/PARTIAL/FAIL-verified, plus the 3 review artifacts | After this skill's review completes, regardless of overall verdict (a NOT READY verdict is still a valid, actionable handoff) |

**External Systems:**

| System | Purpose | Data Flow | Connection Type |
|--------|---------|-----------|----------------|
| None | This skill never connects to a live database, API, or external service | — | — |

### 7.3 Context Propagation & Handoff Protocol

**Context to Carry Forward** _(always pass to all downstream skills)_:
- All 11 check verdicts with their specific explanations
- The 3 review artifacts (`quality-review.md`, `executive-summary-for-review.md`, `final-sanity-check.md`)
- The overall Gate readiness recommendation

**State to Persist** _(store across sessions / incremental runs)_:
- The check verdicts from the most recent run, so a subsequent re-review can note what changed since the prior pass

**Handoff Artifact Format:**

```json
{
  "source_skill": "SKL-AA2",
  "run_id": "RUN-20260601-210000",
  "target_skill": "SKL-FOUNDATION",
  "confidence_score": 0.86,
  "context": {
    "overall_verdict": "READY WITH MINOR FIXES",
    "checks_passed": 9,
    "checks_partial": 2,
    "checks_failed": 0
  },
  "artifacts": {
    "quality-review.md": "...",
    "executive-summary-for-review.md": "...",
    "final-sanity-check.md": "..."
  },
  "validation_queue": [
    { "item": "2 orphaned dependency-graph edges in the Payments module", "tag": "PARTIAL", "reason": "edges reference node IDs not present in nodes[]" }
  ]
}
```

**Recommended Starting Point for Downstream Agent:**
> Not a fixed value — `final-sanity-check.md`'s structural-check results (1, 2, 4, 5, 6) should be resolved first if any are not PASS, since the judgment-based findings (3, 7, 8, 9, 10, 11) are more trustworthy once the structural base is confirmed sound.

---

## BLOCK 8 — RELIABILITY

### 8.1 Error Handling & Fallbacks

| Failure Mode | Likelihood | Detection | Fallback Strategy | Escalation Rule |
|--------------|-----------|-----------|------------------|----------------|
| `SKL-AA1`'s output location is empty at the documented input path | M | Checked at activation | Check `SKL-AA1`'s own documented output path before concluding nothing exists (§7.2 discrepancy) | If truly nothing exists at either path, stop and ask the user to run `SKL-AA1` first |
| A `.json` file fails to parse | L | Attempted during Step 1 | Mark Check 2 FAIL for that file specifically; still attempt to review other files | Continue — do not abandon the whole review for one bad file |
| Fewer than half of the 14 artifacts exist | L | Checked at activation | N/A | Recommend re-running `SKL-AA1` rather than reviewing a mostly-empty output set |
| A judgment-based check is genuinely borderline | M | Observed during Step 2 | Record PARTIAL with specific reasoning | Never force a PASS or FAIL the evidence doesn't clearly support |

**Human Review Triggers** _(mandatory escalation conditions)_:
- [ ] Any structural check (1, 2, 4, 5, 6) is FAIL
- [ ] More than 3 of the 11 checks are PARTIAL or FAIL
- [ ] Overall `confidence_score` below 0.60
- [ ] Check 10 (no invented cloud/platform/runtime assumptions) fails — this is treated as a hard gate given how directly it maps to `SKL-AA1`'s own Non-Negotiable Rule 2.1

**Escalation Path:**
1. Every PARTIAL/FAIL is written into `quality-review.md` with its specific explanation
2. `executive-summary-for-review.md`'s overall recommendation (READY / READY WITH MINOR FIXES / NOT READY) is the primary escalation signal to the human reviewer or `SKL-FOUNDATION`
3. If NOT READY, the specific blocking checks are named so the next action (re-run `SKL-AA1`, or fix specific artifacts) is unambiguous

**Partial Output Policy:**
> All 3 review artifacts should always be written, even if some checks could not be run — mark which checks were skipped and why in `quality-review.md`. A NOT READY verdict, clearly reasoned with specific failing checks named, is a valid and useful complete output, not a failure of this skill.

### 8.2 Validation & QA Checklist

**Agent Self-Check** _(run before emitting any output)_:
- [ ] All 11 checks were actually run against the real artifacts, not assumed
- [ ] Every PARTIAL/FAIL has a specific, actionable explanation citing which file/entry
- [ ] `confidence_score` calculated per the method in §6.2
- [ ] `gaps` populated for every check not marked PASS
- [ ] `handoff_context` package includes the overall Gate readiness recommendation
- [ ] No new architecture findings were invented — this skill verified `SKL-AA1`'s claims, it did not add new ones
- [ ] The output-path discrepancy (§7.2) was checked, not silently assumed away
- [ ] All 3 review artifacts (`quality-review.md`, `executive-summary-for-review.md`, `final-sanity-check.md`) were written

**Human Review Checklist:**
- [ ] Verdicts align with a spot-check of the underlying artifacts
- [ ] PARTIAL/FAIL explanations are specific enough to act on without re-deriving them
- [ ] No PASS verdict looks like a rubber-stamp (§6.1 H-001 pattern)
- [ ] The overall Gate readiness recommendation is clearly reasoned

**Automated Test Cases:**

| Test ID | Scenario | Input | Expected Output | Pass Criteria |
|---------|----------|-------|-----------------|---------------|
| T-001 | Clean `SKL-AA1` output, all checks pass | All 14 artifacts present, internally consistent, well-evidenced | All 11 checks PASS; overall verdict READY | No PARTIAL/FAIL without genuine cause |
| T-002 | Orphaned dependency edges | `dependency-graph.json` has 2 edges referencing undefined node IDs | Check 4 marked PARTIAL/FAIL with the specific edge IDs named | Never silently ignored |
| T-003 | Generic forward-engineering advice | `forward-engineering-input-map.md` contains only generic statements with no named modules | Check 11 marked PARTIAL/FAIL with the generic language quoted as evidence | Specific counter-example cited, not a vague "not actionable" verdict |
| T-004 | Output not found at documented input path but present at `SKL-AA1`'s documented output path | `architecture-output/final/` is empty; `OUTPUT_ROOT/D1-application-architecture/` has all 14 files | This skill checks the alternate path and proceeds with the review, noting the path discrepancy | Does NOT falsely report "SKL-AA1 has not run" |

---

## BLOCK 9 — REFERENCE

### 9.1 Examples

#### Canonical Example (Standard Case)

**Scenario:**
> A well-formed `SKL-AA1` output set with one minor structural gap — the standard "PARTIAL, not FAIL" case.

**Input:**
```json
{ "aa1_outputs": "14 artifacts present, dependency-graph.json has 2 orphaned edges out of 47" }
```

**Expected Output:**
```json
{
  "confidence_score": 0.88,
  "findings": {
    "checks": [
      { "check": "Dependency edges resolve to nodes", "verdict": "PARTIAL", "detail": "2 of 47 edges reference undefined node IDs in the Payments module" }
    ]
  },
  "gaps": [
    { "area": "dependency-graph.json edge integrity", "reason": "2 orphaned edges", "severity": "Low" }
  ]
}
```

**Notes:**
> Canonical because the finding is specific (exact count, exact module) rather than a vague "some issues found" — this is what makes a PARTIAL verdict actionable.

#### Edge Cases

| ID | Description | Input Pattern | Expected Behaviour | Risk if Mishandled |
|----|-------------|--------------|-------------------|-------------------|
| E-001 | Output-path discrepancy | Files not found at `architecture-output/final/` | Check `OUTPUT_ROOT/D1-application-architecture/` before failing Check 1 | False "SKL-AA1 has not run" verdict wastes a re-run |
| E-002 | Structurally broken input (JSON parse failure) | `component-registry.json` is truncated/corrupted | Check 2 FAIL for that file; still attempt other checks against readable files | Abandoning the entire review loses value from the files that ARE fine |
| E-003 | Borderline actionability judgment | Forward-engineering advice is specific for 2 of 5 sections, generic for the other 3 | Check 11 marked PARTIAL, naming which sections are specific and which are generic | Forcing a binary PASS/FAIL loses the nuance a human reviewer needs |

#### Anti-Patterns _(What NOT to Do)_

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|---------------|-----------------|
| Marking all 11 checks PASS without citing specific evidence for each | Rubber-stamp review defeats the purpose of an independent quality gate | Every PASS should be as specific as every PARTIAL/FAIL — "all 47 edges verified against nodes[]" not just "PASS" |
| Adding a new architecture finding this skill noticed but `SKL-AA1` didn't report | Out of scope for a verification skill — creates an inconsistency between what `SKL-AA1` claims to have found and what actually appears in its own artifacts | Note it as feedback for `SKL-AA1`'s next run, not as a new finding injected into the review artifacts |
| Concluding "SKL-AA1 has not run" the moment the documented input path is empty | Ignores the known path-naming discrepancy (§7.2) | Always check the alternate path before concluding nothing exists |
| Giving a FAIL verdict with no specific explanation | Unactionable — the recipient can't tell what to fix | Every non-PASS verdict names the specific file/entry/example |

### 9.2 Changelog & Version Notes

| Version | Date | Author | Change Description |
|---------|------|--------|--------------------|
| 1.0.0 | 2026-06-01 | AA Reverse Engineering System | Original `08_AA_Agent2_QualityReview.md` prompt — a ~44-line stub: a Role line, an Input path, 3 Output file names, an 11-item bullet checklist with no defined pass/fail criteria per item, and a PASS/PARTIAL/FAIL marking instruction |
| 1.0.0 (template conversion) | 2026-07-06 | Skill file conversion pass | Reformatted into the `sdlc_skill_file_template_v2.md` 9-block structure. Because the source was too thin to convert directly, the PASS/PARTIAL/FAIL criteria in §4.2's table, the process steps in §5.2, the decision rules in §6.1, and the self-check items in §8.2 were **derived** from `SKL-AA1`'s own 10 Quality Parameters (`skill-files/07_AA_Agent1_AppExtractor.md` §4.2) — since a reviewer's job is naturally to apply the producer's own quality rubric. This is an explicit, disclosed expansion of thin source material using the paired agent's own stated standards as the basis, not fabrication from nothing; it should be reviewed by a human owner before being treated as an authoritative spec. The output-path discrepancy between this file's stated input (`architecture-output/final/`) and `SKL-AA1`'s stated output (`OUTPUT_ROOT/D1-application-architecture/`) was documented (§7.2) rather than silently resolved. |

---

_Template v2.0 · 9 Blocks · 24 Sections · SDLC Agentic AI Platform · RE-optimised_
_Converted from: `prompts-ready-to-use/08_AA_Agent2_QualityReview.md` · Pair with: `skill-files/07_AA_Agent1_AppExtractor.md` (`SKL-AA1`)_
