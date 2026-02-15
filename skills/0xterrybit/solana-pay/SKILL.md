---
name: solana-pay
description: Solana Pay 协议集成：在 Solana 区块链上生成支付请求、二维码，并验证交易。
metadata: {"clawdbot":{"emoji":"⚡","requires":{"bins":["solana","curl","jq","qrencode"],"env":["SOLANA_KEYPAIR_PATH"]}}}
---

# Solana Pay ⚡

基于Solana构建的去中心化支付协议，支持即时支付且手续费接近于零。

## 环境变量

| 变量 | 描述 | 是否必需 |
|----------|-------------|----------|
| `SOLANA_KEYPAIR_PATH` | 商户钱包密钥对的路径 | 是 |
| `SOLANA_RPC_URL` | 自定义RPC端点 | 否 |
| `MERCHANT_NAME` | 支付显示名称 | 否 |

## 主要功能

- 💸 **即时支付**：交易确认时间约400毫秒 |
- 🆓 **近乎零的手续费**：每笔交易手续费约为0.00025美元 |
- 🔗 **二维码支付**：生成可扫描的支付请求 |
- 🛒 **销售点集成**：支持与商家系统对接 |
- 📱 **钱包支持**：兼容Phantom、Solflare、Backpack等钱包 |

## 支付请求的URL格式

Solana Pay使用特定的URL格式来发送支付请求：

```
solana:<recipient>?amount=<amount>&spl-token=<mint>&reference=<reference>&label=<label>&message=<message>&memo=<memo>
```

## 生成SOL支付请求

```bash
RECIPIENT=$(solana address --keypair "$SOLANA_KEYPAIR_PATH")
AMOUNT="1.5"
REFERENCE=$(solana-keygen new --no-bip39-passphrase --silent --outfile /dev/stdout | head -1)
LABEL="My Store"
MESSAGE="Order #12345"

# Build Solana Pay URL
PAY_URL="solana:${RECIPIENT}?amount=${AMOUNT}&reference=${REFERENCE}&label=${LABEL}&message=${MESSAGE}"

echo "Payment URL: $PAY_URL"

# Generate QR code (requires qrencode)
echo "$PAY_URL" | qrencode -o payment_qr.png -s 10
echo "QR code saved to payment_qr.png"
```

## 生成SPL代币支付请求

```bash
RECIPIENT=$(solana address --keypair "$SOLANA_KEYPAIR_PATH")
AMOUNT="100"
SPL_TOKEN="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"  # USDC
REFERENCE=$(openssl rand -hex 32)
LABEL="My Store"
MESSAGE="Order #12345"

# Build Solana Pay URL with SPL token
PAY_URL="solana:${RECIPIENT}?amount=${AMOUNT}&spl-token=${SPL_TOKEN}&reference=${REFERENCE}&label=${LABEL}&message=${MESSAGE}"

echo "Payment URL: $PAY_URL"
echo "$PAY_URL" | qrencode -o payment_qr.png -s 10
```

## 常见代币的发行地址

| 代币 | 发行地址 |
|-------|--------------|
| USDC | EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v |
| USDT | Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB |
| BONK | DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263 |
| JUP | JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN |

## 通过参考编号验证支付

```bash
REFERENCE="<REFERENCE_PUBKEY>"
RPC_URL="${SOLANA_RPC_URL:-https://api.mainnet-beta.solana.com}"

# Find transaction with reference
curl -s -X POST "$RPC_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"jsonrpc\": \"2.0\",
    \"id\": 1,
    \"method\": \"getSignaturesForAddress\",
    \"params\": [\"${REFERENCE}\", {\"limit\": 1}]
  }" | jq '.result[0]'
```

## 验证交易

```bash
SIGNATURE="<TX_SIGNATURE>"
EXPECTED_RECIPIENT="<MERCHANT_WALLET>"
EXPECTED_AMOUNT="1000000"  # in lamports or token units

# Get transaction details
TX=$(curl -s -X POST "$RPC_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"jsonrpc\": \"2.0\",
    \"id\": 1,
    \"method\": \"getTransaction\",
    \"params\": [\"${SIGNATURE}\", {\"encoding\": \"jsonParsed\", \"maxSupportedTransactionVersion\": 0}]
  }")

# Verify recipient and amount
echo "$TX" | jq '.result.transaction.message.instructions[] | select(.parsed.type == "transfer")'
```

## 交互式支付请求（需要服务器处理的复杂交易）

