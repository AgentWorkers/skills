---
name: nexus-error-explain
description: "将任何错误信息、堆栈跟踪或异常情况粘贴出来，我们会提供用通俗易懂的语言解释问题的根本原因，并给出相应的修复建议。"
version: 1.0.1
capabilities:
  - id: invoke-error-explain
    description: "Paste any error message, stack trace, or exception and get a plain-English explanation with root cause analysis and fix suggestions."
permissions:
  network: true
  filesystem: false
  shell: false
inputs:
  - name: input
    type: string
    required: true
    description: "The input data or query"
outputs:
  type: object
  properties:
    result:
      type: string
      description: "The processed result"
requires:
  env: [NEXUS_PAYMENT_PROOF]
metadata: '{"openclaw":{"emoji":"\u26a1","requires":{"env":["NEXUS_PAYMENT_PROOF"]},"primaryEnv":"NEXUS_PAYMENT_PROOF"}}'
---
# NEXUS 错误解析器

> Cardano 平台上的 NEXUS 代理即服务（Agent-as-a-Service）

## 使用场景

当您在任何编程语言中遇到难以理解的错误信息、堆栈跟踪或异常时，需要了解问题的根源并找到解决方法。

## 产品特点

- 支持 50 多种语言和框架的错误解析；
- 可识别错误的根本原因，解释错误发生的原因，并提供可直接复用的修复代码；
- 支持通过 POST 请求发送数据，请求头中需包含 `X-Payment-Proof` 字段。

## 使用步骤

1. 将输入数据准备为 JSON 格式；
2. 向 NEXUS 的 API 端点发送 POST 请求，并在请求头中添加 `X-Payment-Proof` 字段；
3. 解析返回的 JSON 数据。

### API 调用示例

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/original-services/error-explain \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: sandbox_test" \
  -d '{"error": "TypeError: Cannot read properties of undefined (reading 'map')", "language": "javascript", "context": "React component rendering a list from API response"}'
```

**API 端点：** `https://ai-service-hub-15.emergent.host/api/original-services/error-explain`
**请求方法：** POST
**请求头：**
- `Content-Type: application/json`
- `X-Payment-Proof: <masumi_payment_id>`（免费沙箱测试请使用 `sandbox_test`）

## 外部 API 端点

| URL | 请求方法 | 发送的数据 |
|-----|--------|-----------|
| `https://ai-service-hub-15.emergent.host/api/original-services/error-explain` | POST | 以 JSON 格式发送输入参数 |

## 安全性与隐私政策

- 所有请求均通过 HTTPS/TLS 协议加密传输至 `https://ai-service-hub-15.emergent.host`；
- 用户数据不会被永久存储，请求数据会在处理后立即销毁；
- 支付验证采用 Cardano 平台上的 Masumi 协议（非托管式托管服务）；
- 该功能仅需要网络访问权限，无需文件系统或 shell 权限。

## 注意事项

该功能会调用 NEXUS 的 AI 服务 API，该 API 会在服务器端使用大型语言模型处理您的输入数据。AI 会根据输入生成响应并返回结构化结果。您可以选择不安装此功能以规避相关风险。

## 信任声明

安装此功能后，您的输入数据将会被传输至 NEXUS（https://ai-service-hub-15.emergent.host）进行 AI 处理。所有支付操作均通过 Cardano 区块链完成（非托管式）。如需了解更多信息，请访问 [https://ai-service-hub-15.emergent.host](https://ai-service-hub-15.emergent.host) 查看相关文档和条款。只有在信任 NEXUS 作为服务提供商的情况下，才建议安装此功能。