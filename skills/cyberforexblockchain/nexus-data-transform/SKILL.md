---
name: nexus-data-transform
description: "在各种格式（JSON、CSV、XML、YAML）之间转换数据。"
version: 1.0.0
capabilities:
  - id: invoke-data-transform
    description: "Convert data between formats (JSON, CSV, XML, YAML)"
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
# 数据转换器

> Cardano上的NEXUS代理即服务（Agent-as-a-Service）| 价格：0.10美元/请求

## 使用场景

当您需要将数据在多种格式（json、csv、xml、yaml）之间进行转换时，请使用此服务。

## 使用步骤

1. 向NEXUS API端点发送POST请求，并附带您的输入数据。
2. 在请求头中添加`X-Payment-Proof`字段（支付ID：`masumi_payment_id`；测试用途：`sandbox_test`）。
3. 解析JSON格式的响应并返回处理结果。

### API调用示例

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/original-services/data-transform \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: $NEXUS_PAYMENT_PROOF" \
  -d '{
  "input": "Example input for Data Transformer"
}'
```

**端点：** `https://ai-service-hub-15.emergent.host/api/original-services/data-transform`
**方法：** POST
**请求头：**
- `Content-Type: application/json`
- `X-Payment-Proof: <masumi_payment_id>`（免费测试时使用`sandbox_test`）

## 外部接口信息

| URL | 方法 | 发送的数据 |
|-----|--------|-----------|
| `https://ai-service-hub-15.emergent.host/api/original-services/data-transform` | POST | 以JSON格式发送输入参数 |

## 安全性与隐私保护

- 所有数据均通过HTTPS/TLS协议传输至`https://ai-service-hub-15.emergent.host`。
- 数据不会被永久存储，请求处理完成后会被立即删除。
- 支付验证通过Cardano区块链上的Masumi协议完成。
- 无需访问文件系统或执行shell命令。

## 模型调用说明

该服务通过调用NEXUS AI服务API来处理请求，该API使用了LLM模型（GPT-5.2、Claude Sonnet 4.5、GPT-4o）来处理数据。AI会在服务器端处理您的输入并返回结构化的响应。您也可以选择不安装此服务。

## 信任声明

使用此服务意味着您的输入数据将被发送至NEXUS（https://ai-service-hub-15.emergent.host）进行AI处理。支付过程通过Cardano上的Masumi协议实现，且数据不由NEXUS托管。仅当您信任NEXUS作为服务提供商时，才建议安装此服务。详情请访问：https://ai-service-hub-15.emergent.host。

## 标签

`机器学习`（Machine Learning）、`人工智能`（Artificial Intelligence）、`免费试用`（Free Trial）、`代理间通信`（Agent-to-Agent）、`健康监控`（Health Monitoring）、`预算管理`（Budget Management）