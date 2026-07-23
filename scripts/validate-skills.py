#!/usr/bin/env python3
"""Validate local Codex skill structure without external dependencies."""

from __future__ import annotations

import argparse
import hashlib
import json
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
GRILL_ME_REQUIRED_TEXT = (
    "## 完成条件",
    "关键 upstream constraints",
    "用户同意方案方向只表示可以继续细化",
    "仍有关键问题未收束时",
    "不得使用 `Natural Handoff` 推荐后续 skill",
    "推荐 `$to-spec`",
    "推荐 `$to-plan`",
    "推荐 `$implement`",
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
        "PlanningHandoffPacket v1",
        "implementation-plan",
        "spec-only",
        "stop-here",
        "$to-plan",
        "$to-spec",
    ),
    "implement/SKILL.md": (
        "CheckedPlanHandoff",
        "Planning Quality Status: Pass",
        "外部 artifacts",
        "N1 分支门",
        "N5 评审子 agent 门",
        "N7 验证门",
    ),
    "to-spec/SKILL.md": (
        "独立 formal-spec",
    ),
    "analyze/SKILL.md": (
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
CONSOLIDATION_REQUIRED_TEXT = {
    "implement/SKILL.md": (
        "ImplementationPathDecision v1",
        "Path: Quick | Standard | Blocked",
        "Quick Path",
        "Standard Path",
        "Quick→Standard",
        "IMP-QUICK",
        "IMP-STANDARD",
        "IMP-UPGRADE",
        "IMP-NO-REPRO",
        "IMP-NEEDS-PLAN",
        "IMP-NEEDS-DESIGN",
        "IMP-EXTERNAL-FAKE-PASS",
        "IMP-NATURAL-CONFIRM",
        "Q1 -- \"无可靠 signal\" --> HB",
        "Quick 文件或行为改变",
        "N1 分支门",
        "N5 评审子 agent 门",
        "N7 验证门",
        "$diagnose",
        "$to-plan",
        "$brainstorming",
    ),
    "implement/agents/openai.yaml": (
        "$implement",
        "Quick/Standard/Blocked",
    ),
    "implement/references/quick-path.md": (
        "ImplementationPathDecision v1",
        "对所有候选路径读取 decision schema",
        "Standard 不加载 Quick execution 细节",
        "## Qualification",
        "## Disqualifiers",
        "Scope:",
        "Acceptance:",
        "Verification:",
        "light self-review",
        "Quick→Standard",
        "10–15",
        "current/new branch",
        "N1 Branch Gate",
    ),
    "diagnose/SKILL.md": (
        "DiagnosticContext v1",
        "Profile: Generic | UE",
        "EvidenceMode: Active Repro | Artifact-based Triage",
        "Active Repro",
        "Artifact-based Triage",
        "RootCauseStatus",
        "references/ue/runtime-modes.md",
        "references/ue/probes-and-artifacts.md",
        "references/ue/regression-seams.md",
        "DGN-GENERIC-ACTIVE",
        "DGN-GENERIC-ARTIFACT",
        "DGN-UE-ACTIVE",
        "DGN-UE-ARTIFACT",
        "DGN-UE-MODE-DRIFT",
        "DGN-PERF-BASELINE",
        "DGN-HANDOFF",
        "pending — <target failure>",
        "不要进入 Phase 3 hypotheses",
        "初始 `RootCauseStatus` 只能为 `likely` 或 `blocked`",
        "Artifact-based Triage 必须明确“未复现”",
        "根因状态提升门",
        "因果干预",
        "证据指针",
        "$implement",
    ),
    "diagnose/agents/openai.yaml": (
        "$diagnose",
        "Generic/UE Profile",
        "Active Repro/Artifact-based Triage",
    ),
    "diagnose/references/ue/runtime-modes.md": (
        "## Runtime Parity",
        "Packaged",
        "network",
        "RHI",
    ),
    "diagnose/references/ue/probes-and-artifacts.md": (
        "## UE Hypothesis Dimensions",
        "## Artifact-based Triage",
        "不得使用 `RootCauseStatus: confirmed`",
        "只能为 `likely` 或 `blocked`",
        "[DEBUG-UE-*]",
        "纯 `.rdc` Caveat",
    ),
    "diagnose/references/ue/regression-seams.md": (
        "## Runtime Parity",
        "## Repair Handoff",
        "$implement",
    ),
    "diagnose/scripts/hitl-loop.template.sh": (
        "Human-in-the-loop reproduction loop.",
        "set -euo pipefail",
        "step()",
        "capture()",
    ),
    "checking-branch/SKILL.md": (
        "普通实现请求先进入 `$implement`",
        "内部 `N1 Branch Gate`",
        "branch-only",
    ),
    "checking-branch/agents/openai.yaml": (
        "$checking-branch",
        "branch-only",
    ),
    "README.md": (
        "Quick / Standard / Blocked",
        "进入 `$implement` Standard",
        "N3 Analyze Gate",
        "Generic/UE Profile",
        "Natural Handoff",
    ),
    "AGENTS.md": (
        "Quick/Standard/Blocked",
        "进入 `$implement` Standard",
        "N3 Analyze Gate",
        "Natural Handoff",
    ),
}
RETIRED_SKILL_NAMES = ("quick-change", "diagnose-ue", "workflow-router")
ACTIVE_ARTIFACT_SUFFIXES = {".html", ".md", ".sh", ".yaml", ".yml"}
ADAPTIVE_PLANNING_STALE_TEXT = (
    "$to-spec -> $to-plan -> $analyze",
    "`to-spec` → `to-plan` → `analyze`",
    'Spec["to-spec"] --> Plan["to-plan"]',
    'Plan["to-plan"] --> Analyze',
    "prepare a spec handoff for $to-spec",
    "准备 to-spec 交接内容",
    "因为后续还需要拆 plan",
)
STABLE_BILINGUAL_HEADINGS = {
    "Trigger Description": "## 触发说明（Trigger Description）",
    "Pressure Scenarios": "## 压力场景（Pressure Scenarios）",
    "Natural Handoff": "## 自然交接（Natural Handoff）",
}
SKILL_HEADING_INVENTORY = {
    "analyze": frozenset(STABLE_BILINGUAL_HEADINGS),
    "brainstorming": frozenset(STABLE_BILINGUAL_HEADINGS),
    "checking-branch": frozenset(STABLE_BILINGUAL_HEADINGS),
    "clarify": frozenset(),
    "diagnose": frozenset(STABLE_BILINGUAL_HEADINGS),
    "finishing-branch": frozenset(),
    "grill-me": frozenset({"Natural Handoff"}),
    "handoff": frozenset(),
    "implement": frozenset(STABLE_BILINGUAL_HEADINGS),
    "improve-codebase-architecture": frozenset({"Pressure Scenarios"}),
    "requesting-code-review": frozenset(),
    "session-curator": frozenset({"Pressure Scenarios"}),
    "tdd": frozenset({"Pressure Scenarios"}),
    "to-plan": frozenset(STABLE_BILINGUAL_HEADINGS),
    "to-spec": frozenset(STABLE_BILINGUAL_HEADINGS),
    "verification-before-completion": frozenset(),
}
HAN_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
TRAILING_WHITESPACE_RE = re.compile(r"(?m)[ \t]+$")
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
MARKDOWN_LINK_TARGET_RE = re.compile(r"\]\([^)]+\)")
BILINGUAL_HEADING_ALIAS_RE = re.compile(
    r"(?:\([^)\n]*[A-Za-z][^)\n]*\)|（[^）\n]*[A-Za-z][^）\n]*）)"
)
ENGLISH_PROSE_RE = re.compile(
    r"\b[A-Za-z][A-Za-z0-9/&+-]*(?:[ \t]+[A-Za-z][A-Za-z0-9/&+-]*){4,}\b"
)
ROUTING_CASE_REQUIRED = {
    "CaseId",
    "Skill",
    "CaseKind",
    "PromptLanguage",
    "LiveRequired",
    "ExpectedOwner",
    "ExpectedGate",
    "ForbiddenOwnerOrAction",
    "Prompt",
    "TriggerPhraseRef",
    "BoundaryRef",
    "StaticResult",
    "LiveResult",
    "Notes",
}
SKILL_INVENTORY_REQUIRED = {"Name", "H1", "Source"}
ROUTE_INVARIANT_REQUIRED = {
    "EdgeId",
    "SourceSkill",
    "TargetSkill",
    "Pattern",
    "BaselineCount",
    "Condition",
    "StopBoundary",
    "BaselineEvidence",
    "FinalEvidence",
}
STABLE_TOKEN_REQUIRED = {
    "Skill",
    "Category",
    "Token",
    "BaselineCount",
    "FinalCount",
    "Evidence",
}
NORMATIVE_INVARIANT_REQUIRED = {
    "Skill",
    "Constraint",
    "BaselineEvidence",
    "FinalEvidence",
    "Result",
}
REVIEW_REQUIRED = {
    "ReviewId",
    "File",
    "LineOrSection",
    "Fragment",
    "Category",
    "KeepOrTranslate",
    "Rationale",
    "RoutingCase",
    "Reviewer",
    "Result",
}
SMOKE_REQUIRED = {
    "CaseId",
    "Skill",
    "PromptLanguage",
    "Prompt",
    "ExpectedOwner",
    "ExpectedGate",
    "ForbiddenOwnerOrAction",
    "CandidateLocator",
    "GlobalLocatorDisabled",
    "ObservedOwner",
    "ObservedGate",
    "ForbiddenActionTaken",
    "EventsSha256",
    "ControlEventsSha256",
    "ReadObservationAvailable",
    "ReadEvent",
    "ObservationFailure",
    "MutationEventCount",
    "Result",
    "Notes",
}
CANDIDATE_PROOF_REQUIRED = {
    "Name",
    "DiscoveryJunction",
    "CandidateLocator",
    "ModelVisibleLocator",
    "GlobalLocator",
    "GlobalDisabled",
    "PromptInputSha256",
    "CandidateSha256",
}
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
LOCALIZATION_BASELINE_PATH = (
    ROOT
    / "docs"
    / "features"
    / "skill-content-chinese-localization"
    / "baseline-snapshot.json"
)
LOCALIZATION_MANIFEST_PATH = LOCALIZATION_BASELINE_PATH.with_name("manifest.md")
LOCALIZATION_BASELINE_SHA256 = (
    "2f9a510349e607ba1b60cd7e7e6a0c86d27a43fc6fb2f26105932fb83d4e0b10"
)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"not valid UTF-8: {exc}") from exc


