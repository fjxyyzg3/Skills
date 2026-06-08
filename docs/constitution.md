<!--
Sync Impact Report
Version: 0.3.0 -> 0.4.0
Changed Principles:
- Replaced: Branch Prepared By User -> Branch Decision Gate
Templates/Skills:
- Updated: checking-branch, implement, using-skills
- Updated: README, AGENTS
Follow-up TODOs:
- None
-->

# Project Constitution

## Metadata

- **Version**: 0.4.0
- **Ratified**: 2026-06-07
- **Last Amended**: 2026-06-08

## Principles

### 1. Skill Routing First

Tasks that match a local workflow skill MUST load the relevant skill before acting. When multiple skills apply, process skills such as `using-skills`, `diagnose`, `to-prd`, `to-issues`, and `analyze` determine the workflow before implementation skills write files or code.

### 2. Artifact Traceability

Non-trivial implementation work MUST trace back to a local artifact or explicit conversation requirement. PRDs SHOULD use stable requirement IDs such as `FR-001`; issues MUST declare `Covers`; implementation reports MUST state which requirements or issues were completed.

### 3. Observable Verification

Every behavior change MUST define an observable verification seam before completion. Automated tests are preferred. If automation is impractical, the closest manual, static, or artifact-level verification MUST be recorded with the reason automation was skipped.

### 4. Skill Changes Are Tested Workflows

新增或修改 skill MUST include pressure scenarios or an explicit note explaining why forward-testing was not performed. Skill edits MUST be validated for frontmatter, folder/name consistency, metadata, TODO residue, and encoding issues before completion.

### 5. Local-First Outputs

Workflow artifacts MUST be written locally by default. Skills in this repository MUST NOT create remote issues, push branches, open PRs, or mutate external trackers unless the user explicitly requests that action.

### 6. Chinese-First, English-Preserved Writing

`SKILL.md` 正文 MUST 优先使用中文。文件名、目录名、YAML frontmatter key、配置字段、命令、代码、API 名称、英文专业术语和英文专有名词 MUST 保留 English。

### 7. Progressive Disclosure

Skill bodies SHOULD stay concise and action-oriented. Large references, reusable scripts, and output assets SHOULD live in `references/`, `scripts/`, or `assets/` and be loaded only when needed.

### 8. Branch Decision Gate

Before implementation, the agent MUST display the current branch name and Git status, then ask whether to modify the current branch directly. If the user does not approve direct modification and provides a new branch name, the agent MUST create that branch from the repository default branch when one is defined. If the repository default branch cannot be confirmed, the agent MUST ask whether to create the branch from the current branch and MUST wait for approval before doing so. The agent MUST NOT overwrite an existing branch or discard user changes without explicit approval.

### 9. Fast Path With Guardrails

Small bug fixes and small feature requests MAY use `quick-change` instead of PRD, issue breakdown, and artifact analysis. The fast path MUST still define scope, acceptance, and verification before implementation. If scope, risk, or uncertainty expands, the agent MUST stop the fast path and upgrade to the appropriate full workflow.

## Governance

This constitution constrains PRD generation, issue breakdown, analysis, implementation, review, verification, and skill maintenance workflows.

Amendments require:

1. Updating this document.
2. Incrementing `Version` using SemVer.
3. Updating the Sync Impact Report.
4. Checking affected skills and templates.
5. Running `python scripts/validate-skills.py`.
