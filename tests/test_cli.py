import json
from pathlib import Path

from dotenv_linter_plus.cli import main


def test_init_schema(tmp_path: Path):
    out = tmp_path / ".env.schema.json"
    code = main(["init-schema", "--output", str(out)])
    assert code == 0
    assert out.exists()


def test_lint_json(tmp_path: Path, capsys):
    schema = tmp_path / ".env.schema.json"
    env_file = tmp_path / ".env"
    schema.write_text('{"keys":{"URL":{"type":"url","required":true}}}', encoding="utf-8")
    env_file.write_text("URL=https://example.com\n", encoding="utf-8")
    code = main(
        [
            "lint",
            "--schema",
            str(schema),
            "--env-file",
            str(env_file),
            "--format",
            "json",
        ]
    )
    payload = json.loads(capsys.readouterr().out.strip())
    assert code == 0
    assert payload["ok"] is True


def test_lint_strict_fails_on_warning(tmp_path: Path):
    schema = tmp_path / ".env.schema.json"
    env_file = tmp_path / ".env"
    schema.write_text('{"keys":{"A":{"type":"string","required":true}}}', encoding="utf-8")
    env_file.write_text("A=ok\nEXTRA=1\n", encoding="utf-8")
    code = main(
        [
            "lint",
            "--schema",
            str(schema),
            "--env-file",
            str(env_file),
            "--strict",
        ]
    )
    assert code == 1

