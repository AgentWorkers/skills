---
name: paytrigo-openclawbot
description: **使用场景：**  
当 OpenClawBot 需要在没有 Webhook 的情况下创建或验证基于 Base/USDC 的 PayTrigo 支付时，请使用此方法。
metadata: {"openclaw":{}}
---

# PayTrigo（OpenClawBot，支持Base/USDC）

此技能提供了一种简单的、适用于PayTrigo的支付流程，该流程仅使用**平台API密钥**和**Base/USDC**进行支付。该流程专为不使用Webhook、而是通过轮询来获取支付状态的OpenClawBot进行了优化。平台API密钥已嵌入到辅助脚本中，无需额外设置即可使用。

## 假设条件
- 必须使用**平台API密钥**（并且需要提供**`recipientAddress`）。
- 该API密钥仅支持Base/USDC作为支付链/货币（根据平台费用配置设置）。
- Bot可以存储在创建发票时返回的`invoiceId`和`checkoutToken`。

## 不需要环境变量
辅助脚本中已包含API密钥，因此OpenClawBot可以直接使用。

## 安装要求
需要Node.js 18及以上版本。

```
npm install
```

## 建议的本地钱包存储方式
OpenClawBot可以将收款人地址和加密后的付款人钱包信息存储在本地（无需外部服务）。

### 1) 创建本地钱包
```
node {baseDir}/scripts/moltbot-wallet-setup.mjs create --passphrase-file ./passphrase.txt --set-recipient-from-wallet
```
此操作会生成`.openclawbot/wallet.json`、`.openclawbot/wallet-address.txt`和`.openclawbot/recipient.txt`文件。

### 如果您已经拥有钱包
则无需重新创建。

```
node {baseDir}/scripts/moltbot-wallet-setup.mjs recipient --address 0xYourWallet
node {baseDir}/scripts/moltbot-wallet-setup.mjs import --pk-file ./payer.pk --passphrase-file ./passphrase.txt --set-recipient-from-wallet
```

### 2) 使用存储的数据执行支付流程
```
node {baseDir}/scripts/moltbot-human-flow.mjs human --amount 0.001
node {baseDir}/scripts/moltbot-bot-flow.mjs bot --amount 0.001 --passphrase-file ./passphrase.txt
```

### 3) 可选：设置单独的收款人地址
```
node {baseDir}/scripts/moltbot-wallet-setup.mjs recipient --address 0xYourWallet
```

## 快速入门（CLI脚本）
可以使用预设的脚本来测试端到端的支付流程，无需额外设置。

### 人工干预（用户在浏览器中完成支付）
```
node {baseDir}/scripts/moltbot-human-flow.mjs human --amount 0.001 --recipient 0xYourWallet...
```

### Bot直接完成支付（需要私钥）
```
node {baseDir}/scripts/moltbot-bot-flow.mjs bot --amount 0.001 --recipient 0xYourWallet... --pk 0xPRIVATE_KEY
```

有关OpenClawBot的详细使用指南，请参阅该文件夹中的`README.md`文件。

## 核心流程（人工干预）
1) **创建发票**（需要平台API密钥、Base/USDC和收款人地址）
2) 将`payUrl`发送给用户（用户需进行批准并完成支付）
3) 轮询发票状态，直到状态变为`confirmed`、`expired`、`invalid`或`refunded`。

## 核心流程（Bot直接完成支付）
1) 创建发票
2) 获取支付意图（批准或支付的详细信息）
3) 在链上发送交易（必要时先进行批准，然后完成支付）
4) 提交交易哈希值（`txHash`）
5) 轮询发票状态

> 重要提示：**直接进行token转移是无效的**。请始终使用`/intent`路径下的`steps.pay`接口来完成支付操作。

---

# API使用说明（HTTP请求）

## 1) 创建发票
**接口地址**：`POST /v1/invoices`

**请求头**：
- `Authorization: Bearer <platform_key>`（如果直接通过HTTP请求，则必须提供）
- `Content-Type: application/json`
- `Idempotency-Key: pay_attempt_<uuid>`

**请求体**（固定使用Base/USDC作为支付货币，且必须提供`recipientAddress`）：
```json
{
  "amount": "49.99",
  "recipientAddress": "0xYourWallet...",
  "ttlSeconds": 900,
  "metadata": { "botId": "openclawbot_123", "purpose": "checkout" }
}
```

**响应**中包含`invoiceId`、`payUrl`、`checkoutToken`和`expiresAt`信息。

## 2) 获取支付意图（Bot执行支付）
**接口地址**：`GET /v1/invoices/{invoiceId}/intent?chain=base&token=usdc`

**推荐使用的请求头**：
- `X-Checkout-Token: <checkoutToken>`

**响应**中包含`steps.approve`、`steps.pay`、`routerAddress`和`grossAmountAtomic`信息。

## 3) 提交支付意图（包含交易哈希值）
**接口地址**：`POST /v1/invoices/{invoiceId}/payment-intents`

**请求头**：
- `X-Checkout-Token: <checkoutToken>`
- `Content-Type: application/json`

**请求体**：
```json
{ "txHash": "0x...", "payerAddress": "0x..." }
```

## 4) 轮询发票状态
**接口地址**：`GET /v1/invoices/{invoiceId}`

**请求头**：
- `X-Checkout-Token: <checkoutToken>`

**轮询规则**：
- 交易提交后立即开始轮询：每3-5秒轮询一次，持续2分钟。
- 2分钟后：每10-15秒轮询一次。
- 当发票状态变为`confirmed`、`expired`、`invalid`或`refunded`时，停止轮询。
- 如果收到`429`错误代码，应稍后重试。

---

# 常见错误
- 使用平台API密钥时未提供`recipientAddress`（导致请求无效）
- 直接进行token转移（应使用`Router`的`steps.pay`接口）
- 丢失`checkoutToken`（该Token仅在创建发票时才会被返回）