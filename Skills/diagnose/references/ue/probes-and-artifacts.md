# Probes And Artifacts

仅在 `UE Profile` 选择 UE hypothesis、probe 或 artifact 时读取。每个 probe 必须对应一个 hypothesis 的 prediction；一次只改变一个变量，结束前清理或明确保留所有临时 instrumentation。

## Artifact 清单

按症状收集最小材料：

- Crash/assert/ensure：callstack、CrashContext、minidump、Saved/Logs、最后一次成功操作、相关 asset path。
- Cook/package：完整 cook/package log、command line、target platform、build configuration、失败 asset、AssetManager rule 和 config 差异。
- Blueprint/asset/load：asset path、Blueprint class、CDO/default value、redirector、soft reference、load timing、GC 或 async loading 时机。
- Network：server/client log、role/ownership、RPC 调用条件、replication order、packet lag/loss、Network Profiler capture。
- Rendering：截图、RHI、scalability、view mode、Unreal Insights trace、stat unit/stat gpu、RenderDoc capture 路径。
- Performance：baseline、地图、视角、采样窗口、Unreal Insights trace、MemReport、stat command 输出。

## UE Hypothesis Dimensions

只选择与当前 symptom 和 runtime facts 有关的维度，不要机械列全：

- 生命周期：constructor、PostInitProperties、BeginPlay、OnRegister、Tick、EndPlay、GC、async loading、level streaming 顺序。
- Reflection/Blueprint：UPROPERTY 缺失、Blueprint stale class、hot reload 产物、CDO/default value、cook 差异。
- Asset/Cook：引用丢失、soft reference 未 cook、redirector、AssetManager rule、platform-specific asset 或 shader permutation。
- Threading：GameThread/RenderThread/RHIThread/AsyncTask 边界、非线程安全 UObject 访问。
- Network：authority/ownership、RPC 条件、replication order、prediction、dormancy、seamless travel。
- Performance：CPU/GPU/render thread bottleneck、GC spike、asset streaming、shader compilation、tick fan-out、allocation churn。

每个选择的维度都要转化为可证伪 prediction，不能只作为主题列表。

## Probe 优先级

1. Debugger、breakpoint、watch：C++ crash、assert、lifecycle 和 threading 问题优先使用。
2. 已有 UE 工具：Unreal Insights、Session Frontend、stat unit、stat game、stat gpu、MemReport、obj refs、Reference Viewer、Asset Audit、Network Profiler。
3. 定向 log：只在能区分假设的边界加 log，使用项目已有 log category；临时 log 使用唯一前缀，例如 `[DEBUG-UE-a4f2]`。
4. Blueprint probe：只有 C++ debugger、已有 UE 工具或定向 log 无法观察 Blueprint-only 状态时，才添加 Print String、breakpoint 或 watch pin。

不要用 “log everything and grep”。probe 输出必须让某个 hypothesis 更可信、更不可信，或明确 blocked。

## Artifact-based Triage

只有 log、callstack、截图、trace、capture 或 asset、没有工程访问时：

- 明确标记为 Artifact-based Triage 和“未复现”。
- 记录 artifact provenance、直接 facts、inferences、unknowns 与最小 missing evidence。
- 仍可列出 3–5 个可证伪 hypotheses，以及每个 hypothesis 需要的下一步 probe。
- 不得使用 `RootCauseStatus: confirmed`；只能为 `likely` 或 `blocked`。

后续获得可运行工程或目标 build 时，更新 `DiagnosticContext v1` 并转入 Active Repro。

## 纯 `.rdc` Caveat

纯 RenderDoc `.rdc` capture 可以支持 GPU event、resource、pipeline state 和 shader evidence，但通常不能单独证明 UE gameplay、asset lifecycle、CPU submission 或 engine-side root cause。

- 用户只要求 capture 内容解释时，应明确当前证据边界，不虚构 UE 工程 repro。
- 需要 repair-ready diagnosis 时，必须回到对应 UE project/runtime 建立 CPU/GPU 关联、原始 symptom loop 和 regression seam。
- capture 的 platform、RHI、frame、view、scalability、resolution 与 build 必须记录。

## Cleanup

结束前处理：

- 搜索并移除所有 `[DEBUG-UE-*]` 和具体 `[DEBUG-UE-<id>]` logs。
- 删除 Blueprint Print String、temporary breakpoint/watch pin 或明确记录保留原因。
- 删除临时 map、Actor、Asset、console command、Editor Utility、automation driver，或移动到项目约定的 debug location。
- trace、capture、CrashContext、minidump 与 Saved/Logs 如需保留，记录稳定路径、采集条件和敏感信息边界。
- 不把 throwaway probe 留在 production/default content path。