def read_strict_artifact(path: Path) -> tuple[str | None, list[str]]:
    errors: list[str] = []
    try:
        data = path.read_bytes()
    except OSError as exc:
        return None, [f"E_ARTIFACT_READ {path}: {exc}"]

    if data.startswith(b"\xef\xbb\xbf"):
        errors.append(f"E_BOM {path}: UTF-8 BOM is not allowed")
    if b"\r" in data:
        errors.append(f"E_CRLF {path}: only LF newlines are allowed")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        return None, errors + [f"E_UTF8 {path}: {exc}"]
    if TRAILING_WHITESPACE_RE.search(text):
        errors.append(f"E_TRAILING {path}: trailing whitespace is not allowed")
    return text, errors


def parse_jsonl_block(
    text: str,
    marker: str,
    artifact_path: Path,
) -> tuple[list[dict[str, object]], list[str]]:
    begin = f"<!-- {marker}_BEGIN -->"
    end = f"<!-- {marker}_END -->"
    errors: list[str] = []
    if text.count(begin) != 1 or text.count(end) != 1:
        return [], [
            f"E_MARKER {artifact_path}: expected exactly one {begin!r} and {end!r}"
        ]
    body = text.split(begin, 1)[1].split(end, 1)[0]
    records: list[dict[str, object]] = []
    for line_number, line in enumerate(body.splitlines(), 1):
        stripped = line.strip()
        if not stripped:
            continue
        if not stripped.startswith("{"):
            errors.append(
                f"E_JSONL {artifact_path}:{line_number}: non-empty block line is not JSON"
            )
            continue
        try:
            value = json.loads(stripped)
        except json.JSONDecodeError as exc:
            errors.append(f"E_JSONL {artifact_path}:{line_number}: {exc}")
            continue
        if not isinstance(value, dict):
            errors.append(
                f"E_JSONL {artifact_path}:{line_number}: record must be an object"
            )
            continue
        records.append(value)
    return records, errors


