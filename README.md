# eShopOnWeb — Enterprise Forward Engineering Package

A complete, production-ready enterprise architecture package reverse-engineered from the eShopOnWeb .NET 8 reference application. Includes 20 architecture documents, a 274-node knowledge graph, 8 ready-to-paste AI prompts, and a **fully automated pipeline** that runs the entire analysis with a single command.

**Production hardened:** auto-retries on Claude API failures (3 attempts, 30s wait), resumes from last completed step if interrupted — safe to re-run at any time.

---

## Two Ways to Use This

| | Manual (prompts) | Automated (pipeline) |
|---|---|---|
| **How** | Paste 8 prompts into Claude one by one | `python run.py --source <path>` |
| **Time** | Days / weeks | ~1.5–2 hours |
| **Human needed** | Yes — at every step | No |
| **Output** | Same 20 docs + KG | Same 20 docs + KG |
| **Use when** | You want full control at each step | You want results fast |

---

## Quickstart — Automated Pipeline

### Prerequisites

```bash
# Python dependencies
pip install -r requirements.txt

# Claude Code CLI (required — agents call Claude headlessly)
npm install -g @anthropic/claude-code
claude login
```

### Run on the included eShopOnWeb source

```bash
python run.py \
  --source "source/eShopOnWeb" \
  --output ./results
```

### Run on any other codebase

```bash
# GitHub URL
python run.py --source "https://github.com/your-org/your-app" --output ./results

# Local folder
python run.py --source "C:/projects/legacy-app" --output ./results

# Skip Layer 1 if already extracted
python run.py --source "C:/projects/legacy-app" --output ./results --skip-layer1
```

### Output structure

```
results/
├── Source_Extraction/          ← Layer 1 JSON artifacts
├── Business_Analysis/          ← BA Agent 1 + 2 outputs
├── Data_Analysis/              ← DA Agent 1 + 2 outputs
├── Technology_Analysis/        ← TA Agent 1 + 2 outputs
├── Application_Analysis/       ← AA Agent 1 + 2 outputs
├── Foundation_KnowledgeGraph/  ← Enterprise Knowledge Graph + 4 views
└── ForwardEngineering_Docs/    ← 20 forward-engineering documents
```

---

## Run Batch-by-Batch (avoid token limits)

Instead of running all 10 steps at once with `run.py`, you can run each step as a
separate command. Each command is its own Claude session, so the token cost is spread
across multiple runs — ideal when you hit per-session token limits.

**Run every command from the project root.** Set the source and output once:

```powershell
$src = "source/eShopOnWeb"
$out = "./results"
```

### Order rules
- **Batches 1 → 2 → 3 must run first, in order.**
- The **DA / TA / AA tracks (batches 4–9)** can run in any order after batch 3, but within each track Agent 1 must run before Agent 2.
- **Batch 10 (Foundation) runs last** — it needs all previous outputs.
- Wait for each command to finish before starting the next.

### Batch 1 — Layer 1 (deterministic AST, no tokens)
```powershell
# Run from inside the pipeline/ folder
cd pipeline
python -m layer1 --source (Resolve-Path "../source/eShopOnWeb") --output "../results/Source_Extraction"
cd ..
```
> If `results/Source_Extraction/` already exists from a previous run, you can **skip Batch 1** and reuse it.

### Batch 2 — BA Agent 1 (Structural Scout)
```powershell
python pipeline/runners/ba_agent1_runner.py --input "$out/Source_Extraction" --repo-root $src --output "$out/Business_Analysis"
```

### Batch 3 — BA Agent 2 (Deep Analyst)
```powershell
python pipeline/runners/ba_agent2_runner.py --input "$out/Source_Extraction" --repo-root $src --output "$out/Business_Analysis"
```

### Batch 4 & 5 — DA track (Data Extractor → Data Reviewer)
```powershell
python pipeline/runners/da_agent1_runner.py --input "$out/Source_Extraction" --repo-root $src --output "$out/Data_Analysis"
python pipeline/runners/da_agent2_runner.py --input "$out/Source_Extraction" --repo-root $src --output "$out/Data_Analysis"
```

### Batch 6 & 7 — TA track (Stack Scout → Deep Analyst)
```powershell
python pipeline/runners/ta_agent1_runner.py --input "$out/Source_Extraction" --repo-root $src --output "$out/Technology_Analysis"
python pipeline/runners/ta_agent2_runner.py --input "$out/Source_Extraction" --repo-root $src --output "$out/Technology_Analysis"
```

