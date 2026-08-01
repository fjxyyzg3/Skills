# Spec-Plan Workflow 替换 PRD-Issues 工作流 PRD

## 元数据 (Metadata)

- **Status**: Draft
- **Source**: conversation context (grill-me 会话共识, 2026-07-03)
- **Generated at**: 2026-07-03
- **Feature Slug**: spec-plan-workflow

## 问题陈述 (Problem Statement)

现有 `to-prd -> to-issues` 链条是围绕"多 issue 并行多 agent 开发"设计的：PRD 产出需求契约，issues 产出带依赖图、执行波次和并行字段的垂直切片。但实际使用中能多 issue 并行的场景很少，issue 拆分的全套机制（Wave、Parallelization、依赖类型、Subagent 执行指引）成为日常不使用却必须维护的负担。维护者更习惯 obra-superpowers 的 spec -> plan 两段式：先写叙事型 design doc，再写任务级 implementation plan，串行执行。

## 目标 (Goals)

- 用 `to-spec` + `to-plan` 两个新 skill 替换 `to-prd` + `to-issues`，对齐 spec -> plan 的日常使用习惯。
- 保留现有链条后半段的机器可核对锚点：`FR-###`/`SC-###` 稳定 ID 和 plan task 的 `Covers` 追溯，使 `analyze` 和 `verification-before-completion` 的 coverage 检查继续成立。
- 移除以"多 issue 并行"为前提的机制：依赖图、执行波次、并行字段、implement 的 wave 执行分支。
- 一次性完成全部引用面更新，`validate-skills.py` 保持全绿。

## 非目标 (Non-Goals)

- 不照搬 superpowers 的代码级 plan（每步带完整测试/实现代码）；代码由 `implement` 的 TDD 循环现场产出。
- 不设 deprecation 过渡期，不保留旧 skill 的别名或跳转桩。
- 不修改历史产物（`docs/features/natural-handoff-workflow/` 等既有 prd/issues 文档保持原样，作为历史记录）。
- 不改动 `brainstorming`、`grill-me` 等上游 skill 的核心工作方式，只更新它们的 Natural Handoff 目标和描述。
- 不引入 superpowers 的 `docs/superpowers/specs/YYYY-MM-DD-*` 日期命名；沿用 feature workspace 的 slug 目录制。

## 用户故事 (User Stories)

1. 作为 skill 库维护者，我希望在方向共识后一步生成叙事型 spec（含稳定需求 ID），以便按我熟悉的 spec -> plan 节奏推进，而不是先写产品向 PRD。
2. 作为 skill 库维护者，我希望 plan 直接给出"改哪些文件、接口契约是什么、怎么验证"，以便 `implement` 拿到就能串行执行，不需要先理解波次和并行标记。
3. 作为 skill 库维护者，我希望 `analyze` 仍能机器化核对"每条 FR 有 task 覆盖、每个 task 能追回 FR"，以便实现前发现覆盖缺口。

## 功能需求 (Functional Requirements)

