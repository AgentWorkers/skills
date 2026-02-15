---
name: book-fitness
description: 通过 Lokuli MCP 预订健身服务。当用户需要查找和预订健身课程时使用该功能。该功能会在用户输入“预订健身课程”、“查找附近的健身场所”或其他任何与健身服务相关的请求时被触发。
---

# uook健身

通过Lokuli的MCP服务器预订健身服务。

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
      "query": "fitness",
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