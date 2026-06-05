---
name: to-prd
description: 将当前 conversation context、local plan/spec 或 codebase context 转成一份本地 PRD Markdown 文档。Use when user wants to create a PRD, 生成产品需求文档, 把讨论整理成 PRD, or prepare a spec for local issue breakdown. This skill writes local files only and does not use remote trackers or external skills.
---

# To PRD

将当前上下文和必要的 codebase 理解综合成一份本地 PRD。不要默认访谈用户；优先综合已经知道的信息。只有当关键产品边界缺失且会导致 PRD 明显误导时，最多问 1-3 个具体问题。

## 输出约定

- 只生成本地 Markdown 文档，不创建任何远端 issue。
- 不依赖任何外部 setup、远端标签配置、远端 tracker 配置或其他 skill。
- 如果用户指定输出路径，写入该路径。
- 如果用户没有指定路径，使用 `docs/prd/<feature-slug>.md`。
- 如果目标目录不存在，创建目录。
- 文件名使用简短、可读、lowercase kebab-case slug。

## Process

### 1. 收集上下文

从 conversation context 开始。如果用户给出本地文件路径，读取该文件作为主要来源。

如果还不了解 repo，做一次轻量探索：

- 读取 `README.md`、`AGENTS.md`、`CLAUDE.md`、`CONTEXT.md`、`CONTEXT-MAP.md` 中存在的文件。
- 查看 `docs/adr/` 或相关 ADRs 中存在且明显相关的决策。
- 使用项目已有的 domain vocabulary；如果没有 glossary，不要编造术语。

不要因为缺少 domain docs、ADRs 或配置文件而停止；这些文件只是可选输入。

### 2. 明确测试 seam

草拟 feature 应该通过哪些 seam 验证。优先使用已有 seam，尽量选择最高层、最接近 external behavior 的 seam。

如果 seam 选择会影响架构或测试策略，先向用户简短确认。若用户要求直接产出文档，将 seam 假设写进 `Testing Decisions` 和 `Open Questions`，不要阻塞输出。

### 3. 写入本地 PRD

使用下面模板。保持面向产品和工程交接，避免把 PRD 写成逐文件实施计划。

<prd-template>

# <Feature Name> PRD

## Metadata

- **Status**: Draft
- **Source**: conversation context / local file / codebase notes
- **Generated at**: <YYYY-MM-DD>

## Problem Statement

从用户视角描述用户正在面对的问题。

## Goals

列出本 PRD 要达成的结果。每个 goal 应该能被用户行为或系统行为验证。

## Solution

从用户视角描述解决方案。说明用户会获得什么能力，以及成功体验是什么。

## User Stories

列出覆盖完整 feature 的 user stories。格式：

1. As an <actor>, I want a <feature>, so that <benefit>.

## Functional Requirements

列出必须支持的行为。每条 requirement 应该具体、可验证。

## Implementation Decisions

列出已经确定的 implementation decisions。可以包括：

- 将要新增或修改的 modules
- 将要修改的 module interfaces
- 来自 developer 的技术澄清
- Architectural decisions
- Schema changes
- API contracts
- 具体 interactions

不要包含容易过期的具体 file paths 或完整 code snippets。

例外：如果 prototype 产出的 snippet 比文字更精确地表达了某个决策，例如 state machine、reducer、schema、type shape，可以把它内联到相关 decision 中，并简要说明它来自 prototype。只保留承载决策的信息，不要放完整 demo。

## Testing Decisions

列出已经确定的 testing decisions。包括：

- 什么是好的测试：只测试 external behavior，不测试 implementation details
- 将通过哪些 seam 验证行为
- 可参考的 test prior art，例如 codebase 中相似类型的 tests

## Out of Scope

说明本 PRD 明确不覆盖的事项。

## Risks and Open Questions

列出风险、未知项、需要用户或后续实现者确认的问题。

## Handoff Notes for Issue Breakdown

给后续 issue breakdown 使用的拆分提示。指出适合做 tracer-bullet vertical slice 的维度，例如用户流程、状态转换、API contract、数据生命周期或 UI workflow。

</prd-template>

### 4. 验证输出

写入文件后检查：

- PRD 是本地 Markdown 文件。
- 文档没有要求运行外部 setup skill。
- 文档没有要求创建或修改远端 issue。
- `Implementation Decisions` 没有不必要的易过期 file paths。

最后向用户报告写入路径和核心假设。
