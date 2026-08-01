# Skill 正文中文化迁移 Spec

## 元数据 (Metadata)

- **Status**: Approved
- **Source**: conversation context、`grill-me` 决策记录、当前 16 个 `SKILL.md`、仓库规则与 validator contract
- **Generated at**: 2026-07-23
- **Feature Slug**: skill-content-chinese-localization
- **Repository Snapshot**: target submodule `45d99a8`; parent workspace `3ef2b44`
- **Supersedes**: 当前仓库及历史 feature artifacts 中的运行时中文输出保证、`Language Contract` marker/exception 要求及其 validator enforcement；历史文件的其他 workflow 与安全要求继续有效且保留原文

## 问题陈述 (Problem Statement)

当前仓库已经声明 skill 与其生成内容应以中文为主，但 16 个 `SKILL.md` 仍混有大量英文 `description`、section heading、场景说明、流程叙述和 Mermaid 可见标签。英文既承担了用户可见说明，也承担 trigger phrase、稳定 contract、YAML key、ID 和 validator 精确 marker 等不同职责，导致维护者无法简单判断哪些内容应该中文化、哪些内容必须保留。

现有 `Language Contract` 又把“仓库如何编写 skill”与“skill 运行时使用什么语言输出”混在一起。该段落被复制到全部 16 个 skill，并由 validator 逐字检查。用户已经明确选择删除这些段落，接受 skill 独立安装后不再由 skill 自身保证中文输出；运行时语言改由用户请求、目标项目规则和会话上下文决定。

本 feature 需要把全部现有及未来 `SKILL.md` 收敛到可审计的中文优先编写规则，同时保护隐式触发、workflow 路由、授权边界、稳定 ID 和验证行为。除删除 `Language Contract` 这一项已授权行为变化外，迁移不得重新设计 skill。

## 目标 (Goals)

- 让现有全部 16 个及未来新增的 `SKILL.md` 采用中文主文。
- 让 frontmatter `description` 采用中文主句，同时保留有测试证据的必要 English trigger phrases。
- 明确机器语法、稳定标识、技术专名、测试数据和普通叙述的语言边界。
- 原子移除全部 per-skill `Language Contract` 及其当前规则和 validator 强制检查。
- 保持既有 skill inventory、workflow 路由、约束强度、artifact contract 和安全门不变。
- 通过硬规则、非阻塞 English-heavy 审阅和代表性 routing smoke test 建立可重复验证的完成标准。

## 方案与架构 (Approach and Architecture)

### 分层语言模型

每个 `SKILL.md` 的内容按用途分为四层：

1. **机器语法与稳定 contract**：skill 目录名、frontmatter `name`、代表 canonical skill name 的 H1、YAML frontmatter key、Markdown/代码语法、命令、API、路径、`$skill` ID、稳定字段、枚举值、版本名和 gate ID 保持英文或原始拼写。
2. **触发 metadata**：`description` 使用中文主句；只有能映射到英文 trigger test、且确有边界识别价值的 English phrase 才能保留。不得附加完整英文复述。
3. **用户可见说明**：普通正文、普通 section heading、场景解释、表格说明和 Mermaid 可见标签使用中文。被 validator、其他 skill 或仓库 contract 稳定引用的标题使用“中文（English）”形式。
4. **行为测试数据**：英文用户 prompt 可以作为与中文用例成对的原始测试输入保留；其场景名称、预期行为和失败说明使用中文。

稳定 ID 与可见说明必须分开处理。例如 Mermaid node ID 可以保持 `N1`，节点标签应写成中文；`Planning Quality Status: Pass` 可以保持原样，其周围的风险解释应使用中文。

稳定双语标题不能仅因为旧 validator 写死英文就获得保留资格。最小 allowlist 为 `Trigger Description`、`Pressure Scenarios` 和 `Natural Handoff`；其他标题只有在 active cross-skill contract 确实按名称引用时才能加入，普通英文 validator marker 应随正文一起中文化。

### 运行时语言契约移除

删除 `Language Contract` 是独立的全局原子阶段。该阶段同时移除：

