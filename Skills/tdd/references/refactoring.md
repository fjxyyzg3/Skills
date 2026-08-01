# Refactor Candidates

TDD cycle 全绿后再寻找这些 refactor 候选：

- Duplication -> extract function/class。
- Long methods -> 拆成 private helpers，但测试仍保持在 public interface。
- Shallow modules -> 合并或加深。
- Feature envy -> 把 logic 移到 data 所在处。
- Primitive obsession -> 引入 value objects。
- New code reveals existing problem -> 新实现暴露的旧结构问题。

Refactor 期间保持行为不变；如果出现新 behavior，先回到 RED/GREEN cycle。
