---
name: biz-reporter
description: >
  自动化商业智能报告系统：该系统能够从 Google Analytics GA4、Google Search Console、Stripe 收入数据、社交媒体指标（Twitter/X、LinkedIn、Instagram）、HubSpot CRM 以及 Airtable 中提取数据，并将这些数据整理成格式化的每日关键绩效指标（KPI）报告、每周营销报告以及每月业务回顾报告。报告内容包含趋势分析及异常警报功能。该系统适用于以下场景：  
  - 商业报告编制  
  - KPI 仪表盘展示  
  - 每周数据监控  
  - 营销效果评估  
  - 收入汇总  
  - 流量分析  
  - 分析报告生成  
  - 绩效评估  
  - 数据可视化  
  - 增长指标分析  
  - 客户流失率分析  
  系统支持通过 Slack、电子邮件或 Markdown 文件的形式发送报告结果。此外，还可根据特定需求生成临时报告（如“我们的推广活动效果如何？”或“本月与上月的数据对比情况”）。
metadata:
  openclaw:
    emoji: "📊"
---
# Biz Reporter

这是一个能够自动生成商业智能报告的工具。它可以从多个数据源中提取数据，识别趋势，并根据需求或预定时间生成美观的报告。

## 为何需要这个工具

在ClawHub的3,286个功能中，与数据和分析相关的功能仅有18个，这是目前服务最不足的领域之一。然而，在OpenClaw社区中，自动化报告功能却被称为“最受用户欢迎的自动化工具”。每个企业都需要这样的工具，但目前还没有人能够真正将其开发得完善。

## 工作原理

Biz Reporter会连接到用户使用的业务工具，提取关键指标，进行趋势分析，然后生成格式化的报告。无论用户使用的是何种工具（从仅使用Google Analytics的单人创业者，到拥有完整数据栈的团队），Biz Reporter都能满足需求。

## 支持的数据源

### 网络分析
- **Google Analytics (GA4)**：会话数、用户数、页面浏览量、跳出率、热门页面、流量来源
- **Google Search Console**：展示量、点击次数、点击率、平均排名、热门搜索词
- 可通过`gog`工具、浏览器自动化脚本或API调用获取数据

### 收入与支付
- **Stripe**: 月收入（MRR）、收入总额、新客户数量、客户流失率、热门产品
- **PayPal**: 交易汇总信息
- 可通过CLI工具或配置好的API调用获取数据

### 社交媒体
- **Twitter/X**: 关注者数量、互动次数、热门帖子
- **LinkedIn**: 页面浏览量、帖子互动情况、关注者增长
- **Instagram**: 覆盖范围、互动次数、关注者数量
- 可通过API或浏览器自动化脚本获取数据

### 客户关系管理（CRM）与销售
- **HubSpot**: 潜在客户信息、销售线索价值、成交记录、联系人增长
- **Airtable**: 自定义数据库指标
- 可通过API（使用存储的访问密钥）获取数据

### 自定义数据源
- **任意API**: 用户可以指定自定义API接口以获取数据
- **CSV文件**: 如果用户以CSV格式导出数据，系统会解析并纳入报告
- **电子表格**: 可通过API获取Google Sheets的数据

## 报告类型

### 每日关键绩效指标（KPI）快照
快速查看业务状况——生成时间约2-3分钟，适用于每日晨会。

```
📊 Daily KPI Snapshot — [Date]

🌐 Website: [sessions] sessions ([+/-]% vs yesterday)
   Top page: [page] ([views] views)
   
💰 Revenue: $[amount] ([+/-]% vs yesterday)
   New customers: [count]
   
📱 Social: [total engagement] across platforms
   Best post: [platform] — [description] ([engagement])

⚡ Quick take: [One sentence AI analysis of the day]
```

### 每周营销报告
全面的营销绩效概览。

```
📈 Weekly Marketing Report — [Date Range]

EXECUTIVE SUMMARY
[2-3 sentence overview: what went well, what needs attention, key number]

WEBSITE PERFORMANCE
• Sessions: [number] ([%] vs last week)
• Unique visitors: [number]
• Top traffic sources: [source 1] ([%]), [source 2] ([%]), [source 3] ([%])
• Top 5 pages by traffic:
  1. [page] — [views] views
  2. ...
• Bounce rate: [%] ([trend])

SEARCH PERFORMANCE
• Impressions: [number] ([%] change)
• Clicks: [number] ([%] change)
• Average CTR: [%]
• Average position: [number]
• Top gaining queries: [query] (+[positions])
• Top losing queries: [query] (-[positions])

SOCIAL MEDIA
• Total followers: [number] (net +[growth])
• Total engagement: [number]
• Best performing post: [description]
• Platform breakdown:
  - Twitter/X: [followers], [engagement]
  - LinkedIn: [followers], [engagement]

REVENUE (if available)
• Total revenue: $[amount] ([%] vs last week)
• New customers: [count]
• Churn: [count] ([%])
• MRR: $[amount]

TRENDS & INSIGHTS
• [AI-generated insight about notable trends]
• [Comparison to historical averages]
• [Actionable recommendation]

NEXT WEEK FOCUS
• [Suggested action based on data]
```

