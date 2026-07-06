# SKILL FILE: DA Agent 1 — Data Architecture Extractor

> Skill ID: `SKL-DA1` | Version: `2.0.0` | Status: `ACTIVE`
> SDLC Phase: `Analysis`
> Domain: `Reverse Engineering` | Sub-Domain: `DB Schema`
> Owner: `[Team / Member]` | Last Updated: `2026-06-01`

---

## BLOCK 1 — IDENTITY

### 1.1 Skill Metadata

| Field | Value |
|-------|-------|
| Skill ID | `SKL-DA1` |
| Skill Name | DA Agent 1 — Data Architecture Extractor |
| Version | `2.0.0` |
| SDLC Phase | `Analysis` |
| Domain | `Reverse Engineering` |
| Sub-Domain | `DB Schema` |
| Owner | `[Team / Member]` |
| Tags | `data-architecture`, `schema-extraction`, `pii-inventory`, `agent-1-of-2`, `live-db-verification` |
| Status | `Active` |
| Paired With | `SKL-DA2` (DA Agent 2 — Data Architecture Reviewer) — hard dependency, `SKL-DA2` cannot run without this skill's 13 output files in `da-outputs/` |

### 1.2 Goal & Success Criteria

**Primary Goal:**
> Fully reverse-engineer the data architecture of a codebase — schema, relationships, data flow, PII, data quality, hidden business rules encoded in data, and canonical/shadow entity duplication — surfacing facts only, verified against the live database wherever one is reachable.

**Secondary Goals:**
- Never silently fall back to code-only analysis when a database is unreachable — always document the exact connection error and command attempted
- Detect and flag canonical vs. shadow (duplicate) representations of the same business concept (e.g. "customer" as `AspNetUsers`, `Buyer`, and a loose `BuyerId` string)
- Capture business-meaning and governance evidence (soft-delete flags, audit columns, `[Authorize]` roles) alongside pure schema facts, since these feed the data dictionary, conceptual model, retention policy, and access control matrix

**Success Definition:**
> A run is successful when all 13 output files exist in `da-outputs/`, the `db_connection` field is set to `CONNECTED` or `CODE-ONLY` with the exact error and command documented, every table/column in `schema-catalogue.json` has a matching `data-dictionary.md` entry, every `[Authorize]`-derived role appears in `access-control-matrix.md`, and every value below the 0.70 confidence floor is marked `UNKNOWN` with an inline reason rather than guessed.

**What This Skill Does NOT Do:**
> Everything requiring business-intent interpretation or independent re-verification belongs to `SKL-DA2` (or, beyond code, to human stakeholders).
- Does not interpret business intent or make design decisions — surfaces facts only
- Does not produce a Business Requirements Document (BRD) — that is a downstream artifact, not this skill's job
- Does not review UI, frontend, or non-data code
- Does not write new code or fix bugs
- Does not skip the database connection attempt and silently fall back to code-only — if the DB is unreachable, it documents exactly why

---

## BLOCK 2 — ACTIVATION

### 2.1 Trigger Conditions

**Explicit Triggers** _(user states these directly)_:
- "reverse engineer this project"
- "analyse my data architecture"
- "document the schema"
- "map the database"
- "what databases does this use?"
- "map the data flow"

**Implicit Signals** _(infer from conversation context or orchestrator routing)_:
- A codebase folder is dropped and the user's intent concerns data, tables, entities, or migrations
- `SKL-DA2` is present in the session and the user wants a full DA pipeline run (this skill runs first)
- The orchestrator has classified the request as belonging to the Data Architecture reverse-engineering pipeline

**Activation Keywords / Patterns:**
```
"reverse engineer this" | "analyse my data architecture" | "document the schema" |
"map the database" | "what databases does this use" | "map the data flow"
```

### 2.2 Pre-conditions & Guards

**Must Be True Before Activation:**
- [ ] A project codebase is provided (folder, zip, tree, or pasted code)
- [ ] The environment where this skill runs has shell/CLI access to attempt a live database connection (Phase 2 is mandatory, not optional)

**Disqualifiers** _(do NOT activate if any of these are true)_:
- [ ] Paired agent (`SKL-DA2`) is expecting to review an already-completed run, and this skill is being asked to re-run the full extraction unnecessarily — confirm with the user first (re-running is expensive; `SKL-DA2` only re-runs targeted verification, not full extraction)
- [ ] No project input of any kind is present
- [ ] The request is purely about non-data code (UI, frontend) — out of scope for this skill

---

## BLOCK 3 — CONTEXT

> _Block 3 is the most critical block for Reverse Engineering skills. Precision here directly determines output accuracy._

### 3.1 Environment Context

| Dimension | Details |
|-----------|---------|
| Target Language(s) | Language/framework-agnostic — detected from Layer 1 JSON or raw source in Phase 0 |
| Framework(s) | Any ORM/data-access framework — detected, not assumed |
| Platform / OS | Must have a database CLI tool locatable on the local machine for Phase 2 (e.g. `psql`, `mysql`, `sqlcmd`, `mongosh`) |
| Database Type | Any relational or document database whose CLI tool can be located and invoked |
| Architecture Pattern | Detected from `source_code.json`/`database.json`, not assumed |
| Available Tools | Read access to project source; shell access to run a DB CLI connection test; write access to create the `da-outputs/` folder |
| Repository Access | `Read-Write` (write is scoped to the `da-outputs/` output folder only — never to source code) |
| Authentication Level | Whatever credentials are already available in the project's own config/connection strings — this skill never requests new credentials from the user |
| **Layer 1 JSON (optional accelerator)** | If present, `source_code.json`, `database.json`, `config.json`, and `logs.json` are used INSTEAD of raw file scanning wherever they cover the needed evidence (see §3.2). This is produced by an external, non-skill automated pre-step — if absent, this skill falls back to raw source scanning per its own reading rules. |

### 3.2 Artifact Taxonomy

> _Which artifact types can this skill ingest and analyze?_

