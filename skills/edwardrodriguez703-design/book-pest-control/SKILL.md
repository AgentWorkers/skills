---
name: book-pest-control
description: 通过 Lokuli MCP 预订害虫控制服务。当用户需要查找或预订害虫控制服务时，可以使用该功能。该功能会在用户输入“预订害虫控制服务”、“查找附近的害虫控制服务”或其他相关请求时被触发。
---

# uook 害虫控制服务

通过 Lokuli 的 MCP 服务器预订害虫控制服务。

## MCP 端点

```
https://lokuli.com/mcp/sse
```

传输方式：SSE | JSON-RPC 2.0 | POST 请求

## 工具

### 搜索（Search）
```json
{
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": {
      "query": "pest-control",
      "zipCode": "90640",
      "maxResults": 20
    }
  }
}
```

### 检查可用性（Check Availability）
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

### 创建预订（Create Booking）
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