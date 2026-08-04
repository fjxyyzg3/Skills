---
name: to-spec
description: "当用户明确需要根据已确认设计、brainstorming 交接、规划讨论或对话上下文生成独立 formal spec 或 decision artifact，并要求稳定 requirement IDs、architecture decisions、tradeoffs 与 verification seams 时使用；保留英文触发短语 standalone formal spec、stable requirement IDs、architecture decisions、tradeoffs 和 verification seams。"
---

# To Spec

将方向共识和必要的 codebase 理解沉淀成本地叙事型 spec。spec 回答"要什么、为什么、边界在哪、怎么算成"；文件级落点和执行拆分是 plan 的职责，不属于 spec。

## 职责边界

- 本 skill 是 standalone formal spec 的唯一 owner：负责把已确认的方向写入 spec、维护对应 manifest，并完成 spec 自审与结构验证。`$to-plan` 的 Full Path 生成的 planning-coupled `spec.md` 不经过本 skill。
- 输入可以来自用户直接要求、`brainstorming` handoff、规划讨论或本地文件；如果来自 `brainstorming`，应消费其已确认的目标、范围、决策、约束、风险和 `Recommended spec focus`，不要无理由重新打开已收束的方案讨论。
- 本 skill 不负责重新主持 Brainstorming，不负责逐文件 implementation plan，也不修改业务代码；需要 checked plan 时由用户随后明确转入 `$to-plan`。
- spec-only 交付在报告 spec 与 manifest 路径后结束；不得在本 skill 内自动生成 plan 或进入实现。

## 进入边界

- 这是独立 formal-spec 入口：适用于用户明确要 spec、design doc、requirements 或长期 decision artifact，而不要求同一次运行生成 implementation plan。
- 适用于需要把 conversation context、brainstorming handoff、planning discussion 或本地文件整理成 spec/design doc 的任务。
- 可以由用户显式调用，也可以由当前 context trigger 进入。
- 不要把 spec 写成逐文件实施计划；实现细节只记录稳定 contract、schema、API、interaction 或 architecture decision。
- 如果用户要的是 checked implementation plan，应使用 `$to-plan`；其 Full Path 会在同一次 Planning Run 内生成需要的 spec 与 plan。

## 触发说明（Trigger Description）

`to-spec` 的 trigger 是用户明确需要独立 formal spec、requirements 或长期 decision artifact。它把已确认方向写成本地叙事文档；如果用户要的是 checked implementation plan，直接路由到 `$to-plan`。

## 压力场景（Pressure Scenarios）

1. 用户请求：“只要正式 spec，暂时不要 implementation plan。”
   - 预期触发：独立写 spec 与既有 feature manifest，并在完成后停止或推荐 `none`。
   - 未使用本 skill 时的常见失败：因 adaptive planning 存在而强制创建 plan。
   - 本 skill 必须强制的行为：保持 spec-only 产物边界。
2. brainstorming 交接已确认，但用户要求的结果是 checked plan。
   - 预期触发：不进入本 skill，改由 `$to-plan` 自动判断 Fast/Full。
   - 未使用本 skill 时的常见失败：恢复多一次 `$to-spec -> $to-plan` 中间确认。
   - 本 skill 必须强制的行为：formal spec 与 planning outcome owner 的职责不重叠。
3. spec 来源详细提到了文件和任务。
   - 预期触发：只固化稳定 contract、architecture decision 与 verification seam。
   - 未使用本 skill 时的常见失败：把 spec 写成逐文件 implementation plan。
   - 本 skill 必须强制的行为：文件级拆分留给 `$to-plan`。

## Spec 编写约定

- 只生成本地 Markdown 文档，不创建远端 issue 或 ticket。
- 核心 section heading 遵循目标 artifact 已有规范；`FR-001`、`SC-001` 等 workflow contract fields 保持稳定。
- 保留 `FR-001`、`SC-001`、`Metadata`、`Status`、`Source` 等 workflow contract fields 和稳定 ID。
- 如果用户指定输出路径，写入该路径；否则默认使用 `docs/features/<feature-slug>/spec.md`。
- 同时创建或更新 `docs/features/<feature-slug>/manifest.md`。
- 文件名使用简短、可读、lowercase kebab-case slug。

Spec 编写必须遵循以下职责规则：

- 先写清问题、现状、选定方案和被排除的 alternatives，再提炼可验证需求和成功标准。
- 每条功能需求使用稳定 `FR-###`；每条可由实现或验证直接影响的成功标准使用稳定 `SC-###`。
- 只记录稳定的 contract、schema、API、interaction、architecture decision 和 verification seam；文件级任务拆分、代码实现顺序和逐文件命令留给 `$to-plan`。
- spec 与 manifest 必须形成同一 feature workspace 的成对产物；除非用户指定路径，否则使用 `docs/features/<feature-slug>/`。
- 如果用户指定自定义 spec 路径，manifest 仍应放在同一 feature workspace；只有用户同时指定 manifest 路径时才使用该自定义路径。
- 写入后必须执行本 skill 的验证清单，再向用户报告路径、manifest 和核心 assumptions。

