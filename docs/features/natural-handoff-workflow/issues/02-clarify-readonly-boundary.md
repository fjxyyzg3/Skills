# ISSUE-002: 收束 clarify 为只读解释型 skill

## 元数据 (Metadata)

- **Type**: `AFK`
- **Covers**: `FR-005`
- **Parallelization**: `coordination-needed`
- **Wave**: 2
- **Depends on**: `ISSUE-001 (hard: 需要先确定 Natural Handoff 共享语义)`
- **Unblocks**: `ISSUE-004`

## 构建内容 (What to build)

更新 `clarify` 的职责边界，使它明确只用于回答问题、解释源码、调用链、架构或本地证据。`clarify` 完成后自然结束，不推荐后续 skill，也不把解释任务推向 planning、diagnosis 或 implementation。

## 验收标准 (Acceptance Criteria)

- [ ] `clarify` 文档明确“只回答问题，不推荐后续 skill”。
- [ ] `clarify` 不要求输出 `Next Skill Gate` 或等价字段清单。
- [ ] `clarify` 的完成标准允许自然结束，例如说明本次解释已经完成。
- [ ] 如果 `workflow-router` 推荐 `$clarify`，也明确它是只读解释路径，不承担后续 handoff 推荐。
- [ ] 不改变 `clarify` 读取源码、生成图表或解释报告的能力。

## 测试说明 (Testing Notes)

- Verification seam: `rg -n "Recommended next skill|Next Skill Gate|推荐.*skill|不推荐后续|只回答问题" clarify workflow-router`
- Prior art: PRD 中将 `clarify` 定义为 `Natural Handoff` 的例外路径。
- Manual fallback: 人工审查一次 `clarify` 输出样例，确认它不会引导用户进入 `$to-prd`、`$diagnose` 或 `$implement`。

## 并行执行说明 (Parallel Execution Notes)

- 可以与 ISSUE-003 并行，但两者都需要沿用 ISSUE-001 的自然交接词汇。
- 如需修改 `README.md` 的 skill table，需要避免和 ISSUE-003 的同一段落冲突。

## 实现说明 (Implementation Notes)

- 保持 `clarify` 的只读源码探索和解释能力。
- 不要把 `clarify` 改成 workflow-router 的替代品。
- 如果 validator 需要特判 `clarify`，把规则留给 ISSUE-004。
