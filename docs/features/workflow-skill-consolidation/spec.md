# Workflow Skill Consolidation Spec

## 元数据 (Metadata)

- **Status**: Approved
- **Source**: 2026-07-23 conversation-confirmed brainstorming design、当前 19 个 `SKILL.md` / `agents/openai.yaml`、`README.md`、`AGENTS.md`、`scripts/validate-skills.py` 与父仓库 `CLAUDE.md`
- **Generated at**: 2026-07-23
- **Feature Slug**: `workflow-skill-consolidation`
- **Planning Mode**: Full
- **Supersedes**: 当前 active workflow 中把 `quick-change`、`diagnose-ue`、`workflow-router` 作为独立入口的行为；既有 `docs/features/` 与父仓库 quality/improvement reports 继续作为历史记录，不回写

## 问题陈述 (Problem Statement)

当前仓库公开 19 个 Skill，但其中三项已经形成可消除的职责重叠：

- `quick-change` 与 `implement` 都执行 branch、scope、repro/test、最小实现、review、verification 和 finish，只是在风险与 ceremony 上不同。
- `diagnose-ue` 与 `diagnose` 都执行 feedback loop、复现、3–5 个可证伪 hypotheses、targeted instrumentation、regression seam、cleanup 六阶段；UE 的真正增量是 runtime mode、probe/artifact 和 regression seam 等 domain profile。
- `workflow-router` 不产生 artifact 或执行业务动作，只重复 frontmatter descriptions、README 路由表和各 Skill 的 `Natural Handoff`。当前静态表已经出现遗漏 `$brainstorming` 和 `improve-codebase-architecture` 的 drift。

重复入口让用户和 agent 在 `$quick-change` / `$implement`、`$diagnose-ue` / `$diagnose` 之间重复路由，也让 validator、README、AGENTS、metadata 和 Natural Handoff 同时维护相同决策。用户已经明确接受废弃旧入口，不要求 alias 或旧命令兼容，因此可以把严格子集能力并入 owner Skill，并删除纯 meta-router。

## 目标 (Goals)

- 将公开 Skill 数量从 19 精确收敛为 16。
- 让 `$implement` 成为唯一 implementation entry，并在内部可靠区分 Quick Path 与 Standard Path。
- 让 `$diagnose` 成为唯一 diagnosis entry，并按 Generic/UE Profile 与 Active Repro/Artifact-based Triage 两个正交维度执行。
- 删除 `$workflow-router`，改由 frontmatter trigger、仓库级 `Natural Handoff` 和各 Skill 的本地 handoff contract 直接路由。
- 保留 branch、planning、read-only audit、independent review、verification、finish 和持久知识写入的现有安全边界。
- 保持每个保留 Skill 可被 `npx skills use . --skill <name> --full-depth` 独立加载，不依赖 sibling Skill 的 reference。
- 让 validator、active docs、metadata、父仓库 living contract 与本地 `npx skills` discoverability 对 16-Skill 拓扑保持一致。

## 方案与架构 (Approach and Architecture)

### 最终公开拓扑

```text
Design / Planning
  brainstorming
  grill-me
  to-spec
  to-plan
  analyze

Understanding / Diagnosis
  clarify
  diagnose
  improve-codebase-architecture

Implementation / Delivery
  checking-branch
  tdd
  implement
  requesting-code-review
  verification-before-completion
  finishing-branch

Session
  handoff
  session-curator
```

删除且不保留 alias：

- `quick-change`
- `diagnose-ue`
- `workflow-router`

### `$implement` 的 Quick / Standard 执行路径与 Blocked outcome

`implement` 在任何写入和 branch 操作之前执行只读 path dispatch，并记录 `ImplementationPathDecision v1`：

| Field | Contract |
| --- | --- |
| `Path` | `Quick | Standard | Blocked` |
| `Evidence` | 命中的资格或升级事实 |
| `Scope` | 用户已授权的 implementation boundary；Quick 为 tight change，Standard 可为 task set，Blocked 记录未收束 gap |
| `Acceptance` | 可独立判断的完成条件；Blocked 记录缺失 decision |
| `Verification` | 预期先失败/暴露症状、后通过的 seam/set；Blocked 记录缺失 evidence seam |
| `EscalationReason` | 仅在 `Standard` 或 `Blocked` 时记录；无则 `None` |

