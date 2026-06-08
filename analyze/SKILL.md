---
name: analyze
description: Use when checking local PRD, spec, plan, issue files, task lists, dependency graphs, execution waves, implementation notes, or constitution alignment before implementation, especially to find ambiguity, inconsistency, missing coverage, dependency cycles, parallelization risk, or quality-gate violations.
---

# Analyze

对本地 artifacts 做只读一致性分析。目标是在实现前发现需求、拆分、依赖、并行建议和质量门之间的断裂。

## Language Contract

Language Contract: generated documents and chat outputs default to Chinese-first; preserve English for code, commands, API names, contract fields, IDs, proper nouns, and necessary technical terms. 用户或目标项目明确要求英文时可以例外，但必须记录原因。

## 核心规则

- 默认只读，不修改文件。
- 先检查用户指定的文件；没有指定时，按当前 feature 目录、`docs/features/`、`docs/prd/`、`docs/issues/` 的线索查找。
- 如果存在 `docs/constitution.md` 或 `.specify/memory/constitution.md`，把 constitution 作为最高优先级约束。
- 报告具体位置，避免只给泛泛建议。
- 不要因为 artifacts 不完整而编造缺失内容；缺失本身就是 finding。

## 输入识别

优先级：

1. 用户指定的 PRD/spec/plan/issues 目录或文件。
2. 当前 feature manifest：`docs/features/<feature-slug>/manifest.md` 或 `manifest.json`。
3. `docs/issues/<feature-slug>/00-index.md` 和相邻 issue 文件。
4. 最近或最明显相关的 `docs/prd/<feature-slug>.md`。

## 分析步骤

1. 建立 artifact map。
   - PRD/spec: goals、requirements、user stories、success criteria、open questions。
   - Issues/tasks: issue ID、acceptance criteria、testing notes、dependencies、wave、parallelization。
   - Implementation notes: contracts、schemas、module decisions、verification commands。
   - Constitution: MUST/SHOULD 规则。

2. 建立 traceability map。
   - 每个 requirement 是否至少被一个 issue/task 覆盖。
   - 每个 issue 是否指向 requirement、story、bug 或明确 conversation requirement。
   - 每个 acceptance criterion 是否有 testing notes 或 verification seam。

3. 运行 finding passes。
   - Ambiguity: 模糊形容词、缺少 actor/object/outcome、不可测试验收。
   - Inconsistency: 术语漂移、相互冲突的 scope、不同文件对同一 contract 描述不一致。
   - Coverage gap: requirement 没有 issue、issue 没有验收、测试 seam 缺失。
   - Dependency issue: cycle、hard dependency 漏写、wave 顺序错误。
   - Parallelization risk: 标记 `parallel-safe` 但共享 contract/schema/core module。
   - Constitution violation: 违反 MUST 或缺少强制质量门。

4. 分配严重度。
   - `CRITICAL`: constitution MUST 冲突、核心 requirement 无覆盖、dependency cycle 阻塞执行。
   - `HIGH`: 不可测试验收、冲突需求、错误并行建议、高风险质量门缺失。
   - `MEDIUM`: 术语漂移、非核心 requirement 漏测、依赖理由不足。
   - `LOW`: 可读性、格式、轻微重复。

## 输出格式

```markdown
## 产物分析报告 (Artifact Analysis Report)

| ID | Severity | Category | Location | Finding | Recommendation |
| --- | --- | --- | --- | --- | --- |
| A1 | HIGH | Coverage | docs/... | ... | ... |

## 覆盖摘要 (Coverage Summary)

| Requirement | Covered by | Verification seam | Notes |
| --- | --- | --- | --- |

## 依赖和并行 (Dependency And Parallelization)

- Cycles: None / ...
- Unsafe parallel claims: ...

## 治理原则对齐 (Constitution Alignment)

- Pass / Findings...

## 下一步 (Next Actions)

1. ...
```

## 完成标准

- 报告列出已检查的 artifact 路径。
- 所有阻塞实现的问题都按严重度排序。
- 给出是否可以进入 `implement` 的明确建议。
- 没有写入或修改 artifacts，除非用户后续明确要求修复。
