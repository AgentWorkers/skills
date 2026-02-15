---
name: agent-wallet
description: 适用于AI代理的多链钱包管理工具。支持创建钱包、查询余额、转账代币（USDC/原生代币）以及跨链操作。当代理需要发送/接收付款、查询资金或管理加密钱包时，可使用该工具。支持Solana、Base和Ethereum区块链。常用指令包括：“create wallet”（创建钱包）、“check balance”（查询余额）、“send USDC”（发送USDC）、“transfer”（转账）、“my addresses”（查看地址列表）和“wallet status”（查看钱包状态）。
---

# AgentWallet

这是一个专为AI代理设计的多链钱包工具。只需提供一个种子短语，即可管理所有支持的区块链。

## 快速参考

| 命令 | 例子 |
|---------|---------|
| 创建钱包 | "创建一个新的钱包" |
| 显示地址 | "显示我的地址" / "我的钱包里有什么?" |
| 检查余额 | "查看我的余额" / "我有多少USDC?" |
| 转账 | "向0x...转账10 USDC" / "向...转账5 SOL" |
| 跨链转账 | "将10 USDC从Base链桥接到Solana链" |
| 链路信息 | "支持哪些区块链?" |

## 设置

### 新钱包

```
User: "Create a new wallet"
```

生成BIP-39种子短语，并为所有支持的区块链生成地址。该种子短语仅会显示一次，并会发出安全警告。

### 导入现有钱包

```
User: "Import my wallet"
```

提示：请将您的种子短语添加到`.env`文件中（键名为`WALLET_SEED_PHRASE`），然后输入“Show my addresses”进行验证。

**注意：** 为了安全起见，导入钱包时不允许在聊天框中输入种子短语。

### 环境配置

```bash
# Required for wallet operations
WALLET_SEED_PHRASE="your twelve word seed phrase goes here"

# Optional
NETWORK=testnet          # testnet (default) or mainnet
SOLANA_RPC=              # Custom Solana RPC (defaults to public)
BASE_RPC=                # Custom Base RPC (defaults to public)
ETH_RPC=                 # Custom Ethereum RPC (defaults to public)
```

## 命令

### 创建钱包

运行命令：`node scripts/wallet.js create`

输出格式：
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔐 NEW WALLET GENERATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  CRITICAL: Save this seed phrase securely!
    It will NOT be shown again.
    Anyone with this phrase can access your funds.

Seed Phrase:
┌────────────────────────────────────────────┐
│ word1 word2 word3 word4 word5 word6        │
│ word7 word8 word9 word10 word11 word12     │
└────────────────────────────────────────────┘

Your Addresses:
├─ Solana:   7xK9...mP4q
├─ Base:     0x7a3B...4f2E
└─ Ethereum: 0x7a3B...4f2E (same as Base)

Add to .env:
WALLET_SEED_PHRASE="word1 word2 word3 ..."

Network: TESTNET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 显示地址

运行命令：`node scripts/wallet.js addresses`

会显示生成的地址，但不会暴露种子短语。

### 检查余额

运行命令：`node scripts/wallet.js balance [chain]`

- `node scripts/wallet.js balance` - 查看所有链路的余额
- `node scripts/wallet.js balance solana` - 仅查看Solana链的余额
- `node scripts/wallet.js balance base` - 仅查看Base链的余额

输出结果包括每个链路的原生代币和USDC余额。

### 转账

运行命令：`node scripts/wallet.js transfer <chain> <token> <amount> <recipient>`

示例：
- `node scripts/wallet.js transfer solana USDC 10 7xK9fR2...`  
- `node scripts/wallet.js transfer base ETH 0.01 0x7a3B...`  
- `node scripts/wallet.js transfer solana SOL 0.5 7xK9fR2...`

**支持的代币：**
- **Solana**: SOL, USDC
- **Base**: ETH, USDC
- **Ethereum**: ETH, USDC

### 跨链转账

运行命令：`node scripts/wallet.js bridge <from-chain> <to-chain> <amount>`

使用Circle CCTP V2协议在区块链之间转账USDC。

示例：
- `node scripts/wallet.js bridge base solana 10` - 将10 USDC从Base链桥接到Solana链
- `node scripts/wallet.js bridge ethereum base 50` - 将50 USDC从Ethereum链桥接到Base链
- `node scripts/wallet.js bridge solana ethereum 25` - 将25 USDC从Solana链桥接到Ethereum链

**注意：** 跨链转账需要1-5分钟的时间（包括燃烧、验证和铸造过程）。操作需要源链上有足够的USDC，并且目标链上有足够的原生代币作为交易手续费。

### 链路信息

运行命令：`node scripts/wallet.js chains`

会列出所有支持的区块链、网络以及相关的USDC合约地址。

## 密钥生成机制

所有链路的地址都是基于同一个BIP-39种子短语生成的：

| 链路 | 密钥生成路径 | 标准 |
|-------|------|----------|
| Solana | `m/44'/501'/0'/0'` | Solana/Phantom |
| EVM (Base/Eth) | `m/44'/60'/0'/0/0` | BIP-44 Ethereum |

EVM系列区块链使用相同的密钥生成路径。

## 安全模型

- **每个代理使用独立的种子短语**：确保每个代理实例的隐私安全。
- **种子短语仅显示一次**：仅在创建钱包时显示，不会被记录。
- **密钥动态生成**：私钥按需生成，不会被持久化存储。
- **禁止通过聊天框导入种子短语**：种子短语必须通过`.env`文件进行配置。

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|-----|
| "WALLET_SEED_PHRASE未设置" | `.env`文件中缺少该环境变量 | 请将种子短语添加到`.env`文件中。 |
| "种子短语格式错误" | 种子短语长度不正确（应为12或24个单词） | 请确保格式正确。 |
| “余额不足” | 账户余额不足 | 请先检查余额。 |
| “地址格式错误” | 收件人地址格式不正确 | 请验证收件人地址。 |

## 链路参考

有关RPC端点、USDC地址和各链路的详细信息，请参阅[references/chains.md](references/chains.md)。