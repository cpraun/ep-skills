# Changelog

All notable changes to `ep-skills` are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The version is the `version` in `plugin.json` and `.claude-plugin/plugin.json`. Renamed or moved skills change the commands users type, so they are marked **breaking**.

## [Unreleased]

### Changed

- Learned rules and your own Word template now live in `~/.ep-skills/` (`learned/<skill>.md`, `template.docx`) instead of the plugin folder, so a plugin update no longer removes them. `/learn` moves an old `LEARNED.md` on its next run; move an old `assets/template.docx` yourself.

## [0.9.0] - 2026-11-10

Initial release.
