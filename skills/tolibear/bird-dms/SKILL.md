---
name: bird-dm
description: 这是一个用于“Bird”技能的插件，它允许您的智能助手检查用户的X（Twitter）或Twitter的私信收件箱。当用户请求查看私信、阅读Twitter的直接消息、列出私信对话内容或监控其X账号的收件箱时，可以使用该插件。
metadata:
  openclaw:
    emoji: "💬"
    requires:
      bins: ["node"]
    install:
      - id: npm
        kind: node
        package: bird-dm
        bins: ["bird-dm"]
        label: "Install bird-dm (npm)"
---

# Bird DM

这是一个为 [bird](https://github.com/steipete/bird) 开发的 DM（Direct Message）插件，用于查看您在 X 或 Twitter 上收到的私信。

## 安装

```bash
npm install -g bird-dm
```

## 命令

```bash
bird-dm inbox              # List DM conversations
bird-dm inbox -n 50        # More conversations
bird-dm inbox --json       # JSON output

bird-dm read <conv-id>     # Read messages
bird-dm read <id> -n 100   # More messages
bird-dm read <id> --json   # JSON output
```

## 示例

**列出所有对话记录：**
```
💬 @alice, @bob
   ID: 352135192-2015310805076430848
   @alice: hey, check this out
   1/30/2026, 9:15 AM

👥 Project Team
   ID: 1234567890-9876543210
   @carol: meeting at 3pm
   1/30/2026, 8:42 AM
```

**阅读私信内容：**
```
Conversation: 352135192-2015310805076430848

@alice • 1/29/2026, 12:12 PM
hey, wanted to share this article

@bob • 1/29/2026, 2:07 PM
thanks! checking it out now

Showing 2 of 2 messages
```

## 认证

该插件使用与 [bird](https://github.com/steipete/bird) 相同的浏览器 cookie 进行身份验证。请运行 `bird check` 命令来验证您的会话状态。