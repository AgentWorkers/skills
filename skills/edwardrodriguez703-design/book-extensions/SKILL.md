---
name: book-extensions
description: 通过 Lokuli MCP 提供扩展服务。当用户需要查找和预订扩展时使用该服务。该服务会在用户发起“预订扩展”、“查找附近的扩展”或任何与扩展服务相关的请求时被触发。
---

# uook扩展功能

通过Lokuli的MCP服务器提供书籍扩展服务。

## MCP端点

```
https://lokuli.com/mcp/sse
```

传输协议：SSE | JSON-RPC 2.0 | 使用POST请求

## 工具

### search（搜索）
```json
{
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": {
      "query": "extensions",
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