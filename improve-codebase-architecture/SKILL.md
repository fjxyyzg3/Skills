---
name: improve-codebase-architecture
description: Use when the user wants to improve codebase architecture, find deepening opportunities, consolidate shallow or tightly-coupled modules, improve testability, or make code easier for agents to navigate.
---

# Improve Codebase Architecture

发现可执行的架构加深机会：把 shallow modules 调整成更 deep 的 modules，让 interface 更小、implementation 承担更多行为，并提升 testability、locality 和 agent navigability。

## Language Contract

语言契约：生成的文档和聊天输出默认以中文优先；代码、命令、API 名称、契约字段、ID、专有名词以及必要的技术术语保留英文。用户或目标项目明确要求英文时可以例外，但必须记录原因。

## Pressure Scenarios

1. User says: "看看这个仓库哪里值得重构。"
   - Expected skill trigger: 做架构扫描和候选报告。
   - Common failure without skill: 泛泛列 best practices，没有源码证据。
   - Behavior this skill must force: 用具体文件、调用关系和 deletion test 支撑每个候选。
2. User says: "这个模块太乱，帮我设计更好的接口。"
   - Expected skill trigger: 先确认 deepening candidate，再进入 interface design。
   - Common failure without skill: 直接给单一接口方案，忽略 seam、adapter 和测试策略。
   - Behavior this skill must force: 至少比较多个不同 interface，并说明 leverage、locality 和 trade-offs。
3. User says: "修完 bug 后顺便看看架构为什么会出这个问题。"
   - Expected skill trigger: 从已验证的 failure mode 反推 architectural friction。
   - Common failure without skill: 在 bug 未收敛前泛泛重构。
   - Behavior this skill must force: 只在 failure mode 已明确后提出 deepening opportunity。

## 核心规则

- 先读取用户指定或与扫描范围直接相关的 domain docs、ADRs 和架构说明；没有就记录缺失，不要编造。
- 使用 `references/language.md` 的架构词汇：`module`、`interface`、`implementation`、`depth`、`seam`、`adapter`、`leverage`、`locality`。
- 每个候选必须有源码证据：文件位置、调用关系、重复知识、测试痛点、依赖泄漏或维护 friction。
- 只提出 deepening opportunities；除非用户明确要求实现，不要直接改业务代码。
- 不要把 pass-through、wrapper、过早抽象包装成架构改进。对可疑模块执行 deletion test。
- 如果候选与 ADR 冲突，只在 friction 足以重开决策时提出，并明确标注冲突。
- 如果没有足够证据，给出已检查范围和下一步探索建议，不要强行产出候选。

## 工作流程

### 1. 定义扫描范围

- 用户指定模块、目录、bug 或计划时，以该范围为主。
- 用户只说"改善架构"时，先根据 docs、近期改动、测试布局和明显核心模块选择 2-4 个高价值区域。
- 记录 scope、source docs、已知 constraints 和显式 non-goals。

### 2. 探索代码

- 使用当前环境可用的 code navigation、`rg`、测试、调用关系、配置和文档。
- 寻找这些信号：
  - 理解一个 domain concept 需要在多个小模块之间来回跳。
  - module 的 interface 几乎和 implementation 一样复杂。
  - 为了测试抽出很多 pure functions，但真实 bug 藏在调用编排里。
  - 调用方需要知道过多 ordering、config、error mode 或依赖细节。
  - tests 绕过 public interface，或需要 mock 很多内部步骤。
- 对每个候选用 deletion test：删除该 module 后，复杂度是消失，还是重新分散到多个 callers？
- 按 `references/deepening.md` 给依赖分类，决定 test seam 和 adapter 策略。

### 3. 产出候选

默认产出一个架构评审摘要。用户要求报告、候选较多或关系复杂时，读取 `references/html-report.md`，写一个 self-contained HTML report 到 OS temp directory：

- Windows: `$env:TEMP`
- macOS/Linux: `$TMPDIR`，缺失时用 `/tmp`
- 文件名：`architecture-review-<timestamp>.html`

每个 candidate 必须包含：

- Files: 涉及的文件或 modules。
- Problem: 当前 architecture friction。
- Solution: deepening 后的形状。
- Benefits: 用 locality、leverage 和 testability 解释收益。
- Dependency strategy: `in-process`、`local-substitutable`、`ports & adapters` 或 `mock`。
- Recommendation strength: `Strong`、`Worth exploring` 或 `Speculative`。
- Evidence: 具体文件和行为证据。

报告最后给出 Top recommendation，并问用户："你想先深入哪一个候选？"

### 4. 候选深入和 grilling loop

用户选择候选后，围绕这些问题推进：

- deepened module 叫什么，是否符合项目 domain language？
- seam 放在哪里，interface 要隐藏哪些 ordering、config、error mode 和依赖？
- implementation 后面保留哪些 internal seams？
- 需要哪些 adapters？是否真的有两个以上 adapter 证明 seam 存在？
- 旧 tests 哪些删除，哪些迁移到新 interface？
- 哪些 ADR 或 `CONTEXT.md` 术语需要更新？

如果用户要比较 interface 方案，读取 `references/interface-design.md`。有 parallel sub-agent 工具时并行设计；没有时由当前 agent 产出至少 3 个明显不同的 interface alternatives。

### 5. 文档同步

- 新 module 名称来自尚未记录的 domain concept 时，建议写入 `CONTEXT.md`；用户同意后再改。
- 用户用 load-bearing reason 否决候选时，询问是否记录 ADR，避免未来重复建议。
- ADR 使用本地 `docs/adr/`；没有固定模板时，至少包含 status、context、decision、consequences。

## 完成标准

- 已报告扫描范围、已读取的 docs 和缺失信息。
- 每个候选都有文件证据和明确 recommendation strength。
- 候选说明使用统一 architecture language，没有漂移到 `component`、`service`、`API`、`boundary` 等替代词。
- 已说明 dependency strategy 和测试 seam。
- 如果生成 HTML report，已报告绝对路径；如果没有生成，已说明原因。
- 没有直接实施重构，除非用户明确要求。
