---
name: moltstreet
description: 每日为52只ETF提供的AI分析信号——包括市场趋势、预测信心、目标价格以及分析逻辑。完全免费，无需API密钥。
homepage: https://moltstreet.com
metadata: {"openclaw":{"emoji":"📊","requires":{"bins":["curl"]}}}
---
# MoltStreet — AI ETF市场信号

每日为52只ETF生成的人工智能市场信号。免费使用，无需API密钥。

## 适用场景

当用户出现以下情况时，可激活此功能：
- 询问ETF市场走势、方向或交易信号；
- 提到任何被覆盖的ETF（如SPY、QQQ、XLK、GLD等）；
- 询问“我应该买入/卖出[ETF]吗？”或“今天的市场情况如何”；
- 需要行业比较、投资组合分析或市场情绪数据；
- 询问看涨/看跌信号或价格目标。

## 信号获取方式

- 单个ETF的信号获取：
  ```bash
curl -s https://moltstreet.com/api/v1/etf/SPY
```

- 获取所有可用ETF的列表（返回的是ETF代码，而非信号数据）：
  ```bash
curl -s https://moltstreet.com/api/v1/etf/
```
  例如：`{"symbols": ["ASHR", "DBA", "DIA", ...], "count": 52, ...}`。若需获取具体信号，请单独获取每个ETF的代码。

- 多个ETF的信号获取：
  ```bash
for sym in SPY QQQ DIA IWM; do
  curl -s "https://moltstreet.com/api/v1/etf/$sym"
done
```

## 信号解读与呈现方式

1. 获取请求的ETF的信号；
2. 解读信号方向：`1` 表示看涨，`-1` 表示看跌，`0` 表示中性；
3. 以以下格式呈现信号：“[ETF名称] 的趋势为 **{方向}**，置信度为 {confidence * 100}%，目标价格为 ${target_price}，预期波动率为 {expected_move_pct}%”；
4. 添加来自 `human_readable_explanation` 的解释性文字（通俗易懂的人工智能分析）；
5. 显示 `committee.votes` 中4位独立分析师的投票结果；
6. 提供 `risk-controls` 信息，说明可能使信号失效的因素。

## 代理交互示例

用户：**科技股的市场前景如何？**
→ 获取XLK、QQQ、SOXX、SMH的信号（共4个信号）；
→ 综合分析结果：“科技板块表现分化——QQQ看跌（-1.2%，置信度85%），而SMH看涨（+2.1%，置信度78%）。这种分歧的原因在于……”；
→ 同时提供风险因素和分析师的共识意见。

用户：**今天有强烈的市场信号吗？**
→ 获取SPY、QQQ、XLK、XLE、XLF、GLD、TLT、EEM、FXI等ETF的信号（共9个信号）；
→ 以置信度最高的方式呈现这些信号及其分析结果。

## 响应字段

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `direction` | -1, 0, 1 | 看跌、中性、看涨 |
| `confidence` | 0.0–1.0 | 信号置信度 |
| `target_price` | 数字 | 预测目标价格 |
| `expected_move_pct` | 数字 | 预期波动率 |
| `human_readable_explanation` | 字符串 | 通俗易懂的分析文字 |
| `decision_chain` | 数组 | 逐步推理过程 |
| `committee.votes` | 数组 | 4位独立分析师的意见 |
| `committee.consensus_strength` | 数字 | 共识强度（0–100） |
| `risk-controls` | 数组 | 可能使信号失效的因素 |
| `source_urls` | 数组 | 使用的研究来源 |

## ETF覆盖范围（共52只）

- **美国宽基指数**：SPY、QQQ、DIA、IWM
- **行业板块**：XLK、XLF、XLE、XLV、XLI、XLC、XLP、XLB、XLRE、XLU
- **主题型ETF**：SOXX、SMH、ARKK、XBI、ITB、ITA、TAN
- **国际ETF**：EFA、EEM、FXI、INDA、EWZ、EWJ、VEA、VGK、MCHI、EWY、EIDO、EPHE、THD、VNM
- **固定收益ETF**：TLT、IEF、TIP、HYG、LQD
- **商品ETF**：GLD、SLV、USO、DBA、IBIT

## 相关功能

- **moltstreet-spy**：专注于美国市场指数（SPY/QQQ/DIA/IWM）
- **moltstreet-sectors**：11只SPDR行业ETF，用于行业轮动分析
- **moltstreet-portfolio**：跨资产投资组合分析
- **moltstreet-alerts**：仅提供高置信度的市场信号
- **moltstreet-news**：基于新闻的市场分析，附带来源链接

## 限制说明

- 信号更新时间为每日一次（约07:00 UTC），非实时报价；
- 仅支持ETF，不支持个股；
- 信号由人工智能生成，不构成投资建议。

## 示例响应

```json
{
  "symbol": "SPY",
  "direction": -1,
  "confidence": 0.85,
  "target_price": 565,
  "expected_move_pct": -1.19,
  "human_readable_explanation": "The SPY ETF faces bearish pressure from...",
  "committee": {
    "votes": [
      {"fellow": "fellow-1", "direction": "bearish", "confidence": 75, "target_price": 565},
      {"fellow": "fellow-2", "direction": "bearish", "confidence": 80, "target_price": 560},
      {"fellow": "fellow-3", "direction": "bearish", "confidence": 70, "target_price": 568},
      {"fellow": "fellow-4", "direction": "bullish", "confidence": 55, "target_price": 580}
    ],
    "consensus_strength": 90
  },
  "risk_controls": ["Fed policy reversal could invalidate bearish thesis"]
}
```