Quick Path 必须同时满足：

- 单一 tight change；`Scope` 与 `Acceptance` 均可用一句话表达。
- 低风险且不需要多个 task、产品决策或 architecture 决策。
- 已有快速可靠的 pass/fail seam，或能在约 10–15 分钟内建立。
- 不改变 public contract、schema、migration、权限、安全、数据生命周期或 core workflow。
- 预计只涉及少量局部文件可以作为正向 signal，但不得仅凭文件数量分类。

Standard Path 命中任一即可：

- 输入为 checked plan、包含多个 task、跨模块或中高风险。
- 修改 shared/public contract、schema、migration 或 core workflow。
- Quick 条件不能全部满足，但 scope、acceptance 与 implementation authorization 已经清楚。

两条路径共享：

- 写入前的 `checking-branch` gate。
- 用户 scope 和 existing changes 保护。
- 最终 `verification-before-completion`。
- 仅在用户要求 commit、PR、merge、discard 或分支交付时进入 `finishing-branch`。

Quick Path 额外执行三行 `Scope / Acceptance / Verification` contract、targeted failing test 或等价 repro、最小实现和 light self-review。Standard Path 继续消费 checked plan / conditional `$analyze`、串行 TDD tasks、独立 review subagent 和更宽 verification。

Quick Path 在 scope、acceptance 和 branch authorization 不变时发现影响面或验证范围扩大，可以在同一 `$implement` 内升级为 Standard Path，不重新 handoff，也不重复 branch gate。若 scope、acceptance 或产品/架构决策改变，则停止并唯一推荐 `$to-plan` 或 `$brainstorming`；若 bug 无可靠 repro，则停止并唯一推荐 `$diagnose`。

Quick 资格、disqualifiers、升级规则和输出 contract 的 single source of truth 放在 `implement/references/quick-path.md`；`implement/SKILL.md` 只保留 dispatch、graph integration 和不可绕过的 gate。

### `$diagnose` 的 Profile / Evidence Mode 双轴

`diagnose` 保留唯一 canonical six-phase protocol：

1. Feedback loop
2. Reproduce / evidence bounding
3. Falsifiable hypotheses
4. Targeted instrumentation
5. Repair direction / regression seam
6. Cleanup / retrospective

Phase 1 前记录 `DiagnosticContext v1`：

| Field | Contract |
| --- | --- |
| `Profile` | `Generic | UE` |
| `EvidenceMode` | `Active Repro | Artifact-based Triage` |
| `ObservedFailure` | 当前 observation status 与精确目标症状/artifact facts；Active 首次进入可为 `pending — <target failure>` |
| `RuntimeMode` | UE 时记录 Editor/PIE/Standalone/Cooked/Packaged/Shipping、server/client、platform、RHI、build configuration；Generic 时可为 `N/A` |
| `RootCauseStatus` | `confirmed | likely | blocked`；初始只能为 `likely` 或 `blocked` |
| `RegressionSeam` | 正确 test/repro/command seam；没有时说明 gap |
| `MissingEvidence` | 仍需的最小材料；无则 `None` |

Profile 选择规则：

- 用户明确描述 Unreal Engine、Editor、PIE、Cooked、Packaged、Shipping、Blueprint、RHI 等症状，或仓库事实与症状共同指向 UE runtime path 时选择 `UE`。
- 其他诊断选择 `Generic`。
- 只有 `UE` Profile 才按需读取同一 Skill 目录下的：
  - `diagnose/references/ue/runtime-modes.md`
  - `diagnose/references/ue/probes-and-artifacts.md`
  - `diagnose/references/ue/regression-seams.md`

Evidence Mode 选择规则：

