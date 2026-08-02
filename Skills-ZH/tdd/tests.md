# Good and Bad Tests（良好测试与糟糕测试）

## Good Tests（良好测试）

**Integration-style**: Test through real interfaces, not mocks of internal parts.

> **中文译文：** **Integration-style**：通过真实 interface 进行测试，而不是 mock 内部组成部分。

```typescript
// GOOD: Tests observable behavior
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

> **代码说明：** 此测试通过公共 interface 验证可观察行为。

Characteristics:

- Tests behavior users/callers care about
- Uses public API only
- Survives internal refactors
- Describes WHAT, not HOW
- One logical assertion per test

> **中文译文：**
> - 测试用户或 caller 关心的行为。
> - 只使用 public API。
> - 能经受住内部 refactor。
> - 描述 WHAT，而不是 HOW。
> - 每个测试只包含一个逻辑 assertion。

## Bad Tests（糟糕测试）

**Implementation-detail tests**: Coupled to internal structure.

> **中文译文：** **实现细节测试**：与内部结构耦合。

```typescript
// BAD: Tests implementation details
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

> **代码说明：** 此测试验证实现细节，因此与内部结构耦合。

Red flags:

- Mocking internal collaborators
- Testing private methods
- Asserting on call counts/order
- Test breaks when refactoring without behavior change
- Test name describes HOW not WHAT
- Verifying through external means instead of interface

> **中文译文：**
> - Mock 内部协作者。
> - 测试 private method。
> - 对调用次数或顺序进行 assertion。
> - 行为未改变，测试却在 refactor 时失败。
> - 测试名称描述 HOW，而不是 WHAT。
> - 不通过 interface，而是使用外部手段验证。

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

> **代码说明：** 前一个测试绕过 interface 查询数据库；后一个测试通过 public interface 验证用户可以被取回。

**Tautological tests**: Expected value restates the implementation, so the test passes by construction.

> **中文译文：** **同义反复测试**：Expected value 重述实现，因此测试从构造上就必然通过。

```typescript
// BAD: Expected value is recomputed the way the code computes it
test("calculateTotal sums line items", () => {
  const items = [{ price: 10 }, { price: 5 }];
  const expected = items.reduce((sum, i) => sum + i.price, 0);
  expect(calculateTotal(items)).toBe(expected);
});

// GOOD: Expected value is an independent, known literal
test("calculateTotal sums line items", () => {
  expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
});
```

> **代码说明：** 前一个测试用与实现相同的方式重新计算 expected value；后一个测试使用独立且已知正确的 literal。
