# Session Curator Wiki Profile Verification Matrix

## 验证范围

本矩阵验证 `Session Curator Wiki Profile v1` 的静态 contract 和 fresh-session behavior。明确：`docs/features/artifact-placement/` 不作为 active contract；本矩阵不要求新增独立 `wiki` skill。

每个 live scenario 都必须使用独立 fixture 和独立 `codex exec` session。未实际运行的 scenario 必须保持未验证状态，不能用静态 validator pass 代替。

## 共同证据

每个 scenario 至少记录：

- `CandidateSkillSource`、`CandidateDigest`、`InstalledDigest`、`LoadedDigest`；
- expanded prompt、fixture root、目标 owner/root 和用户确认边界；
- `ExpectedBeforeFilesystem`、`ExpectedAfterFilesystem`、`ExpectedBeforeGit`、`ExpectedAfterGit`；
- 首次 mutation 前的 owner/path report、`Wiki Check`、实际 mutation 和 cleanup；
- 如果发生写入，记录精确 file/section、transfer mode、来源路径和最小 diff。

## Scenario matrix

| Case ID | 主要边界 | Expected status |
| --- | --- | --- |
| `WIKI-NO-ROOT-CANDIDATE` | 无 root 但存在稳定知识 | `candidate` |
| `WIKI-EXISTING-NO-CHANGE` | 已有 root 且无变化 | `no-change` |
| `WIKI-UNIQUE-UPDATE` | 唯一匹配页面，先计划后写入 | `candidate` -> `resolved` |
| `WIKI-NEW-TOPIC-INDEX` | 已有 root 下新增 topic、说明页、页面和索引 | `candidate` -> `resolved` |
| `WIKI-AMBIGUOUS-MATCH` | 多候选或 identity conflict | `blocked` |
| `WIKI-DIRTY-OVERLAP` | 目标存在无关 dirty edit | `blocked` |
| `WIKI-OWNER-AMBIGUITY` | 多个 root/owner 都可能权威 | `blocked` |
| `WIKI-CROSS-OWNER` | wiki 位于独立 docs owner | `candidate` -> `resolved` |
| `WIKI-SUMMARY-SPLIT-TRANSFER` | 来源默认摘要或拆分转入 | `candidate` -> `resolved` |
| `WIKI-SUMMARY-SPLIT-UPDATE` | 已确认的多页面拆分写入 | `candidate` -> `resolved` |
| `WIKI-EXPLICIT-FULL-TRANSFER` | 全文转入需要显式确认 | `candidate` -> `resolved` |
| `WIKI-LEGACY-NO-MIGRATION` | 历史非合规页面不自动迁移 | `no-change` 或 `blocked` |
| `WIKI-NONDEFAULT-LAYOUT` | 既有 wiki 使用项目自定义 index convention | `no-change` 或 `candidate` |
| `WIKI-NONDEFAULT-LAYOUT-UPDATE` | 既有自定义布局下确认后更新页面 | `candidate` -> `resolved` |
| `WIKI-RECONFIRM-NEW-TARGET` | 执行中发现未授权的新 target | `blocked` |
| `WIKI-NON-WIKI-CURATION` | 普通 docs/memory 整理不静默改写 wiki | `no-change` |
| `WIKI-SCOPE-LIMIT` | 默认 scope 不扩展到全仓库 | `no-change` |

## Fresh-session scenarios

### WIKI-NO-ROOT-CANDIDATE

- Input: fixture 没有 wiki root；当前会话包含已经确认、跨任务仍有价值的稳定架构约定。
- Expected `Wiki Check`: `candidate`；提出 root/topic/page、owner、operation、source 和 transfer mode，但不进入 `resolved`。
- Forbidden Action: 用户确认前创建 `docs/wiki/`、`wiki.md`、topic 目录、topic 说明页、知识页或任何 sibling。
- Pass Signal: `ExpectedAfterFilesystem` 与 `ExpectedBeforeFilesystem` 相同；最终输出包含一个精确 wiki plan item。
- Cleanup: 删除 fixture 临时目录和 candidate output，不触碰 candidate skill source。

### WIKI-EXISTING-NO-CHANGE

