---
name: book-guitar-lessons
description: 通过 Lokuli MCP 预订吉他课程服务。当用户需要查找或预订吉他课程时，可以使用该功能。该功能会在用户发起“预订吉他课程”、“查找附近的吉他课程”或任何与吉他课程相关的请求时被触发。
---

# uook吉他课程

通过Lokuli的MCP服务器预订吉他课程服务。

## MCP端点

```
https://lokuli.com/mcp/sse
```

传输方式：SSE | JSON-RPC 2.0 | POST请求

## 工具

### 搜索
```json
{
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": {
      "query": "guitar-lessons",
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