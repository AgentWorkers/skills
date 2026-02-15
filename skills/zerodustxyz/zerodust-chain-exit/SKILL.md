---
name: zerodust-chain-exit
description: 从支持 EIP-7702 协议的链上清除所有原生气体（native gas）代币，确保这些链上的余额降为零。目前支持 25 个主网（mainnet）链。
user-invocable: true
metadata: {"openclaw": {"always": false, "emoji": "🧹", "requires": {"env": ["ZERODUST_API_KEY"]}}}
---

# ZeroDust：链退出功能

ZeroDust支持通过EIP-7702协议，将原生气体代币的数量精确地清零。该功能仅适用于支持EIP-7702的区块链（并非所有EVM区块链都支持此协议）。

## 适用场景

当用户需要执行以下操作时，可使用此功能：
- 完全退出某个区块链（将所有原生代币转移出去）
- 清除钱包中的小额余额
- 将所有代币转移至新链，确保转移后余额为零
- 彻底清空钱包
- 将资金从多个区块链合并到一个链上

## 常用指令

- “完全退出此链”
- “将我所有的代币转移到[目标链]”
- “清除钱包中的小额余额”
- “将所有代币转移到[目标链]”
- “确保余额为零”

## 支持的区块链（共25个支持EIP-7702的链）

| 链名 | ID | 原生代币 |
|-------|-----|--------------|
| Ethereum | 1 | ETH |
| BSC | 56 | BNB |
| Base | 8453 | ETH |
| Arbitrum | 42161 | ETH |
| Optimism | 10 | ETH |
| Polygon | 137 | POL |
| Gnosis | 100 | XDAI |
| Scroll | 534352 | ETH |
| Zora | 7777777 | ETH |
| Mode | 34443 | ETH |
| Mantle | 5000 | MNT |
| Celo | 42220 | CELO |
| Fraxtal | 252 | FRAX |
| Unichain | 130 | ETH |
| World Chain | 480 | ETH |
| Berachain | 80094 | BERA |
| Ink | 57073 | ETH |
| Plasma | 9745 | XPL |
| BOB | 60808 | ETH |
| Story | 1514 | IP |
| Superseed | 5330 | ETH |
| Sei | 1329 | SEI |
| Sonic | 146 | S |
| Soneium | 1868 | ETH |
| X Layer | 196 | OKB |

**注意：**Avalanche、Blast、Linea和Apechain等区块链不支持EIP-7702协议，因此无法使用此功能进行代币转移。

## API基础URL

```
https://zerodust-backend-production.up.railway.app
```

## 第1步：注册API密钥（仅限首次使用）

```bash
curl -X POST https://zerodust-backend-production.up.railway.app/agent/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My OpenClaw Agent",
    "agentId": "openclaw-unique-id"
  }'
```

响应结果：
```json
{
  "apiKey": "zd_abc123...",
  "keyPrefix": "zd_abc12",
  "keyId": "uuid",
  "keyType": "agent",
  "rateLimits": { "perMinute": 300, "daily": 1000 },
  "message": "IMPORTANT: Save your API key now - it will not be shown again!"
}
```

将`apiKey`保存为环境变量`ZERODUST_API_KEY`。

## 第2步：获取报价信息

在清除代币前，需要先查看用户的余额及所需费用：

```bash
curl "https://zerodust-backend-production.up.railway.app/quote?userAddress=0xUSER&fromChainId=42161&toChainId=8453&destination=0xDEST"
```

响应结果：
```json
{
  "quoteId": "uuid",
  "fromChainId": 42161,
  "toChainId": 8453,
  "userAddress": "0x...",
  "destination": "0x...",
  "balance": "500000000000000",
  "balanceFormatted": "0.0005",
  "estimatedReceive": "485000000000000",
  "estimatedReceiveFormatted": "0.000485",
  "totalFeeWei": "15000000000000",
  "serviceFeeWei": "5000000000000",
  "gasFeeWei": "10000000000000",
  "expiresAt": "2026-02-04T16:00:00Z"
}
```

## 第3步：获取授权数据

获取用于签名的EIP-712数据：

```bash
curl -X POST https://zerodust-backend-production.up.railway.app/authorization \
  -H "Content-Type: application/json" \
  -d '{"quoteId": "uuid-from-quote"}'
```

