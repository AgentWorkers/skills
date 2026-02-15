---
name: moonpay
description: MoonPay 支持将法定货币（fiat currency）转换为加密货币（crypto currency）的快速入门集成服务。用户可以通过信用卡、银行转账和移动支付等方式购买和出售加密货币。
metadata: {"clawdbot":{"emoji":"🌙","always":true,"requires":{"bins":["curl","jq"]}}}
---

# MoonPay 🌙

领先的法定货币到加密货币的转换平台。支持在160多个国家使用信用卡、银行转账和移动支付方式购买加密货币。

## 环境变量

| 变量 | 描述 | 是否必需 |
|----------|-------------|----------|
| `MOONPAY_API_KEY` | 可公开的API密钥 | 是 |
| `MOONPAY_SECRET_KEY` | 用于签名的密钥 | 是 |
| `MOONPAY_ENV` | `sandbox` 或 `production` | 否 |

## 主要功能

- 💳 **信用卡支付** - 支持Visa、Mastercard、Apple Pay、Google Pay |
- 🏦 **银行转账** - 支持SEPA、ACH、Faster Payments |
- 📱 **移动支付** - 支持PIX、GCash、GrabPay |
- 🔄 **将加密货币兑换回法定货币** |
- 🎨 **NFT支付** - 支持使用法定货币购买NFT |

## API基础URL

- 测试环境：`https://api.moonpay.com`（使用测试API密钥） |
- 生产环境：`https://api.moonpay.com` |

## 获取支持的货币

```bash
API_KEY="${MOONPAY_API_KEY}"

# Get crypto currencies
curl -s "https://api.moonpay.com/v3/currencies" \
  -H "Authorization: Api-Key ${API_KEY}" | jq '.[] | select(.type == "crypto") | {code: .code, name: .name, minBuyAmount: .minBuyAmount}'

# Get fiat currencies
curl -s "https://api.moonpay.com/v3/currencies" \
  -H "Authorization: Api-Key ${API_KEY}" | jq '.[] | select(.type == "fiat") | {code: .code, name: .name}'
```

## 获取报价

```bash
API_KEY="${MOONPAY_API_KEY}"
BASE_CURRENCY="usd"
QUOTE_CURRENCY="eth"
BASE_AMOUNT="100"

curl -s "https://api.moonpay.com/v3/currencies/${QUOTE_CURRENCY}/buy_quote" \
  -G \
  --data-urlencode "apiKey=${API_KEY}" \
  --data-urlencode "baseCurrencyCode=${BASE_CURRENCY}" \
  --data-urlencode "baseCurrencyAmount=${BASE_AMOUNT}" | jq '{
    quoteCurrencyAmount: .quoteCurrencyAmount,
    feeAmount: .feeAmount,
    networkFeeAmount: .networkFeeAmount,
    totalAmount: .totalAmount,
    extraFeeAmount: .extraFeeAmount
  }'
```

## 生成插件URL

```bash
API_KEY="${MOONPAY_API_KEY}"
SECRET_KEY="${MOONPAY_SECRET_KEY}"

# Build widget URL
BASE_URL="https://buy.moonpay.com"
PARAMS="?apiKey=${API_KEY}&currencyCode=eth&walletAddress=<WALLET>&baseCurrencyAmount=100"

# Sign URL (required for production)
SIGNATURE=$(echo -n "${PARAMS}" | openssl dgst -sha256 -hmac "${SECRET_KEY}" -binary | base64 | tr '+/' '-_' | tr -d '=')

WIDGET_URL="${BASE_URL}${PARAMS}&signature=${SIGNATURE}"
echo "Widget URL: $WIDGET_URL"
```

## 创建交易（服务器端）

