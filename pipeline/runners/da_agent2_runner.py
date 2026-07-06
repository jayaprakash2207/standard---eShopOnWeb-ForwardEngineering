"""
DA Agent 2 Runner — Data Reviewer
Loads 04_DA_Agent2_DataReviewer.md, injects DA Agent 1 output,
calls Claude headlessly, saves output to da-outputs/da_agent2_output.md.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from base_runner import (call_claude, load_layer1, read_source_files,
                         save_output, load_prior_output)

PROMPT_FILE = Path(__file__).parent.parent.parent / "prompts-ready-to-use" / "04_DA_Agent2_DataReviewer.md"
OUTPUT_FILE = "da_agent2_output.md"


def build_prompt(input_dir: str, repo_root: str, output_dir: str) -> str:
    prompt_text = PROMPT_FILE.read_text(encoding="utf-8")

    agent1_output = load_prior_output(output_dir, "da_agent1_output.md")
    if not agent1_output:
        raise RuntimeError("DA Agent 1 output not found — run DA Agent 1 first.")

    layer1 = load_layer1(input_dir)

    src_files = read_source_files(
        repo_root,
        extensions=(".cs",),
        max_files=60,
        max_bytes_per_file=6000,
    ) if repo_root else []

    context = {
        "da_agent1_output":  agent1_output,
        "database":          layer1.get("database", {}),
        "source_files":      src_files,
    }

    data_block = json.dumps(context, indent=2, ensure_ascii=False)
    return (
        f"{prompt_text}\n\n"
        f"---\n\n"
        f"# Input: DA Agent 1 Output + Source Evidence\n\n"
        f"```json\n{data_block}\n```\n\n"
        f"Review DA Agent 1's findings now. Validate, enrich, and produce the Gate G1 verdict."
    )


def run(input_dir: str, repo_root: str, output_dir: str) -> str:
    print("\n[DA Agent 2] Data Reviewer — starting...")
    prompt = build_prompt(input_dir, repo_root, output_dir)
    output = call_claude(prompt, label="DA Agent 2", timeout=1800)
    save_output(output_dir, OUTPUT_FILE, output)
    print("[DA Agent 2] Complete.")
    return output


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--input",     required=True)
    p.add_argument("--repo-root", default="")
    p.add_argument("--output",    required=True)
    args = p.parse_args()
    run(args.input, args.repo_root, args.output)
