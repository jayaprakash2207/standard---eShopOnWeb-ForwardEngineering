"""
Standard Forward Engineering Pipeline — Master Orchestrator
============================================================
Automates Repo A's 8 manual prompts end-to-end with the same quality
as the manual approach, but zero human intervention required.

Pipeline sequence:
  Step 1  — Layer 1  (deterministic AST extraction, no LLM)
  Step 2  — BA Agent 1 (Structural Scout)
  Step 3  — BA Agent 2 (Deep Analyst)          ← runs after Step 2
  Steps 4-7 run in 3 PARALLEL threads:
    Thread 1: DA Agent 1 → DA Agent 2          (sequential within thread)
    Thread 2: TA Agent 1 → TA Agent 2          (sequential within thread)
    Thread 3: AA Agent 1 → AA Agent 2          (sequential within thread)
  Step 8  — Foundation (Knowledge Graph Synthesis + 20 FE documents)

Usage:
  python run.py --source "https://github.com/org/repo" --output ./results
  python run.py --source "C:/path/to/local/repo"       --output ./results
  python run.py --source "C:/path/to/repo"             --output ./results --skip-layer1

Output structure:
  <output>/Source_Extraction/         — Layer 1 JSON artifacts
  <output>/Business_Analysis/         — BA Agent 1 + 2 outputs
  <output>/Data_Analysis/             — DA Agent 1 + 2 outputs
  <output>/Technology_Analysis/       — TA Agent 1 + 2 outputs
  <output>/Application_Analysis/      — AA Agent 1 + 2 outputs
  <output>/Foundation_KnowledgeGraph/ — Enterprise Knowledge Graph + 4 views
  <output>/ForwardEngineering_Docs/   — 20 forward-engineering documents
"""

import argparse
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR   = Path(__file__).parent.resolve()
PIPELINE_DIR = SCRIPT_DIR / "pipeline"
RUNNERS_DIR  = PIPELINE_DIR / "runners"

# ── ANSI colours ───────────────────────────────────────────────────────────────
_USE_COLOR = sys.stdout.isatty()

def _c(code, text): return f"\033[{code}m{text}\033[0m" if _USE_COLOR else text
def green(t):  return _c("32", t)
def yellow(t): return _c("33", t)
def red(t):    return _c("31", t)
def bold(t):   return _c("1",  t)
def cyan(t):   return _c("36", t)
def dim(t):    return _c("2",  t)


# ── Step banner ────────────────────────────────────────────────────────────────

_TOTAL_STEPS = 8

def _banner(step, label):
    print(f"\n{'─' * 64}")
    print(bold(cyan(f"[STEP {step}/{_TOTAL_STEPS}]  {label}")))
    print(f"{'─' * 64}")


# ── Subprocess runner ──────────────────────────────────────────────────────────

def _run(cmd: list, label: str, timeout: int = 3600, cwd: str = None) -> dict:
    t0 = time.monotonic()
    cmd_str = " ".join(str(c) for c in cmd)
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            check=False, timeout=timeout, cwd=cwd,
        )
        return {
            "label":      label,
            "returncode": proc.returncode,
            "stdout":     proc.stdout or "",
            "stderr":     proc.stderr or "",
            "duration_s": time.monotonic() - t0,
        }
    except subprocess.TimeoutExpired:
        return {"label": label, "returncode": -1, "stdout": "",
                "stderr": f"Timed out after {timeout}s", "duration_s": time.monotonic() - t0}
    except Exception as exc:
        return {"label": label, "returncode": -1, "stdout": "",
                "stderr": str(exc), "duration_s": time.monotonic() - t0}


def _print_result(r: dict):
    ok  = r["returncode"] == 0
    dur = f"{r['duration_s']:.1f}s"
    sep = "=" * 64
    status = green("COMPLETE") if ok else red("FAILED")
    print(f"\n{sep}")
    print(f"{bold(r['label'])} — {status}  {dim('(' + dur + ')')}")
    print(sep)
    if r["stdout"].strip():
        for line in r["stdout"].rstrip().splitlines():
            print(f"  {line}")
    if not ok and r["stderr"].strip():
        print(f"\n  {red('[stderr]')} {r['stderr'][:600].strip()}")
    print()


