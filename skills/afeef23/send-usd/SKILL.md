---
name: send-usd
description: 将 USD 从一个代理发送到另一个代理。
version: 0.1.0
tags:
  - payment
  - transfer
  - usd
  - money
  - finance
  - agent-to-agent
---

# 发送 USD 技能

该技能用于在两个代理之间发起 USD 转账操作。

## 输入参数

- **from_agent**: 字符串 - 发送方代理的标识符
- **to_agent**: 字符串 - 收件方代理的标识符
- **amount**: 数字 - 要转账的 USD 金额（默认值：1.00）
- **memo**: 字符串（可选） - 交易备注

## 输出参数

- **success**: 布尔值 - 转账是否成功
- **transaction_id**: 字符串 - 唯一的交易标识符
- **message**: 字符串 - 交易状态信息

## 示例

**输入参数：**
```json
{
  "from_agent": "agentA",
  "to_agent": "agentB",
  "amount": 1.00,
  "memo": "Payment for services"
}
```

**成功输出：**
```json
{
  "success": true,
  "transaction_id": "txn_abc123",
  "message": "Successfully transferred $1.00 USD from agentA to agentB"
}
```

**失败输出：**
```json
{
  "success": false,
  "transaction_id": null,
  "message": "Insufficient funds"
}
```

## 错误代码

- `INSUFFICIENT_FUNDS` - 账户余额不足，无法完成转账
- `INVALID_RECIPIENT` - 未找到收件方代理
- `INVALID_AMOUNT` - 金额必须为正数且至少为 0.01 美元
- `RATE_LIMITED` - 请求次数过多，请稍后再试

## 安全注意事项

- 所有转账操作均需进行身份验证
- 交易记录会被记录并可供审计
- 可能存在每日转账限额