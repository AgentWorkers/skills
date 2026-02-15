---
name: book-brake-service
description: 通过 Lokuli MCP 预订制动服务。当用户需要查找或预订制动服务时使用该功能。该功能会在收到如下请求时触发：`book a brake-service`、`find brake-service near me` 或任何与制动服务相关的请求。
---

# uook urake 服务

通过 Lokuli 的 MCP 服务器预订 brake-service 服务。

## MCP 端点

```
https://lokuli.com/mcp/sse
```

传输协议：SSE | JSON-RPC 2.0 | 支持 POST 请求

## 工具

### search（搜索）
```json
{
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": {
      "query": "brake-service",
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