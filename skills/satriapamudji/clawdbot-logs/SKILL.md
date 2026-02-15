---
name: clawdbot-logs
description: 分析 Clawdbot 的日志和诊断信息。当用户询问机器人的性能、响应时间、错误情况、会话统计信息、令牌使用情况、API 费用，或者希望调试响应缓慢的问题时，可以使用此功能。
---

# Clawdbot 日志与诊断

用于分析 Clawdbot 的性能、错误信息以及会话数据。

## 快速命令

### 响应时间（最近 N 条消息）
```bash
scripts/response-times.sh [count]
```

### 最近的错误
```bash
journalctl --user -u clawdbot-gateway.service --no-pager --since "1 hour ago" | grep -iE "(error|fail|invalid)" | tail -20
```

### 会话统计信息
```bash
scripts/session-stats.sh
```

### 网关状态
```bash
systemctl --user status clawdbot-gateway.service --no-pager
```

### 配置验证
```bash
cat ~/.clawdbot/clawdbot.json | jq . > /dev/null && echo "Config valid" || echo "Config invalid"
```

## 日志来源

| 来源 | 位置 | 包含内容 |
|--------|----------|----------|
| 日志文件 | `journalctl --user -u clawdbot-gateway.service` | 会话状态、错误信息、工具执行记录 |
| 日志文件（每日） | `/tmp/clawdbot/clawdbot-YYYY-MM-DD.log` | 详细的 JSON 格式日志 |
| 会话文件 | `~/.clawdbot/agents/main/sessions/*.jsonl` | 完整的对话记录、令牌使用情况、费用信息 |
| 会话元数据 | `~/.clawdbot/agents/main/sessions/sessions.json` | 当前会话状态、模型信息 |

## 常见诊断方法

### 响应速度过慢
1. 检查响应时间：`scripts/response-times.sh 20`
2. 查看 `sessions.json` 文件中的令牌数量：`jq '.["agent:main:main"].totalTokens' ~/.clawdbot/agents/main/sessions/sessions.json`
3. 如果令牌数量超过 30000 个，请在 Telegram 中运行 `/compact` 命令或开始新的会话

### 配置错误
```bash
journalctl --user -u clawdbot-gateway.service --no-pager --since "10 minutes ago" | grep -i "invalid config"
```

### API 使用费用（来自会话数据）
```bash
scripts/session-stats.sh
```

## 有用的操作模式

### 按类别过滤日志文件
```bash
# Session state changes
journalctl --user -u clawdbot-gateway.service | grep "session state"

# Tool execution
journalctl --user -u clawdbot-gateway.service | grep "\[tools\]"

# Telegram activity
journalctl --user -u clawdbot-gateway.service | grep "\[telegram\]"
```

### 解析会话文件以获取最近的消息
```bash
tail -20 ~/.clawdbot/agents/main/sessions/*.jsonl | jq -r 'select(.message.role=="user") | .message.content[0].text' 2>/dev/null | tail -10
```