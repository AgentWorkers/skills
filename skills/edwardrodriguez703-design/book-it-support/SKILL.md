---
name: book-it-support
description: 通过 Lokuli MCP 预订 IT 支持服务。当用户需要查找或预订 IT 支持服务时，可以使用该功能。该功能会在用户发起“预订 IT 支持”、“查找附近的 IT 支持服务”或其他任何与 IT 支持服务相关的请求时被触发。
---

# uook it 支持

您可以通过 Lokuli 的 MCP 服务器来预订服务。

## MCP 端点

```
https://lokuli.com/mcp/sse
```

传输协议：SSE | JSON-RPC 2.0 | 支持 POST 请求

## 工具

### 搜索
```json
{
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": {
      "query": "it-support",
      "zipCode": "90640",
      "maxResults": 20
    }
  }
}
```

### 检查可用性
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

### 创建预订
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