```bash
API_KEY="${MOONPAY_API_KEY}"
SECRET_KEY="${MOONPAY_SECRET_KEY}"

curl -s -X POST "https://api.moonpay.com/v3/transactions" \
  -H "Authorization: Api-Key ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "baseCurrencyCode": "usd",
    "baseCurrencyAmount": 100,
    "quoteCurrencyCode": "eth",
    "walletAddress": "<WALLET_ADDRESS>",
    "returnUrl": "https://your-app.com/success",
    "externalCustomerId": "customer-123"
  }' | jq '.'
```

## 检查交易状态

```bash
API_KEY="${MOONPAY_API_KEY}"
TX_ID="<TRANSACTION_ID>"

curl -s "https://api.moonpay.com/v3/transactions/${TX_ID}" \
  -H "Authorization: Api-Key ${API_KEY}" | jq '{
    status: .status,
    cryptoTransactionId: .cryptoTransactionId,
    quoteCurrencyAmount: .quoteCurrencyAmount,
    walletAddress: .walletAddress
  }'
```

## 交易状态代码

| 状态 | 描述 |
|--------|-------------|
| `waitingPayment` | 正在等待付款 |
| `pending` | 收到付款，正在处理中 |
| `waitingAuthorization` | 正在等待3DS认证或银行授权 |
| `completed` | 交易成功完成 |
| `failed` | 交易失败 |

## 支持的支付方式

| 支付方式 | 支持地区 | 支付速度 |
|--------|---------|-------|
| 信用卡/借记卡 | 全球 | 即时 |
| Apple Pay | 全球 | 即时 |
| Google Pay | 全球 | 即时 |
| SEPA | 欧洲 | 1-2天 |
| ACH | 美国 | 3-5天 |
| Faster Payments | 英国 | 即时 |
| PIX | 巴西 | 即时 |
| iDEAL | 荷兰 | 即时 |

## 支持的加密货币

| 类别 | 币种 |
|----------|--------|
| 主流加密货币 | BTC、ETH、SOL、MATIC、AVAX |
| 稳定币 | USDT、USDC、DAI |
| 第二层网络（L2）代币 | ARB、OP、BASE |
| 赞助币（Meme） | DOGE、SHIB |

## Webhook事件

```bash
# Webhook payload structure
{
  "type": "transaction_updated",
  "data": {
    "id": "tx-123",
    "status": "completed",
    "cryptoTransactionId": "0x...",
    "quoteCurrencyAmount": 0.05,
    "walletAddress": "0x..."
  }
}
```

## 验证Webhook签名

```bash
verify_webhook() {
  local payload="$1"
  local signature="$2"
  
  local expected=$(echo -n "$payload" | openssl dgst -sha256 -hmac "$MOONPAY_SECRET_KEY" -binary | base64)
  
  [[ "$signature" == "$expected" ]]
}
```

## 插件定制

```bash
# Widget parameters
PARAMS="?apiKey=${API_KEY}"
PARAMS+="&currencyCode=eth"
PARAMS+="&walletAddress=<WALLET>"
PARAMS+="&baseCurrencyAmount=100"
PARAMS+="&baseCurrencyCode=usd"
PARAMS+="&lockAmount=true"           # Lock amount
PARAMS+="&colorCode=%23FF6B00"       # Custom color
PARAMS+="&language=en"               # Language
PARAMS+="&showWalletAddressForm=false"  # Hide wallet input
```

## 安全规则

1. **在生产环境中** **务必** 对插件URL进行加密处理。
2. **绝对不要** 在客户端暴露密钥。
3. **务必** 验证Webhook签名。
4. **在完成交易前** **务必** 检查交易状态。

## 错误代码

| 代码 | 描述 |
|------|-------------|
| `invalid_api_key` | API密钥无效 |
| `invalid_signature` | URL签名不匹配 |
| `currency_not_supported` | 支持的货币不存在 |
| `amount_too_low` | 金额过低 |
| `amount_too_high` | 金额过高 |

## 链接

- [MoonPay文档](https://docs.moonpay.com/) |
- [控制面板](https://dashboard.moonpay.com/) |
- [插件构建工具](https://dashboard.moonpay.com/widget)