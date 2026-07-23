# Skill 正文中文化迁移 Plan

## 元数据 (Metadata)

- **Status**: Ready
- **Source Spec**: `docs/features/skill-content-chinese-localization/spec.md`
- **Generated at**: 2026-07-23
- **Planning Mode**: Full
- **Risk rationale**: 已有正式 spec；变更同时覆盖 16 个 skill、仓库 authoring rules、validator 精确 marker、跨 skill 路由与 fresh-session 验证，并包含一次已接受的运行时行为变化。
- **Repository Snapshot**: target submodule `45d99a8` (`main`); parent workspace `3ef2b44` (`master`)
- **Verified baseline**:
  - `python scripts/validate-skills.py` 输出 `Validated 16 skills.`
  - `npx --yes skills add . --list` 列出且只列出当前 16 个 skill。
  - `npx --yes skills --version` 输出 `1.5.18`。
  - `codex --version` 输出 `codex-cli 0.144.6`；当前 CLI 支持 `codex debug prompt-input`、`codex exec --ephemeral`、`--ignore-user-config` 和 one-shot `skills.config` override。
- **Analysis**: Not requested；本 Planning Run 不生成 `analysis.md`。

## 实现假设 (Assumptions)

1. 实现入口仍为 `$implement`；本 plan 不授权 branch、业务文件写入、review、commit、push、PR、merge、discard 或远端操作。
2. 目标 inventory 是 snapshot `45d99a8` 上的 16 个顶层 skill 目录；实现开始时若 inventory、validator contract 或工作树发生实质漂移，先停止并回到 planning。
3. `agents/openai.yaml` 当前只复述对应 `SKILL.md` 的名称和简短描述。除非逐文件证据证明中文化后的 trigger scope 与 metadata 直接矛盾，否则它们只做 no-change 检查。
4. `references/`、`assets/`、examples 和非 validator scripts 不在正文中文化范围内；通过 progressive disclosure 读取的英文材料属于已接受的 residual risk。
5. 全局安装目录 `C:\Users\Administrator\.agents\skills` 只用于基线 hash 和隔离验证，不修改其中任何文件。
6. 四个历史 feature artifact 目录保持原文；当前 spec 的 supersession metadata 是区分历史记录和 active rule 的唯一机制。
7. 不新增 routing eval harness。静态 48-case matrix 是全量覆盖，live smoke 只覆盖 FR-019 指定的 8 个高耦合 skill。
8. 现有文件可能混用 CRLF/LF。每个文件只保留或局部匹配其既有格式，不进行跨文件 EOL 统一。
9. 本 feature 有两个 write surface：目标 submodule 与父仓库 active `AGENTS.md`。`$implement` 在任何 Task 1 migration write 前必须分别展示两者 branch/status 并完成适用的 branch decision；不得把其中一个仓库的授权推断为另一个仓库的授权。

## 全局约束 (Global Constraints)

- `name` 值、目录名、canonical H1、`$skill` ID、YAML key、Markdown/代码语法、命令、API、路径、schema field、enum、版本名、gate ID、`FR-###` 和 `SC-###` 保持原样。
- `description` 使用中文主句；只有具备 English 正向 case 的必要 trigger phrase 才能保留，不保留完整英文描述副本。
- 普通 prose、普通 heading、表格可见标签、场景解释、Mermaid 可见标签与边条件使用中文。
- 仅已有的 `Trigger Description`、`Pressure Scenarios`、`Natural Handoff` 使用以下精确标题；不得为测试覆盖新增原本不存在的 section：
  - `## 触发说明（Trigger Description）`
  - `## 压力场景（Pressure Scenarios）`
  - `## 自然交接（Natural Handoff）`
- 翻译必须保持 `必须`、`不得`、`仅当`、`最多一个`、`唯一推荐`、`只读`、`写入前停止` 等规范性强度。语义不确定时停止该 skill，不做猜测式改写。
- 第一项 migration task 原子删除全部 active `Language Contract` 与等价运行时中文保证；不得把要求搬到其他 per-skill section。
- Preflight 可读取两个仓库；任何 migration write 前，`checking-branch` gate 必须覆盖 target `main` 与 parent `master` 两个真实 repository context。
- 不使用中文字符比例门槛，也不为迁移期引入临时 skill allowlist。永久的全 inventory `description` 中文硬门只在六批全部完成后启用；各批使用 scoped verification。
- 六个批次严格串行；Batch 1 后必须通过唯一 human calibration gate，之后才可继续。
- 每批都运行 validator、该批 full-depth 解析、English-heavy 审阅、matrix 更新和 scoped `git diff --check`。
- correctness 与 trigger reliability 优先于中文纯度；任何保留英文都写入 `EnglishHeavyReviewLedger v1`。
- 除目标仓库内容、本 feature workspace 和父工作区 active `C:\WorkSpace\skill-development\AGENTS.md` 外，不修改历史 artifacts、父仓库其他文件、其他 submodule、全局 skill 副本或无关工作树文件。

## 共享产物与契约 (Shared Artifacts and Contracts)

### `RuntimeLanguageDecouplingContract v1`

| Field | Value |
| --- | --- |
| `per_skill_language_contract` | `removed` |
| `runtime_language_source` | `user request \| target project rules \| conversation context` |
| `skill_authoring_language` | `Chinese-first` |
| `authorized_behavior_change` | 独立安装的 skill 不再由自身保证中文输出 |

### `RoutingVerificationMatrix v1`

文件：`docs/features/skill-content-chinese-localization/verification-matrix.md`

- `SkillInventoryBaseline`: 16 个 canonical name、H1、description、source path。
- `RoutingCase`: `CaseId | Skill | CaseKind | PromptLanguage | LiveRequired | ExpectedOwner | ExpectedGate | ForbiddenOwnerOrAction | Prompt | TriggerPhraseRef | BoundaryRef | StaticResult | LiveResult | Notes`。
- 每个 skill 至少三例：中文正向、英文正向、near-miss；case ID 使用 `LOC-<GROUP>-ZH|EN|NEAR`，总数至少 48。
- canonical routing case 使用一行一个 JSON object 的 JSONL block，位于 `<!-- ROUTING_CASES_BEGIN -->` 与 `<!-- ROUTING_CASES_END -->` 之间；`CaseKind` 固定为 `ZH-positive|EN-positive|near-miss`。Markdown 表格只能作为派生摘要，验证以 JSONL block 为准。
- `RouteInvariant`: `EdgeId | SourceSkill | TargetSkill | Pattern | BaselineCount | Condition | StopBoundary | BaselineEvidence | FinalEvidence`。
- `StableTokenInvariant`: `Skill | Category | Token | BaselineCount | FinalCount | Evidence`。
- `NormativeConstraintInvariant`: `Skill | Constraint | BaselineEvidence | FinalEvidence | Result`。
- `CandidateSourceSmoke`: `CaseId | Skill | PromptLanguage | Prompt | ExpectedOwner | ExpectedGate | ForbiddenOwnerOrAction | CandidateLocator | GlobalLocatorDisabled | ObservedOwner | ObservedGate | ForbiddenActionTaken | EventsSha256 | ControlEventsSha256 | ReadObservationAvailable | ReadEvent | ObservationFailure | MutationEventCount | Result | Notes`。
- `EnvironmentBaseline`: target HEAD、CLI versions、目标/父仓库状态、历史目录状态和全局同名 skill hash。
- `RouteInvariant`、`StableTokenInvariant`、`NormativeConstraintInvariant` 分别使用 `ROUTE_INVARIANTS`、`STABLE_TOKEN_INVARIANTS`、`NORMATIVE_INVARIANTS` 的 begin/end marker 包围 canonical JSONL block。evidence verifier 对 scoped skill 逐条执行 regex/token exact-count 比较；`rg` 只用于展示证据，不作为 pass/fail 的唯一依据。

### `EnglishHeavyReviewLedger v1`

文件：`docs/features/skill-content-chinese-localization/english-heavy-review.md`

canonical 记录使用 `<!-- ENGLISH_REVIEW_BEGIN -->` 与 `<!-- ENGLISH_REVIEW_END -->` 包围的 JSONL block；每条记录包含：

`ReviewId | File | LineOrSection | Fragment | Category | KeepOrTranslate | Rationale | RoutingCase | Reviewer | Result`

允许的 `Category` 至少包括 `canonical-name`、`trigger-phrase`、`technical-term`、`command-or-path`、`stable-contract`、`test-data`。audit 只产生候选，不凭命中改变退出码。

`RoutingVerificationMatrix v1` 与 `EnglishHeavyReviewLedger v1` 是 versioned in-place accumulators：Task 1 产生 `@T1`，每个后续 task 必须显式消费上一 revision 并产生自己的 revision，Task 9 产生 `@Final`。

`LocalizationBaselineSnapshot v1` 使用 JSON object，固定字段为 `Version`、`TargetHead`、`SkillInventory`、`NoChangeEntries`、`GlobalCopyEntries`、`ParentStatus`、`SubmoduleStatus`、`ToolVersions`。每个 file entry 使用 `Path | Exists | Sha256`；目录必须展开成逐文件 entry，不以目录名代替内容 hash。该文件由 Task 1 在任何 migration write 前产生，Task 2–9 只读消费。

`NoChangeEntries` 必须包含本 Planning Run 已检查的 `spec.md` 与 `plan.md`。Task 1 创建 snapshot 后，把它的 SHA-256 写入现有 `manifest.md` 的 `Baseline Snapshot SHA-256` 字段；该字段构成 `BaselineDigestAnchor v1`。Task 2–9 每次 verification 开始和结束都运行 `BaselineIntegrityGate v1`：先验证 snapshot hash 与 manifest anchor 一致，再逐项重算 `NoChangeEntries` 和 `GlobalCopyEntries` 的 existence/hash。Task 9 虽可更新 manifest 的 implementation 状态与 report 路径，但不得改变 anchor。

以下是 `BaselineIntegrityGate v1` 的 canonical blocking probe。Task 1 在写入 64-hex anchor 后、Phase 0 前执行一次，并在 task 结束时再执行一次；Task 2–9 把它作为 verification 的第一条和最后一条命令，不得省略：

```powershell
@'
from pathlib import Path
import hashlib
import json
import re

root = Path(".").resolve()
feature = root / "docs/features/skill-content-chinese-localization"
snapshot_path = feature / "baseline-snapshot.json"
manifest_path = feature / "manifest.md"

manifest = manifest_path.read_text(encoding="utf-8")
anchors = re.findall(
    r"(?m)^- Baseline Snapshot SHA-256: `([0-9a-f]{64})`$",
    manifest,
)
assert len(anchors) == 1, anchors
snapshot_digest = hashlib.sha256(snapshot_path.read_bytes()).hexdigest()
assert snapshot_digest == anchors[0], (snapshot_digest, anchors[0])

snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
assert snapshot["Version"] == "LocalizationBaselineSnapshot v1"
required_checked_plan = {
    (feature / "spec.md").resolve(),
    (feature / "plan.md").resolve(),
}
actual_no_change = {
    Path(entry["Path"]).resolve()
    for entry in snapshot["NoChangeEntries"]
}
assert required_checked_plan <= actual_no_change, (
    required_checked_plan - actual_no_change
)

for group in ("NoChangeEntries", "GlobalCopyEntries"):
    for entry in snapshot[group]:
        assert set(entry) == {"Path", "Exists", "Sha256"}, entry
        path = Path(entry["Path"])
        assert path.is_absolute(), path
        exists = path.exists()
        assert exists == entry["Exists"], path
        if exists:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            assert digest == entry["Sha256"], path
        else:
            assert entry["Sha256"] is None, entry
'@ | python -
```

