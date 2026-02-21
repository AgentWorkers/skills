---
name: glass2claw
description: "这是一种基于逻辑的协议，用于将生活中的重要时刻（如照片、视频等）整理到 Notion 文档中。该协议为在您的私有 OpenClaw 消息传递系统中路由（管理）这些图像提供了结构化的指导。"
metadata:
  {
    "openclaw":
      {
        "emoji": "👁️",
        "requires": { 
          "env": ["NOTION_API_KEY"]
        },
      },
  }
---
# glass2claw：视觉信息路由协议

`glass2claw` 提供了一套逻辑模板，帮助您将来自移动设备的视觉信息整理到结构化的 Notion 数据库中。

## 🏗️ 设计理念
该技能仅提供指导性内容，它依赖于 OpenClaw 平台的原生功能来处理媒体和消息。其主要功能包括：
- **分类**：将图片分为“Wine”（酒类）、“Tea”（茶类）或“Contacts”（联系人）等类别。
- **上下文绑定**：使用特定的配置文件来指定数据库 ID。
- **隐私保护**：在您的私人通讯环境中处理数据。

## 🚀 配置

### 1. 数据库配置
为防止代理程序搜索您的文件系统，请将数据库 ID 存放在一个专门的文件中：`configs/vision_router.md`。
```markdown
- Wine Cellar: [YOUR_DATABASE_ID]
- Tea Closet: [YOUR_DATABASE_ID]
```

### 2. 实现方法
将提供的模板应用于您的代理程序提示中：
- **路由逻辑**：请参考 `SAMPLE_AGENT.md` 以获取中心辐射式（hub-and-spoke）路由的详细指南。
- **专业角色**：请参考 `SAMPLE_SOUL_WINE.md` 以获取关于酒类分析的指导。

## 🛡️ 最佳实践
- **最小权限原则**：使用仅具有访问所需数据库权限的 Notion 令牌。
- **安全通道**：对于敏感的生活记录数据，始终使用私有的 Discord 服务器或直接消息进行传输。
- **工具使用**：本协议假设您使用的是经过授权的标准平台工具来进行 API 交互。

---
*创建者：JonathanJing | 人工智能可靠性架构师*