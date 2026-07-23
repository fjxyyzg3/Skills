---
name: checking-branch
description: "作为 $implement 选择可执行路径后的内部 branch gate，或用户明确要求检查、准备、创建或切换 Git 分支时使用；先展示状态，确认直接修改或指定分支，推导安全 base 并运行 baseline 检查；保留英文触发短语 inspect, prepare, create, or switch a Git branch。"
---

# Checking Branch

作为实现工作流的内部 branch gate，或响应用户明确的 branch-only 请求。先展示当前分支和 Git 状态，再让用户选择直接修改或提供新分支名。

## 触发说明（Trigger Description）

- 普通实现请求先进入 `$implement`；本 skill 不与唯一实现入口竞争。
- `$implement` 完成只读路径分派、确认 Path 可执行后，把本 skill 作为内部 `N1 Branch Gate` 使用。
- 用户明确只要求检查状态、准备分支、创建分支或切换分支时，可以直接进入本 skill。

## 压力场景（Pressure Scenarios）

1. 用户说：“实现这个已收束需求。”
   - 预期触发：`$implement`，不是独立 `$checking-branch`。
   - 禁止动作：在路径/范围分派前先创建或切换分支。
   - 通过信号：只有目标工作流调用本 skill 后才执行 branch gate。
2. `$implement` 已选择 Quick 或 Standard，并调用 branch gate。
   - 预期触发：展示状态、已有改动与 baseline，并等待直接修改/新分支选择。
   - 禁止动作：把路径选择当成分支修改授权。
   - 通过信号：用户明确同意直接修改，或提供的新分支已安全创建/切换。
3. 用户说：“只帮我从默认分支创建 `feat/x`，暂时不要实现。”
   - 预期触发：直接执行 branch-only 工作流。
   - 禁止动作：顺带开始业务实现。
   - 通过信号：branch/base/baseline 被报告，随后自然结束。

## 核心规则

- 除明确 branch-only 请求外，只接受 `$implement` 等目标 workflow 的内部 gate 调用。
- 先检查当前 git 状态，再开始写文件。
- 不要覆盖、stash、reset 或删除用户已有改动，除非用户明确要求。
- 必须向用户展示当前分支名和分支状态，然后确认是否直接修改。
- 如果用户同意直接修改，继续使用当前分支。
- 如果用户没有同意直接修改，而是提供新分支名，创建并切换到该分支。
- 创建新分支时，默认从当前仓库定义的主分支派生；如果无法确认主分支，必须再向用户确认是否从当前分支派生。
- 如果已有未提交改动，判断是否与本任务相关；相关则读懂后继续，不相关则避开并在报告中说明。

## 工作流程

1. 检查仓库状态。

```bash
git status -sb
git branch --show-current
git rev-parse --show-toplevel
```

2. 展示当前状态并询问用户。

```text
Repository: <path>
Current branch: <branch>
Status: clean / dirty (<short summary>)

是否直接在当前分支修改？如果不直接修改，请给出新分支名。
```

3. 处理用户选择。
   - 用户同意直接修改：继续使用当前分支。
   - 用户提供新分支名：创建并切换到新分支。
   - 用户拒绝直接修改但未提供分支名：停止实现，等待分支名。
   - 当前不是 git 仓库：说明无法做分支检查，只能在当前目录继续。
   - 当前有无关改动：不要触碰；必要时说明哪些文件将避开。

4. 创建新分支时选择 base。

优先尝试仓库定义的主分支：

```bash
git symbolic-ref --short refs/remotes/origin/HEAD
git remote show origin
```

选择规则：

- 如果能解析到 `origin/<default-branch>`，先 `git fetch origin`，再从 `origin/<default-branch>` 创建新分支。
- 如果没有 remote default branch，但本地存在 `main` 或 `master`，从本地 `main` 或 `master` 创建。
- 如果无法确认仓库主分支，向用户说明无法确认的原因，并询问是否从当前分支创建。
- 只有用户确认从当前分支派生后，才能从当前分支创建新分支。
- 不要覆盖已有同名分支；若分支已存在，询问用户是切换到已有分支还是换名。

5. 建立基线。
   - 读取项目 README/AGENTS/CONTEXT 中的 setup/test 命令。
   - 有快速测试时先跑 baseline。
   - 如果 baseline 已失败，记录失败并询问是否先修 baseline 或继续目标任务。

6. 报告准备状态。

```text
Repository: <path>
Branch: <branch>
Branch decision: direct / created from <base>
Baseline: pass / fail / skipped (<reason>)
Pre-existing changes: <none or list>
```

## 降级策略

- 没有 git 仓库：继续前说明无法验证分支状态。
- 测试太慢或缺少依赖：记录跳过原因，后续 `verification-before-completion` 需要重新评估验证范围。
- 用户既不同意直接修改、也没有提供新分支名：停止实现，不要自行创建或切换分支。
- 用户提供新分支名但无法确认主分支，且没有同意从当前分支派生：停止实现，不要自行创建分支。

## 完成标准

- 已向用户展示当前分支名和状态。
- 用户已同意直接修改，或已按用户提供的新分支名创建/切换分支。
- Baseline 是否通过已经记录。
- 用户已有改动没有被覆盖或误纳入本任务。
- 实现阶段可以安全继续。

## 自然交接（Natural Handoff）

- 作为内部 gate 调用时，把分支选择和 baseline 结果返回给调用中的 `$implement`；这不是新的跨 skill 交接。
- 用户只要求 branch 操作时，完成后推荐 `none`，不自动开始实现。
