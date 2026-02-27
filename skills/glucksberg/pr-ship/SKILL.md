---
name: pr-ship
description: >
  **OpenClaw Pull Request（PR）的发货前风险报告**  
  该报告会动态扫描代码库，以评估各个模块的风险、潜在问题及其影响范围（即“爆炸半径”），并针对具体版本中的问题进行分类（🟢/🟡/🔴）。所有风险都会根据严重程度进行评分。报告内容会随着OpenClaw版本的更新而实时更新——请定期运行 `clawhub update pr-ship` 命令以确保信息始终是最新的。
---
# pr-ship

## 概述

本工具用于生成针对 **[OpenClaw](https://github.com/openclaw/openclaw)** 提交请求（Pull Requests, PRs）的预发布风险报告。

该工具会 **频繁更新**，以跟踪 OpenClaw 的版本变更。每次上游版本发布时，工具会更新与当前版本相关的风险信息（如潜在问题、行为变化、活跃的风险区域等）。请定期运行 `clawhub update pr-ship` 命令以获取最新风险报告。

### 功能说明：
- 将当前分支与 OpenClaw 仓库的 `main` 分支进行差异对比。
- 对每个发生变更的模块进行动态检测（使用 `grep`, `find`, `git` 等命令）。
- 生成一份结构化的风险报告，其中包含基于证据的风险发现结果，并根据严重程度进行分级（🟢/🟡/🔴）。

### 参考文件

这些文件位于 `references/` 目录中，各自具有不同的用途：
1. **`STABLE-PRINCIPLES.md` -- OpenClaw 的通用编码规范：测试指南、文件命名规则、安全注意事项、常见错误以及 PR 提交的最佳实践。
2. **`ARCHITECTURE-MAP.md` -- OpenClaw 的模块结构信息：模块层次结构、风险等级定义、关键路径模式、模块间的耦合关系以及变更影响矩阵。
3. **`CURRENT-CONTEXT.md` **（可选）** -- 与当前版本相关的问题、最近的行为变化及活跃的风险区域。如果存在该文件，请将其加载，以便了解当前版本的详细风险情况。
4. **`EXPLORATION-PLAYBOOK.md` -- 动态检测流程：包含用于查看 OpenClaw 代码库状态的只读命令（`grep`, `find`, `ls`, `git`）。
5. **`VISION-GUIDELINES.md` -- 项目愿景、贡献政策以及合并规则。这些内容基于 OpenClaw 的官方文档制定，涵盖了 PR 的提交范围、安全原则、插件与核心代码的边界、技能使用规范以及明确的“不予合并”列表。通过该文件可以确保代码符合项目政策和架构要求。

**注意**：`STABLE-PRINCIPLES`, `ARCHITECTURE-MAP`, `EXPLORATION-PLAYBOOK`, 和 `VISION-GUIDELINES` 必须始终存在；`CURRENT-CONTEXT` 是可选的。如果缺少该文件，工具仍能正常运行，但无法获取版本特定的风险信息。

### 工作流程：

### 1. 加载参考文件
- 阅读上述四个参考文件。

### 2. 获取与 `main` 分支的差异
- 查看当前分支：`git branch --show-current`
- 获取文件列表：`git diff --name-only main...HEAD`
- 获取差异内容：`git diff main...HEAD`

### 3. 分类变更的模块
- 对于每个发生变更的文件，确定其所在的路径（`src/<module>/`）。
- 在 `ARCHITECTURE-MAP.md` 中查找该模块的风险等级。
- 如果该模块未在列表中或需要进一步验证，请执行 `EXPLORATION-PLAYBOOK.md` 中的“动态风险分类”部分。

### 4. 对每个变更的模块进行动态检测
- 遵循 `EXPLORATION-PLAYBOOK.md` 中的“Blast Radius Discovery”流程来检测每个变更文件的潜在问题。
- 根据模块类型，执行相应的“模块特定检测策略”。
- 使用“Test Discovery”步骤来识别相关的测试用例。
- 根据差异内容检查“Red Flags Table”中的警告信息。

### 5. 评估风险发现结果
- 将检测结果与以下内容进行对比：
  - `STABLE-PRINCIPLES.md` 中的安全注意事项和常见错误。
  - （如果加载了 `CURRENT-CONTEXT.md`）当前版本特有的问题。
  - `ARCHITECTURE-MAP.md` 中的模块耦合模式。
  - `VISION-GUIDELINES.md` 中的贡献政策和合并规则。
- 确保 PR 的提交范围符合项目规定（每个 PR 应针对一个具体主题，遵守大小限制和打包规则）。
- 检查是否存在 `VISION-GUIDELINES.md` 第 7 节中列出的“不予合并”的情况。
- 评估新功能是否符合插件与核心代码的边界以及安全要求。

### 6. 生成报告
- 使用以下格式生成报告。报告中不会显示“批准/拒绝”状态。

## 风险等级与警报评分：
- 🟢 **低风险**（评分 1-2）：仅是风格上的小问题或信息性提示，可以直接发布。
- 🟡 **需要关注**（评分 3-6）：存在部分不匹配、模糊之处、安全防护措施缺失或非关键性的不一致性，建议审查但不太可能导致问题。
- 🔴 **高风险**（评分 7-10）：存在明显的编码规范、架构模式或版本限制违规，可能导致错误、代码回退或违反项目政策。

### 评分规则：
- 对每个风险发现结果单独评分（1-10 分）。
- **最终警报评分（final_alert_score）** = 所有发现结果中的最高分。如果没有发现问题，则 `final_alert_score` 为 0。

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

### 使用限制：
- 本工具仅适用于 **OpenClaw 仓库**，请勿在其他项目中使用。
- 仅检查当前分支与 `main` 分支之间的差异。
- 请勿查看仓库的历史记录。
- 除非明确要求，否则不要自动修改代码。
- 除非特别请求，否则不要将报告直接用于批准或拒绝决策。
- 所有检测命令（`grep`, `find`, `ls`, `git diff`）均为只读操作；建议将检测结果提供给用户以便他们自行决定如何处理代码。

### 致谢：
本工具的原始格式和实现方法借鉴自 [mudrii](https://github.com/mudrii) 的开发者参考指南。动态检测功能是根据 OpenClaw 维护社区的反馈进行设计的。