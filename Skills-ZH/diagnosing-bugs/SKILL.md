---
name: diagnosing-bugs
description: Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow.
---

> **`description` 中文译文：** 用于棘手 bug 和 performance regression 的诊断循环。当用户说“diagnose”/“debug this”，或报告某项功能损坏、抛出异常、失败或运行缓慢时，使用此 Skill。

# Diagnosing Bugs

> **标题中文译文：** 诊断 Bug

A discipline for hard bugs. Skip phases only when explicitly justified.

> **中文译文：** 一套用于处理棘手 bug 的严格方法。只有在明确说明理由时，才可跳过阶段。

When exploring the codebase, read `CONTEXT.md` (if it exists) to get a clear mental model of the relevant modules, and check ADRs in the area you're touching.

> **中文译文：** 探索代码库时，读取 `CONTEXT.md`（如果存在），以建立对相关 module 的清晰心智模型；同时检查所触及区域的 ADR。

## Phase 1 — Build a feedback loop（阶段 1——建立反馈循环）

**This is the skill.** Everything else is mechanical. If you have a **tight** pass/fail signal for the bug — one that goes red on _this_ bug — you will find the cause; bisection, hypothesis-testing, and instrumentation all just consume it. If you don't have one, no amount of staring at code will save you.

> **中文译文：** **这就是本 Skill 的核心。** 其余一切都只是机械操作。如果你拥有针对该 bug 的**紧密** pass/fail 信号——一个会因*这个* bug 而变 red 的信号——你就能找到原因；二分、hypothesis testing 和 instrumentation 都只是在使用这个信号。如果没有这样的信号，无论盯着代码看多久都无济于事。

Spend disproportionate effort here. **Be aggressive. Be creative. Refuse to give up.**

> **中文译文：** 应把格外多的精力投入这里。**积极进取。发挥创造力。拒绝放弃。**

### Ways to construct one — try them in roughly this order（构建反馈循环的方法——大致按此顺序尝试）

1. **Failing test** at whatever seam reaches the bug — unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) — drives the UI, asserts on DOM/console/network.
5. **Replay a captured trace.** Save a real network request / payload / event log to disk; replay it through the code path in isolation.
6. **Throwaway harness.** Spin up a minimal subset of the system (one service, mocked deps) that exercises the bug code path with a single function call.
7. **Property / fuzz loop.** If the bug is "sometimes wrong output", run 1000 random inputs and look for the failure mode.
8. **Bisection harness.** If the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" so you can `git bisect run` it.
9. **Differential loop.** Run the same input through old-version vs new-version (or two configs) and diff outputs.
10. **HITL bash script.** Last resort. If a human must click, drive _them_ with `scripts/hitl-loop.template.sh` so the loop is still structured. Captured output feeds back to you.

> **中文译文：**
> 1. 在任何能够触达 bug 的 seam 上编写 **failing test**——unit、integration 或 e2e。
> 2. 针对正在运行的 dev server 编写 **Curl / HTTP script**。
> 3. 使用 fixture input 执行 **CLI invocation**，并把 stdout 与已知正确的 snapshot 做 diff。
> 4. 编写 **headless browser script**（Playwright / Puppeteer）——驱动 UI，并对 DOM、console 和 network 作 assertion。
> 5. **重放已捕获的 trace。** 把真实 network request、payload 或 event log 保存到磁盘；通过隔离的代码路径重放它。
> 6. **一次性 harness。** 启动系统的最小子集（一个 service、mocked dependency），通过一次 function call 执行 bug 所在的代码路径。
> 7. **Property / fuzz loop。** 如果 bug 表现为“sometimes wrong output”，运行 1000 个随机 input 并寻找 failure mode。
> 8. **Bisection harness。** 如果 bug 出现在两个已知状态（commit、dataset、version）之间，自动执行“在状态 X 启动、检查、重复”，以便运行 `git bisect run`。
> 9. **Differential loop。** 让同一 input 分别经过 old-version 与 new-version（或两种 config），再对 output 做 diff。
> 10. **HITL bash script。** 这是最后手段。如果必须由人点击，就使用 `scripts/hitl-loop.template.sh` 引导*他们*操作，使循环仍保持结构化。捕获的 output 会反馈给你。

Build the right feedback loop, and the bug is 90% fixed.

> **中文译文：** 建立正确的反馈循环后，这个 bug 就已经解决了 90%。

