---
name: api-endpoint-tester
description: 这是一个命令行工具（CLI），用于测试 REST API 端点，支持使用多种 HTTP 方法、请求头（headers）以及不同的请求数据（payloads）。
version: 1.0.0
author: skill-factory
metadata:
  openclaw:
    requires:
      bins:
        - python3
      packages:
        - requests
---
# API端点测试工具

## 功能介绍

这是一个简单的命令行工具（CLI），用于向REST API端点发送HTTP请求并验证响应。支持GET、POST、PUT、DELETE、PATCH方法，同时支持自定义请求头和请求体（JSON或表单数据）。

## 使用场景

- 需要手动或通过脚本测试API端点
- 需要验证HTTP状态码和响应格式
- 在调试API集成时需要快速发送请求
- 需要检查某个端点是否可访问以及响应是否正确

## 使用方法

- 发送基本的GET请求：
  ```
  python3 scripts/main.py run --url "https://api.example.com/users" --method GET
  ```

- 发送带有JSON请求体的POST请求：
  ```
  python3 scripts/main.py run --url "https://api.example.com/users" --method POST --body '{"name": "John", "email": "john@example.com"}'
  ```

- 使用自定义请求头：
  ```
  python3 scripts/main.py run --url "https://api.example.com/users" --method GET --headers '{"Authorization": "Bearer token123"}'
  ```

## 示例

### 示例1：简单的GET请求

```bash
python3 scripts/main.py run --url "https://jsonplaceholder.typicode.com/posts/1" --method GET
```

### 示例2：带有数据验证的POST请求

```bash
python3 scripts/main.py run --url "https://jsonplaceholder.typicode.com/posts" --method POST --body '{"title": "foo", "body": "bar", "userId": 1}' --expected-status 201
```

## 系统要求

- Python 3.x
- `requests`库（如果未安装，请通过pip安装）

## 限制

- 该工具仅作为命令行工具使用，不支持自动集成
- 不支持WebSocket或流式API端点
- 仅支持HTTP/HTTPS协议（不支持gRPC、GraphQL等）
- 除了请求头之外，不提供内置的身份验证机制
- 不支持保存测试用例或历史记录（每次仅执行一个请求）
- 默认超时时间为10秒