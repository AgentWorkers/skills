---
name: polyclawster-agent
description: 在 Polymarket 的预测市场中进行交易。这种交易方式属于非托管模式：您的代理程序会在您的设备上生成一个 Polygon 钱包，使用该钱包的私钥来签署交易订单，并通过 polyclawster.com 的中继服务（支持地理绕过功能）来提交这些订单。私钥始终不会离开您的设备。
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["node"] },
      "permissions": {
        "network": [
          "polyclawster.com",
          "polygon-rpc.com"
        ],
        "fs": {
          "write": ["~/.polyclawster/config.json"],
          "read":  ["~/.polyclawster/config.json"]
        }
      },
      "credentials": [
        {
          "key": "POLYCLAWSTER_API_KEY",
          "description": "Agent API key (auto-generated at setup, stored in ~/.polyclawster/config.json). Not a private key — just for polyclawster.com portfolio/demo API.",
          "required": false
        }
      ]
    }
  }
---
# polyclawster-agent

使用您的 OpenClaw 代理在 [Polymarket](https://polymarket.com) 的预测市场中进行交易。

## 如何与 OpenClaw 一起使用

安装此插件后，您可以像与普通代理交流一样自然地与其对话：

```
"Set me up to trade Polymarket in demo mode"
→ runs: node scripts/setup.js --auto

"Browse crypto markets on Polymarket"
→ runs: node scripts/browse.js "crypto"

"Place a $2 demo bet on bitcoin reaching 100k"
→ runs: node scripts/trade.js --market "bitcoin-100k" --side YES --amount 2 --demo

"Show my Polymarket balance"
→ runs: node scripts/balance.js

"Auto-trade Polymarket every hour with score above 8"
→ sets up OpenClaw cron: node scripts/auto.js --min-score 8 --max-bet 5 --demo
```

您的代理能够理解插件的指令，并可以执行一系列命令，例如：浏览市场 → 选择交易市场 → 进行交易。

## OpenClaw 的 Cron 任务设置

您可以要求代理设置自动交易规则：

> *"以演示模式每 30 分钟自动执行一次 polyclawster 交易"*

或者您也可以手动设置 Cron 任务——只需告诉您的代理相应的指令：

```
Create a cron job that runs every 30 minutes:
  node /path/to/polyclawster/scripts/auto.js --demo --min-score 7 --max-bet 5
```

代理会通过 `cron` 工具自动完成这些设置。

## 架构 —— 非托管模式

**您的私钥始终存储在您的设备上。**

```
Your Agent Container:
  ├─ generates wallet locally (ethers.Wallet.createRandom())
  ├─ signs orders locally (EIP-712 with private key)
  ├─ signs requests locally (HMAC with api_secret)
  └─ private key: ~/.polyclawster/config.json (chmod 600) only

polyclawster.com:
  ├─ stores: wallet_address, demo_balance, trade_history
  ├─ does NOT store: private key, CLOB api_secret
  ├─ /api/clob-relay: geo-bypass proxy → clob.polymarket.com (Tokyo)
  ├─ /api/signals: AI-scored trading opportunities
  └─ /api/agents: portfolio, leaderboard, TMA visibility

Polymarket CLOB:
  └─ receives already-signed orders, verifies EIP-712 signature
```

## 快速入门

### 1. 设置（在本地生成钱包）
```bash
node scripts/setup.js --auto
```

### 2. 浏览市场
```bash
node scripts/browse.js "bitcoin"
node scripts/browse.js "election" --min-volume 100000
```

### 3. 演示交易（免费提供 10 美元余额）
```bash
node scripts/trade.js --market "bitboy-convicted" --side YES --amount 2 --demo
```

### 4. 查看余额与未平仓头寸
```bash
node scripts/balance.js
```

### 5. 实时交易（在您的钱包中存入 USDC 后）
```bash
node scripts/approve.js         # one-time USDC approval (~0.01 POL gas)
node scripts/trade.js --market "bitboy-convicted" --side YES --amount 10
```

### 6. 根据 AI 信号进行自动交易
```bash
node scripts/auto.js --dry-run                         # preview
node scripts/auto.js --demo --min-score 7 --max-bet 5  # demo mode
node scripts/auto.js --min-score 8 --max-bet 10        # live mode
```

## 安全模型

| 数据类型 | 存储位置 | 可查看数据的人员 |
|------|-------------|----------------|
| 私钥 | `~/.polyclawster/config.json`（权限设置为 600） | 仅您的设备 |
| CLOB api_secret | `~/.polyclawster/config.json` | 仅您的设备 |
| CLOB api_key | `~/.polyclawster/config.json` | 您的设备以及 Polymarket |
| 钱包地址 | polyclawster.com + Polygon 区块链 | 公开 |
| 交易历史记录 | polyclawster.com 的 Supabase 数据库 | polyclawster.com |

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `setup.js --auto` | 生成钱包、派生 CLOB 凭据并完成注册 |
| `setup.js --derive-clob` | 重新生成 CLOB 凭据 |
| `setup.js --info` | 显示当前配置 |
| `approve.js` | 为实时交易进行一次性的链上 USDC 批准 |
| `approve.js --check` | 检查批准状态（无交易记录） |
| `browse.js [topic]` | 在 Polymarket 上搜索市场 |
| `trade.js --market X --side YES --amount N` | 进行实时交易（本地签名） |
| `trade.js ... --demo` | 进行演示交易 |
| `balance.js` | 查看投资组合和余额 |
| `sell.js --list` | 列出未平仓头寸 |
| `sell.js --bet-id N` | 平仓头寸 |
| `auto.js` | 根据 AI 信号进行自动交易 |
| `auto.js --dry-run` | 模拟交易过程（不进行实际交易） |
| `link.js PC-XXXXX` | 将代理与 TMA 账户关联 |

## 代理控制面板

设置完成后，您可以通过以下链接访问代理的控制面板：`https://polyclawster.com/a/YOUR_AGENT_ID`

由 [Virix Labs](https://virixlabs.com) 开发 · [polyclawster.com](https://polyclawster.com) 提供支持