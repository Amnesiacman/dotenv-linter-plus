# dotenv-linter-plus

[Русская версия](README.ru.md)

Schema-aware `.env` validator for local development and CI.

## Features

- validate required keys
- validate value types: `string`, `int`, `bool`, `url`
- report extra keys
- strict mode for CI
- JSON output for automation

## Commands

```bash
python3 main.py init-schema --output .env.schema.json
python3 main.py lint --schema .env.schema.json --env-file .env
python3 main.py lint --schema .env.schema.json --env-file .env --format json
python3 main.py lint --schema .env.schema.json --env-file .env --allow-extra
python3 main.py lint --schema .env.schema.json --env-file .env --strict
```

## Exit codes

- `0` successful validation
- `1` validation failed
