---
name: book-dance-lessons
description: 通过 Lokuli MCP 提供舞蹈课程预订服务。当用户需要查找或预订舞蹈课程时，可以使用该服务。该服务会在用户发起诸如“预订舞蹈课程”、“查找附近的舞蹈课程”或任何与舞蹈课程相关的请求时被触发。
---

# 舞蹈课程预订服务

通过 Lokuli 的 MCP 服务器预订舞蹈课程。

## MCP 端点

```
https://lokuli.com/mcp/sse
```

传输协议：SSE | JSON-RPC 2.0 | 使用 POST 请求

## 工具

### 搜索
```json
{
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": {
      "query": "dance-lessons",
      "zipCode": "90640",
      "maxResults": 20
    }
  }
}
```

### 检查课程可用性
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