- 当前 agent 能建立并运行或结构化指导 feedback loop 时选择 `Active Repro`；首次进入尚未观察到目标 failure 时记录 `ObservedFailure: pending`，初始 `RootCauseStatus: blocked`。
- 只有 log、callstack、trace、capture、截图、asset 或其他 concrete artifact，无法运行原场景时选择 `Artifact-based Triage`。
- Artifact-based Triage 可以列出 3–5 个可证伪 hypotheses 和下一步 probes，但不得声称“已复现”或把 root cause 标为 `confirmed`；只能为 `likely` 或 `blocked`。
- Active Repro 在 evidence-bounding 阶段仍未观察到目标 failure 时必须停止、继续磨尖 loop 或请求最小 runtime/input；有 concrete artifacts 时可更新 context 后转入 Artifact-based Triage，但不得进入 hypotheses 或 root-cause claim。
- Active Repro 只有在精确 failure 已观察、hypothesis prediction 经定向 probe 或 causal intervention 验证、主要替代假设已被证据排除，并记录 evidence pointer 后，才能把 `RootCauseStatus` 从 `likely/blocked` 提升为 `confirmed`。
- 既无可信 loop、又无足够 artifact 时停止并请求最小材料。
- 后续获得运行环境时允许从 Artifact-based Triage 转入 Active Repro。

UE Profile 必须保持 runtime parity：Packaged/RHI/network/platform-only failure 不能仅凭 PIE 通过宣称验证完成；UE debug logs、Blueprint probes、临时 maps/assets 和 captures 必须清理或明确归档位置。

repair scope 与 regression seam 已可执行时，`diagnose` 唯一推荐 `$implement`，由后者选择 Quick/Standard；证据不足、没有正确 repair seam 或用户只要诊断报告时以 `none` 结束。

### 无中央 Router 的直接路由

- 初始请求由每个 `SKILL.md` frontmatter description 和 `agents/openai.yaml` metadata 触发。
- 用户显式点名 Skill 时直接进入该 Skill，并保留其内部 gate。
- 一个 Skill 完成后，最多通过本地 `Natural Handoff` 推荐一个 next Skill 或 `none`。
- 用户的 `继续`、`可以`、`按你说的办`、`go ahead`、`ok`、`好的` 只绑定上一条回复的唯一推荐；如果上一条有多个选项或用户增加新条件，则重新按当前上下文选择。
- Natural Handoff 只完成转场，不批准 branch、code、review、verification、commit、push、PR、merge、discard 或文档写入。
- 普通 implementation request 直接进入 `$implement`，由其内部执行 branch gate；只有用户明确只想准备分支时才单独进入 `$checking-branch`。

### Migration 与 repository contract

- 在同一原子 cutover 中删除三个 Skill 目录、更新 retained Skills、README、AGENTS、metadata 和 validator。
- active retained artifacts 不再出现 retired names；`docs/features/**` 与父仓库 root quality/improvement reports 明确排除在 retired-text 扫描外。
- 父仓库 `CLAUDE.md` 作为 living contract 同步到新拓扑，但 submodule validator 不得读取或依赖 parent file。
- 仓库没有 plugin/marketplace manifest，`npx skills` 直接扫描各目录 `SKILL.md`；本次不新增 manifest。
- 新 feature workspace 不存在既有 manifest，因此 Full Planning Run 只创建本 `spec.md + plan.md`。

## 关键决策与取舍 (Key Decisions and Tradeoffs)

