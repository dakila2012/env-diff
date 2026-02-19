env-diff

A CLI tool to compare two `.env` files or the current environment against a file. It detects added, removed, and changed variables, displaying differences with colorized output (red for removed, green for added, yellow for changed). Handles comments, inline comments, quoted values, and errors like missing files gracefully. Ideal for spotting environment drifts between dev/prod setups or local vs. deployed configs.

Production-ready with excellent parsing, UX, and error handling.

## Installation

```bash
git clone <repository-url>
cd env-diff
```

No external dependencies; uses Python standard library only. Run directly with:

```bash
python src/main.py --help
```

## Usage

```bash
# Show help
python src/main.py --help

# Diff two .env files (left -> right)
python src/main.py dev.env prod.env

# Compare current environment (left) to file (right)
python src/main.py --current prod.env

# Show version
python src/main.py --version
```

Exits with code 1 if differences found, 0 otherwise.

## Features

- Compares two `.env` files or current `os.environ` vs. a file (`--current`)
- Colorized output: REMOVED (red), ADDED (green), CHANGED (yellow)
- Robust `.env` parsing: skips comments/empty lines, trims inline comments, strips quotes
- Sorted output for consistency
- Graceful error handling (e.g., missing files)
- `argparse`-powered CLI with validation (exact 1/2 files required)

## Dependencies

Python standard library only (`argparse`, `os`, `sys`).

## Tests

No tests implemented.

## License

MIT