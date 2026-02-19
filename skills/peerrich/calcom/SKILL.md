---
name: calcom-api
description: 与 Cal.com API v2 进行交互，以管理日程安排、预订、事件类型、可用性以及日历。在构建需要创建或管理预订、检查可用性、配置事件类型或与 Cal.com 的日程安排系统同步日历的集成时，请使用此技能。
license: MIT
metadata:
  author: calcom
  version: "1.0.0"
  api-version: "v2"
---
# Cal.com API v2

本文档为AI代理提供了与Cal.com API v2交互的指南，支持自动化日程安排、预订管理以及日历集成等功能。

## 基本URL

所有API请求应发送至：
```
https://api.cal.com/v2
```

## 认证

所有API请求都需要在`Authorization`头部使用Bearer令牌进行认证：

```
Authorization: Bearer cal_<your_api_key>
```

API密钥前缀必须为`cal_`。您可以在Cal.com的“设置” > “开发者” > “API密钥”中生成API密钥。

## 核心概念

### 事件类型
事件类型定义了可预订的会议配置（时长、地点、可用性规则）。每种事件类型都有一个唯一的标识符（slug），用于构建预订URL。

### 预订
预订是指用户成功预订某个事件类型后创建的预约记录。每个预订都有一个唯一的UID用于识别。

### 日程安排
日程安排表示用户可用于预订的时间段。用户可以拥有多个具有不同工作时间的日程安排。

### 时间段
时间段表示根据事件类型配置和用户可用性可预订的可用时间窗口。

## 常用操作

### 检查可用时间段
在创建预订之前，请先检查可用时间段：

```http
GET /v2/slots?startTime=2024-01-15T00:00:00Z&endTime=2024-01-22T00:00:00Z&eventTypeId=123&eventTypeSlug=30min
```

查询参数：
- `startTime`（必填）：时间的ISO 8601格式起始时间
- `endTime`（必填）：时间的ISO 8601格式结束时间
- `eventTypeId` 或 `eventTypeSlug`：事件类型的标识
- `timeZone`：时间段显示的时区（默认：UTC）

响应结果会按日期分组显示可用时间段。

### 创建预订
```http
POST /v2/bookings
Content-Type: application/json

{
  "start": "2024-01-15T10:00:00Z",
  "eventTypeId": 123,
  "attendee": {
    "name": "John Doe",
    "email": "john@example.com",
    "timeZone": "America/New_York"
  },
  "meetingUrl": "https://cal.com/team/meeting",
  "metadata": {}
}
```

必填字段：
- `start`：预订的开始时间（ISO 8601格式）
- `eventTypeId`：要预订的事件类型的ID
- `attendee.name`：参与者的全名
- `attendee.email`：参与者的电子邮件地址
- `attendee.timeZone`：参与者的时区

### 获取预订记录
可以添加筛选条件来列出预订记录：

```http
GET /v2/bookings?status=upcoming&take=10
```

查询参数：
- `status`：按状态筛选（即将开始、重复、已结束、已取消、未确认）
- `attendeeEmail`：按参与者电子邮件筛选
- `eventTypeId`：按事件类型筛选
- `take`：返回的结果数量（最多250条）
- `skip`：分页偏移量

### 获取单个预订记录
```http
GET /v2/bookings/{bookingUid}
```

### 取消预订
```http
POST /v2/bookings/{bookingUid}/cancel
Content-Type: application/json

{
  "cancellationReason": "Schedule conflict"
}
```

### 重新安排预订
```http
POST /v2/bookings/{bookingUid}/reschedule
Content-Type: application/json

{
  "start": "2024-01-16T14:00:00Z",
  "reschedulingReason": "Conflict with another meeting"
}
```

### 列出所有事件类型
```http
GET /v2/event-types
```

返回当前认证用户可使用的所有事件类型。

### 获取单个事件类型
```http
GET /v2/event-types/{eventTypeId}
```

### 创建事件类型
```http
POST /v2/event-types
Content-Type: application/json

{
  "title": "30 Minute Meeting",
  "slug": "30min",
  "lengthInMinutes": 30,
  "locations": [
    {
      "type": "integration",
      "integration": "cal-video"
    }
  ]
}
```

### 列出日程安排
```http
GET /v2/schedules
```

### 获取默认日程安排
```http
GET /v2/schedules/default
```

### 创建日程安排
```http
POST /v2/schedules
Content-Type: application/json

{
  "name": "Working Hours",
  "timeZone": "America/New_York",
  "isDefault": true,
  "availability": [
    {
      "days": [1, 2, 3, 4, 5],
      "startTime": "09:00",
      "endTime": "17:00"
    }
  ]
}
```

日期从0开始计数（0表示星期日，1表示星期一等）。

### 获取当前用户信息
```http
GET /v2/me
```

返回当前认证用户的个人信息。

## 团队和组织端点
对于团队预订和组织管理，请使用以下组织级别的端点：

### 列出组织内的团队
```http
GET /v2/organizations/{orgId}/teams
```

### 获取团队可用的事件类型
```http
GET /v2/organizations/{orgId}/teams/{teamId}/event-types
```

### 创建团队预订
团队事件类型支持不同的调度模式：
- `COLLECTIVE`：所有团队成员都必须参加
- `ROUND_ROBIN`：在团队成员之间分配预订任务

## Webhook
配置Webhook以接收实时通知：

### 列出Webhook
```http
GET /v2/webhooks
```

### 创建Webhook
```http
POST /v2/webhooks
Content-Type: application/json

{
  "subscriberUrl": "https://your-app.com/webhook",
  "triggers": ["BOOKING_CREATED", "BOOKING_CANCELLED"],
  "active": true
}
```

可用的触发事件：
- `BOOKING CREATED`：预订创建
- `BOOKING_CANCELLED`：预订取消
- `BOOKING_RESCHEDULED`：预订重新安排
- `BOOKING_CONFIRMED`：预订确认
- `MEETING_STARTED`：会议开始
- `MEETING_ENDED`：会议结束

## 日历集成
### 列出已连接的日历
```http
GET /v2/calendars
```

### 检查用户繁忙时间
```http
GET /v2/calendars/busy-times?startTime=2024-01-15T00:00:00Z&endTime=2024-01-22T00:00:00Z
```

## 错误处理
API返回标准HTTP状态码：
- `200`：成功
- `201`：创建成功
- `400`：请求错误（参数无效）
- `401`：未经授权（API密钥无效或缺失）
- `403`：禁止访问（权限不足）
- `404`：未找到
- `422`：实体无法处理（验证错误）
- `500`：内部服务器错误

错误响应会包含错误信息：

```json
{
  "status": "error",
  "message": "Booking not found"
}
```

## 速率限制
API实施了速率限制。如果超过限制，将会收到`429 Too Many Requests`的错误响应。请使用指数退避策略进行重试。

## 分页
列表端点支持通过`take`和`skip`参数进行分页：
- `take`：返回的记录数量（默认：10条，最多250条）
- `skip`：跳过的记录数量

## 最佳实践
1. 在创建预订前务必检查时间段是否可用
2. 存储预订记录的UID以便后续取消或重新安排
3. 小心处理时区转换——始终使用ISO 8601格式
4. 实现Webhook处理程序以接收实时预订更新
5. 缓存事件类型数据以减少API调用次数
6. 对所有API请求进行适当的错误处理

## 额外资源
- [完整API参考文档](https://cal.com/docs/api-reference/v2)
- [OpenAPI规范](https://api.cal.com/v2/docs)