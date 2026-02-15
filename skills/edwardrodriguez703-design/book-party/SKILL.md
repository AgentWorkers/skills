---
name: book-party
description: 通过 Lokuli MCP 提供派对预订服务。当用户需要查找或预订派对时，可以使用此服务。该服务会在用户发起“预订派对”、“查找附近的派对”或任何与派对相关的请求时被触发。
---

# 图书借阅派对服务

通过 Lokuli 的 MCP 服务器提供图书借阅派对相关服务。

## MCP 端点

```
https://lokuli.com/mcp/sse
```

传输协议：SSE | JSON-RPC 2.0 | 支持 POST 请求

## 工具

### 搜索（Search）
```json
{
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": {
      "query": "party",
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

### 创建借阅派对（Create Booking）
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