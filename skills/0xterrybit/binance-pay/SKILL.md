---
name: binance-pay
description: **Binance Pay集成：支持加密货币支付**  
您可以借助全球最大的加密货币交易平台Binance进行加密货币的发送、接收和接受操作。
metadata: {"clawdbot":{"emoji":"🟡","requires":{"bins":["curl","jq"],"env":["BINANCE_PAY_API_KEY","BINANCE_PAY_SECRET"]}}}
---

# Binance Pay 🟡

这是一个由全球最大的加密货币交易所 Binance 提供的加密货币支付解决方案。

## 环境变量

| 变量 | 描述 | 是否必需 |
|----------|-------------|----------|
| `BINANCE_PAY_API_KEY` | 商户 API 密钥 | 是 |
| `BINANCE_PAY_SECRET` | API 秘密密钥 | 是 |
| `BINANCE_PAY_MERCHANT_ID` | 商户 ID | 是 |

## 功能

- 💸 **C2C 转账** - 向 Binance 用户发送加密货币（免费）
- 🛒 **商户收款** - 接受加密货币支付 |
- 🔄 **退款** - 处理退款请求 |
- 📊 **订单管理** - 跟踪支付状态 |
- 🌍 **2 亿+ 用户** - 可访问 Binance 生态系统

## API 基本 URL

```
https://bpay.binanceapi.com
```

## 认证

```bash
API_KEY="${BINANCE_PAY_API_KEY}"
SECRET="${BINANCE_PAY_SECRET}"
TIMESTAMP=$(date +%s%3N)
NONCE=$(openssl rand -hex 16)

# Generate signature
generate_signature() {
  local payload="$1"
  local sign_string="${TIMESTAMP}\n${NONCE}\n${payload}\n"
  echo -n "$sign_string" | openssl dgst -sha512 -hmac "$SECRET" | cut -d' ' -f2 | tr '[:lower:]' '[:upper:]'
}
```

## 创建支付订单

```bash
PAYLOAD='{
  "env": {
    "terminalType": "WEB"
  },
  "merchantTradeNo": "'"$(date +%s)"'",
  "orderAmount": "10.00",
  "currency": "USDT",
  "goods": {
    "goodsType": "01",
    "goodsCategory": "D000",
    "referenceGoodsId": "product-001",
    "goodsName": "Product Name"
  }
}'

SIGNATURE=$(generate_signature "$PAYLOAD")

curl -s -X POST "https://bpay.binanceapi.com/binancepay/openapi/v2/order" \
  -H "Content-Type: application/json" \
  -H "BinancePay-Timestamp: ${TIMESTAMP}" \
  -H "BinancePay-Nonce: ${NONCE}" \
  -H "BinancePay-Certificate-SN: ${API_KEY}" \
  -H "BinancePay-Signature: ${SIGNATURE}" \
  -d "$PAYLOAD" | jq '.'
```

## 查询订单状态

```bash
PAYLOAD='{
  "merchantTradeNo": "<ORDER_ID>"
}'

SIGNATURE=$(generate_signature "$PAYLOAD")

curl -s -X POST "https://bpay.binanceapi.com/binancepay/openapi/v2/order/query" \
  -H "Content-Type: application/json" \
  -H "BinancePay-Timestamp: ${TIMESTAMP}" \
  -H "BinancePay-Nonce: ${NONCE}" \
  -H "BinancePay-Certificate-SN: ${API_KEY}" \
  -H "BinancePay-Signature: ${SIGNATURE}" \
  -d "$PAYLOAD" | jq '.'
```

## 关闭订单

```bash
PAYLOAD='{
  "merchantTradeNo": "<ORDER_ID>"
}'

SIGNATURE=$(generate_signature "$PAYLOAD")

curl -s -X POST "https://bpay.binanceapi.com/binancepay/openapi/v2/order/close" \
  -H "Content-Type: application/json" \
  -H "BinancePay-Timestamp: ${TIMESTAMP}" \
  -H "BinancePay-Nonce: ${NONCE}" \
  -H "BinancePay-Certificate-SN: ${API_KEY}" \
  -H "BinancePay-Signature: ${SIGNATURE}" \
  -d "$PAYLOAD" | jq '.'
```

## 处理退款

```bash
PAYLOAD='{
  "refundRequestId": "'"$(date +%s)"'",
  "prepayId": "<PREPAY_ID>",
  "refundAmount": "5.00"
}'

SIGNATURE=$(generate_signature "$PAYLOAD")

curl -s -X POST "https://bpay.binanceapi.com/binancepay/openapi/v2/order/refund" \
  -H "Content-Type: application/json" \
  -H "BinancePay-Timestamp: ${TIMESTAMP}" \
  -H "BinancePay-Nonce: ${NONCE}" \
  -H "BinancePay-Certificate-SN: ${API_KEY}" \
  -H "BinancePay-Signature: ${SIGNATURE}" \
  -d "$PAYLOAD" | jq '.'
```

## 支持的货币

| 货币 | 类型 | 最小金额 |
|----------|------|------------|
| USDT | 稳定币 | 0.01 |
| BUSD | 稳定币 | 0.01 |
| USDC | 稳定币 | 0.01 |
| BTC | 加密货币 | 0.00001 |
| ETH | 加密货币 | 0.0001 |
| BNB | 加密货币 | 0.001 |

## Webhook 事件

| 事件 | 描述 |
|-------|-------------|
| `PAY` | 支付完成 |
| `REFUND` | 退款处理中 |
| `CANCEL` | 订单已取消 |

## Webhook 验证

```bash
# Verify webhook signature
verify_webhook() {
  local payload="$1"
  local received_sig="$2"
  local timestamp="$3"
  local nonce="$4"
  
  local sign_string="${timestamp}\n${nonce}\n${payload}\n"
  local expected_sig=$(echo -n "$sign_string" | openssl dgst -sha512 -hmac "$SECRET" | cut -d' ' -f2 | tr '[:lower:]' '[:upper:]')
  
  [[ "$received_sig" == "$expected_sig" ]]
}
```

## 订单状态代码

| 状态 | 描述 |
|--------|-------------|
| `INITIAL` | 订单创建 |
| `PENDING` | 等待支付 |
| `PAID` | 支付成功 |
| `CANCELED` | 订单已取消 |
| `REFUNDING` | 退款中 |
| `REFUNDED` | 退款完成 |
| `EXPIRED` | 订单过期 |

## 安全规则

1. **始终** 验证 webhook 签名。
2. **绝不要** 暴露 API 秘密信息。
3. **始终** 使用 idempotent merchantTradeNo。
4. **在完成交易前** 检查订单状态。

## 链接

- [Binance Pay 文档](https://developers.binance.com/docs/binance-pay)
- [商户门户](https://merchant.binance.com/)
- [API 参考](https://developers.binance.com/docs/binance-pay/api-order-create-v2)