---
name: free-groq-voice
description: 使用 Groq 免费的 Whisper API，您可以免费实现语音识别功能。该 API 能够将多种语言的音频消息转录为文本，适用于语音转文本自动化、会议记录生成以及辅助技术（如无障碍功能）等场景。使用该服务需要一个免费的 Groq API 密钥。
---

# 免费的Groq语音识别服务

## 概述

这项语音识别服务完全免费，由Groq提供的免费Whisper API（whisper-large-v3模型）支持。无需信用卡，也没有使用限制。您可以将其用于将音频消息、语音笔记和录音转换为50多种语言的文本。非常适合以下场景：
- 🎙️ 语音消息转录
- 📝 会议记录
- ♿ 辅助功能
- 🤖 语音控制自动化

## 费用：$0.00

- ✅ **完全免费** 的Groq API层级
- ✅ 无需信用卡
- ✅ 无月费
- ✅ 丰富的使用量限制
- ✅ 使用最准确的whisper-large-v3模型

## 设置

### 1. 获取您的免费Groq API密钥

1. 访问 https://console.groq.com/
2. 免费注册（只需30秒）
3. 转到“API Keys”页面
4. 创建一个新的API密钥
5. 复制密钥

**就这样！无需任何支付。**

### 2. 配置代理（如果您位于受限地区）

在某些地区（例如中国大陆），可能需要使用代理来访问Groq API。

**请将以下代码添加到您的TOOLS.md文件中：**
```markdown
### Proxy Settings
- HTTP Proxy: http://127.0.0.1:7890

### Voice Recognition (FREE Groq Whisper)
- API Key: gsk_your_key_here
- Model: whisper-large-v3
- Language: zh (or your preferred language)
- Requires Proxy: Yes (if in restricted region)
```

### 3. 测试该服务

发送一条语音消息，让我们帮您将其转录吧！

## 使用示例

**基本转录：**
```
User: [sends voice message]
You: You said: "你好，这是一条测试消息"
```

**带有语言提示的转录：**
```
User: 识别这段英文语音
You: [automatically uses language=en]
```

**批量处理：**
```
User: 帮我识别这个文件夹里所有的语音文件
You: [processes all .ogg/.mp3/.wav files]
```

## 支持的语言

- 🇨🇳 中文（zh） - 普通话、粤语
- 🇺🇸 英文（en） - 美式、英式、澳式
- 🇯🇵 日文（ja）
- 🇰🇷 韩文（ko）
- 🇫🇷 法文（fr）
- 🇩🇪 德文（de）
- 🇪🇸 西班牙文（es）
- 🇮🇹 意大利文（it）
- 🇵🇹 葡萄牙文（pt）
- 🇷🇺 俄文（ru）
- ……以及更多语言

## 技术细节

**API端点：**
```
https://api.groq.com/openai/v1/audio/transcriptions
```

**模型：** `whisper-large-v3`（OpenAI最准确的模型）

**支持的格式：**
- OGG/OPUS（Feishu、Telegram默认格式）
- MP3
- WAV
- M4A
- WebM

**代理要求：**
- 使用HTTP代理（不支持SOCKS5）
- 默认代理：`http://127.0.0.1:7890`

## 故障排除

**❌ “Forbidden”错误：**
- 确认API密钥有效
- 如果位于受限地区，请确保代理配置正确
- 尝试使用HTTP代理而非SOCKS5

**❌ “文件未找到”错误：**
- 确保文件路径是绝对路径
- 确保文件存在

**❌ 响应缓慢：**
- 检查代理速度
- Groq API通常响应很快（处理短音频文件仅需不到1秒）

## 隐私与安全

- ✅ 音频由Groq的API处理（不会永久存储）
- ✅ API密钥存储在您的TOOLS.md文件中
- ✅ 不会向第三方发送任何数据
- ✅ 代码开源且可审计

## 为什么选择Groq？

**免费与付费服务对比：**

| 服务 | 费用 | 准确率 | 速度 |
|---------|------|----------|-------|
| **Groq（免费）** | **$0** | ⭐⭐⭐⭐⭐ | ⚡⚡⚡⚡⚡ |
| OpenAI Whisper | $0.006/分钟 | ⭐⭐⭐⭐⭐ | ⚡⚡⚡ |
| Google Speech | $0.006/分钟 | ⭐⭐⭐⭐ | ⚡⚡⚡ |
| AWS Transcribe | $0.024/分钟 | ⭐⭐⭐⭐ | ⚡⚡⚡ |

**Groq的免费层级提供：**
- 与OpenAI相同的whisper-large-v3模型
- 更快的推理速度（得益于Groq的LPU芯片）
- 无使用量限制（遵循公平使用政策）
- 无需信用卡

## 贡献

想要改进这项服务吗？
- 在ClawHub上创建分支
- 提交改进方案
- 与社区分享您的成果

## 许可证

MIT许可证——允许免费使用、修改和分发。

---

**享受免费的语音识别服务吧！🎉**

再也不用为转录服务付费了。Groq的免费API让每个人都能使用到专业级的语音转文本服务。