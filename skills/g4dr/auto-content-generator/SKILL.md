# 自动化内容生成管道技能

## 概述

该技能构建了一个全天候运行的**完全自动化内容生成系统**：
1. **Apify** 从 TikTok、Instagram、YouTube 和 Reddit 等平台抓取最热门的内容。
2. **Claude (OpenClaw)** 提取这些内容的核心元素（即“钩子”），反向工程分析其走红的原因，并生成相应的脚本、标题、轮播图和帖子结构。
3. 一个**调度器** 将所有内容批量处理并安排自动发布。

最终结果：一个几乎完全自动化的内容生成渠道。

> 🔗 Apify: https://www.apify.com/?fpr=dx06p

---

## 该技能的功能

- **每隔几小时** 从多个平台抓取最热门的内容。
- **提取** 使内容走红的关键元素（如钩子、结构和格式）。
- **将这些热门内容重新利用**，生成原创的脚本、标题、轮播图和帖子。
- **自动生成** 每周的内容日程安排。
- **批量处理并安排** 在 Instagram、TikTok、LinkedIn 和 Twitter/X 等平台发布内容。
- **跟踪** 哪些内容效果最好，并将这些信息反馈回系统。
- **配置完成后** 可以**完全自主运行**，几乎不需要人工干预。

---

## 架构概述

---

## 第一步 — 获取 API 密钥

### Apify
1. 在 **https://www.apify.com/?fpr=dx06p** 注册账户。
2. 进入 **设置 → 集成**。
3. 复制你的 API 密钥：
   ```bash
   export APIFY_TOKEN=apify_api_xxxxxxxxxxxxxxxx
   ```

### Claude / OpenClaw
1. 从你的 OpenClaw 或 Anthropic 账户中获取 API 密钥。
2. 将其存储起来：
   ```bash
   export CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
   ```

---

## 第二步 — 安装依赖项

```bash
npm install apify-client axios node-cron dotenv
```

---

## 第一层 — 热门内容抓取器（Apify）

```javascript
import ApifyClient from 'apify-client';

const apify = new ApifyClient({ token: process.env.APIFY_TOKEN });

// Define your niche and topics
const NICHE_TOPICS = [
  "productivity", "entrepreneurship", "ai tools",
  "personal finance", "self improvement", "marketing"
];

async function scrapeViralContent() {
  console.log("🔍 Scraping viral content...");

  const [tiktok, instagram, reddit] = await Promise.all([

    // TikTok — top videos by hashtag
    apify.actor("apify/tiktok-hashtag-scraper").call({
      hashtags: NICHE_TOPICS,
      resultsPerPage: 30,
      shouldDownloadVideos: false
    }).then(run => run.dataset().getData()),

    // Instagram — top posts by hashtag
    apify.actor("apify/instagram-hashtag-scraper").call({
      hashtags: NICHE_TOPICS,
      resultsLimit: 30
    }).then(run => run.dataset().getData()),

    // Reddit — hottest posts in relevant subreddits
    apify.actor("apify/reddit-scraper").call({
      startUrls: [
        { url: "https://www.reddit.com/r/Entrepreneur/" },
        { url: "https://www.reddit.com/r/productivity/" },
        { url: "https://www.reddit.com/r/personalfinance/" }
      ],
      maxPostCount: 20,
      sort: "hot"
    }).then(run => run.dataset().getData())

  ]);

  // Normalize all platforms to a common schema
  const normalized = [
    ...tiktok.items.map(p => ({
      platform: "tiktok",
      text: p.text,
      likes: p.diggCount,
      shares: p.shareCount,
      comments: p.commentCount,
      views: p.playCount,
      engagementScore: (p.diggCount + p.shareCount * 3 + p.commentCount * 2),
      url: p.webVideoUrl,
      author: p.authorMeta?.name
    })),
    ...instagram.items.map(p => ({
      platform: "instagram",
      text: p.caption,
      likes: p.likesCount,
      comments: p.commentsCount,
      engagementScore: (p.likesCount + p.commentsCount * 2),
      url: p.url,
      author: p.ownerUsername
    })),
    ...reddit.items.map(p => ({
      platform: "reddit",
      text: p.title + " " + (p.selftext || ""),
      likes: p.score,
      comments: p.numComments,
      engagementScore: (p.score + p.numComments * 3),
      url: p.url,
      author: p.author
    }))
  ];

  // Return top 20 by engagement score
  return normalized
    .sort((a, b) => b.engagementScore - a.engagementScore)
    .slice(0, 20);
}
```

