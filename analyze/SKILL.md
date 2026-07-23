---
name: analyze
description: "当用户要求对既有或外部 spec/plan 产物执行只读审计，或 implementation intake 发现产物未检查或已失效时使用；识别歧义、覆盖缺口、contract mismatch、缺失验证和质量门违规；保留英文触发短语 read-only audit of existing or external spec/plan artifacts。"
---

# Analyze

对本地 artifacts 做只读一致性分析。目标是在实现前发现需求、任务拆分、接口契约和质量门之间的断裂。

## 进入边界

- 这是已有或外部 artifacts 的独立只读审计入口；用户显式要求 analysis、audit、coverage 或 contract review 时使用。
- implementation intake 发现 artifacts 缺少可信 quality status、已经失效或来自外部时，也可把本 skill 作为条件式质量门。
- checked plan 已包含 `Planning Quality Status: Pass` 时，不把本 skill 作为默认 planning chain 的重复阶段；只有用户要求复审或实现入口发现 artifact 未检查/已失效时再运行。
- 本 skill 报告 findings，不自动修复输入 artifacts、不生成 plan，也不进入实现。

## 触发说明（Trigger Description）

`analyze` 的 trigger 是对已有、外部、失效或未检查 spec/plan artifacts 做独立只读审计。它输出带 location 与 severity 的 findings；有效 checked plan 不因默认链路重复触发本 skill。

## 压力场景（Pressure Scenarios）

1. 外部 plan 声称已经就绪，但没有可信质量证据。
   - 预期触发：只读检查 coverage、contracts、paths 和 verification commands。
   - 未使用本 skill 时的常见失败：仅相信 `Pass` 字样，或直接进入实现。
   - 本 skill 必须强制的行为：用 artifact 与仓库事实建立可追溯 findings。
2. 本地 checked plan 已有 `Planning Quality Status: Pass` 且未发生变化。
   - 预期触发：除非用户要求复审，否则不作为默认 planning 阶段重复运行。
   - 未使用本 skill 时的常见失败：重做 producer 已完成的机械检查并增加一次 handoff。
   - 本 skill 必须强制的行为：保持条件式 audit 边界。
3. 审计发现输入 artifact 中有可由源码核实的拼写错误。
   - 预期触发：报告 finding 与修复建议，保持输入文件不变。
   - 未使用本 skill 时的常见失败：把 `$to-plan` 的 Artifact-fixable 权限带入独立 audit。
   - 本 skill 必须强制的行为：read-only contract 优先。

## 核心规则

- 默认只读，不修改文件。
- 先检查用户指定的文件；没有指定时，按当前 feature 目录和 `docs/features/` 的线索查找。
- 只把用户指定文件、输入 artifacts 和它们明确引用的文档作为分析来源。
- 报告具体位置，避免只给泛泛建议。
- 不要因为 artifacts 不完整而编造缺失内容；缺失本身就是 finding。

## 输入识别

优先级：

1. 用户指定的 spec/plan 文件。
2. 用户提供的外部 artifact 路径或明确 artifact 集合。
3. 当前 feature manifest：`docs/features/<feature-slug>/manifest.md`。
4. `docs/features/<feature-slug>/spec.md` 和同目录 `plan.md`。

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
## 产物分析报告

| ID | Severity | Category | Location | Finding | Recommendation |
| --- | --- | --- | --- | --- | --- |
| A1 | HIGH | Coverage | docs/... | ... | ... |

## 覆盖摘要

| Requirement | Covered by | Verification seam | Notes |
| --- | --- | --- | --- |

## 接口契约核对

- Consumes/Produces mismatches: None / ...
- 引用不存在接口的 task: None / ...

## 约束对齐

- Pass / Findings...

## 下一步

1. ...
```

## 完成标准

- 报告列出已检查的 artifact 路径。
- 所有阻塞实现的问题都按严重度排序。
- 给出是否可以进入 `implement` 的明确建议。
- 没有写入或修改 artifacts，除非用户后续明确要求修复。
- 没有把本次独立 audit 宣称为 adaptive planning 的默认必经阶段。

## 自然交接（Natural Handoff）

- audit 通过且用户明确要实现时，最多推荐 `$implement`；其 branch、scope、review 和 verification gate 保持有效。
- artifacts 需要重新生成 checked plan 时，最多推荐 `$to-plan`。
- 用户只要求审计结果时推荐 `none`。
- 本 skill 不在 handoff 前修改输入 artifacts 或进入实现。
