---
name: mpc-accept-crypto-payments
description: 通过 MoonPay Commerce（前身为 Helio）在 Solana 上接受加密货币支付。您可以创建支付链接、生成结账 URL、查看交易记录以及查询支持的货币种类。当用户希望接受加密货币支付、使用加密货币为产品或服务收费或查询支付交易时，可以使用该功能。使用该服务需要拥有 MoonPay Commerce 账户以及相应的 API 密钥和密钥。
metadata:
  openclaw:
    requires:
      bins:
        - jq
        - curl
      env:
        - HELIO_API_KEY
        - HELIO_API_SECRET
    credentials:
      storage: ~/.mpc/helio/config
      setup: bash scripts/setup.sh
      permissions: "600"
---

# MPC：接受加密货币支付

这是一项用于在Solana平台上通过MoonPay Commerce（前身为Helio）接受加密货币支付的商户端功能。

## 设置

使用您的API凭据运行设置脚本（钱包ID会自动获取）：

```bash
bash scripts/setup.sh
```

您需要以下信息：
- **API密钥** — 从 https://app.hel.io → 设置 → API密钥 获取
- **API密钥** — 也在同一页面上生成，请妥善保存

设置脚本将执行以下操作：
1. 验证您的凭据是否有效
2. 自动获取您的Solana钱包信息
3. 选择用于支付的钱包（如果不存在PAYOUT钱包，则选择“CONNECTED”）
4. 将所有设置保存到 `~/.mpc/helio/config` 文件中

如果用户还没有账户，请引导他们访问 https://app.hel.io 进行注册。

### 配置管理
```bash
bash scripts/setup.sh status   # Show current config
bash scripts/setup.sh clear    # Remove saved credentials
```

## 快速参考

基础URL：`https://api.hel.io/v1`

### 支持的货币列表（无需认证）
```bash
curl -s https://api.hel.io/v1/currency | jq '.[].symbol'
```

### 创建支付链接
```bash
curl -s -X POST "https://api.hel.io/v1/paylink/create/api-key?apiKey=$HELIO_API_KEY" \
  -H "Authorization: Bearer $HELIO_API_SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Payment",
    "template": "OTHER",
    "pricingCurrency": "<CURRENCY_ID>",
    "price": "<AMOUNT_IN_BASE_UNITS>",
    "features": {
      "canChangePrice": false,
      "canChangeQuantity": false,
      "canSwapTokens": true
    },
    "recipients": [{
      "currencyId": "<CURRENCY_ID>",
      "walletId": "<YOUR_WALLET_ID>"
    }]
  }'
```

**默认设置：** 使用的货币为USDC（`6340313846e4f91b8abc519b`）。系统支持Token交换，因此付款人可以使用任何支持的Solana代币进行支付（系统会自动将其转换为USDC）。

**价格格式：** `price` 以基本单位表示（int64字符串格式）。例如：
- USDC：`"1000000"` 表示1 USDC
- SOL：`"1000000000"` 表示1 SOL

### 创建支付请求（结账链接）
```bash
curl -s -X POST "https://api.hel.io/v1/charge/api-key?apiKey=$HELIO_API_KEY" \
  -H "Authorization: Bearer $HELIO_API_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"paymentRequestId": "<PAYLINK_ID>"}'
```
返回的结果格式为：`{"id": "...", "pageUrl": "https://..."}` — 请将 `pageUrl` 分享给付款人。

### 查看交易记录
```bash
curl -s "https://api.hel.io/v1/paylink/<PAYLINK_ID>/transactions?apiKey=$HELIO_API_KEY" \
  -H "Authorization: Bearer $HELIO_API_SECRET"
```

### 禁用/启用支付链接
```bash
curl -s -X PATCH "https://api.hel.io/v1/paylink/<PAYLINK_ID>/disable?apiKey=$HELIO_API_KEY&disabled=true" \
  -H "Authorization: Bearer $HELIO_API_SECRET"
```

## 辅助脚本
```bash
# Setup (run first)
bash scripts/setup.sh

# Operations
bash scripts/helio.sh currencies
bash scripts/helio.sh create-paylink "Coffee" 5.00 USDC
bash scripts/helio.sh charge <paylink-id>
bash scripts/helio.sh transactions <paylink-id>
bash scripts/helio.sh disable <paylink-id>
bash scripts/helio.sh enable <paylink-id>
```

## 模板

`template` 字段用于指定支付链接的类型：
- `OTHER`：通用支付
- `PRODUCT`：实物/数字产品
- `INVOICE`：发票
- `SUBSCRIPTION`：订阅服务（需要提供 `subscriptionDetails`）
- `EVENT`：活动门票

## 凭据管理

在设置凭据时，请交互式地运行设置脚本：
```bash
bash scripts/setup.sh
```

脚本会直接在终端中提示您输入凭据，这些凭据不会被保存在聊天记录或日志中。凭据会被保存到 `~/.mpc/helio/config` 文件中（权限设置为600）。

## 高级功能

- 完整的API接口文档：请参阅 `references/api-reference.md`
- OpenAPI规范：https://api.hel.io/v1/docs-json
- 仪表盘：https://app.hel.io
- 官方文档：https://docs.hel.io