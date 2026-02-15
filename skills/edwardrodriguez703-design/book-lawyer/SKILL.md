---
name: book-lawyer
description: 通过 Lokuli MCP 预订律师服务。当用户需要寻找或预约律师时，可以使用此功能。该功能会在用户输入类似“预约律师”、“查找附近的律师”或任何与律师服务相关的请求时被触发。
---

# 使用律师服务

您可以通过 Lokuli 的 MCP 服务器来预约律师服务。

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
      "query": "lawyer",
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

### 创建预约（Create Booking）
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