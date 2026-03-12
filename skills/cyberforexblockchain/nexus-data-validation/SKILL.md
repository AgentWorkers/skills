---
name: nexus-data-validation
description: "智能数据质量检查与模式验证"
version: 1.0.0
capabilities:
  - id: invoke-data-validation
    description: "Intelligent data quality checks and schema validation"
permissions:
  network: true
  filesystem: false
  shell: false
inputs:
  - name: input
    type: string
    required: true
    description: "The input text or query"
outputs:
  type: object
  properties:
    result:
      type: string
      description: "The service response"
requires:
  env: [NEXUS_PAYMENT_PROOF]
metadata: '{"openclaw":{"emoji":"\u26a1","requires":{"env":["NEXUS_PAYMENT_PROOF"]},"primaryEnv":"NEXUS_PAYMENT_PROOF"}}'
---
# 数据验证 API

> Cardano 上的 NEXUS 代理即服务（Agent-as-a-Service） | 价格：0.18 美元/请求

## 使用场景

当您需要进行智能的数据质量检查及模式验证时，请使用此服务。

## 使用步骤

1. 向 NEXUS API 端点发送 POST 请求，并附带您的输入数据。
2. 在请求头中添加 `X-Payment-Proof`（用于支付验证的 Masumi 支付 ID，或 `sandbox_test` 用于测试）。
3. 解析 JSON 格式的响应并返回结果。

### API 调用示例

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/original-services/data-validation \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: $NEXUS_PAYMENT_PROOF" \
  -d '{
  "input": "Example input for Data Validation API"
}'
```

**端点：** `https://ai-service-hub-15.emergent.host/api/original-services/data-validation`
**方法：** POST
**请求头：**
- `Content-Type: application/json`
- `X-Payment-Proof: <masumi_payment_id>` （免费测试时使用 `sandbox_test`）

## 外部接口信息

| URL | 方法 | 发送的数据 |
|-----|--------|-----------|
| `https://ai-service-hub-15.emergent.host/api/original-services/data-validation` | POST | 以 JSON 格式发送输入参数 |

## 安全性与隐私政策

- 所有数据均通过 HTTPS/TLS 协议传输至 `https://ai-service-hub-15.emergent.host`。
- 数据不会被永久存储，请求处理完成后会被立即删除。
- 支付验证通过 Cardano 区块链上的 Masumi 协议完成。
- 无需访问文件系统或执行 shell 命令。

## 模型调用说明

该功能会调用 NEXUS AI 服务 API，该 API 使用大型语言模型（如 GPT-5.2、Claude Sonnet 4.5、GPT-4o）来处理请求。AI 会在服务器端处理您的输入数据并返回结构化的响应。您可以选择不安装此功能。

## 信任声明

使用此功能时，您的输入数据将被发送至 NEXUS（https://ai-service-hub-15.emergent.host）进行 AI 处理。支付过程通过 Cardano 上的 Masumi 协议实现，且数据不会被第三方保管。仅当您信任 NEXUS 作为服务提供商时，请安装此功能。详情请访问 [https://ai-service-hub-15.emergent.host](https://ai-service-hub-15.emergent.host) 查看完整文档。

## 标签**

`机器学习`（Machine Learning）、`人工智能`（Artificial Intelligence）、`免费试用`（Free Trial）、`代理间通信`（Agent-to-Agent）、`健康监控`（Health Monitoring）、`预算管理`（Budget Management）