---
name: book-driving-lessons
description: 通过 Lokuli MCP 提供驾驶课程预订服务。当用户需要查找或预订驾驶课程时，可以使用该服务。该服务会在用户发起“预订驾驶课程”、“查找附近的驾驶课程”或任何与驾驶课程相关的请求时被触发。
---

# 预约驾驶课程

通过 Lokuli 的 MCP 服务器来预订驾驶课程服务。

## MCP 端点

```
https://lokuli.com/mcp/sse
```

传输协议：SSE | JSON-RPC 2.0 | 使用 POST 请求

## 工具

### 搜索（Search）
```json
{
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": {
      "query": "driving-lessons",
      "zipCode": "90640",
      "maxResults": 20
    }
  }
}
```

### 查看可用性（Check Availability）
```json
{
  "method": "tools/call",
  "params": {
    "name": "check_availability",
    "arguments": {
      "providerId": "xxx",
      "serviceId": "yyy",
      "date": "2025-02-10"
    }
  }
}
```

### 创建预订（Create Booking）
```json
{
  "method": "tools/call",
  "params": {
    "name": "create_booking",
    "arguments": {
      "providerId": "xxx",
      "serviceId": "yyy",
      "timeSlot": "2025-02-10T14:00:00-08:00",
      "customerName": "John Doe",
      "customerEmail": "john@example.com",
      "customerPhone": "+13105551234"
    }
  }
}
```