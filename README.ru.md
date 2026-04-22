# dotenv-linter-plus

[English version](README.md)

Валидатор `.env` по JSON-схеме для локальной разработки и CI.

## Возможности

- проверка обязательных ключей
- проверка типов значений: `string`, `int`, `bool`, `url`
- обнаружение лишних ключей
- strict-режим для CI
- JSON-вывод для автоматизаций

## Команды

```bash
python3 main.py init-schema --output .env.schema.json
python3 main.py lint --schema .env.schema.json --env-file .env
python3 main.py lint --schema .env.schema.json --env-file .env --format json
python3 main.py lint --schema .env.schema.json --env-file .env --allow-extra
python3 main.py lint --schema .env.schema.json --env-file .env --strict
```

## Коды возврата

- `0` валидация успешна
- `1` валидация не пройдена
