---
name: pipeline-analytics
description: 根据CRM数据生成交互式分析仪表板。当需要执行以下操作时，可以使用该功能：展示销售流程统计数据、创建报告、分析潜在客户信息、显示转化率、构建仪表板、可视化外展数据、进行漏斗分析，或处理来自DuckDB工作区数据的任何数据可视化请求。
metadata: { "openclaw": { "emoji": "📊" } }
---
# 管道分析 — 自然语言 → SQL → 交互式图表

将自然语言问题转换为DuckDB查询，并将结果以交互式Recharts仪表板的形式直接显示在聊天界面中。

## 工作流程

```
User asks question in plain English
→ Translate to DuckDB SQL against workspace pivot views (v_*)
→ Execute query
→ Format results as report-json
→ Render as interactive Recharts components
```

## DuckDB查询模式

### 数据探索 — 存在哪些对象？
```sql
-- List all objects and their entry counts
SELECT o.name, o.display_name, COUNT(e.id) as entries
FROM objects o
LEFT JOIN entries e ON e.object_id = o.id
GROUP BY o.name, o.display_name
ORDER BY entries DESC;

-- List fields for an object
SELECT f.name, f.field_type, f.display_name
FROM fields f
JOIN objects o ON f.object_id = o.id
WHERE o.name = 'leads'
ORDER BY f.position;

-- Available pivot views
SELECT table_name FROM information_schema.tables
WHERE table_name LIKE 'v_%';
```

### 常见分析查询

#### 管道转化流程
```sql
SELECT "Status", COUNT(*) as count
FROM v_leads
GROUP BY "Status"
ORDER BY CASE "Status"
  WHEN 'New' THEN 1
  WHEN 'Contacted' THEN 2
  WHEN 'Qualified' THEN 3
  WHEN 'Demo Scheduled' THEN 4
  WHEN 'Proposal' THEN 5
  WHEN 'Closed Won' THEN 6
  WHEN 'Closed Lost' THEN 7
  ELSE 99
END;
```

#### 随时间变化的推广活动
```sql
SELECT DATE_TRUNC('week', "Last Outreach"::DATE) as week,
       "Outreach Channel",
       COUNT(*) as messages_sent
FROM v_leads
WHERE "Last Outreach" IS NOT NULL
GROUP BY week, "Outreach Channel"
ORDER BY week;
```

#### 源头对应的转化率
```sql
SELECT "Source",
       COUNT(*) as total,
       COUNT(*) FILTER (WHERE "Status" = 'Qualified') as qualified,
       COUNT(*) FILTER (WHERE "Status" IN ('Closed Won', 'Converted')) as converted,
       ROUND(100.0 * COUNT(*) FILTER (WHERE "Status" = 'Qualified') / COUNT(*), 1) as qual_rate,
       ROUND(100.0 * COUNT(*) FILTER (WHERE "Status" IN ('Closed Won', 'Converted')) / COUNT(*), 1) as conv_rate
FROM v_leads
GROUP BY "Source"
ORDER BY total DESC;
```

#### 回复率分析
```sql
SELECT "Outreach Channel",
       COUNT(*) as sent,
       COUNT(*) FILTER (WHERE "Reply Received" = true) as replied,
       ROUND(100.0 * COUNT(*) FILTER (WHERE "Reply Received" = true) / COUNT(*), 1) as reply_rate
FROM v_leads
WHERE "Outreach Status" IS NOT NULL
GROUP BY "Outreach Channel";
```

#### 转化所需时间
```sql
SELECT "Source",
       AVG(DATEDIFF('day', created_at, "Converted At"::DATE)) as avg_days_to_convert,
       MEDIAN(DATEDIFF('day', created_at, "Converted At"::DATE)) as median_days
FROM v_leads
WHERE "Status" = 'Converted' AND "Converted At" IS NOT NULL
GROUP BY "Source";
```

## Report-JSON格式

生成兼容Recharts的报告卡片：

