---
name: book-painter
description: 通过 Lokuli MCP 提供画家预约服务。当用户需要寻找或预约画家时，可以使用该服务。该服务会在用户发出“预约画家”、“查找附近的画家”或任何与画家相关的请求时被触发。
---

# 图书装帧服务

通过 Lokuli 的 MCP 服务器提供图书装帧服务。

## MCP 端点

```
https://lokuli.com/mcp/sse
```

传输协议：SSE | JSON-RPC 2.0 | 支持 POST 请求

## 工具

### 搜索功能
```json
{
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": {
      "query": "painter",
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

### 创建预约
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