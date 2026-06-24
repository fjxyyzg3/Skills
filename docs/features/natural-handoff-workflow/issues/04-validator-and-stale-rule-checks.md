# ISSUE-004: 加强 validator 与 stale-rule 检查

## 元数据 (Metadata)

- **Type**: `AFK`
- **Covers**: `FR-011`
- **Parallelization**: `sequential`
- **Wave**: 3
- **Depends on**: `ISSUE-002, ISSUE-003 (hard: 需要最终文案稳定后再固化检查)`
- **Unblocks**: `None`

## 构建内容 (What to build)

更新 `scripts/validate-skills.py` 和必要的本地检查约定，防止旧的 `Next Skill Gate` 用户可见格式、`继续` 不算确认、explicit-only 触发语义或缺失 `Natural Handoff` 的文案回漂。同时修复当前 validator 已暴露的既有问题，确保最终 `python scripts/validate-skills.py` 可以通过。

## 验收标准 (Acceptance Criteria)

- [ ] `python scripts/validate-skills.py` 通过。
- [ ] validator 或补充检查能发现 `继续` / `go ahead` 被描述为无效确认的旧语义。
- [ ] validator 或补充检查能发现用户可见 `Next Skill Gate` 字段清单回漂到 workflow skills。
- [ ] validator 或补充检查能确认关键 workflow 文档包含 `Natural Handoff`。
- [ ] 当前 `workflow-router/SKILL.md` 的 `Language Contract` marker 问题被修复或 validator 规则被合理调整。
- [ ] `rg` 检查不再在面向用户的 workflow 规则中发现 stale confirmation wording。

## 测试说明 (Testing Notes)

- Verification seam: `python scripts/validate-skills.py`
- Verification seam: `rg -n "继续.*不算确认|go ahead.*不算确认|Next Skill Gate" README.md AGENTS.md workflow-router *.md */SKILL.md`
- Prior art: 当前 validator 已能检查 skill metadata 和 Language Contract，但尚未覆盖 `Natural Handoff` 语义。
- Manual fallback: 如果自然语言规则难以完全自动化，保留最小 stale phrase blacklist，并在 README 中记录人工 review checklist。

## 并行执行说明 (Parallel Execution Notes)

- 本 issue 应在 Wave 3 串行执行，避免在文案仍变动时过早固化 validator。
- 不要在本 issue 中重新设计 workflow contract；发现 contract 缺口时回到前置 issue 修正。

## 实现说明 (Implementation Notes)

- 先修复 validator 当前失败点，再添加针对 stale phrase 的小而明确检查。
- 避免 validator 过度解析自然语言；优先检查稳定 marker、禁止短语和关键文件存在性。
- 如果保留内部结构化字段，需要明确 validator 检查的是内部 contract，不是用户可见输出模板。
