# Contributing to InterceptIQ

Thanks for your interest in contributing! Here's how to get started.

## Development Setup

```bash
git clone https://github.com/guajiimi/interceptiq.git
cd interceptiq
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest
```

## Project Layout

- `src/interceptiq/` — Core library (zero external dependencies)
- `examples/` — Sample input files for testing
- `docs/` — Documentation and demo dashboard
- `tests/` — Test suite

## Submitting Changes

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/my-change`)
3. Commit your changes (`git commit -am 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-change`)
5. Open a Pull Request

## Guidelines

- Keep it **zero-dependency** — pure Python stdlib only
- All CLI commands must read JSON in, write JSON out
- Add tests for new features
- Update docs if behavior changes

## Code Style

- Python 3.10+ (type hints encouraged)
- 4-space indentation
- Descriptive variable names

## Questions?

Open an [issue](https://github.com/guajiimi/interceptiq/issues) — we're happy to help!
