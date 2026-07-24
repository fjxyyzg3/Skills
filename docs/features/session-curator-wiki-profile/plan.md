# Session Curator Wiki Profile Implementation Plan

## 元数据 (Metadata)

- **Source**: `docs/features/session-curator-wiki-profile/spec.md`
- **Generated at**: 2026-07-24
- **Status**: Ready
- **Planning Mode**: Full
- **Feature Slug**: `session-curator-wiki-profile`
- **Contract Name**: `Session Curator Wiki Profile v1`
- **Risk rationale**: 输入是已有的 conversation-confirmed formal spec；实现会改变 `session-curator` 的默认 workflow contract，新增 wiki-specific reference/projection，调整 metadata、validator 和 fresh-session verification，并必须保持 `CuratedDurable`、owner、identity、dirty-file 与 Git delivery 边界一致。
- **Planning Quality Status**: Pass

## 风险判定 (Risk Decision)

- **PlanningMode**: `Full`
- **Evidence**:
  - 输入已有 `docs/features/session-curator-wiki-profile/spec.md`，包含 `FR-001` 至 `FR-024`、`SC-001` 至 `SC-011`、architecture decisions 和 verification seams。
  - 变更会改变 `session-curator` 的核心 workflow：每次 invocation 增加 `Wiki Check`，并新增 wiki root/owner、summary scan、candidate、transfer mode 和 fail-closed contract。
  - 实现范围跨越 `SKILL.md`、`agents/openai.yaml`、references、README、validator、verification matrix 和 feature manifest。
  - 需要 isolated fresh-session scenarios 验证“用户确认前零写入”、跨 Git owner report、ambiguous/dirty target fail closed 和 scope 不扩张。
- **Conflicts**: `None`
- **UserOverride**: `None`

## 已核实基线 (Verified Baseline)

- `python scripts/validate-skills.py` 当前 exit code 0，输出 `Validated 16 skills.`。
- `codex --version` 当前输出 `codex-cli 0.145.0`。
- `npx --yes skills add . --list` 当前 exit code 0，输出 `Found 16 skills`。
- 当前 active skill inventory 仍为 16 个；没有新增顶层 `wiki` skill。
- 当前 `session-curator/SKILL.md`、metadata 和 references 没有 `Wiki Check`、wiki profile、wiki status enum 或 wiki-specific owner/transfer contract。
- 当前仓库没有 `scripts/tests` 或 `scripts/fixtures`；`scripts/validate-skills.py` 是 stdlib-only 单文件 validator。
- `docs/features/artifact-placement/` 和 `docs/features/session-curator-wiki-profile/` 当前均为未跟踪 feature artifacts；前者是本任务之前已有的 planning artifact，必须保护且不得混入本 feature implementation scope。

## 假设 (Assumptions)

- 用户在 `$grill-me` 中逐项确认的设计决策构成当前 feature 的 approved direction；本 plan 复用 spec 的 `FR-001` 至 `FR-024`，不重新编号或扩大需求。
- `session-curator` 继续是唯一 durable writer；wiki profile 不新增顶层 skill、router 或独立文件写入 authority。
- v1 使用 `SKILL.md`、reference prose、metadata 和 validator markers 表达 `Wiki Check`；不新增 machine-readable Wiki Check JSON declaration。未来 `ArtifactPlacement` active contract 若要求结构化 declaration，必须重新审查兼容性。
- 由于当前没有独立 test harness，静态 validator、verification matrix 和 isolated `codex exec` fresh-session scenarios 共同构成验证路径；没有实际运行的 scenario 不得标记为通过。
- 当前工作树已有的 `docs/features/artifact-placement/` 不属于本 feature 的 active surface；不修改、不移动、不重命名、不删除。
- `README.md` 只增加维护者摘要和 profile 入口，不复制 wiki profile 的完整算法；`AGENTS.md` 不新增 wiki 细节，避免把 runtime reference 重复到 repository policy。

## 全局约束 (Global Constraints)

