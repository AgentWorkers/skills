---
name: glass2claw
description: "这是一种基于逻辑的协议，用于将生活中的重要瞬间（如照片、视频等）整理到 Notion 文档中。该协议通过 OpenClaw 的 `sessions_send` 工具，将来自 WhatsApp 的图片路由到您在 Discord 服务器上创建的分类化的 Notion 数据库中。"
metadata:
  {
    "openclaw":
      {
        "emoji": "👁️",
        "requires": {
          "env": ["NOTION_API_KEY"],
          "configPaths": ["configs/vision_router.md"],
          "tools": ["sessions_send", "message", "web_fetch"]
        },
        "dataFlow": {
          "input": "Image URL forwarded from WhatsApp via sessions_send",
          "routing": "Agent reads configs/vision_router.md, classifies image intent (Wine/Tea/Contacts), then calls sessions_send to the matching Discord channel session key",
          "output": "Structured entry written to the corresponding Notion database using NOTION_API_KEY"
        }
      },
  }
---
# glass2claw：视觉路由协议

`glass2claw` 提供了一套逻辑路由模板，用于将来自 WhatsApp 的视觉捕获内容通过您的私有 Discord 服务器整理到结构化的 Notion 数据库中。

## 🏗️ 设计理念

此技能仅提供指令性指导，不包含任何二进制文件、curl 命令或可执行命令。它完全依赖于 OpenClaw 平台的原生工具：

| 步骤 | 使用的工具 | 功能 |
|------|-----------|--------------|
| 接收图片 | `sessions_send` | 将 WhatsApp 会话中的图片 URL 转发到 Discord 中心会话 |
| 分类意图 | 代理推理 | 从图片中判断用户属于“Wine”组、“Tea”组还是“Contacts”组 |
| 路由 | `sessions_send` | 中心会将图片发送到相应的专家 Discord 频道会话 |
| 存储 | `message` + Notion API | 专家会在 Notion 数据库中发布图片并创建相应的条目 |

**所有数据都不会离开您的私有 OpenClaw 基础设施**。所有的路由操作都在您自己的 Discord 服务器频道内完成。

## 🚀 配置

### 1. 必需的配置文件：`configs/vision_router.md`

请在您的 OpenClaw 工作空间中创建名为 `configs/vision_router.md` 的文件。代理会读取此文件以获取 Notion 数据库的 ID。该文件的路径在技能元数据中的 `configPaths` 部分进行了指定。

```markdown
# Vision Router Config

## Notion Database IDs
- Wine Cellar: [YOUR_NOTION_DATABASE_ID]
- Tea Closet: [YOUR_NOTION_DATABASE_ID]
- Contacts: [YOUR_NOTION_DATABASE_ID]

## Discord Session Keys (hub → specialist routing)
- Wine session: agent:main:discord:channel:[YOUR_WINE_CHANNEL_ID]
- Tea session: agent:main:discord:channel:[YOUR_TEA_CHANNEL_ID]
- Contacts session: agent:main:discord:channel:[YOUR_CONTACTS_CHANNEL_ID]
```

### 2. 应用模板

- **中心路由逻辑**：`SAMPLE_AGENT.md` —— 将其粘贴到您的中心 Discord 频道的 `AGENTS.md` 或 `SOUL.md` 文件中
- **Wine 专家角色模板**：`SAMPLE_SOUL_WINE.md` —— 将其粘贴到您的 Wine 频道的 `SOUL.md` 文件中

## 🔄 数据流（详细说明）

所有数据传输操作都在您的私有 Discord 服务器内完成。`configs/vision_router.md` 中的会话键由用户自行定义，且仅指向您拥有的频道。

## 🛡️ 最佳实践

- **最小权限原则**：将您的 Notion 访问令牌的权限限制在所需的三个数据库范围内
- **仅使用私有 Discord 服务器**：切勿使用公共 Discord 服务器
- **代理无权自行决定数据存储位置**：所有目标会话键都硬编码在 `configs/vision_router.md` 中，不会由代理程序动态推断

---
*创建者：JonathanJing | 人工智能可靠性架构师*