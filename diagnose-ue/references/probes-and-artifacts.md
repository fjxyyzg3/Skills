# Probes And Artifacts

每个 probe 必须对应一个 hypothesis 的 prediction。一次只改变一个变量，结束前清理或明确保留所有临时 instrumentation。

## Artifact 清单

按症状收集最小材料：

- Crash/assert/ensure：callstack、CrashContext、minidump、Saved/Logs、最后一次成功操作、相关 asset path。
- Cook/package：完整 cook/package log、command line、target platform、build configuration、失败 asset、AssetManager rule 和 config 差异。
- Blueprint/asset/load：asset path、Blueprint class、CDO/default value、redirector、soft reference、load timing、GC 或 async loading 时机。
- Network：server/client log、role/ownership、RPC 调用条件、replication order、packet lag/loss、Network Profiler capture。
- Rendering：截图、RHI、scalability、view mode、Unreal Insights trace、stat unit/stat gpu、RenderDoc capture 路径。
- Performance：baseline、地图、视角、采样窗口、Unreal Insights trace、MemReport、stat command 输出。

## Probe 优先级

1. Debugger、breakpoint、watch：C++ crash、assert、lifecycle 和 threading 问题优先使用。
2. 已有 UE 工具：Unreal Insights、Session Frontend、stat unit、stat game、stat gpu、MemReport、obj refs、Reference Viewer、Asset Audit、Network Profiler。
3. 定向 log：只在能区分假设的边界加 log，使用项目已有 log category；临时 log 使用唯一前缀，例如 `[DEBUG-UE-a4f2]`。
4. Blueprint probe：只有 C++ debugger、已有 UE 工具或定向 log 无法观察 Blueprint-only 状态时，才添加 Print String、breakpoint 或 watch pin。

不要用 “log everything and grep”。probe 输出必须能让某个 hypothesis 变得更可信、更不可信，或明确 blocked。

## Artifact-based Diagnosis

只有 log、callstack、截图或 trace、没有工程访问时：

- 标记为 artifact-based diagnosis。
- 不要声称已复现。
- 说明缺少的最小材料。
- 仍然列出 3-5 个可证伪 hypotheses 和每个 hypothesis 需要的下一步 probe。

## Example Input: Packaged-only Crash

用户给出：

- Engine version 和 branch。
- Build configuration 和 target platform。
- Command line 或 packaging command。
- CrashContext/minidump 和 Saved/Logs。
- Last known good build 或 commit。

预期第一轮响应：

- 标记为 artifact-based diagnosis，除非当前环境可运行该 packaged build。
- 找到最短 packaged repro loop。
- 提出 3-5 个可证伪 hypotheses，再决定 instrumentation。
