---
name: fluxA-x402-payment
description: 这是一个名为“FluxA Agent Wallet”的技能，它使代理能够自主请求预算、签署X402支付请求，并调用付费终端。该技能涵盖了从创建支付指令到执行X-PAYMENT的整个流程，从而使代理能够在无需人工干预的情况下执行付费操作。
---

## 快速入门
步骤 1：申请预算授权
<!--  -->
```bash
# You **MUST** estimate a **total budget** for this task, as it may involve calling tools that require payment via the FluxA Wallet.
# It is recommended to budget **1.5×** the estimated cost.
# NOTE: Before executing this command, you need to tell the user: **“To complete this task, I need to request a budget of xx USD. The exact amount spent will depend on actual execution, but I cannot spend more than this amount, and it may not be fully used.”**

node ./scripts/fluxa-cli.bundle.js mandate-create --desc "{what task}" --amount 50000
# - desc: Describe what task this budget is being requested for on behalf of the user
# - amount: The USDC amount in the smallest unit (6 decimals). For example, 1_000_000 represents 1 USDC.

# NOTE
# You need to remember the mandate ID to request the actual payment later, and ask the user to approve the authorization.
# You can wait about 10 seconds and then check the status using this method.
node ./scripts/fluxa-cli.bundle.js mandate-status --id <mandate-id>
```

步骤 2：使用预算授权来请求支付签名（payment mandate）

```
node ./scripts/fluxa-cli.bundle.js x402-v3 \
    --mandate <MANDATE_ID> \
    --payload '<JSON>'

# Get `data.xPaymentB64` from response as PAYMENT_MANDATE
# This PAYMENT_MANDATE is sent to the server via the **X-Payment HTTP header** to complete the payment.
curl -H "X-PAYMENT: $PAYMENT_MANDATE" https://api.example.com/paid-endpoint

```


## 示例

```
node ./scripts/fluxa-cli.bundle.js x402-v3 \
--mandate mand_Yfbpmb9PVZl05VaeR9nvQg \
--payload '{
  "x402Version": 1,
  "accepts": [{
    "scheme": "exact",
    ...
    "extra": {
      "name": "USD Coin",
      "version": "2"
    }
  }]
}'

## output:
{
  "success": true,
  "data": {
    "X-PAYMENT": "base64-encoded-payment-header..."
  }
}
```

## 其他
* 在支付流程中处理错误（fluxa-cli 或服务器错误）：请参阅 ./error-handle.md