"""
TA Agent 2 Runner — Deep Analyst
Loads 06_TA_Agent2_DeepAnalyst.md, injects TA Agent 1 output + source,
calls Claude headlessly, saves output to ta-outputs/ta_agent2_output.md.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from base_runner import (call_claude, load_layer1, read_source_files,
                         save_output, load_prior_output)

PROMPT_FILE = Path(__file__).parent.parent.parent / "Prompts_Ready_To_Use" / "06_TA_Agent2_DeepAnalyst.md"
OUTPUT_FILE = "TA_Deep_Analyst.md"


def build_prompt(input_dir: str, repo_root: str, output_dir: str) -> str:
    prompt_text = PROMPT_FILE.read_text(encoding="utf-8")

    agent1_output = load_prior_output(output_dir, "TA_Stack_Scout.md")
    if not agent1_output:
        raise RuntimeError("TA Agent 1 output not found — run TA Agent 1 first.")

    layer1 = load_layer1(input_dir)

    # Security and infra deep-read files
    src_files = read_source_files(
        repo_root,
        extensions=(".cs", ".json", ".yml", ".yaml"),
        max_files=60,
        max_bytes_per_file=6000,
    ) if repo_root else []

    context = {
        "ta_agent1_inventory": agent1_output,
        "config":              layer1.get("config", {}),
        "source_files":        src_files,
    }

    data_block = json.dumps(context, indent=2, ensure_ascii=False)
    return (
        f"{prompt_text}\n\n"
        f"---\n\n"
        f"# Input: TA Agent 1 Inventory + Source Evidence\n\n"
        f"```json\n{data_block}\n```\n\n"
        f"TA Agent 1 scan is complete. Begin deep technology analysis now — "
        f"patterns, risks, NFRs, security, tech debt."
    )


def run(input_dir: str, repo_root: str, output_dir: str) -> str:
    print("\n[TA Agent 2] Deep Analyst — starting...")
    prompt = build_prompt(input_dir, repo_root, output_dir)
    output = call_claude(prompt, label="TA Agent 2", timeout=1800)
    save_output(output_dir, OUTPUT_FILE, output)
    print("[TA Agent 2] Complete.")
    return output


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--input",     required=True)
    p.add_argument("--repo-root", default="")
    p.add_argument("--output",    required=True)
    args = p.parse_args()
    run(args.input, args.repo_root, args.output)
