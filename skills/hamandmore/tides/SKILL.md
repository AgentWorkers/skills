---
name: tides
description: 访问全球海洋潮汐模型。该模型提供的功能包括：在指定日期/时间/地点获取潮汐高度、潮汐极值数据以及网格天气信息。
---

# Tides JSON-RPC 接口使用指南

请按照以下指南直接调用已部署的 API：

- **基础 URL**: `https://hamandmore.net/api/harmonics/mcp`
- **请求方法**: `POST`
- **内容类型**: `application/json`
- **协议**: JSON-RPC 2.0 请求封装

## **身份验证**

您可以选择以下身份验证方式之一：

- **匿名访问**: 不需要设置 `Authorization` 头部（适用于免费 tier 的使用限制）
- **基于令牌的访问**: 添加 `Authorization: Bearer <token>` 或 `Authorization: Basic <token>`
- 如果需要更高的使用权限，请发送电子邮件至 `hamandmore@gmail.com` 申请身份验证。

**注意**:
- 这里的 `Basic` 表示令牌前缀，并非 RFC 标准的 Base64 编码方式。
- 令牌不需要是有效的 Base64 编码格式。

## **JSON-RPC 请求封装**

每次请求时都必须包含以下字段：
- `id`: 客户端标识符（任意字符串）
- `method`: 可以是 `initialize`, `tools/list`, `tools/call` 中的一个
- `params`: 一个对象（具体格式取决于所请求的方法）

## **快速入门命令**

- **初始化**:  
  ```bash
  ```bash
curl -sS -X POST https://hamandmore.net/api/harmonics/mcp \
  -H 'content-type: application/json' \
  --data '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}'
```
  ```

- **列出所有工具**:  
  ```bash
  ```bash
curl -sS -X POST https://hamandmore.net/api/harmonics/mcp \
  -H 'content-type: application/json' \
  --data '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
```
  ```

- **列出工具（需要身份验证）**:  
  ```bash
  ```bash
curl -sS -X POST https://hamandmore.net/api/harmonics/mcp \
  -H 'content-type: application/json' \
  -H 'authorization: Bearer YOUR_TOKEN' \
  --data '{"jsonrpc":"2.0","id":3,"method":"tools/list","params":{}}'
```
  ```

## **工具调用模式**

所有工具调用都遵循相同的格式：
```bash
```json
{
  "jsonrpc": "2.0",
  "id": 10,
  "method": "tools/call",
  "params": {
    "name": "TOOL_NAME",
    "arguments": {}
  }
}
```
```

## **Curl 示例**

### 1) 获取当前时间 (`tides_time`):
```bash
curl -X POST \
  -H "Authorization: Bearer <token>" \
  -d '{"id": "my_client_id", "method": "tides_time"}' \
  https://hamandmore.net/api/harmonics/mcp
```

### 2) 获取单个潮汐数据 (`tides_single`):
```bash
curl -X POST \
  -H "Authorization: Bearer <token>" \
  -d '{"id": "my_client_id", "method": "tides_single", "param": "tide_id"}' \
  https://hamandmore.net/api/harmonics/mcp
```

### 3) 获取潮汐极值数据 (`tides_extrema`):
```bash
curl -X POST \
  -H "Authorization: Bearer <token>" \
  -d '{"id": "my_client_id", "method": "tides_extrema", "param": "tide_id"}' \
  https://hamandmore.net/api/harmonics/mcp
```

### 4) 获取天气数据 (`weather_met`):
```bash
curl -X POST \
  -H "Authorization: Bearer <token>" \
  -d '{"id": "my_client_id", "method": "tides_met", "param": "weather_point_id"}' \
  https://hamandmore.net/api/harmonics/mcp
```

## **响应格式**

成功响应包含以下内容：
- `result.content[0].text`: 结果以字符串形式返回
- `result.structuredContent`: 结果以对象形式返回（更推荐这种方式）

错误信息会使用 JSON-RPC 的 `error` 状态码表示：
- `-32602`: 参数无效
- `-32601`: 方法未找到
- `-32603`: 服务器或工具出现异常