# Runtime Modes

仅在 `DiagnosticContext v1` 选择 `UE Profile` 且症状依赖 UE runtime 时读取。先确认症状发生在哪个运行形态；Cooked、Packaged、Shipping、network、platform 或特定 RHI failure 不能用 PIE 结果替代完成验证。

## 运行形态记录

记录以下信息：

- Engine version、project branch、build configuration。
- Editor、PIE、Standalone、Cooked、Packaged、Shipping。
- Dedicated Server、Listen Server、Client 数量和角色。
- 目标 platform、RHI、scalability、分辨率和启动参数。
- map、GameMode、actor/component、asset path、输入步骤和复现率。

## 反馈循环选择

按优先级建立最短循环：

1. 最小 map、Actor、Asset、BP、DataAsset、AnimBP、Material、Widget 或 GameplayAbility。
2. UE Automation Test、Functional Test、Gauntlet 或项目已有测试框架。
3. 固定命令行启动指定 map/mode/config，并捕获 log。
4. PIE/Standalone 操作脚本；能用 Editor Utility、Python、console command、exec command 或 automation driver 替代点击时就替代。
5. `BuildCookRun` 或项目打包脚本循环，用于 Cooked/Packaged/Shipping-only 问题。
6. 网络多实例循环，记录 server/client 数量、角色、travel、packet lag/loss、replication graph、net dormancy、prediction/rollback。
7. 性能 profiling 循环，固定地图、视角、玩家数量、资产集、scalability、RHI、分辨率和帧数采样窗口。
8. 崩溃捕获循环：启动、触发、捕获 callstack、CrashContext、minidump 和 Saved/Logs。
9. HITL 循环：只在无法自动化时使用，要求用户每轮回传固定 artifact。

## 运行形态判断

- PIE-only 问题优先检查 Editor state、hot reload、Blueprint stale class、CDO/default value 和 PIE world lifecycle。
- Packaged-only 问题优先检查 cook rule、soft reference、redirector、platform-specific asset、shader permutation 和 config 差异。
- Network-only 问题先分清 server truth、client prediction、replicated presentation、authority、ownership、RPC 条件和 dormancy。
- Rendering 问题先判断 CPU、GPU、render thread 或 RHI thread，再选择 RenderDoc、Unreal Insights、stat 命令或 shader/cook probe。
- Performance 问题先固定 baseline 和采样窗口，再做代码或内容改动。

## Runtime Parity

- 只在一种运行形态出现的 failure，regression 必须至少覆盖该形态。
- Packaged/Shipping failure 的 PIE pass 只能作为邻近证据，不能标记 repair verified。
- network regression 必须说明 server/client 数量、role、authority/ownership 与 travel 条件。
- platform/RHI regression 必须记录目标 platform、RHI、driver/device 或 build configuration。
- 无法运行正确 mode 时，`RootCauseStatus` 保持 `likely` 或 `blocked`，并在 `MissingEvidence` 写明缺口。
