---
name: nexus-summarize
description: "在保持关键信息的同时，对长文档进行总结。"
version: 1.0.0
capabilities:
  - id: invoke-summarize
    description: "Summarize long documents while preserving key info"
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
# AI 数据摘要工具

> Cardano 上的 NEXUS 代理即服务（Agent-as-a-Service）| 价格：0.15 美元/次请求

## 使用场景

当您需要将长文本压缩成简短摘要时，请使用此工具。

## 使用步骤

1. 向 NEXUS API 端点发送 POST 请求，并附带您的输入数据。
2. 必须包含 `X-Payment-Proof` 头部字段（支付 ID 为 `masumi_payment_id`，用于测试时使用 `sandbox_test`）。
3. 解析 JSON 响应并返回结果。

### API 调用

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/original-services/summarize \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: $NEXUS_PAYMENT_PROOF" \
  -d '{"text": "Long article text here...", "format": "bullet_points"}'
```

**端点：** `https://ai-service-hub-15.emergent.host/api/original-services/summarize`
**方法：** POST
**头部字段：**
- `Content-Type: application/json`
- `X-Payment-Proof: <masumi_payment_id>` （免费测试时使用 `sandbox_test`）

## 外部接口

| URL | 方法 | 发送的数据 |
|-----|--------|-----------|
| `https://ai-service-hub-15.emergent.host/api/original-services/summarize` | POST | 输入参数以 JSON 格式发送 |

## 安全性与隐私保护

- 所有数据均通过 HTTPS/TLS 协议传输至 `https://ai-service-hub-15.emergent.host`。
- 数据不会被永久存储；请求处理完成后会被立即删除。
- 支付验证通过 Cardano 区块链上的 Masumi 协议完成。
- 无需访问文件系统或执行 shell 命令。

## 模型调用说明

该工具会调用 NEXUS AI 服务 API，该 API 使用 LLM 模型（GPT-5.2、Claude Sonnet 4.5、GPT-4o）来处理请求。AI 会在服务器端处理您的输入并返回结构化的结果。您也可以选择不安装此工具。

## 信任声明

使用此工具时，您的输入数据将被发送至 NEXUS（https://ai-service-hub-15.emergent.host）进行 AI 处理。支付过程通过 Cardano 上的 Masumi 协议完成，且 NEXUS 不会保管用户的资金。仅当您信任 NEXUS 作为服务提供商时，才建议安装此工具。详情请访问 [https://ai-service-hub-15.emergent.host](https://ai-service-hub-15.emergent.host) 查看完整文档。

## 标签**

`机器学习`、`人工智能`、`免费试用`、`代理间通信`、`健康监控`、`预算管理`