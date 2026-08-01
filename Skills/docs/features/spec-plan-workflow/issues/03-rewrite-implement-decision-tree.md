# ISSUE-003: 重写 `implement` 决策树（去 issue/wave 语义）

## 元数据 (Metadata)

- **Type**: `HITL`
- **Covers**: `FR-011`
- **Parallelization**: `parallel-safe`
- **Wave**: 2
- **Depends on**: `ISSUE-002 (hard: 依赖 plan 模板定稿的 task 字段名)`
- **Unblocks**: `ISSUE-005`

## 构建内容 (What to build)

重写 `implement/SKILL.md`：输入从 issues 目录改为 plan 文件（或 spec、conversation scope），读取 plan task 的文件路径、`Consumes/Produces` 接口契约、验收标准和验证命令，按 task 顺序串行执行；删除以 issue wave/`parallel-safe` 字段为前提的 `Multi-Agent Waves` 执行分支及配套确认节点；保留 subagent 只读探索/spike 能力。

## 验收标准 (Acceptance Criteria)

- [ ] description 与进入边界不再提 issues；输入优先级为 plan > spec > conversation scope。
- [ ] 上下文收集步骤改为：读取 `docs/features/<slug>/plan.md`，提取 task 的 Files/Consumes/Produces/Covers/验收标准/验证命令；scope 超过 plan 范围时推荐 `$to-plan`。
- [ ] 决策树中 `Multi-Agent Waves` 节点（原 N5）及 `Explicit Mode Confirmation`（原 C1）中依赖 wave/parallel-safe 字段的分支被移除；流程图节点编号、Next/Stop 指向全部自洽，无悬空引用。
- [ ] 保留"subagent 只读探索/spike，实现由当前 agent 串行合并"的能力，且不再作为需要模式确认的分支。
- [ ] 完成条件章节的 coverage 表述从 "PRD requirements 或选定 issues" 改为 "spec `FR-###` 或 plan task 验收标准"。
- [ ] 全文 grep 无 `issue`、`wave`、`parallel-safe`、`coordination-needed` 残留（引用历史文档路径除外）。
- [ ] 重写后的决策树经用户人工 review（human-gate，对应 PRD Risk）。

## 测试说明 (Testing Notes)

- Verification seam: `python scripts/validate-skills.py`（stale-text 与语言契约）；人工按流程图走一遍 plan 输入、spec 输入、conversation scope 三条路径确认无死节点。
- Prior art: 现行 `implement/SKILL.md` 的 N6 Inline Serial Slices 节点——串行路径本来就是默认，重写以它为主干收缩。
- Manual fallback: 用 ISSUE-005 的实施本身作为 implement 新流程的首次真实演练。

## 并行执行说明 (Parallel Execution Notes)

- 与 ISSUE-004 文件不相交，理论可并行；建议 inline 串行。

## 实现说明 (Implementation Notes)

- 这是系统性重写而不是字符串替换：C1/N4/N5/N6 等节点的 Trigger/Next/Stop 是一张互指的图，删节点必须同步收拢所有指向它的边（PRD Risk 第二条）。
- 多 slice 场景的表述改为：plan 有多个 task 时按编号串行执行，每个 task 结束跑其验证命令；不再有"领取"概念。
