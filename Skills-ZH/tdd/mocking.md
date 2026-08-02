# When to Mock（何时使用 Mock）

Mock at **system boundaries** only:

- External APIs (payment, email, etc.)
- Databases (sometimes - prefer test DB)
- Time/randomness
- File system (sometimes)

> **中文译文：** 只在 **system boundary** 处使用 mock：
>
> - External API（支付、电子邮件等）。
> - 数据库（有时可以，但优先使用 test DB）。
> - 时间或随机性。
> - 文件系统（有时）。

Don't mock:

- Your own classes/modules
- Internal collaborators
- Anything you control

> **中文译文：** 不要 mock：
>
> - 你自己的 class 或 module。
> - 内部协作者。
> - 任何由你控制的事物。

## Designing for Mockability（为可 Mock 性而设计）

At system boundaries, design interfaces that are easy to mock:

> **中文译文：** 在 system boundary 处，设计易于 mock 的 interface：

**1. Use dependency injection**

> **中文译文：** **1. 使用 dependency injection**

Pass external dependencies in rather than creating them internally:

> **中文译文：** 从外部传入 dependency，而不是在内部创建：

```typescript
// Easy to mock
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// Hard to mock
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

> **代码说明：** 将 `paymentClient` 作为参数传入时易于 mock；在函数内部创建 `StripeClient` 时则难以 mock。

**2. Prefer SDK-style interfaces over generic fetchers**

> **中文译文：** **2. 优先使用 SDK-style interface，而不是通用 fetcher**

Create specific functions for each external operation instead of one generic function with conditional logic:

> **中文译文：** 为每个外部操作创建特定 function，而不是使用一个包含条件逻辑的通用 function：

```typescript
// GOOD: Each function is independently mockable
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch('/orders', { method: 'POST', body: data }),
};

// BAD: Mocking requires conditional logic inside the mock
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

> **代码说明：** 前一个 interface 的每个 function 都可独立 mock；后一个 interface 要求在 mock 内部加入条件逻辑。

The SDK approach means:
- Each mock returns one specific shape
- No conditional logic in test setup
- Easier to see which endpoints a test exercises
- Type safety per endpoint

> **中文译文：** SDK 方法意味着：
> - 每个 mock 只返回一种特定 shape。
> - 测试 setup 中没有条件逻辑。
> - 更容易看出测试调用了哪些 endpoint。
> - 每个 endpoint 都有 type safety。
