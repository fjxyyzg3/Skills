---
name: using-skills
description: Use when a task may match one or more local workflow skills, when starting a new request, choosing skill order, chaining clarify/grill-me/to-prd/to-issues/analyze/implement/diagnose/review/verification/finish workflows, or deciding whether a requested skill should be loaded before acting.
---

# Using Skills

本 skill 是仓库级 workflow router。先判断任务类型，再加载最小必要 skill，并按正确顺序执行。它解决的是“有 skill 但 agent 没有稳定调用”的问题。

## 核心规则

- 收到任务后，先判断是否有本地 skill 适用；有适用 skill 时先加载 skill，再行动。
- 用户显式点名某个 skill 时，必须使用该 skill；若另一个流程 skill 会影响执行顺序，先说明组合顺序。
- Process skill 优先于 implementation skill：先决定怎么工作，再写代码或产出文档。
- 不要只凭记忆执行旧版流程；读取当前 `SKILL.md`。
- 如果多个 skill 都适用，选择覆盖当前风险的最小集合，不要把所有 skill 都加载进上下文。

## 路由表

| 用户意图 | 首选 skill | 常见后续 |
| --- | --- | --- |
| 解释代码、找行为位置、画流程图 | `clarify` | `to-prd` 或 `analyze` |
| 拷问方案、打磨需求边界 | `grill-me` | `to-prd` |
| 生成产品/工程 PRD | `to-prd` | `to-issues` |
| 把 PRD/plan/spec 拆成本地 issues | `to-issues` | `analyze` |
| 检查 PRD/issues/plan 是否一致 | `analyze` | `to-prd`、`to-issues` 或 `implement` |
| 执行实现 | `checking-branch` + `implement` | `requesting-code-review`、`verification-before-completion`、`finishing-branch` |
| debug、bug、failing、broken、performance regression | `diagnose` | `requesting-code-review`、`verification-before-completion` |
| UE/Unreal Engine 问题 | `diagnose-ue` | `requesting-code-review`、`verification-before-completion` |
| 新增或修改本仓库 skill | `writing-skills` | `analyze`、`verification-before-completion` |
| 更新项目原则或质量门 | `constitution` | `analyze` |

## 标准链路

### 新功能

1. 用 `grill-me` 或 `to-prd` 明确目标、边界和验收。
2. 用 `to-issues` 拆成 vertical slices、dependency graph 和 execution waves。
3. 用 `analyze` 做只读一致性与覆盖率检查。
4. 用 `checking-branch` 确认当前开发分支、Git 状态和 baseline。
5. 用 `implement` 按 TDD 执行。
6. 用 `requesting-code-review` 评审规格符合性和代码质量。
7. 用 `verification-before-completion` 做完成前验证。
8. 用 `finishing-branch` 汇总分支状态和交付选项。

### Bug 或性能回归

1. 用 `diagnose` 或 `diagnose-ue` 建立反馈循环并收敛根因。
2. 修复后用 `requesting-code-review` 检查 regression test 和实现质量。
3. 用 `verification-before-completion` 确认原始 repro、回归测试和临时 instrumentation。

### Skill 维护

1. 用 `writing-skills` 定义触发场景和压力测试。
2. 修改 `SKILL.md`、`agents/openai.yaml` 和必要资源。
3. 用 validator 或结构检查验证所有 skill。
4. 用 `analyze` 检查工作流链路是否断裂。

## 冲突处理

- 用户的直接要求优先于本 skill；但如果跳过流程会增加风险，要说明风险和推荐默认做法。
- 如果 skill 之间冲突，选择更具体的领域 skill。例如 UE bug 使用 `diagnose-ue`，不是通用 `diagnose`。
- 如果当前环境没有某个 skill 依赖的工具，说明降级方式并继续执行可完成的部分。

## 输出要求

开始工作时用一句话说明正在使用哪些 skill 以及原因。完成时报告已执行的链路、跳过的环节和原因。
