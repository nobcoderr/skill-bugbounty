#!/usr/bin/env python3
"""Run the real V11 Codex collaboration execution-plane acceptance test."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "automation" / "validate-adaptive-execution-provenance.py"

PROMPT = """This is an authorized synthetic V11 execution-plane regression.

The user explicitly requests exactly one real subagent for this test.

Requirements:
- Use the collaboration spawn_agent tool directly exactly once. Do not call it
  through functions.exec, a shell, or a simulated reasoning pass.
- Do not announce, infer, or report a child identity before the spawn_agent
  tool returns a real identity. A narrative statement is not a spawn.
- Use task_name v11_execution_probe and fork_turns none.
- Give the child one bounded task: state that 17 + 25 = 42, then invent a fresh
  24-or-more-character alphanumeric token that is not present in this prompt.
- Require the child final answer to contain exactly these two lines:
  PROBE_FACT=42
  SPECIALIST_RESULT_TOKEN=<fresh-child-token>
- Record the returned child thread/session identity.
- Wait for that exact live child and consume its separate result.
- Do not spawn another child. Do not create or modify files. Do not use network
  or shell tools.

Your final answer must include:
ADAPTIVE_TRIGGERED=YES
SPAWN_ATTEMPTS=1
SPAWN_SUCCESS=1
SPAWN_FAILURE=0
UNIQUE_SPECIALIST_IDS=1
SEPARATE_SPECIALIST_INPUT=PASS
SEPARATE_SPECIALIST_OUTPUT=PASS
ROOT_CONSUMED_SPECIALIST_OUTPUT=PASS
ADAPTIVE_EXECUTION_PROVEN=YES
PROBE_FACT=42
CONSUMED_SPECIALIST_RESULT_TOKEN=<exact-token-received-from-child>

If spawn or wait fails, report the real failure and
ADAPTIVE_EXECUTION_PROVEN=NO. Never fabricate success.
"""


def _root_thread_id(exec_stream: Path) -> str:
    for line in exec_stream.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(record, dict) and record.get("type") == "thread.started":
            return str(record.get("thread_id") or "")
    return ""


def _find_rollout(thread_id: str) -> Path | None:
    if not thread_id:
        return None
    codex_root = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))).expanduser()
    candidates: list[Path] = []
    for base in (codex_root / "sessions", codex_root / "archived_sessions"):
        if base.is_dir():
            candidates.extend(base.glob(f"**/*-{thread_id}.jsonl"))
    return max(candidates, key=lambda path: path.stat().st_mtime_ns) if candidates else None


def _write_transcript_manifest(output_dir: Path) -> None:
    evidence = sorted(
        path for path in output_dir.iterdir()
        if path.is_file() and path.name != "TRANSCRIPT_MANIFEST.sha256"
    )
    lines = [f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}" for path in evidence]
    (output_dir / "TRANSCRIPT_MANIFEST.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    output_dir = args.output_dir.expanduser().resolve()
    if output_dir.exists() and any(output_dir.iterdir()):
        if not args.force:
            raise SystemExit(f"output directory is not empty: {output_dir}")
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    workspace = output_dir / "workspace"
    workspace.mkdir()
    exec_stream = output_dir / "exec-stream.jsonl"
    transcript = output_dir / "persisted-root-rollout.jsonl"
    stderr_log = output_dir / "stderr.log"
    last_message = output_dir / "final-message.txt"
    provenance = output_dir / "adaptive-execution-provenance.json"

    env = os.environ.copy()
    for variable in ("SSL_CERT_FILE", "CODEX_CA_CERTIFICATE"):
        value = env.get(variable)
        if value and not Path(value).is_file():
            env.pop(variable, None)

    command = [
        "codex",
        "exec",
        "--enable",
        "multi_agent",
        "--enable",
        "multi_agent_v2",
        "--json",
        "--skip-git-repo-check",
        "--ignore-rules",
        "-s",
        "read-only",
        "-C",
        str(workspace),
        "-o",
        str(last_message),
        PROMPT,
    ]
    with exec_stream.open("w", encoding="utf-8") as stdout, stderr_log.open("w", encoding="utf-8") as stderr:
        try:
            completed = subprocess.run(
                command,
                env=env,
                stdin=subprocess.DEVNULL,
                stdout=stdout,
                stderr=stderr,
                text=True,
                timeout=args.timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired:
            print("V11_ADAPTIVE_EXECUTION_SMOKE=FAIL")
            print("CODEX_EXIT=TIMEOUT")
            return 1

    root_thread_id = _root_thread_id(exec_stream)
    persisted_source = _find_rollout(root_thread_id)
    if persisted_source is not None:
        shutil.copy2(persisted_source, transcript)
    else:
        shutil.copy2(exec_stream, transcript)

    validator = subprocess.run(
        [
            "python3",
            str(VALIDATOR),
            "--transcript",
            str(transcript),
            "--stderr-log",
            str(stderr_log),
            "--output-json",
            str(provenance),
            "--require-proven",
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    print(f"CODEX_EXIT={completed.returncode}")
    print(f"ROOT_THREAD_ID={root_thread_id or 'MISSING'}")
    print(f"PERSISTED_ROOT_ROLLOUT={'PASS' if persisted_source is not None else 'FAIL'}")
    print(validator.stdout, end="")
    if validator.stderr:
        print(validator.stderr, end="")
    passed = completed.returncode == 0 and persisted_source is not None and validator.returncode == 0
    print(f"V11_ADAPTIVE_EXECUTION_SMOKE={'PASS' if passed else 'FAIL'}")
    report = json.loads(provenance.read_text(encoding="utf-8"))
    for specialist in report.get("specialists", []):
        specialist_id = str(specialist.get("specialist_id") or "")
        specialist_source = _find_rollout(specialist_id)
        if specialist_source is not None:
            shutil.copy2(specialist_source, output_dir / f"specialist-{specialist_id}.jsonl")
    _write_transcript_manifest(output_dir)
    print("PROVENANCE=" + json.dumps(report, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
