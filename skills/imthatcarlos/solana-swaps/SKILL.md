---
name: solana-swaps
description: 通过 Jupiter 聚合器在 Solana 上进行代币交换，并查看钱包余额。适用于用户需要交换代币、查询 SOL/代币余额或获取交换报价的情况。
metadata: {"clawdbot":{"emoji":"💰","requires":{"bins":["solana","spl-token","curl","jq","node"],"env":["SOLANA_KEYPAIR_PATH"]}}}
---

# Solana 货币兑换

使用 Jupiter 聚合器管理您的 Solana 钱包：查询余额并进行代币兑换。

## 环境变量

这些环境变量已预先配置，可供使用：

| 变量 | 描述 |
|----------|-------------|
| `SOLANA_KEYPAIR_PATH` | 钱包密钥对 JSON 文件的路径 |
| `JUPITER_API_KEY` | Jupiter API 密钥（用于身份验证请求，可避免平台费用，兑换 Token2022/pump.fun 代币时必需） |

**注意：** 这些变量已在技能配置中设置好。只需在命令中直接使用 `$SOLANA_KEYPAIR_PATH` 和 `$JUPITER_API_KEY` 即可。

### 验证设置

```bash
# Check wallet address
solana address --keypair "$SOLANA_KEYPAIR_PATH"

# Check Solana CLI config
solana config get
```

## 查看余额

### 查看 SOL 余额

```bash
solana balance --keypair "$SOLANA_KEYPAIR_PATH"
```

### 列出所有代币账户

```bash
spl-token accounts --owner $(solana address --keypair "$SOLANA_KEYPAIR_PATH")
```

### 查看特定代币的余额

```bash
spl-token balance <TOKEN_MINT_ADDRESS> --owner $(solana address --keypair "$SOLANA_KEYPAIR_PATH")
```

## 常见代币的铸造地址

| 代币 | 符号 | 铸造地址 | 小数位数 |
|-------|--------|-------------|----------|
| Wrapped SOL | SOL | So11111111111111111111111111111111111111112 | 9 |
| USD Coin | USDC | EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v | 6 |
| Tether | USDT | Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB | 6 |
| Bonk | BONK | DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263 | 5 |
| Jupiter | JUP | JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN | 6 |
| Raydium | RAY | 4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R | 6 |

## 通过 Jupiter 进行代币兑换

**重要提示：** 在执行任何兑换操作之前，务必显示兑换详情并等待用户的明确确认。

### 第一步：获取报价

将用户可读的金额转换为原始单位：
- SOL：乘以 1,000,000,000（10^9）
- USDC/USDT：乘以 1,000,000（10^6）
- BONK：乘以 100,000（10^5）

```bash
# Example: Get quote for swapping 1 SOL to USDC
INPUT_MINT="So11111111111111111111111111111111111111112"
OUTPUT_MINT="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
AMOUNT="1000000000"  # 1 SOL in lamports
SLIPPAGE_BPS="50"    # 0.5% slippage

# Get quote with API key authentication
curl -s -H "x-api-key: $JUPITER_API_KEY" \
  "https://api.jup.ag/swap/v1/quote?inputMint=${INPUT_MINT}&outputMint=${OUTPUT_MINT}&amount=${AMOUNT}&slippageBps=${SLIPPAGE_BPS}" | jq .
```

### 第二步：显示报价并请求确认

解析报价响应并显示给用户：
- 输入：金额和代币名称
- 输出：预期金额和代币名称
- 价格影响百分比
- 滑点容忍度
- 最低接收金额（otherAmountThreshold）

**重要提示：** 询问用户“您是否要继续进行此兑换？”并在收到明确确认（“是”、“继续”或“确认”）后才能继续。

### 第三步：构建兑换交易

用户确认后，请求执行兑换交易：

