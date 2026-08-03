> 摘要：本目录维护 `Skills/` 与 `Skills-ZH/` 的长期开发约定和参考资料规则。

# Skills

## Workflow Skill 职责边界

- `Skills/brainstorming/SKILL.md` 只负责 Brainstorming 过程：探索 context、逐题澄清、比较方案、取得设计确认，并整理 handoff。
- `Skills/to-spec/SKILL.md` 是 standalone formal spec 的唯一 owner：负责 spec 模板、稳定 `FR-###` / `SC-###`、feature manifest、spec 自审和结构验证；`$to-plan` Full Path 的 planning-coupled `spec.md` 由 `$to-plan` 在同一次 Planning Run 内负责。
- Brainstorming 的 `spec-only` handoff 只能推荐 `$to-spec`；它不创建 spec 或 manifest。`to-spec` 完成 spec-only 交付后不自动生成 plan；用户随后明确需要 checked plan 时再进入 `$to-plan`。
- 这条职责边界只描述 `Skills/` 的发行 workflow；`Skills-ZH/` 仍是 submodules 参考 Skill 的双语对照资料，不是发行实现。

## 页面

- [`skill-package-localization.md`](skill-package-localization.md)：规定 `Skills/` 中实际发行 Skill 的完整包中文化范围、保留边界和验收标准。
- [`skill-zh-localization.md`](skill-zh-localization.md)：规定 `Skills-ZH/` 中 submodules 参考 Skill 的中英双语中文化边界、格式、同步和验收规则。