### Tighten the loop（收紧循环）

Treat the loop as a product. Once you have _a_ loop, **tighten** it:

> **中文译文：** 把这个循环当作一个 product。一旦建立了*一个*循环，就要**收紧**它：

- Can I make it faster? (Cache setup, skip unrelated init, narrow the test scope.)
- Can I make the signal sharper? (Assert on the specific symptom, not "didn't crash".)
- Can I make it more deterministic? (Pin time, seed RNG, isolate filesystem, freeze network.)

> **中文译文：**
> - 能否让它更快？（缓存 setup、跳过无关 init、缩小测试 scope。）
> - 能否让信号更精确？（对具体 symptom 作 assertion，而不是只检查“didn't crash”。）
> - 能否让它更具确定性？（固定时间、设定 RNG seed、隔离 filesystem、冻结 network。）

A 30-second flaky loop is barely better than no loop; a 2-second deterministic one is tight — a debugging superpower.

> **中文译文：** 一个耗时 30 秒且 flaky 的循环只比没有循环略好；一个耗时 2 秒且 deterministic 的循环才称得上紧密——这是调试的超能力。

### Non-deterministic bugs（非确定性 Bug）

The goal is not a clean repro but a **higher reproduction rate**. Loop the trigger 100×, parallelise, add stress, narrow timing windows, inject sleeps. A 50%-flake bug is debuggable; 1% is not — keep raising the rate until it's debuggable.

> **中文译文：** 目标不是得到干净的 repro，而是获得**更高的复现率**。把 trigger 循环 100 次、并行执行、增加压力、缩窄 timing window、注入 sleep。复现率为 50% 的 flaky bug 可以调试；1% 的则不行——不断提高复现率，直到它可以调试。

### When you genuinely cannot build a loop（确实无法建立循环时）

Stop and say so explicitly. List what you tried. Ask the user for: (a) access to whatever environment reproduces it, (b) a captured artifact (HAR file, log dump, core dump, screen recording with timestamps), or (c) permission to add temporary production instrumentation. Do **not** proceed to hypothesise without a loop.

> **中文译文：** 停下来，并明确说明无法建立循环。列出已经尝试的内容。向用户请求：(a) 访问任何能够复现问题的 environment；(b) 已捕获的 artifact（HAR file、log dump、core dump、带 timestamp 的 screen recording）；或 (c) 添加临时 production instrumentation 的许可。没有循环时，**不得**继续提出 hypothesis。

### Completion criterion — a tight loop that goes red（完成标准——能够变 red 的紧密循环）

Phase 1 is done when the loop is **tight** and **red-capable**: you can name **one command** — a script path, a test invocation, a curl — that you have **already run at least once** (paste the invocation and its output), and that is:

> **中文译文：** 只有当循环既**紧密**又**具备变 red 的能力**时，阶段 1 才算完成：你能够给出**一条 command**——script path、test invocation 或 curl——并且已经**至少实际运行过一次**（粘贴 invocation 及其 output）；它还必须满足：

- [ ] **Red-capable** — it drives the actual bug code path and asserts the **user's exact symptom**, so it can go red on this bug and green once fixed. Not "runs without erroring" — it must be able to _catch this specific bug_.
- [ ] **Deterministic** — same verdict every run (flaky bugs: a pinned, high reproduction rate, per above).
- [ ] **Fast** — seconds, not minutes.
- [ ] **Agent-runnable** — you can run it unattended; a human in the loop only via `scripts/hitl-loop.template.sh`.

> **中文译文：**
> - [ ] **Red-capable**——它会驱动真实的 bug 代码路径，并对**用户描述的精确 symptom**作 assertion，因此会在 bug 存在时变 red、修复后变 green。不能只是“runs without erroring”——它必须能够*捕获这个特定 bug*。
> - [ ] **Deterministic**——每次运行都得到相同 verdict（对于 flaky bug：按上文方法固定在较高的复现率）。
> - [ ] **Fast**——耗时以秒计，而不是分钟。
> - [ ] **Agent-runnable**——可以无人值守地运行；仅允许通过 `scripts/hitl-loop.template.sh` 引入 human in the loop。

If you catch yourself reading code to build a theory before this command exists, **stop — jumping straight to a hypothesis is the exact failure this skill prevents.** No red-capable command, no Phase 2.

