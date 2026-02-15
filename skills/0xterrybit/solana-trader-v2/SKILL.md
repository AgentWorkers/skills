---
name: solana-trader
description: 通过Jupiter聚合器管理Solana钱包并进行代币交易。您可以查看余额、交易历史、兑换代币以及管理您的Solana投资组合。
metadata: {"clawdbot":{"emoji":"🚀","requires":{"bins":["solana","spl-token","curl","jq"],"env":["SOLANA_KEYPAIR_PATH"]}}}
---

# Solana Trader 🚀

这是一个专为Clawdbot设计的全面Solana钱包管理和交易工具，支持管理您的Solana投资组合、查看余额、交易历史以及通过Jupiter DEX聚合器进行代币兑换。

## 环境变量

| 变量 | 描述 | 是否必需 |
|----------|-------------|----------|
| `SOLANA_KEYPAIR_PATH` | 钱包密钥对JSON文件的路径 | 是 |
| `SOLANA_RPC_URL` | 自定义RPC端点（默认：mainnet-beta） | 否 |
| `JUPITER_API_KEY` | 用于身份验证请求的Jupiter API密钥 | 否 |
| `HELIUS_API_KEY` | 用于获取更详细交易数据的Helius API密钥 | 否 |
| `SHYFT_API_KEY` | 用于查看交易历史的Shyft API密钥 | 否 |
| `QUICKNODE_RPC_URL` | QuickNode RPC端点 | 否 |
| `ALCHEMY_RPC_URL` | Alchemy Solana RPC端点 | 否 |

## 免费的公共RPC端点（无需API密钥）

| 提供商 | 端点 | 备注 |
|----------|----------|-------|
| Solana基金会 | `https://api.mainnet-beta.solana.com` | 官方端点，但有限制 |
| PublicNode | `https://solana-rpc.publicnode.com` | 以隐私为优先，响应速度快 |
| Ankr | `https://rpc.ankr.com/solana` | 免费公共端点 |
| Project Serum | `https://solana-api.projectserum.com` | 由社区维护 |

> ⚠️ **注意**: 公共端点通常每10秒限制100次请求。对于生产环境或高频交易，请使用付费的RPC服务。

### RPC选择策略

**默认行为（未配置API密钥时）：**
1. 如果设置了`SOLANA_RPC_URL`，则使用该端点。
2. 依次使用免费的公共端点：
   - `https://api.mainnet-beta.solana.com`
   - `https://solana-rpc.publicnode.com`
   - `https://rpc.ankr.com/solana`

**何时升级到付费RPC服务：**
- 遇到请求限制错误（429 Too Many Requests）
- 需要进行高频交易或使用MEV策略
- 需要更详细的交易数据（如使用Helius API）
- 生产级应用要求99.9%的可用性
- 需要实时更新（通过WebSocket订阅）

**如果遇到请求限制**：询问用户：“您是否希望配置付费的RPC服务？可选服务包括：Helius、QuickNode、Alchemy、Shyft。”

## 💎 推荐费配置

该工具在每次代币兑换时收取0.2%的平台费用，以支持开发工作。费用会在每次交易前透明地向用户显示。

| 变量 | 值 | 描述 |
|----------|-------|-------------|
| `PLATFORM_FEE_BPS` | 20 | 0.2%的平台费用（20个基点） |
| `FEE_ACCOUNT` | `8KDDpruBwpTzJLKEcfv8JefKSVYWYE53FV3B2iLD6bNN` | 收费将转入此Solana钱包 |

**费用分配：**
- 用户支付：代币兑换金额的0.2%
- 开发者获得：费用的97.5%（0.195%）
- Jupiter获得：费用的2.5%（0.005%）

**示例**：在100 USDC的代币兑换中：
- 总费用：0.20 USDC
- 用户获得：约0.195 USDC
- Jupiter获得：约0.005 USDC

## 设置验证

```bash
# Check wallet address
solana address --keypair "$SOLANA_KEYPAIR_PATH"

# Check Solana CLI config
solana config get

# Test RPC connection
solana cluster-version
```

### 导入私钥

如果您只有私钥（base58字符串或字节数组），请将其转换为密钥对JSON格式：

**从Base58私钥导入：**
```bash
# Install solana-keygen if needed
# Your private key looks like: 5K1gR...xyz (base58 string)

echo "Enter your base58 private key:"
read -s PRIVATE_KEY

# Convert to keypair JSON (requires Node.js)
node -e "
const bs58 = require('bs58');
const key = bs58.decode('$PRIVATE_KEY');
console.log(JSON.stringify(Array.from(key)));
" > ~/.config/solana/imported-wallet.json

export SOLANA_KEYPAIR_PATH=~/.config/solana/imported-wallet.json
```

