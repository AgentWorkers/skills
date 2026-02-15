---
name: prism-alerts
description: 实时推送Solana交易者的Pump.fun代币警报：新发行、代币毕业（即完成特定条件后释放）、交易量激增等信息。适用于交易机器人、Discord、Telegram以及AI代理。
version: 1.1.1
keywords: pumpfun, solana, memecoin, token-alerts, trading-bot, crypto-alerts, degen, solana-trading, real-time-alerts, ai, ai-agent, ai-coding, llm, cursor, claude, automation, defi, web3, openclaw, moltbot, vibe-coding, agentic
---

# Pump.fun 警报机器人

**不错过任何新币发布！** 为 Pump.fun 代币的发布、上架以及 Solana 平台上的交易量激增事件提供实时警报。

专为交易机器人、Discord 警报和 Telegram 通知而设计，由 Strykr PRISM 提供支持。

## 快速使用指南

```bash
# Get current bonding tokens
./alerts.sh bonding

# Get recently graduated tokens
./alerts.sh graduated

# Watch for new tokens (poll every 30s)
./alerts.sh watch
```

## 独特的数据来源

PRISM 是为数不多的能够提供 Pump.fun 代币绑定曲线实时数据的 API 之一：

| API 端点 | 描述 | 数据更新速度 |
|----------|-------------|-------|
| `/crypto/trending/solana/bonding` | 提供代币的绑定曲线数据 | 648 毫秒 |
| `/crypto/trending/solana/graduated` | 提供已上架到 DEX 的代币信息 | 307 毫秒 |

## 警报类型

### 1. 新币发布警报
```
🚀 NEW PUMP.FUN TOKEN

$DOGWIFCAT
CA: 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU

📊 Stats:
• Bonding Progress: 12%
• Market Cap: $8,450
• Holders: 23
• Created: 2 min ago

[🔍 Scan] [📈 Chart] [💰 Buy]
```

### 2. 代币上架警报
```
🎓 TOKEN GRADUATED!

$MEMECOIN just graduated to Raydium!

📊 Final Stats:
• Market Cap: $69,000
• Total Holders: 1,247
• Bonding Time: 4h 23m

Trading now live on Raydium DEX
[📈 Trade on Raydium]
```

### 3. 交易量激增警报
```
📈 VOLUME SPIKE DETECTED

$CATDOG seeing unusual activity

• Volume (5m): $45,230 (+340%)
• Price: +28% in 10 minutes
• New holders: +89

⚠️ Could be coordinated buy - DYOR
[🔍 Scan] [📈 Chart]
```

## 机器人命令

```
/start           - Subscribe to alerts
/stop            - Unsubscribe
/bonding         - Current bonding tokens
/graduated       - Recent graduations
/scan <token>    - Scan specific token
/settings        - Configure alert filters
```

## 警报过滤规则

您可以配置接收哪些类型的警报：

```javascript
{
  "minMarketCap": 5000,      // Minimum MC to alert
  "maxMarketCap": 100000,    // Maximum MC to alert
  "minHolders": 10,          // Minimum holder count
  "bondingProgress": 20,     // Alert when > 20% bonded
  "volumeSpike": 200,        // Alert on 200%+ volume increase
  "enableGraduations": true, // Alert on graduations
  "enableNewLaunches": true  // Alert on new tokens
}
```

## 集成方式

### Telegram 机器人
```javascript
import { Telegraf } from 'telegraf';
import { PrismClient } from './prism';

const bot = new Telegraf(process.env.BOT_TOKEN);
const prism = new PrismClient();

// Poll every 30 seconds
setInterval(async () => {
  const bonding = await prism.pumpfunBonding();
  const newTokens = filterNewTokens(bonding);
  
  for (const token of newTokens) {
    await bot.telegram.sendMessage(CHANNEL_ID, formatAlert(token));
  }
}, 30000);
```

### Discord 机器人
```javascript
import { Client } from 'discord.js';

client.on('ready', () => {
  pollPumpfun(client);
});
```

## 环境变量设置

```bash
PRISM_URL=https://strykr-prism.up.railway.app
TELEGRAM_BOT_TOKEN=xxx
TELEGRAM_CHANNEL_ID=xxx
DISCORD_BOT_TOKEN=xxx
DISCORD_CHANNEL_ID=xxx
```

## 数据轮询的最佳实践

1. **速率限制**：每 30 秒最多轮询一次。
2. **去重**：使用 SQLite/Redis 存储已发送的警报信息。
3. **批量发送**：将多个警报合并成一条消息。
4. **冷却机制**：避免在 5 分钟内重复发送同一代币的警报。

---

由 [@NextXFrontier](https://x.com/NextXFrontier) 开发