```json
{
  "type": "report",
  "title": "Pipeline Analytics — February 2026",
  "generated_at": "2026-02-17T14:30:00Z",
  "panels": [
    {
      "title": "Pipeline Funnel",
      "type": "funnel",
      "data": [
        {"name": "New Leads", "value": 200},
        {"name": "Contacted", "value": 145},
        {"name": "Qualified", "value": 67},
        {"name": "Demo Scheduled", "value": 31},
        {"name": "Closed Won", "value": 13}
      ]
    },
    {
      "title": "Outreach Activity",
      "type": "area",
      "xKey": "week",
      "series": [
        {"key": "linkedin", "name": "LinkedIn", "color": "#0A66C2"},
        {"key": "email", "name": "Email", "color": "#EA4335"}
      ],
      "data": [
        {"week": "Feb 3", "linkedin": 25, "email": 40},
        {"week": "Feb 10", "linkedin": 30, "email": 35}
      ]
    },
    {
      "title": "Lead Source Breakdown",
      "type": "donut",
      "data": [
        {"name": "LinkedIn Scrape", "value": 95, "color": "#0A66C2"},
        {"name": "YC Directory", "value": 45, "color": "#FF6600"},
        {"name": "Referral", "value": 30, "color": "#10B981"},
        {"name": "Inbound", "value": 20, "color": "#8B5CF6"}
      ]
    },
    {
      "title": "Reply Rates by Channel",
      "type": "bar",
      "xKey": "channel",
      "series": [{"key": "rate", "name": "Reply Rate %", "color": "#3B82F6"}],
      "data": [
        {"channel": "LinkedIn", "rate": 32},
        {"channel": "Email", "rate": 18},
        {"channel": "Multi-Channel", "rate": 41}
      ]
    }
  ]
}
```

## 可用的图表类型

| 类型 | 使用场景 | Recharts组件 |
|------|----------|-------------------|
| `bar` | 对比分析、分类统计 | BarChart |
| `line` | 随时间变化的趋势 | LineChart |
| `area` | 随时间变化的量值 | AreaChart |
| `pie` | 单层分布 | PieChart |
| `donut` | 带有中心指标的分布 | PieChart (innerRadius) |
| `funnel` | 转化阶段进度 | FunnelChart |
| `scatter` | 两个变量之间的相关性 | ScatterChart |
| `radar` | 多维度对比 | RadarChart |

## 预建的报告模板

### 1. 管道概览
- Funnel：潜在客户 → 被联系 → 符合条件 → 进行演示 → 完成转化
- Donut：潜在客户来源分布
- 数字卡片：潜在客户总数、转化率、平均交易金额

### 2. 推广活动绩效
- Area：按渠道划分的发送消息数量
- Bar：按渠道划分的回复率
- Line：每周的转化趋势
- 数字卡片：发送总数、回复率、预约会议数量

### 3. 推广人员绩效（多用户环境）
- Bar：每位推广人员联系的潜在客户数量
- Bar：每位推广人员的回复率
- Bar：每位推广人员的转化数量
- Scatter：活动量与转化率的关系

### 4. 组群分析
- 热图样式：按注册周和时间划分的转化率
- Line：不同组群的留存/参与度曲线

## 自然语言与SQL的映射关系

| 用户输入 | SQL查询模式 | 图表类型 |
|-----------|-------------|------------|
| “显示管道转化情况” | GROUP BY Status | funnel |
| “推广活动统计” | COUNT by channel + status | bar + area |
| “转化情况如何” | conversion rates | funnel + line |
| “比较不同来源的转化效果” | GROUP BY Source | bar |
| “每周趋势” | DATE_TRUNC + GROUP BY | line / area |
| “谁回复了” | FILTER Reply Received | table |
| “表现最好的推广人员” | ORDER BY conversion DESC | bar |
| “潜在客户来源分析” | GROUP BY any dimension | pie / donut |

## 保存报告

报告可以保存为`.report.json`文件，存储在工作区中：
```
~/.openclaw/workspace/reports/
  pipeline-overview.report.json
  weekly-outreach.report.json
  monthly-review.report.json
```

这些报告文件在打开Ironclaw网页界面时可以显示为实时仪表板。

## Cron任务集成

自动生成每周/每月的报告：
```json
{
  "name": "Weekly Pipeline Report",
  "schedule": { "kind": "cron", "expr": "0 9 * * MON", "tz": "America/Denver" },
  "payload": {
    "kind": "agentTurn",
    "message": "Generate weekly pipeline analytics report. Query DuckDB for this week's data. Create report-json with: funnel, outreach activity (area), reply rates (bar), source breakdown (donut). Save to workspace/reports/ and announce summary."
  }
}
```