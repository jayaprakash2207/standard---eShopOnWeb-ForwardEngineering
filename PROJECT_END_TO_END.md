# Project End-to-End — What It Is, What It Has, How It Works

**Project:** Forward-/Reverse-Engineering Enterprise Platform (`frwd engg - op's`)
**Document type:** Whole-project deep-dive (system + prompt-architecture journey)
**Last updated:** 2026-06-29
**Grounding:** Every claim below is drawn from files in this repository. Where the source records `unknown`/`inferred`/`LOW`, this document preserves that — it does not invent.

---

## 0. TL;DR — what this project is in three sentences

1. It is an **AI-assisted reverse-engineering platform** that takes a legacy codebase (worked example: **eShopOnWeb**, a .NET 8 reference app) and reconstructs a complete, evidence-anchored **enterprise architecture** across five TOGAF-style layers — Business, Data, Application, Technology, and a Foundation/synthesis layer.
2. The Foundation layer merges all four layers into a single **Enterprise Knowledge Graph (274 evidence-anchored nodes)**, which is then projected into a **20-document Forward-Engineering Package** an AI agent can use to *regenerate* the application on a modern stack **without the legacy source**.
3. Wrapped around the pipeline is a full **prompt-governance program** — the prompts that drive the LLM stages were audited, governed, refactored, conformance-checked, optimized, cutover-validated, redesigned, and finally assembled into **8 ready-to-use prompts** in `prompts-ready-to-use/`.

So the repo contains **two intertwined things**: (A) the *engine* that does reverse→forward engineering, and (B) the *governance system* that makes the engine's prompts enterprise-grade.

---

## 1. The big picture (one diagram)

```
                          ┌─────────────────────────────────────────────────────────┐
   LEGACY CODEBASE  ─────▶│  LAYER 1 — Deterministic Python extraction (no LLM)      │
   (e.g. eShopOnWeb)      │  source_code.json · database.json · config.json · logs   │
                          └───────────────────────────┬─────────────────────────────┘
                                                       │  (raw, non-authoritative feed)
        ┌──────────────────────┬───────────────────────┼───────────────────────┬───────────────────────┐
        ▼                      ▼                        ▼                       ▼
  BUSINESS (BA)           DATA (DA)              APPLICATION (AA)         TECHNOLOGY (TA)
  Agent1 Scout →          Agent1 Extractor →     Agent1 AppExtractor →    Agent1 StackScout →
  Agent2 Analyst          Agent2 Reviewer        Agent2 QualityReview     Agent2 DeepAnalyst
  rules, capabilities,    schema, ERD, PII,      modules, services,       tech stack, infra,
  processes, docs         ownership, data flows  APIs, dependencies       NFRs, security
        └──────────────────────┴───────────────────────┬───────────────────────┴───────────────────────┘
                                                        │  (owner-cited facts)
                          ┌─────────────────────────────▼───────────────────────────┐
                          │  FOUNDATION / SYNTHESIS                                  │
                          │  reconcile → ENTERPRISE_KNOWLEDGE_GRAPH.json (274 nodes) │
                          │  → canonical model · inventory · traceability matrix     │
                          └─────────────────────────────┬───────────────────────────┘
                                                        │
                          ┌─────────────────────────────▼───────────────────────────┐
                          │  FORWARD-ENGINEERING PACKAGE (20 docs)                   │
                          │  Business(01-04) → Data(05-09) → Application(10-11) →   │
                          │  Technology(12-14) → Governance(15-17) →                │
                          │  Deployment(18) → Frontend(19-20)                       │
                          └─────────────────────────────┬───────────────────────────┘
                                                        ▼
                              [ AI agent regenerates the app on a modern stack ]
```

**Prompt system (around the LLM stages):**
```
prompt-governance/ → prompt-refactored/ → prompt-resolved/ → prompt-v2/ → prompts-ready-to-use/
(rules & standards)  (GOV-03 prompts)    (runnable)          (spec stubs)  ← USE THESE (8 complete prompts)
```

---

## 2. What's in the repository (top-level map)