### 精确 no-change 路径集合

`MetadataNoChangeSet v1`：

- `analyze/agents/openai.yaml`
- `brainstorming/agents/openai.yaml`
- `checking-branch/agents/openai.yaml`
- `clarify/agents/openai.yaml`
- `diagnose/agents/openai.yaml`
- `finishing-branch/agents/openai.yaml`
- `grill-me/agents/openai.yaml`
- `handoff/agents/openai.yaml`
- `implement/agents/openai.yaml`
- `improve-codebase-architecture/agents/openai.yaml`
- `requesting-code-review/agents/openai.yaml`
- `session-curator/agents/openai.yaml`
- `tdd/agents/openai.yaml`
- `to-plan/agents/openai.yaml`
- `to-spec/agents/openai.yaml`
- `verification-before-completion/agents/openai.yaml`

`GlobalCopyNoChangeSet v1`：

- `C:\Users\Administrator\.agents\skills\analyze\SKILL.md`
- `C:\Users\Administrator\.agents\skills\brainstorming\SKILL.md`
- `C:\Users\Administrator\.agents\skills\checking-branch\SKILL.md`
- `C:\Users\Administrator\.agents\skills\clarify\SKILL.md`
- `C:\Users\Administrator\.agents\skills\diagnose\SKILL.md`
- `C:\Users\Administrator\.agents\skills\finishing-branch\SKILL.md`
- `C:\Users\Administrator\.agents\skills\grill-me\SKILL.md`
- `C:\Users\Administrator\.agents\skills\handoff\SKILL.md`
- `C:\Users\Administrator\.agents\skills\implement\SKILL.md`
- `C:\Users\Administrator\.agents\skills\improve-codebase-architecture\SKILL.md`
- `C:\Users\Administrator\.agents\skills\requesting-code-review\SKILL.md`
- `C:\Users\Administrator\.agents\skills\session-curator\SKILL.md`
- `C:\Users\Administrator\.agents\skills\tdd\SKILL.md`
- `C:\Users\Administrator\.agents\skills\to-plan\SKILL.md`
- `C:\Users\Administrator\.agents\skills\to-spec\SKILL.md`
- `C:\Users\Administrator\.agents\skills\verification-before-completion\SKILL.md`

## 顺序任务 (Sequential Tasks)

### Task 1 — Preflight（只读）+ Phase 0（原子）：冻结基线后仅移除运行时语言契约

**Files**

- **Modify**:
  - `C:\WorkSpace\skill-development\AGENTS.md`
  - `AGENTS.md`
  - `README.md`
  - `scripts/validate-skills.py`
  - `docs/features/skill-content-chinese-localization/manifest.md`
  - `analyze/SKILL.md`
  - `brainstorming/SKILL.md`
  - `checking-branch/SKILL.md`
  - `clarify/SKILL.md`
  - `diagnose/SKILL.md`
  - `finishing-branch/SKILL.md`
  - `grill-me/SKILL.md`
  - `handoff/SKILL.md`
  - `implement/SKILL.md`
  - `improve-codebase-architecture/SKILL.md`
  - `requesting-code-review/SKILL.md`
  - `session-curator/SKILL.md`
  - `tdd/SKILL.md`
  - `to-plan/SKILL.md`
  - `to-spec/SKILL.md`
  - `verification-before-completion/SKILL.md`
- **Create**:
  - `docs/features/skill-content-chinese-localization/baseline-snapshot.json`
  - `docs/features/skill-content-chinese-localization/verification-matrix.md`
  - `docs/features/skill-content-chinese-localization/english-heavy-review.md`
- **Test, no change**:
  - `docs/features/skill-content-chinese-localization/spec.md`
  - `docs/features/skill-content-chinese-localization/plan.md`
  - `MetadataNoChangeSet v1` 中列出的 16 个精确路径
  - `docs/features/spec-plan-workflow/`（recursive）
  - `docs/features/adaptive-planning-workflow/`（recursive）
  - `docs/features/natural-handoff-workflow/`（recursive）
  - `docs/features/workflow-skill-consolidation/`（recursive）
  - `GlobalCopyNoChangeSet v1` 中列出的 16 个精确路径

**Consumes**

- Approved `spec.md` 中的 `FR-001` 至 `FR-021`。
- snapshot `45d99a8` 的 16-skill inventory、route edge、stable token、normative constraint 和全局同名副本 hash。
- 当前 validator 中的 `LANGUAGE_CONTRACT_MARKER`、`LANGUAGE_CONTRACT_EXCEPTION`、`GRILL_ME_REQUIRED_TEXT`、`ADAPTIVE_PLANNING_REQUIRED_TEXT`、`CONSOLIDATION_REQUIRED_TEXT`。

**Produces**

- `RuntimeLanguageDecouplingContract v1`。
- `LocalizationBaselineSnapshot v1`，落点为 `docs/features/skill-content-chinese-localization/baseline-snapshot.json`。
- `BaselineDigestAnchor v1`，写入现有 `manifest.md` 的唯一 `Baseline Snapshot SHA-256` 字段。
- `RoutingVerificationMatrix v1@T1`，包含完整 48+ 静态 case、行为 invariant 与环境基线。
- `EnglishHeavyReviewLedger v1@T1`。

**Covers**

`FR-001`、`FR-002`、`FR-003`、`FR-004`、`FR-006`、`FR-012`、`FR-014`、`FR-017`、`FR-018`、`FR-020`、`FR-021`。

**Acceptance Criteria**

1. 16 个 `## Language Contract` section 在同一个 task 中全部删除；目标仓库 `AGENTS.md`、父工作区 active `AGENTS.md`、目标仓库 `README.md` 和 validator 不再要求 marker、exception 或独立安装后的默认中文输出。
2. 同一 task 中性化 `to-spec/SKILL.md` 与 `brainstorming/SKILL.md` 其他 active section 中的等价运行时中文保证；不得把等价要求移动到新 section。
3. 两层 active `AGENTS.md` 和目标仓库 `README.md` 仍保留仓库 authoring rule：当前及未来 `SKILL.md` 中文优先，机器语法与必要 English 保留。
4. validator 删除 `LANGUAGE_CONTRACT_MARKER`、`LANGUAGE_CONTRACT_EXCEPTION` 及对应逐字检查，其他 workflow、安全和 stale-text gate 仍通过。
5. 在任何 active migration write 前，先创建 immutable-by-contract 的 `baseline-snapshot.json`、matrix 和 ledger；snapshot 记录全部 16 个 skill、全局副本、MetadataNoChangeSet、历史目录、references/assets/examples/非 validator scripts、父仓库与其他 submodule 的 path/existence/SHA-256/status，并在 `NoChangeEntries` 中以 absolute path 记录已检查 `spec.md`、`plan.md` 的 existence/SHA-256；matrix 记录中文正向、英文正向、near-miss、route/stable-token/normative baseline。这是只读 preflight。
6. snapshot 创建后立即计算 SHA-256，把 64-hex digest 写入 manifest 的唯一 `Baseline Snapshot SHA-256` 字段，并在 Phase 0 前通过 `BaselineIntegrityGate v1`；不得重写 snapshot 来吸收后续 drift。
7. preflight 和 digest anchor 完成后才执行 Phase 0；Phase 0 的 active 修改只做运行时语言契约移除及 current rule/validator 同步，不加入 audit/evidence CLI 或正文翻译。
8. Task 结束时再次通过 `BaselineIntegrityGate v1`；四个历史 feature 目录、16 个 `agents/openai.yaml` 和全局安装副本未修改。
9. 本 task 不翻译其余正文；因此不得提前启用全 inventory CJK hard gate，也不得写迁移 allowlist。

**Verification**

先在 Phase 0 前、再在本 task 最后执行全局约束中的 canonical `BaselineIntegrityGate v1` probe；两次都必须通过。

```powershell
python scripts/validate-skills.py
```

预期 validator 输出 `Validated 16 skills.`。

```powershell
@'
from pathlib import Path
import json
import re

root = Path(".").resolve()
skills = sorted(root.glob("*/SKILL.md"))
assert len(skills) == 16, len(skills)

active = skills + [
    root / "AGENTS.md",
    root.parents[1] / "AGENTS.md",
    root / "README.md",
    root / "scripts/validate-skills.py",
]
forbidden = (
    "## Language Contract",
    "## 语言契约",
    "## 语言契约（Language Contract）",
    "LANGUAGE_CONTRACT_MARKER",
    "LANGUAGE_CONTRACT_EXCEPTION",
    "生成的文档和聊天输出默认以中文优先",
    "Skill 生成的 Markdown/HTML",
    "产出型 skill 必须包含统一 `Language Contract`",
    "spec 正文必须中文优先",
    "文档正文默认中文为主",
    "功能需求使用稳定 ID，并用中文描述",
    "用中文描述一个外部可观察行为",
    "用中文描述另一个可验证需求",
    "用中文描述可验证成功标准",
    "用中文描述风险",
    "用中文描述开放问题",
    "各章节描述正文是中文主文",
    "PlanningHandoffPacket v1`。使用中文主文",
)
hits = []
for path in active:
    text = path.read_text(encoding="utf-8")
    for token in forbidden:
        if token in text:
            hits.append(f"{path.as_posix()}: {token}")
if hits:
    raise SystemExit("\n".join(hits))

matrix = (root / "docs/features/skill-content-chinese-localization/verification-matrix.md").read_text(encoding="utf-8")
body = matrix.split("<!-- ROUTING_CASES_BEGIN -->", 1)[1].split("<!-- ROUTING_CASES_END -->", 1)[0]
cases = [json.loads(line) for line in body.splitlines() if line.lstrip().startswith("{")]
required = {
    "CaseId", "Skill", "CaseKind", "PromptLanguage", "LiveRequired",
    "ExpectedOwner", "ExpectedGate", "ForbiddenOwnerOrAction", "Prompt",
    "TriggerPhraseRef", "BoundaryRef", "StaticResult", "LiveResult", "Notes",
}
assert cases and all(required <= case.keys() for case in cases)
ids = [case["CaseId"] for case in cases]
assert len(ids) == len(set(ids)), "duplicate CaseId"
expected_skills = {path.parent.name for path in skills}
expected_kinds = {"ZH-positive", "EN-positive", "near-miss"}
actual_pairs = {(case["Skill"], case["CaseKind"]) for case in cases}
assert {(skill, kind) for skill in expected_skills for kind in expected_kinds} <= actual_pairs
assert {case["Skill"] for case in cases} == expected_skills
for case in cases:
    if case["CaseKind"] in {"ZH-positive", "EN-positive"}:
        assert case["ExpectedOwner"] == case["Skill"], case["CaseId"]
    else:
        assert case["ExpectedOwner"] != case["Skill"], case["CaseId"]
