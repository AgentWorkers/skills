---
name: http-request-builder
description: Build and test HTTP requests with CLI interface: headers, auth, body, cookies, with history and templates.
version: 1.0.0
author: skill-factory
metadata:
  openclaw:
    requires:
      bins:
        - python3
      python:
        - requests
---

# HTTP 请求构建器

## 功能介绍

这是一个命令行（CLI）工具，用于构建、测试和保存 HTTP 请求。支持自定义请求头、身份验证、请求体以及 Cookie 的设置。用户可以将请求保存为模板以供后续使用，并记录所有的 HTTP 请求历史记录。

**主要功能：**
- **发送 HTTP 请求**：支持 GET、POST、PUT、DELETE、PATCH、HEAD、OPTIONS 等方法
- **设置自定义请求头**：支持键值对格式
- **添加身份验证**：支持基本身份验证（Basic Auth）和 bearer token 身份验证
- **包含请求体**：支持 JSON、表单数据或原始文本格式
- **管理请求中的 Cookie**
- **将请求保存为模板**：以 JSON 文件的形式保存，便于重复使用
- **加载并执行保存的模板**
- **交互式模式**：允许用户逐步构建请求
- **命令行模式**：支持脚本编写和自动化操作
- **请求历史记录**：记录用户的最近请求操作

## 使用场景

- 需要在终端中快速测试 REST API 端点
- 需要保存和复用复杂的 API 请求
- 更倾向于使用 CLI 工具而非 Postman 等图形化工具
- 需要在脚本中自动化 API 测试
- 需要与团队成员共享 API 请求配置
- 在调试 API 问题时需要重新发送请求

## 使用方法

基本命令如下：
```bash
# Send a GET request
python3 scripts/main.py get https://api.example.com/data

# Send a POST request with JSON body
python3 scripts/main.py post https://api.example.com/api \
  --header "Content-Type: application/json" \
  --body '{"name": "test", "value": 123}'

# Send with Basic authentication
python3 scripts/main.py get https://api.example.com/secure \
  --auth basic --username admin --password secret

# Send with Bearer token
python3 scripts/main.py get https://api.example.com/secure \
  --auth bearer --token "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"

# Save request as template
python3 scripts/main.py post https://api.example.com/api \
  --header "Content-Type: application/json" \
  --body '{"name": "test"}' \
  --save-template my-request

# Load and execute template
python3 scripts/main.py template my-request

# Interactive mode
python3 scripts/main.py interactive

# View request history
python3 scripts/main.py history

# Clear history
python3 scripts/main.py history --clear
```

## 示例

### 示例 1：简单的 GET 请求

```bash
python3 scripts/main.py get https://jsonplaceholder.typicode.com/posts/1
```

**输出结果：**
```
Response Status: 200 OK
Response Headers:
  content-type: application/json; charset=utf-8
  ...

Response Body:
{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
  "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
}
```

### 示例 2：带有 JSON 请求体和请求头的 POST 请求

```bash
python3 scripts/main.py post https://jsonplaceholder.typicode.com/posts \
  --header "Content-Type: application/json" \
  --header "X-API-Key: my-secret-key" \
  --body '{
    "title": "foo",
    "body": "bar",
    "userId": 1
  }'
```

### 示例 3：保存请求模板以供重复使用

```bash
# Save template
python3 scripts/main.py post https://api.example.com/users \
  --header "Content-Type: application/json" \
  --header "Authorization: Bearer token123" \
  --body '{"name": "New User"}' \
  --save-template create-user

# Use template later
python3 scripts/main.py template create-user

# List all templates
python3 scripts/main.py templates
```

### 示例 4：交互式模式

在交互式模式下，用户可以按照以下步骤构建请求：
1. 选择 HTTP 方法
2. 输入请求 URL
3. 配置请求头
4. 设置身份验证信息
5. 输入请求体
6. 发送请求并查看结果

## 系统要求

- Python 3.x
- `requests` 库（已自动安装或通过 pip 安装）

**安装缺失的依赖库：**
```bash
pip3 install requests
```

## 限制

- 该工具为命令行工具，不提供图形化界面
- 请求历史记录和模板保存在 `~/.http-request-builder/` 目录下的简单 JSON 文件中
- 身份验证支持有限（仅支持基本身份验证和 bearer token）
- 不支持 OAuth、API 密钥或复杂的身份验证流程
- Cookie 仅在单次请求中有效，无法在会话间持久化
- 不支持代理配置
- 不提供 SSL 证书验证功能
- 不支持 WebSocket 或流式响应
- 不支持响应验证或测试断言等高级功能
- 默认情况下，请求历史记录最多保存 100 条记录
- 模板为未加密的 JSON 文件
- 模板中不支持环境变量
- 性能受 `requests` 库限制
- 大型响应内容可能会被截断显示
- 不支持上传多部分表单数据
- 不提供内置的速率限制或重试机制
- 不支持 HTTP/2 或 HTTP/3 协议

## 文件结构

工具的数据存储在 `~/.http-request-builder/` 目录下：
- `templates/`：保存的请求模板（JSON 文件）
- `history.json`：请求历史记录日志
- `config.json`：配置信息（如有）

## 错误处理

- 错误的 URL 会返回详细的错误信息
- 网络请求超时后会给出提示
- JSON 解析错误会显示出问题所在
- 如果找不到模板，会提示相应的错误信息
- 身份验证失败时会提示正确的格式要求

## 贡献方式

该工具由 Skill Factory 开发。如有问题或改进建议，请通过 OpenClaw 项目进行反馈。