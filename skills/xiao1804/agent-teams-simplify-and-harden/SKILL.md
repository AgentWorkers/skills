---
name: agent-teams-simplify-and-harden
description: "**实施与审计循环：采用并行代理团队，结合结构化的简化、加固和文档编写流程**  
该流程首先启动实施代理来执行具体任务，随后审计代理会检查代码中的复杂性、安全漏洞以及与规范的偏差。这一循环会持续进行，直到代码能够顺利编译、所有测试通过，并且审计人员未发现任何问题，或者达到循环的预设上限。  
**适用场景：**  
- 根据规范或计划实现新功能；  
- 加固现有代码；  
- 修复一批问题；  
- 任何需要经过“构建-验证-修复”循环来提升代码质量的多文件项目。"
---
# Agent Teams：简化与强化代码质量

## 安装

```bash
npx skills add pskoett/pskoett-ai-skills/agent-teams-simplify-and-harden
```

这是一个分为两个阶段的团队协作流程，用于生成高质量的代码：**首先进行实现（implement）**，然后使用 **Simplify** 和 **Harden** 工具进行审核，**修复审核中发现的问题**，**再次进行审核**，这个过程会一直重复，直到代码库达到稳定状态或达到预定的循环次数上限。

## 适用场景

- 从规范或计划中实现多个功能时
- 在进行批量代码修改后对代码库进行强化处理时
- 修复在审查中发现的各类问题或漏洞时
- 任何涉及5个以上文件且质量控制至关重要的任务时

## 工作流程

```
┌──────────────────────────────────────────────────────────┐
│                  TEAM LEAD (you)                          │
│                                                           │
│  Phase 1: IMPLEMENT (+ document pass on fix rounds)       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                 │
│  │ impl-1   │ │ impl-2   │ │ impl-3   │  ...            │
│  │ (general │ │ (general │ │ (general │                 │
│  │ purpose) │ │ purpose) │ │ purpose) │                 │
│  └──────────┘ └──────────┘ └──────────┘                 │
│       │             │            │                        │
│       ▼             ▼            ▼                        │
│  ┌─────────────────────────────────────┐                 │
│  │  Verify: compile + tests            │                 │
│  └─────────────────────────────────────┘                 │
│       │                                                   │
│  Phase 2: SIMPLIFY & HARDEN AUDIT                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                 │
│  │ simplify │ │ harden   │ │ spec     │  ...            │
│  │ auditor  │ │ auditor  │ │ auditor  │                 │
│  │ (Explore)│ │ (Explore)│ │ (Explore)│                 │
│  └──────────┘ └──────────┘ └──────────┘                 │
│       │             │            │                        │
│       ▼             ▼            ▼                        │
│  Exit conditions met?                                     │
│    YES → Produce summary. Ship it.                        │
│    NO  → back to Phase 1 with findings as tasks           │
│          (max 3 audit rounds)                             │
└──────────────────────────────────────────────────────────┘
```

## 循环限制与退出条件

当满足以下任意一条条件时，循环将终止：

1. **审核结果无问题**：所有审核人员均未发现任何问题。
2. **所有问题均为低严重级别**：将这些问题直接修复（由团队负责人或指定的实现代理完成），然后退出循环，无需再次审核。
3. **达到循环上限**：已完成3轮审核。在第三轮审核后，直接修复剩余的严重/高严重级别问题，并在最终总结中记录所有未解决的问题（中等/低严重级别问题）。

**预算建议**：跟踪各轮审核中代码差异的累积增长情况。如果修复工作导致的差异超过了原始代码差异的30%，应缩小审核范围，仅关注需要强化的代码部分和规范中的遗漏内容。

## 详细步骤

### 1. 创建团队

```
TeamCreate:
  team_name: "<project>-harden"
  description: "Implement and harden <description>"
```

### 2. 划分任务

将工作分解为独立、可并行处理的任务。每个任务应足够独立，以便单个代理能够独立完成，而不会影响到其他任务的进展。

