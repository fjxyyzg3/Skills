---
name: tdd
description: "当用户明确要求 TDD、test-driven development、test-first development、red-green-refactor、在实现前先写失败测试、为 feature 或 bugfix 添加 integration tests，或希望由 behavior-focused tests 引导实现时使用；按 RED/GREEN/REFACTOR loop 推进。"
---

# TDD

用 test-first 方式推进功能、bugfix 或重构：每次只选择一个可观察行为，先写会失败的测试或等价 repro，再写最小实现，最后在全绿时重构。

## 压力场景（Pressure Scenarios）

1. 用户请求："用 TDD 实现这个功能。"
   - 预期触发：先确认 public interface 和关键行为，再按纵向切片执行 RED/GREEN/REFACTOR。
   - 未使用本 skill 时的常见失败：一次性写完所有测试或实现，测试变成对想象中结构的确认。
   - 本 skill 必须强制的行为：每个 cycle 只覆盖一个 external behavior，并保留失败到通过的证据。
2. 用户请求："先写失败测试复现这个 bug。"
   - 预期触发：建立最小 repro test，确认它先失败，再改实现直到测试通过。
   - 未使用本 skill 时的常见失败：直接修代码，事后补一个可能无法证明 bug 的测试。
   - 本 skill 必须强制的行为：bugfix 先 RED，不能跳过复现。
3. 用户请求："给这个模块加 integration tests。"
   - 预期触发：通过 public interface 验证行为，少 mock 内部 collaborator。
   - 未使用本 skill 时的常见失败：mock 自己的模块、断言 call count、测试 private method。
   - 本 skill 必须强制的行为：测试描述 WHAT，不锁死 HOW。

## 核心原则

- 测试应验证 external behavior，而不是实现细节。
- 优先使用 public interface、CLI、API、UI workflow 或真实 integration path。
- 好测试读起来像 specification，例如 "user can checkout with valid cart"。
- 坏测试会因为内部重命名、拆函数、换 collaborator 而失败，即使外部行为没有变化。
- 只在 system boundaries mock：外部 API、时间、随机数、文件系统或必要的数据库边界。

更多测试例子见 [references/tests.md](references/tests.md)，mock 取舍见 [references/mocking.md](references/mocking.md)。

## 反模式：横向切片

不要先批量写完所有测试，再批量写完所有实现。这会把 RED 误解成 "write all tests"，把 GREEN 误解成 "write all code"。

问题：

- 批量测试会验证想象中的结构，而不是真实学习后的行为。
- 容易测试 data shape、函数签名和内部编排，而不是用户关心的能力。
- 测试可能对真实行为变化不敏感，却对无害重构过度敏感。
- 过早承诺测试结构，会限制更好的 interface 设计。

正确方式是纵向切片 / tracer bullets：

```text
WRONG:
  RED:   test1, test2, test3, test4
  GREEN: impl1, impl2, impl3, impl4

RIGHT:
  RED -> GREEN: test1 -> impl1
  RED -> GREEN: test2 -> impl2
  RED -> GREEN: test3 -> impl3
```

## 工作流程

### 1. 计划

开始写测试或代码前：

- 明确本次范围、public interface、关键行为和验收顺序。
- 读取相关 domain glossary、ADR、spec、issue 或 PRD；没有时记录缺失。
- 只列行为，不列内部实现步骤。
- 识别是否存在 deep module 机会，参考 [references/deep-modules.md](references/deep-modules.md)。
- 让 interface 更容易测试，参考 [references/interface-design.md](references/interface-design.md)。
- 如果范围、interface 或最重要行为不清楚，最多问一个阻塞问题；否则做保守假设并记录。

### 2. 探路切片

选择一个最高价值行为并写一个失败测试：

```text
RED:   Write one test for one behavior -> observe failure
GREEN: Write minimal code -> observe pass
```

如果新测试第一次运行就通过，它没有证明缺失行为；调整测试或选择真实缺口。

### 3. 增量循环

对每个后续行为重复：

```text
RED:   Write next focused test -> fails
GREEN: Minimal implementation -> passes
```

规则：

- 一次只写一个行为测试。
- 只写足够通过当前测试的实现。
- 不提前实现未来测试需要的能力。
- 测试名称描述可观察行为。
- 每个 cycle 后运行最小相关测试；跨模块完成后运行更宽验证。

### 4. 重构

所有相关测试通过后，才考虑重构。候选见 [references/refactoring.md](references/refactoring.md)。

- 消除重复。
- 加深 modules，把复杂度收进更小 interface 后面。
- 自然应用 SOLID 或项目既有 design style。
- 每一步重构后重新跑相关测试。

永远不要在 RED 状态下 refactor。

## 每个 Cycle 检查

```text
[ ] Test describes behavior, not implementation
[ ] Test uses public interface or accepted system boundary
[ ] Test would survive internal refactor
[ ] RED failure proves the intended gap or bug
[ ] Code is minimal for this behavior
[ ] No speculative features added
[ ] Relevant tests pass after GREEN / REFACTOR
```

## 验证方式

- 记录每个重要 cycle 的 RED/GREEN/REFACTOR 证据：测试文件、失败原因、修复范围和通过命令。
- Bugfix 必须保留复现失败的测试或等价 repro loop。
- 如果无法自动化测试，说明原因，并执行最接近用户可观察行为的手动、静态或 CLI 验证。
- 完成前报告已覆盖行为、未覆盖范围、运行命令和残留风险。
