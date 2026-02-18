---
name: voice-ai-tts
description: 使用Voice.ai API，可以实现高质量的语音合成功能，支持9种人物角色（personas）、11种语言，并支持实时流媒体播放（streaming）。
version: 1.1.5
tags: [tts, voice, speech, voice-ai, audio, streaming, multilingual]
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"bins":["node"],"env":["VOICE_AI_API_KEY"]},"primaryEnv":"VOICE_AI_API_KEY"},"openclaw":{"requires":{"bins":["node"],"env":{"VOICE_AI_API_KEY":"required"},"note":"Set VOICE_AI_API_KEY via an environment variable."}}}
---
# Voice.ai 语音合成服务

## ✨ 主要功能

- **9种语音角色**：为不同使用场景精心挑选的语音库  
- **11种语言支持**：支持多语言的语音合成  
- **流式输出**：生成音频时即可实时播放  
- **语音定制**：可通过 `temperature` 和 `top_p` 参数调整语音表达效果  
- **与OpenClaw集成**：兼容OpenClaw内置的语音合成功能  

---

## ⚙️ 配置  

请将您的API密钥设置为环境变量：  
```bash
export VOICE_AI_API_KEY="your-api-key"
```  

**获取API密钥：** [Voice.ai控制面板](https://voice.ai/dashboard)  

---

## 📦 安装  

无需额外安装步骤。该语音合成工具包含Node.js命令行界面（CLI）和SDK，不依赖任何外部npm包。  

## 🧩 关键文件  

- `scripts/tts.js`：CLI的入口脚本  
- `voice-ai-tts-sdk.js`：CLI使用的Node.js SDK  
- `voices.json`：包含所有可用语音数据的文件  
- `voice-ai-tts.yaml`：API接口的详细规范  
- `package.json`：工具的元数据文件  

## 安全注意事项  

请参阅 [SECURITY.md](SECURITY.md) 以了解完整的安全和隐私政策：  
- 仅向 `https://devvoice.ai` 发送HTTPS请求  
- 读取本地文件 `voices.json`  
- 将音频输出保存到指定的路径（默认为 `output.mp3`）  
- 不会执行shell命令，也不会修改系统配置文件  

## 🌐 API接口  

SDK和API规范均使用 `https://devvoice.ai`（Voice.ai的正式生产环境API地址）。  

## 🤖 与OpenClaw的集成  

如果您的环境已配置 `VOICE.AI_API_KEY`，可以直接通过OpenClaw调用该CLI脚本。根据OpenClaw的配置使用 `/tts` 命令。  

## 📝 可用的聊天命令  

以下命令可在OpenClaw中使用：  
| 命令            | 功能                        |  
|-----------------|---------------------------|  
| `/tts <文本>`       | 用默认语音生成语音            |  
| `/tts --voice ellie <文本>` | 用指定语音生成语音            |  
| `/tts --stream <文本>`     | 以流式模式生成语音            |  
| `/voices`         | 显示可用的语音列表            |  

**示例：**  
```
/tts Hello, welcome to Voice.ai!
/tts --voice oliver Good morning, everyone.
/tts --voice lilith --stream This is a long story that will stream as it generates...
```  

## 🎙️ 可用语音列表  

| 语音名称 | ID            | 性别 | 适用场景                          |  
|-------------|-----------------|-----------------|--------------------------------|  
| ellie         | `d1bf0f33-8e0e-4fbf-acf8-45c3c6262513` | 女性    | 视频博客、社交内容                   |  
| oliver        | `f9e6a5eb-a7fd-4525-9e92-75125249c933` | 男性    | 解说、教程                      |  
| lilith        | `4388040c-8812-42f4-a264-f457a6b2b5b9` | 女性    | ASMR、舒缓内容                   |  
| smooth        | `dbb271df-db25-4225-abb0-5200ba1426bc` | 男性    | 纪录片、有声书                   |  
| shadow        | `72d2a864-b236-402e-a166-a838ccc2c273` | 男性    | 游戏、娱乐内容                   |  
| sakura        | `559d3b72-3e79-4f11-9b62-9ec702a6c057` | 女性    | 动漫角色语音                   |  
| zenith        | `ed751d4d-e633-4bb0-8f5e-b5c8ddb04402` | 男性    | 游戏、剧情类内容                   |  
| flora        | `a931a6af-fb01-42f0-a8c0-bd14bc302bb1` | 女性    | 儿童内容、轻松愉悦的音乐             |  
| commander     | `bd35e4e6-6283-46b9-86b6-7cfa3dd409b9` | 男性    | 冒险、动作类内容                   |  

## 🌍 支持的语言  

| 代码       | 语言                         |  
|------------|---------------------------|  
| `en`        | 英语                          |  
| `es`        | 西班牙语                         |  
| `fr`        | 法语                         |  
| `de`        | 德语                         |  
| `it`        | 意大利语                         |  
| `pt`        | 葡萄牙语                         |  
| `pl`        | 波兰语                         |  
| `ru`        | 俄语                         |  
| `nl`        | 荷兰语                         |  
| `sv`        | 瑞典语                         |  
| `ca`        | 加泰罗尼亚语                         |  

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

可通过以下参数自定义语音输出：  
| 参数           | 范围          | 默认值       | 说明                          |  
|-----------------|--------------|------------|--------------------------------|  
| `temperature`    | 0–2           | 1.0        | 数值越大，表达越丰富；数值越小，语音更连贯       |  
| `top_p`       | 0–1           | 0.8        | 控制语音生成的随机性                   |  

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

支持实时流式音频输出（推荐用于长文本处理）：  
```bash
# Stream audio as it generates
node scripts/tts.js --text "This is a long story..." --voice ellie --stream

# Streaming with custom output
node scripts/tts.js --text "Chapter one..." --voice oliver --stream --output chapter1.mp3
```  

## SDK流式传输说明：  
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

| 格式           | 说明                          | 适用场景                        |  
|-----------------|---------------------------|--------------------------------|  
| `mp3`         | 标准MP3格式（32kHz）                | 通用用途                         |  
| `wav`         | 未压缩的WAV文件                   | 高质量音频                         |  
| `pcm`         | 原始PCM音频                     | 用于音频处理                     |  
| `opus_48000_128`    | Opus格式（128kbps）                | 适用于流式传输                   |  
| `mp3_44100_192`    | 高质量MP3格式                   | 专业用途                         |  

更多格式选项请参阅 `voice-ai-tts-sdk.js`。  

## 💻 CLI使用指南  

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

## 💰 费用与使用说明  

Voice.ai采用信用点数计费制度。请查看您的使用情况：  
```javascript
// The SDK tracks usage via API responses
const voices = await client.listVoices();
// Check response headers for rate limit info
```  

**节省费用的提示：**  
- 长文本使用流式输出（更高效）  
- 尽可能缓存生成的音频文件  
- 根据实际需求选择合适的音频质量  

## 🔗 链接  

- **[获取API密钥](https://voice.ai/dashboard)**：注册并获取API密钥  
- **[API文档](https://voice.ai/docs)**：完整API参考文档  
- **[语音库](https://voice.ai/voices)**：浏览所有可用语音  
- **[API参考](https://voice.ai/docs/api-reference/text-to-speech/generate-speech)**：接口详情  
- **[定价信息](https://voice.ai/pricing)**：套餐与费用说明  

## 📋 更新日志  

### v1.1.5 (2026-02-16)  
- 通过 `metadata.clawdbot` 明确运行时所需的环境变量  

### v1.1.4 (2026-02-16)  
- 将 `VOICE.AI_API_KEY` 设为元数据中的主要环境变量  

### v1.1.3 (2026-02-16)  
- 从发布版本中移除语音样本上传功能以降低隐私风险  
- 强制要求通过环境变量传递 `VOICE.AI_API_KEY`  

### v1.1.2 (2026-02-16)  
- 添加 `SECURITY.md` 和 `LICENSE.md` 文件以提升透明度和安全性  
- 限制SDK仅通过HTTPS传输  

### v1.1.1 (2026-02-16)  
- 优化ClawHub导入时的打包元数据  

### v1.1.0 (2026-02-16)  
- 在元数据中明确指定所需凭证  
- 明确生产环境API的域名  
- 为避免IP地址泄露，重新命名语音角色名称  
- 添加 `voices.json` 文件以存储语音数据  

### v1.0.0 (2025-01-31)  
- 首次发布版本  
- 提供9种精心设计的语音角色  
- 支持11种语言  
- 流式输出功能  
- 提供语音定制参数  
- 完整的SDK，包含错误处理机制  
- 提供CLI工具  

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

## ❓ 常见问题与解决方法  

| 错误类型 | 原因                         | 解决方案                         |  
|-----------------|---------------------------------|--------------------------------|  
| `AuthenticationError` | API密钥无效                     | 请检查您的 `VOICE.AI_API_KEY`                 |  
| `PaymentRequiredError` | 信用点数不足                     | 在Voice.ai控制面板充值                     |  
| `RateLimitError` | 请求次数过多                     | 等待片刻后重试或升级套餐                 |  
| `ValidationError` | 参数格式不正确                     | 请检查输入的文本长度和语音ID                 |  

## 开发者：[Nick Gill](https://github.com/gizmoGremlin)