- 只修改本 plan 明确列出的 active surfaces；不修改其他 submodule、父仓库 living docs、全局安装副本或已有 `docs/features/artifact-placement/` 文件。
- 保持 16-skill inventory 不变；不得创建 `wiki/SKILL.md`、新的 router 或第二个 durable writer。
- `session-curator` 的既有 scope、confirmation、authoritative target、identity、dirty-file、owner 和 Git delivery safety gates 不得弱化。
- 每个实现 task 串行执行；下一 task 只能消费前一 task 明确产生的 contract/artifact。
- 用户可见 prose 和普通 heading 使用中文主文；paths、commands、contract fields、status values、IDs 和必要技术术语保留 English。
- 文件写入不授权 stage、commit、push、PR、merge、parent gitlink update、discard 或其他 Git/remote action。
- `docs/features/session-curator-wiki-profile/spec.md` 与 `manifest.md` 只能在对应 planning/activation gate 下更新状态；不得提前声明 Implementation Complete 或 Effective。
- 默认不扩大到全仓库 source ingestion；新增 manifest、watcher、自动刷新或强制 raw-source directory 需求必须重新进行 scope review。

## 产物与接口 (Artifacts and Contracts)

| Artifact | Producer | Consumer | 关键字段/内容 |
| --- | --- | --- | --- |
| `SessionCuratorWikiProfileSpec v1` | 已有 spec | T1/T2/T3/T4 | `FR-001..024`、`SC-001..011`、AD decisions、non-goals |
| `SessionCuratorWikiProfileProjection v1` | T1 | T2/T3/T4 | `Wiki Check`、scope、root/owner precedence、structure、transfer、fail-closed、Git boundary |
| `SessionCuratorWikiProfileScenarioSuite v1` | T2 | T3/T4 | no-root、no-change、unique-update、ambiguous、dirty、cross-owner、transfer、scope-limit scenarios |
| `SessionCuratorWikiProfileValidatorGate v1` | T2 | T3/T4 | required markers、status enum、forbidden automation/stale text、metadata/discoverability checks |
| `SessionCuratorWikiProfileFreshSessionEvidence v1` | T3 | T4 | candidate source/digest、expanded prompt、before/after filesystem/Git、Wiki Check、mutation/owner evidence |
| `SessionCuratorWikiProfileActivationEvidence v1` | T4 | manifest/status handoff | all required validation outcomes、residual risks、per-owner status |

## 顺序任务 (Serial Tasks)

### Task 1: 建立 wiki profile contract 与 session-curator projection

- **Files**:
  - Modify: `session-curator/SKILL.md`
  - Modify: `session-curator/agents/openai.yaml`
  - Create: `session-curator/references/wiki-profile.md`
  - Modify: `session-curator/references/document-targets.md`
  - Modify: `session-curator/references/curation-quality.md`
  - Modify: `README.md`
  - Test: `docs/features/session-curator-wiki-profile/spec.md`
- **Consumes**: `SessionCuratorWikiProfileSpec v1`
- **Produces**: `SessionCuratorWikiProfileProjection v1`
- **Covers**: `FR-001`, `FR-002`, `FR-003`, `FR-004`, `FR-006`, `FR-007`, `FR-008`, `FR-009`, `FR-010`, `FR-011`, `FR-012`, `FR-013`, `FR-014`, `FR-015`, `FR-016`, `FR-017`, `FR-021`, `FR-022`, `FR-023`

**验收标准 (Acceptance Criteria)**:

- `session-curator` 的 trigger description 明确覆盖 wiki/知识库请求，但不把 wiki 变成独立 skill。
- 每次 invocation 的 workflow 都要求输出 `Wiki Check`；状态枚举精确为 `not-applicable`、`no-change`、`candidate`、`resolved`、`blocked`。
- wiki check 使用当前 `session-curator` scope；默认只扫描 wiki 路径和第一行摘要，不触发全仓库全文读取。
- wiki root/owner precedence、无 root 时 candidate-only、跨 docs owner report 和 Git delivery 禁止行为都能从独立安装的 `session-curator` bundle 读出。
- `wiki-profile.md` 定义页面摘要、标题、topic 同名说明页、根/目录索引、lowercase kebab-case、forward-only migration、source transfer 和 fail-closed matching。
- `spec`、`plan`、`handoff`、session 的默认 transfer mode 是摘要/整理或拆分；全文转入、原文保留和来源记录规则明确。
- `session-curator` 的统一修改计划包含独立 wiki candidate 字段：target、operation、source、transfer mode、精确 file/section 和 risk；同一 plan item 不要求重复 wiki confirmation。
- `document-targets.md` 与 `curation-quality.md` 不再与 wiki owner、stable-knowledge、no-generic-fallback 或 no-automatic-migration 规则冲突。
- `agents/openai.yaml` 的 `short_description` 和 `default_prompt` 能反映 wiki check，但不暗示自动写入、Git delivery 或全仓库扫描。
- `README.md` 只增加 session-curator/wiki profile 的维护者摘要和入口，不复制完整 wiki 算法。

