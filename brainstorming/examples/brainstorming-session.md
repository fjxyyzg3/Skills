# Brainstorming Session Example

## Input

用户提出一个模糊 feature idea，例如“想做一个编辑器里的批量操作功能，但还没想清楚”。

## Good Flow

1. 读取用户指定的 context；没有指定文件时，快速查看项目结构、README、AGENTS 和相关 docs。
2. 说明 assumptions、constraints、non-goals 和无法从项目事实确认的信息。
3. 只问一个最高优先级澄清问题；回答后先收束结论，再问下一个依赖它的问题。
4. 比较 2-3 个方案，分别说明 shape、benefits、costs/risks、verification 和 recommendation。
5. 按复杂度设置确认点：复杂设计逐 section 确认，小型设计可合并确认。
6. 用户确认整体设计后，根据需要选择且只选择一种结束形态：
   - `implementation-plan`：输出 `PlanningHandoffPacket v1`，唯一推荐 `$to-plan`。
   - `spec-only`：整理 formal-spec handoff，唯一推荐 `$to-spec`。
   - `stop-here`：不写 artifact，推荐 `none`。

## Bad Flow

- 在理解 context 前直接给单一路线。
- 一次提出多个开放问题，让用户无法判断先回答哪个。
- 用户尚未确认设计时，直接创建 spec、plan、mockup 或实现代码。
- 把 `$to-spec`、`$to-plan`、`$analyze`、`$implement` 或 `$quick-change` 串起来自动执行。
- 同时推荐多个 next skills，让自然确认失去唯一指向。
- 只给抽象优缺点，不提供可判断的结构、状态、用户路径或 verification seam。

## PlanningHandoffPacket v1

需要 checked implementation plan 时输出：

- Confirmed problem / goal
- Scope / Non-goals
- Chosen approach
- Alternatives rejected and why
- Key decisions
- Constraints
- Risks and open questions
- Verification seam

自然确认唯一推荐的 `$to-plan` 后，由 `$to-plan` 创建 Planning Authorization；brainstorming 本身不写 planning artifacts，也不授权实现或 Git 操作。

## Formal-Spec Handoff

用户明确只要 formal spec / decision artifact 时，复用已经确认的内容，并补充：

- Recommended spec focus

由 `$to-spec` 独立写入 spec；完成前不自动进入 plan。
