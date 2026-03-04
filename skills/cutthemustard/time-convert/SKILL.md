---
name: time-convert
description: 时区转换、当前时间、日期运算以及时间戳（epoch）转换。
version: 1.0.0
metadata:
  openclaw:
    emoji: "🕐"
    homepage: https://time.agentutil.net
    always: false
---
# time-convert

该工具支持查询任意时区的当前时间、进行时区之间的转换、日期运算（加/减），以及将ISO 8601格式的时间转换为Unix纪元时间（epoch time）。

## 提供的功能

### 当前时间查询
```bash
curl -X POST https://time.agentutil.net/v1/now \
  -H "Content-Type: application/json" \
  -d '{"timezone": "Pacific/Auckland"}'
```

### 时区转换
```bash
curl -X POST https://time.agentutil.net/v1/convert \
  -H "Content-Type: application/json" \
  -d '{"time": "2026-03-04T09:00:00", "from_timezone": "America/New_York", "to_timezone": "Pacific/Auckland"}'
```

### 日期运算
```bash
curl -X POST https://time.agentutil.net/v1/math \
  -H "Content-Type: application/json" \
  -d '{"date": "2026-03-04T00:00:00Z", "operation": "add", "value": 7, "unit": "days"}'
```

时间单位：秒、分钟、小时、天、周、月、年。

### 时间格式转换（ISO 8601到Unix纪元）
```bash
curl -X POST https://time.agentutil.net/v1/epoch \
  -H "Content-Type: application/json" \
  -d '{"value": 1741046400, "direction": "from_epoch"}'
```

## 响应格式
```json
{
  "iso": "2026-03-04T14:30:00.000+13:00",
  "unix": 1741050600,
  "timezone": "Pacific/Auckland",
  "day_of_week": "Wednesday",
  "is_dst": true,
  "request_id": "abc-123",
  "service": "https://time.agentutil.net"
}
```

## 价格政策

- 免费 tier：每天10次查询，无需身份验证。
- 付费 tier：每次查询0.001美元，通过x402协议支付（货币为Base上的USDC）。

## 隐私政策

免费 tier无需身份验证，不会收集任何个人数据。速率限制仅使用IP地址进行识别。