**从字节数组导入（例如Phantom导出的私钥）：**
```bash
# If you have a byte array like [12,34,56,...]
echo '[12,34,56,78,...]' > ~/.config/solana/imported-wallet.json
export SOLANA_KEYPAIR_PATH=~/.config/solana/imported-wallet.json
```

**从助记词导入：**
```bash
# Use solana-keygen to recover
solana-keygen recover -o ~/.config/solana/recovered-wallet.json
# Enter your 12/24 word seed phrase when prompted

export SOLANA_KEYPAIR_PATH=~/.config/solana/recovered-wallet.json
```

> ⚠️ **安全提示**：切勿分享您的私钥或助记词。请使用受限权限存储密钥对文件：`chmod 600 ~/.config/solana/*.json`

---

## 💰 账户管理命令

### 查看SOL余额
```bash
solana balance --keypair "$SOLANA_KEYPAIR_PATH"
```

### 列出所有代币账户
```bash
spl-token accounts --owner $(solana address --keypair "$SOLANA_KEYPAIR_PATH")
```

### 查看特定代币的余额
```bash
# Replace <MINT_ADDRESS> with token mint
spl-token balance <MINT_ADDRESS> --owner $(solana address --keypair "$SOLANA_KEYPAIR_PATH")
```

### 获取投资组合概览
```bash
# Get wallet address
WALLET=$(solana address --keypair "$SOLANA_KEYPAIR_PATH")

# Get SOL balance
SOL_BALANCE=$(solana balance --keypair "$SOLANA_KEYPAIR_PATH" | awk '{print $1}')

# Get all token accounts
spl-token accounts --owner $WALLET
```

---

## 📜 交易历史

### 查看最近的交易记录

支持多种RPC服务。默认使用Solana的原生RPC服务（无需API密钥）。

**选项1：Solana RPC（默认，无需API密钥）**
```bash
WALLET=$(solana address --keypair "$SOLANA_KEYPAIR_PATH")
RPC_URL="${SOLANA_RPC_URL:-https://api.mainnet-beta.solana.com}"

curl -s -X POST "$RPC_URL" \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"getSignaturesForAddress\",\"params\":[\"$WALLET\",{\"limit\":10}]}" | jq '.result[] | {signature: .signature, slot: .slot, blockTime: .blockTime}'
```

**选项2：Helius（提供更详细的数据，推荐用于查看详细交易记录）**
```bash
WALLET=$(solana address --keypair "$SOLANA_KEYPAIR_PATH")

curl -s "https://api.helius.xyz/v0/addresses/${WALLET}/transactions?api-key=${HELIUS_API_KEY:-demo}&limit=10" | jq '.[] | {signature: .signature, type: .type, timestamp: .timestamp, fee: .fee}'
```

**选项3：Shyft（提供免费服务）**
```bash
WALLET=$(solana address --keypair "$SOLANA_KEYPAIR_PATH")

curl -s "https://api.shyft.to/sol/v1/transaction/history?network=mainnet-beta&account=${WALLET}&tx_num=10" \
  -H "x-api-key: ${SHYFT_API_KEY}" | jq '.result.transactions'
```

**选项4：QuickNode**
```bash
WALLET=$(solana address --keypair "$SOLANA_KEYPAIR_PATH")

curl -s -X POST "$QUICKNODE_RPC_URL" \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"getSignaturesForAddress\",\"params\":[\"$WALLET\",{\"limit\":10}]}" | jq '.result'
```

**选项5：Alchemy**
```bash
WALLET=$(solana address --keypair "$SOLANA_KEYPAIR_PATH")

curl -s -X POST "$ALCHEMY_RPC_URL" \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"getSignaturesForAddress\",\"params\":[\"$WALLET\",{\"limit\":10}]}" | jq '.result[] | {signature: .signature, slot: .slot, blockTime: .blockTime}'
```

> 💡 **服务选择**：系统会自动检测可用的API密钥，并选择最佳的服务。如果未配置密钥，则使用Solana的原生RPC服务。

### 查看交易详情
```bash
# Replace <SIGNATURE> with transaction signature
solana confirm -v <SIGNATURE>

# Or via RPC for more details
RPC_URL="${SOLANA_RPC_URL:-https://api.mainnet-beta.solana.com}"
curl -s -X POST "$RPC_URL" \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"getTransaction\",\"params\":[\"<SIGNATURE>\",{\"encoding\":\"jsonParsed\",\"maxSupportedTransactionVersion\":0}]}" | jq '.result'
```

---

## 🪙 常见代币地址

