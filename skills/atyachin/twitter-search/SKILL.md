---
name: xpoz-social-search
description: "实时搜索 Twitter、Instagram 和 Reddit 上的帖子。查找社交媒体中的提及内容，追踪话题标签（hashtags），发现具有影响力的用户（influencers），并分析用户互动情况——索引了超过 15 亿条帖子。AI 代理可以轻松实现社交监听（social listening）、品牌监控（brand monitoring）和竞争对手研究（competitor research）。"
homepage: https://xpoz.ai
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["mcporter"], "skills": ["xpoz-setup"], "network": ["mcp.xpoz.ai"], "credentials": "Xpoz account (free tier) — auth via xpoz-setup skill (OAuth 2.1)" },
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

# Xpoz 社交媒体搜索

**基于超过15亿条已索引帖子的多平台社交媒体搜索工具。**

您可以使用自然语言查询在 Twitter、Instagram 和 Reddit 上搜索帖子、查找用户并发现相关讨论。该功能基于 Xpoz MCP（社交智能服务器）构建，使得跨平台数据检索变得像调用一个函数一样简单。

---

## ⚡ 设置（请先阅读此部分）

**在使用此功能之前，请确保 Xpoz MCP 服务器已配置并完成身份验证。**

👉 请阅读并遵循 [`xpoz-setup/SKILL.md`](https://clawhub.ai/skills/xpoz-setup) 文档——所有步骤都将自动完成。用户无需运行任何命令，最多只需在浏览器中点击“授权”即可。

当 `mcporter call xpoz.checkAccessKeyStatus` 返回 `hasAccessKey: true` 时，再返回此处继续阅读下面的**使用模式**。

---

## 该功能的用途

该功能可指导 OpenClaw 代理执行以下操作：
- 根据关键词在 Twitter、Instagram 和 Reddit 上搜索帖子
- 查找讨论特定主题的用户
- 通过用户名或 ID 查找用户资料
- 通过名称搜索账户
- 按日期范围筛选数据以进行时效性研究
- 查找与特定主题相关的相关子版块
- 将结果导出为 CSV 格式以供分析

### 为什么选择多平台搜索？

与单平台工具不同，Xpoz 可同时搜索 Twitter、Instagram 和 Reddit，帮助您找到真正的讨论热点，而不仅仅是您认为存在讨论的地方。

**已索引的数据量：**
- 🐦 Twitter：超过 10 亿条帖子
- 📸 Instagram：超过 4 亿条帖子（包含标题和视频字幕）
- 🗨️ Reddit：超过 1 亿条帖子和评论

---

## 设置

请参阅 [`xpoz-setup`](https://clawhub.ai/skills/xpoz-setup) 文档以获取完整的设置和身份验证说明。

**简而言之：** 所有操作均由代理自动完成。您只需在浏览器打开页面后点击“授权”（或点击代理发送的链接）即可。

---

## 使用模式

### 模式 1：按主题跨平台搜索帖子

**用例：** 查找关于某个产品、趋势或事件的最新讨论。

**示例：** 在 Twitter 上查找关于“Model Context Protocol”的帖子**

```bash
mcporter call xpoz.getTwitterPostsByKeywords \
  query="model context protocol OR MCP" \
  startDate=2026-01-01 \
  limit=50
```

响应中会包含一个 `operationId`。**请务必定期轮询结果：**

```bash
mcporter call xpoz.checkOperationStatus operationId=op_abc123
```

**跨平台搜索：**

```bash
# Twitter
mcporter call xpoz.getTwitterPostsByKeywords query="AI agents"

# Instagram
mcporter call xpoz.getInstagramPostsByKeywords query="AI agents"

# Reddit
mcporter call xpoz.getRedditPostsByKeywords query="AI agents"
```

---

### 模式 2：查找讨论特定主题的用户

**用例：** 寻找潜在联系人、影响者或社区成员。

**示例：** 查找在 Twitter 上发布关于“开源 LLM”内容的用户**

```bash
mcporter call xpoz.getTwitterUsersByKeywords \
  query="\"open source\" AND LLM" \
  limit=100
```

然后轮询结果：

```bash
mcporter call xpoz.checkOperationStatus operationId=op_xyz789
```

**结果：** 显示用户列表，包括帖子数量、粉丝数量和相关性评分。

**跨平台搜索：**

```bash
# Find Instagram users posting about fitness
mcporter call xpoz.getInstagramUsersByKeywords query="fitness routine"

# Find Reddit users discussing Python
mcporter call xpoz.getRedditUsersByKeywords query="python programming"
```

---

### 模式 3：查找特定用户资料

**用例：** 获取已知账户的详细信息。

**示例：** 通过用户名查找 Twitter 用户**

```bash
mcporter call xpoz.getTwitterUser \
  identifier=elonmusk \
  identifierType=username
```

**示例：** 通过 Twitter 用户 ID 查找用户**

```bash
mcporter call xpoz.getTwitterUser \
  identifier=44196397 \
  identifierType=id
```

**其他平台：**

```bash
# Instagram profile
mcporter call xpoz.getInstagramUser identifier=instagram identifierType=username

# Reddit profile
mcporter call xpoz.getRedditUser identifier=spez identifierType=username
```

---

### 模式 4：按名称搜索账户

**用例：** 在不知道确切用户名时查找账户。

**示例：** 查找名为“OpenAI”的 Twitter 账户**

```bash
mcporter call xpoz.searchTwitterUsers query="OpenAI" limit=20
```

**跨平台搜索：**

```bash
# Search Instagram users
mcporter call xpoz.searchInstagramUsers query="National Geographic"

# Search Reddit users
mcporter call xpoz.searchRedditUsers query="AutoModerator"
```

---

### 模式 5：在指定日期范围内搜索

**用例：** 分析特定事件或时间段内的舆论趋势。

**示例：** 在超级碗比赛当天查找相关推文**

**注意：** 当前年份为 2026 年，使用 `YYYY-MM-DD` 格式。

---

### 模式 6：查找相关子版块

**用例：** 发现讨论某个主题的子版块。

**示例：** 查找关于“机器学习”的子版块**

```bash
mcporter call xpoz.getRedditSubredditsByKeywords \
  query="machine learning" \
  limit=30
```

然后轮询结果：

```bash
mcporter call xpoz.checkOperationStatus operationId=op_reddit123
```

**结果：** 显示子版块列表，包括订阅者数量、描述和活动指标。

---

### 模式 7：高级布尔查询

**用例：** 使用布尔运算符进行精确过滤。

**运算符说明：**
- `AND` — 两个条件都必须满足
- `OR` — 至少有一个条件必须满足
- `NOT` — 排除某个条件
- `"exact phrase"` — 匹配完整短语
- `()` — 对表达式进行分组

**示例：** 查找关于特斯拉的推文，但不包括关于股票的内容**

```bash
mcporter call xpoz.getTwitterPostsByKeywords \
  query="Tesla AND (cars OR vehicles) NOT stock NOT TSLA"
```

**示例：** 查找关于旅行或冒险的 Instagram 帖子**

```bash
mcporter call xpoz.getInstagramPostsByKeywords \
  query="travel OR adventure OR wanderlust"
```

---

### 模式 8：导出结果为 CSV

**用例：** 将大量结果导出以供外部分析。

每次搜索操作都会返回一个 `dataDumpExportOperationId`。使用该 ID 可以导出结果：

```bash
# Step 1: Get search results
mcporter call xpoz.getTwitterPostsByKeywords query="climate change" limit=1000

# Step 2: Poll for results
mcporter call xpoz.checkOperationStatus operationId=op_search123

# Step 3: Export using dataDumpExportOperationId from response
mcporter call xpoz.checkOperationStatus operationId=export_op_abc
```

导出链接将在 `result.url` 字段中提供。

---

## 工具参考

### 搜索帖子

| 工具 | 平台 | 搜索内容 |
|------|----------|------------------|
| `getTwitterPostsByKeywords` | Twitter | 推文和转推 |
| `getInstagramPostsByKeywords` | Instagram | 帖子、Reels（包含标题和字幕） |
| `getRedditPostsByKeywords` | Reddit | 仅帖子 |
| `getRedditCommentsByKeywords` | Reddit | 仅评论 |

**关键参数：**
- `query`（必填）— 搜索关键词（支持布尔运算符）
- `startDate` / `endDate`（可选）— 日期范围（格式：YYYY-MM-DD） |
- `limit`（可选）— 最大结果数量（默认：100 条） |
- `language`（可选）— 语言代码（例如：`en`、`es`） |
- `fields`（可选）— 指定返回的字段（可提高查询性能）

### 查找用户

| 工具 | 平台 | 返回内容 |
|------|----------|-----------------|
| `getTwitterUsersByKeywords` | Twitter | 发布匹配内容的用户 |
| `getInstagramUsersByKeywords` | Instagram | 发布匹配内容的用户 |
| `getRedditUsersByKeywords` | Reddit | 发布匹配内容的用户 |

**关键参数：**
- `query`（必填）— 搜索关键词 |
- `limit`（可选）— 最大用户数量（默认：100 人）

### 查找用户资料

| 工具 | 平台 | 识别方式 |
|------|----------|------------------|
| `getTwitterUser` | Twitter | `username` 或 `id` |
| `getInstagramUser` | Instagram | `username` 或 `id` |
| `getRedditUser` | Reddit | `username` |

**参数：**
- `identifier`（必填）— 用户名或 ID |
- `identifierType`（必填）— 识别方式类型

### 按名称搜索

| 工具 | 平台 | 功能 |
|------|----------|---------|
| `searchTwitterUsers` | Twitter | 通过显示名称查找账户 |
| `searchInstagramUsers` | Instagram | 通过显示名称查找账户 |
| `searchRedditUsers` | Reddit | 通过用户名查找账户 |

**参数：**
- `query`（必填）— 搜索关键词 |
- `limit`（可选）— 最大结果数量

### 辅助工具

| 工具 | 功能 | |
|------|---------| |
| `checkOperationStatus` | 轮询异步操作结果（必填） |
| `checkAccessKeyStatus` | 验证 API 密钥是否已配置 |
| `getRedditSubredditsByKeywords` | 查找与特定主题相关的子版块 |

---

## 重要说明

### ⚠️ 请务必定期轮询结果

**所有搜索工具都会返回一个 `operationId`——您必须调用 `checkOperationStatus` 来获取实际数据。**

```bash
# ❌ WRONG: This doesn't return results immediately
mcporter call xpoz.getTwitterPostsByKeywords query="AI"

# ✅ CORRECT: Poll for results
mcporter call xpoz.getTwitterPostsByKeywords query="AI"
# Returns: { operationId: "op_123" }

mcporter call xpoz.checkOperationStatus operationId=op_123
# Returns: { status: "completed", result: { posts: [...] } }
```

### 🚀 使用 `fields` 参数提升性能

如果您只需要某些字段（例如用户名和粉丝数量），请明确指定：

```bash
mcporter call xpoz.getTwitterUsersByKeywords \
  query="AI startups" \
  fields="username,displayName,followerCount"
```

这样可以减少响应数据量并加快查询速度。

### 📅 日期格式

请始终使用 `YYYY-MM-DD` 格式：

```bash
# ✅ Correct
startDate=2026-01-15

# ❌ Wrong
startDate="Jan 15, 2026"
```

**当前年份为 2026 年**——这对于计算相对日期非常重要。

### 📊 CSV 导出

当数据量较大（超过 1000 条结果）时，可以将其导出为 CSV 格式：
1. 每次搜索都会返回一个 `dataDumpExportOperationId`。
2. 使用 `checkOperationStatus` 轮询该操作 ID。
3. 完成后从 `result.url` 下载 CSV 文件。

### 🔍 布尔查询语法

- `AND`、`OR`、`NOT` 必须大写。
- 使用引号标注完整短语：`"artificial intelligence"`。
- 使用括号分组条件：`(AI OR ML) AND startups`。
**示例：`"climate change" AND (policy OR regulation) NOT conspiracy`。

### 🌍 语言过滤

指定语言代码以获得更准确的结果：

```bash
mcporter call xpoz.getTwitterPostsByKeywords \
  query="football" \
  language=en
```

常用语言代码：`en`、`es`、`fr`、`de`、`pt`、`ja`、`ko`

---

## 示例工作流程

### 工作流程 1：竞争情报

**目标：** 查找过去 30 天内关于竞争对手的提及内容。

```bash
# Search Twitter
mcporter call xpoz.getTwitterPostsByKeywords \
  query="CompetitorName" \
  startDate=2026-01-12 \
  endDate=2026-02-11 \
  limit=500

# Poll results
mcporter call xpoz.checkOperationStatus operationId=op_comp123

# Find who's talking about them
mcporter call xpoz.getTwitterUsersByKeywords \
  query="CompetitorName" \
  limit=100

# Check operation
mcporter call xpoz.checkOperationStatus operationId=op_comp_users456
```

### 工作流程 2：影响者发现

**目标：** 找到健身领域的微影响者。

```bash
# Find Instagram users posting about fitness
mcporter call xpoz.getInstagramUsersByKeywords \
  query="fitness transformation OR workout routine" \
  limit=200

# Poll results
mcporter call xpoz.checkOperationStatus operationId=op_fitness123

# Look up promising profiles for detailed stats
mcporter call xpoz.getInstagramUser \
  identifier=fitnessguru123 \
  identifierType=username
```

### 工作流程 3：社区研究

**目标：** 了解您的目标受众在 Reddit 上的活动情况。

```bash
# Find relevant subreddits
mcporter call xpoz.getRedditSubredditsByKeywords \
  query="startup OR entrepreneur OR indie hacker" \
  limit=50

# Poll results
mcporter call xpoz.checkOperationStatus operationId=op_subs789

# Search posts in those communities
mcporter call xpoz.getRedditPostsByKeywords \
  query="launch AND feedback" \
  startDate=2026-02-01 \
  limit=100

# Check operation
mcporter call xpoz.checkOperationStatus operationId=op_posts456
```

### 工作流程 4：趋势分析

**目标：** 分析产品发布期间的舆论变化。

```bash
# Week before launch
mcporter call xpoz.getTwitterPostsByKeywords \
  query="ProductName" \
  startDate=2026-01-27 \
  endDate=2026-02-03

# Launch week
mcporter call xpoz.getTwitterPostsByKeywords \
  query="ProductName" \
  startDate=2026-02-03 \
  endDate=2026-02-10

# Compare volume, engagement, sentiment
```

---

## 故障排除

### “操作未找到”

您可能使用了无效的 `operationId`。请确保使用的 ID 是搜索请求返回的正确值。

### “访问密钥无效”

您的 API 密钥未配置或已过期：

**解决方法：** 设置 `XPOZ_ACCESS_KEY` 环境变量（详见设置部分）。

### 结果为空

- **检查查询语法** — 布尔运算符必须大写。
- **验证日期范围** — 日期格式必须为 `YYYY-MM-DD`。
- **尝试使用更宽泛的关键词** — 完整短语可能过于具体。

### 查询速度慢

- **使用 `fields` 参数仅请求所需数据**。
- **减少 `limit` 值以加快初始查询速度**。
- **添加日期筛选条件以缩小搜索范围**。

---

## 相关技能

- **[xpoz-marketing](../xpoz-marketing)** — 用于 Xpoz 的内容创作工作流程。
- **[find-influencers](../find-influencers)** — 自动化影响者联系工具。
- **[xpoz-social](../xpoz-social)** — 用于管理 Xpoz 社交媒体渠道的工具。

---

## 资源

- **官方网站：** [xpoz.ai](https://xpoz.ai)
- **MCP 包：** [@xpozinc/xpoz-mcp](https://www.npmjs.com/package/@xpozinc/xpoz-mcp)
- **控制面板：** [xpoz.ai/dashboard](https://xpoz.ai/dashboard)
- **支持：** support@xpoz.ai

---

## 许可证与使用说明

该功能为开源代码。使用 Xpoz MCP 服务器需要 [xpoz.ai](https://xpoz.ai) 提供的免费或付费账户。

**免费 tier 的限制：**
- 每月 100 次搜索
- 每次搜索最多 1,000 条结果
- 支持所有平台

**升级后可享受：**
- 无限次搜索
- 批量导出（每次查询最多 500,000 条结果）
- 查看 2019 年以来的历史数据
- 自定义数据保留策略
- 优先支持

## 负责任的使用

该功能会搜索公开可用的社交媒体数据。使用时应遵守：
- Twitter、Instagram 和 Reddit 的平台服务条款
- 遵守适用于您的地区的隐私法律（如 GDPR、CCPA 等）
- 不得用于骚扰、跟踪或未经授权的监控
- 仅收集满足您使用需求的数据
- 在法律或道德规范要求的情况下公开数据收集情况

Xpoz 仅索引公开可用的帖子和用户资料。无法访问私人消息、受保护账户或非公开数据。

---

**由 ClawHub 开发 • 发布于 2026-02-11**