def resolve_repo_path(value: object) -> tuple[Path | None, str | None]:
    if not isinstance(value, str) or not value:
        return None, "path must be a non-empty string"
    candidate = Path(value)
    path = candidate.resolve() if candidate.is_absolute() else (ROOT / candidate).resolve()
    try:
        path.relative_to(ROOT)
    except ValueError:
        return None, f"path escapes repository: {value}"
    return path, None


def normalized_path(value: object) -> str:
    return str(Path(str(value)).resolve()).replace("/", "\\").casefold()


def english_heavy_candidates(path: Path) -> list[dict[str, object]]:
    text = read_text(path)
    try:
        display_path = path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        display_path = str(path.resolve())

    candidates: list[dict[str, object]] = []
    in_fence = False
    canonical_h1_seen = False
    for line_number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence or not stripped or line.startswith(("    ", "\t", "<!--")):
            continue
        if stripped.startswith("# ") and not canonical_h1_seen:
            canonical_h1_seen = True
            continue

        visible = INLINE_CODE_RE.sub("", stripped)
        visible = MARKDOWN_LINK_TARGET_RE.sub("]", visible).strip()
        if not visible:
            continue

        fragment: str | None = None
        if visible.startswith("##") and not HAN_RE.search(visible):
            fragment = visible.lstrip("#").strip()
        elif not HAN_RE.search(visible) and ENGLISH_PROSE_RE.search(visible):
            fragment = visible
        else:
            match = ENGLISH_PROSE_RE.search(visible)
            if match:
                fragment = match.group(0)

        if fragment:
            candidates.append(
                {
                    "File": display_path,
                    "LineOrSection": str(line_number),
                    "Fragment": fragment,
                }
            )
    return candidates


def run_english_heavy_audit(arguments: list[str]) -> int:
    if arguments:
        paths = [
            path.resolve() if path.is_absolute() else (ROOT / path).resolve()
            for path in map(Path, arguments)
        ]
    else:
        paths = sorted(ROOT.glob("*/SKILL.md"))

    candidates: list[dict[str, object]] = []
    errors: list[str] = []
    for path in paths:
        if not path.is_file():
            errors.append(f"E_AUDIT_PATH {path}: file does not exist")
            continue
        try:
            candidates.extend(english_heavy_candidates(path))
        except (OSError, ValueError) as exc:
            errors.append(f"E_AUDIT_READ {path}: {exc}")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    candidates.sort(
        key=lambda item: (
            str(item["File"]),
            int(str(item["LineOrSection"])),
            str(item["Fragment"]),
        )
    )
    print(f"English-heavy review candidates: {len(candidates)}")
    for candidate in candidates:
        print(json.dumps(candidate, ensure_ascii=False, sort_keys=True))
    return 0


def require_keys(
    records: list[dict[str, object]],
    required: set[str],
    kind: str,
) -> list[str]:
    errors: list[str] = []
    for index, record in enumerate(records, 1):
        missing = required - record.keys()
        if missing:
            errors.append(
                f"E_REQUIRED_FIELD {kind}[{index}]: missing {sorted(missing)}"
            )
    return errors


