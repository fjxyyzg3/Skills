---
name: tdd
description: Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests.
---

> **`description` 中文译文：** 测试驱动开发。当用户希望以测试优先的方式构建 feature 或修复 bug、提到“red-green-refactor”，或希望编写 integration test 时，使用此 Skill。

# Test-Driven Development

> **标题中文译文：** 测试驱动开发

TDD is the red → green loop. This skill is the reference that makes that loop produce tests worth keeping: what a good test is, where tests go, the anti-patterns, and the rules of the loop. Every section applies on every cycle — consult them before and during the loop, not after.

> **中文译文：** TDD 是 red → green 循环。本 Skill 是一份参考指南，旨在让这个循环产出值得保留的测试：它说明什么是良好测试、测试应放在哪里、有哪些反模式，以及循环应遵循哪些规则。每个小节都适用于每一次循环——应在循环开始前和进行期间查阅，而不是事后查阅。

When exploring the codebase, read `CONTEXT.md` (if it exists) so test names and interface vocabulary match the project's domain language, and respect ADRs in the area you're touching.

> **中文译文：** 探索代码库时，读取 `CONTEXT.md`（如果存在），以确保测试名称和 interface 词汇与项目的领域语言一致；同时遵循所触及区域的 ADR。

## What a good test is（何为良好测试）

Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification — "user can checkout with valid cart" tells you exactly what capability exists — and survives refactors because it doesn't care about internal structure.

> **中文译文：** 测试应通过 public interface 验证行为，而不是验证实现细节。代码可以彻底改变，测试不应随之改变。良好测试读起来像 specification——“user can checkout with valid cart”会准确说明现有能力——而且能经受住 refactor，因为它不关心内部结构。

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

> **中文译文：** 示例见 [tests.md](tests.md)，mocking 指南见 [mocking.md](mocking.md)。

## Seams — where tests go（Seam——测试应放在哪里）

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

> **中文译文：** **Seam** 是执行测试的公共边界：你在这个 interface 上观察行为，而不深入内部。测试应位于 seam，绝不针对内部实现。

**Test only at pre-agreed seams.** Before writing any test, write down the seams under test and confirm them with the user. No test is written at an unconfirmed seam. You can't test everything — agreeing the seams up front is how testing effort lands on the critical paths and complex logic instead of every edge case.

> **中文译文：** **只在预先商定的 seam 上测试。** 编写任何测试前，先写下要测试的 seam，并与用户确认。不得在未经确认的 seam 上编写测试。你无法测试所有内容——预先商定 seam，才能让测试投入集中在关键路径和复杂逻辑上，而不是每个 edge case 上。

Ask: "What's the public interface, and which seams should we test?"

> **中文译文：** 询问：“公共 interface 是什么？我们应该测试哪些 seam？”

## Anti-patterns（反模式）

- **Implementation-coupled** — mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
- **Tautological** — the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth — a known-good literal, a worked example, the spec.
- **Horizontal slicing** — writing all tests first, then all implementation. Bulk tests verify _imagined_ behavior: you test the _shape_ of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in **vertical slices** instead — one test → one implementation → repeat, each test a **tracer bullet** that responds to what the last cycle taught you.

> **中文译文：**
> - **与实现耦合（Implementation-coupled）**——mock 内部协作者、测试 private method，或通过旁路进行验证（不使用 interface，而是查询数据库）。识别信号：refactor 后行为没有改变，测试却失败了。
> - **同义反复（Tautological）**——assertion 按照代码的计算方式重新计算 expected value（例如 `expect(add(a, b)).toBe(a + b)`、以相同方式手工推导的 snapshot，或断言某个 constant 等于自身），因此测试从构造上就必然通过，永远不可能与代码产生分歧。Expected value 必须来自独立的事实来源——已知正确的 literal、完整推导过的示例或 spec。
> - **水平切片（Horizontal slicing）**——先编写所有测试，再编写所有实现。批量测试验证的是*想象中的*行为：测试的是事物的*形状*，而不是面向用户的行为；测试会对真实变化失去敏感性；而且你会在理解实现之前就锁定测试结构。应改用 **vertical slice**——一个测试 → 一个实现 → 重复；每个测试都是一枚 **tracer bullet**，会响应上一轮循环带来的认知。

## Rules of the loop（循环规则）

- **Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Refactoring is not part of the loop.** It belongs to the review stage (see the `code-review` skill), not the red → green implementation cycle.

> **中文译文：**
> - **Red 在 green 之前。** 先编写失败测试，再只编写足以让测试通过的代码。不要预判未来的测试，也不要添加推测性 feature。
> - **一次一个 slice。** 每轮循环只处理一个 seam、一个测试和一个最小实现。
> - **Refactoring 不属于这个循环。** 它属于 review 阶段（见 `code-review` skill），而不属于 red → green 实现循环。
