---
name: proxy-balance
description: 检查代理账户余额及可用支出额度。会显示待处理的交易请求（pending intents），若余额不足则建议补充资金。
disable-model-invocation: true
---

# 检查余额

获取当前余额和消费能力。

## 指令

1. 调用 `proxy.balance.get`
2. 调用 `proxy.intents.list` 以获取待处理的操作意图（pending intents）

## 输出格式

```
💰 Proxy Balance
────────────────
Available:  $X,XXX.XX USD
Pending:    X intents ($XXX.XX reserved)
────────────────
Net Available: $X,XXX.XX
```

如果余额过低（< $100），请执行以下操作：
```
💡 Low balance. Use /proxy-fund for deposit instructions.
```

如果有待审批的操作意图，请列出这些意图：
```
⏳ Pending Approval:
  • $XXX.XX - Merchant Name (intent_id)
```