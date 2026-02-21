---
name: pr-ship
description: >
  **OpenClaw PRs的发货前风险报告**  
  该报告会动态扫描代码库，以评估模块的风险、潜在问题及其影响范围（即“爆炸半径”），并针对每个问题按严重程度进行分类（🟢/🟡/🔴）。报告内容会随着OpenClaw版本的更新而实时更新——请定期运行`clawhub update pr-ship`命令以获取最新信息。
---
# pr-ship

## 概述

使用此技能可为当前分支生成一份**PR发布风险报告**。

该技能会**频繁更新**，以跟踪OpenClaw的版本变化。每次上游版本发布时，都会更新与特定版本相关的信息（潜在问题、行为变化、活跃的风险区域）。请定期运行`clawhub update pr-ship`以获取最新内容。

**使用范围**非常明确：  
- 仅分析**当前分支与`main`分支之间的差异**（如果`main`分支不存在，则使用仓库的默认基分支）。  
- 使用代码库本身动态检查每个发生变化的模块。  
- 输出报告供人工决策使用（不提供自动批准/拒绝的功能）。

## 参考文件

请按以下顺序从`references/`目录中加载这些文件。每个文件都有其特定的用途：  

1. **`STABLE-PRINCIPLES.md`** – 永恒的编码标准：测试指南、文件命名规则、安全不变量、常见陷阱、PR提交规范。  
2. **`ARCHITECTURE-MAP.md`** – 代码结构信息：模块层次结构、风险等级定义、关键路径模式、模块间的耦合关系。  
3. **`CURRENT-CONTEXT.md`** （可选）– 与当前版本相关的潜在问题、最近的行为变化以及活跃的风险区域。如果存在此文件，请加载它，因为它会随着OpenClaw版本的更新而变化。  
4. **`EXPLORATION-PLAYBOOK.md` – 动态检查流程：该文档中的命令用于发现代码库的当前状态，而非依赖静态参考信息。  

如果缺少任何文件，也可以继续执行操作，因为该技能可以仅使用部分参考文件。  

## 工作流程  

### 1. 加载参考文件  
- 阅读上述四个参考文件。  

### 2. 确定分支上下文  
- 获取当前分支。  
- 确认基分支：  
  - 如果存在`main`分支，请优先使用它。  
  - 否则，使用`origin/HEAD`作为目标分支。  

### 3. 收集差异信息  
- 获取文件列表：`git diff --name-only <base>...HEAD`  
- 获取补丁内容：`git diff <base>...HEAD`  

### 4. 分类发生变化的模块  
- 对于每个发生变化的文件，确定其`src/<module>/`路径。  
- 在`ARCHITECTURE-MAP.md`中查找该模块的风险等级。  
- 如果该模块未在列表中，或者需要进一步验证，请运行`EXPLORATION-PLAYBOOK.md`中的“动态风险分类”部分中的命令。  

### 5. 对每个发生变化的模块进行动态检查  
- 遵循`EXPLORATION-PLAYBOOK.md`中的“Blast Radius Discovery”步骤来检查每个文件。  
- 根据模块类型，执行相应的“模块特定检查策略”。  
- 通过“Test Discovery”步骤识别相关的测试用例。  
- 根据差异内容检查“Red Flags Table”中的警告信息。  

### 6. 评估检查结果  
- 将检查结果与以下内容进行对比：  
  - `STABLE-PRINCIPLES.md`中的安全不变量和常见陷阱  
  - （如果已加载）`CURRENT-CONTEXT.md`中的版本特定问题  
  - `ARCHITECTURE-MAP.md`中的架构耦合模式  

- 每个检查结果必须包括：  
  - **差异内容**（文件及代码片段）  
  **检查证据**（显示影响范围、依赖模块或匹配模式的命令输出）  
  - 该问题违反的具体原则、陷阱或模式的**参考链接**  

### 7. 生成报告  
- 不输出“批准/拒绝”的结论，而是输出问题的严重程度和警报分数以及最终得分。  

## 严重程度和警报评分  

使用以下等级对问题进行评分：  

- 🟢 **低风险**  
  - 仅是风格上的小问题或信息性提示，没有功能或安全方面的问题。可以直接发布。  
  - 警报分数范围：**1-2**  

- 🟡 **需要关注**  
  - 存在部分不匹配、模糊性、安全措施缺失或非关键性的不一致性。  
  - 值得审查，但不太可能导致故障。  
  - 警报分数范围：**3-6**  

- 🔴 **高风险**  
  - 明显违反编码指南或代码库模式，可能导致错误、回归、维护性问题或政策违规。  
  - 警报分数范围：**7-10**  

**评分规则**：  
- 单个问题的得分范围为1-10分。  
- 评分说明要简洁明了。  
- 最终得分应为：`final_alert_score = max(per_finding_scores)`  
- 如果没有发现任何问题，`final_alert_score = 0`。  

## 报告格式  

使用以下格式生成报告：  

```markdown
## pr-ship report

- Branch: `<current-branch>`
- Base: `<main-or-default-base>`
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
   - Reference: `<principle, gotcha, or pattern>`
   - Evidence in diff: `<file + short snippet/description>`
   - Exploration evidence: `<what dynamic investigation revealed>`
   - Why this matters: `<1-2 lines>`
   - Suggested fix: `<1-2 concrete actions>`

(repeat)

### Executive summary
- `<short practical summary for decision>`
- `<top 1-3 actions before publishing PR>`
```  

## 命令提示  

- 使用标准的git命令来收集证据：  
```bash
# current branch
git branch --show-current

# verify main exists
git show-ref --verify --quiet refs/heads/main

# fallback base branch from origin/HEAD (if needed)
git symbolic-ref refs/remotes/origin/HEAD

# changed files
git diff --name-only <base>...HEAD

# full diff
git diff <base>...HEAD
```  

- 关于动态检查命令，请参考`EXPLORATION-PLAYBOOK.md`。  

## 限制条件  
- 仅检查当前分支与基分支之间的差异。  
- 不要查看仓库的历史记录。  
- 除非明确要求，否则不要自动修改代码。  
- 除非特别请求，否则不要将报告转换为批准/拒绝的格式。  
- 必须始终运行检查命令来验证假设；切勿在未经验证的情况下直接判断模块的风险等级。  

## 致谢  

本技能的原始格式和设计源自[mudrii](https://github.com/mudrii)的开发者参考方法论。动态检查机制是根据OpenClaw维护者社区的反馈进行设计的。