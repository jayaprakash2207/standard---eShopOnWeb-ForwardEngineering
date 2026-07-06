"""
AA Agent 1 Runner — Application Extractor
Loads 07_AA_Agent1_AppExtractor.md, injects full source + Layer 1 application artifacts,
calls Claude headlessly, saves output to aa-outputs/aa_agent1_output.md.

NOTE: Repo A's AA layer uses Claude (not pure Python like Repo B).
This is a quality advantage — Claude reads call chains, violations, and DI wiring
that static Python analysis misses.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from base_runner import (call_claude, load_layer1, read_source_files,
                         save_output)

PROMPT_FILE = Path(__file__).parent.parent.parent / "prompts-ready-to-use" / "07_AA_Agent1_AppExtractor.md"
OUTPUT_FILE = "aa_agent1_output.md"


def build_prompt(input_dir: str, repo_root: str) -> str:
    prompt_text = PROMPT_FILE.read_text(encoding="utf-8")

    layer1 = load_layer1(input_dir)
    source = layer1.get("source_code", [])

    # AA cares about services, interfaces, controllers, endpoints, DI wiring
    app_artifacts = [
        {
            "name":     a.get("name"),
            "type":     a.get("type"),
            "file":     a.get("source_file"),
            "content":  a.get("content", "")[:3000],
            "category": a.get("business_category"),
        }
        for a in source
    ][:120]

    # Source files — focus on services, controllers, endpoints, startup
    all_src = read_source_files(
        repo_root,
        extensions=(".cs",),
        max_files=120,
        max_bytes_per_file=8000,
    ) if repo_root else []

    service_files = [
        f for f in all_src
        if any(kw in f["path"].lower() for kw in
               ["service", "controller", "endpoint", "handler", "mediator",
                "program", "startup", "interface", "reposit"])
    ][:80]
    other_files = [f for f in all_src if f not in service_files][:(120 - len(service_files))]

    context = {
        "extraction_summary":  layer1.get("summary", {}),
        "all_artifacts":       app_artifacts,
        "database":            layer1.get("database", {}),
        "config":              layer1.get("config", {}),
        "service_source_files": service_files,
        "other_source_files":   other_files,
    }

    data_block = json.dumps(context, indent=2, ensure_ascii=False)
    return (
        f"{prompt_text}\n\n"
        f"---\n\n"
        f"# Codebase Data (full source artifacts + Layer 1 output)\n\n"
        f"```json\n{data_block}\n```\n\n"
        f"Begin application architecture extraction now. "
        f"Run all 6 internal phases: inventory → parse → evidence → final → forward-engineering → security."
    )


def run(input_dir: str, repo_root: str, output_dir: str) -> str:
    print("\n[AA Agent 1] App Extractor — starting (6 internal phases)...")
    prompt = build_prompt(input_dir, repo_root)
    output = call_claude(prompt, label="AA Agent 1", timeout=2400)
    save_output(output_dir, OUTPUT_FILE, output)
    print("[AA Agent 1] Complete.")
    return output


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--input",     required=True)
    p.add_argument("--repo-root", default="")
    p.add_argument("--output",    required=True)
    args = p.parse_args()
    run(args.input, args.repo_root, args.output)
