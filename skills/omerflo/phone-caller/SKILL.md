---
name: phone-caller
description: "使用 ElevenLabs 的语音技术、GPT 智能语言模型以及 Twilio 平台，实现基于人工智能的 outbound 电话呼叫功能。该服务支持以下两种方式：  
1. 单向预录语音消息的发送；  
2. 实时的双向通话（AI 在通话过程中实时监听、分析并作出回应）。  
适用场景包括：  
- 根据用户需求拨打电话；  
- 留下语音消息；  
- 预约早晨的通话；  
- 通过 AI 完成预订或预约服务；  
- 运行语音营销活动；  
- 建立交互式的电话对话。  
使用该服务需要具备 Twilio 和 ElevenLabs 的相关认证信息。  
触发命令包括：  
`call`、`phone`、`voice message`、`reserve`、`book by phone`、`schedule a call`、`call and tell them`。"
---
# phone-caller

通过 Twilio 发起由 ElevenLabs 提供语音支持的智能外拨电话，支持可选的基于 GPT 的实时对话功能。

## 两种模式

**模式 1：单向消息** — 使用 ElevenLabs 生成音频文件，上传后通过 Twilio 播放。简单快捷，无需服务器。

**模式 2：交互式对话** — 启动 `server.py`，并通过 webhook URL 进行通话。AI 会实时监听用户的回答（使用 Twilio 的 STT 技术），进行思考（通过 GPT），然后通过 ElevenLabs 发出语音回应。通话结束后，会通过 iMessage 自动发送通话总结。

## 所需凭据（环境变量）

```bash
ELEVENLABS_API_KEY   # from elevenlabs.io
TWILIO_ACCOUNT_SID   # from console.twilio.com (starts with AC...)
TWILIO_AUTH_TOKEN    # from console.twilio.com
TWILIO_PHONE_NUMBER  # your Twilio number e.g. +12025551234
OPENAI_API_KEY       # for interactive mode brain
```

## 模式 1：单向通话

```bash
python3 scripts/one_way_call.py \
  --to "+13105551234" \
  --text "Hey! Just calling to say good morning." \
  --voice "tyepWYJJwJM9TTFIg5U7"   # optional, defaults to Clara (Australian female)
```

请参阅 `references/voices.md` 以获取精选的语音 ID。

## 模式 2：交互式对话

### 第 1 步：建立通信通道（确保 Twilio 能够连接到您的服务器）
```bash
npx localtunnel --port 5050 --subdomain my-caller
# Note the URL: https://my-caller.loca.lt
```

### 第 2 步：启动服务器
```bash
export CLARA_PUBLIC_URL="https://my-caller.loca.lt"
python3 scripts/server.py
```

### 第 3 步：发起通话
```bash
python3 scripts/interactive_call.py \
  --to "+13105551234" \
  --url "https://my-caller.loca.lt" \
  --persona "You are calling a restaurant to book a table for 2 at 8pm tonight." \
  --opening "Hi! I'd like to make a reservation for two people this evening around 8pm. Do you have availability?"
```

通话结束后，系统会通过 iMessage 将由 GPT 生成的通话总结自动发送到 `MASTER_PHONE` 环境变量中。

## 安排定时通话

可以使用 macOS 的 cron 任务来安排定时通话：
```bash
# Add to crontab — this example calls at 8:45 AM
crontab -e
45 8 24 2 * python3 /path/to/scripts/one_way_call.py --to "+1..." --text "Good morning!" >> /tmp/call.log 2>&1
```

## 语音选择

- 默认语音：**Clara**（ID：`tyepWYJJwJM9TTFIg5U7`）——澳大利亚女性声音，温暖、清晰、专业
- 请参阅 `references/voices.md` 以获取完整的精选语音列表及其描述。

## 重要说明

- **Twilio 试用账户**：仅能拨打已验证的号码。请在 console.twilio.com 上升级账户或验证号码（以获取已验证的来电显示信息）。
- **音频存储**：脚本使用 tmpfiles.org 临时存储音频文件（有效期 60 分钟）。对于定时通话，`server.py` 会通过通信通道将音频文件发布到 `/audio/<file>` 路径。
- **localtunnel**：免费服务，无需注册账户；ngrok 需要免费账户及自动生成的认证令牌。
- **交互式对话的延迟**：每次对话轮次大约需要 3-5 秒（包括 ElevenLabs 的文本转语音（TTS）处理时间、GPT 的响应时间以及音频上传时间）。这个延迟在电话通话中属于正常范围。