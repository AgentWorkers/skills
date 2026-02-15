---
name: pr-reviewer
description: **自动化GitHub PR代码审查工具：支持差异分析、代码风格检查（lint）以及结构化报告生成**  
该工具用于在审查Pull请求时，检测潜在的安全问题、错误处理漏洞、代码覆盖率不足的情况以及代码风格问题。支持Go、Python以及JavaScript/TypeScript语言。  
使用前提：需要通过`gh` CLI进行身份验证，并具备对仓库的访问权限。
---

# PR Reviewer

这是一个用于自动审查 GitHub 提交请求（pull requests）的工具。它会分析代码差异，以检测安全问题、错误处理漏洞、代码风格问题以及测试覆盖率。

## 先决条件

- 已安装并配置了 `gh` CLI（通过 `gh auth status` 命令验证身份）
- 具有仓库访问权限（至少具备读取权限，提交评论时需要写入权限）
- 可选：使用 `golangci-lint` 对 Go 代码进行代码检查，使用 `ruff` 对 Python 代码进行代码检查

## 快速入门

```bash
# Review all open PRs in current repo
scripts/pr-review.sh check

# Review a specific PR
scripts/pr-review.sh review 42

# Post review as GitHub comment
scripts/pr-review.sh post 42

# Check status of all open PRs
scripts/pr-review.sh status

# List unreviewed PRs (useful for heartbeat/cron integration)
scripts/pr-review.sh list-unreviewed
```

## 配置

请设置以下环境变量，或者让脚本从当前 Git 仓库中自动检测这些配置：

- `PR_REVIEW_REPO` — GitHub 仓库的路径，格式为 `owner/repo`（默认值：从 `gh repo view` 中获取）
- `PR_REVIEW_DIR` — 用于代码检查的本地目录路径（默认值：当前工作目录的根目录）
- `PR_REVIEW_STATE` — 用于存储审查状态信息的文件路径（默认值：`./data/pr-reviews.json`）
- `PR_REVIEW_OUTDIR` — 报告输出目录的路径（默认值：`./data/pr-reviews/`）

## 检查内容

| 类别 | 图标 | 例子 |
|----------|------|----------|
| 安全性 | 🔴 | 代码中硬编码的凭据、AWS 密钥等敏感信息 |
| 错误处理 | 🟡 | 被忽略的错误处理语句（如 Go 语言中的 `_ :=`）、简单的 `except:` 语句、未检查的 `Close()` 调用 |
| 风险 | 🟠 | 使用 `panic()` 或 `process.exit()` 导致程序异常终止 |
| 代码风格 | 🔵 | 在生产环境中使用 `fmt.Print`、`print()` 或 `console.log`；代码行过长 |
| 待办事项 | 📝 | 使用 `TODO`、`FIXME`、`HACK` 等标记的待办事项 |
| 测试覆盖率 | 📊 | 源代码发生变化但相应的测试代码没有更新 |

## 智能重审机制

该工具会跟踪每个 PR 的 HEAD SHA 值，仅在有新的提交时才重新进行代码审查。可以使用 `review <PR#>` 命令强制重新审查。

## 报告格式

报告以 Markdown 格式保存在输出目录中。每份报告包含以下内容：

- PR 的元数据（作者、分支、变更内容）
- 提交记录列表
- 按语言/类型分类的被修改文件
- 自动检测到的代码差异信息（包括文件名、行号、问题类别及上下文）
- 测试覆盖率分析结果
- 当本地检出仓库时，还会显示代码检查的结果
- 综合评估结果：🔴 安全问题严重 / 🟡 需要关注 / 🔵 仅是小问题 / ✅ 代码质量良好

## 集成到定期检查流程中

可以将该工具集成到周期性的检查任务中（例如心跳检测、定时任务或持续集成流程中）：

```bash
UNREVIEWED=$(scripts/pr-review.sh list-unreviewed)
if [ -n "$UNREVIEWED" ]; then
  scripts/pr-review.sh check
fi
```

## 扩展功能

该脚本中的代码检查规则是按语言分类的。如需添加新的检查规则，只需在 `analyze_diff()` 函数中相应的规则列表中添加新的规则即可：

```python
# Add a new Go pattern
go_patterns.append((r'^\+.*os\.Exit\(', 'RISK', 'Direct os.Exit() — consider returning error'))
```