---
name: implement
description: 读取本地 PRD、issue 文档或当前 conversation context 并执行实现。Use when user asks to implement, build, code, execute issues, execute PRD, run implementation work, or decide between multi-agent parallel execution and inline serial execution from local issues. This skill is local-first and uses TDD for feature, bugfix, refactor, and behavior-change work.
---

# Implement

读取 PRD、issue 文档或当前上下文，选择合适的执行模式，并把实现推进到验证完成。优先从本地文档获取上下文；只有真正影响实现且无法从文档或代码发现的问题才询问用户。

## 核心规则

- 如果存在本地 issue 文档，先读取 `00-index.md` 和相关 issue 文件，基于 dependency graph、execution waves、parallelization notes 给出执行模式推荐，并向用户确认采用 `multi-agent parallel execution` 还是 `inline serial execution`。
- 如果没有 issue 文档，只有 PRD、plan、spec 或当前 conversation context，默认采用 `inline serial execution`，无需确认执行模式。
- 不要从 PRD 或上下文直接推断可以并行执行；并行只建立在明确 issue 依赖、执行波次和共享写入风险已经被拆清楚的基础上。
- 实现 feature、bugfix、refactor 或 behavior change 时使用 TDD：先写一个可观察行为的失败测试，确认失败原因正确，再写最小实现，最后重构并保持测试通过。
- 不要在 `main` / `master` 上开始实现，除非用户明确同意。

## 输入判定

按优先级识别输入：

1. 用户指定的 issue 目录或 issue 文件。
   - 读取 `00-index.md`。
   - 读取本次要执行的 issue 文件；如果用户没有指定范围，读取 index 中所有 issue 的摘要与依赖信息。
2. 用户指定的 PRD、plan 或 spec 文件。
   - 读取完整文档。
   - 轻量检查相关代码、测试、README、AGENTS、ADR 或 domain docs。
3. 当前 conversation context。
   - 将已知目标、约束和验收条件整理成可执行 slice。
   - 如果目标不足以实现，最多问一个阻塞问题，并给出推荐默认答案。

## 执行模式决策

### 有 issue 文档

读取 issue index 后，给用户一个简短推荐：

- 推荐 `multi-agent parallel execution`：同一 wave 内有 2 个以上 `parallel-safe` issues；没有共享 contract、schema、核心 module 或同一文件写入冲突；前置依赖清晰；验证可以独立运行。
- 推荐 `inline serial execution`：issues 标记为 `sequential` 或 `coordination-needed`；依赖链很深；多个 issues 修改同一 public interface、schema、migration、核心 workflow 或设计系统；测试/验证必须按顺序建立。
- 推荐 `serial with limited parallel exploration`：可以让 subagent 并行做只读探索或局部 spike，但实现/提交必须串行合并。

确认问题只问一次：

```text
我建议采用 <mode>，因为 <dependency / wave / shared ownership reason>。
你要按这个模式执行吗？
```

用户确认后持续执行，不要在每个小步骤重复确认。除非遇到无法自行解决的 blocker、计划错误或新的高风险决策。

### 没有 issue 文档

只有 PRD、plan、spec 或当前上下文时，默认 `inline serial execution`：

- 先把工作拆成少量 vertical slices。
- 每个 slice 都应能通过外部可观察行为验证。
- 按依赖顺序一个一个完成。
- 不要询问是否并行，除非用户主动要求多 agent 并行。

## Multi-Agent Parallel Execution

仅在用户确认后使用。当前环境有可用 subagent / multi-agent 工具时才启动；没有可用工具时，说明无法实际并行，并退回 `inline serial execution`。

执行方式：

1. 作为 coordinator 保留全局上下文：PRD、issue index、依赖图、共享 contracts、验证命令、完成标准。
2. 只把某个 issue 必需的完整文本、相关 PRD 摘要、依赖边界和验证要求交给对应 subagent；不要让 subagent 自行重新解释整份 plan。
3. 同一 wave 只并行启动 `parallel-safe` issues。`coordination-needed` issues 最多并行探索，不要并行落地共享接口。
4. 要求每个 implementation subagent 按 TDD 工作，并在交付中报告：
   - issue ID 和完成范围
   - RED/GREEN/REFACTOR 证据
   - 修改文件
   - 验证命令和结果
   - blocker、concern 或超出范围的发现
5. 每个 issue 完成后做两类 review：
   - spec compliance review：确认实现完全满足该 issue / PRD，不少做也不多做。
   - code quality review：确认代码质量、测试质量、集成风险和维护性。
6. review 发现问题时，先让负责该 issue 的 subagent 修复并重新验证；不要把未解决问题带入下一 wave。
7. 每个 wave 结束后同步依赖状态，再启动下一 wave。

## Inline Serial Execution

串行执行时，当前 agent 自己实现并验证：

1. 建立 todo：按 issue、PRD requirement 或可验证 slice 列出任务。
2. 对每个 slice 执行 TDD：
   - RED：写一个描述 external behavior 的测试，并确认失败原因正确。
   - GREEN：写最小实现让该测试通过。
   - REFACTOR：只在全绿后清理命名、重复和结构。
3. 每个 slice 结束时运行相关测试；跨模块行为完成后运行更宽的验证。
4. 遇到 PRD 或 issue 与代码事实冲突时，先记录冲突并提出推荐修正；只有阻塞实现时才停下来问用户。
5. 所有 slice 完成后做自检：需求覆盖、测试覆盖、未解决风险、工作树状态。

## TDD 约束

- 测试描述行为，不测试 implementation details。
- 优先通过 public interface、CLI、API、UI workflow 或集成 seam 验证。
- 一次只为一个行为写测试；不要先批量写完所有测试再实现。
- 新测试如果第一次运行就通过，说明没有证明缺失行为；调整测试或选择下一个真实缺口。
- bugfix 必须先有复现失败的测试。
- refactor 前必须保持测试全绿；refactor 不引入新行为。
- 如果某类变更无法自动化测试，记录原因，并执行最接近用户可观察行为的手动或静态验证。

## 完成标准

完成前确认：

- 已执行用户确认过的执行模式；若退回串行，说明原因。
- 已覆盖 PRD requirements 或选定 issues 的 acceptance criteria。
- 已运行相关测试和必要的更宽验证。
- 已列出未解决风险、跳过测试的原因、以及需要用户后续决定的事项。
- 没有遗留正在运行的实现或验证进程。
