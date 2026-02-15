---
name: xpoz-social-search
description: "实时搜索 Twitter、Instagram 和 Reddit 上的帖子。查找社交媒体中的提及内容，追踪话题标签（hashtags），发现具有影响力的用户（influencers），并分析用户互动情况——系统已索引超过 15 亿条帖子。AI 代理可以轻松实现社交监听（social listening）、品牌监控（brand monitoring）和竞争对手研究（competitor research）。"
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
  - social-media
  - search
  - twitter
  - instagram
  - reddit
  - mcp
  - xpoz
  - research
  - intelligence
  - discovery
  - social-search
  - twitter-search
  - social-listening
  - brand-monitoring
  - hashtag
  - mentions
  - influencer
  - engagement
  - viral
  - trending
---

# Xpoz 社交搜索

**多平台社交搜索：覆盖 Twitter、Instagram 和 Reddit，可搜索超过 15 亿条帖子。**

支持搜索帖子、查找用户以及发现热门讨论。该功能基于 Xpoz MCP 构建。

## 设置

运行 `xpoz-setup` 命令进行初始化。验证功能是否正常：`mcporter call xpoz.checkAccessKeyStatus`

## 工具参考

| 工具        | 平台        | 功能            |
|-------------|------------|-------------------|
| `getTwitterPostsByKeywords` | Twitter     | 搜索 Twitter 帖子         |
| `getInstagramPostsByKeywords` | Instagram     | 搜索 Instagram 帖子         |
| `getRedditPostsByKeywords` | Reddit      | 搜索 Reddit 帖子         |
| `getTwitterUsersByKeywords` | Twitter     | 搜索 Twitter 用户         |
| `getInstagramUsersByKeywords` | Instagram     | 搜索 Instagram 用户         |
| `getRedditUsersByKeywords` | Reddit      | 搜索 Reddit 用户         |
| `getTwitterUser`     | Twitter     | 通过用户名/ID 查看用户资料     |
| `getInstagramUser`     | Instagram     | 通过用户名/ID 查看用户资料     |
| `getRedditUser`     | Reddit      | 通过用户名查看用户资料     |
| `searchTwitterUsers`   | Twitter     | 按名称搜索用户         |
| `checkOperationStatus` |           | **查询搜索结果的状态**       |
| `getRedditSubredditsByKeywords` | Reddit      | 搜索相关的 Reddit 子版块       |

**参数：** `query`、`startDate`/`endDate`（YYYY-MM-DD 格式）、`limit`、`fields`

## 搜索模式

**搜索帖子：**
```bash
mcporter call xpoz.getTwitterPostsByKeywords query="MCP" startDate=2026-01-01
mcporter call xpoz.checkOperationStatus operationId=op_abc # Poll every 5s
```

**查找用户：**
```bash
mcporter call xpoz.getTwitterUsersByKeywords query='"open source" AND LLM'
```

**查看用户资料：**
```bash
mcporter call xpoz.getTwitterUser identifier=elonmusk identifierType=username
```

**逻辑运算符：** `AND`、`OR`、`NOT`、`"exact"`、`()`  
```bash
query="Tesla AND cars NOT stock"
```

**CSV 导出：** 使用 `dataDumpExportOperationId` 进行 CSV 导出（最多支持 64,000 行数据）。

## 示例

**竞争对手信息：**
```bash
mcporter call xpoz.getTwitterPostsByKeywords query="CompetitorName"
mcporter call xpoz.getTwitterUsersByKeywords query="CompetitorName"
```

**影响者信息：**
```bash
mcporter call xpoz.getInstagramUsersByKeywords query="fitness transformation"
```

**社区信息：**
```bash
mcporter call xpoz.getRedditSubredditsByKeywords query="startup"
```

## 注意事项：

⚠️ **务必使用 `checkOperationStatus` 命令查询搜索结果的状态**——搜索操作仅返回操作 ID，而非实际数据。  
🚀 **为提高性能，请使用 `fields` 参数指定需要获取的字段。**  
📊 **若需批量导出数据，请使用 `dataDumpExportOperationId`。**  
📅 **日期格式：YYYY-MM-DD**（当前示例：2026 年）

**免费 tier：** 每月 100 次搜索，每次搜索最多返回 1,000 条结果 | [xpoz.ai](https://xpoz.ai)