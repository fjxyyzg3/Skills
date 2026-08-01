# Deepening

本文件说明如何根据依赖类型安全加深一组 shallow modules。术语沿用 `language.md`：module、interface、seam、adapter、leverage、locality。

## Dependency Categories

### 1. In-process

纯计算、内存状态、无 I/O。通常可以直接 deepening：合并或重塑 modules，并通过新的 interface 测试 behavior。不需要 adapter。

### 2. Local-substitutable

依赖有本地测试替身，例如 PGLite、in-memory filesystem、本地 fake queue。可以 deepening，但测试要通过本地替身跨 seam 验证。seam 通常是 internal seam，不一定暴露在 module 的 external interface。

### 3. Remote But Owned: Ports & Adapters

跨网络访问自己控制的服务，例如 internal API、microservice、queue worker。deep module 拥有业务逻辑；transport 通过 port 注入，production adapter 使用 HTTP/gRPC/queue，tests 使用 in-memory adapter。

推荐表达：

> Define a port at the seam, implement a production adapter and an in-memory test adapter, so logic sits in one deep module even though transport crosses a network.

### 4. True External: Mock

第三方服务，例如 Stripe、Twilio、OpenAI API。deep module 把外部依赖作为 injected port；tests 使用 mock adapter。不要假装第三方 behavior 是自己可以重塑的 implementation。

## Seam Discipline

- One adapter = hypothetical seam。Two adapters = real seam。
- 不要因为测试想 mock 就把所有 internal seams 暴露成 external interface。
- deep module 可以有 private internal seams，供自己的 tests 或 implementation 使用。
- external seam 应服务 callers，而不是服务 implementation 的偶然结构。

## Testing Strategy

- 新 tests 应跨 deepened module 的 interface 验证 observable outcomes。
- 旧 shallow module unit tests 如果只锁死 implementation details，应删除或迁移。
- Tests 不应断言 internal state、调用顺序或 private helpers，除非这些本来就是 interface 的一部分。
- 如果 implementation 变化会迫使 tests 大量改写，说明 tests 可能越过了 interface。