| Artifact Type | Supported | Accepted Formats | Notes |
|---------------|-----------|-----------------|-------|
| Source Code | ✓ | Any — via `source_code.json` (Layer 1) first, raw files only for gaps | Entity/model classes, service signatures, repository/query classes |
| Database Schema | ✓ | Live DB connection (preferred) + migration files (`.sql`, ORM migrations) | Migration chronological order is NOT in Layer 1 JSON — always read migrations directly |
| API Contracts | ✗ | — | Out of scope |
| Configuration Files | ✓ | `.yaml`, `.json`, `.env`, framework config | Via `config.json` (Layer 1) first; raw config opened only if a connection string is missing/unknown |
| UI Wireframes / Designs | ✗ | — | Out of scope |
| Application Logs / Traces | ✓ (limited) | `logs.json` (Layer 1) | Used for audit trails and event patterns only |
| Test Cases | ✗ | — | Out of scope for this skill — `SKL-DA2` reads tests |
| Documentation | ✗ | — | Out of scope for this skill — `SKL-DA2` reads README/docs |
| Infrastructure as Code | ✗ | — | Out of scope — belongs to `SKL-TA1` |
| Binary / Compiled Code | ✗ | — | Cannot be scanned |
| **Live Database** | ✓ (mandatory attempt) | Any DB reachable via a local CLI tool | Phase 2 is mandatory — no skipping, no silent fallback |

### 3.3 Domain Knowledge References

**Architectural Patterns to Recognise:**
- Repository / Specification pattern (entity + repository class pairing, raw SQL in repository classes)
- Canonical vs. shadow entity duplication (the same business concept represented more than once)
- Soft-delete and audit-column conventions (`IsDeleted`, `CreatedAt`, etc.)

**Design Patterns to Detect** _(e.g. Repository, CQRS, Singleton, Saga)_:
- Repository pattern
- Caching layer wrapping a data-access class (`*/Cache*`, `*/Services*`)

**Standards & Protocols:**
- FK `ON DELETE` semantics (`NO ACTION`, `CASCADE`, etc.) and their operational implications
- `[Authorize(Roles=...)]`-style role/policy annotations feeding the access control matrix

**Domain Glossary:**

| Term | Definition |
|------|-----------|
| Canonical entity | The representation of a business concept treated as the source of truth when duplicates exist |
| Shadow entity | A duplicate/loose representation of a business concept that is not the source of truth (e.g. a bare `BuyerId` string alongside a full `Buyer` entity) |
| CODE-ONLY | The `db_connection` state when a live database could not be reached; every finding derived without live verification is capped below the highest confidence tier |
| Evidence Strength Hierarchy | The ranked list of sources (live DB highest, naming conventions lowest) used to resolve conflicts (see §6.3) |

**RE Checklist for This Sub-Domain:**
> _Specific things this skill must look for in this sub-domain._
- [ ] Database connection attempted and result documented (CONNECTED or exact CODE-ONLY reason)
- [ ] Row counts, schema verification, FK rules, indexes, sequences, triggers, and DQ checks run if connected
- [ ] Caching layer identified and documented in both `data-source-inventory.json` and `storage-pattern-analysis.md`
- [ ] At least one canonical/shadow entity check completed, even if the result is "no duplicates found"
- [ ] Every soft-delete flag and audit column identified and tied to a retention-policy implication
- [ ] Every `[Authorize]`-derived role captured in the access control matrix

---

## BLOCK 4 — INTERFACE

### 4.1 Input Specification

#### Required Inputs

| Field | Type | Format / Example | Description |
|-------|------|-----------------|-------------|
| `project_source` | file tree / zip / pasted code | Codebase root | The codebase to extract data architecture from |

#### Optional Inputs

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `layer1_json` | object | none | `source_code.json`, `database.json`, `config.json`, `logs.json` — if present, used instead of raw scanning wherever they cover the needed evidence (§3.1) |
| `db_credentials_hint` | string | none | Already-present connection string location, if the user knows where it lives — used only to speed up Phase 0, never to introduce new credentials |

#### Input Validation Rules
- A database CLI tool must be locatable on the machine for Phase 2 to run meaningfully; if none can be found, document this as the CODE-ONLY reason
- Entity/model files (or, as fallback, migration files) must exist somewhere in the project

#### Input Rejection Criteria
- Entity/model files not found after a full folder scan → stop and ask the user
- More than 40% of files are binary with no source counterparts → stop and ask the user
- Connection string is encrypted or redacted with no way to derive it → stop and ask the user

### 4.2 Output Specification

#### Standard Output Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `skill_id` | string | ✓ | `SKL-DA1` |
| `run_id` | string | ✓ | `RUN-YYYYMMDD-HHMMSS` |
| `confidence_score` | float 0–1 | ✓ | Computed per §6.2 formula, informed by the domain-specific confidence ladder |
| `analysis_depth` | string | ✓ | `module` for schema/entity extraction, `line` for raw SQL and migration parsing |
| `coverage_pct` | float 0–1 | ✓ | Files written / 13 total required output files |
| `findings` | object | ✓ | Maps each of the 13 output filenames to a short description of its top-level shape (not full contents — full contents are written to disk in `da-outputs/`) |
| `gaps` | array | ✓ | All `UNKNOWN`/low-confidence items, with inline reasons |
| `recommendations` | array | | Suggested domain/entity for `SKL-DA2` to verify first |
| `handoff_context` | object | | `db_connection` state, key entities, most important gaps |

#### `findings` Object Structure _(skill-specific — maps to the 13 real files written to `da-outputs/`)_

