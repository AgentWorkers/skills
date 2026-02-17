---
name: solana-connect
description: **OpenClaw Solana Connect** — 一个用于AI代理与Solana区块链交互的工具包。该工具包提供了私钥保护功能：私钥永远不会被暴露给代理程序。支持查询账户余额、生成地址以及内部签名交易。
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "env": ["SOLANA_RPC_URL", "MAX_SOL_PER_TX", "MAX_TOKENS_PER_TX"],
          },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": "@solana/kit",
              "label": "Install Solana Kit (SDK v2)",
            },
            {
              "id": "npm",
              "kind": "npm", 
              "package": "tweetnacl",
              "label": "Install TweetNaCl for secure key handling",
            },
            {
              "id": "npm",
              "kind": "npm",
              "package": "bs58",
              "label": "Install bs58 for encoding",
            },
          ],
      },
  }
---
# 🔗 OpenClaw Solana Connect v2.0

> ⚠️ 目前仅支持读取操作——签名功能尚未实现

**当前状态：**
- ✅ 可以读取区块链数据（余额、交易记录、代币信息）
- ⚠️ 写入操作仅处于模拟阶段

**请注意：此版本为开发预览版，切勿使用真实资金进行交易。**

---

## ⚠️ 安全警告

本工具包会处理私钥，并能够执行真实的加密货币交易。请仔细阅读以下安全指南。

### 建议操作步骤：

1. **始终先在测试网（Testnet）上使用本工具包**  

```bash
# Set testnet RPC for development
export SOLANA_RPC_URL=https://api.testnet.solana.com

# Only switch to mainnet after thorough testing
export SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
```

### 最佳实践：
1. **使用专用钱包** — 切勿使用您的主钱包；为代理交易创建一个包含有限资金的独立钱包。
2. **设置交易限额** — 配置最大交易金额，以防止重大损失。
3. **确认重要交易** — 对于大额交易，务必由人工操作员进行确认。
4. **安全存储私钥** — 使用环境变量存储私钥，切勿将私钥硬编码到代码中。
5. **定期监控交易记录** — 定期查看交易历史和钱包余额。

### 推荐配置：

```javascript
// Recommended: Use environment variables for sensitive data
const config = {
  rpcUrl: process.env.SOLANA_RPC_URL,
  // NEVER hardcode private keys in source code
  // Use: process.env.AGENT_PRIVATE_KEY instead
};
```

---

## 为什么选择 OpenClaw Solana Connect？

大多数 Solana 工具包都是为人类开发者设计的，用于将其集成到应用程序中。但 OpenClaw Solana Connect 的设计有所不同：
- 🧠 **以人工智能为核心** — 专为自动化代理（agents）设计，而非开发者使用。
- 🔄 **与 OpenClaw 兼容** — 可直接与 OpenClaw 的技能（skills）配合使用。
- 🤖 **用户友好** — 支持自然语言输入和自动验证。
- 🛡️ **默认安全** — 交易过程受到安全保护，权限设置清晰明确。

---

## 安装方法：

```bash
# Install via ClawHub
clawhub install solana-connect

# Or clone manually
git clone https://github.com/Seenfinity/openclaw-solana-connect.git
```

### 配置

请设置您的 Solana RPC 端点：

```bash
# For testing (RECOMMENDED FIRST)
export SOLANA_RPC_URL=https://api.testnet.solana.com

# For production (mainnet)
export SOLANA_RPC_URL=https://api.mainnet-beta.solana.com

# Or use Helius (free tier available)
export SOLANA_RPC_URL=https://api.mainnet.helius-rpc.com
```

---

## 测试结果：

所有测试均通过：
- ✅ 能够生成钱包。
- ✅ 成功连接到 Solana RPC 服务器。
- ✅ 可查询余额。
- ✅ 获取代币账户信息。
- ✅ 可获取交易记录。

---

## 功能介绍：

### 钱包操作：
- 生成新的钱包（供代理使用）。
- 通过私钥或助记词连接现有钱包。
- 查看余额（SOL、代币、NFT）。
- 获取交易历史记录。

### 交易操作：
- 向任意地址发送 SOL。
- 发送 SPL 代币。
- 签署并验证交易信息。
- 在发送交易前进行模拟测试。

