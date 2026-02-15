---
name: pr-review
description: 在提交 Pull Request (PR) 之前，先找到并修复代码中的问题。系统会启动 5 个并行分析代理，分别检查代码是否存在漏洞、安全隐患、性能问题、是否符合开发规范以及代码质量。对于那些置信度较高的问题，系统会直接在您的代码中进行自动修复。此外，该工具还支持按路径对现有代码进行审计。需要 Git 环境才能使用。
metadata: {"openclaw": {"requires": {"bins": ["git"]}}}
---

# 预审

在提交 Pull Request (PR) 之前，务必找到并修复问题——而不是之后。

传统的审阅工具会在 PR 发布后添加评论，从而导致“先修复再更新”的循环。而预审机制则相反：先在本地进行分析，直接修复问题，然后再提交干净的代码。

## 使用方法

```
/pr-review                    # Review changes on current branch vs main/master
/pr-review src/api/ src/auth/ # Audit specific directories
/pr-review **/*.ts            # Audit files matching a pattern
/pr-review --audit            # Audit entire codebase with smart prioritization
```

有两种模式，只需一个命令即可切换：

| 模式 | 触发条件 | 审查范围 | 问题修复的最低分数 | 适用场景 |
|------|---------|-------|---------------|----------|
| **差异对比 (Diff)** | 无参数，针对有变更的分支 | 仅检查变更的文件 | 分数 >= 70 | 在提交 PR 之前使用 |
| **安全审计 (Audit)** | 提供文件路径或模式，或使用 `--audit` 选项 | 指定文件或整个代码库 | 分数 >= 80（较为严格） | 适用于安全审查或代码库健康状况检查 |

## 操作步骤

请严格按照以下步骤执行：

### 第一步：确定模式和审查范围

创建一个待办列表，以跟踪整个流程的进度。

**无参数时：**
- 运行 `git diff main...HEAD --name-only`（如果 `main` 不存在，请使用 `master`）
- 如果有变更：进入 **差异对比模式**——仅审查分支中的变更
- 如果没有变更：通知用户“未发现变更。请使用 `/pr-review <路径>` 对现有代码进行安全审计”，然后停止操作

**提供文件路径或模式时：**
- 确定具体的文件范围
- 如果文件数量超过 50 个，请让用户缩小审查范围或确认是否继续进行 **安全审计模式**

**使用 `--audit` 选项时：**
- 确定源代码目录（如 `src/`、`lib/`、`app/` 等）
- 排除以下文件：`node_modules`、`dist`、`build`、`vendor`、`.git`、`coverage` 文件
- 向用户提出审查范围，等待确认

### 第二步：获取项目规范（使用 Haiku Agent）

启动 Haiku Agent（Task 工具，模型：haiku），以获取以下信息：
- 根目录下的 `CLAUDE.md` 文件以及相关目录中的其他规范文件
- `.eslintrc`、`.prettierrc`、`tsconfig.json`、`biome.json` 等代码风格配置文件
- `CONTRIBUTING.md` 文件及代码风格指南
- `package.json` 文件（了解项目的技术栈）

返回项目规范和技术栈的摘要。

### 第三步：构建审查环境

**差异对比模式：** 启动 Haiku Agent，执行以下操作：
- 运行 `git diff main...HEAD`（获取完整代码差异）
- 返回结构化的摘要：哪些文件发生了变更，变更的性质，以及新增或删除的行号

**安全审计模式：** 启动 Haiku Agent，根据文件的风险等级对文件进行分类：

| 优先级 | 问题示例 |
|----------|---------|
| **高** | 用户认证、支付处理、数据库查询、API 端点、输入验证、文件处理逻辑、加密相关代码 |
| **中** | 业务逻辑、服务相关代码、辅助工具、状态管理代码 |
| **低** | 测试代码（除非特别要求）、配置文件、类型与接口相关代码、常量定义 |

返回按优先级排序的文件列表。审查重点应放在高优先级和中优先级的文件上。

### 第四步：并行进行深度分析（使用 5 个 Sonnet Agent）

同时启动 **5 个 Sonnet Agent**（Task 工具，模型：sonnet，子代理类型：通用类型）。

