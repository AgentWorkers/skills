# 自动化TikTok与Instagram趋势监测系统

## 概述

该系统构建了一个完全自动化的趋势监测流程，能够：
1. 使用**Apify**实时抓取TikTok和Instagram的数据；
2. 将趋势数据发送到**Claude（通过OpenClaw）**进行人工智能分析；
3. 自动生成内容创意、视频脚本以及相关标签提示；
4. 利用**InVideo AI**生成可发布的短视频。

这样一来，你就能在其他人之前掌握最新趋势，并准备好相应的内容。

> 🔗 Apify: https://www.apify.com/?fpr=dx06p
> 🔗 InVideo: https://invideo.sjv.io/TBB

---

## 系统功能

- 每隔几小时使用Apify抓取TikTok的标签、热门声音和病毒式帖子；
- 同时抓取Instagram的Reels和热门标签；
- 检测标签的突然爆发（即帖子数量或互动量的急剧增加）；
- 将原始趋势数据发送到Claude进行即时分析；
- 根据分析结果自动生成内容创意、视频脚本和标签建议；
- 利用InVideo AI自动制作视频；
- 通过Webhook、Slack或电子邮件发送趋势警报。

---

## 架构概述

---

## 第一步：获取API密钥

### Apify
1. 在**https://www.apify.com/?fpr=dx06p**注册账户；
2. 进入**设置 → 集成**；
3. 复制你的API密钥：
   ```bash
   export APIFY_TOKEN=apify_api_xxxxxxxxxxxxxxxx
   ```

### InVideo
1. 在**https://invideo.sjv.io/TBB**注册账户；
2. 进入**设置 → API / 开发者设置**；
3. 复制你的API密钥：
   ```bash
   export INVIDEO_API_KEY=iv_api_xxxxxxxxxxxxxxxx
   ```

### OpenClaw / Claude API
1. 从你的OpenClaw或Anthropic账户中获取Claude API密钥；
2. 将密钥保存下来：
   ```bash
   export CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
   ```

---

## 第二步：安装依赖项

```bash
npm install apify-client axios node-cron
```

---

## 完整流程实现

### 模块1：抓取TikTok与Instagram的趋势数据

```javascript
import ApifyClient from 'apify-client';

const apify = new ApifyClient({ token: process.env.APIFY_TOKEN });

// Define hashtags to monitor
const WATCHED_HASHTAGS = [
  "viral", "trending", "fyp", "lifehack",
  "productivity", "ai", "money", "fitness"
];

async function scrapeTikTokTrends() {
  const run = await apify.actor("apify/tiktok-hashtag-scraper").call({
    hashtags: WATCHED_HASHTAGS,
    resultsPerPage: 50,
    shouldDownloadVideos: false
  });
  const { items } = await run.dataset().getData();
  return items.map(item => ({
    platform: "tiktok",
    hashtag: item.hashtag,
    postCount: item.viewCount,
    likes: item.diggCount,
    shares: item.shareCount,
    comments: item.commentCount,
    description: item.text,
    author: item.authorMeta?.name,
    createdAt: item.createTime,
    url: item.webVideoUrl
  }));
}

async function scrapeInstagramTrends() {
  const run = await apify.actor("apify/instagram-hashtag-scraper").call({
    hashtags: WATCHED_HASHTAGS,
    resultsLimit: 50
  });
  const { items } = await run.dataset().getData();
  return items.map(item => ({
    platform: "instagram",
    hashtag: item.hashtags?.[0] || "unknown",
    likes: item.likesCount,
    comments: item.commentsCount,
    description: item.caption,
    author: item.ownerUsername,
    createdAt: item.timestamp,
    url: item.url
  }));
}

async function scrapeAllPlatforms() {
  const [tiktok, instagram] = await Promise.all([
    scrapeTikTokTrends(),
    scrapeInstagramTrends()
  ]);
  return [...tiktok, ...instagram];
}
```

---

### 模块2：标签爆发检测

