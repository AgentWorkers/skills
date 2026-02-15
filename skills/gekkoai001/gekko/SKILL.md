---
name: gekko-portfolio-manager
description: 基于 Base 网络的 AI 驱动型去中心化金融（DeFi）投资组合管理器。该工具能够分析收益机会、管理投资组合配置，并提供跨各类 DeFi 协议的市场情报。实时获取来自 Morpho 和 Yearn 的投资组合收益（APY）分析数据。
version: 1.0.0
metadata: {"clawdbot":{"emoji":"🤖","category":"defi","requires":{"bins":["node"],"api_endpoint":"https://gekkoterminal.ai/api/a2a?agent=gekko"}}}
---

# Gekko — 组合投资管理器

这是一个基于人工智能的DeFi（去中心化金融）组合投资管理工具，专为Base网络设计。它能够帮助用户分析收益机会、管理投资组合配置，并提供市场洞察。

**代理ID：** 13445 | **区块链网络：** Base | **协议版本：** A2A v0.3.0

## Gekko的功能

Gekko具备以下功能：
- 分析Base网络上的DeFi协议中的收益机会；
- 管理多个投资组合中的资产分配；
- 提供实时的市场信息和交易建议；
- 根据用户的风险偏好优化收益策略。

## 命令

### portfolio_management
使用Morpho和Yearn协议的数据，进行实时投资组合收益分析，并根据当前的年化收益率（APY）、总价值锁定（TVL）和风险状况，推荐最佳的投资组合配置。

**使用方法：**
```bash
curl -X POST https://gekkoterminal.ai/api/a2a?agent=gekko \
  -H "Content-Type: application/json" \
  -d '{
    "capability": "portfolio_management",
    "parameters": {
      "action": "analyze",
      "tokens": ["0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"]
    }
  }'
```

**参数：**
- `action`（字符串，可选）：`analyze` | `optimize` | `recommend`
- `tokens`（数组，可选）：需要分析的代币地址列表

### token_analysis
从DexScreener获取任意代币的实时价格、交易量和流动性数据，识别市场趋势并提供可操作的交易信号。

**使用方法：**
```bash
curl -X POST https://gekkoterminal.ai/api/a2a?agent=gekko \
  -H "Content-Type: application/json" \
  -d '{
    "capability": "token_analysis",
    "parameters": {
      "token": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      "metrics": ["price", "volume", "trend"]
    }
  }'
```

**参数：**
- `token`（字符串，必填）：代币合约地址
- `metrics`（数组，可选）：`price` | `volume` | `trend` | `liquidity`

### yield_optimization
在Base网络上寻找最高的收益机会，比较所有被监控投资组合的年化收益率（APY）、总价值锁定（TVL）和风险状况。支持按风险容忍度和资产类型进行筛选。

**使用方法：**
```bash
curl -X POST https://gekkoterminal.ai/api/a2a?agent=gekko \
  -H "Content-Type: application/json" \
  -d '{
    "capability": "yield_optimization",
    "parameters": {
      "chain": "base",
      "asset": "USDC",
      "risk_tolerance": "medium"
    }
  }'
```

**参数：**
- `chain`（字符串，可选）：区块链网络（默认：`base`）
- `asset`（字符串，可选）：需要优化的资产（默认：`USDC`）
- `risk_tolerance`（字符串，可选）：`low` | `medium` | `high`

### market_intelligence
提供市场洞察、趋势分析和交易信号，分析不同时间范围内的DeFi市场状况。

**使用方法：**
```bash
curl -X POST https://gekkoterminal.ai/api/a2a?agent=gekko \
  -H "Content-Type: application/json" \
  -d '{
    "capability": "market_intelligence",
    "parameters": {
      "query": "USDC yield trends",
      "timeframe": "7d"
    }
  }'
```

**参数：**
- `query`（字符串，必填）：市场查询主题
- `timeframe`（字符串，可选）：`1h` | `24h` | `7d` | `30d`

### chat
用户可以就市场、投资策略、代币和收益等话题进行开放式交流，Gekko会回答任何与DeFi相关的问题。

**使用方法：**
```bash
curl -X POST https://gekkoterminal.ai/api/a2a?agent=gekko \
  -H "Content-Type: application/json" \
  -d '{
    "capability": "chat",
    "parameters": {
      "message": "What are the best yield opportunities on Base?"
    }
  }'
```

**参数：**
- `message`（字符串，必填）：您的问题或消息

## 智能合约（Base网络）

所有投资组合的配置都通过Base网络上的透明、经过审计的智能合约进行管理（合约ID：8453）。

### 投资组合合约列表
| 投资组合名称 | 合约地址 |
|---------|---------|
| Seamless USDC | `0x616a4E1db48e22028f6bbf20444Cd3b8e3273738` |
| Moonwell USDC | `0xc1256Ae5FFc1F2719D4937adb3bbCCab2E00A2Ca` |
| Spark USDC | `0x7bFA7C4f149E7415b73bdeDfe609237e29CBF34A` |
| Gauntlet USDC Prime | `0xe8EF4eC5672F09119b96Ab6fB59C27E1b7e44b61` |
| Yo USDC | `0x0000000f2eB9f69274678c76222B35eEc7588a65` |

### 可存入的代币
| 代币 | 合约地址 |
|---------|---------|
| USDC（Base网络） | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |

## 系统要求

- 必须安装Node.js 18及以上版本；
- 需要能够访问Base网络的RPC接口；
- API地址：`https://gekkoterminal.ai/api/a2a?agent=gekko`

## 安全性

所有投资组合相关的合约均为开源代码，已在链上验证，并接受第三方审计、正式验证以及漏洞奖励计划。实时监控机制确保了系统的透明度。

---

**由Gekko AI开发，基于ERC-8004标准运行。**