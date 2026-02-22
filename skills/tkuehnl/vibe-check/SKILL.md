---
name: vibe-check
version: 0.1.1
description: >
  **审计代码中的“问题模式”——用于识别未经适当审查就被接受的AI生成代码**  
  该工具能够检测出表明代码由AI生成且存在问题的模式，并生成一份包含评分结果及修复建议的报告。
author: Anvil AI
tags: [code-quality, code-review, ai-audit, vibe-coding, linting, security, python, typescript, javascript, discord, discord-v2]
---
# 🎭 代码质量检查

本工具用于审核代码中是否存在“vibe coding”（即未经适当人工审核的、由AI生成的代码）。它会生成一份包含具体问题及修复建议的评分报告。

## 触发条件

当用户提及以下关键词时，工具将被激活：
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

询问用户需要分析的代码文件或目录：
- **单个文件：** `app.py`、`src/utils.ts`
- **目录：** `src/`、`.`、`my-project/`
- **Git差异：** 最近的N次提交、暂存中的更改或分支对比

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

分析结果将以Markdown格式呈现。该报告设计得非常适合截图展示。

### 在Discord中的使用方式（OpenClaw v2026.2.14及以上版本）

当对话在Discord频道中进行时：
- 首先发送一份简洁的摘要（评分、文件数量、主要问题），然后询问用户是否需要查看完整报告。
- 确保第一条消息长度不超过1200个字符，并避免在回复中使用过长的Markdown表格。
- 如果Discord支持相关功能，可以提供以下快捷操作：
  - `Show Top Findings`（显示主要问题）
  - `Show Fix Suggestions`（显示修复建议）
  - `Run Diff Mode`（运行差异对比模式）
- 如果Discord不支持这些功能，可以用编号列表的形式提供相同的信息。
- 在发送完整报告时，每条消息的长度应尽量控制在15行以内。

### 快速参考

| 命令 | 功能 |
|---------|-------------|
| `vibe-check FILE` | 分析单个文件 |
| `vibe-check DIR` | 递归扫描目录 |
| `vibe-check --diff` | 检查最近一次提交的更改 |
| `vibe-check --diff HEAD~5` | 检查最近5次提交的更改 |
| `vibe-check --staged` | 检查暂存中的更改 |
| `vibe-check --fix DIR` | 提供修复建议 |
| `vibe-check --output report.md DIR` | 将报告保存到指定文件 |

### 检查内容

| 检查类别 | 权重 | 检查内容 |
|---------|------:|-----------------|
| 错误处理 | 20% | 缺少try/catch语句、直接抛出异常、未处理边界情况 |
| 输入验证 | 15% | 未进行类型检查、未进行范围检查、盲目信任所有输入 |
| 代码重复 | 15% | 代码重复、违反DRY（Don't Repeat Yourself）原则 |
| 无用代码 | 10% | 未使用的导入语句、被注释掉的代码块、无法执行的代码 |
| 硬编码值 | 10% | 未使用常量的硬编码字符串/数字/URL |
| 测试覆盖率 | 10% | 无测试文件、无测试用例、无断言 |
| 命名规范 | 10% | 名称不明确（如data、result、temp等）或容易引起误解的命名 |
| 安全性 | 10% | 使用eval()、exec()函数、硬编码敏感信息、SQL注入风险 |

### 评分标准

- **A（90-100分）：** 代码质量极佳，几乎没有问题 |
- **B（80-89分）：** 代码较为干净，但存在一些小问题 |
- **C（70-79分）：** 代码尚可，但存在一些不良编程习惯 |
- **D（60-69分）：** 需要人工进一步处理 |
- **F（<60分）：** 显著存在“vibe coding”问题 |

### 对机器人的提示

- **报告非常重要**：请完整地展示报告内容，因为它的外观设计非常美观。
- 在展示报告后，如果用户尚未请求，可以建议他们使用`--fix`选项来修复问题。
- 建议用户添加`![Vibe Score](https://img.shields.io/badge/vibe--score-XX%2F100-COLOR)`徽章到他们的GitHub仓库中。
- 对于大型代码库，建议用户重点检查特定目录或使用`--diff`模式。
- 如果用户未设置LLM API密钥，工具将使用启发式分析方法（虽然准确性较低，但仍有一定参考价值）。
- **支持的语言（v1）：** 仅支持Python、TypeScript和JavaScript。

## 参考文件

- `scripts/vibe-check.sh` — 主执行脚本
- `scripts/analyze.sh` — 代码分析引擎（包含启发式分析功能）
- `scripts/git-diff.sh` — 用于提取Git差异的脚本
- `scripts/report.sh` — 用于生成Markdown报告的脚本
- `scripts/common.sh` — 公共工具和配置文件

## 示例

### 示例1：审核整个目录

**用户：** “检查我的src目录的代码质量”

**机器人执行：**
```bash
bash "$SKILL_DIR/scripts/vibe-check.sh" src/
```

**输出：** 包含每个文件的详细评分和问题清单的完整报告。

### 示例2：检查代码并提出修复建议

**用户：** “检查这段代码是否存在‘vibe coding’问题，并提供修复建议”

**机器人执行：**
```bash
bash "$SKILL_DIR/scripts/vibe-check.sh" --fix src/
```

**输出：** 包含评分报告以及每个问题的具体修复建议和差异对比结果。

### 示例3：查看Git差异

**用户：** “检查我最近3次提交的代码质量”

**机器人执行：**
```bash
bash "$SKILL_DIR/scripts/vibe-check.sh" --diff HEAD~3
```

**输出：** 仅针对最近更改的文件生成的评分报告。