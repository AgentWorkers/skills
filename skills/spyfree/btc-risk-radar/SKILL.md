---
name: btc-risk-radar
description: 使用公开衍生品和现货数据（Deribit期权/永久合约 + Binance现货）来分析比特币市场风险。当用户需要比特币风险评估、恐慌/黑天鹅事件验证、期权价格偏斜度/隐含波动率（IV）解读，或者需要包含时间戳证据的结构化多头/空头风险快照时，可使用此方法。
---
# BTC风险雷达

根据公开数据生成可验证的BTC风险快照，然后提供简洁的分析结论。

## 工作流程

1. 运行 `scripts/btc_risk_radar.py` 以收集当前数据并计算相关指标。
2. 首先读取JSON格式的输出结果；将其视为最权威的数据来源。
3. 以明确的置信度和注意事项来解释分析结论。
4. 避免做出确定性预测；仅展示风险状态（绿色/琥珀色/红色）及其触发原因。

## 命令

```bash
python3 skills/btc-risk-radar/scripts/btc_risk_radar.py --json
python3 skills/btc-risk-radar/scripts/btc_risk_radar.py --prompt "用户问题"
python3 skills/btc-risk-radar/scripts/btc_risk_radar.py --lang en
python3 skills/btc-risk-radar/scripts/btc_risk_radar.py --lang zh
python3 skills/btc-risk-radar/scripts/btc_risk_radar.py --horizon-hours 72
python3 skills/btc-risk-radar/scripts/btc_risk_radar.py --event-mode high-alert
python3 skills/btc-risk-radar/scripts/btc_risk_radar.py --audience beginner --lang zh
```

## 输出策略

- 默认响应语言：英语。
- 如果用户使用中文提问（或提示中包含中文），则将最终答案转换为中文。
- 内部推理/分析部分可以使用英语。
- 必须包含以下内容：
  - 数据更新时间（`as_of_utc`）
  - 关键指标（ATM隐含波动率（ATM IV）、RR25、RR15、看跌期权成交量代理值（put-volume proxy）、资金流动情况（funding）、基差（basis）
  - 72小时验证结果（`validation_72h`）
  - 置信度（`confidence.score`、`confidence.level`）
  - 行动触发条件（`action_triggers`）
  - 数据来源说明及注意事项
- 面向不同受众的模式：
  - `pro`（默认）：简洁的交易/风险语言
  - `beginner`：用通俗语言解释指标含义
- 事件模式：
  - `normal`（默认）
  - `high-alert`：针对宏观事件或特殊情况的更敏感的阈值设置

## 解释规则

- `put_buy_share_proxy` 是基于看跌期权与看涨期权成交量比例计算得出的**代理值**，并非真实的交易流量。
- RR和ATM隐含波动率是根据到期时间最接近的期权计算得出的；这种方法较为稳健，但可能与某些专有数据平台的显示结果有所不同。
- 状态显示为红色（RED）表示下行风险增加，并不意味着市场一定会崩盘。

## 数据来源（公开数据）

- Deribit公开API：
  - `/public/get_instruments`
  - `/public/get_order_book`
  - `/public/get_book_summary_by_currency`
  - `/public/get_index_price`
  - `/public/get_book_summary_by_instrument`
- Coinbase公开API：
  - `/v2/prices/BTC-USD/spot`
- Binance公开API（可选）：
  - `/api/v3/ticker/price`
- OKX公开API：
  - `/api/v5/market/ticker`
  - `/api/v5/public/funding-rate`
- Bybit公开API：
  - `/v5/market/tickers`