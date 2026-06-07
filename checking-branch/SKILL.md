---
name: checking-branch
description: Use when starting implementation work after the user has prepared a git branch, checking the current branch, refusing to implement on main/master unless explicitly allowed, inspecting dirty git status, running baseline checks, or confirming the branch is ready before code changes.
---

# Checking Branch

开始实现前确认当前分支和基线。这个 skill 假设用户会先准备好开发分支；agent 不主动创建额外工作空间，也不默认新建分支。

## 核心规则

- 先检查当前 git 状态，再开始写文件。
- 不要覆盖、stash、reset 或删除用户已有改动，除非用户明确要求。
- 如果当前在 `main` / `master`，停下来要求用户切换到开发分支；只有用户明确允许时才在主分支继续。
- 如果当前分支已经是用户准备好的开发分支，继续使用当前分支。
- 如果已有未提交改动，判断是否与本任务相关；相关则读懂后继续，不相关则避开并在报告中说明。

## 工作流程

1. 检查仓库状态。

```bash
git status --short
git branch --show-current
git rev-parse --show-toplevel
```

2. 判断是否可以实现。
   - 当前在开发分支且改动范围清楚：继续。
   - 当前在 `main` / `master`：暂停，要求用户先切换分支，或明确授权继续。
   - 当前不是 git 仓库：说明无法做分支检查，只能在当前目录继续。
   - 当前有无关改动：不要触碰；必要时说明哪些文件将避开。

3. 建立基线。
   - 读取项目 README/AGENTS/CONTEXT 中的 setup/test 命令。
   - 有快速测试时先跑 baseline。
   - 如果 baseline 已失败，记录失败并询问是否先修 baseline 或继续目标任务。

4. 报告准备状态。

```text
Repository: <path>
Branch: <branch>
Baseline: pass / fail / skipped (<reason>)
Pre-existing changes: <none or list>
```

## 降级策略

- 没有 git 仓库：继续前说明无法验证分支隔离。
- 测试太慢或缺少依赖：记录跳过原因，后续 `verification-before-completion` 需要重新评估验证范围。
- 分支状态不满足要求且用户不在：停止实现，不要自行创建或切换分支。

## 完成标准

- 当前分支已确认可用于实现，或用户明确允许例外。
- Baseline 是否通过已经记录。
- 用户已有改动没有被覆盖或误纳入本任务。
- 实现阶段可以安全继续。