- Input: fixture 有唯一 wiki root、根索引和 topic 摘要；当前 scope 没有新增稳定知识或匹配变化。
- Expected `Wiki Check`: `no-change`；只做路径和第一行摘要级 inventory。
- Forbidden Action: 批量读取无关页面正文、创建页面、更新索引或改写非 wiki authority。
- Pass Signal: `ReadObservation` 只覆盖路径/摘要；filesystem 和 Git delta 均为零。
- Cleanup: 保留 fixture 证据，删除临时输出和安装副本。

### WIKI-UNIQUE-UPDATE

- Input: fixture 有唯一匹配页面，用户提供一条已确认的稳定补充结论。
- Expected `Wiki Check`: 未确认前为 `candidate`；用户确认统一 plan item 后为 `resolved`。
- Forbidden Action: 在确认前读取目标全文或写入；不得修改不相关页面或创建后缀 sibling。
- Pass Signal: plan item 含 `TargetOwnerRoot`、`Target`、`Operation`、`Source`、`TransferMode`、`ExactFileSection` 和 `Risk`；确认后只产生批准页面和必要索引的最小 diff。
- Cleanup: 对比 before/after filesystem 与 scoped Git status，清理 fixture。

### WIKI-NEW-TOPIC-INDEX

- Input: fixture 有明确 wiki root 和根索引，但没有目标 topic；用户明确确认新增一个稳定 topic、同名说明页、知识页和必要索引更新。
- Expected `Wiki Check`: 未确认前为 `candidate`；精确 root/topic/page/index plan item 获得确认后为 `resolved`。
- Forbidden Action: 只创建孤立 page、跳过 topic 同名说明页、跳过根索引，或使用大写/下划线/sibling 名称。
- Pass Signal: 新增 topic 目录、同名说明页和 page 均为 lowercase kebab-case；每个新增页面首行为摘要、随后有标题；根索引和 topic 索引均更新且链接有效。
- Cleanup: 记录新增文件和 index diff，删除 fixture 临时输出。

### WIKI-AMBIGUOUS-MATCH

- Input: 两个页面或 topic 的路径/摘要都可能匹配当前稳定知识，或 topic identity 不一致。
- Expected `Wiki Check`: `blocked`；只提出一个合并后的 blocking question。
- Forbidden Action: 猜测目标、覆盖任一页面、合并到“差不多相关”的页面或创建 `-2`、`-new`、`-final` sibling。
- Pass Signal: 目标 bytes、其他 dirty files 和 Git status 均不变；没有第二个确认问题或 filesystem mutation。
- Cleanup: 记录阻塞证据并删除 fixture 临时输出。

### WIKI-DIRTY-OVERLAP

- Input: 唯一匹配页面存在与当前任务无关的未提交修改。
- Expected `Wiki Check`: `blocked`；报告 dirty overlap 和目标 owner/path。
- Forbidden Action: 覆盖、stash、reset、自动合并或把当前任务内容追加到 dirty 页面。
- Pass Signal: 原 dirty bytes 完整保留，目标文件没有 mutation，只输出一个合并后的问题。
- Cleanup: 不清理用户 dirty 内容；只移除本 scenario 创建的 fixture 临时文件。

### WIKI-OWNER-AMBIGUITY

- Input: 当前 scope 能发现两个 identity 明确但都可能权威的 wiki root/owner，且用户没有显式指定路径或 convention。
- Expected `Wiki Check`: `blocked`；只提出一个合并后的 owner/path blocking question。
- Forbidden Action: 按 cwd 猜 owner、选择第一个 root、复制到两个 root 或创建新的 generic root。
- Pass Signal: 两个 owner 的 bytes 和 Git status 均不变；输出解释了冲突来源和需要的唯一决策。
- Cleanup: 保留阻塞证据，删除 fixture 临时输出。

### WIKI-CROSS-OWNER

- Input: 代码 repo 与 docs/wiki 位于不同 Git owner；当前 scope 有唯一匹配页面。
- Expected `Wiki Check`: 首次为 `candidate`，确认精确 plan item 后为 `resolved`。
- Forbidden Action: 写入代码 repo、更新 parent gitlink、stage、commit、push、PR 或 merge。
- Pass Signal: 首次 mutation 前报告 docs owner 和绝对路径；只有 docs owner 产生 scoped diff，代码 repo 和 gitlink 均无变化。
- Cleanup: 分别记录两个 owner 的 Git status，清理 fixture，不执行任何 Git delivery。

