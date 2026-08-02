---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

> **`description` 中文译文：** 当你已有 multi-step task 的 spec 或需求、且尚未开始修改代码时使用此 Skill。

# Writing Plans

> **标题中文译文：** 编写计划

## Overview（概览）

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

> **中文译文：** 编写全面的实现计划，并假设工程师对我们的代码库毫无 context，且品味存疑。记录他们需要知道的一切：每个 task 要修改哪些文件、具体代码、测试、可能需要查阅的文档，以及如何测试。把完整计划拆成 bite-sized task。遵循 DRY、YAGNI、TDD，并频繁 commit。

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

> **中文译文：** 假设他们是熟练的开发者，但对我们的 toolset 或问题域几乎一无所知；同时假设他们不太了解良好的测试设计。

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

> **中文译文：** **开始时声明：** “我正在使用 writing-plans skill 创建实现计划。”

**Context:** If working in an isolated worktree, it should have been created via the `superpowers:using-git-worktrees` skill at execution time.

> **中文译文：** **Context：** 如果正在隔离的 worktree 中工作，该 worktree 应已在执行阶段通过 `superpowers:using-git-worktrees` skill 创建。

**Save plans to:** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`
- (User preferences for plan location override this default)

> **中文译文：** **计划保存位置：** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`。
> - 用户对计划位置的偏好会覆盖此默认值。

## Scope Check（Scope 检查）

If the spec covers multiple independent subsystems, it should have been broken into sub-project specs during brainstorming. If it wasn't, suggest breaking this into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

> **中文译文：** 如果 spec 覆盖多个相互独立的子系统，它本应在 brainstorming 阶段被拆成多个子项目 spec。如果尚未拆分，建议把它拆成多个独立 plan——每个子系统一个。每个 plan 都应能独立产出可工作、可测试的软件。

## File Structure（文件结构）

Before defining tasks, map out which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

> **中文译文：** 定义 task 之前，先规划要创建或修改哪些文件，以及每个文件负责什么。这一步会锁定拆分决策。

- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- You reason best about code you can hold in context at once, and your edits are more reliable when files are focused. Prefer smaller, focused files over large ones that do too much.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. If the codebase uses large files, don't unilaterally restructure - but if a file you're modifying has grown unwieldy, including a split in the plan is reasonable.

> **中文译文：**
> - 设计边界清晰、interface 定义明确的单元。每个文件应只有一个明确职责。
> - 你最擅长推理能一次放进 context 的代码，而且文件职责越聚焦，编辑越可靠。应优先选择较小且聚焦的文件，避免承担过多职责的大文件。
> - 一起变化的文件应放在一起。按职责拆分，而不是按技术分层拆分。
> - 在现有代码库中遵循已有 pattern。如果代码库使用大文件，不要单方面调整结构；但如果你正在修改的文件已变得难以驾驭，把拆分纳入 plan 是合理的。

This structure informs the task decomposition. Each task should produce self-contained changes that make sense independently.

> **中文译文：** 这一结构会指导 task 拆分。每个 task 都应产出自包含、单独看也合理的变更。

## Task Right-Sizing（Task 大小控制）

A task is the smallest unit that carries its own test cycle and is worth a
fresh reviewer's gate. When drawing task boundaries: fold setup,
configuration, scaffolding, and documentation steps into the task whose
deliverable needs them; split only where a reviewer could meaningfully
reject one task while approving its neighbor. Each task ends with an
independently testable deliverable.

> **中文译文：** 一个 task 是既拥有自身测试循环、又值得由新 reviewer 设置一道 gate 的最小单元。划分 task 边界时，把 setup、configuration、scaffolding 和 documentation 步骤归入需要它们的 deliverable 所属 task；只有当 reviewer 可以有意义地拒绝一个 task、同时批准相邻 task 时，才进行拆分。每个 task 最终都要产出可独立测试的 deliverable。

## Bite-Sized Task Granularity（小步 Task 粒度）

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

> **中文译文：** **每个 step 只包含一个动作（2-5 分钟）：**
> - “编写失败测试”——一个 step。
> - “运行测试并确认失败”——一个 step。
> - “编写使测试通过的最小实现”——一个 step。
> - “运行测试并确认通过”——一个 step。
> - “Commit”——一个 step。

## Plan Document Header（Plan 文档头部）

**Every plan MUST start with this header:**

> **中文译文：** **每个 plan 都必须以此 header 开始：**

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

## Global Constraints

[The spec's project-wide requirements — version floors, dependency limits,
naming and copy rules, platform requirements — one line each, with exact
values copied verbatim from the spec. Every task's requirements implicitly
include this section.]

