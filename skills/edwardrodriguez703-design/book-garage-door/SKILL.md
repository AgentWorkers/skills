---
name: book-garage-door
description: 通过 Lokuli MCP 预订车库门服务。当用户需要查找或预订车库门时，可以使用该功能。该功能会在用户发起“预订车库门”、“查找附近的车库门”或任何与车库门服务相关的请求时被触发。
---

# uook车库门服务

您可以通过Lokuli的MCP服务器预订车库门服务。

## MCP端点

```
https://lokuli.com/mcp/sse
```

传输协议：SSE | JSON-RPC 2.0 | 支持POST请求

## 工具

### 搜索（Search）
```json
{
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": {
      "query": "garage-door",
      "zipCode": "90640",
      "maxResults": 20
    }
  }
}
```

### 检查可用性（Check Availability）
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