每个 Agent 都会接收以下信息：
- 第二步中的项目规范摘要
- 第三步中的代码环境信息
- 以及将问题以结构化列表的形式返回的指令，包括文件路径、行号、问题严重程度（严重/重要/轻微）、问题类别、修复建议以及问题的可信度评分（0-100 分）。

#### 差异对比模式下的 Agent 分工：

**Agent #1 — 规范合规性检查：**
- 根据项目规范（如 `CLAUDE.md`、`eslint`、`prettierrc` 等工具）检查代码变更：
  - 命名规范
  - 必需或禁止的代码模式
  - 文档编写要求
  - 项目特有的反模式（不良编程习惯）

**Agent #2 — 错误检测：**
- 检查代码中是否存在实际漏洞（而非仅仅关注代码风格问题）：
  - 逻辑错误、数值计算错误
  - `null`/`undefined` 变量的处理方式
  - 竞态条件、资源泄漏问题
  - 错误处理机制的缺陷
  - `async/await` 语句的使用错误

**Agent #3 — Git 历史记录与代码回归检查：**
- 查看被修改文件的 Git 提交记录（`git blame`）。当发现代码回归或问题时，将这些问题作为缺陷报告：
  - 重新引入之前已修复的漏洞
  - 对稳定代码的破坏性修改
  - 之前提交中已建立的代码模式被破坏
  - 与最近提交历史中的代码逻辑矛盾的变更

**Agent #4 — 安全性与性能评估：**
- 检查是否存在注入漏洞（如 SQL 注入、XSS、命令注入、路径遍历）
- 是否存在泄露敏感信息、认证漏洞、不安全的操作
- 是否存在 N+1 查询、不必要的循环、内存泄漏、API 的不当使用

**Agent #5 — 代码质量与测试评估：**
- 新功能对应的测试是否缺失或不足
- 是否引入了无用的代码
- 是否存在重复的代码逻辑
- 错误处理机制是否不一致
- 由于代码变更导致注释变得过时或不再适用

#### 安全审计模式下的 Agent 分工：

**Agent #1 — 安全性深度扫描：**
- 对目标文件进行全面的安全部门扫描：
  - SQL/NoSQL 注入、XSS、命令注入、路径遍历漏洞
- 硬编码的敏感信息或密码、弱加密算法
- 认证绕过漏洞、授权缺陷、跨站请求伪造（SSRF）问题
- 不安全的序列化操作

**Agent #2 — 错误检测：**
- 检查代码中的错误和逻辑问题：
  - `null`/`undefined` 变量的处理方式、数值计算错误
- 竞态条件、资源泄漏（内存、文件句柄、连接操作）
- 无限循环、无法执行的代码路径
- 类型强制转换问题、`async/await` 语句的使用错误

**Agent #3 — 数据流分析：**
- 跟踪数据在应用程序中的流动：
  - 未经过验证的用户输入是否直接影响了敏感操作
- 数据泄露（如日志中泄露了用户隐私信息）
- 输入边界处的处理不当
- 信任边界被违反的情况

**Agent #4 — 性能与资源优化：**
- 是否存在 N+1 查询模式、缺乏分页功能
- 对用户控制的数据进行无限制的循环操作
- 在异步上下文中存在内存累积问题
- 算法效率低下（本应使用 O(n) 的情况下使用了 O(n^2) 的算法）
- 对重复的高耗时操作缺乏缓存机制

**Agent #5 — 代码质量与可维护性评估：**
- 函数长度超过 50 行，嵌套层次超过 4 层
- 循环复杂度过高
- 文件间存在重复的代码逻辑
- 代码风格不一致或使用了过时的编程习惯
- 未完成的代码任务（如标记为 TODO 或 FIXME）

### 第五步：去重与问题评分（使用 Haiku Agent）

启动 Haiku Agent 处理第四步中的所有结果：

1. **去重**：删除多个 Agent 发现的相同问题（同一文件和相同行范围内的问题只计为一个问题）
2. **合并**：将具有相同根本原因的问题合并在一起
3. **重新评分**：根据完整的代码环境重新评估问题的可信度：

