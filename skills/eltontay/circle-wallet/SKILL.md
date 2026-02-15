# Circle Wallet 技能

通过 Circle 开发者控制的钱包，为 OpenClaw 代理提供 USDC 钱包操作功能。

## 主要功能

- 创建 SCA（智能合约账户）
- 查看多个链上的 USDC 余额
- 向任意地址发送 USDC
- 通过 Circle Gas Station 进行无需 gas 费用的交易
- 支持多钱包管理（可通过地址或 ID 进行管理）
- 地址验证和余额查询
- 支持 21 个区块链（主网 + 测试网）

## 安装

```bash
clawhub install circle-wallet
cd ~/.openclaw/workspace/skills/circle-wallet
npm install
npm link
```

## 快速入门

### 1. 获取 API 密钥
从 https://console.circle.com 获取您的 API 密钥。

### 2. 设置

**新用户：**
```bash
circle-wallet setup --api-key your-api-key
```

**现有用户：**
```bash
circle-wallet configure --api-key your-key --entity-secret your-secret
```

### 3. 创建钱包并获取资金
```bash
circle-wallet create "My Wallet"
circle-wallet drip                    # Testnet only
circle-wallet balance
```

### 4. 发送 USDC
```bash
circle-wallet send 0x... 10 --from 0x...
```

## 所有命令

```bash
# Setup
circle-wallet setup --api-key <key>                          # Generate and register entity secret
circle-wallet configure --api-key <key> --entity-secret <s>  # Use existing credentials
circle-wallet config                                         # View configuration

# Chains
circle-wallet chains                   # List all supported blockchains
circle-wallet chains --show-tokens     # Show USDC token IDs
circle-wallet chains --mainnet         # Mainnets only
circle-wallet chains --testnet         # Testnets only

# Wallets
circle-wallet create [name] [--chain <blockchain>]   # Create new SCA wallet
circle-wallet list                                    # List all wallets with balances
circle-wallet balance [wallet-id]                     # Check balance

# Transactions
circle-wallet send <to> <amount> [--from <wallet-id-or-address>]  # Auto-detects chain from wallet
circle-wallet drip [address]                                       # Get testnet USDC (sandbox only)
```

## 支持的区块链

**主网（10 个）：**
APTOS, ARB, AVAX, BASE, ETH, MONAD, OP, MATIC, SOL, UNI

**测试网（11 个）：**
APTOS-TESTNET, ARB-SEPOLIA, ARC-TESTNET, AVAX-FUJI, BASE-SEPOLIA, ETH-SEPOLIA, MONAD-TESTNET, OP-SEPOLIA, MATIC-AMOY, SOL-DEVNET, UNI-SEPOLIA

使用 `circle-wallet chains --show-tokens` 命令可查看每个链上的 USDC 代币 ID。

## 使用示例

### 多链钱包管理
```bash
# Create wallets on different chains (default: ARC-TESTNET for sandbox)
circle-wallet create "Arc Wallet" --chain ARC-TESTNET
circle-wallet create "Base Wallet" --chain BASE-SEPOLIA
circle-wallet create "Polygon Wallet" --chain MATIC-AMOY

# Send automatically uses the correct chain for each wallet
circle-wallet send 0xRecipient... 5 --from 0xArcWallet...
circle-wallet send 0xRecipient... 3 --from 0xPolygonWallet...
```

### 在不同钱包之间转账
```bash
# Create two wallets
circle-wallet create "Wallet 1"
circle-wallet create "Wallet 2"

# Fund first wallet
circle-wallet drip

# Send from wallet 1 to wallet 2 (using addresses)
circle-wallet send 0xWallet2Address... 5 --from 0xWallet1Address...
```

### 代理使用
```
User: "Check my wallet balance"
Agent: [circle-wallet balance] "You have 42.5 USDC"

User: "Send 10 USDC to 0x123..."
Agent: [circle-wallet send 0x123... 10] "Sent! TX: 0xabc..."
```

## 配置

凭据存储位置：`~/.openclaw/circle-wallet/`

**环境变量：**
- `CIRCLE_API_KEY` - 设置命令所需
- `CIRCLE_ENV` - 可选：`sandbox` 或 `production`（默认：sandbox）

## 故障排除

- **“未配置钱包”**  
- **“余额不足”**  
- **“实体密钥已注册”**  
- **“以太坊地址格式无效”**  
  地址必须以 `0x` 开头，后跟 40 个十六进制字符。

## 资源

- Circle 开发者文档：https://developers.circle.com
- Circle 控制台：https://console.circle.com
- GitHub 仓库：https://github.com/eltontay/clawhub_circle_wallet_skill

## 许可证

MIT

---

**此项目为 OpenClaw 社区个人开发，未获得 Circle 的官方支持。**