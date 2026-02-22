---
metadata:
  name: CatalystWatch
  description: Monitor and analyze market-moving catalysts including earnings, FDA decisions, economic data releases, and corporate events
  version: 0.0.2
  tags: [finance, trading, catalysts, earnings, market-events]
  openclaw:
    requires:
      env: [CATALYSTWATCH_API_KEY]
    primaryEnv: CATALYSTWATCH_API_KEY
---

# CatalystWatch

监控并分析影响股票及其他金融工具市场走势的催化剂事件。

## 功能介绍

CatalystWatch 会追踪可能引发股价波动的即将发生或已经发生的催化剂事件，包括：

- **财报报告**：预定的发布日期、市场共识预测、非官方传闻数据以及历史上的业绩超预期/低于预期的情况
- **FDA（美国食品药品监督管理局）的决策**：产品批准日期、咨询委员会会议结果以及审批/拒绝的决定
- **经济数据**：就业报告、CPI（消费者价格指数）/PPI（生产者价格指数）、联邦公开市场委员会（FOMC）会议以及其他宏观经济数据发布
- **公司事件**：并购公告、业务分拆、股票回购、内幕交易以及投资者维权活动
- **行业相关事件**：行业会议、监管政策变化以及大宗商品供应中断

## 使用方法

您可以要求您的代理监控特定股票代码、行业或关注列表中的催化剂事件：

- “本月苹果公司（AAPL）有哪些即将发布的财报报告？”
- “显示本季度所有生物科技股票的 FDA 决策日期”
- “当我的关注列表中的任何股票业绩超出预期（超出 10%）时，向我发送警报”
- “总结今天的宏观经济事件及其对市场的影响”

## 配置设置

请设置以下环境变量以访问数据源：

- `CATALYSTWATCH_API_KEY`：CatalystWatch 的 API 密钥，用于验证获取财报日历、FDA 事件日期、宏观经济数据发布计划以及公司动态数据的请求
- `CATALYSTWATCH_watchLIST`：（可选）需要监控的股票代码列表，用逗号分隔（例如：`AAPL,TSLA,NVDA`）