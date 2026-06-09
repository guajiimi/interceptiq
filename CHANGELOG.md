# Changelog

## [0.3.0] - 2026-06-09

### Added
- GitHub Actions CI workflow (Python 3.10, 3.11, 3.12, 3.13 on ubuntu-latest)
- Real-world output examples in README showing actual CLI output
- Architecture diagram in README explaining the full pipeline
- "Why AI Agents Need This" section targeting Codex/Claude Code reviewers
- CI and PyPI badges in README header
- `docs/examples/real-world-demo.md` — complete end-to-end workflow guide
- `scripts/set-github-topics.sh` — automated topic configuration script

### Changed
- Version aligned to 0.3.0 across `__init__.py` and `pyproject.toml`
- README rewritten for clarity, completeness, and AI-agent positioning
- Improved `docs/submission/description.md` with technical depth

### Fixed
- Version inconsistency between `__init__.py` (was 0.1.0) and `pyproject.toml` (was 0.2.0)

## [0.2.0] - 2026-06-01

### Added
- Improved README with comprehensive documentation
- CONTRIBUTING.md guide
- GitHub topics and project metadata
- Python classifiers for PyPI discoverability

### Changed
- Bumped version to 0.2.0
- Enhanced pyproject.toml with full metadata

## [0.1.0] - 2026-05-01

### Added
- Initial release
- `payload-analyze` — JSON/form/base64/hex payload decoder
- `dom-analyze` — HTML DOM structure and selector extractor
- `replay-generate` — Replay plan + scraper scaffold generator
- `agent-brief` — AI agent context brief builder
- `jsonl-dedupe` — JSONL key-based deduplication
- CLI entry point via `interceptiq` command
- Example capture files and demo dashboard
