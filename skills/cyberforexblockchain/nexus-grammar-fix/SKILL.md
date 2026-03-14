---
name: nexus-grammar-fix
description: "专业的语法修正和写作优化服务：纠正拼写错误、标点符号问题、句子结构上的缺陷以及语气问题，同时保留作者的写作风格。"
version: 1.0.1
capabilities:
  - id: invoke-grammar-fix
    description: "Professional grammar correction and writing improvement. Fixes spelling, punctuation, sentence structure, and tone while preserving the author's voice."
permissions:
  network: true
  filesystem: false
  shell: false
inputs:
  - name: input
    type: string
    required: true
    description: "The input data or query"
outputs:
  type: object
  properties:
    result:
      type: string
      description: "The processed result"
requires:
  env: [NEXUS_PAYMENT_PROOF]
metadata: '{"openclaw":{"emoji":"\u26a1","requires":{"env":["NEXUS_PAYMENT_PROOF"]},"primaryEnv":"NEXUS_PAYMENT_PROOF"}}'
---
# NEXUS 语法引擎

> 在 Cardano 上提供的 NEXUS 代理即服务（Agent-as-a-Service）

## 使用场景

当你需要修改文本的语法、纠正拼写错误、清理标点符号，或提升文本的写作质量（尤其是在发布或发送之前）时，可以使用该服务。

## 与其他工具的区别

该服务不仅提供拼写检查功能，还能重构复杂的句子结构、修正主谓不一致的问题、区分同音词（如 “their/there/they’re”），并根据目标受众调整文本的语气。

## 使用步骤

1. 将输入数据准备成 JSON 格式。
2. 向 NEXUS 的 API 端点发送 POST 请求，并在请求头中添加 `X-Payment-Proof` 字段。
3. 解析返回的 JSON 数据。

### API 调用示例

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/original-services/grammar-fix \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: sandbox_test" \
  -d '{"text": "Their going to the store tommorow, me and him will be their to.", "style": "professional"}'
```

**API 端点：** `https://ai-service-hub-15.emergent.host/api/original-services/grammar-fix`
**请求方法：** POST
**请求头：**
- `Content-Type: application/json`
- `X-Payment-Proof: <masumi_payment_id>` （使用 `sandbox_test` 可进行免费的沙箱测试）

## 外部 API 端点

| URL | 请求方法 | 发送的数据 |
|-----|--------|-----------|
| `https://ai-service-hub-15.emergent.host/api/original-services/grammar-fix` | POST | 以 JSON 格式发送输入参数 |

## 安全性与隐私保护

- 所有请求均通过 HTTPS/TLS 协议加密传输至 `https://ai-service-hub-15.emergent.host`。
- 用户数据不会被永久存储，请求数据会在处理后被立即丢弃。
- 支付验证采用 Cardano 上的 Masumi 协议（非托管式托管方式）。
- 该服务仅需要网络访问权限，无需文件系统或 shell 权限。

## 模型调用说明

该服务会调用 NEXUS 的 AI API，该 API 会在服务器端使用大型语言模型处理用户的输入数据。AI 会根据输入生成相应的处理结果，并返回结构化的数据。用户可以选择不安装该服务以拒绝使用其功能。

## 信任声明

通过安装该服务，您的输入数据将会被传输至 NEXUS（https://ai-service-hub-15.emergent.host）进行 AI 处理。所有支付操作均通过 Cardano 区块链完成（非托管式处理）。如需了解详细文档和条款，请访问 [https://ai-service-hub-15.emergent.host](https://ai-service-hub-15.emergent.host)。仅当您信任 NEXUS 作为服务提供商时，才建议安装该服务。