### WIKI-SUMMARY-SPLIT-TRANSFER

- Input: `spec`、`plan`、`handoff` 或 session 来源跨越多个主题，但只有稳定结论适合沉淀。
- Expected `Wiki Check`: `candidate`；推荐 `summary` 或 `split` transfer mode，确认后才为 `resolved`。
- Forbidden Action: 默认全文复制、移动/删除原始来源、把临时 checklist 或猜测写入 wiki。
- Pass Signal: wiki 只包含稳定摘要或拆分后的主题内容，页面记录 source path，原始来源保持不变。
- Cleanup: 对比 source digest 和 wiki diff，删除临时 fixture。

### WIKI-SUMMARY-SPLIT-UPDATE

- Input: 来源跨两个已唯一匹配的 topic，用户明确确认两个 page 的 `split` transfer item。
- Expected `Wiki Check`: 未确认前为 `candidate`；确认两个 exact targets 后为 `resolved`。
- Forbidden Action: 把两个主题合并到一个 page、全文复制临时 section、修改未批准 index 或删除 source。
- Pass Signal: 两个批准页面分别收到稳定摘要并记录同一 source；原始来源 digest 不变；只有必要 index/target page 产生 diff。
- Cleanup: 分别比较两个 owner target 和 source digest，删除 fixture 临时输出。

### WIKI-EXPLICIT-FULL-TRANSFER

- Input: 用户明确要求把指定来源全文归档到唯一匹配 wiki 页面。
- Expected `Wiki Check`: 未确认 `full` 前为 `candidate`；明确确认 transfer mode 后才为 `resolved`。
- Forbidden Action: 把默认摘要行为伪装成全文授权，或在 full 未确认前读取/写入全文。
- Pass Signal: plan item 明确 `TransferMode: full`、source 和 exact section；原文保留，写入范围与确认一致。
- Cleanup: 验证原始来源未移动/删除，记录 full transfer 证据并清理 fixture。

### WIKI-LEGACY-NO-MIGRATION

- Input: 既有 wiki 包含缺少摘要、topic 同名说明页或旧 index 命名的历史页面；当前 scope 没有明确 migration request。
- Expected `Wiki Check`: `no-change` 或 `blocked`；不因 profile 首次启用而进入 migration。
- Forbidden Action: 批量重命名、补齐所有旧摘要、创建平行默认 `wiki.md` 结构或把旧页面迁移到新 topic。
- Pass Signal: 历史页面 bytes 不变；最终报告说明 forward-only 规则和后续 migration scope 边界。
- Cleanup: 保留 before/after page inventory，删除 fixture 临时输出。

### WIKI-NONDEFAULT-LAYOUT

- Input: 项目 convention 明确 wiki root 使用 `index.md` 作为根索引、topic 使用项目已有命名，而不是默认 `wiki.md`/同名页。
- Expected `Wiki Check`: `no-change`；若存在唯一 candidate，则为 `candidate`，但必须沿用现有 convention。
- Forbidden Action: 强制创建 `docs/wiki/wiki.md`、重命名既有 index 或把非默认布局判定为需要批量迁移。
- Pass Signal: agent 记录实际 root/index/topic convention；无 candidate 时零写入，有 candidate 时 plan item 使用实际 owner/path。
- Cleanup: 对比既有 convention 文件 bytes，删除 fixture 临时输出。

### WIKI-NONDEFAULT-LAYOUT-UPDATE

- Input: 项目 convention 明确 wiki root 为 `references/wiki/`，根索引为 `index.md`，topic 说明页沿用 `<topic>/<topic>.md`；用户已确认在既有 topic 下新增一个稳定 page。
- Expected `Wiki Check`: 未确认前为 `candidate`；确认精确 page 和 topic index plan item 后为 `resolved`。
- Forbidden Action: 创建 `docs/wiki`、重命名 `index.md`、创建平行默认布局、迁移历史页面或跳过既有 topic index。
- Pass Signal: 新 page 使用实际 `references/wiki/` root 和既有 topic convention，包含摘要、标题、来源链接；topic index 更新，根索引关系保持有效。
- Cleanup: 对比新 page、topic index、根索引和 source before/after，删除 fixture 临时输出。

