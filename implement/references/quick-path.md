# Quick Path

本 reference 是 `$implement` 的 `ImplementationPathDecision v1` schema，以及 Quick Path qualification、execution、escalation 与 result contract 的 single source of truth。`N0A Read-only Path Dispatch` 对所有候选路径读取 decision schema；只有 Quick candidate 继续读取完整 Quick playbook，Blocked 只读取对应 escalation，Standard 不加载 Quick execution 细节。完整 playbook 不应复制回主 `SKILL.md`。

## Contents

- [ImplementationPathDecision v1](#implementationpathdecision-v1)
- [Qualification](#qualification)
- [Disqualifiers](#disqualifiers)
- [Quick Execution](#quick-execution)
- [Quick→Standard](#quickstandard)
- [Blocked Escalation](#blocked-escalation)
- [Result](#result)
- [Completion](#completion)

## ImplementationPathDecision v1

在 branch 操作和文件写入前记录：

| Field | Contract |
| --- | --- |
| `Path` | `Quick | Standard | Blocked` |
| `Evidence` | 支持当前 path 的 repository facts、risk facts 与 verification facts |
| `Scope` | 用户已授权的 implementation boundary；Quick 为唯一 tight change，Standard 可为 checked task set，Blocked 记录尚未收束的 gap |
| `Acceptance` | 可独立判断的完成条件；Blocked 记录缺失的 acceptance decision |
| `Verification` | 预期先失败或稳定暴露症状、实现后通过的 seam/set；Blocked 记录缺失的 evidence seam |
| `EscalationReason` | `Standard` 或 `Blocked` 的原因；没有时为 `None` |

Quick contract 使用以下三行：

```text
Scope:
Acceptance:
Verification:
```

任一行无法明确填写时，不得选择 Quick。

## Qualification

Quick 必须同时满足：

- 只有一个 tight change，`Scope` 与 `Acceptance` 均可用一句话表达。
- 风险低，不需要多个 implementation task，也不需要产品、设计或 architecture 决策。
- 已有可靠快速的 pass/fail seam，或能在约 10–15 分钟内建立。
- 不改变 public/shared contract、schema、migration、权限、安全、计费、数据生命周期或 core workflow。
- 不需要跨模块协调或独立 rollout/migration。
- 预计只涉及少量局部文件是正向 heuristic，但文件数不是单独判据；一个文件也可能属于 Standard。

选择 Quick 时，`Evidence` 必须逐项说明上述条件为何成立，不能只写“改动很小”。

## Disqualifiers

命中任一项，不能选择 Quick：

- 输入是 checked multi-task plan。
- 修改 shared/public contract、schema、migration 或 core workflow。
- 需要多个 behavior slice、跨模块协调、中高风险验证或独立 review。
- acceptance、产品方向或 architecture 边界仍需用户决策。
- bug 在约 10–15 分钟内无法建立可信 failing signal 或等价 repro。
- external artifacts 未检查、失效或与 repository facts 不一致；这类输入在 executable scope 与 authorization 清楚时进入 Standard 的 `N3 Analyze Gate`。
- implementation authorization 或 scope 尚不明确。current/new branch 的选择由主 skill 的 `N1 Branch Gate` 处理，不影响写入前的 path dispatch。

如果 scope、acceptance 与 implementation authorization 已明确，但仅因复杂度、风险或 artifact quality 不符合 Quick，选择 `Standard`；若这些授权边界本身不明确，选择 `Blocked`。

## Quick Execution

1. 通过主 skill 的 `N1 Branch Gate`，记录 existing changes 边界。
2. 写下 `Scope / Acceptance / Verification` 三行 contract。
3. 对 bug 先运行 targeted failing test、稳定暴露症状的等价 repro 或 command。
4. 对无法自动化的文档、metadata 或静态 contract，先运行会证明 marker/path 缺失的 static RED。
5. 只做满足当前 acceptance 所需的最小实现。
6. 运行 targeted GREEN；必要时补最邻近的 regression check。
7. 执行 light self-review：
   - diff 是否只覆盖 Scope。
   - 是否遗漏直接相关 edge case。
   - existing/user changes 是否保持不动。
   - verification 是否真正证明 Acceptance。
   - 是否已经触发 Standard 或 Blocked 条件。
8. 进入主 skill 的共享 `N7 Verification Gate`。

Quick 默认不启动独立 review subagent；一旦风险或验证需要独立 review，应按升级规则进入 Standard。

## Quick→Standard

以下条件全部成立时，在同一 `$implement` 内从 Quick→Standard：

- 原 `Scope`、`Acceptance` 与 branch authorization 均不变。
- 新发现的是实现复杂度、shared contract/core workflow 影响、multi-task 需求或更宽验证需求。
- 仍有明确可执行目标，不需要新的产品或 architecture 决策。

升级时：

- 在 `EscalationReason` 记录证据。
- 直接进入主 skill 的 `N2 Standard Input Intake`。
- 不重复 `N1 Branch Gate`。
- 补齐 serial tasks、独立 review subagent 和更宽 verification。
- 不产生一次指向 `$implement` 自身的 Natural Handoff。

## Blocked Escalation

- bug 缺少可靠 pass/fail seam：停止写入，唯一推荐 `$diagnose`。
- scope 已确认但需要 checked multi-task plan：停止写入，唯一推荐 `$to-plan`。
- acceptance、产品或 architecture 边界不清：停止写入，唯一推荐 `$brainstorming`。

一次只能根据当前 blocker 推荐一个 next skill。自然确认不扩大 scope，也不授权 branch、code、commit、push 或 PR。

## Result

```markdown
## Implementation Path

- Path: Quick
- Evidence:
- Scope:
- Acceptance:
- Verification:
- EscalationReason: None

## Result

- Changed:
- RED:
- GREEN:
- Light review:
- Final verification:
- Skipped:
- Risk:
```

## Completion

- [ ] 所有 Quick qualification 均有 evidence，且无 disqualifier。
- [ ] branch gate、三行 contract 与 existing-change boundary 已记录。
- [ ] targeted signal 在实现前失败或稳定暴露缺口。
- [ ] minimal change 后 targeted verification 通过。
- [ ] light self-review 未发现 scope drift 或升级条件。
- [ ] 共享 final verification 已通过。
