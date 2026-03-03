---
name: doubletick
description: 通过 Gmail 发送带有追踪功能的电子邮件，并检查这些邮件是否已被打开。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - npx
    emoji: "\u2714\ufe0f"
    homepage: https://doubletickr.com
    install:
      - kind: node
        package: doubletick-cli
        bins:
          - doubletick
---
# DoubleTick

通过Gmail发送带有跟踪功能的电子邮件，并检查收件人是否已打开这些邮件。

## 设置

1. 安装并登录（仅需一次）：

```bash
npx doubletick-cli login
```

2. 将DoubleTick添加到您的MCP配置中：

```json
{
  "mcpServers": {
    "doubletick": {
      "command": "npx",
      "args": ["-y", "doubletick-cli"]
    }
  }
}
```

## 功能说明

DoubleTick会在通过Gmail API发送的电子邮件中嵌入一个1x1像素的跟踪代码。当收件人打开邮件时，该跟踪代码会被触发，从而记录邮件被打开的时间。您可以通过相应的工具查看邮件的阅读状态。

## 工具

- **send_tracked_email**：发送带有阅读跟踪功能的电子邮件。邮件正文支持Markdown格式（会自动转换为HTML）。
- **check_tracking_status**：检查邮件是否已被打开，以及打开的次数、设备类型和时间。
- **list_tracked_emails**：列出最近发送的带有跟踪功能的电子邮件及其打开率和相关统计数据。

## 示例

```
Send a tracked email to jane@company.com with subject "Q1 Planning" and body "Hi Jane, here are the numbers for Q1..."
```

```
Check if my last tracked email was opened
```

```
Show my tracked emails dashboard
```

## 系统要求

- Node.js 18及以上版本
- 一个Gmail账户
- 一个[DoubleTick](https://doubletickr.com)账户（免费 tier：每周可跟踪5封邮件）

## 链接

- npm：https://www.npmjs.com/package/doubletick-cli
- GitHub：https://github.com/cseguinlz/doubletick-cli
- 官网：https://doubletickr.com