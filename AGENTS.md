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
- 新增或修改 skill 时，明确 pressure scenarios、trigger description、metadata 和验证方式。
- 仓库级工作流按任务类型直接选择最小必要 skill；spec、plan、analysis、implementation、review、verification 和 branch finish 应保持可追溯。
- workflow skill 之间使用 `Natural Handoff`：完成后最多推荐一个 next skill；`继续`、`可以`、`按你说的办`、`go ahead`、`ok` 和 `好的` 只确认上一条回复中唯一推荐的 next skill。
- 如果上一条给了多个选项，或用户确认时附加新条件、改变方向，必须重新路由；自然确认不能绕过目标 skill 的 branch、scope、verification、review、commit、push 或修改计划确认。
- 设计确认后需要 implementation plan 时，`brainstorming` 唯一推荐 `$to-plan`；自然确认或显式调用创建一次 Planning Authorization，只批准本地 planning artifacts 和机械修复。
- `$to-plan` 按风险选择 Fast Path 或 Full Path：Fast 只写自包含 `plan.md`，Full 在同一次 Planning Run 内写共享 `FR-###` 的 `spec.md + plan.md`，两者都不默认生成 `analysis.md`。
- 独立 `$to-spec` 只处理 formal spec / decision artifact；独立 `$analyze` 只读审查已有、外部、失效或未检查 artifacts，不把两者恢复成固定 planning 中间阶段。
- `clarify` 只回答问题和解释代码证据，不推荐后续 skill。
- `brainstorming` 不直接写业务代码，并按已确认 outcome 路由到 `$to-plan`、`$to-spec` 或 `none`。
- `grill-me` 和 `diagnose` 不直接写业务代码；repair-ready diagnosis 唯一推荐 `$implement`，由它内部选择 Quick/Standard/Blocked。
- `$implement` 是唯一 implementation entry；写入前选择 Quick/Standard/Blocked，Quick 必须保留 scope、acceptance、verification，风险扩大但授权边界不变时在同一 skill 内升级 Standard。
- `$implement` 在写入前使用 `checking-branch` 展示当前分支名和状态；用户不同意直接修改但提供新分支名时，默认从仓库主分支创建，无法确认主分支时需再确认是否从当前分支创建。
- `Planning Quality Status: Pass` 的 checked plan 可直接进入 `$implement` 的内部 branch gate；缺少该状态、存在未处理 finding 或来自 external artifacts 时仍先进入 `$implement` Standard，再由内部 N3 Analyze Gate 使用只读 `$analyze`，不在 implementation entry 前另行路由。
- 非平凡 feature 或 bug fix 仍必须保留 `checking-branch -> requesting-code-review -> verification-before-completion`；adaptive planning 不授权实现、branch、commit、push、PR、merge、discard 或远端操作。
- 完成前运行 `python scripts/validate-skills.py`，并修复 frontmatter、metadata、TODO、乱码和名称不一致问题。
