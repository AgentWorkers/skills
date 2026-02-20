---
name: pr-reviewer
version: 1.0.1
description: >
  **自动化GitHub PR代码审查工具：支持差异分析、代码质量检查（lint）以及结构化报告生成**  
  该工具适用于在审查Pull Request时，检测潜在的安全问题、错误处理机制的缺陷、代码覆盖率不足的情况，以及代码风格上的问题。支持Go、Python和JavaScript/TypeScript语言。  
  **使用要求：**  
  需要使用`gh` CLI工具进行身份验证，并具备对相关仓库的访问权限。
metadata:
  openclaw:
    requires:
      bins: ["gh", "python3"]
      anyBins: ["golangci-lint", "ruff"]
---
# PR Reviewer

这是一个用于自动审查 GitHub 提交请求（pull requests）的工具。它能够分析代码差异，检测安全问题、错误处理漏洞、代码风格问题以及测试覆盖率。

## 前提条件

- 已安装并登录 `gh` CLI（使用 `gh auth status` 命令验证身份）
- 具有仓库访问权限（至少需要读取权限，提交评论时需要写入权限）
- 可选工具：`golangci-lint` 用于 Go 语言的代码检查；`ruff` 用于 Python 语言的代码检查

## 快速开始

```bash
# Review all open PRs in current repo
scripts/github/pr-reviewer.sh check

# Review a specific PR
scripts/github/pr-reviewer.sh review 42

# Post review as GitHub comment
scripts/github/pr-reviewer.sh post 42

# Check status of all open PRs
scripts/github/pr-reviewer.sh status

# List unreviewed PRs (useful for heartbeat/cron integration)
scripts/github/pr-reviewer.sh list-unreviewed
```

## 配置

请设置以下环境变量，或者让脚本从当前的 Git 仓库中自动检测这些配置：

- `PR_REVIEW_REPO` — GitHub 仓库的路径，格式为 `owner/repo`（默认值：通过 `gh repo view` 命令获取）
- `PR_REVIEW_DIR` — 用于代码检查的本地目录路径（默认值：当前工作目录的根目录）
- `PR_REVIEW_STATE` — 用于存储审查状态的文件路径（默认值：`./data/pr-reviews.json`）
- `PR_REVIEW_OUTDIR` — 用于保存审查报告的目录路径（默认值：`./data/pr-reviews/`）

## 相关目录

- **`PR_REVIEW_STATE`**（默认值：`./data/pr-reviews.json`）—— 记录被审查的 Pull Request 及其对应的 HEAD SHA 值
- **`PR_REVIEW_OUTDIR`**（默认值：`./data/pr-reviews/`）—— 存储 Markdown 格式的审查报告

## 检查内容

| 类别 | 图标 | 例子 |
|----------|------|----------|
| 安全性 | 🔴 | 代码中硬编码的凭据、AWS 密钥等敏感信息 |
| 错误处理 | 🟡 | 被忽略的错误处理语句（如 Go 语言中的 `_ :=`）、简单的 `except:` 语句、未检查的 `Close()` 调用 |
| 风险 | 🟠 | 引发程序崩溃的 `panic()` 调用、`process.exit()` 函数 |
| 代码风格 | 🔵 | 在生产环境中使用 `fmt.Print`/`print()`/`console.log`，代码行过长 |
| 待办事项 | 📝 | 使用 `TODO`、`FIXME`、`HACK` 等标记的代码 |
| 测试覆盖率 | 📊 | 源代码发生变化但相应的测试代码未更新 |

## 智能重审机制

该工具会跟踪每个 Pull Request 的 HEAD SHA 值，仅在有新的提交时才重新进行审查。可以使用 `review <PR#>` 命令强制重新审查。

## 报告格式

审查报告以 Markdown 格式保存在指定的输出目录中。每份报告包含以下内容：

- Pull Request 的元信息（作者、分支、修改内容）
- 提交记录
- 按语言/类型分类的修改文件列表
- 自动检测到的代码差异（包括文件名、行号、问题类别及上下文）
- 测试覆盖率分析结果
- 当仓库在本地被检出时的代码检查结果
- 总体审查结果：🔴 安全问题严重 / 🟡 需要关注 / 🔵 仅是风格问题 / ✅ 代码通过审查

## 集成到定期检查流程中

可以将该工具集成到定期的检查流程中（例如心跳检测、Cron 作业或持续集成（CI）系统中）：

```bash
UNREVIEWED=$(scripts/github/pr-reviewer.sh list-unreviewed)
if [ -n "$UNREVIEWED" ]; then
  scripts/github/pr-reviewer.sh check
fi
```

## 扩展功能

脚本中的代码检查规则是按语言分类的。可以通过在 `analyze_diff()` 函数中添加新的规则来扩展检查功能：

```python
# Add a new Go pattern
go_patterns.append((r'^\+.*os\.Exit\(', 'RISK', 'Direct os.Exit() — consider returning error'))
```