> **中文译文：** 如果你发现自己在这条 command 出现之前就开始阅读代码、构建 theory，**停下来——直接跳到 hypothesis，正是本 Skill 要防止的失败。** 没有 red-capable command，就不得进入阶段 2。

## Phase 2 — Reproduce + minimise（阶段 2——复现并最小化）

Run the loop. Watch it go red — the bug appears.

> **中文译文：** 运行循环。观察它变 red——bug 随之出现。

Confirm:

- [ ] The loop produces the failure mode the **user** described — not a different failure that happens to be nearby. Wrong bug = wrong fix.
- [ ] The failure is reproducible across multiple runs (or, for non-deterministic bugs, reproducible at a high enough rate to debug against).
- [ ] You have captured the exact symptom (error message, wrong output, slow timing) so later phases can verify the fix actually addresses it.

> **中文译文：** 确认：
>
> - [ ] 循环产生的是**用户**描述的 failure mode，而不是恰好发生在附近的另一个 failure。Bug 找错，fix 也会错。
> - [ ] 该 failure 可以在多次运行中复现（对于 non-deterministic bug，则应达到足以据此调试的高复现率）。
> - [ ] 已捕获精确 symptom（error message、错误 output、缓慢 timing），使后续阶段能够验证 fix 是否确实解决了它。

### Minimise（最小化）

Once it's red, shrink the repro to the **smallest scenario that still goes red**. Cut inputs, callers, config, data, and steps **one at a time**, re-running the loop after each cut — keep only what's load-bearing for the failure.

> **中文译文：** 循环变 red 后，把 repro 缩减为**仍会变 red 的最小场景**。每次只移除一项 input、caller、config、data 或 step，并在每次移除后重新运行循环——只保留对 failure 必不可少的内容。

Why bother: a minimal repro shrinks the hypothesis space in Phase 3 (fewer moving parts left to suspect) and becomes the clean regression test in Phase 5.

> **中文译文：** 这样做的原因是：最小 repro 会缩小阶段 3 的 hypothesis space（剩下需要怀疑的活动部分更少），并会成为阶段 5 中干净的 regression test。

Done when **every remaining element is load-bearing** — removing any one of them makes the loop go green.

> **中文译文：** 只有当**剩余的每个元素都必不可少**时，才算完成——移除其中任何一个都会使循环变 green。

Do not proceed until you have reproduced **and** minimised.

> **中文译文：** 在完成复现**并且**完成最小化之前，不得继续。

## Phase 3 — Hypothesise（阶段 3——提出假设）

Generate **3–5 ranked hypotheses** before testing any of them. Single-hypothesis generation anchors on the first plausible idea.

> **中文译文：** 测试任何 hypothesis 之前，先生成 **3–5 个按优先级排序的 hypothesis**。只生成一个 hypothesis 会使判断锚定在第一个看似合理的想法上。

Each hypothesis must be **falsifiable**: state the prediction it makes.

> **中文译文：** 每个 hypothesis 都必须**可证伪**：明确写出它所作的 prediction。

> Format: "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

> **格式中文译文：** “如果 <X> 是原因，那么 <changing Y> 会使 bug 消失，或 <changing Z> 会使它恶化。”

If you cannot state the prediction, the hypothesis is a vibe — discard or sharpen it.

> **中文译文：** 如果无法写出 prediction，这个 hypothesis 就只是一种感觉——丢弃它，或使它更加明确。

**Show the ranked list to the user before testing.** They often have domain knowledge that re-ranks instantly ("we just deployed a change to #3"), or know hypotheses they've already ruled out. Cheap checkpoint, big time saver. Don't block on it — proceed with your ranking if the user is AFK.

> **中文译文：** **测试前先向用户展示按优先级排序的列表。** 用户往往拥有能够立刻改变排序的 domain knowledge（“we just deployed a change to #3”），或知道哪些 hypothesis 已被排除。这是成本低、节省时间多的 checkpoint。不要在这里阻塞——如果用户暂时离开，就按你的排序继续。

## Phase 4 — Instrument（阶段 4——插桩）

Each probe must map to a specific prediction from Phase 3. **Change one variable at a time.**

> **中文译文：** 每个 probe 都必须对应阶段 3 中的一项具体 prediction。**一次只改变一个 variable。**

Tool preference:

1. **Debugger / REPL inspection** if the env supports it. One breakpoint beats ten logs.
2. **Targeted logs** at the boundaries that distinguish hypotheses.
3. Never "log everything and grep".

