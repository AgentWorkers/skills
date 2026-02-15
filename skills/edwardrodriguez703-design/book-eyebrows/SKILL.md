---
name: book-eyebrows
description: 通过 Lokuli MCP 预订眉毛服务。当用户需要寻找或预订眉毛服务时，可以使用该功能。该功能会在用户发起“预订眉毛”、“查找附近的眉毛服务”等相关请求时被触发。
---

# 为书籍添加眉毛效果

您可以通过 Lokuli 的 MCP 服务器来为书籍添加眉毛效果。

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
      "query": "eyebrows",
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