### Batch 8 & 9 — AA track (App Extractor → Quality Review)
```powershell
python pipeline/runners/aa_agent1_runner.py --input "$out/Source_Extraction" --repo-root $src --output "$out/Application_Analysis"
python pipeline/runners/aa_agent2_runner.py --input "$out/Source_Extraction" --repo-root $src --output "$out/Application_Analysis"
```

### Batch 10 — Foundation (Knowledge Graph + 20 documents)
```powershell
python pipeline/foundation_runner.py --output $out
```

> **Note (PowerShell):** always run each command on a single line — do not use `\`
> line continuations (that is bash syntax and will error in PowerShell).

---

## Pipeline Architecture

The pipeline runs **8 steps** using 9 Claude agent calls across 4 analysis layers. Steps 1–3 are sequential. Steps 4–7 fan out into **3 parallel threads**. Step 8 synthesises everything.

### Execution Flow

```
INPUT: Legacy codebase (GitHub URL or local path)
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│  STEP 1 — Layer 1: Source Extraction                     │
│  Pure Python AST — zero LLM calls — ~5 min              │
│                                                          │
│  Reads: .cs, .json, .yml, .csproj, migrations           │
│  → Source_Extraction/Source_Code.json                    │
│     (all classes, methods, fields, namespaces)           │
│  → Source_Extraction/Database.json                       │
│     (tables, columns, relationships, indexes)            │
│  → Source_Extraction/Config.json                         │
│     (all config keys/values from appsettings files)      │
│  → Source_Extraction/Logs.json                           │
│     (log patterns and event names)                       │
│  → Source_Extraction/Extraction_Summary.json             │
└──────────────────────────┬───────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────┐
│  STEP 2 — BA Agent 1: Structural Scout                   │
│  Claude agent — ~15 min                                  │
│                                                          │
│  Reads: Layer 1 JSON + source files                      │
│  Maps what exists — entity names, state values, roles,   │
│  method signatures. No interpretation, no meaning.       │
│  → Business_Analysis/BA_Structural_Scout.md              │
│     6 structured inventory files:                        │
│     entity list · state machines · roles & permissions   │
│     business capabilities · API surface · module map     │
└──────────────────────────┬───────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────┐
│  STEP 3 — BA Agent 2: Deep Analyst                       │
│  Claude agent — ~15 min                                  │
│                                                          │
│  Reads: BA_Structural_Scout.md + Layer 1 JSON            │
│  Reads method bodies, validation logic, state            │
│  transitions, call chains — interprets business meaning  │
│  → Business_Analysis/BA_Deep_Analyst.md                  │
│     8 business architecture artifacts:                   │
│     business rules catalogue · process models            │
│     value streams · domain boundaries · capability map   │
└────────┬──────────────────┬──────────────────┬───────────┘
         │                  │                  │
         ▼                  ▼                  ▼
  ┌─────────────┐   ┌──────────────┐   ┌──────────────┐
  │ DATA TRACK  │   │ TECH TRACK   │   │  APP TRACK   │
  │ Thread 1    │   │ Thread 2     │   │  Thread 3    │
  ├─────────────┤   ├──────────────┤   ├──────────────┤
  │ STEP 4      │   │ STEP 4       │   │  STEP 4      │
  │ DA Agent 1  │   │ TA Agent 1   │   │  AA Agent 1  │
  │ Data        │   │ Stack Scout  │   │  App         │
  │ Extractor   │   │ ~15 min      │   │  Extractor   │
  │ ~15 min     │   │              │   │  ~25 min     │
  │             │   │ Inventories: │   │              │
  │ Schema,ERD, │   │ runtime,     │   │ Component    │
  │ data dict,  │   │ frameworks,  │   │ registry, DI │
  │ PII reg,    │   │ data stores, │   │ wiring, call │
  │ data flows  │   │ security     │   │ flows, arch  │
  │             │   │ libs, CI/CD, │   │ violations   │
  │             │   │ infra        │   │              │
  ├─────────────┤   ├──────────────┤   ├──────────────┤
  │ STEP 5      │   │ STEP 5       │   │  STEP 5      │
  │ DA Agent 2  │   │ TA Agent 2   │   │  AA Agent 2  │
  │ Data        │   │ Deep Analyst │   │  Quality     │
  │ Reviewer    │   │ ~15 min      │   │  Review      │
  │ ~15 min     │   │              │   │  ~15 min     │
  │             │   │ Arch pattern │   │              │
  │ Validates   │   │ catalog, NFR │   │ PASS /       │
  │ schema,     │   │ spec, secu-  │   │ PARTIAL /    │
  │ enriches    │   │ rity arch,   │   │ FAIL verdict │
  │ findings,   │   │ tech debt    │   │ + evidence   │
  │ open qs     │   │ register     │   │ traceability │
  └──────┬──────┘   └──────┬───────┘   └──────┬───────┘
         └──────────────────┴──────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│  STEP 8 — Foundation: Knowledge Graph + 20 Documents     │
