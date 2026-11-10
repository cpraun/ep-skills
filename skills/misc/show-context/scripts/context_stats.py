#!/usr/bin/env python3
"""
Helper script to calculate context usage, transcript size, token estimates,
and model limits for Antigravity sessions.
"""

import json
import os
import sys

MODEL_LIMITS = {
    "gemini 3.7 flash": 1048576,
    "gemini 3.7 pro": 1048576,
    "gemini 1.5 pro": 2097152,
    "gemini 1.5 flash": 1048576,
    "claude 3.7 sonnet": 200000,
    "claude 3.5 sonnet": 200000,
    "claude 3.5 haiku": 200000,
    "gpt-4o": 128000,
}

def analyze_context(conv_id, model_name="Gemini 3.7 Flash"):
    app_data = os.path.expanduser("~/.gemini/antigravity")
    transcript_path = os.path.join(app_data, "brain", conv_id, ".system_generated/logs/transcript.jsonl")

    if not os.path.exists(transcript_path):
        return {
            "error": f"Transcript not found at {transcript_path}"
        }

    size_bytes = os.path.getsize(transcript_path)
    size_kb = size_bytes / 1024.0
    size_mb = size_kb / 1024.0

    steps = 0
    total_chars = 0
    tool_calls = 0

    with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                steps += 1
                content = entry.get("content", "") or ""
                thinking = entry.get("thinking", "") or ""
                total_chars += len(content) + len(thinking)
                if "tool_calls" in entry and entry["tool_calls"]:
                    tool_calls += len(entry["tool_calls"])
            except Exception:
                pass

    # Heuristic: ~4 characters per token
    estimated_tokens = total_chars // 4

    norm_model = model_name.lower().strip()
    limit = 1048576  # default 1M
    for k, v in MODEL_LIMITS.items():
        if k in norm_model:
            limit = v
            break

    usage_pct = (estimated_tokens / limit) * 100.0

    return {
        "transcript_path": transcript_path,
        "size_bytes": size_bytes,
        "size_kb": size_kb,
        "size_mb": size_mb,
        "steps": steps,
        "total_chars": total_chars,
        "estimated_tokens": estimated_tokens,
        "tool_calls": tool_calls,
        "model_limit": limit,
        "usage_pct": usage_pct
    }

def detect_host():
    """'claude-code' if run from Claude Code, 'antigravity' if an Antigravity
    data directory exists, else 'unknown'."""
    if os.environ.get("CLAUDECODE"):
        return "claude-code"
    if os.path.isdir(os.path.expanduser("~/.gemini/antigravity")):
        return "antigravity"
    return "unknown"


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--host":
        print(detect_host())
        sys.exit(0)
    cid = sys.argv[1] if len(sys.argv) > 1 else ""
    mname = sys.argv[2] if len(sys.argv) > 2 else "Gemini 3.7 Flash"
    if not cid:
        print("Usage: context_stats.py <conversation_id> [model_name]")
        sys.exit(1)
    res = analyze_context(cid, mname)
    print(json.dumps(res, indent=2))
