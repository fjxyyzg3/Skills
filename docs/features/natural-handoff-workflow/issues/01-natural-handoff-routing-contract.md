# ISSUE-001: 定义 Natural Handoff 路由契约

## 元数据 (Metadata)

- **Type**: `AFK`
- **Covers**: `FR-001, FR-002, FR-003, FR-004, FR-009, FR-010`
- **Parallelization**: `sequential`
- **Wave**: 1
- **Depends on**: `None`
- **Unblocks**: `ISSUE-002, ISSUE-003, ISSUE-004`

## 构建内容 (What to build)

把仓库级 workflow contract 和 `workflow-router` 从用户可见的 `Next Skill Gate` 字段清单，改为自然语言 `Natural Handoff`。该 slice 要定义自然确认语、唯一推荐 next skill 的绑定规则，以及自然确认不能绕过目标 skill 内部安全门的原则。

## 验收标准 (Acceptance Criteria)

- [ ] `workflow-router` 明确使用 `Natural Handoff`，不再要求向用户输出 `Next Skill Gate` 字段清单。
- [ ] 自然确认语包含 `继续`、`可以`、`按你说的办`、`go ahead`、`ok` 和 `好的`。
- [ ] 文档明确自然确认只绑定上一条回复中唯一推荐的 next skill。
- [ ] 文档明确如果上一条给出多个选项，或用户确认时改变条件，必须重新路由。
- [ ] 文档明确自然确认不批准代码修改、分支操作、提交、推送或实现类 skill 的内部安全门。
- [ ] `README.md`、`AGENTS.md` 和 `workflow-router` 的语义一致。

## 测试说明 (Testing Notes)

- Verification seam: `rg -n "Next Skill Gate|继续.*不算确认|go ahead.*不算确认|Natural Handoff" README.md AGENTS.md workflow-router/SKILL.md`
- Prior art: 当前 `workflow-router/SKILL.md` 已有 controlled chain 概念，但仍写着 `继续` 不算确认。
- Manual fallback: 人工审查 `workflow-router` 收尾样例是否像自然对话，而不是字段清单。

## 并行执行说明 (Parallel Execution Notes)

- 本 issue 是后续 skill 边界修改的 contract 前置，不建议与 ISSUE-002 或 ISSUE-003 并行落地。
- 如果另一个 agent 同时修改 `README.md` 或 `AGENTS.md`，必须先对齐 `Natural Handoff` 词汇和自然确认词表。

## 实现说明 (Implementation Notes)

- 优先修改仓库级 contract，再修改 `workflow-router`。
- 可以保留 `recommend-only` 作为内部安全语义，但不要把它作为用户可见字段清单输出。
- 如果保留内部自检结构，应明确它不是聊天输出格式。
