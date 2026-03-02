---
name: pr-review
description: 在提交 Pull Request (PR) 之前，务必先查找并修复代码中的问题。使用该工具可以进行一次性代码审查，并自动修复存在的问题。适用于在提交代码更改之前进行审查，或对现有代码进行漏洞/安全性的审计。但请勿在通过编程工具编写代码时使用该工具（此时应使用专门的编程工具），也不适用于检查 GitHub 的持续集成 (CI) 状态（此时应使用 GitHub 的内置工具）。
metadata: {"openclaw": {"requires": {"bins": ["git"]}}}
---
# 预审

在提交 Pull Request (PR) 之前，务必找到并修复问题——而不是之后。

使用一个性能良好的模型进行一次性审查。无需额外的协调开销，也无需使用代理集群。速度快、成本低且全面。

## 使用场景
- 在提交 PR 之前审查代码变更
- 审查现有代码中的错误、安全问题或质量问题
- 在特定文件或目录中查找并修复问题

## 不适用场景
- 用于编写新代码（请使用 `coding-agent`）
- 检查 GitHub 的持续集成 (CI) 状态（请使用 `github`）
- 管理分支的合并或重基操作（请使用 `fork-manager`）

## 使用方法

```
/pr-review                    # Review changes on current branch vs main/master
/pr-review src/api/ src/auth/ # Audit specific directories
/pr-review **/*.ts            # Audit files matching a pattern
/pr-review --audit            # Audit entire codebase with smart prioritization
```

该工具提供两种模式：

| 模式 | 触发条件 | 审查范围 | 问题修复阈值 |
|------|---------|-------|---------------|
| **Diff** | 无参数，仅在有变更的分支上执行 | 仅审查变更的文件 | 问题得分 >= 70 分 |
| **Audit** | 提供路径、模式或使用 `--audit` 参数 | 指定文件或整个代码库 | 问题得分 >= 80 分 |

## 使用说明

### 第一步：确定模式和审查范围

**无参数时：**
```bash
git diff main...HEAD --name-only 2>/dev/null || git diff master...HEAD --name-only
```
- 如果存在代码变更 → 使用 **Diff 模式**
- 如果没有变更 → 通知用户并停止审查

**提供路径或模式时（或使用 `--audit` 参数）：**
- 确定需要审查的具体文件（排除 `node_modules`、`dist`、`build`、`vendor`、`.git` 和 `coverage` 文件夹）
- 如果涉及的文件超过 50 个，请用户缩小审查范围或确认审查范围 → 使用 **Audit 模式**

### 第二步：获取上下文信息

快速阅读项目规范：
```bash
# Check for project conventions
cat CLAUDE.md .claude/settings.json CONTRIBUTING.md 2>/dev/null | head -100
cat .eslintrc* .prettierrc* biome.json tsconfig.json 2>/dev/null | head -50
cat package.json 2>/dev/null | head -20  # tech stack
```

获取代码差异或文件内容：
```bash
# Diff mode
git diff main...HEAD  # or master

# Audit mode
cat <files>  # read target files
```

### 第三步：进行一次性审查

一次性分析所有代码，按优先级处理以下方面：

**1. 正确性**（最高优先级）
- 逻辑错误、边界情况处理、`null`/`undefined` 的处理
- 数字精度问题、异步/`await` 语句的错误、竞态条件、资源泄漏
- 数据一致性、幂等性问题

**2. 安全性**
- 注入漏洞（SQL 注入、XSS 攻击、命令注入、路径遍历漏洞）
- 认证/授权漏洞、IDOR 风险、敏感信息的泄露
- 未经验证的输入被用于敏感操作
- 敏感数据的日志记录、不安全的默认设置

**3. 可靠性**
- 错误处理机制的缺陷、无声的错误、被忽略的异常
- 缺少超时机制、没有重试机制的代码
- 对用户控制的数据进行无限制的操作

**4. 性能**  
- N+1 查询、不必要的循环、内存泄漏
- 分页功能缺失、算法效率低下
- 在异步环境中执行阻塞操作

**5. 质量**（最低优先级——如果问题不严重可忽略）  
- 新功能缺少测试代码  
- 无用的代码、重复的逻辑  
- 过时的注释、不清晰的命名  
- 仅当代码风格违反项目规范时才进行样式检查

### 第四步：评分和分类

对于每个发现的问题，进行如下分类：

| 问题得分 | 含义 | 处理方式 |
|-------|---------|--------|
| 90-100 | 严重的漏洞或安全问题 | 必须修复 |
| 70-89 | 真实存在的问题，可能导致问题 | 应该修复 |
| 50-69 | 代码质量不佳，需要人工判断 | 仅报告 |
| < 50 | 轻微问题，可能是误报 | 可忽略 |

**忽略的阈值：**
- **Diff 模式**：得分低于 50 分的问题 |
- **Audit 模式**：得分低于 40 分的问题

**问题分类：**
- `blocker`：严重问题（如安全漏洞、数据损坏、可能导致系统崩溃的问题）  
- `important`：可能存在问题的代码、性能下降、验证缺失的问题  
- `minor`：边缘情况、可维护性问题、代码风格问题

### 第五步：自动修复

对于符合修复阈值的问题，直接进行修复：
- **Diff 模式**：修复得分 >= 70 分的问题  
- **Audit 模式**：修复得分 >= 80 分的问题  

对于每个修复操作，需先阅读相关文件，然后进行修改，并确保修改后的代码仍然符合项目规范。

**严禁自动修复的情况：**
- 需要架构调整的问题  
- 有多种正确修复方式的模糊问题  
- 测试文件中的问题（仅报告问题）

修复完成后，如果文件内容发生了变化：
```bash
git diff --stat  # show what changed
```

### 第六步：生成报告

**报告格式：**
```
## Pre-Review Complete

**Risk:** Low / Medium / High
**Verdict:** ✅ Clean | ⚠️ Issues found | 🔴 Blockers

### 🔴 Blockers (must fix)
1. **file:line** — Description
   - Impact: what goes wrong
   - Fix: applied ✅ | manual required (reason)

### ⚠️ Important (should fix)
1. **file:line** — Description (score: XX)
   - Fix: applied ✅ | suggestion

### 💡 Minor
1. **file:line** — Description

### Tests to Add
- description of test

### Files Modified: N
- path/to/file.ts
```

如果未发现任何问题：`## 预审完成 — ✅ 代码无问题。`

## 使用指南

**建议：**
- 直接修复问题，而不仅仅是报告问题  
- 修复后的代码应符合现有的代码风格和规范  
- 详细说明问题所在的位置（文件、行号以及具体的修复方法）  
- 优先考虑问题的影响程度，而非审查的全面性  

**禁止的行为：**
- 在 **Diff 模式** 下修复已存在的问题——仅修复实际发生变更的部分  
- 除非代码风格违反项目规范，否则不要过度修改代码风格  
- 无需报告代码检查工具或类型检查工具能够检测到的问题（假设这些问题已由持续集成系统处理）  
- 不要进行架构调整或大规模的代码重构  
- 不要将资源浪费在显而易见但无关紧要的问题上  

## 需避免的误报情况：
- 当前变更未影响到现有代码的情况（**Diff 模式**）  
- 虽然看起来不常见但实际正确的代码模式  
- 代码检查工具或类型检查工具会标记的问题  
- 仅基于个人主观判断的代码风格问题  
- 高级工程师可能会忽略的细节性问题