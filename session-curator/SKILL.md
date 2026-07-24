---
name: session-curator
description: "当会话接近结束，或用户要求整理持久项目知识、协调文档与记忆、维护 wiki/知识库、减少文档腐烂/膨胀，或在确认具体修改计划后更新 README.md、AGENTS.md、CLAUDE.md、docs、CONTEXT/MEMORY 或项目 memory 时使用；保留英文触发短语 near session end、curate durable project knowledge、reconcile docs and memory、wiki/knowledge-base curation 和 documentation rot/bloat。"
version: 0.1.0
---

# Session Curator

像知识库编辑一样从当前会话中提炼可复用、长期有效、可验证的项目知识，审查文档、记忆和 wiki 是否过期、膨胀或冲突，并在用户确认修改计划后更新项目文档、wiki 或记忆文档。wiki 是本 skill 的受约束 profile，不是并列的顶层 skill 或第二个 durable writer。

## 进入边界

使用本 skill 的前提是用户明确要求整理会话、沉淀记忆、更新项目文档、修正文档腐烂，或上一轮唯一 `Natural Handoff` 推荐本 skill 且用户确认。会话接近结束、完成实现或看到可整理内容都不是静默写文档的授权。

适用：

- 从当前会话或指定材料中提炼长期有效的 workflow、项目约定、验证命令、架构决策、术语或用户偏好。
- 检查并修正 README、AGENTS、CLAUDE、docs、CONTEXT/MEMORY 或项目记忆里的过期、重复、冲突和膨胀。
- 检查或维护已有 wiki/知识库，或把已确认的稳定知识按 wiki profile 的匹配、索引和来源规则整理进去。
- 在用户批准具体计划后同步项目文档、agent 规则或记忆文件。

不适用：

- 只需要跨会话交接给下一位 agent 时，使用 `$handoff`。
- 只需要回答问题、解释代码或总结当前结果时，不写持久文档。
- 用户没有确认修改计划时，不进入文件编辑阶段。

## 压力场景（Pressure Scenarios）

1. 用户说：“把这次会话里值得长期保留的东西整理一下。”
   - 预期 skill 触发：先区分可沉淀内容和一次性过程，再给修改计划。
   - 未使用本 skill 时的常见失败：把完整聊天摘要、临时调试过程或过期计划写进项目文档。
   - 本 skill 必须强制的行为：只保留长期有效、可复用、可验证的信息。
2. 用户说：“这个规则以后都要记住，写到 AGENTS 或 memory。”
   - 预期 skill 触发：先判断受众层级和已有落点，再计划最小 diff。
   - 未使用本 skill 时的常见失败：同一事实同时塞进 README、AGENTS 和 memory，制造重复来源。
   - 本 skill 必须强制的行为：选择单一权威落点；能更新旧条目就不追加新条目。
3. 用户说：“文档有点乱，帮我收一收。”
   - 预期 skill 触发：做尺寸和腐烂体检，优先精简、合并或删除过期内容。
   - 未使用本 skill 时的常见失败：继续追加新 section，让文档更臃肿。
   - 本 skill 必须强制的行为：减优于加；无法证明长期价值时报告无需修改。
4. 用户说：“把这次稳定结论整理到 wiki。”
   - 预期 skill 触发：先在当前 scope 内执行 `Wiki Check`，解析 wiki owner/root，提出精确候选，再等待统一修改计划确认。
   - 未使用本 skill 时的常见失败：直接创建 generic wiki、复制整份 session 或把 wiki 当成当前代码仓库的默认落点。
   - 本 skill 必须强制的行为：默认摘要/整理转入，保留来源，维护索引，并在歧义或 dirty overlap 时 fail closed。
5. 用户只要求普通的 memory 或 docs 整理，但当前项目已有 wiki。
   - 预期 skill 触发：仍输出一次 `Wiki Check`，但不因为 wiki 存在而静默改变 authoritative target。
   - 未使用本 skill 时的常见失败：把所有 durable 内容重复写进 wiki，或为完成检查而全文扫描全仓库。
   - 本 skill 必须强制的行为：复用当前 scope，只做路径和摘要级 wiki inventory；没有候选时明确输出 `no-change` 或 `not-applicable`。

## 核心规则

- 修改任何文件前，必须先列出具体修改计划并等待用户确认。
- 只沉淀通用部分：稳定约定、重复出现的 workflow、项目结构知识、验证命令、长期决策、术语、用户明确偏好的项目级规则。
- 不沉淀一次性过程、临时调试细节、过期计划、聊天寒暄、未验证猜测、隐私信息、secrets、tokens、passwords 或完整对话转录。
- 优先更新已有文档和已有 section；只有用户确认且没有合适落点时才创建新记忆文档。
- 保留项目既有写作风格、语言约定和 heading 层级；不要把文档改成另一套体系。
- 减优于加，合并优于追加，删除过期内容优于保留历史包袱。
- 如果没有值得沉淀的通用内容，明确报告“无需修改”，不要为了产出而改文档。
- 每次 `session-curator` invocation 都必须输出一次 `Wiki Check`，状态只能是 `not-applicable`、`no-change`、`candidate`、`resolved` 或 `blocked`；检查不等于写入。
- `Wiki Check` 复用当前 `session-curator` scope，默认只读取 wiki 路径和 Markdown 第一行摘要；不得因为默认检查而全文扫描全仓库、历史 session 或 raw source directory。
- wiki root/owner 按“用户显式路径 > 项目 convention > 唯一既有 wiki root > 阻塞”解析；没有 root 时只能提出创建 candidate，不能静默创建 generic wiki。
- wiki candidate 必须进入同一份修改计划，明确 `target`、`operation`、`source`、`transfer mode`、精确 `file/section` 和 `risk`；未确认或存在歧义时零写入。
- wiki 文件写入只授权文档内容和必要索引落盘，不授权 stage、commit、push、PR、merge、gitlink update、discard 或其他 Git/remote action。

