---
name: pr-ship
description: >
  **OpenClaw PRs的发货前风险报告**  
  该报告会动态扫描代码库，以评估模块的风险、潜在问题及其影响范围（即“破坏半径”），并针对每个问题按严重程度进行分级（🟢/🟡/🔴）。报告内容会随着OpenClaw版本的更新而实时更新——请定期运行`clawhub update pr-ship`命令以确保获取最新信息。
---
# pr-ship

## 概述

本工具用于生成针对 **[OpenClaw](https://github.com/openclaw/openclaw)** 提交请求（Pull Requests, PRs）的预发布风险报告。

该工具会 **频繁更新**，以跟踪 OpenClaw 的最新版本信息。每次上游版本发布后，工具会更新与该版本相关的具体风险信息（如潜在问题、行为变化、当前存在的风险区域等）。请定期运行 `clawhub update pr-ship` 命令以获取最新信息。

**功能说明：**
- 将您当前的分支与 OpenClaw 仓库的 `main` 分支进行差异对比。
- 对每个发生变更的模块进行动态检查，利用 `grep`、`find` 和 `git` 等命令在代码库中查找问题。
- 生成一份结构化的风险报告，其中包含基于证据的分析结果，并根据问题的严重程度进行评分（🟢/🟡/🔴）。

**注意：** 该工具仅提供信息，不提供批准/拒绝的决策建议，供您在发布代码前参考是否需要修复这些问题。

## 参考文件

这些文件位于 `references/` 目录中，每个文件都有其特定的用途：

1. **`STABLE-PRINCIPLES.md`** – OpenClaw 的通用编码标准：测试指南、文件命名规则、安全注意事项、常见错误以及提交代码时的最佳实践。
2. **`ARCHITECTURE-MAP.md`** – OpenClaw 的架构结构：模块层次结构、风险等级定义、关键路径模式以及模块间的耦合关系。
3. **`CURRENT-CONTEXT.md`** （可选） – 与当前版本相关的潜在问题、最近的行为变化及风险区域。如果存在该文件，请将其加载，以便了解当前版本的详细情况。
4. **`EXPLORATION-PLAYBOOK.md` – 动态检查流程：包含用于了解 OpenClaw 代码库状态的只读命令（`grep`、`find`、`ls`、`git`）。

**必读文件：** `STABLE-PRINCIPLES.md`、`ARCHITECTURE-MAP.md` 和 `EXPLORATION-PLAYBOOK.md` 必须始终存在。`CURRENT-CONTEXT.md` 是可选的，如果缺少该文件，工具仍能正常使用，但无法获取版本特定的风险信息。

## 工作流程

### 1. 加载参考文件
- 阅读上述四个参考文件。

### 2. 获取与 `main` 分支的差异
- 查看当前分支：`git branch --show-current`
- 获取文件列表：`git diff --name-only main...HEAD`
- 获取差异内容：`git diff main...HEAD`

### 3. 分类变更的模块
- 对于每个发生变更的文件，确定其所在的路径（`src/<module>/`）。
- 在 `ARCHITECTURE-MAP.md` 中查找该模块的风险等级。
- 如果该模块未在列表中或需要进一步验证，请执行 `EXPLORATION-PLAYBOOK.md` 中的“动态风险分类”部分中的相关命令。

### 4. 对每个变更的模块进行动态检查
- 遵循 `EXPLORATION-PLAYBOOK.md` 中的“Blast Radius Discovery”流程来分析每个变更文件。
- 根据模块类型，执行相应的“模块特定检查策略”。
- 查找相关的测试用例。
- 根据差异内容，检查“Red Flags Table”中的警告信息。

### 5. 评估检查结果
- 将检查结果与以下内容进行对比：
  - `STABLE-PRINCIPLES.md` 中的安全注意事项和常见错误。
  - （如果加载了 `CURRENT-CONTEXT.md`，则）与该版本相关的潜在问题。
  - `ARCHITECTURE-MAP.md` 中的架构耦合模式。
- 每个检查结果都必须包含：
  - **差异内容**（相关文件及代码片段）。
  **检查证据**（显示影响范围、依赖模块或匹配模式的命令输出）。
  **参考信息**（指出该问题涉及的具体编码标准、潜在问题或耦合模式）。

### 6. 生成报告
- 使用以下格式生成报告。
- 报告中不包含“批准/拒绝”的判断。

## 严重程度及警报评分

- 🟢 **低风险**（评分 1-2）：仅是轻微的格式问题或信息性提示，可以按原样发布。
- 🟡 **需要关注**（评分 3-6）：存在部分不匹配、模糊性或安全措施缺失等问题，虽然需要审查，但不太可能导致故障。
- 🔴 **高风险**（评分 7-10）：明显违反 OpenClaw 的编码标准、架构模式或版本限制，可能会导致错误、代码回退或政策违规。

**评分规则：**
- 对每个问题单独评分（1-10 分）。
- **最终警报评分 = 各问题评分的最大值**。如果没有发现任何问题，则最终评分为 0。

## 报告格式

```markdown
## pr-ship report

- Branch: `<current-branch>`
- Base: `main`
- Files changed: `<N>`
- Modules touched: `<list with risk tiers>`
- Findings: `<N>`
- Final alert score: `<0-10>`

### Module Risk Summary

| Module | Risk Tier | Consumers | Files Changed |
| --- | --- | --- | --- |
| <module> | CRITICAL/HIGH/MEDIUM/LOW | <N> | <N> |

### Findings

1. 🟢/🟡/🔴 Title
   - Alert: `<1-10>`
   - Reference: `<principle, gotcha, or pattern from reference docs>`
   - Evidence in diff: `<file + short snippet/description>`
   - Exploration evidence: `<what dynamic investigation revealed>`
   - Why this matters: `<1-2 lines>`
   - Suggested fix: `<1-2 concrete actions>`

(repeat)

### Executive summary
- `<short practical summary for decision>`
- `<top 1-3 actions before publishing PR>`
```

## 限制说明
- 本工具仅适用于 **OpenClaw 仓库**，请勿在其他项目中使用。
- 仅检查当前分支与 `main` 分支之间的差异。
- 请勿查看仓库的历史记录。
- 除非明确要求，否则不要自动修改代码。
- 除非用户明确要求，否则不要将报告作为批准/拒绝的依据。
- 所有检查命令均为只读操作（`grep`、`find`、`ls`、`git diff`），请在报告中向用户推荐这些命令以供进一步处理。

## 致谢

本工具的原始格式和设计源自 [mudrii](https://github.com/mudrii) 的开发者参考文档方法论。动态检查功能是根据 OpenClaw 维护社区的反馈进行改进的。