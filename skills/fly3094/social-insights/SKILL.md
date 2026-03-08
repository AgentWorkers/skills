---
name: social-insights
description: 社交媒体分析与性能追踪：监控用户互动情况、最佳发布时间、分析竞争对手数据，并生成可操作的报告。
author: fly3094
version: 1.0.0
tags: [analytics, social-media, twitter, linkedin, reporting, data, insights]
metadata:
  clawdbot:
    emoji: 📊
    requires:
      bins:
        - python3
        - curl
    config:
      env:
        TWITTER_API_KEY:
          description: Twitter API Key
          required: false
        TWITTER_API_SECRET:
          description: Twitter API Secret
          required: false
        LINKEDIN_ACCESS_TOKEN:
          description: LinkedIn Access Token
          required: false
        ANALYTICS_PLATFORMS:
          description: Platforms to analyze (twitter,linkedin,all)
          default: "twitter"
          required: false
---
# 社交媒体分析 📊

利用人工智能驱动的洞察力，跟踪、分析并优化您的社交媒体表现。

## 功能介绍

- 📈 **性能监控**：追踪粉丝数量、曝光次数、互动率
- ⏰ **最佳发布时间**：为您的目标受众找到最佳发布时机
- 🏆 **热门内容分析**：识别表现最佳的帖子
- 📊 **竞争对手对比**：与竞争对手进行基准测试
- 💡 **智能建议**：获得可操作的优化建议
- 📋 **自动报告**：每周/每月自动生成报告

## 安装

```bash
clawhub install social-analytics
```

## 命令

### 查看每周分析数据
```
Show my Twitter analytics for last week
```

### 查看月度报告
```
Generate social media report for last month
```

### 竞争对手分析
```
Compare my engagement with @competitor1 and @competitor2
```

### 最佳发布时间
```
When should I post for maximum engagement?
```

### 内容洞察
```
What type of content performs best for my audience?
```

### 趋势分析
```
Show my follower growth trend for the last 30 days
```

## 配置

### 环境变量

```bash
# Twitter API credentials (for Twitter analytics)
export TWITTER_API_KEY="your_key"
export TWITTER_API_SECRET="your_secret"
export TWITTER_ACCESS_TOKEN="your_token"
export TWITTER_ACCESS_TOKEN_SECRET="your_token_secret"

# LinkedIn API (optional)
export LINKEDIN_ACCESS_TOKEN="your_token"

# Platforms to analyze
export ANALYTICS_PLATFORMS="twitter"  # twitter, linkedin, or all
```

### 无API访问权限时

即使没有API访问权限，该工具仍可：
- 手动分析提供的数据
- 从导出的CSV文件生成报告
- 提供优化建议

## 输出示例

### 周报
```
📊 Social Media Weekly Report
Week of Mar 1-7, 2026

📈 Key Metrics:
• Followers: 1,234 (+56 this week)
• Impressions: 45,678 (+12%)
• Engagement Rate: 3.2% (industry avg: 1.8%)

🏆 Top Performing Posts:
1. "AI automation saves 20hrs/week" - 234 likes, 45 retweets
2. "New skill released!" - 189 likes, 32 retweets
3. "Client results showcase" - 156 likes, 28 retweets

⏰ Best Posting Times:
• Tuesday 10am-12pm
• Thursday 2pm-4pm
• Sunday 7pm-9pm

💡 Recommendations:
• Post more case studies (highest engagement)
• Increase posting frequency on Tuesdays
• Try video content (competitors seeing 2x engagement)
```

### 竞争对手对比
```
📊 Competitor Analysis Report

Your Account vs Competitors (Last 30 Days)

Metric          You      Comp1    Comp2    Industry Avg
-----------------------------------------------------------------
Engagement Rate 3.2%     2.8%     4.1%     1.8%
Posts/Week      5        7        3        4
Avg Likes       156      134      289      95
Avg Retweets    23       18       45       12
Follower Growth +4.5%    +2.1%    +6.8%    +1.5%

💡 Insights:
• Your engagement rate is 78% above industry average! Great job!
• Comp2 gets more engagement with video content
• You post less frequently than competitors
• Opportunity: Increase posting to 7/week

🎯 Action Items:
1. Add 2 video posts this week
2. Test posting on Wednesday mornings
3. Analyze Comp2's top posts for content ideas
```

### 最佳发布时间
```
⏰ Optimal Posting Times for Your Audience

Based on your last 100 posts:

🥇 Best: Tuesday 10:00-12:00
   Avg Engagement: 4.2%
   Avg Reach: 12,500

🥈 Second: Thursday 14:00-16:00
   Avg Engagement: 3.8%
   Avg Reach: 11,200

🥉 Third: Sunday 19:00-21:00
   Avg Engagement: 3.5%
   Avg Reach: 9,800

❌ Worst: Monday 6:00-8:00
   Avg Engagement: 1.2%
   Avg Reach: 3,200

💡 Recommendation:
Schedule 60% of posts during top 3 time slots for maximum impact.
```

## 与其他工具的集成

### rss-to-social
```
rss-to-social publishes content → social-analytics tracks performance
→ Optimize RSS sources based on engagement
```

### social-media-automator
```
social-media-automator generates posts → social-analytics measures results
→ Improve content generation based on data
```

### seo-content-pro
```
seo-content-pro creates articles → social-analytics tracks social shares
→ Identify topics that resonate with audience
```

实现完全数据驱动的内容循环！🔄

## 使用场景

### 内容营销人员
- 跟踪营销活动的效果
- 向利益相关者证明投资回报率（ROI）
- 优化内容发布计划

### 独立创业者
- 了解受众偏好
- 最大化有限的发布时间
- 与大型账号竞争

### 机构
- 客户报告自动化
- 多账号管理
- 跨行业进行基准测试

### 社交媒体管理者
- 基于数据的策略决策
- 识别热门内容类型
- 为预算增加提供依据

## 价格方案

该工具为LobsterLabs的分析服务提供支持：

| 服务 | 价格 | 交付方式 |
|---------|-------|----------|
| 单次分析 | $99 | 一次性报告 |
| 月度订阅 | $299/月 | 每周报告 + 洞察数据 |
| 竞争对手跟踪 | $199/月 | 最多支持5个竞争对手 |
| 企业版（10个账号） | $999/月 | 定制仪表盘 |

**套餐折扣**：
- 内容自动化 + 分析：节省20%
- 年度订阅：节省15%

联系方式：PayPal 492227637@qq.com

## 优化使用效果的技巧

1. **连接API**：完整的数据分析需要API凭证
2. **持续监控**：每周进行数据分析以获取趋势洞察
3. **对比竞争对手**：与3-5个类似账号进行基准测试
4. **立即行动**：在48小时内实施建议
5. **跟踪变化**：在策略调整前后监控各项指标

## 故障排除

### 无API访问权限
- 使用平台提供的手动数据导出功能
- 上传CSV文件进行分析
- 该工具仍可使用提供的数据进行工作

### 数据不完整
- 确认API凭证是否正确
- 检查API的请求频率限制
- 确保账号设置为公开状态（某些平台要求）

### 分析速度慢
- 大范围的时间段分析耗时较长
- 可缩小时间范围至最近7-30天以获得更快结果
- 尽量在非高峰时段进行分析

## 更新日志

### 1.0.0 (2026-03-07)
- 初始版本发布
- 支持Twitter数据分析
- 增加竞争对手对比功能
- 引入最佳发布时间分析
- 提供人工智能驱动的建议
- 实现自动化的每周/每月报告功能