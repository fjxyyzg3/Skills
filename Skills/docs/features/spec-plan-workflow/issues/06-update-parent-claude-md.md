# ISSUE-006: 更新父仓库 `CLAUDE.md`

## 元数据 (Metadata)

- **Type**: `AFK`
- **Covers**: `FR-017`
- **Parallelization**: `sequential`
- **Wave**: 4
- **Depends on**: `ISSUE-005 (hard: 链条与 validator 行为定稿后才能写文档)`
- **Unblocks**: `None`

## 构建内容 (What to build)

更新父仓库 `C:\WorkSpace\skill-development\CLAUDE.md`（skill-development 根目录，位于 submodule 之外）：canonical chain、validator 常见失败项列表、Natural Handoff 具体规则三处的 PRD/issues 术语替换为 spec/plan。与 submodule 指针更新（gitlink bump）同一提交完成。

## 验收标准 (Acceptance Criteria)

- [ ] "Commands" 节 validator 常见失败项：grill-me 契约描述与新常量一致；无 to-prd/to-issues 字样。
- [ ] "Natural Handoff" 节具体规则更新：`to-prd → to-issues` 相关表述改为 `to-spec → to-plan`；"已有 PRD/issue/plan artifacts 默认链路"改为"已有 spec/plan artifacts"。
- [ ] canonical chain 描述更新为：`workflow-router` 路由 → ... → `to-spec` → `to-plan` → `analyze` → `checking-branch` → implementation → `requesting-code-review` → `verification-before-completion` → `finishing-branch`。
- [ ] 父仓库提交包含 `submodules/fjxyyzg3-Skills` 的新 gitlink。
- [ ] 收尾三连检查通过：`git status --short`、`git submodule status --recursive`、`git diff --check`。

## 测试说明 (Testing Notes)

- Verification seam: 人工 review CLAUDE.md diff + 父仓库收尾三连命令。
- Prior art: 父仓库 CLAUDE.md 现行结构（本次只改术语与链条，不动章节组织）。
- Manual fallback: 无（纯文档，人审即可）。

## 并行执行说明 (Parallel Execution Notes)

- 跨 repo 边界，单独提交；无并行对象。

## 实现说明 (Implementation Notes)

- 历史 artifact 定位段（`improvement-plan-*.md` 等）不动；`docs/features/natural-handoff-workflow/` 的旧引用是历史记录，不改。
- CLAUDE.md 中 validator 失败项列表如与 ISSUE-005 实际落地的检查有出入，以 validator 代码为准回写文档。
