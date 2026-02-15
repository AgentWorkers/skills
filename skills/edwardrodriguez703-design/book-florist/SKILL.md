---
name: book-florist
description: 通过 Lokuli MCP 预订花店服务。当用户需要查找或预订花店时，可以使用此功能。该功能会在用户发起“预订花店”、“查找附近的花店”或任何与花店服务相关的请求时被触发。
---

# uook 花店

通过 Lokuli 的 MCP 服务器预订花店服务。

## MCP 端点

```
https://lokuli.com/mcp/sse
```

传输协议：SSE | JSON-RPC 2.0 | 使用 POST 请求

## 工具

### search （搜索）
```json
{
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": {
      "query": "florist",
      "zipCode": "90640",
      "maxResults": 20
    }
  }
}
```

### check_availability （查询可用性）
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

### create_booking （创建预订）
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