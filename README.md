# Skills

lihuanyu 个人的 Codex skill 仓库，用于沉淀、维护和迭代可复用 workflow skills。

## 核心链路

```mermaid
flowchart LR
  Start["task context"] --> Router["workflow-router"]
  Router --> Clarify["clarify"]
  Router --> Need["grill-me / brainstorming"]
  Router --> Diagnose["diagnose / diagnose-ue"]
  Router --> Quick["quick-change"]
  Need -->|"需要 implementation plan"| Plan["to-plan"]
  Need -->|"只要 formal spec"| SpecOnly["to-spec"]
  Router --> Plan
  Router --> SpecOnly
  Router --> Audit["analyze existing/external artifacts"]
  Plan --> Risk{"risk routing"}
  Risk -->|"Fast Path"| Fast["plan.md"]
  Risk -->|"Full Path"| Full["spec.md + plan.md"]
  Fast --> Checked["checked plan"]
  Full --> Checked
  Checked --> Branch["checking-branch"]
  Branch --> Work["implementation work"]
  Work --> Review["requesting-code-review"]
  Review --> Verify["verification-before-completion"]
  Verify --> Finish["finishing-branch"]
```

workflow skills 使用 `Natural Handoff` 做自然交接：一个 skill 完成后最多推荐一个 next skill，并用 1-3 句说明结果、推荐下一步和理由。用户回复 `继续`、`可以`、`按你说的办`、`go ahead`、`ok` 或 `好的` 时，只会进入上一条回复中唯一推荐的 next skill；如果上一条给了多个选项，或用户确认时改变条件，必须重新路由。

设计确认后需要 implementation plan 时，`brainstorming` 唯一推荐 `$to-plan`。用户自然确认或显式调用会创建一次 Planning Authorization：`$to-plan` 根据风险自动选择 Fast Path 或 Full Path，在同一次 Planning Run 内生成所需 artifacts、闭环机械 findings 并交付 checked plan。Fast 只写自包含 `plan.md`；Full 写共享 `FR-###` 的 `spec.md + plan.md`；两者都不默认生成 `analysis.md`。

独立 `$to-spec` 用于用户只需要 formal spec / decision artifact 的场景；独立 `$analyze` 用于审查已有或外部 artifacts。它们继续可直接调用，但不再是每次 planning 的固定中间阶段。

`Natural Handoff` 与 Planning Authorization 都不会绕过目标 skill 的安全门。planning 只授权本地 planning artifacts；实现类、分支类、提交类 skill 仍必须处理自己的 scope、branch、verification、review、commit 和 push gate。

## Skills

| Skill | 用途 |
| --- | --- |
| `clarify` | 源码解释、调用链、图表和报告；只回答问题，不推荐后续 skill |
| `brainstorming` | 设计前澄清目标、比较方案，并路由 checked plan、formal spec 或结束 |
| `grill-me` | 追问方案、约束、风险和验收 |
| `quick-change` | 处理小型 bug、小需求和低风险快速改动 |
| `to-spec` | 独立生成叙事型 formal spec 和需求/决策契约 |
| `to-plan` | 按风险生成 Fast/Full planning artifacts 与 checked plan |
| `analyze` | 独立只读检查已有/外部 artifacts 的一致性、覆盖率和接口契约 |
| `checking-branch` | 展示当前分支状态，确认直接修改或创建新分支 |
| `tdd` | 按 RED/GREEN/REFACTOR 循环推进测试先行实现 |
| `implement` | 消费 checked plan 或其他已收束输入，按 TDD、review 和 verification 执行实现 |
| `diagnose` | 执行通用 bug / 性能回归诊断，产出 root cause 和修复入口建议 |
| `diagnose-ue` | 执行 Unreal Engine 问题诊断，产出 UE 运行形态、root cause 和修复入口建议 |
| `improve-codebase-architecture` | 架构加深、重构机会和 testability 改进 |
| `requesting-code-review` | 两阶段实现评审 |
| `verification-before-completion` | 完成前验证质量门 |
| `finishing-branch` | 开发分支收尾和交付选项 |
| `handoff` | 生成跨会话交接文档，方便下一位 agent 接手 |
| `session-curator` | 会话结束后手动提炼通用经验，确认计划后同步项目文档、agent 规则和记忆 |

## 开发原则

- 主要语言使用中文。
- Skill 结构要求、文件名、目录名、YAML frontmatter key、配置字段、命令、代码、API 名称、英文专业术语和英文专有名词保留英文。
- Skill 生成的 Markdown/HTML 文档、分析结论、review、handoff、完成报告和聊天式输出默认中文为主；代码、命令、API 名称、contract fields、稳定 ID、英文专有名词和必要技术术语保留 English。
- 用户明确要求英文，或目标项目已有英文 artifact 规范时可以例外，但必须记录原因。
- 产出型 skill 使用统一 `Language Contract` 标记；核心 section heading 使用中文优先、English 括注。
- 新增或修改 skill 时，明确 pressure scenarios、trigger description 和 metadata，再运行本地 validator。
- workflow skill 完成后通过 `Natural Handoff` 最多推荐一个 next skill；自然确认只绑定上一条唯一推荐，不能跨过目标 skill 的内部安全门。
- `clarify` 是只读解释路径，完成后自然结束，不推荐后续 skill。
- `grill-me`、`brainstorming`、`diagnose` 和 `diagnose-ue` 不直接写业务代码；需要进入修复或实现时，通过 `Natural Handoff` 推荐一个适合当前状态的 next skill。
- 小、清楚、低风险且可快速验证的 feature 或 bug fix 可走 `$quick-change`。
- 需要 checked plan 时直接进入 `$to-plan`：Fast Path 处理边界明确的普通需求，Full Path 固化 public contract、schema、migration、核心 workflow 或跨模块高风险决策。
- `Planning Quality Status: Pass` 的 checked plan 可直接进入 `$implement` 的 branch gate；未检查、失效或 external artifacts 先走独立 `$analyze`。

## 验证

```powershell
python scripts/validate-skills.py
```
