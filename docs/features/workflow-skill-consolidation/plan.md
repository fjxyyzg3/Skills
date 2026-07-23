# Workflow Skill Consolidation Plan

## 元数据 (Metadata)

- **Source**: `docs/features/workflow-skill-consolidation/spec.md`
- **Generated at**: 2026-07-23
- **Status**: Ready
- **Planning Mode**: Full
- **Risk rationale**: 本 feature 删除三个公开 Skill 入口，改变 implementation、diagnosis 与 Natural Handoff 核心 workflow，跨越多个 Skill、metadata、references、validator、submodule living docs 与父仓库 `CLAUDE.md`，并产生明确 breaking migration。

## 假设 (Assumptions)

- 当前 baseline 为 19 个 Skill，`python scripts/validate-skills.py` 输出 `Validated 19 skills.`。
- 当前 `npx skills` 版本为 1.5.18；`npx --yes skills add . --list` 已验证可从本地目录发现 19 个 Skill。
- 仓库没有 `package.json`、plugin/marketplace manifest 或额外 registry；Skill discovery 直接来自顶层目录中的 `SKILL.md`。
- 用户已明确接受删除 `quick-change`、`diagnose-ue`、`workflow-router`，不需要 alias、facade 或旧显式命令兼容。
- 新 feature workspace 不存在 `manifest.md`，因此本 Full Planning Run 只创建 `spec.md + plan.md`。
- `docs/features/**`、父仓库 `quality-report-*`、`improvement-plan-*`、`update-report-*` 是历史 artifacts，不随 active contract 回写。
- 父仓库 `CLAUDE.md` 是 living contract；父仓库 `AGENTS.md` 当前不引用三个 retired entries，无需修改。
- 当前仓库没有自动执行跨 turn prompt routing 的 eval harness；path/profile 选择和 Natural Handoff 需要 static markers 加 fresh-session manual scenarios。

## 全局约束 (Global Constraints)

- 用户可见文档与 Skill 正文默认中文优先；命令、路径、contract fields、稳定 ID 与必要技术术语保留 English。
- 修改必须 surgical，只覆盖本 plan 列出的 Skill、active docs、validator 与父仓库 living contract；不得修改其他 submodule。
- `implement` 与 `diagnose` 必须通过同目录 references 使用 progressive disclosure，保留单 Skill `--full-depth` 自包含性，不读取 sibling Skill 文件。
- Quick/Standard dispatch 必须发生在任何写入与 branch 操作前；Quick 只有全部资格条件成立才能进入。
- Artifact-based Triage 不得声称已复现或输出 confirmed root cause。
- `Natural Handoff` 继续最多推荐一个 next Skill 或 `none`，且不得绕过目标 Skill 的内部 gate。
- `checking-branch`、`tdd`、`requesting-code-review`、`verification-before-completion`、`finishing-branch`、独立 `$to-spec` / `$analyze` 与 session Skills 保持独立。
- retired-token 检查只覆盖 active surfaces，必须排除 `docs/features/**` 与父仓库历史 reports。
- submodule validator 必须 standalone，不得读取或依赖 `../../CLAUDE.md`。
- 所有 task 按编号串行执行；不要在实现过程中保留同时有效的第二套 public routing contract。
- 本 plan 不授权 branch、commit、push、PR、merge、discard、安装用户 Skill 副本或远端操作。

## Task 列表 (Tasks)

### Task 1: 将低风险实现收敛为 `$implement` Quick Path

- **Files**:
  - Modify: `implement/SKILL.md`
  - Create: `implement/references/quick-path.md`
  - Modify: `implement/agents/openai.yaml`
  - Test: `scripts/validate-skills.py`
- **Consumes**: `Workflow Skill Consolidation Spec v1`（`docs/features/workflow-skill-consolidation/spec.md` 中的 Quick/Standard architecture、`ImplementationPathDecision v1` 与 `FR-002..FR-007`）
- **Produces**: `ImplementationPathContract v1`（包含 `Path: Quick | Standard | Blocked`、`Evidence`、`Scope`、`Acceptance`、`Verification`、`EscalationReason`，以及 Quick qualification/disqualifier、Quick→Standard 和 blocker handoff 规则）
- **Covers**: `FR-002`, `FR-003`, `FR-004`, `FR-005`, `FR-006`, `FR-007`, `FR-018`

