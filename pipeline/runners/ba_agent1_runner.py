"""
BA Agent 1 Runner — Structural Scout
Loads 01_BA_Agent1_StructuralScout.md, injects Layer 1 JSON + source files,
calls Claude headlessly, saves output to ba-outputs/ba_agent1_output.md.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from base_runner import (call_claude, load_layer1, read_source_files,
                         save_output, load_prior_output)

PROMPT_FILE = Path(__file__).parent.parent.parent / "prompts-ready-to-use" / "01_BA_Agent1_StructuralScout.md"
OUTPUT_FILE = "ba_agent1_output.md"


def build_prompt(input_dir: str, repo_root: str) -> str:
    prompt_text = PROMPT_FILE.read_text(encoding="utf-8")

    layer1 = load_layer1(input_dir)

    # Select business artifacts from source_code
    source = layer1.get("source_code", [])
    business = [
        {
            "name":     a.get("name"),
            "type":     a.get("type"),
            "file":     a.get("source_file"),
            "content":  a.get("content", "")[:1200],
            "category": a.get("business_category"),
            "metadata": a.get("metadata", {}),
        }
        for a in source if a.get("is_business_artifact")
    ][:100]

    structural = [
        {"name": a.get("name"), "type": a.get("type"), "file": a.get("source_file")}
        for a in source if not a.get("is_business_artifact")
        and a.get("type") in ("class", "interface", "enum")
    ][:50]

    # Raw source files for deeper reading
    src_files = read_source_files(repo_root, extensions=(".cs",), max_files=80,
                                  max_bytes_per_file=6000) if repo_root else []

    context = {
        "extraction_summary": layer1.get("summary", {}),
        "business_artifacts": business,
        "structural_types":   structural,
        "database":           {
            "tables":      layer1.get("database", {}).get("tables", [])[:30],
            "ef_entities": layer1.get("database", {}).get("ef_entities", [])[:30],
        },
        "config": {
            "business_params":  layer1.get("config", {}).get("business_params", [])[:50],
            "feature_flags":    layer1.get("config", {}).get("feature_flags", [])[:20],
            "role_definitions": layer1.get("config", {}).get("role_definitions", [])[:20],
        },
        "source_files": src_files,
    }

    data_block = json.dumps(context, indent=2, ensure_ascii=False)
    return (
        f"{prompt_text}\n\n"
        f"---\n\n"
        f"# Codebase Data (Layer 1 extraction + raw source)\n\n"
        f"```json\n{data_block}\n```\n\n"
        f"Begin Chunk 0 now."
    )


def run(input_dir: str, repo_root: str, output_dir: str) -> str:
    print("\n[BA Agent 1] Structural Scout — starting...")
    prompt = build_prompt(input_dir, repo_root)
    output = call_claude(prompt, label="BA Agent 1", timeout=1800)
    save_output(output_dir, OUTPUT_FILE, output)
    print("[BA Agent 1] Complete.")
    return output


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--input",     required=True)
    p.add_argument("--repo-root", default="")
    p.add_argument("--output",    required=True)
    args = p.parse_args()
    run(args.input, args.repo_root, args.output)
