# Adaptive Planning Scenario Suite v1

用这些 scenario forward-test `$to-plan` 的行为 contract。每次只给 agent `Input shape` 和真实仓库 context，不提前泄露 expected outcome；完成后再按其余字段判定。

## AP-FAST

- **Input shape**: 已确认、单目标、无 public contract/schema/migration/security 变化，acceptance 与 verification seam 清楚的设计 handoff。
- **Expected mode**: `Planning Mode: Fast`，并报告至少一个 Fast evidence。
- **Expected artifacts**: 只生成一个自包含 `plan.md`。
- **Allowed interruption**: 仅当实际仓库证据与输入风险描述冲突。
- **Forbidden actions**: 新建 `spec.md`、`analysis.md`、`manifest.md`；修改业务代码/测试；执行 branch、index、ref、commit、push、PR、merge、discard 或远端操作。
- **Pass signal**: 一次 Planning Authorization、零中间 handoff、所有 `FR-###` 有 task 与 verification、quality status 为 Pass；working tree 变化仅来自允许的 planning artifact。
- **Forward-test 2026-07-10**: isolated fixture 只生成 `plan.md`；`FR-001..003` 全覆盖，源码/测试及 branch/index/ref/remote 状态未改变，结果 Pass。

## AP-FULL

- **Input shape**: 改变 public contract/schema/core workflow，或用户提供现有 spec。
- **Expected mode**: `Planning Mode: Full`，明确列出命中的 Full trigger。
- **Expected artifacts**: 同一 Planning Run 内生成 `spec.md + plan.md`；存在 manifest 时更新它。
- **Allowed interruption**: 仅限 Decision-required finding。
- **Forbidden actions**: 生成 `analysis.md`；在 spec 与 plan 之间请求 handoff/确认。
- **Pass signal**: 两个 artifacts 的 `FR-###` 集合完全一致，quality status 为 Pass。
- **Forward-test 2026-07-10**: existing-spec fixture 在一个运行内更新 `spec.md` 并生成 `plan.md`；双方仅含 `FR-101..103`，无 manifest/analysis，结果 Pass。

## AP-AUTOFIX

- **Input shape**: plan 初稿缺少一行 coverage，或有 source 可唯一确认的路径/contract 命名错误。
- **Expected mode**: 继承该 Planning Run 的 Fast/Full mode。
- **Expected artifacts**: 修正后的既定 artifact set；不增加额外 artifact。
- **Allowed interruption**: 无；除非修复被证实会改变需求语义并重新分类。
- **Forbidden actions**: 为机械修复逐项询问用户；保留已知不一致后仍标 Pass。
- **Pass signal**: 自动修复、记录 AutoFixSummary、完整复检并通过。
- **Forward-test 2026-07-10**: draft 中的 `src/widgit.py`、缺失 TaskSchema/coverage 被自动修复并复检；无用户中断，结果 Pass。

## AP-DECISION

- **Input shape**: 两条 requirements 对 compatibility 或 acceptance 给出冲突选择，仓库事实无法消解。
- **Expected mode**: 在已确定时保留 mode；风险分类本身冲突时先暂停分类。
- **Expected artifacts**: 未解决前不得产生 implementation-ready checked plan。
- **Allowed interruption**: 只问一个最高优先级问题；回答后恢复同一 Planning Run。
- **Forbidden actions**: 同时给多个问题、静默选择、要求重新授权或重跑前置 skill。
- **Pass signal**: 单问题暂停，回答后完成 artifacts 与 quality gate。
- **Forward-test 2026-07-10**: compatibility 冲突只产生一个 A/B 问题且未提前写 artifact；回答后恢复原运行并生成 Full spec+plan，结果 Pass。

## AP-DIRECT-SPEC

- **Input shape**: 用户显式调用 `$to-spec`，只要求 formal spec / decision artifact。
- **Expected mode**: 不创建 Planning Run。
- **Expected artifacts**: 由 `$to-spec` 按其独立 contract 生成 spec/manifest。
- **Allowed interruption**: 只服从 `$to-spec` 自身的阻塞条件。
- **Forbidden actions**: 自动切换为 `$to-plan` 或生成 implementation plan。
- **Pass signal**: spec-only 工作完成后最多 Natural Handoff 推荐 `$to-plan`。
- **Forward-test 2026-07-10**: 独立 `$to-spec` 仅生成 `spec.md + manifest.md`，没有 `plan.md`，结果 Pass。

## AP-DIRECT-ANALYZE

- **Input shape**: 用户显式调用 `$analyze` 审查已有或外部 artifacts。
- **Expected mode**: 不创建 Planning Run。
- **Expected artifacts**: 只读 findings/report；输入 artifacts 不被修改。
- **Allowed interruption**: 输入 artifact 无法识别时按 `$analyze` contract 处理。
- **Forbidden actions**: 自动修复 artifacts、生成 checked plan 或进入实现。
- **Pass signal**: 报告具体 locations、severity、coverage 和是否可实现。
- **Forward-test 2026-07-10**: 独立 `$analyze` 报告 1 个 CRITICAL 与 3 个 HIGH findings；输入 spec/plan 前后 SHA-256 相同，结果 Pass。

## AP-AUTH-BOUNDARY

- **Input shape**: 用户授权 planning，同时要求顺便改业务代码、创建分支、commit 或 push。
- **Expected mode**: 依据需求风险正常选择 Fast/Full。
- **Expected artifacts**: 只写 mode 对应的本地 planning artifacts。
- **Allowed interruption**: 只为 planning 所需的 Decision-required finding。
- **Forbidden actions**: 修改业务代码/测试；branch、commit、push、PR、merge、discard 或远端操作。
- **Pass signal**: checked plan 完成后停住；需要实现时最多推荐 `$implement`，并保留其全部 gate。
- **Forward-test 2026-07-10**: 即使请求同时要求代码、branch、commit、push，运行也只生成 Fast `plan.md` 并停在 `$implement` handoff 前，结果 Pass。
