---
name: to-plan
description: "当需要把已确认设计、既有 spec/design doc 或对话上下文转成经过检查的 implementation plan 时使用；自动选择 Fast 或 Full planning、写入所需本地产物、闭环 Artifact-fixable findings，并保留实现安全门；保留英文触发短语 confirmed design、existing spec 和 checked implementation plan。"
---

# To Plan

产出经过一致性检查、可直接交给实现阶段的 checked plan。根据风险选择 Fast Path 或 Full Path，在一次 Planning Run 内完成所需 artifacts、机械修复和 quality gate；不要把风险分类、spec 生成和 artifact analysis 拆成默认的多次 handoff。

## 进入边界

- 适用于已确认设计、已有 spec/design doc 或方向明确的 conversation context，需要形成 implementation plan 的任务。
- 可以由用户显式调用，也可以由当前 context trigger 或上一轮 `Natural Handoff` 唯一推荐后进入。
- 用户只要求正式 spec 或 decision artifact 时使用 `$to-spec`；只要求审查已有/外部 artifacts 时使用 `$analyze`。
- 已可直接实施的任务使用 `$implement`，由它在写入前选择 Quick/Standard/Blocked；不需要先生成 plan。

## 触发说明（Trigger Description）

`to-plan` 的 trigger 是把已成形的需求来源转成本地 checked plan。每次进入都创建一个 Planning Run：自动选择 Fast Path 或 Full Path，写入对应 artifacts，闭环 Artifact-fixable findings，并输出 `Planning Quality Status`。只有可信 source、风险分类或需求决策确实不足时，才一次问一个阻塞问题。

## 压力场景（Pressure Scenarios）

1. 用户确认设计，并对唯一的 `$to-plan` 推荐回复“继续”。
   - 预期触发：把该确认解释为一次 Planning Authorization，连续完成风险分类、artifact 写入和 quality gate。
   - 未使用本 skill 时的常见失败：再要求用户分别确认 `$to-spec`、`$to-plan` 和 `$analyze`。
   - 本 skill 必须强制的行为：checked plan 完成前不产生中间 skill handoff。
2. 一个看似很小的请求改变了 public contract、schema、migration、安全边界或核心 workflow。
   - 预期触发：命中任一高风险证据即选择 Full Path，并说明依据。
   - 未使用本 skill 时的常见失败：只按文件数量判断为 Fast Path，丢失长期决策记录。
   - 本 skill 必须强制的行为：在同一 Planning Run 内生成共享 `FR-###` 的 `spec.md` 与 `plan.md`。
3. 生成的 plan 缺少 coverage row，或包含可由源码核实的路径拼写错误。
   - 预期触发：分类为 Artifact-fixable，自动修复并重新检查。
   - 未使用本 skill 时的常见失败：把机械问题逐项交给用户确认，或直接把未检查 plan 交给实现。
   - 本 skill 必须强制的行为：只有改变 scope、acceptance、compatibility 或 architecture 的问题才暂停为 Decision-required。
4. 用户要求 planning 同时编辑代码、创建分支或推送改动。
   - 预期触发：完成本地 planning artifacts 后停在实现之前。
   - 未使用本 skill 时的常见失败：把一次 planning 确认扩张成 implementation 或 Git 授权。
   - 本 skill 必须强制的行为：通过新的 `Natural Handoff` 最多推荐 `$implement`，保留其全部安全门。

## 规划授权

用户显式调用 `$to-plan`，或自然确认上一条唯一推荐的 `$to-plan`，即创建一次 `Planning Authorization` 并授权一次 Planning Run。该授权允许读取与已确认设计直接相关的上下文、写入本地 planning artifacts、修复 Artifact-fixable findings 并复检。

该授权的停止边界是 checked plan：业务代码和测试修改、branch 操作、commit、push、PR、merge、discard 与远端操作仍需各自 workflow 的明确授权。遇到 Decision-required finding 时暂停并只问一个最高优先级问题；用户回答后恢复同一 Planning Run，无需重新授权。

