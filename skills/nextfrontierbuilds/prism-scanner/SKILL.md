---
name: prism-scanner
description: **即时检测功能：**  
能够快速识别任何代币的潜在风险，包括持有者集中度、流动性问题以及合约风险。在盲目跟风投资之前，请务必自行进行充分研究（DYOR: Do Your Own Research）。该系统支持与人工智能代理协同工作，为您提供更精准的风险评估结果。
version: 1.1.1
keywords: rug-pull, token-scanner, crypto-safety, scam-detector, dyor, holder-analysis, liquidity-checker, solana-scanner, defi-security, ai, ai-agent, ai-coding, llm, cursor, claude, trading-bot, memecoin, web3, openclaw, moltbot, vibe-coding, agentic
---

# Token Rug Checker

**在使用前请自行了解风险。** 该工具可即时检测任何加密货币代币是否存在欺诈行为（如“rug pull”骗局）。

该工具会扫描代币持有者的集中度、流动性锁定情况、合约中的“蜜罐”机制以及是否存在模仿其他代币的诈骗行为。支持 Solana 和 EVM 链路，由 Strykr PRISM 提供技术支持。

## 快速使用方法

```bash
# Scan by symbol
./scan.sh PEPE

# Scan by contract address
./scan.sh 0x6982508145454Ce325dDbE47a25d4ec3d2311933

# Get JSON output
./scan.sh PEPE --json
```

## 检查内容

| 检查项目 | API 端点 | 风险等级 |
|-------|----------|-------------|
| 模仿/诈骗行为 | `/analyze/copycat` | 高风险 |
| 持有者集中度 | `/analytics/holders` | 中等风险 |
| 流动性状况 | `/analyze` | 高风险 |
| 合约验证 | `/analyze` | 中等风险 |
| 代币发行时间 | `/analyze` | 低风险 |
| 代币重新品牌化历史 | `/analyze/rebrand` | 提供参考信息 |

## 风险评分计算

```
0-25:   ✅ Lower Risk (Green)
26-50:  ⚠️ Medium Risk (Yellow)
51-75:  🔶 Higher Risk (Orange)
76-100: 🚨 High Risk (Red)
```

### 评分标准

| 评分因素 | 最高分 | 触发条件 |
|--------|------------|---------|
| 检测到模仿行为 | 30分 | 与已知诈骗行为相似度超过 70% |
| 存在“蜜罐”机制 | 25分 | 买卖交易存在异常（如税收问题） |
| 持有者集中度过高 | 25分 | 前 10 大钱包持有代币占比超过 60% |
| 流动性未锁定 | 20分 | 液态代币未锁定（LP 未锁定） |
| 合约未通过验证 | 15分 | 合约在区块链浏览器中未通过验证 |
| 新发行的代币（<7 天） | 10分 | 代币最近才上线 |
| 流动性过低 | 10分 | 流动性低于 1 万美元 |

## 输出格式

```
🛡️ PRISM Token Scan: PEPE

Contract: 0x6982508...2311933
Chain: Ethereum

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RISK SCORE: 35/100
████████░░░░░░░░░░░░ Lower Risk

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CHECKS:
✅ No copycat detected
✅ Contract verified on Etherscan
✅ Liquidity locked (12 months)
⚠️ Top 10 wallets hold 42% of supply
✅ Token age: 8 months
✅ Normal buy/sell taxes (0%/0%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HOLDER DISTRIBUTION:
• Top holder: 3.2%
• Top 10: 42%
• Top 100: 68%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ DYOR - This is not financial advice
```

## 使用的 API 端点

```bash
# 1. Resolve token to canonical form
GET /resolve/{symbol_or_address}

# 2. Get general analysis
GET /analyze/{symbol}

# 3. Check for copycat/scam
GET /analyze/copycat/{symbol}

# 4. Get holder distribution
GET /analytics/holders/{contract}

# 5. Check rebrand history
GET /analyze/rebrand/{symbol}
```

## 集成示例

### Telegram 机器人
```
User: /scan PEPE
Bot: 🛡️ Scanning PEPE...
     
     Risk Score: 35/100 (Lower Risk)
     
     ✅ No copycat detected
     ✅ Liquidity locked
     ⚠️ Top 10 hold 42%
     
     [Full Report] [Share]
```

### Discord 机器人
```
!scan 0x6982508...
```

### Web 应用程序
```javascript
const result = await prismScan('PEPE');
// { score: 35, checks: [...], holders: {...} }
```

## 环境变量设置

```bash
PRISM_URL=https://strykr-prism.up.railway.app
PRISM_API_KEY=your-api-key  # Optional
```

---

由 [@NextXFrontier](https://x.com/NextXFrontier) 开发