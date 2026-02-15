---
name: linear
description: 查询和管理线性问题（Linear issues）、项目（projects）以及团队工作流程（team workflows）。
homepage: https://linear.app
metadata: {"clawdis":{"emoji":"📊","requires":{"env":["LINEAR_API_KEY"]}}}
---

# Linear

用于管理问题、检查项目进度，并随时掌握团队的工作进展。

## 设置

```bash
export LINEAR_API_KEY="your-api-key"
# Optional: default team key used when a command needs a team
export LINEAR_DEFAULT_TEAM="TEAM"
```

**获取团队密钥：**

```bash
{baseDir}/scripts/linear.sh teams
```

如果设置了 `LINEAR_DEFAULT_TEAM`，则可以在调用相关命令时省略 `team` 参数：

```bash
{baseDir}/scripts/linear.sh create "Title" ["Description"]
```

## 快速命令

```bash
# My stuff
{baseDir}/scripts/linear.sh my-issues          # Your assigned issues
{baseDir}/scripts/linear.sh my-todos           # Just your Todo items
{baseDir}/scripts/linear.sh urgent             # Urgent/High priority across team

# Browse
{baseDir}/scripts/linear.sh teams              # List available teams
{baseDir}/scripts/linear.sh team <TEAM_KEY>    # All issues for a team
{baseDir}/scripts/linear.sh project <name>     # Issues in a project
{baseDir}/scripts/linear.sh issue <TEAM-123>   # Get issue details
{baseDir}/scripts/linear.sh branch <TEAM-123>  # Get branch name for GitHub

# Actions
{baseDir}/scripts/linear.sh create <TEAM_KEY> "Title" ["Description"]
{baseDir}/scripts/linear.sh comment <TEAM-123> "Comment text"
{baseDir}/scripts/linear.sh status <TEAM-123> <todo|progress|review|done|blocked>
{baseDir}/scripts/linear.sh assign <TEAM-123> <userName>
{baseDir}/scripts/linear.sh priority <TEAM-123> <urgent|high|medium|low|none>

# Overview
{baseDir}/scripts/linear.sh standup            # Daily standup summary
{baseDir}/scripts/linear.sh projects           # All projects with progress
```

## 常见工作流程

### 早晨站会
```bash
{baseDir}/scripts/linear.sh standup
```
显示：你的待办事项、团队中受阻的项目、最近完成的任务以及正在审核中的任务。

### 从聊天中快速创建问题
```bash
{baseDir}/scripts/linear.sh create TEAM "Fix auth timeout bug" "Users getting logged out after 5 min"
```

### 问题分类处理模式
```bash
{baseDir}/scripts/linear.sh urgent    # See what needs attention
```

## Git 工作流程（Linear 与 GitHub 的集成）

**请始终使用基于 `Linear` 的分支名称**，以实现自动的问题状态跟踪。

### 获取分支名称
```bash
{baseDir}/scripts/linear.sh branch TEAM-212
# Returns: dev/team-212-fix-auth-timeout-bug
```

### 为问题创建工作区（Worktree）
```bash
# 1. Get the branch name from Linear
BRANCH=$({baseDir}/scripts/linear.sh branch TEAM-212)

# 2. Pull fresh main first (main should ALWAYS match origin)
cd /path/to/repo
git checkout main && git pull origin main

# 3. Create worktree with that branch (branching from fresh origin/main)
git worktree add .worktrees/team-212 -b "$BRANCH" origin/main
cd .worktrees/team-212

# 4. Do your work, commit, push
git push -u origin "$BRANCH"
```

**⚠️ 严禁修改主分支（main）上的文件。** 所有更改都应在工作区（worktree）中进行。

### 这一点的重要性：
- Linear 与 GitHub 的集成会根据分支名称来跟踪 Pull Request（PR）的状态。
- 当你从 `Linear` 分支创建 PR 时，问题会自动标记为“在审核中”（In Review）。
- 当 PR 合并后，问题会自动标记为“已完成”（Done）。
- 手动设置的分支名称会破坏这种自动化机制。
- 保持主分支的整洁可以避免意外推送，同时便于清理工作区（worktree）。

### 快速参考
```bash
# Full workflow example
ISSUE="TEAM-212"
BRANCH=$({baseDir}/scripts/linear.sh branch $ISSUE)

# Always start from fresh main
cd ~/workspace/your-repo
git checkout main && git pull origin main

# Create worktree (inside .worktrees/)
git worktree add .worktrees/${ISSUE,,} -b "$BRANCH" origin/main
cd .worktrees/${ISSUE,,}

# ... make changes ...
git add -A && git commit -m "fix: implement $ISSUE"
git push -u origin "$BRANCH"
gh pr create --title "$ISSUE: <title>" --body "Closes $ISSUE"
```

## 问题优先级

| 优先级 | 值 | 适用场景 |
|-------|-------|---------|
| 紧急 | 1 | 生产环境中的问题或阻碍项目进展的问题 |
| 高 | 2 | 本周需要处理的重要问题 |
| 中等 | 3 | 本冲刺/周期内需要完成的任务 |
| 低 | 4 | 可以考虑完成的问题 |
| 无 | 0 | 待办事项，以后再处理 |

## 团队信息（缓存）

团队密钥和 ID 会通过 API 获取并在首次查询后缓存到本地。
使用 `linear.sh teams` 命令可以刷新并查看可用的团队列表。

## 注意事项：
- 该工具使用 GraphQL API（api.linear.appgraphql）。
- 需要设置 `LINEAR_API_KEY` 环境变量。
- 问题的标识符格式为 `TEAM-123`。

## 致谢

本工具的灵感来源于 [schpet/linear-cli](https://github.com/schpet/linear-cli)，由 Peter Schilling 开发（采用 ISC 许可协议）。
这是一个独立的 Bash 工具，用于与 Clawdbot 进行集成。