assert len(cases) >= 48
'@ | python -
```

```powershell
$expected = @(
  'analyze','brainstorming','checking-branch','clarify','diagnose',
  'finishing-branch','grill-me','handoff','implement',
  'improve-codebase-architecture','requesting-code-review',
  'session-curator','tdd','to-plan','to-spec',
  'verification-before-completion'
)
$actual = Get-ChildItem -Directory |
  Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md') } |
  ForEach-Object Name |
  Sort-Object -Unique
$delta = Compare-Object ($expected | Sort-Object) $actual
if ($delta) { $delta; throw 'filesystem skill inventory mismatch' }
$listOutput = npx --yes skills add . --list
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$plain = [regex]::Replace(($listOutput -join "`n"), '\x1B\[[0-?]*[ -/]*[@-~]', '')
$npxActual = [regex]::Matches(
  $plain,
  '(?m)^\|\s{4}([a-z0-9]+(?:-[a-z0-9]+)*)\s*$'
) | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique
$npxDelta = Compare-Object ($expected | Sort-Object) $npxActual
if ($npxDelta -or $npxActual.Count -ne 16) {
  $npxDelta
  throw "npx skill inventory mismatch: expected=16 actual=$($npxActual.Count)"
}
foreach ($skillName in $expected) {
  npx --yes skills use . --skill $skillName --full-depth *> $null
  if ($LASTEXITCODE -ne 0) { throw "full-depth failed: $skillName" }
}

$history = @(
  'docs/features/spec-plan-workflow',
  'docs/features/adaptive-planning-workflow',
  'docs/features/natural-handoff-workflow',
  'docs/features/workflow-skill-consolidation'
)
$changes = git status --porcelain=v1 --untracked-files=all -- $history
if ($changes) { $changes; exit 1 }
git diff --check
```

### Task 2 — Batch 1：独立终点 skill 中文化

**Files**

- **Modify**:
  - `clarify/SKILL.md`
  - `improve-codebase-architecture/SKILL.md`
  - `handoff/SKILL.md`
  - `scripts/validate-skills.py`
  - `docs/features/skill-content-chinese-localization/verification-matrix.md`
  - `docs/features/skill-content-chinese-localization/english-heavy-review.md`
- **Test, no change**:
  - `docs/features/skill-content-chinese-localization/baseline-snapshot.json`
  - `docs/features/skill-content-chinese-localization/spec.md`
  - `docs/features/skill-content-chinese-localization/plan.md`
  - `docs/features/skill-content-chinese-localization/manifest.md`
  - `clarify/agents/openai.yaml`
  - `improve-codebase-architecture/agents/openai.yaml`
  - `handoff/agents/openai.yaml`
  - `clarify/references/report-structure.md`
  - `clarify/assets/clarify-report-template.html`
  - `improve-codebase-architecture/references/language.md`
  - `improve-codebase-architecture/references/deepening.md`
  - `improve-codebase-architecture/references/html-report.md`
  - `improve-codebase-architecture/references/interface-design.md`

**Consumes**

- `LocalizationBaselineSnapshot v1`（Test, no change）。
- `RuntimeLanguageDecouplingContract v1`。
- `RoutingVerificationMatrix v1@T1`。
- `EnglishHeavyReviewLedger v1@T1`。

**Produces**

- `Batch1LocalizationCandidate v1`：三个 skill 的中文 description/正文、9 个已复核静态 case、route/stable-token/normative invariant evidence。
- `RoutingVerificationMatrix v1@T2`。
- `EnglishHeavyReviewLedger v1@T2`。
- `python scripts/validate-skills.py --audit-english-heavy [optional SKILL.md paths]` 非阻塞审阅入口。
- `python scripts/validate-skills.py --verify-localization-evidence <matrix> <ledger> --skills <names> [--require-static-pass]` 严格 artifact/invariant 检查入口。

**Covers**

`FR-005`、`FR-006`、`FR-007`、`FR-008`、`FR-009`、`FR-010`、`FR-012`、`FR-013`、`FR-014`、`FR-015`、`FR-017`、`FR-018`、`FR-021`。

**Acceptance Criteria**

1. 三个 `description` 使用中文主句，trigger scope 与 boundary 不变；每个保留 English trigger phrase 映射到本 skill 的 English case。
2. `improve-codebase-architecture` 的既有 heading 精确改为 `## 压力场景（Pressure Scenarios）`；`clarify`、`handoff` 不新增该 section。
3. `clarify` 仍只回答源码问题、证据优先、推断显式标注、最多问一个无法探索解决的问题，并明确不使用 `Natural Handoff`。
4. `improve-codebase-architecture` 仍先读 domain docs/ADR、为候选提供 source evidence 与 deletion test、默认不实现、模糊全仓扫描只选 2–4 个高价值区域，文档同步仍需用户同意。
5. `handoff` 仍写 OS temp 中的时间戳 Markdown、只做可执行摘要、引用已有 artifacts、redact secrets/PII，并保留 `Suggested Skills` 等稳定 document fields。
6. canonical H1、reference/asset path、Mermaid token、schema field、enum 和写入边界不变；普通 `Document Contract` 等 heading 中文化。
7. `LOC-CLARIFY-*`、`LOC-ARCH-*`、`LOC-HANDOFF-*` 九例完成 static review；English-heavy 候选均有处置或理由。
8. validator 新增的 audit 排除 fenced/indented code、inline code、命令、路径、canonical H1 和 stable contract，命中本身不改变退出码；evidence verifier 严格检查 scoped case、positive `ExpectedOwner = Skill`、near-miss `ExpectedOwner != Skill`、stable-token count、route regex count、required field、English trigger trace，以及 matrix/ledger 的 UTF-8-no-BOM、LF、trailing whitespace，任一缺失返回非零。最终 `--require-live-resolved` 对 `pass` 还必须验证 absolute candidate locator、global disabled、64-hex `EventsSha256`、成功的完整 command-read event、`MutationEventCount = 0`；只有 candidate locator 已证明且 control probe 的 read observation 失败时，才接受同时具有 64-hex `ControlEventsSha256`、`ReadObservationAvailable = false` 和非空 `ObservationFailure` 的 `unobservable-residual-risk`。任何已观测错误 owner/gate/action 都失败。
9. evidence verifier 必须通过 OS-temp mutation probes 的负向自测；不能只证明全绿 fixture 可通过。

**Verification**

```powershell
python scripts/validate-skills.py
python scripts/validate-skills.py --audit-english-heavy clarify/SKILL.md improve-codebase-architecture/SKILL.md handoff/SKILL.md
python scripts/validate-skills.py --verify-localization-evidence `
  docs/features/skill-content-chinese-localization/verification-matrix.md `
  docs/features/skill-content-chinese-localization/english-heavy-review.md `
  --skills clarify improve-codebase-architecture handoff `
  --require-static-pass

$batchSkills = @('clarify','improve-codebase-architecture','handoff')
foreach ($skillName in $batchSkills) {
  npx --yes skills use . --skill $skillName --full-depth *> $null
  if ($LASTEXITCODE -ne 0) { throw "full-depth failed: $skillName" }
}
```

```powershell
rg -n "references/report-structure\.md|assets/clarify-report-template\.html|references/(language|deepening|html-report|interface-design)\.md|architecture-review-<timestamp>\.html|Suggested Skills" clarify/SKILL.md improve-codebase-architecture/SKILL.md handoff/SKILL.md
rg -n "LOC-(CLARIFY|ARCH|HANDOFF)-(ZH|EN|NEAR)" docs/features/skill-content-chinese-localization/verification-matrix.md
git diff --check -- clarify/SKILL.md improve-codebase-architecture/SKILL.md handoff/SKILL.md docs/features/skill-content-chinese-localization
```

另外在 OS temp 中为每个 probe 重新复制干净 matrix/ledger，使用一次性 inline Python 只施加一项 mutation，再运行同一 `--verify-localization-evidence ... --require-static-pass` 命令。下列七项必须分别返回非零；任一返回 0 都使 Task 2 失败：

| Probe ID | 单一 mutation | 必须被哪个检查拒绝 |
| --- | --- | --- |
| `EV-NEG-REQUIRED-FIELD` | 从一个 case 删除 `BoundaryRef` | required field |
| `EV-NEG-OWNER-RELATION` | 把 positive case 的 `ExpectedOwner` 改为其他 skill | positive owner relation |
| `EV-NEG-INVARIANT-COUNT` | 把一个 stable token 的 `BaselineCount` 加 1 | exact-count invariant |
| `EV-NEG-ENGLISH-TRACE` | 把 retained trigger 的 `RoutingCase` 改为不存在的 ID | English trace |
| `EV-NEG-BOM` | 给 matrix 添加 UTF-8 BOM | encoding |
| `EV-NEG-CRLF` | 把 ledger 的 LF 改为 CRLF | newline |
| `EV-NEG-TRAILING` | 给一个 prose/JSONL 行添加 trailing space | whitespace |

probe root 必须先解析为 OS temp 下的本 task 专用目录；每个 probe 保存 exit code 与 stderr 摘要，完成后只清理该目录。

### Task 3 — Human Calibration Gate：确认统一语言基线

**Files**

- **Modify**:
  - `docs/features/skill-content-chinese-localization/verification-matrix.md`
  - `docs/features/skill-content-chinese-localization/english-heavy-review.md`
- **Test, no change**:
  - `docs/features/skill-content-chinese-localization/baseline-snapshot.json`
  - `docs/features/skill-content-chinese-localization/spec.md`
  - `docs/features/skill-content-chinese-localization/plan.md`
  - `docs/features/skill-content-chinese-localization/manifest.md`
  - `clarify/SKILL.md`
  - `improve-codebase-architecture/SKILL.md`
  - `handoff/SKILL.md`

**Consumes**

- `LocalizationBaselineSnapshot v1`（Test, no change）。
- `Batch1LocalizationCandidate v1`。
- `RoutingVerificationMatrix v1@T2`。
- `EnglishHeavyReviewLedger v1@T2`。

**Produces**

- `LocalizationStyleBaseline v1`，字段为 `ApprovedBatch | HeadingStyle | NormativeLexicon | EnglishRetentionRules | RepresentativeExamples | ReviewerDecision | Status`。
- `RoutingVerificationMatrix v1@T3`。
- `EnglishHeavyReviewLedger v1@T3`。

**Covers**

`FR-013`、`FR-014`、`FR-015`、`SC-008`。

**Acceptance Criteria**

1. 向用户展示 Batch 1 scoped diff、三个 description、双语稳定标题、至少一组规范性强度对照和 English 保留理由摘要。
2. 用户明确确认术语、语气、规范性强度和保留理由；确认结果写入两个 verification artifacts。
3. 若用户要求调整，只返回 Task 2 修正并重跑本 gate；不得进入 Batch 2。
4. gate 只发生一次。确认后后续五批按同一 baseline 推进，不因普通措辞偏好再次暂停；语义 blocker 仍必须停止。

**Verification**

- Manual seam：用户回复明确确认 `LocalizationStyleBaseline v1`。
- Static seam：ledger 中 `Status = approved`，matrix 中 Batch 1 的 9 个 case 均为 `StaticResult = pass`。
- 重新运行 Task 2 的 validator、audit、full-depth 与 `git diff --check`，结果仍通过。

### Task 4 — Batch 2：下游质量门 skill 中文化

**Files**

