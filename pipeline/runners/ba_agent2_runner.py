"""
BA Agent 2 Runner — Deep Analyst
Loads 02_BA_Agent2_DeepAnalyst.md, injects Agent 1 output + source files,
calls Claude headlessly, saves output to ba-outputs/ba_agent2_output.md.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from base_runner import (call_claude, load_layer1, read_source_files,
                         save_output, load_prior_output, output_already_exists)

PROMPT_FILE = Path(__file__).parent.parent.parent / "Prompts_Ready_To_Use" / "02_BA_Agent2_DeepAnalyst.md"
OUTPUT_FILE = "BA_Deep_Analyst.md"


def build_prompt(input_dir: str, repo_root: str, output_dir: str) -> str:
    prompt_text = PROMPT_FILE.read_text(encoding="utf-8")

    agent1_output = load_prior_output(output_dir, "BA_Structural_Scout.md")
    if not agent1_output:
        raise RuntimeError("BA Agent 1 output not found — run BA Agent 1 first.")

    layer1 = load_layer1(input_dir)

    # Agent 2 reads deep into method bodies — provide fuller content
    source = layer1.get("source_code", [])
    business = [
        {
            "name":     a.get("name"),
            "type":     a.get("type"),
            "file":     a.get("source_file"),
            "content":  a.get("content", "")[:3000],
            "category": a.get("business_category"),
        }
        for a in source if a.get("is_business_artifact")
    ][:80]

    src_files = read_source_files(repo_root, extensions=(".cs",), max_files=80,
                                  max_bytes_per_file=8000) if repo_root else []

    context = {
        "agent1_inventory": agent1_output,
        "business_artifacts_with_bodies": business,
        "config": {
            "business_params": layer1.get("config", {}).get("business_params", [])[:60],
        },
        "source_files": src_files,
    }

    data_block = json.dumps(context, indent=2, ensure_ascii=False)
    return (
        f"{prompt_text}\n\n"
        f"---\n\n"
        f"# Input: Agent 1 Inventory + Full Source Data\n\n"
        f"```json\n{data_block}\n```\n\n"
        f"Agent 1 has completed its scan. Begin deep analysis now using the inventory above."
    )


def run(input_dir: str, repo_root: str, output_dir: str) -> str:
    if output_already_exists(output_dir, OUTPUT_FILE):
        print(f"\n[BA Agent 2] Already done — skipping (found {OUTPUT_FILE})")
        return load_prior_output(output_dir, OUTPUT_FILE)
    print("\n[BA Agent 2] Deep Analyst — starting...")
    prompt = build_prompt(input_dir, repo_root, output_dir)
    output = call_claude(prompt, label="BA Agent 2", timeout=1800)
    save_output(output_dir, OUTPUT_FILE, output)
    print("[BA Agent 2] Complete.")
    return output


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--input",     required=True)
    p.add_argument("--repo-root", default="")
    p.add_argument("--output",    required=True)
    args = p.parse_args()
    run(args.input, args.repo_root, args.output)
