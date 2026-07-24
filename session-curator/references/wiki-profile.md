# Wiki Profile

## 定位

wiki profile 是 `session-curator` 的受约束工作模式，不是独立顶层 skill，也不新增第二个 durable writer。它把当前 `session-curator` scope 中已经确认、跨任务或跨会话仍有价值的稳定知识整理到已有 wiki；普通 docs、README、AGENTS 或 memory 的 authoritative target 仍由其他文档规则决定。

每次 `session-curator` invocation 都必须执行一次轻量级 `Wiki Check`。检查可以得出“不适用”或“无需变化”，不代表每次都要创建或修改 wiki。

## Wiki Check 状态

`Wiki Check` 只能使用以下状态：

| Status | 含义 | 允许的 filesystem mutation |
| --- | --- | --- |
| `not-applicable` | 当前 scope 没有适合 wiki 的稳定知识，或没有 wiki authority 且本次不需要提出创建候选 | 无 |
| `no-change` | 已找到明确 wiki authority/root，但当前 scope 没有新增、更新或迁移必要 | 无 |
| `candidate` | 发现可能进入 wiki 的稳定知识，但 target、operation、source 或 transfer mode 尚未被统一修改计划确认 | 无 |
| `resolved` | 精确 target、operation、source、transfer mode、file/section 和 scope 已被用户确认 | 只允许已确认的最小写入 |
| `blocked` | owner、root、identity、匹配、dirty overlap、权限或其他安全条件未收束 | 无 |

最终报告必须同时说明 `Wiki Check` status、当前 scope、root/owner basis、判断理由和 per-owner status。`candidate`、`blocked` 或不唯一 target 不得写入任何 wiki 文件。

## Scope 与读取深度

1. 默认 scope 是当前 `session-curator` scope：当前会话、用户指定来源和已批准的 workflow artifacts。
2. wiki 检查只做轻量 inventory：先读取 root 下的路径、目录关系和每个 Markdown 文件的第一行摘要。
3. 只有 candidate 已进入统一修改计划并被确认后，才读取目标页面全文和必要来源全文。
4. 除非用户明确扩大 scope，不得全文扫描全仓库、历史 session、raw source directory 或无关文档。
5. 初次启用 profile 不得为了修复旧格式而批量读取、迁移或重命名历史页面。

## Root 与 owner 解析

按以下优先级解析 wiki root 和 `TargetOwnerRoot`：

1. 用户明确指定的 repo、目录或文件路径；
2. 项目 `AGENTS.md`、`CLAUDE.md` 或其他 active project convention；
3. 当前 workspace 中唯一且 identity 明确的既有 wiki root；
4. 仍无法唯一确定时进入 `blocked`，只提出一个合并后的 owner/path blocking question。

没有既有 wiki root 时，可以在统一修改计划中提出项目 convention 指定的创建候选，例如 `docs/wiki/`，但在用户确认精确 root、结构和 plan item 前只能保持 `candidate`，不得创建目录、索引、topic 或页面。

如果 docs owner 是独立 Git repo 或 nested repo，wiki 只写入 docs owner。当前 process cwd、外层 workspace 或代码 repo 不能单独决定 wiki owner。首次 filesystem mutation 前必须报告 owner repo 和绝对路径；完成后按 owner 报告 status。

## 可发现性与页面结构

`docs/wiki/wiki.md`、`<topic>/<topic>.md` 和 lowercase kebab-case 是 v1 新建 root/topic/page 的默认模板，不是对所有既有 wiki 的强制迁移目标。已有 wiki 先按已解析的 project convention、root index、topic index 和页面摘要发现实际布局；只有能唯一映射 target、owner 和索引关系时才继续。

```text
docs/wiki/
  wiki.md
  <topic>/
    <topic>.md
    <page>.md
```

- 根索引 `wiki.md` 描述 wiki 范围并索引顶层 topic。
- 每个 topic 目录必须有与目录同名的说明页。
- 每个新增或本次触碰的页面第一行必须是摘要，随后必须有标题。
- 新增 topic 时同步更新根索引；新增页面时同步更新 topic 说明页。
- 新增目录和文件名使用 lowercase kebab-case。
- 页面正文按主题组织，不要求把所有来源强行套进固定章节。

### 既有非默认布局

对已有非默认布局：

