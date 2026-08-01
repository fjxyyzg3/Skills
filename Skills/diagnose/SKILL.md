---
name: diagnose
description: "用于诊断具体的 Generic 或 Unreal Engine 故障，包括 bug、crash、回归、错误输出、flaky behavior 与性能下降；通过 Active Repro 或 Artifact-based Triage、可证伪假设、targeted probes 和 regression seam 严格收敛。"
---

# 诊断

统一诊断 Generic 与 Unreal Engine 症状。先记录 Profile 与 Evidence Mode，再沿同一套 six-phase protocol 收敛 evidence、root cause 和 regression seam；不要把无法运行的 artifact 分析包装成已复现，也不要在本 skill 内提交持久修复。

探索代码库时，先读取相关 domain glossary、ADR 和用户点名的 concrete artifacts，建立与实际 runtime path 一致的心智模型。

## 进入边界

- 适用于 concrete bug、failing test、crash、assert、wrong output、flaky behavior、performance regression，以及 UE 的 PIE/Standalone/Cooked/Packaged/Shipping、Blueprint、asset/load/cook、network、rendering、memory 或 platform-only failure。
- 用户显式调用、当前 context 命中本 skill description，或上一轮唯一 `Natural Handoff` 被自然确认时，都可以直接进入。
- 本 skill 只产出 diagnosis、evidence、repair direction、regression seam 与一个可选 handoff；不提交持久业务代码修改。
- UE API 教学、普通代码解释、新功能设计和纯 code review 不属于本 skill。

## 触发说明（Trigger Description）

`diagnose` 是唯一 diagnosis entry，并沿两个正交轴选择执行上下文：

- `Profile: Generic | UE`
- `EvidenceMode: Active Repro | Artifact-based Triage`

Generic/UE 决定 domain runtime 与 progressive-disclosure references；Active/Artifact 决定可声明的 evidence strength。UE 不等于 Artifact，Generic 也不等于 Active。

## 压力场景（Pressure Scenarios）

1. `DGN-GENERIC-ACTIVE`: 普通 failing test 或 CLI/API/UI bug，当前环境能稳定运行。
   - 预期上下文：`Generic + Active Repro`。
   - 禁止动作：加载或输出无关 UE workflow。
   - 通过信号：精确 failure 被观察后才进入 hypotheses。
2. `DGN-GENERIC-ARTIFACT`: 只有 log、core dump、trace 或截图，无法运行原系统。
   - 预期上下文：`Generic + Artifact-based Triage`。
   - 禁止动作：声称已复现或 `RootCauseStatus: confirmed`。
   - 通过信号：facts、inferences、3–5 个 hypotheses、probes 与 missing evidence 分离。
3. `DGN-UE-ACTIVE`: UE PIE、Packaged、Blueprint、cook、network、rendering 或 platform symptom，当前工程可运行。
   - 预期上下文：`UE + Active Repro`。
   - 禁止动作：不记录 runtime mode 就开始猜代码。
   - 通过信号：运行形态、精确症状、复现率和适用 UE references 均有证据。
4. `DGN-UE-ARTIFACT`: 只有 UE log、callstack、CrashContext、minidump、trace、capture 或 asset。
   - 预期上下文：`UE + Artifact-based Triage`。
   - 禁止动作：把 artifact inspection 写成“已复现”。
   - 通过信号：最小缺料与每个 hypothesis 的下一 probe 明确。
5. `DGN-UE-MODE-DRIFT`: 症状只在 Packaged、RHI、network 或特定 platform 出现，但当前只验证了 PIE。
   - 预期上下文：保持未验证状态。
   - 禁止动作：宣称 repair verified。
   - 通过信号：要求在相同 runtime mode 运行 regression seam。
6. `DGN-PERF-BASELINE`: 性能回退但 map、view、RHI、resolution、scalability 或 sample window 未固定。
   - 预期上下文：先固定 baseline。
   - 禁止动作：先改代码再寻找指标。
   - 通过信号：measurement contract 可重复且能比较 before/after。
7. `DGN-HANDOFF`: repair scope 与正确 regression seam 已可执行。
   - 预期上下文：唯一 next skill 为 `$implement`。
   - 禁止动作：同时给多个 repair entry，或把 architecture observation 变成第二个 next skill。
   - 通过信号：handoff packet 包含 context、root-cause status、seam、repair direction、risk 与 missing evidence。

## 诊断上下文

本节定义 `DiagnosticContext v1`：

Phase 1 前记录：