| Directory / File | What it is | Role |
|---|---|---|
| `prompts-ready-to-use/` | **8 complete, ready-to-use prompts** — paste into Claude and run | Primary prompts (USE THESE) |
| `bussiness-architecture 1/bussiness-architecture/` | The Python pipeline + runners + source prompts + eShopOnWeb output | Reverse-engineering engine |
| `enterprise-foundation-package/` | `ENTERPRISE_KNOWLEDGE_GRAPH.json` (274 nodes) + 4 read-only views | Foundation output |
| `forward-engineering-package/` | 20-doc FE spec + `16_GENERATION_MANIFEST.json` | Forward-engineering input |
| `forward-engineering-completion-package/` | Completion docs produced during EARB audit — all merged into core 20 docs | Historical record |
| `prompt-governance/` | 10 governance docs (GOV-01…GOV-10) | Prompt rules |
| `prompt-refactored/` | 22 governed prompts (GOV-03 structure) | Historical |
| `prompt-resolved/` | 22 prompts with `{{include}}` expanded | Historical |
| `prompt-v2/` | 10 spec stubs (2 per layer) — not fully assembled | Historical |
| `prompt-optimization/` | Analysis that took 21→18 prompts | Historical |
| `migration-output/` | Cutover plan, compatibility, regression risk | Historical |
| `pilot-cutover-validation/` | Evidence-grounded pilot validation (6 reports) | Historical |
| `PROMPT_AUDIT_REPORT.md` | Root-level audit | Audit |
| `FINAL_PROMPT_CONFORMANCE_REPORT.md` | Final conformance check | Audit |
| `EVIDENCE_VERIFICATION_REPORT.md` | Ground-truth verification against real GitHub source | Verification |

---

## 3. PART A — The Reverse-Engineering Engine

### 3.1 Orchestration — how a run is driven

The entry point is **`run_pipeline.py`** (in `bussiness-architecture 1/bussiness-architecture/`). It:

- Takes `--source` (a Git URL, local path, or `.zip`), `--output`, and `--full-run` / `--repo-root`.
- Always runs **Layer 1** (deterministic extraction) via `Layer1Pipeline`.
- With `--full-run`, drives every LLM layer **sequentially as subprocesses**:

```
layer2_runner  →  layer3_runner          (Business)
da_agent1      →  da_agent2              (Data)
ta_agent1      →  ta_agent2              (Technology)
aa_runner                                (Application)
foundation_runner                        (Knowledge Graph synthesis)
```

> **Two prompt sets, two purposes — keep them separate:**
> - **Headless pipeline** (above) uses *data-driven* prompts (`layer2/layer2_prompt.md`, `data-architecture/DA_*`, `technology-architecture/TA_*`, `application-architecture/architecture-prompts/*`). They consume Layer 1's extracted JSON and write output files silently — no human needed.
> - **`prompts-ready-to-use/`** holds the *interactive* v3 prompts for MANUAL use — you paste them into Claude and point at a live codebase. They expect a human and a real source tree, and will stall if run headless. **They are not wired into `run_pipeline.py` by design.**

Each runner: **load prior JSON → build trimmed context → paste prompt + data → call Claude → parse/save outputs.**

### 3.2 Layer 1 — Deterministic extraction (NO LLM)

`layer1/pipeline.py` runs an 8-step extraction — **no model calls**, the reliable factual floor:

| Step | Component | Produces |
|---|---|---|
| 0 | `InputResolver` | clone/unzip/validate source |
| 1 | `LanguageDetector` | primary language → which extractors to use |
| 2 | `FileFilter` | whitelist extensions, blacklist junk dirs |
| 3 | language extractors (dotnet/java/python/javascript) | methods, classes, interfaces, enums |
| 4 | `DatabaseExtractor` | tables, stored procs, triggers, EF entities |
| 5 | `ConfigExtractor` | params, feature flags, connection strings, roles |
| 6 | `LogExtractor` | event/process sequences from logs |
| 7 | `Cleaner` | dedupe (MD5), normalize, drop low-quality |
| 8 | `OutputSaver` | `source_code.json`, `database.json`, `config.json`, `logs.json` |

> **Current weakness:** Uses text/regex parsing — not a formal AST parser (Roslyn). Complex generics, attributes, and nested DI wiring can be missed. Upgrade path: Roslyn Compiler API for .NET codebases.

### 3.3 The 8 ready-to-use prompts (LLM-driven layers)

Located in `prompts-ready-to-use/` — **for MANUAL / interactive runs** (paste into Claude, point at a live codebase). These are the highest-quality v3 prompts; use them when you want a hands-on, human-in-the-loop reverse-engineering session. For the fully automated headless pipeline, `run_pipeline.py` uses its own data-driven prompts instead (see §3.1).

Each layer has 2 agents. Agent 1 scans broad and fast. Agent 2 reads deep and produces final documents. Agent 2 always requires Agent 1's output first.

