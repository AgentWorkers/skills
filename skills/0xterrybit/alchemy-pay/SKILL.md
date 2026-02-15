---
name: alchemy-pay
description: Alchemy Pay（ACH）是一种支持法定货币（Fiat）与加密货币之间转换的支付网关服务，提供接入（on-ramp）和退出（off-ramp）机制，支持商家付款（merchant payments）以及NFT（非同质化代币）结算（NFT checkout services）。
metadata: {"clawdbot":{"emoji":"💎","requires":{"bins":["curl","jq"],"env":["ALCHEMY_PAY_APP_ID","ALCHEMY_PAY_SECRET"]}}}
---

# Alchemy Pay 💎

这是一个混合支付基础设施，能够连接加密货币与传统金融系统。它与 Binance Pay、Solana Pay 以及全球 300 多种支付渠道集成在一起。

## 环境变量

| 变量          | 描述                | 是否必填 |
|---------------|-------------------|---------|
| `ALCHEMY_PAY_APP_ID` | 商户应用 ID            | 是       |
| `ALCHEMY_PAY_SECRET` | API 密钥                | 是       |
| `ALCHEMY_PAY_ENV` | 环境：`sandbox` 或 `production` | 否       | 默认值：sandbox |

## 主要功能

- 🔄 **充值**：支持使用法定货币购买加密货币（覆盖 170 多个国家）  
- 💸 **提现**：支持将加密货币兑换为法定货币  
- 🛒 **商户支付**：接受加密货币支付  
- 🎨 **NFT 购买**：支持使用法定货币购买 NFT  
- 🌍 **全球覆盖**：在亚洲和拉丁美洲地区具有强大的市场影响力  

## API 端点

### 基本 URL  
- 沙箱环境：`https://openapi-test.alchemypay.org`  
- 生产环境：`https://openapi.alchemypay.org`  

### 创建充值订单  
```bash
APP_ID="${ALCHEMY_PAY_APP_ID}"
SECRET="${ALCHEMY_PAY_SECRET}"
BASE_URL="${ALCHEMY_PAY_ENV:-sandbox}"
[[ "$BASE_URL" == "production" ]] && BASE_URL="https://openapi.alchemypay.org" || BASE_URL="https://openapi-test.alchemypay.org"

TIMESTAMP=$(date +%s)
NONCE=$(openssl rand -hex 16)

# Create signature
SIGN_STRING="appId=${APP_ID}&nonce=${NONCE}&timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "${SIGN_STRING}${SECRET}" | sha256sum | cut -d' ' -f1)

curl -s -X POST "${BASE_URL}/open/api/v4/merchant/order/create" \
  -H "Content-Type: application/json" \
  -H "appId: ${APP_ID}" \
  -H "timestamp: ${TIMESTAMP}" \
  -H "nonce: ${NONCE}" \
  -H "sign: ${SIGNATURE}" \
  -d '{
    "crypto": "USDT",
    "network": "ETH",
    "fiat": "USD",
    "fiatAmount": "100",
    "walletAddress": "<USER_WALLET>",
    "callbackUrl": "https://your-callback.com/webhook"
  }' | jq '.'
```  

### 获取支持的加密货币  
```bash
curl -s "${BASE_URL}/open/api/v4/merchant/crypto/list" \
  -H "appId: ${APP_ID}" \
  -H "timestamp: ${TIMESTAMP}" \
  -H "nonce: ${NONCE}" \
  -H "sign: ${SIGNATURE}" | jq '.data'
```  

### 获取汇率  
```bash
curl -s "${BASE_URL}/open/api/v4/merchant/price" \
  -H "appId: ${APP_ID}" \
  -H "timestamp: ${TIMESTAMP}" \
  -H "nonce: ${NONCE}" \
  -H "sign: ${SIGNATURE}" \
  -G --data-urlencode "crypto=BTC" \
     --data-urlencode "fiat=USD" | jq '.data'
```  

### 查看订单状态  
```bash
ORDER_ID="<ORDER_ID>"

curl -s "${BASE_URL}/open/api/v4/merchant/order/query" \
  -H "appId: ${APP_ID}" \
  -H "timestamp: ${TIMESTAMP}" \
  -H "nonce: ${NONCE}" \
  -H "sign: ${SIGNATURE}" \
  -G --data-urlencode "orderId=${ORDER_ID}" | jq '.'
```  

## 支持的支付方式  

| 地区        | 支付方式                |
|------------|----------------------|---------|
| 全球        | Visa、Mastercard、Apple Pay、Google Pay |        |
| 亚洲        | Alipay、WeChat Pay、GrabPay、GCash    |        |
| 拉丁美洲      | PIX、SPEI、PSE             |        |
| 欧洲        | SEPA、iDEAL、Bancontact         |        |

## 支持的加密货币  

- **EVM**：ETH、USDT、USDC、BNB、MATIC  
- **Solana**：SOL、USDC-SPL  
- **比特币**：BTC  
- **其他**：TRX、AVAX、ARB  

## 小程序集成  
```html
<!-- Embed Alchemy Pay widget -->
<iframe 
  src="https://ramp.alchemypay.org?appId=YOUR_APP_ID&crypto=ETH&network=ETH&fiat=USD"
  width="400" 
  height="600"
  frameborder="0">
</iframe>
```  

## Webhook 事件  

| 事件          | 描述                        |         |
|--------------|-----------------------------|---------|
| `PAY_SUCCESS` | 支付完成                    |         |
| `PAY_FAIL` | 支付失败                    |         |
| `REFUND_SUCCESS` | 退款处理完成                |         |

## 安全规则  

1. **务必** 验证 Webhook 签名。  
2. **切勿** 将 API 密钥暴露在客户端代码中。  
3. **回调请求** **必须** 使用 HTTPS 协议。  
4. **确认** 订单金额与预期值一致。  

## 错误代码  

| 代码          | 描述                        |         |
|--------------|-----------------------------|---------|
| 10001         | 签名无效                    |         |
| 10002         | 参数错误                      |         |
| 10003         | 订单未找到                    |         |
| 20001         | 账户余额不足                    |         |

## 链接  

- [Alchemy Pay 文档](https://alchemypay.readme.io/)  
- [控制面板](https://dashboard.alchemypay.org/)  
- [状态页面](https://status.alchemypay.org/)