---
name: clawdwallet
description: 安装并使用 ClawdWallet——这是一个由 Clawdbot 代理控制的多链 Web3 钱包 Chrome 扩展程序。您可以使用它来设置由代理控制的钱包、连接到去中心化应用（dApps）、签署交易，以及在 20 多个区块链（如 EVM、比特币、Solana、Cosmos）上管理加密货币。该钱包基于 ShapeShift 的 HDWallet 技术实现。
---

# ClawdWallet

这是一个多链钱包扩展程序，您的代理可以通过WebSocket对其进行控制。

## 快速安装

```bash
# Clone and build
git clone https://github.com/NeOMakinG/clawdwallet.git
cd clawdwallet
npm install
npm run build

# Or use pre-built dist/ folder directly
```

### 在Chrome中安装

1. 打开“chrome://extensions”页面，启用**开发者模式**。
2. 选择“Load unpacked”（加载解压后的文件），然后选择`dist/`文件夹。
3. 点击扩展程序图标，设置WebSocket地址（默认地址：`ws://localhost:3033/clawdwallet`）。

## Clawdbot网关配置

将以下配置添加到您的网关配置中：

```yaml
extensions:
  clawdwallet:
    enabled: true
```

## 代理命令

### 使用现有种子词串初始化钱包
```json
{"type": "init_wallet", "mnemonic": "your twenty four words..."}
```

### 生成新钱包
```json
{"type": "generate_wallet"}
```
该命令会返回所有支持链路的钱包地址。

### 批准dApp请求
```json
{"type": "sign_and_respond", "requestId": "uuid"}
```

### 拒绝请求
```json
{"type": "reject_request", "requestId": "uuid", "reason": "Looks suspicious"}
```

### 检查状态
```json
{"type": "get_status"}
```

## 接收到的请求

当dApp请求签名时，您会收到相应的请求信息：
```json
{
  "type": "wallet_request",
  "id": "uuid",
  "chain": "ethereum",
  "method": "eth_sendTransaction",
  "params": [{"to": "0x...", "value": "0x..."}],
  "origin": "https://app.uniswap.org"
}
```

根据具体情况审查并批准或拒绝请求。

## 支持的链路

| 链路类型 | 支持的链路 |
|--------|--------|
| EVM | Ethereum、Polygon、Optimism、Arbitrum、Base、Avalanche、Gnosis、BSC |
| UTXO | Bitcoin、Litecoin、Dogecoin、Bitcoin Cash |
| Cosmos | Cosmos Hub、Osmosis、THORChain、Mayachain |
| 其他 | Solana、TON、Near、Sui、Tron |

## 安全注意事项

- 仅与可信赖的代理配合使用。
- 建议为代理操作使用专用的钱包。
- 绝不要公开钱包的助记词或WebSocket地址。