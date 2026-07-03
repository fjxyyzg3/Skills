# ISSUE-004: 改造 `analyze` 为 spec↔plan coverage 检查

## 元数据 (Metadata)

- **Type**: `AFK`
- **Covers**: `FR-012`
- **Parallelization**: `parallel-safe`
- **Wave**: 2
- **Depends on**: `ISSUE-002 (hard: 依赖 plan 模板定稿的 task 字段名)`
- **Unblocks**: `ISSUE-005`

## 构建内容 (What to build)

改造 `analyze/SKILL.md`：检查对象从 PRD + issues 目录改为 spec + plan；coverage 检查为 `FR-###` 与 plan task `Covers` 的双向追溯（每条 FR 有 task 覆盖、每个 task 能追回 FR 或 conversation requirement）；删除依赖环、wave 顺序、并行建议相关检查项；description 同步更新。

## 验收标准 (Acceptance Criteria)

- [ ] description 不再提 issue files、dependency graphs、execution waves、dependency cycles、parallelization risk；改为 spec、plan、task coverage、一致性、质量门。
- [ ] artifact 查找线索从 `docs/prd/`、`docs/issues/` 改为 `docs/features/<slug>/spec.md` 与 `plan.md`。
- [ ] 提取维度改为：spec 的 goals/FR/SC/测试决策；plan 的 task 编号、Files、Consumes/Produces、Covers、验收标准、验证命令。
- [ ] 检查项包含：FR↔task 双向 coverage、task 间 Consumes/Produces 接口一致性（前 task 的 Produces 与后 task 的 Consumes 名称/类型对得上）、验证命令存在性；删除 cycle/wave/并行风险检查。
- [ ] severity 分级与报告模板同步收缩，不引用已删除的检查维度（对应 PRD Risk 第三条）。
- [ ] 保持只读边界不变。
- [ ] 全文 grep 无 `issue`、`wave`、`并行`、`依赖图` 残留检查语义。

## 测试说明 (Testing Notes)

- Verification seam: `python scripts/validate-skills.py`；用本 feature 自己的 spec/plan（若 ISSUE-001/002 试跑产物可用）人工跑一次 analyze 核对报告结构。
- Prior art: 现行 `analyze/SKILL.md` 的报告分级框架；ISSUE-002 定稿的 task 字段名。
- Manual fallback: 人工 review 报告模板与检查项清单的一一对应。

## 并行执行说明 (Parallel Execution Notes)

- 与 ISSUE-003 文件不相交，理论可并行；建议 inline 串行。

## 实现说明 (Implementation Notes)

- Consumes/Produces 一致性检查是新增价值点：它接替了原依赖图检查在"发现拆分断裂"上的职责，对应 superpowers writing-plans Self-Review 的 Type consistency 思路。
- 在 ISSUE-005 完成前不引用 `$to-prd`/`$to-issues`，Natural Handoff 目标写 `$implement` / `$checking-branch` 现行规则不变。
