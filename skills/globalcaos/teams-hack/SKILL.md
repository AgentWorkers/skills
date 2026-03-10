---
name: teams-hack
version: 1.0.0
description: "您的代理会读取 Teams 聊天记录、在频道中发布内容，并搜索所有信息。有一个被窃取的令牌。每个浏览器操作（点击）都会被记录为一次事件，记录时长为 90 天。"
metadata:
  openclaw:
    emoji: "💬"
    os: ["linux", "darwin"]
    requires:
      capabilities: ["browser"]
    notes:
      security: "Shares the Outlook MSAL refresh token. One extraction covers both skills. Token stored at ~/.openclaw/credentials/outlook-msal.json (0600). Auto-rotates on use, lasts 90+ days."
---
# Teams Hack

**一个令牌，两种功能，90天的使用权限。**

此技能与 [**outlook-hack**](https://clawhub.com/globalcaos/outlook-hack) 共享同一个 MSAL 刷新令牌。只需从 Teams 的 `localStorage` 中提取一次令牌，即可同时获得邮箱和聊天访问权限。

## 功能介绍

- 💬 阅读和发送聊天消息（一对一或群组）
- 📢 阅读和发布团队频道内的内容
- 🔍 在整个 Teams 系统中搜索消息
- 👥 浏览组织目录，查看在线状态
- 📅 查看日历，并包含团队会议的链接
- 🏢 列出你加入的团队和频道

## 快速入门

### 1. 令牌提取（一次性操作，约 30 秒）

在 Chrome 浏览器中打开 **Microsoft Teams**（网址：`teams.cloud.microsoft`），然后通过 OpenClaw 浏览器代理附加该标签页。代理会在页面中自动执行以下操作：

```javascript
(() => {
  const keys = Object.keys(localStorage).filter(
    (k) => k.includes("refreshtoken") || k.includes("RefreshToken"),
  );
  const results = keys.map((k) => {
    const parsed = JSON.parse(localStorage.getItem(k));
    return { key: k, secret: parsed.secret, client_id: parsed.client_id };
  });
  // Also get tenant ID
  const accountKeys = Object.keys(localStorage).filter((k) => {
    try {
      return JSON.parse(localStorage.getItem(k)).tenantId;
    } catch {
      return false;
    }
  });
  let tenantId = null;
  for (const k of accountKeys) {
    try {
      tenantId = JSON.parse(localStorage.getItem(k)).tenantId;
      break;
    } catch {}
  }
  return { tokens: results, tenantId };
})();
```

提取令牌后，请将其保存到安全的位置：

```bash
teams token store --refresh-token <secret> --tenant-id <tenantId>
```

### 2. 验证令牌有效性

```bash
teams token test
```

### 3. 使用令牌

```bash
teams chats                          # Recent conversations
teams chat <id> --top 10             # Read messages
teams chat-send <id> --message "hi"  # Send message
teams teams                          # List teams
teams channels <teamId>              # List channels
teams search "project update"        # Search everything
teams users --search "Oscar"         # Find people
teams presence                       # Your status
teams calendar --days 3              # Upcoming meetings
```

## 工作原理

该技能的工作原理与 Outlook Hack 相同：

1. Teams 将 MSAL 刷新令牌存储在 `localStorage` 中。
2. 使用 Teams 的第一方客户端 ID（`5e3ce6c0-2b1f-4285-8d4b-75ee78787346`），将此令牌兑换为 Graph API 访问令牌。
3. 该客户端 ID 已预先获得了访问 Graph API 的权限。
4. 令牌会在每次使用时自动更新；只要在 90 天内使用，访问权限将始终有效。

## 令牌共享机制

这两个技能都从同一个文件中读取令牌：

```
~/.openclaw/credentials/outlook-msal.json
```

只需提取一次令牌，即可同时使用 [outlook-hack] 和 [teams-hack]。无论哪个技能更新了令牌，另一个技能也能继续正常使用。

## 命令行接口 (CLI) 参考

| 命令                                      | 功能描述                                      |
| ------------------------------------------------------ | ------------------------------------------------------ |
| `teams chats`                         | 列出最近的消息（包含最新消息的预览）                          |
| `teams chat <id>`                        | 读取消息（按时间顺序从最新到最早）                         |
| `teams chat-send <id> --message <text>`            | 向指定聊天频道发送消息                             |
| `teams teams`                         | 列出你加入的所有团队                               |
| `teams channels <teamId>`                    | 列出某个团队内的所有频道                             |
| `teams channel <teamId> <channelId>`            | 读取指定频道的消息                             |
| `teams channel-send <teamId> <channelId> --message <text>` | 向指定频道发布消息                             |
| `teams search "<query>"`                   | 在所有消息中进行全文搜索                             |
| `teams users --search <name>`                   | 在组织目录中搜索用户                             |
| `teams presence`                        | 查看你的在线状态                             |
| `teams calendar --days 7`                     | 查看日历（包含会议链接）                         |
| `teams me`                         | 查看你的个人资料                             |

## 相关技能：Outlook Hack

[**outlook-hack**](https://clawhub.com/globalcaos/outlook-hack) 与本技能共享同一个 MSAL 刷新令牌。只需提取一次令牌，即可同时获得邮箱和聊天访问权限。

这两个技能都使用同一个凭据文件来存储登录信息：

```
~/.openclaw/credentials/outlook-msal.json
```

无论哪个技能更新了令牌，另一个技能也能自动获得相应的功能。

| 技能                                      | 功能                                      | 是否支持发送消息？                                      |
| ------------------------------------------------------ | ------------------------------------------------------ | -------------------------------------- |
| **[outlook-hack](https://clawhub.com/globalcaos/outlook-hack)** | 邮箱：读取、搜索、创建邮件、管理文件夹、查看附件、日历、联系人        | ✅ 不支持发送邮件                              |
| **teams-hack**                         | 聊天：读取、发送消息、管理频道、搜索、查看在线状态、浏览组织目录             | 支持发送消息                                      |

## 技术架构

- **完全基于 Node.js（版本 22 及以上）**  
- **使用相同的凭据文件**（与 Outlook 共享）  
- **基于 Graph API v1.0**（标准的 Microsoft API）  
- **支持 Beta 版本**：某些功能在 Graph API v1.0 不支持时会使用 `/beta` 接口  

## 完整技术栈

你可以将 [teams-hack] 与 [outlook-hack](https://clawhub.com/globalcaos/outlook-hack) 结合使用，以实现邮箱功能；与 [whatsapp-ultimate](https://clawhub.com/globalcaos/whatsapp-ultimate) 结合使用，实现即时通讯功能；或与 [jarvis-voice](https://clawhub.com/globalcaos/jarvis-voice) 结合使用，实现语音通信功能。

👉 **[克隆它，修改它，让它成为属于你的工具吧。](https://github.com/globalcaos/tinkerclaw)**