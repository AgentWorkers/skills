---
name: 10dlc-registration
description: 以个体经营者（sole proprietor）的身份注册 10DLC，以启用在美国的短信服务（SMS messaging）。该功能可用于设置 A2P（Application-to-Party）短信服务、注册品牌/活动（register brands/campaigns），或为符合美国法规的短信通信分配电话号码（assign phone numbers for compliant US messaging）。注册过程中需要使用 Telnyx CLI（命令行界面）。
metadata: {"openclaw":{"emoji":"📱","requires":{"bins":["telnyx"],"env":["TELNYX_API_KEY"]},"primaryEnv":"TELNYX_API_KEY"}}
---

# 10DLC 注册

注册 10DLC（10 位长代码），以在美国启用 A2P SMS 功能。

## 使用脚本快速入门

```bash
# Interactive registration wizard
./scripts/register.sh

# Check status of brands/campaigns
./scripts/status.sh

# Assign a phone number to a campaign
./scripts/assign.sh +15551234567 <campaign-id>
```

## 先决条件

- 已安装 Telnyx CLI：`npm install -g @telnyx/api-cli`
- 已配置 API 密钥：`telnyx auth setup`
- 拥有至少一个美国电话号码

## 快速入门

**交互式向导（最简单的方式）：**

```bash
telnyx 10dlc wizard
```

## 手动注册

### 第 1 步：创建个体经营者品牌

```bash
telnyx 10dlc brand create --sole-prop \
  --display-name "Your Business Name" \
  --phone +15551234567 \
  --email you@example.com
```

### 第 2 步：验证品牌（如需要）

```bash
telnyx 10dlc brand get <brand-id>
telnyx 10dlc brand verify <brand-id> --pin 123456
```

### 第 3 步：创建活动（Campaign）

```bash
telnyx 10dlc campaign create \
  --brand-id <brand-id> \
  --usecase CUSTOMER_CARE \
  --description "Customer notifications and support" \
  --sample-message-1 "Your order #12345 has shipped." \
  --sample-message-2 "Reply STOP to opt out."
```

### 第 4 步：分配电话号码

```bash
telnyx 10dlc assign +15551234567 <campaign-id>
```

### 第 5 步：等待审核结果

```bash
telnyx 10dlc campaign get <campaign-id>
```

## 使用场景

| 使用场景 | 描述 |
|----------|-------------|
| `2FA` | 二次验证代码 |
| `CUSTOMER_CARE` | 客户服务信息 |
| `ACCOUNT_NOTIFICATION` | 账户通知 |
| `DELIVERY_NOTIFICATION` | 运输更新 |
| `MIXED` | 多种用途 |

查看所有使用场景：`telnyx 10dlc usecases`

## 状态查询命令

```bash
telnyx 10dlc brand list
telnyx 10dlc campaign list
telnyx 10dlc assignment status +15551234567
```

## 故障排除

### 常见错误

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `需要品牌验证` | 个体经营者品牌需要电话号码验证 | 查看电子邮件或短信中的 PIN 码，运行 `telnyx 10dlc brand verify <id> --pin <code>` |
| `活动被拒绝：描述不够具体` | 描述过于模糊 | 请明确消息的目的，并提供业务背景信息 |
| 样本消息中缺少退订选项 | 样本消息中缺少“回复 STOP 以退订”的提示 | 在样本消息中添加“回复 STOP 以退订” |
| 电话号码已被分配给其他活动 | 该号码已关联到其他活动 | 先运行 `telnyx 10dlc unassign +1...` |
| 品牌审核中 | 审核通常需要 24-72 小时 | 等待审核结果，并使用 `telnyx 10dlc brand get <id>` 查询状态 |
| 该使用场景不适用于个体经营者 | 某些使用场景受到限制 | 个体经营者仅限使用：2FA、CUSTOMER_CARE、DELIVERY_NOTIFICATION、ACCOUNT_NOTIFICATION |
| 超过 API 调用频率限制 | API 调用次数过多 | 等待 60 秒后重试 |

### 调试技巧

```bash
# Verbose output for debugging
telnyx 10dlc brand get <id> --json

# Check number assignment status
telnyx 10dlc assignment status +15551234567

# List all campaigns with details
telnyx 10dlc campaign list --json | jq '.data[] | {id, status, usecase}'
```

### 时间线预期

| 步骤 | 典型时间 |
|------|--------------|
| 创建品牌 | 即时 |
| 品牌验证 | 1-5 分钟（通过短信/电子邮件接收 PIN 码） |
| 品牌审核 | 24-72 小时 |
| 活动审核 | 24-48 小时 |
| 分配电话号码 | 活动审核通过后立即生效 |

### 获取帮助

- Telnyx 文档：https://developers.telnyx.com/docs/messaging/10dlc
- 支持门户：https://support.telnyx.com
- API 状态：https://status.telnyx.com

## 价格

品牌和活动注册：**免费**