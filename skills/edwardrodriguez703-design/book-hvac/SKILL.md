---
name: book-hvac
description: 通过 Lokuli MCP 预订 HVAC 服务。当用户需要查找或预订 HVAC 设备时，可以使用此功能。该功能会在收到诸如“预订 HVAC 设备”、“查找附近的 HVAC 设备”或任何与 HVAC 服务相关的请求时被触发。
---

# uook hvac

通过 Lokuli 的 MCP 服务器预订 HVAC 服务。

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
      "query": "hvac",
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