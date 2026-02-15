---
name: polymarket-trader
description: 构建、评估并优化一个基于 Polymarket 的 BTC 1 小时涨跌交易策略，以 Binance 作为数据源。该策略可用于以下场景：  
1. 设计价格误判/套利模型（判断价格与公平概率之间的关系）；  
2. 添加交易规则过滤器（区分趋势行情与区间行情）；  
3. 调试来自 `events.jsonl` 或 `state.json` 的错误交易指令；  
4. 使用配套脚本进行快速离线分析或参数测试。
---

# Polymarket Trader

通过将决策基于 **Binance BTCUSDT**（数据来源）来维护一个盈利的 **1小时 BTC涨跌** 策略，并执行防止市场波动/风险的控制规则。

## 工作流程（请按此顺序操作）

1) **确认市场类型**
- 该策略专为 `bitcoin-up-or-down-*` 类型的1小时市场（Binance 1小时开盘价与收盘价）进行优化。

2) **计算锚定信号（来自Binance的数据）**
- 获取相关小时的1分钟收盘价以及1小时开盘价。
- 计算波动率（sigma）和到期时间。
- 将波动率转换为 **公平概率**，用于判断涨跌趋势。

3) **仅在存在可测量的优势时进行交易**
- 仅当 `fair_prob - market_price` 超过某个阈值时才入场。
- 设置方向性限制：当价格波动的绝对值（|z|）较大时，不要逆势交易。

4) **使用与入场方式相匹配的逻辑进行出场**
- 根据模型判断：在优势减弱或模型预测结果发生变化时出场；在信心极度强烈时持有至市场提前收盘。
- 对于基于均值回归的交易策略：在达到回归目标时出场，并设置严格的波动限制。

5) **通过日志验证交易行为**
- 对于所有疑似“不合理”的交易，必须提供以下解释：
  - 交易原因（`reason`）/ 交易方式（`entry_mode`）
  - 来自Binance的公平概率值（`fair_prob`）以及相关参数（`z`）
  - 是否触发了正确的出场条件。

## 所有脚本的打包方式

所有脚本均设计为可在 OpenClaw 工作空间中运行。

### 1) 获取Binance的K线数据
- `{baseDir}/scripts/binance_klines.py`
  - 从Binance获取K线数据并生成JSON格式的输出。

### 2) 计算市场稳定性指标
- `{baseDir}/scripts/binance_regime.py`
  - 计算5天/15天的收益率（ret5/ret15）以及市场稳定性指标（slope10），并生成一个简单的布尔值表示市场是否稳定。

### 3) 解释交易行为（events.jsonl文件）
- `{baseDir}/scripts/explain_fills.py`
  - 读取paperbot生成的 `events.jsonl` 文件，并为最近的交易行为生成一个简洁的表格：
    - 交易方向/结果/价格/交易原因
    - 估计的公平概率值（fair_up）以及相关参数（z）
    - 是否逆势交易（“against trend?” 标志）

## 参考资料

- `{baseDir}/references/strategy.md` — 包含数学模型、参数及调整指南。