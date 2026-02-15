---
name: github-pr
description: 在本地获取、预览、合并并测试 GitHub 的 Pull Request（PR）。这非常适合在上游 PR 被合并之前先进行测试。
homepage: https://cli.github.com
metadata:
  clawdhub:
    emoji: "🔀"
    requires:
      bins: ["gh", "git"]
---

# GitHub PR 工具

该工具用于从 GitHub 获取 Pull Request 并将其合并到本地分支中。非常适合以下场景：
- 在上游 Pull Request 被合并之前进行测试
- 将开源 Pull Request 中的功能整合到你的分支中
- 在本地测试 Pull Request 的兼容性

## 先决条件

- 已通过 `gh auth login` 命令认证 `gh` CLI
- 你的 Git 仓库已配置远程仓库（remotes）

## 命令

### 预览 Pull Request
```bash
github-pr preview <owner/repo> <pr-number>
```
显示 Pull Request 的标题、作者、状态、更改的文件、持续集成（CI）状态以及最近的评论。

### 将 Pull Request 的分支克隆到本地
```bash
github-pr fetch <owner/repo> <pr-number> [--branch <name>]
```
将 Pull Request 的分支克隆到本地分支（默认分支为 `pr/<number>`）。

### 将 Pull Request 合并到当前分支
```bash
github-pr merge <owner/repo> <pr-number> [--no-install]
```
获取 Pull Request 的内容并将其合并到当前分支。合并后可以选择运行安装命令。

### 完整的测试流程
```bash
github-pr test <owner/repo> <pr-number>
```
获取 Pull Request 的内容，将其合并到当前分支，安装依赖项，然后运行构建和测试。

## 示例
```bash
# Preview MS Teams PR from clawdbot
github-pr preview clawdbot/clawdbot 404

# Fetch it locally
github-pr fetch clawdbot/clawdbot 404

# Merge into your current branch
github-pr merge clawdbot/clawdbot 404

# Or do the full test cycle
github-pr test clawdbot/clawdbot 404
```

## 注意事项

- Pull Request 默认从 `upstream` 远程仓库获取
- 可使用 `--remote <name>` 参数指定其他远程仓库
- 合并冲突必须手动解决
- `test` 命令会自动检测所使用的包管理器（npm/pnpm/yarn/bun）