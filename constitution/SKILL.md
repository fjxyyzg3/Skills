---
name: constitution
description: Use when creating, updating, or applying project governance principles, quality gates, workflow rules, artifact contracts, testing policy, review policy, branch policy, or skill repository conventions that should constrain PRD, issues, analysis, implementation, and verification.
---

# Constitution

维护项目级原则和质量门。constitution 不是普通说明文档；它是后续 PRD、issues、analysis、implementation 和 verification 的上游约束。

## 输出位置

- 如果项目已有 `.specify/memory/constitution.md`，优先更新它。
- 否则如果项目已有 `docs/constitution.md`，更新该文件。
- 否则默认创建 `docs/constitution.md`。
- 写入前读取 `README.md`、`AGENTS.md`、`CLAUDE.md`、`CONTEXT.md`、`docs/adr/` 中明显相关的内容。

## 工作流程

1. 确定治理范围。
   - 说明本次是首次创建、增补原则、修改质量门，还是同步旧原则。
   - 如果用户只给出局部修改，也要检查它是否影响已有流程和模板。

2. 维护原则。
   - 每条原则必须能被后续流程验证。
   - 使用 `MUST`、`SHOULD`、`MAY` 表达强度。
   - 避免“高质量”“清晰”“合理”这类无法检查的空话；改写成可判断规则。

3. 维护治理信息。
   - 记录 `Version`、`Ratified`、`Last Amended`。
   - 版本号使用 SemVer：
     - `MAJOR`: 删除或重定义不可兼容原则。
     - `MINOR`: 新增原则、质量门或强制流程。
     - `PATCH`: 澄清措辞、修正 typo、不改变语义。
   - 如果版本提升不确定，给出推荐并说明理由。

4. 同步影响面。
   - 检查 `to-prd`、`to-issues`、`analyze`、`implement`、`verification-before-completion` 是否需要引用或遵守新增原则。
   - 如果当前任务不允许修改这些 skill，至少在完成报告中列出 pending sync。

5. 产出 Sync Impact Report。
   - 写在 constitution 文件顶部，使用 HTML comment，避免干扰正文阅读。
   - 内容包括版本变化、修改原则、需要同步的文件、仍未解决的 follow-up items。

## 推荐模板

```markdown
<!--
Sync Impact Report
Version: 0.0.0 -> 0.1.0
Changed Principles:
- Added: Artifact Traceability
Templates/Skills:
- Updated: to-prd, to-issues, analyze, implement
- Pending: None
Follow-up items:
- None
-->

# Project Constitution

## Metadata

- **Version**: 0.1.0
- **Ratified**: YYYY-MM-DD
- **Last Amended**: YYYY-MM-DD

## Principles

### 1. Artifact Traceability

Every non-trivial implementation MUST trace back to a local PRD, issue, plan, bug report, or explicit conversation requirement. Requirements SHOULD have stable IDs when they will be decomposed or implemented over multiple turns.

### 2. Observable Verification

Every behavior change MUST define an observable verification seam before implementation finishes. Automated tests are preferred; when automation is not practical, the closest manual or static verification MUST be recorded.

### 3. Review Before Completion

Implementation work MUST pass spec compliance review and code quality review before completion is claimed.

## Governance

Amendments require updating this document, incrementing the version, and checking affected workflow artifacts.
```

## 完成标准

- Constitution 文件存在且没有未解释的模板 token。
- 每条 MUST/SHOULD 都能被后续流程检查。
- 版本号、日期和 Sync Impact Report 一致。
- 已报告同步过的 skill、未同步的文件和原因。
