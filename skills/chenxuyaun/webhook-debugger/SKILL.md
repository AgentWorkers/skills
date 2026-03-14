---
name: webhook-debugger
description: 在本地测试、调试和检查 Webhook。接收 Webhook 数据，检查其负载内容（payload），调试集成过程，并重放请求。这对于 API 开发和第三方集成至关重要。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": [] },
        "install": [],
      },
  }
---
# Webhook Debugger

用于在本地接收、检查及调试 Webhook 请求。

## 快速入门

```
webhook listen
webhook listen 3000
webhook listen --url https://myendpoint.com/webhook
```

## 主要功能

- 🎣 本地 Webhook 接收器
- 📋 请求体（Payload）检查
- ⏱️ 请求历史记录
- 🔍 请求头（Headers）与查询参数（Query Parameters）
- ✅ 签名验证（Signature Verification）
- 📤 转发到其他 URL

## 使用方法

### 启动监听器
```bash
webhook listen 8080
```

### 检查传入的请求
```
POST /webhook
Headers: { content-type: application/json }
Body: { "event": "payment", "amount": 100 }

✓ Received 2024-01-15 10:30:00
```

### 重放请求
```
webhook replay <request-id> <target-url>
```

## 常见用途

- 调试 Stripe Webhook
- 测试 GitHub Webhook
- 检查表单提交数据
- 验证 API 请求体
- 调试 Zapier 或 Make Webhook 功能

## 命令行指令

- `webhook listen [port]` - 启动本地服务器
- `webhook list` - 显示请求历史记录
- `webhook show <id>` - 显示请求详情
- `webhook replay <id> <url>` - 将请求重放到新的 URL
- `webhook clear` - 清除请求历史记录
- `webhook forward <url>` - 将请求转发到其他服务

## 注意事项

- 默认端口：3000
- 请求历史记录存储在本地
- 支持 JSON、表单数据（Form Data）和纯文本（Plain Text）格式的请求体