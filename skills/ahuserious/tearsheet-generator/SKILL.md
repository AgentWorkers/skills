---
name: tearsheet-generator
description: 使用 QuantStats 库生成包含自定义 SVG 可视化的专业数据报表。这些报表可用于生成包含平均绝对误差（MAE）分析的性能报告、利用相关建议以及生成交易列表。适用于分析策略表现或生成可视化报告的场景。
version: "1.1.0"
allowed-tools: Read, Write, Edit, Bash, Glob
---
# 报表生成器技能

## 关于

该技能使用 [QuantStats 库](https://github.com/ranaroussi/quantstats) 生成自定义报表。QuantStats 是一个用于投资组合分析的 Python 库。

**主要功能：**
- 自定义 SVG 可视化（回报、回撤率、月度热图）
- 专业的 HTML 报表
- MAE（最大不利偏差）分析
- 基于风险指标的杠杆率建议
- 可复制的策略配置

生成的交易策略报表包含以下内容：
- IBM Plex Mono 字体样式（QuantStats 格式）
- MAE（最大不利偏差）百分位分析（p90-p99）
- 最优杠杆率建议及止损水平
- 固定头寸（静态）与全仓头寸（动态）分析
- 10%、20%、30% 的清算缓冲区计算
- 完整的交易列表，包含入场/出场详情和 MAE 统计数据
- 可复制的策略配置文本框
- 多种杠杆率情景对比（1倍、10倍、15倍、20倍）

## 快速入门

```bash
# Generate tearsheet from trades CSV
/generate-tearsheet SOL_MTF_EMA_001 --trades ./trades.csv --capital 10000

# Verify backtest with Nautilus Trader
/verify-backtest SOL_MTF_EMA_001 --trades ./trades.csv

# Test optimal leverage configuration
/verify-mae-lev SOL_MTF_EMA_001 --leverage p95
```

## 命令

### /generate-tearsheet
生成包含所有分析部分的完整报表。

### /verify-backtest
将报表结果与 Nautilus Trader 进行对比，以验证准确性。

### /verify-mae-lev
使用基于 MAE 分析得出的最优杠杆率配置运行回测。

## 输出文件

每次生成报表时，会生成以下文件：
- `{strategy}_comparison.html` - 完整的 HTML 报表
- `{strategy}_comparison_metrics.json` - 用于程序访问的 JSON 统计数据

## 主要部分

### 1. 关键绩效指标
- B&H、Fix1x、Dyn1x、Fix10x、Dyn10x 列
- 累计回报、年化复合收益率（CAGR）、夏普比率（Sharpe Ratio）、索蒂诺比率（Sortino Ratio）、最大回撤率（Max DD）、卡尔马比率（Calmar Ratio）
- 交易过程中的风险指标及清算距离

### 2. MAE 分析与最优杠杆率
- MAE 分布表（最小值、平均值、p50、p75、p90-p99、最大值）
- 每个百分位的安全杠杆率建议
- 停损表（基于价格百分比，而非头寸成本）

### 3. 固定头寸（静态）分析
- 杠杆率表：5倍、10倍、15倍、20倍、25倍、30倍
- 列：清算价格百分比（Liq @ %Price）、建议止损（Rec. SL）、最大损失（Max Loss）、+10% 缓冲区、+20% 缓冲区、风险等级（Risk Level）

### 4. 全仓头寸（动态）分析
- 关于复合风险的警告
- 杠杆率表：1倍、2倍、3倍、5倍、10倍
- 每个杠杆率水平的建议

### 5. 缓冲区分析总结
- 最大 MAE 上方的 +10%、+20%、+30% 缓冲区
- 10倍、15倍、20倍杠杆率的安全性检查

### 6. 完整交易列表
- 所有交易的入场/出场时间、价格、方向、盈亏（PnL）、MAE、最大亏损幅度（MFE）、持续时间
- 带有固定标题的可滚动表格
- 总结行，显示各项平均值

### 7. 策略配置
- 原始配置文本框（可复制的 JSON 数据）
- 经 MAE 优化的配置文本框（可复制的 JSON 数据）
- 回测方法描述

## 依赖项

- Python 3.10+
- pandas、numpy、matplotlib
- backtesting.tearsheets 模块中的 StrategyComparisonTearsheet

## 安装

该技能使用的报表生成器位于：
`/Users/DanBot/Desktop/dev/Backtests/backtesting/tearsheets/strategy_comparison_tearsheet.py`

请确保此路径可访问，或相应地更新脚本路径。