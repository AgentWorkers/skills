---
name: market-environment-analysis
description: 这是一个全面的市场环境分析与报告工具。它能够分析全球市场，包括美国、欧洲和亚洲市场，以及外汇、商品和经济指标。该工具提供风险偏好/风险厌恶评估、行业分析和技术指标解读功能，并能根据诸如“市场分析”、“市场环境”、“全球市场”、“交易环境”、“市场状况”、“投资氛围”、“外汇分析”、“股市分析”等关键词触发相应的功能。
---

# 市场环境分析

这是一个全面的市场状况分析工具，可帮助您随时了解市场情况并生成专业的市场报告。

## 核心工作流程

### 1. 初始数据收集
使用 `web_search` 工具收集最新的市场数据：
- 主要股票指数（标准普尔500指数、纳斯达克指数、道琼斯指数、日经225指数、上证综合指数、恒生指数）
- 外汇汇率（美元/日元、欧元/美元、主要货币对）
- 商品价格（WTI原油、黄金、白银）
- 美国国债收益率（2年期、10年期、30年期）
- VIX指数（市场恐慌情绪指标）
- 市场交易状态（开盘/收盘/当前价格）

### 2. 市场环境评估
根据收集到的数据，评估以下方面：
- **趋势方向**：上升趋势/下降趋势/盘整
- **风险情绪**：风险偏好/风险规避
- **波动性状况**：通过 VIX 指数判断市场焦虑程度
- **行业资金流向**

### 3. 报告结构

#### 标准报告格式：
```
1. Executive Summary (3-5 key points)
2. Global Market Overview
   - US Markets
   - Asian Markets
   - European Markets
3. Forex & Commodities Trends
4. Key Events & Economic Indicators
5. Risk Factor Analysis
6. Investment Strategy Implications
```

## 脚本使用

### market_utils.py
提供用于报告制作的常用功能：
```bash
# Generate report header
python scripts/market_utils.py

# Available functions:
- format_market_report_header(): Create header
- get_market_session_times(): Check trading hours
- categorize_volatility(vix): Interpret VIX levels
- format_percentage_change(value): Format price changes
```

## 参考文档

### 主要指标解读（references/indicators.md）
在需要时参考以下内容：
- 各指数的关键水平
- 技术分析要点
- 各行业的重点关注领域

### 分析模式（references/analysis_patterns.md）
在进行分析时参考以下内容：
- 风险偏好/风险规避的标准
- 经济指标解读
- 市场间的相关性
- 季节性规律和市场异常现象

## 输出示例

### 快速总结版本
```
📊 Market Summary [2025/01/15 14:00]
━━━━━━━━━━━━━━━━━━━━━
【US】S&P 500: 5,123.45 (+0.45%)
【JP】Nikkei 225: 38,456.78 (-0.23%)
【FX】USD/JPY: 149.85 (↑0.15)
【VIX】16.2 (Normal range)

⚡ Key Events
- Japan GDP Flash
- US Employment Report

📈 Environment: Risk-On Continues
```

### 详细分析版本
首先提供执行摘要，然后详细分析每个部分：
- 当前市场阶段（牛市/熊市/中性）
- 短期走势（1-5天展望）
- 需要关注的风险事件
- 建议的持仓调整策略

## 重要注意事项

### 时区意识
- 考虑所有主要市场的时区差异：
  - 美国市场：晚上到凌晨（亚洲时间）
  - 欧洲市场：下午到晚上（亚洲时间）
  - 亚洲市场：早上到下午（当地时间）

### 经济日历的优先级
按重要性分类：
- ⭐⭐⭐ 关键事件（联邦公开市场委员会（FOMC）会议、非农就业数据（NFP）、消费者价格指数（CPI）等）
- ⭐⭐ 重要事件（国内生产总值（GDP）、零售销售数据等）
- ⭐ 参考性事件

### 数据来源的优先级
1. 官方发布的数据（中央银行、政府统计部门）
2. 主要财经媒体（彭博社、路透社）
3. 经纪商报告
4. 分析师的一致预测

## 故障排除

### 数据收集注意事项
- 查看市场节假日安排（节假日日历）
- 注意夏令时的变化
- 区分初步数据和最终数据

### 市场波动应对策略
1. 首先整理相关事实
2. 参考历史类似事件
3. 通过多个来源验证数据
4. 保持客观的分析态度

## 定制选项
根据用户的投资风格进行调整：
- **日内交易者**：关注盘中图表和订单流
- **波段交易者**：强调日/周级别的技术分析
- **长期投资者**：关注基本面和宏观经济
- **外汇交易者**：关注货币间的相关性及利率差异
- **期权交易者**：关注波动性分析及希腊字母（期权相关参数）