响应结果中包含`typedData`（用于清除操作的EIP-712数据）和`eip7702`（授权参数）。

## 第4步：用户签名

用户需要完成以下签名操作：
1. **EIP-7702授权**：将用户的账户操作权限（EOA）委托给ZeroDust合约
2. **EIP-7702授权撤销**：预先签署撤销授权的合约（在清除操作完成后执行）
3. **EIP-712清除指令**：确认具体的清除参数

## 第5步：提交清除请求

```bash
curl -X POST https://zerodust-backend-production.up.railway.app/sweep \
  -H "Content-Type: application/json" \
  -d '{
    "quoteId": "uuid",
    "delegationSignature": "0x...",
    "revokeSignature": "0x...",
    "sweepSignature": "0x..."
  }'
```

响应结果：
```json
{
  "sweepId": "uuid",
  "status": "pending",
  "txHash": null
}
```

通过`GET /sweep/{sweepId}`接口持续查询清除操作的状态，直到状态变为“completed”。

## 便捷接口：合并报价与授权信息

对于代理来说，可以使用以下接口一次性获取报价和授权信息：

```bash
curl -X POST https://zerodust-backend-production.up.railway.app/agent/sweep \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ZERODUST_API_KEY" \
  -d '{
    "fromChainId": 42161,
    "toChainId": 8453,
    "userAddress": "0x...",
    "destination": "0x..."
  }'
```

## 批量清除（多个链）

可以通过一次请求清除多个链上的代币：

```bash
curl -X POST https://zerodust-backend-production.up.railway.app/agent/batch-sweep \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ZERODUST_API_KEY" \
  -d '{
    "sweeps": [
      {"fromChainId": 42161},
      {"fromChainId": 10},
      {"fromChainId": 137}
    ],
    "destination": "0x...",
    "consolidateToChainId": 8453
  }'
```

## 费用说明

- **服务费用**：余额的1%（最低0.05美元，最高0.50美元）
- **Gas费用**：由ZeroDust承担，费用将从清除后的余额中扣除
- **用户实际获得的金额**：大约97-99%的余额（具体取决于Gas价格）

## 速率限制

- 代理账户：每分钟300次请求，每天1000次清除操作
- 如需更高的请求次数，请联系ZeroDust

## 错误代码

| 错误代码 | 说明 |
|-------|---------|
| `BALANCE_TOO_LOW` | 余额低于最低要求（约0.10美元） |
| `QUOTE_EXPIRED` | 报价信息已超过5分钟的有效期 |
| `CHAIN_NOT_SUPPORTED` | 该链不支持EIP-7702协议 |
| `INVALID_SIGNATURE` | 签名验证失败 |
| `RATE_LIMIT_EXCEEDED` | 达到了每日或每分钟的请求限制 |

## 代理操作示例

**用户：**“我想将我所有的ETH从Arbitrum转移到Base链。”

**代理操作步骤：**
1. 调用 `/quote` 获取用户的余额及费用信息
2. 告知用户：“您在Arbitrum链上有0.005 ETH。扣除费用（约1%）后，您将在Base链上收到0.00495 ETH。需要您签署3份合约。继续吗？”
3. 如果用户同意，调用 `/authorization` 获取所需的签名数据
4. 用户签署相关合约（包括EIP-7702授权、撤销授权以及EIP-712清除指令）
5. 将签名信息提交至 `/sweep` 进行清除操作
6. 持续查询操作状态，直到状态变为“completed”
7. 告知用户：“操作完成！您的Arbitrum链上的余额已清零，Base链上收到了0.00494 ETH。”

## 重要提示：

1. **必须支持EIP-7702**：用户的钱包必须支持该协议。截至2026年，大多数现代钱包均支持EIP-7702。
2. **需要用户签名**：清除操作需要用户的钱包签名。ZeroDust不会持有用户的代币。
3. **清除后的余额**：清除操作完成后，源链上的余额将精确地为零。
4. **跨链转移**：可以通过Gas.zip桥接机制将代币转移到任何支持EIP-7702的链上。
5. **并非所有EVM链都支持**：仅上述列出的25个链支持EIP-7702协议。请勿在不受支持的链上进行清除操作。