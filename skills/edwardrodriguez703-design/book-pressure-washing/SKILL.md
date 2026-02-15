---
name: book-pressure-washing
description: 通过 Lokuli MCP 预订高压清洗服务。当用户需要查找或预订高压清洗服务时，可以使用此功能。该功能会在用户输入类似“预订高压清洗服务”、“查找附近的高压清洗服务”或任何与高压清洗服务相关的请求时被触发。
---

# 书籍高压清洗服务

您可以通过 Lokuli 的 MCP 服务器预订书籍高压清洗服务。

## MCP 端点

```
https://lokuli.com/mcp/sse
```

传输协议：SSE | JSON-RPC 2.0 | 使用 POST 请求

## 工具

### 搜索（Search）
```json
{
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": {
      "query": "pressure-washing",
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