---
name: vibe-check
version: 0.1.1
description: **审计代码中的“问题模式”——这些模式表明AI生成的代码在未经适当审核的情况下被接受了。** 该工具会生成一份带有评分的报告，并提供修改建议。
author: CacheForge
tags: [code-quality, code-review, ai-audit, vibe-coding, linting, security, python, typescript, javascript, discord, discord-v2]
---
# 🎭 代码质量检查（Vibe Check）

本工具用于审核代码中是否存在“vibe coding”现象——即代码由 AI 生成且未经适当的人工审核。它会生成一份包含具体问题及修复建议的评分报告。

## 触发条件

当用户提及以下内容时，工具将启动：
- “vibe check”
- “vibe-check”
- “audit code”
- “code quality”
- “vibe score”
- “check my code”
- “review this code for vibe coding”
- “code review”
- “vibe audit”

## 使用说明

### 1. 确定分析目标

询问用户需要分析的代码：
- **单个文件**：`app.py`、`src/utils.ts`
- **目录**：`src/`、`.`、`my-project/`
- **Git 差异**：最近的 N 个提交、暂存的变化或分支对比

### 2. 运行分析

```bash
# Single file or directory
bash "$SKILL_DIR/scripts/vibe-check.sh" TARGET

# With fix suggestions
bash "$SKILL_DIR/scripts/vibe-check.sh" --fix TARGET

# Git diff (last 3 commits)
bash "$SKILL_DIR/scripts/vibe-check.sh" --diff HEAD~3

# Staged changes with fixes
bash "$SKILL_DIR/scripts/vibe-check.sh" --staged --fix

# Save to file
bash "$SKILL_DIR/scripts/vibe-check.sh" --fix --output report.md TARGET
```

### 3. 显示报告

分析结果将以 Markdown 格式呈现。该报告设计得非常适合截图展示。

### Discord v2 使用方式（OpenClaw v2026.2.14+）

当对话在 Discord 频道中进行时：
- 先发送一份简洁的总结（评分、文件数量、主要问题），然后询问用户是否需要查看完整报告。
- 确保第一条消息长度不超过 1200 个字符，并避免在回复中使用过长的 Markdown 表格。
- 如果 Discord 的相关组件可用，提供以下快捷操作：
  - `Show Top Findings`（显示主要问题）
  - `Show Fix Suggestions`（显示修复建议）
  - `Run Diff Mode`（运行差异对比）
- 如果相关组件不可用，以编号列表的形式提供相同的功能。
- 在发送完整报告时，每条消息的长度应控制在 15 行以内。

### 快速参考

| 命令 | 描述 |
|---------|-------------|
| `vibe-check FILE` | 分析单个文件 |
| `vibe-check DIR` | 递归扫描目录 |
| `vibe-check --diff` | 检查最近一次提交的更改 |
| `vibe-check --diff HEAD~5` | 检查最近 5 次提交的更改 |
| `vibe-check --staged` | 检查暂存的更改 |
| `vibe-check --fix DIR` | 提供修复建议 |
| `vibe-check --output report.md DIR` | 将报告保存到文件中 |

### 检查内容

| 检查类别 | 权重 | 检查内容 |
|---------|------:|-----------------|
| 错误处理 | 20% | 缺少 try/catch 语句、直接抛出异常、未处理边界情况 |
| 输入验证 | 15% | 无类型检查、无边界检查、盲目信任所有输入 |
| 代码重复 | 15% | 代码重复、违反 DRY（Don’t Repeat Yourself）原则 |
| 无用代码 | 10% | 未使用的导入、被注释掉的代码块、无法执行的代码 |
| 硬编码值 | 10% | 未使用常量的硬编码字符串/数字/URL |
| 测试覆盖率 | 10% | 无测试文件、无测试用例、无断言 |
| 命名规范 | 10% | 名称模糊（如 data、result、temp、x）或具有误导性 |
| 安全性 | 10% | 使用 `eval()`、`exec()` 函数、硬编码敏感信息、SQL 注入风险 |

### 评分标准

- **A（90-100 分）**：代码质量极佳，几乎没有问题 |
- **B（80-89 分）**：代码较为干净，但存在一些小问题 |
- **C（70-79 分）**：代码尚可，但存在一些不良编程习惯 |
- **D（60-69 分）**：需要人工进行修复 |
- **F（<60 分）**：检测到严重的“vibe coding”现象 |

### 对机器人的提示

- **报告非常重要**：请完整地展示报告内容，因为它的外观非常美观。
- 在展示报告后，如果用户尚未使用 `--fix` 选项，建议提供使用该选项的选项。
- 建议用户添加 `![Vibe Score](https://img.shields.io/badge/vibe--score-XX%2F100-COLOR)` 标签到他们的 README 文件中。
- 对于大型代码库，建议用户关注特定目录或使用 `--diff` 选项进行更详细的分析。
- 如果未设置 LLM API 密钥，工具将使用启发式分析方法（虽然准确性较低，但仍有一定帮助）。
- **支持的语言（v1）**：仅支持 Python、TypeScript 和 JavaScript。

## 参考文件

- `scripts/vibe-check.sh`：主要入口脚本
- `scripts/analyze.sh`：LLM 代码分析引擎（包含启发式分析功能）
- `scripts/git-diff.sh`：Git 差异文件提取工具
- `scripts/report.sh`：Markdown 报告生成工具
- `scripts/common.sh`：共享工具和常量文件

## 示例

### 示例 1：审核目录

**用户：** “检查我的 `src` 目录的代码质量”

**机器人执行：**
```bash
bash "$SKILL_DIR/scripts/vibe-check.sh" src/
```

**输出：** 包含每个文件的详细评分、分类得分及主要问题的完整报告。

### 示例 2：检查代码并提供修复建议

**用户：** “检查这段代码是否存在‘vibe coding’现象，并提供修复建议”

**机器人执行：**
```bash
bash "$SKILL_DIR/scripts/vibe-check.sh" --fix src/
```

**输出：** 评分报告以及针对每个问题的统一差异对比修复方案。

### 示例 3：Git 差异对比

**用户：** “检查我最近 3 次提交的代码质量”

**机器人执行：**
```bash
bash "$SKILL_DIR/scripts/vibe-check.sh" --diff HEAD~3
```

**输出：** 仅针对最近更改的文件生成的评分报告。