- 全部 16 个 `SKILL.md` 中的对应 section。
- validator 中对 marker 和 exception 句的逐字强制检查。
- 目标仓库 `AGENTS.md`、父工作区 `C:\WorkSpace\skill-development\AGENTS.md` 与目标仓库 `README.md` 中“每个 skill 必须包含该 marker”及运行时默认中文输出的当前规则。
- 其他 active `SKILL.md` section 中散落的默认中文输出保证；不得只删除统一标题而留下等价要求。

该阶段不把同一输出语言要求转移到其他 per-skill section。完成后，skill 独立安装时不再保证中文输出，这是用户明确接受的行为变化。

### 依赖驱动迁移

正文中文化在全局契约移除之后按 workflow 依赖顺序推进：

1. 独立终点：`clarify`、`improve-codebase-architecture`、`handoff`。
2. 下游质量门：`tdd`、`requesting-code-review`、`verification-before-completion`。
3. 分支与知识连续性：`checking-branch`、`finishing-branch`、`session-curator`。
4. Planning 契约：`to-spec`、`to-plan`、`analyze`。
5. 上游设计入口：`brainstorming`、`grill-me`。
6. 中心实现与诊断闭环：`diagnose`、`implement`。

每批必须与其 validator 精确 marker 同步，并在进入下一批前保持仓库可验证。第一批完成后设置一次 human calibration gate；用户确认语言风格和术语后，其余批次连续执行，只有真实语义歧义才再次暂停。

### 验证模型

验证采用三层组合，不使用中文字符占比：

- **硬规则**：frontmatter/metadata 合法、`description` 含中文、稳定 ID 未漂移、必要标题符合约定、validator 与 discoverability 检查通过。
- **非阻塞审阅**：列出代码块之外的纯英文标题、整句和长段落；每个保留项必须有明确理由。
- **行为验证**：全部 16 个 skill 定义中文正向、英文正向和 near-miss 静态场景；对边界重叠最大的 planning 组与 implementation/diagnosis 组执行 fresh-session smoke test。

本 feature 不新增跨会话 routing eval harness，也不要求执行 48 次全量 live session。未进行 live routing 的低耦合 skill 作为已接受的 residual risk 记录。

## 关键决策与取舍 (Key Decisions and Tradeoffs)

- **决策**: 覆盖全部现有及未来 skill。**理由**: 只约束新增或改动文件会让仓库长期保持混合状态。**被排除的方案**: forward-only 迁移无法建立一致、可验证的目标态。
- **决策**: `description` 使用中文主句加有证据的 English trigger phrase。**理由**: 中文请求可直接匹配，同时保留英文请求的关键边界。**被排除的方案**: 全英文违背中文优先目标；纯中文可能降低英文隐式触发；中英完整双写会产生冗余并更易被截断。
- **决策**: 不使用中文字符比例。**理由**: 比例会错误惩罚代码、schema 和稳定 contract 密集的 skill，也不能证明语义质量。**被排除的方案**: 固定百分比只能衡量字符，不能衡量触发与约束是否正确。
- **决策**: 仅稳定契约标题保留英文别名。**理由**: 普通标题双语化会制造无功能价值的噪声。**被排除的方案**: 所有标题都写成“中文（English）”不符合“尽可能中文”。
- **决策**: 删除全部 per-skill `Language Contract`。**理由**: 仓库编写语言与运行时输出语言是不同职责，重复段落会回漂并降低跨项目可移植性。**代价**: 独立安装后不再由 skill 自身保证中文输出。
- **决策**: 除契约删除外只做语义保持型中文化。**理由**: 同时翻译和重设计会让 review 无法区分语言问题与 workflow 行为变化。**被排除的方案**: 借迁移顺便重构、删减或修复既有 workflow。
- **决策**: 按依赖分批并仅在第一批后校准一次。**理由**: 下游术语先稳定可降低中心 `implement` 的耦合风险，一次校准能避免错误风格扩散。**被排除的方案**: 平均分批忽略 contract 关系；每批确认过慢；完全无校准会放大主观翻译偏差。
- **决策**: 全量静态场景加高风险组 live smoke test。**理由**: 当前仓库没有自动跨会话 eval harness，48 次 one-shot live session 成本高且仍有随机性。**被排除的方案**: 本次额外开发 eval harness 或把完整 48 次 fresh-session 作为完成前置条件。
- **决策**: 历史 artifacts 保持原文。**理由**: 它们记录当时真实需求；新 spec 通过 supersession 保留演进轨迹。**被排除的方案**: 回写历史文档会制造“规则从未变化”的错误印象。

