---
name: diagnose
description: Use when a bug, failing test, crash, regression, wrong output, flaky behavior, performance slowdown, or debugging request needs disciplined root-cause analysis with a reproducible feedback loop, hypotheses, instrumentation, fix options, and regression verification guidance.
---

# 诊断

面向困难 bug 的定位纪律。只有在理由明确时，才跳过阶段。

探索代码库时，先使用项目的 domain glossary 建立相关模块的清晰心智模型，并检查你要触碰区域的 ADR。

## 进入边界

- 适用于 bug、failing test、crash、regression、wrong output、performance slowdown 或需要 debug 的任务。
- 可以由用户显式调用，也可以由 `workflow-router` 或上一轮 `Natural Handoff` 推荐后进入。
- 本 skill 产出 root cause、证据、修复选项和回归验证建议；不要提交持久业务代码修改。
- 如果需要落地修复，用 `Natural Handoff` 推荐 `$quick-change` 或 `$implement`。

## Language Contract

Language Contract: generated documents and chat outputs default to Chinese-first; preserve English for code, commands, API names, contract fields, IDs, proper nouns, and necessary technical terms. 用户或目标项目明确要求英文时可以例外，但必须记录原因。

## Phase 1 — 建立反馈循环

**这就是本 skill 的核心。** 其他步骤都是机械执行。如果你有一个快速、确定性、agent 可运行的 bug pass/fail 信号，你就能找到原因；bisection、hypothesis-testing 和 instrumentation 都只是消费这个信号。没有这个信号，盯着代码看再久也救不了你。

这里值得投入不成比例的精力。**要主动，要有创造性，不要轻易放弃。**

### 构造反馈循环的方法 — 大致按这个顺序尝试

1. 在能触达 bug 的 seam 上写一个 **failing test**：unit、integration、e2e 都可以。
2. 对运行中的 dev server 使用 **Curl / HTTP script**。
3. 用 fixture input 做 **CLI invocation**，并将 stdout 与已知正确的 snapshot 做 diff。
4. 使用 **Headless browser script**（Playwright / Puppeteer）：驱动 UI，并断言 DOM/console/network。
5. **Replay a captured trace.** 将真实 network request / payload / event log 保存到磁盘，并在隔离环境中通过对应代码路径重放。
6. **Throwaway harness.** 启动系统的最小子集（一个 service、mocked deps），用一次函数调用触发 bug 代码路径。
7. **Property / fuzz loop.** 如果 bug 是“有时输出错误”，运行 1000 个随机输入并寻找失败模式。
8. **Bisection harness.** 如果 bug 出现在两个已知状态之间（commit、dataset、version），自动化“在状态 X 启动、检查、重复”，这样就能用 `git bisect run` 跑它。
9. **Differential loop.** 用同一个输入跑 old-version vs new-version（或两个 config），然后 diff 输出。
10. **HITL bash script.** 最后的手段。如果必须有人点击，就用 `scripts/hitl-loop.template.sh` 来驱动_人_，让循环仍然结构化。捕获到的输出再反馈给你。

建立正确的反馈循环，bug 就已经修好了 90%。

### 迭代反馈循环本身

把这个循环当成一个产品。一旦你有了_一个_循环，就问：

- 能不能让它更快？（缓存 setup、跳过无关 init、缩小 test scope。）
- 能不能让信号更尖锐？（断言具体症状，而不是只断言“没有崩溃”。）
- 能不能让它更确定？（固定时间、设置 RNG seed、隔离 filesystem、冻结 network。）

一个 30 秒且 flaky 的循环几乎不比没有循环强。一个 2 秒且 deterministic 的循环是调试超能力。

### 非确定性 bug

目标不是干净复现，而是获得**更高的复现率**。把触发器循环 100 次、并行化、增加压力、收窄 timing window、注入 sleep。50% flake rate 的 bug 可以调试；1% 不行。持续提高复现率，直到它可调试。

### 当你确实无法建立循环时

停下来，并明确说明。列出你尝试过的办法。向用户请求：(a) 能复现问题的环境访问权限，(b) 捕获到的 artifact（HAR file、log dump、core dump、带时间戳的 screen recording），或 (c) 添加临时 production instrumentation 的许可。没有循环时，**不要**进入 hypothesise。

