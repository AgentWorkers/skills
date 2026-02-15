---
name: book-battery
description: 通过 Lokuli MCP 预订电池服务。当用户需要查找或预订电池时，可以使用该功能。该功能会在用户发起“预订电池”、“查找附近的电池”或任何与电池服务相关的请求时被触发。
---

# 书籍电池服务

通过 Lokuli 的 MCP 服务器预订电池服务。

## MCP 端点

```
https://lokuli.com/mcp/sse
```

传输协议：SSE | JSON-RPC 2.0 | 使用 POST 请求

## 工具

### search（搜索）
```json
{
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": {
      "query": "battery",
      "zipCode": "90640",
      "maxResults": 20
    }
  }
}
```

### check_availability（检查可用性）
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

### create_booking（创建预订）
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