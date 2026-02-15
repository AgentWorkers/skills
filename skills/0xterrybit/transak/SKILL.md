---
name: transak
description: Web3的法定货币到加密货币的转换服务：支持170多个国家中的100多种支付方式，用于买卖加密货币。
metadata: {"clawdbot":{"emoji":"🚀","always":true,"requires":{"bins":["curl","jq"]}}}
---

# Transak 🚀  
Web3支付基础设施，支持600多个DeFi、NFT和钱包项目之间的法币转换（Fiat on/off-ramp服务）。  

## 环境变量  
| 变量 | 描述 | 是否必填 |  
|---------|-------------|---------|  
| `TRANSAK_API_KEY` | API密钥 | 是 |  
| `TRANSAK_SECRET` | Webhook的密钥 | 否 |  
| `TRANSAK_ENV` | 环境（STAGING或PRODUCTION） | 否 |  

## 主要功能  
- 🌍 **覆盖170多个国家**  
- 💳 **支持100多种支付方式**：信用卡、银行转账、移动支付  
- ⛓️ **兼容75多种区块链**：EVM、Solana、Bitcoin等  
- 🔄 **法币转换功能**：可将加密货币兑换为法币  
- 🎨 **NFT购买**：直接支持NFT交易  
- 🔌 **插件SDK**：易于集成到应用程序中  

## API基础URL  
- 测试环境：`https://api-stg.transak.com`  
- 生产环境：`https://api.transak.com`  

## 支持的加密货币  
```bash
API_KEY="${TRANSAK_API_KEY}"
ENV="${TRANSAK_ENV:-STAGING}"
[[ "$ENV" == "PRODUCTION" ]] && BASE_URL="https://api.transak.com" || BASE_URL="https://api-stg.transak.com"

curl -s "${BASE_URL}/api/v2/currencies/crypto-currencies" | jq '.response[:10] | .[] | {symbol: .symbol, name: .name, network: .network.name}'
```  

## 支持的法币  
```bash
curl -s "${BASE_URL}/api/v2/currencies/fiat-currencies" | jq '.response[:10] | .[] | {symbol: .symbol, name: .name, paymentOptions: .paymentOptions}'
```  

## 获取价格报价  
```bash
FIAT="USD"
CRYPTO="ETH"
FIAT_AMOUNT="100"
NETWORK="ethereum"
PAYMENT_METHOD="credit_debit_card"

curl -s "${BASE_URL}/api/v2/currencies/price" \
  -G \
  --data-urlencode "fiatCurrency=${FIAT}" \
  --data-urlencode "cryptoCurrency=${CRYPTO}" \
  --data-urlencode "fiatAmount=${FIAT_AMOUNT}" \
  --data-urlencode "network=${NETWORK}" \
  --data-urlencode "paymentMethod=${PAYMENT_METHOD}" \
  --data-urlencode "isBuyOrSell=BUY" | jq '{
    cryptoAmount: .response.cryptoAmount,
    fiatAmount: .response.fiatAmount,
    totalFee: .response.totalFee,
    conversionPrice: .response.conversionPrice
  }'
```  

## 生成插件URL  
```bash
API_KEY="${TRANSAK_API_KEY}"
WALLET_ADDRESS="<USER_WALLET>"
CRYPTO="ETH"
NETWORK="ethereum"
FIAT_AMOUNT="100"
FIAT_CURRENCY="USD"

# Build widget URL
WIDGET_URL="https://global.transak.com/?apiKey=${API_KEY}"
WIDGET_URL+="&walletAddress=${WALLET_ADDRESS}"
WIDGET_URL+="&cryptoCurrencyCode=${CRYPTO}"
WIDGET_URL+="&network=${NETWORK}"
WIDGET_URL+="&fiatAmount=${FIAT_AMOUNT}"
WIDGET_URL+="&fiatCurrency=${FIAT_CURRENCY}"
WIDGET_URL+="&productsAvailed=BUY"

echo "Widget URL: $WIDGET_URL"
```  

