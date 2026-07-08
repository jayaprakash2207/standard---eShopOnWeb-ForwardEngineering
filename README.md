<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f0c29,50:302b63,100:24243e&height=300&section=header&text=eShopOnWeb%20Forward%20Engineering&fontSize=42&fontColor=ffffff&fontAlignY=40&desc=Enterprise%20Architecture%20Pipeline%20%E2%80%94%209%20AI%20Agents%20%E2%80%94%2025%20Documents&descAlignY=62&descSize=18&animation=fadeIn" width="100%"/>

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&pause=1000&color=58A6FF&center=true&vCenter=true&width=750&lines=Reverse+Engineer+Any+Legacy+Codebase+Automatically;9+Claude+AI+Agents+Across+4+Analysis+Layers;25+Production-Grade+Architecture+Documents;274-Node+Enterprise+Knowledge+Graph;~1.5+Hours+%E2%80%94+Zero+Human+Intervention" alt="Typing SVG" />

<br/><br/>

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Claude AI](https://img.shields.io/badge/Claude-9%20AI%20Agents-FF6B35?style=for-the-badge&logo=anthropic&logoColor=white)](https://anthropic.com)
[![dotNET](https://img.shields.io/badge/.NET-8.0-512BD4?style=for-the-badge&logo=dotnet&logoColor=white)](https://dotnet.microsoft.com)
[![Documents](https://img.shields.io/badge/📄_Documents_Generated-25-27AE60?style=for-the-badge)](#-25-output-documents)
[![KG Nodes](https://img.shields.io/badge/🔗_Knowledge_Graph-274_Nodes-2980B9?style=for-the-badge)](Enterprise_Foundation_Package/ENTERPRISE_KNOWLEDGE_GRAPH.json)
[![APIs](https://img.shields.io/badge/🌐_REST_APIs-55_Documented-8E44AD?style=for-the-badge)](Forward_Engineering_Package/11_API_CONTRACT_SPECIFICATION.md)
[![Services](https://img.shields.io/badge/⚙️_Services-47_Catalogued-E67E22?style=for-the-badge)](Forward_Engineering_Package/10_SERVICE_CATALOG.md)

<br/>

> 🛡️ **Production hardened** — Auto-retry on Claude API failures (3×, 30 s wait) &nbsp;·&nbsp; Resume from last completed step &nbsp;·&nbsp; Safe to re-run at any time

</div>

---

## ⚡ What This Does

Hands a legacy codebase to **9 Claude AI agents** across 4 specialised analysis layers. Each agent reads the code from a different angle — business rules, data schema, tech stack, application structure. A final synthesis agent merges all findings into a **274-node Enterprise Knowledge Graph** and **20 architecture documents** a senior architect would take weeks to produce manually.

<div align="center">

| | Manual (by hand) | This Pipeline |
|---|:---:|:---:|
| ⏱️ **Time** | 2–4 weeks | ~1.5–2 hours |
| 👤 **Human needed** | At every step | Zero |
| 📄 **Documents** | 25 docs + KG | 25 docs + KG |
| ✅ **Reproducible** | No | Yes — re-run anytime |
| 🔍 **Evidence-cited** | Depends on analyst | Every finding cited |
| 💰 **Token cost** | N/A | ~30% lower (Layer 1 pre-extracts) |

</div>

---

## 🚀 Quick Start

```bash
# 1 — Install Python dependencies
pip install -r requirements.txt

# 2 — Install Claude Code CLI
npm install -g @anthropic/claude-code
claude login

# 3 — Run the pipeline
python run.py --source "source/eShopOnWeb" --output ./results

# Or point at any other codebase
python run.py --source "https://github.com/your-org/your-app" --output ./results
python run.py --source "C:/projects/legacy-app"               --output ./results
```

> [!TIP]
> **Interrupted mid-run?** Re-run the exact same command. Every step checks if its output file already exists and skips — only incomplete steps run again.

---

## 🗺️ Pipeline Flow — End to End

```mermaid
flowchart TD
    INPUT([" 📁  Legacy Codebase\n GitHub URL · Local Path · ZIP "])
    INPUT --> L1

    L1["🔧  STEP 1 — Layer 1  ·  Pure Python AST  ·  ~5 min  ·  Zero LLM calls\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\nSource_Code.json  ·  Database.json  ·  Config.json  ·  Logs.json"]
    L1 --> BA1

    BA1["🧠  STEP 2 — BA Agent 1  ·  Structural Scout  ·  ~15 min\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\nEntity list  ·  State machines  ·  Roles  ·  Capabilities  ·  Module map"]
    BA1 --> BA2

    BA2["🧠  STEP 3 — BA Agent 2  ·  Deep Analyst  ·  ~15 min\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\nBusiness rules  ·  Processes  ·  Value streams  ·  Domain boundaries"]
    BA2 --> SPLIT

    SPLIT{{"⚡  3 PARALLEL THREADS  —  wall clock = slowest thread only"}}
    SPLIT --> DA1
    SPLIT --> TA1
    SPLIT --> AA1

    subgraph DATATRACK ["🔵  DATA TRACK  ·  ~30 min"]
        DA1["DA Agent 1 — Data Extractor\nSchema · ERD · Data Dict · PII · Data flows"]
        DA1 --> DA2["DA Agent 2 — Data Reviewer\nValidate · Enrich · Open questions"]
    end

    subgraph TECHTRACK ["🟢  TECH TRACK  ·  ~30 min"]
        TA1["TA Agent 1 — Stack Scout\nRuntime · Frameworks · CI/CD · Infra"]
        TA1 --> TA2["TA Agent 2 — Deep Analyst\nArch patterns · NFR · Security · Tech debt"]
    end

    subgraph APPTRACK ["🟡  APP TRACK  ·  ~30 min"]
        AA1["AA Agent 1 — App Extractor\nComponents · DI wiring · Call flows"]
        AA1 --> AA2["AA Agent 2 — Quality Review\nPASS / PARTIAL / FAIL verdict"]
    end

    DA2 --> FOUND
    TA2 --> FOUND
    AA2 --> FOUND

    FOUND["⭐  STEP 8 — Foundation Synthesis  ·  2 × Claude calls  ·  ~30 min\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\nCall 1 → Enterprise Knowledge Graph  +  docs 01–10\nCall 2 → Architecture documents 11–20  (KG as context)"]
    FOUND --> OUTPUT

    OUTPUT([" ✅  25 Documents Ready\n 274-Node Knowledge Graph  +  20 Architecture Docs "])

    style INPUT   fill:#1a1a2e,color:#e0e0ff,stroke:#5555aa,stroke-width:2px
    style OUTPUT  fill:#0d2d1a,color:#d4ffda,stroke:#27ae60,stroke-width:2px
    style SPLIT   fill:#2d1f00,color:#ffe0a0,stroke:#e67e22,stroke-width:2px
    style FOUND   fill:#1a0d2d,color:#e8d4ff,stroke:#8e44ad,stroke-width:2px
    style DATATRACK fill:#0d1e30,color:#cce5ff,stroke:#2980b9
    style TECHTRACK fill:#0d2d1a,color:#d4ffda,stroke:#27ae60
    style APPTRACK  fill:#2d1a00,color:#ffe5cc,stroke:#e67e22
```

---

## 📊 Pipeline Analytics

<div align="center">

<table>
<tr>
<td align="center" width="50%">

**⏱️ Step Duration (minutes)**

<img src="https://quickchart.io/chart?w=480&h=260&c=%7Btype%3A%27horizontalBar%27%2Cdata%3A%7Blabels%3A%5B%27Foundation+%282+calls%29%27%2C%27DA%2BTA%2BAA+%28Parallel%29%27%2C%27BA+Agent+2%27%2C%27BA+Agent+1%27%2C%27Layer+1+%28Python%29%27%5D%2Cdatasets%3A%5B%7Blabel%3A%27Minutes%27%2Cdata%3A%5B30%2C30%2C15%2C15%2C5%5D%2CbackgroundColor%3A%5B%27rgba%28142%2C68%2C173%2C0.85%29%27%2C%27rgba%28230%2C126%2C34%2C0.85%29%27%2C%27rgba%2839%2C174%2C96%2C0.85%29%27%2C%27rgba%2846%2C204%2C113%2C0.85%29%27%2C%27rgba%2852%2C152%2C219%2C0.85%29%27%5D%7D%5D%7D%2Coptions%3A%7Bscales%3A%7BxAxes%3A%5B%7Bticks%3A%7BbeginAtZero%3Atrue%7D%7D%5D%7D%2Ctitle%3A%7Bdisplay%3Atrue%2Ctext%3A%27Step+Duration+%28minutes%29%27%7D%2Clegend%3A%7Bdisplay%3Afalse%7D%7D%7D" alt="Pipeline Timing Chart"/>

</td>
<td align="center" width="50%">

**📄 25 Documents by Category**

<img src="https://quickchart.io/chart?w=420&h=320&c=%7Btype%3A%27doughnut%27%2Cdata%3A%7Blabels%3A%5B%27Foundation+%26+KG%27%2C%27Business+Arch%27%2C%27Data+Architecture%27%2C%27App+%26+API%27%2C%27Tech+%26+Security%27%2C%27Forward+Engineering%27%5D%2Cdatasets%3A%5B%7Bdata%3A%5B5%2C4%2C5%2C2%2C4%2C5%5D%2CbackgroundColor%3A%5B%27rgba%2852%2C152%2C219%2C0.9%29%27%2C%27rgba%2846%2C204%2C113%2C0.9%29%27%2C%27rgba%28230%2C126%2C34%2C0.9%29%27%2C%27rgba%28142%2C68%2C173%2C0.9%29%27%2C%27rgba%28231%2C76%2C60%2C0.9%29%27%2C%27rgba%28241%2C196%2C15%2C0.9%29%27%5D%7D%5D%7D%2Coptions%3A%7Btitle%3A%7Bdisplay%3Atrue%2Ctext%3A%2725+Documents+by+Category%27%7D%2CcutoutPercentage%3A55%7D%7D" alt="Document Distribution"/>

</td>
</tr>
<tr>
<td align="center" colspan="2">

**🎯 Analysis Coverage by Dimension**

<img src="https://quickchart.io/chart?w=520&h=360&c=%7Btype%3A%27radar%27%2Cdata%3A%7Blabels%3A%5B%27Business+Rules%27%2C%27Data+Schema%27%2C%27Tech+Stack%27%2C%27Application+Layer%27%2C%27Security%27%2C%27API+Coverage%27%5D%2Cdatasets%3A%5B%7Blabel%3A%27Analysis+Depth+%25%27%2Cdata%3A%5B90%2C85%2C88%2C82%2C80%2C90%5D%2CbackgroundColor%3A%27rgba%2888%2C166%2C255%2C0.15%29%27%2CborderColor%3A%27rgba%2888%2C166%2C255%2C0.9%29%27%2CpointBackgroundColor%3A%27rgba%2888%2C166%2C255%2C1%29%27%2CpointRadius%3A5%2CpointHoverRadius%3A7%7D%5D%7D%2Coptions%3A%7Bscale%3A%7Bticks%3A%7BbeginAtZero%3Atrue%2Cmax%3A100%2CstepSize%3A20%7D%7D%2Ctitle%3A%7Bdisplay%3Atrue%2Ctext%3A%27Analysis+Coverage+by+Dimension+%28%25%29%27%7D%7D%7D" alt="Radar Coverage Chart"/>

</td>
</tr>
</table>

</div>

---

## 📦 25 Output Documents

### 🏛️ Foundation — Enterprise Knowledge Graph (5 files)

| File | What it contains |
|---|---|
| [ENTERPRISE_KNOWLEDGE_GRAPH.json](Enterprise_Foundation_Package/ENTERPRISE_KNOWLEDGE_GRAPH.json) | 274-node cross-layer graph — every entity, service, API, and tech node, fully linked with confidence scores |
| [CANONICAL_ENTERPRISE_MODEL.md](Enterprise_Foundation_Package/CANONICAL_ENTERPRISE_MODEL.md) | Human-readable summary — one row per node across all domains |
| [ARCHITECTURE_INVENTORY.md](Enterprise_Foundation_Package/ARCHITECTURE_INVENTORY.md) | Deployables, databases, APIs, services, tech stack, security findings, PII, tech debt |
| [TRACEABILITY_MATRIX.md](Enterprise_Foundation_Package/TRACEABILITY_MATRIX.md) | Full chain: Capability → Process → Entity → Service → API → Database |
| [FORWARD_ENGINEERING_INPUT_MAP.md](Enterprise_Foundation_Package/FORWARD_ENGINEERING_INPUT_MAP.md) | What is KNOWN · INFERRED · MISSING — input spec for AI code regeneration |

### 📄 Forward-Engineering Documents (20 files)

| # | Document | Contains |
|---|---|---|
| 01 | [Business Requirements Document](Forward_Engineering_Package/01_BRD.md) | Business goals, scope, stakeholders, success criteria |
| 02 | [Business Capability Model](Forward_Engineering_Package/02_BUSINESS_CAPABILITY_MODEL.md) | 39 capabilities mapped across business domains |
| 03 | [Use Case Specification](Forward_Engineering_Package/03_USE_CASE_SPECIFICATION.md) | Actors, preconditions, main flows, alternate paths |
| 04 | [Business Process Model](Forward_Engineering_Package/04_BUSINESS_PROCESS_MODEL.md) | End-to-end processes — triggers, steps, outcomes |
| 05 | [Domain Model](Forward_Engineering_Package/05_DOMAIN_MODEL.md) | DDD bounded contexts, aggregates, Mermaid context maps |
| 06 | [Data Dictionary](Forward_Engineering_Package/06_DATA_DICTIONARY.md) | Every entity, field, type, constraint, and business meaning |
| 07 | [Data Model Specification](Forward_Engineering_Package/07_DATA_MODEL_SPECIFICATION.md) | Physical schema + full PostgreSQL DDL ready to execute |
| 08 | [Entity Relationship Diagram](Forward_Engineering_Package/08_ERD.md) | Full ERD with cardinality and foreign key relationships |
| 09 | [Data Flow Diagram](Forward_Engineering_Package/09_DATA_FLOW_DIAGRAM.md) | Data movement across all layers and system boundaries |
| 10 | [Service Catalog](Forward_Engineering_Package/10_SERVICE_CATALOG.md) | 47 services — interfaces, responsibilities, dependencies |
| 11 | [API Contract Specification](Forward_Engineering_Package/11_API_CONTRACT_SPECIFICATION.md) | 55 REST endpoints with full request/response contracts |
| 12 | [Technology Blueprint](Forward_Engineering_Package/12_TECHNOLOGY_BLUEPRINT.md) | Target architecture, stack decisions, patterns |
| 13 | [Security Architecture](Forward_Engineering_Package/13_SECURITY_ARCHITECTURE.md) | RBAC model, auth flows, threat model, modernisation plan |
| 14 | [NFR Specification](Forward_Engineering_Package/14_NFR_SPECIFICATION.md) | Performance, availability, scalability, compliance targets |
| 15 | [Forward Engineering Specification](Forward_Engineering_Package/15_FORWARD_ENGINEERING_SPECIFICATION.md) | 89 generation rules · 68 validation gates |
| 16 | Generation Manifest *(repo root)* | Machine-readable JSON — fill `target_stack` to generate |
| 17 | [Readiness Report](Forward_Engineering_Package/17_FORWARD_ENGINEERING_READINESS_REPORT.md) | Scored readiness assessment — **start here** |
| 18 | [Deployment Architecture](Forward_Engineering_Package/18_DEPLOYMENT_ARCHITECTURE.md) | Containers, infra topology, deployment pipeline |
| 19 | [Frontend Architecture](Forward_Engineering_Package/19_FRONTEND_ARCHITECTURE.md) | UI architecture, component hierarchy, state management |
| 20 | [UI/UX Specification](Forward_Engineering_Package/20_UI_UX_SPECIFICATION.md) | Screen flows, interaction patterns, design system |

---

## 🏗️ Internal Architecture

```mermaid
graph TD
    subgraph ORCH ["🎛️  Orchestrator  —  run.py"]
        RUN["Master controller\nSequential steps + 3 Python threads\nRetry + Resume  via  base_runner.py"]
    end

    subgraph L1BOX ["🔧  Layer 1  —  pipeline/layer1/   Pure Python · No LLM"]
        direction LR
        IR["InputResolver\ngit clone / local / zip"] --> LD["LanguageDetector\n.cs · .java · .py · .ts"]
        LD --> FF["FileFilter\nskip bin/ obj/ node_modules/"]
        FF --> EX["Language Extractors\n.NET · Java · Python · JS\nregex + AST parsing"]
        EX --> DB["DatabaseExtractor\nSQL DDL + EF Core"]
        DB --> CF["ConfigExtractor\nappsettings · .env"]
        CF --> CL["Cleaner & OutputSaver\n→ 5 JSON files"]
    end

    subgraph L2BOX ["🧠  Layer 2  —  Business Analysis   Claude · Sequential"]
        direction LR
        BA1S["BA Agent 1\nStructural Scout"] --> BA2S["BA Agent 2\nDeep Analyst"]
    end

    subgraph L3BOX ["⚡  Layer 3  —  Parallel Analysis   Claude · 3 Threads"]
        direction LR
        DA1S["DA Agent 1\nData Extractor"] --> DA2S["DA Agent 2\nData Reviewer"]
        TA1S["TA Agent 1\nStack Scout"] --> TA2S["TA Agent 2\nDeep Analyst"]
        AA1S["AA Agent 1\nApp Extractor"] --> AA2S["AA Agent 2\nQuality Review"]
    end

    subgraph L4BOX ["⭐  Layer 4  —  Foundation Synthesis   Claude · 2 Calls"]
        direction LR
        C1["Call 1\nKG + Foundation\n+ Docs 01–10"] --> C2["Call 2\nDocs 11–20\n(KG as context)"]
    end

    ORCH --> L1BOX --> L2BOX --> L3BOX --> L4BOX
```

---

## 🛡️ Resilience — Retry & Resume

```mermaid
flowchart LR
    START([Agent starts]) --> CHK{Output file\nalready exists?}
    CHK -- YES --> SKIP([⏭️ Skip\nload saved output])
    CHK -- NO --> ATT1

    ATT1[Attempt 1\ncall Claude] --> OK1{Success?}
    OK1 -- YES --> SAVE([✅ Save output\ncontinue pipeline])
    OK1 -- NO --> W1[Wait 30 s]
    W1 --> ATT2[Attempt 2\ncall Claude] --> OK2{Success?}
    OK2 -- YES --> SAVE
    OK2 -- NO --> W2[Wait 30 s]
    W2 --> ATT3[Attempt 3\ncall Claude] --> OK3{Success?}
    OK3 -- YES --> SAVE
    OK3 -- NO --> FAIL([❌ Raise error\nwith clear message])

    style SKIP fill:#0d2d1a,color:#d4ffda,stroke:#27ae60
    style SAVE fill:#0d2d1a,color:#d4ffda,stroke:#27ae60
    style FAIL fill:#2d0d0d,color:#ffcccc,stroke:#e74c3c
    style START fill:#1a1a2e,color:#e0e0ff,stroke:#5555aa
```

> [!IMPORTANT]
> The pipeline can be interrupted at any point — power cut, rate limit, timeout — and re-running the **same command** resumes from exactly where it stopped. No work is ever repeated unless the step failed.

---

## 📐 Key Numbers

<div align="center">

| 🔗 KG Nodes | 📁 Capabilities | 🗃️ Entities | ⚙️ Services | 🌐 APIs | 📐 Gen Rules | 🚦 Gates | 📄 Docs | ⏱️ Runtime |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **274** | **39** | **15** | **47** | **55** | **89** | **68** | **25** | **~2 hrs** |

</div>

---

## 🔢 Two Ways to Use This

### Option A — Single Command *(recommended)*

```bash
python run.py --source "source/eShopOnWeb" --output ./results
```

Leave it running. Come back in ~2 hours. All 25 documents are waiting.

### Option B — Batch by Batch *(for token budget control)*

Run each agent as its own terminal session. Each session is independent — ideal when you need to stay within a per-session token limit. Wait for each command to fully finish before running the next.

> [!WARNING]
> **PowerShell users:** Run each command on a **single line**. Never use `\` for line continuation — it is bash syntax and will cause a parser error in PowerShell.

---

#### 🟦 STEP 0 — Set variables once (copy this first, then keep the window open)

```powershell
$src = "source/eShopOnWeb"
$out = "./results"
```

---

#### 🟩 STEP 1 — Layer 1: Source Extraction
> Pure Python — no LLM, no token cost. Takes ~5 minutes. Skip if `results/Source_Extraction/` already exists.

```powershell
cd pipeline
python -m layer1 --source (Resolve-Path "../source/eShopOnWeb") --output "../results/Source_Extraction"
cd ..
```

---

#### 🟩 STEP 2 — BA Agent 1: Structural Scout
> Maps all entities, states, roles, capabilities. Must run before Step 3.

```powershell
python pipeline/runners/ba_agent1_runner.py --input "$out/Source_Extraction" --repo-root $src --output "$out/Business_Analysis"
```

---

#### 🟩 STEP 3 — BA Agent 2: Deep Analyst
> Reads method bodies and interprets business rules, processes, value streams. Must run after Step 2.

```powershell
python pipeline/runners/ba_agent2_runner.py --input "$out/Source_Extraction" --repo-root $src --output "$out/Business_Analysis"
```

---

#### 🟦 STEPS 4–9 — DA / TA / AA Tracks
> These three tracks are independent. You can run them in any order after Step 3 — but within each track, Agent 1 must run before Agent 2.

**DATA TRACK — Steps 4 and 5**

```powershell
# Step 4 — DA Agent 1: Data Extractor (schema, ERD, data dictionary, PII register, data flows)
python pipeline/runners/da_agent1_runner.py --input "$out/Source_Extraction" --repo-root $src --output "$out/Data_Analysis"
```

```powershell
# Step 5 — DA Agent 2: Data Reviewer  (validate, enrich, open questions)  — run after Step 4
python pipeline/runners/da_agent2_runner.py --input "$out/Source_Extraction" --repo-root $src --output "$out/Data_Analysis"
```

**TECHNOLOGY TRACK — Steps 6 and 7**

```powershell
# Step 6 — TA Agent 1: Stack Scout  (runtime, frameworks, CI/CD, infra inventory)
python pipeline/runners/ta_agent1_runner.py --input "$out/Source_Extraction" --repo-root $src --output "$out/Technology_Analysis"
```

```powershell
# Step 7 — TA Agent 2: Deep Analyst  (arch patterns, NFR, security, tech debt)  — run after Step 6
python pipeline/runners/ta_agent2_runner.py --input "$out/Source_Extraction" --repo-root $src --output "$out/Technology_Analysis"
```

**APPLICATION TRACK — Steps 8 and 9**

```powershell
# Step 8 — AA Agent 1: App Extractor  (components, DI wiring, call flows, violations)
python pipeline/runners/aa_agent1_runner.py --input "$out/Source_Extraction" --repo-root $src --output "$out/Application_Analysis"
```

```powershell
# Step 9 — AA Agent 2: Quality Review  (PASS/PARTIAL/FAIL verdict + evidence)  — run after Step 8
python pipeline/runners/aa_agent2_runner.py --input "$out/Source_Extraction" --repo-root $src --output "$out/Application_Analysis"
```

---

#### 🟨 STEP 10 — Foundation: Knowledge Graph + 20 Documents
> **Always run this last.** Requires all 9 previous steps to be complete.

```powershell
python pipeline/foundation_runner.py --output $out
```

> ✅ When this finishes, all 25 documents are ready in `results/Foundation_KnowledgeGraph/` and `results/ForwardEngineering_Docs/`

---

**Run order summary:**

```
Step 1 → Step 2 → Step 3 → Steps 4–9 (any order, Agent 1 before Agent 2 within each track) → Step 10
```

---

## 📖 Using the Pre-Built Analysis

The full eShopOnWeb analysis is already included. No pipeline run needed unless you want to analyse a different codebase.

**Recommended reading order:**

```
1. Forward_Engineering_Package/17_FORWARD_ENGINEERING_READINESS_REPORT.md   ← start here
2. Enterprise_Foundation_Package/ENTERPRISE_KNOWLEDGE_GRAPH.json             ← source of truth
3. Forward_Engineering_Package/16_GENERATION_MANIFEST.json                  ← fill target_stack
4. Documents 01–20 by layer  (Business → Data → Application → Technology → Frontend)
```

> [!NOTE]
> `target_stack` in `16_GENERATION_MANIFEST.json` is **intentionally empty** — the package is technology-neutral. The same 25 documents support regeneration to .NET, Java, Node.js, Python, or any target stack.

---

## 📁 Repository Structure

```
📦 standard---eShopOnWeb-ForwardEngineering/
│
├── 🐍 run.py                               ← Pipeline entry point
├── 📄 requirements.txt
│
├── 📂 pipeline/
│   ├── base_runner.py                      ← Claude CLI + retry + resume (shared)
│   ├── foundation_runner.py                ← KG synthesis + 25 docs (2 calls)
│   ├── 📂 layer1/                          ← Pure Python AST extraction (no LLM)
│   │   ├── pipeline.py                     ← 8-step internal orchestrator
│   │   ├── input_resolver.py               ← git clone / local / zip
│   │   ├── language_detector.py            ← .NET · Java · Python · JS
│   │   ├── database_extractor.py           ← SQL DDL + EF Core DbSet
│   │   ├── config_extractor.py             ← appsettings / .env / web.config
│   │   ├── log_extractor.py                ← Business event scanner
│   │   ├── cleaner.py + output_saver.py    ← Normalise + write 5 JSON files
│   │   └── 📂 extractors/                  ← dotnet · java · python · javascript
│   └── 📂 runners/                         ← 8 Claude agent runners
│       ├── ba_agent1/2_runner.py
│       ├── da_agent1/2_runner.py
│       ├── ta_agent1/2_runner.py
│       └── aa_agent1/2_runner.py
│
├── 📂 Prompts_Ready_To_Use/                ← 8 fully-assembled agent prompts
├── 📂 source/eShopOnWeb/                   ← Original .NET 8 source
├── 📂 Enterprise_Foundation_Package/       ← KG + 4 foundation views
└── 📂 Forward_Engineering_Package/         ← 20 architecture documents
```

---

## 🛠️ Tech Stack

<div align="center">

<img src="https://skillicons.dev/icons?i=python,dotnet,github,vscode&theme=dark" alt="Tech Stack Icons"/>

</div>

---

## ⚙️ Key Design Decisions

| Decision | Reason |
|---|---|
| **Layer 1 is pure Python — no LLM** | Deterministic, zero token cost, reads what is literally in the code — not what Claude guesses |
| **BA runs before all others** | BA_Structural_Scout.md produces the entity and capability map that DA, TA, and AA all use as their reference baseline |
| **DA / TA / AA run in 3 parallel threads** | No cross-track dependency — parallel cuts wall clock time by ~2/3 vs sequential |
| **AA uses Claude, not Python** | Catches DI wiring, constructor injection, architecture violations, and cross-layer call chains that static AST cannot see |
| **Foundation uses 2 sequential calls** | Claude's per-response output limit cuts off at ~doc 06 in one call. Two calls with KG-as-context produces all 25 documents reliably |
| **All outputs are plain `.md` / `.json`** | Readable by humans, any LLM, any downstream tool — no proprietary format, no lock-in |

---

## 📜 Changelog

### v1.3 — 2026-07-07
- 🔁 **Retry logic** — every Claude call retries up to 3× (30 s wait) on rate limits, timeouts, or session errors
- ▶️ **Resume logic** — every agent skips if its output file already exists; re-running resumes from exactly where it stopped; Foundation checks Part 1 and Part 2 checkpoints separately

### v1.2 — 2026-07-07
- 🛠️ **Foundation truncation fix** — 2 sequential Claude calls; previously Claude hit its output limit at doc 06, leaving 15 documents unwritten
- 🏷️ **Descriptive naming** — all folders and files renamed from cryptic codes to readable `Title_Case` names
- 📋 **Batch-by-batch commands** — step-by-step PowerShell commands added for token budget control

### v1.1 — 2026-07-06
- 💰 **Token cost reduction (~30–40%)** — DA, TA, AA agents now read from Layer 1 JSON instead of re-reading source files BA already extracted

---

<div align="center">

Built with [Claude Code](https://claude.ai/code) &nbsp;·&nbsp; Powered by [Anthropic Claude](https://anthropic.com)

</div>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:24243e,50:302b63,100:0f0c29&height=120&section=footer" width="100%"/>
