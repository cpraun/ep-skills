# Changelog

All notable changes to `ep-skills` are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The version is the `version` in `plugin.json` and `.claude-plugin/plugin.json`. Users receive an update only when this version changes, so bump it in both files with every release. Renamed or moved skills change the commands users type, so they are marked **breaking**.

## [Unreleased]

### Changed

- Learned rules and your own Word template now live in `~/.ep-skills/` (`learned/<skill>.md`, `template.docx`) instead of the plugin folder, so a plugin update no longer removes them. `/learn` moves an old `LEARNED.md` on its next run; move an old `assets/template.docx` yourself.
- `show-context` (Antigravity) reports a usage percentage only when the model's context limit is known; its outdated table of model limits is gone.

### Fixed

- Skills refer to other skills by name instead of a file path that no longer existed since the group folders.

## [0.9.0] - 2026-11-10

Initial release.