- **决策**: 采用 19 → 16 的边界优先方案。**理由**: 只合并严格子集和纯 meta-router，不混淆 read/write、review/verification 或 branch lifecycle 授权。**被排除的方案**: 进一步把 `tdd` 并入 `implement`、把 `grill-me` 并入 `brainstorming` 会形成更复杂的模式组合；能力家族化会制造大而宽的万能 Skill。
- **决策**: 不保留 compatibility alias。**理由**: 用户明确选择允许废弃旧入口；alias 会继续暴露 19 个选择并保留重复维护点。**代价**: 旧显式命令需要改用 `$implement` 或 `$diagnose`。
- **决策**: Quick→Standard 是同 Skill 内状态转移。**理由**: 风险扩大但 scope 未变时没有新的授权边界，不应制造一次跨 Skill handoff。**保护**: scope、acceptance 或架构决策改变时仍必须停止。
- **决策**: UE 作为 `$diagnose` 的 progressive-disclosure profile。**理由**: canonical protocol 相同，只有 domain references 独有；把 references 放在同一 Skill 目录可保持 standalone `--full-depth` 加载。**保护**: Generic Profile 不加载 UE references。
- **决策**: Artifact-based Triage 是明确 evidence mode。**理由**: UE 和实际诊断经常只有 log/callstack；完全禁止 hypotheses 会丢失可行动分析。**保护**: 未 Active Repro 时禁止 `confirmed` root-cause claim。
- **决策**: 删除 `workflow-router`，不创建替代 meta-skill。**理由**: platform trigger 与 local Natural Handoff 已能完成路由；继续维护中央表会恢复 drift。**保护**: README/AGENTS 和 retained Skill local contracts 由 validator 检查。
- **决策**: validator 动态统计 Skill 数量。**理由**: 本次删除后自然输出 16，永久硬编码 16 会阻碍未来合法新增 Skill。retired directory/text 和 merged-contract markers 提供更稳定的回归保护。

## 非目标 (Non-Goals)

- 不合并或删除 `tdd`、`grill-me`、`to-spec`、`to-plan`、`analyze`、branch/review/verification/finish/session Skills。
- 不改变 `$to-plan` 的 Fast/Full、Planning Authorization、checked-plan 或独立 `$to-spec` / `$analyze` 边界。
- 不降低 `checking-branch`、独立 review subagent、`verification-before-completion` 或 `finishing-branch` 的安全门。
- 不机械更新历史 `docs/features/**`、父仓库 quality/improvement reports 或旧 commit 历史。
- 不更新用户机器上已安装的 Skill 副本，不创建 alias、shim 或 compatibility facade。
- 不在本 feature 中修改其他 submodule、业务代码、测试框架或远端仓库。
- Planning 与后续 implementation 均不自动 commit、push、创建 PR、merge 或 discard。

## 功能需求 (Functional Requirements)

