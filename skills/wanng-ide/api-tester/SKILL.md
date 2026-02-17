---
name: api-tester
description: 执行结构化的 HTTP/HTTPS 请求（GET、POST、PUT、DELETE），支持自定义请求头和 JSON 请求体。可用于 API 测试、健康检查，或以编程方式与 REST 服务进行交互，而无需依赖 `curl`。
---
# API Tester

这是一个轻量级的、无需依赖任何外部库的HTTP客户端，专为OpenClaw设计。

## 使用方法

### 基本的GET请求

```javascript
const api = require('skills/api-tester');
const result = await api.request('GET', 'https://api.example.com/data');
console.log(result.status, result.data);
```

### 带有JSON请求体的POST请求

```javascript
const api = require('skills/api-tester');
const payload = { key: 'value' };
const headers = { 'Authorization': 'Bearer <token>' };
const result = await api.request('POST', 'https://api.example.com/submit', headers, payload);
```

### 返回格式

`request`函数返回一个Promise，该Promise的值会在请求完成时解析为：

```javascript
{
  status: 200,          // HTTP status code
  headers: { ... },     // Response headers
  data: { ... },        // Parsed JSON body (if applicable) or raw string
  raw: "...",           // Raw response body string
  error: "..."          // Error message if request failed (network error, timeout)
}
```

## 主要特性

- **零依赖**：仅使用Node.js内置的`http`和`https`模块。
- **自动解析JSON**：如果请求的`Content-Type`与JSON匹配，会自动将请求体序列化为字符串，并解析响应体。
- **超时支持**：默认超时时间为10秒，可配置。
- **错误处理**：遇到错误时返回结构化的错误对象，而不是直接抛出异常，从而确保程序的稳定运行。