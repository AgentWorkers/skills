# voice-devotional 技能

使用 ElevenLabs 的文本转语音（TTS）功能，以用户的声音生成圣经阅读内容和灵修课程。

## 概述

**voice-devotional** 技能利用专业的文本转语音技术，制作音频形式的灵修内容，包括圣经阅读和灵性教导，非常适合日常灵修、冥想或分享教义。

## 特点

1. **每日灵修** — 圣经阅读 + 反思 + 祈祷（3-5 分钟音频）
2. **圣经阅读** — 带有背景信息的完整经文朗读
3. **多日计划** — 以音频形式提供的阅读计划（每周/每月）
4. **语音模式** — 适合灵修、教导或冥想的多种音调
5. **MP3 输出** — 可以直接分享或在本地播放
6. **元数据** — 包含文字记录、参考文献和时长统计

## 安装

```bash
# Copy to skills directory
cp -r voice-devotional ~/clawd/skills/

# Install dependencies
cd ~/clawd/skills/voice-devotional
npm install

# Configure
cp .env.example .env
# Edit .env with your ELEVEN_LABS_API_KEY
```

## 配置

### 环境变量

```bash
ELEVEN_LABS_API_KEY=sk_your_api_key_here
ELEVEN_LABS_MODEL_ID=eleven_monolingual_v1  # or eleven_turbo_v2
OUTPUT_DIR=~/clawd/voice-devotional/output
```

### 语音设置

请参阅 `config/voice-settings.json` 以配置语音选项：
- **Josh**（ID: pNInz6obpgDQGcFmaJgB）—— 深沉、平静的灵修语音
- **Chris**（ID: iP95p4xoKVk53GoZ742B）—— 教导/解释性的语调
- **Bella**（ID: EXAVITQu4EsNXjlNFYcV）—— 适合冥想的语调

## 使用方法

### 命令行

```bash
# Daily devotional on a theme
voice-devotional daily --theme peace --voice josh --format audio

# Read a specific scripture passage
voice-devotional scripture --passage "Romans 8:1-17" --voice josh

# Generate a multi-day reading plan
voice-devotional plan --topic hope --days 7 --voice josh

# Roman Road gospel presentation
voice-devotional roman-road --voice josh --format audio

# Generate with specific template
voice-devotional generate --template daily-devotional --topic faith --voice josh
```

### 程序化使用

```javascript
const VoiceDevotion = require('./scripts/voice-devotional');

const vd = new VoiceDevotion({
  apiKey: process.env.ELEVEN_LABS_API_KEY,
  outputDir: process.env.OUTPUT_DIR
});

// Generate daily devotional
const result = await vd.generateDaily({ 
  theme: 'peace',
  voiceId: 'pNInz6obpgDQGcFmaJgB'
});

console.log(result.audioPath);  // ~/clawd/voice-devotional/output/devotional-2024-01-15-peace.mp3
console.log(result.metadata);   // { duration, transcript, references, ... }
```

## 课程类型

### 1. 每日灵修
- **时长：** 3-5 分钟
- **结构：** 圣经摘录 + 反思 + 祈祷
- **适用场景：** 早晨/晚上的灵修时间
- **示例：** 以诗篇 4:8 为主题的每日平静冥想

### 2. 圣经阅读
- **时长：** 5-10 分钟
- **结构：** 带有背景信息的完整经文朗读
- **适用场景：** 深入学习或冥想
- **示例：** 带有神学注释的罗马书 8:1-17

### 3. 冥想
- **时长：** 5-15 分钟
- **结构：** 有策略性停顿的冥想式朗读
- **节奏：** 更慢、更专注
- **适用场景：** 深度反思或睡前灵修

### 4. 教导
- **时长：** 10-20 分钟
- **结构：** 主题讲解 + 圣经支持 + 应用指导
- **适用场景：** 学习或小组讨论
- **示例：** 以“危机中的希望”为主题的教导内容，附带相关圣经经文

### 5. 罗马书系列课程
- **时长：** 8-12 分钟
- **结构：** 依次朗读罗马书 3:23 → 6:23 → 10:9 的内容
- **适用场景：** 福音宣讲或传道
- **包含：** 邀请听众做出承诺的环节

## 输出结果

所有输出文件保存在 `~/clawd/voice-devotional/output/` 目录下：

```
devotional-2024-01-15-peace.mp3          # Audio file
devotional-2024-01-15-peace.json         # Metadata
│
├── audioPath: "..."
├── duration: 245                         # Seconds
├── transcript: "..."
├── references: ["Psalm 4:8", "John 14:27"]
├── theme: "peace"
├── voiceId: "pNInz6obpgDQGcFmaJgB"
├── generatedAt: "2024-01-15T08:30:00Z"
└── _links: { download, share, ... }
```

## 与 ElevenLabs 的集成

### API 配置

- **端点：** `https://api.elevenlabs.io/v1/text-to-speech/{voice_id}`
- **模型：** `eleven_monolingual_v1`（或 `eleven_turbo_v2` 以获得更快的处理速度）
- **设置：**
  - `stability: 0.3` — 保持自然的语音表现
  - `similarity_boost: 0.75` — 使语音更加相似
  - `style: 0.5` — 专业、清晰的发音

### 语音预设

