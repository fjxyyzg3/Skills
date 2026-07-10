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
DEFAULT_PROMPT_RE = re.compile(r'^\s*default_prompt:\s*"[^"]+"\s*$', re.MULTILINE)
PLAIN_SCALAR_WITH_MAPPING_RE = re.compile(r"^[^'\"|>].*:\s+.+")
BAD_TEXT = ("[TODO", "TODO:", "placeholder", "\ufffd")
STALE_WORKFLOW_TEXT = (
    "Next Skill Gate",
    "不算确认",
    "explicit only",
    "explicit-only",
    "手动触发边界",
    "只能由用户手动调用",
    "手动调用后",
    "只建议用户显式调用",
    "Current skill result",
    "Recommended next skill",
    "Controlled chain mode",
    "User confirmation required",
    "Stop rule",
    "allow_implicit_invocation: false",
    "to-prd",
    "to-issues",
)
LANGUAGE_CONTRACT_MARKER = (
    "语言契约：生成的文档和聊天输出默认以中文优先；"
    "代码、命令、API 名称、契约字段、ID、专有名词以及必要的技术术语保留英文。"
)
LANGUAGE_CONTRACT_EXCEPTION = "用户或目标项目明确要求英文时可以例外，但必须记录原因。"
GRILL_ME_REQUIRED_TEXT = (
    "## 完成条件",
    "关键 upstream constraints",
    "用户同意方案方向只表示可以继续细化",
    "仍有关键问题未收束时",
    "不要用 `Natural Handoff` 推荐 next skill",
    "## Natural Handoff",
    "推荐 `$to-spec`",
    "推荐 `$to-plan`",
    "推荐 `$quick-change` 或 `$implement`",
    "推荐 `none`",
)
ADAPTIVE_PLANNING_REQUIRED_TEXT = {
    "to-plan/SKILL.md": (
        "Planning Authorization",
        "Fast Path",
        "Full Path",
        "Artifact-fixable",
        "Decision-required",
        "Planning Quality Status",
    ),
    "to-plan/references/adaptive-planning-contract.md": (
        "PlanningAuthorization",
        "RiskDecision",
        "PlanningArtifactSet",
        "FindingClass",
        "PlanningQualityResult",
        "CheckedPlanHandoff",
    ),
    "to-plan/examples/adaptive-planning-scenarios.md": (
        "AP-FAST",
        "AP-FULL",
        "AP-AUTOFIX",
        "AP-DECISION",
        "AP-DIRECT-SPEC",
        "AP-DIRECT-ANALYZE",
        "AP-AUTH-BOUNDARY",
        "Input shape",
        "Expected mode",
        "Expected artifacts",
        "Allowed interruption",
        "Forbidden actions",
        "Pass signal",
    ),
    "brainstorming/SKILL.md": (
        "## Trigger Description",
        "## Pressure Scenarios",
        "## Natural Handoff",
        "PlanningHandoffPacket v1",
        "implementation-plan",
        "spec-only",
        "stop-here",
        "$to-plan",
        "$to-spec",
    ),
    "implement/SKILL.md": (
        "## Trigger Description",
        "## Pressure Scenarios",
        "CheckedPlanHandoff",
        "Planning Quality Status: Pass",
        "external artifacts",
        "N1 Branch Gate",
        "N5 Review Subagent Gate",
        "N7 Verification Gate",
    ),
    "workflow-router/SKILL.md": (
        "## Trigger Description",
        "## Pressure Scenarios",
        "已确认设计",
        "正式 spec",
        "已有或外部 artifacts",
        "checked plan",
    ),
    "to-spec/SKILL.md": (
        "## Trigger Description",
        "## Pressure Scenarios",
        "## Natural Handoff",
        "独立 formal-spec",
    ),
    "analyze/SKILL.md": (
        "## Trigger Description",
        "## Pressure Scenarios",
        "## Natural Handoff",
        "独立只读审计",
    ),
    "README.md": (
        "Planning Authorization",
        "Fast Path",
        "Full Path",
        "checked plan",
        "独立 `$to-spec`",
        "独立 `$analyze`",
    ),
    "AGENTS.md": (
        "Planning Authorization",
        "Fast Path",
        "Full Path",
        "Planning Quality Status: Pass",
    ),
}
ADAPTIVE_PLANNING_STALE_TEXT = (
    "$to-spec -> $to-plan -> $analyze",
    "`to-spec` → `to-plan` → `analyze`",
    'Spec["to-spec"] --> Plan["to-plan"]',
    'Plan["to-plan"] --> Analyze',
    "prepare a spec handoff for $to-spec",
    "准备 to-spec 交接内容",
    "因为后续还需要拆 plan",
)


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
            key = match.group(1)
            value = match.group(2).strip()
            if PLAIN_SCALAR_WITH_MAPPING_RE.match(value):
                raise ValueError(f"{key} contains ': ' and must be quoted")
            fields[key] = value
    raise ValueError("missing closing YAML frontmatter marker")


