# Mocking Guidelines

## 什么时候 Mock

只在 system boundaries mock：

- External APIs，例如 payment、email、third-party service。
- Databases，必要时 mock；优先考虑 test DB。
- Time、randomness。
- File system，必要时 mock。

不要 mock：

- 自己的 classes/modules。
- Internal collaborators。
- 任何你能直接控制的逻辑。

## 为 Mockability 设计

在 system boundaries，设计容易替换的 interface。

### 1. 使用 dependency injection

把外部依赖传入，而不是在函数内部创建：

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

### 2. 优先 SDK-style interfaces

给每个外部操作定义明确函数，不要用一个带条件分支的 generic fetcher。

```typescript
// GOOD: Each function is independently mockable
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch("/orders", { method: "POST", body: data }),
};

// BAD: Mocking requires conditional logic inside the mock
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

SDK-style interface 的好处：

- 每个 mock 返回一种具体 shape。
- 测试 setup 不需要条件逻辑。
- 更容易看出测试触达哪些 endpoint。
- 每个 operation 可以有更清楚的 type。