| Field | Contract |
| --- | --- |
| `Profile` | `Generic | UE` |
| `EvidenceMode` | `Active Repro | Artifact-based Triage` |
| `ObservedFailure` | 当前 observation status 与精确目标症状/artifact facts；Active 首次进入可记录 `pending — <target failure>` |
| `RuntimeMode` | UE 时记录 Editor/PIE/Standalone/Cooked/Packaged/Shipping、server/client、platform、RHI 与 build configuration；Generic 可为 `N/A` |
| `RootCauseStatus` | `confirmed | likely | blocked`；初始只能为 `likely` 或 `blocked` |
| `RegressionSeam` | 正确 test、repro 或 command seam；没有时说明 gap |
| `MissingEvidence` | 仍需的最小材料；无则 `None` |

### Profile 分派

- 用户明确描述 Unreal Engine、Editor、PIE、Cooked、Packaged、Shipping、Blueprint、RHI 等症状，或 repository facts 与症状共同指向 UE runtime path 时，选择 `Profile: UE`。
- 其他问题选择 `Profile: Generic`。
- `Profile: Generic` 不读取或输出 UE references。
- `Profile: UE` 按需读取同一 skill 目录下的 references：
  - runtime 依赖时读取 [references/ue/runtime-modes.md](references/ue/runtime-modes.md)。
  - 选择 UE hypothesis、probe 或 artifact 时读取 [references/ue/probes-and-artifacts.md](references/ue/probes-and-artifacts.md)。
  - 定义 UE regression seam 与 repair handoff 时读取 [references/ue/regression-seams.md](references/ue/regression-seams.md)。

### 证据模式分派

- 当前 agent 能建立并运行或结构化指导 feedback loop 时，选择 `Active Repro`；首次进入尚未观察到目标 failure 时，把 `ObservedFailure` 记录为 `pending`，并把初始 `RootCauseStatus` 设为 `blocked`。
- 只有 concrete log、callstack、trace、capture、截图、asset 或类似 artifact，无法运行原场景时，选择 `Artifact-based Triage`。
- Artifact-based Triage 必须明确“未复现”；可以提出 hypotheses 与 probes，但 `RootCauseStatus` 不得为 `confirmed`，只能为 `likely` 或 `blocked`。
- 既无可信 loop、又无足够 artifact 时停止，请求最小材料，不进入猜测性 diagnosis。
- 后续获得运行环境时，可以从 Artifact-based Triage 转入 Active Repro，并更新 `DiagnosticContext v1`。

## Phase 1 — 建立反馈循环

### Active Repro 模式

建立快速、确定性、agent 可运行或可结构化指导的 pass/fail signal。按最接近 external behavior 的顺序尝试：

1. failing unit/integration/e2e/automation test。
2. Curl、HTTP、CLI 或 fixture/snapshot differential。
3. Headless browser、captured trace replay 或 throwaway harness。
4. property/fuzz、bisection 或 old/new differential loop。
5. 无法自动化时使用 `scripts/hitl-loop.template.sh`，固定每轮输入、操作和回传 artifact。

让 loop 更快、更尖锐、更确定：缩小 setup、断言精确症状、固定时间/RNG/filesystem/network。非确定性 bug 的目标是提高复现率并记录 N 次中 M 次。

`Profile: UE` 还必须记录正确 runtime mode；运行形态选择见 `references/ue/runtime-modes.md`。

### Artifact-based Triage 模式

无法运行原场景时，不虚构 feedback loop：

- 记录 artifact 来源、时间、版本、采集命令和完整性。
- 把直接观察到的事实与推断分开。
- 说明无法验证的 runtime path 和最小 missing evidence。
- 准备能区分 hypotheses 的下一步 probes。

没有足够 concrete artifacts 时停止。

## Phase 2 — 复现 / 证据定界

Active Repro：

- 运行 loop，确认出现的是用户描述的 failure，而不是附近另一个错误。
- 记录精确 error、wrong output、timing、复现率与触发条件。
- 未观察到精确 failure 时停止在本阶段，继续磨尖 loop 或请求最小 runtime/input；若只有 concrete artifacts 可用，则更新 context 后转为 Artifact-based Triage。不要进入 Phase 3 hypotheses 或任何 root-cause claim。

Artifact-based Triage：

- 明确标注“未复现”。
- 建立“观察事实/推断/未知项/缺失证据”边界。
- 只判断 artifact 能支持或排除什么，不把 correlation 写成 confirmed cause。

`Profile: UE` 同时记录 map、actor/component、asset path、network role、platform、RHI、build configuration 与生命周期/cook/streaming 时机。

## Phase 3 — 提出 3–5 个可证伪假设

在测试前列出 3–5 个排序后的 hypotheses。每个 hypothesis 都必须有 prediction：

