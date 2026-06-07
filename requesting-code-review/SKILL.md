---
name: requesting-code-review
description: Use when reviewing local implementation changes, PR diffs, completed issues, generated code, test additions, or subagent output for spec compliance, acceptance criteria coverage, code quality, regression risk, missing tests, or maintainability before declaring implementation complete.
---

# Requesting Code Review

对实现结果做两阶段评审：先确认有没有做对，再确认做法是否可靠。评审优先输出问题，不先写总结。

## 输入

- PRD、spec、issue、plan 或用户原始要求。
- `git diff` / changed files / subagent handoff。
- 测试结果、验证命令和已知跳过项。

## Stage 1：Spec Compliance Review

检查实现是否满足承诺的行为：

- 每个 acceptance criterion 是否被覆盖。
- 有没有漏做 requirement、user story、edge case。
- 有没有超出 scope 引入额外行为或破坏 out-of-scope。
- 测试是否验证 external behavior，而不是 implementation details。
- Bugfix 是否包含正确 failure mode 的 regression test 或等价验证。

## Stage 2：Code Quality Review

检查实现质量和维护风险：

- 接口、schema、migration、状态机或 workflow 是否破坏兼容性。
- 错误处理、边界条件、并发/异步、资源清理是否可靠。
- 是否引入重复、过度抽象、隐藏耦合或难测结构。
- 测试是否 flaky、过浅、依赖顺序或环境。
- 临时 instrumentation、debug file、prototype 是否清理。

## 输出格式

```markdown
## Findings

- HIGH [file:line] 问题描述。
  Impact: ...
  Recommendation: ...

## Open Questions

- ...

## Review Summary

- Spec compliance: pass / fail
- Code quality: pass / fail
- Tests reviewed: ...
```

严重度：

- `CRITICAL`: 会导致核心功能错误、数据损坏、安全问题、无法合并。
- `HIGH`: requirement 漏做、测试不能证明行为、明显回归风险。
- `MEDIUM`: 维护性、边界条件、非核心覆盖不足。
- `LOW`: 命名、格式、轻微重复。

## 执行规则

- 如果用户只要求 review，不要直接改代码。
- 如果作为 `implement` 的内部质量门，`CRITICAL` 和 `HIGH` 必须在完成前修复或明确交给用户决定。
- 没有发现问题时明确说 “No findings”，并列出仍未验证的范围。

## 完成标准

- 已分别完成 spec compliance 和 code quality。
- Findings 有文件位置、影响和建议。
- 已说明是否阻塞 completion。
