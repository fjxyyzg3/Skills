# Retire Workflow Gate Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 删除 `analyze`、`checking-branch`、`requesting-code-review`、`verification-before-completion` 和 `finishing-branch`，并让剩余活动 Skill 不再依赖这些独立入口。

**Architecture:** 将 branch check、artifact quality check、两阶段 review、最终 verification 和交付决策收回 `implement/SKILL.md` 的内部节点；`to-plan` 继续在自己的 Planning Run 中检查输入 artifacts，`brainstorming` 与 `to-spec` 不再暴露已删除的 audit handoff。README、AGENTS 和活动 examples 只描述保留的 11 个 Skill；`Skills/docs/features/` 中既有历史记录不改写。

**Tech Stack:** Markdown、YAML metadata、PowerShell、`rg`、Git。

---

### Task 1: 收回 `implement` 的内部安全门

**Files:**
- Modify: `Skills/implement/SKILL.md`
- Modify: `Skills/implement/references/quick-path.md`

- [x] **Step 1: Replace cross-Skill gate references with local contracts**
  - N1 must directly require branch/status display, pre-existing-change protection, branch decision, safe base selection and baseline recording.
  - N3 must directly perform read-only artifact quality checks for ambiguity, coverage, contracts, paths, verification and quality-gate violations.
  - N5 must directly describe the two review passes: specification/acceptance compliance and code quality/regression risk; blocking findings require repair or explicit user decision.
  - N7 must directly check requirements, external-behavior evidence, artifact/link integrity, temporary content, process state, Git status, skipped validation and residual risk.
  - N8 must directly summarize branch/diff/delivery state and present `keep`/`commit`/`push`/`PR`/`merge`/`discard` options without performing high-impact actions implicitly.
- [x] **Step 2: Update the execution graph, node names, pressure scenarios and completion checklist**
  - Remove all references to the five retired Skill names and `$analyze`.
  - Rename the Quick Path's `N3 Analyze Gate` reference to the internal artifact quality gate.
  - Keep Quick/Standard/Blocked routing, serial TDD, review, verification and delivery behavior as internal `implement` gates.

### Task 2: Remove retired Skill packages

**Files:**
- Delete: `Skills/analyze/SKILL.md`
- Delete: `Skills/analyze/agents/openai.yaml`
- Delete: `Skills/checking-branch/SKILL.md`
- Delete: `Skills/checking-branch/agents/openai.yaml`
- Delete: `Skills/requesting-code-review/SKILL.md`
- Delete: `Skills/requesting-code-review/agents/openai.yaml`
- Delete: `Skills/verification-before-completion/SKILL.md`
- Delete: `Skills/verification-before-completion/agents/openai.yaml`
- Delete: `Skills/finishing-branch/SKILL.md`
- Delete: `Skills/finishing-branch/agents/openai.yaml`

- [x] **Step 1: Delete the complete package contents for all five retired Skills**
- [x] **Step 2: Confirm no retired directory still contains a `SKILL.md`**

### Task 3: Synchronize active routing documentation and examples

**Files:**
- Modify: `README.md`
- Modify: `AGENTS.md`
- Modify: `Skills/brainstorming/SKILL.md`
- Modify: `Skills/brainstorming/examples/brainstorming-session.md`
- Modify: `Skills/to-plan/SKILL.md`
- Modify: `Skills/to-plan/examples/adaptive-planning-scenarios.md`
- Modify: `Skills/to-spec/SKILL.md`

- [x] **Step 1: Remove retired Skills from the active README graph, inventory and rules**
  - Describe `implement` as the owner of its internal branch, artifact, review, verification and delivery gates.
  - Remove the standalone audit and retired Skill rows/edges.
- [x] **Step 2: Remove retired handoff/dependency wording from active Skill prose and examples**
  - Keep `to-plan`'s own quality gate for external/unchecked artifacts.
  - Remove the obsolete direct-audit scenario from the active planning scenario suite.
  - Remove the retired name from the AGENTS naming example.

### Task 4: Verify active topology and repository hygiene

**Files:**
- Test: `Skills/*/SKILL.md`, active `examples/`, `README.md`, `AGENTS.md`

- [x] **Step 1: Assert the remaining active inventory is exactly 11 Skills**
  - Expected: `brainstorming`, `clarify`, `diagnose`, `grill-me`, `handoff`, `implement`, `improve-codebase-architecture`, `session-curator`, `tdd`, `to-plan`, `to-spec`.
- [x] **Step 2: Scan active packages and root routing docs for retired names**
  - Exclude `Skills/docs/features/`, which is explicitly retained historical planning material.
  - Expected: zero matches in active Skill packages, `README.md` and `AGENTS.md`.
- [x] **Step 3: Check active Markdown links and whitespace**
  - Run the repository's available link/reference checks and `git diff --check`.
  - Do not claim `python scripts/validate-skills.py` unless the file exists in this checkout.
  - Result: 32 active local links pass, `git diff --check` passes; root validator is absent. The installed `quick_validate.py` passes 9 unchanged/changed active Skills and reports pre-existing unsupported frontmatter keys in `handoff` (`argument-hint`) and `session-curator` (`version`).
- [x] **Step 4: Review the final diff and worktree**
  - Confirm only the planned active contracts, new plan record and five retired packages changed.
  - Confirm no commit, push, merge, discard or branch cleanup is performed without explicit user instruction.
