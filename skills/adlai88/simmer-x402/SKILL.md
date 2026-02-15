---
name: simmer-x402
displayName: x402 Payments
description: 需要进行 x402 类型的支付才能访问付费 API 和受限制的内容。当某个技能需要从受 x402 限制的端点（例如 Kaito Mindshare API、Simmer Premium 端点或任何 x402 提供商的端点）获取数据时，应使用此功能。该功能会自动使用 USDC 在 Base 平台上处理“402 Payment Required”（需要支付）的响应。
metadata: {"clawdbot":{"emoji":"💳","requires":{"env":["EVM_PRIVATE_KEY"]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
version: "1.0.0"
published: true
---

# x402支付

使用USDC在Base网络上为x402保护的API进行支付。此技能使代理能够在访问需要付费的Web资源时自动进行加密货币支付。

## 何时使用此技能

在以下情况下使用此技能：
- 某个技能或代理需要从x402保护的API获取数据（例如：Kaito的mindshare数据）
- 遇到HTTP 402 “Payment Required”（需要支付）的响应
- 需要查看您的Base钱包余额（USDC + ETH）
- 希望支付超出免费 tier 限制的Simmer高级端点

## 设置

1. **设置您的钱包私钥**
   ```bash
   export EVM_PRIVATE_KEY=0x...your_private_key...
   ```
   如果未设置`EVM_PRIVATE_KEY`，则使用`WALLET_PRIVATE_KEY`（Simmer/Polymarket用户使用的私钥相同）。您的EVM地址适用于所有链——Polygon用于交易，Base用于x402支付。

2. **在Base网络上用USDC充值**
   - 将USDC发送到您的Base网络钱包地址
   - Base上的x402支付是完全无需gas的费用的——您只需要USDC，不需要ETH

3. **安装依赖项**
   ```bash
   pip install x402[httpx,evm]
   ```

## 快速命令

| 命令 | 描述 |
|---------|-------------|
| `python x402_cli.py balance` | 查看Base上的USDC和ETH余额 |
| `python x402_cli.py fetch <url>` | 自动支付费用后获取URL数据 |
| `python x402_cli.py fetch <url> --json` | 同上，但仅输出原始JSON格式 |
| `python x402_cli.py fetch <url> --dry-run` | 显示支付信息（不进行实际支付） |
| `python x402_cli.py fetch <url> --max 5.00` | 修改最大支付限额 |

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

### 获取免费端点数据（无需支付）
```bash
python x402_cli.py fetch "https://api.kaito.ai/api/v1/tokens" --json
```

### 获取Kaito的mindshare数据（每个数据点0.02美元）
```bash
python x402_cli.py fetch "https://api.kaito.ai/api/payg/mindshare?token=BTC&start_date=2026-02-13&end_date=2026-02-14" --json
```

### 获取Kaito的情绪数据（每个数据点0.02美元）
```bash
python x402_cli.py fetch "https://api.kaito.ai/api/payg/sentiment?token=BTC&start_date=2026-02-13&end_date=2026-02-14" --json
```

### 使用AlphaKek知识引擎（每个请求0.01美元）
```bash
python x402_cli.py fetch "https://api.alphakek.ai/x402/knowledge/ask" \
  --method POST --body '{"question": "What is the current sentiment on BTC?", "search_mode": "fast"}' --json
```

### 获取CoinGecko的价格数据（每个请求0.01美元）
```bash
python x402_cli.py fetch "https://pro-api.coingecko.com/api/v3/x402/simple/price?ids=bitcoin&vs_currencies=usd" --json
```

### 获取Simmer高级端点数据
```bash
python x402_cli.py fetch "https://x402.simmer.markets/api/sdk/context/market-123" \
  --header "Authorization: Bearer sk_live_..." --json
```

## 支持的x402提供商

| 提供商 | 端点 | 价格 | 描述 |
|----------|----------|-------|-------------|
| Kaito | `/api/payg/mindshare` | 每个数据点0.02美元 | Token mindshare时间序列数据 |
| Kaito | `/api/payg/sentiment` | 每个数据点0.02美元 | Token情绪时间序列数据 |
| Kaito | `/api/payg/narrative_mindshare` | 每个数据点0.02美元 | 叙事性mindshare时间序列数据 |
| Kaito | `/api/payg/smart_followers` | 每次请求0.20美元 | 智能粉丝指标 |
| AlphaKek | `/x402/knowledge/ask` | 每次请求0.01美元 | AI知识引擎（搜索模式：fast/deep/ultrafast） |
| CoinGecko | `/api/v3/x402/simple/price` | 每次请求0.01美元 | Token价格数据 |
| Simmer | `/api/sdk/context/:id` | 每次请求0.005美元 | 市场上下文数据（绕过费用限制） |
| Simmer | `/api/sdk/briefing` | 每次请求0.005美元 | 投资组合简报（绕过费用限制） |

Kaito API文档：https://github.com/MetaSearch-IO/KaitoX402APIDocs

## 配置

| 设置 | 环境变量 | 默认值 | 描述 |
|---------|---------------------|---------|-------------|
| 钱包密钥 | `EVM_PRIVATE_KEY` | （必需） | 十六进制编码的私钥（未设置时使用`WALLET_PRIVATE_KEY`） |
| 最大支付金额 | `X402_MAX_payment_USD` | 10.00美元 | 每次请求的最大支付限额 |
| 网络 | `X402_NETWORK` | mainnet | `mainnet`或`testnet` |

也可以通过技能目录中的`config.json`文件进行设置：
```json
{
  "max_payment_usd": 10.00,
  "network": "mainnet"
}
```

## 工作原理

1. 该技能向目标URL发送HTTP请求
2. 如果服务器返回200状态码——表示操作完成，无需支付
3. 如果服务器返回402 “Payment Required”状态码——x402 SDK会读取支付要求
4. SDK在Base网络上签署USDC转账授权（无需gas）
5. SDK带着支付签名重新发送请求
6. 服务器验证支付后返回受保护的内容

所有支付处理均通过官方Coinbase x402 Python SDK自动完成。

## 对于其他技能

其他技能可以直接导入x402功能：

```python
from skills.x402.x402_cli import x402_fetch

# Returns parsed JSON response
data = await x402_fetch("https://api.kaito.ai/api/payg/mindshare?token=BTC")
```

## 安全性

- 使用官方Coinbase的`x402` Python SDK进行支付签名
- 私钥不会离开您的设备
- 最大支付限额防止意外超支
- 提供dry-run模式以便在执行前预览支付

## 故障排除

**“EVM_PRIVATE_KEY未设置”**
- 设置您的钱包私钥：`export EVM_PRIVATE_KEY=0x...`

**“USDC余额不足”**
- 在Base网络上为钱包充值USDC
- 运行`python x402_cli.py balance`检查余额

**“支付金额超过限额”**
- 增加限额：`--max 50` 或设置`X402_MAX_payment_USD=50`

**“支付选项中不支持的网络”**
- 确保您的钱包中有USDC。虽然某些提供商可能支持其他链，但此技能仅支持Base网络。