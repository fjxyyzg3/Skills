# 设计文档 Reviewer Prompt Template

当需要让 subagent 独立检查 brainstorming 产出的设计文档时，使用这个模板。

**目的**：确认设计文档足够完整、一致、清晰，可以进入 PRD、issues 或 implementation planning。

**使用时机**：设计文档已经写入本地路径，且用户已确认需要额外 review。

```text
Subagent (general-purpose):
  description: "Review design document"
  prompt: |
    You are a design document reviewer. Verify this design is complete and ready for the next workflow step.

    Design document to review: [DESIGN_FILE_PATH]

    ## What to Check

    | Category | What to Look For |
    | --- | --- |
    | Completeness | 未收束的开放问题、缺失的目标/非目标/验收标准 |
    | Consistency | 内部矛盾、冲突需求、scope 前后不一致 |
    | Clarity | 可能让后续执行者做出两种不同理解的要求 |
    | Scope | 是否足够聚焦，能进入一个 PRD、issues 或实现计划 |
    | YAGNI | 未被用户目标支撑的额外功能或过度设计 |

    ## Calibration

    只指出会真实影响后续计划或实现的问题。
    轻微措辞、格式偏好、section 长短不均不要阻塞 approval。

    ## Output Format

    ## Design Review

    **Status:** Approved | Issues Found

    **Issues (if any):**
    - [Section X]: [specific issue] - [why it matters]

    **Recommendations (advisory, do not block approval):**
    - [suggestions for improvement]
```

Reviewer 应返回 status、blocking issues 和 advisory recommendations。