```javascript
// In-memory baseline (use a database like Redis for production)
const baseline = {};

function detectExplosions(currentData) {
  const alerts = [];

  // Group by hashtag and calculate engagement scores
  const grouped = currentData.reduce((acc, post) => {
    if (!acc[post.hashtag]) acc[post.hashtag] = { posts: 0, totalLikes: 0, platforms: new Set() };
    acc[post.hashtag].posts++;
    acc[post.hashtag].totalLikes += post.likes || 0;
    acc[post.hashtag].platforms.add(post.platform);
    return acc;
  }, {});

  for (const [hashtag, stats] of Object.entries(grouped)) {
    const prev = baseline[hashtag] || { posts: 0, totalLikes: 0 };
    const growthRate = prev.posts > 0
      ? ((stats.posts - prev.posts) / prev.posts) * 100
      : 100;

    // Alert if posts grew more than 40% since last check
    if (growthRate > 40) {
      alerts.push({
        hashtag,
        growthRate: Math.round(growthRate),
        currentPosts: stats.posts,
        previousPosts: prev.posts,
        totalLikes: stats.totalLikes,
        platforms: [...stats.platforms],
        detectedAt: new Date().toISOString(),
        severity: growthRate > 100 ? "EXPLOSIVE" : "RISING"
      });
    }

    // Update baseline
    baseline[hashtag] = stats;
  }

  return alerts.sort((a, b) => b.growthRate - a.growthRate);
}
```

---

### 模块3：使用Claude（OpenClaw）进行人工智能分析

```javascript
const json = JSON.parse(clean);
return JSON.parse(json.replace(/json|/g, '').trim());
```