```bash
# Server endpoint that returns transaction
TRANSACTION_URL="https://your-server.com/api/pay"

# Solana Pay URL pointing to transaction endpoint
PAY_URL="solana:${TRANSACTION_URL}"
```

### 交易请求服务器示例

```javascript
// POST /api/pay
// Returns serialized transaction for wallet to sign

app.post('/api/pay', async (req, res) => {
  const { account } = req.body;  // Payer's wallet
  
  // Build transaction
  const transaction = new Transaction();
  transaction.add(
    SystemProgram.transfer({
      fromPubkey: new PublicKey(account),
      toPubkey: MERCHANT_WALLET,
      lamports: LAMPORTS_PER_SOL * 0.1
    })
  );
  
  // Serialize and return
  const serialized = transaction.serialize({
    requireAllSignatures: false,
    verifySignatures: false
  });
  
  res.json({
    transaction: serialized.toString('base64'),
    message: 'Payment for Order #123'
  });
});
```

## 销售点集成

### 生成动态二维码

```bash
#!/bin/bash
# pos_payment.sh - Generate payment QR for POS

AMOUNT="$1"
ORDER_ID="$2"
TOKEN="${3:-SOL}"

RECIPIENT=$(solana address --keypair "$SOLANA_KEYPAIR_PATH")
REFERENCE=$(openssl rand -hex 32)

if [[ "$TOKEN" == "SOL" ]]; then
  PAY_URL="solana:${RECIPIENT}?amount=${AMOUNT}&reference=${REFERENCE}&memo=Order-${ORDER_ID}"
else
  # Get token mint
  case "$TOKEN" in
    USDC) MINT="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v" ;;
    USDT) MINT="Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB" ;;
  esac
  PAY_URL="solana:${RECIPIENT}?amount=${AMOUNT}&spl-token=${MINT}&reference=${REFERENCE}&memo=Order-${ORDER_ID}"
fi

# Display QR in terminal (requires qrencode)
echo "$PAY_URL" | qrencode -t ANSIUTF8

# Save reference for verification
echo "$REFERENCE" > "/tmp/order_${ORDER_ID}_ref.txt"
echo "Reference saved. Waiting for payment..."
```

### 监控支付状态

```bash
#!/bin/bash
# wait_payment.sh - Wait for payment confirmation

ORDER_ID="$1"
REFERENCE=$(cat "/tmp/order_${ORDER_ID}_ref.txt")
RPC_URL="${SOLANA_RPC_URL:-https://api.mainnet-beta.solana.com}"

echo "Waiting for payment (reference: ${REFERENCE:0:8}...)"

while true; do
  RESULT=$(curl -s -X POST "$RPC_URL" \
    -H "Content-Type: application/json" \
    -d "{
      \"jsonrpc\": \"2.0\",
      \"id\": 1,
      \"method\": \"getSignaturesForAddress\",
      \"params\": [\"${REFERENCE}\", {\"limit\": 1}]
    }")
  
  SIG=$(echo "$RESULT" | jq -r '.result[0].signature // empty')
  
  if [[ -n "$SIG" ]]; then
    echo "✅ Payment received!"
    echo "Transaction: $SIG"
    echo "Explorer: https://solscan.io/tx/$SIG"
    break
  fi
  
  sleep 2
done
```

## 手续费对比

| 网络 | 手续费 | 处理时间 |
|---------|-----|------|
| Solana Pay | 约0.00025美元 | 约400毫秒 |
| Visa/MasterCard | 2-3% | 1-3天 |
| PayPal | 2.9% + 0.30美元 | 即时 |
| 电汇 | 25-50美元 | 1-5天 |

## 安全规则

1. **务必** 在完成交易前验证交易签名。
2. **务必** 确认收款人信息与商户钱包信息一致。
3. **务必** 核对支付金额是否正确。
4. **为每笔支付请求使用** 唯一的参考编号。
5. **严禁** 重复使用参考编号。

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|----------|
| 未找到交易记录 | 支付未完成 | 继续尝试 |
| 收款人信息错误 | 支付被欺诈 | 拒绝支付并提醒用户 |
| 金额错误 | 支付金额不正确 | 请重新请求剩余金额 |
| 交易失败 | 资金不足 | 请重试支付 |

## 相关链接

- [Solana Pay官方文档](https://docs.solanapay.com/) |
- [Solana Pay GitHub仓库](https://github.com/solana-labs/solana-pay) |
- [Solscan浏览器](https://solscan.io/)