| # | Prompt | Layer | What it produces |
|---|---|---|---|
| 01 | `BA_Agent1_StructuralScout` | Business | 6 inventory files: domain map, entity inventory, state registry, role snapshot, capability skeleton, integration map |
| 02 | `BA_Agent2_DeepAnalyst` | Business | 8 docs: capability map, process flows, business rules catalog, stakeholder matrix, value streams, pain points, automation opportunities |
| 03 | `DA_Agent1_DataExtractor` | Data | 13 files: schema catalogue, ERD, data dictionary, PII inventory, data flow map, data quality, migration complexity, hidden business rules, storage patterns, redundancy analysis, conceptual model, access control matrix |
| 04 | `DA_Agent2_DataReviewer` | Data | Verified review report + gate verdict |
| 05 | `TA_Agent1_StackScout` | Technology | 6 inventory files: tech stack, infra, CI/CD, integrations, config, dependencies |
| 06 | `TA_Agent2_DeepAnalyst` | Technology | Technology blueprint, security assessment, NFR analysis, migration risk report, tech debt register |
| 07 | `AA_Agent1_AppExtractor` | Application | Full application architecture: dependency graph, component registry, call flow maps, violation register, API contracts, migration wave plan, security assessment (6 internal phases) |
| 08 | `AA_Agent2_QualityReview` | Application | PASS / PARTIAL / FAIL verdict with specific findings |

**Self-checking built into every agent:**
- DA Agent 1 has a 13-point mandatory checklist before it can finish
- BA Agent 2 has a Validation Queue — all LOW confidence items must be resolved or explained
- BA Agent 2 has a Discrepancy Log — every conflict between Agent 1 and Agent 2 must be logged
- AA Agent 1 has quality gate GR-7.1 — stops if inventory cannot be produced
- AA Agent 2 produces PASS/PARTIAL/FAIL verdict on the full output

### 3.4 The Foundation / Synthesis layer

All 4 layers converge here. Cross-track facts reconcile into one canonical node. Outputs:

- **`ENTERPRISE_KNOWLEDGE_GRAPH.json`** — 274 nodes, 9 sections:
  `metadata · business · data · application · technology · cross_links · assumptions · normalization_log · open_questions`
- **4 read-only views**: `CANONICAL_ENTERPRISE_MODEL.md`, `ARCHITECTURE_INVENTORY.md`, `TRACEABILITY_MATRIX.md`, `FORWARD_ENGINEERING_INPUT_MAP.md`

**The eShopOnWeb graph by the numbers:**

| Section | Contents | Count |
|---|---|---|
| business | capabilities 39, actors 5, processes 10 | 54 |
| data | entities 15, relationships 12, aggregates 4, repositories 4 | 35 |
| application | services 47, interfaces 13, apis 55, dependencies 19 | 134 |
| technology | current_stack 26, infrastructure 8, security 17 | 51 |
| cross_links | capability→process 17, process→entity 29, entity→service 16, service→api 55 | 117 |
| assumptions / open_questions | — | 7 / 9 |
| **Total nodes** | | **274** |

Every node: `id`, `type`, `owner_layer`, `confidence` (HIGH/MEDIUM/LOW/ASSUMED), `evidence` (file:line citations).

### 3.5 The Forward-Engineering Package — 20 documents

| # | Document | Layer |
|---|---|---|
| 01 | Business Requirements (BRD) | Business |
| 02 | Business Capability Model | Business |
| 03 | Use Case Specification | Business |
| 04 | Business Process Model | Business |
| 05 | Domain Model (DDD) | Data |
| 06 | Data Dictionary | Data |
| 07 | Data Model Spec + Physical Model + PostgreSQL DDL | Data |
| 08 | ERD | Data |
| 09 | Data Flow Diagram (L0/L1/L2) | Data |
| 10 | Service Catalog | Application |
| 11 | API Contract Specification (55 APIs) | Application |
| 12 | Technology Blueprint | Technology |
| 13 | Security Architecture + Modernization Plan + RBAC Auth Model | Technology |
| 14 | NFR Specification | Technology |
| 15 | Forward Engineering Specification (89 rules, 68 gates) | Cross-cutting |
| 16 | Generation Manifest (machine-readable JSON) | Cross-cutting |
| 17 | Forward Engineering Readiness Report | Assessment |
| 18 | Deployment Architecture | Technology |
| **19** | **Frontend Architecture** (2 surfaces, 43 routes, components) | Frontend |
| **20** | **UI/UX Specification** (20 pages, 4 user flows, validation rules) | Frontend |

