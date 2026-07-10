# Adaptive Planning Contract v1

本文件是 `$to-plan` 自适应 planning 行为的 single source of truth。每次 Planning Run 必须读取并执行本 contract。

## 目录

- PlanningAuthorization
- RiskDecision
- PlanningArtifactSet
- FindingClass
- PlanningQualityResult
- CheckedPlanHandoff

## PlanningAuthorization

| Field | Required | Contract |
| --- | --- | --- |
| `Source` | Yes | 显式 `$to-plan`，或上一条唯一推荐 `$to-plan` 后的自然确认 |
| `AllowedActions` | Yes | 读取相关上下文；写本地 planning artifacts；修复 Artifact-fixable findings；重新检查 |
| `ForbiddenActions` | Yes | 修改业务代码/测试；branch、commit、push、PR、merge、discard；远端操作 |
| `ResumeToken` | Yes | Decision-required 问题回答后恢复同一 Planning Run，不重新授权 |
| `StopBoundary` | Yes | checked plan 完成或 Decision-required 尚未解决 |

自然确认只绑定上一条回复中唯一推荐的 `$to-plan`。上一条有多个选项或用户附加了改变方向的条件时，先重新路由。

## RiskDecision

输出字段：

| Field | Type | Contract |
| --- | --- | --- |
| `PlanningMode` | `Fast | Full` | 最终选择 |
| `Evidence` | `list[string]` | 命中的仓库或需求事实，至少一项 |
| `Conflicts` | `list[string]` | 互相冲突或无法确认的分类证据；无则 `None` |
| `UserOverride` | `Fast | Full | None` | 用户可以显式要求 Full；显式 Fast 仍不能覆盖 Full trigger |

Fast Path 必须同时满足：

1. 设计方向已确认，目标单一且边界清楚。
2. 不改变 public API、schema、migration、权限、安全或数据生命周期。
3. 不跨 repository 或多个相互独立的 subsystem。
4. acceptance criteria 与 verification seam 已明确。
5. 没有会改变实现方向的开放决策。

Full Path 命中任一项即可：

1. 输入已有 spec，或用户明确要求正式 spec / decision artifact。
2. 改变 public contract、schema、持久化结构或核心 workflow。
3. 涉及 compatibility、migration、权限、安全或数据丢失风险。
4. 跨多个 module/repository，且需要稳定接口交接。
5. 包含多个相互依赖的用户流程或 rollout 阶段。
6. 关键 non-goal、acceptance 或 architecture decision 需要长期固化。

证据冲突或无法可靠分类时，停止写入并只问一个最高优先级问题。

## PlanningArtifactSet

路径按以下优先级确定：

1. 用户指定 artifact 路径时使用该路径。
2. 输入 spec 位于 `docs/features/<feature-slug>/spec.md` 时，在同目录写 `plan.md`。
3. 项目已有 feature workspace 约定时，写入 `docs/features/<feature-slug>/`。
4. 没有项目约定的独立 fixture 或目录任务，在用户指定的工作目录写 `plan.md`；Full Path 同目录写 `spec.md`。路径仍无法可靠确认时才提出一个阻塞问题。

### Fast

- 只创建或更新 `plan.md`。
- 不创建 `spec.md`、`analysis.md` 或新的 `manifest.md`。
- plan 必须包含 `Planning Mode: Fast`、risk rationale、稳定 `FR-###`、assumptions、global constraints、顺序 tasks、coverage self-check 和 `Planning Quality Status`。

### Full

- 在同一 Planning Run 内创建或更新 `spec.md` 与 `plan.md`。
- spec 与 plan 使用完全相同的 `FR-###` 集合；已有 spec 时复用其 IDs，不重新编号。
- 不创建 `analysis.md`。
- 只更新已经存在的 `manifest.md`；没有项目惯例或现有文件时不强制创建。

### TaskSchema

每个 task 都必须包含：

| Field | Contract |
| --- | --- |
| `Files` | 精确到真实路径，并标记 Create/Modify/Test |
| `Consumes` | 前置产出的精确名称与类型；无则 `None` |
| `Produces` | 后续依赖的精确名称、签名、字段或 artifact；无则说明最终 observable outcome |
| `Covers` | 一个或多个 `FR-###`，或明确的 conversation requirement |
| `Acceptance Criteria` | 可独立判断的 external behavior / artifact outcome |
| `Verification` | 当前环境可执行的命令或明确 manual/static seam 与预期结果 |

## FindingClass

### Artifact-fixable

仅包括不改变需求语义、且可由 source 或 contract 唯一确定的修复：

- coverage table 或 task 必需字段遗漏。
- source 可确认的路径/命令错误。
- `Consumes/Produces` 命名或类型没有逐字对齐。
- 既有 manifest 状态错误、模板残留、编号或格式错误。

处理：自动修复，记录摘要，并从完整 quality gate 起点重新检查。若修复会改变 scope、acceptance、compatibility、migration 或 architecture，重新分类为 Decision-required。

### Decision-required

包括需要人类选择或缺少不可从仓库确认的业务事实：

- requirement、scope 或 acceptance 互相冲突。
- 存在多个会实质改变行为的 architecture 选择。
- compatibility、migration、安全或数据取舍不明确。
- 关键业务事实缺失，无法形成真实 task 或 verification seam。

处理：按影响排序，只问一个最高优先级问题；回答后恢复同一 Planning Run。

## PlanningQualityResult

| Field | Type | Contract |
| --- | --- | --- |
| `RequirementsCoverage` | `Pass | Fail` | 每条 `FR-###` 至少映射一个 task 与 verification seam |
| `TaskCompleteness` | `Pass | Fail` | 每个 task 的 TaskSchema 字段完整 |
| `ContractConsistency` | `Pass | Fail` | 相邻 `Consumes/Produces` 逐字一致，无悬空接口 |
| `RepositoryFeasibility` | `Pass | Fail` | 路径、命令和既有 interface 与仓库事实一致 |
| `ConstraintAlignment` | `Pass | Fail` | non-goals、global constraints 和安全边界已保留 |
| `AutoFixSummary` | `list[string]` | 自动修复项；无则 `None` |
| `ResidualRisks` | `list[string]` | 未阻塞但需实现阶段保留的风险；无则 `None` |
| `Planning Quality Status` | `Pass | Decision required` | 只有前五项全部 Pass 且无未决 finding 时为 Pass |

## CheckedPlanHandoff

只有 `Planning Quality Status: Pass` 才能产生：

| Field | Contract |
| --- | --- |
| `PlanningMode` | `Fast | Full` |
| `ArtifactPaths` | plan 路径；Full 时同时列出 spec 路径 |
| `Coverage` | `FR-### -> Task -> Verification` 摘要 |
| `QualityStatus` | 必须为 `Planning Quality Status: Pass` |
| `AutoFixSummary` | 本次自动修复；无则 `None` |
| `Assumptions` | 仍成立的实现假设 |
| `ResidualRisks` | 非阻塞风险；无则 `None` |
| `NextSkill` | implementation-ready 时最多为 `$implement`，否则 `none` |

`CheckedPlanHandoff` 只证明 planning artifact 已检查，不批准 branch、业务代码、测试、review、verification、commit 或 push 动作。
