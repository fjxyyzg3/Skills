---
name: workflow-router
description: Use when starting or resuming a workflow skill chain, deciding which skill should handle a task, interpreting a Natural Handoff, or choosing a controlled next step without bypassing each skill's safety gates.
---

# Workflow Router

在 workflow skills 之间做受控路由。本 skill 判断当前任务应使用哪个 skill，并用自然语言交接下一步；跨 skill 连续执行需要用户确认，但确认可以是自然确认语。

## Language Contract

语言契约：生成的文档和聊天输出默认以中文优先；代码、命令、API 名称、契约字段、ID、专有名词以及必要的技术术语保留英文。用户或目标项目明确要求英文时可以例外，但必须记录原因。

## Controlled Chain Protocol

- 先判断当前请求是解释、规划、artifact 分析、分支准备、实现、诊断、review、verification、收尾还是会话整理。
- 如果用户已经明确点名 `$skill-name`、`use <skill-name>` 或 `使用 <skill-name>`，优先使用该 skill；若明显不匹配或风险过高，先说明原因并推荐更合适的 allowed skill。
- 如果用户没有点名 skill，根据任务上下文选择最小必要 skill；这属于当前任务路由，不等于允许跨 skill 连续自动执行。
- 如果上一条回复只推荐了一个 next skill，用户回复 `继续`、`可以`、`按你说的办`、`go ahead`、`ok` 或 `好的`，视为确认进入该 skill。
- 如果上一条回复给了多个选项，或用户确认时附加新条件、改变方向，必须重新路由；不要把自然确认绑定到模糊选择。
- `Natural Handoff` 只负责 skill 之间的转场，不会批准写文件、改分支、运行实现命令、commit、push 或跳过目标 skill 内部安全门。
- 本 skill 自身不写文件、不改分支、不运行实现命令、不调用远端服务；路由完成后停在自然交接。

## Routing Map

| Situation | Recommend |
| --- | --- |
| 需要源码解释、调用链、架构图或本地解释报告 | `$clarify` |
| 需要拷问方案、约束、风险、验收标准 | `$grill-me` |
| 需要把方向共识整理成叙事型 spec | `$to-spec` |
| 需要把 spec 拆成任务级实现 plan | `$to-plan` |
| 已有 spec/plan，需要只读检查一致性、覆盖率和接口契约 | `$analyze` |
| 即将开始实现，需要确认分支和 baseline | `$checking-branch` |
| 小型低风险变更 | `$quick-change` |
| bug 或性能回归需要系统诊断 | `$diagnose` |
| Unreal Engine 具体症状需要诊断 | `$diagnose-ue` |
| 需要执行实现流程 | `$implement` |
| 用户明确要求 test-first/TDD | `$tdd` |
| 已有实现变更，需要 review | `$requesting-code-review` |
| 完成前需要验证需求覆盖、测试、临时文件和风险 | `$verification-before-completion` |
| 实现完成后需要分支收尾和交付选项 | `$finishing-branch` |
| 需要跨会话交接 | `$handoff` |
| 会话结束后需要沉淀可复用知识 | `$session-curator` |

## Natural Handoff

结束时不要输出字段清单。用 1-3 句自然语言完成交接：

- 说明当前路由判断或当前工作是否完成、阻塞或还需要决策。
- 最多推荐一个 next skill；如果没有合适下一步，明确停在这里。
- 简短说明推荐理由。
- 告诉用户可以显式写 `$skill-name`，也可以回复 `继续`、`可以`、`按你说的办`、`go ahead`、`ok` 或 `好的`。

示例：

```markdown
这一步已经把需求边界收住了。我建议下一步用 `$to-spec` 把它整理成 spec，因为后续还需要拆 plan 和做覆盖检查。你回复“继续”或“使用 `$to-spec`”都可以；如果想先调整边界，也可以直接说。
```

如果没有合适 skill，不推荐下一步，直接说明原因并自然结束。

## 完成标准

- 已根据当前任务选择一个最小必要 skill 或 `none`。
- 已指出该 skill 是否可以作为当前任务 skill 使用，以及是否还有内部确认门。
- 未自动调用下一 skill。
- 未写文件、改分支或开始实现。

## Allowed Routing Targets

Allowed: `$analyze`, `$checking-branch`, `$clarify`, `$diagnose`, `$diagnose-ue`, `$finishing-branch`, `$grill-me`, `$handoff`, `$implement`, `$improve-codebase-architecture`, `$quick-change`, `$requesting-code-review`, `$session-curator`, `$tdd`, `$to-plan`, `$to-spec`, `$verification-before-completion`, `none`.
