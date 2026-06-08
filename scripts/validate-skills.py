#!/usr/bin/env python3
"""Validate local Codex skill structure without external dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAME_RE = re.compile(r"^[a-z0-9-]+$")
FIELD_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")
SHORT_DESCRIPTION_RE = re.compile(r'short_description:\s*"([^"]+)"')
BAD_TEXT = ("[TODO", "TODO:", "placeholder", "\ufffd")
LANGUAGE_CONTRACT_MARKER = (
    "Language Contract: generated documents and chat outputs default to Chinese-first; "
    "preserve English for code, commands, API names, contract fields, IDs, proper nouns, "
    "and necessary technical terms."
)
LANGUAGE_CONTRACT_EXCEPTION = "用户或目标项目明确要求英文时可以例外，但必须记录原因。"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"not valid UTF-8: {exc}") from exc


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening YAML frontmatter marker")
    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        match = FIELD_RE.match(line)
        if match:
            fields[match.group(1)] = match.group(2).strip()
    raise ValueError("missing closing YAML frontmatter marker")


def has_bad_text(text: str) -> list[str]:
    return [token for token in BAD_TEXT if token in text]


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_path = skill_dir / "SKILL.md"

    try:
        text = read_text(skill_path)
        fields = parse_frontmatter(text)
    except ValueError as exc:
        return [f"{skill_path.relative_to(ROOT)}: {exc}"]

    name = fields.get("name", "")
    description = fields.get("description", "")

    if name != skill_dir.name:
        errors.append(f"{skill_path.relative_to(ROOT)}: name '{name}' must match folder '{skill_dir.name}'")
    if not NAME_RE.match(name):
        errors.append(f"{skill_path.relative_to(ROOT)}: invalid skill name '{name}'")
    if not description or description.startswith("["):
        errors.append(f"{skill_path.relative_to(ROOT)}: missing description")
    if len(description) > 1024:
        errors.append(f"{skill_path.relative_to(ROOT)}: description exceeds 1024 characters")

    for token in has_bad_text(text):
        errors.append(f"{skill_path.relative_to(ROOT)}: contains {token!r}")
    if LANGUAGE_CONTRACT_MARKER not in text:
        errors.append(f"{skill_path.relative_to(ROOT)}: missing Language Contract marker")
    if LANGUAGE_CONTRACT_EXCEPTION not in text:
        errors.append(f"{skill_path.relative_to(ROOT)}: missing Language Contract exception rule")

    agents_path = skill_dir / "agents" / "openai.yaml"
    if not agents_path.exists():
        errors.append(f"{agents_path.relative_to(ROOT)}: missing agents metadata")
        return errors

    try:
        agents_text = read_text(agents_path)
    except ValueError as exc:
        errors.append(f"{agents_path.relative_to(ROOT)}: {exc}")
        return errors

    for required in ("display_name:", "short_description:", "default_prompt:"):
        if required not in agents_text:
            errors.append(f"{agents_path.relative_to(ROOT)}: missing {required}")
    short_match = SHORT_DESCRIPTION_RE.search(agents_text)
    if short_match:
        short_len = len(short_match.group(1))
        if short_len < 25 or short_len > 64:
            errors.append(
                f"{agents_path.relative_to(ROOT)}: short_description length must be 25-64 characters "
                f"(got {short_len})"
            )
    if f"${name}" not in agents_text:
        errors.append(f"{agents_path.relative_to(ROOT)}: default_prompt should mention ${name}")
    for token in has_bad_text(agents_text):
        errors.append(f"{agents_path.relative_to(ROOT)}: contains {token!r}")

    return errors


def main() -> int:
    skill_dirs = sorted(
        path for path in ROOT.iterdir()
        if path.is_dir() and (path / "SKILL.md").exists()
    )

    errors: list[str] = []
    for skill_dir in skill_dirs:
        errors.extend(validate_skill(skill_dir))

    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(skill_dirs)} skills.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
