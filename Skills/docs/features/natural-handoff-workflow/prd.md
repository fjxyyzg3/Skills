# Natural Handoff Workflow PRD

## 元数据 (Metadata)

- **Status**: Draft
- **Source**: conversation context and current `fjxyyzg3-Skills` workflow docs
- **Generated at**: 2026-06-24
- **Feature Slug**: natural-handoff-workflow

## 问题陈述 (Problem Statement)

当前 workflow skills 已经有 `workflow-router` 和 `Next Skill Gate` 这类受控路由概念，但用户可见输出过于机械，并且现有规则把 `继续`、`可以`、`按你说的办`、`go ahead` 等自然确认视为无效。这会让 skill 链路显得像协议审计，而不是正常协作；同时 `clarify`、需求澄清、诊断和实现入口之间的职责边界还需要更清楚，避免解释型或定位型 skill 滑入写代码。

## 目标 (Goals)

- 将用户可见的生硬 `Next Skill Gate` 改为自然语言 `Natural Handoff`。
- 让自然确认语可以触发上一条回复中唯一推荐的 next skill。
- 明确 `clarify`、`grill-me`、`brainstorming`、`diagnose`、`diagnose-ue`、`quick-change` 和完整实现链路的职责边界。
- 保留 workflow 的可控性：一个 skill 完成后最多推荐一个 next skill，且不能用自然确认绕过实现类 skill 的内部安全门。
- 让后续 skill 迭代可以通过文档、metadata 和 validator 防止旧规则回漂。

## 非目标 (Non-Goals)

- 不在本 PRD 阶段直接修改任何 skill 行为。
- 不设计全自动跨 skill 连续执行；本需求仍然是受控链路。
- 不取消实现类 skill 的分支、scope、verification、commit、push 等安全确认。
- 不把所有 skill 都强行纳入同一输出模板；解释型 skill 可以停在自然完成语。

## 用户故事 (User Stories)

1. 作为维护 skill workflow 的用户，我希望每个 skill 完成后用自然语言交接下一步，以便交互不再显得像字段清单。
2. 作为连续使用多个 workflow skill 的用户，我希望回复 `继续`、`可以` 或 `按你说的办` 时能进入刚才唯一推荐的 next skill，以便减少重复输入。
3. 作为审查 workflow 边界的用户，我希望 `clarify` 只回答问题，不推荐后续流程，以便解释任务不会被自动推向规划或实现。
4. 作为处理 feature 或 bug 的用户，我希望根据难度选择 `$quick-change` 或完整 `$to-prd -> $to-issues -> $analyze -> $implement` 链路，以便小改动不被过度流程化，复杂变更也不会缺少追踪。

## 功能需求 (Functional Requirements)

- **FR-001**: workflow skill 结束时不再输出可见的 `Next Skill Gate` 字段清单，而是使用 1-3 句自然语言说明当前结果、推荐下一步和理由。
- **FR-002**: 自然交接一次最多推荐一个 next skill；如果无法确定唯一下一步，必须明确停住并请用户选择。
- **FR-003**: 显式确认语包括 `$skill-name`、`use <skill-name>` 和 `使用 <skill-name>`，自然确认语包括 `继续`、`可以`、`按你说的办`、`go ahead`、`ok` 和 `好的`。
- **FR-004**: 自然确认语只绑定上一条回复中唯一推荐的 next skill；如果上一条给了多个选项，或用户确认时附加新条件、改变方向，必须重新路由。
- **FR-005**: `clarify` 只用于回答问题、解释源码、调用链、架构或本地证据，不推荐任何后续 skill；需要收尾时应自然说明“本次解释到此结束”。
- **FR-006**: `grill-me` 和 `brainstorming` 只用于明确需求、比较方案、定义边界、风险和验收，不写业务代码，也不自动进入实现。
- **FR-007**: `diagnose` 和 `diagnose-ue` 只用于 bug 定位、复现、证据收集、root cause 和修复建议，不直接写持久实现代码；如果需要修复，应通过后续 `$quick-change` 或 `$implement` 进入实现链路。
- **FR-008**: feature 和 bug fix 的实现入口按风险分流：小、清楚、低风险且可快速验证的改动推荐 `$quick-change`；跨模块、需求不清、影响 contract、多 slice 或验收复杂的变更推荐完整 `$to-prd -> $to-issues -> $analyze -> $implement` 链路。
- **FR-009**: 其它 skill 可以按上下文触发当前任务路由，但一个 skill 完成后的跨 skill 下一跳仍必须经过自然交接和用户确认。
- **FR-010**: 自然确认不得绕过目标 skill 内部安全门；例如实现类 skill 仍需处理分支、scope、baseline、verification、commit 或 push 的确认要求。
- **FR-011**: repo docs、skill docs、agents metadata 和 validator 必须同步描述 `Natural Handoff`，避免旧的 `Next Skill Gate`、`继续不算确认` 或 explicit-only 语义回漂。

