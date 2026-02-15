---
name: unifai-trading-suite
description: "由 AI 驱动的交易洞察套件：预测市场（Polymarket/Kalshi）以及由 UnifAI 提供支持的社会情绪信号。"
version: 1.0.0
homepage: https://github.com/zbruceli/trading
user-invocable: true
metadata: {"moltbot":{"emoji":"📈","requires":{"env":["UNIFAI_API_KEY","GOOGLE_API_KEY"]},"primaryEnv":"UNIFAI_API_KEY"}}
---

# UnifAI 交易套件

这是一个集成了 AI 驱动交易分析功能的综合性套件，能够整合预测市场数据和社会信号。

## 🛠️ 包含的工具

### 1. Prediction Trader
用于比较 Polymarket 和 Kalshi 平台上的预测概率。
```bash
python3 {baseDir}/skills/prediction-trader/scripts/trader.py analyze "bitcoin"
```

### 2. Kalshi Trader
提供受监管的美国经济指标数据（如美联储利率、CPI）。
```bash
python3 {baseDir}/skills/kalshi-trader/scripts/kalshi.py fed
```

### 3. Social Signals
通过 UnifAI 分析 KOL（关键意见领袖）的提及情况和市场情绪。
```bash
python3 {baseDir}/skills/social-signals/scripts/signals.py trending
```

## 🔐 设置要求
需要 `UNIFAI_API_KEY`（来自 unifAI）和 `GOOGLE_API_KEY`（用于数据分析）。

## 🚀 安装说明
```bash
clawdhub install unifai-trading-suite
```