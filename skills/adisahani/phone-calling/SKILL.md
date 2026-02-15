---
name: phone-calling
description: 您可以拨打国际电话到任何国家，每分钟的通话费用非常低。支持使用 PayPal 或 UPI 进行支付。
version: 1.0.7
author: Ringez
tags: [phone, call, calling, international, voice, communication, family, friends]
api_base: https://ringez-api.vercel.app/api/v1
openapi: openapi.json
---

# Ringez电话呼叫API

无论身在何处，都能以实惠的价格拨打国际电话。没有隐藏费用，无需订阅——只需支付实际使用的分钟数即可。

## Ringez是什么？

Ringez是一款简单且注重隐私的国际电话服务，支持您拨打200多个国家的电话，无需复杂的设置或昂贵的套餐。

**非常适合：**
- 给国外的家人打电话
- 向国际客户进行商务通话
- 由AI代理进行预订或预约
- 需要快速通话但不想购买通话套餐的情况

---

## 快速入门指南

### 1. 创建账户

首先，检查您的电子邮件是否已经注册：

```http
POST https://ringez-api.vercel.app/api/v1/auth/check-email
Content-Type: application/json

{"email": "you@example.com"}
```

**响应：**
- `new_user` → 继续进行OTP验证
- `existing_user` → 使用密码登录

#### 新用户：进行OTP验证

**步骤1：** 请求OTP
```http
POST https://ringez-api.vercel.app/api/v1/auth/send-otp
Content-Type: application/json

{"email": "you@example.com"}
```

**步骤2：** 验证OTP
```http
POST https://ringez-api.vercel.app/api/v1/auth/verify-otp
Content-Type: application/json

{
  "email": "you@example.com",
  "otp": "123456"
}
```

**响应：**
```json
{
  "session_id": "sess_abc123xyz",
  "user": {
    "email": "you@example.com",
    "balance_minutes": 5
  }
}
```

保存`session_id`——所有API调用都需要它。

#### 现有用户：登录
```http
POST https://ringez-api.vercel.app/api/v1/auth/login
Content-Type: application/json

{
  "email": "you@example.com",
  "password": "your-password"
}
```

---

### 2. 查看余额

在拨打电话前，查看您还有多少分钟：

```http
GET https://ringez-api.vercel.app/api/v1/auth/me
X-Session-ID: sess_abc123xyz
```

**响应：**
```json
{
  "balance_minutes": 5,
  "balance_usd": 0,
  "email": "you@example.com"
}
```

---

### 3. 拨打电话

使用`idempotency_key`来防止意外重复拨号：

```http
POST https://ringez-api.vercel.app/api/v1/calls/initiate
X-Session-ID: sess_abc123xyz
Content-Type: application/json

{
  "to_number": "+919876543210",
  "idempotency_key": "sess_abc123xyz_1700000000000_xyz789"
}
```

**成功响应：**
```json
{
  "call_id": "call_xyz789",
  "status": "initiated",
  "mode": "bridge",
  "to_number": "+919876543210",
  "from_number": "+17623713590",
  "twilio_call_sid": "CAxxxxx"
}
```

**重复拨号响应：**
```json
{
  "alreadyInitiated": true,
  "callSid": "CAxxxxx"
}
```

---

## 呼叫模式说明

Ringez支持两种拨打电话的方式：

### 桥接模式（默认）
- **工作原理：** 先拨打您的手机，然后再将您连接到目的地
- **最适合：** 需要正常通话的个人通话
- **您的手机：** 会先响起铃声

### 直接模式
- **工作原理：** 直接拨打目的地
- **最适合：** AI代理、自动通话，或者您不希望自己的手机响起铃声的情况
- **您的手机：** 不会响起铃声

**强制使用直接模式：**
```http
POST /api/v1/calls/initiate
X-Session-ID: sess_abc123xyz
Content-Type: application/json

{
  "to_number": "+919876543210",
  "mode": "direct"
}
```

---

## 防止重复拨号

通过API拨打电话时，网络延迟或重试可能会导致多次拨号。使用**idempotency_key**来避免这种情况。

### 什么是idempotency_key？

idempotency_key是每次通话尝试的唯一标识符。如果您在5分钟内使用相同的key，API会返回之前的通话，而不会创建新的通话。

### 如何使用它

为每个用户操作生成一个唯一的key：