**验收标准 (Acceptance Criteria)**:

- [ ] `implement` 的 description、进入边界、Trigger Description、Pressure Scenarios 和 metadata 同时覆盖 low-risk tight change、conversation-scoped work 与 checked-plan implementation。
- [ ] 在现有 branch gate 前增加只读 Path Dispatch；它输出 `ImplementationPathDecision v1`，且在选择 Quick 前逐项证明所有资格条件。
- [ ] `implement/references/quick-path.md` 成为 Quick qualification、disqualifiers、`Scope / Acceptance / Verification`、repro/test、light review、result 与 escalation 的 single source of truth。
- [ ] Quick Path 复用现有 branch gate，执行 targeted failing signal、最小实现、light self-review 和共享 final verification；它不默认执行独立 review subagent。
- [ ] Standard Path 保留 `N1 Branch Gate`、checked-plan/conditional-analyze intake、serial TDD tasks、`N5 Review Subagent Gate`、fix/re-review、`N7 Verification Gate` 和 finish decision。
- [ ] scope、acceptance 和 branch authorization 不变时，Quick 发现 shared contract、core workflow、multi-task 或更宽验证需求，直接转入 Standard intake，不重复 branch gate。
- [ ] scope/acceptance/architecture 改变时停止并唯一推荐 `$to-plan` 或 `$brainstorming`；约 10–15 分钟仍无可靠 bug seam 时停止并唯一推荐 `$diagnose`。
- [ ] Quick 与 Standard 的 completion checklist 使用条件项，不再把 Standard 的 checked-plan/TDD/review-subagent要求强加给 Quick。
- [ ] `agents/openai.yaml` 的 `short_description` 长度、单行 quoted `default_prompt` 与 `$implement` 引用继续通过 validator。

**验证命令 (Verification)**:

- `python scripts/validate-skills.py`，在旧目录尚未删除时预期仍输出 `Validated 19 skills.`。
- `rg -n "Quick Path|Standard Path|ImplementationPathDecision|Scope.*Acceptance.*Verification|N1 Branch Gate|N5 Review Subagent Gate|N7 Verification Gate|\$diagnose|\$to-plan|\$brainstorming" implement/SKILL.md implement/references/quick-path.md`，预期所有 dispatch、contract、gate 和 blocker markers 均有命中。
- `npx --yes skills use . --skill implement --full-depth`，预期 exit code 0，输出包含新 Quick reference。

### Task 2: 将 UE 诊断收敛为 `$diagnose` 的条件 Profile

- **Files**:
  - Modify: `diagnose/SKILL.md`
  - Modify: `diagnose/agents/openai.yaml`
  - Create from `diagnose-ue/references/runtime-modes.md`: `diagnose/references/ue/runtime-modes.md`
  - Create from `diagnose-ue/references/probes-and-artifacts.md`: `diagnose/references/ue/probes-and-artifacts.md`
  - Create from `diagnose-ue/references/regression-seams.md`: `diagnose/references/ue/regression-seams.md`
  - Test: `scripts/validate-skills.py`
- **Consumes**: `Workflow Skill Consolidation Spec v1`（Generic/UE Profile、Active Repro/Artifact-based Triage、`DiagnosticContext v1` 与 `FR-008..FR-012`）以及三个现有 `diagnose-ue/references/*.md`
- **Produces**: `DiagnosticProfileContract v1`（包含 `Profile: Generic | UE`、`EvidenceMode: Active Repro | Artifact-based Triage`、`ObservedFailure`、`RuntimeMode`、`RootCauseStatus`、`RegressionSeam`、`MissingEvidence` 和唯一 repair handoff）
- **Covers**: `FR-008`, `FR-009`, `FR-010`, `FR-011`, `FR-012`, `FR-018`

**验收标准 (Acceptance Criteria)**:

