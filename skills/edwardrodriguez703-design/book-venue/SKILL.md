---
name: book-venue
description: 通过 Lokuli MCP 提供场地预订服务。当用户需要查找和预订场地时，可以使用该功能。该功能会在用户发出“预订场地”、“查找附近的场地”或任何与场地相关的请求时被触发。
---

# 预订场地服务

您可以通过 Lokuli 的 MCP 服务器来预订场地。

## MCP 端点

```
https://lokuli.com/mcp/sse
```

支持传输协议：SSE | JSON-RPC 2.0 | 使用 POST 请求进行操作

## 工具

### 搜索（Search）
```json
{
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": {
      "query": "venue",
      "zipCode": "90640",
      "maxResults": 20
    }
  }
}
```

### 检查场地可用性（Check Availability）
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