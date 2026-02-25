# Kite AI Agent 智能钱包 无权限协议 V2.0

## 架构

每位用户都在本地运行自己的 Telegram 机器人：
- 用户创建自己的 Telegram 机器人
- 机器人运行在用户的本地机器上
- 用户的私钥保存在用户的机器上
- OpenClaw 提供智能合约

```
User's PC                        Kite AI Network
┌─────────────────┐              ┌──────────────┐
│ Telegram Bot    │◄────────────►│ Smart        │
│ (runs locally)  │   Commands   │ Contracts    │
│                 │              │              │
│ - Private Key  │              │ - Factory    │
│ - Bot Token    │              │ - Wallet     │
└─────────────────┘              └──────────────┘
```

## 快速入门

### 1. 创建您的 Telegram 机器人
1. 打开 Telegram → 输入 @BotFather
2. 发送 `/newbot`
3. 获取您的 **机器人令牌**

### 2. 获取 Testnet KITE
- 提款机：https://faucet.gokite.ai

### 3. 在本地运行机器人

```bash
# Clone
git clone <repo>
cd kite-agent-wallet-v2

# Install
npm install

# Configure
cp .env.example .env
# Edit .env:
#   PRIVATE_KEY=your_wallet_private_key
#   TELEGRAM_BOT_TOKEN=your_bot_token

# Run
node telegram-bot.js
```

## .env 配置文件

```env
PRIVATE_KEY=0xyour_private_key_here
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
RPC_URL=https://rpc-testnet.gokite.ai
```

## 命令

| 命令 | 描述 |
|---------|-------------|
| `/create` | 创建智能钱包 |
| `/wallet` | 获取钱包地址 |
| `/balance` | 查看余额 |
| `/session add <addr> <limit>` | 添加会话密钥 |
| `/limit set <amount>` | 设置消费限额 |
| `/send <addr> <amount>` | 发送 KITE |
| `/help` | 帮助 |

## 网络

- **测试网**：链 ID 2368
- **RPC**：https://rpc-testnet.gokite.ai
- **浏览器**：https://testnet.kitescan.ai

## 部署的合约

| 合约 | 地址 |
|----------|---------|
| AgentSmartWalletFactory | `0x0fa9F878B038DE435b1EFaDA3eed1859a6Dc098a` |

## 安全性

- 私钥保存在用户的机器上
- 只有用户自己能够控制钱包
- 会话密钥提供了额外的安全保障

## 版本

- v2.0.2 (2026-02-25)：用户运行自己的机器人
- v2.0.1 (2026-02-25)：本地部署
- v2.0.0 (2026-02-25)：初始版本
- v1.0.0 (2026-02-25)：核心合约