- **Modify**:
  - `tdd/SKILL.md`
  - `requesting-code-review/SKILL.md`
  - `verification-before-completion/SKILL.md`
  - `docs/features/skill-content-chinese-localization/verification-matrix.md`
  - `docs/features/skill-content-chinese-localization/english-heavy-review.md`
- **Test, no change**:
  - `docs/features/skill-content-chinese-localization/baseline-snapshot.json`
  - `docs/features/skill-content-chinese-localization/spec.md`
  - `docs/features/skill-content-chinese-localization/plan.md`
  - `docs/features/skill-content-chinese-localization/manifest.md`
  - `scripts/validate-skills.py`
  - `tdd/agents/openai.yaml`
  - `requesting-code-review/agents/openai.yaml`
  - `verification-before-completion/agents/openai.yaml`
  - `tdd/references/tests.md`
  - `tdd/references/mocking.md`
  - `tdd/references/deep-modules.md`
  - `tdd/references/interface-design.md`
  - `tdd/references/refactoring.md`

**Consumes**

- `LocalizationBaselineSnapshot v1`（Test, no change）。
- `RuntimeLanguageDecouplingContract v1`。
- `LocalizationStyleBaseline v1`。
- `RoutingVerificationMatrix v1@T3`。
- `EnglishHeavyReviewLedger v1@T3`。

**Produces**

- `QualityGateLocalization v1`：三个质量门 skill、9 个静态 case 与 `TDD -> review -> verification` 行为 invariant evidence。
- `RoutingVerificationMatrix v1@T4`。
- `EnglishHeavyReviewLedger v1@T4`。

**Covers**

`FR-005` 至 `FR-010`、`FR-012` 至 `FR-018`、`FR-021`。

**Acceptance Criteria**

1. 三个 description 中文主句与原 trigger boundary 等义；`tdd` 仍只在用户明确要求 TDD/test-first 时触发。
2. `tdd` 的既有 heading 为 `## 压力场景（Pressure Scenarios）`；`RED/GREEN/REFACTOR`、reference path 与稳定技术术语保持原样，普通 `Stage`/workflow heading 中文化。
3. TDD 仍按一个 external behavior 一个 cycle，先观察 RED、再最小 GREEN、最后 REFACTOR；RED 时不得 refactor，bugfix 保留失败测试或等价 repro。
4. `requesting-code-review` 仍先 Stage 1 spec compliance、后 Stage 2 code quality；findings-first，用户只要求 review 时不得改代码，`CRITICAL/HIGH` 处置要求不弱化。
5. `verification-before-completion` 仍逐项记录 `done/skipped/blocked`，运行贴近 external behavior 的验证，只清理本任务创建内容，并显式报告 skipped validation 与 residual risk。
6. `LOC-TDD-*`、`LOC-REVIEW-*`、`LOC-VERIFY-*` 九例通过 static review；所有非固定英文进入 ledger。

**Verification**

```powershell
python scripts/validate-skills.py
python scripts/validate-skills.py --audit-english-heavy tdd/SKILL.md requesting-code-review/SKILL.md verification-before-completion/SKILL.md
python scripts/validate-skills.py --verify-localization-evidence `
  docs/features/skill-content-chinese-localization/verification-matrix.md `
  docs/features/skill-content-chinese-localization/english-heavy-review.md `
  --skills tdd requesting-code-review verification-before-completion `
  --require-static-pass

$batchSkills = @('tdd','requesting-code-review','verification-before-completion')
foreach ($skillName in $batchSkills) {
  npx --yes skills use . --skill $skillName --full-depth *> $null
  if ($LASTEXITCODE -ne 0) { throw "full-depth failed: $skillName" }
}
```

```powershell
rg -n "RED/GREEN/REFACTOR|references/(tests|mocking|deep-modules|interface-design|refactoring)\.md|CRITICAL|HIGH|MEDIUM|LOW|No findings|Residual risk|\[DEBUG" tdd/SKILL.md requesting-code-review/SKILL.md verification-before-completion/SKILL.md
rg -n "LOC-(TDD|REVIEW|VERIFY)-(ZH|EN|NEAR)" docs/features/skill-content-chinese-localization/verification-matrix.md
git diff --check -- tdd/SKILL.md requesting-code-review/SKILL.md verification-before-completion/SKILL.md docs/features/skill-content-chinese-localization
```

### Task 5 — Batch 3：分支与知识连续性 skill 中文化

**Files**

- **Modify**:
  - `checking-branch/SKILL.md`
  - `finishing-branch/SKILL.md`
  - `session-curator/SKILL.md`
  - `scripts/validate-skills.py`
  - `docs/features/skill-content-chinese-localization/verification-matrix.md`
  - `docs/features/skill-content-chinese-localization/english-heavy-review.md`
- **Test, no change**:
  - `docs/features/skill-content-chinese-localization/baseline-snapshot.json`
  - `docs/features/skill-content-chinese-localization/spec.md`
  - `docs/features/skill-content-chinese-localization/plan.md`
  - `docs/features/skill-content-chinese-localization/manifest.md`
  - `checking-branch/agents/openai.yaml`
  - `finishing-branch/agents/openai.yaml`
  - `session-curator/agents/openai.yaml`
  - `session-curator/references/document-targets.md`
  - `session-curator/references/curation-quality.md`

**Consumes**

- `LocalizationBaselineSnapshot v1`（Test, no change）。
- `RuntimeLanguageDecouplingContract v1`。
- `LocalizationStyleBaseline v1`。
- `QualityGateLocalization v1`。
- `RoutingVerificationMatrix v1@T4`。
- `EnglishHeavyReviewLedger v1@T4`。

**Produces**

- `BranchContinuityLocalization v1`：三个 skill、9 个静态 case、branch routing 与 edit-plan gate invariant evidence。
- `RoutingVerificationMatrix v1@T5`。
- `EnglishHeavyReviewLedger v1@T5`。

**Covers**

`FR-005` 至 `FR-019`、`FR-021`。

**Acceptance Criteria**

1. 三个 description 中文化且 boundary 等义。
2. `checking-branch` 的三个既有稳定标题采用精确双语形式；validator 同批更新对应 marker。
3. `checking-branch` 仍只接受 `$implement` 内部 `N1 Branch Gate` 或显式 branch-only 请求；普通 implementation near-miss 仍属于 `$implement`。
4. branch 操作前仍展示 repository/branch/status；未同意 direct 且未给分支名时停止；不得 overwrite、stash、reset 或删除用户改动。
5. `finishing-branch` 仍只呈现 `keep/commit/push/PR/merge/discard` 等选择，不自动执行远端或破坏性动作。
6. `session-curator` 的既有 `Pressure Scenarios` 使用稳定双语标题；任何写入前仍先给具体修改计划并等待确认，scope 扩大时重新确认。
7. `LOC-BRANCH-*`、`LOC-FINISH-*`、`LOC-CURATOR-*` 九例通过 static review；checking-branch 的 live case 标记为 ready，另外两个登记为不做 live routing 的 residual risk。

**Verification**

```powershell
python scripts/validate-skills.py
python scripts/validate-skills.py --audit-english-heavy checking-branch/SKILL.md finishing-branch/SKILL.md session-curator/SKILL.md
python scripts/validate-skills.py --verify-localization-evidence `
  docs/features/skill-content-chinese-localization/verification-matrix.md `
  docs/features/skill-content-chinese-localization/english-heavy-review.md `
  --skills checking-branch finishing-branch session-curator `
  --require-static-pass

$batchSkills = @('checking-branch','finishing-branch','session-curator')
foreach ($skillName in $batchSkills) {
  npx --yes skills use . --skill $skillName --full-depth *> $null
  if ($LASTEXITCODE -ne 0) { throw "full-depth failed: $skillName" }
}
```

```powershell
rg -n "## 触发说明（Trigger Description）|## 压力场景（Pressure Scenarios）|## 自然交接（Natural Handoff）|N1 Branch Gate|branch-only|\$implement" checking-branch/SKILL.md scripts/validate-skills.py
rg -n "keep branch|commit|push|PR|merge|discard|references/(document-targets|curation-quality)\.md|Session Curation Plan|Session Curation Result" finishing-branch/SKILL.md session-curator/SKILL.md
rg -n "LOC-(BRANCH|FINISH|CURATOR)-(ZH|EN|NEAR)" docs/features/skill-content-chinese-localization/verification-matrix.md
git diff --check -- checking-branch/SKILL.md finishing-branch/SKILL.md session-curator/SKILL.md scripts/validate-skills.py docs/features/skill-content-chinese-localization
```

### Task 6 — Batch 4：planning workflow skill 中文化

**Files**

- **Modify**:
  - `to-spec/SKILL.md`
  - `to-plan/SKILL.md`
  - `analyze/SKILL.md`
  - `scripts/validate-skills.py`
  - `docs/features/skill-content-chinese-localization/verification-matrix.md`
  - `docs/features/skill-content-chinese-localization/english-heavy-review.md`
- **Test, no change**:
  - `docs/features/skill-content-chinese-localization/baseline-snapshot.json`
  - `docs/features/skill-content-chinese-localization/spec.md`
  - `docs/features/skill-content-chinese-localization/plan.md`
  - `docs/features/skill-content-chinese-localization/manifest.md`
  - `to-spec/agents/openai.yaml`
  - `to-plan/agents/openai.yaml`
  - `analyze/agents/openai.yaml`
  - `to-plan/references/adaptive-planning-contract.md`
  - `to-plan/examples/adaptive-planning-scenarios.md`

**Consumes**

- `LocalizationBaselineSnapshot v1`（Test, no change）。
- `RuntimeLanguageDecouplingContract v1`。
- `LocalizationStyleBaseline v1`。
- `BranchContinuityLocalization v1`。
- `RoutingVerificationMatrix v1@T5`。
- `EnglishHeavyReviewLedger v1@T5`。

**Produces**

- `PlanningWorkflowLocalization v1`：三个 planning skill、9 个静态 case、planning artifact/route/stable-field invariant evidence。
- `RoutingVerificationMatrix v1@T6`。
- `EnglishHeavyReviewLedger v1@T6`。

**Covers**

`FR-005` 至 `FR-019`、`FR-021`。

**Acceptance Criteria**

1. 三个 description 中文主句与原 trigger/near-miss boundary 等义；三个既有稳定标题采用精确双语形式，普通 `Process` 等 heading 中文化。
2. `to-spec` 仍是独立 spec-only workflow：产出 `spec.md` 与已有 manifest 更新，保留 `FR-###`/`SC-###`，不生成 plan、不运行 analyze、不实现；handoff 仅 `to-plan|none`。
3. `to-plan` 保留 `Planning Authorization`、Fast/Full、Artifact-fixable/Decision-required、`Planning Quality Status`、`CheckedPlanHandoff`、单次 Planning Run、单问题暂停和无实现/Git 授权边界；handoff 仅 `implement|none`。
4. `analyze` 仍是 existing/external/stale/unchecked artifact 的独立只读 audit；有效 Pass plan 不默认重复触发，不修 artifact；handoff 仅 `implement|to-plan|none`。
5. validator 同批更新 `ADAPTIVE_PLANNING_REQUIRED_TEXT` 的中文可见 marker，不删除稳定 contract marker。
6. `to-plan` 的 reference 与 example、三个 `agents/openai.yaml` byte-identical。
7. `LOC-TOSPEC-*`、`LOC-TOPLAN-*`、`LOC-ANALYZE-*` 九例通过 static review，live cases 标记为 ready。

