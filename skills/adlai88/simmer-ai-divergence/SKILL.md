---
name: simmer-ai-divergence
displayName: Polymarket AI Divergence
description: 在某些公开市场上，Simmer 的 AI 价格与 Polymarket 上的价格存在显著差异。这种价格差异可能意味着存在投资机会（即所谓的 “alpha 机会”）。当用户希望发现 AI 技术与市场观点之间的分歧、寻找交易机会，或者了解 AI 对外部价格的看法（是看涨还是看跌）时，可以使用这一信息。
metadata: {"clawdbot":{"emoji":"🔮","requires":{"env":["SIMMER_API_KEY"]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
version: "1.0.2"
---

# Polymarket AI价格分歧扫描器

该工具用于识别Simmer的AI预测价格与Polymarket实际价格之间存在分歧的表面市场。

## 适用场景

当用户希望：
- 基于AI预测与市场实际表现的差异寻找交易机会
- 扫描价格分歧较大的市场
- 了解Simmer的AI预测是看涨还是看跌
- 分析AI预测与市场价格的差异时，可以使用此工具。

## 快速命令

```bash
# Show all divergences (>5% default)
python ai_divergence.py

# Quick status
python scripts/status.py

# Only high-divergence (>15%)
python ai_divergence.py --min 15

# Bullish only (AI > Polymarket)
python ai_divergence.py --bullish

# Bearish only (AI < Polymarket)
python ai_divergence.py --bearish

# Top opportunities summary
python ai_divergence.py --opportunities

# JSON output
python ai_divergence.py --json
```

**API参考：**
- 基础URL：`https://api.simmer.markets`
- 认证方式：`Authorization: Bearer $SIMMER_API_KEY`
- 市场数据请求：`GET /api/sdk/markets`

## 配置参数

| 参数 | 环境变量 | 默认值 | 说明 |
|---------|---------------------|---------|-------------|
| API密钥 | `SIMMER_API_KEY` | （必填） | 你的Simmer SDK密钥 |
| API地址 | `SIMMER_API_URL` | `https://api.simmer.markets` | API基础URL |

## 工作原理

每个市场的数据包括：
- `current_probability`：受Simmer AI影响的价格
- `external_price_yes`：Polymarket的实际价格
- `divergence`：Simmer预测价格与Polymarket实际价格之间的差异

当AI预测的价格与实际价格之间的差异较大时，可能存在较高的投资机会（即“alpha收益”）。

## 信号解读

| 分歧程度 | 含义 | 应对策略 |
|------------|---------|--------|
| > +10% | AI预测看涨 | 考虑买入 |
| < -10% | AI预测看跌 | 考虑卖出 |
| ±5-10% | 分歧较小 | 继续观察 |
| < ±5% | 预测与市场一致 | 无交易信号 |

## 示例输出

```
🔮 AI Divergence Scanner
===========================================================================
Market                                     Simmer     Poly      Div   Signal
---------------------------------------------------------------------------
Will bitcoin hit $1m before GTA VI?        14.2%   48.5%  -34.3%   🔴 SELL
What will be the top AI model this mon     17.9%    1.0%  +16.9%    🟢 BUY

💡 Top Opportunities (>10% divergence)
===========================================================================
📌 Will bitcoin hit $1m before GTA VI?
   AI says BUY NO (AI: 14% vs Market: 48%)
   Divergence: -34.3% | Resolves: 2026-07-31
```

## 示例用法

**“AI在哪些市场与Polymarket的预测存在分歧？”**
→ `python ai_divergence.py`

**“有哪些看涨的投资机会？”**
→ `python ai_divergence.py --bullish --min 10`

**“AI预测中最有信心的投资策略是什么？”**
→ `python ai_divergence.py --opportunities`

## 常见问题及解决方法

**“SIMMER_API_KEY未设置”**
→ 请从simmer.markets/dashboard的SDK设置中获取API密钥。

**“没有符合筛选条件的市场”**
→ 降低`--min`阈值或取消方向性筛选条件。