- [ ] `diagnose` description、Trigger Description、Pressure Scenarios、output contract 和 metadata 同时覆盖 generic bug/performance regression 与 Unreal Engine crash/assert/PIE/Packaged/Blueprint/cook/network/rendering/platform symptoms。
- [ ] canonical `diagnose/SKILL.md` 只保留一套 six-phase protocol，不复制第二套 UE Phase 1–6。
- [ ] Phase 1 前记录 `DiagnosticContext v1`，独立选择 Generic/UE Profile 和 Active Repro/Artifact-based Triage。
- [ ] Active Repro 可在 loop 可建立但目标 failure 尚未观察时以 `ObservedFailure: pending`、`RootCauseStatus: blocked` 开始；Phase 2 仍未观察到目标 failure 时停止或转入 Artifact-based Triage，不进入 hypotheses。
- [ ] UE Profile 只在对应条件成立时读取 `references/ue/`；Generic Profile 不读取或输出无关 UE runtime workflow。
- [ ] Active Repro 无可信 loop 时不得假装进入 reproduce；有 concrete artifacts 时可以进入 Artifact-based Triage，列出 3–5 个 falsifiable hypotheses 与 probes。
- [ ] Artifact-based Triage 明确“未复现”，`RootCauseStatus` 只允许 `likely` 或 `blocked`；后续取得运行环境时可以转入 Active Repro。
- [ ] 初始 `RootCauseStatus` 只允许 `likely/blocked`；Active Repro 只有在 exact failure、prediction、targeted probe/causal intervention、主要替代假设排除和 evidence pointer 全部成立后才能提升为 `confirmed`。
- [ ] UE runtime/probe/regression 内容迁移到三个同目录 references；`probes-and-artifacts.md` 补充 UE hypothesis dimensions、cleanup 与纯 `.rdc` caveat，`regression-seams.md` 的 repair entry 统一为 `$implement`。
- [ ] Packaged/RHI/network/platform-only failure 必须在对应 runtime mode 验证；`[DEBUG-UE-*]`、Blueprint probe、临时 map/asset/capture 的去留明确。
- [ ] repair-ready 时唯一推荐 `$implement`；证据不足、没有正确 seam 或只需报告时以 `none` 结束，architecture observation 只能作为 residual/follow-up，不能产生第二个 next Skill。
- [ ] `diagnose/scripts/hitl-loop.template.sh` 原样保留。

**验证命令 (Verification)**:

- `python scripts/validate-skills.py`，在旧目录尚未删除时预期仍输出 `Validated 19 skills.`。
- `rg -n "Generic Profile|UE Profile|Active Repro|Artifact-based Triage|DiagnosticContext|RootCauseStatus|references/ue/.*\.md|## Natural Handoff|\$implement" diagnose/SKILL.md diagnose/references/ue`，预期双轴 dispatch、三条 references、claim boundary 和 handoff 均有命中。
- `rg -n "quick-change|diagnose-ue|workflow-router" diagnose/SKILL.md diagnose/agents/openai.yaml diagnose/references/ue`，预期零命中。
- `npx --yes skills use . --skill diagnose --full-depth`，预期 exit code 0，输出包含三个 UE references 与既有 HITL script。

### Task 3: 重连 retained Skills 与 active repository contract

- **Files**:
  - Modify: `brainstorming/SKILL.md`
  - Modify: `brainstorming/examples/brainstorming-session.md`
  - Modify: `grill-me/SKILL.md`
  - Modify: `session-curator/SKILL.md`
  - Modify: `checking-branch/SKILL.md`
  - Modify: `checking-branch/agents/openai.yaml`
  - Modify: `to-plan/SKILL.md`
  - Modify: `to-spec/SKILL.md`
  - Modify: `README.md`
  - Modify: `AGENTS.md`
  - Test: retained `*/SKILL.md`, `*/agents/openai.yaml`, `*/references/**/*.md`, `*/examples/**/*.md`
- **Consumes**: `ImplementationPathContract v1` 与 `DiagnosticProfileContract v1`
- **Produces**: `DirectRoutingContract v1`（frontmatter/metadata 初始触发、per-Skill `Natural Handoff`、六个自然确认语、唯一推荐绑定、目标 Skill gate 保留，以及 direct `$implement` / `$diagnose` owner routes）
- **Covers**: `FR-012`, `FR-013`, `FR-014`, `FR-015`, `FR-018`

**验收标准 (Acceptance Criteria)**:

