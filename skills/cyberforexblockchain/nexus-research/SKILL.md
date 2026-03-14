---
name: nexus-research
description: "对任何主题进行深入研究，并提供结构化的研究结果与建议。"
version: 1.0.0
capabilities:
  - id: invoke-research
    description: "Deep research on any topic with structured findings and recommendations"
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
# AI研究助手

> Cardano上的NEXUS代理即服务（Agent-as-a-Service） | 价格：每次请求0.50美元

## 使用场景

当您需要研究某个主题并获得包含来源信息的全面分析时，请使用该服务。

## 使用步骤

1. 向NEXUS API端点发送POST请求，并附上您的输入数据。
2. 在请求头中添加`X-Payment-Proof`字段（支付ID为`masumi_payment_id`，或使用`sandbox_test`进行测试）。
3. 解析JSON格式的响应内容并获取结果。

### API调用

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/original-services/research \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: $NEXUS_PAYMENT_PROOF" \
  -d '{"topic": "quantum computing developments 2026"}'
```

**端点：** `https://ai-service-hub-15.emergent.host/api/original-services/research`
**方法：** POST
**请求头：**
- `Content-Type: application/json`
- `X-Payment-Proof: <masumi_payment_id>`（免费测试时使用`sandbox_test`）

## 外部端点

| URL | 方法 | 发送的数据 |
|-----|--------|-----------|
| `https://ai-service-hub-15.emergent.host/api/original-services/research` | POST | 以JSON格式发送输入参数 |

## 安全性与隐私

- 所有数据均通过HTTPS/TLS协议传输至`https://ai-service-hub-15.emergent.host`。
- 数据不会被永久存储，请求处理完成后会被立即删除。
- 支付验证通过Cardano区块链上的Masumi协议完成。
- 无需访问文件系统或执行shell命令。

## 模型调用说明

该服务通过调用NEXUS AI服务API来处理用户请求，该API使用了大型语言模型（LLM，如GPT-5.2、Claude Sonnet 4.5、GPT-4o）。AI会在服务器端处理您的输入并返回结构化的响应。您也可以选择不安装此服务。

## 信任声明

使用该服务时，您的输入数据将被发送至NEXUS（https://ai-service-hub-15.emergent.host）进行AI处理。支付过程通过Cardano上的Masumi协议实现，且资金不由NEXUS保管。仅当您信任NEXUS作为服务提供商时，才建议安装此服务。详情请访问https://ai-service-hub-15.emergent.host。

## 标签

`机器学习`、`人工智能`、`免费试用`、`代理间通信`、`健康监控`、`预算管理`