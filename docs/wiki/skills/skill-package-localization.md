> 摘要：本页规定 `Skills/` 中实际发行 Skill 的完整包中文化范围、保留边界和验收标准。

# Skills 完整包中文化规则

## 定位

`Skills/` 存放实际发行和使用的 Skill，中文化采用“完整包中文化”标准：包内所有面向人类的
说明应使用中文主文，而不是只翻译入口 `SKILL.md`。中文化必须保持 routing、行为、授权边界、
machine contract 和验证能力不变。

本页规定当前及未来的目标标准，不代表现有全部 Skill 已经完成完整包迁移。历史
`Skills/docs/features/**` 继续记录当时的范围与验证结论；既有 Skill 只有经过完整包审计和
验证后，才能声明符合本标准。

## 完整包范围

以下人类说明必须中文化：

- `SKILL.md` 的 `description`、普通正文、普通标题、表格说明和 Mermaid 可见标签；
- `references/` 下全部行为说明和维护说明；
- `examples/` 下的场景、步骤、预期结果和解释文字；
- templates、assets 或其他模板文件中的人类说明、占位说明和用户可见标签；
- `agents/openai.yaml` 等 metadata 文件中面向人类或模型的说明性值；
- scripts 中不属于精确 contract 的注释、help text 和人类可见错误说明。

“完整包”按 Skill 目录的实际文件集合判断，不能只检查从 `SKILL.md` 当前可达的文件。新增或
修改 Skill 时，必须先用 `rg --files Skills/<skill-name>` 检查完整包，再确认每个人类说明
surface 的语言边界。

## 保留英文和原始拼写

以下内容保持英文或原始拼写，不为追求中文比例而翻译：

- Skill 目录名、文件名、frontmatter key、frontmatter `name` 和 canonical skill ID；
- YAML/JSON/schema key、contract field、稳定 ID、enum、状态值、placeholder 和 machine marker；
- 代码、命令、路径、API、类名、函数名、环境变量、正则表达式和协议字面量；
- 被测试、parser、外部系统或其他 Skill 精确引用的错误文本和输出值；
- 中文会降低准确性或 routing 识别效果，且有验证证据的必要 English trigger phrase；
- 用于验证英文触发的原始 prompt、测试名称和测试数据；
- 英文专有名词、通行技术术语、许可证文本和必须保持原貌的上游引用。

保留英文 prompt 或测试数据时，其场景名称、目的、预期行为和失败解释必须使用中文。普通
说明不得为了双语对称而保留完整英文副本；`Skills/` 使用中文主文，不采用 `Skills-ZH/` 的
逐段中英对照格式。

## 语义与行为边界

- 翻译不得改变适用条件、routing 边界、授权范围、安全门、数量限制或停止条件。
- `must`、`must not`、`only when`、`should` 和 `may` 等规范性强度必须分别保持为“必须”、
  “不得”、“仅当”、“应”和“可以/允许”的等义强度。
- 无法确认等义时，必须暂停该处迁移并记录 blocker，不得猜测性改写。
- 中文化与 workflow 重构、功能修改、内容删减分开交付；除非任务明确授权，不借翻译顺便改行为。
- 完整包中文化约束 Skill 的 authoring language，不自动保证独立安装后的运行时输出语言；运行时
  语言继续由用户请求、目标项目规则、会话上下文和明确的输出 contract 决定。

## 模板和可执行文件

模板结构、代码、变量名、placeholder token、CSS selector、脚本参数和 machine-readable 输出
保持原样。只翻译其中面向人类的说明和非 contract 文本。若某段英文同时承担用户说明和精确
机器契约，应保留原文，并在相邻位置提供中文解释，不得直接改坏 contract。

## 验收

只有完整包范围与行为验证都通过后，才能声明符合本标准。

语言与结构检查至少覆盖：

- `rg --files Skills/<skill-name>` 返回的完整文件集合；
- `SKILL.md`、`references/`、`examples/`、templates、assets、metadata 和 scripts 中的人类说明；
- frontmatter、相对 Markdown 链接、引用文件和模板依赖仍然有效；
- 所有保留的 English-heavy 片段都有机器契约、精确术语或 routing/test 证据；
- `git diff --check` 无 whitespace error。

行为检查至少覆盖：

- 中文和必要英文正向 trigger 与 near-miss 边界；
- stable ID、contract field、命令、API、enum 和精确字面量未漂移；
- 规范性强度、授权边界、workflow 路由和安全门未改变；
- 受影响的 examples、模板和 scripts 仍满足原用途；
- 仓库实际存在的最小相关 validator 或测试通过。

English-heavy 审阅用于逐项判断保留理由，不以中文字符比例作为硬性通过门槛。不存在的校验脚本
不得宣称已运行；未覆盖的 runtime、统计性 routing 或模板渲染验证必须明确记录为未验证边界。
