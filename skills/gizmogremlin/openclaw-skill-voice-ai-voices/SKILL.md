---
name: voice-ai-tts
description: >
  High-quality voice synthesis with 9 personas, 11 languages, streaming, and voice cloning using Voice.ai API.
version: 1.0.0
---

# Voice.ai 语音服务

## ✨ 主要功能

- **9种语音角色** - 为不同使用场景精心挑选的语音
- **11种语言** - 支持多语言合成
- **流式输出** - 生成语音时实时输出音频
- **语音克隆** - 从音频样本中克隆语音
- **语音定制** - 通过 `temperature` 和 `top_p` 参数进行个性化设置
- **与OpenClaw集成** - 兼容OpenClaw内置的TTS功能

---

## ⚙️ 配置

脚本会按以下顺序查找您的API密钥：
1. `VOICE.AI_API_KEY` 环境变量
2. OpenClaw配置文件（`~/.openclaw/openclaw.json`）
3. 本技能对应的 `.env` 文件

**获取API密钥：** [Voice.ai 控制台](https://voice.ai/dashboard)

### 创建 `.env` 文件（推荐）

```bash
echo 'VOICE_AI_API_KEY=your-key-here' > .env
```

### 或者直接导出API密钥

```bash
export VOICE_AI_API_KEY="your-api-key"
```

---

## 🤖 与OpenClaw的集成

将此技能添加到您的OpenClaw配置文件 `~/.openclaw/openclaw.json` 中：

```json
{
  "skills": {
    "voice-ai-tts": {
      "enabled": true,
      "api_key": "your-voice-ai-api-key",
      "default_voice": "ellie",
      "default_format": "mp3"
    }
  },
  "tts": {
    "skill": "voice-ai-tts",
    "voice_id": "d1bf0f33-8e0e-4fbf-acf8-45c3c6262513",
    "streaming": true
  }
}
```

### YAML配置方式（可选）

```yaml
tts:
  skill: voice-ai-tts
  voice_id: d1bf0f33-8e0e-4fbf-acf8-45c3c6262513
  streaming: true
```

---

## 📝 命令行接口（CLI）

以下命令可在OpenClaw中使用：

| 命令 | 描述 |
|---------|-------------|
| `/tts <text>` | 用默认语音生成语音 |
| `/tts --voice ellie <text>` | 用指定语音生成语音 |
| `/tts --stream <text>` | 以流式模式生成语音 |
| `/voices` | 列出可用的语音 |
| `/clone <audio_url>` | 从音频中克隆语音 |

**示例：**

```
/tts Hello, welcome to Voice.ai!
/tts --voice oliver Good morning, everyone.
/tts --voice lilith --stream This is a long story that will stream as it generates...
```

---

## 🎙️ 可用语音列表

| 语音名称 | ID | 性别 | 适用场景 |
|---------|-----|--------|-------------|
| ellie   | `d1bf0f33-8e0e-4fbf-acf8-45c3c6262513` | 女性 | 适合Vlog、社交内容 |
| oliver  | `f9e6a5eb-a7fd-4525-9e92-75125249c933` | 男性 | 适合旁白、教程 |
| lilith  | `4388040c-8812-42f4-a264-f457a6b2b5b9` | 女性 | 适合ASMR、轻松内容 |
| smooth  | `dbb271df-db25-4225-abb0-5200ba1426bc` | 男性 | 适合纪录片、有声书 |
| corpse  | `72d2a864-b236-402e-a166-a838ccc2c273` | 男性 | 适合游戏、娱乐内容 |
| skadi   | `559d3b72-3e79-4f11-9b62-9ec702a6c057` | 女性 | 适合动漫角色配音 |
| zhongli | `ed751d4d-e633-4bb0-8f5e-b5c8ddb04402` | 男性 | 适合游戏、戏剧性内容 |
| flora   | `a931a6af-fb01-42f0-a8c0-bd14bc302bb1` | 女性 | 适合儿童内容、轻松活泼的语气 |
| chief   | `bd35e4e6-6283-46b9-86b6-7cfa3dd409b9` | 男性 | 适合游戏、动作场景 |

---

## 🌍 支持的语言

| 代码 | 语言       |
|------|------------|
| `en` | 英语         |
| `es` | 西班牙语       |
| `fr` | 法语         |
| `de` | 德语         |
| `it` | 意大利语       |
| `pt` | 葡萄牙语       |
| `pl` | 波兰语        |
| `ru` | 俄语         |
| `nl` | 荷兰语        |
| `sv` | 瑞典语        |
| `ca` | 加泰罗尼亚语      |

非英语语言使用多语言模型：

```javascript
const audio = await client.generateSpeech({
  text: 'Bonjour le monde!',
  voice_id: 'ellie-voice-id',
  model: 'voiceai-tts-multilingual-v1-latest',
  language: 'fr'
});
```

## 🎨 语音定制

通过以下参数自定义语音输出：

| 参数    | 范围     | 默认值    | 说明                |
|---------|---------|-----------|-------------------|
| `temperature` | 0-2       | 1.0       | 数值越高，表达越丰富；越低，语音更连贯   |
| `top_p` | 0-1       | 0.8       | 控制语音生成的随机性         |

**示例：**

```javascript
const audio = await client.generateSpeech({
  text: 'This will sound very expressive!',
  voice_id: 'ellie-voice-id',
  temperature: 1.8,
  top_p: 0.9
});
```

## 📡 流式输出

支持实时流式输出音频（推荐用于长文本处理）：

```bash
# Stream audio as it generates
node scripts/tts.js --text "This is a long story..." --voice ellie --stream

# Streaming with custom output
node scripts/tts.js --text "Chapter one..." --voice oliver --stream --output chapter1.mp3
```

**SDK流式输出详细信息：**

```javascript
const stream = await client.streamSpeech({
  text: 'Long text here...',
  voice_id: 'ellie-voice-id'
});

// Pipe to file
stream.pipe(fs.createWriteStream('output.mp3'));

// Or handle chunks
stream.on('data', chunk => {
  // Process audio chunk
});
```

---

## 🔊 音频格式

| 格式      | 描述                | 适用场景            |
|---------|------------------|-------------------|
| `mp3`    | 标准MP3格式（32kHz）       | 通用用途            |
| `wav`    | 未压缩WAV格式         | 高质量音频            |
| `pcm`    | 原始PCM音频           | 用于进一步处理          |
| `opus_48000_128` | Opus格式（128kbps）      | 适用于流式传输          |
| `mp3_44100_192` | 高质量MP3格式         | 专业级应用            |

更多格式信息请参考 `voice-ai-tts-sdk.js`。

---

## 💻 命令行工具（CLI）

```bash
# Set API key
echo 'VOICE_AI_API_KEY=your-key-here' > .env

# Generate speech
node scripts/tts.js --text "Hello world!" --voice ellie

# Choose different voice
node scripts/tts.js --text "Good morning!" --voice oliver --output morning.mp3

# Use streaming for long texts
node scripts/tts.js --text "Once upon a time..." --voice lilith --stream

# Show help
node scripts/tts.js --help
```

---

## 🧬 语音克隆

可以从音频样本中克隆任意语音：

```javascript
const VoiceAI = require('./voice-ai-tts-sdk');
const client = new VoiceAI(process.env.VOICE_AI_API_KEY);

// Clone from file
const result = await client.cloneVoice({
  file: './my-voice-sample.mp3',
  name: 'My Custom Voice',
  visibility: 'PRIVATE',
  language: 'en'
});

console.log('Voice ID:', result.voice_id);
console.log('Status:', result.status);

// Wait for voice to be ready
const voice = await client.waitForVoice(result.voice_id);
console.log('Voice ready!', voice);
```

**要求：**
- 音频样本时长建议10-30秒
- 语音清晰，背景噪音低
- 支持的音频格式：MP3、WAV、M4A

---

## 📁 相关文件

```
voice-ai-tts/
├── SKILL.md              # This documentation
├── voice-ai-tts.yaml     # OpenAPI specification
├── voice-ai-tts-sdk.js   # JavaScript/Node.js SDK
├── scripts/
│   └── tts.js            # CLI tool
└── .env                  # API key (create this)
```

---

## 💰 费用与使用

Voice.ai采用信用点数计费系统。请查看您的使用情况：

```javascript
// The SDK tracks usage via API responses
const voices = await client.listVoices();
// Check response headers for rate limit info
```

**节省费用的提示：**
- 对于长文本使用流式输出（更高效）
- 可能时缓存生成的音频
- 根据实际需求选择合适的音频质量

---

## 🔗 链接

- **[获取API密钥](https://voice.ai/dashboard)** - 注册并获取API密钥
- **[API文档](https://voice.ai/docs)** - 完整的API参考资料
- **[语音库](https://voice.ai/voices)** - 浏览所有可用语音
- **[API参考](https://voice.ai/docs/api-reference/text-to-speech/generate-speech)** - 端点详细信息
- **[定价方案](https://voice.ai/pricing)** - 计费与信用点数说明

---

## 📋 更新日志

### v1.0.0 (2025-01-31)
- 初始版本发布
- 提供9种精心设计的语音角色
- 支持11种语言
- 新增流式输出功能
- 引入语音克隆功能
- 增加语音定制参数
- 提供带错误处理的完整SDK
- 提供命令行工具

---

## 🛠️ SDK快速参考

```javascript
const VoiceAI = require('./voice-ai-tts-sdk');
const client = new VoiceAI(process.env.VOICE_AI_API_KEY);

// List voices
const voices = await client.listVoices({ limit: 10 });

// Get voice details
const voice = await client.getVoice('voice-id');

// Generate speech
const audio = await client.generateSpeech({
  text: 'Hello, world!',
  voice_id: 'voice-id',
  audio_format: 'mp3'
});

// Generate to file
await client.generateSpeechToFile(
  { text: 'Hello!', voice_id: 'voice-id' },
  'output.mp3'
);

// Stream speech
const stream = await client.streamSpeech({
  text: 'Long text...',
  voice_id: 'voice-id'
});

// Clone voice
const clone = await client.cloneVoice({
  file: './sample.mp3',
  name: 'My Voice'
});

// Delete voice
await client.deleteVoice('voice-id');
```

---

## ❓ 常见问题与解决方法

| 错误类型 | 原因                | 解决方案                |
|---------|------------------|----------------------|
| `AuthenticationError` | API密钥无效            | 请检查 `VOICE.AI_API_KEY` 的值       |
| `PaymentRequiredError` | 信用点数不足            | 在Voice.ai控制台充值信用点数       |
| `RateLimitError` | 请求次数过多             | 等待片刻后重试或升级套餐       |
| `ValidationError` | 参数格式不正确             | 请检查输入的文本长度和语音ID         |

## 由 [Nick Gill](https://github.com/gizmoGremlin) 创作