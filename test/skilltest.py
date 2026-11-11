"""Shared helpers for per-skill test suites.

Importable from any skill's test file because pytest.ini sets `pythonpath = .`
(test/ is the rootdir). Keeping discovery, skill-loading and the eval test itself (gate_test) here means
a suite's test file holds only its gate profile, and the suites cannot drift apart.
"""

import pathlib

import pytest
import yaml

from gates import run_gates
from runner import generate


def skill_dir_for(test_file):
    """The skill directory a suite tests, derived from the suite's folder.

        test/<name>/test_<name>.py  ->  <repo-root>/skills/<group>/<name>/

    Keeps every per-skill test file free of hard-coded paths: it names the skill
    by the folder it lives in.
    """
    p = pathlib.Path(test_file).resolve()
    name = p.parent.name          # test/<name>/
    repo_root = p.parents[2]      # test/<name>/file -> [0]=<name> [1]=test [2]=root
    return next((repo_root / "skills").glob(f"*/{name}"))   # e.g. skills/util/read-pdf


def read_skill_body(skill_dir):
    """Return a skill's SKILL.md body with the YAML frontmatter stripped.

    The body is what gets injected on activation in production; the frontmatter
    (name/description) is discovery metadata, not instructions.

    Every `references/*.md` and `assets/*.md` file the body names is appended. In
    production the model reads such a file when the body tells it to; the single
    model call of a test cannot, so the harness supplies it.
    """
    text = (pathlib.Path(skill_dir) / "SKILL.md").read_text()
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            text = parts[2]
    text = text.strip()
    for folder in ("references", "assets"):
        for doc in sorted((pathlib.Path(skill_dir) / folder).glob("*.md")):
            rel = f"{folder}/{doc.name}"
            if rel in text:
                text += f"\n\n<!-- {rel} -->\n" + doc.read_text().strip()
    return text


def discover_cases(test_file):
    """All case directories for a suite, sorted by name (01-…, 02-…)."""
    cases_dir = pathlib.Path(test_file).parent / "cases"
    return sorted(p for p in cases_dir.iterdir() if p.is_dir())


def load_input(case):
    return (pathlib.Path(case) / "input.md").read_text()


def load_expected(case):
    return yaml.safe_load((pathlib.Path(case) / "expected.yaml").read_text())


def show_output(request, name, output):
    """Print the model's raw output to the console when run with --show-model-output.

    Prints live for every test (pass or fail) with no need for `-s`: it suspends
    pytest's output capture around the print so the text reaches the real stdout,
    then resumes capture. Falls back to a plain print if no capture is active.
    """
    if not request.config.getoption("--show-model-output"):
        return
    text = f"\n===== model output [{name}] =====\n{output}\n===== end [{name}] =====\n"
    capman = request.config.pluginmanager.getplugin("capturemanager")
    if capman is None:
        print(text)
        return
    capman.suspend_global_capture(in_=True)
    try:
        print(text)
    finally:
        capman.resume_global_capture()


def gate_test(test_file, profile):
    """Build a suite's eval test: one model call per scenario under cases/, graded
    by gates.run_gates with the suite's profile. A suite's test file needs only

        test_gates = gate_test(__file__, GATE_PROFILE)
    """
    skill_dir = skill_dir_for(test_file)
    cases = discover_cases(test_file)

    @pytest.mark.parametrize("case", cases, ids=[c.name for c in cases])
    def test_gates(case, request):
        out = generate(read_skill_body(skill_dir), load_input(case))
        show_output(request, case.name, out)
        failures = run_gates(out, load_expected(case), profile)
        assert not failures, "gate failures:\n  - " + "\n  - ".join(failures)

    return test_gates
