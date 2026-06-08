# Interface Design

当用户选中某个 deepening candidate，并希望继续探索 interface 形状时，使用本流程。目标是避免第一个方案过早定型。

## 1. Frame The Problem Space

先向用户说明候选的设计空间：

- 新 interface 必须满足的 constraints。
- 依赖分类，引用 `deepening.md` 的 dependency categories。
- seam 放置候选。
- implementation 需要隐藏的 ordering、config、error modes 和 dependency details。
- 一个用于说明约束的粗略 code sketch。它不是最终 proposal。

说明后直接进入方案设计，不要停在解释。

## 2. Generate Alternatives

有 parallel sub-agent 工具时，启动至少 3 个 agents。没有时，由当前 agent 自己产出至少 3 个明显不同的 designs。

每个 design 选择不同约束：

- Minimal interface: 目标是 1-3 个 entry points，最大化 leverage。
- Flexible interface: 支持更多 use cases 和 extension。
- Common caller optimized: 让最常见 caller 最简单。
- Ports & adapters: 当 dependency 跨 seam 时，优先设计 port 和 adapters。

每个 design 输出：

1. Interface：types、methods、params、invariants、ordering、error modes。
2. Usage example：caller 如何使用。
3. Hidden implementation：interface 后面隐藏什么。
4. Dependency strategy：adapter 和 seam 如何安排。
5. Trade-offs：leverage 高在哪里，locality 薄在哪里。

## 3. Compare And Recommend

按顺序展示 designs，再比较：

- Depth: 每个 entry point 提供多少 leverage。
- Locality: change 和 bugs 集中在哪里。
- Seam placement: caller 是否需要知道过多 internal details。
- Testing: tests 是否能跨 interface 验证 observable behavior。
- Migration: 对 existing callers 的迁移成本。

最后给出自己的推荐。如果多个 designs 可以组合，提出 hybrid，但要说明哪些部分保留、哪些部分丢弃。
