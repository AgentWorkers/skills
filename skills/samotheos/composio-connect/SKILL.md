---
name: composio-connect
description: "通过 Composio 和 mcporter，可以将 850 多款应用程序（如 Gmail、Slack、GitHub、Calendar、Notion、Jira 等）连接到 OpenClaw。当用户需要发送电子邮件、创建问题、发布消息、管理日历、搜索文档或与任何第三方 SaaS 应用程序交互时，可以使用此功能。这一技能涵盖了 11,000 多种工具，并支持 OAuth 认证机制。"
homepage: https://composio.dev
metadata:
  {
    "openclaw":
      {
        "emoji": "🔗",
        "requires":
          {
            "env": ["COMPOSIO_API_KEY", "COMPOSIO_MCP_URL"],
            "bins": ["mcporter"],
          },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "mcporter",
              "bins": ["mcporter"],
              "label": "Install mcporter (npm)",
            },
          ],
      },
  }
---
# 检查 composio MCP 服务器是否已注册到 mcporter

```bash
mcporter list
```

如果 composio 服务器未显示在列表中，您可以使用以下命令进行注册：

```bash
mcporter config add composio --url $COMPOSIO_MCP_URL
```

## 查找工具

在尝试调用任何 composio MCP 工具之前，您必须先进行针对性的搜索，以确定正确的工具名称及所需的参数。

```bash
mcporter list composio --all-parameters | grep -niE -B 14 '^\s*function\s+SPOTIFY_.*(VOLUME|PLAYBACK)|^\s*function\s+.*(VOLUME|PLAYBACK).*SPOTIFY_'
```

## 执行工具

在找到所需的工具名称后，即可调用该工具：

```bash
mcporter call 'composio.SPOTIFY_SET_PLAYBACK_VOLUME(volume_percent:"90")'
```

```bash
mcporter call 'composio.TODOIST_CREATE_TASK(content: "Pay electricity bill", due_string: "tomorrow at 4pm")'
```

```bash
mcporter call 'composio.GMAIL_CREATE_DRAFT(to: "name@example.com", subject: "Quick question", body: "Hey — ...")'
```