"""
Foundation Runner
-----------------
Synthesizes all 4 layer outputs (BA, DA, TA, AA) into the
Enterprise Knowledge Graph and 4 read-only foundation views,
then generates the 20 forward-engineering documents.

Reads:
  <output>/Business_Analysis/     - BA Agent 1 + 2 output
  <output>/Data_Analysis/         - DA Agent 1 + 2 output
  <output>/Technology_Analysis/   - TA Agent 1 + 2 output
  <output>/Application_Analysis/  - AA Agent 1 + 2 output

Writes:
  <output>/Foundation_KnowledgeGraph/ENTERPRISE_KNOWLEDGE_GRAPH.json
  <output>/Foundation_KnowledgeGraph/CANONICAL_ENTERPRISE_MODEL.md
  <output>/Foundation_KnowledgeGraph/ARCHITECTURE_INVENTORY.md
  <output>/Foundation_KnowledgeGraph/TRACEABILITY_MATRIX.md
  <output>/Foundation_KnowledgeGraph/FORWARD_ENGINEERING_INPUT_MAP.md
  <output>/ForwardEngineering_Docs/01_BRD.md … 20_UI_UX_SPECIFICATION.md
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from base_runner import call_claude, save_output, load_prior_output

# ── Foundation synthesis prompt ────────────────────────────────────────────────

FOUNDATION_SYNTHESIS_PROMPT = """
# Foundation Synthesis Agent

You are the Foundation / Synthesis agent — the final stage of a reverse-engineering
pipeline. Your job is to reconcile all four architecture layers (Business, Data,
Application, Technology) into a single Enterprise Knowledge Graph and four
read-only foundation views.

## Rules

1. NEVER invent facts. Every node must trace to evidence in the layer outputs provided.
2. Where the same concept appears in multiple layers (e.g. "Order" in BA, DA, and AA),
   merge into ONE canonical node — do not duplicate.
3. Assign confidence: HIGH (direct code evidence), MEDIUM (inferred from patterns),
   LOW (assumed from naming), ASSUMED (no evidence found).
4. Every node must carry: id, type, owner_layer, confidence, evidence (source ref).
5. Record every cross-layer conflict in normalization_log with a DISC-### id.
6. Record every unresolved question in open_questions with an OQ-### id.
7. Assumptions that cannot be verified go in assumptions with an ASMP-### id.
8. The anti-hallucination rule: if you do not know → say unknown, not a guess.

## Required Outputs

Produce ALL of the following, in this exact order:

### 1. ENTERPRISE_KNOWLEDGE_GRAPH.json
A JSON object with these top-level sections:
  metadata, business, data, application, technology,
  cross_links, assumptions, normalization_log, open_questions

Each node: { "id": "...", "type": "...", "owner_layer": "...",
             "confidence": "HIGH|MEDIUM|LOW|ASSUMED", "evidence": "..." }

### 2. CANONICAL_ENTERPRISE_MODEL.md
A human-readable summary of every domain, aggregate, service, and API
in the system — one row per node, grouped by layer.

### 3. ARCHITECTURE_INVENTORY.md
A complete inventory: deployables, databases, APIs, services, entities,
tech stack, security findings, PII, technical debt register.

### 4. TRACEABILITY_MATRIX.md
Columns: Capability → Process → Entity/Aggregate → Service → API → Database → Confidence
One row per business capability.

### 5. FORWARD_ENGINEERING_INPUT_MAP.md
A map of what is KNOWN, what is INFERRED, and what is MISSING —
organised as the input specification for AI-assisted code regeneration.

---

After the 5 foundation documents, generate the full 20-document
Forward Engineering Package:

01_BRD.md — Business Requirements Document
02_BUSINESS_CAPABILITY_MODEL.md
03_USE_CASE_SPECIFICATION.md
04_BUSINESS_PROCESS_MODEL.md
05_DOMAIN_MODEL.md — with DDD bounded contexts and Mermaid context maps
06_DATA_DICTIONARY.md
07_DATA_MODEL_SPECIFICATION.md — including physical schema and SQL DDL
08_ERD.md
09_DATA_FLOW_DIAGRAM.md
10_SERVICE_CATALOG.md
11_API_CONTRACT_SPECIFICATION.md — full REST contracts
12_TECHNOLOGY_BLUEPRINT.md
13_SECURITY_ARCHITECTURE.md — including RBAC model and modernization plan
14_NFR_SPECIFICATION.md
15_FORWARD_ENGINEERING_SPECIFICATION.md — generation rules and validation gates
16_GENERATION_MANIFEST.json — machine-readable JSON
17_FORWARD_ENGINEERING_READINESS_REPORT.md — scored readiness assessment
18_DEPLOYMENT_ARCHITECTURE.md
19_FRONTEND_ARCHITECTURE.md
20_UI_UX_SPECIFICATION.md

Separate each document with:
=== DOCUMENT: <filename> ===

CRITICAL RULES:
- Output ALL document content as plain text in this response using the markers above.
- Do NOT use file writing tools. Do NOT write files to disk. Do NOT use any tools at all.
- Every document must appear in full in your text response — nothing else will be captured.

