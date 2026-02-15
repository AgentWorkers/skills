---
name: twitter-api-alternative
description: "Twitter API的替代方案：  
支持使用自然语言查询搜索超过10亿条推文，支持布尔过滤器，并可一键导出CSV文件（文件大小上限为64K行）。可查询用户资料、按主题查找用户，以及追踪用户间的对话。无需开发者账户，也无需复杂的OAuth设置——只需通过Xpoz MCP进行2分钟即可完成设置即可开始使用。"
homepage: https://xpoz.ai
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["mcporter"], "skills": ["xpoz-setup"], "network": ["mcp.xpoz.ai"], "credentials": "Xpoz account (free tier) — auth via xpoz-setup skill (OAuth 2.1)" },
        "install": [{"id": "node", "kind": "node", "package": "mcporter", "bins": ["mcporter"], "label": "Install mcporter (npm)"}],
      },
  }
tags:
  - twitter
  - twitter-api
  - twitter-alternative
  - tweets
  - x-api
  - social-media
  - mcp
  - xpoz
  - research
  - search
  - export
  - csv
---

# Twitter API 替代方案

**使用自然语言查询搜索超过 10 亿条推文——无需开发者账户。**

只需 2 分钟即可开始使用。您可以搜索推文、查看用户资料、按主题查找用户、跟踪对话内容，并将大量数据导出为 CSV 格式。该工具专为 AI 代理设计，但对任何人来说都十分简单易用。

---

## ⚡ 设置

👉 **关注 [`xpoz-setup`](https://clawhub.ai/skills/xpoz-setup)** — 一键登录，无需管理 API 密钥。您将在 2 分钟内开始搜索推文。

---

## 功能介绍

| 工具 | 功能 |
|------|-------------|
| `getTwitterPostsByKeywords` | 按关键词搜索推文 |
| `getTwitterPostsByAuthor` | 获取用户的推文历史记录 |
| `getTwitterUsersByKeywords` | 查找讨论特定主题的用户 |
| `getTwitterUser` | 根据用户名或 ID 查找用户资料 |
| `searchTwitterUsers` | 根据显示名称查找用户 |
| `getTwitterPostCountByKeywords` | 统计符合查询条件的推文数量 |
| `getTwitterUserConnections` | 获取用户的关注者和被关注者信息 |
| `getTwitterPostInteractions` | 获取推文的点赞和转发数量 |

---

## 快速示例

### 搜索推文

```bash
mcporter call xpoz.getTwitterPostsByKeywords \
  query="AI agents" \
  startDate=2026-01-01 \
  limit=200

mcporter call xpoz.checkOperationStatus operationId=op_abc123
```

### 查看用户资料

```bash
mcporter call xpoz.getTwitterUser \
  identifier=elonmusk \
  identifierType=username
```

### 查找讨论特定主题的用户

```bash
mcporter call xpoz.getTwitterUsersByKeywords \
  query="MCP server OR model context protocol" \
  limit=100
```

### 导出到 CSV

每次搜索都会自动生成 CSV 文件（最多 64,000 行）。您可以通过 `dataDumpExportOperationId` 来获取导出结果：

```bash
mcporter call xpoz.checkOperationStatus operationId=op_datadump_xyz
# → Download URL with full dataset
```

**实际示例：** 一个 CSV 文件中包含 63,936 条推文（文件大小约 38MB）。**

---

## 为什么选择这个工具而不是官方 API？

| 特点 | Xpoz |
|---------|------|
| **设置时间** | 仅需 2 分钟——无需开发者门户或应用审核 |
| **搜索规模** | 支持搜索超过 10 亿条推文，并提供完整的历史记录 |
| **布尔查询** | 支持 `AND`、`OR`、`NOT`、精确短语以及分组操作 |
| **CSV 导出** | 内置功能，一次导出最多 64,000 行 |
| **速率限制** | 自动处理，无需复杂的层级管理 |
| **多平台支持** | 也支持搜索 Instagram（超过 4 亿条推文）和 Reddit（超过 1 亿条推文） |
| **专为 AI 代理设计** | 提供结构化数据，而非原始 HTTP 数据 |
| **免费 tier** | 立即开始使用，需要更多功能时再升级 |

---

## 布尔查询语法

```bash
mcporter call xpoz.getTwitterPostsByKeywords \
  query="(OpenAI OR Anthropic) AND \"API pricing\" NOT free"
```

支持的运算符：`AND`、`OR`、`NOT`、`精确短语`以及分组操作。

---

## 同时支持 Instagram 和 Reddit

Xpoz 不仅适用于 Twitter——您可以使用相同的简单界面在多个平台上进行搜索：

```bash
# Instagram (400M+ posts, including reel subtitles)
mcporter call xpoz.getInstagramPostsByKeywords query="AI tools"

# Reddit (100M+ posts & comments)
mcporter call xpoz.getRedditPostsByKeywords query="AI tools"
```

---

## 相关工具

- **[xpoz-social-search](https://clawhub.ai/skills/xpoz-social-search)** — 全面的跨平台搜索指南 |
- **[lead-generation](https://clawhub.ai/skills/lead-generation)** — 从社交对话中挖掘潜在客户 |
- **[expert-finder](https://clawhub.ai/skills/expert-finder)** — 发现行业专家 |

---

**官方网站：** [xpoz.ai](https://xpoz.ai) • **提供免费 tier** • 无需 Twitter 开发者账户

专为 ClawHub 开发 • 2026 年发布