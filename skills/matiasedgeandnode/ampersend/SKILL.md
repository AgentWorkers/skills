---
name: ampersend
description: 通过Ampersend钱包为支持x402支付的应用程序提供的CLI工具
metadata:
  {
    "openclaw":
      { "requires": { "bins": ["npx"], "env": ["AMPERSEND_AGENT_KEY"] }, "primaryEnv": "AMPERSEND_AGENT_KEY" },
  }
---
# ampersend CLI

这是一个用于构建和使用Ampersend智能账户钱包与x402支付功能应用程序进行交互的命令行工具（CLI）。

## 先决条件

使用以下任一格式设置钱包凭证：

```bash
# Combined format (recommended)
export AMPERSEND_AGENT_KEY="0xaddress:::0xsession_key"

# Or separate variables
export AMPERSEND_SMART_ACCOUNT_ADDRESS="0x..."
export AMPERSEND_SESSION_KEY="0x..."
```

（可选：）

```bash
export AMPERSEND_NETWORK="base"                 # Network (default: base)
export AMPERSEND_API_URL="https://..."          # Custom Ampersend API URL
```

## 支持的网络

- `base`（默认）
- `base-sepolia`

---

## fetch

该工具用于向支持x402支付协议的API发送HTTP请求。当遇到HTTP 402 “Payment Required”（需要支付）的响应时，它会自动使用配置好的Ampersend智能账户钱包创建并签署支付请求。

### 使用场景

在以下情况下，应使用`ampersend fetch`代替`curl`：

- API使用了x402支付协议
- 接收到HTTP 402 “Payment Required”响应
- 需要通过加密方式支付API访问费用

### 不适用场景

- 不涉及x402支付的普通HTTP请求（请使用`curl`）
- 使用传统API密钥、OAuth或其他认证方式的API
- 流式响应（不支持）
- 需要对支付授权进行细粒度控制的情况（请直接使用SDK）

### 使用方法

#### 基本GET请求

```bash
npx --yes -p @ampersend_ai/ampersend-sdk@beta ampersend fetch https://api.example.com/paid-endpoint
```

#### 带JSON请求体的POST请求

```bash
npx --yes -p @ampersend_ai/ampersend-sdk@beta ampersend fetch \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"query": "your data"}' \
  https://api.example.com/paid-endpoint
```

#### 查看支付要求（无需支付）

使用`--inspect`选项可以预览所需的支付信息，而无需实际执行支付操作：

```bash
npx --yes -p @ampersend_ai/ampersend-sdk@beta ampersend fetch --inspect https://api.example.com/paid-endpoint
```

#### 调试模式

将支付流程的详细JSONL日志输出到标准错误流（stderr）：

```bash
npx --yes -p @ampersend_ai/ampersend-sdk@beta ampersend fetch --debug https://api.example.com/paid-endpoint
```

### 选项说明

| 选项                        | 描述                                                                                          |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `-X, --method <method>`     | HTTP请求方法（默认为GET）                                                                                   |
| `-H, --header <header>`    | HTTP请求头（格式：`Key: Value`），可以多次使用                                      |
| `-d, --data <data>`       | 请求体数据                                                                                         |
| `--inspect`         | 预览支付要求（无需支付）                                                                                   |
| `--raw`          | 输出原始响应体（而非JSON格式）                                                                                   |
| `--headers`        | 在JSON输出中包含响应头                                                                                   |
| `--debug`         | 将JSONL日志输出到标准错误流（stderr），便于调试                                                                                   |

### 工作原理

1. 向目标URL发送HTTP请求。
2. 如果服务器返回HTTP 402 “Payment Required”响应：
   - 从响应中解析支付要求。
   - 使用用户的智能账户创建支付请求。
   - 用会话密钥签署支付请求。
   - 重新发送带有支付信息的请求。
3. 返回成功的响应结果。

### 错误处理

如果未配置钱包，将会出现以下错误信息：

```
Error: Wallet not configured.

Set the following environment variables:
  AMPERSEND_SMART_ACCOUNT_ADDRESS - Your smart account address
  AMPERSEND_SESSION_KEY - Session key private key
```

### 示例

#### 查询已付费的AI API

```bash
npx --yes -p @ampersend_ai/ampersend-sdk@beta ampersend fetch \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, world!"}' \
  https://ai-api.example.com/chat
```

#### 获取高级数据

```bash
npx --yes -p @ampersend_ai/ampersend-sdk@beta ampersend fetch https://data-api.example.com/premium/market-data
```

#### 检查API是否需要支付

```bash
npx --yes -p @ampersend_ai/ampersend-sdk@beta ampersend fetch --inspect https://api.example.com/endpoint
```

#### 原始响应体

```bash
npx --yes -p @ampersend_ai/ampersend-sdk@beta ampersend fetch --raw https://api.example.com/paid-endpoint
```

### 输出格式

默认情况下，`ampersend fetch`会输出结构化的JSON响应。请务必首先检查`ok`字段以确认请求是否成功。

#### 成功响应

```json
{
  "ok": true,
  "data": {
    "status": 200,
    "body": "{\"result\": \"data\"}",
    "payment": { ... }
  }
}
```

使用`--headers`选项可以包含响应头：

```json
{
  "ok": true,
  "data": {
    "status": 200,
    "headers": { "content-type": "application/json" },
    "body": "..."
  }
}
```

#### 查看响应内容

```json
{
  "ok": true,
  "data": {
    "url": "https://api.example.com/endpoint",
    "paymentRequired": true,
    "requirements": {
      "scheme": "exact",
      "network": "base",
      "maxAmountRequired": "1000000",
      "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      "payTo": "0x..."
    }
  }
}
```

结合`--headers`和`--inspect`选项，可以在输出中同时显示响应头和详细内容。

#### 错误响应

```json
{
  "ok": false,
  "error": "Wallet not configured."
}
```