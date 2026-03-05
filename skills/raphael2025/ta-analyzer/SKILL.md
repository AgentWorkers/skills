---
name: ta-analyzer
description: 使用 CCXT 进行多时间框架的技术分析。能够计算 20 多种指标，包括 RSI、MACD、布林带、一目均衡线、随机指标、威廉百分比指标（Williams %R）、ADX、MFI、CCI、斐波那契指标、支撑/阻力位，并能识别 10 多种图表形态。适用于用户需要技术分析、图表分析、指标数值、交易信号或价格预测的场景。
---
# TA Analyzer – 技术分析工具

这是一个功能强大的技术分析工具，能够实时获取市场数据并计算20多种技术指标。

## 主要功能

### 价格数据
- 通过CCXT从Binance获取OHLCV（开高、低、收盘价、成交量）数据
- 支持多种时间帧：15分钟、1小时、4小时、1天
- 支持多时间帧分析，以增强信号确认的准确性

### 技术指标

#### 趋势指标
- EMA（9日、21日、50日）
- SMA（20日、50日）
- MACD（12日、26日、9日）
- SuperTrend

#### 动量指标
- RSI（14日）
- Stochastic（14日、3周期、3线）
- Williams %R（14日）
- ADX（14日）
- MFI（14日）
- CCI（20日）

#### 波动性指标
- Bollinger Bands（20日、2倍标准差）
- ATR（14日）
- Keltner Channel
- Donchian Channel

#### 成交量指标
- OBV（On-Balance Volume）
- Volume SMA（成交量移动平均线）
- 成交量分析（判断市场健康状况或是否存在背离）

#### 支持/阻力位
- 自动检测局部高点/低点
- 标记附近的支撑/阻力位
- 计算最近的支撑/阻力水平

### 图表形态
- 单根K线形态
- Hammer（锤子形态）
- Shooting Star（流星形态）
- Doji（十字星形态）

- 多根K线形态
- Engulfing Pattern（吞没形态，牛市/熊市信号）
- Morning Star（晨星形态）
- Evening Star（晚星形态）
- Double Top/Bottom（双顶/双底）
- Head & Shoulders（头肩顶/肩顶/头肩底）
- Triangle（三角形形态，上升/下降/对称）
- Flag（旗形）

### 斐波那契与枢轴点
- 斐波那契回调率（0.236、0.382、0.5、0.618、0.786）
- 经典枢轴点（PP、R1-R3、S1-S3）
- VWAP（加权成交量平均价）

## 使用方法

```javascript
const { analyze } = require('./index.js');

// Analyze BTC on all timeframes
const result = await analyze('BTC/USDT');

// Analyze specific timeframe
const { analyzeTimeframe } = require('./index.js');
const result = await analyzeTimeframe('BTC/USDT', '1h', 100);
```

## 输出结果

该工具会返回以下综合分析内容：
- 当前价格及趋势
- 所有技术指标的数值
- 检测到的图表形态
- 买卖建议
- 止损和获利目标位

## 使用场景
- “分析BTC的价格走势”
- “ETH的RSI是多少？”
- “4小时时间框架内是否存在买入信号？”
- “当前的支撑位在哪里？”
- “我应该买入还是卖出？”

---

作者：Lucifer（路西法）
创建时间：2026-03-05
版本：1.0.0