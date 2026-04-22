import argparse
import json
from pathlib import Path

from dotenv_linter_plus.linting import lint_env


DEFAULT_SCHEMA = {
    "keys": {
        "APP_ENV": {"type": "string", "required": True},
        "DEBUG": {"type": "bool", "required": True},
        "PORT": {"type": "int", "required": True},
    }
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dotenv-linter-plus",
        description="Schema-aware .env validator with CI-friendly output.",
    )
    sub = parser.add_subparsers(dest="command")

    lint = sub.add_parser("lint", help="Validate env file against schema")
    lint.add_argument("--schema", default=".env.schema.json")
    lint.add_argument("--env-file", default=".env")
    lint.add_argument("--allow-extra", action="store_true")
    lint.add_argument("--strict", action="store_true")
    lint.add_argument("--format", choices=("text", "json"), default="text")

    init = sub.add_parser("init-schema", help="Create starter schema file")
    init.add_argument("--output", default=".env.schema.json")
    init.add_argument("--force", action="store_true")

    return parser


def _render_text(report: dict) -> str:
    lines = [
        f"Schema: {report['schema_path']}",
        f"Env: {report['env_path']}",
        f"Status: {'ok' if report['ok'] else 'failed'}",
        f"Checked keys: {report['checked_keys']}",
    ]
    if report["errors"]:
        lines.append("Errors:")
        lines.extend([f"- {err}" for err in report["errors"]])
    if report["warnings"]:
        lines.append("Warnings:")
        lines.extend([f"- {warn}" for warn in report["warnings"]])
    return "\n".join(lines)


def _init_schema(output: Path, force: bool) -> tuple[bool, str]:
    if output.exists() and not force:
        return False, f"{output} already exists. Use --force to overwrite."
    output.write_text(json.dumps(DEFAULT_SCHEMA, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return True, f"Schema created: {output}"


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "init-schema":
        ok, msg = _init_schema(Path(args.output), args.force)
        print(msg)
        return 0 if ok else 1
    if args.command == "lint":
        report = lint_env(
            Path(args.schema),
            Path(args.env_file),
            allow_extra=args.allow_extra,
        )
        if args.format == "json":
            print(json.dumps(report, ensure_ascii=True))
        else:
            print(_render_text(report))
        if args.strict and (report["errors"] or report["warnings"]):
            return 1
        return 0 if report["ok"] else 1
    build_parser().print_help()
    return 1

