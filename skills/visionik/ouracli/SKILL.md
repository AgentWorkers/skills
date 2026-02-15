---
name: oura-ring-data
description: 使用 ouracli CLI 工具访问 Oura Ring 的健康数据。当用户询问“oura 数据”、“睡眠统计”、“活动数据”、“心率”、“健康状况评分”或想要获取他们的 Oura Ring 的健康指标时，可以使用该工具。
allowed-tools: Bash
---

# Oura Ring 数据访问

通过 `ouracli` 命令行接口从 Oura Ring 中检索健康和健身数据。

## 重要提示：需要身份验证

**在运行 `ouracli` 命令之前，请务必检查身份验证。** 该工具需要一个名为 `PERSONAL_ACCESS_TOKEN` 的环境变量。

- 令牌的位置：`secrets/oura.env` 或 `~/.secrets/oura.env`
- 如果命令因身份验证错误而失败，请告知用户从以下链接获取令牌：https://cloud.ouraring.com/personal-access-tokens

## 可用的数据类型

### 核心健康指标
- `activity` - 每日活动量（步数、MET 值、卡路里）
- `sleep` - 睡眠数据（睡眠阶段、睡眠效率、心率）
- `readiness` - 准备状态得分及相关因素
- `heartrate` - 心率时间序列数据（5分钟分辨率）
- `spo2` - 血氧饱和度数据
- `stress` - 每日压力水平

### 其他数据
- `workout` - 锻炼记录
- `session` - 活动会话记录
- `tag` - 用户添加的标签
- `rest-mode` - 休息模式时间段
- `personal-info` - 用户个人信息
- `all` - 所有可用数据类型

## 日期范围指定

### ✅ 支持的格式（请使用这些格式！）

```bash
# Single date (no quotes needed)
ouracli activity 2025-12-25
ouracli sleep today
ouracli heartrate yesterday

# Relative ranges from today (MUST use quotes)
ouracli activity "7 days"      # Last 7 days including today
ouracli sleep "30 days"        # Last 30 days
ouracli readiness "2 weeks"    # Last 2 weeks
ouracli stress "1 month"       # Last month

# Date + duration (MUST use quotes)
ouracli activity "2025-12-01 28 days"    # 28 days starting Dec 1
ouracli sleep "2025-09-23 7 days"        # Week starting Sept 23
```

**⚠️ 重要提示：当日期范围包含空格时，请使用引号！**

### ❌ 不支持的格式（请勿使用）

```bash
# ❌ WRONG - Two separate dates
ouracli activity 2025-09-23 2025-09-30

# ❌ WRONG - "to" syntax
ouracli activity "2025-09-23 to 2025-09-30"

# ❌ WRONG - Range operators
ouracli activity "2025-09-23..2025-09-30"

# ❌ WRONG - Relative past expressions
ouracli activity "3 months ago"
```

### 转换日期范围

如果用户请求特定日期之间的数据：

**步骤 1**：计算日期之间的天数（包含起始和结束日期）
```
Example: Sept 23 to Sept 30 = 7 days
         Dec 1 to Dec 31 = 30 days
```

**步骤 2**：使用“日期 + 持续时间”的格式
```bash
# ✅ CORRECT
ouracli activity "2025-09-23 7 days"
ouracli activity "2025-12-01 30 days"
```

## 输出格式

**进行程序化数据分析时，请始终使用 `--json` 格式。** 这是解析数据最可靠的格式。

```bash
# ✅ RECOMMENDED for AI analysis
ouracli activity "7 days" --json

# Other formats (human-readable)
ouracli activity today --tree        # Default: tree structure
ouracli activity "7 days" --markdown # Markdown with charts
ouracli activity "7 days" --html > activity.html  # Interactive HTML charts
ouracli activity "7 days" --dataframe  # Pandas DataFrame format
```

## 常见使用场景

### 快速数据查询
```bash
# Today's activity
ouracli activity today --json

# Recent sleep data
ouracli sleep "7 days" --json

# Current readiness
ouracli readiness today --json
```

### 详细分析
```bash
# Weekly health summary
ouracli all "7 days" --json

# Monthly activity report
ouracli activity "30 days" --json

# Heart rate for specific date
ouracli heartrate "2025-12-15 1 days" --json
```

### 多日报告
```bash
# All data grouped by day (HTML report)
ouracli all "7 days" --by-day --html > weekly-report.html

# All data grouped by type
ouracli all "7 days" --by-method --json
```

## 关键注意事项

### 关于准备状态得分的说明
⚠️ **重要提示**：`readiness` 数据中的 `contributors/resting_heartrate` 字段是一个 **得分（0-100）**，而非实际的心率值：
- 低得分（19, 47）表示心率高于基线（负面影响）
- 高得分（95, 100）表示心率处于最佳状态（正面影响）
- 实际的心率值可以在 `heartrate` 命令的输出中获取

**请勿将得分解释为实际的心率测量值。**

### Oura API 的特殊注意事项
- 单日查询有时会因时区问题返回空结果
- 使用日期范围（例如：“YYYY-MM-DD 2 days”）以获得更可靠的结果
- 在查询特定日期时，请考虑添加一个缓冲日

## 故障排除

### 错误：“收到意外的额外参数”
**原因**：使用了两个独立的日期参数，而不是一个包含引号的日期范围
```bash
# ❌ WRONG
ouracli activity 2025-09-23 2025-09-30

# ✅ CORRECT
ouracli activity "2025-09-23 7 days"
```

### 错误：“无效的日期格式”
**原因**：使用了不支持的语法，如 “to”、“..” 或相对表达式
```bash
# ❌ WRONG
ouracli activity "2025-09-23 to 2025-09-30"

# ✅ CORRECT
ouracli activity "2025-09-23 7 days"
```

### 未返回数据
**解决方法**：
1. 尝试使用更宽的日期范围：`ouracli activity "7 days" --json`
2. 添加缓冲日：`ouracli activity "2025-12-25 2 days" --json`
3. 检查 Oura Ring 是否已同步数据
4. 确认日期是否在数据可用范围内

## 用户查询的示例响应

### “显示我上周的活动情况”
```bash
ouracli activity "7 days" --json
```

### “我昨晚的睡眠质量如何？”
```bash
ouracli sleep today --json
```

### “我12月的准备状态如何？”
```bash
ouracli readiness "2025-12-01 30 days" --json
```

### “获取我9月23日至9月30日的所有数据”
```bash
# Calculate: Sept 30 - Sept 23 = 7 days
ouracli all "2025-09-23 7 days" --json
```

### “显示我昨天的心率”
```bash
ouracli heartrate yesterday --json
```

## 快速参考

| 用户意图 | 命令 |
|-------------|---------|
| 查看今天的活动量 | `ouracli activity today --json` |
| 查看上周的睡眠情况 | `ouracli sleep "7 days" --json` |
| 查看当前的准备状态 | `ouracli readiness today --json` |
| 查看今天的心率 | `ouracli heartrate today --json` |
| 查看每月总结 | `ouracli all "30 days" --json` |
| 查看特定日期范围的数据 | `ouracli [类型] "YYYY-MM-DD N days" --json` |
| 查看所有数据类型 | `ouracli all "7 days" --json` |

## 注意事项

- 对于 AI 分析，请始终使用 `--json` 格式
- 当日期范围包含空格时，请使用引号
- 计算特定日期范围的天数
- 如果命令失败，请检查身份验证是否正确
- 在查询特定日期时，请注意时区的特殊性