## 参考资料

- 选择文档受众、候选文件和跨文档影响时，使用 `references/document-targets.md`。
- 过滤沉淀内容、检查文档腐烂、控制膨胀和敏感信息时，使用 `references/curation-quality.md`。
- 进行每次 `Wiki Check`、解析 wiki owner/root、匹配页面、选择 transfer mode 和执行 fail-closed 判断时，使用 `references/wiki-profile.md`。

## 工作流程

1. 明确整理范围。
   - 默认范围是当前对话。
   - 如果用户指定了某段会话、某些文件或某个主题，只整理指定范围。
   - 在盘点候选文档前，按 `references/wiki-profile.md` 执行一次 `Wiki Check`，先记录 scope、root/owner basis 和状态；不要把检查结果当成写入授权。

2. 盘点候选文档。
   - 先列目录再判断：项目根、`docs/`、根目录 Markdown、ADR/decision 目录、项目已有记忆文件。
   - 按 `references/document-targets.md` 选择候选文件和受众层级。
   - 只读取和候选内容相关的文档；不要批量重写所有文档，也不要漏掉明显受影响的文档。
   - 如果项目有 git，先记录 `git status --short`，避免覆盖用户已有改动。
   - 做尺寸体检：如果项目规则或记忆文件已接近臃肿，计划优先精简、迁移或合并，再考虑新增内容。

3. 提炼候选内容。
   - 将会话内容分类为 `workflow`、`project convention`、`architecture/domain decision`、`setup/verification`、`terminology`、`user preference` 或 `skip`。
   - 对每个可沉淀候选写明来源依据、适用范围、目标读者和为什么它不是一次性信息。
   - 按 `references/curation-quality.md` 对不沉淀内容写 skip 原因，特别是敏感信息、临时实验、未确认决策和相对时间。
   - 用 `references/document-targets.md` 的影响矩阵检查是否需要同步上下游文档，或是否应只更新一个权威落点。

4. 输出修改计划并停止等待确认。
   - 不要在确认前调用编辑工具。
   - 如果计划包含多个文件，允许用户选择部分执行。
   - 如果用户修改计划，先复述新的批准范围再编辑。
   - 如果 `Wiki Check` 为 `candidate`，把 wiki candidate 作为独立 plan item，列出 target、operation、source、transfer mode、精确 file/section 和 risk；不要再追加一轮重复的 wiki confirmation。
   - 如果 `Wiki Check` 为 `blocked`，只提出一个合并后的阻塞问题；在 owner、identity、匹配或 dirty overlap 收束前不得写入 wiki。

5. 执行已确认的修改。
   - 只修改用户批准的文件、section 和内容类型。
   - 使用最小 diff；不要顺手整理无关段落。
   - 优先顺序：先更新面向外部读者的 `docs/` / `README.md`，再更新 `AGENTS.md` / `CLAUDE.md`，最后整理记忆。
   - 新信息更新旧条目时直接改旧条目；新增条目前先搜索同义内容，能合并就不追加。
   - 删除已完成临时计划、被新版本取代的事实、重复记忆和相对时间表达。
   - wiki 只有在精确 plan item 被确认后才从 `candidate` 进入 `resolved`；首次 mutation 前报告 owner 和绝对路径。
   - 新增 wiki 文件或目录必须遵守摘要、标题、topic 同名说明页、根/目录索引和 lowercase kebab-case 规则；触碰既有非默认布局时沿用已解析的 root/index/topic convention，不强制改名、补建平行默认结构或迁移历史页面。
   - 如果编辑过程中发现新风险或需要新增文件，停止并重新确认。

6. 验证和报告。
   - 运行项目已有的文档或 skill validator；没有专用验证时至少运行 `git diff --check` 并检查 links/headings/metadata。
   - 按 `references/curation-quality.md` 做最终自检。
   - 汇总实际修改、验证命令、`Wiki Check` 状态和理由、per-owner status、跳过项和残留风险。

## 修改计划格式

```markdown
## 会话整理计划

- Scope:
- Candidate docs checked:
- Recommendation: edit / no changes / needs user decision
- Size/bloat check:
- Wiki Check: `<status>`；scope/root/owner basis 与理由

| ID | Candidate | Audience layer | Target file/section | Change type | Why durable | Risk |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | ... | agent rules / docs / memory | ... | add/update/remove | ... | ... |

### Wiki 候选（仅在存在时）

| ID | Target owner/root | Target | Operation | Source | Transfer mode | Exact file/section | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| W1 | ... | ... | add/update/split | ... | summary / split / full | ... | ... |

## 不沉淀内容

- ...

请确认要执行的 ID；确认前我不会修改文件。
```

## 完成报告格式

```markdown
## 会话整理结果

- Approved scope:
- Changed:
- Verified:
- Wiki Check:
- Per-owner status:
- Skipped:
- Residual risk:
```

## 完成标准

- 用户明确调用了本 skill，或通过上一轮唯一 `Natural Handoff` 推荐后确认进入。
- 文件修改前已给出修改计划，并收到用户确认。
- 已输出一次合法的 `Wiki Check`，并说明 scope、root/owner basis、状态和理由。
- 只写入长期有效、可复用、可验证的项目知识。
- 已区分 agent 记忆、项目规则和项目文档的不同受众。
- 已优先处理过期、重复、膨胀和相对时间问题。
- 没有泄露敏感信息或转录完整对话。
- 未确认的 `candidate`、`blocked` 或不唯一 target 没有产生 wiki filesystem mutation。
- 修改范围与用户批准范围一致。
- 已运行可用验证，或说明跳过原因。
