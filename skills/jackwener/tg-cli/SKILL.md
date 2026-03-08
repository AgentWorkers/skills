---
name: tg-cli
description: **Telegram CLI 技能：通过终端同步聊天记录、搜索消息、过滤关键词以及监控群组**
author: jackwener
version: "1.0.0"
tags:
  - telegram
  - tg
  - chat
  - monitor
  - cli
---
# tg-cli 技能

tg-cli 是一个用于 Telegram 的命令行工具，支持同步聊天记录、搜索消息、过滤关键词、发送消息以及监控群组活动。

## 先决条件

```bash
# Install (requires Python 3.10+)
uv tool install kabi-tg-cli
# Or: pipx install kabi-tg-cli
```

## 认证

该工具使用您的 Telegram 账户（基于 MTProto 协议）进行认证。内置了 API 凭据，只需使用手机号码登录即可。

```bash
tg chats              # First run: enter phone + verification code
tg whoami             # Check current user
```

## 命令参考

### Telegram 操作

```bash
tg chats                          # List joined chats
tg chats --type group             # Filter by type
tg whoami                         # Show current user info
tg whoami --json                  # JSON output
tg history CHAT -n 1000           # Fetch historical messages
tg sync CHAT                      # Incremental sync (only new)
tg sync-all                       # Sync ALL chats (single connection)
tg listen                         # Real-time listener
tg info CHAT                      # Chat details
tg send CHAT "Hello!"             # Send a message
```

### 搜索与查询

```bash
tg search "Rust"                     # Search stored messages
tg search "Rust" -c "牛油果" --json  # Filter by chat + JSON
tg filter "Rust,Golang,Java"         # Multi-keyword filter (today)
tg filter "招聘,remote" --hours 48   # Filter last N hours
tg stats                             # Message statistics per chat
tg top -c "牛油果" --hours 24        # Most active senders
tg timeline --by hour                # Activity bar chart
tg today                             # Today's messages by chat
```

### 数据管理

```bash
tg export CHAT -f json -o out.json   # Export messages
tg export CHAT --hours 24            # Export last 24 hours
tg purge CHAT -y                     # Delete stored messages
```

## JSON 输出

大部分命令支持使用 `--json` 选项来生成机器可读的 JSON 输出格式：

```bash
tg search "Rust" --json | jq '.[0].content'
tg whoami --json | jq '.username'
tg today --json | jq 'length'
tg filter "招聘" --hours 48 --json
```

## 适用于 AI 代理的常见模式

```bash
# Quick daily workflow
tg sync-all                          # Sync everything
tg today                             # See today's messages
tg filter "Rust,Golang" --hours 24   # Filter job posts

# Search and export for analysis
tg search "招聘" -n 100 --json > jobs.json
tg filter "远程,remote,Web3" --hours 72 --json > filtered.json

# Send messages
tg send "GroupName" "Hello from CLI!"
```

## 调试

```bash
tg -v sync-all       # Debug logging for troubleshooting
tg -v stats          # See SQL queries and timing
```

## 错误处理

- 命令执行成功时返回代码 0，失败时返回非零代码
- 错误信息会以 ✗ 作为前缀显示，或以红色字体显示
- 聊天名称采用模糊匹配方式（输入部分名称即可匹配到相关聊天）
- `sync-all` 命令会优雅地跳过无法找到的聊天记录

## 安全提示

- 请勿要求用户在聊天记录中分享手机号码或验证码。
- 会话数据仅存储在本地，不会上传到任何外部服务器。