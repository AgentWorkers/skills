---
name: proxy-pay
description: 用于通过 Proxy 创建支付的快捷命令。使用方法：/proxy-pay [金额] [商家名称] [支付描述]。该命令会生成支付意图（payment intent）并配置虚拟卡片（virtual card）信息。
disable-model-invocation: true
argument-hint: "[amount] [merchant] [description]"
---

# 进行支付

创建一个支付意图（payment intent）并获取一张虚拟卡。

## 使用方法

```
/proxy-pay 49.99 Amazon office supplies
/proxy-pay 150 "Best Buy" laptop stand
/proxy-pay 29.99 Netflix monthly subscription
```

## 指令

从 `$ARGUMENTS` 中解析请求内容：

### 第一步：检查余额
```
Call: proxy.balance.get
If insufficient: Inform user, offer proxy.funding.get
```

### 第二步：创建支付意图
```
Call: proxy.intents.create
Parameters:
  - merchant: (from request)
  - amount: (parse number)
  - description: (remaining text or generate one)
```

### 第三步：处理响应

- 如果 `status: "pending"` 或 `status: "card_issued"`：
  ```
Call: proxy.cards.get_sensitive
Provide card details formatted as:

Card Number: 4111 1111 1111 1111
CVV: 123
Expiry: 12/26
Billing ZIP: 10001
```

- 如果 `status: "pending_approval"`：
  ```
Inform user: "This purchase requires approval because it exceeds
your auto-approve limit. You'll be notified when approved."
```

- 如果出现错误：
  ```
Explain the error clearly based on error code.
Provide resolution steps.
```