---
name: nexus-data-profile
description: "数据集的统计分析与质量评估"
version: 1.0.0
capabilities:
  - id: invoke-data-profile
    description: "Statistical profiling and quality assessment of datasets"
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
# 数据分析工具

> Cardano 上的 NEXUS 代理即服务（Agent-as-a-Service） | 价格：0.20 美元/请求

## 使用场景

当您需要对数据集进行统计分析和质量评估时，请使用此工具。

## 使用步骤

1. 向 NEXUS API 端点发送 POST 请求，并附上您的输入数据。
2. 在请求头中添加 `X-Payment-Proof`（支付 ID 或 `sandbox_test` 用于测试）。
3. 解析 JSON 响应并获取结果。

### API 调用

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/original-services/data-profile \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: $NEXUS_PAYMENT_PROOF" \
  -d '{
  "input": "Example input for Data Profiler"
}'
```

**端点：** `https://ai-service-hub-15.emergent.host/api/original-services/data-profile`
**方法：** POST
**请求头：**
- `Content-Type: application/json`
- `X-Payment-Proof: <masumi_payment_id>`（使用 `sandbox_test` 进行免费测试）

## 外部接口

| URL | 方法 | 发送的数据 |
|-----|--------|-----------|
| `https://ai-service-hub-15.emergent.host/api/original-services/data-profile` | POST | 以 JSON 格式发送输入参数 |

## 安全性与隐私

- 所有数据均通过 HTTPS/TLS 协议传输至 `https://ai-service-hub-15.emergent.host`。
- 数据不会被永久存储；请求处理完成后会被立即删除。
- 支付验证通过 Cardano 区块链上的 Masumi 协议完成。
- 无需访问文件系统或执行 shell 命令。

## 模型调用说明

该工具会调用 NEXUS AI 服务 API，该 API 使用大型语言模型（如 GPT-5.2、Claude Sonnet 4.5、GPT-4o）来处理请求。AI 会在服务器端处理您的输入数据并返回结构化的响应。您也可以选择不安装此工具。

## 信任声明

使用此工具时，您的输入数据将发送至 NEXUS（https://ai-service-hub-15.emergent.host）进行 AI 处理。支付过程通过 Cardano 上的 Masumi 协议完成，且数据不会被第三方保管。仅当您信任 NEXUS 作为服务提供商时，请安装此工具。详情请访问 [https://ai-service-hub-15.emergent.host](https://ai-service-hub-15.emergent.host) 查看完整文档。

## 标签**

`机器学习`、`人工智能`、`免费试用`、`代理间通信`、`健康监控`、`预算管理`