| 代币 | 符号 | 发行地址 | 小数位数 |
|-------|--------|--------------|----------|
| Wrapped SOL | SOL | So11111111111111111111111111111111111111112 | 9 |
| USD Coin | USDC | EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v | 6 |
| Tether | USDT | Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB | 6 |
| Bonk | BONK | DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263 | 5 |
| Jupiter | JUP | JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN | 6 |
| Raydium | RAY | 4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R | 6 |
| Pyth | PYTH | HZ1JovNiVvGrGNiiYvEozEVgZ58xaU3RKwX8eACQBCt3 | 6 |
| Jito | JTO | jtojtomepa8beP8AuQc6eXt5FriJwfFMwQx2v2f9mCL | 9 |

---

## 🔄 通过Jupiter进行代币兑换

**⚠️ 重要提示：**在执行任何代币兑换前，务必显示兑换详情并等待用户的明确确认。**

### 步骤1：获取兑换报价

- 将用户输入的金额转换为实际数量：
  - SOL：乘以1,000,000,000（10^9）
  - USDC/USDT/JUP：乘以1,000,000（10^6）
  - BONK：乘以100,000（10^5）

```bash
# Example: Quote for swapping 1 SOL to USDC
INPUT_MINT="So11111111111111111111111111111111111111112"
OUTPUT_MINT="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
AMOUNT="1000000000"  # 1 SOL in lamports
SLIPPAGE_BPS="50"    # 0.5% slippage
PLATFORM_FEE_BPS="20"  # 0.2% platform fee

# Get quote with platform fee
QUOTE=$(curl -s "https://api.jup.ag/swap/v1/quote?inputMint=${INPUT_MINT}&outputMint=${OUTPUT_MINT}&amount=${AMOUNT}&slippageBps=${SLIPPAGE_BPS}&platformFeeBps=${PLATFORM_FEE_BPS}")

echo "$QUOTE" | jq '{
  inputAmount: .inAmount,
  outputAmount: .outAmount,
  priceImpact: .priceImpactPct,
  minimumReceived: .otherAmountThreshold,
  platformFee: .platformFee
}'
```

### 步骤2：显示报价并请求用户确认

- 显示给用户的信息包括：
  - 输入的金额和代币名称
  - 预计的兑换数量和代币名称
  - 价格变动百分比
  - 承受的滑点范围
  - 最小接收数量
  - **平台费用：0.2%（用于支持工具开发）**

**重要提示**：在继续之前，请询问用户“您是否确认进行此兑换？”并等待用户的明确回复（“是”、“继续”或“确认”）。

**显示示例：**
```
📊 Swap Preview:
├─ From: 1.0 SOL
├─ To: ~150.25 USDC (estimated)
├─ Price Impact: 0.01%
├─ Slippage: 0.5%
├─ Minimum Received: 149.50 USDC
├─ Platform Fee: 0.2% (~0.30 USDC)
└─ Network Fee: ~0.000005 SOL

⚠️ Confirm swap? (yes/no)
```

### 步骤3：创建兑换交易

用户确认后，执行兑换操作：
```bash
USER_PUBKEY=$(solana address --keypair "$SOLANA_KEYPAIR_PATH")

# Fee account for referral rewards
FEE_ACCOUNT="8KDDpruBwpTzJLKEcfv8JefKSVYWYE53FV3B2iLD6bNN"

# Save quote to file
echo "$QUOTE" > /tmp/jupiter_quote.json

# Request swap transaction with fee account
SWAP_RESPONSE=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  "https://api.jup.ag/swap/v1/swap" \
  -d "{
    \"quoteResponse\": $(cat /tmp/jupiter_quote.json),
    \"userPublicKey\": \"${USER_PUBKEY}\",
    \"feeAccount\": \"${FEE_ACCOUNT}\",
    \"dynamicComputeUnitLimit\": true,
    \"prioritizationFeeLamports\": {
      \"priorityLevelWithMaxLamports\": {
        \"maxLamports\": 5000000,
        \"priorityLevel\": \"high\"
      }
    }
  }")

# Extract transaction
SWAP_TX=$(echo "$SWAP_RESPONSE" | jq -r '.swapTransaction')
```

> 💡 **注意**：`feeAccount`账户将收到平台费用。请确保您拥有用于接收费用的USDC、USDT等常见代币的账户。

### 步骤4：签名并提交交易
```bash
# Decode base64 transaction
echo "$SWAP_TX" | base64 -d > /tmp/swap_tx.bin

# Sign with keypair (requires solana-cli)
solana transfer --from "$SOLANA_KEYPAIR_PATH" \
  --blockhash $(solana block-height) \
  --sign-only \
  /tmp/swap_tx.bin

# Or use the raw transaction submission
curl -s -X POST "https://api.mainnet-beta.solana.com" \
  -H "Content-Type: application/json" \
  -d "{
    \"jsonrpc\": \"2.0\",
    \"id\": 1,
    \"method\": \"sendTransaction\",
    \"params\": [\"${SWAP_TX}\", {\"encoding\": \"base64\"}]
  }"
```

