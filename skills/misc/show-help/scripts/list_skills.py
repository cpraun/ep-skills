#!/usr/bin/env python3
"""
List the skills and agents of this library with their frontmatter properties.

Reads every <skills-dir>/*/SKILL.md and <skills-dir>/*/*/SKILL.md (skills in a group
folder such as util/) next to this skill and every
<plugin-root>/agents/*.md, so the listing is always current. Standard
library only.

Usage:
    list_skills.py            # tables of all skills and agents
    list_skills.py --json     # same data as JSON
"""

import json
import re
import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parents[3]
AGENTS_DIR = SKILLS_DIR.parent / "agents"


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    fm, out = m.group(1), {}
    for key in ("name", "trainable", "disable-model-invocation", "model", "tools"):
        km = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
        if km:
            out[key] = km.group(1).strip().strip("\"'")
    dm = re.search(r"^description:\s*(.*?)(?=^\S|\Z)", fm, re.S | re.M)
    if dm:
        d = dm.group(1).strip()
        if d[:2] in (">-", "|-") or d[:1] in (">", "|"):
            d = d.split("\n", 1)[1] if "\n" in d else ""
        out["description"] = " ".join(d.split()).strip("\"'")
    return out


def skills():
    found = [*SKILLS_DIR.glob("*/SKILL.md"), *SKILLS_DIR.glob("*/*/SKILL.md")]
    for p in sorted(found, key=lambda p: p.parent.name):
        fm = frontmatter(p.read_text(encoding="utf-8"))
        learned = p.parent / "LEARNED.md"
        yield {
            "kind": "skill",
            "name": fm.get("name", p.parent.name),
            "description": fm.get("description", ""),
            "trainable": fm.get("trainable") == "true" or learned.exists(),
            "learned_rules": learned.read_text(encoding="utf-8").count("\n### [") if learned.exists() else 0,
            "command_only": fm.get("disable-model-invocation") == "true",
            "path": str(p.relative_to(SKILLS_DIR.parent)),
        }


def agents():
    for p in sorted(AGENTS_DIR.glob("*.md")):
        fm = frontmatter(p.read_text(encoding="utf-8"))
        yield {
            "kind": "agent",
            "name": fm.get("name", p.stem),
            "description": fm.get("description", ""),
            "model": fm.get("model", ""),
            "tools": fm.get("tools", "").strip("[]"),
            "path": str(p.relative_to(SKILLS_DIR.parent)),
        }


def main():
    rows = list(skills())
    agent_rows = list(agents())
    if "--json" in sys.argv:
        json.dump(rows + agent_rows, sys.stdout, ensure_ascii=False, indent=1)
        return
    print("| Skill | Trainable (rules) | Command only | Description |")
    print("|---|---|---|---|")
    for r in rows:
        t = f"yes ({r['learned_rules']})" if r["trainable"] else "no"
        c = "yes" if r["command_only"] else "no"
        print(f"| {r['name']} | {t} | {c} | {r['description']} |")
    if agent_rows:
        print()
        print("| Agent | Model | Tools | Description |")
        print("|---|---|---|---|")
        for r in agent_rows:
            print(f"| {r['name']} | {r['model']} | {r['tools']} | {r['description']} |")


if __name__ == "__main__":
    main()
