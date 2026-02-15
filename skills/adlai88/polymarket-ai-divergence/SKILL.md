---
name: polymarket-ai-divergence
displayName: Polymarket AI Divergence
description: 在某些公开市场上，Simmer的AI价格与Polymarket上的价格存在显著差异。这种价格差异可能意味着存在投资机会（即“alpha机会”）。当用户希望发现AI模型与市场预期的不一致之处、寻找交易机会，或者了解AI模型相对于外部价格的走势（ bullish/bearish）时，可以使用这一工具。
metadata: {"clawdbot":{"emoji":"🔮","requires":{"env":["SIMMER_API_KEY"]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
version: "1.0.3"
published: true
---

# Polymarket AI 价格分歧扫描器

该工具用于识别 Simmer 的 AI 预测价格与 Polymarket 实际价格之间存在分歧的市场。

## 适用场景

当用户希望：
- 基于 AI 预测与市场实际价格之间的分歧寻找交易机会
- 扫描价格分歧较大的市场
- 了解 Simmer 的 AI 对市场走势的看涨/看跌判断
- 分析 AI 预测与市场价格之间的差异时，可以使用此工具。

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

**API 参考：**
- 基本 URL：`https://api.simmer.markets`
- 认证方式：`Authorization: Bearer $SIMMER_API_KEY`
- 获取市场数据：`GET /api/sdk/markets`

## 配置参数

| 参数 | 环境变量 | 默认值 | 说明 |
|---------|---------------------|---------|-------------|
| API 密钥 | `SIMMER_API_KEY` | （必填） | 你的 Simmer SDK 密钥 |
| API 地址 | `SIMMER_API_URL` | `https://api.simmer.markets` | API 的基础地址 |

## 工作原理

每个市场的数据包括：
- `current_probability`：受 Simmer AI 影响的价格
- `external_price_yes`：Polymarket 的实际价格
- `divergence`：两者之间的价格差异

当 AI 的预测价格与 Polymarket 的实际价格差异较大时，可能存在较高的投资机会（即“alpha”效应）。

## 信号解读

| 价格差异 | 含义 | 应对策略 |
|------------|---------|--------|
| > +10% | AI 更看涨 | 考虑买入 |
| < -10% | AI 更看跌 | 考虑卖出 |
| ±5-10% | 价格差异较小 | 继续观察 |
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

## 使用示例

**“AI 在哪些市场与 Polymarket 的预测存在分歧？”**
→ `python ai_divergence.py`

**“有哪些看涨的交易机会？”**
→ `python ai_divergence.py --bullish --min 10`

**“AI 认为最具投资潜力的市场是哪个？”**
→ `python ai_divergence.py --opportunities`

## 常见问题及解决方法

**“SIMMER_API_KEY 未设置”**
- 请从 simmer.markets/dashboard 的 SDK 标签页获取 API 密钥。

**“没有符合筛选条件的市场”**
- 降低 `--min` 阈值或移除方向性筛选条件。