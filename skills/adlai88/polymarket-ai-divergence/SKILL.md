---
name: polymarket-ai-divergence
displayName: Polymarket AI Divergence
description: 在某些公开市场上，Simmer的AI价格与Polymarket上的价格存在显著差异。这种价格差异可能预示着潜在的投资机会（即“alpha机会”）。当用户希望了解AI模型与市场预期的不一致之处、寻找交易机会，或者判断AI模型相对于外部价格的趋势（ bullish/bearish）时，可以使用这一功能。
metadata: {"clawdbot":{"emoji":"🔮","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false,"automaton":{"managed":true,"entrypoint":"ai_divergence.py"}}}
authors:
  - Simmer (@simmer_markets)
version: "1.0.4"
published: true
---
# Polymarket AI 价格分歧扫描器

该工具用于检测 Simmer 的 AI 驱动的价格与 Polymarket 的价格之间的分歧情况。

> **这只是一个模板。** 默认扫描结果显示 AI 与市场之间的价格分歧；您可以根据需要添加自己的过滤条件，将其与其他信号结合使用，或在此基础上构建自动化交易系统。该工具负责处理所有数据获取和价格分歧计算的工作，而具体的交易策略则由用户自行制定。

## 适用场景

当用户希望：
- 基于 AI 与市场的价格分歧寻找交易机会
- 扫描价格分歧较大的市场
- 了解 Simmer 的 AI 对市场持乐观/悲观态度的情况
- 分析 AI 与市场之间的价格差异时，可以使用该工具。

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
- 数据请求：`GET /api/sdk/markets`

## 配置参数

| 参数 | 环境变量 | 默认值 | 说明 |
|---------|---------------------|---------|-------------|
| API 密钥 | `SIMMER_API_KEY` | （必填） | 您的 Simmer SDK 密钥 |

## 工作原理

每个市场的数据包括：
- `current_probability`：受 Simmer AI 影响的价格
- `external_price_yes`：Polymarket 的实际价格
- `divergence`：两者之间的价格差异

当 AI 的预测与市场实际价格之间的差异较大时，可能存在较高的投资机会（即较高的 “alpha 值”）。

## 信号解读

| 价格分歧值 | 含义 | 应采取的行动 |
|------------|---------|--------|
| > +10% | AI 对市场持更乐观态度 | 考虑买入 |
| < -10% | AI 对市场持更悲观态度 | 考虑卖出 |
| ±5-10% | 价格分歧较小 | 继续观察 |
| < ±5% | 两者价格一致 | 无交易信号 |

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

**“AI 与 Polymarket 在哪些市场存在分歧？”**
→ `python ai_divergence.py`

**“有哪些看涨的投资机会？”**
→ `python ai_divergence.py --bullish --min 10`

**“AI 认为最具投资潜力的市场是哪个？”**
→ `python ai_divergence.py --opportunities`

## 常见问题解决方法

- **“SIMMER_API_KEY 未设置”**：请从 `simmer.markets/dashboard` 的 SDK 标签页获取 API 密钥。
- **“没有符合过滤条件的市场”**：降低 `--min` 阈值或移除方向性过滤条件。