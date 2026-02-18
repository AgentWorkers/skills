---
name: metrika-analysis
description: 该工具用于分析来自 Yandex.Metrika API 的数据。当用户请求分析网站流量、转化率、访客行为或网站报告时，该工具便会发挥作用。
metadata:
  openclaw:
    emoji: "📈"
---
# Metrika 分析

该机器人**不会发布数据**，**未经允许不会修改计数器**，并且会节约token。

## 使用场景
当用户有以下需求时，请使用此技能：
- 请求分析 Yandex.Metrika 数据
- 希望获取流量或转化率的报告
- 询问网站访问者的行为
- 寻找错误率（bounce rate）较高的页面

## 请求示例
- 分析 Yandex.Metrika 的数据
- 我的网站错误率（bounce rate）为什么这么高？
- 哪些流量来源的转化率更高？

## 操作步骤
1. 检查 METRIKA_TOKEN 和 COUNTER_ID 是否存在
2. 获取数据：
   - 使用 METRIKA_TOKEN 和 COUNTER_ID
   - 获取相关指标：访问次数、页面浏览深度、错误率、转化率
3. 分析数据：
   - 确定主要的流量来源及其转化情况
   - 找出错误率较高的页面
   - 识别转化流程中的薄弱环节
4. 提出建议：
   - 优化目标页面和内容
   - 改进错误率较高的页面
   - 提出提高转化率的初步方案