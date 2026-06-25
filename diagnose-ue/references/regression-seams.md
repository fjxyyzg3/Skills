# Regression Seams

定位到可信 root cause 后，先定义 regression seam 或等价验证循环，再进入修复。不要用过浅的 unit test 制造虚假信心。

## 可接受 seam

- Automation Test、Functional Test 或 Gauntlet 覆盖真实运行形态。
- 小型 repro map + command line + 断言 log 或 exit code。
- C++ unit/automation test 覆盖真实 lifecycle、serialization、asset rule 或 replication path。
- Cook/package 问题使用 cook/package loop 验证，而不是只跑 PIE。
- Network 问题使用多实例启动脚本或明确的手工多实例步骤，覆盖 server/client 角色和 replication 条件。
- Performance 问题使用同一 map、视角、scalability、RHI、分辨率和采样窗口的 baseline。

## 修复入口 handoff

进入 `$quick-change` 或 `$implement` 前，handoff 必须说明：

- regression test 或等价验证如何先失败、后通过。
- 最小修复方向、影响范围和风险。
- 原始未最小化场景如何重新验证。
- Cooked/Packaged-only、network-only、platform-only 问题对应的最终运行形态验证。

如果没有正确 seam，记录这是测试性或架构缺口，并说明临时验证能覆盖什么、不能覆盖什么。
