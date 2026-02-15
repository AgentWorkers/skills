---
name: whatsapp-voice-talk
description: 实时处理WhatsApp语音消息：通过Whisper将语音笔记转录为文本，识别用户意图，执行相应的处理逻辑，并发送回复。适用于开发用于WhatsApp的对话式语音界面。支持英语和印地语，提供可定制的意图（如查询天气、状态信息、执行命令等），具备自动语言检测功能，并可通过TTS技术实现流式语音回复。
---

# WhatsApp语音通话功能

该功能可将WhatsApp中的语音消息转换为实时对话。它提供了一个完整的处理流程：**语音 → 语音转录 → 意图检测 → 响应生成 → 文本转语音**。

**适用场景：**
- WhatsApp上的语音助手
- 免提命令界面
- 多语言聊天机器人
- 物联网语音控制（无人机、智能家居等）

## 快速入门

### 1. 安装依赖项

```bash
pip install openai-whisper soundfile numpy
```

### 2. 处理语音消息

```javascript
const { processVoiceNote } = require('./scripts/voice-processor');
const fs = require('fs');

// Read a voice message (OGG, WAV, MP3, etc.)
const buffer = fs.readFileSync('voice-message.ogg');

// Process it
const result = await processVoiceNote(buffer);

console.log(result);
// {
//   status: 'success',
//   response: "Current weather in Delhi is 19°C, haze. Humidity is 56%.",
//   transcript: "What's the weather today?",
//   intent: 'weather',
//   language: 'en',
//   timestamp: 1769860205186
// }
```

### 3. 运行自动监听器

为了自动处理传入的WhatsApp语音消息，需要运行以下脚本：

```bash
node scripts/voice-listener-daemon.js
```

该脚本会每5秒检查一次`~/.clawdbot/media/inbound/`目录，并处理新添加的语音文件。

## 工作原理

```
Incoming Voice Message
        ↓
    Transcribe (Whisper API)
        ↓
  "What's the weather?"
        ↓
  Detect Language & Intent
        ↓
   Match against INTENTS
        ↓
   Execute Handler
        ↓
   Generate Response
        ↓
   Convert to TTS
        ↓
  Send back via WhatsApp
```

## 主要特点

✅ **零配置复杂度**：无需安装FFmpeg，也无需依赖复杂的库。仅使用`whisper`库即可完成语音转录。
✅ **多语言支持**：自动识别英语和印地语；可轻松扩展支持更多语言。
✅ **基于意图驱动**：通过关键词定义自定义处理逻辑。
✅ **实时处理**：每条语音消息的处理时间约为5-10秒（在模型加载完成后）。
✅ **高度可定制**：可添加天气信息、状态更新、命令功能等。
✅ **适用于生产环境**：该功能基于Clawdbot的实际使用场景开发而成。

## 常见应用场景

### 天气信息机器人
```javascript
// User says: "What's the weather in Bangalore?"
// Response: "Current weather in Delhi is 19°C..."

// (Built-in intent, just enable it)
```

### 智能家居控制
```javascript
// User says: "Turn on the lights"
// Handler: Sends signal to smart home API
// Response: "Lights turned on"
```

### 任务管理器
```javascript
// User says: "Add milk to shopping list"
// Handler: Adds to database
// Response: "Added milk to your list"
```

### 状态更新机器人
```javascript
// User says: "Is the system running?"
// Handler: Checks system status
// Response: "All systems online"
```

## 自定义功能

### 添加自定义意图

编辑`voice-processor.js`文件：
1. 在`INTENTS`字典中添加新的意图：
```javascript
const INTENTS = {
  'shopping': {
    keywords: ['shopping', 'list', 'buy', 'खरीद'],
    handler: 'handleShopping'
  }
};
```

2. 为该意图添加相应的处理逻辑：
```javascript
const handlers = {
  async handleShopping(language = 'en') {
    return {
      status: 'success',
      response: language === 'en' 
        ? "What would you like to add to your shopping list?"
        : "आप अपनी शॉपिंग लिस्ट में क्या जोड़ना चाहते हैं?"
    };
  }
};
```

### 支持更多语言

1. 更新`detectLanguage()`函数以支持目标语言的编码格式：
```javascript
const urduChars = /[\u0600-\u06FF]/g; // Add this
```

2. 在返回结果中包含语言代码：
```javascript
return language === 'ur' ? 'Urdu response' : 'English response';
```

3. 在`transcribe.py`中设置语言参数：
```python
result = model.transcribe(data, language="ur")
```

### 更换语音转录模型

在`transcribe.py`文件中修改相关配置：
```python
model = whisper.load_model("tiny")    # Fastest, 39MB
model = whisper.load_model("base")    # Default, 140MB  
model = whisper.load_model("small")   # Better, 466MB
model = whisper.load_model("medium")  # Good, 1.5GB
```

## 架构

**核心脚本：**
- `transcribe.py`：负责语音转录（使用`whisper`库）
- `voice-processor.js`：处理语音消息的逻辑（意图解析、响应生成）
- `voice-listener-daemon.js`：自动监听新语音消息的守护进程

**参考资料：**
- `SETUP.md`：安装与配置指南
- `API.md`：详细的功能文档

## 与Clawdbot的集成

如果将该功能作为Clawdbot的一个技能来使用，需要将其与Clawdbot的消息处理机制集成：

```javascript
// In your Clawdbot handler
const { processVoiceNote } = require('skills/whatsapp-voice-talk/scripts/voice-processor');

message.on('voice', async (audioBuffer) => {
  const result = await processVoiceNote(audioBuffer, message.from);
  
  // Send response back
  await message.reply(result.response);
  
  // Or send as voice (requires TTS)
  await sendVoiceMessage(result.response);
});
```

## 性能表现

- **首次运行**：约30秒（下载`whisper`模型，占用约140MB内存）
- **常规处理速度**：每条消息处理时间约为5-10秒
- **内存消耗**：约1.5GB（基础模型）
- **支持的语言**：英语、印地语；可轻松扩展支持更多语言

## 支持的音频格式

OGG（Opus编码）、WAV、FLAC、MP3、CAF、AIFF等（通过`libsndfile`库支持）。

WhatsApp默认使用Opus编码的OGG格式，因此无需额外配置即可直接使用。

## 常见问题解决方法

- **“找不到‘whisper’模块”**：确保已正确安装`whisper`库。
- **“找不到‘soundfile’模块”**：检查`soundfile`库是否已安装。
- **语音消息无法被处理？**：
  1. 检查Clawdbot是否正在运行。
  2. 确认`~/.clawdbot/media/inbound/`目录中是否有新添加的语音文件。
  3. 手动运行`node scripts/voice-listener-daemon.js`脚本（查看日志信息）。
- **转录速度较慢？**：尝试使用较小的`whisper`模型（例如`whisper.load_model("base")`或`whisper.load_model("tiny")`）。

## 更多信息

- **安装指南**：请参阅`references/SETUP.md`以获取详细的安装和配置步骤。
- **API参考**：请参阅`references/API.md`以了解函数接口和示例代码。
- **示例代码**：请查看`scripts/`目录中的示例文件。

## 许可证

本功能采用MIT许可证，可自由使用、进行定制或贡献代码！

---

该功能专为实际应用场景开发，已在Clawdbot中经过多次测试，支持多种语言和应用场景。