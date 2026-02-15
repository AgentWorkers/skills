---
name: synth-data
description: 从 Synthdata.co 查询加密货币、商品和股票的波动性预测数据。可以对这些资产进行比较，运行蒙特卡洛模拟，并生成图表。
---

# Synthdata波动性分析技能

查询并分析来自Synthdata.co的加密货币、商品和股票指数的波动性预测。

## 设置

设置您的API密钥：
```bash
export SYNTHDATA_API_KEY=your_key_here
```

## 快速入门

```bash
# Single asset
python3 scripts/synth.py BTC

# Multiple assets comparison
python3 scripts/synth.py BTC ETH SOL --compare

# All assets overview
python3 scripts/synth.py --all

# Monte Carlo simulation (24h max)
python3 scripts/synth.py BTC --simulate --hours 12

# Generate chart
python3 scripts/synth.py --all --chart
```

## 可用资产

| 代码 | 名称 | 类别 |
|------|------|---------|
| BTC | 比特币 | 加密货币 |
| ETH | 以太坊 | 加密货币 |
| SOL | Solana | 加密货币 |
| XAU | 黄金 | 商品 |
| SPYX | 标普500指数 | 指数 |
| NVDAX | NVIDIA股票 | 股票 |
| GOOGLX | 谷歌股票 | 股票 |
| TSLAX | 特斯拉股票 | 股票 |
| AAPLX | 苹果股票 | 股票 |

## 输出示例

```
==================================================
  BTC — Bitcoin
==================================================
  Price:           $77,966
  24h Change:      🔴 -0.95%
  Current Vol:     58.4% 🟠 [Elevated]
  Avg Realized:    53.3%
  Forecast Vol:    52.2%
```

## 波动性等级

| 等级 | 范围 | 表情符号 |
|------|------|---------|
| 低 | < 20% | 🟢 |
| 中等 | 20-40% | 🟡 |
| 高 | 40-60% | 🟠 |
| 非常高 | 60-80% | 🔴 |
| 极高 | > 80% | 🔴 |

## 使用场景

### 1. 市场概览
```bash
python3 scripts/synth.py --all
```
获取按波动性排名的所有资产列表。

### 2. 交易信号
- **预测波动性高 → 当前波动性低**：预期波动性将上升
- **预测波动性低 → 当前波动性高**：波动性可能下降
- 用于调整持仓规模和期权交易

### 3. 蒙特卡洛预测
```bash
python3 scripts/synth.py BTC --simulate --hours 24 --paths 1000 --chart
```
使用预测的波动性生成价格区间（最大24小时范围，基于Synthdata的预测数据）。

### 4. 定时报告
创建定时任务，每日通过Slack/Telegram发送预测结果（详见examples/use-cases.md）。

### 5. 风险警报
监控资产波动性是否超过阈值，并触发通知。

## API参考

请参阅`references/api.md`以获取完整的API文档。

## 直接使用API

```python
import requests

resp = requests.get(
    "https://api.synthdata.co/insights/volatility",
    params={"asset": "BTC"},
    headers={"Authorization": f"Apikey {API_KEY}"}
)
data = resp.json()

# Key fields:
price = data["current_price"]
realized_vol = data["realized"]["average_volatility"]
forecast_vol = data["forecast_future"]["average_volatility"]
```

## 集成建议

- **Polymarket**：利用波动性预测来指导市场方向的投注
- **期权交易**：预测波动性高时考虑买入期权
- **投资组合管理**：当整体波动性突然上升时重新平衡投资组合
- **警报系统**：当预测结果与实际波动性差异较大时发送通知