```json
{
  "skill_id": "SKL-DA1",
  "run_id": "RUN-20260601-160000",
  "confidence_score": 0.86,
  "analysis_depth": "module",
  "coverage_pct": 1.0,
  "findings": {
    "schema-catalogue.json": "tables[], columns[], relationships[], indexes[], db_connection status",
    "erd.md": "entity-relationship diagram in markdown, plus a WARNING section listing soft (undeclared FK) references",
    "data-source-inventory.json": "every data store found (DB, cache, queue) with connection evidence",
    "data-flow-map.md": "narrative + diagram of how data moves between layers/domains",
    "pii-inventory.json": "every PII-classified column with source evidence",
    "data-quality-report.md": "DQ findings including FK ON DELETE = NO ACTION risks",
    "migration-complexity.json": "migration count, chronology, row counts per migrated table",
    "hidden-business-rules.json": "business rules implied by data constraints (e.g. cache TTLs, DB-level checks)",
    "storage-pattern-analysis.md": "caching layer detail, including TTL as a business rule",
    "redundancy-analysis.json": "canonical vs shadow entity findings",
    "data-dictionary.md": "every table/column with a plain-English definition",
    "conceptual-data-model.md": "business-language-only model, no table/type/FK syntax",
    "access-control-matrix.md": "every [Authorize]-derived role mapped to the data it can access"
  },
  "gaps": [
    { "area": "PostgreSQL connection", "reason": "connection refused at localhost:5432; command attempted: psql -h localhost -p 5432 -U postgres -d eShopCatalog -c \\dt", "severity": "High" }
  ],
  "recommendations": [
    "SKL-DA2 should prioritize verifying the Order/Payment relationship first — highest entity density and a live-DB-unconfirmed FK rule"
  ],
  "handoff_context": {
    "db_connection": "CODE-ONLY — connection refused at localhost:5432",
    "key_entities": ["Order", "Payment", "Customer"],
    "top_gaps": ["Live DB unreachable — all confidence capped below 1.0 tier"]
  }
}
```

#### Quality Criteria
- Every UNKNOWN value has an inline reason
- Every table/column in `schema-catalogue.json` has a matching entry in `data-dictionary.md`
- `conceptual-data-model.md` uses business language only — no table names, types, or FK syntax
- Code-vs-DB conflicts are resolved using the Evidence Strength Hierarchy (§6.3), never guessed

### 4.3 Confidence & Evidence Tagging Schema

> _Every finding in the output must carry a tag declaring how it was obtained._

#### Tag Taxonomy

| Tag | Symbol | Definition | Downstream Action |
|-----|--------|-----------|------------------|
| EXTRACTED | `✅` | Confirmed by live DB query, migration file, or entity/ORM code | Proceed; no review needed unless conflicted |
| PARTIAL | `⚠️` | Confirmed by repository/query code only — real evidence, not the strongest tier | Include with warning flag; surface in `gaps` |
| INFERRED | `〰️` | Inferred from naming convention or framework default only | Mark as inferred; `SKL-DA2` to verify |
| UNKNOWN | `❓` | Cannot reach the 0.70 confidence floor by any method | Escalate; populate `gaps`; do NOT guess |

