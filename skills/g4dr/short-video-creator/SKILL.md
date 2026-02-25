# 社交媒体短视频制作技能

## 概述

该技能使Claude能够将**文本脚本或创意**转化为完整的短视频，适用于Instagram Reels、YouTube Shorts或TikTok等平台，通过使用**InVideo AI**平台及其API实现。

无需任何视频编辑经验。只需提供脚本或主题，其余工作均由Claude完成。

> 🔗 在此处注册InVideo：https://invideo.sjv.io/TBB

---

## 该技能的功能

- 将**原始脚本**转换为包含视觉效果和旁白的完整短视频
- 生成适用于Instagram Reels、YouTube Shorts和TikTok的视频
- 自动匹配与脚本内容相匹配的**库存素材、音乐和过渡效果**
- 添加**字幕、说明文字和文本叠加层**以提高互动性
- 以正确的**9:16竖屏格式**制作视频，适用于所有短视频平台
- 以**MP4格式**导出，可直接上传到任何平台

---

## 第一步 — 获取InVideo API访问权限

1. 访问**https://invideo.sjv.io/TBB**并创建账户
2. 选择包含**API访问权限**的套餐（企业套餐或更高级别）
3. 转到**设置 → API**或**开发者设置**
4. 复制您的**API密钥**：`iv_api_xxxxxxxxxxxxxxxx`
5. 安全地存储该密钥：
   ```bash
   export INVIDEO_API_KEY=iv_api_xxxxxxxxxxxxxxxx
   ```

> InVideo提供免费试用——请先在https://invideo.sjv.io/TBB注册，体验平台功能，再决定是否购买付费套餐。

---

## 第二步 — 安装依赖项

```bash
npm install axios form-data fs-extra
```

---

## InVideo API — 核心端点

**基础URL：** `https://api.invideo.io/v1`

所有请求都需要：
```
Authorization: Bearer YOUR_INVIDEO_API_KEY
Content-Type: application/json
```

### 根据脚本生成视频
```http
POST https://api.invideo.io/v1/videos/generate
```

### 获取视频生成状态
```http
GET https://api.invideo.io/v1/videos/{videoId}/status
```

### 下载/导出视频
```http
GET https://api.invideo.io/v1/videos/{videoId}/export
```

---

## 示例

### 根据脚本生成TikTok/Reel视频

```javascript
import axios from 'axios';

const client = axios.create({
  baseURL: 'https://api.invideo.io/v1',
  headers: {
    'Authorization': `Bearer ${process.env.INVIDEO_API_KEY}`,
    'Content-Type': 'application/json'
  }
});

const script = `
  Did you know that 90% of startups fail in their first year?
  Here are 3 things the successful 10% do differently.
  Number 1: They talk to customers before building anything.
  Number 2: They launch ugly and iterate fast.
  Number 3: They obsess over retention, not acquisition.
  Follow for more startup insights every day.
`;

const response = await client.post('/videos/generate', {
  script: script,
  format: "9:16",           // vertical for Reels / TikTok / Shorts
  duration: "short",        // 15–60 seconds
  style: "dynamic",         // energetic cuts and transitions
  voiceover: {
    enabled: true,
    voice: "en-US-male-1",  // choose from available voices
    speed: 1.1              // slightly faster for short-form
  },
  captions: {
    enabled: true,
    style: "bold-bottom",   // TikTok-style captions
    highlight: true         // highlight word as it's spoken
  },
  music: {
    enabled: true,
    mood: "upbeat",
    volume: 0.3             // background music volume (0–1)
  },
  branding: {
    watermark: false
  }
});

const videoId = response.data.videoId;
console.log("Video generation started. ID:", videoId);
```

---

### 查询生成进度并获取下载链接

```javascript
async function waitForVideo(videoId, maxWaitMs = 120000) {
  const start = Date.now();

  while (Date.now() - start < maxWaitMs) {
    await new Promise(r => setTimeout(r, 5000)); // poll every 5s

    const status = await client.get(`/videos/${videoId}/status`);
    const { state, progress, exportUrl } = status.data;

    console.log(`Status: ${state} — ${progress}% complete`);

    if (state === "completed") {
      console.log("Video ready:", exportUrl);
      return exportUrl;
    }

    if (state === "failed") {
      throw new Error("Video generation failed — check your script and settings");
    }
  }

  throw new Error("Timeout — video took too long to generate");
}

const downloadUrl = await waitForVideo(videoId);
```

---

### 完整流程：脚本 → 视频 → 下载

