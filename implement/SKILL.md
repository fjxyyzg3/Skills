---
name: implement
description: Use when executing local issues, PRDs, specs, implementation plans, bugfixes, refactors, or conversation-scoped coding work; when choosing serial vs multi-agent execution; or when applying TDD, review, verification, and branch handoff gates to implementation work.
---

# Implement

读取 PRD、issue 文档或当前上下文，选择合适执行模式，并把实现推进到验证完成。实现不是结束于“代码写完”，而是结束于需求覆盖、测试、review 和 completion verification 都有证据。

## 必须配合的流程

- 开始实现前：使用 `using-worktrees` 检查分支/工作树和 baseline。
- 有 PRD/issues/plan artifacts 时：优先运行或读取 `analyze` 结果；`CRITICAL` finding 未解决前不要开始实现。
- 实现后：使用 `requesting-code-review` 做 spec compliance 和 code quality review。
- 声明完成前：使用 `verification-before-completion`。
- 用户要求交付分支、commit、PR 或收尾时：使用 `finishing-branch`。

## 核心规则

- 如果存在本地 issue 文档，先读取 `00-index.md` 和相关 issue 文件，基于 dependency graph、execution waves、parallelization notes 推荐执行模式。
- 如果没有 issue 文档，只有 PRD、plan、spec 或当前 conversation context，默认 `inline serial execution`，除非用户主动要求多 agent 并行。
- 不要从 PRD 或上下文直接推断可以并行执行；并行只建立在明确 issue 依赖、执行波次和共享写入风险已经拆清楚的基础上。
- feature、bugfix、refactor 或 behavior change 使用 TDD：先写一个可观察行为的失败测试，确认失败原因正确，再写最小实现，最后重构并保持测试通过。
- 不在 `main` / `master` 上开始实现，除非用户明确同意；优先让 `using-worktrees` 处理隔离。
- 不要跳过 review 和 verification 来换取“更快完成”。

## 输入判定

按优先级识别输入：

1. 用户指定的 issue 目录或 issue 文件。
   - 读取 `00-index.md`。
   - 读取本次要执行的 issue 文件；如果用户没有指定范围，读取 index 中所有 issue 的摘要、coverage 和依赖信息。
2. 用户指定的 PRD、plan 或 spec 文件。
   - 读取完整文档。
   - 轻量检查相关代码、测试、README、AGENTS、constitution、ADR 或 domain docs。
   - 如果 scope 超过一个薄 slice，建议先用 `to-issues` 拆分；用户要求直接做时，当前 agent 自行拆成少量 slices。
3. 当前 conversation context。
   - 将已知目标、约束和验收条件整理成可执行 slice。
   - 如果目标不足以实现，最多问一个阻塞问题，并给出推荐默认答案。

## 执行模式决策

### 有 issue 文档

读取 issue index 后给用户一个简短推荐：

- 推荐 `multi-agent parallel execution`：同一 wave 内有 2 个以上 `parallel-safe` issues；没有共享 contract、schema、核心 module 或同一文件写入冲突；验证可以独立运行。
- 推荐 `inline serial execution`：issues 标记为 `sequential` 或 `coordination-needed`；依赖链很深；多个 issues 修改同一 public interface、schema、migration、核心 workflow 或设计系统。
- 推荐 `serial with limited parallel exploration`：可以让 subagent 并行只读探索或 spike，但实现/提交必须串行合并。

确认问题只问一次：

```text
我建议采用 <mode>，因为 <dependency / wave / shared ownership reason>。
你要按这个模式执行吗？
```

用户确认后持续执行，不要在每个小步骤重复确认。除非遇到 blocker、计划错误或新的高风险决策。

### 没有 issue 文档

默认 `inline serial execution`：

- 先把工作拆成少量 vertical slices。
- 每个 slice 都应能通过 external behavior 验证。
- 按依赖顺序一个一个完成。
- 不询问是否并行，除非用户主动要求多 agent 并行。

## Multi-Agent Parallel Execution

仅在用户确认且当前环境有可用 subagent / multi-agent 工具时启动；没有可用工具时，说明无法实际并行，并退回 `inline serial execution`。

执行方式：

1. 作为 coordinator 保留全局上下文：PRD、issue index、coverage、依赖图、共享 contracts、验证命令、完成标准。
2. 只把某个 issue 必需的完整文本、相关 PRD 摘要、依赖边界和验证要求交给对应 subagent。
3. 同一 wave 只并行启动 `parallel-safe` issues。`coordination-needed` issues 最多并行探索，不要并行落地共享接口。
4. 要求每个 implementation subagent 按 TDD 工作，并在交付中报告：
   - issue ID 和完成范围
   - covered requirements
   - RED/GREEN/REFACTOR 证据
   - 修改文件
   - 验证命令和结果
   - blocker、concern 或超出范围发现
5. 每个 issue 完成后运行 `requesting-code-review` 的两阶段 review。
6. review 发现问题时，先让负责该 issue 的 subagent 修复并重新验证。
7. 每个 wave 结束后同步依赖状态，再启动下一 wave。

## Inline Serial Execution

当前 agent 自己实现并验证：

1. 建立 todo：按 issue、PRD requirement 或可验证 slice 列出任务。
2. 对每个 slice 执行 TDD：
   - RED：写一个描述 external behavior 的测试，并确认失败原因正确。
   - GREEN：写最小实现让该测试通过。
   - REFACTOR：只在全绿后清理命名、重复和结构。
3. 每个 slice 结束时运行相关测试；跨模块行为完成后运行更宽验证。
4. 遇到 PRD/issue 与代码事实冲突时，先记录冲突并提出推荐修正；只有阻塞实现时才停下来问用户。
5. 所有 slice 完成后运行 `requesting-code-review` 和 `verification-before-completion`。

## TDD 约束

- 测试描述 external behavior，不测试 implementation details。
- 优先通过 public interface、CLI、API、UI workflow 或 integration seam 验证。
- 一次只为一个行为写测试；不要先批量写完所有测试再实现。
- 新测试如果第一次运行就通过，说明没有证明缺失行为；调整测试或选择下一个真实缺口。
- Bugfix 必须先有复现失败的测试或等价 repro loop。
- Refactor 前必须保持测试全绿；refactor 不引入新行为。
- 如果某类变更无法自动化测试，记录原因，并执行最接近用户可观察行为的手动或静态验证。

## 完成标准

完成前确认：

- 已执行或明确降级 `using-worktrees`。
- 已处理 artifacts 中的 `CRITICAL` analyze findings。
- 已覆盖 PRD requirements 或选定 issues 的 acceptance criteria。
- 已运行相关测试和必要的更宽验证。
- 已通过 `requesting-code-review`，或列出未修复 findings 和用户决定。
- 已通过 `verification-before-completion`。
- 已列出未解决风险、跳过测试的原因、以及需要用户后续决定的事项。
- 没有遗留正在运行的实现或验证进程。
