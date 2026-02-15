---
name: book-web-developer
description: 通过 Lokuli MCP 预订网页开发服务。当用户需要寻找或预订网页开发人员时可以使用该功能。该功能会在收到诸如“预订网页开发人员”、“查找附近的网页开发人员”或任何与网页开发服务相关的请求时被触发。
---

# 乌克·韦乌开发服务

您可以通过 Lokuli 的 MCP 服务器预订网页开发服务。

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
      "query": "web-developer",
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