def validate_localization_evidence(
    matrix_path: Path,
    ledger_path: Path,
    scoped_names: list[str] | None,
    require_static_pass: bool,
    require_live_resolved: bool,
) -> list[str]:
    errors: list[str] = []
    matrix_text, matrix_errors = read_strict_artifact(matrix_path)
    ledger_text, ledger_errors = read_strict_artifact(ledger_path)
    errors.extend(matrix_errors)
    errors.extend(ledger_errors)
    if matrix_text is None or ledger_text is None:
        return errors

    inventory, block_errors = parse_jsonl_block(
        matrix_text, "SKILL_INVENTORY", matrix_path
    )
    errors.extend(block_errors)
    cases, block_errors = parse_jsonl_block(matrix_text, "ROUTING_CASES", matrix_path)
    errors.extend(block_errors)
    routes, block_errors = parse_jsonl_block(
        matrix_text, "ROUTE_INVARIANTS", matrix_path
    )
    errors.extend(block_errors)
    stable_tokens, block_errors = parse_jsonl_block(
        matrix_text, "STABLE_TOKEN_INVARIANTS", matrix_path
    )
    errors.extend(block_errors)
    normative, block_errors = parse_jsonl_block(
        matrix_text, "NORMATIVE_INVARIANTS", matrix_path
    )
    errors.extend(block_errors)
    candidate_proof, block_errors = parse_jsonl_block(
        matrix_text, "CANDIDATE_SOURCE_PROOF", matrix_path
    )
    errors.extend(block_errors)
    smoke, block_errors = parse_jsonl_block(
        matrix_text, "CANDIDATE_SOURCE_SMOKE", matrix_path
    )
    errors.extend(block_errors)
    reviews, block_errors = parse_jsonl_block(
        ledger_text, "ENGLISH_REVIEW", ledger_path
    )
    errors.extend(block_errors)

    errors.extend(require_keys(inventory, SKILL_INVENTORY_REQUIRED, "SkillInventory"))
    errors.extend(require_keys(cases, ROUTING_CASE_REQUIRED, "RoutingCase"))
    errors.extend(require_keys(routes, ROUTE_INVARIANT_REQUIRED, "RouteInvariant"))
    errors.extend(
        require_keys(stable_tokens, STABLE_TOKEN_REQUIRED, "StableTokenInvariant")
    )
    errors.extend(
        require_keys(
            normative,
            NORMATIVE_INVARIANT_REQUIRED,
            "NormativeConstraintInvariant",
        )
    )
    errors.extend(require_keys(reviews, REVIEW_REQUIRED, "EnglishHeavyReview"))
    errors.extend(
        require_keys(
            candidate_proof,
            CANDIDATE_PROOF_REQUIRED,
            "CandidateSourceProof",
        )
    )
    errors.extend(require_keys(smoke, SMOKE_REQUIRED, "CandidateSourceSmoke"))
    if errors:
        return errors

    skill_dirs = sorted(
        path
        for path in ROOT.iterdir()
        if path.is_dir() and (path / "SKILL.md").exists()
    )
    actual_skills = {path.name for path in skill_dirs}
    baseline_h1: dict[str, str] = {}
    try:
        baseline_bytes = LOCALIZATION_BASELINE_PATH.read_bytes()
        baseline_digest = hashlib.sha256(baseline_bytes).hexdigest()
        if baseline_digest != LOCALIZATION_BASELINE_SHA256:
            errors.append(
                "E_BASELINE_DIGEST localization baseline snapshot hash mismatch"
            )
        baseline_snapshot = json.loads(baseline_bytes.decode("utf-8"))
        baseline_inventory = baseline_snapshot.get("SkillInventory")
        if not isinstance(baseline_inventory, list):
            errors.append("E_BASELINE_INVENTORY SkillInventory must be a list")
        else:
            for entry in baseline_inventory:
                if (
                    not isinstance(entry, dict)
                    or not isinstance(entry.get("Name"), str)
                    or not isinstance(entry.get("H1"), str)
                ):
                    errors.append(
                        "E_BASELINE_INVENTORY every entry requires string Name and H1"
                    )
                    continue
                name = str(entry["Name"])
                if name in baseline_h1:
                    errors.append(
                        f"E_BASELINE_INVENTORY duplicate baseline skill {name!r}"
                    )
                    continue
                baseline_h1[name] = str(entry["H1"])
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f"E_BASELINE_READ {LOCALIZATION_BASELINE_PATH}: {exc}")

    try:
        manifest_text = read_text(LOCALIZATION_MANIFEST_PATH)
        manifest_anchors = re.findall(
            r"(?m)^- Baseline Snapshot SHA-256: `([0-9a-f]{64})`$",
            manifest_text,
        )
        if manifest_anchors != [LOCALIZATION_BASELINE_SHA256]:
            errors.append(
                "E_BASELINE_ANCHOR manifest must contain the canonical baseline digest"
            )
    except (OSError, ValueError) as exc:
        errors.append(f"E_BASELINE_READ {LOCALIZATION_MANIFEST_PATH}: {exc}")

    if baseline_h1 and set(baseline_h1) != actual_skills:
        errors.append(
            "E_BASELINE_INVENTORY baseline skill set does not match filesystem: "
            f"baseline={sorted(baseline_h1)} filesystem={sorted(actual_skills)}"
        )

    inventory_name_list = [str(item["Name"]) for item in inventory]
    inventory_names = set(inventory_name_list)
    if len(inventory_name_list) != len(inventory_names):
        errors.append("E_INVENTORY duplicate skill Name")
    if inventory_names != actual_skills:
        errors.append(
            "E_INVENTORY matrix inventory does not match filesystem: "
            f"matrix={sorted(inventory_names)} filesystem={sorted(actual_skills)}"
        )
    if len(inventory) != len(actual_skills):
        errors.append(
            "E_INVENTORY matrix inventory count does not match filesystem: "
            f"matrix={len(inventory)} filesystem={len(actual_skills)}"
        )
    for item in inventory:
        name = str(item["Name"])
        if name not in actual_skills:
            continue
        expected_source = f"{name}/SKILL.md"
        if item["Source"] != expected_source:
            errors.append(
                f"E_INVENTORY_SOURCE {name}: expected {expected_source!r}, "
                f"got {item['Source']!r}"
            )
        skill_text = read_text(ROOT / expected_source)
        current_h1 = next(
            (
                line[2:].strip()
                for line in skill_text.splitlines()
                if line.startswith("# ")
            ),
            "",
        )
        if item["H1"] != current_h1:
            errors.append(
                f"E_INVENTORY_H1 {name}: expected {item['H1']!r}, "
                f"got {current_h1!r}"
            )
        baseline_expected_h1 = baseline_h1.get(name)
        if baseline_expected_h1 is not None and item["H1"] != baseline_expected_h1:
            errors.append(
                f"E_BASELINE_H1 {name}: matrix H1 {item['H1']!r} differs from "
                f"baseline {baseline_expected_h1!r}"
            )
        if baseline_expected_h1 is not None and current_h1 != baseline_expected_h1:
            errors.append(
                f"E_BASELINE_H1 {name}: current H1 {current_h1!r} differs from "
                f"baseline {baseline_expected_h1!r}"
            )

    scope = set(scoped_names or sorted(actual_skills))
    unknown_scope = scope - actual_skills
    if unknown_scope:
        errors.append(f"E_SCOPE unknown skills: {sorted(unknown_scope)}")

    case_ids: list[str] = []
    allowed_kinds = {"ZH-positive", "EN-positive", "near-miss"}
    case_by_id: dict[str, dict[str, object]] = {}
    for case in cases:
        case_id = str(case["CaseId"])
        skill = str(case["Skill"])
        kind = str(case["CaseKind"])
        case_ids.append(case_id)
        case_by_id[case_id] = case
        if skill not in actual_skills:
            errors.append(f"E_CASE_SKILL {case_id}: unknown skill {skill!r}")
        if kind not in allowed_kinds:
            errors.append(f"E_CASE_KIND {case_id}: invalid CaseKind {kind!r}")
        if kind in {"ZH-positive", "EN-positive"}:
            if case["ExpectedOwner"] != skill:
                errors.append(
                    f"E_OWNER_RELATION {case_id}: positive ExpectedOwner must equal Skill"
                )
        elif kind == "near-miss" and case["ExpectedOwner"] == skill:
            errors.append(
                f"E_OWNER_RELATION {case_id}: near-miss ExpectedOwner must differ from Skill"
            )
    if len(case_ids) != len(set(case_ids)):
        errors.append("E_CASE_ID duplicate CaseId")
    if len(cases) != len(actual_skills) * len(allowed_kinds):
        errors.append(
            f"E_CASE_COVERAGE expected {len(actual_skills) * len(allowed_kinds)} "
            f"cases, got {len(cases)}"
        )
    for skill in actual_skills:
        owned_cases = [
            case
            for case in cases
            if str(case["Skill"]) == skill
        ]
        kinds = [str(case["CaseKind"]) for case in owned_cases]
        if len(owned_cases) != 3 or set(kinds) != allowed_kinds or len(kinds) != len(set(kinds)):
            errors.append(
                f"E_CASE_COVERAGE {skill}: expected one each of "
                f"{sorted(allowed_kinds)}, got {sorted(kinds)}"
            )

    review_ids = [str(review["ReviewId"]) for review in reviews]
    if len(review_ids) != len(set(review_ids)):
        errors.append("E_REVIEW_ID duplicate ReviewId")
    review_by_id = {str(review["ReviewId"]): review for review in reviews}
    for review in reviews:
        review_id = str(review["ReviewId"])
        disposition = review["KeepOrTranslate"]
        if disposition not in {"keep", "translate"}:
            errors.append(
                f"E_REVIEW_DISPOSITION {review_id}: expected keep or translate"
            )
        if disposition == "keep" and not str(review["Rationale"]).strip():
            errors.append(f"E_REVIEW_RATIONALE {review_id}: keep requires rationale")

    if require_static_pass:
        for case in cases:
            if str(case["Skill"]) in scope and case["StaticResult"] != "pass":
                errors.append(
                    f"E_STATIC_RESULT {case['CaseId']}: scoped case is not pass"
                )

        scoped_reviews = [
            review
            for review in reviews
            if str(review["File"]).split("/", 1)[0] in scope
        ]
        for review in scoped_reviews:
            review_id = str(review["ReviewId"])
            if review["Result"] != "pass":
                errors.append(
                    f"E_REVIEW_RESULT {review_id}: scoped review is not pass"
                )
            file_path, path_error = resolve_repo_path(review["File"])
            if path_error or file_path is None:
                errors.append(f"E_REVIEW_PATH {review_id}: {path_error}")
                continue
            try:
                current_text = read_text(file_path)
            except (OSError, ValueError) as exc:
                errors.append(f"E_REVIEW_PATH {review_id}: {exc}")
                continue
            if (
                review["KeepOrTranslate"] == "translate"
                and str(review["Fragment"]) in current_text
            ):
                errors.append(
                    f"E_TRANSLATION_PENDING {review_id}: translated fragment remains"
                )
            if (
                review["KeepOrTranslate"] == "keep"
                and str(review["Fragment"]) not in current_text
            ):
                errors.append(
                    f"E_REVIEW_FRAGMENT {review_id}: retained fragment is absent"
                )
            if (
                review["Category"] == "trigger-phrase"
                and review["KeepOrTranslate"] == "keep"
            ):
                case_id = str(review["RoutingCase"])
                case = case_by_id.get(case_id)
                if (
                    case is None
                    or case["CaseKind"] != "EN-positive"
                    or case["Skill"] != str(review["File"]).split("/", 1)[0]
                    or review_id not in str(case["TriggerPhraseRef"])
                ):
                    errors.append(
                        f"E_ENGLISH_TRACE {review_id}: missing bidirectional EN-positive trace"
                    )

        for case in cases:
            if str(case["Skill"]) not in scope or case["CaseKind"] != "EN-positive":
                continue
            references = [
                review_id
                for review_id in review_ids
                if review_id in str(case["TriggerPhraseRef"])
            ]
            valid = [
                review_id
                for review_id in references
                if review_by_id[review_id]["KeepOrTranslate"] == "keep"
                and review_by_id[review_id]["Result"] == "pass"
                and review_by_id[review_id]["RoutingCase"] == case["CaseId"]
            ]
            if not valid:
                errors.append(
                    f"E_ENGLISH_TRACE {case['CaseId']}: no passing retained-trigger review"
                )

        for skill in sorted(scope):
            try:
                audit_candidates = english_heavy_candidates(
                    ROOT / skill / "SKILL.md"
                )
            except (OSError, ValueError) as exc:
                errors.append(f"E_AUDIT_READ {skill}: {exc}")
                continue
            for candidate in audit_candidates:
                covered = any(
                    review["Result"] == "pass"
                    and review["KeepOrTranslate"] == "keep"
                    and review["File"] == candidate["File"]
                    and review["Fragment"] == candidate["Fragment"]
                    for review in scoped_reviews
                )
                if not covered:
                    errors.append(
                        "E_AUDIT_COVERAGE "
                        f"{candidate['File']}:{candidate['LineOrSection']}: "
                        f"{candidate['Fragment']!r}"
                    )

    route_ids = [str(route["EdgeId"]) for route in routes]
    if len(route_ids) != len(set(route_ids)):
        errors.append("E_ROUTE_ID duplicate EdgeId")
    for route in routes:
        skill = str(route["SourceSkill"])
        if skill not in scope:
            continue
        skill_text = read_text(ROOT / skill / "SKILL.md")
        section_match = re.search(
            r"(?m)^## (?:自然交接（Natural Handoff）|Natural Handoff)\s*$",
            skill_text,
        )
        if section_match is None:
            errors.append(
                f"E_ROUTE_SECTION {route['EdgeId']}: Natural Handoff section missing"
            )
            continue
        section = skill_text[section_match.end() :]
        next_heading = re.search(r"\n## ", section)
        if next_heading:
            section = section[: next_heading.start()]
        try:
            observed = len(re.findall(str(route["Pattern"]), section))
        except re.error as exc:
            errors.append(f"E_ROUTE_PATTERN {route['EdgeId']}: {exc}")
            continue
        if type(route["BaselineCount"]) is not int or observed != route["BaselineCount"]:
            errors.append(
                f"E_INVARIANT_COUNT {route['EdgeId']}: "
                f"observed={observed} baseline={route['BaselineCount']}"
            )
        if require_static_pass and not str(route["FinalEvidence"]).strip():
            errors.append(
                f"E_FINAL_EVIDENCE {route['EdgeId']}: FinalEvidence is required"
            )

    for invariant in stable_tokens:
        skill = str(invariant["Skill"])
        if skill not in scope:
            continue
        observed = read_text(ROOT / skill / "SKILL.md").count(str(invariant["Token"]))
        baseline_count = invariant["BaselineCount"]
        if type(baseline_count) is not int or observed != baseline_count:
            errors.append(
                f"E_INVARIANT_COUNT {skill}:{invariant['Token']}: "
                f"observed={observed} baseline={baseline_count}"
            )
        if require_static_pass:
            final_count = invariant["FinalCount"]
            if type(final_count) is not int or observed != final_count:
                errors.append(
                    f"E_INVARIANT_COUNT {skill}:{invariant['Token']}: "
                    f"observed={observed} final={final_count}"
                )

    for invariant in normative:
        skill = str(invariant["Skill"])
        if skill not in scope:
            continue
        baseline = invariant["BaselineEvidence"]
        if not isinstance(baseline, dict):
            errors.append(
                f"E_NORMATIVE_EVIDENCE {skill}: BaselineEvidence must be an object"
            )
            continue
        path, path_error = resolve_repo_path(baseline.get("Path"))
        if path_error or path is None:
            errors.append(f"E_NORMATIVE_PATH {skill}: {path_error}")
            continue
        try:
            observed = len(
                re.findall(str(baseline.get("Pattern", "")), read_text(path))
            )
        except re.error as exc:
            errors.append(f"E_NORMATIVE_PATTERN {skill}: {exc}")
            continue
        baseline_count = baseline.get("Count")
        if type(baseline_count) is not int or observed != baseline_count:
            errors.append(
                f"E_INVARIANT_COUNT {skill}:{invariant['Constraint']}: "
                f"observed={observed} baseline={baseline_count}"
            )
        if require_static_pass:
            final = invariant["FinalEvidence"]
            if (
                not isinstance(final, dict)
                or final.get("Path") != baseline.get("Path")
                or type(final.get("Count")) is not int
                or observed != final.get("Count")
                or invariant["Result"] != "pass"
            ):
                errors.append(
                    f"E_FINAL_EVIDENCE {skill}:{invariant['Constraint']}: "
                    "FinalEvidence/Result does not match current evidence"
                )

    if require_live_resolved:
        proof_names = [str(record["Name"]) for record in candidate_proof]
        if len(proof_names) != len(set(proof_names)):
            errors.append("E_SOURCE_PROOF duplicate candidate Name")
        proof_by_name = {
            str(record["Name"]): record
            for record in candidate_proof
        }
        if len(candidate_proof) != len(actual_skills):
            errors.append(
                "E_SOURCE_PROOF candidate proof count does not match filesystem: "
                f"proof={len(candidate_proof)} filesystem={len(actual_skills)}"
            )
        if set(proof_by_name) != actual_skills:
            errors.append(
                "E_SOURCE_PROOF candidate proof skill set does not match filesystem"
            )
        prompt_input_hashes: set[str] = set()
        for name, record in proof_by_name.items():
            if name not in actual_skills:
                continue
            candidate_path = (ROOT / name / "SKILL.md").resolve()
            candidate_locator = str(record["CandidateLocator"])
            if (
                not Path(candidate_locator).is_absolute()
                or normalized_path(candidate_locator)
                != normalized_path(candidate_path)
            ):
                errors.append(
                    f"E_SOURCE_PROOF {name}: candidate locator mismatch"
                )
            model_visible_locator = str(record["ModelVisibleLocator"])
            if (
                normalized_path(model_visible_locator)
                != normalized_path(candidate_path)
            ):
                errors.append(
                    f"E_SOURCE_PROOF {name}: model-visible locator mismatch"
                )
            candidate_hash = str(record["CandidateSha256"])
            current_hash = hashlib.sha256(candidate_path.read_bytes()).hexdigest()
            if (
                not HEX64_RE.fullmatch(candidate_hash)
                or candidate_hash != current_hash
            ):
                errors.append(
                    f"E_SOURCE_PROOF {name}: candidate hash mismatch"
                )
            prompt_hash = str(record["PromptInputSha256"])
            if not HEX64_RE.fullmatch(prompt_hash):
                errors.append(
                    f"E_SOURCE_PROOF {name}: invalid prompt-input hash"
                )
            else:
                prompt_input_hashes.add(prompt_hash)
            discovery_junction = Path(str(record["DiscoveryJunction"]))
            if (
                not discovery_junction.is_absolute()
                or discovery_junction.name != name
                or discovery_junction.parent.name != "skills"
                or discovery_junction.parent.parent.name != ".agents"
            ):
                errors.append(
                    f"E_SOURCE_PROOF {name}: invalid discovery junction locator"
                )
            global_locator = str(record["GlobalLocator"])
            if (
                not Path(global_locator).is_absolute()
                or normalized_path(global_locator)
                == normalized_path(candidate_path)
                or record["GlobalDisabled"] is not True
            ):
                errors.append(
                    f"E_SOURCE_PROOF {name}: invalid global-disable evidence"
                )
        if len(prompt_input_hashes) != 1:
            errors.append(
                "E_SOURCE_PROOF candidate records must share one prompt-input hash"
            )

        live_cases = {
            str(case["CaseId"]): case
            for case in cases
            if case["LiveRequired"] is True
        }
        required_live_skills = {
            "brainstorming",
            "grill-me",
            "to-plan",
            "to-spec",
            "analyze",
            "implement",
            "diagnose",
            "checking-branch",
        }
        if len(live_cases) != 16:
            errors.append(
                f"E_LIVE_COVERAGE expected 16 LiveRequired cases, got {len(live_cases)}"
            )
        if {str(case["Skill"]) for case in live_cases.values()} != required_live_skills:
            errors.append("E_LIVE_COVERAGE LiveRequired skill set mismatch")
        for skill in required_live_skills:
            owned = [
                case
                for case in live_cases.values()
                if case["Skill"] == skill
            ]
            kinds = [str(case["CaseKind"]) for case in owned]
            if (
                len(owned) != 2
                or kinds.count("near-miss") != 1
                or sum(kind in {"ZH-positive", "EN-positive"} for kind in kinds) != 1
            ):
                errors.append(
                    f"E_LIVE_COVERAGE {skill}: expected one positive and one near-miss"
                )
        positive_languages = {
            str(case["PromptLanguage"])
            for case in live_cases.values()
            if case["CaseKind"] in {"ZH-positive", "EN-positive"}
        }
        if not {"zh-CN", "en"} <= positive_languages:
            errors.append(
                "E_LIVE_COVERAGE positive live cases must include zh-CN and en"
            )

        smoke_ids = [str(record["CaseId"]) for record in smoke]
        if len(smoke_ids) != len(set(smoke_ids)):
            errors.append("E_LIVE_COVERAGE duplicate CandidateSourceSmoke CaseId")
        smoke_by_case = {str(record["CaseId"]): record for record in smoke}
        if smoke_by_case.keys() != live_cases.keys():
            errors.append(
                "E_LIVE_COVERAGE live smoke CaseIds do not match LiveRequired cases"
            )

        for case_id, case in live_cases.items():
            record = smoke_by_case.get(case_id)
            if record is None:
                continue
            expected_owner = str(case["ExpectedOwner"])
            if (
                record["Skill"] != case["Skill"]
                or record["PromptLanguage"] != case["PromptLanguage"]
                or record["Prompt"] != case["Prompt"]
                or record["ExpectedOwner"] != case["ExpectedOwner"]
                or record["ExpectedGate"] != case["ExpectedGate"]
                or record["ForbiddenOwnerOrAction"]
                != case["ForbiddenOwnerOrAction"]
            ):
                errors.append(f"E_LIVE_CASE {case_id}: smoke/case contract mismatch")
            if record["GlobalLocatorDisabled"] is not True:
                errors.append(f"E_LIVE_SOURCE {case_id}: global locator not disabled")
            if (
                record["ObservedOwner"] != expected_owner
                or not isinstance(record["ObservedGate"], str)
                or not str(record["ObservedGate"]).strip()
            ):
                errors.append(
                    f"E_LIVE_ROUTE {case_id}: observed owner mismatch "
                    "or missing gate observation"
                )
            if (
                record["ForbiddenActionTaken"] is not False
                or record["MutationEventCount"] != 0
            ):
                errors.append(f"E_LIVE_MUTATION {case_id}: forbidden action observed")

            locator = str(record["CandidateLocator"])
            if expected_owner == "none":
                if locator or record["ReadEvent"] is not None:
                    errors.append(
                        f"E_LIVE_SOURCE {case_id}: none owner must not read a candidate"
                    )
            else:
                expected_locator = str((ROOT / expected_owner / "SKILL.md").resolve())
                if (
                    not Path(locator).is_absolute()
                    or normalized_path(locator) != normalized_path(expected_locator)
                ):
                    errors.append(
                        f"E_LIVE_SOURCE {case_id}: candidate locator mismatch"
                    )
                owner_proof = proof_by_name.get(expected_owner)
                if (
                    owner_proof is None
                    or normalized_path(locator)
                    != normalized_path(owner_proof["CandidateLocator"])
                ):
                    errors.append(
                        f"E_LIVE_SOURCE {case_id}: smoke locator is not bound "
                        "to candidate source proof"
                    )

            result = record["Result"]
            if case["LiveResult"] != result:
                errors.append(
                    f"E_LIVE_RESULT {case_id}: case LiveResult and smoke Result differ"
                )
            if not HEX64_RE.fullmatch(str(record["EventsSha256"])):
                errors.append(f"E_LIVE_HASH {case_id}: invalid EventsSha256")
            if not HEX64_RE.fullmatch(str(record["ControlEventsSha256"])):
                errors.append(f"E_LIVE_HASH {case_id}: invalid ControlEventsSha256")
            if result == "pass":
                read_event = record["ReadEvent"]
                if record["ReadObservationAvailable"] is not True:
                    errors.append(f"E_LIVE_READ {case_id}: invalid successful read evidence")
                if str(record["ObservationFailure"]):
                    errors.append(
                        f"E_LIVE_READ {case_id}: pass must not report observation failure"
                    )
                if expected_owner == "none":
                    if read_event is not None:
                        errors.append(
                            f"E_LIVE_READ {case_id}: none owner must not have ReadEvent"
                        )
                elif (
                    not isinstance(read_event, dict)
                    or read_event.get("EventType") != "item.completed"
                    or read_event.get("ItemType") != "command_execution"
                    or read_event.get("Status") != "completed"
                    or read_event.get("ExitCode") not in {None, 0}
                ):
                    errors.append(
                        f"E_LIVE_READ {case_id}: invalid successful read evidence"
                    )
                else:
                    command = str(read_event.get("Command", ""))
                    normalized_command = re.sub(
                        r"\\+",
                        r"\\",
                        command.replace("/", "\\"),
                    ).casefold()
                    if (
                        re.search(
                            r"(?i)Get-Content\s+-Raw\s+-LiteralPath",
                            command,
                        )
                        is None
                        or normalized_path(locator) not in normalized_command
                    ):
                        errors.append(
                            f"E_LIVE_READ {case_id}: command does not prove full candidate read"
                        )
            elif result == "unobservable-residual-risk":
                if (
                    record["ReadObservationAvailable"] is not False
                    or record["ReadEvent"] is not None
                    or not str(record["ObservationFailure"]).strip()
                ):
                    errors.append(
                        f"E_LIVE_UNOBSERVABLE {case_id}: incomplete control evidence"
                    )
            else:
                errors.append(f"E_LIVE_RESULT {case_id}: unresolved result {result!r}")

    return errors


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
    if description and not HAN_RE.search(description):
        errors.append(
            f"{skill_path.relative_to(ROOT)}: description must contain at least one Han character"
        )

    h2_headings = [
        line.strip()
        for line in text.splitlines()
        if re.match(r"^## (?!#)", line)
    ]
    markdown_headings = [
        line.strip()
        for line in text.splitlines()
        if re.match(r"^#{2,6}\s+", line)
    ]
    ordinary_bilingual_headings = [
        heading
        for heading in markdown_headings
        if (
            heading not in STABLE_BILINGUAL_HEADINGS.values()
            and BILINGUAL_HEADING_ALIAS_RE.search(
                MARKDOWN_LINK_TARGET_RE.sub("]", heading)
            )
        )
    ]
    if ordinary_bilingual_headings:
        errors.append(
            f"{skill_path.relative_to(ROOT)}: ordinary headings must not keep "
            f"English parenthetical aliases: {ordinary_bilingual_headings!r}"
        )

    expected_headings = SKILL_HEADING_INVENTORY.get(name)
    for english_name, exact_heading in STABLE_BILINGUAL_HEADINGS.items():
        exact_count = h2_headings.count(exact_heading)
        chinese_only = exact_heading.split("（", 1)[0]
        malformed = [
            heading
            for heading in h2_headings
            if (
                english_name in heading
                or heading == chinese_only
            )
            and heading != exact_heading
        ]
        if malformed:
            errors.append(
                f"{skill_path.relative_to(ROOT)}: stable heading must be "
                f"{exact_heading!r}, got {malformed!r}"
            )
        if expected_headings is not None:
            should_exist = english_name in expected_headings
            if should_exist and exact_count != 1:
                errors.append(
                    f"{skill_path.relative_to(ROOT)}: expected exactly one "
                    f"{exact_heading!r} heading (got {exact_count})"
                )
            if not should_exist and exact_count != 0:
                errors.append(
                    f"{skill_path.relative_to(ROOT)}: unexpected stable heading "
                    f"{exact_heading!r}"
                )

    for token in has_bad_text(text):
        errors.append(f"{skill_path.relative_to(ROOT)}: contains {token!r}")
    for token in has_stale_workflow_text(text):
        errors.append(f"{skill_path.relative_to(ROOT)}: contains stale workflow text {token!r}")
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
    required_doc_text = (
        "Natural Handoff",
        "继续",
        "可以",
        "按你说的办",
        "go ahead",
        "ok",
        "好的",
        "上一条",
        "唯一推荐",
        "绕过",
    )

    for doc_name in ("README.md", "AGENTS.md"):
        doc_path = ROOT / doc_name
        try:
            doc_text = read_text(doc_path)
        except (OSError, ValueError) as exc:
            errors.append(f"{doc_name}: {exc}")
            continue
        for required in required_doc_text:
            if required not in doc_text:
                errors.append(f"{doc_name}: missing Natural Handoff marker {required!r}")
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


