---
name: presage
description: 连接到 Solana 平台上的 Presage 预测市场终端（由 Kalshi 提供支持）。您可以实时分析市场行情，寻找交易机会，并获得关于体育、加密货币、政治等领域的“是/否”结果的 AI 预测分析。无论您需要市场分析、发现投资机会还是跟踪投资组合，都可以使用该工具。
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "env": [],
          },
      },
  }
---

# 📊 **Presage** — AI 预测市场分析技能  
**利用 AI 的强大功能分析预测市场**  

本技能由 **Kalshi**（一个受监管的预测市场交易平台）提供支持，基于 **Solana** 架构构建，具备快速、低成本的链上交易能力。  

---

## 该技能的功能  
本技能为 Presage 预测市场提供以下 **只读市场分析工具**：  
- 📊 **实时市场数据**：实时价格、成交量和订单簿  
- 🔍 **机会检测**：自动识别价格异常的市场  
- 📈 **投资组合视图**：查看余额和持仓情况  
- 🧠 **AI 智能分析**：获取分析结果和建议  

**注意：** 本技能仅用于市场分析，实际交易操作需要另行实现。  

---

## 安装  
```bash
# Install via ClawHub (recommended)
clawhub install presage

# Or manually
git clone https://github.com/Seenfinity/presage-skill.git
```  

---

## 立即尝试  
**最佳测试方式：** 访问 [presage.market](https://presage.market)  
- 浏览实时市场数据（NFL、NBA、比特币、以太坊、政治等）  
- 观看 AI 代理的实时交易行为  
- 查看终端界面中的图表、订单簿及代理交易表现  

---

## 可用工具  
### `analyzeMarkets`  
获取所有可用市场的完整概览，并结合 AI 智能分析结果。  
```javascript
const { analyzeMarkets } = require('./scripts/analysis.js');
const result = await analyzeMarkets({ limit: 20 });
// Returns: total markets, top volume, AI recommendations
```  

### `analyzeMarket`  
深入分析任意特定市场。  
```javascript
const { analyzeMarket } = require('./scripts/analysis.js');
const result = await analyzeMarket({ ticker: "KXBTC-100K-26MAR-YES" });
// Returns: price, volume, orderbook, AI analysis
```  

### `findOpportunities`  
自动扫描价格异常的市场。  
```javascript
const { findOpportunities } = require('./scripts/analysis.js');
const result = await findOpportunities({ minVolume: 50000 });
// Returns: markets where YES/NO prices seem off
```  

### `getPortfolio`  
查看您的余额和持仓情况。  
```javascript
const { getPortfolio } = require('./scripts/analysis.js');
const result = await getPortfolio({ agentId: "your-agent-id" });
// Returns: balance, positions, P&L
```  

---

## 示例输出  
```json
{
  "totalMarkets": 45,
  "opportunities": [
    {
      "ticker": "KXBTC-100K-26MAR-YES",
      "title": "Bitcoin above $100K by March 2026?",
      "price": 0.72,
      "volume": 1200000,
      "recommendation": "CONSIDER_NO",
      "reasoning": "High volume but price very high. Market may be overconfident."
    }
  ],
  "topMarkets": [...],
  "summary": "Found 45 markets with 8 potential opportunities."
}
```  

---

## API 使用  
本技能可通过 Presage 的公开 API 进行数据交互：  
```bash
# Browse markets
curl https://presage.market/api/events?limit=20

# Get market details
curl https://presage.market/api/markets/{ticker}
```  

---

## 系统要求  
- 需要安装 OpenClaw 或兼容的代理平台  
- Node.js 18 及以上版本（内置 fetch 模块）  

---

## 资源链接  
- 🌐 **终端界面**：[presage.market](https://presage.market)  
- 📖 **文档**：[presage.market/api](https://presage.market/api)  
- 🦞 **技能详情**：[clawhub.ai/Seenfinity/presage](https://clawhub.ai/Seenfinity/presage)  
- 📂 **GitHub 仓库**：[github.com/Seenfinity/presage-skill](https://github.com/Seenfinity/presage-skill)  

---

*智能分析，更明智地交易。*