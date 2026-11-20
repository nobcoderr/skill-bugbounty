#!/usr/bin/env python3
"""Derive adaptive-specialist execution provenance from a session JSONL transcript.

The validator is network-free. It accepts Codex session JSONL / `codex exec
--json` streams and equivalent records whose tool names are Cursor `Task`,
Codex `spawn_agent`/`spawn`, or Claude Code `Agent`. An adaptive execution is
proven only when a real spawn has a unique child identity, a separate child
result, and a later root receipt for a child-generated result token.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

SPAWN_TOOLS = {"spawn", "spawn_agent", "Task", "Agent"}
WAIT_TOOLS = {"wait", "wait_agent"}
RESULT_TOKEN_RE = re.compile(r"(?m)^SPECIALIST_RESULT_TOKEN=([A-Za-z0-9._:-]{16,128})\s*$")
RECEIPT_TOKEN_RE = re.compile(r"(?m)^CONSUMED_SPECIALIST_RESULT_TOKEN=([A-Za-z0-9._:-]{16,128})\s*$")
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f-]{27,}$", re.IGNORECASE)


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts: list[str] = []
        for item in value:
            if isinstance(item, dict):
                parts.append(_text(item.get("text") or item.get("input_text") or item.get("content") or ""))
            else:
                parts.append(_text(item))
        return "\n".join(part for part in parts if part)
    if isinstance(value, dict):
        return _text(value.get("text") or value.get("content") or value.get("output") or "")
    return ""


def _json_object(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if not isinstance(value, str):
        return {}
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _tool_call(record: dict[str, Any]) -> tuple[str, str, Any] | None:
    if record.get("type") == "response_item":
        payload = record.get("payload") or {}
        if payload.get("type") in {"function_call", "custom_tool_call"}:
            return (
                str(payload.get("name") or ""),
                str(payload.get("call_id") or payload.get("id") or ""),
                payload.get("arguments", payload.get("input")),
            )
    if record.get("type") in {"item.started", "item.completed"}:
        item = record.get("item") or {}
        if item.get("type") == "collab_tool_call":
            return str(item.get("tool") or ""), str(item.get("id") or ""), item.get("prompt")
    return None


def _tool_output(record: dict[str, Any]) -> tuple[str, str] | None:
    if record.get("type") != "response_item":
        return None
    payload = record.get("payload") or {}
    if payload.get("type") not in {"function_call_output", "custom_tool_call_output"}:
        return None
    return str(payload.get("call_id") or ""), _text(payload.get("output"))


def _assistant_text(record: dict[str, Any]) -> str:
    if record.get("type") == "response_item":
        payload = record.get("payload") or {}
        if payload.get("type") == "message" and payload.get("role") == "assistant":
            return _text(payload.get("content"))
    if record.get("type") == "item.completed":
        item = record.get("item") or {}
        if item.get("type") == "agent_message":
            return _text(item.get("text") or item.get("content"))
    return ""


@dataclass
class Spawn:
    call_id: str
    index: int
    raw_input: str
    task_name: str = ""
    specialist_ids: set[str] = field(default_factory=set)
    agent_paths: set[str] = field(default_factory=set)
    output_identity_seen: bool = False
    output_text: str = ""
    output_index: int = -1


def _state_outputs(value: Any) -> list[str]:
    outputs: list[str] = []
    if isinstance(value, dict):
        for state in value.values():
            if isinstance(state, dict):
                completed = state.get("completed")
                if isinstance(completed, str) and completed.strip():
                    outputs.append(completed)
            elif isinstance(state, str) and state.strip():
                outputs.append(state)
    return outputs


def analyze_transcript(path: Path, stderr_log: Path | None = None) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    malformed = 0
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            malformed += 1
            continue
        if isinstance(value, dict):
            records.append(value)

    root_session_id = ""
    spawns: dict[str, Spawn] = {}
    wait_calls = 0
    call_outputs: dict[str, str] = {}
    child_messages: list[tuple[int, str, str]] = []
    root_messages: list[tuple[int, str]] = []
    explicit_failure_markers = 0

    for index, record in enumerate(records):
        if record.get("type") == "session_meta":
            root_session_id = str((record.get("payload") or {}).get("id") or root_session_id)
        elif record.get("type") == "thread.started":
            root_session_id = str(record.get("thread_id") or root_session_id)

        call = _tool_call(record)
        if call is not None:
            name, call_id, raw = call
            if name in SPAWN_TOOLS and call_id and call_id not in spawns:
                args = _json_object(raw)
                raw_input = raw if isinstance(raw, str) else json.dumps(raw, sort_keys=True)
                spawns[call_id] = Spawn(
                    call_id=call_id,
                    index=index,
                    raw_input=raw_input,
                    task_name=str(args.get("task_name") or args.get("task") or ""),
                )
            elif name in WAIT_TOOLS and record.get("type") in {"response_item", "item.started"}:
                wait_calls += 1

        output = _tool_output(record)
        if output is not None:
            call_outputs[output[0]] = output[1]

        if record.get("type") == "event_msg":
            payload = record.get("payload") or {}
            activity = payload
            if payload.get("type") == "item_completed" and isinstance(payload.get("item"), dict):
                item = payload["item"]
                if item.get("type") == "SubAgentActivity":
                    activity = item
            if activity.get("type") in {"sub_agent_activity", "SubAgentActivity"} and activity.get("kind") == "started":
                call_id = str(activity.get("event_id") or activity.get("id") or "")
                spawn = spawns.get(call_id)
                if spawn is not None:
                    child_id = str(activity.get("agent_thread_id") or "")
                    agent_path = str(activity.get("agent_path") or "")
                    if child_id:
                        spawn.specialist_ids.add(child_id)
                    if agent_path:
                        spawn.agent_paths.add(agent_path)

        if record.get("type") in {"item.started", "item.completed"}:
            item = record.get("item") or {}
            if item.get("type") == "collab_tool_call":
                call_id = str(item.get("id") or "")
                spawn = spawns.get(call_id)
                if spawn is not None:
                    for child_id in item.get("receiver_thread_ids") or []:
                        if child_id:
                            spawn.specialist_ids.add(str(child_id))
                    state_outputs = _state_outputs(item.get("agents_states"))
                    if state_outputs:
                        spawn.output_text = "\n".join(state_outputs)
                        spawn.output_index = index

        if record.get("type") == "response_item":
            payload = record.get("payload") or {}
            if payload.get("type") == "agent_message":
                author = str(payload.get("author") or "")
                content = _text(payload.get("content"))
                if author and content:
                    child_messages.append((index, author, content))

        assistant = _assistant_text(record)
        if assistant:
            root_messages.append((index, assistant))

        serialized = json.dumps(record, sort_keys=True)
        if "collab spawn failed" in serialized.lower() or "spawn_agent failed" in serialized.lower():
            explicit_failure_markers += 1

    if stderr_log is not None and stderr_log.is_file():
        stderr_text = stderr_log.read_text(encoding="utf-8", errors="replace").lower()
        explicit_failure_markers += stderr_text.count("collab spawn failed")
        explicit_failure_markers += stderr_text.count("spawn_agent failed")

    for call_id, spawn in spawns.items():
        output_text = call_outputs.get(call_id, "")
        parsed = _json_object(output_text)
        identity = str(parsed.get("agent_id") or parsed.get("task_name") or parsed.get("canonical_task_name") or "")
        if identity:
            spawn.output_identity_seen = True
            if UUID_RE.match(identity):
                spawn.specialist_ids.add(identity)
            else:
                spawn.agent_paths.add(identity)
        for msg_index, author, content in child_messages:
            if author in spawn.agent_paths or (spawn.task_name and author.endswith("/" + spawn.task_name)):
                spawn.output_text = content
                spawn.output_index = msg_index

    if len(spawns) == 1 and len(child_messages) == 1:
        only_spawn = next(iter(spawns.values()))
        if not only_spawn.output_text:
            msg_index, author, content = child_messages[0]
            only_spawn.agent_paths.add(author)
            only_spawn.output_text = content
            only_spawn.output_index = msg_index

    successful = [
        spawn for spawn in spawns.values()
        if spawn.output_identity_seen and spawn.specialist_ids
    ]
    unique_ids = sorted({child_id for spawn in successful for child_id in spawn.specialist_ids})
    provenance_specialists: list[dict[str, Any]] = []
    input_ok = bool(successful)
    output_ok = bool(successful)
    consumption_ok = bool(successful)

    for spawn in successful:
        input_ok = input_ok and bool(spawn.raw_input.strip())
        token_match = RESULT_TOKEN_RE.search(spawn.output_text)
        token = token_match.group(1) if token_match else ""
        if not token or token in spawn.raw_input:
            output_ok = False
        receipt_found = False
        if token:
            for msg_index, message in root_messages:
                if msg_index > spawn.output_index and token in RECEIPT_TOKEN_RE.findall(message):
                    receipt_found = True
                    break
        if not receipt_found:
            consumption_ok = False
        provenance_specialists.append({
            "spawn_call_id": spawn.call_id,
            "task_name": spawn.task_name or (sorted(spawn.agent_paths)[0] if spawn.agent_paths else ""),
            "specialist_id": sorted(spawn.specialist_ids)[0] if spawn.specialist_ids else "",
            "input_sha256": _sha256_text(spawn.raw_input),
            "output_sha256": _sha256_text(spawn.output_text),
            "result_token": token,
            "root_receipt_found": receipt_found,
        })

    spawn_attempts = len(spawns)
    spawn_successes = len(successful)
    spawn_failures = max(spawn_attempts - spawn_successes, explicit_failure_markers)
    reasons: list[str] = []
    if malformed:
        reasons.append(f"MALFORMED_JSONL_LINES:{malformed}")
    if not spawn_attempts:
        reasons.append("NO_SPAWN_ATTEMPT")
    if not spawn_successes:
        reasons.append("NO_SUCCESSFUL_SPAWN")
    if spawn_failures:
        reasons.append(f"SPAWN_FAILURES:{spawn_failures}")
    if not unique_ids:
        reasons.append("NO_UNIQUE_SPECIALIST_ID")
    if len(unique_ids) != spawn_successes:
        reasons.append("SPECIALIST_ID_NOT_UNIQUE_PER_SPAWN")
    if not input_ok:
        reasons.append("SEPARATE_SPECIALIST_INPUT_MISSING")
    if not output_ok:
        reasons.append("SEPARATE_SPECIALIST_OUTPUT_MISSING")
    if not consumption_ok:
        reasons.append("ROOT_CONSUMPTION_RECEIPT_MISSING")

    proven = (
        spawn_attempts >= 1
        and spawn_successes >= 1
        and spawn_failures == 0
        and len(unique_ids) == spawn_successes
        and input_ok
        and output_ok
        and consumption_ok
        and malformed == 0
    )
    return {
        "schema_version": "1.0",
        "transcript_path": str(path),
        "transcript_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "root_session_id": root_session_id,
        "adaptive_triggered": spawn_attempts > 0,
        "spawn_attempts": spawn_attempts,
        "spawn_successes": spawn_successes,
        "spawn_failures": spawn_failures,
        "wait_calls": wait_calls,
        "unique_specialist_ids": len(unique_ids),
        "separate_specialist_input": "PASS" if input_ok else "FAIL",
        "separate_specialist_output": "PASS" if output_ok else "FAIL",
        "root_consumed_specialist_output": "PASS" if consumption_ok else "FAIL",
        "specialists": provenance_specialists,
        "adaptive_execution_proven": proven,
        "failure_reasons": reasons,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--transcript", type=Path, required=True)
    parser.add_argument("--stderr-log", type=Path)
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--require-proven", action="store_true")
    args = parser.parse_args()

    report = analyze_transcript(args.transcript, args.stderr_log)
    if args.output_json is not None:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"ADAPTIVE_TRIGGERED={'YES' if report['adaptive_triggered'] else 'NO'}")
    print(f"SPAWN_ATTEMPTS={report['spawn_attempts']}")
    print(f"SPAWN_SUCCESS={report['spawn_successes']}")
    print(f"SPAWN_FAILURE={report['spawn_failures']}")
    print(f"WAIT_CALLS={report['wait_calls']}")
    print(f"UNIQUE_SPECIALIST_IDS={report['unique_specialist_ids']}")
    print(f"SEPARATE_SPECIALIST_INPUT={report['separate_specialist_input']}")
    print(f"SEPARATE_SPECIALIST_OUTPUT={report['separate_specialist_output']}")
    print(f"ROOT_CONSUMED_SPECIALIST_OUTPUT={report['root_consumed_specialist_output']}")
    print(f"ADAPTIVE_EXECUTION_PROVEN={'YES' if report['adaptive_execution_proven'] else 'NO'}")
    if report["failure_reasons"]:
        print("FAILURE_REASONS=" + ",".join(report["failure_reasons"]))
    if args.require_proven and not report["adaptive_execution_proven"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