### 代币操作：
- 查询代币余额。
- 查看 NFT 持有情况。
- 获取代币元数据。
- 判断某个地址是否为代币账户。

### 智能合约/程序操作：
- 获取合约账户信息。
- 获取合约数据。
- 解码交易指令。

---

## 快速入门：

```javascript
const { connectWallet, getBalance, sendSol } = require('./scripts/solana.js');

// Connect with a private key (base58)
const wallet = await connectWallet(privateKey);

// Check balance
const balance = await getBalance(walletAddress);

// Send SOL
const tx = await sendSol(fromWallet, toAddress, amountInSol);
```

---

## 示例：在 Solana 上使用代理进行交易：

```javascript
// 1. Check portfolio balance
const balance = await getBalance(agentWallet);

// 2. Get token accounts
const tokens = await getTokenAccounts(agentWallet);

// 3. Execute trade (via DEX integration)
// const result = await swapToken(inputMint, outputMint, amount);
```

---

## 可用功能：

### `connectWallet`  
连接到现有钱包或生成新钱包。

```javascript
const { connectWallet } = require('./scripts/solana.js');

// From private key (base58)
const wallet = await connectWallet('your-private-key-base58');

// Generate new wallet (returns { address, privateKey })
const newWallet = await connectWallet();
```

### `getBalance`  
查询任意地址的 SOL 和代币余额。

```javascript
const { getBalance } = require('./scripts/solana.js');

const balance = await getBalance('SolanaAddress');
// Returns: { sol: 12.5, tokens: [...], nfts: [...] }
```

### `sendSol`  
将 SOL 从一个地址发送到另一个地址。

```javascript
const { sendSol } = require('./scripts/solana.js');

const tx = await sendSol(fromWallet, toAddress, 1.0); // 1 SOL
```

### `getTokenAccounts`  
获取某个地址的所有 SPL 代币和 NFT 持有情况。

```javascript
const { getTokenAccounts } = require('./scripts/solana.js');

const tokens = await getTokenAccounts(walletAddress);
```

### `sendToken`  
发送 SPL 代币。

```javascript
const { sendToken } = require('./scripts/solana.js');

const tx = await sendToken(fromWallet, toAddress, tokenMint, amount);
```

---

## 应用场景：
- **自动化交易代理**：基于市场分析，在 Solana DEX 上自动执行交易。
- **NFT 监控工具**：监控 NFT 收藏品并实时提醒价格变化。
- **DeFi 收益优化工具**：自动寻找并执行 Solana 协议中的收益 farming 机会。
- **钱包管理工具**：管理多个钱包，自动化支付流程，跟踪投资组合。
- **数据分析工具**：利用 AI 分析链上数据并生成可视化报告。

---

## 架构概述：

```
┌─────────────────────────────────────────────────────┐
│                   OpenClaw Agent                    │
│                  (Your AI Agent)                    │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│           OpenClaw Solana Connect                   │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────┐  │
│  │   Wallet    │  │  Transaction │  │   Token   │  │
│  │  Manager    │  │   Handler    │  │  Manager  │  │
│  └─────────────┘  └──────────────┘  └───────────┘  │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│              @solana/web3.js                        │
│                  Solana RPC                         │
└─────────────────────────────────────────────────────┘
```

---

## 系统要求：
- 需要 OpenClaw 代理（agent）。
- 系统运行环境：Node.js 18 及以上版本。
- 推荐使用 Helius 作为 Solana RPC 服务器。

---

## 开发计划：
- [x] 实现基本钱包功能。
- [x] 支持余额查询。
- [ ] 支持代币转账。
- [ ] 加入 NFT 支持。
- [ ] 集成 DeFi 平台（如 Jupiter、Raydium）。
- [ ] 推出 MCP 服务器模式。

---

## 资源链接：
- 🌐 **GitHub 仓库**：[github.com/Seenfinity/openclaw-solana-connect](https://github.com/Seenfinity/openclaw-solana-connect)
- **Solana 官方文档**：[docs.solana.com]
- **Helius RPC 服务**：[helius.dev]
- **Solana 安全指南**：[docs.solana.com/security]

---

## 许可证：
MIT © 2026 Seenfinity

---

*专为 OpenClaw 代理设计，基于 Solana 架构开发。*