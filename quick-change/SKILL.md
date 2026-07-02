---
name: quick-change
description: Use for quick changes: small bug fixes, tiny behavior/copy/configuration tweaks, or low-risk implementation tasks with one-sentence acceptance and a fast verification seam.
---

# Quick Change

面向小型 bug 和小型需求的快速链路。它跳过 PRD、issue breakdown 和 `analyze`，但不跳过分支确认、范围收束、最小验证和风险升级。

## 进入边界

- 适用于小、清楚、低风险且可快速验证的 bug fix、tiny feature、copy/configuration tweak 或行为微调。
- 可以由用户显式调用，也可以由 `workflow-router` 或上一轮 `Natural Handoff` 推荐后进入。
- 不要把中高风险任务包装成 quick change；一旦范围扩大，停止快速链路并升级。

## Language Contract

语言契约：生成的文档和聊天输出默认以中文优先；代码、命令、API 名称、契约字段、ID、专有名词以及必要的技术术语保留英文。用户或目标项目明确要求英文时可以例外，但必须记录原因。

## Trigger Description

`quick-change` 只处理一个 tight change：scope 可用一句话圈住，acceptance 可被用户直接判断，verification 能在当前环境快速给出 pass/fail 信号。写不出 `Scope / Acceptance / Verification` 三行时，不进入快速链路。

## Pressure Scenarios

1. User says: "顺手把这个也改一下。"
   - Expected skill trigger: 重新收束为一个 tight change，只保留当前任务直接需要的改动。
   - Common failure without skill: 把相邻重构、命名整理或额外需求混进 diff。
   - Behavior this skill must force: 每个改动行都能对应到 contract 的 `Scope` 或 `Acceptance`。
2. User reports a small bug, but no reliable pass/fail signal appears quickly.
   - Expected skill trigger: 10-15 分钟内建立最小 repro、targeted failing test 或等价命令。
   - Common failure without skill: 直接猜修，最后无法证明 bug 被修掉。
   - Behavior this skill must force: 没有 reliable seam 时停止快速链路，并通过 `Natural Handoff` 推荐 `$diagnose` 或 `$diagnose-ue`。
3. A tiny edit touches shared contract、core workflow、performance-sensitive path 或底层共享代码。
   - Expected skill trigger: 先证明现有数据、字段或 seam 不能满足当前语义。
   - Common failure without skill: 为了快速落地新增重复计算、结构字段或隐藏耦合。
   - Behavior this skill must force: 影响面变大时升级到 `$analyze` 或 `$implement`，不要把风险藏在 quick change 中。

## 适用条件

全部满足时使用：

- 预期修改 1-3 个文件。
- 验收条件能用一句话说清。
- 有明显、快速的 verification seam。
- 不改 schema、migration、public API、权限、安全、计费、数据迁移或核心 workflow。
- 不需要产品、设计、架构或多角色决策。
- 不需要并行执行或拆分多个 issues。

## 升级条件

遇到任一情况，停止快速链路并升级：

- 需求变成多个 slice。
- 影响 shared contract、schema、核心 workflow、权限、安全或数据生命周期。
- 小 bug 在 10-15 分钟内无法建立可靠 repro 或 pass/fail 信号。
- 没有可接受的 verification seam。
- 用户描述含糊，验收标准无法一句话确认。
- 修复过程中发现架构性问题、测试 seam 缺失或影响面扩大。

升级目标：

- 复杂 bug：停止快速链路，并通过 `Natural Handoff` 推荐 `$diagnose` 或 `$diagnose-ue`。
- 需求边界不清：通过 `Natural Handoff` 推荐 `$grill-me` 或 `$to-prd`。
- 多 slice 实现：通过 `Natural Handoff` 推荐 `$to-issues` 或 `$analyze`。
- 中高风险改动：如果已有 artifacts，通过 `Natural Handoff` 推荐 `$analyze` 或 `$implement`；如果没有 artifacts，推荐完整 `$to-prd -> $to-issues -> $analyze -> $implement` 链路。

## 工作流程

1. 用 `checking-branch` 确认当前开发分支、Git 状态和 baseline。
2. 写下 1-3 行任务 contract；如果任一行写不清，先按升级条件停止：
   - Scope:
   - Acceptance:
   - Verification:
3. 小 bug 先建立最小 repro、targeted failing test 或等价 pass/fail 命令；信号必须先失败或能稳定暴露症状。
4. 小需求优先写一个 external behavior test；不适合自动化时，先记录 manual/static verification。
5. 对 performance-sensitive path 或共享底层代码，做最小实现前先列出现有数据来源和不可复用原因；若计划新增重复计算或结构字段，先证明现有字段不能满足语义。
6. 做最小实现，只改完成 contract 所需内容。
7. 运行 targeted verification；必要时运行邻近测试。
8. 做轻量 self-review：
   - 是否只覆盖约定 scope。
   - 是否有未处理 edge case。
   - 是否需要升级到完整 review。
9. 用简短完成报告说明修改、验证、跳过项和残留风险。

## Natural Handoff

- 完成后如果没有 commit、push、PR 或分支收尾需求，推荐 `none`，自然结束。
- 如果用户要求分支收尾，最多推荐 `$finishing-branch`，不要在本 skill 内替代它的 gate。
- 如果触发升级条件，停止当前链路，并最多推荐一个 next skill：`$diagnose`、`$diagnose-ue`、`$grill-me`、`$to-prd`、`$to-issues`、`$analyze` 或 `$implement`。
- 自然确认只进入上一条唯一推荐的 next skill，不代表跳过该 skill 自己的 branch、scope、verification、review、commit 或 push gate。

## 输出格式

```markdown
## 快速变更契约 (Quick Change Contract)

- Scope:
- Acceptance:
- Verification:

## 结果 (Result)

- Changed:
- Verified:
- Skipped:
- Risk:
```

## 完成标准

- 已确认当前分支可用，或用户明确允许例外。
- Scope、acceptance、verification 已明确。
- 已执行 targeted verification，或说明无法执行的原因。
- 没有把中高风险任务伪装成 quick change。
- 若触发升级条件，已停止快速链路并切换到正确 workflow。