## 非目标 (Non-Goals)

- 不修改 skill workflow、路由边集合、授权边界、产物 schema 或安全门。
- 不对 `references/`、`assets/`、templates、非 validator 脚本或历史 `docs/features/**` 做本地化；`scripts/validate-skills.py` 只进行本 feature 必需的 contract 同步和 guardrail 调整。
- 不修改 `agents/openai.yaml`，除非后续 plan 发现它与已确认 trigger 语义存在直接、可证明的不一致；普通语言统一不构成修改理由。
- 不修改 `C:\Users\Administrator\.agents\skills` 中的全局安装副本。
- 不修改其他 submodule、父仓库中除上述 active `AGENTS.md` 之外的无关文件或远端仓库。
- 不新增 routing eval harness，不建立中文字符比例评分器。
- 不自动创建或切换 branch，不执行 commit、push、PR、merge 或 discard。

## 功能需求 (Functional Requirements)

- **FR-001**: 迁移目标必须覆盖仓库当前全部 16 个 `SKILL.md`，且新增 skill 必须遵守同一中文优先编写规则。
- **FR-002**: 全局第一阶段必须原子删除 16 个 `Language Contract` section、其他 active section 中等价的默认中文输出保证、validator 对 marker/exception 的强制检查，以及目标仓库 `AGENTS.md`、父工作区 active `AGENTS.md`、目标仓库 `README.md` 中对应当前规则；不得把同一输出语言要求复制到其他 per-skill section。
- **FR-003**: 删除 `Language Contract` 后，skill 运行时语言必须由用户请求、目标项目规则和会话上下文决定；不得继续宣称独立安装的 skill 保证中文输出。
- **FR-004**: 新 spec 必须明确只 supersede `spec-plan-workflow`、`adaptive-planning-workflow`、`natural-handoff-workflow` 与 `workflow-skill-consolidation` 历史 artifacts 中的运行时中文输出保证、`Language Contract` marker/exception 及其 validator enforcement；其余 workflow 与安全要求继续有效，且实现不得回写这些历史文件。
- **FR-005**: `name` 值、YAML frontmatter key、目录名和 `$skill` ID 必须保持原样；`description` 值必须改为中文主句并保持原 trigger scope 与 boundary。
- **FR-006**: `description` 中保留的每个非专名 English trigger phrase 必须至少映射到一个英文触发场景；不得保留完整英文描述副本。
- **FR-007**: 普通说明、普通 heading、表格标签、场景解释和流程叙述必须使用中文；代表 canonical skill name 的 H1 保持原样，中文会降低准确性时只能保留最小必要 English term。
- **FR-008**: 稳定 section heading 的基础 allowlist 为 `Trigger Description`、`Pressure Scenarios` 和 `Natural Handoff`，它们必须使用“中文（English）”形式并同步更新 validator；只有 active cross-skill contract 确实按名称引用时才能扩展 allowlist，普通 heading 不得因旧 validator 写死或双语对称而保留英文别名。
- **FR-009**: YAML/Markdown/代码语法、命令、API、路径、稳定 contract field、enum、版本名、gate ID、`FR-###`、`SC-###` 和其他机器消费值必须保持原始拼写。
- **FR-010**: `Pressure Scenarios`、示例和测试用例的说明必须中文化；用于验证英文触发的原始 prompt 必须与中文正向场景成对保留。
- **FR-011**: Mermaid node ID、schema field 和固定状态值必须保持原样；Mermaid 可见标签、边条件、schema 解释和示例叙述必须中文化。
- **FR-012**: 除 FR-002 明确授权的行为变化外，迁移必须保持 workflow 顺序、handoff 目标、路由边、停止条件、读写边界、产物 contract 和验证要求不变。
- **FR-013**: `必须`、`不得`、`仅当`、`最多一个`、`唯一推荐`、`只读`、`写入前停止` 等规范性强度不得在翻译中弱化；无法确认等价时必须暂停该 skill 并报告 blocker。
- **FR-014**: 每个保留的非固定英文片段必须进入 English-heavy 审阅清单并记录理由；正确性与触发可靠性优先于中文纯度。
- **FR-015**: 正文迁移必须按本 spec 的六个依赖批次推进，每批与对应 validator marker 同步，且第一批完成后必须经过一次 human calibration gate。
- **FR-016**: validator 必须新增 `description` 至少包含一个中文字符的硬检查，并验证必要的中文优先标题；不得新增中文字符比例门槛。
- **FR-017**: English-heavy 检查必须排除真正的代码块、命令、路径和稳定 contract，并作为非阻塞审阅清单，不得仅凭命中判定失败。
- **FR-018**: 独立 verification matrix 必须为全部 16 个 skill 分别定义中文正向、英文正向和 near-miss 静态场景；保留的 English trigger phrase 必须能追溯到这些场景。既有 `Pressure Scenarios` 只做等义中文化，不得为了测试覆盖而给原本没有该 section 的 skill 新增运行时流程。
- **FR-019**: `brainstorming`、`grill-me`、`to-plan`、`to-spec`、`analyze` 以及 `implement`、`diagnose`、`checking-branch` 必须执行代表性 fresh-session routing smoke test，并提供加载仓库候选版本而非全局安装副本的证据；其他 skill 未执行 live routing 必须记录为 residual risk。
- **FR-020**: 全部迁移完成后，本地 skill inventory 与 discoverability 必须仍为同一组 16 个名称，且每个 skill 能以 full-depth 方式被解析。
- **FR-021**: 实现范围必须限制在 16 个 `SKILL.md`、必要的 `scripts/validate-skills.py`、目标仓库 `AGENTS.md`、父工作区 `C:\WorkSpace\skill-development\AGENTS.md`、目标仓库 `README.md` 和本 feature workspace；历史 artifacts、全局安装副本、父仓库其他文件及无关文件必须保持不变。

