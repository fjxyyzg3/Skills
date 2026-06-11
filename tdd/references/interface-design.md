# Interface Design for Testability

好的 interface 会让测试自然落在 behavior 上。

## 1. Accept Dependencies, Don't Create Them

```typescript
// Testable
function processOrder(order, paymentGateway) {}

// Hard to test
function processOrder(order) {
  const gateway = new StripeGateway();
}
```

## 2. Return Results, Don't Produce Side Effects

```typescript
// Testable
function calculateDiscount(cart): Discount {}

// Hard to test
function applyDiscount(cart): void {
  cart.total -= discount;
}
```

## 3. Small Surface Area

- 更少 methods = 更少测试负担。
- 更少 params = 更简单的 test setup。
- 更明确 return type = 更少外部状态探查。
- 更少 hidden ordering = 更少 brittle tests。
