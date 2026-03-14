---
name: nexus-multi-model
description: "将这些提示引导至最佳的人工智能模型"
version: 1.0.0
capabilities:
  - id: invoke-multi-model
    description: "Routes prompts to the best AI model"
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
# 多模型AI路由器

> Cardano上的NEXUS代理即服务（Agent-as-a-Service） | 价格：0.15美元/请求

## 使用场景

当您需要根据任务类型和成本优化来将请求路由到最合适的AI模型时，请使用此服务。

## 使用步骤

1. 向NEXUS API端点发送POST请求，并附带您的输入数据。
2. 在请求头中添加`X-Payment-Proof`字段（支付ID：`masumi_payment_id`；测试用途：`sandbox_test`）。
3. 解析JSON响应并返回结果。

### API调用示例

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/original-services/multi-model \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: $NEXUS_PAYMENT_PROOF" \
  -d '{"prompt": "Explain machine learning to a beginner", "optimize_for": "balanced"}'
```

**端点：** `https://ai-service-hub-15.emergent.host/api/original-services/multi-model`
**方法：** POST
**请求头：**
- `Content-Type: application/json`
- `X-Payment-Proof: <masumi_payment_id>`（免费测试时使用`sandbox_test`）

## 外部接口信息

| URL | 方法 | 发送的数据 |
|-----|--------|-----------|
| `https://ai-service-hub-15.emergent.host/api/original-services/multi-model` | POST | 以JSON格式发送输入参数 |

## 安全性与隐私保护

- 所有数据均通过HTTPS/TLS协议传输至`https://ai-service-hub-15.emergent.host`。
- 数据不会被永久存储，请求处理完成后会被立即删除。
- 支付验证通过Cardano区块链上的Masumi协议完成。
- 无需访问文件系统或执行shell命令。

## 模型调用说明

该服务会调用NEXUS AI服务API，该API使用大语言模型（如GPT-5.2、Claude Sonnet 4.5、GPT-4o）来处理请求。AI会在服务器端处理您的输入并返回结构化的响应。您可以选择不安装此服务以拒绝使用相关功能。

## 信任声明

使用本服务意味着您的输入数据将被发送至NEXUS（https://ai-service-hub-15.emergent.host）进行AI处理。支付过程通过Cardano上的Masumi协议实现，且NEXUS不负责资金保管。仅在使用者信任NEXUS作为服务提供商的情况下才建议安装此服务。详情请访问：https://ai-service-hub-15.emergent.host。

## 标签

`机器学习`（Machine Learning）、`人工智能`（Artificial Intelligence）、`免费试用`（Free Trial）、`代理间通信`（Agent-to-Agent）、`健康监控`（Health Monitoring）、`预算管理`（Budget Management）