**Verification**

```powershell
python scripts/validate-skills.py
python scripts/validate-skills.py --audit-english-heavy to-spec/SKILL.md to-plan/SKILL.md analyze/SKILL.md
python scripts/validate-skills.py --verify-localization-evidence `
  docs/features/skill-content-chinese-localization/verification-matrix.md `
  docs/features/skill-content-chinese-localization/english-heavy-review.md `
  --skills to-spec to-plan analyze `
  --require-static-pass

$batchSkills = @('to-spec','to-plan','analyze')
foreach ($skillName in $batchSkills) {
  npx --yes skills use . --skill $skillName --full-depth *> $null
  if ($LASTEXITCODE -ne 0) { throw "full-depth failed: $skillName" }
}
```

```powershell
rg -n "Planning Authorization|Fast Path|Full Path|Artifact-fixable|Decision-required|Planning Quality Status|CheckedPlanHandoff|FR-###|SC-###" to-plan/SKILL.md to-plan/references
rg -n "^## (Trigger Description|Pressure Scenarios|Natural Handoff|Process)$" to-spec/SKILL.md to-plan/SKILL.md analyze/SKILL.md
if ($LASTEXITCODE -eq 0) { throw 'unlocalized ordinary/stable heading remains' }
git diff --exit-code -- to-plan/references/adaptive-planning-contract.md to-plan/examples/adaptive-planning-scenarios.md to-spec/agents/openai.yaml to-plan/agents/openai.yaml analyze/agents/openai.yaml
git diff --check -- to-spec/SKILL.md to-plan/SKILL.md analyze/SKILL.md scripts/validate-skills.py docs/features/skill-content-chinese-localization
```

### Task 7 — Batch 5：设计入口 skill 中文化

**Files**

- **Modify**:
  - `brainstorming/SKILL.md`
  - `grill-me/SKILL.md`
  - `scripts/validate-skills.py`
  - `docs/features/skill-content-chinese-localization/verification-matrix.md`
  - `docs/features/skill-content-chinese-localization/english-heavy-review.md`
- **Test, no change**:
  - `docs/features/skill-content-chinese-localization/baseline-snapshot.json`
  - `docs/features/skill-content-chinese-localization/spec.md`
  - `docs/features/skill-content-chinese-localization/plan.md`
  - `docs/features/skill-content-chinese-localization/manifest.md`
  - `brainstorming/agents/openai.yaml`
  - `grill-me/agents/openai.yaml`
  - `brainstorming/examples/brainstorming-session.md`

**Consumes**

- `LocalizationBaselineSnapshot v1`（Test, no change）。
- `RuntimeLanguageDecouplingContract v1`。
- `LocalizationStyleBaseline v1`。
- `PlanningWorkflowLocalization v1`。
- `RoutingVerificationMatrix v1@T6`。
- `EnglishHeavyReviewLedger v1@T6`。

**Produces**

- `DesignEntryLocalization v1`：两个设计入口 skill、6 个静态 case、outcome/handoff/completion invariant evidence。
- `RoutingVerificationMatrix v1@T7`。
- `EnglishHeavyReviewLedger v1@T7`。

**Covers**

`FR-005` 至 `FR-019`、`FR-021`。

**Acceptance Criteria**

1. 两个 description 中文主句与原 trigger boundary 等义。
2. `brainstorming` 保持一次一个问题、2–3 个方案、分 section 确认、设计确认前不写代码或本地 artifact；`PlanningHandoffPacket v1` field 不变。
3. brainstorming outcome edge 精确保持 `implementation-plan -> to-plan`、`spec-only -> to-spec`、`stop-here -> none`；不得自动运行下游 skill。
4. `grill-me` 保持一次一个上游问题和推荐答案；完成条件前不得 `Natural Handoff` 或实现，完成后最多一个 `to-spec|to-plan|implement|none`。
5. `grill-me` 原本没有 `Trigger Description`/`Pressure Scenarios`；不得为了 matrix 新增。只将既有 `Natural Handoff` 改成稳定双语标题。
6. validator 同批更新 `GRILL_ME_REQUIRED_TEXT` 与 `ADAPTIVE_PLANNING_REQUIRED_TEXT` 的可见中文 marker，不削弱“关键问题未收束不得 handoff”。
7. example 与两个 `agents/openai.yaml` 不变；`LOC-BRAINSTORM-*`、`LOC-GRILL-*` 六例通过 static review，live cases 标记为 ready。

**Verification**

```powershell
python scripts/validate-skills.py
python scripts/validate-skills.py --audit-english-heavy brainstorming/SKILL.md grill-me/SKILL.md
python scripts/validate-skills.py --verify-localization-evidence `
  docs/features/skill-content-chinese-localization/verification-matrix.md `
  docs/features/skill-content-chinese-localization/english-heavy-review.md `
  --skills brainstorming grill-me `
  --require-static-pass

$batchSkills = @('brainstorming','grill-me')
foreach ($skillName in $batchSkills) {
  npx --yes skills use . --skill $skillName --full-depth *> $null
  if ($LASTEXITCODE -ne 0) { throw "full-depth failed: $skillName" }
}
```

```powershell
rg -n "PlanningHandoffPacket v1|implementation-plan|spec-only|stop-here|\$to-plan|\$to-spec|none" brainstorming/SKILL.md
rg -n "关键.*未收束|\$to-spec|\$to-plan|\$implement|none" grill-me/SKILL.md
rg -n "^## (Trigger Description|Pressure Scenarios)$" grill-me/SKILL.md
if ($LASTEXITCODE -eq 0) { throw 'grill-me gained a forbidden runtime section' }
git diff --exit-code -- brainstorming/examples/brainstorming-session.md brainstorming/agents/openai.yaml grill-me/agents/openai.yaml
git diff --check -- brainstorming/SKILL.md grill-me/SKILL.md scripts/validate-skills.py docs/features/skill-content-chinese-localization
```

### Task 8 — Batch 6：diagnosis/implementation 中心 skill 中文化

**Files**

- **Modify**:
  - `diagnose/SKILL.md`
  - `implement/SKILL.md`
  - `scripts/validate-skills.py`
  - `docs/features/skill-content-chinese-localization/verification-matrix.md`
  - `docs/features/skill-content-chinese-localization/english-heavy-review.md`
- **Test, no change**:
  - `docs/features/skill-content-chinese-localization/baseline-snapshot.json`
  - `docs/features/skill-content-chinese-localization/spec.md`
  - `docs/features/skill-content-chinese-localization/plan.md`
  - `docs/features/skill-content-chinese-localization/manifest.md`
  - `diagnose/agents/openai.yaml`
  - `implement/agents/openai.yaml`
  - `diagnose/references/ue/runtime-modes.md`
  - `diagnose/references/ue/regression-seams.md`
  - `diagnose/references/ue/probes-and-artifacts.md`
  - `diagnose/scripts/hitl-loop.template.sh`
  - `implement/references/quick-path.md`

**Consumes**

- `LocalizationBaselineSnapshot v1`（Test, no change）。
- `RuntimeLanguageDecouplingContract v1`。
- `LocalizationStyleBaseline v1`。
- `DesignEntryLocalization v1`。
- `RoutingVerificationMatrix v1@T7`。
- `EnglishHeavyReviewLedger v1@T7`。

**Produces**

- `ImplementationDiagnosisLocalization v1`：两个中心 skill、6 个静态 case、diagnostic/path/graph/handoff invariant evidence。
- `RoutingVerificationMatrix v1@T8`。
- `EnglishHeavyReviewLedger v1@T8`。

**Covers**

`FR-005` 至 `FR-019`、`FR-021`。

**Acceptance Criteria**

1. 两个 description 中文主句与原 trigger/near-miss boundary 等义；既有三类稳定标题采用精确双语形式。
2. `diagnose` 保留 `DiagnosticContext v1` fields、`Generic|UE`、`Active Repro|Artifact-based Triage`、`confirmed|likely|blocked`、Phase 1–6 顺序、runtime parity、artifact-only 永不 confirmed、全部 7 个 `DGN-*` ID 与 `implement|none` handoff。
3. `implement` 保留 `ImplementationPathDecision v1`、`Quick|Standard|Blocked`、写入/branch 前 dispatch、只执行一次 N1、Standard 的 N2/N3/N4/N5/N7、安全升级、全部 8 个 `IMP-*` ID、Blocked 与完成 route。稳定项是 `N1/N3/N5/N7` 等 gate ID 及语义，不是 `Branch Gate`、`Analyze Gate` 等英文可见描述。
4. Mermaid node endpoint multiset 保持 `N0,N0A,N1,HB,Q1,Q2,N2,N3,H1,N4,N5,N6,N7,N8,N9,N10` 的原结构与重数；node ID 保持，所有自然语言可见 label/edge condition 中文化。只有 matrix/ledger 证明 active cross-skill contract 必须逐字引用时，才允许保留最小 English alias。
5. validator 同批更新 consolidation/adaptive marker；可见自然语言 marker 改成中文，稳定 ID、field、enum、route count 和约束强度不弱化。
6. quick-path、UE references、template script 与两个 `agents/openai.yaml` byte-identical。
7. `LOC-DIAGNOSE-*`、`LOC-IMPLEMENT-*` 六例通过 static review，live cases 标记为 ready。

**Verification**

```powershell
python scripts/validate-skills.py
python scripts/validate-skills.py --audit-english-heavy diagnose/SKILL.md implement/SKILL.md
python scripts/validate-skills.py --verify-localization-evidence `
  docs/features/skill-content-chinese-localization/verification-matrix.md `
  docs/features/skill-content-chinese-localization/english-heavy-review.md `
  --skills diagnose implement `
  --require-static-pass

$batchSkills = @('diagnose','implement')
foreach ($skillName in $batchSkills) {
  npx --yes skills use . --skill $skillName --full-depth *> $null
  if ($LASTEXITCODE -ne 0) { throw "full-depth failed: $skillName" }
}
```

```powershell
rg -n "DiagnosticContext v1|Profile|EvidenceMode|ObservedFailure|RuntimeMode|RootCauseStatus|RegressionSeam|MissingEvidence|DGN-(GENERIC-ACTIVE|GENERIC-ARTIFACT|UE-ACTIVE|UE-ARTIFACT|UE-MODE-DRIFT|PERF-BASELINE|HANDOFF)" diagnose/SKILL.md
rg -n "ImplementationPathDecision v1|Quick|Standard|Blocked|IMP-(QUICK|STANDARD|UPGRADE|NO-REPRO|NEEDS-PLAN|NEEDS-DESIGN|EXTERNAL-FAKE-PASS|NATURAL-CONFIRM)|N1|N3|N5|N7" implement/SKILL.md
git diff --exit-code -- diagnose/agents/openai.yaml implement/agents/openai.yaml diagnose/references/ue diagnose/scripts/hitl-loop.template.sh implement/references/quick-path.md
git diff --check -- diagnose/SKILL.md implement/SKILL.md scripts/validate-skills.py docs/features/skill-content-chinese-localization
```

另外用一个只读 Python probe 从 `git show HEAD:implement/SKILL.md` 和 worktree Mermaid block 提取 `source node -> target node` multiset；`Counter` 必须完全相等。可见 label 不参与 endpoint 比较，但需人工逐边核对语义。