## 成功标准 (Success Criteria)

- **SC-001**: `python scripts/validate-skills.py` 退出码为 0，并输出 `Validated 16 skills.`
- **SC-002**: 16 个 `SKILL.md` 的 `description` 均包含中文，且不存在无测试映射的完整英文描述副本。
- **SC-003**: active `SKILL.md`、validator、目标仓库与父工作区 active `AGENTS.md`、目标仓库 `README.md` 不再要求或包含 per-skill `Language Contract`；历史 `docs/features/**` 保持原文。
- **SC-004**: 除 canonical skill name H1 和已批准的稳定双语标题外，普通英文 heading、代码块外整段英文说明和未解释的 English-heavy 文本为零；所有合理保留项均有审阅理由。
- **SC-005**: 迁移前后的 16-skill inventory、`Natural Handoff` 路由边、稳定 ID、schema field、gate ID 和规范性约束集合不发生非授权变化。
- **SC-006**: 独立 verification matrix 至少包含 48 个静态 routing case，覆盖 16 个 skill 的中文正向、英文正向和 near-miss，并能从每个保留的 English trigger phrase 追溯到至少一个 case。
- **SC-007**: planning 组与 implementation/diagnosis 组的代表性 fresh-session smoke test 能证明加载的是仓库候选版本，能区分正向触发和 near-miss，且未出现因中文化导致的边界扩大或遗漏。
- **SC-008**: 第一批 human calibration 完成后，后续五批使用同一语言规则推进；每批 validator、English-heavy 审阅与 `git diff --check` 均通过。
- **SC-009**: 本地 `npx skills` 列出且只列出预期 16 个 skill，16 个名称的 full-depth 解析全部成功。
- **SC-010**: 历史 artifacts、其他 submodule、全局安装副本、父仓库中除 active `AGENTS.md` 外的其他文件和无关工作树文件没有本 feature 产生的修改。
- **SC-011**: 最终报告明确记录未做 live routing 的低耦合 skill、触发随机性以及移除运行时语言契约后的行为变化，不把 residual risk 包装成已验证事实。

## 测试决策 (Testing Decisions)