---
"""

# ── Forward-engineering prompt (second Claude call) ────────────────────────────

FORWARD_ENGINEERING_PROMPT = """
# Forward Engineering Package Generator

You are given the Enterprise Knowledge Graph and foundation views produced by
the Foundation Synthesis agent. Your job is to generate the complete
20-document Forward Engineering Package from this foundation.

Each document must be:
- Grounded in the Knowledge Graph — cite node IDs where relevant
- Technology-neutral where the target stack is unresolved (GR-08)
- Written at the level of a senior architect reviewing the spec
- Self-contained — a developer should be able to implement from each document alone

Produce all 20 documents now. Separate each with:
=== DOCUMENT: <filename> ===
"""


# ── Output loaders ─────────────────────────────────────────────────────────────

def _load_layer_outputs(output_dir: str) -> dict:
    """Load all agent outputs from the 4 layer output directories."""
    base = Path(output_dir)
    layers = {}

    for folder, keys in [
        ("Business_Analysis",    ["BA_Structural_Scout.md", "BA_Deep_Analyst.md"]),
        ("Data_Analysis",        ["DA_Data_Extractor.md", "DA_Data_Reviewer.md"]),
        ("Technology_Analysis",  ["TA_Stack_Scout.md", "TA_Deep_Analyst.md"]),
        ("Application_Analysis", ["AA_App_Extractor.md", "AA_Quality_Review.md"]),
    ]:
        folder_path = base / folder
        for key in keys:
            path = folder_path / key
            if path.exists():
                layers[key] = path.read_text(encoding="utf-8")
                print(f"  Loaded: {folder}/{key} ({len(layers[key])} chars)")
            else:
                print(f"  Missing (will proceed without): {folder}/{key}")
                layers[key] = ""

    return layers


def _split_documents(text: str) -> dict:
    """
    Split combined Claude output into individual documents.
    Looks for === DOCUMENT: <filename> === markers.
    """
    import re
    docs = {}
    pattern = re.compile(r"=== DOCUMENT:\s*(.+?)\s*===", re.IGNORECASE)
    parts = pattern.split(text)

    # parts alternates: [preamble, filename1, content1, filename2, content2, ...]
    i = 1
    while i < len(parts) - 1:
        filename = parts[i].strip()
        content  = parts[i + 1].strip()
        docs[filename] = content
        i += 2

    return docs


# ── Main ───────────────────────────────────────────────────────────────────────

def run(output_dir: str) -> None:
    print("\n[Foundation] Loading all layer outputs...")
    layers = _load_layer_outputs(output_dir)

    all_layer_text = "\n\n".join(
        f"## {key}\n\n{content}"
        for key, content in layers.items()
        if content
    )

    # ── Step 1: Foundation synthesis → KG + 4 views ───────────────────────────
    print("\n[Foundation] Step 1 — synthesising Enterprise Knowledge Graph...")
    foundation_prompt = (
        f"{FOUNDATION_SYNTHESIS_PROMPT}\n\n"
        f"---\n\n"
        f"# All Layer Outputs\n\n"
        f"{all_layer_text}\n\n"
        f"Produce the 5 foundation documents now, followed by all 20 forward-engineering documents."
    )

    combined_output = call_claude(foundation_prompt, label="Foundation Synthesis", timeout=3600, allow_tools=False)

    # ── Save raw combined output ───────────────────────────────────────────────
    save_output(output_dir, "Foundation_Raw_Output.md", combined_output)

    # ── Split into individual documents ───────────────────────────────────────
    print("\n[Foundation] Splitting documents...")
    docs = _split_documents(combined_output)

    foundation_dir    = Path(output_dir) / "Foundation_KnowledgeGraph"
    fwd_eng_dir       = Path(output_dir) / "ForwardEngineering_Docs"
    foundation_dir.mkdir(parents=True, exist_ok=True)
    fwd_eng_dir.mkdir(parents=True, exist_ok=True)

    # Foundation docs → foundation/
    foundation_files = {
        "ENTERPRISE_KNOWLEDGE_GRAPH.json",
        "CANONICAL_ENTERPRISE_MODEL.md",
        "ARCHITECTURE_INVENTORY.md",
        "TRACEABILITY_MATRIX.md",
        "FORWARD_ENGINEERING_INPUT_MAP.md",
    }

    saved = []
    for filename, content in docs.items():
        if filename in foundation_files or filename.endswith(".json") and "GRAPH" in filename:
            path = foundation_dir / filename
        else:
            path = fwd_eng_dir / filename

        path.write_text(content, encoding="utf-8")
        saved.append(str(path))
        print(f"  Saved → {path}")

    # If no split markers found, save everything to one file
    if not docs:
        print("  [Warning] No document markers found — saving full output as single file.")
        save_output(str(foundation_dir), "FOUNDATION_OUTPUT.md", combined_output)

    print(f"\n[Foundation] Complete — {len(saved)} documents saved.")
    print(f"  Foundation: {foundation_dir}")
    print(f"  Forward-Engineering: {fwd_eng_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Foundation Runner — synthesise all layers into Enterprise Knowledge Graph"
    )
    parser.add_argument("--output", required=True,
                        help="Root output directory containing the *_Analysis/ folders")
    args = parser.parse_args()
    run(args.output)
