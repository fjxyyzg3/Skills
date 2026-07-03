---
name: analyze
description: Use when checking a local spec and plan for ambiguity, inconsistency, requirement coverage gaps, interface contract mismatches between tasks, missing verification commands, or quality-gate violations before implementation.
---

# Analyze

对本地 artifacts 做只读一致性分析。目标是在实现前发现需求、任务拆分、接口契约和质量门之间的断裂。

## Language Contract

语言契约：生成的文档和聊天输出默认以中文优先；代码、命令、API 名称、契约字段、ID、专有名词以及必要的技术术语保留英文。用户或目标项目明确要求英文时可以例外，但必须记录原因。

## 核心规则

- 默认只读，不修改文件。
- 先检查用户指定的文件；没有指定时，按当前 feature 目录和 `docs/features/` 的线索查找。
- 只把用户指定文件、输入 artifacts 和它们明确引用的文档作为分析来源。
- 报告具体位置，避免只给泛泛建议。
- 不要因为 artifacts 不完整而编造缺失内容；缺失本身就是 finding。

## 输入识别

优先级：

1. 用户指定的 spec/plan 文件。
2. 当前 feature manifest：`docs/features/<feature-slug>/manifest.md`。
3. `docs/features/<feature-slug>/spec.md` 和同目录 `plan.md`。

## 分析步骤

1. 建立 artifact map。
   - Spec: 问题陈述、方案与架构、关键决策、`FR-###` requirements、`SC-###` success criteria、测试决策、open questions。
   - Plan: task 编号与顺序、`Files`、`Consumes/Produces`、`Covers`、acceptance criteria、验证命令。
   - Constraints: 输入 artifacts 中明确写出的 MUST/SHOULD 规则和全局约束。

2. 建立 traceability map。
   - 每条 `FR-###` 是否至少被一个 plan task 的 `Covers` 覆盖。
   - 每个 task 是否指向 `FR-###` 或明确 conversation requirement。
   - 每个 acceptance criterion 是否有对应验证命令或 verification seam。

3. 运行 finding passes。
   - Ambiguity: 模糊形容词、缺少 actor/object/outcome、不可测试验收。
   - Inconsistency: 术语漂移、相互冲突的 scope、spec 与 plan 对同一 contract 描述不一致。
   - Coverage gap: requirement 没有 task 覆盖、task 没有验收标准、验证命令缺失。
   - Contract mismatch: 后置 task 的 `Consumes` 与前置 task 的 `Produces` 名称、签名或类型对不上；task 引用了任何 task 都不产出的接口。
   - Feasibility: `Files` 路径与仓库事实明显不符、验证命令引用不存在的脚本或目标。
   - Constraint violation: 违反输入 artifacts 中的明确 MUST 约定或缺少强制质量门。

4. 分配严重度。
   - `CRITICAL`: 明确 MUST 约束冲突、核心 requirement 无覆盖、contract mismatch 使后续 task 无法开始。
   - `HIGH`: 不可测试验收、冲突需求、验证命令缺失或不可执行、高风险质量门缺失。
   - `MEDIUM`: 术语漂移、非核心 requirement 漏测、task 切分粒度存疑。
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

## 接口契约核对 (Contract Consistency)

- Consumes/Produces mismatches: None / ...
- 引用不存在接口的 task: None / ...

## 约束对齐 (Constraint Alignment)

- Pass / Findings...

## 下一步 (Next Actions)

1. ...
```

## 完成标准

- 报告列出已检查的 artifact 路径。
- 所有阻塞实现的问题都按严重度排序。
- 给出是否可以进入 `implement` 的明确建议。
- 没有写入或修改 artifacts，除非用户后续明确要求修复。
