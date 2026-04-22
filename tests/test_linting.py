from pathlib import Path

from dotenv_linter_plus.linting import lint_env


def test_lint_success(tmp_path: Path):
    schema = tmp_path / ".env.schema.json"
    env_file = tmp_path / ".env"
    schema.write_text(
        '{"keys":{"PORT":{"type":"int","required":true},"DEBUG":{"type":"bool","required":true}}}',
        encoding="utf-8",
    )
    env_file.write_text("PORT=8080\nDEBUG=true\n", encoding="utf-8")
    report = lint_env(schema, env_file)
    assert report["ok"] is True
    assert report["errors"] == []


def test_lint_missing_required(tmp_path: Path):
    schema = tmp_path / ".env.schema.json"
    env_file = tmp_path / ".env"
    schema.write_text('{"keys":{"PORT":{"type":"int","required":true}}}', encoding="utf-8")
    env_file.write_text("", encoding="utf-8")
    report = lint_env(schema, env_file)
    assert report["ok"] is False
    assert "Missing required key: PORT" in report["errors"][0]
