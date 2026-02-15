---
name: whatsapp-business
description: 通过 WhatsApp Business Cloud API 发送消息。可以向客户发送模板消息、媒体文件以及交互式消息。
metadata: {"clawdbot":{"emoji":"💬","requires":{"env":["WHATSAPP_TOKEN","WHATSAPP_PHONE_ID"]}}}
---

# WhatsApp Business Cloud API

用于在 WhatsApp 上发送企业消息。

## 环境配置

```bash
export WHATSAPP_TOKEN="xxxxxxxxxx"
export WHATSAPP_PHONE_ID="xxxxxxxxxx"
```

## 发送文本消息

```bash
curl -X POST "https://graph.facebook.com/v18.0/$WHATSAPP_PHONE_ID/messages" \
  -H "Authorization: Bearer $WHATSAPP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "messaging_product": "whatsapp",
    "to": "1234567890",
    "type": "text",
    "text": {"body": "Hello from WhatsApp Business!"}
  }'
```

## 发送模板消息

```bash
curl -X POST "https://graph.facebook.com/v18.0/$WHATSAPP_PHONE_ID/messages" \
  -H "Authorization: Bearer $WHATSAPP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "messaging_product": "whatsapp",
    "to": "1234567890",
    "type": "template",
    "template": {
      "name": "hello_world",
      "language": {"code": "en_US"}
    }
  }'
```

## 发送图片

```bash
curl -X POST "https://graph.facebook.com/v18.0/$WHATSAPP_PHONE_ID/messages" \
  -H "Authorization: Bearer $WHATSAPP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "messaging_product": "whatsapp",
    "to": "1234567890",
    "type": "image",
    "image": {"link": "https://example.com/image.jpg"}
  }'
```

## 发送交互式按钮

```bash
curl -X POST "https://graph.facebook.com/v18.0/$WHATSAPP_PHONE_ID/messages" \
  -H "Authorization: Bearer $WHATSAPP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "messaging_product": "whatsapp",
    "to": "1234567890",
    "type": "interactive",
    "interactive": {
      "type": "button",
      "body": {"text": "Choose an option:"},
      "action": {
        "buttons": [
          {"type": "reply", "reply": {"id": "yes", "title": "Yes"}},
          {"type": "reply", "reply": {"id": "no", "title": "No"}}
        ]
      }
    }
  }'
```

## 获取消息模板

```bash
curl "https://graph.facebook.com/v18.0/{WABA_ID}/message_templates" \
  -H "Authorization: Bearer $WHATSAPP_TOKEN"
```

## 链接：
- 控制台：https://business.facebook.com/wa/manage/home
- 文档：https://developers.facebook.com/docs/whatsapp/cloud-api