---
name: to-prd
description: Use when creating a local PRD, feature spec, product requirements, engineering requirements, or implementation-ready requirements document from conversation context, local plans/specs, codebase context, or design notes, especially before issue breakdown or implementation.
---

# To PRD

将当前上下文和必要的 codebase 理解综合成本地 PRD。PRD 是后续 `to-issues`、`analyze` 和 `implement` 的需求来源，不是逐文件实施计划。

## 输出约定

- 只生成本地 Markdown 文档，不创建远端 issue。
- 如果用户指定输出路径，写入该路径。
- 如果项目已有 `docs/features/`，或这是新的 feature，默认使用 `docs/features/<feature-slug>/prd.md`。
- 如果项目明显沿用旧结构 `docs/prd/`，可以使用 `docs/prd/<feature-slug>.md`，但完成报告要说明未使用 feature workspace。
- 如果使用 feature workspace，同时创建或更新 `docs/features/<feature-slug>/manifest.md`。
- 文件名使用简短、可读、lowercase kebab-case slug。

## Process

### 1. 收集上下文

从 conversation context 开始。如果用户给出本地文件路径，读取该文件作为主要来源。

轻量探索项目事实：

- 读取存在的 `README.md`、`AGENTS.md`、`CLAUDE.md`、`CONTEXT.md`、`CONTEXT-MAP.md`。
- 读取存在的 `docs/constitution.md` 或 `.specify/memory/constitution.md`。
- 查看 `docs/adr/` 或相关 ADRs 中明显相关的决策。
- 使用项目已有 domain vocabulary；没有 glossary 时不要编造术语。

不要因为缺少 domain docs、ADRs 或 constitution 而停止；缺失只写入 assumptions 或 risks。

### 2. 明确需求 contract

PRD 中的 functional requirements 必须使用稳定 ID：

- `FR-001`, `FR-002`, ...
- 每条 requirement 描述外部可观察行为。
- 每条 requirement 应能被 issue、test 或手动 verification seam 覆盖。

Success criteria 使用 `SC-001`, `SC-002`, ...。只有可由实现或验证工作直接影响的 success criteria 才进入后续 issue coverage；纯业务结果可以保留但标记为 post-launch metric。

### 3. 明确测试 seam

草拟 feature 应通过哪些 seam 验证。优先使用最高层、最接近 external behavior 的 seam，例如 public API、CLI、UI workflow、integration test、repro command。

如果 seam 选择会影响架构或测试策略，先向用户简短确认。若用户要求直接产出文档，将 seam 假设写进 `Testing Decisions` 和 `Open Questions`，不要阻塞输出。

### 4. 写入 PRD

使用下面模板。避免不必要的具体 file paths；只有稳定 contract、schema、API 或 workflow 决策需要写入。

```markdown
# <Feature Name> PRD

## Metadata

- **Status**: Draft
- **Source**: conversation context / local file / codebase notes
- **Generated at**: <YYYY-MM-DD>
- **Feature Slug**: <feature-slug>

## Problem Statement

从用户视角描述正在面对的问题。

## Goals

- ...

## Non-Goals

- ...

## User Stories

1. As an <actor>, I want <capability>, so that <benefit>.

## Functional Requirements

- **FR-001**: ...
- **FR-002**: ...

## Success Criteria

- **SC-001**: ...

## Implementation Decisions

- 已确定的 module、contract、schema、API、interaction 或 architecture decisions。

## Testing Decisions

- Verification seam:
- Prior art:
- Manual fallback:

## Risks and Open Questions

- ...

## Handoff Notes for Issue Breakdown

- 推荐 vertical slice 维度。
- 高风险 dependencies。
- 需要 human-gate 的决策。
```

### 5. 更新 manifest

如果使用 `docs/features/<feature-slug>/`，创建或更新：

```markdown
# <Feature Name> Manifest

## Artifacts

- PRD: `prd.md`
- Issues: `issues/00-index.md` (pending)
- Analysis: `analysis.md` (pending)

## Status

- PRD: Draft
- Issues: Not started
- Analysis: Not started
- Implementation: Not started
```

### 6. 验证输出

写入后检查：

- PRD 是本地 Markdown 文件。
- Functional requirements 使用稳定 `FR-###`。
- Testing Decisions 至少有 seam 假设或 open question。
- 没有要求运行外部 setup skill 或创建远端 issue。
- `Implementation Decisions` 没有不必要的易过期 file paths。

最后向用户报告 PRD 路径、manifest 路径、核心 assumptions 和建议的下一步 `to-issues`。
