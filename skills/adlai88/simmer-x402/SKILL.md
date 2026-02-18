---
name: simmer-x402
displayName: x402 Payments
description: 需要进行 x402 类型的支付才能访问付费 API 和受限内容。当某个技能需要从受 x402 保护的端点（例如 Kaito 的 Mindshare API、Simmer 的高级端点，或任何使用 x402 协议的提供商）获取数据时，应使用此功能。该功能会自动使用 USDC 在 Base 平台上处理“402 Payment Required”（需要支付）的响应。
metadata: {"clawdbot":{"emoji":"💳","requires":{"env":["EVM_PRIVATE_KEY"]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
version: "1.0.0"
published: true
---
# x402支付

使用USDC在Base网络上为需要x402权限控制的API进行支付。该技能使代理能够在访问付费Web资源时自动进行加密货币支付。

## 何时使用此技能

在以下情况下使用此技能：
- 需要从需要x402权限控制的API（例如Kaito的mindshare API）获取数据
- 遇到HTTP 402 “Payment Required”（需要支付）的响应
- 需要查看Base钱包中的余额（USDC + ETH）
- 需要支付超出免费 tier 限制的Simmer高级端点费用

## 设置

1. **设置钱包私钥**
   ```bash
   export EVM_PRIVATE_KEY=0x...your_private_key...
   ```
   如果未设置`EVM_PRIVATE_KEY`，则使用`WALLET_PRIVATE_KEY`（Simmer/Polymarket用户使用的私钥相同）。您的EVM地址适用于所有链：Polygon用于交易，Base用于x402支付。

2. **在Base网络上用USDC充值**
   - 将USDC发送到您的Base网络钱包地址
   - Base上的x402支付完全不需要Gas费用，只需USDC即可

3. **安装依赖项**
   ```bash
   pip install x402[httpx,evm]
   ```

## 快速命令

| 命令 | 描述 |
|---------|-------------|
| `python x402_cli.py balance` | 查看Base钱包中的USDC和ETH余额 |
| `python x402_cli.py fetch <url>` | 自动支付费用后获取指定URL的数据 |
| `python x402_cli.py fetch <url> --json` | 同上，但仅输出原始JSON格式 |
| `python x402_cli.py fetch <url> --dry-run` | 显示支付信息（不实际支付） |
| `python x402_cli.py fetch <url> --max 5.00` | 修改最大支付限额 |
| `python x402_cli.py rpc <network> <method> [params...]` | 通过Quicknode x402进行RPC调用 |

## 示例

### 查看余额
```bash
python x402_cli.py balance
```
```
x402 Wallet Balance
==============================
Address: 0x1234...5678
Network: Base Mainnet

USDC:  $42.50
ETH:   0.000000 ETH
```

### 获取免费端点的数据（无需支付）
```bash
python x402_cli.py fetch "https://api.kaito.ai/api/v1/tokens" --json
```

### 获取Kaito mindshare数据（每个数据点0.02美元）
```bash
python x402_cli.py fetch "https://api.kaito.ai/api/payg/mindshare?token=BTC&start_date=2026-02-13&end_date=2026-02-14" --json
```

### 获取Kaito情感数据（每个数据点0.02美元）
```bash
python x402_cli.py fetch "https://api.kaito.ai/api/payg/sentiment?token=BTC&start_date=2026-02-13&end_date=2026-02-14" --json
```

### 使用AlphaKek知识引擎（每个请求0.01美元）
```bash
python x402_cli.py fetch "https://api.alphakek.ai/x402/knowledge/ask" \
  --method POST --body '{"question": "What is the current sentiment on BTC?", "search_mode": "fast"}' --json
```

### 获取CoinGecko价格数据（每个请求0.01美元）
```bash
python x402_cli.py fetch "https://pro-api.coingecko.com/api/v3/x402/simple/price?ids=bitcoin&vs_currencies=usd" --json
```

### 获取Simmer高级端点的数据
```bash
python x402_cli.py fetch "https://x402.simmer.markets/api/sdk/context/market-123" \
  --header "Authorization: Bearer sk_live_..." --json
```

### 使用Quicknode进行RPC调用（无需API密钥）
```bash
# Get ETH balance on Ethereum mainnet
python x402_cli.py rpc ethereum-mainnet eth_getBalance 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 latest

# Get latest block on Polygon
python x402_cli.py rpc polygon-mainnet eth_blockNumber

# Get token balance on Base
python x402_cli.py rpc base-mainnet eth_call '{"to":"0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913","data":"0x70a08231000000000000000000000000YOUR_ADDRESS"}' latest
```
Quicknode x402支持55个以上的区块链网络（Ethereum、Polygon、Base、Arbitrum、Solana、Bitcoin等）。10美元可购买100万次RPC调用次数——每次成功调用消耗1次信用额度。

## 支持的x402提供者

| 提供者 | 端点 | 价格 | 描述 |
|----------|----------|-------|-------------|
| Kaito | `/api/payg/mindshare` | 每个数据点0.02美元 | Token mindshare时间序列数据 |
| Kaito | `/api/payg/sentiment` | 每个数据点0.02美元 | Token情感时间序列数据 |
| Kaito | `/api/payg/narrative_mindshare` | 每个数据点0.02美元 | 叙事性mindshare时间序列数据 |
| Kaito | `/api/payg/smart_followers` | 每次请求0.20美元 | 智能粉丝指标 |
| AlphaKek | `/x402/knowledge/ask` | 每次请求0.01美元 | AI知识引擎（搜索模式：fast/deep/ultrafast） |
| CoinGecko | `/api/v3/x402/simple/price` | 每次请求0.01美元 | Token价格数据 |
| Simmer | `/api/sdk/context/:id` | 每次请求0.005美元 | 市场上下文数据（绕过速率限制） |
| Simmer | `/api/sdk/briefing` | 每次请求0.005美元 | 投资组合简报（绕过速率限制） |
| Quicknode | `/:network`（55个以上网络） | 每次请求10美元/100万次信用额度 | 无需API密钥的RPC访问 |

Kaito API文档：https://github.com/MetaSearch-IO/KaitoX402APIDocs
Quicknode x402文档：https://x402.quicknode.com/llms.txt

## 配置

| 设置 | 环境变量 | 默认值 | 描述 |
|---------|---------------------|---------|-------------|
| 钱包密钥 | `EVM_PRIVATE_KEY` | （必填） | 十六进制编码的私钥（未设置时使用`WALLET_PRIVATE_KEY`） |
| 最大支付金额 | `X402_MAX_PAYMENT_USD` | 10.00美元 | 每次请求的最大支付限额 |
| 网络 | `X402_NETWORK` | mainnet | `mainnet`或`testnet` |

或者通过技能目录中的`config.json`文件进行配置：
```json
{
  "max_payment_usd": 10.00,
  "network": "mainnet"
}
```

## 工作原理

1. 该技能向目标URL发送HTTP请求
2. 如果服务器返回200状态码——表示操作成功，无需支付
3. 如果服务器返回402 “Payment Required”状态码——x402 SDK会读取支付要求
4. SDK在Base网络上生成USDC转账授权（无需Gas费用）
5. SDK使用授权信息重新发送请求
6. 服务器验证支付信息后返回受限内容

所有支付处理均通过官方Coinbase x402 Python SDK自动完成。

## 对于其他技能

其他技能可以直接导入x402功能：

```python
from skills.x402.x402_cli import x402_fetch

# Returns parsed JSON response
data = await x402_fetch("https://api.kaito.ai/api/payg/mindshare?token=BTC")
```

## 安全性

- 使用官方Coinbase `x402` Python SDK进行支付签名
- 私钥永远不会离开您的设备
- 最大支付限额防止意外超支
- 提供Dry-run模式以在执行前预览支付信息

**私钥安全提示：**
- 将私钥存储在`.env`文件中，切勿在shell历史记录中直接传递
- 确保`.env`文件被包含在`.gitignore`文件中——切勿将私钥提交到Git仓库
- 使用专用热钱包存储私钥，并限制其资金量，避免使用主钱包
- 如果怀疑私钥被泄露，请立即更换私钥

## 故障排除

**“EVM_PRIVATE_KEY未设置”**
- 设置钱包私钥：`export EVM_PRIVATE_KEY=0x...`

**“USDC余额不足”**
- 在Base网络上为钱包充值USDC
- 运行`python x402_cli.py balance`检查余额

**“支付金额超过限额”**
- 增加限额：`--max 50` 或设置`X402_MAX_PAYMENT_USD=50`

**“支付选项中未支持的网络”**
- 确保您的钱包中包含Base网络的USDC。虽然某些提供者可能支持其他网络，但此技能仅使用Base网络。