### 每月业务回顾
包含历史数据对比和战略建议的深入分析。

报告格式与每周报告相同，但会扩展以下内容：
- 月度与去年同期对比
- 客户留存率的群体分析（如有数据）
- 内容效果分析（哪些文章吸引了流量）
- 营销漏斗分析：访问者 → 注册用户 → 客户转化过程（如可追踪）
- 包含具体行动建议的战略部分

### 定制报告
根据用户需求定制报告：
- “显示按收入贡献排名的前10个页面”
- “比较本月与上个月的社交互动情况”
- “哪些关键词的排名下降了？”

## 趋势检测

Biz Reporter不仅展示数字，还能发现数据中的模式：
1. **周环比异常**: 标记与前一周相比变化超过20%的指标
2. **下降趋势**: 如果某个指标连续多期下降，会特别突出显示
3. **相关性提示**: “来自Twitter的流量激增了40%——这可能与[日期]发布的病毒式帖子有关”
4. **季节性规律**: 如果历史数据存在规律性变化（例如周末流量下降），会予以说明而非发出警报
5. **对比基准**: 始终提供对比基准，以便数据有上下文

## 自然语言查询

用户可以以对话形式询问关于数据的问题：

| 用户问题 | 功能响应 |
|-----------|--------|
| “本周的流量情况如何？” | 提供包含周环比的快速网络分析总结 |
| “我们的月收入是多少？” | 获取Stripe数据并展示当前月收入及趋势 |
| “哪些博客文章的流量最高？” | 提供GA4统计的热门页面报告 |
- “本月我们的排名是上升还是下降？” | 提供Search Console的对比结果 |
- “生成我的每周报告” | 生成完整的每周营销报告 |
- “我们的产品发布情况如何？” | 提供指定时间范围内的相关数据 |
- “显示过去6个月的每月收入情况” | 提供历史收入图表 |

## 报告定时生成

帮助用户设置定期报告的触发机制（例如通过cron任务）：

```json
[
  {
    "name": "Daily KPI snapshot",
    "schedule": "0 8 * * 1-5",
    "prompt": "Generate daily KPI snapshot and send to Slack #metrics"
  },
  {
    "name": "Weekly marketing report",
    "schedule": "0 9 * * 1",
    "prompt": "Generate weekly marketing report for last week and send via email"
  },
  {
    "name": "Monthly business review",
    "schedule": "0 10 1 * *",
    "prompt": "Generate monthly business review for last month and post to Notion"
  }
]
```

## 设置与配置

首次使用时：
1. **了解可用数据源**: 检查用户可以访问哪些数据源（如GA4、Stripe等）
2. **身份验证**: 帮助用户配置每个数据源的API密钥或访问权限。密钥应安全存储在环境变量中，切勿保存在SKILL.md文件或内存中
3. **建立基准**: 提取初始数据以供后续对比使用
4. **个性化设置**: 询问用户报告的频率、发送渠道以及哪些指标最重要
5. **保存配置**: 将所有设置保存在工作区内存中

## 输出格式

报告可以以以下方式发送：
- **聊天消息**: 直接在聊天或消息渠道中显示格式化后的报告
- **Markdown文件**: 保存在工作区以供存档
- **Notion页面**: 如果用户使用Notion工具
- **电子邮件**: 通过配置好的电子邮件功能发送
- **Slack/Discord消息**: 发送到团队频道

## 特殊情况处理
- **数据不完整**: 如果某些数据源无法访问，使用现有数据生成报告，并注明缺失的部分
- **无历史数据**: 首次运行时仅显示当前数据快照。后续会提供对比数据
- **API请求限制**: 在同一会话内缓存数据并批量处理请求
- **流量为零/新网站**: 不显示“0访问者”的消极信息，而是重点展示设置进度和初步成果
- **多个网站/产品**: 询问用户具体关注哪个网站或产品，或生成合并报告
- **货币单位**: 根据用户设置显示正确的货币格式
- **隐私保护**: 报告中绝不包含个人用户数据或敏感信息，仅展示汇总数据