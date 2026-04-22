# dotenv-linter-plus

Schema-aware .env validator with CI-friendly JSON output.

## MVP status

- Basic CLI scaffold is ready (`main.py`).
- Supports `--format text|json` and `--dry-run`.
- Intended as a foundation for iterative feature work.

## Quick start

```bash
python3 main.py --help
python3 main.py --format json --dry-run
```

## Next steps

1. Add domain-specific command set and config file support.
2. Add tests and GitHub Actions workflow.
3. Package and publish first tagged release.
