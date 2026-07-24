# Session Curator Wiki Profile Manifest

## 产物 (Artifacts)

- Spec: `spec.md`
- Plan: `plan.md`
- Analysis: not requested（独立 `$analyze` 按需执行）

## 状态 (Status)

- Spec: Approved
- Plan: Ready (`Planning Quality Status: Pass`)
- Analysis: Not requested
- Contract Effect: Effective（2026-07-24；17 个 current-candidate fresh-session cases）
- Implementation: Complete

## 关系 (Relationships)

- Extends: `session-curator` 的 `CuratedDurable` curation workflow
- Checked plan: `plan.md` 使用 `Full` planning，并复用 `FR-001..024`
- Preserves: 现有 `session-curator` 的 scope、confirmation、authoritative target、owner、identity、dirty-file 和 Git delivery safety gates
- Excludes: 独立顶层 `wiki` skill、自动 source ingestion、`source-manifest.json`、watcher、全仓库默认扫描、历史 wiki 批量迁移和所有 Git delivery
- Compatibility note: 当前 `docs/features/artifact-placement/` 为未跟踪 planning artifact，不因本 manifest 变为 active implementation
