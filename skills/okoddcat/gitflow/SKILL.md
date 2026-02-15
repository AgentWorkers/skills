---
name: gitflow
description: 在新代码被推送到 GitHub 或 GitLab 时，能够自动监控 CI/CD 管道的状态。这就是自动 DevOps 的实现方式 🦞！
---

# GitFlow — OpenClaw 技能

## 概述
**GitFlow** 是 OpenClaw 提供的一项功能，它能够自动推送代码更改，并为 GitHub 和 GitLab 仓库提供实时的持续集成/持续交付（CI/CD）管道状态监控。通过减少开发者在不同仓库和管道仪表板之间切换的频率，该功能显著提升了开发效率。

该技能可以自动推送代码更改并报告管道运行结果，从而实现更快速的反馈和更顺畅的部署过程。

## 主要功能
GitFlow 可以：
- 自动推送本地提交
- 触发远程的 CI/CD 管道
- 获取管道状态和结果
- 报告构建的成功或失败情况
- 显示管道的 URL 和日志
- 监控多个仓库

## 典型工作流程
1. 开发者在本地提交代码更改。
2. GitFlow 自动或根据指令推送这些更改。
3. 远程的 CI/CD 管道开始运行。
4. GitFlow 报告管道的运行状态。
5. 开发者立即收到关于构建或部署的反馈。

## GitHub 命令行接口（CLI）命令
在推送代码后，可以使用 `gh` CLI 工具来获取工作流程的状态：

### 检查工作流程运行状态
```bash
gh run list
```
列出仓库最近的工作流程运行记录。

### 查看当前分支的最新运行记录
```bash
gh run list --branch $(git branch --show-current) --limit 1
```
显示当前分支最近的一次工作流程运行情况。

### 查看运行详情
```bash
gh run view <run-id>
```
显示特定工作流程运行的详细信息。

### 实时监控运行过程
```bash
gh run watch
```
实时监控最近一次工作流程的运行情况，并接收状态更新。

### 查看运行日志
```bash
gh run view <run-id> --log
```
显示某次工作流程的完整日志。

### 查看失败任务的日志
```bash
gh run view <run-id> --log-failed
```
仅显示失败任务的日志。

### 重新运行失败的任务
```bash
gh run rerun <run-id> --failed
```
仅重新运行工作流程中失败的任务。

---

## GitLab 命令行接口（CLI）命令
在推送代码后，可以使用 `glab` CLI 工具来获取管道状态：

### 检查管道状态
```bash
glab ci status
```
显示当前分支上最新管道的运行状态。

### 查看管道详情
```bash
glab ci view
```
以交互式方式查看当前管道的详细信息。

### 列出最近的管道
```bash
glab ci list
```
列出仓库中最近的所有管道。

### 查看特定管道
```bash
glab ci view <pipeline-id>
```
通过 ID 查看特定管道的详细信息。

### 实时监控管道
```bash
glab ci status --live
```
持续监控管道的运行状态，直到完成。

### 获取管道任务日志
```bash
glab ci trace <job-id>
```
实时显示特定任务的日志。

---

## 推送后的钩子示例
Git 没有原生的推送后钩子功能，但你可以创建一个 Git 别名来实现推送后自动监控管道状态的功能。

将以下内容添加到你的 `~/.gitconfig` 文件中：

```ini
[alias]
    pushflow = "!f() { \
        git push \"${1:-origin}\" \"${2:-$(git branch --show-current)}\"; \
        url=$(git remote get-url \"${1:-origin}\"); \
        if echo \"$url\" | grep -q 'github.com'; then \
            sleep 3 && gh run watch; \
        elif echo \"$url\" | grep -q 'gitlab'; then \
            sleep 3 && glab ci status --live; \
        fi; \
    }; f"
```

### 使用方法
```bash
git pushflow
git pushflow origin main
```

---