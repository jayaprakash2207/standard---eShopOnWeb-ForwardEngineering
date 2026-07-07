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

```
INPUT: Legacy codebase (GitHub URL / local path)
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  STEP 1 — Layer 1 (Python AST, NO LLM, ~5 min)         │
│  → source_code.json  database.json  config.json         │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  STEP 2 — BA Agent 1: Structural Scout (~15 min)        │
│  → 6 inventory files (entities, states, roles, caps)   │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  STEP 3 — BA Agent 2: Deep Analyst (~15 min)            │
│  → 8 business docs (rules, processes, value streams)   │
└──────────┬───────────┴──────────────┬───────────────────┘
           │                          │
    ┌──────▼──────┐  ┌───────▼──────┐  ┌──────▼──────┐
    │  THREAD 1   │  │  THREAD 2    │  │  THREAD 3   │
    │  DA track   │  │  TA track    │  │  AA track   │
    │  Steps 4-5  │  │  Steps 6-7   │  │  Steps 8-9  │
    │  ~20 min    │  │  ~20 min     │  │  ~25 min    │
    │             │  │              │  │  (Claude,   │
    │  schema,ERD │  │  blueprint,  │  │  not Python)│
    │  PII, flows │  │  security,   │  │             │
    │             │  │  NFRs, debt  │  │  services,  │
    └──────┬──────┘  └───────┬──────┘  │  APIs, DI   │
           │                 │         │  wiring     │
           └─────────────────┴─────────┴──────┬──────┘
                                              │
                                              ▼
┌─────────────────────────────────────────────────────────┐
│  STEP 10 — Foundation: Knowledge Graph + 20 Docs        │
│  (~30 min)                                              │
│  → ENTERPRISE_KNOWLEDGE_GRAPH.json                      │
│  → CANONICAL_ENTERPRISE_MODEL.md                        │
│  → ARCHITECTURE_INVENTORY.md                            │
│  → TRACEABILITY_MATRIX.md                               │
│  → 20 forward-engineering documents                     │
└─────────────────────────────────────────────────────────┘

Total wall clock: ~1.5–2 hours
```

**Key design decisions:**
- Layer 1 is deterministic Python — zero LLM calls, zero token cost, reads what is actually in the code
- BA agents run sequentially (Agent 2 needs Agent 1's output)
- DA, TA, AA run in 3 parallel threads — wall clock = slowest track only
- AA layer uses Claude (not Python) — catches correct method signatures, DI wiring, architecture violations

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