---

## 💸 发送代币

### 发送SOL代币
```bash
# ALWAYS confirm with user before sending!
RECIPIENT="<RECIPIENT_ADDRESS>"
AMOUNT="0.1"  # SOL amount

# Display and confirm
echo "Sending ${AMOUNT} SOL to ${RECIPIENT}"
echo "Confirm? (yes/no)"

# After confirmation:
solana transfer --keypair "$SOLANA_KEYPAIR_PATH" "$RECIPIENT" "$AMOUNT"
```

### 发送SPL代币
```bash
# ALWAYS confirm with user before sending!
RECIPIENT="<RECIPIENT_ADDRESS>"
TOKEN_MINT="<TOKEN_MINT_ADDRESS>"
AMOUNT="100"  # Token amount

# Display and confirm
echo "Sending ${AMOUNT} tokens (${TOKEN_MINT}) to ${RECIPIENT}"
echo "Confirm? (yes/no)"

# After confirmation:
spl-token transfer --keypair "$SOLANA_KEYPAIR_PATH" "$TOKEN_MINT" "$AMOUNT" "$RECIPIENT"
```

---

## 📊 查询代币价格

### 从Jupiter获取代币价格
```bash
# Get SOL price in USDC
curl -s "https://api.jup.ag/price/v2?ids=So11111111111111111111111111111111111111112" | jq '.data.So11111111111111111111111111111111111111112.price'

# Get multiple token prices
curl -s "https://api.jup.ag/price/v2?ids=So11111111111111111111111111111111111111112,JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN" | jq '.data'
```

### 获取代币信息
```bash
# Search token by symbol or name
curl -s "https://tokens.jup.ag/token/<MINT_ADDRESS>" | jq '{name: .name, symbol: .symbol, decimals: .decimals}'
```

---

## 🛡️ 安全规则

1. **务必**在执行任何交易前显示交易详情并等待用户确认。
2. **绝不要**在未经用户明确同意的情况下自动执行交易或转账。
3. **在尝试交易前**务必检查余额。
4. **如果价格变动超过1%，请警告用户**。
5. **如果滑点超过1%（100个基点），请警告用户**。
6. **绝不要**记录、显示或传输私钥内容。
7. **在执行交易后**务必显示交易签名和交易详情链接。

---

## ⚠️ 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|----------|
| “余额不足” | 代币数量不足 | 检查余额并减少交易金额 |
| “滑点超出范围” | 交易过程中价格发生变动 | 重新获取报价并调整滑点范围 |
| “交易已过期” | 区块哈希过期 | 重新获取报价并重试交易 |
| “账户未找到” | 未找到相应的代币账户 | 系统会自动创建账户 |
| “找不到交易路线” | 无流动性 | 尝试减少交易金额或选择其他代币对 |

### 重试逻辑

如果交易失败：
1. 等待2-3秒。
2. 重新获取报价（价格可能已经变化）。
3. 向用户展示新的报价并重新确认交易。
4. 重试交易。

---

## 📝 示例交互流程

### 查看余额
```
User: "What's my SOL balance?"
→ Run: solana balance --keypair "$SOLANA_KEYPAIR_PATH"
→ Report: "Your wallet has X.XXX SOL"
```

### 进行代币兑换
```
User: "Swap 0.5 SOL for USDC"
→ Get Jupiter quote for 0.5 SOL → USDC (with platformFeeBps=20)
→ Display:
   "📊 Swap Preview:
    ├─ From: 0.5 SOL
    ├─ To: ~75.50 USDC (estimated)
    ├─ Price Impact: 0.01%
    ├─ Minimum Received: 75.12 USDC
    ├─ Platform Fee: 0.2% (~0.15 USDC)
    └─ Network Fee: ~0.000005 SOL
    
    Confirm swap? (yes/no)"
→ Wait for "yes"
→ Execute swap with feeAccount
→ Report: "✅ Swap successful! TX: https://solscan.io/tx/..."
```

### 发送代币
```
User: "Send 10 USDC to ABC123..."
→ Display:
   "Transfer Preview:
    - Amount: 10 USDC
    - To: ABC123...
    - Network Fee: ~0.000005 SOL
    
    Confirm transfer? (yes/no)"
→ Wait for "yes"
→ Execute transfer
→ Report: "✅ Transfer successful! TX: https://solscan.io/tx/..."
```

---

## 🔗 有用链接

- [Solscan浏览器](https://solscan.io/)
- [Jupiter聚合器](https://jup.ag/)
- [Solana官方文档](https://docs.solana.com/)
- [SPL代币文档](https://spl.solana.com/token)