- 先记录实际 root、root index、topic index 和页面摘要；不要因为文件名不是 `wiki.md` 或 topic 不是同名页就自动重命名。
- 既有 root 可能使用 `index.md` 或项目 convention 指定的其他 index 文件名。
- 新增或触碰的页面仍必须满足摘要、标题、来源和可发现性要求；必要的索引更新应使用已有 convention。
- 如果 root index、topic identity、owner 或页面关系无法唯一映射，进入 `blocked`，不要创建平行默认布局。

既有不符合上述规则的历史页面不因 profile 首次启用而自动批量迁移。只有用户明确扩大到 migration scope 时，才能另行建立迁移计划。

## Candidate 与统一修改计划

发现稳定知识后，必须把 wiki candidate 作为 `session-curator` 统一修改计划中的独立 item，至少包含：

| Field | 要求 |
| --- | --- |
| `TargetOwnerRoot` | 目标 owner repo 和 wiki root |
| `Target` | 唯一页面、topic 或待创建的 root/topic/page |
| `Operation` | `add`、`update` 或 `split` |
| `Source` | 当前会话、spec、plan、handoff 或用户指定来源的路径/标识 |
| `TransferMode` | `summary`、`split` 或经显式确认的 `full` |
| `ExactFileSection` | 精确文件和 section，不能只写“更新 wiki” |
| `Risk` | identity、owner、dirty overlap、索引或来源保留风险 |

`candidate` 只表示“发现候选”，不表示已经授权。用户确认精确 plan item 后，状态才可进入 `resolved`；同一 item 不再要求重复的 wiki 二次确认。执行期间出现新的 target、source mapping、目录关系或 scope，必须停止并重新确认。

## 内容判断与 transfer mode

默认只进入跨任务、跨会话仍有价值且已经确认的稳定知识：

- 架构、模块职责、术语、项目约定、稳定流程、常见问题和已确认决策背景；
- 能改变未来 agent 判断的长期验证规则、owner 边界或安全约束。

以下内容默认跳过：

- 未确认猜测、临时状态、一次性执行步骤、完整聊天转录、未批准方案和敏感信息；
- 仍会快速过期的工作树状态、相对时间表达或仅用于当前任务的 checklist。

从 `spec`、`plan`、`handoff`、session 或其他文档转入时：

- 默认使用摘要/整理转入；
- 一个来源跨多个主题时优先提出拆分转入；
- 全文转入必须作为 `full` transfer mode 被显式确认；
- wiki 页面记录来源路径或链接；
- 原始来源默认保留，不移动、删除或覆盖。

## Matching 与 fail-closed

只有唯一且范围明确的 target 才能继续。以下任一情况都必须进入 `blocked` 并保持零写入：

- 多个候选页面或 topic；
- unknown target、identity conflict 或 topic scope conflict；
- 目标文件存在与本任务无关的 dirty edit；
- owner 或 root 不唯一；
- operation、transfer mode、source 或授权范围不明确。

不得把内容塞进“差不多相关”的页面，也不得通过 `-2`、`-new`、`-final` 或同义后缀创建 sibling 页面规避冲突。阻塞时只提出一个合并后的问题，不猜测、不覆盖、不自动合并。

## Git 与交付边界

wiki filesystem mutation 只授权已确认的文档内容和必要索引落盘。它不授权：

- stage、commit、push、PR、merge、parent gitlink update 或 discard；
- 自动刷新、background watcher、hash-based ingestion 或远端 wiki service；
- 新增 `source-manifest.json`、强制 raw-source directory 或全仓库默认 source ingestion。

Git delivery、branch lifecycle 和其他 repo owner 的后续提交必须由独立 workflow 和用户明确授权处理。

## 执行前后检查

执行前：

- 确认 `resolved`、TargetOwnerRoot、absolute path、exact file/section 和 transfer mode；
- 记录目标 owner 的 Git status，并确认没有不相关 dirty overlap；
- 确认未授权的 source、topic、index 或 Git action 不会被带入。

执行后：

- 检查每个新增或触碰页面的第一行摘要和标题；
- 检查 topic 同名说明页、根/目录索引和 lowercase kebab-case；
- 检查来源路径仍然存在且原始来源未被移动或删除；
- 按 owner 检查 Git status、`git diff --check` 和实际修改范围；
- 报告 `Wiki Check`、per-owner status、Skipped 和 Residual risk。