### Task 9 — 启用永久 guardrail 并执行全量验证

**Files**

- **Modify**:
  - `scripts/validate-skills.py`
  - `docs/features/skill-content-chinese-localization/verification-matrix.md`
  - `docs/features/skill-content-chinese-localization/english-heavy-review.md`
  - `docs/features/skill-content-chinese-localization/manifest.md`
- **Create**:
  - `docs/features/skill-content-chinese-localization/implementation-verification-report.md`
- **Test, no change**:
  - `docs/features/skill-content-chinese-localization/baseline-snapshot.json`
  - `docs/features/skill-content-chinese-localization/spec.md`
  - `docs/features/skill-content-chinese-localization/plan.md`
  - Task 1 `Files/Modify` 中列出的全部 16 个精确 `SKILL.md` 路径（本 task 不再修改）
  - `AGENTS.md`、`README.md` 与 `C:\WorkSpace\skill-development\AGENTS.md`（只验证计划内 diff）
  - `MetadataNoChangeSet v1` 中列出的 16 个精确路径
  - `LocalizationBaselineSnapshot v1.NoChangeEntries` 中展开的全部精确 `references/`、`assets/`、examples、非 validator scripts 与历史 artifact 文件路径
  - `GlobalCopyNoChangeSet v1` 中列出的 16 个精确路径
  - 父仓库除 `C:\WorkSpace\skill-development\AGENTS.md` 与目标 submodule gitlink 状态外的文件
  - 其他 submodule

**Consumes**

- `LocalizationBaselineSnapshot v1`（Test, no change）。
- `RuntimeLanguageDecouplingContract v1`。
- `LocalizationStyleBaseline v1`。
- `QualityGateLocalization v1`。
- `BranchContinuityLocalization v1`。
- `PlanningWorkflowLocalization v1`。
- `DesignEntryLocalization v1`。
- `ImplementationDiagnosisLocalization v1`。
- `RoutingVerificationMatrix v1@T8`。
- `EnglishHeavyReviewLedger v1@T8`。

**Produces**

- 永久 `SkillChineseAuthoringGuardrail v1`。
- `RoutingVerificationMatrix v1@Final` 与 `EnglishHeavyReviewLedger v1@Final`。
- `ImplementationVerificationReport v1`，落点为 `docs/features/skill-content-chinese-localization/implementation-verification-report.md`，记录 validator、inventory、full-depth、static/live routing、scope、history/global no-change 与 residual risk。其 canonical residual-risk JSONL block 位于 `<!-- RESIDUAL_RISKS_BEGIN -->` 与 `<!-- RESIDUAL_RISKS_END -->` 之间，字段为 `RiskId | AffectedSkills | Evidence | Status`。
- `manifest.md` 新增该 report 路径并将 `Implementation: Complete`；仅在全部阻塞验收通过后写入。

**Covers**

`FR-001` 至 `FR-021`。

**Acceptance Criteria**

1. validator 对动态发现的每个 skill 要求 `description` 至少包含一个 Han 字符，不设置比例、不使用临时 allowlist。
2. validator 集中维护现有稳定双语 heading inventory，检查原本存在的 section，不要求原本不存在的 section；旧 marker 集合只保留行为 contract。
3. 普通 validator 输出 `Validated 16 skills.`；English-heavy audit 的每个候选都在 ledger 中标记 translate 或带理由 keep。
4. matrix 的 skill set 与 16-skill inventory 精确相等，每个 skill 至少具备 `ZH-positive`、`EN-positive`、`near-miss`，CaseId 唯一、required field 完整、`StaticResult = pass`；ledger 中每个保留 English trigger phrase 与有效 English case 双向可追溯。
5. 16-skill name inventory、canonical H1、Natural Handoff route edge、stable ID/schema field/gate ID、Mermaid endpoint 与 normative constraint 相对 Task 1 baseline 无非授权 delta。
6. `npx skills` list 仍精确为同一组 16 个 name，16 个 full-depth 解析全部成功。
7. 对 `brainstorming`、`grill-me`、`to-plan`、`to-spec`、`analyze`、`implement`、`diagnose`、`checking-branch` 各执行至少一个正向和一个 near-miss fresh-session case；正向集合同时包含中文与英文 prompt。
8. live smoke 必须先证明模型可见 locator 指向仓库候选版本且同名全局 locator 已禁用。明确错误路由返回所属 batch 修正；不可观测或模型随机性只按 spec 记录 residual risk，不得扩大 trigger scope 刷测试。
9. 未执行 live routing 的 8 个低耦合 skill、routing 随机性、references/ 仍可能为英文、移除运行时语言契约后的行为变化写入最终报告。
10. Task 9 首尾的 `BaselineIntegrityGate v1` 均通过；manifest 更新 report 路径和 implementation 状态时保留唯一 64-hex baseline anchor 原值。
11. 历史 artifacts、全局安装副本、其他 submodule、agents metadata、reference/assets/example/script 和无关文件无本 feature 产生的修改。
12. verification report 包含 `Requirements`、`Commands run`、`Skipped validation`、`Cleanup`、`Git status`、`Residual risk` 六个 section，并由 manifest 链接。risk block 至少包含：
    - `RISK-LOW-COUPLING-LIVE-COVERAGE`，`AffectedSkills` 精确为未做 live routing 的另外 8 个 skill。
    - `RISK-ROUTING-STOCHASTICITY`。
    - `RISK-RUNTIME-LANGUAGE-CONTRACT-REMOVED`。
    - `RISK-PROGRESSIVE-DISCLOSURE-ENGLISH`。
    四项 `Status` 均为 `accepted-residual`，并有非空 `Evidence`。

**Verification**

Permanent validator 与全量 description/heading 检查：

```powershell
python scripts/validate-skills.py
python scripts/validate-skills.py --audit-english-heavy
python scripts/validate-skills.py --verify-localization-evidence `
  docs/features/skill-content-chinese-localization/verification-matrix.md `
  docs/features/skill-content-chinese-localization/english-heavy-review.md `
  --require-static-pass

@'
from pathlib import Path
import re

root = Path(".").resolve()
han = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
skills = sorted(root.glob("*/SKILL.md"))
assert len(skills) == 16, len(skills)

failures = []
for path in skills:
    lines = path.read_text(encoding="utf-8").splitlines()
    description = next(
        line.split(":", 1)[1].strip()
        for line in lines
        if line.startswith("description:")
    )
    if not han.search(description):
        failures.append(path.as_posix())
if failures:
    raise SystemExit("description 缺少中文：\n" + "\n".join(failures))

active = skills + [
    root / "AGENTS.md",
    root.parents[1] / "AGENTS.md",
    root / "README.md",
    root / "scripts/validate-skills.py",
]
forbidden = (
    "## Language Contract",
    "## 语言契约",
    "## 语言契约（Language Contract）",
    "LANGUAGE_CONTRACT_MARKER",
    "LANGUAGE_CONTRACT_EXCEPTION",
    "生成的文档和聊天输出默认以中文优先",
    "Skill 生成的 Markdown/HTML",
    "产出型 skill 必须包含统一 `Language Contract`",
    "spec 正文必须中文优先",
    "文档正文默认中文为主",
    "功能需求使用稳定 ID，并用中文描述",
    "用中文描述一个外部可观察行为",
    "用中文描述另一个可验证需求",
    "用中文描述可验证成功标准",
    "用中文描述风险",
    "用中文描述开放问题",
    "各章节描述正文是中文主文",
    "PlanningHandoffPacket v1`。使用中文主文",
)
hits = []
for path in active:
    text = path.read_text(encoding="utf-8")
    for token in forbidden:
        if token in text:
            hits.append(f"{path.as_posix()}: {token}")
if hits:
    raise SystemExit("active runtime language contract remains:\n" + "\n".join(hits))
'@ | python -
```

Inventory 与 full-depth：

```powershell
$expected = @(
  'analyze','brainstorming','checking-branch','clarify','diagnose',
  'finishing-branch','grill-me','handoff','implement',
  'improve-codebase-architecture','requesting-code-review',
  'session-curator','tdd','to-plan','to-spec',
  'verification-before-completion'
)

$listOutput = npx --yes skills add . --list
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$plain = [regex]::Replace(($listOutput -join "`n"), '\x1B\[[0-?]*[ -/]*[@-~]', '')
$actual = [regex]::Matches(
  $plain,
  '(?m)^\|\s{4}([a-z0-9]+(?:-[a-z0-9]+)*)\s*$'
) | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique
$delta = Compare-Object ($expected | Sort-Object) $actual
if ($delta -or $actual.Count -ne 16) {
  $delta
  throw "npx skill inventory mismatch: expected=16 actual=$($actual.Count)"
}
foreach ($skillName in $expected) {
  npx --yes skills use . --skill $skillName --full-depth *> $null
  if ($LASTEXITCODE -ne 0) { throw "full-depth failed: $skillName" }
}
```

Candidate-source fresh-session seam：

1. 在 OS temp 下创建一次性 Git repo，并在其 `.agents/skills/` 下为全部 16 个候选目录创建 junction；junction target 必须是当前目标仓库中的 skill 目录。
2. 用 `apply_patch` 在 temp repo 创建 routing-only `AGENTS.md` 和 `routing-result.schema.json`：要求对后续原始 user prompt 执行正常 implicit skill selection；命中时必须用 `Get-Content -Raw -LiteralPath <absolute candidate SKILL.md>` 完整读取所选候选文件，随后立即停止，不执行原任务。schema 固定 `owner/source_locator/first_gate/forbidden_owner_or_action/forbidden_action_taken` 五个 required field，禁止额外字段。该临时规则用于观测真实选择与完整读取，不把 prompt 改写成 meta-classification。
3. 构造 one-shot `skills.config=[{path="<global>/SKILL.md",enabled=false}, ...]`，只禁用实际存在的 16 个同名全局副本，不修改任何 config 文件。
4. 从 temp repo 运行 `codex debug prompt-input -c $skillsConfig "routing probe"`；解析模型可见 input，断言 16 个候选 locator 全部出现、同名全局 locator 全部不出现，并把 junction target、候选 hash 和 locator 写入 matrix。此步只证明 discoverability，不单独计为 routing pass。
5. 从 matrix 的 canonical JSONL block 选择 `LiveRequired = true` 的 case，并在发起模型调用前做精确结构检查：

```powershell
$liveCasesJson = @'
from pathlib import Path
import json

matrix = Path("docs/features/skill-content-chinese-localization/verification-matrix.md").read_text(encoding="utf-8")
body = matrix.split("<!-- ROUTING_CASES_BEGIN -->", 1)[1].split("<!-- ROUTING_CASES_END -->", 1)[0]
cases = [json.loads(line) for line in body.splitlines() if line.lstrip().startswith("{")]
live = [case for case in cases if case["LiveRequired"] is True]
targets = {
    "brainstorming", "grill-me", "to-plan", "to-spec",
    "analyze", "implement", "diagnose", "checking-branch",
}
assert len(live) == 16, len(live)
assert {case["Skill"] for case in live} == targets
for skill in targets:
    owned = [case for case in live if case["Skill"] == skill]
    assert len(owned) == 2
    assert sum(case["CaseKind"] == "near-miss" for case in owned) == 1
    assert sum(case["CaseKind"] in {"ZH-positive", "EN-positive"} for case in owned) == 1
