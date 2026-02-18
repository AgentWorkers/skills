---
name: direct-analysis
description: Yandex.Direkt广告活动分析
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: ["curl"]
---# 直接分析

该机器人**不会发布数据**，**未经允许不会更改广告活动**，并且会节省令牌（tokens）。

## 使用场景
当用户询问以下内容时：
- 直接分析（direct analysis）
- 广告（advertising）
- 广告活动（advertising campaigns）
- 广告效果分析（advertising analysis）

用于评估广告活动的效果，包括点击率（CTR）、每次点击成本（CPC）、花费、转化率以及效果不佳的广告。

## 操作步骤
1. 获取广告活动的统计数据：
   - 使用 YANDEX_TOKEN 和 CLIENT_LOGIN
   - 计算点击率（CTR）、每次点击成本（CPC）以及花费
2. 分析效果不佳的广告和关键词
3. 提出简要建议：
   - 优化广告出价和预算
   - 修改广告文案和呼叫行动按钮（CTA）
   - 建议针对新的目标受众群体进行广告投放