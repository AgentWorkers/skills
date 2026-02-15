---
name: reddit-api
description: "Reddit搜索功能：  
您可以在超过1亿条已索引的Reddit帖子、评论、用户和子版块中搜索内容。该功能支持搜索帖子、评论、用户以及子版块，帮助您找到相关讨论、追踪热门话题、发现新的社区，并分析用户参与度。无需使用Reddit API密钥，即可通过Xpoz MCP平台利用自然语言查询实现搜索功能。"
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
  - reddit
  - reddit-search
  - reddit-api
  - subreddit
  - reddit-comments
  - reddit-posts
  - community
  - discussion
  - social-media
  - mcp
  - xpoz
  - research
---

# Reddit搜索

**无需Reddit API密钥，即可搜索1亿多篇Reddit帖子和评论。**

通过Xpoz MCP，您可以查找讨论内容、发现子版块、查询用户信息并导出搜索结果。无需提供Reddit API凭证，无需担心请求速率限制，也无需进行OAuth设置。

---

## ⚡ 设置

👉 **请参考[`xpoz-setup`](https://clawhub.ai/skills/xpoz-setup)`——该工具可自动处理身份验证。用户只需点击一次“授权”即可完成设置。**

---

## 功能介绍

运行`xpoz-setup`工具后，可以通过`mcporter call xpoz.checkAccessKeyStatus`来验证设置是否成功。

## 可用的搜索功能

| 工具 | 功能说明 |
|------|-------------|
| `getRedditPostsByKeywords` | 按主题搜索帖子 |
| `getRedditCommentsByKeywords` | 搜索评论（其中包含丰富的专业见解） |
| `getRedditUsersByKeywords` | 查找讨论特定主题的用户 |
| `getRedditSubredditsByKeywords` | 发现相关的子版块 |
| `getRedditPostsByAuthor` | 获取用户的发帖历史 |
| `getRedditUser` | 查询特定用户的资料 |
| `searchRedditUsers` | 按名称查找用户 |

---

## 快速示例

### 搜索帖子

```bash
mcporter call xpoz.getRedditPostsByKeywords \
  query="self hosting AND docker" \
  startDate=2026-01-01 \
  limit=100

# Always poll for results:
mcporter call xpoz.checkOperationStatus operationId=op_abc123
```

### 搜索评论

评论中往往蕴含着最深入的专业知识——专家们分享他们的实际经验：

```bash
mcporter call xpoz.getRedditCommentsByKeywords \
  query="kubernetes networking troubleshoot" \
  fields='["id","text","authorUsername","subredditName","score","createdAtDate"]'
```

### 查找子版块

```bash
mcporter call xpoz.getRedditSubredditsByKeywords \
  query="machine learning" \
  limit=30
```

### 查询用户信息

```bash
mcporter call xpoz.getRedditUser \
  identifier=spez \
  identifierType=username
```

---

## 常用查询语法

- `AND`、`OR`、`NOT`（需大写）
- 使用`"`进行精确匹配
- 使用`()`对查询结果进行分组

```bash
mcporter call xpoz.getRedditPostsByKeywords \
  query="(python OR rust) AND \"web scraping\" NOT selenium"
```

---

## 数据导出

每次搜索都会生成一个`dataDumpExportOperationId`。通过该ID，您可以获取包含全部数据的CSV文件（最多64,000行）：

```bash
mcporter call xpoz.checkOperationStatus operationId=op_datadump_xyz
# → result.url = S3 download link
```

---

**为什么不用Reddit API直接搜索？**

| Reddit API | Xpoz Reddit搜索 |
|--|-----------|-------------------|
| **身份验证** | 需要OAuth、客户端ID和密钥 | Xpoz支持一键式身份验证 |
| **请求速率限制** | 每分钟100次请求 | 由Xpoz自动处理 |
| **搜索质量** | Reddit的搜索功能较差 | Xpoz支持全文索引和布尔运算符 |
| **评论搜索** | 不支持对评论进行关键词搜索 | ✅ 支持对评论进行全文搜索 |
| **数据导出** | 需手动分页 | 支持一键导出CSV文件（最多64,000行） |
| **历史数据** | 只能查询到2019年之前的数据 |

---

**相关技能**

- **[xpoz-social-search](https://clawhub.ai/skills/xpoz-social-search)** — 跨平台搜索（Twitter + Instagram + Reddit）
- **[expert-finder](https://clawhub.ai/skills/expert-finder)** — 从社交数据中筛选领域专家 |
- **[social-sentiment](https://clawhub.ai/skills/social-sentiment)** — 品牌情感分析

---

**官方网站：** [xpoz.ai](https://xpoz.ai) • **提供免费试用** • 无需Reddit API密钥

该工具专为ClawHub开发，发布于2026年。