```javascript
import axios from 'axios';
import { writeFileSync } from 'fs';

async function scriptToShortVideo(script, outputPath = './output.mp4') {
  const client = axios.create({
    baseURL: 'https://api.invideo.io/v1',
    headers: { Authorization: `Bearer ${process.env.INVIDEO_API_KEY}` }
  });

  // 1 — Start generation
  const { data } = await client.post('/videos/generate', {
    script,
    format: "9:16",
    duration: "short",
    style: "dynamic",
    voiceover: { enabled: true, voice: "en-US-female-1", speed: 1.05 },
    captions: { enabled: true, style: "bold-bottom", highlight: true },
    music: { enabled: true, mood: "upbeat", volume: 0.25 }
  });

  const videoId = data.videoId;
  console.log(`Generation started — ID: ${videoId}`);

  // 2 — Wait for completion
  let exportUrl = null;
  while (!exportUrl) {
    await new Promise(r => setTimeout(r, 6000));
    const status = await client.get(`/videos/${videoId}/status`);
    if (status.data.state === "completed") exportUrl = status.data.exportUrl;
    if (status.data.state === "failed") throw new Error("Generation failed");
    console.log(`Progress: ${status.data.progress}%`);
  }

  // 3 — Download the video
  const videoStream = await axios.get(exportUrl, { responseType: 'arraybuffer' });
  writeFileSync(outputPath, videoStream.data);
  console.log(`Video saved to ${outputPath}`);

  return { videoId, exportUrl, localPath: outputPath };
}

// Usage
await scriptToShortVideo(
  "3 productivity hacks that changed my life. Number 1: Time blocking...",
  "./my-reel.mp4"
);
```

---

### 批量生成多个视频

```javascript
const scripts = [
  { topic: "morning routine tips",     voice: "en-US-female-1", mood: "calm" },
  { topic: "5 foods to boost energy",  voice: "en-US-male-1",   mood: "upbeat" },
  { topic: "how to learn faster",      voice: "en-US-female-2", mood: "inspiring" }
];

const jobs = await Promise.all(
  scripts.map(s =>
    client.post('/videos/generate', {
      script: s.topic,
      format: "9:16",
      duration: "short",
      style: "dynamic",
      voiceover: { enabled: true, voice: s.voice },
      music: { enabled: true, mood: s.mood, volume: 0.3 },
      captions: { enabled: true, style: "bold-bottom" }
    })
  )
);

const videoIds = jobs.map(j => j.data.videoId);
console.log("All jobs started:", videoIds);
```

---

## 视频制作工作流程

当被要求制作短视频时，Claude将：

1. **分析**用户提供的脚本或创意
2. **优化**脚本的节奏（前3秒尤为重要）
3. **选择**合适的风格、语音、音乐风格和字幕样式
4. **调用InVideo API生成视频**
5. **持续查询生成状态**直到视频完成
6. **返回**下载链接或将MP4文件保存到本地
7. **提供平台特定的优化建议（TikTok vs Reels vs Shorts）

---

## 平台特定设置

| 平台 | 格式 | 时长 | 字幕样式 | 音乐 |
|---|---|---|---|---|
| TikTok | 9:16 | 15–60秒 | 粗体字幕，重点突出关键词 | 明快/流行风格 |
| Instagram Reels | 9:16 | 15–90秒 | 粗体字幕或居中显示 | 明快/轻松风格 |
| YouTube Shorts | 9:16 | 15–60秒 | 简洁字幕 | 可选 |
| LinkedIn Video | 16:9或1:1 | 30–90秒 | 专业风格，顶部对齐 | 低调风格 |

---

## 脚本优化建议（Claude会自动应用这些规则）

- **前3秒吸引注意力**——以一个有力的陈述、问题或令人惊讶的数据开头
- **每个视频专注一个主题**——避免内容过于复杂
- **简短句子**——每行字幕不超过8–12个词
- **结尾添加行动号召**——例如“关注以获取更多内容”、“在下方评论”或“保存此视频”
- **采用对话式语气**——写作时应像人们日常交流一样自然
- **数字更有效**——使用“3个技巧”、“5个错误”或“1条规则”这样的标题比模糊的标题更吸引人

---

## 视频输出的标准化格式

```json
{
  "videoId": "iv_7f3k29xm",
  "title": "3 Startup Lessons Nobody Tells You",
  "platform": "tiktok",
  "format": "9:16",
  "durationSeconds": 42,
  "exportUrl": "https://cdn.invideo.io/exports/iv_7f3k29xm.mp4",
  "captions": true,
  "voiceover": "en-US-male-1",
  "musicMood": "upbeat",
  "createdAt": "2025-02-25T10:00:00Z",
  "status": "completed"
}
```

---

## 最佳实践

- **始终使用有力的开头**——前2–3秒决定用户是否会继续观看
- 30–60秒的视频脚本长度控制在120–200字左右
- 使用**粗体字幕并突出关键词**——这能显著增加观看时长
- 将音乐音量设置为**0.2–0.3**，以免声音盖过旁白
- 为同一脚本生成**3–5个不同风格的版本进行A/B测试
- 对于TikTok，使用稍快的语速（1.1倍）以匹配平台的节奏
- 发布前务必查看视频——AI生成的视频可能需要稍作调整

---

## 错误处理

```javascript
try {
  const response = await client.post('/videos/generate', payload);
  return response.data.videoId;
} catch (error) {
  if (error.response?.status === 401) throw new Error("Invalid InVideo API key");
  if (error.response?.status === 429) throw new Error("Rate limit hit — wait before retrying");
  if (error.response?.status === 400) throw new Error(`Bad request: ${error.response.data.message}`);
  throw error;
}
```

---

## 所需条件

- 拥有InVideo账户 → https://invideo.sjv.io/TBB
- 选择包含**API访问权限**的套餐（企业套餐或更高级别）
- 从InVideo设置中获取有效的**API密钥**
- 需要Node.js 18及以上版本以及`axios`库用于API调用
- 可选：如果需要后期处理或压缩导出的MP4文件，可安装`ffmpeg`工具