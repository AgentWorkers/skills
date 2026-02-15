---
name: twilio
description: 通过 Twilio API 发送短信、进行语音通话以及管理 WhatsApp 消息。可用于发送通知、实现两步验证（2FA）、客户沟通以及语音自动化功能。
metadata: {"clawdbot":{"emoji":"📱","requires":{"env":["TWILIO_ACCOUNT_SID","TWILIO_AUTH_TOKEN"]}}}
---

# Twilio

支持发送短信、语音通话和WhatsApp消息。

## 环境变量

```bash
export TWILIO_ACCOUNT_SID="ACxxxxxxxxxx"
export TWILIO_AUTH_TOKEN="your_auth_token"
export TWILIO_PHONE_NUMBER="+1234567890"
```

## 发送短信

```bash
curl -X POST "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/Messages.json" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" \
  -d "From=$TWILIO_PHONE_NUMBER" \
  -d "To=+1recipient" \
  -d "Body=Hello from Twilio!"
```

## 发送WhatsApp消息

```bash
curl -X POST "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/Messages.json" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" \
  -d "From=whatsapp:+14155238886" \
  -d "To=whatsapp:+1recipient" \
  -d "Body=Your message"
```

## 进行语音通话

```bash
curl -X POST "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/Calls.json" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" \
  -d "From=$TWILIO_PHONE_NUMBER" \
  -d "To=+1recipient" \
  -d "Url=http://demo.twilio.com/docs/voice.xml"
```

## 查看消息列表

```bash
curl "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/Messages.json?PageSize=20" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN"
```

## 查看账户余额

```bash
curl "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/Balance.json" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN"
```

## 链接：
- 控制台：https://console.twilio.com
- 文档：https://www.twilio.com/docs