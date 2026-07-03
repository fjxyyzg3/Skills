# ISSUE-001: 新建 `to-spec` skill

## 元数据 (Metadata)

- **Type**: `HITL`
- **Covers**: `FR-001, FR-002, FR-015, FR-016`
- **Parallelization**: `coordination-needed`
- **Wave**: 1
- **Depends on**: `None`
- **Unblocks**: `ISSUE-002, ISSUE-003, ISSUE-004, ISSUE-005`

## 构建内容 (What to build)

创建 `to-spec/SKILL.md` 和 `to-spec/agents/openai.yaml`，将 conversation context、brainstorming handoff 或本地文件整理成叙事型 spec，默认写入 `docs/features/<feature-slug>/spec.md`，并负责创建/更新 feature manifest（artifact 清单：`spec.md`、`plan.md`、`analysis.md`）。

spec 模板结构：问题陈述、方案与架构、关键决策与取舍、功能需求（`FR-###`）、成功标准（`SC-###`）、测试决策（verification seam / prior art / manual fallback）、风险与开放问题、plan 交接说明。正文中文优先，含完整语言契约 marker 与例外句。

## 验收标准 (Acceptance Criteria)

- [ ] `to-spec/SKILL.md` frontmatter `name: to-spec`，description 覆盖 spec/design doc/需求整理触发场景，且措辞不与旧 `to-prd` description 雷同。
- [ ] SKILL.md 含语言契约 marker 句和例外句（validator 逐字校验）。
- [ ] spec 模板包含叙事章节 + `FR-###`/`SC-###` 稳定 ID + 测试决策 + plan 交接说明。
- [ ] 明确输出路径约定：`docs/features/<feature-slug>/spec.md`；manifest 产物行为 `spec.md`/`plan.md`/`analysis.md`，无 `Issues` 行。
- [ ] `agents/openai.yaml` 含 `display_name`、`short_description`（25–64 字符）、`default_prompt`（单行引号、引用 `$to-spec`）。
- [ ] Natural Handoff：完成后最多推荐 `$to-plan` 作为唯一 next skill。
- [ ] description 与模板措辞经用户过目确认（human-gate）。

## 测试说明 (Testing Notes)

- Verification seam: `python scripts/validate-skills.py`（新目录自动纳入全量校验）；人工 review 模板字段。
- Prior art: 旧 `to-prd/SKILL.md` 的输出约定、语言契约段与验证清单结构；obra-superpowers `brainstorming` 的 spec 叙事结构。
- Manual fallback: 用一个小需求人工试跑，核对产物字段。

## 并行执行说明 (Parallel Execution Notes)

- 与 ISSUE-002 共享模板字段约定（`FR-###` 定义方、`Covers` 消费方）和相互的 handoff 措辞；建议串行先行。

## 实现说明 (Implementation Notes)

- 在 ISSUE-005 完成前，SKILL.md 内不要引用 `$to-prd`/`$to-issues`（避免为原子切片制造额外改动点）；Natural Handoff 直接写 `$to-plan`。
- 沿用 workflow contract 字段规范：中文主文 + 英文字段名/ID；禁止英文模板句式。
- spec 定位沿袭旧 to-prd 的边界：不写逐文件实施计划，实现细节只记录稳定 contract/schema/API/architecture decision——文件级落点是 `to-plan` 的职责。
