# Document Targets

用这份参考选择沉淀内容的受众层级、目标文件和跨文档影响。目标是让每个事实只有一个权威落点，避免 README、AGENTS、docs 和 memory 互相复制。

## 受众层级

| 层级 | 典型位置 | 受众 | 适合内容 |
| --- | --- | --- | --- |
| Agent 记忆 | `MEMORY.md`、`PROJECT_MEMORY.md`、agent 支持的记忆目录 | 跨会话 agent | 用户偏好、非显而易见的项目事实、可复用踩坑 |
| 项目规则 | `AGENTS.md`、`CLAUDE.md`、`CONTEXT.md` | 当前项目里的 AI | 硬边界、禁止事项、命令速查、架构红线、协作流程 |
| 项目文档 | `README.md`、`docs/**/*.md`、runbook、integration guide、ADR | 人类同事、下游开发者、未来接手的 AI | 接入指南、架构说明、运维步骤、API/环境变量/术语表 |

## 目标文件规则

- `AGENTS.md` / `CLAUDE.md` 是规则手册，不是变更日志；不要写“某日某功能上线”这类历史叙事。
- `README.md` 说明项目入口、安装、运行、验证和最短使用路径；不要塞入只有 agent 需要的偏好。
- `docs/` 面向第一次接触项目的人，写“怎么用、怎么工作、怎么运维”。
- ADR / decision 文档保存仍会影响未来选择的决策；不要把临时计划伪装成 ADR。
- 记忆文件只放跨会话会再次影响判断的信息；单次事故流水账通常不该沉淀。

## 候选文档扫描

按需检查这些落点，不要批量读取或重写全部文档：

- 项目根：`README.md`、`AGENTS.md`、`CLAUDE.md`、`CONTEXT.md`、`MEMORY.md`、`PROJECT_MEMORY.md`。
- 文档目录：`docs/**/*.md`、`adr/**/*.md`、`decisions/**/*.md`、runbook、integration guide、architecture 文档。
- 配套 metadata：如果目标仓库有 skill、plugin、agent 或 template metadata，同步检查是否需要最小更新。

## 影响矩阵

- 新增 API / 路由：检查项目规则、integration guide、architecture 是否需要同步。
- 新增环境变量：检查项目规则、README/runbook、部署说明是否需要同步。
- 新增数据库表或领域模型：检查 architecture、Data Model、项目规则是否需要同步。
- 新增跨项目能力：检查上下游项目文档是否都需要同步。
- 完成或推翻旧计划：检查记忆和文档中是否要删除或改写旧事实。
- 迁移 workflow 或工具命令：检查 README、runbook、AGENTS/CLAUDE 和已有脚本注释是否存在冲突。

