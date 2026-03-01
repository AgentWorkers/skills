---
name: pr-ship
description: >
  **OpenClaw Pull Request（PR）的发货前风险报告**  
  该报告会动态扫描代码库，以评估模块的风险、潜在问题（“blast radius”）以及特定版本可能存在的缺陷。每个问题会根据严重程度进行分级（🟢/🟡/🔴）。报告内容会随着OpenClaw版本的更新而实时更新——请定期运行`clawhub update pr-ship`命令以获取最新信息。
---
# pr-ship

## 概述

本技能用于生成针对 **[OpenClaw](https://github.com/openclaw/openclaw)** 提交请求（Pull Requests, PRs）的预发布风险报告。

该技能会**频繁更新**，以跟踪 OpenClaw 的版本变化。每次上游版本发布时，都会更新与特定版本相关的风险信息（潜在问题、行为变化、活跃的风险区域）。请定期运行 `clawhub update pr-ship` 命令以获取最新风险报告。

**功能说明：**
- 将当前分支与 OpenClaw 仓库的 `main` 分支进行差异对比。
- 对代码库中每个发生变化的模块进行动态检查（使用 `grep`、`find`、`git` 等工具）。
- 生成一份结构化的风险报告，其中包含基于证据的风险发现结果，并根据严重程度进行评分（🟢/🟡/🔴）。
- 本工具仅提供信息，供您在提交代码前决定是否需要进行修复，不涉及批准或拒绝的决策。

## 参考文件

这些文件位于 `references/` 目录中，每个文件都有其特定的用途：

1. **`STABLE-PRINCIPLES.md`** – OpenClaw 的通用编码标准：测试指南、文件命名规则、安全不变量、常见错误以及 PR 提交规范。
2. **`ARCHITECTURE-MAP.md`** – OpenClaw 的架构结构：模块层次结构、风险等级定义、关键路径模式、模块间的耦合关系以及变更影响矩阵。
3. **`CURRENT-CONTEXT.md`** （可选） – 与当前版本相关的潜在问题、最近的行为变化及活跃的风险区域。如果存在该文件，请将其加载，以便了解当前版本的详细风险情况。
4. **`EXPLORATION-PLAYBOOK.md` – 动态检查流程：包含用于查看 OpenClaw 代码库状态的只读命令（`grep`、`find`、`ls`、`git`）。
5. **VISION-GUIDELINES.md** – 项目愿景、贡献政策以及合并规则，这些内容基于 OpenClaw 的 `VISION.md` 文档制定。涵盖了 PR 的提交范围、安全理念、插件与核心代码的边界、技能使用规范以及明确的“不予合并”列表。通过该文件可以检测政策或架构上的不一致之处。

**注意事项：**
- `STABLE-PRINCIPLES`、`ARCHITECTURE-MAP`、`EXPLORATION-PLAYBOOK` 和 `VISION-GUIDELINES` 文件必须始终存在。`CURRENT-CONTEXT` 文件是可选的；如果缺失，该工具仍可正常使用，但无法获取特定版本的风险信息。

## 工作流程

### 1. 加载参考文件
- 阅读上述四个参考文件。

### 2. 获取与 `main` 分支的差异
- 查看当前分支：`git branch --show-current`
- 获取文件列表：`git diff --name-only main...HEAD`
- 获取差异内容：`git diff main...HEAD`

### 3. 分类发生变化的模块
- 对于每个发生变化的文件，确定其所在的路径（`src/<module>/`）。
- 在 `ARCHITECTURE-MAP.md` 中查找该模块的风险等级。
- 如果该模块未在列表中或需要进一步验证，请根据 `EXPLORATION-PLAYBOOK.md` 中的“动态风险分类”部分执行相应的检查。

### 4. 对每个发生变化的模块进行动态检查
- 遵循 `EXPLORATION-PLAYBOOK.md` 中的“Blast Radius Discovery”流程来检查每个发生变化的文件。
- 根据模块类型，执行相应的“模块特定检查策略”。
- 使用“Test Discovery”部分来识别相关的测试用例。
- 根据差异结果检查“Red Flags Table”中的警告信息。

### 5. 评估风险发现结果
- 将检查结果与以下内容进行对比：
  - `STABLE-PRINCIPLES.md` 中的安全不变量和常见错误。
  - （如果加载了 `CURRENT-CONTEXT.md`，则）与当前版本相关的潜在问题。
  - `ARCHITECTURE-MAP.md` 中的架构耦合模式。
  - `VISION-GUIDELINES.md` 中的贡献政策、合并规则及架构方向。
- 确保 PR 的提交范围符合项目规定（每个 PR 应针对一个具体主题，遵守大小限制和打包规则）。
- 检查是否存在 `VISION-GUIDELINES.md` 第 7 节中列出的“不予合并”的情况。
- 评估新功能是否遵守插件与核心代码的边界以及安全理念。
- 每个风险发现结果都必须包括：
  - 来自差异对比的**证据**（文件内容及代码片段）。
  - **动态检查的结果**（显示影响范围、依赖模块或匹配模式的命令输出）。
  - 与该问题或耦合模式相关的具体规范、潜在问题或架构模式的**参考链接**。

### 6. 生成报告
- 使用以下格式生成报告。
- 报告中不包含“批准/拒绝”的判断结果。

## 风险等级与警报评分

- 🟢 **低风险**（评分 1-2）：仅是风格上的小问题或信息性提示，可以按原样发布。
- 🟡 **需要关注**（评分 3-6）：存在部分不匹配、模糊性或安全加固措施缺失的情况，建议审查但不太可能导致故障。
- 🔴 **高风险**（评分 7-10）：存在明显的编码标准、架构模式或版本限制违规，可能导致错误、代码回退或政策违规。

**评分规则：**
- 对每个风险发现结果单独评分（1-10 分）。
- **最终警报评分 = 最高风险得分**。如果没有发现风险，则最终评分为 0。

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

- 本技能仅适用于 **OpenClaw 仓库**，请勿在其他项目中使用。
- 仅检查当前分支与 `main` 分支之间的差异。
- 无需查看其他仓库的历史记录。
- 除非明确要求，否则不要自动修改代码。
- 除非明确请求，否则不要将报告转化为批准或拒绝的决策。
- 所有检查命令均为**只读**（`grep`、`find`、`ls`、`git diff`），严禁执行构建、测试或代码生成命令；建议在报告中向用户推荐这些命令以供参考。

## 来源与维护信息

- **来源：** [github.com/Glucksberg/pr-ship](https://github.com/Glucksberg/pr-ship)
- **维护者：** Markus Glucksberg ([@Glucksberg](https://github.com/Glucksberg))
- **更新机制：** 当 OpenClaw 仓库的 `CHANGELOG.md` 发生更新时，`CURRENT-CONTEXT.md` 的元数据会通过 cron 任务每日更新。GitHub 仓库由维护者单独维护。
- **验证方式：** GitHub 仓库是官方的权威版本。如需验证您安装的版本是否与官方版本一致，请参考以下内容：

```bash
# Quick: compare file list + versions
diff <(clawhub list | grep pr-ship) <(curl -s https://api.github.com/repos/Glucksberg/pr-ship/contents/package.json | jq -r '.content' | base64 -d | jq -r .version)

# Full: diff your local install against GitHub
SKILL_DIR="$(find ~/.openclaw/skills -maxdepth 1 -name pr-ship -type d 2>/dev/null || echo skills/pr-ship)"
for f in SKILL.md package.json references/CURRENT-CONTEXT.md; do
  diff <(cat "$SKILL_DIR/$f") <(curl -s "https://raw.githubusercontent.com/Glucksberg/pr-ship/main/$f") && echo "$f: ✔ match" || echo "$f: ✘ differs"
done
```

## 安全提示

本工具生成的报告中可能包含来自您本地仓库的差异对比结果和 `grep` 命令的输出。如果您的配置文件、环境或代码中包含敏感信息（如 API 密钥、令牌、凭据等），这些信息可能会出现在报告中。**在发布或共享报告之前，请先检查其中是否包含敏感数据。**

## 致谢

本技能的原始格式和实现方法借鉴自 [mudrii](https://github.com/mudrii) 的开发者参考文档。动态检查流程是根据 OpenClaw 维护者社区的反馈进行设计的。