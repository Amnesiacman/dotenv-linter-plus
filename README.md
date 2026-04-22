# dotenv-linter-plus

`dotenv-linter-plus` проверяет `.env` по JSON-схеме с типами и required-правилами.
Инструмент подходит для локальной проверки и CI-гейтов.

## Поддерживаемые типы

- `string`
- `int`
- `bool` (`true/false/1/0/yes/no`)
- `url`

## Установка

```bash
python3 -m pip install -e .
dotenv-linter-plus --help
```

Локально без установки:

```bash
python3 main.py --help
```

## Быстрый старт

1) Создать стартовую схему:

```bash
python3 main.py init-schema
```

2) Проверить `.env`:

```bash
python3 main.py lint --schema .env.schema.json --env-file .env
```

3) Получить JSON-отчет:

```bash
python3 main.py lint --schema .env.schema.json --env-file .env --format json
```

## Режимы

- `--allow-extra`: не ругаться на ключи, которых нет в схеме
- `--strict`: падать (exit code `1`) не только на errors, но и на warnings

## Формат схемы

```json
{
  "keys": {
    "APP_ENV": {"type": "string", "required": true},
    "DEBUG": {"type": "bool", "required": true},
    "PORT": {"type": "int", "required": true}
  }
}
```

## GitHub Actions

- `ci.yml`: запускает тесты и smoke lint
- `release.yml`: создает GitHub Release по тегу `v*`