---

## 第二层 — AI 内容引擎（Claude / OpenClaw）

### 钩子提取器

```javascript
import axios from 'axios';

const claude = axios.create({
  baseURL: 'https://api.anthropic.com/v1',
  headers: {
    'x-api-key': process.env.CLAUDE_API_KEY,
    'anthropic-version': '2023-06-01',
    'Content-Type': 'application/json'
  }
});

async function extractHooks(viralPosts) {
  const prompt = `
You are an expert viral content analyst.

Analyze these top-performing posts and extract the exact patterns that made them go viral.

VIRAL POSTS:
${JSON.stringify(viralPosts.slice(0, 10), null, 2)}

Respond ONLY in this JSON format, no preamble:
{
  "hookPatterns": [
    {
      "pattern": "pattern name",
      "template": "reusable template with [BRACKETS] for variables",
      "example": "real example from the data",
      "whyItWorks": "psychological reason this triggers engagement",
      "bestPlatforms": ["tiktok", "instagram"]
    }
  ],
  "commonStructures": [
    {
      "format": "format name (list | storytime | tutorial | controversy | etc)",
      "openingFormula": "how these posts start",
      "bodyFormula": "how they build",
      "closingFormula": "how they end / CTA",
      "avgEngagementBoost": "estimated % above average"
    }
  ],
  "topEmotions": ["curiosity", "surprise", "..."],
  "keyInsight": "single most important lesson from this batch of viral content"
}
`;

  const { data } = await claude.post('/messages', {
    model: "claude-opus-4-5",
    max_tokens: 2000,
    messages: [{ role: "user", content: prompt }]
  });

  return JSON.parse(data.content[0].text.replace(/```json|```/g, '').trim());
}
```

---

### Script Generator

```javascript
async function generateScripts(hookAnalysis, niche, count = 5) {
  const prompt = `
你是一个内容创作者。使用这些经过验证的钩子模式来生成 ${count} 个原创视频脚本。

主题：${niche}
钩子模式：${JSON.stringify(hookAnalysis.hookPatterns, null, 2)}
最佳结构：${JSON.stringify(hookAnalysis.commonStructures, null, 2)}