def _run_or_exit(cmd: list, label: str, timeout: int = 3600, cwd: str = None) -> dict:
    r = _run(cmd, label, timeout, cwd=cwd)
    _print_result(r)
    if r["returncode"] != 0:
        print(red(f"\nPIPELINE STOPPED — {label} failed. Fix the issue and re-run."))
        sys.exit(1)
    return r


# ── Input resolver ─────────────────────────────────────────────────────────────

def _is_url(source: str) -> bool:
    s = source.lower()
    return s.startswith("http://") or s.startswith("https://") or s.startswith("git@")


def clone_repo(url: str, output_dir: Path) -> str:
    clone_dir = output_dir / "repo-clone" / "repo"
    clone_dir.parent.mkdir(parents=True, exist_ok=True)
    print(f"  Cloning {url} → {clone_dir}")
    r = _run(["git", "clone", "--depth", "1", url, str(clone_dir)],
             label="git clone", timeout=600)
    _print_result(r)
    if r["returncode"] != 0:
        raise RuntimeError(f"Clone failed: {r['stderr'][:400]}")
    return str(clone_dir)


# ── Individual steps ───────────────────────────────────────────────────────────

py = sys.executable


def step_layer1(source: str, pipeline_out: Path) -> dict:
    pipeline_out.mkdir(parents=True, exist_ok=True)
    return _run_or_exit(
        [py, "-m", "layer1",
         "--source", source, "--output", str(pipeline_out)],
        label="[STEP 1/8] Layer 1 — Source Extraction",
        cwd=str(PIPELINE_DIR),
    )


def step_ba1(pipeline_out: Path, repo_root: str, ba_out: Path) -> dict:
    return _run_or_exit(
        [py, str(RUNNERS_DIR / "ba_agent1_runner.py"),
         "--input", str(pipeline_out), "--repo-root", repo_root,
         "--output", str(ba_out)],
        label="[STEP 2/8] BA Agent 1 — Structural Scout",
    )


def step_ba2(pipeline_out: Path, repo_root: str, ba_out: Path) -> dict:
    return _run_or_exit(
        [py, str(RUNNERS_DIR / "ba_agent2_runner.py"),
         "--input", str(pipeline_out), "--repo-root", repo_root,
         "--output", str(ba_out)],
        label="[STEP 3/8] BA Agent 2 — Deep Analyst",
    )


# ── Parallel track runners ─────────────────────────────────────────────────────

def _da_track(pipeline_out, repo_root, da_out, results, lock):
    for runner, label in [
        ("da_agent1_runner.py", "[STEP 4/8] DA Agent 1 — Data Extractor"),
        ("da_agent2_runner.py", "[STEP 5/8] DA Agent 2 — Data Reviewer"),
    ]:
        r = _run(
            [py, str(RUNNERS_DIR / runner),
             "--input", str(pipeline_out), "--repo-root", repo_root,
             "--output", str(da_out)],
            label=label,
        )
        with lock:
            results.append(r)
            _print_result(r)


def _ta_track(pipeline_out, repo_root, ta_out, results, lock):
    for runner, label in [
        ("ta_agent1_runner.py", "[STEP 4/8] TA Agent 1 — Stack Scout"),
        ("ta_agent2_runner.py", "[STEP 5/8] TA Agent 2 — Deep Analyst"),
    ]:
        r = _run(
            [py, str(RUNNERS_DIR / runner),
             "--input", str(pipeline_out), "--repo-root", repo_root,
             "--output", str(ta_out)],
            label=label,
        )
        with lock:
            results.append(r)
            _print_result(r)


def _aa_track(pipeline_out, repo_root, aa_out, results, lock):
    for runner, label in [
        ("aa_agent1_runner.py", "[STEP 4/8] AA Agent 1 — App Extractor"),
        ("aa_agent2_runner.py", "[STEP 5/8] AA Agent 2 — Quality Review"),
    ]:
        r = _run(
            [py, str(RUNNERS_DIR / runner),
             "--input", str(pipeline_out), "--repo-root", repo_root,
             "--output", str(aa_out)],
            label=label,
        )
        with lock:
            results.append(r)
            _print_result(r)


