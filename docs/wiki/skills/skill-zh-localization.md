> 摘要：本页规定 `Skills-ZH/` 中 submodules 参考 Skill 的中英双语中文化、上游同步和验收规则。

# Skills-ZH 参考 Skill 中文化规则

## 定位

`Skills-ZH/` 存放 `submodules/` 中参考 Skill 的中英双语对照版本，用于帮助
`Skills/` 下实际发行和使用的 Skill 开发。`Skills-ZH/` 本身不用于发行、安装、运行或
routing，因此中文化的第一优先级是忠实、易理解和可追溯，而不是运行时触发效果或英文
字符清零。

本规则只约束 `Skills-ZH/`。`Skills/` 中的实际 Skill 继续按自身 authoring、routing 和
验证规则开发；不得把参考译文不经设计与验证直接视为可发行实现。

## 基本原则

- 采用逐段中英双语，英文原文在前，中文译文在后。
- 采用契约等义翻译：中文可以调整语序，但不得改变条件、授权、禁止、数量或停止边界。
- 保留上游目录结构、frontmatter、machine contract 和精确字面量。
- 翻译不得顺便重构、纠错或改变上游 Skill 行为。
- 只翻译行为相关内容；不因追求中文比例而改写代码、配置或资产。

## 文件范围

每个参考 Skill 位于 `Skills-ZH/<skill-name>/`，来源映射由统一 manifest 记录。翻译范围包括：

- `SKILL.md`；
- `SKILL.md` 递归引用的行为说明 Markdown；
- 影响设计或行为理解的 examples。

以下内容保留上游原样：

- scripts、配置、模板实现和二进制资产；
- 代码、命令、路径、API、schema、稳定 ID、enum 和 placeholder；
- 原始用户 prompt、测试名称、精确错误文本和其他行为字面量；
- 未被引用且不影响行为理解的材料。

不在翻译范围内的源文件仍应复制到参考包，保持完整目录结构和相对链接。不得直接修改
`submodules/` 中的参考源。

## 双语格式

### Frontmatter

frontmatter 整体保持上游原样，字段和值都不得为了中文显示而改写。紧邻 frontmatter 后为
`description` 提供中文译文：

```markdown
> **`description` 中文译文：** 当用户……时使用此 Skill。
```

不得创建第二个 frontmatter，也不得把中文追加到上游 `description` 值中。

### 标题与段落

- 普通标题使用 `English（中文）`。
- 代表 canonical skill name 的 H1、稳定 section name 或 machine marker 保持原样；需要解释时紧邻补充中文，不改标识本身。
- 普通正文按逻辑段配对，英文原文完整保留，中文译文紧随其后：

```markdown
Original English paragraph.

> **中文译文：** 对应的中文译文。
```

- 列表和表格按完整逻辑块配对，不把同一条规则拆散到不相邻位置。
- 代码块、命令和精确字面量只保留一份；需要时在其后说明用途，不复制一份“中文代码”。
- 上游歧义、疑似错误或额外背景使用 `> **译者注：**`，不得混入译文或静默修正原文。

## 契约等义

规范性强度必须保持一致，常见对应关系如下：

| English | 中文强度 |
| --- | --- |
| `must` | 必须 |
| `must not` | 不得 |
| `only when` | 仅当 |
| `should` | 应 |
| `may` | 可以或允许 |

翻译时按上下文选择自然表达，但不得把强制规则弱化为建议，也不得把建议升级为强制规则。
无法确认等义时，应暂停该处翻译并记录待校对项。

## 上游追踪与同步

`Skills-ZH/manifest.yaml` 统一记录每个参考 Skill 的：

- Skill 名称；
- 来源 submodule 和相对路径；
- 完整译本对应的 source commit；
- 纳入翻译的文件集合；
- 翻译和校对状态；
- 最近校对日期；
- 可选的待同步 `upstream_available_commit`。

以单个 Skill 为单位原子同步。只有纳入范围的全部文件完成翻译和校对后，才能更新
`source_commit` 并标记完成。同步进行中继续保留上一份完整译本的 commit；不得把部分新译文
和部分旧译文标记为完整同步结果。

## 验收

完成声明必须同时通过自动检查和语义校对。

自动检查至少覆盖：

- manifest、来源 commit、文件集合与翻译状态一致；
- 英文原文与中文译文按规则配对；
- 相对 Markdown 链接有效；
- frontmatter、machine contract 和精确字面量未漂移；
- 未完成的部分同步没有被标记为完成；
- `git diff --check` 无 whitespace error。

语义校对至少覆盖：

- 条件、行为和例外等义；
- 规范性强度未弱化或升级；
- trigger、授权和安全边界未改变；
- 译者注与上游规则明确分离。

由于 `Skills-ZH/` 不用于发行或实际使用，不要求安装验证、runtime routing test 或运行时中文
输出保证。若译文内容进入 `Skills/`，必须重新按实际 Skill 的规则完成独立设计与验证。