**Verification**:

- `python scripts/validate-skills.py`，预期输出 `Validated 16 skills.`。
- `npx --yes skills use . --skill session-curator --full-depth`，预期能够解析候选 skill bundle。
- `rg -n "Wiki Check|not-applicable|no-change|candidate|resolved|blocked|wiki-profile|source-manifest|stage、commit、push|不能.*自动" session-curator README.md`，预期 profile contract、状态和禁止行为可定位。
- `git diff --check -- session-curator README.md`，预期无 whitespace error。
- 人工检查独立读取 `session-curator/SKILL.md` 和 `references/wiki-profile.md` 时不依赖 repo-root `AGENTS.md` 才能理解默认 wiki behavior。

### Task 2: 建立 validator gate 与 scenario matrix

- **Files**:
  - Modify: `scripts/validate-skills.py`
  - Create: `docs/features/session-curator-wiki-profile/verification-matrix.md`
  - Test: `session-curator/SKILL.md`
  - Test: `session-curator/agents/openai.yaml`
  - Test: `session-curator/references/wiki-profile.md`
  - Test: `session-curator/references/document-targets.md`
  - Test: `session-curator/references/curation-quality.md`
  - Test: `README.md`
  - Test: `docs/features/session-curator-wiki-profile/spec.md`
  - Test: `docs/features/session-curator-wiki-profile/manifest.md`
- **Consumes**: `SessionCuratorWikiProfileProjection v1`
- **Produces**: `SessionCuratorWikiProfileScenarioSuite v1`; `SessionCuratorWikiProfileValidatorGate v1`
- **Covers**: `FR-001`, `FR-002`, `FR-003`, `FR-004`, `FR-005`, `FR-006`, `FR-007`, `FR-008`, `FR-009`, `FR-010`, `FR-011`, `FR-012`, `FR-013`, `FR-014`, `FR-015`, `FR-016`, `FR-017`, `FR-018`, `FR-019`, `FR-020`, `FR-021`, `FR-022`, `FR-023`, `FR-024`

**验收标准 (Acceptance Criteria)**:

- `verification-matrix.md` 至少定义以下场景，并为每个场景给出 Input、Expected `Wiki Check`、Forbidden Action、Pass Signal 和 Cleanup：
  - `WIKI-NO-ROOT-CANDIDATE`
  - `WIKI-EXISTING-NO-CHANGE`
  - `WIKI-UNIQUE-UPDATE`
  - `WIKI-AMBIGUOUS-MATCH`
  - `WIKI-DIRTY-OVERLAP`
  - `WIKI-CROSS-OWNER`
  - `WIKI-SUMMARY-SPLIT-TRANSFER`
  - `WIKI-EXPLICIT-FULL-TRANSFER`
  - `WIKI-NON-WIKI-CURATION`
  - `WIKI-SCOPE-LIMIT`
- validator 新增 focused wiki profile gate，至少检查：
  - `session-curator`、metadata、wiki reference 和 README 的 required markers；
  - 五个 `Wiki Check` status values；
  - summary/index/owner/transfer/fail-closed contract；
  - `source-manifest.json`、watcher、自动刷新、全仓库默认扫描和独立 `wiki` skill 等 v1 forbidden drift；
  - `-2`、`-new`、`-final` sibling bypass；
  - 不修改或扫描历史 `docs/features/artifact-placement/` 作为 active contract。
- validator 继续保持 stdlib-only、默认 `run_default_validation()` 入口和 `Validated 16 skills.` 输出，不新建 test framework。
- scenario matrix 的 expected behavior 与 spec 的 `FR`/`SC` 使用相同 status/value 语义，不创建第二套枚举。
- 文档自身通过 strict UTF-8、LF、BOM、trailing whitespace、TODO/模板残留和 stable ID 检查。

**Verification**:

