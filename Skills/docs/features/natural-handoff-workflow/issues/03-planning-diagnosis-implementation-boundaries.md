# ISSUE-003: 对齐需求澄清、诊断和实现入口边界

## 元数据 (Metadata)

- **Type**: `AFK`
- **Covers**: `FR-006, FR-007, FR-008`
- **Parallelization**: `coordination-needed`
- **Wave**: 2
- **Depends on**: `ISSUE-001 (hard: 需要先确定 Natural Handoff 共享语义)`
- **Unblocks**: `ISSUE-004`

## 构建内容 (What to build)

更新需求澄清、诊断和实现入口相关 skill 的边界说明：`grill-me` 和 `brainstorming` 用于明确需求和实现边界，不写业务代码；`diagnose` 和 `diagnose-ue` 用于定位 bug 和提出修复建议，不直接提交持久实现；feature 和 bug fix 根据风险选择 `$quick-change` 或完整 `$to-prd -> $to-issues -> $analyze -> $implement` 链路。

## 验收标准 (Acceptance Criteria)

- [ ] `grill-me` 和 `brainstorming` 明确不写业务代码、不自动进入实现。
- [ ] `diagnose` 和 `diagnose-ue` 明确不直接提交持久实现代码。
- [ ] `diagnose` 和 `diagnose-ue` 明确可以推荐 `$quick-change` 或 `$implement` 作为修复入口。
- [ ] `quick-change` 的适用范围包含小、清楚、低风险且可快速验证的 feature 或 bug fix。
- [ ] 完整链路适用条件包含跨模块、需求不清、影响 contract、多 slice 或验收复杂。
- [ ] `README.md`、`AGENTS.md` 和相关 `SKILL.md` 对这些边界的描述一致。

## 测试说明 (Testing Notes)

- Verification seam: `rg -n "不写业务代码|持久实现|quick-change|to-prd -> \\$to-issues|完整链路|低风险" grill-me brainstorming diagnose diagnose-ue quick-change README.md AGENTS.md`
- Prior art: PRD 已定义 planning、diagnosis 和 implementation entry 的职责分流。
- Manual fallback: 人工审查 bug 场景和 feature 场景各一个，确认推荐路径符合风险分流。

## 并行执行说明 (Parallel Execution Notes)

- 可以与 ISSUE-002 并行，但两个 issues 都可能修改仓库总览文档，需要最后统一措辞。
- 不建议把 validator 修改混入本 issue；文案稳定后由 ISSUE-004 固化检查。

## 实现说明 (Implementation Notes)

- 注意区分“诊断阶段可运行测试或临时 instrumentation”和“诊断阶段不提交持久业务代码”。
- 不要把完整链路写成所有 feature 和 bug 的默认强制路径；小型低风险变更仍可走 `$quick-change`。
- 如果当前 `agents/openai.yaml` 中有 explicit-only 相关 metadata，是否调整应和仓库级触发语义一起处理。
