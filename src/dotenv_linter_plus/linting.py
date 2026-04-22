import json
from pathlib import Path
from urllib.parse import urlparse


def parse_env_file(path: Path) -> dict:
    values = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def load_schema(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _is_bool(value: str) -> bool:
    return value.lower() in {"true", "false", "1", "0", "yes", "no"}


def _is_url(value: str) -> bool:
    parsed = urlparse(value)
    return bool(parsed.scheme and parsed.netloc)


def _validate_type(type_name: str, value: str) -> bool:
    if type_name == "string":
        return True
    if type_name == "int":
        return value.lstrip("+-").isdigit()
    if type_name == "bool":
        return _is_bool(value)
    if type_name == "url":
        return _is_url(value)
    return False


def lint_env(schema_path: Path, env_path: Path, allow_extra: bool = False) -> dict:
    report = {
        "ok": False,
        "schema_path": str(schema_path),
        "env_path": str(env_path),
        "allow_extra": allow_extra,
        "errors": [],
        "warnings": [],
        "checked_keys": 0,
    }
    if not schema_path.exists():
        report["errors"].append(f"Schema file not found: {schema_path}")
        return report
    if not env_path.exists():
        report["errors"].append(f"Env file not found: {env_path}")
        return report

    schema = load_schema(schema_path)
    env_values = parse_env_file(env_path)
    keys = schema.get("keys", {})
    report["checked_keys"] = len(keys)

    for key, rules in keys.items():
        required = bool(rules.get("required", False))
        expected_type = rules.get("type", "string")
        value = env_values.get(key)
        if required and value is None:
            report["errors"].append(f"Missing required key: {key}")
            continue
        if value is None:
            continue
        if not _validate_type(expected_type, value):
            report["errors"].append(
                f"Invalid type for {key}: expected {expected_type}, got '{value}'"
            )

    if not allow_extra:
        extra = sorted(set(env_values.keys()) - set(keys.keys()))
        for key in extra:
            report["warnings"].append(f"Extra key not in schema: {key}")

    report["ok"] = len(report["errors"]) == 0
    return report

