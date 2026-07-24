# Curation Quality

用这份参考判断内容是否值得沉淀，以及最终编辑是否减少文档腐烂而不是制造新负担。

## Durable 候选

可考虑沉淀：

- 稳定项目约定、反复出现的 workflow、长期有效的验证命令。
- 非显而易见的项目结构知识、跨仓库边界、工具入口和常见踩坑。
- 已验证的 architecture/domain decision、术语定义、用户明确偏好的项目级规则。
- 会影响未来 agent 判断的分支、提交、发布、测试或安全边界。

默认跳过：

- 一次性过程、临时调试步骤、未验证猜测、过期计划、聊天寒暄。
- 完整对话转录、大段日志、没有复用价值的中间输出。
- 隐私信息、secrets、tokens、passwords、内部凭据或可能泄露身份/权限的信息。
- 只有相对时间的事实，例如 `今天`、`昨天`、`最近`、`today`、`recently`，除非改成绝对日期。

## Wiki 质量门

- 每次 `session-curator` invocation 都执行一次 `Wiki Check`，但 `not-applicable`、`no-change`、`candidate` 和 `blocked` 都不产生 wiki 写入。
- wiki 只接收已经确认、跨任务或跨会话仍有价值的稳定知识；临时计划、一次性步骤、未确认猜测和完整 session 默认跳过。
- 初次扫描只读取 wiki 路径和 Markdown 第一行摘要；确认 candidate 后才读取目标页面全文和必要来源全文。
- 默认 transfer mode 是 `summary` 或 `split`；`full` 必须显式确认，且原始来源默认保留并记录来源路径。
- 新增页面必须有第一行摘要和标题；新增 topic 必须有同名说明页并同步根索引，新增 page 必须同步 topic 索引，名称使用 lowercase kebab-case。触碰既有非默认布局时沿用实际 root/index/topic convention，只校验必要的摘要、标题、来源和索引关系，不强制迁移。
- 多候选、unknown target、identity conflict、owner ambiguity 或 dirty overlap 必须 fail closed；不得创建 `-2`、`-new`、`-final` sibling 页面绕过冲突。
- 历史页面不因 profile 首次启用而自动迁移；不引入 `source-manifest.json`、watcher、自动刷新、全仓库默认扫描或强制 raw-source directory。

## 腐烂和膨胀检查

- 如果目标 section 已经存在同义内容，优先更新旧条目，不追加新条目。
- 如果旧内容被新事实取代，直接改写或删除旧事实，不保留历史包袱。
- 如果项目规则文件已过长，优先迁移详细教程到 docs，只保留硬边界和入口链接。
- 如果 docs 已有详细机制，不要把机制复制到 AGENTS/CLAUDE；规则文件只放 agent 需要遵守的结论。
- 如果没有单一权威落点，先在计划里说明候选落点和取舍，让用户决定。

## 最终自检

- `AGENTS.md` / `CLAUDE.md` 没新增历史叙事或变更日志式段落。
- README 的安装、运行、验证命令与当前代码一致。
- 文档中提到的路径、命令、环境变量、API 和工具真实存在，或明确标注为计划项。
- 记忆内容没有互相矛盾，索引链接指向存在文件。
- 没有遗留 `今天`、`昨天`、`最近`、`today`、`recently` 等相对时间。
- 跨项目影响已经检查上下游文档，或在报告中说明不适用。
- Wiki candidate 已进入统一修改计划，包含 target、operation、source、transfer mode、精确 file/section 和 risk；未确认项没有产生 filesystem mutation。
- wiki owner/root 在首次 mutation 前已经明确，跨 Git owner 的写入和最终 status 按 owner 报告。
- 修改计划中每个 ID 都能映射到实际 diff；未批准的候选没有被写入文件。
