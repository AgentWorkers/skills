---
name: reddit-insights
description: |
  Search and analyze Reddit content using semantic AI search via reddit-insights.com MCP server.
  Use when you need to: (1) Find user pain points and frustrations for product ideas, (2) Discover niche markets or underserved needs, (3) Research what people really think about products/topics, (4) Find content inspiration from real discussions, (5) Analyze sentiment and trends on Reddit, (6) Validate business ideas with real user feedback.
  Triggers: reddit search, find pain points, market research, user feedback, what do people think about, reddit trends, niche discovery, product validation.
---

# Reddit Insights MCP

这是一个能够对数百万条Reddit帖子进行语义搜索的工具。与关键词搜索不同，它能够理解用户的意图和帖子的真实含义。

## 设置

### 1. 获取API密钥（免费 tier 可用）
1. 访问 https://reddit-insights.com 注册
2. 进入设置 → API
3. 复制您的API密钥

### 2. 安装MCP服务器

**对于Claude Desktop** - 添加到 `claude_desktop_config.json` 文件中：
```json
{
  "mcpServers": {
    "reddit-insights": {
      "command": "npx",
      "args": ["-y", "reddit-insights-mcp"],
      "env": {
        "REDDIT_INSIGHTS_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**对于Clawdbot** - 添加到 `config/mcporter.json` 文件中：
```json
{
  "mcpServers": {
    "reddit-insights": {
      "command": "npx reddit-insights-mcp",
      "env": {
        "REDDIT_INSIGHTS_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**验证安装：**
```bash
mcporter list reddit-insights
```

## 可用工具

| 工具 | 功能 | 关键参数 |
|------|---------|------------|
| `reddit_search` | 对帖子进行语义搜索 | `query`（自然语言查询），`limit`（1-100） |
| `reddit_list_subreddits` | 浏览可用的子版块 | `page`，`limit`，`search` |
| `reddit_get_subreddit` | 获取子版块详情及最新帖子 | `subreddit`（不包括前缀r/） |
| `reddit_get_trends` | 获取热门话题 | `filter`（最新/今日/本周/本月），`category` |

## 性能说明

- **响应时间：** 12-25秒（取决于查询的复杂度）
  - 简单查询：约12-15秒
  - 复杂的语义查询：约17-20秒
  - 高负载时段：最长可达25秒
- **最佳效果：** 适用于特定产品、涉及情感表达的查询，以及需要比较的查询
- **效果较差的查询：** 涉及抽象概念、非英语内容的查询，或通用商业术语的查询
- **最佳使用场景：** 适合在Reddit上人们会提出的问题

## 经过测试的最佳使用案例

| 使用场景 | 效果 | 原因 |
|----------|--------------|-----|
| 产品对比（A vs B） | ⭐⭐⭐⭐⭐ | Reddit用户喜欢讨论产品优劣 |
| 工具/应用推荐 | ⭐⭐⭐⭐⭐ | 这类问题通常具有较高的讨论热度 |
| 业余副业/财务相关话题 | ⭐⭐⭐⭐⭐ | 这些话题的社区参与度较高 |
| 发现用户痛点 | ⭐⭐⭐⭐ | 涉及情感表达的帖子更容易被搜索到 |
| 健康相关问题 | ⭐⭐⭐⭐ | 健康相关的子版块活跃度较高 |
| 技术教程 | ⭐⭐⭐ | 应在特定子版块中进行搜索 |
| 抽象的市场研究 | ⭐⭐ | 这类问题较难通过语义搜索得到准确结果 |
| 非英语查询 | ⭐ | Reddit主要以英语为主 |

## 经过实际数据测试的查询策略

### ✅ 高效的查询（相关性0.70以上）

**产品对比**（效果最佳！）：
```
"Notion vs Obsidian for note taking which one should I use"
→ Relevance: 0.72-0.81 | Found: Detailed comparison discussions, user experiences

"why I switched from Salesforce to HubSpot honest experience"  
→ Relevance: 0.70-0.73 | Found: Migration stories, feature comparisons
```

**业余副业/财务相关话题：**
```
"side hustle ideas that actually make money not scams"
→ Relevance: 0.70-0.77 | Found: Real experiences, specific suggestions
```

**细分领域应用研究：**
```
"daily horoscope apps which one is accurate and why"
→ Relevance: 0.67-0.72 | Found: App recommendations, feature requests
```

### ✅ 较好的查询（相关性0.60-0.69）

**发现用户痛点：**
```
"I hate my current CRM it is so frustrating"
→ Relevance: 0.60-0.64 | Found: Specific CRM complaints, feature wishlists

"cant sleep at night tried everything what actually works"
→ Relevance: 0.60-0.63 | Found: Sleep remedies discussions, medical advice seeking
```

**工具评估：**
```
"AI tools that actually save time not just hype"
→ Relevance: 0.64-0.65 | Found: Real productivity gains, tool recommendations
```

### ✌ 应避免的无效查询模式

- **过于抽象的查询**：难以被准确理解
- **非英语查询**：Reddit主要使用英语

### 查询公式速查表

| 目标 | 查询模式 | 相关性 |
|------|---------|-----------|
| 比较产品 | “[产品A] 和 [产品B]，我应该使用哪个？” | 0.70-0.81 |
| 了解用户转换原因 | “我为什么从[A]切换到[B]？” | 0.70-0.73 |
| 金融/副业相关话题 | “[某个主题]真的有效/能赚钱，而不是骗局/炒作？” | 0.70-0.77 |
| 应用推荐 | “[某个类别]中哪个应用最准确/最好，为什么？” | 0.67-0.72 |
| 描述问题 | “我讨厌现在的[工具]，因为它太[令人沮丧/效率低下]” | 0.60-0.64 |
| 寻找解决方案 | “[某个问题]，我尝试过所有方法，什么方法真正有效？” | 0.60-0.63 |

## 响应内容

每个搜索结果包含以下信息：
- `title`，`content` - 帖子内容
- `subreddit` - 帖子来源的子版块
- `upvotes`，`comments` - 用户互动情况
- `relevance`（0-1） - 语义匹配得分（0.5以上表示匹配度较高，0.6以上表示匹配度非常好）
- `sentiment` - 帖子的类型（讨论、问答、故事分享、原创内容或新闻）
- `url` - 帖子的Reddit链接

**示例响应：**
```json
{
  "id": "1oecf5e",
  "title": "Trying to solve the productivity stack problem",
  "content": "The perfect productivity app doesn't exist. No single app can do everything well, so we use a stack of apps. But this creates another problem: multi app fragmentation...",
  "subreddit": "productivityapps",
  "upvotes": 1,
  "comments": 0,
  "relevance": 0.631,
  "sentiment": "Discussion",
  "url": "https://reddit.com/r/productivityapps/comments/1oecf5e"
}
```

## 使用技巧

1. **使用自然语言提问** - 尽量像人类一样提问
2. **提供上下文** - 添加如“对于小型企业”或“作为开发者”等关键词，可以提高搜索效果
3. **使用情感词汇** - 如“沮丧”、“喜欢”、“讨厌”、“希望”等词汇，有助于获取更具体的反馈
4. **根据互动情况筛选结果** - 高点赞数/高评论数的帖子往往反映了真实的问题
5. **多角度搜索** - 同一主题在不同子版块可能有不同的讨论结果

## 示例工作流程

**寻找SaaS产品机会：**
1. 使用 `reddit_search`：搜索“对远程团队的项目管理工具感到不满”
2. 筛选互动度高的结果
3. 识别用户反复抱怨的问题，从而发现潜在的产品机会

**验证想法：**
1. 使用 `reddit_search`：搜索“[你的产品类别]的相关推荐”
2. 查看用户提到的替代方案
3. 发现现有解决方案中的不足之处

**内容研究：**
1. 使用 `reddit_get_subreddit` 获取目标子版块的帖子
2. 使用 `reddit_search` 查找相关问题或讨论
3. 根据用户需求创建有价值的内容