在拥有一个可信的循环之前，不要进入 Phase 2。

## Phase 2 — 复现

运行这个循环。看着 bug 出现。

确认：

- [ ] 这个循环产生的是**用户**描述的 failure mode，而不是附近刚好发生的另一个 failure。错 bug = 错 fix。
- [ ] 这个 failure 可以在多次运行中复现；对于非确定性 bug，则要达到足够高的复现率，能支撑调试。
- [ ] 你已经捕获了精确症状（error message、wrong output、slow timing），后续阶段才能验证 fix 是否真正解决问题。

复现 bug 之前，不要继续。

## Phase 3 — 提出假设

在测试任何假设之前，先生成 **3–5 个排序后的 hypotheses**。只生成单个假设会让你锚定在第一个看起来合理的想法上。

每个 hypothesis 都必须是**可证伪的**：明确它给出的 prediction。

> Format: "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

如果你说不出 prediction，这个 hypothesis 就只是感觉：丢掉它，或把它磨尖。

**测试前，把排序后的列表展示给用户。** 用户经常掌握可以立刻重排优先级的 domain knowledge（例如“我们刚部署了 #3 相关的变更”），或知道哪些假设已经被排除。这是低成本 checkpoint，能节省大量时间。不要卡在这里；如果用户 AFK，就按你的排序继续推进。

## Phase 4 — 加仪表

每个 probe 都必须映射到 Phase 3 中的某个具体 prediction。**一次只改变一个变量。**

工具偏好：

1. 如果 env 支持，优先使用 **Debugger / REPL inspection**。一个 breakpoint 胜过十条 log。
2. 在能区分 hypotheses 的边界处添加 **Targeted logs**。
3. 永远不要 “log everything and grep”。

**给每条 debug log 打上 tag**，使用唯一前缀，例如 `[DEBUG-a4f2]`。最后清理时只需要一次 grep。没有 tag 的 log 会存活；带 tag 的 log 必须消失。

**Perf branch.** 对 performance regression 来说，log 通常不是正确工具。应该先建立 baseline measurement（timing harness、`performance.now()`、profiler、query plan），然后 bisect。先测量，再修复。

## Phase 5 — 修复方案与回归验证入口

在进入修复之前先确定 regression seam，但前提是存在一个**正确的 seam**。

正确的 seam 是指：测试能覆盖 call site 中实际发生的**真实 bug pattern**。如果唯一可用的 seam 太浅（bug 需要多个 caller 才能触发，却只写 single-caller test；或 unit test 无法复刻触发 bug 的调用链），在这里写 regression test 只会带来虚假的信心。

**如果不存在正确的 seam，这本身就是发现。** 记录下来。代码库架构正在阻止这个 bug 被锁定。把它标记给下一阶段。

如果存在正确的 seam：

1. 说明如何把 minimised repro 转成该 seam 上的 failing test 或等价 pass/fail 命令。
2. 记录该测试或命令应该先失败、修复后通过。
3. 给出最小修复方向、影响范围和风险。
4. 用 `Natural Handoff` 推荐 `$quick-change` 或 `$implement` 执行修复。
5. 要求修复完成后重新运行原始（未 minimised）场景和 Phase 1 的反馈循环。

## Phase 6 — 清理 + 事后复盘

宣布完成前必须做到：

- [ ] 已确认 root cause，或明确说明仍缺少什么证据。
- [ ] 已给出 regression seam、等价验证方式，或已经记录没有正确 seam。
- [ ] 已给出修复入口建议：`$quick-change`、`$implement` 或暂不修复。
- [ ] 所有 `[DEBUG-...]` instrumentation 都已移除（`grep` 这个 prefix）
- [ ] Throwaway prototypes 已删除（或移动到明确标记的 debug location）
- [ ] 在诊断报告或后续修复 handoff 中说明最终被证明正确的 hypothesis，让下一位调试者能学到东西

**然后问：什么原本可以防止这个 bug？** 如果答案涉及 architectural change（没有好的 test seam、callers 缠绕、hidden coupling），就带着具体信息交给 `improve-codebase-architecture`。建议要在 fix 完成**之后**提出，而不是之前；此时你掌握的信息比刚开始更多。
