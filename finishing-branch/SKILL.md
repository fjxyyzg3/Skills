---
name: finishing-branch
description: Use after implementation or debugging work is complete on a local branch/worktree, when preparing handoff, summarizing git status, deciding merge/PR/commit/keep/discard options, cleaning branch artifacts, or reporting final verification and residual risks.
---

# Finishing Branch

完成开发分支时整理交付状态。它不自动 merge、push、discard；只在用户明确要求时执行这些改变远端或历史的动作。

## 前置条件

- 已运行 `verification-before-completion`，或明确说明为什么无法运行。
- 已处理 `requesting-code-review` 中的阻塞问题，或用户接受残留风险。

## 工作流程

1. 汇总分支状态。

```bash
git branch --show-current
git status --short
git diff --stat
```

2. 汇总交付内容。
   - 需求/issue 覆盖范围。
   - 关键文件变更。
   - 测试和验证命令。
   - 未解决风险。

3. 给出后续选项。
   - `keep branch`: 保留当前分支，用户继续检查。
   - `commit`: 用户要求时再按清晰 scope 提交。
   - `push / PR`: 用户要求时再使用对应 GitHub/remote workflow。
   - `merge`: 用户明确要求且验证通过时才执行。
   - `discard`: 只有用户明确要求并确认目标路径/分支时才执行。

4. 清理可安全清理的内容。
   - 停止本任务启动的后台进程。
   - 删除本任务创建且明确临时的文件。
   - 不清理未知来源文件。

## 输出格式

```markdown
## Branch Finish Report

- Branch: <name>
- Status: clean / dirty
- Changed files: ...
- Verification: ...
- Residual risk: ...
- Recommended next step: ...
```

## 完成标准

- 用户能清楚知道分支是否可交付。
- 没有自动执行 merge/push/delete 等高影响操作。
- 已说明下一步建议和原因。
