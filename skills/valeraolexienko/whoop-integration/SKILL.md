---
name: whoop-integration
description: **与 WHOOP 健身追踪器 API 集成，以监控睡眠、恢复状况和身体负荷数据。**  
当您需要检查睡眠质量、恢复评分、分析健身模式、根据睡眠表现调整早晨的作息习惯，或创建自动化的健康监测工作流程时，可以使用该功能。该集成支持 OAuth 认证、睡眠表现追踪以及智能助手的辅助功能。
metadata:
  {
    "openclaw":
      {
        "emoji": "🏃‍♀️",
        "requires": { "env": ["WHOOP_CLIENT_ID", "WHOOP_CLIENT_SECRET"] },
        "primaryEnv": "WHOOP_CLIENT_SECRET",
      }
  }
---

# WHOOP 集成

从 WHOOP 健身追踪器中监控睡眠、恢复情况和身体负荷数据。

## 令牌（Tokens）

令牌存储在 `~/.openclaw/whoop_tokens.json` 文件中：
```json
{
  "access_token": "...",
  "refresh_token": "...",
  "obtained_at": "ISO timestamp",
  "expires_at": "ISO timestamp"
}
```

## 令牌更新（Token Rotation）

请刷新相关端点（非常重要——其他路径会返回 404 错误！）：
```
POST https://api.prod.whoop.com/oauth/oauth2/token
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token&refresh_token=REFRESH_TOKEN&client_id=CLIENT_ID&client_secret=CLIENT_SECRET
```

`CLIENT_ID` 和 `CLIENT_SECRET` 分别存储在环境变量 `WHOOP_CLIENT_ID` 和 `WHOOP_CLIENT_SECRET` 中。

当令牌的 `expires_at` 日期在 1 小时内时，需要更新令牌。更新后的令牌应包含新的 `obtained_at` 和 `expires_at` 日期。

## API 端点（API Endpoints）

**基础 URL：** `https://api.prod.whoop.com/developer`
**认证方式：** `Authorization: Bearer {access_token}`

**⚠️ 请使用 V2 端点！V1 版本会返回 404 错误！**

### 睡眠数据（Sleep Data）
```
GET /v2/activity/sleep?limit=1
```

`records[0].score` 中的关键字段包括：
- `sleep_performance_percentage` — 睡眠质量（0-100%）
- `sleep_efficiency_percentage` — 实际睡眠时间与躺在床上的时间的比例
- `sleep_consistency_percentage` — 睡眠的稳定性
- `respiratory_rate` — 呼吸频率
- `stage_summary`：
  - `total_in_bed_time_milli` — 总睡眠时间（毫秒）
  - `total_light_sleep_time_milli` — 轻度睡眠时间（毫秒）
  - `total_slow_wave_sleep_time_milli` — 深度睡眠时间（毫秒）
  - `totalREM_sleep_time_milli` — 快速眼动睡眠时间（毫秒）
  - `total_awake_time_milli` — 清醒时间（毫秒）
  - `sleep_cycle_count` — 睡眠周期数
  - `disturbance_count` — 睡眠中断次数

### 恢复数据（Recovery Data）
```
GET /v2/recovery?limit=1
```

`records[0].score` 中的关键字段包括：
- `recovery_score`（0-100 分）—— 恢复情况
- `resting_heart_rate`（心率，单位：bpm）  
- `hrv_rmssd_milli`（心率变异性，单位：毫秒，数值越低越好）
- `spo2_percentage` — 血氧饱和度百分比
- `skin_temp_celsius` — 皮肤温度（摄氏度）

## 早晨报告格式（Morning Report Format）

**恢复数据优先显示——这对用户来说非常重要！**

将数据发送到 Telegram（频道：`telegram`，目标账号：`36171288`）：
```
🏃‍♀️ WHOOP Ранковий звіт

💚 Відновлення: X% [колір]
❤️ Пульс: X bpm | HRV: X ms | SpO2: X%
📋 [Рекомендація]

😴 Сон: X% ефективність (Xг Xхв загалом)
💤 Deep: Xхв | REM: Xхв | Light: Xхв
🔄 Циклів: X | Пробуджень: X
```

### 恢复情况的颜色编码及建议：
- **>67%（绿色 🟢）**：状态良好，可以全力训练
- **34-67%（黄色 🟡）**：注意，避免过度训练
- **<34%（红色 🔴）**：需要休息，避免剧烈运动

### 时间单位转换：
- 将毫秒（millisecond）转换为分钟：除以 60000
- 将毫秒转换为小时：除以 3600000

## 按时间段分析数据（Analysis by Period）

要分析任意时间段的数据，请使用 `start`、`end` 和 `limit` 参数：

### 按时间段分析睡眠数据（Sleep Analysis by Period）
```
GET /v2/activity/sleep?start=2026-01-28T00:00:00.000Z&end=2026-02-04T00:00:00.000Z&limit=25
```

### 按时间段分析恢复数据（Recovery Analysis by Period）
```
GET /v2/recovery?start=2026-01-28T00:00:00.000Z&end=2026-02-04T00:00:00.000Z&limit=25
```

### 按时间段分析身体负荷数据（Strain Analysis by Period）
```
GET /v2/cycle?start=2026-01-28T00:00:00.000Z&end=2026-02-04T00:00:00.000Z&limit=25
```

### 按时间段分析锻炼数据（Workout Analysis by Period）
```
GET /v2/activity/workout?start=2026-01-28T00:00:00.000Z&end=2026-02-04T00:00:00.000Z&limit=25
```

日期格式遵循 ISO 8601 标准。`start` 参数包含起始时间，`end` 参数不包括结束时间。`limit` 参数的最大值为 25，超过该值需要通过 `nextToken` 进行分页查询。

### 可分析的内容：
- **恢复趋势（Recovery Trends）**：一周或一个月内的恢复情况是否有所改善
- **平均心率变异性（Average HRV）**：数值上升表示身体适应良好，下降表示过度训练
- **睡眠质量（Sleep Quality）**：深度睡眠和快速眼动睡眠占总睡眠时间的比例，以及睡眠效率的趋势
- **身体负荷与恢复能力（Strain vs Recovery）**：训练强度是否与身体恢复能力相匹配
- **静息心率趋势（Resting HR Trend）**：心率下降表示身体状况良好，上升可能表示压力或疾病
- **睡眠稳定性（Consistency）**：睡眠模式的稳定性

### 分析报告的格式（Analysis Report Format，用于 Telegram）：
```
📊 WHOOP Аналіз: [період]

💚 Recovery: avg X% (min X% — max X%) [тренд ↑↓→]
❤️ HRV: avg X ms (тренд ↑↓→)
💤 Сон: avg Xг Xхв (ефективність avg X%)
🏋️ Strain: avg X (max X)
🫀 Пульс спокою: avg X bpm (тренд ↑↓→)

📈 Висновки: [коротко що добре/погано і рекомендації]
```

## 自适应行为（Adaptive Behavior）

根据用户的恢复情况调整沟通内容：
- **>80%**：状态良好，建议安排具有挑战性的任务
- **67-80%**：状态正常，建议采取平衡的作息方式
- **34-67%**：状态一般，建议安排较为轻松的任务
- **<34%**：状态较差，建议减少活动量，重点休息