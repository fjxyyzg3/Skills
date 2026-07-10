# Adaptive Planning Workflow Plan

## 元数据 (Metadata)

- **Source**: `docs/features/adaptive-planning-workflow/spec.md`
- **Generated at**: 2026-07-10
- **Status**: Complete
- **Planning Mode**: Full
- **Risk rationale**: 本 feature 修改核心 workflow contract，横跨 planning、routing、implementation intake、metadata、validator 和父仓库说明，因此必须保留独立 spec 与完整 requirement traceability。

## 假设 (Assumptions)

- 当前仓库共有 19 个 skills，`python scripts/validate-skills.py` 是权威结构与 workflow-contract validator。
- 对 active files 的搜索表明，没有脚本、validator 或 runtime code 扫描 `manifest.md`；只有 `to-spec`、`to-plan` 和 `analyze` 的 skill 文档引用它。因此 Fast Path 可以不创建新 manifest，同时继续更新已经存在的 manifest。
- `Natural Handoff` 的唯一推荐和自然确认语义保持不变；Planning Authorization 是 `$to-plan` 内部的一次本地 artifact 授权，不是跨 skill 自动执行许可。
- 当前环境没有自动执行跨 turn agent 对话的 eval harness；Fast/Full、自动修复、决策暂停和授权越界场景需要由 scenario contract 加 validator marker，并在最终验证时人工试跑代表场景。
- 历史目录 `docs/features/spec-plan-workflow/` 和 `docs/features/natural-handoff-workflow/` 只作为 prior art 保留，不修改其内容。

## 全局约束 (Global Constraints)

- 所有用户可见文档和 skill 正文使用中文主文；命令、路径、contract fields、稳定 ID 和必要技术术语保留 English。
- `to-plan` 是 planning outcome owner；主 `SKILL.md` 保持执行导向，风险矩阵、artifact schemas、finding taxonomy 和 scenario 细节通过 progressive disclosure 放入 references/examples。
- Planning Authorization 只允许读取相关上下文、写本地 planning artifacts、修复 Artifact-fixable findings 和重新检查；不得授权业务代码/测试修改、branch、commit、push、PR、merge、discard 或远端操作。
- Fast Path 不能降低 `FR-###`、task、`Consumes/Produces`、`Covers`、acceptance criteria、verification commands 和 coverage 的完整性。
- Full Path 的 `spec.md` 与 `plan.md` 必须共享完全相同的 `FR-###`；Fast/Full 均不得默认创建 `analysis.md`。
- 独立 `$to-spec` 与独立只读 `$analyze` 必须继续可用；`$quick-change` 和 `implement` 的 branch、review、verification 与交付安全门不得弱化。
- 所有修改按下面 task 编号串行完成；不要修改其他 submodule 或历史 feature artifacts。

## Task 列表 (Tasks)

### Task 1: 建立 adaptive `$to-plan` 核心 contract 与 scenario seam

- **Files**:
  - Create: `to-plan/references/adaptive-planning-contract.md`
  - Create: `to-plan/examples/adaptive-planning-scenarios.md`
  - Modify: `to-plan/SKILL.md`
  - Modify: `to-plan/agents/openai.yaml`
  - Test: `scripts/validate-skills.py`
- **Consumes**: `Adaptive Planning Spec v1`（`docs/features/adaptive-planning-workflow/spec.md` 中的 Planning Authorization、Risk Routing、Artifact Contract 和 Planning Quality Gate）
- **Produces**: `AdaptivePlanningContract v1`（包含 `PlanningAuthorization`、`RiskDecision`、`PlanningArtifactSet`、`FindingClass`、`PlanningQualityResult`、`CheckedPlanHandoff` 的 Markdown field schemas）和 `AdaptivePlanningScenarioSuite v1`（Fast、Full、Artifact-fixable、Decision-required、direct-to-spec、direct-analyze、authorization-boundary 七类 scenario contracts）
- **Covers**: `FR-003`, `FR-004`, `FR-005`, `FR-006`, `FR-007`, `FR-008`, `FR-009`, `FR-010`, `FR-011`, `FR-012`, `FR-013`, `FR-014`, `FR-015`, `FR-018`, `FR-020`

**验收标准 (Acceptance Criteria)**:

- [ ] `adaptive-planning-contract.md` 定义 Planning Authorization 的允许/禁止动作，以及 `Planning Mode: Fast | Full` 的确定性风险规则。
- [ ] contract 明确 Fast Path 只写自包含 `plan.md`；Full Path 在同一 Planning Run 内写共享 `FR-###` 的 `spec.md + plan.md`；两者都不默认写 `analysis.md`。
- [ ] contract 定义 `Planning Quality Status: Pass | Decision required`，并把 findings 严格分成 `Artifact-fixable` 与 `Decision-required`。
- [ ] `to-plan/SKILL.md` 从 source intake 开始自动分类并报告依据，只在分类证据冲突或 Decision-required finding 时一次问一个问题。
- [ ] `to-plan/SKILL.md` 对 Artifact-fixable finding 自动修复并重新检查；完成后只报告一次 artifacts、coverage、auto-fix summary、assumptions 和 residual risks。
- [ ] 用户提供现有 spec 时进入 Full Path 并复用现有 `FR-###`；只有 conversation context 时按风险规则决定是否补写 spec。
- [ ] checked plan 完成后最多推荐 `$implement`，并明确该 handoff 不绕过其 branch、scope、review 或 verification gate。
- [ ] `adaptive-planning-scenarios.md` 为七类 scenario 分别记录 input shape、expected mode、expected artifacts、allowed interruption、forbidden actions 和 pass signal。
- [ ] `agents/openai.yaml` 的 `short_description` 与 `default_prompt` 描述 adaptive checked-plan outcome，并继续满足长度、单行引号和 `$to-plan` 引用约束。

**验证命令 (Verification)**:

- `python scripts/validate-skills.py`，预期输出 `Validated 19 skills.`。
- `rg -n 'Planning Authorization|Fast Path|Full Path|Artifact-fixable|Decision-required|Planning Quality Status|\$implement' to-plan/SKILL.md to-plan/references/adaptive-planning-contract.md`，预期所有核心 contract markers 均有命中。
- `rg -n "AP-FAST|AP-FULL|AP-AUTOFIX|AP-DECISION|AP-DIRECT-SPEC|AP-DIRECT-ANALYZE|AP-AUTH-BOUNDARY" to-plan/examples/adaptive-planning-scenarios.md`，预期七个 scenario ID 各命中一次。
- `rg -n "manifest\.md|feature manifest|manifest" -g "!docs/features/**" .`，预期仍只命中 planning skill 文档，不出现新的脚本/runtime dependency。

### Task 2: 重连 `brainstorming` 入口并保留独立 spec/audit 路径

- **Files**:
  - Modify: `brainstorming/SKILL.md`
  - Modify: `brainstorming/agents/openai.yaml`
  - Modify: `brainstorming/examples/brainstorming-session.md`
  - Modify: `to-spec/SKILL.md`
  - Modify: `to-spec/agents/openai.yaml`
  - Modify: `analyze/SKILL.md`
  - Modify: `analyze/agents/openai.yaml`
  - Test: `scripts/validate-skills.py`
- **Consumes**: `AdaptivePlanningContract v1` 和 `AdaptivePlanningScenarioSuite v1`
- **Produces**: `PlanningEntryRoutingContract v1`（包含 `PlanningHandoffPacket v1` 的 confirmed goal、scope、non-goals、chosen approach、rejected alternatives、key decisions、risks、open questions、verification seam fields，以及 plan/spec/audit 三类独立入口条件）
- **Covers**: `FR-001`, `FR-002`, `FR-016`, `FR-017`, `FR-019`

**验收标准 (Acceptance Criteria)**:

- [ ] `brainstorming` 在设计确认且目标是 implementation-ready plan 时输出完整 `PlanningHandoffPacket v1`，唯一推荐 `$to-plan`，不再默认经 `$to-spec` 中转。
- [ ] 用户只需要正式 spec/decision artifact 时，`brainstorming` 仍可唯一推荐 `$to-spec`；只需要方案结果时以 `none` 结束。
- [ ] brainstorming handoff 只完成 skill 转场；用户自然确认后由 `$to-plan` 的 Planning Authorization 批准 planning artifact 写入，不授权实现或 Git 操作。
- [ ] `brainstorming-session.md` 同步展示 implementation-plan、spec-only 和 stop-here 三种结束形态，且每种只出现一个 next skill 或 `none`。
- [ ] `$to-spec` 的 description、进入边界和 metadata 明确其是独立 formal-spec 入口；其 spec-only 行为和完成后可选 `$to-plan` handoff 保持可用。
- [ ] `$analyze` 的 description、进入边界和 metadata 明确其用于用户显式要求或已有/外部 artifacts 的独立只读审计，不再被描述为 checked plan 的默认下一阶段。
- [ ] 三个 skills 的 `Language Contract`、pressure scenarios、Natural Handoff 和只读/不实现边界保持有效。