│  2 sequential Claude calls — ~30 min total               │
│                                                          │
│  Reads: Business_Analysis/ · Data_Analysis/              │
│         Technology_Analysis/ · Application_Analysis/     │
│                                                          │
│  Call 1 (~15 min) → KG + foundation views + docs 01–10  │
│  Call 2 (~15 min) → docs 11–20 (receives KG as context) │
│                                                          │
│  → Foundation_KnowledgeGraph/                            │
│      ENTERPRISE_KNOWLEDGE_GRAPH.json  (274 nodes)        │
│      CANONICAL_ENTERPRISE_MODEL.md                       │
│      ARCHITECTURE_INVENTORY.md                           │
│      TRACEABILITY_MATRIX.md                              │
│      FORWARD_ENGINEERING_INPUT_MAP.md                    │
│  → ForwardEngineering_Docs/                              │
│      01_BRD.md through 20_UI_UX_SPECIFICATION.md         │
└──────────────────────────────────────────────────────────┘

Total wall clock: ~1.5–2 hours
Parallel tracks wall clock = slowest thread only (~25 min), not the sum
```

### Step-by-Step Reference

| Step | Agent | Input | Output File | Produces |
|---|---|---|---|---|
| 1 | Layer 1 (Python) | Source code | Source_Code.json · Database.json · Config.json · Logs.json | Full class/method/field inventory, DB schema, all config keys — **no LLM** |
| 2 | BA Agent 1 | Layer 1 JSON + source | BA_Structural_Scout.md | Entity list, state machines, roles, capabilities, API surface, module map |
| 3 | BA Agent 2 | BA_Structural_Scout.md | BA_Deep_Analyst.md | Business rules, processes, value streams, domain boundaries, capability map |
| 4† | DA Agent 1 | Layer 1 JSON | DA_Data_Extractor.md | Schema catalogue, ERD, data dictionary, PII register, data flows |
| 5† | DA Agent 2 | DA_Data_Extractor.md | DA_Data_Reviewer.md | Validated schema, enriched findings, open questions for review |
| 4† | TA Agent 1 | Layer 1 JSON + infra files | TA_Stack_Scout.md | Runtime, frameworks, data stores, security libs, CI/CD, infra inventory |
| 5† | TA Agent 2 | TA_Stack_Scout.md | TA_Deep_Analyst.md | Architecture pattern catalogue, NFR spec, security analysis, tech debt register |
| 4† | AA Agent 1 | Layer 1 JSON + service files | AA_App_Extractor.md | Component registry, module boundaries, call flow map, DI wiring, violations |
| 5† | AA Agent 2 | AA_App_Extractor.md | AA_Quality_Review.md | PASS / PARTIAL / FAIL verdict, evidence traceability report |
| 8 | Foundation (2 calls) | All \*_Analysis/ folders | 5 KG files + 20 FE docs | Enterprise Knowledge Graph + 20 forward-engineering documents |

> **†** Steps marked 4† and 5† run inside 3 parallel threads simultaneously. Wall clock time = slowest thread, not the sum.

### Resilience — Retry and Resume

Every Claude call has two automatic protections built into [pipeline/base_runner.py](pipeline/base_runner.py):

**Retry** — on any failure (rate limit, timeout, non-zero exit code) the runner waits 30 seconds and retries, up to 3 attempts. Only raises an error after all 3 attempts fail.

**Resume** — before calling Claude, every runner checks whether its output file already exists and is non-empty. If yes, it loads the saved file and skips the call. Foundation checks `Foundation_Raw_Output_Part1.md` before Call 1 and `Foundation_Raw_Output_Part2.md` before Call 2.

Practical effect: re-running the same command after any interruption resumes from exactly where it stopped — no repeated work, no overwritten outputs.

### Key Design Decisions

| Decision | Reason |
|---|---|
| Layer 1 is pure Python AST — no LLM | Deterministic, zero token cost, reads what is actually in the code — not what Claude guesses |
| BA agents run sequentially before all others | BA_Structural_Scout.md gives the entity and capability map that DA, TA, and AA agents all use as their starting point |
| DA / TA / AA run in 3 parallel threads | All three tracks are independent — no cross-track data dependency — so running them in parallel cuts wall clock by ~2/3 |
| AA uses Claude, not Python | Catches DI wiring patterns, constructor injection, architecture violations, and cross-layer call chains that static Python AST analysis cannot see |
| Foundation uses 2 sequential Claude calls | Claude has a per-response output limit. Generating all 25 documents in one call hits that limit after ~doc 06. Call 1 produces the KG + docs 01–10; Call 2 receives the KG as context and produces docs 11–20 |
| All output files are plain text or JSON | No proprietary formats — any downstream tool, LLM, or human can read them directly |

---

## Quickstart — Manual Prompts

The `Prompts_Ready_To_Use/` folder contains 8 fully assembled prompts. Paste each one directly into Claude with access to the target codebase.

```
STEP 1 → 01_BA_Agent1_StructuralScout.md     Business layer scan
STEP 2 → 02_BA_Agent2_DeepAnalyst.md         Business layer deep analysis
STEP 3 → 03_DA_Agent1_DataExtractor.md       Data layer extraction
STEP 4 → 04_DA_Agent2_DataReviewer.md        Data layer review
STEP 5 → 05_TA_Agent1_StackScout.md          Technology layer scan
STEP 6 → 06_TA_Agent2_DeepAnalyst.md         Technology layer deep analysis
STEP 7 → 07_AA_Agent1_AppExtractor.md        Application layer extraction
STEP 8 → 08_AA_Agent2_QualityReview.md       Application layer quality review
```

Run Agent 1 first, paste its output, then run Agent 2 in the same conversation. See `Prompts_Ready_To_Use/00_README.md` for full instructions.

---

## Pre-Built Output — eShopOnWeb

The analysis of eShopOnWeb is already complete and included in this repo. No need to run the pipeline unless you want to analyse a different codebase.

### Read the results

```
Forward_Engineering_Package/17_FORWARD_ENGINEERING_READINESS_REPORT.md  ← start here
Enterprise_Foundation_Package/ENTERPRISE_KNOWLEDGE_GRAPH.json            ← 274-node graph
Forward_Engineering_Package/                                              ← 20 documents
```

### Use for code generation

Feed to Claude (or any LLM) in this order:

```
1. Forward_Engineering_Package/16_GENERATION_MANIFEST.json
2. Forward_Engineering_Package/15_FORWARD_ENGINEERING_SPECIFICATION.md
3. Documents by layer:
   Business    → 01–04
   Data        → 05–09
   Application → 10–11
   Technology  → 12–14
   Frontend    → 19–20