```
TaskCreate for each unit of work:
  subject: "Implement <specific thing>"
  description: "Detailed requirements, file paths, acceptance criteria"
  activeForm: "Implementing <thing>"
```

根据需要设置任务之间的依赖关系：
```
TaskUpdate: { taskId: "2", addBlockedBy: ["1"] }
```

### 3. 创建实现代理

创建 **通用型** 代理（这些代理具有读写和编辑文件的功能）。每个任务对应一个代理，或者每个逻辑模块对应一个代理。这些代理需要 **并行执行**。

```
Task tool (spawn teammate):
  subagent_type: general-purpose
  team_name: "<project>-harden"
  name: "impl-<area>"
  mode: bypassPermissions
  prompt: |
    You are an implementation agent on the <project>-harden team.
    Your name is impl-<area>.

    Check TaskList for your assigned tasks and complete them.
    After completing each task, mark it completed and check for more.

    Quality gates:
    - Code must compile cleanly (substitute your project's compile
      command, e.g. bunx tsc --noEmit, cargo build, go build ./...)
    - Tests must pass (substitute your project's test command,
      e.g. bun test, pytest, go test ./...)
    - Follow existing code patterns and conventions

    When all your tasks are done, notify the team lead.
```

### 4. 等待实现任务完成

监控代理的运行状态。当所有实现代理都报告任务完成后：

1. 运行编译和类型检查，确保代码构建无误。
2. 运行测试，确保所有功能都能正常运行。
3. 如果有任何问题，先修复这些问题，然后再进行下一步。

在创建审核代理之前，收集本次修改的文件列表：
```bash
git diff --name-only <base-branch>  # or: git diff --name-only HEAD~N
```
将这份文件列表提供给所有审核人员。

### 5. 创建审核代理

创建 **只读型** 的审核代理（这些代理无法修改文件，从而避免他们无意中修改代码）。每个审核人员负责检查不同的方面，遵循 **Simplify & Harden** 的审核方法。

**推荐的审核维度**：

| 审核类型 | 审核重点 | 审核思路 |
|---------|-------|---------|
| **简化审核** | 代码的清晰度和不必要的复杂性 | “是否有更简洁的实现方式？” |
| **强化审核** | 安全性和代码的健壮性 | “如果攻击者看到这段代码，他们会尝试做什么？” |
| **规范审核** | 代码实现与规范/计划的匹配程度 | “代码是否符合要求？” |

#### 简化审核代理

```
Task tool (spawn teammate):
  subagent_type: Explore
  team_name: "<project>-harden"
  name: "simplify-auditor"
  prompt: |
    You are a simplify auditor on the <project>-harden team.
    Your name is simplify-auditor.

    Your job is to find unnecessary complexity -- NOT fix it. You are
    read-only.

    SCOPE: Only review the following files (modified in this session).
    Do NOT flag issues in other files, even if you notice them.
    Files to review:
    <paste file list here>

    Fresh-eyes start (mandatory): Before reporting findings, re-read all
    listed changed code with "fresh eyes" and actively look for obvious
    bugs, errors, confusing logic, brittle assumptions, naming issues,
    and missed hardening opportunities.

    Review each file and check for:

    1. Dead code and scaffolding -- debug logs, commented-out attempts,
       unused imports, temporary variables left from iteration
    2. Naming clarity -- function names, variables, and parameters that
       don't read clearly when seen fresh
    3. Control flow -- nested conditionals that could be flattened, early
       returns that could replace deep nesting, boolean expressions that
       could be simplified
    4. API surface -- public methods/functions that should be private,
       more exposure than necessary
    5. Over-abstraction -- classes, interfaces, or wrapper functions not
       justified by current scope. Agents tend to over-engineer.
    6. Consolidation -- logic spread across multiple functions/files that
       could live in one place

    For each finding, categorize as:
    - **Cosmetic** (dead code, unused imports, naming, control flow,
      visibility reduction) -- low risk, easy fix
    - **Refactor** (consolidation, restructuring, abstraction changes)
      -- only flag when genuinely necessary, not just "slightly better."
      The bar: would a senior engineer say the current state is clearly
      wrong, not just imperfect?

    For each finding report:
    1. File and line number
    2. Category (cosmetic or refactor)
    3. What's wrong
    4. What it should be (specific fix, not vague)
    5. Severity: high / medium / low

    If you notice issues outside the scoped files, list them separately
    under "Out-of-scope observations" at the end.

    Be thorough within scope. Check every listed file.
    When done, send your complete findings to the team lead.
    If you find ZERO in-scope issues, say so explicitly.
```