## 成功标准 (Success Criteria)

- **SC-001**: `workflow-router` 的用户可见输出规则使用 `Natural Handoff`，并接受自然确认语进入唯一推荐的 next skill。
- **SC-002**: `clarify` 的文档明确不推荐后续 skill，且不会要求输出 next-skill gate。
- **SC-003**: `grill-me`、`brainstorming`、`diagnose` 和 `diagnose-ue` 的职责边界明确写明“不直接写业务代码”。
- **SC-004**: `quick-change` 与完整链路的选择标准可由后续 issue 或 reviewer 检查。
- **SC-005**: `python scripts/validate-skills.py` 通过，并能覆盖关键结构规则或至少不再鼓励旧 `Next Skill Gate` 文案。
- **SC-006**: 使用 `rg` 检查时，不应在面向用户的 workflow 规则中残留“`继续` 不算确认”的旧语义。

## 实现决策 (Implementation Decisions)

- 使用 `Natural Handoff` 作为新交接概念，替代用户可见的 `Next Skill Gate`。
- 保留 `recommend-only` 的核心安全语义：skill 可以推荐下一步，但不会在没有用户确认时自动执行。
- 自然确认只在上一条有唯一推荐 next skill 时生效，避免把泛泛的“继续”错误绑定到多选决策。
- `clarify` 是例外路径：它可以自然结束，但不参与 next skill 推荐。
- 实现类 skill 的内部确认门不被降级；自然交接只负责 skill 之间的转场，不负责批准代码修改、提交或推送。

## 测试决策 (Testing Decisions)

- Verification seam（验证切入点）: `python scripts/validate-skills.py`、针对 stale phrase 的 `rg` 检查、以及人工审查典型 skill 收尾文本。
- Prior art（现有依据）: 当前仓库已有 `workflow-router`、`Allowed Next Skills` 和 `Next Skill Gate` 概念，但文案和确认语义需要更新。
- Manual fallback（手动兜底）: 如果 validator 不适合检查自然语言质量，至少用 checklist review 确认每个相关 skill 的职责边界、确认语义和自然交接样例。

## 风险和开放问题 (Risks and Open Questions)

- **Risk**: 自然确认语过宽可能误触发下一 skill；通过“上一条必须只有一个推荐 next skill”降低风险。
- **Risk**: 如果只改 `workflow-router` 而不改各 skill 和 validator，旧 gate 语义会继续回漂。
- **Risk**: `diagnose` 当前可能包含测试或调试实现动作，后续需要小心区分“定位证据”与“持久代码修改”。
- **Open Question**: 是否要保留内部结构化字段供 validator 或 agent 自检使用，但禁止直接暴露给用户。
- **Open Question**: `ok` 和 `好的` 是否需要支持大小写、标点和短语变体，例如 `OK`、`好`、`行`。

## Issue 拆分交接说明 (Handoff Notes for Issue Breakdown)

- 推荐 vertical slice 维度：先更新 workflow contract 和 README/AGENTS，再更新 `workflow-router`，再逐个更新边界相关 skills，最后加强 validator。
- 高风险 dependencies：`workflow-router`、`clarify`、`grill-me`、`brainstorming`、`diagnose`、`diagnose-ue`、`quick-change`、`to-prd`、`to-issues`、`implement` 之间的触发语义需要保持一致。
- 需要 human-gate 的决策：自然确认语的完整词表、内部结构化自检是否保留、以及诊断 skill 是否允许临时测试或 instrumentation。
