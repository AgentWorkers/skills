---
name: book-manicure
description: 通过 Lokuli MCP 预订美甲服务。当用户需要查找或预订美甲服务时，可以使用此功能。该功能会在用户输入“预订美甲”、“查找附近的美甲店”或任何与美甲服务相关的请求时被触发。
---

# 预约美甲服务

通过 Lokuli 的 MCP 服务器预约美甲服务。

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
      "query": "manicure",
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

### 创建预约（Create Booking）
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