- **Verification seam（验证切入点）**: 以本地 validator、skill discoverability、静态 trigger matrix、跨 skill route invariant 和代表性 fresh-session routing 为主 seam；这些检查直接覆盖 skill 是否可发现、何时触发、加载后是否保持既有行为。
- **Prior art（现有依据）**: `scripts/validate-skills.py` 已检查 frontmatter、metadata、stale workflow text 和多组精确 contract marker；现有 workflow feature plans 已明确当前没有自动跨 turn eval harness，并采用 static marker 加 fresh-session manual scenario。
- **Automated checks（自动检查）**:
  - 运行 `python scripts/validate-skills.py`。
  - 检查 active surfaces 中 `Language Contract`、纯英文 heading、整段英文说明和未同步 marker。
  - 检查 16-skill inventory、稳定 `$skill` reference、route edge 与 contract ID 集合。
  - 使用本地 `npx skills` list 与 full-depth 解析验证 discoverability。
- **Manual checks（人工检查）**:
  - 第一批完成后审核术语、语气、规范性强度和 English 保留理由。
  - 对所有批次复核 `must/should/may` 等约束没有被翻译弱化。
  - 对 planning 与 implementation/diagnosis 高耦合组执行代表性中英文正向和 near-miss fresh-session smoke test，并记录候选 source/path 或等价加载证据。
- **Manual fallback（手动兜底）**: 如果 routing smoke test 无法稳定观测 skill 选择，保留静态场景和 description diff 证据，将该项标为 residual risk；不得为通过测试而扩大 trigger scope。

## 风险与开放问题 (Risks and Open Questions)

- **Risk**: 中文翻译可能弱化规范性强度或误改授权边界。通过稳定词汇、route/contract invariant、逐批 review 和 blocker 规则控制。
- **Risk**: `description` 的中文化可能改善中文触发但降低英文触发，或因中文概括过宽造成误触发。通过 English phrase 可追溯规则、双语静态场景和高风险组 live smoke test控制。
- **Risk**: validator 当前对多个英文 heading、Mermaid label 和普通 contract 文本做逐字检查。相关 skill 与 marker 必须同批更新，避免 validator 反向固化旧语言。
- **Risk**: 删除 `Language Contract` 后，独立安装的 skill 不再保证中文输出。这是已接受的行为变化，最终报告仍须明确说明。
- **Risk**: `references/` 和 `assets/` 不在本次范围内，skill 通过 progressive disclosure 加载它们时仍可能读取英文材料。这不属于 `SKILL.md` 正文迁移失败，但必须保留为范围说明。
- **Risk**: fresh-session routing 具有模型随机性，代表性 smoke test 不能证明所有 prompt 永久稳定。不得把未执行的 48 次全量矩阵描述为已覆盖。
- **Risk**: 全局安装副本明确不更新，fresh-session 若未隔离 source 可能误测旧版本。live smoke 的结果只有在候选版本加载证据存在时才有效。
- **Risk**: 大面积 Markdown 中文化可能引入 CRLF、UTF-8 或 whitespace 噪声。每批必须使用 scoped diff 与 `git diff --check` 区分内容变化和格式漂移。
- **Risk**: 历史 artifacts 仍包含旧 `Language Contract` 要求。新 spec 的 supersession 元数据和 current repo docs 必须让读者能区分历史记录与当前规则。
- **Open Question**: 无阻塞开放问题。用户已确认语言边界、契约移除、历史保留、批次顺序、校准点、验证范围和失败优先级。

## Plan 交接说明 (Handoff Notes for Plan)

- 第一原子阶段只处理 `Language Contract` 全局移除及 current rule/validator 同步，单独验证这一项行为变化。
- 后续按六个依赖批次拆分 tasks；每批需要覆盖对应 `SKILL.md`、validator marker、English-heavy 审阅和静态场景。
- 第一批 task 之后设置唯一 human calibration gate；通过后其余批次不得因普通措辞再次中断。
- Planning、implementation、diagnosis 相关批次必须显式维护迁移前后的 route edge、稳定 contract 和规范性强度 invariant。
- 最终 task 必须覆盖全量 validator、discoverability、full-depth、scope audit、历史文件不变证明及代表性 fresh-session smoke test。
- plan 必须为 `FR-001` 至 `FR-021` 建立 task 与 verification coverage；不得把本 spec 解释为 branch、implementation、commit、push 或远端操作授权。