- `python -B -c "import ast, pathlib; p=pathlib.Path('scripts/validate-skills.py'); ast.parse(p.read_text(encoding='utf-8'), filename=str(p))"`，预期 exit code 0 且不创建 `__pycache__`。
- `python scripts/validate-skills.py`，预期输出 `Validated 16 skills.`。
- `rg -n "WIKI-NO-ROOT-CANDIDATE|WIKI-EXISTING-NO-CHANGE|WIKI-UNIQUE-UPDATE|WIKI-AMBIGUOUS-MATCH|WIKI-DIRTY-OVERLAP|WIKI-CROSS-OWNER|WIKI-SCOPE-LIMIT" docs/features/session-curator-wiki-profile/verification-matrix.md`，预期全部命中。
- `rg -n "Wiki Check|not-applicable|no-change|candidate|resolved|blocked|source-manifest|watcher|-2|-new|-final" scripts/validate-skills.py docs/features/session-curator-wiki-profile/verification-matrix.md`，预期 validator gate 与 forbidden drift 可定位。
- `git diff --check -- scripts docs/features/session-curator-wiki-profile session-curator README.md`，预期无 whitespace error。

### Task 3: 执行 isolated fresh-session verification

- **Files**:
  - Test: `session-curator/SKILL.md`
  - Test: `session-curator/agents/openai.yaml`
  - Test: `session-curator/references/wiki-profile.md`
  - Test: `session-curator/references/document-targets.md`
  - Test: `session-curator/references/curation-quality.md`
  - Test: `scripts/validate-skills.py`
  - Test: `docs/features/session-curator-wiki-profile/verification-matrix.md`
  - Test: `docs/features/session-curator-wiki-profile/spec.md`
- **Consumes**: `SessionCuratorWikiProfileProjection v1`; `SessionCuratorWikiProfileScenarioSuite v1`; `SessionCuratorWikiProfileValidatorGate v1`
- **Produces**: `SessionCuratorWikiProfileFreshSessionEvidence v1`
- **Covers**: `FR-001`, `FR-002`, `FR-003`, `FR-004`, `FR-005`, `FR-006`, `FR-007`, `FR-008`, `FR-009`, `FR-010`, `FR-011`, `FR-012`, `FR-013`, `FR-014`, `FR-015`, `FR-016`, `FR-017`, `FR-018`, `FR-019`, `FR-020`, `FR-021`, `FR-022`, `FR-023`, `FR-024`

**验收标准 (Acceptance Criteria)**:

- 每个 scenario 使用独立 fixture 和独立 `codex exec` session；不得依赖前一个 session 的 conversational state。
- candidate skill 从当前 submodule 的 project-local full-depth copy 加载；记录 `CandidateSkillSource`、`CandidateDigest`、`InstalledDigest`、`LoadedDigest`，三者必须一致。
- `WIKI-NO-ROOT-CANDIDATE` 在用户确认前只输出 candidate，不创建 root、topic、page 或 index。
- `WIKI-EXISTING-NO-CHANGE` 只读取路径和摘要，不批量读取 wiki 正文，不产生 filesystem/Git delta。
- `WIKI-UNIQUE-UPDATE` 先输出精确 plan item；确认后只更新批准页面和必要 index，并保持最小 diff。
- `WIKI-AMBIGUOUS-MATCH`、`WIKI-DIRTY-OVERLAP` 和 owner ambiguity 输出 `blocked`，只问一个合并后的问题，目标 bytes 和其他 dirty files 保持不变。
- `WIKI-CROSS-OWNER` 首次 filesystem mutation 前报告 docs owner/path，只产生 docs owner change，无 code repo change、gitlink change 或 Git delivery。
- `WIKI-SUMMARY-SPLIT-TRANSFER` 默认只写稳定摘要/拆分内容并记录 source；`WIKI-EXPLICIT-FULL-TRANSFER` 只有明确 full mode 后才允许全文归档，原文保持不变。
- `WIKI-NON-WIKI-CURATION` 仍输出 Wiki Check，但不因 wiki 存在而静默改写 wiki。
- `WIKI-SCOPE-LIMIT` 不扫描全仓库、历史 session 或 raw source；只有显式扩大 scope 才进入更大扫描。
- 任一 required scenario 未实际运行或失败时，不把 spec/manifest 标为 Effective/Complete，保留 residual risk。

**Verification**:

- 初始化每个 fixture 后先执行 `git status --short --untracked-files=all`，记录 `ExpectedBeforeGit`；clean-intake case 不得因 harness bootstrap 产生被测 workspace dirty。
- 使用 project-local candidate skill 安装/复制流程，推荐命令：
  - `npx --yes skills add <candidate-repo> --skill session-curator --agent codex --copy -y --full-depth`
  - 对无 ambient Git root 的 fixture，在核验 source/destination absolute paths 后执行等价 full-depth copy，不使用 `-g`。
