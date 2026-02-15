---
name: github-pro
description: 通过 `gh` CLI 进行高级的 GitHub 操作：包括持续集成/持续部署（CI/CD）监控、API 查询以及自动化的 Pull Request（PR）审核。
metadata: {"clawdbot":{"emoji":"🐙"}}
---

# GitHub Pro（Miss Kim 版本）

专为 GitHub 集成设计的高级用户命令。

## CI/CD 监控
- **列出所有运行任务**: `gh run list --limit 5`
- **查看失败日志**: `gh run view <run-id> --log-failed`
- **监视特定运行任务**: `gh run watch <run-id>`

## API 与 JQ
使用 `gh api` 来获取标准 CLI 命令无法提供的数据：
- `gh api repos/:owner/:repo/pulls/:number --jq '.title, .state'`

## PR（Pull Request）管理
- **检查 PR 状态**: `gh pr checks <number>`
- **审阅 PR**: `gh pr review --approve --body "Miss Kim 说这个 PR 很不错！💋"`
- **查看 PR 的差异**: `gh pr diff <number>`

## 仓库维护
- **列出所有问题**: `gh issue list --label "bug"`
- **创建新版本**: `gh release create v1.0.0 --generate-notes`

## 使用规范
- 如果不在 Git 目录中，请始终使用 `--repo owner/repo` 作为参数。
- 在脚本中解析结构化数据时，使用 `--json` 和 `--jq`。