**Legacy tag mapping** _(this skill's original numeric confidence ladder, mapped onto the taxonomy above)_:

| Original numeric score | Meaning | Maps to |
|---|---|---|
| 1.0 | Confirmed by live DB query | `EXTRACTED` |
| 0.9 | Confirmed by migration file | `EXTRACTED` |
| 0.8 | Confirmed by entity/ORM code (EF model, annotations) | `EXTRACTED` |
| 0.75 | Confirmed by repository/query code | `PARTIAL` |
| 0.70 | Inferred from naming convention or framework default only | `INFERRED` |
| < 0.70 | Below floor | `UNKNOWN` — mark with inline reason, never guess |

#### Mandatory Tagging Rules

- Every finding in every one of the 13 output files carries a `confidence_tag` (or the numeric score it maps from)
- `confidence_score` is computed per §6.2, informed by the numeric ladder above
- `INFERRED` and `UNKNOWN` findings always appear in `gaps` with a reason
- `UNKNOWN` findings are never presented to stakeholders without `SKL-DA2` (or human) resolution first

#### Display Convention

```
✅ EXTRACTED — "db_connection": "CONNECTED — psql at C:\\Program Files\\PostgreSQL\\18\\bin\\psql.exe"
⚠️ PARTIAL  — confirmed by repository/query code only (0.75) — [table/field]
〰️ INFERRED — naming convention/framework default only (0.70) — [table/field]
❓ UNKNOWN  — "db_connection": "CODE-ONLY — connection refused at localhost:5432. Command run: psql -h localhost -p 5432 -U postgres -d eShopCatalog -c \\dt"
```

---

## BLOCK 5 — EXECUTION

### 5.1 Constraints & Guardrails

**Hard Constraints _(MUST NOT do these under any circumstances)_:**
- NEVER interpret business intent or make design decisions — surface facts only
- NEVER produce a Business Requirements Document
- NEVER review UI, frontend, or non-data code
- NEVER write new code or fix bugs
- NEVER skip the database connection attempt and silently fall back to code-only — document the exact error and command if it fails
- NEVER guess a value below the 0.70 confidence floor — mark `UNKNOWN` with an inline reason instead

**Soft Constraints _(PREFER NOT TO — may override with justification)_:**
- Prefer to use Layer 1 JSON over raw file reads wherever it covers the needed evidence (§3.1) — override only when a field is marked `unknown` or missing
- Prefer to write each of the 13 output files as its phase completes rather than batching all writes at the end

**Scope Boundaries:**

| IN Scope | OUT of Scope |
|----------|-------------|
| Schema extraction (tables, columns, relationships, indexes) | Business Requirements Document generation |
| Live DB verification | UI / frontend review |
| PII and data-quality inventory | Writing or fixing application code |
| Canonical/shadow entity detection | Independent re-verification against tests/docs (SKL-DA2's job) |
| Data dictionary / conceptual model / access control matrix | Business-intent interpretation beyond what data structure implies |

**Data Sensitivity Rules:**

| Data Type | Rule |
|-----------|------|
| PII (names, emails, IDs) | Column *names* and classification recorded in `pii-inventory.json`; never record real row-level PII values |
| Credentials / Secrets | Connection host/port/db-name/username may be recorded; passwords and secrets are never recorded |
| Confidential Business Logic | Hidden business rules encoded in data constraints (e.g. cache TTLs) ARE the point of `hidden-business-rules.json` — recorded as rules, not raw values |
| Third-party IP / Licensed Code | Not applicable at this depth |

**Exclusion List** _(never scan these)_:
```
node_modules/    .git/          dist/          build/
out/             .next/         .nuxt/         __pycache__/
*.min.js         *.bundle.js    *.lock         *.map
coverage/        .cache/        vendor/        bin/
```

### 5.2 Process & Methodology

**Step 1 — Phase 0: Auto-Detection**
- Input: `source_code.json`, `database.json` (Layer 1, if present) or raw source
- Action: detect language, framework, ORM, database engine; extract connection strings from `config.json` (host, port, database name, username — open raw config only if a connection string is missing/unknown); list all entity/route/config/integration files via the Layer 1 index (not a folder scan, if available); produce a chunk plan (one chunk per domain)
- Output: detected stack summary + chunk plan
- Decision Point: if entity/model files cannot be located at all after a full scan → escalate (§8.1)

**Step 2 — Phase 1: Code Discovery**
- Input: `source_code.json` (Layer 1) plus targeted raw reads for gaps
- Action, in order:
  1. Entity/model classes — fields, types, relationships from `source_code.json`; open a raw source file only if a field is `unknown` or a relationship is ambiguous
  2. Migration files, read chronologically — columns, indexes, FK rules, sequences (Layer 1 does not extract migration order — always read these directly)
  3. Repository and query classes, read directly — specifications, raw SQL, N+1 risks (not in Layer 1)
  4. Service class signatures via `source_code.json` — transaction boundaries visible from signatures; open service source only if method bodies are needed for constructor business rules
  5. Mandatory spot check — `config.json` (Layer 1) for `*/Config*` `*/Extensions*` `*/Cache*` settings; open `*/HealthChecks*` and `*/Background*` files directly (not fully extracted by Layer 1)
  6. Business-meaning & governance capture — XML doc comments, README/glossary text, validation messages, `[Authorize]` attributes and role/policy names, soft-delete flags and audit columns (`IsDeleted`, `CreatedAt`, etc.) — feeds the data dictionary, conceptual model, retention policy, and access control matrix
  7. Canonical/shadow entity detection — for every business concept appearing more than once, identify the canonical (source-of-truth) representation vs. shadow/duplicate ones; check whether each representation is actually constructed/queried anywhere (never-instantiated = strong shadow signal)
- Output: entity/relationship inventory, hidden business rules, redundancy analysis, data dictionary inputs

**Step 3 — Phase 2: Database Connection (mandatory, no skipping)**
- Input: connection strings from Phase 0
- Action: locate the DB CLI tool on the machine; run a connection test; on success, run row counts, schema verification, FK rules, indexes, sequences, triggers, and DQ checks — apply the Evidence Strength Hierarchy (§6.3) whenever live results conflict with code/migration assumptions, documenting both sides and which prevailed; on failure, document the exact error and command, continue code-only; repeat for every database found in Phase 0
- Output: live-verified (or CODE-ONLY-documented) schema facts

**Step 4 — Phase 3: Write Output Files**
- Input: all Phase 1/2 findings
- Action: write each of the 13 files to `da-outputs/` as its phase completes — do not batch:

| # | File | Write After |
|---|---|---|
| 1 | `schema-catalogue.json` | Phase 2 complete |
| 2 | `erd.md` | Phase 2 complete |
| 3 | `data-source-inventory.json` | Phase 1 step 6 + Phase 2 complete |
| 4 | `data-flow-map.md` | Phase 1 complete |
| 5 | `pii-inventory.json` | Phase 2 complete |
| 6 | `data-quality-report.md` | Phase 2 complete |
| 7 | `migration-complexity.json` | Phase 2 complete |
| 8 | `hidden-business-rules.json` | Phase 1 complete |
| 9 | `storage-pattern-analysis.md` | Phase 1 step 5 complete |
| 10 | `redundancy-analysis.json` | Phase 1 step 7 complete |
| 11 | `data-dictionary.md` | Phase 1 step 6 complete |
| 12 | `conceptual-data-model.md` | Phase 1 step 6 complete |
| 13 | `access-control-matrix.md` | Phase 1 step 6 + Phase 2 complete |

- Output: 13 files in `da-outputs/`

**Step 5 — Phase 4: Self-Check (fix any ❌ before finishing)**

| Check | Pass? |
|---|---|
| DB connection attempted? (YES or exact error documented) | |
| `db_connection` field set to CONNECTED or CODE-ONLY with reason? | |
| Row counts from live DB where connected? | |
| Caching section in `storage-pattern-analysis.md`? | |
| At least 5 files read from `*/Config*` `*/Extensions*` `*/HealthChecks*`? | |
| Every UNKNOWN value has an inline reason? | |
| All soft references listed in `erd.md` WARNING section? | |
| Caching TTL documented as a business rule in `hidden-business-rules.json`? | |
| Code-vs-DB conflicts resolved using the Evidence Strength Hierarchy (not guessed)? | |
| At least one canonical/shadow entity check completed (even if "no duplicates found")? | |
| Every table/column in `schema-catalogue.json` has a matching `data-dictionary.md` entry? | |
| Every role found in `[Authorize]` attributes appears in `access-control-matrix.md`? | |
| `conceptual-data-model.md` uses business language only — no table names, types, or FK syntax? | |

**Decision Tree:**

| Condition | Branch A | Branch B | Default |
|-----------|----------|----------|---------|
| DB connection fails with auth error | Run `dotnet ef database update` (or equivalent), retry once | — | Document the retry attempt regardless of outcome |
| DB connection fails with "connection refused" | Check for `docker-compose.yml` and note start command | Mark CODE-ONLY with exact error + command | — |
| A file is relevant in multiple domains | Read once, mark `🔁 SHARED`, reference by path in all chunks | — | Never re-read |
| Confidence cannot reach 0.80 | Include the finding, mark `⚠️ LOW CONFIDENCE — SKL-DA2 to verify` | — | Never omit |

**Iteration / Retry Rules:**

| Trigger | Max Retries | Strategy |
|---------|------------|---------|
| DB connection fails with auth error | 1 | Run migration/update command, retry connection once, then document final state either way |
| A domain's entity file is unreadable | 0 | Mark unresolved, continue with remaining files |

### 5.3 Analysis Depth & Granularity

| Level | Description | When to Activate | Typical Output Artifact |
|-------|-------------|-----------------|------------------------|
| System | Full system / portfolio overview | Not used — this skill scopes to data architecture, not full system | — |
| Module / Service | Component-level analysis | Default depth for entity/schema extraction | `schema-catalogue.json`, `erd.md` |
| Class / Entity | Object-level analysis | Entity/ORM model extraction | `data-dictionary.md`, `conceptual-data-model.md` |
| Function / Method | Procedural analysis | Repository/query method signatures for transaction boundaries | `hidden-business-rules.json` |
| Line / Statement | Detailed code inspection | Raw SQL in repository classes; migration column definitions | `migration-complexity.json`, `data-quality-report.md` |

**Default Depth Level for This Skill:** `Module / Service`, descending to `Line / Statement` specifically for raw SQL and migration parsing (these are never available pre-extracted in Layer 1 JSON).

**Coverage Threshold:**
> All 13 output files must exist in `da-outputs/`, and the Phase 4 self-check table must show no unresolved ❌ before the run is considered complete.

**Action if Coverage Threshold Not Met:**
> Still write every file that could be completed; mark incomplete files with their specific self-check failures in `gaps`; never silently omit a required output file.

**Reading Depth Rules** _(what to read deep vs skim vs skip)_:

| File / Artifact Type | Reading Rule | Reason |
|---------------------|--------------|--------|
| Entity/model classes | Layer 1 JSON first; raw file only for `unknown`/ambiguous fields | Avoids redundant reads when already extracted |
| Migration files | Read chronologically, in full | Not extracted by Layer 1; defines schema evolution order |
| Repository/query classes | Read directly, in full | Raw SQL and N+1 risk are not in Layer 1 |
| `*/Config*` `*/Extensions*` `*/Cache*` | Layer 1 JSON first | Fully extracted |
| `*/HealthChecks*` `*/Background*` | Read directly | Not fully extracted by Layer 1 |
| XML doc comments, README/glossary, validation messages | Read directly | Feeds data dictionary, conceptual model, retention policy |

### 5.4 Chunking & Context Management

> _Critical for RE on large codebases._

#### Chunking Strategy

| Dimension | Rule | Default |
|-----------|------|---------|
| Chunk unit | One domain (for code discovery) — but ALSO gated by a strict phase sequence (Phase 0 → 1 → 2 → 3 → 4) that cannot be skipped or reordered | Domain chunks, phase-gated |
| Max chunk size | No fixed line cap; Layer 1 JSON substitutes for most raw reads, keeping per-domain reads small | Layer 1 JSON preferred over raw reads wherever available |
| Chunk ordering | Domain-by-domain for Phase 1; Phase 2 (DB connection) runs once per database found, not per domain | Domain-first within Phase 1; DB-first within Phase 2 |

#### Context Window Caps

| Item Type | Cap | Selection Strategy When Over Cap |
|-----------|-----|----------------------------------|
| Config/extension/cache files spot-checked | At least 5 files minimum (Phase 4 self-check requirement) | Prioritize files not yet covered by Layer 1 JSON |
| Repository/query classes | Read in full (raw SQL not in Layer 1) | No truncation — raw SQL is high-value evidence |
| Migration files | Read in full, chronologically | No truncation — defines schema evolution ground truth |

#### Cross-Chunk Continuity Rules

- **Carried registries:** cumulative entity list, cumulative canonical/shadow entity findings, cumulative confidence-scored findings across all 13 output files
- **SHARED file rule:** if a file is relevant to multiple domains → read once, mark `🔁 SHARED`, reference by path in all chunks
- **Phase-gating rule:** Phase 2 (DB connection) never runs until Phase 1 (Code Discovery) is complete for all domains — the connection test is informed by every connection string found across the whole codebase, not just one domain
- **Registry reset rule:** never reset cumulative registries between domain chunks

#### Multi-Run / Incremental Analysis

| Scenario | Behaviour |
|----------|-----------|
| Re-running on same codebase after a code change | Re-run Phase 0-1 for domains whose files changed; Phase 2 (DB connection) re-runs in full since schema/data may have changed independent of code |
| Running on a subset of the codebase first | Treat the subset as the full domain set for this run; note in the handoff that other domains were out of scope |
| Resuming after a failed run mid-phase | Resume from the last completed phase; do not re-run completed phases; Phase 2 in particular should not be re-attempted if it already produced a definitive CONNECTED or CODE-ONLY result |

---

## BLOCK 6 — INTELLIGENCE

### 6.1 Decision Rules & Heuristics

| ID | Trigger Condition | Agent Action | Rationale |
|----|-------------------|--------------|-----------|
| H-001 | DB connection fails with "connection refused" | Check for `docker-compose.yml`, note start command, mark CODE-ONLY with exact error + command | Gives the user an actionable next step instead of a dead end |
| H-002 | A caching class is found in `*/Services*` | Document in BOTH `data-source-inventory.json` AND `storage-pattern-analysis.md` | Caching is both a data-source fact and a storage-pattern fact — must not be dropped from either view |
| H-003 | An FK has `ON DELETE = NO ACTION` | Flag in `data-quality-report.md` | Deleting a parent row with children present will error at runtime — an operational risk |
| H-004 | A file is relevant in multiple domains | Read once, mark `🔁 SHARED`, reference by path in all chunks | Avoids wasted re-reads and duplicate entries |
| H-005 | Confidence cannot reach 0.80 | Include the finding, mark `⚠️ LOW CONFIDENCE — SKL-DA2 to verify` | Never omit a real finding just because its confidence is thin |

**Pattern Recognition Catalog:**

| Pattern Name | Signature / Indicator | RE Significance | Action |
|--------------|----------------------|-----------------|--------|
| Canonical/shadow entity duplication | Same business concept represented by 2+ classes/fields (e.g. `AspNetUsers`, `Buyer`, loose `BuyerId`) | Indicates data integrity risk and migration complexity | Record all representations in `redundancy-analysis.json`; flag which is canonical vs. shadow |
| Soft-delete convention | `IsDeleted`, `DeletedAt` columns present | Indicates logical (not physical) deletion — affects retention policy and query correctness | Record in `data-dictionary.md` and note retention implication |
| Caching wrapper | A class in `*/Services*` or `*/Cache*` wrapping a repository/query call | Indicates a read-performance optimization with a TTL business rule | Record TTL as a business rule in `hidden-business-rules.json` |

**Ambiguity Resolution Strategy:**

| Ambiguity Type | Resolution Strategy |
|----------------|-------------------|
| Conflicting naming conventions across tables | Record both verbatim; flag `⚠️ PARTIAL`; do not normalise |
| A field's true type is undeclared anywhere | Mark `❓ UNKNOWN` with reason; do not guess a plausible type |
| Undocumented magic values in a data constraint | Record the literal value with source location; tag per the confidence ladder |
| An entity is defined but never constructed/queried | Strong shadow-entity signal — include in `redundancy-analysis.json`, mark accordingly |

**Prioritisation Logic:**
> When context window or time is constrained, analyze in this order:
1. Phase 0 (Auto-Detection) — always first, establishes the chunk plan
2. Phase 1 Code Discovery, domain by domain
3. Phase 2 Database Connection — once, after all domains' connection strings are known
4. Phase 3 Output writing, in the file-dependency order shown in §5.2 Step 4's table

### 6.2 Confidence & Uncertainty Handling

| Band | Score | Label | Agent Behaviour |
|------|-------|-------|----------------|
| High | 0.85 – 1.00 | Confident | Proceed; tag `✅ EXTRACTED`; include in output |
| Medium | 0.60 – 0.84 | Review advised | Tag `⚠️ PARTIAL`; include with warning; surface in `gaps` |
| Low | 0.40 – 0.59 | Uncertain | Tag `〰️ INFERRED`; attempt disambiguation before finalizing |
| Very Low | 0.00 – 0.39 | Cannot determine | Tag `❓ UNKNOWN`; escalate; do NOT fabricate |

**Confidence Score Calculation:**
- Method: `Hybrid` (rule-based numeric ladder, aggregated into the 4-band system)
- Formula: `(count(EXTRACTED)×1.0 + count(PARTIAL)×0.7 + count(INFERRED)×0.4 + count(UNKNOWN)×0) / total findings`

**Source-type confidence ladder** _(this skill's domain-specific refinement of the bands above)_:

| Score | Meaning | Band |
|---|---|---|
| 1.0 | Confirmed by live DB query | High → EXTRACTED |
| 0.9 | Confirmed by migration file | High → EXTRACTED |
| 0.8 | Confirmed by entity/ORM code (EF model, annotations) | High → EXTRACTED |
| 0.75 | Confirmed by repository/query code | Medium → PARTIAL |
| 0.70 | Inferred from naming convention or framework default only | Low → INFERRED |
| < 0.70 | Below floor | Very Low → UNKNOWN, mark with inline reason |

**Disambiguation Strategies** _(attempt in order before escalating)_:
1. Attempt a live DB query if not already connected — this is the highest-reliability disambiguator available (§6.3 rank 1)
2. Check the migration history chronologically for the most recent authoritative definition
3. If still unresolved, mark `UNKNOWN` with the specific reason (e.g. "DB not connected — connection refused at localhost:5432. Command attempted: ...") — never guess

### 6.3 Evidence Hierarchy

> _When multiple sources provide conflicting information about the same fact, this ranking determines which source wins. Identical to `SKL-DA2`'s Block 6.3 — both agents in this pair must agree on what outranks what. (Harmonized during template conversion — see §9.2 changelog.)_

#### Source Reliability Ranking

| Rank | Source Type | Reliability | Notes |
|------|-------------|-------------|-------|
| 1 — Highest | Live database (queried directly) | Definitive | What the system actually contains at runtime |
| 2 | Migration files (chronological) | Very High | Ground truth for schema evolution |
| 3 | ORM entity / model class | High | Declared structure — may lag behind DB |
| 4 | Test files with explicit data-shape assertions | Medium-High | Not read by this skill directly (out of scope, §3.2) — listed for hierarchy completeness since `SKL-DA2` inherits and uses this same ranking |
| 5 | Repository / query layer code | Medium-High | Shows what data is actually read/written |
| 6 | Naming conventions alone | Low | Inference only — must be flagged `INFERRED` |
| 7 — Lowest | Documentation / README / git history | Very Low | Wins ONLY if it cites a hard constraint (e.g. a documented legal retention period) — otherwise always loses to code/DB |

#### Conflict Resolution Rule

When two sources disagree:
1. The higher-ranked source wins
2. Document both sides in the output: `"code says X, live DB says Y — live DB wins per evidence hierarchy"`
3. Tag the winning value with the source that provided it
4. Add the conflict to `gaps` with both values and the resolution applied

#### Common RE Conflict Patterns

| Conflict | Typical Cause | Resolution |
|----------|--------------|------------|
| Entity in ORM but not in DB | Migration not run or entity deleted | Live DB wins; flag gap |
| Field in migration but not in ORM entity | ORM entity not updated after migration | Migration wins; flag for developer review |
| Config value differs between environments | Environment-specific override | Document all values; do not pick one |
| A documented "retention period" in README contradicts the code's actual delete behavior | Doc may state a legal requirement not yet implemented, or may simply be stale | If the doc cites a specific hard legal/compliance constraint, it wins and is flagged as an implementation gap; otherwise code wins and the doc is flagged stale |

---

## BLOCK 7 — INTEGRATION

### 7.1 Tools & Integrations

| Tool / API / MCP Server | Purpose | Access Method | Required |
|-------------------------|---------|---------------|---------|
| Codebase file access | Source of all extraction input | Read-only file access | ✓ |
| Database CLI tool (`psql`, `mysql`, `sqlcmd`, `mongosh`, etc.) | Live database verification (Phase 2) | Shell/CLI invocation, local machine | ✓ (attempt mandatory; success not required) |
| Layer 1 JSON extraction output | Pre-extracted `source_code.json`, `database.json`, `config.json`, `logs.json` | Read from disk if present | — (optional accelerator) |

**File Operation Permissions:**

| Operation | Permitted Paths | Restrictions |
|-----------|----------------|-------------|
| Read | Entire provided project source, excluding the exclusion list (§5.1); Layer 1 JSON output folder if present | — |
| Write | `da-outputs/` only | Never writes to source code or any path outside `da-outputs/` |
| Execute | Database CLI connection-test and read-only query commands only | No schema-mutating commands (no `CREATE`, `ALTER`, `DROP`, `INSERT`, `UPDATE`, `DELETE`) — except the documented retry of a migration/update command on an auth-error connection failure (§5.2 Decision Tree), which is an explicit, narrow exception |

### 7.2 Dependencies

**Upstream Skills** _(must complete before this skill runs)_:

| Skill ID | Skill Name | Output Consumed | Dependency Type |
|----------|------------|-----------------|--------------------|
| — | None (no skill file) | — | — |

**External Systems:**

| System | Purpose | Data Flow | Connection Type |
|--------|---------|-----------|----------------|
| Layer 1 Extraction (external, non-skill automated pre-step) | Provides `source_code.json`, `database.json`, `config.json`, `logs.json` as an accelerator | → (inbound to this skill) | Async (pre-computed before this skill runs); optional — falls back to raw scanning if absent |
| Live project database | Schema/data verification | ↔ (read-only queries out, results in) | Sync, local CLI invocation |

**Downstream Skills** _(receive this skill's output)_:

| Skill ID | Skill Name | What This Skill Provides | Trigger Condition |
|----------|------------|--------------------------|--------------------|
| `SKL-DA2` | DA Agent 2 — Data Architecture Reviewer | All 13 files in `da-outputs/` | Immediately after this skill's Phase 4 self-check passes |
| `SKL-FOUNDATION` _(not yet templated)_ | Foundation Layer | Indirectly, via `SKL-DA2`'s enriched output | After all four architecture pairs complete |

### 7.3 Context Propagation & Handoff Protocol

**Context to Carry Forward** _(always pass to all downstream skills)_:
- The `db_connection` state (CONNECTED or CODE-ONLY with exact reason) — this gates `SKL-DA2`'s Pre-Flight Check
- All 13 output files in `da-outputs/`
- The full list of `LOW CONFIDENCE` items for `SKL-DA2` to verify

**State to Persist** _(store across sessions / incremental runs)_:
- `db_connection` result and the domain-by-domain completion state, to support resuming an interrupted run

**Handoff Artifact Format:**

```json
{
  "source_skill": "SKL-DA1",
  "run_id": "RUN-20260601-160000",
  "target_skill": "SKL-DA2",
  "confidence_score": 0.86,
  "context": {
    "db_connection": "CODE-ONLY — connection refused at localhost:5432",
    "domains_found": ["Catalog", "Ordering", "Identity"]
  },
  "artifacts": {
    "schema-catalogue.json": "...", "erd.md": "...", "...": "... (13 files total)"
  },
  "validation_queue": [
    { "item": "Order-Payment FK rule", "tag": "PARTIAL", "reason": "confirmed by repository code only (0.75); DB unreachable to confirm at 1.0" }
  ]
}
```

**Recommended Starting Point for Downstream Agent:**
> Not a fixed table name — `SKL-DA2` should start with whichever entity/domain has the most `LOW CONFIDENCE` items in the Validation Queue, since that is where verification retires the most risk; if `db_connection` is `CODE-ONLY`, `SKL-DA2`'s Pre-Flight Check requires it to attempt the connection again before anything else.

---

## BLOCK 8 — RELIABILITY

### 8.1 Error Handling & Fallbacks

| Failure Mode | Likelihood | Detection | Fallback Strategy | Escalation Rule |
|--------------|-----------|-----------|------------------|----------------|
| DB connection fails with auth error | M | Connection test command returns an auth error | Run `dotnet ef database update` (or equivalent), retry once | Document final CONNECTED/CODE-ONLY state regardless of retry outcome |
| DB connection fails with "connection refused" | M | Connection test command times out / refused | Mark CODE-ONLY with exact error + command; check for `docker-compose.yml` and note start command | Continue code-only — do not stop the whole run |
| Entity/model files not found after full folder scan | L | Phase 0/1 scan finds no model layer | N/A | Stop and ask the user |
| More than 40% of files are binary with no source | L | File-type scan | N/A | Stop and ask the user |
| Connection string is encrypted or redacted | L | Config parsing finds no usable string | N/A | Stop and ask the user |
| Caching class found in `*/Services*` | M | Pattern match during Phase 1 | Document in BOTH `data-source-inventory.json` AND `storage-pattern-analysis.md` | Continue |
| FK `ON DELETE = NO ACTION` | M | Schema/migration inspection | Flag in `data-quality-report.md` | Continue |
| A file is relevant in multiple domains | M | Cross-domain reference detected | Read once, mark `🔁 SHARED` | Continue |
| Confidence cannot reach 0.80 | M | Confidence ladder scoring | Include the finding, mark `⚠️ LOW CONFIDENCE — SKL-DA2 to verify` | Continue — never omit |

**Human Review Triggers** _(mandatory escalation conditions)_:
- [ ] Overall `confidence_score` below 0.60
- [ ] `gaps` list contains more than 10 items
- [ ] More than 30% of findings tagged `INFERRED` or `UNKNOWN`
- [ ] `db_connection` is `CODE-ONLY` AND more than 50% of schema findings are below the 0.80 confidence tier
- [ ] Evidence hierarchy conflict found that cannot be resolved automatically (§6.3)

**Escalation Path:**
1. Flag the item in `gaps` with the exact reason (including the connection command/error where relevant)
2. Carry it into the handoff to `SKL-DA2` as a Validation Queue item
3. If `SKL-DA2` also cannot resolve it (e.g. DB remains unreachable), it surfaces to human review at the Gate G1 stakeholder checkpoint

**Partial Output Policy:**
> A partial output (some of the 13 files incomplete) is acceptable only if every incomplete file still exists with its specific gap documented — never omit a required file entirely. `db_connection: CODE-ONLY` with a fully documented reason is an acceptable complete state, not a partial one — code-only analysis with honest confidence scoring is a valid, complete run.

### 8.2 Validation & QA Checklist

**Agent Self-Check** _(run before emitting any output — mirrors the Phase 4 table in §5.2)_:
- [ ] All required output schema fields are populated
- [ ] Every finding carries a `confidence_tag` from the taxonomy in §4.3
- [ ] `confidence_score` calculated per the method in §6.2
- [ ] `gaps` populated for all `INFERRED`, `UNKNOWN`, and below-0.80 items
- [ ] `handoff_context` package is well-formed and includes `db_connection` state
- [ ] No PII values, credentials, or secrets in output (names/keys only)
- [ ] No fabricated entities, relationships, or business rules
- [ ] Evidence hierarchy applied to all conflicting signals (§6.3)
- [ ] All 13 output files exist in `da-outputs/`
- [ ] Every table/column in `schema-catalogue.json` has a matching `data-dictionary.md` entry
- [ ] Every `[Authorize]`-derived role appears in `access-control-matrix.md`
- [ ] `conceptual-data-model.md` uses business language only

**Human Review Checklist:**
- [ ] Findings align with known system behaviour
- [ ] `INFERRED` findings are plausible and flagged for confirmation
- [ ] `UNKNOWN` findings are genuinely unresolvable from available artifacts
- [ ] No `EXTRACTED` findings that appear to be fabricated
- [ ] Coverage meets the threshold defined in §5.3 (all 13 files present)
- [ ] `db_connection` state and reason are clearly documented

**Automated Test Cases:**

| Test ID | Scenario | Input | Expected Output | Pass Criteria |
|---------|----------|-------|-----------------|---------------|
| T-001 | Live DB reachable | Valid connection string, DB running | `db_connection: CONNECTED`; row counts populated | All schema findings reach 1.0 tier where directly queried |
| T-002 | DB unreachable | Connection refused | `db_connection: CODE-ONLY` with exact error + command | Findings capped at 0.90 or below; `gaps` documents the reason |
| T-003 | Canonical/shadow entity present | `AspNetUsers`, `Buyer`, loose `BuyerId` all represent "customer" | `redundancy-analysis.json` identifies canonical vs shadow with construction/query evidence | At least one canonical/shadow check completed |
| T-004 | FK with `ON DELETE = NO ACTION` | Migration defines this FK rule | Flagged in `data-quality-report.md` | Risk documented, not silently passed over |

---

## BLOCK 9 — REFERENCE

### 9.1 Examples

#### Canonical Example (Standard Case)

**Scenario:**
> A .NET project with a reachable PostgreSQL database — the happy path where Phase 2 succeeds.

**Input:**
```json
{
  "project_source": ".NET solution with EF Core entities and PostgreSQL",
  "layer1_json": { "database.json": "present" }
}
```

**Expected Output:**
```json
{
  "confidence_score": 0.97,
  "findings": {
    "schema-catalogue.json": "12 tables, all confirmed via live DB query"
  },
  "gaps": []
}
```

**Notes:**
> Canonical because live DB confirmation is available for every finding, reaching the 1.0 tier.

#### Edge Cases

| ID | Description | Input Pattern | Expected Behaviour | Risk if Mishandled |
|----|-------------|--------------|-------------------|-------------------|
| E-001 | Live DB unreachable | Connection refused at localhost:5432 | `db_connection: CODE-ONLY` with exact error + command; continue code-only | Silently proceeding without documenting the failure misrepresents confidence |
| E-002 | Canonical/shadow entity duplication | "Customer" represented as `AspNetUsers`, `Buyer`, and loose `BuyerId` | All three recorded; canonical vs. shadow determined by construction/query evidence | Missing the duplication hides a real data-integrity risk from `SKL-DA2` |
| E-003 | Caching layer with a TTL | `IMemoryCache` with a 30s sliding TTL in a `*/Services*` class | TTL documented as a business rule in `hidden-business-rules.json`, AND the cache itself in `storage-pattern-analysis.md` | Recording it in only one file loses half the required cross-reference |

#### Anti-Patterns _(What NOT to Do)_

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|---------------|-----------------|
| Skipping the DB connection attempt because it "probably won't work" | Violates the mandatory Phase 2 requirement and produces undocumented confidence gaps | Always attempt; document the exact result either way |
| Guessing a column's type when it's undeclared everywhere | Fabricates a fact with no evidence | Mark `❓ UNKNOWN` with the specific reason |
| Recording only one representation of a duplicated business concept | Hides a real data-integrity/migration risk | Record all representations; mark canonical vs shadow |
| Batching all 13 output files to write at the very end | Loses partial progress if the run is interrupted mid-way | Write each file as its phase completes (§5.2 Step 4 table) |
| Skipping the Evidence Hierarchy when code and DB disagree | Arbitrary resolution; inconsistent output quality | Always rank sources (§6.3) and document which one won |

### 9.2 Changelog & Version Notes

| Version | Date | Author | Change Description |
|---------|------|--------|--------------------|
| 2.0.0 | 2026-06-01 | DA Reverse Engineering System | Original `03_DA_Agent1_DataExtractor.md` prompt (v2, June 2026) |
| 2.0.0 (template conversion) | 2026-07-06 | Skill file conversion pass | Reformatted into the `sdlc_skill_file_template_v2.md` 9-block structure; no behavioral change to the underlying extraction logic. The Evidence Hierarchy (§6.3) was harmonized with `SKL-DA2`'s more complete version (which additionally ranks test files above repository code) — the original v2 prompt for this file did not mention tests in its hierarchy at all; both files now state the identical ranking since they operate on the same evidence. |

---

_Template v2.0 · 9 Blocks · 24 Sections · SDLC Agentic AI Platform · RE-optimised_
_Converted from: `prompts-ready-to-use/03_DA_Agent1_DataExtractor.md` · Pair with: `skill-files/04_DA_Agent2_DataReviewer.md` (`SKL-DA2`)_
