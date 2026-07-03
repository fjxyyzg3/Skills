---
name: verification-before-completion
description: Use before claiming a task is done, after implementation, debugging, documentation generation, skill edits, multi-agent work, or review fixes, to verify tests, acceptance criteria, artifact integrity, temporary files, branch status, skipped validation, and unresolved risks.
---

# Verification Before Completion

完成声明之前做最后质量门。核心问题是：用户要求的东西是否真的完成，证据是否足够，工作区是否干净到可以交接。

## Language Contract

语言契约：生成的文档和聊天输出默认以中文优先；代码、命令、API 名称、契约字段、ID、专有名词以及必要的技术术语保留英文。用户或目标项目明确要求英文时可以例外，但必须记录原因。

## 检查项

1. 需求覆盖。
   - 对照用户要求、spec、plan、acceptance criteria。
   - 每项标记 done / skipped / blocked。

2. 验证证据。
   - 运行最接近 external behavior 的测试或命令。
   - 记录命令、结果和失败/跳过原因。
   - 对 bugfix，重新运行原始 repro 或最小化 repro。

3. Artifact integrity。
   - 文档、spec/plan artifacts、Mermaid、HTML、agents metadata、generated assets 没有模板残留。
   - 本地链接、文件路径、编号和 task 顺序一致。

4. 临时内容清理。
   - 搜索并处理 debug 前缀，例如 `[DEBUG-...]`、`[DEBUG-UE-...]`。
   - 删除或标记 throwaway harness、prototype、临时 trace。
   - 不删除用户或工具产生但与任务无关的文件；只报告。

5. Git 状态。
   - 运行 `git status --short`。
   - 区分本次改动、用户已有改动和生成产物。
   - 确认没有遗留正在运行的进程或 dev server，除非用户需要并已说明。

## 输出格式

```markdown
## 验证 (Verification)

- Requirements: pass / partial / blocked
- Commands run:
  - `<command>` -> pass / fail
- Skipped validation:
  - ...
- Cleanup:
  - ...
- Git status:
  - ...
- Residual risk:
  - ...
```

## 完成标准

- 有足够证据支持“完成”。
- 跳过的验证有具体原因。
- 残留风险和用户后续决策已列出。
- 未把未完成或未验证的内容包装成完成。