### 3.6 Accuracy & Verification

| Item | Result |
|---|---|
| EARB initial audit | 79/100 |
| Ground-truth check vs real GitHub source | Verified |
| DISC-001 found and fixed | CatalogItem stock fields absent from real source — removed from all data artifacts |
| Completion package merged into core docs | Physical DDL, security modernization, RBAC auth model, implementation guidelines all merged |
| Docs 09, 12, 13 independently verified | Clean — no invented facts |
| **Final accuracy** | **97%** |

### 3.7 The anti-hallucination rule

The entire engine is built on **"never invent a fact."**
- Empty target stack stays empty
- Unknown versions stay `unknown`
- Inferred capabilities are labeled `inferred/LOW`
- Security gaps are recorded as findings, not silently fixed
- DISC-001 corrections are documented and physically applied — not papered over

---

## 4. PART B — The Prompt-Governance Journey

### 4.1 The seven stages

| Stage | Package | What happened | Result |
|---|---|---|---|
| 1. Audit | `PROMPT_AUDIT_REPORT.md` | Audited 20 legacy prompts | Uniformity 46/100; 3 paradigms, 3 confidence schemes, 4 cross-layer violations |
| 2. Govern | `prompt-governance/` (GOV-01…10) | Wrote the single-source rulebook | One standard every prompt follows |
| 3. Refactor | `prompt-refactored/` | Rewrote 20 → 22 governed prompts | All inline duplication removed |
| 4. Conformance | `FINAL_PROMPT_CONFORMANCE_REPORT.md` | Re-checked all 22 prompts | 98/100, all PASS |
| 5. Optimize | `prompt-optimization/` | Removed unwired duplicates | 21 → 18 prompts (−14%) |
| 6. Cutover | `migration-output/` + `prompt-resolved/` + `pilot-cutover-validation/` | Resolved `{{include}}`; validated against real outputs | PASS — 98.7% output-compat, 274-node graph preserved |
| 7. Redesign | `prompt-v2/` | Collapsed to 2-prompt-per-layer model (spec stubs) | 18 → 10 spec stubs |
| **8. Assemble** | **`prompts-ready-to-use/`** | **Assembled full working prompts from best source versions** | **8 complete, paste-and-run prompts** |

### 4.2 The four cross-layer violations fixed

| Violation | Fix |
|---|---|
| Technology layer doing Data work (transaction/consistency) | Relocated to Data layer |
| Technology layer doing Application security work | Relocated to Application layer |
| Application layer authoring the business capability map | Relocated to Business layer; AA now consumes it |
| Application layer authoring the data-ownership map | Relocated to Data layer; AA now consumes it |

**Principle: each fact has exactly one owning layer. Everyone else consumes-and-cites.**

### 4.3 The governance rulebook (GOV-01…GOV-10)

| Doc | Rule |
|---|---|
| GOV-01 | Global rules (GR-1…GR-10): anti-hallucination, evidence hierarchy, exclusions, no-modification, parse-first, validation, output, model pinning |
| GOV-02 | Ownership matrix — who owns what, who may only consume |
| GOV-03 | The canonical 12-section prompt template |
| GOV-04 | One confidence model: HIGH/MEDIUM/LOW/ASSUMED/DISCREPANCY |
| GOV-05 | Foundation/synthesis layer spec + reconciliation algorithm |
| GOV-06 | Per-prompt refactoring/migration plan |
| GOV-07 | Dependency model — DAG that terminates at Foundation |
| GOV-08 | Layer boundaries — May Extract / Consume / Produce / Must-Not |
| GOV-09 | 5 reusable components (CMP-GOV/CONF/VALID/EVID/OUT) |
| GOV-10 | Target end-state + readiness scoring |

### 4.4 The prompt generations — oldest to newest

| Generation | Folder | Prompts | Usable? |
|---|---|---|---|
| Legacy | `bussiness-architecture 1/.../` | Original BA/DA/AA/TA prompts | Yes — what ran the pipeline |
| Governed | `prompt-refactored/` | 22 governed prompts with `{{include}}` | Needs assembly |
| Resolved | `prompt-resolved/` | 22 with includes expanded | Yes but verbose |
| Spec stubs | `prompt-v2/` | 10 spec stubs | No — missing instructions |
| **Ready-to-use** | **`prompts-ready-to-use/`** | **8 complete prompts** | **Yes — USE THESE** |

---

## 5. End-to-end walkthrough (one concrete run, eShopOnWeb)

