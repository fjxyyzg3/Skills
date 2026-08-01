# ISSUE-005: 原子替换切片：删除旧 skill + 全量引用 + validator

## 元数据 (Metadata)

- **Type**: `AFK`
- **Covers**: `FR-006, FR-007, FR-008, FR-009, FR-010, FR-013, FR-014`
- **Parallelization**: `sequential`
- **Wave**: 3
- **Depends on**: `ISSUE-001, ISSUE-002, ISSUE-003, ISSUE-004 (hard: 新增 stale-text 检查扫描所有 SKILL.md，任一前置未完成则 validator 必红)`
- **Unblocks**: `ISSUE-006`

## 构建内容 (What to build)

单次原子提交完成旧工作流下线：删除 `to-prd/`、`to-issues/` 目录；更新 `workflow-router`、`brainstorming`（SKILL.md + openai.yaml）、`grill-me`、`quick-change`、`README.md`、`AGENTS.md` 中全部旧引用为 `$to-spec`/`$to-plan`；更新 `scripts/validate-skills.py` 契约常量并新增 stale-text 检查。结束时 `validate-skills.py` 必须全绿。

## 验收标准 (Acceptance Criteria)

- [ ] `to-prd/`、`to-issues/` 目录删除。
- [ ] `workflow-router/SKILL.md`：路由表两行改为"整理成 spec → `$to-spec`"、"拆成任务级 plan → `$to-plan`"，示例段与 Allowed 列表同步替换；analyze 行描述去掉"依赖和并行风险"。
- [ ] `brainstorming/SKILL.md` + `agents/openai.yaml`：handoff 目标改为 `$to-spec`，packet 名称随之调整，禁跳列表改为 `$to-plan`/`$analyze`/`$implement`/`$quick-change`。
- [ ] `grill-me/SKILL.md`：Natural Handoff 规则改为"未 formalized 推荐 `$to-spec`；已有 spec 需拆 plan 推荐 `$to-plan`"。
- [ ] `quick-change/SKILL.md`：升级链路与推荐列表改为 `$to-spec -> $to-plan -> $analyze -> $implement`。
- [ ] `README.md` 链条图（mermaid）与 skill 表格、`AGENTS.md` 默认链路表述更新为 spec/plan 术语。
- [ ] `validate-skills.py`：`GRILL_ME_REQUIRED_TEXT` 中旧推荐文本替换为 ``推荐 `$to-spec` ``/``推荐 `$to-plan` ``；新增 stale-text 检查将 `$to-prd`、`$to-issues` 视为过期措辞，作用域限 `*/SKILL.md`、`README.md`、`AGENTS.md`，不扫描 `docs/`。
- [ ] `python scripts/validate-skills.py` 退出码 0（SC-001）。
- [ ] `grep -r "to-prd\|to-issues"`（排除 `docs/features/`、`.git`）零命中（SC-002）。
- [ ] 按路由表人工核对 spec/plan 两场景各只命中一个 skill（SC-003）。

## 测试说明 (Testing Notes)

- Verification seam: `python scripts/validate-skills.py` + 仓库级 grep（上两条验收即命令本身）。
- Prior art: validator 现有 `STALE_WORKFLOW_TEXT` 机制——新检查按同一模式扩展，不改校验架构。
- Manual fallback: 逐文件 diff review，确认没有半改状态的引用。

## 并行执行说明 (Parallel Execution Notes)

- 必须单独、完整、一次提交：validator 常量与 grill-me/README/AGENTS/workflow-router 契约文本互锁，任何拆分提交都会产生校验红窗口。

## 实现说明 (Implementation Notes)

- 建议实施顺序：先删目录 → 改五处 SKILL.md/yaml 引用 → 改 README/AGENTS → 最后改 validator 常量并新增 stale-text → 跑全量校验。
- stale-text 作用域实现注意：现有 BAD_TEXT/STALE_WORKFLOW_TEXT 的扫描目标需要确认是否已排除 `docs/`；若 validator 本就只扫 SKILL.md + 根文档则直接沿用，不要顺手扩大扫描范围。
- `find-skills` 触发词兼容：README 表格中 `to-spec`/`to-plan` 的一句话描述避免复用旧 description 的关键词组合（对应 PRD Open Question 第二条）。