- 每个 case 使用：
  - `codex exec -C <fixture-root> --ephemeral --ignore-user-config --json --output-last-message <out>\agent-final.json`
  - 无 Git fixture 额外使用 `--skip-git-repo-check`；
  - 记录 expanded prompt、candidate source/digest、before/after filesystem、before/after Git、Wiki Check、first mutation 和 cleanup。
- 每个 case 完成后执行 `git status --short --untracked-files=all` 和 scoped filesystem comparison；预期结果必须与 `verification-matrix.md` 完全一致。
- fresh-session evidence 未完整记录时，结果为 `Not yet effective`，不得使用静态 validator pass 替代。

### Task 4: 完成 activation gate 与 planning/implementation handoff

- **Files**:
  - Modify: `docs/features/session-curator-wiki-profile/spec.md`（仅更新真实 Effective/implementation status）
  - Modify: `docs/features/session-curator-wiki-profile/manifest.md`（记录真实 Plan/Implementation/Contract Effect）
  - Test: `docs/features/session-curator-wiki-profile/plan.md`
  - Test: `docs/features/session-curator-wiki-profile/verification-matrix.md`
  - Test: `scripts/validate-skills.py`
  - Test: `session-curator/SKILL.md`
  - Test: `session-curator/agents/openai.yaml`
  - Test: `README.md`
  - Test: `AGENTS.md`
- **Consumes**: `SessionCuratorWikiProfileProjection v1`; `SessionCuratorWikiProfileValidatorGate v1`; `SessionCuratorWikiProfileFreshSessionEvidence v1`
- **Produces**: `SessionCuratorWikiProfileActivationEvidence v1`
- **Covers**: `FR-001`, `FR-002`, `FR-003`, `FR-004`, `FR-005`, `FR-006`, `FR-007`, `FR-008`, `FR-009`, `FR-010`, `FR-011`, `FR-012`, `FR-013`, `FR-014`, `FR-015`, `FR-016`, `FR-017`, `FR-018`, `FR-019`, `FR-020`, `FR-021`, `FR-022`, `FR-023`, `FR-024`

**验收标准 (Acceptance Criteria)**:

- `python scripts/validate-skills.py`、strict artifact checks、discoverability、scenario matrix 和 fresh-session evidence 全部通过。
- `npx --yes skills add . --list` 仍输出 `Found 16 skills`，不出现独立 `wiki` skill。
- `session-curator` project-local full-depth discovery、metadata、Wiki Check markers 和 reference links 全部一致。
- spec/manifest 只在所有 required activation gates 通过后更新为真实状态：
  - planning 完成时：`Plan: Ready`、`Planning Quality Status: Pass`、`Implementation: Not started`；
  - implementation 未完成前：不得写 `Implementation: Complete` 或 `Effective`；
  - fresh-session required case 缺失或失败时：保持 `Not yet effective` 并记录 residual risk。
- parent workspace 与 target submodule 分别报告 status；本 feature 不产生父仓库文件修改、不修改其他 submodule、不混入 `artifact-placement/`。
- checked plan handoff 只推荐 `$implement` 或 `none`，不包含 branch、commit、push 或远端授权。

**Verification**:

- `python scripts/validate-skills.py`，预期输出 `Validated 16 skills.`。
- `npx --yes skills add . --list`，预期输出 `Found 16 skills`。
- `npx --yes skills use . --skill session-curator --full-depth`，预期 full-depth 解析成功。
- `git diff --check -- session-curator scripts README.md docs/features/session-curator-wiki-profile`，预期无 whitespace error。
- `git status --short --branch`（target submodule）和父仓库 `git status --short --branch`，预期只显示批准范围内的 submodule/feature artifact 状态。
- `git submodule status --recursive`，预期其他 submodule 指针不变。
- `git diff --name-only -- docs/features ":(exclude)docs/features/artifact-placement/**"`，实现阶段除本 feature 外不得出现意外 feature artifact 修改。

## FR Coverage Matrix

