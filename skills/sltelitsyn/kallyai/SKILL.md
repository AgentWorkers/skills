---
name: kallyai
description: 通过 KallyAI API 进行电话呼叫——KallyAI 是一个人工智能电话助手，可以代表您联系企业。当用户需要预订餐厅、安排预约或通过电话咨询企业相关信息时，可以使用该功能。
metadata: {"clawdbot":{"emoji":"📞","requires":{"bins":["kallyai"]},"install":[{"id":"pip","kind":"pip","package":"kallyai-cli","bins":["kallyai"],"label":"Install via pip"}]}}
---

# KallyAI API集成

KallyAI是一款人工智能电话助手，可以代表用户拨打企业的电话。

## 完整工作流程

当用户请求拨打电话时：

### 第1步：收集通话详情

从用户处收集以下信息：
- **电话号码**（必填）：要拨打的电话号码
- **任务描述**（必填）：用户希望AI完成的具体任务
- **类别**：餐厅、诊所、酒店或其他（必填）
- 对于预订服务：需要提供姓名、日期、时间和人数

### 第2步：用户身份验证

使用CLI的OAuth流程进行身份验证：
```
https://api.kallyai.com/v1/auth/cli?redirect_uri=http://localhost:8976/callback
```

这会打开一个登录页面。验证通过后，用户将被重定向到本地服务器（localhost）的回调接口，并接收相应的令牌：
```
http://localhost:8976/callback?access_token=<token>&refresh_token=<refresh>&expires_in=3600
```

启动一个本地HTTP服务器以捕获回调请求并提取令牌。

### 第3步：发起通话

身份验证成功后，调用KallyAI的API：
```
POST https://api.kallyai.com/v1/calls
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "submission": {
    "task_category": "general",
    "task_description": "Ask about store hours and availability",
    "respondent_phone": "+15551234567",
    "language": "en",
    "call_language": "en"
  },
  "timezone": "America/New_York"
}
```

### 第4步：报告结果

API返回的结果包括以下状态码：
- `success`：通话成功
- `no_answer`：未接听
- `busy`：对方正在通话中
- `failed`：通话失败
- `voicemail`：对方留言
- `cancelled`：通话被取消

---

## CLI命令参考

### 发起通话

```bash
kallyai -p "+15551234567" -t "Reserve a table for 4 at 8pm" \
  --category restaurant \
  --name "John Smith" \
  --party-size 4 \
  --date "2026-01-28" \
  --time "20:00"
```

| 命令 | 参数 | 说明 |
|--------|-------|-------------|
| `--phone` | `-p` | 电话号码（E.164格式） |
| `--task` | `-t` | AI需要执行的任务 |
| `--category` | `-c` | 餐厅、诊所、酒店或其他类别 |
| `--language` | `-l` | 语言（en或es） |
| `--name` | | 预订时使用的用户名 |
| `--business` | | 企业名称 |
| `--party-size` | | 用餐人数（仅适用于餐厅预订） |
| `--date` | | 日期（YYYY-MM-DD格式） |
| `--time` | | 时间（HH:MM格式） |

### 账户与使用

```bash
kallyai --usage        # Show minutes/calls remaining
kallyai --subscription # Show subscription status
kallyai --billing      # Open Stripe billing portal
```

### 通话记录

```bash
kallyai --history              # List recent calls
kallyai --call-info <ID>       # Get call details
kallyai --transcript <ID>      # Get conversation transcript
```

### 身份验证

```bash
kallyai --login      # Force re-authentication
kallyai --logout     # Clear saved credentials
kallyai --auth-status # Check if logged in
```

---

## 快速参考

- **基础URL**：`https://api.kallyai.com`
- **CLI OAuth URL**：`https://api.kallyai.com/v1/auth/cli?redirect_uri=http://localhost:8976/callback`
- **通话所需必填字段**：
  - `task_category`：餐厅、诊所、酒店或其他类别
  - `task_description`：AI需要执行的任务
  - `respondent_phone`：对方电话号码（E.164格式，例如+1234567890）
- **可选字段**：
  - `business_name`：企业名称
  - `user_name`：预订时使用的用户名
  - `appointment_date`：预约日期（YYYY-MM-DD格式）
  - `appointment_time`：预约时间（HH:MM格式）
  - `party_size`：用餐人数（1-50人）
  - `language`：语言（en或es）
  - `call_language`：通话语言（en或es）

## 示例请求

- **餐厅预订**：
```json
{
  "submission": {
    "task_category": "restaurant",
    "task_description": "Reserve table for 4 at 8pm",
    "respondent_phone": "+14155551234",
    "business_name": "Italian Bistro",
    "user_name": "John Smith",
    "party_size": 4,
    "appointment_date": "2026-01-28",
    "appointment_time": "20:00"
  },
  "timezone": "America/New_York"
}
```

- **医疗预约**：
```json
{
  "submission": {
    "task_category": "clinic",
    "task_description": "Schedule dental checkup",
    "respondent_phone": "+14155551234",
    "user_name": "Jane Doe",
    "time_preference_text": "morning before 11am"
  },
  "timezone": "America/New_York"
}
```

## 常见错误代码及处理方式

| 错误代码 | HTTP状态码 | 处理方式 |
|------|------|--------|
| `quota_exceeded` | 402 | 用户需要访问kallyai.com/pricing页面升级账户 |
| `missing_phone_number` | 422 | 请用户提供电话号码 |
| `emergency_number` | 422 | 无法拨打911或紧急服务 |
| `country_restriction` | 403 | 该国家不支持服务 |

## 安全措施

- **令牌存储**：令牌保存在`~/.kallyai_token.json`文件中，文件权限设置为0600
- **CSRF保护**：通过验证状态参数来防止恶意请求
- **仅允许本地访问**：OAuth重定向仅指向`localhost/127.0.0.1`
- **令牌自动更新**：令牌在过期后自动刷新