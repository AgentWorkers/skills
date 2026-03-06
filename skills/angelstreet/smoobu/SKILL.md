---
name: smoobu
description: 与 Smoobu 物业管理 API 进行交互。该 API 用于查询预订信息、查询房源可用性、管理预订以及发布公寓/房源信息。适用于租赁物业管理、Airbnb 数据同步、度假租赁预订以及客人管理等相关场景。
metadata:
  openclaw:
    emoji: "🏠"
---
# Smoobu 物业管理

Smoobu 是一个用于管理度假租赁房源（如 Airbnb、Booking.com 等）的工具。

## 设置

需要在 `~/.openclaw/.env` 文件中设置 `SMOOBU_API_KEY`：
```
SMOOBU_API_KEY=your_api_key_here
```

您可以在 Smoobu 的“设置” → “开发者”选项中找到您的 API 密钥。

## 快速参考

### API 基础地址
`https://login.smoobu.com`

### 认证
请求头：`Api-Key: {SMOOBU_API_KEY}`

### 请求速率限制
每分钟 1000 次请求

## 常用操作

### 列出房源信息
```bash
curl -s "https://login.smoobu.com/api/apartments" \
  -H "Api-Key: $SMOOBU_API_KEY" | jq
```

### 获取预订信息
```bash
# All bookings
curl -s "https://login.smoobu.com/api/reservations" \
  -H "Api-Key: $SMOOBU_API_KEY" | jq

# Filter by dates
curl -s "https://login.smoobu.com/api/reservations?from=2026-02-01&to=2026-02-28" \
  -H "Api-Key: $SMOOBU_API_KEY" | jq

# Filter by apartment
curl -s "https://login.smoobu.com/api/reservations?apartmentId=123" \
  -H "Api-Key: $SMOOBU_API_KEY" | jq
```

### 检查房源可用性
```bash
curl -s -X POST "https://login.smoobu.com/booking/checkApartmentAvailability" \
  -H "Api-Key: $SMOOBU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "arrivalDate": "2026-03-01",
    "departureDate": "2026-03-05",
    "apartments": [123, 456]
  }' | jq
```

### 创建预订
```bash
curl -s -X POST "https://login.smoobu.com/api/reservations" \
  -H "Api-Key: $SMOOBU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "arrivalDate": "2026-03-01",
    "departureDate": "2026-03-05",
    "apartmentId": 123,
    "channelId": 70,
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com",
    "adults": 2
  }' | jq
```

### 更新预订信息
```bash
curl -s -X PUT "https://login.smoobu.com/api/reservations/{id}" \
  -H "Api-Key: $SMOOBU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "arrivalTime": "15:00",
    "departureTime": "11:00",
    "notice": "Late checkout requested"
  }' | jq
```

### 获取用户信息
```bash
curl -s "https://login.smoobu.com/api/me" \
  -H "Api-Key: $SMOOBU_API_KEY" | jq
```

## 辅助脚本

使用 `scripts/smoobu.py` 执行常用操作：

```bash
# List apartments
python3 scripts/smoobu.py apartments

# List bookings (optional date range)
python3 scripts/smoobu.py bookings
python3 scripts/smoobu.py bookings --from 2026-02-01 --to 2026-02-28

# Check availability
python3 scripts/smoobu.py availability --arrival 2026-03-01 --departure 2026-03-05

# Get user info
python3 scripts/smoobu.py me
```

## API 响应示例

### 预订信息对象
```json
{
  "id": 291,
  "type": "reservation",
  "arrival": "2026-02-10",
  "departure": "2026-02-12",
  "apartment": {"id": 123, "name": "Beach House"},
  "channel": {"id": 465614, "name": "Booking.com"},
  "guest-name": "John Doe",
  "price": 250.00,
  "adults": 2,
  "children": 0
}
```

### 公寓信息对象
```json
{
  "id": 123,
  "name": "Beach House",
  "location": {"city": "Nice", "country": "France"}
}
```

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 401 | API 密钥无效 |
| 400 | 验证错误（请查看响应内容） |
| 429 | 超过请求速率限制 |

## 文档

完整 API 文档：https://docs.smoobu.com