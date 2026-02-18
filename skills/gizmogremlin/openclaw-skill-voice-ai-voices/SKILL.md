---
name: voice-ai-tts
description: 高质量的语音合成功能，支持9种人物角色（personas）、11种语言，并可通过Voice.ai API实现语音流媒体传输。
version: 1.1.4
tags: [tts, voice, speech, voice-ai, audio, streaming, multilingual]
metadata:
  openclaw:
    requires:
      bins: ["node"]
      env:
        VOICE_AI_API_KEY: "required"
      primary_env: "VOICE_AI_API_KEY"
      note: "Set VOICE_AI_API_KEY via an environment variable."
---
# Voice.ai 语音合成服务

## ✨ 主要功能

- **9种语音角色** - 为不同使用场景精心挑选的语音
- **11种语言** - 支持多语言语音合成
- **流式输出** - 生成音频的同时实时播放
- **语音定制** - 通过 `temperature` 和 `top_p` 参数进行个性化设置
- **与OpenClaw集成** - 可与OpenClaw内置的TTS功能配合使用

---

## ⚙️ 配置

请将您的API密钥设置为环境变量：

```bash
export VOICE_AI_API_KEY="your-api-key"
```

**获取API密钥：** [Voice.ai控制面板](https://voice.ai/dashboard)

---

## 📦 安装

无需安装。该技能包含一个Node.js命令行工具（CLI）和SDK（不依赖外部npm包）。

## 🧩 关键文件

- `scripts/tts.js` - CLI的入口脚本
- `voice-ai-tts-sdk.js` - CLI使用的Node.js SDK
- `voices.json` - CLI使用的语音数据文件
- `voice-ai-tts.yaml` - API规范文件
- `package.json` - 技能的元数据文件

## 安全须知

请参阅 [SECURITY.md](SECURITY.md) 以了解完整的安全性和隐私政策。

- 该技能仅向 `https://devvoice.ai` 发送HTTPS请求
- 会读取本地文件 `voices.json`
- 将音频输出保存到指定路径（默认为 `output.mp3`）
- 不会执行shell命令，也不会修改系统配置文件

## 🌐 API端点

SDK和API规范使用 `https://devvoice.ai`，这是Voice.ai的官方生产环境API地址。

---

## 🤖 与OpenClaw的集成

如果您的环境已设置 `VOICE.AI_API_KEY`，可以直接通过OpenClaw调用CLI脚本。请使用 `/tts` 命令进行操作（具体用法请参考OpenClaw的文档）。

---

## 📝 可用的聊天命令

以下聊天命令可在OpenClaw中使用：

| 命令 | 功能 |
|---------|-------------|
| `/tts <文本>` | 用默认语音生成语音 |
| `/tts --voice ellie <文本>` | 用指定语音生成语音 |
| `/tts --stream <文本>` | 以流式模式生成语音 |
| `/voices` | 列出可用的语音 |

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
| ellie   | `d1bf0f33-8e0e-4fbf-acf8-45c3c6262513` | 女性 | 适合Vlog、社交媒体内容 |
| oliver  | `f9e6a5eb-a7fd-4525-9e92-75125249c933` | 男性 | 适合旁白、教程 |
| lilith  | `4388040c-8812-42f4-a264-f457a6b2b5b9` | 女性 | 适合ASMR、舒缓内容 |
| smooth  | `dbb271df-db25-4225-abb0-5200ba1426bc` | 男性 | 适合纪录片、有声书 |
| shadow  | `72d2a864-b236-402e-a166-a838ccc2c273` | 男性 | 适合游戏、娱乐内容 |
| sakura  | `559d3b72-3e79-4f11-9b62-9ec702a6c057` | 女性 | 适合动漫角色配音 |
| zenith  | `ed751d4d-e633-4bb0-8f5e-b5c8ddb04402` | 男性 | 适合游戏、戏剧性内容 |
| flora   | `a931a6af-fb01-42f0-a8c0-bd14bc302bb1` | 女性 | 适合儿童内容、轻松愉快的场景 |
| commander | `bd35e4e6-6283-46b9-86b6-7cfa3dd409b9` | 男性 | 适合游戏、动作场景 |

---

## 🌍 支持的语言

| 代码 | 语言 |
|------|------------|
| `en` | 英语 |
| `es` | 西班牙语 |
| `fr` | 法语 |
| `de` | 德语 |
| `it` | 意大利语 |
| `pt` | 葡萄牙语 |
| `pl` | 波兰语 |
| `ru` | 俄语 |
| `nl` | 荷兰语 |
| `sv` | 瑞典语 |
| `ca` | 加泰罗尼亚语 |

非英语语言支持多语言模型：

```javascript
const audio = await client.generateSpeech({
  text: 'Bonjour le monde!',
  voice_id: 'ellie-voice-id',
  model: 'voiceai-tts-multilingual-v1-latest',
  language: 'fr'
});
```

## 🎨 语音定制

可以通过以下参数自定义语音输出：

| 参数 | 范围 | 默认值 | 说明 |
|-----------|-------|---------|-------------|
| `temperature` | 0-2 | 1.0 | 数值越高，表达越丰富；数值越低，语音越稳定 |
| `top_p` | 0-1 | 0.8 | 控制语音生成的随机性 |

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

支持实时流式音频生成（推荐用于长文本处理）：

```bash
# Stream audio as it generates
node scripts/tts.js --text "This is a long story..." --voice ellie --stream

# Streaming with custom output
node scripts/tts.js --text "Chapter one..." --voice oliver --stream --output chapter1.mp3
```

## SDK流式输出配置：

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

## 🔊 音频格式

| 格式 | 说明 | 适用场景 |
|--------|-------------|----------|
| `mp3` | 标准MP3（32kHz） | 通用用途 |
| `wav` | 未压缩的WAV文件 | 高质量音频 |
| `pcm` | 原始PCM音频 | 用于进一步处理 |
| `opus_48000_128` | Opus 128kbps格式 | 适用于流式传输 |
| `mp3_44100_192` | 高质量MP3 | 专业用途 |

详细格式信息请参阅 `voice-ai-tts-sdk.js`。

## 💻 CLI使用方法

```bash
# Set API key
export VOICE_AI_API_KEY="your-key-here"

# Generate speech
node scripts/tts.js --text "Hello world!" --voice ellie

# Choose different voice
node scripts/tts.js --text "Good morning!" --voice oliver --output morning.mp3

# Use streaming for long texts
node scripts/tts.js --text "Once upon a time..." --voice lilith --stream

# Show help
node scripts/tts.js --help
```

## 📁 相关文件

```
voice-ai-tts/
├── SKILL.md              # This documentation
├── README.md             # Quick start
├── CHANGELOG.md          # Version history
├── LICENSE.md            # MIT license
├── SECURITY.md           # Security & privacy notes
├── voices.json           # Voice definitions
├── voice-ai-tts.yaml     # OpenAPI specification
├── voice-ai-tts-sdk.js   # JavaScript/Node.js SDK
├── package.json          # OpenClaw metadata
├── scripts/
│   └── tts.js            # CLI tool
```

## 💰 费用与使用方式

Voice.ai采用信用点数计费系统。请查看您的使用情况：

```javascript
// The SDK tracks usage via API responses
const voices = await client.listVoices();
// Check response headers for rate limit info
```

**节省费用的提示：**
- 对于长文本，使用流式输出（更高效）
- 尽可能缓存生成后的音频文件
- 根据实际需求选择合适的音频质量

---

## 🔗 链接

- **[获取API密钥](https://voice.ai/dashboard)** - 注册并获取API密钥
- **[API文档](https://voice.ai/docs)** - 完整的API参考
- **[语音库](https://voice.ai/voices)** - 浏览所有可用语音 |
- **[API参考](https://voice.ai/docs/api-reference/text-to-speech/generate-speech)** - API端点详情
- **[价格信息](https://voice.ai/pricing)** - 计划和费用详情

## 📋 更新日志

### v1.1.4 (2026-02-16)
- 在元数据中明确指定 `VOICE.AI_API_KEY` 为必填环境变量

### v1.1.3 (2026-02-16)
- 从发布的包中移除语音样本上传功能以降低隐私风险
- 仅通过环境变量要求提供 `VOICE.AI_API_KEY`

### v1.1.2 (2026-02-16)
- 添加了 `SECURITY.md` 和 `LICENSE.md` 文件以说明来源和透明度
- 限制SDK仅通过HTTPS传输

### v1.1.1 (2026-02-16)
- 优化了ClawHub的包导入元数据

### v1.1.0 (2026-02-16)
- 在元数据中明确要求输入必要的凭证
- 明确了生产环境的API地址
- 重新命名语音角色名称以保护IP地址隐私
- 添加了 `voices.json` 文件以存储语音数据

### v1.0.0 (2025-01-31)
- 首次发布
- 提供9种精选语音角色
- 支持11种语言
- 支持流式输出
- 提供语音定制参数
- 完整的SDK，包含错误处理功能
- 提供CLI工具

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

// Delete voice
await client.deleteVoice('voice-id');
```

## ❓ 故障排除

| 错误类型 | 原因 | 解决方案 |
|-------|-------|----------|
| `AuthenticationError` | API密钥无效 | 请检查 `VOICE.AI_API_KEY` 是否正确 |
| `PaymentRequiredError` | 信用点数不足 | 请在Voice.ai控制面板充值 |
| `RateLimitError` | 请求次数过多 | 等待片刻后重试，或升级套餐 |
| `ValidationError` | 参数无效 | 请检查输入的文本长度和语音ID是否正确 |

## 由 [Nick Gill](https://github.com/gizmoGremlin) 制作