---
name: book-pilates
description: 通过 Lokuli MCP 预订普拉提课程。当用户需要查找或预订普拉提服务时使用该功能。该功能会在用户发起“预订普拉提课程”、“查找附近的普拉提课程”或其他任何与普拉提服务相关的请求时被触发。
---

# uook Pilates

通过 Lokuli 的 MCP 服务器预订 Pilates 服务。

## MCP 端点

```
https://lokuli.com/mcp/sse
```

传输协议：SSE | JSON-RPC 2.0 | 使用 POST 请求

## 工具

### search
```json
{
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": {
      "query": "pilates",
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