def validate_consolidation_contract(skill_dirs: list[Path]) -> list[str]:
    errors: list[str] = []

    for retired_name in RETIRED_SKILL_NAMES:
        retired_path = ROOT / retired_name
        if retired_path.exists():
            errors.append(f"{retired_name}/: retired skill directory must not exist")

    for display_path, required_markers in CONSOLIDATION_REQUIRED_TEXT.items():
        path = ROOT / display_path
        try:
            text = read_text(path)
        except (OSError, ValueError) as exc:
            errors.append(f"{display_path}: {exc}")
            continue
        for marker in required_markers:
            if marker not in text:
                errors.append(f"{display_path}: missing consolidation marker {marker!r}")

    retired_pattern = re.compile(
        "|".join(re.escape(name) for name in RETIRED_SKILL_NAMES),
        re.IGNORECASE,
    )
    active_paths = [ROOT / "README.md", ROOT / "AGENTS.md"]
    for skill_dir in skill_dirs:
        active_paths.extend(
            path
            for path in skill_dir.rglob("*")
            if path.is_file() and path.suffix.lower() in ACTIVE_ARTIFACT_SUFFIXES
        )

    for path in active_paths:
        try:
            text = read_text(path)
        except (OSError, ValueError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue
        for match in retired_pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            errors.append(
                f"{path.relative_to(ROOT)}:{line}: contains retired skill name {match.group(0)!r}"
            )

    return errors


def run_default_validation() -> int:
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
    errors.extend(validate_consolidation_contract(skill_dirs))

    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(skill_dirs)} skills.")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--audit-english-heavy",
        nargs="*",
        metavar="SKILL.md",
        help="list English-heavy prose candidates without failing on matches",
    )
    mode.add_argument(
        "--verify-localization-evidence",
        nargs=2,
        metavar=("MATRIX", "LEDGER"),
        help="validate localization matrix, ledger, and scoped invariants",
    )
    parser.add_argument(
        "--skills",
        nargs="+",
        help="skill names scoped by localization evidence verification",
    )
    parser.add_argument(
        "--require-static-pass",
        action="store_true",
        help="require scoped static cases, reviews, and invariants to pass",
    )
    parser.add_argument(
        "--require-live-resolved",
        action="store_true",
        help="require all LiveRequired candidate-source smoke cases to resolve",
    )
    args = parser.parse_args(argv)
    if args.verify_localization_evidence is None and (
        args.skills or args.require_static_pass or args.require_live_resolved
    ):
        parser.error(
            "--skills/--require-static-pass/--require-live-resolved require "
            "--verify-localization-evidence"
        )
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.audit_english_heavy is not None:
        return run_english_heavy_audit(args.audit_english_heavy)
    if args.verify_localization_evidence is not None:
        matrix_path, ledger_path = (
            path.resolve() if path.is_absolute() else (ROOT / path).resolve()
            for path in map(Path, args.verify_localization_evidence)
        )
        errors = validate_localization_evidence(
            matrix_path,
            ledger_path,
            args.skills,
            args.require_static_pass,
            args.require_live_resolved,
        )
        if errors:
            print("Localization evidence validation failed:", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1
        print("Localization evidence validated.")
        return 0
    return run_default_validation()


if __name__ == "__main__":
    sys.exit(main())
