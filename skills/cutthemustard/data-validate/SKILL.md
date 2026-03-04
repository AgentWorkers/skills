---
name: data-validate
description: 验证 URL 和 JSON 模式是否符合格式规范。
version: 1.0.2
metadata:
  openclaw:
    emoji: "✅"
    homepage: https://validate.agentutil.net
    always: false
---
# 数据验证

本模块用于验证数据格式，包括 URL 解析、JSON Schema（草案-07）验证、电子邮件语法（RFC 5322）以及电话号码格式（E.164）的验证。

## 重要提示：需要用户同意

在验证任何用户提供的数据之前，**务必先征得用户的同意**，确认他们同意将数据发送到外部验证服务。未经用户明确授权，切勿自行验证可能包含个人身份信息（PII）的数据。

## 终端点（Endpoints）

### URL 验证

```bash
curl -X POST https://validate.agentutil.net/v1/url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/path"}'
```

### JSON Schema 验证

```bash
curl -X POST https://validate.agentutil.net/v1/json-schema \
  -H "Content-Type: application/json" \
  -d '{"data": {"name": "test"}, "schema": {"type": "object", "required": ["name"]}}'
```

### 电子邮件语法检查

仅验证 RFC 5322 规范的结构，不涉及 SMTP 连接或收件箱验证。

```bash
curl -X POST https://validate.agentutil.net/v1/email \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'
```

### 电话号码格式检查

仅验证 E.164 格式。

```bash
curl -X POST https://validate.agentutil.net/v1/phone \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1-555-0100"}'
```

## 响应格式

```json
{
  "valid": true,
  "url": "https://example.com/path",
  "protocol": "https:",
  "hostname": "example.com",
  "errors": [],
  "request_id": "abc-123",
  "service": "https://validate.agentutil.net"
}
```

## 价格方案

- 免费 tier：每天 10 次查询，无需身份验证
- 付费 tier：每次查询费用为 0.001 美元，通过 x402 协议支付（基础货币为 USDC）

## 隐私政策

所有验证操作仅限于**语法/格式检查**。验证后的数据不会被存储或记录，也不会被转发给第三方。系统不会进行 SMTP 探测或支付网络通信，同时采用 IP 哈希技术来实现速率限制。