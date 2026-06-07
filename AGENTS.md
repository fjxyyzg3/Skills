# AGENTS.md

## 仓库定位

这是 lihuanyu 个人的 Codex skill 仓库，用于沉淀、维护和迭代可复用的 skills。

## Skill 开发原则

- 主要语言使用中文。
- Skill 结构要求、文件名、目录名、YAML frontmatter key、配置字段、命令、代码、API 名称、英文专业术语和英文专有名词保留英文。
- 编写 `SKILL.md` 时，正文说明优先使用中文；当中文会降低准确性或触发识别效果时，保留必要的 English trigger phrases。
- 新增或修改 skill 时，保持结构精简，只加入对 agent 执行任务有直接帮助的内容。
- 新增或修改 skill 时，先参考 `writing-skills`，明确 pressure scenarios、trigger description、metadata 和验证方式。
- 仓库级工作流以 `using-skills` 为入口；PRD、issues、analysis、implementation、review、verification 和 branch finish 应保持可追溯。
- 非平凡 feature work 默认经过 `to-prd -> to-issues -> analyze -> using-worktrees -> implement -> requesting-code-review -> verification-before-completion`。
- 完成前运行 `python scripts/validate-skills.py`，并修复 frontmatter、metadata、TODO、乱码和名称不一致问题。