```
1. INPUT       Provide legacy codebase (local path, Git URL, or zip)

2. LAYER 1     Python extractors scan the repo (no LLM)
               → source_code.json, database.json, config.json, logs.json

3. BUSINESS    01_BA_Agent1 scans → 6 inventory files
               02_BA_Agent2 deep analysis → 8 business documents

4. DATA        03_DA_Agent1 extracts → 13 data files (schema, ERD, PII, flows)
               04_DA_Agent2 reviews → verified report + gate verdict

5. TECHNOLOGY  05_TA_Agent1 scans → 6 inventory files
               06_TA_Agent2 deep analysis → tech blueprint, security, NFRs

6. APPLICATION 07_AA_Agent1 extracts → full architecture (6 internal phases)
               08_AA_Agent2 reviews → PASS/PARTIAL/FAIL verdict

7. FOUNDATION  Reconcile all 4 layers → ENTERPRISE_KNOWLEDGE_GRAPH.json (274 nodes)
               → canonical model + inventory + traceability matrix

8. FWD-ENG     Project graph → 20 docs + generation manifest
               Verify against real source → 97% accuracy
               Fix DISC-001 (stock fields) across all affected files

9. OUTPUT      AI agent can now regenerate eShopOnWeb on any modern stack
               WITHOUT the legacy source — once target stack is decided (GR-08)
```

---

## 6. What the project has (capability inventory)

- ✅ Deterministic extraction floor (Layer 1, no LLM)
- ✅ 8 complete ready-to-use prompts in `prompts-ready-to-use/`
- ✅ Four TOGAF-aligned reverse-engineering layers (BA/DA/AA/TA), each Scout→Analyst
- ✅ Self-checking built into every agent (checklists, validation queues, discrepancy logs)
- ✅ Enterprise Knowledge Graph (274 nodes, 9 sections, full citations)
- ✅ Traceability matrix — capability → process → entity → service → API, end to end
- ✅ 20-document forward-engineering package — technology-neutral
- ✅ Physical data model + PostgreSQL DDL (merged from completion package)
- ✅ Security modernization plan + RBAC authorization model (merged)
- ✅ Frontend architecture + UI/UX specification (docs 19 + 20)
- ✅ Machine-consumable generation manifest (strict JSON, graph-grounded)
- ✅ Full audit trail: audit → conformance → optimization → cutover → pilot validation
- ✅ DISC-001 correction applied: stock fields removed from all data artifacts
- ✅ 97% verified accuracy

---

## 7. What it deliberately does NOT do / known limits

- ❌ **Does not pick a target stack** — empty by design; human decides (GR-08, the single remaining gate)
- ❌ **Does not reproduce legacy defects** — module dependency cycle and endpoint→repo violations are flagged to be re-architected, not regenerated
- ⚠️ **Layer 1 uses text/regex, not AST** — complex .NET generics/attributes can be missed; Roslyn upgrade would reach ~99%
- ⚠️ **No true self-healing** — agents self-check (checklists + validation queues) but cannot rerun themselves or execute code to verify findings
- ⚠️ **Deployment is local-dev-ready, production-incomplete** — containers + compose exist; no production IaC/release automation in evidence
- ✅ **Foundation runner wired and output present** — `foundation_runner.py` is the final pipeline step; output lives at `output/eShopOnWeb/foundation/` (mirrored from `enterprise-foundation-package/`)

---

## 8. How to navigate the repo (reading order)

1. **Want to run the pipeline on a new codebase?**
   Start at `prompts-ready-to-use/00_README.md` → run 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08

2. **Want the eShopOnWeb result?**
   Read `enterprise-foundation-package/CANONICAL_ENTERPRISE_MODEL.md` → then `forward-engineering-package/` docs 01→20

3. **Want the governance story?**
   `PROMPT_AUDIT_REPORT.md` → `prompt-governance/00_README.md` → `FINAL_PROMPT_CONFORMANCE_REPORT.md` → `pilot-cutover-validation/06_EXECUTIVE_SUMMARY.md`

4. **Want to start forward engineering?**
   Read `forward-engineering-package/17_FORWARD_ENGINEERING_READINESS_REPORT.md` → decide stack (GR-08) → feed `16_GENERATION_MANIFEST.json` + `15_FORWARD_ENGINEERING_SPECIFICATION.md` to a code generator

---

*This document is a navigational/explanatory overview. The authoritative source of truth for all
architecture facts is `enterprise-foundation-package/ENTERPRISE_KNOWLEDGE_GRAPH.json`.*
