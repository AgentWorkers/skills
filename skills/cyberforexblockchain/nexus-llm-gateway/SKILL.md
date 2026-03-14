---
name: nexus-llm-gateway
description: "基于 Cardano 的智能多模型 AI 网关：该网关能够将用户输入的请求路由到最适合的 Large Language Model（LLM），包括 GPT-5.2、Claude Sonnet 4.5、GPT-4o、Claude Haiku 4.5 和 GPT-4o-mini，并提供自动回退机制。支持分层定价，输出格式兼容 OpenAI。用户可通过 Masumi 使用 ADA 进行支付。"
version: 1.0.0
capabilities:
  - id: invoke-llm-gateway
    description: "Smart multi-model AI gateway on Cardano. Routes prompts to the best LLM (GPT-5.2, Claude Sonnet 4.5, GPT-4o, Claude Haiku 4.5, GPT-4o-mini) with automatic fallback, tiered pricing, and OpenAI-compatible format. Pay with ADA via Masumi."
permissions:
  network: true
  filesystem: false
  shell: false
inputs:
  - name: prompt
    type: string
    required: true
    description: "The prompt to send"
  - name: tier
    type: string
    required: false
    description: "The tier parameter"
  - name: model
    type: string
    required: false
    description: "Optional: specific model override"
  - name: task_type
    type: string
    required: false
    description: "The task_type parameter"
  - name: messages
    type: array
    required: false
    description: "OpenAI-compatible messages array"
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
# LLM网关

> Cardano上的NEXUS代理即服务（Agent-as-a-Service） | 价格：0.10美元/请求

## 使用场景

当您需要通过一个端点调用任何大型语言模型（LLM，如GPT-5.2、Claude Sonnet 4.5、GPT-4o、Claude Haiku 4.5、GPT-4o-mini）时，请使用此服务。该服务支持基于级别的路由（经济型/标准型/高级型/自动型），并兼容OpenAI的消息格式。

## 使用步骤

1. 向NEXUS API端点发送POST请求，并附带您的输入数据。
2. 在请求头中添加`X-Payment-Proof`字段（使用`masumi_payment_id`进行支付验证，或使用`sandbox_test`进行测试）。
3. 解析JSON响应并返回结果。

### API调用

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/original-services/llm-gateway \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: $NEXUS_PAYMENT_PROOF" \
  -d '{"prompt": "Write a Python function to sort a list", "tier": "auto", "task_type": "code"}'
```

**端点：** `https://ai-service-hub-15.emergent.host/api/original-services/llm-gateway`
**方法：** POST
**请求头：**
- `Content-Type: application/json`
- `X-Payment-Proof: <masumi_payment_id>`（免费测试时使用`sandbox_test`）

## 外部端点

| URL | 方法 | 发送的数据 |
|-----|--------|-----------|
| `https://ai-service-hub-15.emergent.host/api/original-services/llm-gateway` | POST | 以JSON格式发送输入参数 |

## 安全性与隐私

- 所有数据均通过HTTPS/TLS协议传输至`https://ai-service-hub-15.emergent.host`。
- 数据不会被永久存储，请求处理完成后会被立即删除。
- 支付验证通过Cardano区块链上的Masumi协议完成。
- 无需访问文件系统或执行shell命令。

## 模型调用说明

此功能通过调用NEXUS AI服务API来使用大型语言模型（GPT-5.2、Claude Sonnet 4.5、GPT-4o）处理请求。AI会在服务器端处理您的输入并返回结构化的响应。您也可以选择不安装此功能。

## 信任声明

使用此功能意味着您的输入数据将被发送至NEXUS（https://ai-service-hub-15.emergent.host）进行AI处理。支付过程通过Cardano上的Masumi协议实现，且NEXUS不负责资金保管。仅当您信任NEXUS作为服务提供商时，才建议安装此功能。详情请访问https://ai-service-hub-15.emergent.host。

## 标签

`llm`, `ai`, `gateway`, `multi-model`, `gpt`, `claude`, `router`, `cardano`