> 如果 `<X>` 是原因，那么 `<改变 Y / 添加 probe Z / 切换 runtime mode>` 会让症状消失、移动或加重。

把排序列表展示给用户；用户 AFK 时按当前排序继续。一个无法给出 prediction 的 hypothesis 应删除或磨尖。

`Profile: UE` 读取 `references/ue/probes-and-artifacts.md` 中的生命周期、Reflection/Blueprint、Asset/Cook、Threading、Network 与 Performance dimensions；不要把这些维度无条件输出给 `Profile: Generic`。

## Phase 4 — 定向仪表

每个 probe 必须对应 Phase 3 的一个 prediction，一次只改变一个变量：

1. 优先 Debugger / REPL / breakpoint / watch。
2. 使用能直接区分 hypotheses 的现有 profiler、trace 或 domain tool。
3. 最后才添加 targeted logs；不要 “log everything and grep”。

通用临时 log 使用唯一 `[DEBUG-<id>]`；UE probe、artifact 与 cleanup 规则见 `references/ue/probes-and-artifacts.md`。

Performance branch 必须先建立固定 measurement baseline，再 bisect 或修复；log 通常不是首选。

### 根因状态提升门

初始 `RootCauseStatus` 只能为 `likely` 或 `blocked`。只有同时满足以下条件，Active Repro 才能提升为 `confirmed`：

- 已在正确 runtime/context 观察到用户描述的精确 failure。
- 排序 hypothesis 的 prediction 已由 targeted probe、单变量实验或因果干预验证。
- 主要替代假设已被直接 evidence 排除，而不是只因“看起来不像”。
- diagnosis report 记录可复查的证据指针，以及它如何连接 cause、failure 与 regression seam。

Artifact-based Triage 永远不能通过本 gate；取得运行环境后必须先转入 Active Repro。

## Phase 5 — 修复方案与回归验证入口

在 repair handoff 前定义能覆盖真实 failure pattern 的 regression seam：

- Active Repro：把 minimised repro 转成先失败、修复后通过的 test 或等价 command。
- Artifact-based Triage：如果没有运行验证能力，只能给出候选 seam 与缺失条件，不能声称 seam 已执行。
- 唯一 seam 太浅时，明确记录 testability gap，不用浅 unit test 制造虚假信心。
- `Profile: UE` 的 seam 和 runtime parity 见 `references/ue/regression-seams.md`。

UE Packaged/RHI/network/platform-only failure 必须在对应 runtime mode 验证；PIE 通过不能替代。

repair scope、最小方向、风险与正确 seam 已可执行时，唯一推荐 `$implement`。修复后必须重新运行原始未最小化场景和 Phase 1 loop。

## Phase 6 — 清理 + 事后复盘

完成前：

- [ ] 已确认 root cause，或明确 `likely / blocked` 与缺失证据。
- [ ] 已给出正确 regression seam、候选 seam，或记录 testability gap。
- [ ] 所有 `[DEBUG-...]` instrumentation 已移除。
- [ ] UE 的 `[DEBUG-UE-*]`、Blueprint probe、临时 map/asset/capture 已清理或明确归档位置。
- [ ] throwaway harness、prototype、trace 与 minidump 的去留明确。
- [ ] 报告说明最终被支持/排除的 hypothesis 与对应 evidence。

最后记录“什么原本可以防止这个问题”。test seam、hidden coupling、asset rule、ownership model 或 profiling baseline 等 architecture observation 只能成为 residual/follow-up，不得产生第二个 next skill。

## 自然交接（Natural Handoff）

- repair scope 与正确 regression seam 已可执行：唯一推荐 `$implement`。
- 证据不足、没有正确 seam、Artifact-only 结论仍 blocked，或用户只需要 diagnosis report：推荐 `none`。
- handoff packet 必须包含 `DiagnosticContext v1`、root-cause evidence、regression seam、最小 repair direction、risk、cleanup 状态与 missing evidence。
- 自然确认只进入上一条唯一推荐，不绕过目标 skill 的 branch、scope、review、verification、commit、push 或修改计划确认。

## 输出契约

```markdown
## 诊断上下文

- Profile: Generic | UE
- EvidenceMode: Active Repro | Artifact-based Triage
- ObservedFailure:
- RuntimeMode:
- RootCauseStatus: confirmed | likely | blocked
- RegressionSeam:
- MissingEvidence:

## 证据

- Facts:
- Inferences:
- Hypotheses tested:
- Root-cause conclusion:

## 修复交接

- Minimal direction:
- Verification:
- Risk:
- Cleanup:
- Next: $implement | none
```
