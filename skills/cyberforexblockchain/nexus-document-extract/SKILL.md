---
name: nexus-document-extract
description: "使用人工智能从非结构化文本文档中提取结构化数据（名称、日期、金额、实体）。返回包含提取字段的整洁 JSON 数据。"
version: 1.0.1
capabilities:
  - id: invoke-document-extract
    description: "Extract structured data (names, dates, amounts, entities) from unstructured text documents using AI. Returns clean JSON with extracted fields."
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
# NEXUS 文本提取器

> 在 Cardano 上运行的 NEXUS 代理即服务（Agent-as-a-Service）

## 使用场景

当你面对一段非结构化的文本（如发票、合同、电子邮件或报告）时，需要从中提取特定的数据（如名称、日期、金额和关键术语），并将其转换为结构化的 JSON 格式。

## 与其他工具的区别

与一般的文本摘要工具不同，该服务返回的是包含类型化字段的机器可读 JSON 数据，非常适合用于数据管道和自动化文档处理工作流程。

## 使用步骤

1. 将输入数据准备成 JSON 格式。
2. 向 NEXUS 的 API 端点发送 POST 请求，并在请求头中添加 `X-Payment-Proof` 字段。
3. 解析返回的结构化 JSON 数据。

### API 调用示例

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/original-services/document-extract \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: sandbox_test" \
  -d '{"text": "Invoice #1234 from Acme Corp. Due: March 15, 2026. Amount: $5,400.00 for consulting services.", "extract_fields": ["company", "date", "amount", "service"]}'
```

**API 端点：** `https://ai-service-hub-15.emergent.host/api/original-services/document-extract`
**请求方法：** POST
**请求头：**
- `Content-Type: application/json`
- `X-Payment-Proof: <masumi_payment_id>`（使用 `sandbox_test` 进行免费沙箱测试）

## 外部 API 端点

| URL | 请求方法 | 发送的数据 |
|-----|--------|-----------|
| `https://ai-service-hub-15.emergent.host/api/original-services/document-extract` | POST | 以 JSON 格式发送输入参数 |

## 安全性与隐私保护

- 所有请求均通过 HTTPS/TLS 协议加密传输至 `https://ai-service-hub-15.emergent.host`。
- 用户数据不会被永久存储，请求数据会在处理后被立即销毁。
- 支付验证采用 Cardano 上的 Masumi 协议（非托管式托管服务）。
- 该功能仅需要网络访问权限，无需文件系统或 shell 权限。

## 模型调用说明

该功能会调用 NEXUS 的 AI 服务 API，该 API 会在服务器端使用大型语言模型处理输入数据，并生成结构化的响应。您可以选择不安装此功能以拒绝使用相关服务。

## 信任声明

通过安装此功能，您的输入数据将被传输至 NEXUS（https://ai-service-hub-15.emergent.host）进行 AI 处理。所有支付操作均通过 Cardano 区块链完成（属于非托管式交易）。如需了解更多信息，请访问 [https://ai-service-hub-15.emergent.host](https://ai-service-hub-15.emergent.host) 查看相关文档和条款。仅在使用方信任 NEXUS 作为服务提供商的情况下才建议安装此功能。