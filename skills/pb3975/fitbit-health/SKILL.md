---
name: fitbit
description: 通过命令行界面（CLI）查询 Fitbit 的健康数据（活动量、睡眠质量、心率、体重）。适用于需要 Fitbit 数据来回答健康/健身相关问题，或者当用户询问自己的步数、睡眠情况、心率或体重时使用。
metadata: {"clawdbot":{"emoji":"💪","requires":{"bins":["fitbit"]}}}
---

# Fitbit CLI

用于从 Fitbit 的 Web API 中检索健康和健身数据。

## 设置

1. 在 https://dev.fitbit.com/apps 注册一个应用程序：
   - OAuth 2.0 应用程序类型：**个人**
   - 回调 URL：`http://localhost:18787/callback`
2. 运行 `fitbit configure` 并输入您的客户端 ID。
3. 运行 `fitbit login` 进行授权。

## 快速参考

```bash
# Setup & auth
fitbit configure              # Set client ID (first time)
fitbit login                  # Authorize via browser
fitbit logout                 # Sign out
fitbit status                 # Check auth status

# Data
fitbit profile                # User profile info
fitbit activity [date]        # Daily activity summary
fitbit activity steps [date]  # Just steps
fitbit summary [date]         # Full daily summary
fitbit today                  # Today's summary (shortcut)
```

## 选项

所有命令都支持以下选项：
- `--json` — 以 JSON 格式输出结果
- `--no-color` — 以纯文本格式输出结果
- `--verbose` — 显示调试信息及 HTTP 请求的详细信息
- `--tz <zone>` — 更改时区（例如：`America/Chicago`）

## 示例

```bash
# Get today's step count
fitbit activity steps

# Get yesterday's full summary as JSON
fitbit summary 2026-01-25 --json

# Check if authenticated
fitbit status
```

## 注意事项

- 如果省略日期，默认使用当前日期。
- 日期格式为 `YYYY-MM-DD` 或 `today`。
- 令牌存储在 `~/.config/fitbit-cli/tokens.json` 文件中（权限设置为 600）。
- 令牌会自动更新。