| 评分 | 含义 |
|-------|---------|
| 90-100 | 严重漏洞或问题，有明确的证据，必须立即修复 |
| 70-89 | 可能会导致问题的问题，需要修复 |
| 50-69 | 代码存在问题或潜在风险，需要人工判断 |
| < 50 | 问题较轻微，属于风格上的问题，或可能是误报 |

**评分阈值：**
- **差异对比模式**：评分低于 70 的问题可以忽略（因为这些问题是你自己引入的，且代码环境是新鲜的）
- **安全审计模式**：评分低于 50 的问题也需要报告，但修复时需更加谨慎

### 第六步：自动修复

对于评分达到最低阈值的问题，直接在代码中进行修复：
- **差异对比模式**：修复评分 >= 70 的问题
- **安全审计模式**：修复评分 >= 80 的问题

对于每个需要修复的问题：
1. 阅读包含该问题的文件
2. 使用编辑工具进行修复
3. 确保修复后的代码不会影响周围的代码结构和功能

将修复操作按文件进行分组，以减少修改次数。

**切勿自动修复的情况：**
- 需要架构调整的问题
- 修复方案存在多种可能性的问题
- 位于测试文件中的问题（仅报告问题）
- 评分低于相应模式阈值的问题

### 第七步：生成报告并展示给用户

**差异对比模式：**

```
## Pre-Review Complete

### Issues Found and Fixed: X

1. **file:line** - Description
   - Severity: critical/important/minor | Confidence: XX
   - Category: security/bug/performance/quality/guidelines
   - Fix applied: What was changed

### Manual Review Required: Y
(Issues with confidence >= 70 that could not be auto-fixed: requires architectural change, ambiguous fix, or in test file)

1. **file:line** - Description (confidence: XX)
   - Reason: Why it needs manual review
   - Suggested approach: Description

### Files Modified: Z
- path/to/file1.ts
- path/to/file2.ts

### Recommendations
- Tests to run
- Areas needing human judgment
```

**安全审计模式：**

```
## Code Audit Report

### Summary
- Files Audited: X | Issues Found: Y | Fixed: Z | Manual Review: W

### Critical Issues (Fixed)
1. **file:line** - Description
   - Category: security/bug/performance
   - Fix applied: What was changed

### Critical Issues (Manual Review Required)
(Confidence >= 80 but requires architectural change, ambiguous fix, or in test file)
1. **file:line** - Description
   - Reason: Why it was not auto-fixed
   - Recommended: Suggested approach

### Important Issues (Confidence 50-79)
1. **file:line** - Description (confidence: XX)

### Security Summary
- Hardcoded credentials: none found (or: X instances found)
- Injection risks: none found (or: X potential risks)
- XSS vulnerabilities: none found (or: X potential)
- Input validation: adequate (or: X gaps found)

### Files Modified
- path/to/file1.ts

### Recommendations
- Priority items for manual review
- Tests to add
```

### 第八步：后续操作

向用户提供以下建议：
- “运行测试以验证修复效果吗？”
- “使用 `git diff` 查看修复后的代码变化吗？”
- “提交修复后的代码吗？”
- （仅限安全审计模式）“是否需要进一步审计其他目录？”

## 规范说明

**应该做：**
- 直接在代码中修复问题，而不仅仅是报告问题
- 保持代码的原有逻辑和风格规范
- 将相关问题按文件分组，以减少修改次数
- 在不确定的情况下，优先报告问题而非直接修复

**不应该做：**
- 用不确定的修复方法破坏现有的代码功能
- 在差异对比模式下，只修复实际发生变更的部分
- 除非项目有明确要求，否则不要仅仅为了调整代码风格而进行修改
- 不要重构没有实际问题的代码
- 不要审计 `node_modules`、第三方库、生成的代码文件或构建过程中的文件

## 需避免的误报情况：
- 问题并非由当前变更引起（差异对比模式）
- 由代码检查工具（如 linters 或类型检查器）能够发现的错误
- 高级工程师在正式审阅中可能不会关注的小问题
- 虽然看起来不寻常但实际是正确的代码模式
- 位于当前变更范围之外的代码问题（差异对比模式）
- 仅基于个人主观判断的代码质量问题（这些问题并非由当前变更引起）