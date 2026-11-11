#!/usr/bin/env python3
"""
Helper script to calculate context usage, transcript size and token estimates
for Antigravity sessions.

Usage:
    context_stats.py --host
    context_stats.py <conversation_id> [context_limit_tokens]

The usage percentage is reported only if the model's context limit is given;
the script holds no table of model limits, because such a table goes stale.
"""

import json
import os
import sys

def analyze_context(conv_id, limit=None):
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

    usage_pct = (estimated_tokens / limit) * 100.0 if limit else None

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
    limit = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else None
    if not cid:
        print("Usage: context_stats.py <conversation_id> [context_limit_tokens]")
        sys.exit(1)
    res = analyze_context(cid, limit)
    print(json.dumps(res, indent=2))