```

Fill in `target_stack` in `16_GENERATION_MANIFEST.json` first — currently empty by design (technology-neutral).

---

## Repository Structure

```
standard---eShopOnWeb-ForwardEngineering/
│
├── run.py                               ← AUTOMATED PIPELINE entry point (NEW)
├── requirements.txt                     ← Python dependencies (NEW)
│
├── pipeline/                            ← Automated pipeline engine (NEW)
│   ├── base_runner.py                   ← Shared Claude CLI + Layer 1 loading
│   ├── foundation_runner.py             ← KG synthesis + 20 docs
│   ├── layer1/                          ← Deterministic AST extraction
│   │   ├── pipeline.py
│   │   ├── extractors/ (dotnet/java/python/js)
│   │   └── ...
│   └── runners/                         ← 8 prompt runners
│       ├── ba_agent1_runner.py          ← 01_BA_Agent1_StructuralScout.md
│       ├── ba_agent2_runner.py          ← 02_BA_Agent2_DeepAnalyst.md
│       ├── da_agent1_runner.py          ← 03_DA_Agent1_DataExtractor.md
│       ├── da_agent2_runner.py          ← 04_DA_Agent2_DataReviewer.md
│       ├── ta_agent1_runner.py          ← 05_TA_Agent1_StackScout.md
│       ├── ta_agent2_runner.py          ← 06_TA_Agent2_DeepAnalyst.md
│       ├── aa_agent1_runner.py          ← 07_AA_Agent1_AppExtractor.md
│       └── aa_agent2_runner.py          ← 08_AA_Agent2_QualityReview.md
│
├── source/eShopOnWeb/                   ← Original .NET 8 source code
│
├── Enterprise_Foundation_Package/        ← Knowledge graph (canonical)
│   ├── ENTERPRISE_KNOWLEDGE_GRAPH.json  ← 274-node graph
│   ├── CANONICAL_ENTERPRISE_MODEL.md
│   ├── TRACEABILITY_MATRIX.md
│   ├── ARCHITECTURE_INVENTORY.md
│   └── FORWARD_ENGINEERING_INPUT_MAP.md
│
├── Forward_Engineering_Package/          ← 20 architecture documents
│   ├── 01_BRD.md
│   ├── 02_BUSINESS_CAPABILITY_MODEL.md
│   ├── 03_USE_CASE_SPECIFICATION.md
│   ├── 04_BUSINESS_PROCESS_MODEL.md
│   ├── 05_DOMAIN_MODEL.md
│   ├── 06_DATA_DICTIONARY.md
│   ├── 07_DATA_MODEL_SPECIFICATION.md   ← includes PostgreSQL DDL
│   ├── 08_ERD.md
│   ├── 09_DATA_FLOW_DIAGRAM.md
│   ├── 10_SERVICE_CATALOG.md            ← 47 services
│   ├── 11_API_CONTRACT_SPECIFICATION.md ← 55 APIs
│   ├── 12_TECHNOLOGY_BLUEPRINT.md
│   ├── 13_SECURITY_ARCHITECTURE.md      ← includes RBAC model
│   ├── 14_NFR_SPECIFICATION.md
│   ├── 15_FORWARD_ENGINEERING_SPECIFICATION.md  ← 89 rules, 68 gates
│   ├── 16_GENERATION_MANIFEST.json      ← fill in target_stack here
│   ├── 17_FORWARD_ENGINEERING_READINESS_REPORT.md
│   ├── 18_DEPLOYMENT_ARCHITECTURE.md
│   ├── 19_FRONTEND_ARCHITECTURE.md
│   └── 20_UI_UX_SPECIFICATION.md
│
├── Prompts_Ready_To_Use/                 ← 8 manual prompts
│   ├── 00_README.md
│   └── 01–08 *.md
│
├── README.md                            ← This file
└── PROJECT_END_TO_END.md                ← Full pipeline design doc
```

---

## Key Numbers

| Metric | Value |
|---|---|
| Knowledge Graph nodes | 274 |
| Business Capabilities | 39 |
| Domain Entities | 15 |
| Services / Modules | 47 |
| APIs documented | 55 |
| Forward engineering rules | 89 |
| Forward engineering documents | 20 |
| Pipeline steps | 10 |
| Parallel threads (steps 4–9) | 3 |
| Estimated pipeline runtime | ~1.5–2 hours |

---

## Notes

- `target_stack` is intentionally empty — the package is technology-neutral. This is a deliberate human decision.
- `Buyer` / `CustomerProfile` entities are aspirational — not implemented in the legacy source.
- `DISC-001` — stock fields (`AvailableStock`, `RestockThreshold`, `MaxStockThreshold`, `OnReorder`) were verified absent from the real source and removed from all data artifacts.
- The automated pipeline and the manual prompts use the same 8 prompt files from `Prompts_Ready_To_Use/` — the runners load and inject them headlessly.

---

## Changelog

### v1.3 (2026-07-07)
- **Retry logic** — Every Claude call now automatically retries up to 3 times (30s wait between attempts) on rate limits, timeouts, or session errors. Only fails after all 3 attempts are exhausted.
- **Resume logic** — Every agent checks if its output file already exists before running. If yes, it skips and reuses the saved output. Foundation Call 1 and Call 2 each check for their raw output files. Re-running the same command after any interruption resumes from where it stopped — no wasted time, no duplicate work.

### v1.2 (2026-07-07)
- **Foundation truncation fix** — Foundation step now makes 2 sequential Claude calls (Call 1: KG + docs 01–10, Call 2: docs 11–20). Previously Claude hit its output limit after doc 06, leaving 15 documents unwritten. All 25 documents are now produced correctly.
- **Descriptive naming** — All output folders and files renamed from short codes (`ba-outputs`, `ba_agent1_output.md`) to readable names (`Business_Analysis/BA_Structural_Scout.md`). Applies to `results/`, `Test_Run/`, `Data_Analysis_Legacy/`, and all other output locations.
- **Batch-by-batch commands** — Added step-by-step PowerShell commands so the pipeline can be run one agent at a time to stay within per-session token limits.

### v1.1 (2026-07-06)
- **Token cost reduction (~30–40%)** — DA, TA, and AA agent prompts now read from Layer 1 JSON first instead of re-reading the same source files that BA already extracted. Same output, lower cost.
