---
name: session-curator
description: Use near the end of a conversation/session to extract durable project knowledge, reconcile docs and memory, prevent documentation rot and bloat, and after presenting a proposed edit plan for confirmation, update README.md, AGENTS.md, CLAUDE.md, docs, CONTEXT/MEMORY, or other project memory artifacts.
---

# Session Curator

像知识库编辑一样从当前会话中提炼可复用、长期有效、可验证的项目知识，审查文档与记忆是否过期、膨胀或冲突，并在用户确认修改计划后更新项目文档或记忆文档。

## Language Contract

语言契约：生成的文档和聊天输出默认以中文优先；代码、命令、API 名称、契约字段、ID、专有名词以及必要的技术术语保留英文。用户或目标项目明确要求英文时可以例外，但必须记录原因。

## 核心规则

- 可以由用户显式调用，也可以由 `workflow-router` 或上一轮 `Natural Handoff` 推荐后进入；不要因为会话接近结束、完成实现或看到可整理内容就静默修改文档。
- 修改任何文件前，必须先列出具体修改计划并等待用户确认。
- 只沉淀通用部分：稳定约定、重复出现的 workflow、项目结构知识、验证命令、长期决策、术语、用户明确偏好的项目级规则。
- 不沉淀一次性过程、临时调试细节、过期计划、聊天寒暄、未验证猜测、隐私信息、secrets、tokens、passwords 或完整对话转录。
- 优先更新已有文档和已有 section；只有用户确认且没有合适落点时才创建新记忆文档。
- 保留项目既有写作风格、语言约定和 heading 层级；不要把文档改成另一套体系。
- 减优于加，合并优于追加，删除过期内容优于保留历史包袱。
- 如果没有值得沉淀的通用内容，明确报告“无需修改”，不要为了产出而改文档。

## 知识分层

先按受众决定落点，避免把同一事实重复塞进所有文件：

| 层级 | 典型位置 | 受众 | 适合内容 |
| --- | --- | --- | --- |
| Agent 记忆 | `MEMORY.md`、`PROJECT_MEMORY.md`、agent 支持的记忆目录 | 跨会话 agent | 用户偏好、非显而易见的项目事实、可复用踩坑 |
| 项目规则 | `AGENTS.md`、`CLAUDE.md`、`CONTEXT.md` | 当前项目里的 AI | 硬边界、禁止事项、命令速查、架构红线、协作流程 |
| 项目文档 | `README.md`、`docs/**/*.md`、runbook、integration guide、ADR | 人类同事、下游开发者、未来接手的 AI | 接入指南、架构说明、运维步骤、API/环境变量/术语表 |

判断规则：

- `AGENTS.md` / `CLAUDE.md` 是规则手册，不是变更日志；不要写“某日某功能上线”这类历史叙事。
- `docs/` 面向第一次接触项目的人，写“怎么用、怎么工作、怎么运维”。
- 记忆文件只放跨会话会再次影响判断的信息；单次事故流水账通常不该沉淀。

## 工作流程

1. 明确整理范围。
   - 默认范围是当前对话。
   - 如果用户指定了某段会话、某些文件或某个主题，只整理指定范围。

2. 盘点候选文档。
   - 先列目录再判断：项目根、`docs/`、根目录 Markdown、ADR/decision 目录、项目已有记忆文件。
   - 查找 `README.md`、`AGENTS.md`、`CLAUDE.md`、`CONTEXT.md`、`MEMORY.md`、`PROJECT_MEMORY.md`、`docs/**/*.md`、runbook、integration guide、architecture 文档。
   - 只读取和候选内容相关的文档；不要批量重写所有文档，也不要漏掉明显受影响的文档。
   - 如果项目有 git，先记录 `git status --short`，避免覆盖用户已有改动。
   - 做尺寸体检：如果 `AGENTS.md` / `CLAUDE.md` 已接近臃肿，计划优先精简、迁移或合并，再考虑新增内容。

3. 提炼候选内容。
   - 将会话内容分类为 `workflow`、`project convention`、`architecture/domain decision`、`setup/verification`、`terminology`、`user preference` 或 `skip`。
   - 对每个可沉淀候选写明来源依据、适用范围、目标读者和为什么它不是一次性信息。
   - 对不沉淀内容写简短 skip 原因，特别是敏感信息、临时实验和未确认决策。
   - 用变更影响矩阵思考落点：
     - 新增 API / 路由：检查项目规则、integration guide、architecture 是否需要同步。
     - 新增环境变量：检查项目规则、README/runbook、部署说明是否需要同步。
     - 新增数据库表或领域模型：检查 architecture、Data Model、项目规则是否需要同步。
     - 新增跨项目能力：检查上下游项目文档是否都需要同步。
     - 完成或推翻旧计划：检查记忆和文档中是否要删除或改写旧事实。

4. 输出修改计划并停止等待确认。
   - 不要在确认前调用编辑工具。
   - 如果计划包含多个文件，允许用户选择部分执行。
   - 如果用户修改计划，先复述新的批准范围再编辑。

5. 执行已确认的修改。
   - 只修改用户批准的文件、section 和内容类型。
   - 使用最小 diff；不要顺手整理无关段落。
   - 优先顺序：先更新面向外部读者的 `docs/` / `README.md`，再更新 `AGENTS.md` / `CLAUDE.md`，最后整理记忆。
   - 新信息更新旧条目时直接改旧条目；新增条目前先搜索同义内容，能合并就不追加。
   - 删除已完成临时计划、被新版本取代的事实、重复记忆和相对时间表达。
   - 如果编辑过程中发现新风险或需要新增文件，停止并重新确认。

6. 验证和报告。
   - 运行项目已有的文档或 skill validator；没有专用验证时至少运行 `git diff --check` 并检查 links/headings/metadata。
   - 汇总实际修改、验证命令、跳过项和残留风险。

## 修改计划格式 (Curation Plan)

```markdown
## 会话整理计划 (Session Curation Plan)

- Scope:
- Candidate docs checked:
- Recommendation: edit / no changes / needs user decision
- Size/bloat check:

| ID | Candidate | Audience layer | Target file/section | Change type | Why durable | Risk |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | ... | agent rules / docs / memory | ... | add/update/remove | ... | ... |

## 不沉淀内容 (Skipped)

- ...

请确认要执行的 ID；确认前我不会修改文件。
```

## 完成报告格式

```markdown
## 会话整理结果 (Session Curation Result)

- Approved scope:
- Changed:
- Verified:
- Skipped:
- Residual risk:
```

## 完成标准

- 用户明确调用了本 skill。
- 文件修改前已给出修改计划，并收到用户确认。
- 只写入长期有效、可复用、可验证的项目知识。
- 已区分 agent 记忆、项目规则和项目文档的不同受众。
- 已优先处理过期、重复、膨胀和相对时间问题。
- 没有泄露敏感信息或转录完整对话。
- 修改范围与用户批准范围一致。
- 已运行可用验证，或说明跳过原因。

## 自检清单

- `AGENTS.md` / `CLAUDE.md` 没新增历史叙事或变更日志式段落。
- 没把 `docs/` 已有详细机制复制到项目规则文件。
- README 的安装、运行、验证命令与当前代码一致。
- 文档中提到的路径、命令、环境变量、API 和工具真实存在或明确标注为计划项。
- 记忆内容没有互相矛盾，索引链接指向存在文件。
- 没有遗留 `今天`、`昨天`、`最近`、`today`、`recently` 等相对时间。
- 跨项目影响已经检查上下游文档，或在报告中说明不适用。
