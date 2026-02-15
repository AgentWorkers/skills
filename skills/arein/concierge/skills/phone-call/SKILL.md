---
name: phone-call
description: 使用 Twilio、Deepgram 和 ElevenLabs 的 AI 语音功能，实现自主拨打电话的功能。
version: 1.2.0
triggers:
  - call
  - phone
  - dial
  - make a call
  - book by phone
  - call the hotel
  - call the restaurant
---

# 电话通话技能

通过一个目标驱动的AI代理来自动拨打电话。AI会负责整个通话过程，直到目标达成为止。

## 先决条件

1. **必需的配置：**
   ```bash
   concierge config set twilioAccountSid <your-sid>
   concierge config set twilioAuthToken <your-token>
   concierge config set twilioPhoneNumber <your-number>
   concierge config set deepgramApiKey <your-key>
   concierge config set elevenLabsApiKey <your-key>
   concierge config set elevenLabsVoiceId <voice-id>
   concierge config set anthropicApiKey <your-key>
   ```

2. **（针对自动管理的ngrok）可选配置：**
   ```bash
   concierge config set ngrokAuthToken <your-ngrok-token>
   ```

## 使用方法

### 基本通话
```bash
concierge call "+1-555-123-4567" \
  --goal "Book a hotel room for February 15" \
  --name "John Smith" \
  --email "john@example.com" \
  --customer-phone "+1-555-444-1212" \
  --context "2 nights, king bed preferred"
```

### 交互式模式
```bash
concierge call "+1-555-123-4567" \
  --goal "Make a reservation" \
  --name "John Smith" \
  --email "john@example.com" \
  --customer-phone "+1-555-444-1212" \
  --interactive
```
在交互式模式下，您可以实时输入AI应该说的话。

### 基础架构行为

- 默认情况下，如果服务器不可用，`call`命令会自动启动`ngrok`和`server`。
- 使用`--no-auto-infra`选项可以禁用自动管理功能，所有操作都将手动执行。
- 通话结束后，相关进程会自动停止。
- 日志文件会被保存在以下路径：
  - `~/.config/concierge/call-runs/<run-id>/server.log`
  - `~/.config/concierge/call-runs/<run-id>/ngrok.log`

### 服务器管理
```bash
# Check server status
concierge server status

# Start server
concierge server start --public-url <ngrok-url>

# Stop server
concierge server stop
```

## 预检

在拨打电话之前，系统会验证以下内容：
- 本地运行时依赖项（`ffmpeg`二进制文件及MP3解码支持；如果使用自动管理功能，则还需验证`ngrok`）
- Twilio的凭据/账户状态及来电号码的可用性
- Deepgram API密钥的可用性
- ElevenLabs的字符配额是否足够（用于估算通话时长）

## 工作原理

1. 命令行界面（CLI）会发送包含目标信息及客户身份详情的通话请求。
2. 服务器通过Twilio发起通话。
3. 音频流通过WebSocket实现双向传输。
4. Deepgram会实时转录人类语音。
5. Claude会生成相应的响应内容。
6. ElevenLabs会合成语音并发送给对方。
7. 通话会持续进行，直到目标达成或用户挂断电话。

## 示例

### 预订酒店
```bash
concierge call "+1-800-HILTON" \
  --goal "Book a room for 2 nights" \
  --name "Sarah Johnson" \
  --email "sarah@example.com" \
  --customer-phone "+1-555-000-2222" \
  --context "Check-in: March 10, Guest: Sarah Johnson, King bed, non-smoking"
```

### 预订餐厅
```bash
concierge call "+1-555-DINER" \
  --goal "Reserve a table for dinner" \
  --name "Garcia" \
  --email "garcia@example.com" \
  --customer-phone "+1-555-000-3333" \
  --context "Party of 4, 7:30 PM, Saturday, name: Garcia"
```

### 取消预约
```bash
concierge call "+1-555-DOCTOR" \
  --goal "Cancel appointment" \
  --name "Mike Chen" \
  --email "mike@example.com" \
  --customer-phone "+1-555-000-4444" \
  --context "Patient: Mike Chen, Appointment on Tuesday at 2 PM"
```

## 支持的语音ID

一些常用的ElevenLabs语音：
- `EXAVITQu4vr4xnSDxMaL` - Rachel（默认女性语音）
- `pNInz6obpgDQGcFmaJgB` - Adam（男性语音）
- `21m00Tcm4TlvDq8ikWAM` - Rachel（旁白语音）
- `AZnzlk1XvdvUeBnXmlld` - Domi（年轻女性语音）

您可以设置自己喜欢的语音：
```bash
concierge config set elevenLabsVoiceId <voice-id>
```

## 延迟

目标语音到语音的延迟：< 500毫秒

- Deepgram的语音转文字（STT）时间：约150毫秒
- 响应生成时间：约100-200毫秒
- ElevenLabs的语音合成（TTS）时间：约75毫秒
- 网络传输时间：约50毫秒

## 故障排除

### 服务器无法启动
- 确保所有配置项都已正确设置：`concierge config show`
- 如果使用手动模式，请确认`ngrok`正在运行且URL正确。
- 检查端口3000是否可用。

### 通话无法连接
- 确认Twilio电话号码处于激活状态。
- 检查Twilio账户是否有足够的余额。
- （手动模式）确保`ngrok`提供的URL可以公开访问。

### 通话过程中TTS失败
- 检查ElevenLabs的字符配额是否足够。
- 通常在拨打电话前会进行预检，以避免此类问题。
- 如果问题仍然存在，可以缩短提示或上下文长度，或为ElevenLabs充值。

### 音频质量问题
- ElevenLabs使用了优化的电话通话设置。
- Deepgram采用了专门的电话通话模型。
- 音频质量为8kHz（电话通话标准）。