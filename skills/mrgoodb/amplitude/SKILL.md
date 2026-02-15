---
name: amplitude
description: 通过 Amplitude API 追踪事件并分析产品使用情况。可以查询用户行为、用户群体（cohorts）以及用户转化路径（funnels）。
metadata: {"clawdbot":{"emoji":"📈","requires":{"env":["AMPLITUDE_API_KEY","AMPLITUDE_SECRET_KEY"]}}}
---

# Amplitude

产品分析平台。

## 环境配置

```bash
export AMPLITUDE_API_KEY="xxxxxxxxxx"
export AMPLITUDE_SECRET_KEY="xxxxxxxxxx"
```

## 跟踪事件（HTTP API）

```bash
curl -X POST "https://api2.amplitude.com/2/httpapi" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "'$AMPLITUDE_API_KEY'",
    "events": [{
      "user_id": "user123",
      "event_type": "Button Clicked",
      "event_properties": {"button_name": "signup"}
    }]
  }'
```

## 批量跟踪事件

```bash
curl -X POST "https://api2.amplitude.com/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "'$AMPLITUDE_API_KEY'",
    "events": [
      {"user_id": "user1", "event_type": "Page View"},
      {"user_id": "user2", "event_type": "Page View"}
    ]
  }'
```

## 导出事件数据（仪表盘 API）

```bash
curl -u "$AMPLITUDE_API_KEY:$AMPLITUDE_SECRET_KEY" \
  "https://amplitude.com/api/2/export?start=20240101T00&end=20240102T00"
```

## 获取用户活动数据

```bash
curl -u "$AMPLITUDE_API_KEY:$AMPLITUDE_SECRET_KEY" \
  "https://amplitude.com/api/2/useractivity?user=user123"
```

## 获取活跃用户信息

```bash
curl -u "$AMPLITUDE_API_KEY:$AMPLITUDE_SECRET_KEY" \
  "https://amplitude.com/api/2/users/list?start=20240101&end=20240131"
```

## 链接：
- 仪表盘：https://analytics.amplitude.com
- 文档：https://www.docs.developers.amplitude.com