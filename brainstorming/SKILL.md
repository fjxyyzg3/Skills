---
name: brainstorming
description: Use when brainstorming, exploring an idea before design/spec/implementation, comparing product/UX/architecture approaches, or turning a vague feature request into a validated design; ask one question at a time, propose alternatives, and require user approval before writing design artifacts or recommending next workflow skills.
---

# Brainstorming

把模糊想法推进成可验证的设计。目标不是替用户直接决定，而是在实现前澄清目的、约束、成功标准和关键取舍。

## Language Contract

语言契约：生成的文档和聊天输出默认以中文优先；代码、命令、API 名称、契约字段、ID、专有名词以及必要的技术术语保留英文。用户或目标项目明确要求英文时可以例外，但必须记录原因。

## 进入边界

- 适用于用户明确表达要 `brainstorm`、`brainstorming`、头脑风暴、方案探索、设计前澄清、比较多种产品/UX/架构方案，或当前任务明显需要把模糊想法整理成设计时。
- 不要因为普通小改动、明确 bugfix、直接实现请求或已有清晰 issues 就自动阻塞实现。
- 如果当前任务明显缺少目标、边界或验收标准，可以通过 `workflow-router` 或 `Natural Handoff` 推荐 `$brainstorming`，但不要直接开始实现。
- 本 skill 一旦进入，在用户确认设计前不要写业务代码、scaffold 项目、改行为或调用 implementation skill。

## Pressure Scenarios

1. User says: "帮我 brainstorm 一下这个功能怎么做。"
   - Expected skill trigger: 先探索当前项目和用户目标，再逐步收敛到设计。
   - Common failure without skill: 直接给单一路线，隐藏关键假设。
   - Behavior this skill must force: 至少提出 2-3 个方案、取舍和推荐理由。
2. User says: "我有个产品想法，但还没想清楚。"
   - Expected skill trigger: 一次只问一个澄清问题，先定义用户、场景、约束和成功标准。
   - Common failure without skill: 提前写 PRD 或实现计划，后续大幅返工。
   - Behavior this skill must force: 在每个关键 section 后取得用户确认。
3. User says: "这个 UI/架构方向有几种可能，帮我比较。"
   - Expected skill trigger: 比较方案时给出推荐和风险，必要时使用 visual companion 展示可视化差异。
   - Common failure without skill: 用抽象描述代替具体结构，用户难以判断。
   - Behavior this skill must force: 对视觉问题用图或 mockup，对文本问题保持终端讨论。

## 核心规则

- 先理解当前项目 context：用户指定文件、README、AGENTS、相关 docs、近期提交或明显相关源码。
- 一次只问一个问题。能通过读取文件或代码回答的问题，不要问回用户。
- 优先使用 multiple-choice 问题；需要开放回答时保持问题短而具体。
- 先判断 scope。如果用户描述多个独立子系统，先拆解项目边界，不要把多个系统塞进一个设计。
- 至少提出 2-3 个可行方案，说明 trade-offs，并给出推荐方案和理由。
- 设计分 section 展示；复杂 section 控制在足够清晰但不过度展开的长度，简单 section 用几句话即可。
- 每个关键 section 后询问用户是否认可；用户不认可时回到对应问题重新澄清。
- 不要引入用户没有要求、当前目标不需要的 speculative features。
- 在现有 codebase 中工作时，先跟随已有 patterns；只把服务于当前目标的局部改进纳入设计。

## 工作流程

### 1. 探索 context

- 读取用户指定的 artifacts。
- 没有指定文件时，快速查看项目结构、README/AGENTS/CONTEXT、相关 docs 和最近提交。
- 记录 assumptions、constraints、non-goals 和无法从项目事实确认的信息。

### 2. 澄清问题

- 从最高层约束开始：目标用户、触发场景、成功标准、必须兼容的现有行为、明确非目标。
- 如果 scope 过大，先帮助拆成 sub-projects，并选择第一个 sub-project 进入后续流程。
- 每轮只问一个问题；回答后收束结论，再问下一个依赖它的问题。

### 3. 比较方案

为 2-3 个方案分别说明：

- Shape: 方案结构或用户体验形态。
- Benefits: 解决什么问题。
- Costs/Risks: 复杂度、迁移、测试、维护和用户体验风险。
- Verification: 如何验证它真的满足目标。
- Recommendation: 推荐哪个方案，以及为什么。

### 4. 呈现设计

按实际复杂度选择 section，不需要机械填满所有项。常见 section：

- Scope / Non-goals
- User workflow
- Architecture / components
- Data flow / state
- Error handling / edge cases
- Testing / verification
- Rollout / migration

每个 section 后明确问用户是否认可。如果用户提出修正，更新设计后再继续。

### 5. 写设计 artifact

只有在用户确认整体设计后才写文件。默认路径：

- 如果项目已有 `docs/features/<feature-slug>/`：写入 `docs/features/<feature-slug>/design.md`。
- 否则写入 `docs/brainstorming/YYYY-MM-DD-<topic>-design.md`。
- 如果用户指定路径，优先使用用户路径。

设计文档使用中文主文，保留必要 English fields、API、命令和稳定 ID。完成后做快速 self-review：

- 是否有未收束的开放问题。
- 是否有相互矛盾的 scope、设计或验收。
- 是否把多个独立子系统混成一个实现单元。
- 是否存在会导致后续计划误解的模糊要求。
- 是否加入了未被用户目标支撑的功能。

不要自动 commit，除非用户明确要求提交。

### 6. 后续建议

完成设计 artifact 后，让用户先 review。根据用户下一步选择，用 `Natural Handoff` 最多推荐一个 next skill：

- `$to-prd`：需要把设计整理成 PRD 或 requirements 文档。
- `$to-issues`：已有足够清晰的设计，需要拆成本地 issues。
- `$analyze`：已有 PRD/issues/plan，需要只读检查覆盖率和一致性。
- `$implement` 或 `$quick-change`：用户明确要进入实现，且已有足够清晰的 scope。

不要在本 skill 内自动进入实现；自然确认只会进入上一条唯一推荐的 next skill。

## Visual Companion

visual companion 是可选工具，只在视觉问题确实比文字更容易判断时使用。不要一开始就询问是否开启。

适合使用浏览器：

- UI mockups、wireframes、布局比较。
- 架构图、数据流图、关系图。
- 多个视觉方向的 side-by-side comparison。
- spacing、层级、视觉密度或交互布局问题。

适合留在终端：

- scope、需求、成功标准和取舍讨论。
- API、data model、测试策略或非视觉架构选择。
- 用户能用文字直接回答的澄清问题。

第一次出现真正需要可视化的问题时，单独发送一条询问：

```text
这一步可能看图比文字更清楚。我可以打开 browser companion，边做 mockups、diagram 或方案对比边让你选择。它会多消耗一些上下文。要打开吗？
```

用户同意后再读取 [visual-companion.md](visual-companion.md)，并按其中步骤启动 `scripts/start-server.sh`。用户拒绝后继续 text-only，除非用户之后主动提出可视化。

## 完成标准

- 已说明检查过的 context 和仍需假设的点。
- 已一次一个问题地收敛目标、约束、non-goals 和 success criteria。
- 已比较至少 2 个方案；除非任务确实只有一个合理方案，并说明原因。
- 已给出推荐方案及 trade-offs。
- 设计的关键 section 已经得到用户确认。
- 如果写了设计 artifact，已报告绝对路径并完成 self-review。
- 未在设计确认前执行实现动作。