positive_languages = {
    case["PromptLanguage"]
    for case in live
    if case["CaseKind"] in {"ZH-positive", "EN-positive"}
}
assert {"zh", "en"} <= positive_languages
print(json.dumps(live, ensure_ascii=False))
'@ | python -
$liveCases = @($liveCasesJson | ConvertFrom-Json)
```

6. 先运行一个显式 `$clarify` control probe，只接受 JSONL 中成功的 `item.completed`、`item.type = command_execution` event，并确认当前 CLI 能观测到包含候选绝对 `clarify/SKILL.md` 与 `Get-Content -Raw -LiteralPath` 的完整读取 command。只有该 control 也无法暴露这种 event 时，才把 `readObservationAvailable` 设为 false；普通 live case 自己没有读文件不能冒充基础设施不可观测。

```powershell
$controlEventsPath = Join-Path $tempProject 'control-clarify.events.jsonl'
$controlLastPath = Join-Path $tempProject 'control-clarify.last.json'
codex -a never exec --ephemeral --ignore-user-config --sandbox read-only `
  -c $skillsConfig -C $tempProject --json `
  --output-schema (Join-Path $tempProject 'routing-result.schema.json') `
  -o $controlLastPath `
  '$clarify：这是 observation control；按 routing-only AGENTS.md 读取候选 skill 后立即报告。' |
  Tee-Object -FilePath $controlEventsPath
if ($LASTEXITCODE -ne 0) { throw 'clarify observation control failed' }