请仅以以下 JSON 格式回复：
{
  "scripts": [
    {
      "id": 1,
      "title": "视频标题",
      "platform": "tiktok | instagram | youtube_shorts",
      "hookPattern": "使用的钩子模式",
      "hook": "开头语句 — 前 3 秒",
      "fullScript": "完整的逐字脚本（120-180 字）",
      "estimatedDuration": "30秒",
      "hashtags": ["#tag1", "#tag2", "#tag3", "#tag4", "#tag5"],
      "cta": "行动号召",
      "thumbnailIdea": "缩略图创意",
      "viralPotential": "高 | 中等",
      "bestPostTime": "上午 | 下午 | 晚上"
    }
  ]
}
};

  const { data } = await claude.post('/messages', {
    model: "claude-opus-4-5",
    max_tokens: 3000,
    messages: [{ role: "user", content: prompt }]
  };

  return JSON.parse(data.content[0].text.replace(/```json|```/g, '').trim());
}
```

---

### Caption & Post Writer

```javascript
async function generatePostCaptions(scripts) {
  const prompt = `
将这些视频脚本转换为适合各个平台的社交媒体标题。

脚本：${JSON.stringify(scripts, null, 2)}

请仅以以下 JSON 格式回复：
{
  "posts": [
    {
      "scriptId": 1,
      "platforms": {
        "instagram": {
          "caption": "包含换行符和表情符号的完整标题",
          "hashtags": ["#tag1", "#tag2"],
          "firstComment": "要放在第一条评论中的标签"
        },
        "tiktok": {
          "caption": "简短有力的 TikTok 标题",
          "hashtags": ["#fyp", "#tag2"]
        },
        "linkedin": {
          "caption": "同一内容的专业版，150-200 字",
          "hashtags": ["#tag1"]
        },
        "twitter": {
          "thread": [
            "推文 1 (钩子)",
            "推文 2",
            "推文 3",
            "推文 4 (行动号召)"
          ]
        }
      }
    }
  ]
};

  const { data } = await claude.post('/messages', {
    model: "claude-opus-4-5",
    max_tokens: 3000,
    messages: [{ role: "user", content: prompt }]
  });

  return JSON.parse(data.content[0].text.replace(/```json|```/g, '').trim());
}
```

---

### Weekly Content Calendar Builder

```javascript
async function buildContentCalendar(scripts, captions) {
  const today = new Date();
  const days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday';

  const prompt = `
根据这些生成的帖子制定一个 7 天的内容日程安排。
通过在不同的平台和时间智能分配内容来最大化传播效果。

可用内容：
脚本：${scripts.scripts.length} 个视频脚本
标题：已为 Instagram、TikTok、LinkedIn、Twitter 准备好

今天是 ${today.toDateString()}。

请仅以以下 JSON 格式回复：
{
  "calendar": [
    {
      "day": "Monday",
      "date": "YYYY-MM-DD",
      "posts": [
        {
          "time": "08:00",
          "platform": "instagram",
          "contentType": "reel | carousel | story | post",
          "scriptId": 1,
          "caption": "标题预览",
          "hashtags": ["#tag1"],
          "status": "已安排",
          "notes": "此帖子的建议"
        }
      ]
    }
  ],
  "weekSummary": {
    "totalPosts": 0,
    "platformBreakdown": { "instagram": 0, "tiktok": 0, "linkedin": 0, "twitter": 0 },
    "estimatedReach": "大致估算",
    "bestDayToPost": "最佳发布日",
    "strategy": "本周策略的简要总结"
  }
};
};

  const { data } = await claude.post('/messages', {
    model: "claude-opus-4-5",
    max_tokens: 3000,
    messages: [{ role: "user", content: prompt }]
  });

  return JSON.parse(data.content[0].text.replace(/```json|```/g, '').trim());
}
```

---

## Layer 3 — Scheduled Publisher

```javascript
async function publishToSchedulercalendar) {
  // 示例：发送到 Buffer API
  const BUFFER_TOKEN = process.env.BUFFER_ACCESS_TOKEN;

  for (const day of calendar.calendar) {
    for (const post of day.posts) {
      const scheduledTime = new Date(`${day.date}T${post.time}:00`);
      if (BUFFER_TOKEN) {
        await axios.post(
          'https://api.bufferapp.com/1/updates/create.json',
          {
            text: post.caption,
            profile_ids: [process.env[`BUFFER_${post.platform.toUpperCase()}_ID`]],
            scheduled_at: scheduledTime.toISOString(),
            hashtags: post.hashtags.join(' ')
          },
          { headers: { Authorization: `Bearer ${BUFFER_TOKEN}` } }
        );
      }

      // 或者推送到你自己的 webhook / CMS
      if (process.env.PUBLISH_WEBHOOK_URL) {
        await axios.post(process.env.PUBLISH_WEBHOOK_URL, {
          platform: post.platform,
          caption: post.caption,
          hashtags: post.hashtags,
          scheduledAt: scheduledTime.toISOString(),
          scriptId: post.scriptId
        });
      }

      console.log(`✅ 已安排：[${post.platform}] ${day.date} ${post.time}`);
    }
  }
}
```

---

## Master Orchestrator — Full Automated Pipeline

```javascript
import cron from 'node-cron';

async function runContentPipeline(niche = "entrepreneurship") {
  console.log(`\n🏭 内容管道已启动 — ${new Date().toISOString()}`);
  const report = {};

  try {
    // 第一步 — 抓取热门内容
    console.log("\n[1/5] 使用 Apify 抓取热门内容...");
    const viralContent = await scrapeViralContent();
    report.postsScraped = viralContent.length;
    console.log(`  ✅ 收集到 ${viralContent.length} 条热门内容`);
    
    // 第二步 — 提取钩子和模式
    console.log("\n[2/5] 使用 Claude 提取热门内容的钩子...");
    const hookAnalysis = await extractHooks(viralContent);
    report.hookPatterns = hookAnalysis.hookPatterns.length;
    console.log(`  ✅ 识别出 ${hookAnalysis.hookPatterns} 个钩子模式`);
    console.log(`  💡 关键洞察：${hookAnalysis.keyInsight}`);
    
    // 第三步 — 生成脚本
    console.log("\n[3/5] 生成视频脚本...");
    const scripts = await generateScripts(hookAnalysis, niche, 7);
    report.scriptsGenerated = scripts.scripts.length;
    console.log(`  ✅ 生成了 ${scripts.scripts.length} 个脚本`);
    
    // 第四步 — 为所有平台编写标题
    console.log("\n[4/5] 为所有平台编写标题...");
    const captions = await generatePostCaptions(scripts.scripts);
    report.captionsWritten = captions.posts.length;
    console.log(`  ✅ 为 ${captions.posts.length} 条帖子编写了标题`);
    
    // 第五步 — 制定每周日程安排
    console.log("\n[5/5] 制定内容日程并安排发布...");
    const calendar = await buildContentCalendar(scripts, captions);
    reportcalendarBuilt = true;
    report.totalPostsScheduled = calendar.weekSummary.totalPosts;
    await publishToScheduler(calendar);
    console.log(`  ✅ 本周已安排发布 ${report.totalPosts} 条帖子`);
    // 总结
    console.log("\n📊 管道完成:");
    console.log(`  • 收集到的热门帖子数量：${report.postsScraped}`);
    console.log(`  • 识别的钩子模式数量：${report.hookPatterns}`);
    console.log(`  • 生成的脚本数量：${report.scriptsGenerated}`);
    console.log(`  • 已安排的帖子数量：${report.totalPostsScheduled}`);
    console.log(`  • 本周最佳发布日：${calendar.weekSummary.bestDayToPost}`);
    console.log(`  • 策略：${calendar.weekSummary.strategy}`);
    return { success: true, report, calendar };
  } catch (err) {
    console.error("管道错误:", err.message);
    throw err;
  }
}

