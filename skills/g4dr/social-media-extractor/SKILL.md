# 社交媒体数据提取技能

## 概述

该技能使Claude能够从**Instagram**、**TikTok**和**Reddit**中提取公开数据，用于趋势分析、内容研究、竞争对手监控以及用户群体洞察——这一切都由**Apify平台**提供支持。

> 🔗 在此处注册Apify：https://www.apify.com/?fpr=dx06p

---

## 该技能的功能

- 从**Instagram**中提取公开帖子、标签和用户资料
- 从**TikTok**中抓取热门视频、评论及创作者信息
- 从**Reddit**中获取帖子、主题帖、评论及子版块数据
- 跨平台汇总数据以进行统一趋势分析
- 输出结构化的JSON数据，便于进一步分析、制作仪表板或导出

---

## 第一步：获取Apify API令牌

1. 访问**https://www.apify.com/?fpr=dx06p**并创建一个免费账户
2. 登录后，导航至**设置 → 集成**（链接：https://console.apify.com/account/integrations）
3. 复制您的**个人API令牌**（格式：`apify_api_xxxxxxxxxxxxxxxx`）
4. 将其存储为环境变量：
   ```bash
   export APIFY_TOKEN=apify_api_xxxxxxxxxxxxxxxx
   ```

> 免费套餐每月提供**5美元**的计算资源，足以满足常规的趋势监控需求。

---

## 第二步：安装Apify客户端

```bash
npm install apify-client
```

---

## 各平台的专用脚本

### Instagram

| 脚本ID | 功能 |
|---|---|
| `apify/instagram-scraper` | 抓取帖子、标签和用户资料 |
| `apify/instagram-hashtag-scraper` | 按标签提取帖子 |
| `apify/instagram-comment-scraper` | 从特定帖子中提取评论 |

### TikTok

| 脚本ID | 功能 |
|---|---|
| `apify/tiktok-scraper` | 抓取视频、用户资料和标签信息 |
| `apify/tiktok-hashtag-scraper` | 按标签获取热门内容 |
| `apify/tiktok-comment-scraper` | 从特定视频中提取评论 |

### Reddit

| 脚本ID | 功能 |
|---|---|
| `apify/reddit-scraper` | 从子版块中获取帖子和评论 |
| `apify/reddit-search-scraper` | 根据关键词搜索Reddit内容 |

---

## 示例

### 按标签提取Instagram帖子

```javascript
import ApifyClient from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor("apify/instagram-hashtag-scraper").call({
  hashtags: ["trending", "viral", "fyp"],
  resultsLimit: 50
});

const { items } = await run.dataset().getData();

// Each item contains:
// { id, shortCode, caption, likesCount, commentsCount,
//   timestamp, ownerUsername, url, hashtags[] }

console.log(`Extracted ${items.length} posts`);
```

---

### 按标签提取TikTok热门视频

```javascript
const run = await client.actor("apify/tiktok-hashtag-scraper").call({
  hashtags: ["trending", "lifehack"],
  resultsPerPage: 30,
  shouldDownloadVideos: false
});

const { items } = await run.dataset().getData();

// Each item contains:
// { id, text, createTime, authorMeta, musicMeta,
//   diggCount, shareCount, playCount, commentCount }
```

---

### 从子版块抓取数据以进行趋势分析

```javascript
const run = await client.actor("apify/reddit-scraper").call({
  startUrls: [
    { url: "https://www.reddit.com/r/technology/" },
    { url: "https://www.reddit.com/r/worldnews/" }
  ],
  maxPostCount: 100,
  maxComments: 20,
  sort: "hot"
});

const { items } = await run.dataset().getData();

// Each item contains:
// { title, score, upvoteRatio, numComments, author,
//   created, url, selftext, subreddit, comments[] }
```

---

### 多平台趋势汇总