**验证命令 (Verification)**:

- `python scripts/validate-skills.py`，预期输出 `Validated 19 skills.`。
- `rg -n 'PlanningHandoffPacket|\$to-plan|\$to-spec|none' brainstorming/SKILL.md brainstorming/examples/brainstorming-session.md`，预期三种结束形态和唯一推荐规则均可定位。
- `rg -n "独立|formal spec|只读|已有.*artifacts" to-spec/SKILL.md analyze/SKILL.md to-spec/agents/openai.yaml analyze/agents/openai.yaml`，预期 spec-only 与 standalone audit 边界均有明确 marker。
- `rg -n 'prepare a spec handoff for \$to-spec|默认.*\$to-spec|不得自动进入 \$to-plan' brainstorming/SKILL.md brainstorming/agents/openai.yaml`，预期零命中。

### Task 3: 让 implementation intake 消费 checked plan，并收束 quick-change 升级路由

- **Files**:
  - Modify: `implement/SKILL.md`
  - Modify: `quick-change/SKILL.md`
  - Test: `scripts/validate-skills.py`
- **Consumes**: `AdaptivePlanningContract v1` 和 `PlanningEntryRoutingContract v1`
- **Produces**: `AdaptiveImplementationIntakeContract v1`（`Planning Quality Status: Pass` 直接满足 artifact quality gate；缺少该状态、状态失败或属于外部未检查 artifacts 时进入独立 `$analyze`；所有 branch/review/verification gates 保持不变）
- **Covers**: `FR-015`, `FR-017`, `FR-020`

**验收标准 (Acceptance Criteria)**:

- [ ] `implement` 的 trigger graph 和 Input Intake 能读取 `CheckedPlanHandoff` 的 Planning Mode、artifact paths、coverage、quality status 和 residual risks。
- [ ] `Planning Quality Status: Pass` 的 checked plan 不再触发重复独立 analysis；缺少 quality status、包含未处理 finding 或来自外部的 artifacts 仍进入只读 `$analyze` gate。
- [ ] 现有 `CRITICAL` finding 停止条件、branch gate、串行 TDD、review subagent、verification 和 finishing decision 均保持不变。
- [ ] `quick-change` 保留原有适用条件；需求不清时推荐 `$grill-me`/`$brainstorming`，已明确但升级为多 task 或中高风险时推荐 `$to-plan`，已有未检查 artifacts 时才推荐 `$analyze`。
- [ ] `quick-change` 不再描述固定 `$to-spec -> $to-plan -> $analyze -> $implement` 链路，也不因本 feature 扩大其写入授权。

**验证命令 (Verification)**:

- `python scripts/validate-skills.py`，预期输出 `Validated 19 skills.`。
- `rg -n "Planning Quality Status|checked plan|external|CRITICAL|Branch Gate|Review Subagent Gate|Verification Gate" implement/SKILL.md`，预期 checked/unverified 两种 artifact 路径和所有既有安全门均有命中。
- `rg -n '\$brainstorming|\$to-plan|\$analyze|\$implement' quick-change/SKILL.md`，预期升级目标按输入状态区分。
- `rg -n '\$to-spec -> \$to-plan -> \$analyze -> \$implement' quick-change/SKILL.md implement/SKILL.md`，预期零命中。

### Task 4: 同步 repository contract、validator 与最终 scenario 验证

- **Files**:
  - Modify: `workflow-router/SKILL.md`
  - Modify: `README.md`
  - Modify: `AGENTS.md`
  - Modify: `scripts/validate-skills.py`
  - Modify: `../../CLAUDE.md`
  - Modify: `docs/features/adaptive-planning-workflow/manifest.md`
  - Test: `to-plan/examples/adaptive-planning-scenarios.md`
  - Test: `scripts/validate-skills.py`
