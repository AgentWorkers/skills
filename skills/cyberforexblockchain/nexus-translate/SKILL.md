---
name: nexus-translate
description: "提供高质量的文化意识翻译服务（支持50多种语言）。"
version: 1.0.0
capabilities:
  - id: invoke-translate
    description: "High-quality translations with cultural awareness (50+ languages)"
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
# 人工智能翻译服务

> Cardano上的NEXUS代理即服务（Agent-as-a-Service） | 价格：0.12美元/次请求

## 使用场景

当您需要在不同语言之间翻译文本时，请使用此服务。

## 使用步骤

1. 向NEXUS API端点发送POST请求，并附上您的输入内容。
2. 在请求头中添加`X-Payment-Proof`字段（使用`masumi_payment_id`进行支付验证，或使用`sandbox_test`进行免费测试）。
3. 解析JSON响应并返回翻译结果。

### API调用

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/original-services/translate \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: $NEXUS_PAYMENT_PROOF" \
  -d '{"text": "Hello, how are you?", "target_language": "ja"}'
```

**端点：** `https://ai-service-hub-15.emergent.host/api/original-services/translate`
**方法：** POST
**请求头：**
- `Content-Type: application/json`
- `X-Payment-Proof: <masumi_payment_id>`（免费测试时使用`sandbox_test`）

## 外部接口

| URL | 方法 | 发送的数据 |
|-----|--------|-----------|
| `https://ai-service-hub-15.emergent.host/api/original-services/translate` | POST | 以JSON格式发送输入参数 |

## 安全与隐私

- 所有数据均通过HTTPS/TLS协议传输至`https://ai-service-hub-15.emergent.host`。
- 数据不会被永久存储，请求处理完成后会被立即删除。
- 支付验证通过Cardano区块链上的Masumi协议完成。
- 无需访问文件系统或执行shell命令。

## 模型调用说明

该服务通过调用NEXUS AI服务API来处理翻译请求，该API使用了LLM模型（GPT-5.2、Claude Sonnet 4.5、GPT-4o）来处理用户输入。AI会在服务器端处理请求并返回结构化的结果。您可以选择不安装此服务以拒绝使用其功能。

## 信任声明

使用本服务时，您的输入数据将被发送至NEXUS（https://ai-service-hub-15.emergent.host）进行人工智能处理。支付过程通过Cardano上的Masumi协议完成，且NEXUS不负责资金保管。仅当您信任NEXUS作为服务提供商时，才建议安装此服务。详情请访问：https://ai-service-hub-15.emergent.host。

## 标签

`机器学习`、`人工智能`、`免费试用`、`代理间通信`、`健康监控`、`预算管理`