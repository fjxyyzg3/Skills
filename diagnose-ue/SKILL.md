---
name: diagnose-ue
description: Use when a concrete Unreal Engine / UE symptom needs disciplined diagnosis, including crash/assert/ensure, PIE/Standalone/Cooked/Packaged differences, Blueprint/asset/load/cook, networking, rendering, memory, performance, or platform-only behavior.
---

# Diagnose UE

面向 UE 开发问题的定位纪律。核心不是先猜代码，而是先构造一个可重复、可观察、agent 可运行或可指导用户运行的反馈循环；再用可证伪假设、定向仪表和回归验证收敛问题。

UE 问题通常横跨 C++、Blueprint、Asset、Editor state、Cooked content、平台配置和异步线程。不要只按 Web 应用思路找 request/response；要先确定问题发生在哪个运行形态：Editor、PIE、Standalone、Dedicated Server、Listen Server、Client、Cooked、Packaged、Shipping、目标平台。

## 进入边界

- 适用于具体 UE 症状：crash、assert、ensure、PIE/Standalone/Cooked/Packaged 差异、Blueprint、asset/load/cook、network、rendering、memory、performance 或平台问题。
- 可以由用户显式调用，也可以由 `workflow-router` 或上一轮 `Natural Handoff` 推荐后进入。
- 本 skill 产出运行形态、root cause、证据、修复选项和回归验证建议；不要提交持久业务代码修改。
- 如果需要落地修复，用 `Natural Handoff` 推荐 `$quick-change` 或 `$implement`。

## 适用边界

使用本 skill 的前提是：存在具体 UE 症状，需要定位原因或验证修复。

适用：

- crash、assert、ensure、Editor hang、PIE/Standalone/Cooked/Packaged/Shipping 差异。
- 错误运行时行为、Blueprint 异常、asset/load/cook 问题。
- network desync、replication 错误、rendering artifact、memory/performance regression、platform-only failure。

不适用：

- UE API 教学、概念解释、一般架构设计。
- 新功能设计或普通实现任务。
- 纯代码 review。
- RenderDoc `.rdc` 捕获分析，除非目标是回到 UE 工程里建立 repro 和修复验证循环。

## Language Contract

Language Contract: generated documents and chat outputs default to Chinese-first; preserve English for code, commands, API names, contract fields, IDs, proper nouns, and necessary technical terms. 用户或目标项目明确要求英文时可以例外，但必须记录原因。

## 压力规则

- 用户要求“直接修”时，仍必须先确认运行形态、精确症状和最短反馈循环；未复现或未定界前不要改代码。
- 只有 log、callstack、截图或 trace、没有工程访问时，不要声称已复现；标记为 artifact-based diagnosis，并列出需要用户补充的最小材料。
- 只在 Cooked、Packaged、Shipping、network、platform 或特定 RHI 出现的问题，不能用 PIE 或不对应的运行形态通过作为完成验证。
- 性能问题必须先固定 baseline、地图、视角、scalability、RHI、分辨率和采样窗口，再改代码。
- 临时 instrumentation 必须能对应某个 hypothesis 的 prediction；结束前清理或明确保留位置。

## Phase 1 — 建立 UE 反馈循环

先得到一个能稳定暴露症状的 pass/fail 信号。优先选择能被命令行、自动化测试或固定操作脚本重复执行的循环。

按以下优先顺序尝试：

1. **最小地图 / 最小 Actor / 最小 Asset**：复制或新建只包含触发问题所需对象的 map、BP、DataAsset、AnimBP、Material、Widget 或 GameplayAbility。
2. **Automation / Functional Test**：能写自动化测试时，优先用 UE Automation Test、Functional Test、Gauntlet 或项目已有测试框架复现。
3. **固定命令行启动**：用项目已有脚本或 UE 命令行启动指定 map/mode/config，并捕获 log。保留完整 command line、Engine version、platform、build configuration。
4. **PIE/Standalone 操作脚本**：如果必须在 Editor 中触发，写出最短人工步骤；能用 Editor Utility、Python、console command、exec command 或 automation driver 替代点击时就替代。
5. **Cook/Package 复现**：如果只在 cooked/packaged/shipping 出现，建立 `BuildCookRun` 或项目打包脚本循环，不要用 PIE 结果替代。
6. **网络复现**：明确 server/client 数量、角色、travel 方式、packet lag/loss、replication graph、net dormancy、prediction/rollback 条件；优先脚本化多实例启动，不能脚本化时记录手工步骤、实例启动参数和不可脚本化原因。
7. **性能复现**：固定地图、视角、玩家数量、资产集、scalability、RHI、分辨率、帧数采样窗口；使用 Unreal Insights、stat 命令或项目 profiling harness。
8. **崩溃复现**：保留 callstack、CrashContext、minidump、Saved/Logs、最后一次成功操作和相关 asset 路径。能稳定崩溃时，循环就是“启动 -> 触发 -> 捕获 callstack”。
9. **HITL 循环**：最后手段。如果必须人手操作，给用户一组编号步骤，让用户每轮只回传固定信息：log 片段、callstack、截图、Insights trace、复现次数。

迭代循环本身：

- 让它更快：跳过无关启动、缩小 map、减少 asset、禁用无关 plugin、固定启动参数。
- 让它更尖锐：断言具体症状，例如 crash function、ensure 文本、错误 asset、错误 replicated value、帧时间阈值。
- 让它更确定：固定随机种子、固定地图和 GameMode、清理 DerivedDataCache 影响、隔离 Saved/Config、明确 Editor vs packaged。