- [ ] retained Skills 不再声明只能经 `workflow-router` 进入；显式调用、context trigger 和上一条唯一 Natural Handoff 均可直接进入。
- [ ] `grill-me` 在 implementation-ready 时只推荐 `$implement`；Quick/Standard 不在上游重复判断。
- [ ] `brainstorming` 与其 example 删除 retired implementation entry，但继续只按 outcome 推荐 `$to-plan`、`$to-spec` 或 `none`。
- [ ] `to-plan` 不再把低风险直接改动路由到 retired entry，改为说明 `$implement` 内部选择 Quick/Standard；Planning Authorization 边界保持不变。
- [ ] `to-spec` 与 `session-curator` 移除中央 router 依赖，分别保留 formal-spec 与 explicit-plan-confirmation安全边界。
- [ ] README 移除中央 Router 节点，展示 task context 直接进入最小必要 Skill；Skill inventory 精确列出 16 个 retained names。
- [ ] README 与 AGENTS 将低风险实现归入 `$implement` Quick Path，将 UE 症状归入 `$diagnose` UE Profile，并继续保留 Natural Handoff 与 implementation safety gates。
- [ ] 普通 implementation request 直接进入 `$implement` 并由内部运行 branch gate；仅明确“只准备分支”时单独进入 `$checking-branch`。
- [ ] `checking-branch` 的 description、Trigger Description 与 metadata 只覆盖 `$implement` 等 workflow 的内部 gate，或用户明确的 branch-only 请求，不再与普通 implementation 初始入口竞争。
- [ ] `docs/features/**` 不做机械更新。

**验证命令 (Verification)**:

- `rg -ni -e "quick-change|diagnose-ue|workflow-router|Quick Change|Diagnose UE|Workflow Router" README.md AGENTS.md brainstorming/SKILL.md brainstorming/examples/brainstorming-session.md grill-me/SKILL.md session-curator/SKILL.md to-plan/SKILL.md to-spec/SKILL.md implement/SKILL.md diagnose/SKILL.md`，预期零输出且 `rg` exit code 1。
- `rg -n "Natural Handoff|继续|可以|按你说的办|go ahead|ok|好的|Quick Path|UE Profile" README.md AGENTS.md`，预期 direct routing 与自然确认 contract 均有命中。
- `rg -n "\$implement|\$diagnose|\$to-plan|\$to-spec|none" brainstorming/SKILL.md grill-me/SKILL.md to-plan/SKILL.md diagnose/SKILL.md`，人工核对每个完成状态最多一个 next Skill。
- `rg -n "普通 implementation request|内部.*branch gate|branch-only|\$implement" checking-branch/SKILL.md checking-branch/agents/openai.yaml`，预期 direct implementation exclusion、internal invocation 和 explicit branch-only markers 均有命中。
- 本 task 不以全量 validator 为独立通过条件；`GRILL_ME_REQUIRED_TEXT` 与 retired-file硬依赖必须在 Task 4 原子 cutover 后一起复检。

### Task 4: 原子删除旧入口并改写 validator

- **Files**:
  - Delete: `quick-change/SKILL.md`
  - Delete: `quick-change/agents/openai.yaml`
  - Delete: `diagnose-ue/SKILL.md`
  - Delete: `diagnose-ue/agents/openai.yaml`
  - Delete: `diagnose-ue/references/runtime-modes.md`
  - Delete: `diagnose-ue/references/probes-and-artifacts.md`
  - Delete: `diagnose-ue/references/regression-seams.md`
  - Delete: `workflow-router/SKILL.md`
  - Delete: `workflow-router/agents/openai.yaml`
  - Modify: `scripts/validate-skills.py`
  - Test: `README.md`, `AGENTS.md`, retained Skills 与迁移后的 references
- **Consumes**: `ImplementationPathContract v1`、`DiagnosticProfileContract v1` 与 `DirectRoutingContract v1`
- **Produces**: `ConsolidatedSkillSet v1`（本 spec 列出的 16 个公开 Skill）与 `ConsolidationValidatorContract v1`（Natural Handoff、merged markers、reference existence、retired directory/text 和 active-surface checks）
- **Covers**: `FR-001`, `FR-013`, `FR-014`, `FR-015`, `FR-016`, `FR-017`, `FR-018`

**验收标准 (Acceptance Criteria)**:

- [ ] 三个 retired Skill 顶层目录及其 metadata/references 全部消失，没有 alias、shim 或空目录。
- [ ] `GRILL_ME_REQUIRED_TEXT` 不再要求双 implementation entry，只要求唯一 `$implement` handoff。
- [ ] adaptive-planning validator markers 与 active paths 删除 `workflow-router` / `quick-change` 硬依赖，并继续保护 Fast/Full、checked plan、独立 spec/audit。
- [ ] 新增独立 consolidation contract validation，要求 `implement` 的 Quick/Standard/Blocked/upgrade markers、`quick-path.md`、`diagnose` 的双轴/claim-promotion/handoff markers、三个 `references/ue/*.md` 与既有 HITL script。
- [ ] `validate_workflow_contract()` 不再读取 router 文件，改为验证 README/AGENTS 中的 `Natural Handoff`、六个自然确认语、上一条唯一推荐绑定与“不绕过内部 gates”。
- [ ] retired-entry 检查验证三个顶层目录不存在，并扫描 README、AGENTS、所有 retained `SKILL.md`、metadata、references、examples、shell scripts 与 HTML assets；它明确排除 `docs/features/**` 与 validator 自身的 retired-name常量。
- [ ] Skill 总数继续动态统计，不永久硬编码 16；本次实际结果必须为 `Validated 16 skills.`。
- [ ] submodule validator 不读取父仓库 `CLAUDE.md`。

**验证命令 (Verification)**:

- `python scripts/validate-skills.py`，预期 exit code 0 并输出 `Validated 16 skills.`。
- `$expected = @('analyze','brainstorming','checking-branch','clarify','diagnose','finishing-branch','grill-me','handoff','implement','improve-codebase-architecture','requesting-code-review','session-curator','tdd','to-plan','to-spec','verification-before-completion') | Sort-Object; $actual = Get-ChildItem -Directory | Where-Object { Test-Path (Join-Path $_.FullName 'SKILL.md') } | Select-Object -ExpandProperty Name | Sort-Object; $delta = @(Compare-Object $expected $actual); if ($delta) { $delta; throw 'Skill inventory does not match the expected 16-skill topology.' }`，预期零 delta。
- `rg -ni -g "!docs/features/**" -g "!scripts/validate-skills.py" -e "quick-change|diagnose-ue|workflow-router|Quick Change|Diagnose UE|Workflow Router" .`，预期零输出且 `rg` exit code 1。
- `rg -n -g "!docs/features/**" "references/(runtime-modes|probes-and-artifacts|regression-seams)\.md" .`，预期零输出；所有 active UE links 必须使用 `references/ue/`。
- `npx --yes skills add . --list`，预期输出 `Found 16 skills` 且不包含 retired names。

### Task 5: 同步父仓库 living contract 并完成端到端验证

- **Files**:
  - Modify: `../../CLAUDE.md`
  - Test: `docs/features/workflow-skill-consolidation/spec.md`
  - Test: `docs/features/workflow-skill-consolidation/plan.md`
  - Test: all 16 retained Skill directories
  - Test: parent/submodule Git status and diffs
- **Consumes**: `ConsolidatedSkillSet v1` 与 `ConsolidationValidatorContract v1`
- **Produces**: `ConsolidationVerificationEvidence v1`（local validator、exact inventory、full-depth discovery、retired no-match、manual forward scenarios、stale-text、diff/status 与 residual-risk evidence）
- **Covers**: `FR-001`, `FR-002`, `FR-003`, `FR-004`, `FR-005`, `FR-006`, `FR-008`, `FR-009`, `FR-010`, `FR-011`, `FR-012`, `FR-013`, `FR-014`, `FR-015`, `FR-016`, `FR-017`, `FR-018`

**验收标准 (Acceptance Criteria)**:

- [ ] 父仓库 `CLAUDE.md` 删除 validator 对 router 的依赖描述，并将 quick/UE behavior 分别归入 `implement` / `diagnose`；第 22 行一类历史 report 文件示例保持不改。
- [ ] 父仓库 `AGENTS.md` 不因本 feature产生无关改动；其他 reference submodule 保持不变。
- [ ] 16 个 retained names 的本地 `npx ... use --full-depth` 全部 exit 0，三个 retired names 全部 exit 1 且报告 no match。
- [ ] fresh-session implementation scenarios 覆盖 `IMP-QUICK`、`IMP-STANDARD`、`IMP-UPGRADE`、`IMP-NO-REPRO`、`IMP-NEEDS-PLAN`、`IMP-NEEDS-DESIGN`、`IMP-EXTERNAL-FAKE-PASS`、`IMP-NATURAL-CONFIRM`。
- [ ] fresh-session diagnosis scenarios 覆盖 `DGN-GENERIC-ACTIVE`、`DGN-GENERIC-ARTIFACT`、`DGN-UE-ACTIVE`、`DGN-UE-ARTIFACT`、`DGN-UE-MODE-DRIFT`、`DGN-PERF-BASELINE`、`DGN-HANDOFF`。
- [ ] routing scenarios 证明 direct implementation / UE diagnosis 不经过 meta-skill；单一 Natural Handoff 的自然确认进入目标 Skill但保留内部 gates，多选或新增条件不会隐式进入。
- [ ] scenario evidence 区分 static contract pass 与实际 runtime/manual observation；未运行项必须作为 residual risk，不能包装成通过。
- [ ] submodule 与 parent `git diff --check` 通过；status 只包含本 plan 批准的 files，历史 artifacts 和其他 submodule 无变化。
- [ ] 最终报告明确 local source 已验证、public remote 尚未发布；除非用户另行授权，不执行 commit/push 或远端 discoverability claim。

