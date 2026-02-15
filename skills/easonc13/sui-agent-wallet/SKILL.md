# Sui Agent Wallet 技能

为您的 AI 代理创建一个专属的 Sui 钱包，以便与 DApp 交互并签署交易。

**GitHub:** <https://github.com/EasonC13-agent/sui-skills/tree/main/sui-agent-wallet>

## 架构

```
Chrome Extension ◄──WebSocket──► Local Server ◄──API──► Agent
     │                                │
     ▼                                ▼
  DApp Page                    Key Management
  (Wallet Standard)            (Seed Phrase)
```

## 安装

```bash
cd <your-workspace>/skills/sui-agent-wallet

# Install server dependencies
cd server && bun install

# Start the server
bun run index.ts
```

**安装 Chrome 扩展程序：**
1. 打开 `chrome://extensions/`
2. 启用“开发者模式”
3. 点击“加载解压文件”
4. 选择 `extension/` 文件夹

## 首次启动

服务器会自动生成一个 12 个单词的助记词，并将其存储在 **macOS Keychain** 中：

```
═══════════════════════════════════════════════════════════
  🔐 NEW WALLET CREATED
═══════════════════════════════════════════════════════════

  Seed phrase stored securely in macOS Keychain.

  To view your seed phrase for backup:
    curl http://localhost:3847/mnemonic

  Or use macOS Keychain Access app:
    Service: sui-agent-wallet
    Account: mnemonic
═══════════════════════════════════════════════════════════
```

## 安全存储

| 存储位置 | 存储内容 |
|----------|----------|
| macOS Keychain | 助记词（已加密） |
| `~/.sui-agent-wallet/wallet.json` | 账户地址、网络设置（不含敏感数据） |

**查看 Keychain 中的助记词：**
```bash
# Command line
security find-generic-password -s "sui-agent-wallet" -a "mnemonic" -w

# Or open Keychain Access app
# Search for "sui-agent-wallet"
```

## 代理 API

### 钱包信息

```bash
# Get current address
curl http://localhost:3847/address

# Get balance
curl http://localhost:3847/balance

# Get seed phrase (for backup)
curl http://localhost:3847/mnemonic
```

### 账户管理

```bash
# List all accounts
curl http://localhost:3847/accounts

# Create new account
curl -X POST http://localhost:3847/accounts

# Create account at specific index
curl -X POST http://localhost:3847/accounts \
  -H "Content-Type: application/json" \
  -d '{"index": 2}'

# Switch account
curl -X POST http://localhost:3847/accounts/switch \
  -H "Content-Type: application/json" \
  -d '{"index": 1}'
```

### 网络管理

```bash
# Get current network
curl http://localhost:3847/network

# Switch network (mainnet | testnet | devnet | localnet)
curl -X POST http://localhost:3847/network \
  -H "Content-Type: application/json" \
  -d '{"network": "testnet"}'
```

### 获取测试币（矿池）

**测试网：**
- 官方矿池：<https://faucet.testnet.sui.io/>
- Discord：加入 [Sui Discord](https://discord.gg/sui)，在 `#testnet-faucet` 区域发布您的钱包地址
- 命令行工具：`sui client faucet --address <YOUR_ADDRESS>`

**开发网：**
- 官方矿池：<https://faucet.devnet.sui.io/>
- Discord：在 `#devnet-faucet` 区域发布您的钱包地址
- 命令行工具：`sui client faucet --address <YOUR_ADDRESS>`

**注意**：主网需要使用真实的 SUI 代币，无法使用矿池。

### 交易签名

```bash
# View pending transactions
curl http://localhost:3847/pending

# View transaction details
curl http://localhost:3847/tx/<request-id>

# Approve transaction
curl -X POST http://localhost:3847/approve/<request-id>

# Reject transaction
curl -X POST http://localhost:3847/reject/<request-id>
```

### 导入/导出

```bash
# Import seed phrase (WARNING: overwrites existing wallet!)
curl -X POST http://localhost:3847/import \
  -H "Content-Type: application/json" \
  -d '{"mnemonic": "your twelve word seed phrase here ..."}'
```

### 命令行工具集成（直接签名）

**使用 Sui CLI 生成未签名交易并签名：**
```bash
# 1. Generate unsigned transaction (using Agent Wallet address)
AGENT_ADDR=$(curl -s localhost:3847/address | jq -r .address)
TX_BYTES=$(sui client publish --serialize-unsigned-transaction \
  --sender $AGENT_ADDR --gas-budget 100000000 | tail -1)

# 2. Sign and execute with Agent Wallet
curl -X POST http://localhost:3847/sign-and-execute \
  -H "Content-Type: application/json" \
  -d "{\"txBytes\": \"$TX_BYTES\"}"

# Or sign only without executing
curl -X POST http://localhost:3847/sign-raw \
  -H "Content-Type: application/json" \
  -d "{\"txBytes\": \"$TX_BYTES\"}"
```

**支持的命令行工具：**
- `sui client publish --serialize-unsigned-transaction`
- `sui client call --serialize-unsigned-transaction`
- `sui client transfer-sui --serialize-unsigned-transaction`

## 交易解析

当收到签名请求时，代理会进行以下检查：

```json
{
  "id": "req_123",
  "method": "signTransaction",
  "origin": "http://localhost:5173",
  "payload": {
    "transaction": "{\"commands\":[{\"MoveCall\":{...}}]}",
    "chain": "sui:devnet"
  }
}
```

## 安全检查清单

在签名之前，请确认：
- [ ] 目标合约是否可信？
- [ ] 交易金额是否合理？
- [ ] 是否存在可疑的币转移行为？
- [ ] 交易所需的 Gas 预算是否正常？

## 测试 DApp

内置的 Counter DApp 用于测试：

```bash
# Start frontend
cd test-dapp/frontend && pnpm dev

# Open http://localhost:5173
# 1. Connect Wallet → Select "Sui Agent Wallet"
# 2. Click "+1" → Sends a signing request
# 3. Agent uses /pending to view, /approve to sign
```

## 技术细节

### BIP44 导出路径

```
m/44'/784'/{accountIndex}'/0'/0'
```

- 784 表示 Sui 的代币类型
- 每个 `accountIndex` 对应一个钱包地址

### 钱包标准功能

实现了 Sui 钱包的标准功能：
- `standard:connect`：连接钱包
- `standard:disconnect`：断开连接
- `standard:events`：接收事件通知
- `sui:signTransaction`：签署交易
- `sui:signAndExecuteTransaction`：签署并执行交易
- `sui:signPersonalMessage`：发送个人消息

### 事件通知

在切换账户或网络时，服务器会通过 WebSocket 通知扩展程序：
- `accountChanged`：账户信息变更
- `networkChanged`：网络信息变更

## 相关技能

此技能属于 Sui 开发技能套件的一部分：

| 技能 | 描述 |
|-------|-------------|
| [sui-decompile](https://clawhub.ai/EasonC13/sui-decompile) | 获取并读取链上合约源代码 |
| [sui-move](https://clawhub.ai/EasonC13/sui-move) | 编写和部署 Move 智能合约 |
| [sui-coverage](https://clawhub.ai/EasonC13/sui-coverage) | 使用安全分析工具检查测试覆盖率 |
| **sui-agent-wallet** | 构建和测试 DApp 的前端界面 |

**工作流程：**
```
sui-decompile → sui-move → sui-coverage → sui-agent-wallet
    Study        Write      Test & Audit   Build DApps
```

所有技能的完整列表请参见：<https://github.com/EasonC13-agent/sui-skills>