- **FR-001**: 最终 public inventory 必须精确包含本 spec 列出的 16 个 Skill；`quick-change/`、`diagnose-ue/`、`workflow-router/` 及其 metadata/references 必须删除，且不得保留 alias。
- **FR-002**: `implement` 的 frontmatter、进入边界、Trigger Description、Pressure Scenarios 和 `agents/openai.yaml` 必须覆盖低风险单点变更、conversation-scoped implementation 与 checked-plan implementation，使其成为唯一 implementation entry。
- **FR-003**: `implement` 必须在任何写入和 branch 操作前生成可审计的 `ImplementationPathDecision v1`；只有全部 Quick 条件成立时才能选择 Quick Path，否则选择 Standard 或 Blocked。
- **FR-004**: Quick Path 必须保留 branch gate、`Scope / Acceptance / Verification` contract、先失败/暴露症状的 targeted test 或等价 repro、最小实现、light self-review、最终 verification 和 finish boundary。
- **FR-005**: Quick 条件在 scope/acceptance/branch authorization 不变时失效，必须在同一 `$implement` 内升级 Standard 且不重复 branch gate；scope/acceptance/architecture 改变时停止，缺少可靠 repro 时唯一推荐 `$diagnose`。
- **FR-006**: Standard Path 必须继续保留 checked-plan intake、对未检查/external artifacts 的 `$analyze` gate、串行 TDD、独立 review subagent、fix/re-review、verification 和 optional finishing flow。
- **FR-007**: Quick qualification、disqualifiers、escalation 和输出 contract 必须以 `implement/references/quick-path.md` 为 single source of truth；主 `implement/SKILL.md` 不得复制完整 Quick playbook。
- **FR-008**: `diagnose` 的 frontmatter、Trigger Description、Pressure Scenarios、output contract 和 `agents/openai.yaml` 必须同时覆盖 Generic 与 UE symptoms，使其成为唯一 diagnosis entry。
- **FR-009**: `diagnose` 必须记录 `Profile: Generic | UE`，且只在 UE Profile 条件读取同目录三个 `references/ue/*.md`；Generic Profile 不得加载或输出无关 UE workflow。
- **FR-010**: `diagnose` 必须记录 `EvidenceMode: Active Repro | Artifact-based Triage`；初始 `RootCauseStatus` 只能为 `likely/blocked`，Artifact-based Triage 不得声称已复现或输出 `confirmed`，Active Repro 只有通过 prediction、targeted probe/causal intervention、主要替代假设排除与 evidence pointer 后才能提升为 `confirmed`。
- **FR-011**: UE Profile 必须记录对应 runtime mode，并要求 packaged/network/platform/RHI-specific failure 在相同 mode 验证；所有 UE-specific instrumentation 与临时 artifacts 必须清理或明确归档。
- **FR-012**: repair-ready diagnosis 必须唯一推荐 `$implement`，由 `$implement` 决定 Quick/Standard；证据不足、没有正确 seam 或只需报告时必须以 `none` 结束，不得引用 retired implementation/diagnosis entry。
- **FR-013**: `workflow-router` 必须删除；初始路由由 Skill description/metadata 完成，跨 Skill 转场由仓库级与 per-Skill `Natural Handoff` 完成，并继续限制自然确认只绑定上一条唯一推荐。
- **FR-014**: 所有 retained active Skills 必须移除对三个 retired names 的进入条件、路由和 handoff；普通 implementation request 必须直接进入 `$implement`，而不是先单独路由 `$checking-branch`。
- **FR-015**: `README.md`、submodule `AGENTS.md`、retained examples/references/metadata 与父仓库 `CLAUDE.md` 必须描述同一 16-Skill 拓扑；历史 artifacts 必须保持不改。
- **FR-016**: `scripts/validate-skills.py` 必须移除对 retired files 的硬依赖，验证 README/AGENTS 的 Natural Handoff、Quick/Standard 与 Generic/UE/evidence-mode markers、迁移后 references 存在、retired directories 不存在及 active artifacts 无 retired names；不得依赖父仓库文件。
- **FR-017**: 本地 `npx skills` 必须发现且只发现目标 16 个 Skill；16 个保留名称的 `--full-depth` 必须成功，三个 retired names 必须返回 no match；公开远端 discoverability 只能在后续获得 push 授权并发布 submodule 后验证。
- **FR-018**: 实现必须保持独立 planning、branch、review、verification、finish、session 与 read-only audit 边界，不修改其他 submodule，不更新安装副本，也不执行未授权的 commit/push/PR/merge/discard。

## 成功标准 (Success Criteria)

- **SC-001**: `python scripts/validate-skills.py` 退出码为 0，并输出 `Validated 16 skills.`
- **SC-002**: `npx --yes skills add . --list` 输出 `Found 16 skills`，集合与本 spec 最终拓扑完全一致。
- **SC-003**: 16 个 retained names 的本地 `npx ... use --full-depth` 均成功；三个 retired names 均 exit 1 并报告 `No matching skill found`。
- **SC-004**: 单一低风险 tight change 命中 Quick Path，执行 branch、三行 contract、targeted signal、minimal change、light review 和 final verification，不生成 plan。
- **SC-005**: checked plan、多 task 或中高风险输入命中 Standard Path，保留独立 review subagent 和完整 verification。
- **SC-006**: 初始 Quick 在发现 shared contract/core workflow/multi-task 后，在 scope 不变时同 Skill 升级 Standard，不重复 branch gate，也不推荐 retired Skill。
- **SC-007**: 无可靠 pass/fail seam 的 bug 在写代码前停止，并唯一推荐 `$diagnose`；需要 planning/design 的输入分别唯一推荐 `$to-plan` / `$brainstorming`。
- **SC-008**: Generic diagnosis 不加载 UE references；UE Active Repro 记录 runtime mode；UE Artifact-based Triage 明确未复现且不输出 confirmed root cause。
- **SC-009**: packaged/RHI/network/platform-only UE 场景仅在对应 runtime mode 验证后才能宣称 repair verified。
- **SC-010**: 直接 implementation/UE symptom 分别进入 `$implement`/`$diagnose`；唯一 Natural Handoff 后的自然确认无需 meta-router 即可进入目标 Skill且不跳过其 gates。
- **SC-011**: 排除 `docs/features/**` 与父仓库历史 reports 后，active artifacts 对三个 retired names 的搜索为零命中。
- **SC-012**: submodule 与 parent worktree 只包含本 feature 批准的文件，`git diff --check` 均通过，其他 submodule 保持不变。