**验证命令 (Verification)**:

- `python scripts/validate-skills.py`，预期 `Validated 16 skills.`。
- `npx --yes skills add . --list`，预期 `Found 16 skills`。
- 对下列集合逐项运行 `npx --yes skills use . --skill <name> --full-depth`，预期 exit 0：
  `analyze`, `brainstorming`, `checking-branch`, `clarify`, `diagnose`, `finishing-branch`, `grill-me`, `handoff`, `implement`, `improve-codebase-architecture`, `requesting-code-review`, `session-curator`, `tdd`, `to-plan`, `to-spec`, `verification-before-completion`。
- 对 `quick-change`, `diagnose-ue`, `workflow-router` 逐项运行同一 `use` 命令，预期 exit 1 与 `No matching skill found`。
- `rg -ni -g "!docs/features/**" -g "!scripts/validate-skills.py" -e "quick-change|diagnose-ue|workflow-router|Quick Change|Diagnose UE|Workflow Router" .`，预期零输出。
- `$claude = Get-Content -Raw ../../CLAUDE.md; $allowedRegex = [regex]::new('(?<![A-Za-z0-9._-])improvement-plan-diagnose-ue\.md(?![A-Za-z0-9._-])'); $allowedMatches = $allowedRegex.Matches($claude); if ($allowedMatches.Count -ne 1) { throw 'Historical filename exception drifted.' }; $parentLiving = $allowedRegex.Replace($claude, '', 1) + "`n" + (Get-Content -Raw ../../AGENTS.md); $unexpected = [regex]::Matches($parentLiving, '(?i)quick-change|diagnose-ue|workflow-router|Quick Change|Diagnose UE|Workflow Router'); if ($unexpected.Count) { $unexpected.Value; throw 'Retired living-contract reference found.' }`，预期只剔除一次带 filename 边界的 historical token；`old-improvement-plan-diagnose-ue.md`、`improvement-plan-diagnose-ue.md.bak` 等变体必须失败，随后 living contract 零命中。
- `git diff --check` 与 `git -C ../.. diff --check`，预期均无 whitespace error。
- `git status --short`、`git -C ../.. status --short`、`git -C ../.. submodule status --recursive`，人工核对两个 repo 与所有 submodule 边界。
- 按本 plan 的 manual forward scenarios 在 fresh sessions 中记录 `Input / Expected Path / Forbidden Action / Pass Signal / Observed Result`；未获得实际 agent run 的 scenario 标为未验证。

## Coverage 自查 (Coverage Self-Check)

