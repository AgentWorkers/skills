---
name: rescuetime
description: 从 RescueTime 获取生产力数据。当用户询问他们的屏幕使用时间、生产力得分、应用程序使用情况、时间跟踪记录，或者希望了解自己一天/一周的工作安排时，可以使用此功能。需要使用 `TOOLS.md` 文件中提供的 API 密钥，或者直接提供 API 密钥。
---

# RescueTime

从 RescueTime API 获取生产力分析数据。

## 设置

将 API 密钥保存在 `TOOLS.md` 文件中：

```markdown
### RescueTime
- API Key: YOUR_KEY_HERE
```

获取 API 密钥的地址：https://www.rescuetime.com/anapi/manage

## API 端点

### 分析数据（主要端点）

```bash
curl "https://www.rescuetime.com/anapi/data?key=API_KEY&format=json&perspective=rank&restrict_kind=activity"
```

参数：
- `perspective`：排名、时间间隔、成员
- `restrict_kind`：类别、活动类型、生产力指标、效率指标、文档相关活动
- `interval`：月份、周、天、小时（仅适用于时间间隔维度）
- `restrict_begin` / `restrict_end`：日期格式为 YYYY-MM-DD
- `restrict_thing`：用于过滤特定应用程序/网站/类别的数据

### 每日总结数据

```bash
curl "https://www.rescuetime.com/anapi/daily_summary_feed?key=API_KEY"
```

返回过去 14 天的生产力指标（`productivity_pulse`，范围 0-100）和总工作时间。

## 生产力等级：

- 2：非常高效（编码、写作、使用终端、集成开发环境）
- 1：高效（沟通、查阅资料、学习）
- 0：中性（未分类）
- -1：分散注意力的活动（新闻、购物）
- -2：极其分散注意力的活动（社交媒体、游戏）

## 常见查询

**按应用程序划分的今日活动：**
```bash
curl "https://www.rescuetime.com/anapi/data?key=API_KEY&format=json&perspective=rank&restrict_kind=activity&restrict_begin=$(date +%Y-%m-%d)&restrict_end=$(date +%Y-%m-%d)"
```

**生产力指标细分：**
```bash
curl "https://www.rescuetime.com/anapi/data?key=API_KEY&format=json&perspective=rank&restrict_kind=productivity"
```

**按类别划分的生产力数据：**
```bash
curl "https://www.rescuetime.com/anapi/data?key=API_KEY&format=json&perspective=rank&restrict_kind=category"
```

**今日每小时的生产力数据：**
```bash
curl "https://www.rescuetime.com/anapi/data?key=API_KEY&format=json&perspective=interval&restrict_kind=productivity&interval=hour&restrict_begin=$(date +%Y-%m-%d)&restrict_end=$(date +%Y-%m-%d)"
```

## 响应格式

```json
{
  "row_headers": ["Rank", "Time Spent (seconds)", "Number of People", "Activity", "Category", "Productivity"],
  "rows": [[1, 3600, 1, "VS Code", "Editing & IDEs", 2], ...]
}
```

将秒数转换为小时：`seconds / 3600`

## 提示：

- 生产力指标超过 75 表示表现良好，超过 85 表示非常出色
- 使用类别视图有助于了解整体工作模式
- 对于时间分析，建议结合时间间隔和小时维度使用该 API
- 数据同步频率为：高级会员每 3 分钟一次，免费会员每 30 分钟一次