```json
{
  "josh": {
    "voice_id": "pNInz6obpgDQGcFmaJgB",
    "tone": "devotional",
    "stability": 0.3,
    "similarity_boost": 0.75,
    "style": 0.5,
    "description": "Deep, calm, reverent — perfect for devotionals"
  },
  "chris": {
    "voice_id": "iP95p4xoKVk53GoZ742B",
    "tone": "teaching",
    "stability": 0.5,
    "similarity_boost": 0.75,
    "style": 0.5,
    "description": "Clear, engaging, authoritative — teaching/explanations"
  },
  "bella": {
    "voice_id": "EXAVITQu4EsNXjlNFYcV",
    "tone": "meditation",
    "stability": 0.2,
    "similarity_boost": 0.75,
    "style": 0.6,
    "description": "Soft, contemplative, soothing — meditation/sleep"
  }
}
```

## 圣经数据集成

当外部圣经数据可用时，该功能会与其集成；否则会使用内置的圣经库。

## 示例

### 示例 1：早晨平静灵修

```bash
voice-devotional daily --theme peace --voice josh
```

**输出结构：**
1. **开场**（10 秒）—— “早上好。今天的灵修主题是‘和平’。”
2. **圣经阅读**（30 秒）—— 诗篇 4:8 和约翰福音 14:27
3. **反思**（90 秒）—— 关于在混乱中寻找和平的冥想
4. **祈祷**（60 秒）—— 引导性的结束祷告

### 示例 2：每周希望学习计划

```bash
voice-devotional plan --topic hope --days 7 --voice josh
```

**生成内容：** 7 个独立的 MP3 文件 + `manifest.json` 文件
- 第 1 天：希望的定义（罗马书 15:13）
- 第 2 天：试炼中的希望（彼得前书 1:3-7）
- 第 3 天：希望与信心（希伯来书 11:1）
- 第 4 天：活出希望（彼得前书 1:3）
- 第 5 天：希望的依靠（希伯来书 6:19）
- 第 6 天：分享希望（彼得前书 3:15）
- 第 7 天：希望的实现（启示录 21:4）

### 示例 3：扩展圣经阅读

```bash
voice-devotional scripture --passage "Romans 8:1-17" --voice josh
```

**包含：**
- 经文背景信息（保罗写给罗马人的书信及其历史背景）
- 以自然节奏朗读完整经文
- 关键经文的标注
- 结束时的反思

## 高级功能

### 自定义模板

可以创建具有自定义结构的灵修内容：

```javascript
const template = {
  opening: "Your opening message",
  scripture: ["John 3:16", "Romans 5:8"],
  reflection: "Your reflection text",
  prayer: "Closing prayer",
  music: "optional-fade-out"
};

const result = await vd.generateCustom(template, { voiceId });
```

### 批量生成

可以一次性生成多个灵修内容：

```javascript
const themes = ['peace', 'hope', 'faith', 'love', 'strength'];
const results = await vd.generateBatch(themes, { 
  voiceId: 'josh',
  includeManifest: true 
});
```

### 背景音乐

可以选择在语音播放时添加背景音乐（音量较低）：

```javascript
const result = await vd.generateDaily({
  theme: 'peace',
  voiceId: 'josh',
  music: 'peaceful-piano'  // ambient, peaceful-piano, nature-sounds
});
```

## 故障排除

### 问题：API 使用次数超出限制

**解决方法：**
- 在请求之间添加延迟：`--delay 2000`
- 在非高峰时段批量处理
- 检查 ElevenLabs 账户的使用限制

### 问题：音频质量听起来像机器人声音

**解决方法：**
- 降低 `stability` 值（0.1-0.3 以增加语音变化）
- 调整 `similarity_boost` 值（0.5-0.95）
- 尝试使用其他语音选项：`--voice chris` 或 `--voice bella`

### 问题：输出文件过长

**解决方法：**
- 使用较短的圣经段落
- 缩短反思部分
- 删除背景音乐等可选内容

## API 参考

命令行使用的 API 详情请参阅 `README.md`。
程序化 API 的相关代码请参见：
- `scripts/voice-devotional.js` — 主要处理类
- `scripts/lesson-generator.js` — 内容生成逻辑
- `scripts/tts-generator.js` — ElevenLabs TTS 模块

## 文件结构

```
voice-devotional/
├── SKILL.md                          # This file
├── README.md                         # User guide
├── package.json
├── .env.example
├── scripts/
│   ├── voice-devotional.js          # Main orchestrator
│   ├── lesson-generator.js          # Content creation
│   ├── tts-generator.js             # ElevenLabs integration
│   └── cli.js                       # Command-line interface
├── config/
│   ├── devotional-templates.json    # Lesson templates
│   ├── voice-settings.json          # Voice configurations
│   ├── scripture-library.json       # Built-in scripture data
│   └── prayers-library.json         # Prayer templates
├── output/                          # Generated MP3s (gitignored)
└── tests/
    └── voice-devotional.test.js     # Unit tests
```

## 性能说明

- **生成时间：** 根据音频长度不同，大约需要 30-120 秒
- **文件大小：** 每分钟音频约 500KB（MP3 128kbps 格式）
- **API 费用：** 每条灵修内容约 0.30 美元（基于 1000 个字符）
- **缓存机制：** 自动缓存语音 ID 和配置信息

## 许可证

该功能属于 Clawdbot 生态系统的一部分。详细许可信息请参见根目录下的 `LICENSE` 文件。

## 相关技能

- **scripture-curated** — 提供圣经数据的源
- **telegram-integration** — 将音频发送到 Telegram
- **meditation-guide** — 管理冥想时间表

---

**版本：** 1.0.0  
**最后更新时间：** 2024-01-15  
**状态：** 正在维护中