def run_parallel_tracks(pipeline_out, repo_root, output_dir) -> list:
    da_out = output_dir / "Data_Analysis"
    ta_out = output_dir / "Technology_Analysis"
    aa_out = output_dir / "Application_Analysis"
    for d in (da_out, ta_out, aa_out):
        d.mkdir(parents=True, exist_ok=True)

    results = []
    lock    = threading.Lock()

    print(f"\n{bold(yellow('Starting parallel tracks: DA + TA + AA'))}")
    print(dim("  DA: Data Extractor → Data Reviewer       (thread 1)"))
    print(dim("  TA: Stack Scout    → Deep Analyst        (thread 2)"))
    print(dim("  AA: App Extractor  → Quality Review      (thread 3)"))

    threads = [
        threading.Thread(target=_da_track, args=(pipeline_out, repo_root, da_out, results, lock)),
        threading.Thread(target=_ta_track, args=(pipeline_out, repo_root, ta_out, results, lock)),
        threading.Thread(target=_aa_track, args=(pipeline_out, repo_root, aa_out, results, lock)),
    ]
    t0 = time.monotonic()
    for t in threads: t.start()
    for t in threads: t.join()
    print(dim(f"\nAll parallel tracks finished in {time.monotonic() - t0:.1f}s"))
    return results


def step_foundation(output_dir: Path) -> dict:
    return _run_or_exit(
        [py, str(PIPELINE_DIR / "foundation_runner.py"),
         "--output", str(output_dir)],
        label="[STEP 8/8] Foundation — Knowledge Graph + 20 Documents",
        timeout=3600,
    )


# ── Final summary ──────────────────────────────────────────────────────────────

def _count(path: Path) -> int:
    return sum(1 for _ in path.rglob("*") if _.is_file()) if path.exists() else 0


