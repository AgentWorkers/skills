# 代理呼叫技能

**使AI代理能够使用Twilio自主发起和接听电话。**

## 概述

该技能为AI代理提供了完整的工具包，以便它们能够以编程方式处理电话呼叫。代理可以：
- 发起带有自定义语音消息的出站呼叫
- 接听来电并动态响应
- 将文本转换为语音以实现自然对话
- 将来电者的语音转录为文本
- 管理呼叫路由和转发
- 管理语音邮件和录音

## 先决条件

1. **Twilio账户**：在 [twilio.com](https://www.twilio.com) 注册
2. **Twilio电话号码**：购买具有语音功能的电话号码
3. **Twilio凭据**：账户SID和认证令牌

## 快速入门

### 1. 配置凭据

在 `~/.clawdbot/twilio-config.json` 文件中创建配置：

```json
{
  "accountSid": "YOUR_ACCOUNT_SID",
  "authToken": "YOUR_AUTH_TOKEN",
  "phoneNumber": "+1XXXXXXXXXX"
}
```

或者设置环境变量：

```bash
export TWILIO_ACCOUNT_SID="YOUR_ACCOUNT_SID"
export TWILIO_AUTH_TOKEN="YOUR_AUTH_TOKEN"
export TWILIO_PHONE_NUMBER="+1XXXXXXXXXX"
```

### 2. 发起第一个呼叫

```bash
./scripts/make-call.sh --to "+15551234567" --message "Hello! This is your AI assistant calling."
```

### 3. 设置来电处理

```bash
./scripts/setup-webhook.sh --url "https://your-server.com/voice"
```

## 核心脚本

### `make-call.sh` - 发起出站呼叫

使用文本转语音功能发起电话呼叫：

```bash
# Simple call with message
./scripts/make-call.sh --to "+15551234567" --message "Hello from your AI assistant"

# Call with custom voice
./scripts/make-call.sh --to "+15551234567" --message "Important update" --voice "Polly.Matthew"

# Call with recording
./scripts/make-call.sh --to "+15551234567" --message "Please hold" --record true

# Call with status callback
./scripts/make-call.sh --to "+15551234567" --message "Hello" --callback "https://your-server.com/status"
```

**参数：**
- `--to`（必填）：目标电话号码（E.164格式）
- `--message`（必填）：要播放的语音消息
- `--voice`（可选）：使用的语音（默认：Polly.Joanna）
- `--record`（可选）：是否录制呼叫（true/false）
- `--callback`（可选）：状态更新URL
- `--timeout`（可选）：呼叫超时时间（秒）（默认：30）

### `receive-call.sh` - 处理来电

服务器脚本，用于使用TwiML响应处理来电：

```bash
# Start webhook server on port 3000
./scripts/receive-call.sh --port 3000

# Custom greeting
./scripts/receive-call.sh --port 3000 --greeting "Thank you for calling AI Services"

# Forward to another number
./scripts/receive-call.sh --port 3000 --forward "+15559876543"

# Record voicemail
./scripts/receive-call.sh --port 3000 --voicemail true
```

### `sms-notify.sh` - 发送短信通知

发送短信通知（适用于电话跟进）：

```bash
# Simple SMS
./scripts/sms-notify.sh --to "+15551234567" --message "Missed call from AI assistant"

# With media (MMS)
./scripts/sms-notify.sh --to "+15551234567" --message "Summary attached" --media "https://example.com/summary.pdf"
```

### `call-status.sh` - 检查呼叫状态

监控正在进行的和已完成的呼叫：

```bash
# Get status of specific call
./scripts/call-status.sh --sid "CA1234567890abcdef"

# List recent calls
./scripts/call-status.sh --list --limit 10

# Get call recording
./scripts/call-status.sh --sid "CA1234567890abcdef" --download-recording
```

## 高级用法

### 自定义IVR（交互式语音应答）

创建动态电话菜单：

```bash
./scripts/create-ivr.sh --menu "Press 1 for sales, 2 for support, 3 for emergencies"
```

### 会议呼叫

设置多方会议呼叫：

```bash
# Create conference
./scripts/conference.sh --create --name "Team Standup"

# Add participant
./scripts/conference.sh --add-participant --conference "Team Standup" --number "+15551234567"
```

### 呼叫录音与转录

```bash
# Record and transcribe
./scripts/make-call.sh --to "+15551234567" --message "How can I help?" --record true --transcribe true

# Download recording
./scripts/call-status.sh --sid "CA123..." --download-recording --output "call.mp3"

# Get transcription
./scripts/call-status.sh --sid "CA123..." --get-transcript
```

### 语音克隆（实验性）

使用ElevenLabs集成来实现自定义语音：

```bash
# Requires ElevenLabs API key
./scripts/make-call-elevenlabs.sh --to "+15551234567" --message "Hello" --voice-id "YOUR_VOICE_ID"
```

## 集成模式

### 1. 约会提醒

```bash
#!/bin/bash
# Send appointment reminder calls
while read -r name phone appointment; do
  ./scripts/make-call.sh \
    --to "$phone" \
    --message "Hello $name, this is a reminder about your appointment on $appointment. Press 1 to confirm, 2 to reschedule."
done < appointments.txt
```

### 2. 紧急警报

```bash
#!/bin/bash
# Broadcast emergency alert to list
emergency_message="Emergency alert: System outage detected. Team members are working on resolution."

cat on-call-list.txt | while read phone; do
  ./scripts/make-call.sh \
    --to "$phone" \
    --message "$emergency_message" \
    --urgent true &
done
wait
```

### 潜在客户资格评估

```bash
#!/bin/bash
# Call leads and route based on IVR response
./scripts/make-call.sh \
  --to "+15551234567" \
  --message "Thank you for your interest. Press 1 if you'd like to schedule a demo, 2 for pricing information, or 3 to speak with a representative." \
  --callback "https://your-crm.com/lead-response"
```

## 语音选项

支持的语音（Amazon Polly）：

**英语（美国）：**
- `Polly.Joanna`（女性，默认）
- `Polly.Matthew`（男性）
- `Polly.Ivy`（女性，儿童音）
- `Polly.Joey`（男性）
- `Polly.Kendra`（女性）
- `Polly.Kimberly`（女性）
- `Polly.Salli`（女性）

**英语（英国）：**
- `Polly.Amy`（女性）
- `Polly.Brian`（男性）
- `Polly.Emma`（女性）

**其他语言：**
- 西班牙语：`Polly.Miguel`, `Polly.Penelope`
- 法语：`Polly.Celine`, `Polly.Mathieu`
- 德语：`Polly.Hans`, `Polly.Marlene`

## Webhook与TwiML

### 设置Webhook

配置您的Twilio号码，在接听电话时向您的Webhook URL发送POST请求：

```bash
./scripts/configure-number.sh \
  --voice-url "https://your-server.com/voice" \
  --voice-method "POST" \
  --status-callback "https://your-server.com/status"
```

### 示例TwiML响应

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">Hello! Thank you for calling.</Say>
    <Gather numDigits="1" action="/handle-key">
        <Say>Press 1 for sales, 2 for support, or 3 to leave a message.</Say>
    </Gather>
</Response>
```

## 成本优化

- **出站呼叫**：约0.013美元/分钟（美国）
- **来电**：约0.0085美元/分钟（美国）
- **短信**：约0.0079美元/条（美国）
- **电话号码**：约1.15美元/月

**提示：**
- 使用区域电话号码以降低成本
- 在非高峰时段批量发送呼叫
- 保持消息简洁以减少通话时长
- 使用短信发送简单通知

## 安全最佳实践

1. **保护凭据**：切勿将凭据提交到git
2. **使用HTTPS**：始终使用HTTPS进行Webhook通信
3. **验证请求**：验证Webhook上的Twilio签名
4. **限制速率**：对出站呼叫实施速率限制
5. **日志记录**：记录所有呼叫以备审计

## 故障排除

### 呼叫无法连接

```bash
# Check number formatting (must be E.164)
./scripts/validate-number.sh "+15551234567"

# Test connectivity
./scripts/make-call.sh --to "$TWILIO_PHONE_NUMBER" --message "Test call"
```

### Webhook未接收到呼叫

```bash
# Test webhook
curl -X POST https://your-server.com/voice \
  -d "Called=+15551234567" \
  -d "From=+15559876543"

# Check Twilio debugger
./scripts/check-logs.sh --recent 10
```

### 音频质量问题

```bash
# Use different voice engine
./scripts/make-call.sh --to "+15551234567" --message "Test" --voice "Google.en-US-Neural2-A"

# Adjust speech rate
./scripts/make-call.sh --to "+15551234567" --message "Test" --rate "90%"
```

## 示例

请查看 `examples/` 目录中的完整用例：

- `examples/appointment-reminder.sh` - 自动化约会提醒
- `examples/emergency-broadcast.sh` - 广播紧急警报
- `examples/ivr-menu.sh` - 交互式语音菜单
- `examples/voicemail-transcription.sh` - 将语音邮件转录为电子邮件
- `examples/two-factor-auth.sh` - 基于语音的双因素认证

## API参考

完整的Twilio API文档：https://www.twilio.com/docs/voice

## 支持

- GitHub问题：[报告错误或请求功能]
- Twilio文档：https://www.twilio.com/docs
- 社区：https://discord.com/invite/clawd

## 许可证

MIT许可证 - 您可以自由将其用于您自己的项目

## 致谢

由Kelly Claude（AI助手）创建
由Twilio和Clawdbot提供支持