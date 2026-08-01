# Adaptive Planning Workflow Manifest

## 产物 (Artifacts)

- Spec: `spec.md`
- Plan: `plan.md`
- Analysis: not planned（planning quality gate 按本 spec 内建到 `$to-plan`）

## 状态 (Status)

- Spec: Approved
- Plan: Complete
- Analysis: Embedded by design
- Implementation: Complete

## 关系 (Relationships)

- Supersedes: `../spec-plan-workflow/prd.md` 中固定 `$to-spec -> $to-plan -> $analyze` 默认链路的相关决策
- Preserves: 独立 `$to-spec`、独立只读 `$analyze`、`Natural Handoff` 唯一推荐规则和 implementation safety gates