def print_summary(output_dir: Path, all_results: list, total_s: float):
    sep = "═" * 64
    print(f"\n{sep}")
    print(bold(green("STANDARD FORWARD ENGINEERING PIPELINE — COMPLETE")))
    print(sep)

    print(f"\n{bold('Step results:')}")
    for r in all_results:
        icon = green("OK  ") if r["returncode"] == 0 else red("FAIL")
        dur = f"({r['duration_s']:.1f}s)"
        print(f"  {icon}  {r['label']}  {dim(dur)}")

    print(f"\n{bold('Output folders:')}")
    for label, folder in [
        ("Business Analysis",    output_dir / "Business_Analysis"),
        ("Data Analysis",        output_dir / "Data_Analysis"),
        ("Technology Analysis",  output_dir / "Technology_Analysis"),
        ("Application Analysis", output_dir / "Application_Analysis"),
        ("Foundation / KG",      output_dir / "Foundation_KnowledgeGraph"),
        ("Forward Engineering",  output_dir / "ForwardEngineering_Docs"),
    ]:
        n = _count(folder)
        status = green(f"{n:>3} files") if n > 0 else dim("  —  not created")
        print(f"  {status}  {label:<24}  {dim(str(folder))}")

    mins, secs = int(total_s // 60), int(total_s % 60)
    print(f"\n  Total wall time: {bold(f'{mins}m {secs}s')}")
    print(f"\n{bold('Output root:')}  {output_dir}")
    print(sep + "\n")


# ── Main orchestrator ──────────────────────────────────────────────────────────

def orchestrate(source: str, output_dir: Path, skip_layer1: bool) -> int:
    output_dir   = output_dir.resolve()
    pipeline_out = output_dir / "Source_Extraction"
    ba_out       = output_dir / "Business_Analysis"
    output_dir.mkdir(parents=True, exist_ok=True)
    # Resolve source to absolute path so Layer 1 InputResolver accepts it
    if not _is_url(source):
        source = str(Path(source).resolve())

    all_results = []
    t0 = time.monotonic()

    print(f"\n{'═' * 64}")
    print(bold(cyan("STANDARD FORWARD ENGINEERING PIPELINE")))
    print(f"{'═' * 64}")
    print(f"  Source      : {source}")
    print(f"  Output root : {output_dir}")
    print(f"  Skip Layer1 : {skip_layer1}")
    print(f"{'═' * 64}\n")

    # ── Resolve local repo path ───────────────────────────────────────────────
    repo_root = source
    if _is_url(source):
        print(bold("Cloning remote repository..."))
        try:
            repo_root = clone_repo(source, output_dir)
            print(green(f"  Local repo: {repo_root}\n"))
        except RuntimeError as exc:
            print(red(f"  Clone failed: {exc}"))
            repo_root = ""

    # ── Step 1: Layer 1 ───────────────────────────────────────────────────────
    _banner(1, "Layer 1 — Deterministic Source Extraction")
    if skip_layer1:
        print(yellow("  Skipped (--skip-layer1)\n"))
        all_results.append({"label": "[STEP 1/8] Layer 1", "returncode": 0,
                             "stdout": "skipped", "stderr": "", "duration_s": 0.0})
    else:
        r = step_layer1(repo_root or source, pipeline_out)
        all_results.append(r)

    # ── Step 2: BA Agent 1 ────────────────────────────────────────────────────
    _banner(2, "BA Agent 1 — Structural Scout")
    ba_out.mkdir(parents=True, exist_ok=True)
    r2 = step_ba1(pipeline_out, repo_root, ba_out)
    all_results.append(r2)

    # ── Step 3: BA Agent 2 ────────────────────────────────────────────────────
    _banner(3, "BA Agent 2 — Deep Analyst")
    r3 = step_ba2(pipeline_out, repo_root, ba_out)
    all_results.append(r3)

    # ── Steps 4-7: Parallel tracks ────────────────────────────────────────────
    print(f"\n{'─' * 64}")
    print(bold(cyan(f"[STEPS 4-7/{_TOTAL_STEPS}]  Parallel Tracks: DA + TA + AA")))
    print(f"{'─' * 64}")
    parallel_results = run_parallel_tracks(pipeline_out, repo_root, output_dir)
    all_results.extend(parallel_results)

    # ── Step 8: Foundation ────────────────────────────────────────────────────
    _banner(8, "Foundation — Knowledge Graph Synthesis + 20 Forward-Engineering Documents")
    r8 = step_foundation(output_dir)
    all_results.append(r8)

    # ── Summary ───────────────────────────────────────────────────────────────
    print_summary(output_dir, all_results, time.monotonic() - t0)

    failed = [r for r in all_results if r["returncode"] != 0]
    return 0 if not failed else 1


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="run.py",
        description=(
            "Standard Forward Engineering Pipeline — "
            "fully automated reverse engineering using Repo A's 8 high-quality prompts."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py --source "https://github.com/dotnet-architecture/eShopOnWeb" --output ./results
  python run.py --source "C:/projects/legacy-app"                            --output ./results
  python run.py --source "C:/projects/legacy-app"  --output ./results --skip-layer1

Output:
  <output>/Business_Analysis/         BA Agent outputs
  <output>/Data_Analysis/             DA Agent outputs
  <output>/Technology_Analysis/       TA Agent outputs
  <output>/Application_Analysis/      AA Agent outputs
  <output>/Foundation_KnowledgeGraph/ Enterprise Knowledge Graph + 4 views
  <output>/ForwardEngineering_Docs/   20 forward-engineering documents
""",
    )
    parser.add_argument("--source",       required=True,
                        help="GitHub URL or local folder path")
    parser.add_argument("--output",       default="./forward-engineering-output",
                        help="Root output directory (default: ./forward-engineering-output)")
    parser.add_argument("--skip-layer1",  action="store_true", default=False,
                        help="Skip Layer 1 extraction (use when already extracted)")
    args = parser.parse_args()

    code = orchestrate(
        source       = args.source,
        output_dir   = Path(args.output),
        skip_layer1  = args.skip_layer1,
    )
    sys.exit(code)


if __name__ == "__main__":
    main()
