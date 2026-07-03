# ISSUE-002: 新建 `to-plan` skill

## 元数据 (Metadata)

- **Type**: `HITL`
- **Covers**: `FR-003, FR-004, FR-005, FR-015, FR-016`
- **Parallelization**: `coordination-needed`
- **Wave**: 1
- **Depends on**: `ISSUE-001 (soft: spec 模板字段与 handoff 措辞需一致，可提前起草)`
- **Unblocks**: `ISSUE-003, ISSUE-004, ISSUE-005`

## 构建内容 (What to build)

创建 `to-plan/SKILL.md` 和 `to-plan/agents/openai.yaml`，将 spec（或 conversation context）拆成任务级 plan，默认写入 `docs/features/<feature-slug>/plan.md`（单 Markdown 文件，非目录），完成后更新 manifest 的 Plan 状态。

每个 task 包含：精确文件路径（Create/Modify/Test）、`Consumes/Produces` 接口契约、`Covers`（`FR-###` 或 conversation requirement）、验收标准、验证命令；task 按执行顺序编号，串行语义。plan 末尾有 coverage 自查表。

## 验收标准 (Acceptance Criteria)

- [ ] `to-plan/SKILL.md` frontmatter `name: to-plan`，description 覆盖 plan/任务拆分触发场景，措辞不与旧 `to-issues` description 雷同（不出现 tracer-bullet、dependency graph、execution waves、parallelization 词汇）。
- [ ] SKILL.md 含语言契约 marker 句和例外句。
- [ ] task 模板包含：Files（Create/Modify/Test 精确路径）、Consumes/Produces、Covers、验收标准、验证命令。
- [ ] SKILL.md 验证清单包含负向约束：plan 中无实现代码、无依赖图、无 `Wave`/`Parallelization`/`AFK`/`HITL` 字段、无 subagent 并行指引。
- [ ] plan 末尾 coverage 自查表覆盖所有 `FR-###`，未覆盖项注明原因。
- [ ] `agents/openai.yaml` 含 `display_name`、`short_description`（25–64 字符）、`default_prompt`（单行引号、引用 `$to-plan`）。
- [ ] Natural Handoff：完成后最多推荐 `$analyze` 作为唯一 next skill。
- [ ] description 与模板措辞经用户过目确认（human-gate）。

## 测试说明 (Testing Notes)

- Verification seam: `python scripts/validate-skills.py`；SC-004 试跑——本 issue 完成后用一个真实需求跑 `to-spec -> to-plan`，核对产物字段齐全且无代码/并行字段。
- Prior art: obra-superpowers `writing-plans` 的 Files/Interfaces/Task 结构与 Self-Review 思路（去掉每步代码要求）；旧 `to-issues` 的 Covers/coverage 表机制。
- Manual fallback: 人工 review plan 模板与一次真实产物。

## 并行执行说明 (Parallel Execution Notes)

- 与 ISSUE-001 共享 `FR-###`/`Covers` 契约与 handoff 措辞；建议在 001 定稿后串行执行。
- 本 issue 定稿的 task 字段名是 ISSUE-003/004 的硬前置。

## 实现说明 (Implementation Notes)

- "plan 决定分解、implement 决定代码"是硬分界：模板中不得出现要求预写测试/实现代码的步骤；代码级内容一律留给 `implement` 的 TDD 循环。
- 在 ISSUE-005 完成前不引用 `$to-prd`/`$to-issues`。
- plan 单文件、task 顺序编号即执行顺序；如 spec 覆盖多个独立子系统，建议拆成多个 feature workspace 而不是在 plan 内引入依赖图。
