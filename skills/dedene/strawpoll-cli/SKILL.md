---
name: strawpoll-cli
description: >
  Create and manage StrawPoll polls, meeting polls, and ranking polls from the terminal
  using the strawpoll CLI. Use when the user wants to create polls, view poll results,
  schedule meetings with availability, run ranked-choice votes, delete or update polls,
  or automate StrawPoll workflows in scripts.
---

# strawpoll-cli

这是一个用于 [StrawPoll API v3](https://strawpoll.com/) 的命令行接口。支持三种类型的投票：多项选择、会议可用性投票以及排名投票。

## 安装

```bash
# Homebrew (macOS/Linux)
brew install dedene/tap/strawpoll

# Or via Go
go install github.com/dedene/strawpoll-cli/cmd/strawpoll@latest
```

## 认证

需要一个 API 密钥。您可以在 [strawpoll.com/account/settings](https://strawpoll.com/account/settings) 获取密钥。

```bash
# Store in system keyring (interactive prompt)
strawpoll auth set-key

# Or use environment variable (for scripts/CI)
export STRAWPOLL_API_KEY="your-key-here"

# Verify setup
strawpoll auth status
```

## 快速入门

```bash
# Create a poll
strawpoll poll create "Favorite language?" Go Rust Python TypeScript

# View poll details (accepts ID or full URL)
strawpoll poll get NPgxkzPqrn2
strawpoll poll get https://strawpoll.com/NPgxkzPqrn2

# View results with vote counts
strawpoll poll results NPgxkzPqrn2

# Delete (with confirmation)
strawpoll poll delete NPgxkzPqrn2
```

## 投票类型

### 多项选择投票

```bash
# Basic poll
strawpoll poll create "Best editor?" Vim Emacs "VS Code" Neovim

# With voting rules
strawpoll poll create "Pick up to 3" A B C D E \
  --is-multiple-choice --multiple-choice-max 3 \
  --dupcheck session --deadline 24h

# Private poll, copy URL to clipboard
strawpoll poll create "Team vote" Opt1 Opt2 --is-private --copy

# Open in browser after creation
strawpoll poll create "Quick poll" Yes No --open

# List your polls
strawpoll poll list --limit 10

# Update a poll
strawpoll poll update NPgxkzPqrn2 --title "New title" --add-option "New option"

# Reset votes (with confirmation)
strawpoll poll reset NPgxkzPqrn2
```

### 会议可用性投票

```bash
# With all-day dates
strawpoll meeting create "Team standup" \
  -d 2025-03-10 -d 2025-03-11 -d 2025-03-12

# With time ranges
strawpoll meeting create "1:1 meeting" \
  -r "2025-03-10 09:00-10:00" \
  -r "2025-03-10 14:00-15:00" \
  --tz "America/New_York" --location "Room 4B"

# Interactive wizard (no dates = launches wizard)
strawpoll meeting create "Sprint planning"

# View availability grid
strawpoll meeting results xYz123abc

# List meeting polls
strawpoll meeting list
```

### 排名投票

```bash
# Create ranking poll
strawpoll ranking create "Rank these frameworks" React Vue Svelte Angular Solid

# View Borda count results
strawpoll ranking results rAnK456

# Verbose: per-position breakdown
strawpoll ranking results rAnK456 --verbose

# List ranking polls
strawpoll ranking list
```

## 输出格式

所有命令都支持三种输出格式：

```bash
# Default: colored table (human-readable)
strawpoll poll results NPgxkzPqrn2

# JSON: structured output for scripting
strawpoll poll results NPgxkzPqrn2 --json

# Plain: tab-separated values
strawpoll poll results NPgxkzPqrn2 --plain

# Disable colors (also respects NO_COLOR env var)
strawpoll poll results NPgxkzPqrn2 --no-color
```

### 脚本示例

```bash
# Get poll ID from creation
POLL_ID=$(strawpoll poll create "Vote" A B --json | jq -r '.id')

# Pipe results
strawpoll poll results "$POLL_ID" --plain | cut -f1,3

# Delete without confirmation
strawpoll poll delete "$POLL_ID" --force

# Results with participant breakdown
strawpoll poll results "$POLL_ID" --participants --json
```

## 配置默认值

保存您的偏好设置，以避免重复输入参数：

```bash
# Set defaults
strawpoll config set dupcheck session
strawpoll config set results_visibility after_vote

# View config
strawpoll config show

# Config file location
strawpoll config path
```

配置文件保存在 `~/.config/strawpoll/config.yaml` 中。

## 交互式模式

在终端中不带参数运行该命令时，会启动一个交互式向导：

```bash
# Launches wizard (poll title, options, settings)
strawpoll poll create

# Launches meeting wizard (dates, times, location)
strawpoll meeting create "Team sync"
```

向导的输出会显示在标准错误流（stderr）中，数据输出会显示在标准输出流（stdout）中。在非终端环境（如管道）中，需要通过参数传递所有必要的信息。

## 重要说明

- 投票选项：最少 2 个，最多 30 个
- 投票 ID：可以接受简短的 ID 或完整的 URL（包含/不包含 `https://`、`www.`、`/polls/`）
- 截止时间：使用 RFC3339 格式（例如 `2025-03-15T18:00:00Z`）或持续时间（例如 `24h`、`1h30m`）
- 会议日期：`YYYY-MM-DD` 表示全天，`YYYY-MM-DD HH:MM-HH:MM` 表示特定时间段
- 时区：使用 IANA 格式（例如 `Europe/Berlin`、`America/New_York`）
- 无专门的投票端点——投票只能通过投票 URL 在浏览器中完成

## Shell 完成提示（Shell Completion Tips）

```bash
strawpoll completion bash > /etc/bash_completion.d/strawpoll
strawpoll completion zsh > "${fpath[1]}/_strawpoll"
strawpoll completion fish > ~/.config/fish/completions/strawpoll.fish
```

有关所有命令的完整参数说明，请参阅 [reference.md](reference.md)。