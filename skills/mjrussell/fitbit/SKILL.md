---
name: fitbit
description: 查询 Fitbit 的健康数据，包括睡眠质量、心率、活动量、血氧饱和度（SpO2）和呼吸频率。当用户询问自己的健康状况、睡眠质量、步数或健康指标时，可以使用此功能。
homepage: https://www.fitbit.com
metadata:
  clawdbot:
    emoji: "💪"
    requires:
      bins: ["fitbit-cli"]
---

# Fitbit CLI

用于查询来自 Fitbit 可穿戴设备的健康和健身数据。

## 命令

### 健康数据
```bash
# Sleep logs (deep, light, REM, awake times)
fitbit-cli -s                    # today
fitbit-cli -s yesterday          # yesterday
fitbit-cli -s last-week          # last 7 days
fitbit-cli -s 2026-01-01         # specific date

# Heart rate time series
fitbit-cli -e                    # today
fitbit-cli -e last-week          # last 7 days

# Blood oxygen (SpO2)
fitbit-cli -o                    # today
fitbit-cli -o last-3-days        # last 3 days

# Active Zone Minutes
fitbit-cli -a                    # today
fitbit-cli -a last-month         # last month

# Breathing rate
fitbit-cli -b                    # today

# Daily activity (steps, calories, distance, floors)
fitbit-cli -t                    # today
fitbit-cli -t yesterday          # yesterday
```

### 账户与设备
```bash
# User profile
fitbit-cli -u

# Connected devices (battery, sync status)
fitbit-cli -d
```

### 日期格式

- 无参数：今日
- 特定日期：`2026-01-05`
- 日期范围：`2026-01-01,2026-01-05`
- 相对日期：`昨天`、`上周`、`上个月`
- 自定义相对日期：`过去2天`、`过去3周`、`过去2个月`

## 使用示例

**用户询问：“我昨晚的睡眠情况如何？”**
```bash
fitbit-cli -s yesterday
```

**用户询问：“我这周的心率情况如何？”**
```bash
fitbit-cli -e last-week
```

**用户询问：“我今天走了多少步？”**
```bash
fitbit-cli -t
```

**用户询问：“显示我的血氧饱和度（SpO2）水平。”**
```bash
fitbit-cli -o
```

**用户询问：“我的 Fitbit 设备是否已同步？”**
```bash
fitbit-cli -d
```

**用户询问：“我上个月的活动量如何？”**
```bash
fitbit-cli -a last-month
```

## 注意事项

- 只能读取 Fitbit 数据
- 令牌会自动刷新（8 小时后失效）
- 数据可能因设备同步延迟而有所延迟
- 首次设置时需要运行：`fitbit-cli --init-auth`