没有可信反馈循环时，停下来说明已尝试内容，并向用户请求缺失的最小材料：可复现工程、最小 repro、Saved/Logs、callstack、CrashContext/minidump、Unreal Insights trace、Network Profiler capture、Cook/Package log、目标平台访问，或允许添加临时 instrumentation。

## Phase 2 — 复现并定界

运行反馈循环并确认看到的是用户描述的问题，不是附近的另一个错误。

必须记录：

- 运行形态：Editor、PIE、Standalone、Cooked、Packaged、Shipping、Server/Client、平台、RHI、build configuration。
- 精确症状：crash/ensure/assert 文本、callstack 顶部有效帧、错误 log category、错误画面、错误状态值、耗时指标。
- 触发条件：map、actor/component、asset path、输入步骤、网络角色、关卡切换、存档/加载、GC、异步加载或 shader/cook 时机。
- 复现率：稳定复现、N 次中 M 次复现，或性能指标的 baseline。

复现前不要进入修复。

## Phase 3 — 提出 3-5 个可证伪假设

先列出排序后的 hypotheses，再测试。每个 hypothesis 必须写出 prediction。

格式：

> 如果 `<X>` 是原因，那么 `<改变 Y / 添加 probe Z / 切换运行形态>` 会让症状消失、移动或变得更严重。

UE 常见假设维度：

- 生命周期：constructor、PostInitProperties、BeginPlay、OnRegister、Tick、EndPlay、GC、async loading、level streaming 顺序错误。
- Reflection/Blueprint：UPROPERTY 缺失、Blueprint stale class、hot reload 产物、CDO/default value、nativization/cook 差异。
- Asset/Cook：引用丢失、soft reference 未 cook、redirector、AssetManager rule、platform-specific asset 或 shader permutation。
- Threading：GameThread/RenderThread/RHIThread/AsyncTask 边界错误，非线程安全 UObject 访问。
- Network：authority/ownership、RPC 条件、replication order、prediction、dormancy、seamless travel。
- Performance：CPU/GPU/render thread bottleneck、GC spike、asset streaming、shader compilation、tick fan-out、allocation churn。

把排序列表展示给用户；用户不在时，按你的排序继续。

## Phase 4 — 定向仪表

每个 probe 都要对应 Phase 3 的一个 prediction。一次只改变一个变量。

优先级：

1. **Debugger / breakpoint / watch**：C++ 崩溃、断言、生命周期问题优先用 debugger。
2. **已有 UE 工具**：Unreal Insights、Session Frontend、stat unit/stat game/stat gpu、MemReport、obj refs、Reference Viewer、Asset Audit、Network Profiler。
3. **定向 log**：只在能区分假设的边界加 log，使用项目已有 log category；临时 log 必须带唯一前缀，例如 `[DEBUG-UE-a4f2]`。
4. **Blueprint probe**：只有 C++ debugger、已有 UE 工具或定向 log 无法观察 Blueprint-only 状态时，才添加 Print String、breakpoint、watch pin，并在结束前清理。

不要 “log everything and grep”。性能问题先测 baseline，再改代码；渲染问题先判断 CPU/GPU/render thread/RHI thread；网络问题先分清 server truth、client prediction 和 replicated presentation。

## Phase 5 — 修复方案与回归验证入口

有正确 seam 时，先把最小 repro 转成 regression test 或自动化验证建议，再进入修复。

可接受 seam：

- Automation/Functional/Gauntlet test 覆盖真实运行形态。
- 小型 repro map + command line + 断言 log/exit code。
- C++ unit/automation test 覆盖真实生命周期或序列化路径。
- 性能 baseline 测试覆盖同一 map、视角和采样窗口。
- 打包/cook 问题用 cook/package 验证，而不是只用 PIE。

如果没有正确 seam，记录这是架构或测试性缺口；不要用过浅的 unit test 制造虚假信心。

修复入口必须说明：

1. regression test 或等价验证应该如何先失败、后通过。
2. 最小修复方向、影响范围和风险。
3. 是否推荐 `$quick-change` 或 `$implement` 执行修复。
4. 修复后必须重新运行原始未最小化场景。
5. 对 cooked/packaged-only、network-only、platform-only 问题，修复后必须在对应运行形态再验证一次。

## Phase 6 — 清理与复盘

完成前检查：

- [ ] 已确认 root cause，或明确说明仍缺少什么 UE 运行形态证据。
- [ ] 已给出 regression seam、等价验证循环，或已记录没有正确 seam。
- [ ] 已给出修复入口建议：`$quick-change`、`$implement` 或暂不修复。
- [ ] 所有 `[DEBUG-UE-...]` log、Blueprint Print String、临时 console command、测试 map 中的 debug-only 对象已清理或移动到明确 debug 位置。
- [ ] 临时 asset、repro map、trace、minidump 的去留明确；保留时放在项目约定的 debug/artifact 位置。
- [ ] 诊断报告或后续修复 handoff 中说明最终正确的 hypothesis、验证方式和覆盖的运行形态。

最后追问：什么原本可以防止这个问题？如果答案是缺少测试 seam、生命周期耦合、资产引用规则不清、网络 ownership 模型混乱或 profiling 基线缺失，把具体结论交给架构改进或测试基础设施建设，而不是在修复前泛泛重构。