| Requirement | Implementation Task(s) | Verification seam |
| --- | --- | --- |
| `FR-001` | T1, T2, T3, T4 | Wiki Check marker; status output; fresh sessions |
| `FR-002` | T1, T2, T3, T4 | scope rules; `WIKI-SCOPE-LIMIT` |
| `FR-003` | T1, T2, T3, T4 | no broad scan marker; scope-limit case |
| `FR-004` | T1, T2, T3, T4 | enum validator; all scenario statuses |
| `FR-005` | T2, T3, T4 | candidate/blocked zero-write cases |
| `FR-006` | T1, T2, T3, T4 | owner precedence; cross-owner/ambiguous cases |
| `FR-007` | T1, T3, T4 | no-root candidate-only case |
| `FR-008` | T1, T3, T4 | pre-write owner/path report |
| `FR-009` | T1, T2, T3, T4 | forbidden Git action scans and status evidence |
| `FR-010` | T1, T2, T3 | page structure checks |
| `FR-011` | T1, T2, T3 | root/topic index checks |
| `FR-012` | T1, T2, T3 | naming rule checks |
| `FR-013` | T1, T3 | path/summary-only scan evidence |
| `FR-014` | T1, T2, T3, T4 | forward-only migration case |
| `FR-015` | T1, T2, T3 | stable-content filtering cases |
| `FR-016` | T1, T3 | summary/split transfer case |
| `FR-017` | T1, T3 | explicit full transfer and source preservation |
| `FR-018` | T1, T2, T3 | unique candidate case |
| `FR-019` | T1, T2, T3 | ambiguous/identity/dirty/owner blocked cases |
| `FR-020` | T2, T3 | sibling suffix forbidden scan |
| `FR-021` | T1, T2, T3 | unified plan item schema and confirmation evidence |
| `FR-022` | T1, T3 | candidate-to-resolved transition |
| `FR-023` | T1, T3 | single confirmation and re-confirm-on-new-target case |
| `FR-024` | T1, T2, T4 | no automation/manifest/watcher gate |

## Assumptions 与 Residual Risks

### Assumptions

- `session-curator` 的当前 `CuratedDurable` semantics 在实现期间仍以当前 active `SKILL.md` 为基线；未激活的 `artifact-placement` plan 不能被当作 runtime behavior。
- `README.md` 摘要更新不会改变独立安装时的 runtime contract；完整 wiki profile 必须保留在 `session-curator` 自身 bundle 中。
- validator marker gate 可以在没有额外 test framework 的情况下表达静态 contract；行为正确性仍由 fresh-session scenarios 证明。
- `Wiki Check` 的 machine-readable declaration 不属于 v1；若未来需要，必须新增 decision/plan scope。

### Residual Risks

- 当前没有现成 fresh-session harness，Task 3 的隔离 fixture、candidate digest、filesystem watcher 和 evidence capture 需要 implementation 阶段实现或以可复现手动流程完成。
- 现有 wiki 历史页面可能不符合新摘要/index contract；本 plan 不自动迁移，长期一致性需要后续显式 migration scope。
- `docs/features/artifact-placement/` 后续若激活，可能要求 session-curator 增加结构化 placement declaration；实现前需重新核对两份 contract。
- model-driven cross-turn behavior 不能被静态 validator 完全证明；required fresh-session case 未通过时必须保持 `Not yet effective`。

## Planning Quality Gate

- **RequirementsCoverage**: Pass
- **TaskCompleteness**: Pass
- **ContractConsistency**: Pass
- **RepositoryFeasibility**: Pass
- **ConstraintAlignment**: Pass
- **AutoFixSummary**: None
- **ResidualRisks**: Listed above
- **Planning Quality Status**: Pass

## Checked Plan Handoff

- **PlanningMode**: `Full`
- **ArtifactPaths**:
  - `docs/features/session-curator-wiki-profile/spec.md`
  - `docs/features/session-curator-wiki-profile/plan.md`
- **Coverage**: `FR-001..024 -> Task 1/2/3/4 -> contract projection, validator/scenario gate, fresh-session evidence and activation verification`
- **QualityStatus**: `Planning Quality Status: Pass`
- **AutoFixSummary**: `None`
- **Assumptions**: v1 uses prose/reference plus validator markers；当前未激活的 `artifact-placement` planning artifact 不作为 runtime contract；fresh-session verification 是 activation 前置条件
- **ResidualRisks**: 当前没有专用 fresh-session harness；历史 wiki 页面可能不符合 forward-only 结构；未来 `ArtifactPlacement` activation 可能要求额外 placement declaration
- **NextSkill**: `none`（本次请求只要求 planning artifacts）