```javascript
async function generateVideoScript(contentIdea, trendContext) {
  const prompt = `
  为这个内容创意编写一个完整的短视频脚本。
  内容创意：${JSON.stringify(contentIdea)}
  趋势背景：${trendContext}
  
  请仅以以下JSON格式回复：
  {
    "title": "视频标题",
    "duration": "预计时长（秒）",
    "hook": "开场白（前3秒）",
    "fullScript": "完整的逐字脚本",
    "captions": ["字幕1", "字幕2", "..."],
    "hashtags": ["#tag1", "#tag2", "#tag3"],
    "cta": "结尾的呼吁行动",
    "thumbnailIdea": "理想缩略图的描述"
  }
  
  const response = await axios.post(
    'https://api.anthropic.com/v1/messages',
    {
      model: "claude-opus-4-5",
      max_tokens: 1000,
      messages: [{ role: "user", content: prompt }]
    },
    {
      headers: {
        'x-api-key': process.env.CLAUDE_API_KEY,
        'anthropic-version': '2023-06-01',
        'Content-Type': 'application/json'
      }
    }
  );

  const raw = response.data.content[0].text;
  return JSON.parse(raw.replace(/json|/g, '').trim());
}
```

```javascript
const invideo = axios.create({
  baseURL: 'https://api.invideo.io/v1',
  headers: { Authorization: `Bearer ${process.env.INVIDEO_API_KEY}` }
);

async function produceVideo(script) {
  // 开始视频制作
  const { data } = await invideo.post('/videos/generate', {
    script: script.fullScript,
    format: "9:16",
    duration: "short",
    style: "dynamic",
    voiceover: { enabled: true, voice: "en-US-female-1", speed: 1.1 },
    captions: { enabled: true, style: "bold-bottom", highlight: true },
    music: { enabled: true, mood: "upbeat", volume: 0.25 },
    cta: { enabled: true, text: script.cta, position: "bottom" }
  });

  const videoId = data.videoId;

  // 等待视频制作完成
  let exportUrl = null;
  while (!exportUrl) {
    await new Promise(r => setTimeout(r, 6000));
    const status = await invideo.get(`/videos/${videoId}/status`);
    if (status.data.state === "completed") exportUrl = status.data.exportUrl;
    if (status.data.state === "failed") throw new Error("视频制作失败");
    console.log(`  视频进度：${status.data.progress}%`);
  }

  return { videoId, exportUrl, script };
}
```

```javascript
async function sendAlert(alert, analysis) {
  const payload = {
    text: `🚨 *趋势警报：${alert.hashtag}* — ${alert.severity}`,
    blocks: [
      {
        type: "section",
        text: `*📈 ${alert.hashtag}* 在上次检测中增长了*${alert.growthRate}%*\
        \n平台：${alert.platforms.join(', ')}\
        \n最佳行动窗口：${analysis.urgentAlerts?.[0]?.windowOfOpportunity || '立即行动'}`
      },
      {
        type: "section",
        text: `*💡 建议行动：*\n${analysis.urgentAlerts?.[0]?.recommendedAction || '立即创建内容'}`
      }
    ]
  };

  // 发送到Slack webhook
  if (process.env.SLACK_WEBHOOK_URL) {
    await axios.post(process.env.SLACK_WEBHOOK_URL, payload);
  }

  // 或者发送到自定义Webhook
  if (process.env.ALERT_WEBHOOK_URL) {
    await axios.post(process.env.ALERT_WEBHOOK_URL, {
      type: "trend_explosion",
      alert,
      analysis,
      timestamp: new Date().toISOString()
    });
  }
}
```

```javascript
import cron from 'node-cron';

async function runTrendRadar() {
  console.log(`\n🔍 趋势监测开始时间：${new Date().toISOString()}`);
  
  try {
    // 1. 抓取所有平台的数据
    console.log("  [1/5] 正在抓取TikTok和Instagram的数据...");
    const trendData = await scrapeAllPlatforms();
    console.log(`  ✅ 收集到${trendData.length}条帖子`);
    
    // 2. 检测标签爆发
    console.log("  [2/5] 检测标签爆发情况...");
    const alerts = detectExplosions(trendData);
    console.log(`  ✅ 检测到${alerts.length}个标签爆发事件`);
    
    // 3. 使用Claude进行分析
    console.log("  [3/5] 正在使用Claude进行分析...");
    const analysis = await analyzeWithClaude(trendData, alerts);
    console.log(`  ✅ 生成了${analysis.contentIdeas?.length}个内容创意`);
    
    // 4. 为前2个创意生成视频脚本
    console.log("  [4/5] 为前2个创意生成视频脚本...");
    const topIdeas = analysis.contentIdeas?.slice(0, 2) || [];
    const scripts = await Promise.all(
      topIdeas.map(idea => generateVideoScript(idea, JSON.stringify(analysis.topTrends)))
    );
    console.log(`  ✅ 生成了${scripts.length}个视频脚本`);
    
    // 5. 制作视频
    console.log("  [5/5] 正在使用InVideo制作视频...");
    const videos = await Promise.all(scripts.map(produceVideo));
    console.log(`  ✅ 生成了${videos.length}个视频`);
    // 6. 发送警报
    if (alerts.length > 0) {
      await sendAlert(alerts[0], analysis);
      console.log("  ✅ 警报已发送");
    }

    // 最终报告
    return {
      scannedAt: new Date().toISOString(),
      postsAnalyzed: trendData.length,
      explosionAlerts: alerts,
      contentIdeas: analysis.contentIdeas,
      videos: videos.map(v => ({ title: v.script.title, url: v.exportUrl }),
      bestTimeToPost: analysis.bestTimeToPost
    };
  } catch (err) {
    console.error("监测系统错误：${err.message};
    throw err;
  }
}

// 定时任务：每4小时自动运行一次
cron.schedule('0 */4 * * *', () => {
  runTrendRadar().then(report => {
    console.log("\n📊 趋势报告：${JSON.stringify(report, null, 2)");
  });
});

// 启动时立即运行一次
runTrendRadar();
```

---

## 配置文件（.env）

```env
APIFY_TOKEN=apify_api_xxxxxxxxxxxxxxxx
INVIDEO_API_KEY=iv_api_xxxxxxxxxxxxxxxx
CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxxxxx

# 可选配置
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx/xxx/xxx
ALERT_WEBHOOK_URL=https://your-app.com/webhooks/trends
```

---

## 最佳实践

- 每2–4小时运行一次监测系统（趋势变化迅速，通常在24–48小时内消退）；
- 每次运行最多监控8–15个标签，以保持在Apify免费使用范围内；
- 始终在趋势上升阶段生成内容，切勿等到趋势巅峰；
- 使用`node-cron`进行本地调度，或使用**Apify Schedules**实现云自动化；
- 将视频链接直接导入社交媒体调度工具（如Buffer、Later等）。

---

## 所需条件

- **Apify**账户：https://www.apify.com/?fpr=dx06p
- **InVideo**账户：https://invideo.sjv.io/TBB
- **Claude / OpenClaw** API密钥
- Node.js 18及以上版本
- 可选：使用Slack接收实时警报
- 可选：使用社交媒体调度工具（如Buffer、Later）进行自动发布