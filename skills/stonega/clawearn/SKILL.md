---
name: clawearn
version: 1.1.0
description: 这是一个专为 OpenClaw 机器人设计的模块化预测市场交易平台。用户可以在 Polymarket 上进行交易、管理钱包、转移 USDC（Uniswap 的稳定币），并实现交易策略的自动化。
homepage: https://clawearn.xyz
documentation: https://docs.clawearn.xyz
repository: https://github.com/stonega/moltearn
support: https://discord.gg/clawearn
metadata: 
  category: trading
  type: prediction-markets
  platforms: ["polymarket"]
  features: ["wallet-management", "market-trading", "usdc-transfers", "multi-market", "modular"]
  requires: ["bun", "ethers.js"]
---

# Clawearn - OpenClaw 的模块化交易平台 🎯

**直接从您的 OpenClaw 机器人进行交易预测市场操作。**

Clawearn 使您的 AI 代理能够：
- 🎯 在 Polymarket 预测市场上进行交易
- 💼 创建和管理加密货币钱包
- 💸 将 USDC 发送到 Arbitrum 上的任何以太坊地址
- 📊 监控多个市场中的余额和持仓
- 🤖 自动执行交易策略

---

## 快速入门（3 个步骤）

### 第一步：安装 clawearn CLI

```bash
curl -fsSL https://clawearn.xyz/install.sh | bash
# or: bun link (if in repo)
```

### 第二步：创建您的第一个钱包

```bash
clawearn wallet create
```

您会看到您的钱包地址，请保存它——接下来您需要为其充值。

### 第三步：为钱包充值并开始交易

**选项 A：从其他钱包发送 USDC**
```bash
clawearn wallet send --to YOUR_AGENT_ADDRESS --amount 100
```

**选项 B：自行将 USDC 桥接到 Arbitrum**
- 将 USDC 发送到 Arbitrum 网络
- 发送到 `clawearn wallet show` 显示的地址

**然后搜索市场：**
```bash
clawearn polymarket market search --query "bitcoin price 2025"
```

---

## OpenClaw 机器人的安装

### 安装所有技能文件

```bash
# Create skill directory
mkdir -p ~/.openclaw/skills/clawearn

# Install main files
curl -s https://clawearn.xyz/skills/SKILL.md > ~/.openclaw/skills/clawearn/SKILL.md
curl -s https://clawearn.xyz/skills/HEARTBEAT.md > ~/.openclaw/skills/clawearn/HEARTBEAT.md

# Install core skills
mkdir -p ~/.openclaw/skills/clawearn/core/{wallet,security}
curl -s https://clawearn.xyz/skills/core/wallet/SKILL.md > ~/.openclaw/skills/clawearn/core/wallet/SKILL.md
curl -s https://clawearn.xyz/skills/core/security/SKILL.md > ~/.openclaw/skills/clawearn/core/security/SKILL.md

# Install market skills
mkdir -p ~/.openclaw/skills/clawearn/markets/polymarket
curl -s https://clawearn.xyz/skills/markets/polymarket/SKILL.md > ~/.openclaw/skills/clawearn/markets/polymarket/SKILL.md
curl -s https://clawearn.xyz/skills/markets/polymarket/HEARTBEAT.md > ~/.openclaw/skills/clawearn/markets/polymarket/HEARTBEAT.md
```

## 支持的市场

| 市场 | 状态 | 功能 | 安装方式 |
|--------|--------|----------|--------------|
| **Polymarket** | ✅ 正式上线 | 全面交易、订单管理、市场发现 | 详见上文 |

---

## 核心命令

### 钱包管理

```bash
# Create a new wallet
clawearn wallet create

# Show your wallet address
clawearn wallet show

# Send USDC to another address (on Arbitrum)
clawearn wallet send --to 0x... --amount 100
```

### Polymarket 交易

```bash
# Search for markets
clawearn polymarket market search --query "bitcoin price 2025"

# Get market details
clawearn polymarket market info --market-id MARKET_ID

# Check your balance
clawearn polymarket balance check

# Place a buy order
clawearn polymarket order buy --token-id TOKEN_ID --price 0.50 --size 10

# View open orders
clawearn polymarket order list-open

# Cancel an order
clawearn polymarket order cancel --order-id ORDER_ID
```

## 配置

您可以创建一个可选的配置文件来记录设置：

**`~/.clawearn/config.json`**（可选）
```json
{
  "version": "1.1.0",
  "enabled_markets": ["polymarket"],
  "default_network": "arbitrum",
  "wallet": {
    "network": "arbitrum",
    "auto_fund_threshold": 50
  },
  "trading": {
    "signature_type": 0,
    "default_slippage_pct": 0.5
  },
  "risk_limits": {
    "max_position_size_pct": 20,
    "max_total_exposure_pct": 50,
    "min_balance_alert": 10,
    "daily_loss_limit": 100
  }
}
```

---

## 快速参考

### 检查已安装的市场
```bash
ls ~/.clawearn/skills/markets/
```

### 更新所有技能
```bash
# Update core
curl -s http://localhost:3000/skills/SKILL.md > ~/.clawearn/skills/SKILL.md

# Update each enabled market
for market in $(cat ~/.clawearn/config.json | grep -o '"polymarket"'); do
  curl -s http://localhost:3000/skills/markets/$market/SKILL.md > ~/.clawearn/skills/markets/$market/SKILL.md
done
```

### 添加新市场
```bash
# 1. Install the skill files
mkdir -p ~/.clawearn/skills/markets/NEW_MARKET
curl -s http://localhost:3000/skills/markets/NEW_MARKET/SKILL.md > ~/.clawearn/skills/markets/NEW_MARKET/SKILL.md

# 2. Update your config.json to add "NEW_MARKET" to enabled_markets

# 3. Set up credentials following the market's SETUP.md
```

---

## 安全最佳实践

🔒 **重要提示：**
- 在进行交易之前，请阅读 `core/SECURITY.md`
- 绝不要共享私钥
- 为不同的市场使用不同的钱包
- 在支持的情况下启用双重身份验证（2FA）

---

## 获取帮助

- **关于钱包的问题**：请参阅 `core/WALLET.md`
- **安全相关问题**：请参阅 `core/SECURITY.md`
- **特定市场的相关帮助**：请参阅 `markets/{market}/README.md`
- **常规交易操作**：请参阅 `HEARTBEAT.md` 以获取常规检查信息

---

**检查更新：** 随时重新获取此文件，以查看新增支持的市场！

```bash
curl -s https://clawearn.xyz/skills/SKILL.md | grep '^version:'
```

**准备好开始了吗？** 安装核心技能，选择您想要交易的市场，然后开始交易吧！🚀