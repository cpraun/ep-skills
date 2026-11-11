# Changelog

All notable changes to `ep-skills` are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The version is the `version` in `plugin.json` and `.claude-plugin/plugin.json`. Users receive an update only when this version changes, so bump it in both files with every release. Renamed or moved skills change the commands users type, so they are marked **breaking**.

## [Unreleased]

## [0.9.1] - 2026-11-11

### Added

- Plugin logo (`logo.png`, source `logo.svg`): a light bulb, set as `icon` (Claude plugin directory) and `logo` (Antigravity plugin list) in both manifests.

### Changed

- Learned rules and your own Word template now live in `~/.ep-skills/` (`learned/<skill>.md`, `template.docx`) instead of the plugin folder, so a plugin update no longer removes them. `/learn` moves an old `LEARNED.md` on its next run; move an old `assets/template.docx` yourself.
- `.gitignore` no longer lists `LEARNED.md` and `assets/template.docx`; the plugin no longer writes these files into its own folder.
- `show-context` (Antigravity) reports a usage percentage only when the model's context limit is known; its outdated table of model limits is gone.
- The "insufficient input" notice in 18 skills is one sentence; it still points to `/grill-me`.
- `learn` moved to `skills/misc/learn/`, so every skill sits in a group folder. The command `/learn` is unchanged.
- Test harness: each eval suite's test file holds only its gate profile; the shared test is `gate_test()` in `test/skilltest.py`. Test names and commands are unchanged.
- The plugin entry in `marketplace.json` no longer repeats the description of `plugin.json`.

### Removed

- `spec/agent-skills-spec.md` (a link only; the link is now in the README) and the unused `version` key in the frontmatter of `check-art-123-2-epc`.

### Fixed

- Skills refer to other skills by name instead of a file path that no longer existed since the group folders.
- Typos in `test/env_sample.sh` and `test/README.md`.

## [0.9.0] - 2026-11-10

Initial release.