$controlCommands = @(
  Get-Content -Encoding UTF8 $controlEventsPath |
    ForEach-Object { $_ | ConvertFrom-Json } |
    Where-Object {
      $_.type -eq 'item.completed' -and
      $_.item.type -eq 'command_execution' -and
      $_.item.status -eq 'completed' -and
      (
        -not $_.item.PSObject.Properties['exit_code'] -or
        $_.item.exit_code -eq 0
      )
    } |
    ForEach-Object { [string]$_.item.command }
)
$clarifyCandidate = (
  Resolve-Path -LiteralPath (Join-Path $candidateRoot 'clarify\SKILL.md')
).Path
$readerPattern = '(?i)Get-Content\s+-Raw\s+-LiteralPath'
$readObservationAvailable = @(
  $controlCommands | Where-Object {
    $_ -match $readerPattern -and
    (
      $_ -match [regex]::Escape($clarifyCandidate) -or
      $_ -match [regex]::Escape($clarifyCandidate.Replace('\','/'))
    )
  }
).Count -gt 0
$controlEventsSha256 = (
  Get-FileHash -Algorithm SHA256 -LiteralPath $controlEventsPath
).Hash.ToLowerInvariant()
$observationFailure = if ($readObservationAvailable) {
  ''
} else {
  'control probe produced no successful full-file command-read event'
}
```

7. 对上述 16 个 case 逐一把 matrix 中的 `Prompt` 原样交给 fresh session，不在 user prompt 中加入 skill name 或分类问题：

```powershell
foreach ($case in $liveCases) {
  $eventsPath = Join-Path $tempProject "$($case.CaseId).events.jsonl"
  $lastPath = Join-Path $tempProject "$($case.CaseId).last.json"

  codex -a never exec --ephemeral --ignore-user-config --sandbox read-only `
    -c $skillsConfig -C $tempProject --json `
    --output-schema (Join-Path $tempProject 'routing-result.schema.json') `
    -o $lastPath $case.Prompt |
    Tee-Object -FilePath $eventsPath
  if ($LASTEXITCODE -ne 0) { throw "codex exec failed: $($case.CaseId)" }

  $eventObjects = @(
    Get-Content -Encoding UTF8 $eventsPath |
      ForEach-Object { $_ | ConvertFrom-Json }
  )
  $allCommandEvents = @(
    $eventObjects |
      Where-Object {
        $_.type -in @('item.started','item.completed') -and
        $_.item.type -eq 'command_execution'
      }
  )
  $commandEvents = @(
    $allCommandEvents |
      Where-Object {
        $_.type -eq 'item.completed' -and
        $_.item.status -eq 'completed' -and
        (
          -not $_.item.PSObject.Properties['exit_code'] -or
          $_.item.exit_code -eq 0
        )
      }
  )
  $commands = @($commandEvents | ForEach-Object { [string]$_.item.command })
  $allCommands = @($allCommandEvents | ForEach-Object { [string]$_.item.command })
  $mutationPattern = '(?i)(Set-Content|Add-Content|Out-File|Remove-Item|Move-Item|Copy-Item|New-Item|apply_patch|git\s+(?:add|commit|checkout|switch|reset|clean|push|merge))'
  $mutationItemEvents = @(
    $eventObjects |
      Where-Object {
        $_.type -in @('item.started','item.completed') -and
        $_.item.type -in @('file_change','mcp_tool_call')
      }
  )
  $mutationCommandEvents = @(
    $allCommands |
      Where-Object { $_ -match $mutationPattern }
  )
  $mutationEventCount = $mutationItemEvents.Count + $mutationCommandEvents.Count
  if ($mutationEventCount -ne 0) {
    throw "mutation/tool event observed: $($case.CaseId)"
  }
  $result = Get-Content -Raw -Encoding UTF8 $lastPath | ConvertFrom-Json
  if ($result.owner -ne $case.ExpectedOwner) {
    throw "wrong owner: $($case.CaseId)"
  }
  if (
    $result.forbidden_owner_or_action -ne $case.ForbiddenOwnerOrAction -or
    $result.forbidden_action_taken -ne $false
  ) {
    throw "forbidden owner/action mismatch: $($case.CaseId)"
  }
  if ($result.first_gate -ne $case.ExpectedGate) {
    throw "gate mismatch: $($case.CaseId)"
  }

  $expectedPath = if ($case.ExpectedOwner -eq 'none') {
    $null
  } else {
    (Resolve-Path -LiteralPath (Join-Path $candidateRoot "$($case.ExpectedOwner)\SKILL.md")).Path
  }
  $forbiddenPath = (
    Resolve-Path -LiteralPath (Join-Path $candidateRoot "$($case.Skill)\SKILL.md")
  ).Path
  if ($case.ExpectedOwner -eq 'none') {
    if ($result.source_locator -ne 'none') {
      throw "none owner returned a source locator: $($case.CaseId)"
    }
  } else {
    $reportedSource = [System.IO.Path]::GetFullPath([string]$result.source_locator)
    if (-not $reportedSource.Equals(
      $expectedPath,
      [System.StringComparison]::OrdinalIgnoreCase
    )) {
      throw "candidate source locator mismatch: $($case.CaseId)"
    }
  }
  $readerPattern = '(?i)Get-Content\s+-Raw\s+-LiteralPath'
  $candidatePaths = @(
    Get-ChildItem -LiteralPath $candidateRoot -Directory |
      Where-Object {
        Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md')
      } |
      ForEach-Object {
        (Resolve-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md')).Path
      }
  )
  $observedReadPaths = @(
    foreach ($candidatePath in $candidatePaths) {
      $didRead = @(
        $commands | Where-Object {
          $_ -match $readerPattern -and
          (
            $_ -match [regex]::Escape($candidatePath) -or
            $_ -match [regex]::Escape($candidatePath.Replace('\','/'))
          )
        }
      ).Count -gt 0
      if ($didRead) { $candidatePath }
    }
  )
  $expectedRead = $null -ne $expectedPath -and (
    $observedReadPaths -contains $expectedPath
  )
  $forbiddenRead = $observedReadPaths -contains $forbiddenPath

  if ($readObservationAvailable) {
    if ($case.ExpectedOwner -ne 'none' -and -not $expectedRead) {
      throw "candidate SKILL.md was not read: $($case.CaseId)"
    }
    if ($case.ExpectedOwner -eq 'none' -and $observedReadPaths.Count -ne 0) {
      throw "none-owner case read a candidate skill: $($case.CaseId)"
    }
    $unexpectedReads = @(
      $observedReadPaths |
        Where-Object { $_ -ne $expectedPath }
    )
    if ($case.ExpectedOwner -ne 'none' -and $unexpectedReads.Count -ne 0) {
      throw "unexpected candidate skill read: $($case.CaseId)"
    }
    if ($case.CaseKind -eq 'near-miss' -and $forbiddenRead) {
      throw "near-miss read forbidden skill: $($case.CaseId)"
    }
    $liveResult = 'pass'
  } else {
    $liveResult = 'unobservable-residual-risk'
  }
  $eventsSha256 = (
    Get-FileHash -Algorithm SHA256 -LiteralPath $eventsPath
  ).Hash.ToLowerInvariant()
  $readEvent = if ($observedReadPaths.Count -eq 0) {
    ''
  } else {
    ($commands | Where-Object { $_ -match $readerPattern }) -join "`n"
  }

  # 将 owner/gate/action、成功的完整 command-read event 或 control-probe
  # 不可观测证据、MutationEventCount、$eventsSha256、
  # $controlEventsSha256、$observationFailure 与 $liveResult 写回
  # CandidateSourceSmoke。
}
```

每例保留原始 JSONL hash、实际 candidate `SKILL.md` command-read event 与归一化结果；最多允许一次相同原始 prompt 重试来识别 flake，不调整 trigger phrase。明确错误 owner、读取 forbidden skill、gate 丢失、`ForbiddenOwnerOrAction` 未被遵守或发生 forbidden action 都返回所属 batch 修正；只有 control probe 已证明 CLI 无法暴露 read event 时才能记录 `unobservable-residual-risk`。

全部 16 个 live case 写回 matrix 后，才运行 live-resolved gate：

```powershell
python scripts/validate-skills.py --verify-localization-evidence `
  docs/features/skill-content-chinese-localization/verification-matrix.md `
  docs/features/skill-content-chinese-localization/english-heavy-review.md `
  --require-static-pass `
  --require-live-resolved
```

随后在 OS temp copy 上分别把一个 `pass` smoke record 的 `EventsSha256` 改为非 64-hex、清空 `ReadEvent`、把 `MutationEventCount` 改为 1；三次 `--require-live-resolved` 都必须返回非零，证明 final live gate 没有漏检关键证据。

Scope 与 no-change：

```powershell
git status --short
git diff --check
git diff --exit-code -- `
  docs/features/spec-plan-workflow `
  docs/features/adaptive-planning-workflow `
  docs/features/natural-handoff-workflow `
  docs/features/workflow-skill-consolidation

git -C ..\.. status --short
git -C ..\.. submodule status --recursive
git -C ..\.. diff --check
```

`git status` 的打印结果不是 pass 条件；随后执行 changed-path allowlist、snapshot hash 与新 artifact integrity 断言：

```powershell
@'
from pathlib import Path
import hashlib
import json
import re
import subprocess

root = Path(".").resolve()
parent = root.parents[1]
feature_prefix = "docs/features/skill-content-chinese-localization/"
allowed_feature = {
    feature_prefix + name for name in (
        "spec.md", "plan.md", "manifest.md", "baseline-snapshot.json",
        "verification-matrix.md", "english-heavy-review.md",
        "implementation-verification-report.md",
    )
}
allowed_target = {
    "AGENTS.md",
    "README.md",
    "scripts/validate-skills.py",
    *allowed_feature,
    *{f"{name}/SKILL.md" for name in (
        "analyze", "brainstorming", "checking-branch", "clarify", "diagnose",
        "finishing-branch", "grill-me", "handoff", "implement",
        "improve-codebase-architecture", "requesting-code-review",
        "session-curator", "tdd", "to-plan", "to-spec",
        "verification-before-completion",
    )},
}
allowed_parent = {"AGENTS.md", "submodules/fjxyyzg3-Skills"}

def changed(repo):
    output = subprocess.check_output(
        ["git", "-C", str(repo), "status", "--porcelain=v1", "--untracked-files=all"],
        text=True,
        encoding="utf-8",
    )
    return {line[3:].replace("\\", "/") for line in output.splitlines() if line}

target_changes = changed(root)
unexpected_target = {
    path for path in target_changes
    if path not in allowed_target
}
assert not unexpected_target, sorted(unexpected_target)

parent_changes = changed(parent)
assert parent_changes <= allowed_parent, sorted(parent_changes - allowed_parent)

snapshot_path = root / feature_prefix / "baseline-snapshot.json"
manifest_path = root / feature_prefix / "manifest.md"
manifest = manifest_path.read_text(encoding="utf-8")
anchors = re.findall(
    r"(?m)^- Baseline Snapshot SHA-256: `([0-9a-f]{64})`$",
    manifest,
)
assert len(anchors) == 1, anchors
assert hashlib.sha256(snapshot_path.read_bytes()).hexdigest() == anchors[0]
snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
assert snapshot["Version"] == "LocalizationBaselineSnapshot v1"
assert snapshot["TargetHead"] == subprocess.check_output(
    ["git", "rev-parse", "HEAD"], cwd=root, text=True, encoding="utf-8"
).strip()

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

for group in ("NoChangeEntries", "GlobalCopyEntries"):
    for entry in snapshot[group]:
        path = Path(entry["Path"])
        assert path.is_absolute(), path
        assert path.exists() is entry["Exists"], path
        if entry["Exists"]:
            assert sha256(path) == entry["Sha256"], path

feature_files = sorted((root / feature_prefix).glob("*"))
for path in feature_files:
    if not path.is_file():
        continue
    data = path.read_bytes()
    assert not data.startswith(b"\xef\xbb\xbf"), f"UTF-8 BOM: {path}"
    text = data.decode("utf-8")
    assert "\r" not in text, f"non-LF newline: {path}"
    bad = [i for i, line in enumerate(text.splitlines(), 1) if line != line.rstrip()]
    assert not bad, f"trailing whitespace {path}: {bad[:10]}"

report = (root / feature_prefix / "implementation-verification-report.md").read_text(encoding="utf-8")
for heading in (
    "## Requirements", "## Commands run", "## Skipped validation",
    "## Cleanup", "## Git status", "## Residual risk",
):
    assert heading in report, heading
risk_body = report.split("<!-- RESIDUAL_RISKS_BEGIN -->", 1)[1].split(
    "<!-- RESIDUAL_RISKS_END -->", 1
)[0]
risks = [
    json.loads(line)
    for line in risk_body.splitlines()
    if line.lstrip().startswith("{")
]
required_risk_ids = {
    "RISK-LOW-COUPLING-LIVE-COVERAGE",
    "RISK-ROUTING-STOCHASTICITY",
    "RISK-RUNTIME-LANGUAGE-CONTRACT-REMOVED",
    "RISK-PROGRESSIVE-DISCLOSURE-ENGLISH",
}
by_id = {risk["RiskId"]: risk for risk in risks}
assert required_risk_ids <= by_id.keys()
for risk_id in required_risk_ids:
    assert by_id[risk_id]["Status"] == "accepted-residual"
    assert by_id[risk_id]["Evidence"].strip()
assert set(by_id["RISK-LOW-COUPLING-LIVE-COVERAGE"]["AffectedSkills"]) == {
    "clarify", "improve-codebase-architecture", "handoff", "tdd",
    "requesting-code-review", "verification-before-completion",
    "finishing-branch", "session-curator",
}
manifest = (root / feature_prefix / "manifest.md").read_text(encoding="utf-8")
assert "implementation-verification-report.md" in manifest
assert "Implementation: Complete" in manifest
'@ | python -
```

另将 snapshot 的 `SubmoduleStatus` 与最终 `git submodule status --recursive` 比较；目标 submodule 允许工作树 dirty，但 commit SHA 不得漂移，其他 submodule 的 SHA/status 必须逐字一致。temp repo 清理前解析并确认其绝对路径位于 OS temp，且只移除本 task 创建的目录。

## 覆盖自检 (Coverage Self-check)

### Functional Requirements

| Requirement | Tasks | Verification seam |
| --- | --- | --- |
| `FR-001` | 1, 9 | 16-skill baseline；最终动态 inventory CJK guard |
| `FR-002` | 1, 9 | active forbidden-marker scan；最终 scope audit |
| `FR-003` | 1, 9 | `RuntimeLanguageDecouplingContract v1`；最终 docs/skill scan |
| `FR-004` | 1, 9 | 四个历史目录 no-change diff |
| `FR-005` | 2, 4–9 | 每批 description/name/H1 检查；最终 CJK 与 inventory |
| `FR-006` | 1, 2, 4–9 | English case mapping + ledger trace |
| `FR-007` | 2, 4–9 | scoped audit；最终 English-heavy 全量审阅 |
| `FR-008` | 2, 5–9 | 双语 heading marker；最终集中 heading inventory |
| `FR-009` | 1, 2, 4–9 | stable-token baseline/final count |
| `FR-010` | 1, 2, 4–9 | 每 skill ZH/EN/NEAR case 与既有 scenario diff |
| `FR-011` | 5–9 | schema/field invariant；Mermaid endpoint multiset |
| `FR-012` | 1, 2, 4–9 | route/stop/artifact contract invariant |
| `FR-013` | 2–9 | human calibration；normative constraint ledger |
| `FR-014` | 1–9 | `EnglishHeavyReviewLedger v1` |
| `FR-015` | 2–8 | 六批顺序 + Task 3 human gate |
| `FR-016` | 2, 4–9 | scoped heading checks；最终全 inventory CJK hard gate |
| `FR-017` | 2–9 | non-blocking `--audit-english-heavy` |
| `FR-018` | 1–9 | 48+ 独立 static cases；禁止新增 runtime section |
| `FR-019` | 5–9 | 8-skill candidate-source fresh-session smoke |
| `FR-020` | 1, 9 | `npx skills` exact list + 16 full-depth loop |
| `FR-021` | 1–9 | 每批 scoped diff；最终 parent/submodule/global audit |

### Success Criteria

| Criterion | Tasks | Verification seam |
| --- | --- | --- |
| `SC-001` | 1–9 | 每批及最终 validator 输出 |
| `SC-002` | 2, 4–9 | description CJK、English case trace |
| `SC-003` | 1, 9 | active forbidden-marker 与历史 no-change scan |
| `SC-004` | 1–9 | scoped/final English-heavy audit + ledger |
| `SC-005` | 1, 2, 4–9 | route/stable-token/normative invariant |
| `SC-006` | 1–9 | 48+ unique case assertion |
| `SC-007` | 5–9 | source-isolated 8-skill live smoke |
| `SC-008` | 2–8 | Task 3 approval + per-batch validator/audit/diff |
| `SC-009` | 1, 9 | exact inventory + full-depth loop |
| `SC-010` | 1, 9 | history/global/other-submodule no-change |
| `SC-011` | 9 | `ImplementationVerificationReport v1` residual-risk section |

## Planning Quality Gate

- **RequirementsCoverage**: Pass — `FR-001` 至 `FR-021` 均映射到至少一个 task 和可执行 verification seam。
- **TaskCompleteness**: Pass — 9 个 task 均包含 `Files`、`Consumes`、`Produces`、`Covers`、`Acceptance Criteria`、`Verification`。
- **ContractConsistency**: Pass — `RuntimeLanguageDecouplingContract v1`、`LocalizationStyleBaseline v1` 与各批次 localization contract 的 producer/consumer 顺序闭合；无悬空产物。
- **RepositoryFeasibility**: Pass — 路径、16-skill inventory、validator、`npx skills`、实际 UE reference 文件、Codex source-locator/debug 与 ephemeral CLI flags 已在当前环境核验。
- **ConstraintAlignment**: Pass — 只同步父工作区直接冲突的 active `AGENTS.md`；保留父仓库其他文件、历史 artifacts、global copies、reference/assets、agents metadata、其他 submodule 与 Git 授权边界；只接受 FR-002 的运行时语言行为变化。
- **AutoFixSummary**:
  - 将全 inventory CJK hard gate 延后到 Batch 6 后，避免当前 15 个英文 description 造成 Phase 0 假失败。
  - 把 `to-spec` 和 `brainstorming` 中散落的等价运行时中文保证纳入原子移除。
  - 增加 candidate locator 可见性与全局同名副本 one-shot disable，区分 full-depth 解析和真实 fresh-session routing。
  - 要求 live JSONL 证明实际读取候选 `SKILL.md`，避免把 meta-classification 冒充 routing。
  - 将 matrix/ledger 改为可机器解析的 canonical JSONL，并增加 exact 16×3、stable/route count、English trace 与 live-result verifier。
  - 增加 immutable-by-contract baseline snapshot、changed-path allowlist、全局/历史 hash 对比和独立 verification report。
  - 用 manifest 中的 `BaselineDigestAnchor v1` 锁定 snapshot，并把已检查的 spec/plan 纳入逐 task 完整性 gate。
  - 纳入父工作区 active `AGENTS.md`，关闭其旧 `Language Contract` 要求与目标仓库新规则的冲突。
  - 将 Batch 1 human calibration 拆成独立阻塞 gate，并让后续五批显式消费同一 baseline。
- **ResidualRisks**:
  - live routing 受模型随机性影响；精确 candidate source 可证明，但代表性 smoke 不能替代长期全量 eval。
  - 未做 live routing 的 8 个低耦合 skill 只由静态 case、description diff 和 full-depth 覆盖。
  - `references/`、`assets/` 和 examples 保持原文，progressive disclosure 仍可能加载英文内容。
  - 删除 `Language Contract` 后，独立安装的 skill 不再保证中文输出；这是已接受的行为变化。
  - 实现会在 Task 3 等待一次用户校准确认。
- **Planning Quality Status**: Pass

## Checked Plan Handoff

| Field | Value |
| --- | --- |
| `PlanningMode` | `Full` |
| `ArtifactPaths` | `docs/features/skill-content-chinese-localization/spec.md`; `docs/features/skill-content-chinese-localization/plan.md` |
| `Coverage` | `FR-001..FR-021 -> Task 1..9 -> scoped validator/static matrix/live smoke/scope audit` |
| `QualityStatus` | `Pass` |
| `AutoFixSummary` | 见 Planning Quality Gate |
| `Assumptions` | 16-skill snapshot 与仓库 contract 在 implementation intake 时未发生实质漂移 |
| `ResidualRisks` | routing 随机性、8 个低耦合 skill 未 live、progressive disclosure 英文材料、已接受的运行时语言保证移除 |
| `NextSkill` | `$implement` |

本 handoff 只证明 planning artifacts 已检查，不批准 branch、skill 正文修改、测试修改、review、verification、commit 或 push。
