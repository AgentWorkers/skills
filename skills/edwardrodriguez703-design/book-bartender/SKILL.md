---
name: book-bartender
description: 通过 Lokuli MCP 预订调酒师服务。当用户需要寻找或预订调酒师时，可以使用该功能。该功能会在用户发出“预订调酒师”、“查找附近的调酒师”或任何与调酒师服务相关的请求时被触发。
---

# uook uartender

通过 Lokuli 的 MCP 服务器预订酒吧服务。

## MCP 端点

```
https://lokuli.com/mcp/sse
```

传输协议：SSE | JSON-RPC 2.0 | 支持 POST 请求

## 工具

### search
```json
{
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": {
      "query": "bartender",
      "zipCode": "90640",
      "maxResults": 20
    }
  }
}
```

### check_availability
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

### create_booking
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