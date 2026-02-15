---
name: elevenlabs-phone-reminder-lite
description: 使用 ElevenLabs 的 Conversational AI 和 Twilio 构建 AI 电话提醒功能。免费入门指南。
version: 1.0.0
author: LittleLobster
license: MIT
---

# 📞 AI电话提醒（Lite版）

构建一个能够通过自然语音与你通话的AI助手！

## 🎯 你将构建的内容

- 一个能够发起外拨电话的AI代理
- 具备语音克隆功能的自然对话系统
- 多语言支持（包括中文、日语等）
- 实时语音交互（非预录制）

## 📋 先决条件

1. **ElevenLabs账户**（Creator计划或以上）
   - 注册：https://elevenlabs.io
   - 包含每月250分钟的对话式AI使用时间

2. **Twilio账户**
   - 注册：https://twilio.com
   - 需要：Account SID、Auth Token和电话号码（美国号码费用约为每月1.15美元）

## 🏗️ 架构

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Your App  │────▶│ ElevenLabs  │────▶│   Twilio    │
│  (trigger)  │     │ Conv. AI    │     │   (call)    │
└─────────────┘     └─────────────┘     └─────────────┘
                           │                    │
                           ▼                    ▼
                    ┌─────────────┐     ┌─────────────┐
                    │  AI Agent   │     │  Phone      │
                    │  (voice)    │◀───▶│  Network    │
                    └─────────────┘     └─────────────┘
```

## 🚀 快速入门

### 第1步：获取凭证

```bash
# ElevenLabs
ELEVENLABS_API_KEY="your_api_key_here"

# Twilio (from console.twilio.com)
TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TWILIO_AUTH_TOKEN="your_auth_token_here"
```

### 第2步：购买Twilio电话号码

1. 登录Twilio控制台 → 电话号码 → 购买号码
2. 选择一个具备**语音**功能的美国号码（费用约为每月1.15美元）
3. 如有需要，启用国际通话功能（需要设置地理权限）

### 第3步：创建ElevenLabs代理

```bash
curl -X POST "https://api.elevenlabs.io/v1/convai/agents/create" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Reminder Agent",
    "conversation_config": {
      "agent": {
        "prompt": {
          "prompt": "You are a helpful assistant making reminder calls. Be friendly and concise.",
          "llm": "gemini-2.0-flash-001"
        },
        "first_message": "Hi! This is your AI assistant calling with a reminder.",
        "language": "en"
      },
      "tts": {
        "model_id": "eleven_multilingual_v2",
        "voice_id": "YOUR_VOICE_ID"
      }
    }
  }'
```

### 第4步：将Twilio与ElevenLabs连接

```bash
curl -X POST "https://api.elevenlabs.io/v1/convai/phone-numbers/create" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+1XXXXXXXXXX",
    "provider": "twilio",
    "label": "My Reminder Line",
    "sid": "'$TWILIO_ACCOUNT_SID'",
    "token": "'$TWILIO_AUTH_TOKEN'"
  }'
```

### 第5步：发起电话

```bash
curl -X POST "https://api.elevenlabs.io/v1/convai/twilio/outbound-call" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "YOUR_AGENT_ID",
    "agent_phone_number_id": "YOUR_PHONE_NUMBER_ID",
    "to_number": "+1RECIPIENT_NUMBER"
  }'
```

## 💰 成本估算

| 项目 | 成本 |
|------|------|
| ElevenLabs Creator计划 | 每月22美元（包含250分钟使用时间） |
| Twilio美国号码 | 每月约1.15美元 |
| 美国内拨电话 | 每分钟约0.013美元 |
| 国际电话 | 每分钟约0.15-0.30美元 |
| 每次1分钟的提醒电话 | 每次约0.11-0.40美元 |

## ⚠️ Lite版的限制

- 仅提供基本设置指南
- 无优化的语音参数设置
- 无错误处理示例
- 无调度/自动化功能
- 仅提供社区支持

## 🚀 想了解更多？

**高级版**包含：
- ✅ 优化的语音参数（经过测试，音质更自然）
- ✅ 完整的自动化脚本
- ✅ 多语言配置
- ✅ 错误处理与重试机制
- ✅ Cron作业集成
- ✅ 优先支持

可在**Virtuals ACP**平台上购买：[即将推出]

---

由LittleLobster制作 🦞