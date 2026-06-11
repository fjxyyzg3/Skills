---
name: quick-change
description: Use only when the user explicitly invokes Quick Change, quick-change, or $quick-change for a small bug fix, quick fix, tiny behavior change, copy/configuration tweak, or low-risk implementation task; do not infer this skill from ordinary small requests or quick fixes.
---

# Quick Change

面向小型 bug 和小型需求的快速链路。它跳过 PRD、issue breakdown 和 `analyze`，但不跳过分支确认、范围收束、最小验证和风险升级。

## 手动触发边界

- 只在用户明确写出 `quick-change`、`Quick Change`、`$quick-change` 或“使用快速变更 skill”时加载本 skill。
- 不要因为任务看起来小、用户说 quick fix、小 bug、小需求、copy tweak 或配置改动就自动触发。
- 如果当前任务适合本流程但用户没有手动调用，只能简短建议“可以使用 `$quick-change`”，不要自行切换到本 skill。

## Language Contract

Language Contract: generated documents and chat outputs default to Chinese-first; preserve English for code, commands, API names, contract fields, IDs, proper nouns, and necessary technical terms. 用户或目标项目明确要求英文时可以例外，但必须记录原因。

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

- 复杂 bug：停止快速链路，并建议用户显式调用 `$diagnose` 或 `$diagnose-ue`。
- 需求边界不清：使用 `grill-me` 或 `to-prd`。
- 多 slice 实现：使用 `to-issues` 和 `analyze`。
- 中高风险改动：使用 `requesting-code-review`。

## 工作流程

1. 用 `checking-branch` 确认当前开发分支、Git 状态和 baseline。
2. 写下 1-3 行任务 contract：
   - Scope:
   - Acceptance:
   - Verification:
3. 小 bug 先建立最小 repro、targeted failing test 或等价 pass/fail 命令。
4. 小需求优先写一个 external behavior test；不适合自动化时记录 manual/static verification。
5. 做最小实现，只改完成任务所需内容。
6. 运行 targeted verification；必要时运行邻近测试。
7. 做轻量 self-review：
   - 是否只覆盖约定 scope。
   - 是否有未处理 edge case。
   - 是否需要升级到完整 review。
8. 用简短完成报告说明修改、验证、跳过项和残留风险。

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