#### 强化审核代理

```
Task tool (spawn teammate):
  subagent_type: Explore
  team_name: "<project>-harden"
  name: "harden-auditor"
  prompt: |
    You are a security/harden auditor on the <project>-harden team.
    Your name is harden-auditor.

    Your job is to find security and resilience gaps -- NOT fix them.
    You are read-only.

    SCOPE: Only review the following files (modified in this session).
    Do NOT flag issues in other files, even if you notice them.
    Files to review:
    <paste file list here>

    Fresh-eyes start (mandatory): Before reporting findings, re-read all
    listed changed code with "fresh eyes" and actively look for obvious
    bugs, errors, confusing logic, brittle assumptions, naming issues,
    and missed hardening opportunities.

    Review each file and check for:

    1. Input validation -- unvalidated external inputs (user input, API
       params, file paths, env vars), type coercion issues, missing
       bounds checks, unconstrained string lengths
    2. Error handling -- non-specific catch blocks, errors logged without
       context, swallowed exceptions, sensitive data in error messages
    3. Injection vectors -- SQL injection, XSS, command injection, path
       traversal, template injection in string-building code
    4. Auth and authorization -- endpoints or functions missing auth,
       incorrect permission checks, privilege escalation risks
    5. Secrets and credentials -- hardcoded secrets, API keys, tokens,
       credentials in log output, unparameterized connection strings
    6. Data exposure -- internal state in error output, stack traces in
       responses, PII in logs, database schemas leaked
    7. Dependency risk -- new dependencies that are unmaintained, poorly
       versioned, or have known vulnerabilities
    8. Race conditions -- unsynchronized shared resources, TOCTOU
       vulnerabilities in concurrent code

    For each finding, categorize as:
    - **Patch** (adding validation, escaping output, removing a secret)
      -- straightforward fix
    - **Security refactor** (restructuring auth flow, replacing a
      vulnerable pattern) -- requires structural changes

    For each finding report:
    1. File and line number
    2. Category (patch or security refactor)
    3. What's wrong
    4. Severity: critical / high / medium / low
    5. Attack vector (if applicable)
    6. Specific fix recommendation

    If you notice issues outside the scoped files, list them separately
    under "Out-of-scope observations" at the end.

    Be thorough within scope. Check every listed file.
    When done, send your complete findings to the team lead.
    If you find ZERO in-scope issues, say so explicitly.
```

#### 规范审核代理

