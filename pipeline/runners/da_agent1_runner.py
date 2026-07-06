"""
DA Agent 1 Runner — Data Extractor
Loads 03_DA_Agent1_DataExtractor.md, injects Layer 1 DB/schema artifacts + source,
calls Claude headlessly, saves output to da-outputs/da_agent1_output.md.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from base_runner import (call_claude, load_layer1, read_source_files,
                         save_output)

PROMPT_FILE = Path(__file__).parent.parent.parent / "prompts-ready-to-use" / "03_DA_Agent1_DataExtractor.md"
OUTPUT_FILE = "da_agent1_output.md"


def build_prompt(input_dir: str, repo_root: str) -> str:
    prompt_text = PROMPT_FILE.read_text(encoding="utf-8")

    layer1 = load_layer1(input_dir)
    db     = layer1.get("database", {})
    cfg    = layer1.get("config", {})
    source = layer1.get("source_code", [])

    # Entity and DB focused artifacts
    entities = [
        {
            "name":    a.get("name"),
            "type":    a.get("type"),
            "file":    a.get("source_file"),
            "content": a.get("content", "")[:3000],
        }
        for a in source
        if a.get("type") in ("class", "interface") and a.get("is_business_artifact")
    ][:60]

    # Source files — focus on entity, migration, repository, context files
    src_files = read_source_files(
        repo_root,
        extensions=(".cs",),
        max_files=80,
        max_bytes_per_file=8000,
    ) if repo_root else []

    # Filter to data-relevant files
    data_files = [
        f for f in src_files
        if any(kw in f["path"].lower() for kw in
               ["entit", "migrat", "context", "reposit", "model", "schema", "aggregat"])
    ][:50]
    # Fill remaining slots with other source files
    other_files = [f for f in src_files if f not in data_files][:(80 - len(data_files))]

    context = {
        "extraction_summary": layer1.get("summary", {}),
        "database": {
            "tables":            db.get("tables", []),
            "ef_entities":       db.get("ef_entities", []),
            "stored_procedures": db.get("stored_procedures", []),
            "triggers":          db.get("triggers", []),
            "views":             db.get("views", []),
        },
        "config": {
            "connection_strings": cfg.get("connection_strings", []),
            "business_params":    cfg.get("business_params", [])[:40],
        },
        "entity_artifacts": entities,
        "data_focused_source_files": data_files,
        "other_source_files":        other_files,
    }

    data_block = json.dumps(context, indent=2, ensure_ascii=False)
    return (
        f"{prompt_text}\n\n"
        f"---\n\n"
        f"# Codebase Data (Layer 1 DB extraction + source files)\n\n"
        f"```json\n{data_block}\n```\n\n"
        f"Begin full data architecture extraction now."
    )


def run(input_dir: str, repo_root: str, output_dir: str) -> str:
    print("\n[DA Agent 1] Data Extractor — starting...")
    prompt = build_prompt(input_dir, repo_root)
    output = call_claude(prompt, label="DA Agent 1", timeout=1800)
    save_output(output_dir, OUTPUT_FILE, output)
    print("[DA Agent 1] Complete.")
    return output


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--input",     required=True)
    p.add_argument("--repo-root", default="")
    p.add_argument("--output",    required=True)
    args = p.parse_args()
    run(args.input, args.repo_root, args.output)