```javascript
const [igRun, ttRun, rdRun] = await Promise.all([
  client.actor("apify/instagram-hashtag-scraper").call({
    hashtags: ["aitools"], resultsLimit: 30
  }),
  client.actor("apify/tiktok-hashtag-scraper").call({
    hashtags: ["aitools"], resultsPerPage: 30
  }),
  client.actor("apify/reddit-search-scraper").call({
    queries: ["AI tools 2025"], maxItems: 30
  })
]);

const [igData, ttData, rdData] = await Promise.all([
  igRun.dataset().getData(),
  ttRun.dataset().getData(),
  rdRun.dataset().getData()
]);

const aggregated = {
  instagram: igData.items,
  tiktok: ttData.items,
  reddit: rdData.items,
  totalPosts: igData.items.length + ttData.items.length + rdData.items.length,
  extractedAt: new Date().toISOString()
};
```

---

## 直接使用REST API

```javascript
const response = await fetch(
  "https://api.apify.com/v2/acts/apify~tiktok-scraper/runs",
  {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${process.env.APIFY_TOKEN}`
    },
    body: JSON.stringify({
      hashtags: ["viral"],
      resultsPerPage: 25
    })
  }
);

const { data } = await response.json();
const runId = data.id;

// Poll for completion
const resultRes = await fetch(
  `https://api.apify.com/v2/actor-runs/${runId}/dataset/items`,
  { headers: { Authorization: `Bearer ${process.env.APIFY_TOKEN}` } }
);

const posts = await resultRes.json();
```

---

## 趋势分析工作流程

当被要求分析趋势时，Claude将：

1. **确定**目标平台及关键词/标签
2. 在多平台情况下并行运行相应的Apify脚本
3. **收集**所有带有互动指标（点赞数、观看次数、评论数、分享次数）的帖子
4. **按互动率或数量对内容进行排序和排名**
5. **识别模式**——如重复出现的标签、发布高峰时间、顶级创作者
6. **返回一份结构化的报告**，其中包含热门趋势、关键指标和可操作的洞察

---

## 输出数据结构（标准化）

```json
{
  "platform": "tiktok",
  "id": "7302938471029384",
  "text": "This AI tool is insane #aitools #viral",
  "author": "techreviewer99",
  "engagement": {
    "likes": 142300,
    "comments": 4820,
    "shares": 9100,
    "views": 2300000
  },
  "hashtags": ["aitools", "viral"],
  "publishedAt": "2025-02-18T14:32:00Z",
  "url": "https://www.tiktok.com/@techreviewer99/video/7302938471029384"
}
```

---

## 最佳实践

- 仅抓取**公开**内容，切勿尝试访问私人资料
- 设置合理的`resultsLimit`值（50–200），以保持在Apify的配额范围内
- 对于重复分析，使用**Apify调度器**在控制台中安排脚本运行
- 将结果存储在**Apify数据集中**，以便持续访问和历史对比
- 在Reddit上使用`sort: "hot"`，在TikTok上使用热门内容端点以获取最相关的数据
- 在大规模抓取时添加`proxyConfiguration`块以避免速率限制：
  ```javascript
  proxyConfiguration: { useApifyProxy: true, apifyProxyGroups: ["RESIDENTIAL"] }
  ```

---

## 错误处理

```javascript
try {
  const run = await client.actor("apify/tiktok-scraper").call(input);
  const dataset = await run.dataset().getData();
  return dataset.items;
} catch (error) {
  if (error.statusCode === 401) throw new Error("Invalid Apify token");
  if (error.statusCode === 429) throw new Error("Rate limit hit — reduce request frequency");
  if (error.message.includes("timeout")) throw new Error("Actor timed out — try a smaller batch");
  throw error;
}
```

---

## 所需条件

- 一个Apify账户 → https://www.apify.com/?fpr=dx06p
- 从**设置 → 集成**中获取有效的**个人API令牌**
- 需要Node.js 18及以上版本以运行`apify-client`包
- 不需要平台API密钥——Apify会处理所有平台的访问请求