- **FR-001**: 存在新 skill `to-spec`（`to-spec/SKILL.md` + `to-spec/agents/openai.yaml`），将 conversation context、brainstorming handoff 或本地文件整理成叙事型 spec，默认写入 `docs/features/<feature-slug>/spec.md`。
- **FR-002**: `to-spec` 产出的 spec 采用叙事结构（问题陈述、方案与架构、关键决策与取舍），同时功能需求使用 `FR-###`、成功标准使用 `SC-###` 稳定 ID，并包含测试决策（verification seam）与风险/开放问题章节，正文中文优先。
- **FR-003**: 存在新 skill `to-plan`（`to-plan/SKILL.md` + `to-plan/agents/openai.yaml`），将 spec 拆成任务级 plan，默认写入 `docs/features/<feature-slug>/plan.md`（单文件，不再是 issues 目录）。
- **FR-004**: plan 中每个 task 包含：精确文件路径（Create/Modify/Test）、`Consumes/Produces` 接口契约、`Covers`（指向 `FR-###` 或 conversation requirement）、验收标准、验证命令；task 按执行顺序编号，串行语义。
- **FR-005**: plan 不包含实现代码、依赖图、`Wave`、`Parallelization`、`AFK/HITL` 类型字段或 subagent 并行指引；plan 末尾有 coverage 自查表，列出所有 `FR-###` 与对应 task，未覆盖项需注明原因。
- **FR-006**: `to-prd/` 和 `to-issues/` 两个 skill 目录被删除，仓库中（历史产物目录除外）不再有对 `$to-prd`/`$to-issues` 的活引用。
- **FR-007**: `workflow-router/SKILL.md` 的路由表、示例和 Allowed skill 列表更新为 `$to-spec`/`$to-plan`；spec 场景与 plan 场景各有唯一路由入口。
- **FR-008**: `brainstorming/SKILL.md` 及其 `agents/openai.yaml` 的 handoff 目标从 `$to-prd` 改为 `$to-spec`（handoff packet 名称随之调整），禁跳约束同步改为不得自动进入 `$to-plan`/`$analyze`/`$implement`/`$quick-change`。
- **FR-009**: `grill-me/SKILL.md` 的 Natural Handoff 规则更新：未 formalized 时推荐 `$to-spec`，已有 spec 需拆 plan 时推荐 `$to-plan`。
- **FR-010**: `quick-change/SKILL.md` 的升级链路从 `$to-prd -> $to-issues -> $analyze -> $implement` 改为 `$to-spec -> $to-plan -> $analyze -> $implement`，升级推荐列表同步替换。
- **FR-011**: `implement/SKILL.md` 改为以 plan（或 spec、conversation scope）为输入：读取 plan task 的文件路径、接口契约、验收标准和验证命令，按 task 顺序串行执行；删除以 issue wave/parallel-safe 字段为前提的 `Multi-Agent Waves` 执行分支及相关确认节点；保留"subagent 只读探索/spike"的能力。
- **FR-012**: `analyze/SKILL.md` 的检查对象改为 spec + plan：coverage 检查为 `FR-###` 与 task `Covers` 的双向追溯；删除依赖环、wave 顺序、并行建议相关检查项；description 同步更新。
- **FR-013**: `README.md` 和 `AGENTS.md` 的链条图、skill 表格和默认链路描述更新为 `to-spec -> to-plan`；`AGENTS.md` 中"已有 artifacts 默认链路"的表述随之更新。
- **FR-014**: `scripts/validate-skills.py` 更新：`GRILL_ME_REQUIRED_TEXT` 中的 ``推荐 `$to-prd` ``/``推荐 `$to-issues` `` 改为对应 `$to-spec`/`$to-plan` 文本；新增 stale-text 检查将 `$to-prd`、`$to-issues` 的引用视为过期措辞（仅作用于 SKILL.md、README.md、AGENTS.md，不扫描 `docs/features/` 历史产物）。
- **FR-015**: 新 skill 的 `agents/openai.yaml` 满足既有约束：`display_name`、`short_description`（25–64 字符）、`default_prompt`（单行引号、引用 `$to-spec`/`$to-plan`）；`SKILL.md` 包含完整语言契约 marker 与例外句。
- **FR-016**: `to-spec` 负责创建/更新 feature manifest，artifact 清单为 `spec.md`、`plan.md`、`analysis.md`（原 `Issues` 行移除）；`to-plan` 完成后更新 manifest 中 Plan 状态。
- **FR-017**: 父仓库 `CLAUDE.md`（skill-development 根目录）中 canonical chain、validator 失败项列表和 Natural Handoff 规则描述同步更新为 spec/plan 术语。

## 成功标准 (Success Criteria)

- **SC-001**: 在 `submodules/fjxyyzg3-Skills` 内运行 `python scripts/validate-skills.py` 退出码为 0，且新 skill `to-spec`、`to-plan` 被纳入校验。
- **SC-002**: `grep -r "to-prd\|to-issues"`（排除 `docs/features/` 历史产物与 `.git`）在 skill 库内零命中。
- **SC-003**: 按 `workflow-router` 路由表人工核对："整理成 spec"与"拆成 plan"两个场景各只命中一个 skill，无旧入口残留。
- **SC-004**: 用一个真实需求人工试跑一次 `to-spec -> to-plan`，产物字段齐全（FR/SC ID、Covers、文件路径、接口契约、验收标准、验证命令、coverage 自查表），且 plan 中无实现代码与并行字段。
- **SC-005** (post-launch metric): 日常 feature 开发默认走 spec -> plan 链路，不再感觉需要绕过或手工裁剪 issue 机制。

