# Brainstorming Session Example

## Input

用户提出一个模糊 feature idea，例如“想做一个编辑器里的批量操作功能，但还没想清楚”。

## Good Flow

1. 读取用户指定的 context；没有指定文件时，快速查看项目结构、README、AGENTS 和相关 docs。
2. 说明 assumptions、constraints、non-goals 和无法从项目事实确认的信息。
3. 只问一个最高优先级澄清问题；回答后先收束结论，再问下一个依赖它的问题。
4. 比较 2-3 个方案，分别说明 shape、benefits、costs/risks、verification 和 recommendation。
5. 按复杂度设置确认点：复杂设计逐 section 确认，小型设计可合并确认。
6. 用户确认整体设计且明确要生成正式 spec 后，输出 spec handoff packet，并用 `Natural Handoff` 推荐 `$to-spec`。
7. 用户只需要 brainstorming 结果或暂不进入文档产出时，推荐 `none`。

## Bad Flow

- 在理解 context 前直接给单一路线。
- 一次提出多个开放问题，让用户无法判断先回答哪个。
- 用户尚未确认设计时，直接创建 spec、design doc、mockup 或实现代码。
- 把 `$to-spec`、`$to-plan`、`$implement` 或 `$quick-change` 串起来自动执行。
- 只给抽象优缺点，不提供可判断的结构、状态、用户路径或 verification seam。

## Spec Handoff Packet Shape

只有用户确认要进入正式 spec 时才输出：

- Confirmed problem / goal
- Scope / Non-goals
- Chosen approach
- Alternatives rejected and why
- User workflow / system workflow
- Key decisions and constraints
- Risks and open questions
- Verification seam
- Recommended spec focus