## 测试决策 (Testing Decisions)

- **Static validator**: 扩展 `validate-skills.py` 检查 merged contracts、Natural Handoff、reference paths、retired directory/text；skill count 继续动态计算。
- **Local discoverability**: 使用已在当前环境验证可运行的 `npx --yes skills add . --list` 与 `npx --yes skills use . --skill <name> --full-depth`。
- **Manual forward scenarios**:
  - Implementation: `IMP-QUICK`、`IMP-STANDARD`、`IMP-UPGRADE`、`IMP-NO-REPRO`、`IMP-NEEDS-PLAN`、`IMP-NEEDS-DESIGN`、`IMP-EXTERNAL-FAKE-PASS`、`IMP-NATURAL-CONFIRM`。
  - Diagnosis: `DGN-GENERIC-ACTIVE`、`DGN-GENERIC-ARTIFACT`、`DGN-UE-ACTIVE`、`DGN-UE-ARTIFACT`、`DGN-UE-MODE-DRIFT`、`DGN-PERF-BASELINE`、`DGN-HANDOFF`。
  - Routing: direct implementation、direct UE diagnosis、single Natural Handoff confirmation、ambiguous/multi-option confirmation。
- **Historical exclusion**: retired-token scan 必须排除 `docs/features/**`；parent scan 必须排除 root `quality-report-*`、`improvement-plan-*`、`update-report-*`。
- **Remote verification boundary**: `fjxyyzg3/Skills` 远端检查不是本地 implementation completion 的前置条件；只有用户之后授权 commit/push 并实际发布 submodule 时才能作为 confirmed-current evidence。

## 风险与开放问题 (Risks and Open Questions)

- **Risk**: `implement` trigger 变宽后可能把需要 diagnosis/planning 的请求误判为 Quick。通过写入前 `ImplementationPathDecision v1`、Quick 全条件与 Blocked handoff scenarios 降低风险。
- **Risk**: Quick 与 Standard 共存可能让 `implement/SKILL.md` 继续膨胀。通过 `references/quick-path.md` progressive disclosure 和只在主 graph 保留 dispatch/gates 控制体积。
- **Risk**: Artifact-based Triage 可能弱化“无反馈循环不猜测”的纪律。通过独立 Evidence Mode、禁止 confirmed claim、要求 artifact provenance 和 missing evidence 控制。
- **Risk**: 删除 router 后，自然确认可能在上一条不唯一时被误绑定。仓库级 contract 必须继续要求“上一条唯一推荐”，并通过 ROUTE-HANDOFF scenario 验证。
- **Risk**: retired names 会继续出现在历史 artifacts 与本 feature spec/plan。validator/stale scan 必须只覆盖 active surfaces，不得篡改历史记录。
- **Risk**: 本地 `npx skills` 通过不能证明公开远端已更新。最终报告必须区分 local verified 与 remote not published。
- **Open Questions**: None。用户已确认允许废弃旧入口、采用 19 → 16 方案、删除 router、无 alias、历史 artifacts 不回写。

## Plan 交接说明 (Handoff Notes for Plan)

- 先为 `implement` 和 `diagnose` 建立新 owner contracts，确保新入口已能承载旧能力。
- 再重连 retained Skills 与 active docs，使所有 handoff 只指向新 owner。
- 最后原子删除三个旧目录并同步 validator，避免留下 validator 硬依赖或 active stale routes。
- 父仓库 `CLAUDE.md` 在 submodule contract 稳定后更新；submodule validator 必须保持 standalone。
- plan 必须为 `FR-001` 至 `FR-018` 建立 task、acceptance 和 verification coverage，并明确本 Planning Run 不授权任何 implementation 或 Git/remote 操作。
