"""
Base runner — shared Claude CLI invocation, Layer 1 loading, and output helpers.
All 8 prompt runners import from here.
"""

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ── Claude CLI ─────────────────────────────────────────────────────────────────

def claude_cmd(allow_tools: bool = True) -> list:
    """Return base claude CLI command. Headless, no session persistence."""
    if sys.platform == "win32":
        base = ["cmd", "/c", "claude", "-p", "--output-format", "text", "--no-session-persistence"]
        if allow_tools:
            base += ["--permission-mode", "acceptEdits"]
        return base
    found = shutil.which("claude")
    if not found:
        raise FileNotFoundError("claude CLI not found. Install: npm install -g @anthropic/claude-code")
    base = [found, "-p", "--output-format", "text", "--no-session-persistence"]
    if allow_tools:
        base += ["--permission-mode", "acceptEdits"]
    return base


def call_claude(prompt: str, label: str, timeout: int = 1800, allow_tools: bool = True,
                max_retries: int = 3, retry_wait: int = 30) -> str:
    """
    Call claude -p with prompt on stdin. Returns the output text.
    Retries up to max_retries times on failure, waiting retry_wait seconds between attempts.
    Raises RuntimeError if all attempts fail.
    """
    cmd = claude_cmd(allow_tools=allow_tools)
    last_error = None

    for attempt in range(1, max_retries + 1):
        if attempt > 1:
            print(f"  [{label}] retry {attempt}/{max_retries} (waiting {retry_wait}s)...")
            time.sleep(retry_wait)
        else:
            print(f"  [{label}] calling Claude CLI...")

        try:
            proc = subprocess.run(
                cmd,
                input=prompt,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            last_error = f"[{label}] Claude call timed out after {timeout}s"
            print(f"  [{label}] attempt {attempt} timed out — {'retrying' if attempt < max_retries else 'giving up'}.")
            continue
        except Exception as exc:
            last_error = f"[{label}] Claude call failed: {exc}"
            print(f"  [{label}] attempt {attempt} error: {exc} — {'retrying' if attempt < max_retries else 'giving up'}.")
            continue

        if proc.returncode != 0:
            stderr = (proc.stderr or "")[:600].strip()
            last_error = f"[{label}] Claude exited {proc.returncode}: {stderr}"
            print(f"  [{label}] attempt {attempt} non-zero exit ({proc.returncode}) — {'retrying' if attempt < max_retries else 'giving up'}.")
            continue

        return proc.stdout or ""

    raise RuntimeError(last_error or f"[{label}] all {max_retries} attempts failed.")


# ── Layer 1 output loader ──────────────────────────────────────────────────────

def load_layer1(input_dir: str) -> dict:
    """Load all Layer 1 JSON artifacts from input_dir."""
    base = Path(input_dir)

    def read(filename):
        path = base / filename
        if path.exists():
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        return {}

    return {
        "source_code": read("Source_Code.json"),
        "database":    read("Database.json"),
        "config":      read("Config.json"),
        "logs":        read("Logs.json"),
        "summary":     read("Extraction_Summary.json"),
    }


# ── Source file reader (for prompts that want raw source) ──────────────────────

def read_source_files(repo_root: str, extensions: tuple = (".cs", ".json", ".yml", ".yaml"),
                      max_files: int = 120, max_bytes_per_file: int = 8000) -> list:
    """
    Walk repo_root and return a list of {path, content} dicts for source files.
    Skips bin/, obj/, node_modules/, .git/, wwwroot/lib/, migrations (large ones).
    """
    skip_dirs = {"bin", "obj", "node_modules", ".git", "wwwroot", "packages",
                 "TestResults", ".vs", "Properties"}
    files = []
    root = Path(repo_root)

    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        # skip excluded dirs
        if any(part in skip_dirs for part in p.parts):
            continue
        if p.suffix.lower() not in extensions:
            continue
        try:
            content = p.read_text(encoding="utf-8", errors="replace")
            if len(content) > max_bytes_per_file:
                content = content[:max_bytes_per_file] + "\n... [truncated]"
            files.append({"path": str(p.relative_to(root)), "content": content})
        except Exception:
            continue
        if len(files) >= max_files:
            break

    return files


# ── Output helpers ─────────────────────────────────────────────────────────────

def save_output(output_dir: str, filename: str, content: str) -> Path:
    """Save text content to output_dir/filename. Creates dirs if needed."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / filename
    path.write_text(content, encoding="utf-8")
    print(f"  Saved → {path}")
    return path


def save_json(output_dir: str, filename: str, data: dict) -> Path:
    """Save dict as JSON to output_dir/filename."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  Saved → {path}")
    return path


def load_prior_output(output_dir: str, filename: str) -> str:
    """Load a prior agent's output file as text. Returns empty string if missing."""
    path = Path(output_dir) / filename
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def output_already_exists(output_dir: str, filename: str) -> bool:
    """Return True if the output file already exists and is non-empty.
    Used to skip steps that completed in a previous run (resume logic)."""
    path = Path(output_dir) / filename
    return path.exists() and path.stat().st_size > 0