## 必读契约

- 每次 Planning Run 都必须读取 [`references/adaptive-planning-contract.md`](references/adaptive-planning-contract.md)，按其中的风险矩阵、artifact schemas、finding taxonomy 和 quality gate 执行。
- 验证行为、修改 adaptive contract 或判断边界案例时，读取 [`examples/adaptive-planning-scenarios.md`](examples/adaptive-planning-scenarios.md)，逐项核对对应 scenario 的 pass signal。

## 工作流程

### 1. 收集可信来源

优先读取用户指定的 spec、design doc 或 brainstorming handoff。没有明确路径时，从当前 conversation context 和 `docs/features/` 中寻找最相关 artifact；读取与拆分直接相关的项目规则、代码、测试和接口说明，确认真实路径与 verification seam。

如果缺少可信 source、目标 feature 无法识别，或一个关键事实会改变需求方向，暂停并只问一个阻塞问题。其余不确定项写入 `Assumptions` 或 `Residual Risks`。

### 2. 选择规划模式

按 contract 的确定性风险矩阵分类：

- 已有 spec 时选择 Full Path，并复用其稳定 `FR-###`。
- 只有 conversation context 时，Fast 条件必须全部成立；任一 Full trigger 命中即选择 Full Path。
- 只在证据互相冲突或无法可靠分类时暂停询问。

首次状态更新用一句话报告 `Planning Mode: Fast | Full` 和至少一个可审计依据。

### 3. 写入产物

- Fast Path：只写一个自包含 `plan.md`；不要新建 `spec.md`、`analysis.md` 或 `manifest.md`。
- Full Path：在同一 Planning Run 内写 `spec.md` 与 `plan.md`，两者使用完全相同的 `FR-###`；不要生成 `analysis.md`。
- feature workspace 已有 `manifest.md` 时更新状态和路径；不存在时不要仅为本流程创建。

plan 的 task 按执行顺序编号。每个 task 必须有精确 `Files`、`Consumes`、`Produces`、`Covers`、验收标准和 verification command；契约只写到稳定字段或签名层，不预写实现代码。

### 4. 运行内建规划质量门

检查全部 requirement coverage、task completeness、相邻 `Consumes/Produces`、真实路径与既有 interface、verification commands、non-goals 和 global constraints。

- Artifact-fixable：在当前 Planning Run 内修复 artifact 并从头复检，直到通过或重新分类。
- Decision-required：暂停，报告影响并只问一个最高优先级问题；收到回答后更新 artifacts 并复检。

只有所有检查通过，才能写入 `Planning Quality Status: Pass`。存在未决问题时使用 `Planning Quality Status: Decision required`，不要把 plan 标为 implementation-ready。

### 5. 最终汇报

quality gate 通过后只做一次最终汇报，包含：

- Planning Mode 与风险依据。
- artifact 路径。
- `FR-### -> Task -> Verification` coverage 摘要。
- auto-fix 摘要、assumptions 和 residual risks。
- `Planning Quality Status`。

## 自然交接（Natural Handoff）

checked plan 达到 implementation-ready 且没有阻塞问题时，最多推荐 `$implement` 作为唯一 next skill。说明用户的自然确认只进入 `$implement`，不会绕过它的 branch、scope、review、verification、commit 或 push gate。用户只要求 planning artifacts 时推荐 `none`。

## 完成标准

- 已报告确定的 Planning Mode 和可审计风险依据。
- artifacts 数量与 mode 一致，Full Path 的 spec/plan 共享相同 `FR-###`。
- 每条 requirement 都映射到 task 和 verification seam；每个 task 的必需字段完整。
- 所有 Artifact-fixable findings 已闭环，Decision-required findings 已解决或明确停住。
- 最终 artifact 包含 `Planning Quality Status`，且最终汇报只出现一次。
- Planning Run 没有越过本地 planning artifact 的授权边界。
