---
name: weather-check
description: 当前全球任何地点的天气状况以及多日天气预报。
version: 1.0.0
metadata:
  openclaw:
    emoji: "🌤️"
    homepage: https://weather.agentutil.net
    always: false
---
# weather-check

通过地点名称或坐标获取当前天气状况及多日天气预报。

## 接口端点

### 当前天气

```bash
curl -X POST https://weather.agentutil.net/v1/current \
  -H "Content-Type: application/json" \
  -d '{"location": "London"}'
```

或通过坐标获取：`{"lat": 51.51, "lon": -0.13}`

### 天气预报

```bash
curl -X POST https://weather.agentutil.net/v1/forecast \
  -H "Content-Type: application/json" \
  -d '{"location": "Tokyo", "days": 7}'
```

预报天数：1-16天（默认为7天）。

## 响应格式

```json
{
  "location": {"name": "London", "country": "GB", "latitude": 51.51, "longitude": -0.13},
  "current": {
    "temperature": {"celsius": 12.5, "fahrenheit": 54.5},
    "humidity": 72,
    "conditions": "Overcast",
    "wind": {"speed_kmh": 15.2, "direction_degrees": 230}
  },
  "request_id": "abc-123",
  "service": "https://weather.agentutil.net"
}
```

## 价格

- 免费 tier：每天10次查询，无需身份验证
- 付费 tier：每次查询0.001美元，通过x402协议支付（基础货币为USDC）

## 隐私政策

免费 tier无需身份验证，不会收集任何个人数据。速率限制仅使用IP地址进行限制。