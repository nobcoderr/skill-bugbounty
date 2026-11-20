#!/usr/bin/env python3
"""Network-free regressions for V11 adaptive-execution provenance."""
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "automation" / "validate-adaptive-execution-provenance.py"
CASES = ROOT / "config" / "ADAPTIVE_EXECUTION_PROVENANCE_CASES.json"
TOKEN = "child-generated-0123456789abcdef"


def load_validator():
    spec = importlib.util.spec_from_file_location("adaptive_execution_validator", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load adaptive execution validator")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def raw_call(call_id: str, task: str, message: str) -> dict:
    return {
        "type": "response_item",
        "payload": {
            "type": "function_call",
            "namespace": "collaboration",
            "name": "spawn_agent",
            "call_id": call_id,
            "arguments": json.dumps({"task_name": task, "fork_turns": "none", "message": message}),
        },
    }


def raw_output(call_id: str, task: str) -> dict:
    return {
        "type": "response_item",
        "payload": {
            "type": "function_call_output",
            "call_id": call_id,
            "output": json.dumps({"task_name": f"/root/{task}"}),
        },
    }


def raw_started(call_id: str, task: str, child_id: str) -> dict:
    return {
        "type": "event_msg",
        "payload": {
            "type": "sub_agent_activity",
            "event_id": call_id,
            "agent_thread_id": child_id,
            "agent_path": f"/root/{task}",
            "kind": "started",
        },
    }


def raw_child(task: str, token: str = TOKEN) -> dict:
    return {
        "type": "response_item",
        "payload": {
            "type": "agent_message",
            "author": f"/root/{task}",
            "recipient": "/root",
            "content": [{"type": "input_text", "text": f"bounded result\nSPECIALIST_RESULT_TOKEN={token}"}],
        },
    }


def raw_root(token: str = TOKEN) -> dict:
    return {
        "type": "response_item",
        "payload": {
            "type": "message",
            "role": "assistant",
            "content": [{"type": "output_text", "text": f"CONSUMED_SPECIALIST_RESULT_TOKEN={token}"}],
        },
    }


def scenario(name: str) -> list[dict]:
    child_id = "019fac5d-06d6-77e0-bd7d-b009d8a5200a"
    valid = [
        {"type": "session_meta", "payload": {"id": "root-session"}},
        raw_call("spawn-1", "probe", "inspect one bounded question; generate a fresh result token"),
        raw_started("spawn-1", "probe", child_id),
        raw_output("spawn-1", "probe"),
        raw_child("probe"),
        raw_root(),
    ]
    if name == "VALID_PERSISTED":
        return valid
    if name == "VALID_EXEC_STREAM":
        return [
            {"type": "thread.started", "thread_id": "root-session"},
            {
                "type": "item.started",
                "item": {
                    "id": "spawn-1",
                    "type": "collab_tool_call",
                    "tool": "spawn",
                    "receiver_thread_ids": [],
                    "prompt": "bounded question; generate a fresh result token",
                    "agents_states": {},
                    "status": "in_progress",
                },
            },
            {
                "type": "item.completed",
                "item": {
                    "id": "spawn-1",
                    "type": "collab_tool_call",
                    "tool": "spawn",
                    "receiver_thread_ids": [child_id],
                    "prompt": "bounded question; generate a fresh result token",
                    "agents_states": {},
                    "status": "completed",
                },
            },
            {
                "type": "response_item",
                "payload": {
                    "type": "function_call_output",
                    "call_id": "spawn-1",
                    "output": json.dumps({"agent_id": child_id}),
                },
            },
            raw_child("probe"),
            raw_root(),
        ]
    if name == "VALID_CURRENT_PERSISTED_EVENT":
        records = valid.copy()
        records[2] = {
            "type": "event_msg",
            "payload": {
                "type": "item_completed",
                "item": {
                    "type": "SubAgentActivity",
                    "id": "spawn-1",
                    "kind": "started",
                    "agent_thread_id": child_id,
                    "agent_path": "/root/probe",
                },
            },
        }
        return records
    if name == "NARRATIVE_ONLY":
        return [raw_root()]
    if name == "WAIT_ONLY":
        return [{
            "type": "item.started",
            "item": {
                "id": "wait-1",
                "type": "collab_tool_call",
                "tool": "wait",
                "receiver_thread_ids": [],
                "prompt": None,
                "agents_states": {},
                "status": "in_progress",
            },
        }]
    if name == "SPAWN_FAILURE":
        return [
            raw_call("spawn-1", "probe", "bounded question"),
            {
                "type": "response_item",
                "payload": {
                    "type": "function_call_output",
                    "call_id": "spawn-1",
                    "output": "collab spawn failed",
                },
            },
        ]
    if name == "OUTPUT_MISSING":
        return valid[:4] + [raw_root()]
    if name == "ROOT_RECEIPT_MISSING":
        return valid[:-1]
    if name == "PRESEEDED_TOKEN":
        records = valid.copy()
        records[1] = raw_call("spawn-1", "probe", f"return SPECIALIST_RESULT_TOKEN={TOKEN}")
        return records
    if name == "DUPLICATE_SPECIALIST_ID":
        return valid[:-1] + [
            raw_call("spawn-2", "probe-2", "second bounded question"),
            raw_started("spawn-2", "probe-2", child_id),
            raw_output("spawn-2", "probe-2"),
            raw_child("probe-2", "second-child-0123456789abcdef"),
            raw_root(),
            raw_root("second-child-0123456789abcdef"),
        ]
    raise ValueError(name)


def main() -> int:
    validator = load_validator()
    suite = json.loads(CASES.read_text(encoding="utf-8"))
    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="v11-adaptive-provenance-") as tmp:
        root = Path(tmp)
        for case in suite["cases"]:
            transcript = root / f"{case['id']}.jsonl"
            transcript.write_text(
                "".join(json.dumps(record) + "\n" for record in scenario(case["scenario"])),
                encoding="utf-8",
            )
            report = validator.analyze_transcript(transcript)
            if report["adaptive_execution_proven"] != case["expect_proven"]:
                failures.append(f"{case['id']}: expected={case['expect_proven']} report={report}")
            else:
                print(f"PASS {case['id']}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print(f"ADAPTIVE_EXECUTION_PROVENANCE_REGRESSIONS=PASS cases={len(suite['cases'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