```bash
USER_PUBKEY=$(solana address --keypair "$SOLANA_KEYPAIR_PATH")

# Save quote response to file
QUOTE_FILE="/tmp/jupiter_quote.json"
curl -s -H "x-api-key: $JUPITER_API_KEY" \
  "https://api.jup.ag/swap/v1/quote?inputMint=${INPUT_MINT}&outputMint=${OUTPUT_MINT}&amount=${AMOUNT}&slippageBps=${SLIPPAGE_BPS}" > "$QUOTE_FILE"

# Request swap transaction
curl -s -X POST \
  -H "x-api-key: $JUPITER_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.jup.ag/swap/v1/swap" \
  -d "{
    \"quoteResponse\": $(cat $QUOTE_FILE),
    \"userPublicKey\": \"${USER_PUBKEY}\",
    \"dynamicComputeUnitLimit\": true,
    \"prioritizationFeeLamports\": {
      \"priorityLevelWithMaxLamports\": {
        \"maxLamports\": 5000000,
        \"priorityLevel\": \"high\"
      }
    }
  }" > /tmp/jupiter_swap.json

# Extract the swap transaction
SWAP_TX=$(cat /tmp/jupiter_swap.json | jq -r '.swapTransaction')
```

### 第四步：签名并提交交易

使用 jupiter-swap.mjs 脚本进行签名和提交：

```bash
node "$(dirname "$0")/scripts/jupiter-swap.mjs" \
  --keypair "$SOLANA_KEYPAIR_PATH" \
  --transaction "$SWAP_TX"
```

脚本将输出交易签名和 Solscan 链接。

## 安全规则

1. **务必** 在执行任何兑换操作之前显示兑换详情并等待用户确认。
2. **绝不要** 在未经明确批准的情况下自动执行兑换。
3. **务必** 在尝试兑换前检查余额，确保有足够的资金。
4. **如果价格影响超过 1%，** 警告用户。
5. **如果滑点设置超过 1%（100 bps），** 警告用户。
6. **绝不要** 记录、显示或传输私钥内容。

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| “余额不足” | 输入的代币数量不足 | 检查余额，减少兑换金额 |
| “滑点容忍度超出” | 兑换过程中价格变动 | 获取新的报价，考虑更高的滑点 |
| “交易已过期” | 区块哈希过旧 | 获取新的报价并立即重试 |
| “账户未找到” | 代币账户不存在 | 会自动创建代币账户 |
| “路线未找到” | 该代币对没有流动性 | 尝试较小的金额或其他代币 |
| “平台不支持该费用” | Token2022 代币需要支付平台费用 | 使用带有 `$JUPITER_API_KEY` 标头的身份验证 API |

### 重试逻辑

如果由于网络问题导致兑换失败：
1. 等待 2-3 秒。
2. 获取新的报价（价格可能已发生变化）。
3. 向用户展示新的报价并重新确认。
4. 重试兑换。

## 示例交互

### 查看余额
用户：我的 SOL 余额是多少？
1. 运行：`solana balance --keypair "$SOLANA_KEYPAIR_PATH"`
2. 回报：您的钱包中有 X.XXX SOL。

### 兑换代币
用户：将 0.5 SOL 兑换为 USDC
1. 获取钱包地址。
2. 获取 0.5 SOL（500000000 lamports）兑换为 USDC 的 Jupiter 报价。
3. 显示报价详情：
   - 出发代币：0.5 SOL
   - 目标代币：约 XX.XX USDC（估计）
   - 价格影响：X.XX%
   - 最低接收金额：XX.XX USDC
4. 询问：您是否要继续进行此兑换？
5. 等待用户确认。
6. 用户确认后：执行兑换并显示交易链接。
7. 用户拒绝后：确认取消。

### 列出所有代币
用户：显示我所有的代币
1. 运行：`spl-token accounts --owner $(solana address --keypair "$SOLANA_KEYPAIR_PATH")`
2. 格式化并显示带有余额的代币列表。