// 每周日在上午 8:00 运行 — 生成未来一周的内容
cron.schedule('0 8 * * 0', () => {
  runContentPipeline("entrepreneurship");
});

// 每天早上 6:00 运行 — 生成当天的新鲜内容
cron.schedule('0 6 * * *', () => {
  runContentPipeline("productivity");
});

// 启动时立即运行
runContentPipeline("ai tools");
```

---

## Environment Variables

```bash
# .env
APIFY_TOKEN=apify_api_xxxxxxxxxxxxxxxx
CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxxxxx

# 发布（可选 — 选择一个或多个）
BUFFER_ACCESS_TOKEN=your_buffer_token
BUFFER_INSTAGRAM_ID=your_ig_profile_id
BUFFER_TIKTOK_ID=your_tiktok_profile_id
BUFFER(LinkEDIN_ID=your_linkedin_profile_id
PUBLISH_WEBHOOK_URL=https://your-app.com/webhooks/publish

# 通知（可选）
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx/xxx/xxx
```

---

## Normalized Pipeline Output Schema

```json
{
  "runAt": "2025-02-25T06:00:00Z",
  "niche": "entrepreneurship",
  "postsScraped": 90,
  "hookPatterns": 6,
  "scriptsGenerated": 7,
  "totalPostsScheduled": 21,
  "calendar": {
    "Monday": [
      { "time": "08:00", "platform": "instagram", "type": "reel", "scriptId": 1 },
      { "time": "18:00", "platform": "tiktok",    "type": "video", "scriptId": 1 },
      { "time": "12:00", "platform": "linkedin",  "type": "post",  "scriptId": 2 }
    ],
    "weekSummary": {
      "totalPosts": 21,
      "platformBreakdown": {
        "instagram": 7, "tiktok": 7, "linkedin": 4, "twitter": 3
    },
    "bestDayToPost": "Tuesday",
    "strategy": "在周初使用 TikTok 上的引人好奇心的钩子开头，中间使用 LinkedIn 的见解，周末使用互动性强的帖子结尾"
  }
}
```

---

## 最佳实践

- **广泛抓取，精准发布** — 收集 50 多条热门内容，生成 5–7 个原创内容。
- **切勿复制** — 仅将热门内容作为结构灵感使用，始终生成原创文本。
- 将 `cron` 设置为在 **每周日晚上** 运行，以预先生成未来一周的内容。
- 最多使用 **3–5 个主题**，以保持内容的专注性和受众的增长。
- 跟踪哪些帖子效果最好，并将这些信息反馈给系统作为额外的参考。
- 结合 **Trend Radar 技能**，将实时趋势数据融入管道中。
- 为了实现最大程度的自动化，可以将生成的脚本连接到 **InVideo**（参见 Short Video Creator 技能）。

---

## 所需条件

- **Apify** 账户 → https://www.apify.com/?fpr=dx06p
- **Claude / OpenClaw** API 密钥
- Node.js 18+ 及相关依赖库（`apify-client`、`axios`、`node-cron`）
- 可选：Buffer、Later 或 Hootsuite 账户用于自动发布
- 可选：InVideo 账户，用于根据生成的脚本自动生成视频

---

---

（由于文件内容较长，此处仅展示了部分代码和注释。完整文件请参考原始 SKILL.md 文件。）