## 查看订单状态  
```bash
ORDER_ID="<ORDER_ID>"

curl -s "${BASE_URL}/api/v2/partners/order/${ORDER_ID}" \
  -H "api-key: ${API_KEY}" | jq '{
    status: .response.status,
    cryptoAmount: .response.cryptoAmount,
    transactionHash: .response.transactionHash,
    walletAddress: .response.walletAddress
  }'
```  

## 支持的网络  
| 网络 | ID | 支持的代币 |  
|---------|-----|--------|  
| Ethereum | ethereum | ETH、USDT、USDC、DAI |  
| Polygon | polygon | MATIC、USDT、USDC |  
| Arbitrum | arbitrum | ETH、ARB、USDC |  
| Optimism | optimism | ETH、OP、USDC |  
| BSC | bsc | BNB、BUSD、USDT |  
| Solana | solana | SOL、USDC |  
| Avalanche | avaxcchain | AVAX、USDC |  
| Base | base | ETH、USDC |  
| Bitcoin | bitcoin | BTC |  

## 支付方式  
| 支付方式 | 支持地区 | 处理速度 |  
|---------|---------|---------|  
| 信用卡/借记卡 | 全球 | 即时 |  
| Apple Pay | 全球 | 即时 |  
| Google Pay | 全球 | 即时 |  
| 银行转账 | 全球 | 1-3天 |  
| SEPA | 欧洲 | 1-2天 |  
| PIX | 巴西 | 即时 |  
| UPI | 印度 | 即时 |  
| GCash | 菲律宾 | 即时 |  
| GrabPay | 东南亚 | 即时 |  

## 订单状态代码  
| 状态 | 说明 |  
|---------|-------------|---------|  
| `AWAITING_payment_FROM_USER` | 等待用户付款 |  
| `PAYMENT_DONE_MARKED_BY_USER` | 用户已提交付款 |  
| `PROCESSING` | 正在处理订单 |  
| `PENDING_DELIVERY_FROM_TRANSAK` | 正在发送加密货币 |  
| `COMPLETED` | 订单已完成 |  
| `CANCELLED` | 订单已取消 |  
| `FAILED` | 订单失败 |  
| `REFUNDED` | 退款完成 |  
| `EXPIRED` | 订单已过期 |  

## Webhook事件  
```bash
# Webhook payload
{
  "eventID": "ORDER_COMPLETED",
  "webhookData": {
    "id": "order-123",
    "status": "COMPLETED",
    "cryptoAmount": 0.05,
    "cryptoCurrency": "ETH",
    "transactionHash": "0x...",
    "walletAddress": "0x..."
  }
}
```  

## 验证Webhook  
```bash
verify_webhook() {
  local payload="$1"
  local signature="$2"
  
  local expected=$(echo -n "$payload" | openssl dgst -sha256 -hmac "$TRANSAK_SECRET" | cut -d' ' -f2)
  
  [[ "$signature" == "$expected" ]]
}
```  

## 插件定制  
```bash
# Additional widget parameters
WIDGET_URL+="&themeColor=0066FF"           # Custom color
WIDGET_URL+="&hideMenu=true"               # Hide menu
WIDGET_URL+="&disableWalletAddressForm=true"  # Lock wallet
WIDGET_URL+="&exchangeScreenTitle=Buy%20Crypto"  # Custom title
WIDGET_URL+="&defaultPaymentMethod=credit_debit_card"
```  

## 安全规则  
1. **务必验证** Webhook签名。  
2. **切勿** 在客户端暴露API密钥。  
3. **在完成交易前** 需要检查订单状态。  
4. **验证** 支付钱包地址的合法性。  

## 错误处理  
| 错误类型 | 原因 | 解决方案 |  
|---------|---------|---------|  
| `INVALID_API_KEY` | API密钥无效 | 请检查凭证。  
| `UNSUPPORTED_crypto` | 该货币不受支持 | 请查看支持的货币列表。  
| `AMOUNT_TOO_LOW` | 金额过低 | 请增加金额。  
| `AMOUNT_TOO_HIGH` | 金额过高 | 请降低金额。  

## 链接  
- [Transak文档](https://docs.transak.com/)  
- [控制面板](https://dashboard.transak.com/)  
- [插件演示](https://global.transak.com/)