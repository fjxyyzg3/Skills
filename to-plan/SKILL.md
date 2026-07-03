---
name: to-plan
description: Use when converting a local spec, design doc, or conversation context into a sequential task-level implementation plan with exact file paths, interface contracts, requirement coverage, acceptance criteria, and verification commands, before starting implementation.
---

# To Plan

将 spec（或当前上下文）拆成任务级实现 plan。plan 回答"改哪些文件、接口契约是什么、每步怎么验证"；plan 决定分解，`implement` 决定代码——plan 中不预写实现代码。

## 进入边界

- 适用于已有 spec、design doc 或方向明确的 conversation context，需要拆成可执行 plan 的任务。
- 可以由用户显式调用，也可以由 `workflow-router` 或上一轮 `Natural Handoff` 推荐后进入。
- 不要把 plan 写成无来源的任务清单；每个 task 必须能通过 `Covers` 追溯到 requirement 或 conversation requirement。

## Language Contract

语言契约：生成的文档和聊天输出默认以中文优先；代码、命令、API 名称、契约字段、ID、专有名词以及必要的技术术语保留英文。用户或目标项目明确要求英文时可以例外，但必须记录原因。

## 输出约定

- 只生成本地 Markdown 文档，不创建远端 issue 或 ticket。
- 文档正文默认中文为主；核心 section heading 使用中文优先、English 括注。
- 保留 `Task`、`Files`、`Consumes`、`Produces`、`Covers` 等 workflow contract fields 和 `FR-###` 稳定 ID。
- plan 是单个 Markdown 文件：如果源 spec 位于 `docs/features/<feature-slug>/spec.md`，默认写入同目录 `plan.md`；用户指定路径时写入该路径。
- task 按执行顺序编号，编号即串行执行顺序。
- 如果存在 feature manifest，更新 Plan 状态和路径。

## Process

### 1. 收集上下文

优先读取用户给出的 spec。没有明确路径时，从当前上下文和 `docs/features/` 中寻找最相关 artifact。

同时读取与拆分直接相关的项目决策文档：

- 用户指定的来源文档。
- spec 引用的 ADRs、domain docs、接口说明或架构说明。
- 将要改动的代码区域，确认文件路径和现有接口是真实的，不要凭空编造路径。

如果 spec 覆盖多个互相独立的子系统，建议拆成多个 feature workspace 分别出 plan，而不是在一个 plan 里混排。

### 2. 确定文件落点

拆 task 之前，先映射本次改动会创建或修改哪些文件、每个文件的职责是什么。分解决策在这一步锁定：

- 单元边界清晰、职责单一；文件路径必须精确到真实路径，不写"某个合适的位置"。
- 在既有 codebase 中遵循已有组织模式，不顺手重组无关结构。

### 3. 拆成 task

拆分规则：

- 每个 task 是一个可独立验证的交付单元：完成后可以单独 demo、verify 或 test。
- task 大小以"值得一次独立验证"为准：把 setup、配置、文档等步骤折叠进需要它们的 task，只在验证边界处切分。
- task 之间的顺序就是执行顺序；有顺序约束的内容通过编号表达，不引入额外的依赖标注机制。
- 每个 task 声明 `Covers`：`FR-001`、`FR-001, FR-003` 或 `Conversation requirement: ...`。

### 4. 写清接口契约

相邻 task 之间通过 `Consumes/Produces` 传递契约：

- `Produces`: 本 task 产出、后续 task 会依赖的精确接口——函数/类/命令/字段名、参数和返回类型、文件产物路径。
- `Consumes`: 本 task 依赖的前置 task 产出，名称和类型必须与对应 `Produces` 逐字一致。
- 契约只写到签名和稳定字段层；实现方式留给 `implement`。

### 5. 先给用户确认拆分

除非用户明确要求直接写文件，否则先展示拟定 task 列表（编号、标题、Covers、主要 Files），用户确认后再写入。若用户要求直接产出，在 plan 的假设章节标记未确认 assumptions。

### 6. 写入 plan

使用下面模板：

````markdown
# <Feature Name> Plan

## 元数据 (Metadata)

- **Source**: <spec path / conversation context>
- **Generated at**: <YYYY-MM-DD>
- **Status**: Draft

## 假设 (Assumptions)

- None

## 全局约束 (Global Constraints)

- 从 spec 各章节（非目标、关键决策、测试决策等）提炼的项目级硬约束（版本下限、命名规则、语言契约等），每条一行。

## Task 列表 (Tasks)

### Task 1: <标题>

- **Files**:
  - Create: `exact/path/to/new-file`
  - Modify: `exact/path/to/existing-file`
  - Test: `exact/path/to/test-file`
- **Consumes**: None
- **Produces**: <后续 task 依赖的精确接口或产物>
- **Covers**: `FR-001`

**验收标准 (Acceptance Criteria)**:

- [ ] 用中文描述可独立验证的行为。

**验证命令 (Verification)**:

- `<command>`，预期 <结果>。

## Coverage 自查 (Coverage Self-Check)

| Requirement | Tasks | Notes |
| --- | --- | --- |
| FR-001 | Task 1 | ... |

未覆盖的 `FR-###` 必须注明原因。
````

### 7. 验证输出

写入后检查：

- 每个 task 都有 `Files`（精确路径）、`Consumes`、`Produces`、`Covers`、验收标准和验证命令。
- plan 中没有实现代码或测试代码；契约只到签名层。
- plan 中没有依赖图、执行波次、`Wave`/`Parallelization`/`AFK`/`HITL` 类字段、并行标记或 subagent 分工指引；顺序由 task 编号表达。
- 相邻 task 的 `Consumes`/`Produces` 名称与类型逐字一致。
- Coverage 自查表覆盖 spec 全部 `FR-###`，或明确说明未覆盖原因。
- 没有要求调用远端 tracker 或外部 skill。

最后报告 plan 路径、task 数量和 coverage 情况；如果建议实现前做只读一致性检查，用 `Natural Handoff` 推荐 `$analyze` 作为唯一 next skill，用户可以回复 `继续` 或显式写 `$analyze`；用户也可以直接显式调用 `$implement`。