```
Task tool (spawn teammate):
  subagent_type: Explore
  team_name: "<project>-harden"
  name: "spec-auditor"
  prompt: |
    You are a spec auditor on the <project>-harden team.
    Your name is spec-auditor.

    Your job is to find gaps between implementation and spec/plan --
    NOT fix them. You are read-only.

    SCOPE: Only review the following files (modified in this session).
    Do NOT flag issues in other files, even if you notice them.
    Files to review:
    <paste file list here>

    Fresh-eyes start (mandatory): Before reporting findings, re-read all
    listed changed code with "fresh eyes" and actively look for obvious
    bugs, errors, confusing logic, brittle assumptions, and
    implementation/spec mismatches before running the spec checklist.

    Review each file against the spec/plan and check for:

    1. Missing features -- spec requirements that have no corresponding
       implementation
    2. Incorrect behavior -- logic that contradicts what the spec
       describes (wrong conditions, wrong outputs, wrong error handling)
    3. Incomplete implementation -- features that are partially built
       but missing edge cases, error paths, or configuration the spec
       requires
    4. Contract violations -- API shapes, response formats, status
       codes, or error messages that don't match the spec
    5. Test coverage -- untested code paths, missing edge case tests,
       assertions that don't verify enough, happy-path-only testing
    6. Acceptance criteria gaps -- spec conditions that aren't verified
       by any test

    For each finding, categorize as:
    - **Missing** -- feature or behavior not implemented at all
    - **Incorrect** -- implemented but wrong
    - **Incomplete** -- partially implemented, gaps remain
    - **Untested** -- implemented but no test coverage

    For each finding report:
    1. File and line number (or "N/A -- not implemented")
    2. Category (missing, incorrect, incomplete, untested)
    3. What the spec requires (quote or reference the spec)
    4. What the implementation does (or doesn't do)
    5. Severity: critical / high / medium / low

    If you notice issues outside the scoped files, list them separately
    under "Out-of-scope observations" at the end.

    Be thorough within scope. Cross-reference every spec requirement.
    When done, send your complete findings to the team lead.
    If you find ZERO in-scope issues, say so explicitly.
```

### 6. 处理审核结果

收集所有审核人员的审核结果。对于每个问题：

- **严重/高严重级别问题**：创建相应的任务，并分配给实现代理处理。
- **中等严重级别问题**：将这些问题纳入下一次实现循环中处理。
- **低严重级别或外观性问题**：只有在修复起来非常简单的情况下才纳入下一次循环；否则在最终总结中记录，跳过本次循环。

**重构判断标准**：对于被归类为 **需要重构** 或 **安全重构** 的问题，在创建任务之前，需要评估重构的必要性。判断标准是：**高级工程师是否会认为当前代码存在明显错误（而不仅仅是不够完善）？** 如果重构只是基于个人编码风格或微小的改进，应拒绝该提案。

**退出检查**：如果本轮审核中所有问题的严重级别均为低级别，直接修复这些问题，并跳过下一次审核（参见循环限制）。

在创建修复任务时，为每个实现代理分配以下文档编写任务：

> 在修复问题后，在你修改的文件中添加最多5条简短的注释，说明以下内容：
> - 对于那些需要花费超过5秒时间思考的逻辑决策，解释其存在的必要性。
> - 说明所做的临时解决方案或变通方法，以及未来需要改进的地方。
> - 说明当前性能选择的理由。

**注意**：不要在注释中讨论具体的修复内容，只需说明原始实现中缺乏解释的部分。

这样可以让文档编写任务保持简洁且目标明确。后续的审核人员不应将这些注释视为问题。

### 7. 重复循环

如果有问题需要修复：

1. 根据审核结果创建相应的任务。
2. 创建实现代理（或通过 SendMessage函数重新分配空闲的代理）。
3. 等待问题被修复。
4. 运行编译和测试验证。
5. 检查循环是否达到终止条件（参见循环限制）。
6. 如果未达到终止条件，再次创建审核代理（使用新的代理，避免使用之前的代理，以确保审核的客观性）。
7. 重复上述步骤。

### 8. 最终验证与总结

当满足退出条件时：

1. 运行编译和类型检查，确保代码无误。
2. 所有测试都必须通过。
3. 确保没有未解决的 **// TODO** 或 **// FIXME** 注释。

