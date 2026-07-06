"""
AA Agent 2 Runner — Quality Review
Loads 08_AA_Agent2_QualityReview.md, injects AA Agent 1 output,
calls Claude headlessly, saves output to aa-outputs/aa_agent2_output.md.
Produces PASS / PARTIAL / FAIL verdict.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from base_runner import (call_claude, save_output, load_prior_output)

PROMPT_FILE = Path(__file__).parent.parent.parent / "prompts-ready-to-use" / "08_AA_Agent2_QualityReview.md"
OUTPUT_FILE = "aa_agent2_output.md"


def build_prompt(output_dir: str) -> str:
    prompt_text = PROMPT_FILE.read_text(encoding="utf-8")

    agent1_output = load_prior_output(output_dir, "aa_agent1_output.md")
    if not agent1_output:
        raise RuntimeError("AA Agent 1 output not found — run AA Agent 1 first.")

    return (
        f"{prompt_text}\n\n"
        f"---\n\n"
        f"# Input: AA Agent 1 Full Output\n\n"
        f"{agent1_output}\n\n"
        f"Review the above output now. "
        f"Validate JSON, graph edges, evidence traceability, and completeness. "
        f"Produce your PASS / PARTIAL / FAIL verdict with specific findings."
    )


def run(input_dir: str, repo_root: str, output_dir: str) -> str:
    print("\n[AA Agent 2] Quality Review — starting...")
    prompt = build_prompt(output_dir)
    output = call_claude(prompt, label="AA Agent 2", timeout=1800)
    save_output(output_dir, OUTPUT_FILE, output)
    print("[AA Agent 2] Complete.")
    return output


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--input",     required=True)
    p.add_argument("--repo-root", default="")
    p.add_argument("--output",    required=True)
    args = p.parse_args()
    run(args.input, args.repo_root, args.output)
