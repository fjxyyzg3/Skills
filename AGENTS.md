# Repository Guidelines

## 项目结构与模块组织

`Skills/` 存放本仓库原生技能；`Skills-ZH/` 存放从 `submodules/` 参考技能翻译而来的
中文版本。每个技能位于 `<目录>/<skill-name>/`，入口文件固定为 `SKILL.md`；按需在同级
使用 `agents/`、`references/`、`examples/`、`assets/` 或 `scripts/`。功能规划记录放在
`Skills/docs/features/`，工作区偏好放在 `docs/user/`。子模块仅作参考；翻译任务默认写入
`Skills-ZH/<skill-name>/`，不要直接改动参考子模块或将其改动混入根仓库更新。
`Skills-ZH/` 的双语格式、翻译范围、上游同步和验收必须遵循
[`docs/wiki/skills/skill-zh-localization.md`](docs/wiki/skills/skill-zh-localization.md)。

## 开发与验证

当前根目录没有已跟踪的构建或测试入口。修改某个技能时，先用
`rg --files Skills-ZH/<skill-name>`（或对应的 `Skills/` 路径）检查完整包，并确认相对
Markdown 链接和引用文件
均存在。请求评审前运行 `git diff --check`，以发现空白和换行问题。README 提到的
`python scripts/validate-skills.py` 当前不在工作树中；除非该脚本实际可用，否则不要
声称已运行此校验。

## 风格与命名

目录使用小写 kebab-case，例如 `verification-before-completion`；入口文件必须精确命名为
`SKILL.md`。`Skills/` 中的技能正文和 `description` 以中文为主；路径、YAML key、命令、
API、稳定 ID（如 `FR-001`）及会降低触发精度的术语保留英文。`Skills-ZH/` 中的参考译本
保留上游 frontmatter 和机器契约，采用英文原文在前、中文译文在后的逐段双语格式，具体
边界以中文化规则 wiki 为准。YAML 沿用两空格缩进，Markdown 保持短标题和短列表。可复用
细节放入本技能的 `references/`，不要复制其他 workflow 的契约。

## 测试指南

仓库没有覆盖率门槛或已提交的测试框架。手动验证可观察的路由或指令变化、frontmatter、
独立引用和受影响示例；先执行最小相关路径。在变更说明中记录跳过的验证及原因。除非任务
明确要求迁移，否则保留 `Skills/docs/features/` 下的历史文件。

## 提交与拉取请求

近期提交使用简短、祈使式中文主题，例如 `结构重整`、`精简 workflow skills`。每次提交
仅覆盖一项连贯的技能或文档变更。需要创建 Pull Request 时，说明范围、受影响的技能路径、
已执行或跳过的验证，以及关联的 issue/plan；只有视觉资产变化才附截图。子模块更新须作为
独立且明确限定范围的提交。
