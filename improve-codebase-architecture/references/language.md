# Architecture Language

本文件定义 `improve-codebase-architecture` 必须使用的架构词汇。建议中要保持术语一致，不要随意替换成 `component`、`service`、`API` 或 `boundary`。

## Terms

**Module**

任何同时拥有 interface 和 implementation 的东西。尺度不限，可以是 function、class、package，也可以是跨层 slice。

避免用：unit、component、service。

**Interface**

调用方为了正确使用 module 必须知道的一切。不只是 type signature，还包括 invariants、ordering constraints、error modes、required configuration 和 performance characteristics。

避免用：API、signature。它们过窄，只覆盖类型层面的表面。

**Implementation**

module 内部的代码和行为。它不同于 adapter：adapter 是在某个 seam 上满足 interface 的具体角色。

**Depth**

interface 上的 leverage。调用方或测试每学习一单位 interface，可以触达多少 behavior。deep module 用较小 interface 隐藏大量 behavior；shallow module 的 interface 几乎和 implementation 一样复杂。

**Seam**

可以不在原处编辑就改变 behavior 的位置，也就是 module interface 所在的位置。选择 seam 是设计决策。

避免用：boundary。它容易和 DDD bounded context 混淆。

**Adapter**

在 seam 上满足 interface 的具体实现。它描述角色，不描述内部规模。

**Leverage**

调用方从 depth 得到的收益：一个小 interface 支撑更多能力，一个 implementation 回报多个 call sites 和 tests。

**Locality**

维护者从 depth 得到的收益：change、bugs、knowledge 和 verification 集中在一个地方，而不是散在多个 callers。

## Principles

- Depth 是 interface 的属性，不是 implementation 行数的属性。
- 一个 deep module 内部可以有 internal seams，但这些 seams 不应该自动暴露给 callers。
- Deletion test：想象删除某个 module。如果复杂度消失，它可能只是 pass-through；如果复杂度重新散落到多个 callers，它在创造 locality。
- Interface is the test surface：tests 和 callers 应该跨同一个 seam。
- One adapter = hypothetical seam。Two adapters = real seam。不要为了单一 adapter 引入外部 seam。

## Relationships

- 一个 Module 暴露一个 Interface。
- Depth 根据 Module 的 Interface 衡量。
- Seam 是 Interface 所在的位置。
- Adapter 位于 Seam 上并满足 Interface。
- Depth 为 callers 产生 Leverage，为 maintainers 产生 Locality。

## Rejected Framings

- 不用 implementation lines / interface lines 的比例衡量 depth；这会奖励膨胀 implementation。
- 不把 Interface 缩窄成 TypeScript `interface` keyword 或 public methods。
- 不用 Boundary 表示 seam。