> **中文译文：** Tool 优先级：
>
> 1. 如果 environment 支持，使用 **Debugger / REPL inspection**。一个 breakpoint 胜过十条 log。
> 2. 在能够区分 hypothesis 的边界添加 **targeted log**。
> 3. 绝不要“log everything and grep”。

**Tag every debug log** with a unique prefix, e.g. `[DEBUG-a4f2]`. Cleanup at the end becomes a single grep. Untagged logs survive; tagged logs die.

> **中文译文：** 使用唯一 prefix（例如 `[DEBUG-a4f2]`）**标记每一条 debug log**。这样最终 cleanup 只需执行一次 grep。未标记的 log 保留，已标记的 log 删除。

**Perf branch.** For performance regressions, logs are usually wrong. Instead: establish a baseline measurement (timing harness, `performance.now()`, profiler, query plan), then bisect. Measure first, fix second.

> **中文译文：** **性能分支。** 对于 performance regression，log 通常不是正确工具。应先建立 baseline measurement（timing harness、`performance.now()`、profiler、query plan），然后二分。先测量，再修复。

## Phase 5 — Fix + regression test（阶段 5——修复并添加回归测试）

Write the regression test **before the fix** — but only if there is a **correct seam** for it.

> **中文译文：** 在 fix **之前**编写 regression test——但仅当存在适合它的 **correct seam** 时才这样做。

A correct seam is one where the test exercises the **real bug pattern** as it occurs at the call site. If the only available seam is too shallow (single-caller test when the bug needs multiple callers, unit test that can't replicate the chain that triggered the bug), a regression test there gives false confidence.

> **中文译文：** Correct seam 是这样一个位置：测试能够执行发生在 call site 的**真实 bug pattern**。如果唯一可用的 seam 太浅（例如 bug 需要多个 caller，却只能编写 single-caller test；或 unit test 无法复现触发 bug 的调用链），在该处编写 regression test 会带来虚假信心。

**If no correct seam exists, that itself is the finding.** Note it. The codebase architecture is preventing the bug from being locked down. Flag this for the next phase.

> **中文译文：** **如果不存在 correct seam，这本身就是一项发现。** 记录下来。代码库 architecture 正在阻止这个 bug 被测试锁定。把它标记出来，供下一阶段处理。

If a correct seam exists:

1. Turn the minimised repro into a failing test at that seam.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 feedback loop against the original (un-minimised) scenario.

> **中文译文：** 如果存在 correct seam：
>
> 1. 在该 seam 上把最小化后的 repro 转化为 failing test。
> 2. 观察测试失败。
> 3. 应用 fix。
> 4. 观察测试通过。
> 5. 针对原始的、未经最小化的场景，重新运行阶段 1 的反馈循环。

## Phase 6 — Cleanup + post-mortem（阶段 6——清理与复盘）

Required before declaring done:

- [ ] Original repro no longer reproduces (re-run the Phase 1 loop)
- [ ] Regression test passes (or absence of seam is documented)
- [ ] All `[DEBUG-...]` instrumentation removed (`grep` the prefix)
- [ ] Throwaway prototypes deleted (or moved to a clearly-marked debug location)
- [ ] The hypothesis that turned out correct is stated in the commit / PR message — so the next debugger learns

> **中文译文：** 声明完成前必须满足：
>
> - [ ] 原始 repro 不再复现（重新运行阶段 1 的循环）。
> - [ ] Regression test 通过（或已记录不存在 seam）。
> - [ ] 所有 `[DEBUG-...]` instrumentation 均已移除（对该 prefix 执行 `grep`）。
> - [ ] 一次性 prototype 已删除（或移至明确标记的 debug 位置）。
> - [ ] 已在 commit / PR message 中说明最终被证实正确的 hypothesis——让下一位 debugger 从中学习。

**Then ask: what would have prevented this bug?** If the answer involves architectural change (no good test seam, tangled callers, hidden coupling) hand off to the `/improve-codebase-architecture` skill with the specifics. Make the recommendation **after** the fix is in, not before — you have more information now than when you started.

> **中文译文：** **然后询问：怎样才能预防这个 bug？** 如果答案涉及 architecture change（没有良好的 test seam、caller 相互纠缠、存在 hidden coupling），就把具体情况交接给 `/improve-codebase-architecture` skill。应在 fix 落地**之后**再提出建议，而不是之前——此时掌握的信息比开始时更多。