- **Consumes**: `AdaptivePlanningContract v1`、`AdaptivePlanningScenarioSuite v1`、`PlanningEntryRoutingContract v1` 和 `AdaptiveImplementationIntakeContract v1`
- **Produces**: `AdaptivePlanningRepositoryContract v1`（router、repo docs、parent workspace docs、validator markers 和 scenario evidence 对同一 adaptive planning 语义达成一致）
- **Covers**: `FR-019`, `FR-020`

**验收标准 (Acceptance Criteria)**:

- [ ] `workflow-router` 把“从已确认设计/spec 产出 implementation plan”路由到 `$to-plan`，把“只要正式 spec”路由到 `$to-spec`，把“审查已有/外部 artifacts”路由到 `$analyze`。
- [ ] `workflow-router` 保持单一 next skill 和不写文件的职责；Planning Authorization 由 `$to-plan` 内部处理，不变成 router 的跨-skill例外。
- [ ] README Mermaid、skill 表格和开发原则显示 adaptive `brainstorming -> to-plan -> checked plan` 主路径、Full Path 的按需 spec，以及独立 `$to-spec`/`$analyze`。
- [ ] submodule `AGENTS.md` 与父仓库 `../../CLAUDE.md` 不再宣称复杂任务固定经过独立 `$to-spec -> $to-plan -> $analyze`，并保留所有 implementation safety gates。
- [ ] `scripts/validate-skills.py` 新增 focused adaptive-planning contract validation：要求 `to-plan`、`brainstorming`、`implement`、README 和 AGENTS 的关键 markers，拒绝活跃文档中的旧固定链路与旧 brainstorming 默认 handoff。
- [ ] `GRILL_ME_REQUIRED_TEXT` 和无关 skill contracts 不被本 feature 意外改写；历史 feature artifacts 不进入 stale-text 扫描。
- [ ] 按 `AdaptivePlanningScenarioSuite v1` 人工试跑代表性的 Fast、Full、Artifact-fixable、Decision-required、direct-to-spec、direct-analyze 和 authorization-boundary 场景，记录每个场景的 mode、artifacts、interruptions、final reports 和 forbidden-action 结果。
- [ ] 所有验证通过后，manifest 将 Plan 标记为完成，并仅在 implementation 确实完成时更新 Implementation 状态；不得提前标记。

**验证命令 (Verification)**:

- `python scripts/validate-skills.py`，预期输出 `Validated 19 skills.`。
- `rg -n "Planning Authorization|Fast Path|Full Path|Artifact-fixable|Decision-required|Planning Quality Status" to-plan/SKILL.md brainstorming/SKILL.md implement/SKILL.md README.md AGENTS.md`，预期 repository contract markers 完整。
- `rg -n '\$to-spec -> \$to-plan -> \$analyze|Spec\["to-spec"\].*Plan|Plan\["to-plan"\].*Analyze' README.md AGENTS.md workflow-router/SKILL.md quick-change/SKILL.md ../../CLAUDE.md`，预期零命中。
- `git diff --check` 和 `git -c safe.directory=C:/WorkSpace/skill-development -C ../.. diff --check`，预期 submodule 与父仓库都无 whitespace error。
- `git status --short`，预期 submodule 只包含本 feature 批准范围内的 skill、metadata、docs 和 validator 改动；`git -c safe.directory=C:/WorkSpace/skill-development -C ../.. status --short` 预期父仓库只包含 `CLAUDE.md` 与 submodule 状态，任何其他文件必须单独说明。
- 按 `to-plan/examples/adaptive-planning-scenarios.md` 的 pass signals 完成人工 scenario run，预期 `AP-FAST` 只产出 plan、`AP-FULL` 产出 spec+plan、`AP-AUTOFIX` 不打断、`AP-DECISION` 只问一个问题、显式入口保持独立、越界动作全部拒绝。

## Coverage 自查 (Coverage Self-Check)