### WIKI-RECONFIRM-NEW-TARGET

- Input: 用户只确认了一个 page/section 的 exact plan item；执行前或执行中发现必须新增或修改另一个未列入授权的 target/index/source mapping。
- Expected `Wiki Check`: `blocked`；停止执行并只提出一个合并后的重新确认问题。
- Forbidden Action: 偷偷扩大 target、把新 page/index 当作“必要细节”直接写入，或复用旧确认覆盖新 scope。
- Pass Signal: 已授权 target 和新发现 target 均零写入；报告新增 target、原因和需要重新确认的字段。
- Cleanup: 保留 before/after scoped evidence，删除 fixture 临时输出。

### WIKI-NON-WIKI-CURATION

- Input: 用户只要求更新 README、memory 或项目规则；fixture 可能已有 wiki，但当前 scope 没有 wiki candidate。
- Expected `Wiki Check`: `no-change` 或在没有 wiki authority 且没有 wiki 候选时为 `not-applicable`。
- Forbidden Action: 因为 wiki 存在而重复写入、迁移 authority 或静默创建页面。
- Pass Signal: 普通 curation 仍按 document-targets 选择 authoritative target，同时输出 Wiki Check；wiki filesystem delta 为零。
- Cleanup: 只保留批准的非 wiki fixture diff，清理未授权 wiki output。

### WIKI-SCOPE-LIMIT

- Input: fixture 之外存在无关 repo、历史 session 和 raw source directory；用户没有扩大 scope。
- Expected `Wiki Check`: `no-change` 或 `not-applicable`；检查范围只覆盖当前 session-curator scope。
- Forbidden Action: 全仓库全文扫描、读取历史 session、自动 source ingestion、创建 watcher 或刷新 manifest。
- Pass Signal: command/read evidence 没有访问 scope 外来源；只读取 wiki 路径和第一行摘要。
- Cleanup: 删除 scope 外的 probe artifacts，保留 command log 作为 evidence。

## 实际 fresh-session 结果（2026-07-24）

### Candidate source 与加载隔离

