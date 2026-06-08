---
name: handoff
description: Use when compacting the current conversation into a handoff document for another agent or session to continue, especially before context reset, session transfer, or pausing work with important unresolved context.
argument-hint: "下一位 agent 要接着做什么？"
---

# Handoff

把当前会话整理成可继续执行的 handoff document，让下一位 agent 不需要重新追溯上下文。

## 核心规则

- 生成 Markdown handoff document，并保存到用户 OS 的临时目录；不要写入当前 workspace，除非用户明确要求。
- 文件名包含 `handoff` 和时间戳，避免覆盖旧文件。
- 只保留继续工作必需的信息：目标、当前状态、关键决策、已改文件、未完成事项、验证证据和残留风险。
- 已经存在于 PRD、issues、ADR、plans、commits、diffs 或报告中的内容不要重复粘贴；用 path 或 URL 引用。
- 必须包含 `Suggested Skills` section，列出下一位 agent 应优先加载的 skills 及原因。
- 不要逐字转录完整对话；只写可执行摘要。
- Redact secrets、API keys、tokens、passwords 和 personally identifiable information；不确定是否敏感时，只描述类型，不写具体值。
- 如果用户传入参数，把参数视为下一次会话的重点，并据此裁剪 handoff。

## 工作流程

1. 明确 handoff 目的：下一位 agent 要继续实现、诊断、review、写文档，还是只需要背景。
2. 盘点当前状态：workspace、branch、git status、关键文件、已执行命令、验证结果、阻塞点和用户最近指令。
3. 找到可引用 artifacts：PRD、issues、分析报告、ADR、commit、diff、测试输出或本地文件路径。
4. 写入系统临时目录：
   - Windows: 使用 `[System.IO.Path]::GetTempPath()`。
   - macOS/Linux: 优先使用 `$TMPDIR`，没有时使用 `/tmp`。
5. 输出最终文件路径，并用一句话说明 handoff 面向的下一步；不要在聊天里贴完整文档，除非用户要求。

## Document Contract

handoff document 至少包含：

- `Purpose`: 下一次会话要完成什么。
- `Current State`: 当前进展、分支、工作区和最重要上下文。
- `Artifact References`: 已存在文档、issues、commits、diffs 或文件路径。
- `Decisions`: 已确认的技术或产品决策。
- `Verification`: 已运行的命令、结果和未验证项。
- `Open Work`: 下一步清单、阻塞点和需要用户确认的问题。
- `Suggested Skills`: 推荐加载的 skills 和原因。
- `Risks`: 残留风险、敏感信息处理和不要误做的事项。

## 完成标准

- handoff 文件已保存到系统临时目录，并把路径告知用户。
- 文档能让下一位 agent 继续工作，不依赖原始聊天全文。
- 没有泄露 secrets、tokens、passwords 或不必要的个人信息。
- 已引用现有 artifacts，避免重复长文档内容。
- 已包含 `Suggested Skills` 和未完成事项。