def has_bad_text(text: str) -> list[str]:
    return [token for token in BAD_TEXT if token in text]


def has_stale_workflow_text(text: str) -> list[str]:
    lowered = text.lower()
    return [token for token in STALE_WORKFLOW_TEXT if token.lower() in lowered]


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
    for token in has_stale_workflow_text(text):
        errors.append(f"{skill_path.relative_to(ROOT)}: contains stale workflow text {token!r}")
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
    if not DEFAULT_PROMPT_RE.search(agents_text):
        errors.append(f"{agents_path.relative_to(ROOT)}: default_prompt must be a single quoted line")
    for token in has_bad_text(agents_text):
        errors.append(f"{agents_path.relative_to(ROOT)}: contains {token!r}")
    for token in has_stale_workflow_text(agents_text):
        errors.append(f"{agents_path.relative_to(ROOT)}: contains stale workflow text {token!r}")

    return errors


def validate_workflow_contract() -> list[str]:
    errors: list[str] = []
    workflow_router = ROOT / "workflow-router" / "SKILL.md"
    try:
        router_text = read_text(workflow_router)
    except ValueError as exc:
        return [f"{workflow_router.relative_to(ROOT)}: {exc}"]

    required_router_text = (
        "## Natural Handoff",
        "继续",
        "可以",
        "按你说的办",
        "go ahead",
        "ok",
        "好的",
    )
    for required in required_router_text:
        if required not in router_text:
            errors.append(f"{workflow_router.relative_to(ROOT)}: missing Natural Handoff marker {required!r}")

    for doc_name in ("README.md", "AGENTS.md"):
        doc_path = ROOT / doc_name
        try:
            doc_text = read_text(doc_path)
        except ValueError as exc:
            errors.append(f"{doc_name}: {exc}")
            continue
        if "Natural Handoff" not in doc_text:
            errors.append(f"{doc_name}: missing Natural Handoff workflow contract")
        for token in has_stale_workflow_text(doc_text):
            errors.append(f"{doc_name}: contains stale workflow text {token!r}")

    return errors


def validate_grill_me_contract() -> list[str]:
    errors: list[str] = []
    grill_me_path = ROOT / "grill-me" / "SKILL.md"
    try:
        grill_me_text = read_text(grill_me_path)
    except ValueError as exc:
        return [f"{grill_me_path.relative_to(ROOT)}: {exc}"]

    for required in GRILL_ME_REQUIRED_TEXT:
        if required not in grill_me_text:
            errors.append(f"{grill_me_path.relative_to(ROOT)}: missing grill-me contract marker {required!r}")

    return errors


def validate_adaptive_planning_contract() -> list[str]:
    errors: list[str] = []

    for display_path, required_markers in ADAPTIVE_PLANNING_REQUIRED_TEXT.items():
        path = (ROOT / display_path).resolve()
        try:
            text = read_text(path)
        except (OSError, ValueError) as exc:
            errors.append(f"{display_path}: {exc}")
            continue

        for marker in required_markers:
            if marker not in text:
                errors.append(f"{display_path}: missing adaptive planning marker {marker!r}")

    active_paths = (
        "to-plan/SKILL.md",
        "brainstorming/SKILL.md",
        "brainstorming/agents/openai.yaml",
        "to-spec/SKILL.md",
        "analyze/SKILL.md",
        "implement/SKILL.md",
        "quick-change/SKILL.md",
        "workflow-router/SKILL.md",
        "README.md",
        "AGENTS.md",
    )
    for display_path in active_paths:
        path = (ROOT / display_path).resolve()
        try:
            text = read_text(path)
        except (OSError, ValueError) as exc:
            errors.append(f"{display_path}: {exc}")
            continue
        lowered = text.lower()
        for stale in ADAPTIVE_PLANNING_STALE_TEXT:
            if stale.lower() in lowered:
                errors.append(f"{display_path}: contains stale adaptive planning text {stale!r}")

    return errors


def main() -> int:
    skill_dirs = sorted(
        path for path in ROOT.iterdir()
        if path.is_dir() and (path / "SKILL.md").exists()
    )

    errors: list[str] = []
    for skill_dir in skill_dirs:
        errors.extend(validate_skill(skill_dir))
    errors.extend(validate_workflow_contract())
    errors.extend(validate_grill_me_contract())
    errors.extend(validate_adaptive_planning_contract())

    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(skill_dirs)} skills.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