```javascript
const idempotencyKey = `${sessionId}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
// Example: sess_abc123_1700000000000_xyz789abc
```

### 重要说明

- **5分钟窗口：** 在5分钟内使用相同的key会返回之前的通话
- **5分钟后：** 使用相同的key会创建新的通话
- **生成新key：** 每次点击按钮时生成一个新的key，而不是在API重试时生成
- **响应：** 如果检测到重复拨号，您会收到`{alreadyInitiated: true, callSid: "..."}`

---

## 价格

只需支付您实际使用的费用。没有月费，无需订阅。

### USD套餐

| 套餐 | 价格 | 分钟数 | 每分钟费率 |
|------|-------|---------|-----------------|
| 起始套餐 | $5 | 30 | $0.17 |
| 热门套餐 | $15 | 120 | $0.13 |
| 最值套餐 | $30 | 300 | $0.10 |

### INR套餐

| 套餐 | 价格 | 分钟数 | 每分钟费率 |
|------|-------|---------|-----------------|
| 起始套餐 | ₹99 | 7 | ₹14/min |
| 热门套餐 | ₹199 | 19 | ₹10/min |
| 高性价比套餐 | ₹499 | 60 | ₹8/min |
| 高端套餐 | ₹999 | 143 | ₹7/min |

**计费：** 四舍五入到最接近的分钟。2分钟30秒的通话按3分钟计费。

---

## 管理正在进行的通话

### 查看通话状态

查看您的通话是否仍在响铃、已连接或已完成：

```http
GET https://ringez-api.vercel.app/api/v1/calls/call_xyz789
X-Session-ID: sess_abc123xyz
```

**响应：**
```json
{
  "call_id": "call_xyz789",
  "status": "in-progress",
  "duration": 120,
  "estimated_cost": {
    "minutes": 2,
    "amount": 0.25,
    "currency": "USD"
  }
}
```

### 提前结束通话

在通话结束前挂断电话：

```http
DELETE https://ringez-api.vercel.app/api/v1/calls/call_xyz789
X-Session-ID: sess_abc123xyz
```

### 操作手机菜单（DTMF）

在通话过程中按数字（适用于银行菜单、客户服务）：

```http
POST https://ringez-api.vercel.app/api/v1/calls/call_xyz789/actions
X-Session-ID: sess_abc123xyz
Content-Type: application/json

{
  "action": "dtmf",
  "parameters": {
    "digits": "1"
  }
}
```

**常见的DTMF用法：**
- `{"digits": "1"}` — 按1选择英语
- `{"digits": "1234"}` — 输入PIN码
- `{"digits": "w"}` — 等待0.5秒

---

## 通话记录

查看您的过往通话记录：

```http
GET https://ringez-api.vercel.app/api/v1/calls?limit=10&offset=0
X-Session-ID: sess_abc123xyz
```

**响应：**
```json
{
  "calls": [
    {
      "call_id": "call_abc123",
      "to_number": "+919876543210",
      "status": "completed",
      "duration": 300,
      "cost": 0.375,
      "started_at": "2026-02-09T10:00:00Z"
    }
  ],
  "pagination": {
    "total": 25,
    "has_more": true
  }
}
```

---

## 使用场景

### 给家人打电话

```
User: Call my mom in India
AI: I will help you call India. First, let me check your balance...
      You have 15 minutes available.
      Calling +91 98765 43210 now...
      
AI: Your phone is ringing. Pick up and I will connect you.
```

### AI代理进行预订

```
User: Book a table at Taj Restaurant for 7 PM
AI: I will call Taj Restaurant for you.
      
      [AI uses direct mode — your phone does not ring]
      
AI: Calling +91 12345 67890...
      
AI: Hello, I would like to make a reservation for 2 people at 7 PM today.
      
AI: ✅ Reservation confirmed! Table for 2 at 7 PM under your name.
```

---

## 重要信息

### 免费分钟

新账户可获得**5分钟**的免费通话时间来测试服务。这些分钟仅用于测试——请为常规使用添加信用额度。

### 添加信用额度

**此技能无法直接添加信用额度。** 要添加分钟数，请：
1. 访问：https://ringez.com/wallet
2. 使用PayPal（USD）或UPI（INR）支付
3. 信用额度会立即显示

**原因：** 支付处理需要安全的浏览器重定向和PCI合规性，这些功能API无法实现。

### 余额不足时的处理

如果某人的余额不足尝试拨打电话：

```
AI: Let me check your balance...
      
      You have 0 minutes left. You will need to add credits first.
      
      💳 Add credits at: https://ringez.com/wallet
      
      The rates are:
      • USA: $0.05/min
      • India: $0.08/min
      • UK: $0.06/min
      
      Come back after adding credits and I will make that call!
```

---

## API参考快速参考

| 动作 | 方法 | 端点 | 请求头 |
|--------|--------|----------|---------|
| 检查电子邮件 | POST | /auth/check-email | Content-Type |
| 发送OTP | POST | /auth/send-otp | Content-Type |
| 验证OTP | POST | /auth/verify-otp | Content-Type |
| 登录 | POST | /auth/login | Content-Type |
| 查看余额 | GET | /auth/me | X-Session-ID |
| 拨打电话 | POST | /calls/initiate | X-Session-ID, Content-Type |
| 查看通话状态 | GET | /calls/:call_id | X-Session-ID |
| 结束通话 | DELETE | /calls/:call_id | X-Session-ID |
| 通话记录 | GET | /calls | X-Session-ID |
| DTMF/操作 | POST | /calls/:call_id/actions | X-Session-ID, Content-Type |

---

## 支持

需要帮助？请发送邮件至support@ringez.com

**关于Ringez：** 由独立开发者创建，非大型企业运营。您的支持让服务得以持续运行！🙏