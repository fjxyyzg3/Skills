---
name: using-worktrees
description: Use when starting implementation work, executing issues or plans, isolating changes from main/master, creating or selecting a git branch/worktree, checking dirty worktrees, running setup, or establishing a clean baseline before code changes.
---

# Using Worktrees

开始实现前建立隔离工作空间和干净基线，避免把新改动混进用户已有工作。

## 核心规则

- 先检查当前 git 状态，再决定是否创建分支或 worktree。
- 不要覆盖、stash、reset 或删除用户已有改动，除非用户明确要求。
- 不在 `main` / `master` 上开始实现；如果已经在主分支，创建短分支名。
- 有平台原生 worktree/branch 工具时优先使用；没有时使用普通 git 分支即可。
- 如果工作树已 dirty，判断是否与本任务相关；相关则读懂后继续，不相关则避开。

## 工作流程

1. 检查仓库状态。

```bash
git status --short
git branch --show-current
git rev-parse --show-toplevel
```

2. 决定隔离方式。
   - 已在非主分支：通常继续使用当前分支。
   - 在 `main` / `master` 且工作树干净：创建 `work/<short-topic>` 或用户指定分支。
   - 在 `main` / `master` 且有用户改动：不要混写；询问是否创建 worktree/新分支，或只做只读分析。
   - 已在 git worktree：不要嵌套创建 worktree。

3. 建立基线。
   - 读取项目 README/AGENTS/CONTEXT 中的 setup/test 命令。
   - 有快速测试时先跑 baseline。
   - 如果 baseline 已失败，记录失败并询问是否先修 baseline 或继续目标任务。

4. 报告准备状态。

```text
Workspace: <path>
Branch: <branch>
Baseline: pass / fail / skipped (<reason>)
Dirty files before work: <none or list>
```

## 降级策略

- 没有 git 仓库：说明无法创建分支，只做当前目录内工作。
- 无法创建 worktree：退回当前分支或新分支，并说明原因。
- 测试太慢或缺少依赖：记录跳过原因，后续 `verification-before-completion` 需要重新评估验证范围。

## 完成标准

- 明确当前分支和工作空间。
- 明确 baseline 是否通过。
- 未破坏用户已有改动。
- 实现阶段可以安全继续。