---
```

> **中文译文：** header 必须包含 feature 名称，并明确要求 agentic worker 使用 `superpowers:subagent-driven-development`（推荐）或 `superpowers:executing-plans`，以逐 task 的方式实施 plan；各 step 使用 `- [ ]` checkbox 语法跟踪。header 还必须包含单句 `Goal`、2-3 句 `Architecture`、关键 `Tech Stack`，以及 `Global Constraints`。`Global Constraints` 应逐行记录从 spec 原样复制的项目级要求，包括版本下限、dependency 限制、命名与 copy 规则和平台要求；每个 task 都隐含包含这些要求。

## Task Structure（Task 结构）

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Interfaces:**
- Consumes: [what this task uses from earlier tasks — exact signatures]
- Produces: [what later tasks rely on — exact function names, parameter
  and return types. A task's implementer sees only their own task; this
  block is how they learn the names and types neighboring tasks use.]

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

> **中文译文：** 每个 task 以 `### Task N: [Component Name]` 开始，并精确列出要创建、修改和测试的文件。`Interfaces` 必须说明该 task 从更早 task 消费的精确 signature，以及后续 task 依赖的精确 function name、parameter 和 return type；因为 task implementer 只会看到自己的 task，这个 block 是他们了解相邻 task 名称和类型的途径。随后用 checkbox step 依次给出失败测试、验证失败的精确命令和预期输出、最小实现、验证通过的精确命令和预期输出，以及限定文件范围的 commit 命令。

## No Placeholders（不得使用占位说明）

Every step must contain the actual content an engineer needs. These are **plan failures** — never write them:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code — the engineer may be reading tasks out of order)
- Steps that describe what to do without showing how (code blocks required for code steps)
- References to types, functions, or methods not defined in any task

> **中文译文：** 每个 step 都必须包含工程师实际需要的内容。以下内容属于 **plan failure**，绝不要写入：
> - “TBD”、“TODO”、“implement later”或“fill in details”。
> - “Add appropriate error handling”、“add validation”或“handle edge cases”。
> - “Write tests for the above”，却没有实际测试代码。
> - “Similar to Task N”；必须重复代码，因为工程师可能不按顺序阅读 task。
> - 只描述做什么却不展示如何做的 step；涉及代码的 step 必须包含 code block。
> - 引用未在任何 task 中定义的 type、function 或 method。

## Self-Review（自审）

After writing the complete plan, look at the spec with fresh eyes and check the plan against it. This is a checklist you run yourself — not a subagent dispatch.

> **中文译文：** 完整 plan 写完后，以全新视角重新审视 spec，并对照 spec 检查 plan。这是一份你亲自执行的 checklist，而不是一次 subagent dispatch。

**1. Spec coverage:** Skim each section/requirement in the spec. Can you point to a task that implements it? List any gaps.

> **中文译文：** **1. Spec 覆盖度：** 浏览 spec 的每个 section 和 requirement。你能指出实现它的具体 task 吗？列出所有缺口。

**2. Placeholder scan:** Search your plan for red flags — any of the patterns from the "No Placeholders" section above. Fix them.

> **中文译文：** **2. Placeholder 扫描：** 在 plan 中搜索危险信号，即上文 “No Placeholders” 一节列出的任何 pattern，并修复它们。

**3. Type consistency:** Do the types, method signatures, and property names you used in later tasks match what you defined in earlier tasks? A function called `clearLayers()` in Task 3 but `clearFullLayers()` in Task 7 is a bug.

> **中文译文：** **3. Type 一致性：** 后续 task 使用的 type、method signature 和 property name 是否与前面 task 的定义一致？如果同一 function 在 Task 3 中叫 `clearLayers()`，在 Task 7 中却叫 `clearFullLayers()`，这就是 bug。

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.

> **中文译文：** 如果发现问题，就地修复。无需重新审阅——修复后继续。如果发现某项 spec requirement 没有对应 task，就添加该 task。

## Execution Handoff（执行交接）

After saving the plan, offer execution choice:

> **中文译文：** 保存 plan 后，提供执行方式选择：

**"Plan complete and saved to `docs/superpowers/plans/<filename>.md`. Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?"**

> **中文译文：** “Plan 已完成并保存到 `docs/superpowers/plans/<filename>.md`。有两种执行方式：
>
> **1. Subagent-Driven（推荐）**——我为每个 task 派发一个全新 subagent，并在 task 之间进行 review，以便快速迭代。
>
> **2. Inline Execution**——在当前 session 中使用 executing-plans 执行 task，采用带 checkpoint 的批量执行。
>
> 选择哪一种？”

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use superpowers:subagent-driven-development
- Fresh subagent per task + two-stage review

> **中文译文：** **如果选择 Subagent-Driven：**
> - **REQUIRED SUB-SKILL：** 使用 superpowers:subagent-driven-development。
> - 每个 task 使用一个全新 subagent，并进行两阶段 review。

**If Inline Execution chosen:**
- **REQUIRED SUB-SKILL:** Use superpowers:executing-plans
- Batch execution with checkpoints for review

> **中文译文：** **如果选择 Inline Execution：**
> - **REQUIRED SUB-SKILL：** 使用 superpowers:executing-plans。
> - 批量执行，并设置 review checkpoint。
