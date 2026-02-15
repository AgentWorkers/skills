---
name: bank-skill
version: 0.1.4
description: 通过 Wise 功能，您可以查询账户余额、转账资金，以及查看转账的详细信息。
homepage: https://github.com/singularityhacker/bank-skills
metadata: {"openclaw":{"emoji":"🏦","requires":{"bins":["python"],"env":["WISE_API_TOKEN"]},"primaryEnv":"WISE_API_TOKEN"}}
---

# 银行服务技能

## 目的

通过 Wise API 为 AI 代理提供银行相关功能。代理可以查询多货币余额、转账资金以及获取收款所需的账户/路由信息。

## 先决条件

- 环境变量 `WISE_API_TOKEN` 已设置为一个有效的 Wise API 令牌。
- 可选：`WISE_PROFILE_ID`（默认使用第一个可用的账户信息）。

## 操作

### 1. 查询余额

**目的：** 查询配置账户的多货币余额。

**输入：**
- `action`：`"balance"`（必填）
- `currency`：货币代码过滤器，例如 `"USD"`（可选——省略时返回所有货币）

**输出：**
- 一个 JSON 数组，其中每个对象包含 `currency`（货币代码）、`amount`（余额）和 `reservedAmount`（预留金额）

**使用方式：**
```bash
echo '{"action": "balance"}' | ./run.sh
echo '{"action": "balance", "currency": "USD"}' | ./run.sh
```

**示例输出：**
```json
{
  "success": true,
  "balances": [
    {"currency": "USD", "amount": 1250.00, "reservedAmount": 0.00},
    {"currency": "EUR", "amount": 500.75, "reservedAmount": 10.00}
  ]
}
```

### 2. 获取收款信息

**目的：** 获取账户号码、路由号码、IBAN 及其他相关信息，以便他人向您转账。

**输入：**
- `action`：`"receive-details"`（必填）
- `currency`：货币代码，例如 `"USD"`（可选——省略时返回所有货币）

**输出：**
- 一个 JSON 对象，其中包含账户持有人姓名、账户号码、路由号码（非 USD 账户的 IBAN/SWIFT）以及银行名称

**使用方式：**
```bash
echo '{"action": "receive-details"}' | ./run.sh
echo '{"action": "receive-details", "currency": "USD"}' | ./run.sh
```

**示例输出：**
```json
{
  "success": true,
  "details": [
    {
      "currency": "USD",
      "accountHolder": "Your Business Name",
      "accountNumber": "1234567890",
      "routingNumber": "026073150",
      "bankName": "Community Federal Savings Bank"
    }
  ]
}
```

### 3. 转账资金

**目的：** 从您的 Wise 账户向指定收款人转账。

**输入：**
- `action`：`"send"`（必填）
- `sourceCurrency`：源货币代码，例如 `"USD"`（必填）
- `targetCurrency`：目标货币代码，例如 `"EUR"`（必填）
- `amount`：转账金额（数字形式，必填）
- `recipientName`：收款人全名（必填）
- `recipientAccount`：收款人账户号码或 IBAN（必填）

**针对 USD ACH 转账的额外字段：**
- `recipientRoutingNumber`：9 位 ABA 路由号码（必填）
- `recipientCountry`：国家代码（2 个字母，例如 `"US"`（必填）
- `recipientAddress`：街道地址（必填）
- `recipientCity`：城市名称（必填）
- `recipientState`：州代码（例如 `"NY"`（必填）
- `recipientPostCode`：邮政编码（必填）
- `recipientAccountType`：`"CHECKING"` 或 `"SAVINGS"`（可选，默认为 `"CHECKING"`）

**输出：**
- 一个 JSON 对象，其中包含转账 ID、转账状态及确认信息

**USD ACH 转账示例：**
```bash
echo '{
  "action": "send",
  "sourceCurrency": "USD",
  "targetCurrency": "USD",
  "amount": 100.00,
  "recipientName": "John Smith",
  "recipientAccount": "123456789",
  "recipientRoutingNumber": "111000025",
  "recipientCountry": "US",
  "recipientAddress": "123 Main St",
  "recipientCity": "New York",
  "recipientState": "NY",
  "recipientPostCode": "10001",
  "recipientAccountType": "CHECKING"
}' | ./run.sh
```

**EUR IBAN 转账示例（简化版）：**
```bash
echo '{
  "action": "send",
  "sourceCurrency": "USD",
  "targetCurrency": "EUR",
  "amount": 100.00,
  "recipientName": "Jane Doe",
  "recipientAccount": "DE89370400440532013000"
}' | ./run.sh
```

**示例输出：**
```json
{
  "success": true,
  "transfer": {
    "id": 12345678,
    "status": "processing",
    "sourceAmount": 100.00,
    "sourceCurrency": "USD",
    "targetAmount": 93.50,
    "targetCurrency": "EUR"
  }
}
```

## 失败情况

- **缺少 `WISE_API_TOKEN`：** 返回 `{"success": false, "error": "WISE_API_TOKEN 环境变量未设置"}`。请设置令牌后重试。
- **API 令牌无效：** 返回 `{"success": false, "error": "身份验证失败 — 请检查您的 WISE_API_TOKEN"}`。
- **余额不足：** 返回 `{"success": false, "error": "USD 余额不足"`。请先查询余额，然后尝试转账较小的金额。
- **收款人信息无效：** 返回 `{"success": false, "error": "收款人账户信息无效"}`。请核实收款人信息后重试。
- **未知操作：** 返回 `{"success": false, "error": "未知操作：<action>"}`。请使用 `balance`、`receive-details` 或 `send` 中的一个操作。

## 适用场景

当您需要查询银行余额、向他人转账或共享账户信息以接收付款时，可以使用此技能。

## 不适用场景

- 不适用于加密货币交易（Wise 禁止使用加密货币相关功能）。
- 不适用于持有大量资金的账户（仅限研发用途）。