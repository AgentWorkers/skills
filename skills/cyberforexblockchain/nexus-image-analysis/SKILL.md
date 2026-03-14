---
name: nexus-image-analysis
description: "全面的图像理解能力——包括物体识别、文本识别以及颜色分析"
version: 1.0.0
capabilities:
  - id: invoke-image-analysis
    description: "Comprehensive image understanding - objects, text, colors"
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
# 图像分析 API

> Cardano 上的 NEXUS 代理即服务（Agent-as-a-Service）| 价格：0.35 美元/请求

## 使用场景

当您需要全面理解图像内容（包括物体、文本和颜色信息）时，请使用此服务。

## 使用步骤

1. 向 NEXUS API 端点发送 POST 请求，并附上您的输入数据。
2. 在请求头中添加 `X-Payment-Proof`（支付凭证）字段（使用 `masumi_payment_id` 表示支付，或使用 `sandbox_test` 进行免费测试）。
3. 解析 JSON 格式的响应并获取处理结果。

### API 调用示例

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/original-services/image-analysis \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: $NEXUS_PAYMENT_PROOF" \
  -d '{
  "input": "Example input for Image Analysis API"
}'
```

**端点：** `https://ai-service-hub-15.emergent.host/api/original-services/image-analysis`
**方法：** POST
**请求头：**
- `Content-Type: application/json`
- `X-Payment-Proof: <masumi_payment_id>` （免费测试时使用 `sandbox_test`）

## 外部接口信息

| URL | 方法 | 发送的数据 |
|-----|--------|-----------|
| `https://ai-service-hub-15.emergent.host/api/original-services/image-analysis` | POST | 以 JSON 格式发送输入参数 |

## 安全性与隐私政策

- 所有数据均通过 HTTPS/TLS 协议传输至 `https://ai-service-hub-15.emergent.host`。
- 数据不会被永久存储，请求处理完成后会被立即删除。
- 支付凭证会通过 Cardano 区块链上的 Masumi 协议进行验证。
- 无需访问文件系统或执行 shell 命令。

## 模型调用说明

此功能会调用 NEXUS 的 AI 服务 API，该 API 使用大型语言模型（如 GPT-5.2、Claude Sonnet 4.5、GPT-4o）来处理请求。AI 会在服务器端处理您的输入数据并返回结构化的响应。您也可以选择不安装此功能。

## 信任声明

使用此功能时，您的输入数据将会被发送至 NEXUS（https://ai-service-hub-15.emergent.host）进行 AI 处理。支付过程通过 Cardano 上的 Masumi 协议完成，且数据不会由 NEXUS 保管。仅当您信任 NEXUS 作为服务提供商时，才建议安装此功能。详情请访问 [https://ai-service-hub-15.emergent.host](https://ai-service-hub-15.emergent.host) 查看完整文档。

## 标签**

`机器学习`（Machine Learning）、`人工智能`（Artificial Intelligence）、`免费试用`（Free Trial）、`代理间通信`（Agent-to-Agent）、`健康监测`（Health Monitoring）、`预算管理`（Budget Management）