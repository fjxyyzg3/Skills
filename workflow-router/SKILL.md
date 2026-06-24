---
name: workflow-router
description: Use when starting or resuming a workflow skill chain, deciding which skill should handle a task, interpreting a Next Skill Gate, or choosing a controlled next step without automatically invoking high-risk workflow skills.
---

# Workflow Router

在 workflow skills 之间做受控路由。本 skill 判断当前任务应使用哪个 skill，跨 skill 连续执行需要用户明确确认

## Language Contract

语言契约：生成的文档和聊天输出默认以中文优先；代码、命令、API 名称、契约字段、ID、专有名词以及必要的技术术语保留英文。用户或目标项目明确要求英文时可以例外，但必须记录原因。

## Controlled Chain Protocol

- 先判断当前请求是解释、规划、artifact 分析、分支准备、实现、诊断、review、verification、收尾还是会话整理。
- 如果用户已经明确点名 `$skill-name`、`use <skill-name>` 或 `使用 <skill-name>`，优先使用该 skill；若明显不匹配或风险过高，先说明原因并推荐更合适的 allowed skill。
- 如果用户没有点名 skill，根据任务上下文选择最小必要 skill；这属于当前任务路由，不等于允许跨 skill 连续自动执行。
- 如果上一条输出包含 `Next Skill Gate`，只有用户本轮明确点名推荐的 skill，才算确认进入下一步；`继续`、`可以`、`按你说的办`、`go ahead` 不算确认。
- `to-prd`、`to-issues`、`quick-change`、`diagnose`、`diagnose-ue`、`implement` 和 `session-curator` 可以按上下文作为当前任务 skill 使用；但它们完成后的下一跳仍必须通过 gate 停止。
- 不写文件、不改分支、不运行实现命令、不调用远端服务。路由完成后停在 gate。

## Routing Map

| Situation | Recommend |
| --- | --- |
| 需要源码解释、调用链、架构图或本地解释报告 | `$clarify` |
| 需要拷问方案、约束、风险、验收标准 | `$grill-me` |
| 需要把上下文整理成 PRD/spec | `$to-prd` |
| 需要把 PRD/spec/plan 拆成本地 issues | `$to-issues` |
| 已有 PRD/issues/plan，需要只读检查一致性、覆盖率、依赖和并行风险 | `$analyze` |
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

## Output Format

```markdown
## Workflow Routing Decision

- Current context: ...
- Recommended skill: `$skill-name` / `none`
- Why: ...
- Confirmation phrase: `使用 $skill-name`
```

如果没有合适 skill，推荐 `none` 并直接说明原因。

## 完成标准

- 已根据当前任务选择一个最小必要 skill 或 `none`。
- 已指出该 skill 是否可以作为当前任务 skill 使用，以及是否还有内部确认门。
- 未自动调用下一 skill。
- 未写文件、改分支或开始实现。

## Allowed Next Skills

Allowed: `$analyze`, `$checking-branch`, `$clarify`, `$diagnose`, `$diagnose-ue`, `$finishing-branch`, `$grill-me`, `$handoff`, `$implement`, `$improve-codebase-architecture`, `$quick-change`, `$requesting-code-review`, `$session-curator`, `$tdd`, `$to-issues`, `$to-prd`, `$verification-before-completion`, `none`.

## Next Skill Gate

最终输出本 skill 时，在常规结果后追加一次本 section。中途阻塞或分支确认不要使用本 section。

- Current skill result: `completed / blocked / needs decision`
- Recommended next skill: one allowed skill or `none`
- Controlled chain mode: `recommend-only`; this skill may recommend a next skill but must not invoke it automatically.
- Why: one sentence
- User confirmation required: `yes` if recommended next skill is not `none`; otherwise `no`
- Stop rule: If a next skill is recommended, stop after this gate. Do not invoke it, write files, change branches, or start implementation until the user's next message explicitly names that skill (`$skill-name`, `use <skill-name>`, or `使用 <skill-name>`). Generic approval such as `继续`, `可以`, `按你说的办`, or `go ahead` is not confirmation.