> **中文说明：** 本节是 spec 编写约定的集中入口；上方的稳定字段、路径和 ID 是 workflow contract，不得为了措辞优化而改名。

## 工作流程

### 1. 收集上下文

从 conversation context 开始。如果用户给出本地文件路径，读取该文件作为主要来源。

如果输入来自 `brainstorming` handoff，先读取 handoff 中的 `Confirmed problem / goal`、`Scope / Non-goals`、`Chosen approach`、`Key decisions`、`Constraints`、`Risks and open questions` 和 `Recommended spec focus`，再补充必要的项目事实。

轻量探索项目事实：

- 读取用户指定或与当前需求直接相关的项目文档。
- 查看明显相关的 ADRs 或 domain docs。
- 使用项目已有 domain vocabulary；没有 glossary 时不要编造术语。

不要因为缺少 domain docs 或 ADRs 而停止；缺失只写入 assumptions 或 risks。

### 2. 写清叙事主线

spec 的前半部分是叙事：问题是什么、选了什么方案、为什么不选别的。这部分承接 brainstorming 或 grill-me 已达成的共识，把讨论中的关键决策和被排除的 alternatives 连同理由固化下来，避免后续实现时重新争论。

### 3. 明确需求契约

功能需求使用稳定 ID，并描述外部可观察行为：

- `FR-001`, `FR-002`, ...
- 每条 requirement 描述外部可观察行为，应能被 plan task、test 或手动 verification seam 覆盖。

成功标准使用 `SC-001`, `SC-002`, ...。只有可由实现或验证工作直接影响的 success criteria 才进入后续 plan coverage；纯业务结果可以保留但标记为 post-launch metric。

### 4. 明确测试切入点

草拟 feature 应通过哪些 seam 验证。优先使用最高层、最接近 external behavior 的 seam，例如 public API、CLI、UI workflow、integration test、repro command。

如果 seam 选择会影响架构或测试策略，先向用户简短确认。若用户要求直接产出文档，将 seam 假设写进 `测试决策` 和 `风险与开放问题`，不要阻塞输出。

### 5. 写入 spec

使用下面模板：

```markdown
# <Feature Name> Spec

## 元数据

- **Status**: Draft
- **Source**: conversation context / local file / codebase notes
- **Generated at**: <YYYY-MM-DD>
- **Feature Slug**: <feature-slug>

## 问题陈述

从用户视角描述正在面对的问题和现状的痛点。

## 方案与架构

用叙事描述选定的方案：整体思路、涉及的 module/contract/schema/API、与现有架构的关系。

## 关键决策与取舍

- **决策**: <选了什么>。**理由**: <为什么>。**被排除的方案**: <alternative 及排除原因>。

## 非目标

- ...

## 功能需求

- **FR-001**: 描述一个外部可观察行为。
- **FR-002**: 描述另一个可验证需求。

## 成功标准

- **SC-001**: 描述可验证成功标准。

## 测试决策

- Verification seam（验证切入点）:
- Prior art（现有依据）:
- Manual fallback（手动兜底）:

## 风险与开放问题

- **Risk**: 描述风险。
- **Open Question**: 描述开放问题。

## 计划交接说明

- 建议的 task 切分维度和顺序约束。
- 高风险改动点或必须原子完成的部分。
- 需要 human-gate 的决策。
```

### 6. 更新 manifest

创建或更新 `docs/features/<feature-slug>/manifest.md`：

```markdown
# <Feature Name> Manifest

## 产物

- Spec: `spec.md`
- Plan: `plan.md` (pending)

## 状态

- Spec: Draft
- Plan: Not started
- Implementation: Not started
```

### 7. 验证输出

写入后检查：

- spec 是本地 Markdown 文件，叙事章节（问题陈述、方案与架构、关键决策与取舍）不是空壳。
- Functional requirements 使用稳定 `FR-###`，success criteria 使用 `SC-###`。
- 测试决策至少有 seam 假设或 open question。
- 各章节描述正文已完整填写，没有残留未替换模板句。
- 没有逐文件实施计划；实现细节只到稳定 contract/schema/API/architecture decision 层。
- 没有要求运行外部 setup skill 或创建远端 issue。

完成以上检查后，spec-only 结果才算完成；报告中应明确哪些内容来自已确认 handoff，哪些仍是 assumptions 或 open questions。

最后向用户报告 spec 路径、manifest 路径和核心 assumptions。

## 后续处理

- spec-only 完成后报告路径并结束，不自动进入其他 skill。
- 用户随后明确需要 implementation plan 时，由用户显式调用 `$to-plan`。
- 不在本 skill 内自动生成 plan 或进入实现。
