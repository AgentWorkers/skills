---
name: nexus-trust-score
description: "使用 Cardano 上的 Masumi 交易数据，为钱包和代理生成链上信任评分。"
version: 1.0.0
capabilities:
  - id: invoke-trust-score
    description: "Generate on-chain trust scores for wallets and agents using Masumi transaction data on Cardano"
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
# 信任与声誉代理

> Cardano上的NEXUS代理即服务（Agent-as-a-Service） | 价格：0.75美元/请求

## 使用场景

当您需要根据链上交易历史来评估Cardano钱包地址或AI代理的可靠性时，请使用此服务。

## 使用步骤

1. 向NEXUS API端点发送POST请求，并提供相应的输入数据。
2. 在请求头中添加`X-Payment-Proof`字段（用于支付验证；测试时可使用`sandbox_test`）。
3. 解析JSON响应并获取结果。

### API调用

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/original-services/trust-score \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: $NEXUS_PAYMENT_PROOF" \
  -d '{"wallet_address": "addr1qy...", "include_details": true}'
```

**端点：** `https://ai-service-hub-15.emergent.host/api/original-services/trust-score`
**方法：** POST
**请求头：**
- `Content-Type: application/json`
- `X-Payment-Proof: <masumi_payment_id>`（免费测试时使用`sandbox_test`）

## 外部端点

| URL | 方法 | 发送的数据 |
|-----|--------|-----------|
| `https://ai-service-hub-15.emergent.host/api/original-services/trust-score` | POST | 以JSON格式发送输入参数 |

## 安全性与隐私

- 所有数据均通过HTTPS/TLS协议传输至`https://ai-service-hub-15.emergent.host`。
- 数据不会被永久存储；请求处理完成后会被立即删除。
- 支付验证通过Cardano区块链上的Masumi协议完成。
- 无需访问文件系统或执行shell命令。

## 模型调用说明

该服务会调用NEXUS的AI服务API，该API使用大语言模型（如GPT-5.2、Claude Sonnet 4.5、GPT-4o）来处理请求。AI会在服务器端处理您的输入并返回结构化的响应。您可以选择不安装此服务以拒绝使用相关功能。

## 信任声明

使用此服务时，您的输入数据将被发送至NEXUS（https://ai-service-hub-15.emergent.host）进行AI处理。所有支付操作均通过Cardano上的Masumi协议完成，且NEXUS不负责资金托管。仅当您信任NEXUS作为服务提供商时，才建议安装此服务。详情请访问：https://ai-service-hub-15.emergent.host。

## 标签

`机器学习`（Machine Learning）、`人工智能`（Artificial Intelligence）、`免费试用`（Free Trial）、`代理间通信`（Agent-to-Agent）、`健康监控`（Health Monitoring）