| Requirement | Tasks | Notes |
| --- | --- | --- |
| FR-001 | Task 2 | brainstorming implementation-plan handoff 改为 `$to-plan` |
| FR-002 | Task 2 | 定义并输出完整 `PlanningHandoffPacket v1` |
| FR-003 | Task 1 | Planning Authorization 和连续 Planning Run |
| FR-004 | Task 1, Task 3 | planning 授权白名单与 implementation 安全门 |
| FR-005 | Task 1 | 自动 Fast/Full 分类与依据报告 |
| FR-006 | Task 1 | 只在分类冲突时问一个问题 |
| FR-007 | Task 1 | Fast Path 单 plan artifact |
| FR-008 | Task 1 | Fast plan 的 requirements/tasks/contracts/coverage/quality 字段 |
| FR-009 | Task 1 | Full Path 同一运行内生成共享 FR 的 spec+plan |
| FR-010 | Task 1 | 无默认 analysis，manifest 只更新既有文件 |
| FR-011 | Task 1 | 内建 requirements、task、contract、path、verification 检查 |
| FR-012 | Task 1 | Artifact-fixable 自动修复与复检 |
| FR-013 | Task 1 | Decision-required 单问题暂停与恢复 |
| FR-014 | Task 1 | 单次最终报告 contract |
| FR-015 | Task 1, Task 3 | checked plan handoff 与 implement intake |
| FR-016 | Task 2 | 独立 `$to-spec` 保留 |
| FR-017 | Task 2, Task 3 | 独立只读 `$analyze` 与未检查 artifact gate |
| FR-018 | Task 1 | existing spec 复用 FR；conversation context 自动分流 |
| FR-019 | Task 2, Task 4 | skill metadata、router、repo docs、validator 同步 |
| FR-020 | Task 1, Task 3, Task 4 | quick-change、implementation 和 Git/remote gates 不弱化 |

## Success Criteria Coverage

| Success Criterion | Tasks | Verification seam |
| --- | --- | --- |
| SC-001 | Task 1, Task 2, Task 4 | `AP-FAST` 记录一次授权、零中间 handoff |
| SC-002 | Task 1, Task 4 | `AP-FAST` artifact 和 coverage assertions |
| SC-003 | Task 1, Task 4 | `AP-FULL` spec/plan FR equality 与 artifact assertions |
| SC-004 | Task 1, Task 4 | `AP-AUTOFIX` 无用户确认的修复复检 |
| SC-005 | Task 1, Task 4 | `AP-DECISION` 单问题暂停与恢复 |
| SC-006 | Task 1, Task 4 | scenario 首次状态与最终报告计数 |
| SC-007 | Task 2, Task 4 | `AP-DIRECT-SPEC`、`AP-DIRECT-ANALYZE` |
| SC-008 | Task 1, Task 3, Task 4 | `AP-AUTH-BOUNDARY` forbidden-action assertions |
| SC-009 | Task 4 | `python scripts/validate-skills.py` |
| SC-010 | Task 2, Task 3, Task 4 | repository marker 和 stale-chain 检查 |
| SC-011 | Post-launch | 不阻塞实现完成；后续真实会话统计确认次数 |

## Planning Quality Gate

- **Requirements coverage**: Pass，`FR-001` 至 `FR-020` 全部至少映射到一个 task；`SC-001` 至 `SC-010` 均有实现 task 和 verification seam。
- **Contract consistency**: Pass，`AdaptivePlanningContract v1` / `AdaptivePlanningScenarioSuite v1` 由 Task 1 产出并被 Task 2–4 逐字消费；`PlanningEntryRoutingContract v1` 由 Task 2 产出并被 Task 3–4 消费；`AdaptiveImplementationIntakeContract v1` 由 Task 3 产出并被 Task 4 消费。
- **File feasibility**: Pass，所有 Modify/Test 路径当前存在；两个 Create 路径位于现有 `to-plan/` skill 内，符合仓库已有 references/examples 组织模式；父仓库 canonical chain 的真实落点为 `../../CLAUDE.md`。
- **Verification feasibility**: Pass，`python`、`rg`、`git` 和当前 validator 均已在本 workspace 验证可用；跨 turn 行为明确使用 scenario manual fallback。
- **Decision-required findings**: None。manifest 搜索已经排除 runtime/script 依赖；剩余跨 turn 行为风险已转成 Task 4 scenario gate，而不是未决产品选择。
- **Planning Quality Status**: Pass