生成本次审核的最终总结：
```
## Hardening Summary

**Audit rounds completed:** 2 of 3 max
**Exit reason:** Clean audit (all auditors reported zero findings)

### Findings by round

Round 1:
- simplify-auditor: 4 cosmetic, 1 refactor (rejected -- style preference)
- harden-auditor: 2 patches, 1 security refactor (approved)
- spec-auditor: 1 missing feature

Round 2:
- simplify-auditor: 0 findings
- harden-auditor: 0 findings
- spec-auditor: 0 findings

### Actions taken
- Fixed: 6 findings (4 cosmetic, 2 patches, 1 security refactor, 1 missing feature -- rejected refactor excluded)
- Skipped: 1 refactor proposal (reason: style preference, not a defect)
- Document pass: 3 comments added across 2 files

### Unresolved
- None

### Out-of-scope observations
- <any out-of-scope items auditors flagged, for future reference>
```

请根据实际情况调整总结格式。总结应清晰记录发现的问题、已修复的问题、未修复的问题及其原因，以及剩余的问题。

### 9. 清理工作

向所有代理发送结束任务的通知，然后解散团队：
```
SendMessage type: shutdown_request to each agent
TeamDelete
```

## 代理数量建议

| 代码库/任务规模 | 实现代理数量 | 审核代理数量 |
|----------------------|-------------|--------------|
| 小型（<10个文件） | 1-2个 | 2个（简化 + 强化） |
| 中型（10-30个文件） | 2-3个 | 2-3个 |
| 大型（30个以上文件） | 3-5个 | 3个（简化 + 强化 + 规范审核） |

代理数量越多，并行处理的效率越高，但协调工作量也会增加。对于大多数任务来说，2-3个实现代理和2-3个审核代理是最合适的配置。

## 提示：

- **实现代理应为通用型代理**，因为它们需要具有写权限。
- **审核代理应为只读型代理**，以防止它们在未经许可的情况下修改代码。
- **每轮使用新的审核代理**，避免使用之前的代理，因为它们可能会带有对已检查部分的偏见。
- **任务描述必须具体**，包括文件路径、函数名称和预期的行为。模糊的任务会导致实现结果同样模糊。
- **在两个阶段之间运行编译和测试**：在代码存在问题时不要立即启动审核；先修复编译或测试错误。
- **保持循环的紧凑性**：如果审核人员只发现1-2个低严重级别的问题，可以自行修复，无需启动完整的实现循环。
- **在创建任务前先分配任务**：通过TaskUpdate设置任务的所有者，让代理明确知道需要处理的内容。
- **优先进行简化工作**：在处理审核结果时，先处理那些能减少代码杂乱性的问题，再考虑重构。通常情况下，优先进行代码优化，只有在必要时才进行重构。
- **在资源有限的情况下，优先处理强化问题**，而非简化问题。
- **提供文件列表**：务必向审核人员提供详细的修改文件列表，避免他们自行判断审核范围。

## 示例：根据规范实现功能

```
1.  Read spec, identify 8 features to implement
2.  TeamCreate: "feature-harden"
3.  TaskCreate x8 (one per feature)
4.  Spawn 3 impl agents, assign ~3 tasks each
5.  Wait → all done → compile clean → tests pass
6.  Collect modified file list (git diff --name-only)
7.  Spawn 3 auditors: simplify-auditor, harden-auditor, spec-auditor
8.  Simplify-auditor finds 4 cosmetic + 1 refactor proposal
9.  Harden-auditor finds 2 patches + 1 security refactor
10. Spec-auditor finds 1 missing feature
11. Team lead evaluates refactors (approve security refactor,
    reject simplify refactor), creates fix + document tasks
12. Spawn 2 impl agents for fixes
13. Wait → compile clean → tests pass
14. Round 2: Spawn 3 fresh auditors
15. Auditors find 0 issues → exit condition met
16. Produce hardening summary
17. Shutdown agents, TeamDelete
```

## 质量控制标准（不可协商）

在循环结束之前，必须满足以下条件：

1. 编译和类型检查无误，无错误。
2. 所有测试都通过。
3. 达到退出条件（审核结果无问题，或所有问题均为低严重级别，或达到循环上限且所有严重/高严重级别问题都已解决）。
4. 不能有未解决的 **// TODO** 或 **// FIXME** 注释。