# 测试示例（Good and Bad Tests）

## Good Tests

Good tests 通过真实 interface 验证 observable behavior，而不是 mock 内部细节。

```typescript
// GOOD: Tests observable behavior
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

特征：

- 测试用户或调用方关心的 behavior。
- 只使用 public API。
- 能承受内部 refactor。
- 描述 WHAT，而不是 HOW。
- 每个测试聚焦一个 logical assertion。

## Bad Tests

Implementation-detail tests 会耦合内部结构。

```typescript
// BAD: Tests implementation details
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

危险信号：

- Mock 内部 collaborators。
- 测试 private methods。
- 断言 call counts 或 call order。
- 外部行为没变时，refactor 会打碎测试。
- 测试名称描述 HOW，而不是 WHAT。
- 绕过 interface 去验证外部状态。

```typescript
// BAD: Bypasses interface to verify
test("createUser saves to database", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});

// GOOD: Verifies through interface
test("createUser makes user retrievable", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```