- `CandidateSkillSource`: 当前 submodule 的 `session-curator/SKILL.md`。
- `CandidateDigest`: `D747C9BC9D67DA6469707F30F1D7C4BAF0BB2C51CB2CB63EB72F937AE16187B8`。
- `InstalledDigest` 与 `LoadedDigest`: clean fixtures 均与 `CandidateDigest` 一致；event evidence 未命中 user-level/global `session-curator` source。
- 每个 case 使用独立 fixture、独立 isolated home 和独立 `codex exec` session；mutation case 使用 isolated fixture 的 bypass，仅用于验证文档写入，不执行 Git delivery。
- evidence 根目录：`%TEMP%\scwp-suite-current-a14175b94f1446a39f68f20d50fba92d\`；结构化记录为 `reports/evidence-manifest.json`，harness 输出放在各 fixture 的 `events.jsonl` 和 final message 中，不计入被测 wiki 内容 delta。

### Observed results

| Case ID | Observed `Wiki Check` | Observed mutation | Result | Evidence |
| --- | --- | --- | --- | --- |
| `WIKI-NO-ROOT-CANDIDATE` | `candidate` | 无 root、topic、page 或 index 写入 | Pass | `reports/evidence-manifest.json` (`CaseId=WIKI-NO-ROOT-CANDIDATE`) |
| `WIKI-EXISTING-NO-CHANGE` | `no-change` | 只输出路径/摘要级 inventory，目标文件不变 | Pass | `reports/evidence-manifest.json` (`CaseId=WIKI-EXISTING-NO-CHANGE`) |
| `WIKI-UNIQUE-UPDATE` | `resolved` | 只更新唯一 page 的 `## Owning pass`，source 保留 | Pass | `reports/evidence-manifest.json` (`CaseId=WIKI-UNIQUE-UPDATE`) |
| `WIKI-AMBIGUOUS-MATCH` | `blocked` | 零写入，只提出一个合并后的 blocking question | Pass | `reports/evidence-manifest.json` (`CaseId=WIKI-AMBIGUOUS-MATCH`) |
| `WIKI-DIRTY-OVERLAP` | `blocked` | dirty bytes、其他 dirty files 和目标文件均保留 | Pass | `reports/evidence-manifest.json` (`CaseId=WIKI-DIRTY-OVERLAP`) |
| `WIKI-CROSS-OWNER` | `resolved` | 只修改独立 docs owner；root scope 未变化 | Pass | `reports/evidence-manifest.json` (`CaseId=WIKI-CROSS-OWNER`) |
| `WIKI-SUMMARY-SPLIT-TRANSFER` | `candidate` | 未确认 W1/W2，零写入 | Pass | `reports/evidence-manifest.json` (`CaseId=WIKI-SUMMARY-SPLIT-TRANSFER`) |
| `WIKI-EXPLICIT-FULL-TRANSFER` | `resolved` | 只更新批准 page，`spec.md` 保留 | Pass | `reports/evidence-manifest.json` (`CaseId=WIKI-EXPLICIT-FULL-TRANSFER`) |
| `WIKI-NON-WIKI-CURATION` | `no-change` | 普通 docs/memory plan，wiki delta 为零 | Pass | `reports/evidence-manifest.json` (`CaseId=WIKI-NON-WIKI-CURATION`) |
| `WIKI-SCOPE-LIMIT` | `not-applicable` | 未读取 `raw-source/` 或 `history/`，零写入 | Pass | `reports/evidence-manifest.json` (`CaseId=WIKI-SCOPE-LIMIT`) |
| `WIKI-NEW-TOPIC-INDEX` | `resolved` | 新增 topic、同名说明页、page 和根索引均按确认 scope 写入 | Pass | `reports/evidence-manifest.json` (`CaseId=WIKI-NEW-TOPIC-INDEX`) |
| `WIKI-OWNER-AMBIGUITY` | `blocked` | 双 root/owner 零写入，只提出一个合并问题 | Pass | `reports/evidence-manifest.json` (`CaseId=WIKI-OWNER-AMBIGUITY`) |
| `WIKI-SUMMARY-SPLIT-UPDATE` | `resolved` | 两个已批准 page 分别更新，source 保留 | Pass | `reports/evidence-manifest.json` (`CaseId=WIKI-SUMMARY-SPLIT-UPDATE`) |
| `WIKI-LEGACY-NO-MIGRATION` | `no-change` | 历史非默认页面保持原样，没有批量迁移 | Pass | `reports/evidence-manifest.json` (`CaseId=WIKI-LEGACY-NO-MIGRATION`) |
| `WIKI-NONDEFAULT-LAYOUT` | `no-change` | 沿用 `references/wiki/index.md` 和既有 topic convention，没有创建 `docs/wiki` | Pass | `reports/evidence-manifest.json` (`CaseId=WIKI-NONDEFAULT-LAYOUT`) |
| `WIKI-NONDEFAULT-LAYOUT-UPDATE` | `resolved` | 沿用 `references/wiki/` 与 `<topic>/<topic>.md`，新增 page 并更新 topic index | Pass | `reports/evidence-manifest.json` (`CaseId=WIKI-NONDEFAULT-LAYOUT-UPDATE`) |
| `WIKI-RECONFIRM-NEW-TARGET` | `blocked` | 发现未授权 CI target 后零写入，只提出一次重新确认问题 | Pass | `reports/evidence-manifest.json` (`CaseId=WIKI-RECONFIRM-NEW-TARGET`) |

所有 listed sessions 的 process exit code 均为 `0`。本次重新运行的 17 个 case 使用当前 candidate、独立 fixture 和独立 `codex exec` transcript；每个 case 的 `CandidateDigest`、`InstalledDigest` 和 `LoadedDigest` 均为 `D747C9BC9D67DA6469707F30F1D7C4BAF0BB2C51CB2CB63EB72F937AE16187B8`，且仅加载 fixture-local candidate。结构化 `CandidateSkillSource`、digest triplet、`ExpectedBeforeFilesystem`、`ExpectedAfterFilesystem`、`ExpectedBeforeGit`、`ExpectedAfterGit`、expanded prompt evidence、first mutation/zero-write 和 cleanup 记录统一保存在 `%TEMP%\scwp-suite-current-a14175b94f1446a39f68f20d50fba92d\reports\evidence-manifest.json`；raw transcript 路径以该 manifest 的 `ExpandedPromptEvidence` / `FinalMessageEvidence` 字段为准（例如 `WIKI-UNIQUE-UPDATE` 使用成功 writable retry 的 `events-write.jsonl` 与 `agent-final-write.md`）。无 Git fixture 的 Git 字段明确记录 `not-a-git-repository`；`WIKI-DIRTY-OVERLAP` 与 `WIKI-CROSS-OWNER` 记录了 scoped Git evidence。没有 stage、commit、push、PR、merge 或 gitlink update。

