---
name: improve-codebase-architecture
description: "当用户希望改善代码库架构、寻找 deepening opportunities、整合 shallow 或 tightly-coupled modules、提升可测试性，或让 agent 更容易理解和导航代码时使用；保留英文触发短语 improve codebase architecture、deepening opportunities 和 shallow or tightly-coupled modules。"
---

# Improve Codebase Architecture

发现可执行的架构加深机会：将 shallow modules 调整为更 deep 的 modules，使 interface 更小、implementation 承担更多行为，并提升可测试性、locality 和 agent 导航性。

## 压力场景（Pressure Scenarios）

1. 用户请求："看看这个仓库哪里值得重构。"
   - 预期触发：做架构扫描和候选报告。
   - 未使用本 skill 时的常见失败：泛泛列出通用最佳实践，没有源码证据。
   - 本 skill 必须强制的行为：用具体文件、调用关系和 deletion test 支撑每个候选。
2. 用户请求："这个模块太乱，帮我设计更好的接口。"
   - 预期触发：先确认 deepening candidate，再进入 interface design。
   - 未使用本 skill 时的常见失败：直接给出单一接口方案，忽略 seam、adapter 和测试策略。
   - 本 skill 必须强制的行为：至少比较多个不同 interface，并说明 leverage、locality 和取舍。
3. 用户请求："修完 bug 后顺便看看架构为什么会出这个问题。"
   - 预期触发：从已验证的失效模式反推架构摩擦。
   - 未使用本 skill 时的常见失败：在 bug 未收敛前泛泛重构。
   - 本 skill 必须强制的行为：只在失效模式已明确后提出 deepening opportunity。

## 核心规则

- 先读取用户指定或与扫描范围直接相关的 domain docs、ADRs 和架构说明；没有就记录缺失，不要编造。
- 使用 `references/language.md` 的架构词汇：`module`、`interface`、`implementation`、`depth`、`seam`、`adapter`、`leverage`、`locality`。
- 每个候选必须有源码证据：文件位置、调用关系、重复知识、测试痛点、依赖泄漏或维护摩擦。
- 只提出 deepening opportunities；除非用户明确要求实现，不要直接改业务代码。
- 不要把 pass-through、wrapper、过早抽象包装成架构改进。对可疑模块执行 deletion test。
- 如果候选与 ADR 冲突，只在 friction 足以重开决策时提出，并明确标注冲突。
- 如果没有足够证据，给出已检查范围和下一步探索建议，不要强行产出候选。

## 工作流程

### 1. 定义扫描范围

- 用户指定模块、目录、bug 或计划时，以该范围为主。
- 用户只说"改善架构"时，先根据 docs、近期改动、测试布局和明显核心模块选择 2-4 个高价值区域。
- 记录范围、来源文档、已知约束和明确非目标。

### 2. 探索代码

- 使用当前环境可用的 code navigation、`rg`、测试、调用关系、配置和文档。
- 寻找这些信号：
  - 理解一个 domain concept 需要在多个小模块之间来回跳。
  - module 的 interface 几乎和 implementation 一样复杂。
  - 为了测试抽出很多纯函数，但真实 bug 藏在调用编排里。
  - 调用方需要知道过多顺序、配置、错误模式或依赖细节。
  - 测试绕过 public interface，或需要 mock 很多内部步骤。
- 对每个候选用 deletion test：删除该 module 后，复杂度是消失，还是重新分散到多个 callers？
- 按 `references/deepening.md` 给依赖分类，决定 test seam 和 adapter 策略。

### 3. 产出候选

默认产出一个架构评审摘要。用户要求报告、候选较多或关系复杂时，读取 `references/html-report.md`，把自包含 HTML 报告写入 OS 临时目录：

- Windows: `$env:TEMP`
- macOS/Linux: `$TMPDIR`，缺失时用 `/tmp`
- 文件名：`architecture-review-<timestamp>.html`

每个候选必须包含：

- Files: 涉及的文件或 modules。
- Problem: 当前 architecture friction。
- Solution: deepening 后的形状。
- Benefits: 用 locality、leverage 和可测试性解释收益。
- Dependency strategy: `in-process`、`local-substitutable`、`ports & adapters` 或 `mock`。
- Recommendation strength: `Strong`、`Worth exploring` 或 `Speculative`。
- Evidence: 具体文件和行为证据。

报告最后给出首选建议，并问用户："你想先深入哪一个候选？"

### 4. 候选深入与拷问循环

用户选择候选后，围绕这些问题推进：

- deepened module 叫什么，是否符合项目领域语言？
- seam 放在哪里，interface 要隐藏哪些 ordering、config、error mode 和依赖？
- implementation 后面保留哪些 internal seams？
- 需要哪些 adapters？是否真的有两个以上 adapter 证明 seam 存在？
- 旧 tests 哪些删除，哪些迁移到新 interface？
- 哪些 ADR 或 `CONTEXT.md` 术语需要更新？

如果用户要比较 interface 方案，读取 `references/interface-design.md`。有并行 sub-agent 工具时并行设计；没有时由当前 agent 产出至少 3 个明显不同的 interface 备选方案。

### 5. 文档同步

- 新 module 名称来自尚未记录的领域概念时，建议写入 `CONTEXT.md`；用户同意后再改。
- 用户用关键支撑理由否决候选时，询问是否记录 ADR，避免未来重复建议。
- ADR 使用本地 `docs/adr/`；没有固定模板时，至少包含 status、context、decision、consequences。

## 完成标准

- 已报告扫描范围、已读取的 docs 和缺失信息。
- 每个候选都有文件证据和明确的 recommendation strength。
- 候选说明使用统一架构词汇，没有漂移到 `component`、`service`、`API`、`boundary` 等替代词。
- 已说明 dependency strategy 和测试 seam。
- 如果生成 HTML 报告，已报告绝对路径；如果没有生成，已说明原因。
- 没有直接实施重构，除非用户明确要求。
