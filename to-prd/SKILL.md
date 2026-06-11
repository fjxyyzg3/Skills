---
name: to-prd
description: Use only when the user explicitly invokes To PRD, to-prd, or $to-prd to create a local PRD, feature spec, product requirements, engineering requirements, or implementation-ready requirements document; do not infer this skill from ordinary planning, feature, spec, issue breakdown, or implementation requests.
---

# To PRD

将当前上下文和必要的 codebase 理解综合成本地 PRD。PRD 是后续 issue breakdown、analysis 和 implementation 的需求来源，不是逐文件实施计划。

## 手动触发边界

- 只在用户明确写出 `to-prd`、`To PRD`、`$to-prd` 或“使用 PRD skill”时加载本 skill。
- 不要因为用户在做 feature planning、spec、需求整理、issue breakdown 或实现前准备就自动触发。
- 如果当前任务适合本流程但用户没有手动调用，只能简短建议“可以使用 `$to-prd`”，不要自行切换到本 skill。

## Language Contract

Language Contract: generated documents and chat outputs default to Chinese-first; preserve English for code, commands, API names, contract fields, IDs, proper nouns, and necessary technical terms. 用户或目标项目明确要求英文时可以例外，但必须记录原因。

## 输出约定

- 只生成本地 Markdown 文档，不创建远端 issue。
- 文档正文默认中文为主；核心 section heading 使用中文优先、English 括注，例如 `## 功能需求 (Functional Requirements)`。
- 保留 `FR-001`、`SC-001`、`Metadata`、`Status`、`Source` 等 workflow contract fields 和稳定 ID。
- 如果用户指定输出路径，写入该路径。
- 如果项目已有 `docs/features/`，或这是新的 feature，默认使用 `docs/features/<feature-slug>/prd.md`。
- 如果项目明显沿用旧结构 `docs/prd/`，可以使用 `docs/prd/<feature-slug>.md`，但完成报告要说明未使用 feature workspace。
- 如果使用 feature workspace，同时创建或更新 `docs/features/<feature-slug>/manifest.md`。
- 文件名使用简短、可读、lowercase kebab-case slug。

## Process

### 1. 收集上下文

从 conversation context 开始。如果用户给出本地文件路径，读取该文件作为主要来源。

轻量探索项目事实：

- 读取用户指定或与当前需求直接相关的项目文档。
- 查看明显相关的 ADRs 或 domain docs。
- 使用项目已有 domain vocabulary；没有 glossary 时不要编造术语。

不要因为缺少 domain docs 或 ADRs 而停止；缺失只写入 assumptions 或 risks。

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

## 元数据 (Metadata)

- **Status**: Draft
- **Source**: conversation context / local file / codebase notes
- **Generated at**: <YYYY-MM-DD>
- **Feature Slug**: <feature-slug>

## 问题陈述 (Problem Statement)

从用户视角描述正在面对的问题。

## 目标 (Goals)

- ...

## 非目标 (Non-Goals)

- ...

## 用户故事 (User Stories)

1. As an <actor>, I want <capability>, so that <benefit>.

## 功能需求 (Functional Requirements)

- **FR-001**: ...
- **FR-002**: ...

## 成功标准 (Success Criteria)

- **SC-001**: ...

## 实现决策 (Implementation Decisions)

- 已确定的 module、contract、schema、API、interaction 或 architecture decisions。

## 测试决策 (Testing Decisions)

- Verification seam:
- Prior art:
- Manual fallback:

## 风险和开放问题 (Risks and Open Questions)

- ...

## Issue 拆分交接说明 (Handoff Notes for Issue Breakdown)

- 推荐 vertical slice 维度。
- 高风险 dependencies。
- 需要 human-gate 的决策。
```

### 5. 更新 manifest

如果使用 `docs/features/<feature-slug>/`，创建或更新：

```markdown
# <Feature Name> Manifest

## 产物 (Artifacts)

- PRD: `prd.md`
- Issues: `issues/00-index.md` (pending)
- Analysis: `analysis.md` (pending)

## 状态 (Status)

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

最后向用户报告 PRD 路径、manifest 路径、核心 assumptions；如果需要拆 issue，只建议用户显式调用 `$to-issues`。