## 实现决策 (Implementation Decisions)

- 两段式 artifact：spec 承担"要什么、为什么、边界与验收"，plan 承担"改哪里、接口是什么、怎么验证"；"plan 决定分解、implement 决定代码"是硬分界。
- 稳定 ID 契约保留：`FR-###`/`SC-###` 由 spec 定义，plan task 用 `Covers` 追溯，`analyze` 与 `verification-before-completion` 继续以此为锚点。
- plan 为单 Markdown 文件而非目录：串行 task 列表天然有序，不需要 index 文件、依赖图和波次表。
- 并行能力收缩为"只读探索"：implement 仍可派 subagent 做只读 spike，但不再有按 wave 并行落地实现的模式。
- 删除而非弃用：单人库无兼容对象，git 历史即过渡期；旧引用由 validator 的 stale-text 检查防回归。
- 语言契约与既有 workflow contract 字段规范（中文主文 + 英文字段名/ID）对新 skill 完全沿用。

## 测试决策 (Testing Decisions)

- Verification seam（验证切入点）: `python scripts/validate-skills.py` 全量校验 + 仓库级 grep 残留检查（SC-002）+ 人工试跑一次 `to-spec -> to-plan`（SC-004）。
- Prior art（现有依据）: validator 已有的 frontmatter/openai.yaml/语言契约/stale-text 检查框架，本次只扩展常量与检查目标，不改校验架构。
- Manual fallback（手动兜底）: 逐文件人工 review `workflow-router`、`implement`、`analyze` 的改写段落，确认没有残留 issue/wave 语义的孤句。

## 风险和开放问题 (Risks and Open Questions)

- **Risk**: validator 常量与 `grill-me/SKILL.md`、`workflow-router/SKILL.md`、`README.md`、`AGENTS.md` 的契约文本必须在同一提交中改齐，否则 `validate-skills.py` 立即失败；实现顺序上应最后统一跑校验。
- **Risk**: `implement/SKILL.md` 中 issue 领取、wave 执行、并行确认的措辞散布在多个节点（C1、N4、N5、N6 等），需要系统性重写决策树而不是字符串替换，容易漏改造成自相矛盾的流程图。
- **Risk**: `analyze` 删除依赖/并行检查后，其 severity 分级和报告模板中相关条目需要同步收缩，避免报告模板引用不存在的检查维度。
- **Open Question**: 用户本机 `~/.claude/skills/` 下安装的 skill 副本（如本次会话使用的 grill-me、to-prd）与仓库源的同步机制不在本仓库范围内；替换落地后需要用户自行更新安装副本，否则旧 skill 仍会被触发。
- **Open Question**: `find-skills` 等外部技能发现机制如何看待新旧 description 的语义重叠（`to-plan` 的 description 需避免与已删除的 `to-issues` 描述雷同以致误触发历史习惯用语），在写 description 时需要一次性斟酌。

## Issue 拆分交接说明 (Handoff Notes for Issue Breakdown)

- 推荐 vertical slice 维度：(1) 新建 `to-spec`（含 openai.yaml 与 manifest 职责）；(2) 新建 `to-plan`；(3) 删除旧 skill 并更新 `workflow-router`/`brainstorming`/`grill-me`/`quick-change` 引用 + validator 常量（必须同片完成，见 Risk）；(4) 重写 `implement` 决策树；(5) 改造 `analyze`；(6) 更新 `README.md`/`AGENTS.md` 与父仓库 `CLAUDE.md`。
- 高风险 dependencies：切片 (3) 是链条断点——validator、grill-me、router 三者互锁，必须原子提交；切片 (4)(5) 依赖 (2) 定稿的 plan 模板字段名。
- 需要 human-gate 的决策：`implement` 决策树重写后的流程图需人工 review（Risk 第二条）；新 skill 的 description 措辞（Open Question 第二条）建议写完后给用户过目一次。
