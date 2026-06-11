---
name: writing-skills
description: Use when creating, editing, validating, or refactoring Codex skills, SKILL.md files, skill descriptions, agents/openai.yaml metadata, bundled references, skill trigger behavior, pressure scenarios, or this repository's reusable workflow definitions.
---

# Writing Skills

把 skill 当成可测试的流程代码来维护。新增或修改 skill 前，先明确它要阻止哪些 agent 失败模式；修改后验证 agent 是否更稳定地执行。

## Language Contract

Language Contract: generated documents and chat outputs default to Chinese-first; preserve English for code, commands, API names, contract fields, IDs, proper nouns, and necessary technical terms. 用户或目标项目明确要求英文时可以例外，但必须记录原因。

## 核心原则

- Skill 只写对 agent 执行任务直接有帮助的内容。
- `description` 优先描述触发条件和症状，避免把完整 workflow 摘成捷径。
- 正文使用中文为主；文件名、YAML key、命令、API、英文术语保留英文。
- 新增或修改 skill 时必须包含统一 `Language Contract` 标记；产出的文档和聊天输出默认中文为主，例外必须记录原因。
- 新 skill 默认包含 `SKILL.md` 和 `agents/openai.yaml`；只有确实需要时才加 `scripts/`、`references/`、`assets/`。
- 不把一次性经验写成 skill；只有可复用流程、纪律、工具或领域知识才沉淀。

## RED：定义压力场景

修改前先写下 2-5 个压力场景。它们应描述用户会如何触发 skill，以及 agent 容易如何失败。

压力来源：

- 时间压力：用户要求“直接做”“别分析太多”。
- 模糊输入：用户只给目标，没有验收。
- 错误捷径：agent 想跳过测试、跳过 review、跳过源码探索。
- 上下文污染：已有计划、旧记忆或相邻 skill 诱导错误。
- 工具限制：没有 subagent、没有浏览器、没有测试环境。

记录格式：

```markdown
## Pressure Scenarios

1. User says: "..."
   - Expected skill trigger:
   - Common failure without skill:
   - Behavior this skill must force:
```

如果没有时间实际 forward-test，也要在最终报告中说明“只做了结构验证，未做压力场景验证”。

## GREEN：写最小 skill

`SKILL.md` 建议结构：

```markdown
---
name: skill-name
description: Use when ...
---

# Skill Name

一句话说明这个 skill 解决什么执行问题。

## Language Contract

Language Contract: generated documents and chat outputs default to Chinese-first; preserve English for code, commands, API names, contract fields, IDs, proper nouns, and necessary technical terms. 用户或目标项目明确要求英文时可以例外，但必须记录原因。

## 核心规则

- ...

## 工作流程

1. ...

## 完成标准

- ...
```

写作约束：

- 用命令式、检查清单和决策规则，少写背景散文。
- 对纪律型 skill，明确禁止常见绕行理由。
- 对复杂流程，给出 artifact contract 和完成标准。
- 对需要额外材料的 skill，在正文中说明何时读取对应 `references/` 文件。

## REFACTOR：堵住漏洞

读完 skill 后问：

- agent 会不会只看 description 就执行错？
- 有没有未定义的停止条件？
- 有没有“应当测试”但没有测试 seam 的地方？
- 是否和 `using-skills`、`implement` 等上游 workflow 冲突？
- 是否可以删掉对执行没有帮助的段落？

## Metadata

`agents/openai.yaml` 至少包含：

```yaml
interface:
  display_name: "Human Name"
  short_description: "25-64 chars"
  default_prompt: "使用 $skill-name ..."
```

更新 `SKILL.md` 后检查 metadata 是否仍匹配当前 skill。

## 验证

- 对每个 skill 运行结构验证工具；没有统一工具时，至少检查 `SKILL.md` frontmatter、目录名、name 一致性和 metadata 存在。
- 确认 `Language Contract` 标记存在，且输出模板的核心 heading 中文优先、English 括注。
- 运行文本搜索确认没有脚手架残留、未完成标记或乱码。
- 对新流程 skill，至少人工执行一次 pressure scenario walkthrough。
- 如果使用 subagent forward-test，只给 subagent skill 路径和用户式请求，不泄露预期答案。

## 完成标准

- Skill 可被触发、可被执行、可被验证。
- 没有未解释的未完成标记或模板残留。
- 已报告 pressure scenarios、验证方式、未做 forward-test 的原因。
