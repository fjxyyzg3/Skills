# Regression Seams

仅在 `UE Profile` 定义 repair-ready regression seam 或 handoff 时读取。定位到可信 root cause 后，先定义覆盖真实 runtime path 的 seam，再进入修复；不要用过浅的 unit test 制造虚假信心。

## 可接受 Seam

- Automation Test、Functional Test 或 Gauntlet 覆盖真实运行形态。
- 小型 repro map + command line + 断言 log 或 exit code。
- C++ unit/automation test 覆盖真实 lifecycle、serialization、asset rule 或 replication path。
- Cook/package 问题使用 cook/package loop 验证，而不是只跑 PIE。
- Network 问题使用多实例启动脚本或明确的手工多实例步骤，覆盖 server/client role、authority、ownership 和 replication 条件。
- Performance 问题使用同一 map、视角、scalability、RHI、分辨率和采样窗口的 baseline。

## Runtime Parity

- PIE-only failure 至少在同一 PIE lifecycle/config 验证。
- Cooked/Packaged/Shipping-only failure 必须运行对应 build/cook/package loop。
- network-only failure 必须在相同 server/client topology、role 与 travel 条件验证。
- platform/RHI-only failure 必须在目标 platform/RHI/build configuration 验证。
- 只能运行邻近 mode 时，把结果标为 partial evidence，不得写成 repair verified。

## Repair Handoff

进入 `$implement` 前，handoff 必须说明：

- `DiagnosticContext v1` 与 `RootCauseStatus`。
- regression test 或等价验证如何先失败、修复后通过。
- 最小 repair direction、影响范围和风险。
- 原始未最小化场景如何重新验证。
- 对 Cooked/Packaged、network、platform 或 RHI-specific failure 的最终 runtime-mode 验证。
- 仍缺材料、temporary artifacts 与 cleanup 状态。

如果没有正确 seam，记录这是 testability 或 architecture gap，并说明临时验证能覆盖什么、不能覆盖什么；此时以 `none` 结束，不制造 repair-ready handoff。
