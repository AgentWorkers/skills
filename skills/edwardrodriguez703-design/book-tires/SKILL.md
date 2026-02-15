---
name: book-tires
description: 通过 Lokuli MCP 预订轮胎服务。当用户需要查找和预订轮胎时，可以使用此功能。该功能会在用户发起“预订轮胎”、“查找附近的轮胎”或任何与轮胎服务相关的请求时被触发。
---

# 更换轮胎服务

您可以通过 Lokuli 的 MCP 服务器来预订轮胎更换服务。

## MCP 端点

```
https://lokuli.com/mcp/sse
```

传输协议：SSE | JSON-RPC 2.0 | 使用 POST 请求

## 工具

### 搜索轮胎（search）
```json
{
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": {
      "query": "tires",
      "zipCode": "90640",
      "maxResults": 20
    }
  }
}
```

### 查看轮胎可用性（check_availability）
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

### 预订轮胎更换服务（create_booking）
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