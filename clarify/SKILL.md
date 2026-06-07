---
name: clarify
description: Use when answering codebase questions, finding where behavior lives, tracing callers/callees or data flow, explaining architecture, locating source evidence, generating Mermaid diagrams, or producing source-grounded local explanation reports.
---

# Clarify

把代码库问题转化为有来源支撑的解释。只澄清无法自行发现的信息；充分检查相关源码以避免猜测；在有帮助时，用代码位置、代码解释、图表和文档回答。

## 核心规则

- 一次最多问一个澄清问题，并给出你建议采用的默认答案。
- 如果细节可以从代码、文档、配置、示例、测试、历史记录或生成产物中发现，先检查这些来源，不要直接提问。
- 明确标注推断。不要把猜测当作有源码支撑的事实。
- 优先给出精确的文件和行号引用，而不是模糊的模块名。

## 工作流程

1. 定义目标问题。
   - 将用户问题重述为要解释的具体行为、子系统或流程。
   - 判断需要的回答形态：源码位置、主要 symbol、调用/数据流、图表，以及用户要求时的文档输出。
   - 如果请求范围不清晰，且代码探索无法解决歧义，只问一个问题并推荐默认路径。

2. 探索代码库。
   - 当项目文档能帮助回答问题时，检查解释架构、领域语言、设置方式或功能行为的文档。
   - 使用当前环境可用的源码导航工具：symbol search、text search、caller/callee lookup、dependency graph、测试、日志和聚焦文件读取。
   - 从用户提供的名称、错误文本、功能术语、API 名称、class、function、配置 key、route、command、测试和文档开始。
   - 沿 caller、callee、注册点、配置、测试、生成代码和相邻实现继续追踪，直到解释具备足够证据。
   - 维护证据地图，记录 `file:line`、symbol、在流程中的角色和可信度。

3. 综合答案。
   - 先直接回答问题，再展示支撑结论的代码路径。
   - 用自然语言解释每个重要 class、function 或 module，以及它为什么重要。
   - 在环境支持时，给出带可点击路径的关键代码引用。
   - 当控制流和数据流都重要时，分别解释两者。
   - 明确指出未解决的歧义、依赖版本的行为、缺失测试，或需要运行时验证的位置。

4. 绘制图表。
   - 对非平凡的架构或流程问题加入 Mermaid 图。
   - 根据问题选择 `flowchart`、`sequenceDiagram` 或 `classDiagram`。
   - 保持节点标签简短；包含标点的标签要加引号；避免用过密的图替代解释。
   - 用架构图表达 ownership/module 关系，用流程图表达执行路径。

5. 在用户要求或答案较大时生成文档。
   - 创建 HTML 文档前，先阅读 `references/report-structure.md`。
   - 编写独立报告时，以 `assets/clarify-report-template.html` 作为起点。
   - 如果用户指定路径，将报告保存到该路径；否则根据主题和项目结构选择清晰的本地路径。
   - 充分检查生成的 HTML，避免破损 markup。如果无法检查 Mermaid 的可视化渲染，要明确说明。

## 输出形态

简短回答：

- 直接答案
- 代码位置
- 代码讲解
- 有帮助时的 Mermaid 图
- 剩余问题或风险

生成文档时：

- 说明生成文件路径
- 总结关键结论
- 总结已检查的证据
- 如仍存在未解决歧义，明确指出