| Requirement | Tasks | Verification seam |
| --- | --- | --- |
| FR-001 | Task 4, Task 5 | validator count、exact inventory、local `npx` list/use |
| FR-002 | Task 1, Task 5 | implement trigger/metadata markers、IMP-QUICK / IMP-STANDARD |
| FR-003 | Task 1, Task 5 | `ImplementationPathDecision v1` markers、write-before-dispatch scenario |
| FR-004 | Task 1, Task 5 | Quick contract、targeted signal、light review、verification scenario |
| FR-005 | Task 1, Task 5 | IMP-UPGRADE / IMP-NO-REPRO / planning-design blockers |
| FR-006 | Task 1, Task 5 | Standard graph markers、checked-plan/external-artifact scenarios |
| FR-007 | Task 1, Task 4 | `quick-path.md` existence/markers 与 full-depth output |
| FR-008 | Task 2, Task 5 | diagnose trigger/metadata 与 Generic/UE scenarios |
| FR-009 | Task 2, Task 4, Task 5 | Profile markers、reference existence、Generic no-UE scenario |
| FR-010 | Task 2, Task 5 | Evidence Mode markers、artifact no-confirmed scenarios |
| FR-011 | Task 2, Task 5 | runtime parity、cleanup markers、DGN-UE-MODE-DRIFT |
| FR-012 | Task 2, Task 3, Task 5 | unique `$implement`/`none` handoff 与 DGN-HANDOFF |
| FR-013 | Task 3, Task 4, Task 5 | router directory absence、Natural Handoff contract/scenarios |
| FR-014 | Task 3, Task 4, Task 5 | retained stale scan、direct implementation scenario |
| FR-015 | Task 3, Task 5 | README/AGENTS/parent CLAUDE diff 与 historical no-change check |
| FR-016 | Task 4, Task 5 | validator static checks 与 standalone boundary review |
| FR-017 | Task 4, Task 5 | local `npx` exact 16/full-depth/no-match evidence |
| FR-018 | Task 1–5 | gate markers、status/diff/submodule checks、no remote actions |

## Success Criteria Coverage

| Success Criterion | Tasks | Verification seam |
| --- | --- | --- |
| SC-001 | Task 4, Task 5 | `python scripts/validate-skills.py` |
| SC-002 | Task 4, Task 5 | local `npx skills add . --list` exact set |
| SC-003 | Task 5 | retained full-depth loop 与 retired no-match loop |
| SC-004 | Task 1, Task 5 | IMP-QUICK |
| SC-005 | Task 1, Task 5 | IMP-STANDARD |
| SC-006 | Task 1, Task 5 | IMP-UPGRADE |
| SC-007 | Task 1, Task 5 | IMP-NO-REPRO / IMP-NEEDS-PLAN / IMP-NEEDS-DESIGN |
| SC-008 | Task 2, Task 5 | Generic/UE Active/Artifact scenarios |
| SC-009 | Task 2, Task 5 | DGN-UE-MODE-DRIFT |
| SC-010 | Task 3, Task 5 | ROUTE-DIRECT / ROUTE-HANDOFF |
| SC-011 | Task 3, Task 4, Task 5 | active retired-token scans |
| SC-012 | Task 5 | parent/submodule diff/status/submodule checks |

## Planning Quality Gate

- **RequirementsCoverage**: Pass。`FR-001` 至 `FR-018` 均映射到至少一个 implementation task 与 verification seam。
- **TaskCompleteness**: Pass。五个 task 均包含精确 Files、Consumes、Produces、Covers、Acceptance Criteria 和 Verification。
- **ContractConsistency**: Pass。Task 1/2 分别产出 `ImplementationPathContract v1` / `DiagnosticProfileContract v1`，Task 3 逐字消费并产出 `DirectRoutingContract v1`，Task 4 消费三项 contract 并产出 `ConsolidatedSkillSet v1` / `ConsolidationValidatorContract v1`，Task 5 消费最终 contract 并产出验证 evidence。
- **RepositoryFeasibility**: Pass。所有 Modify/Delete/Test 路径当前存在；Create 路径位于现有 Skill 目录的 progressive-disclosure结构中；父仓库 living contract 的真实落点为 `../../CLAUDE.md`。
- **ConstraintAlignment**: Pass。breaking removal、历史 artifact 排除、standalone validator、no-alias、no-other-submodule、no-remote 与全部安全 gate 已写入 spec、task acceptance 和 final verification。
- **AutoFixSummary**: 将 Task 2 的 PowerShell-native wildcard 路径改为目录参数；将 inventory 验证改为 exact-set assertion；修正 parent stale scan；在 review 发现入口竞争后把 `checking-branch` 的 owner trigger/metadata 明确纳入 Task 3。四项修复均未改变设计或任务边界。
- **ResidualRisks**:
  - 当前没有跨 turn automatic eval harness；manual forward scenarios 未实际运行前只能标为 residual risk。
  - 本地 source 验证不能证明 `fjxyyzg3/Skills` public remote 已发布；remote verification 需要后续 commit/push 授权。
  - 删除旧显式入口是用户已接受的 breaking change，但外部使用者仍需自行迁移命令。
- **Planning Quality Status**: Pass
