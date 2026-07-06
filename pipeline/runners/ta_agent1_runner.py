"""
TA Agent 1 Runner — Stack Scout
Loads 05_TA_Agent1_StackScout.md, injects config/infra/dependency files + Layer 1,
calls Claude headlessly, saves output to ta-outputs/ta_agent1_output.md.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from base_runner import (call_claude, load_layer1, read_source_files,
                         save_output)

PROMPT_FILE = Path(__file__).parent.parent.parent / "prompts-ready-to-use" / "05_TA_Agent1_StackScout.md"
OUTPUT_FILE = "ta_agent1_output.md"


def build_prompt(input_dir: str, repo_root: str) -> str:
    prompt_text = PROMPT_FILE.read_text(encoding="utf-8")

    layer1 = load_layer1(input_dir)
    cfg    = layer1.get("config", {})

    # TA Agent 1 cares about config, infra, CI/CD, dependency manifests
    infra_files = read_source_files(
        repo_root,
        extensions=(".json", ".yml", ".yaml", ".bicep", ".dockerfile",
                    ".csproj", ".props", ".sln"),
        max_files=60,
        max_bytes_per_file=6000,
    ) if repo_root else []

    # Also grab key .cs files for framework/DI wiring
    cs_infra = read_source_files(
        repo_root,
        extensions=(".cs",),
        max_files=30,
        max_bytes_per_file=4000,
    ) if repo_root else []
    cs_infra = [
        f for f in cs_infra
        if any(kw in f["path"].lower() for kw in
               ["startup", "program", "extension", "config", "middleware",
                "infra", "docker", "deploy"])
    ][:20]

    context = {
        "extraction_summary": layer1.get("summary", {}),
        "config": {
            "all_params":         cfg.get("all_params", [])[:60],
            "connection_strings": cfg.get("connection_strings", []),
            "feature_flags":      cfg.get("feature_flags", []),
        },
        "infra_and_config_files": infra_files,
        "framework_wiring_files": cs_infra,
    }

    data_block = json.dumps(context, indent=2, ensure_ascii=False)
    return (
        f"{prompt_text}\n\n"
        f"---\n\n"
        f"# Codebase Data (Layer 1 config + infra/config source files)\n\n"
        f"```json\n{data_block}\n```\n\n"
        f"Begin technology stack scan now. Map all components — no interpretation yet."
    )


def run(input_dir: str, repo_root: str, output_dir: str) -> str:
    print("\n[TA Agent 1] Stack Scout — starting...")
    prompt = build_prompt(input_dir, repo_root)
    output = call_claude(prompt, label="TA Agent 1", timeout=1800)
    save_output(output_dir, OUTPUT_FILE, output)
    print("[TA Agent 1] Complete.")
    return output


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--input",     required=True)
    p.add_argument("--repo-root", default="")
    p.add_argument("--output",    required=True)
    args = p.parse_args()
    run(args.input, args.repo_root, args.output)