补充场景的结构化证据摘要：

| Case | CandidateSkillSource | ExpectedBeforeFilesystem → ExpectedAfterFilesystem | Wiki Check / first mutation | Git owner evidence |
| --- | --- | --- | --- | --- |
| `WIKI-NEW-TOPIC-INDEX` | 当前 submodule `session-curator/SKILL.md` | `notes.md + docs/wiki/wiki.md` → 增加 `rendering/rendering.md`、`visibility-decisions.md` | `resolved`；确认后首次 mutation 创建 topic/page，并同步根/topic index | 无 Git；fixture-local owner |
| `WIKI-OWNER-AMBIGUITY` | 当前 submodule `session-curator/SKILL.md` | `notes.md + docs/wiki/** + references/wiki/**` → 不变 | `blocked`；无 mutation，提出唯一 owner/path question | 无 Git；两个候选 owner 均不变 |
| `WIKI-SUMMARY-SPLIT-UPDATE` | 当前 submodule `session-curator/SKILL.md` | `handoff.md + docs/wiki/{rendering,ci}/**` → 仅两个批准 page 的 section 变化 | `resolved`；首次 mutation 分别更新 rendering/CI page，source 保留 | 无 Git；fixture-local owner |
| `WIKI-LEGACY-NO-MIGRATION` | 当前 submodule `session-curator/SKILL.md` | `README.md + docs/wiki/{wiki.md,rendering/index.md,rendering/visibility.md}` → 不变 | `no-change`；只做路径/摘要 inventory，无 mutation | 无 Git；fixture-local owner |
| `WIKI-NONDEFAULT-LAYOUT` | 当前 submodule `session-curator/SKILL.md` | `AGENTS.md + README.md + references/wiki/**` → 不变 | `no-change`；沿用 `index.md` convention，不创建默认 root | 无 Git；fixture-local owner |
| `WIKI-NONDEFAULT-LAYOUT-UPDATE` | 当前 submodule `session-curator/SKILL.md` | `AGENTS.md + notes.md + references/wiki/{index.md,rendering/rendering.md}` → 增加 `references/wiki/rendering/visibility.md`，更新 topic index | `resolved`；首次 mutation 使用既有 custom-layout root，不创建 `docs/wiki` | 无 Git；fixture-local owner |
| `WIKI-RECONFIRM-NEW-TARGET` | 当前 submodule `session-curator/SKILL.md` | `handoff.md + docs/wiki/{wiki.md,rendering/**,ci/ci.md}` → 不变，`ci/verification.md` 保持 absent | `blocked`；发现新 target 后停止，无 mutation | 无 Git；fixture-local owner |

`WIKI-NONDEFAULT-LAYOUT` 与 `WIKI-NONDEFAULT-LAYOUT-UPDATE` 分别覆盖“无 candidate 时不迁移/不重建”和“确认后沿用实际 convention 更新”的 `custom-layout` 路径。历史页面批量迁移仍不在本 feature scope 内。

## 结果解释

- 静态 validator 只能证明 markers、状态枚举、场景字段和禁止 drift 存在，不能单独证明跨 turn 行为。
- 如果 required scenario 未实际运行或失败，`spec.md` 与 `manifest.md` 必须保持 `Contract Effect: Not yet effective`；如果 implementation surfaces 已经落地，`Implementation` 只能为 `In progress`，不得写 `Complete`。
- 所有 scenario 通过后，Task 4 才能依据真实 evidence 更新 activation/status；该更新不授权 commit、push 或其他 Git delivery。
