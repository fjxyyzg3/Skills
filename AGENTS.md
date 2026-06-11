# AGENTS.md

## 仓库定位

这是 lihuanyu 个人的 Codex skill 仓库，用于沉淀、维护和迭代可复用的 skills。

## Skill 开发原则

- 主要语言使用中文。
- Skill 结构要求、文件名、目录名、YAML frontmatter key、配置字段、命令、代码、API 名称、英文专业术语和英文专有名词保留英文。
- 编写 `SKILL.md` 时，正文说明优先使用中文；当中文会降低准确性或触发识别效果时，保留必要的 English trigger phrases。
- Skill 生成的 Markdown/HTML 文档、分析结论、review、handoff、完成报告和聊天式输出默认中文为主；代码、命令、API 名称、contract fields、稳定 ID、英文专有名词和必要技术术语保留 English。
- 用户明确要求英文，或目标项目已有英文 artifact 规范时可以例外，但必须在 metadata、assumptions 或完成报告中记录原因。
- 产出型 skill 必须包含统一 `Language Contract` 标记，便于 validator 做轻量检查；核心 section heading 使用中文优先、English 括注。
- 新增或修改 skill 时，保持结构精简，只加入对 agent 执行任务有直接帮助的内容。
- 新增或修改 skill 时，先参考 `writing-skills`，明确 pressure scenarios、trigger description、metadata 和验证方式。
- 仓库级工作流按任务类型直接选择最小必要 skill；PRD、issues、analysis、implementation、review、verification 和 branch finish 应保持可追溯。
- `session-curator`、`diagnose`、`diagnose-ue`、`implement`、`quick-change`、`to-prd` 和 `to-issues` 只由用户手动调用；可建议用户显式使用 `$skill-name`，但不要按任务类型自动触发。
- 用户显式调用 `$quick-change` 处理小型 bug 和小需求时，必须保留 scope、acceptance、verification，并在风险扩大时升级到完整链路。
- 实现前使用 `checking-branch` 展示当前分支名和状态；用户不同意直接修改但提供新分支名时，默认从仓库主分支创建，无法确认主分支时需再确认是否从当前分支创建。
- 非平凡 feature work 如果已有 PRD/issues/plan artifacts，默认经过 `analyze -> checking-branch -> requesting-code-review -> verification-before-completion`；需要生成 PRD 或 issues 时，只能建议用户显式调用 `$to-prd` 或 `$to-issues`。
- 完成前运行 `python scripts/validate-skills.py`，并修复 frontmatter、metadata、TODO、乱码和名称不一致问题。
