---
name: nexus-log-analyzer
description: "输入服务器日志、应用程序日志或系统日志，即可获得模式分析、异常检测、错误聚类以及可操作的事件摘要。"
version: 1.0.1
capabilities:
  - id: invoke-log-analyzer
    description: "Feed in server logs, application logs, or system logs and get pattern analysis, anomaly detection, error clustering, and actionable incident summaries."
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
# NEXUS 日志智能分析工具

> NEXUS 作为 Cardano 平台上的“代理即服务”（Agent-as-a-Service）产品

## 使用场景

当您拥有来自服务器、应用程序或基础设施的大量日志记录时，需要识别其中的错误、异常模式或事件的根本原因。

## 该工具的独特之处

- 能够关联相关的日志条目，识别故障的连锁反应，并生成事件时间线；
- 支持解析来自 nginx、Apache、Docker、Kubernetes 以及云服务提供商的日志格式。

## 使用步骤

1. 将输入数据准备为 JSON 格式；
2. 向 NEXUS 的 API 端点发送 POST 请求，并在请求头中添加 `X-Payment-Proof` 字段；
3. 解析返回的 JSON 数据。

### API 调用示例

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/original-services/log-analyzer \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: sandbox_test" \
  -d '{"logs": "2026-03-12 10:00:01 ERROR db_pool: Connection timeout after 30s\n2026-03-12 10:00:02 WARN api: Retry attempt 3/5 for /users endpoint\n2026-03-12 10:00:03 ERROR api: 503 Service Unavailable", "focus": "identify root cause"}'
```

**API 端点：** `https://ai-service-hub-15.emergent.host/api/original-services/log-analyzer`
**请求方法：** POST
**请求头：**
- `Content-Type: application/json`
- `X-Payment-Proof: <masumi_payment_id>` （免费沙盒测试请使用 `sandbox_test`）

## 外部 API 端点信息

| URL | 请求方法 | 发送的数据 |
|-----|--------|-----------|
| `https://ai-service-hub-15.emergent.host/api/original-services/log-analyzer` | POST | 以 JSON 格式发送输入参数 |

## 安全性与隐私政策

- 所有请求均通过 HTTPS/TLS 协议加密传输至 `https://ai-service-hub-15.emergent.host`；
- 用户数据不会被永久存储，请求数据会在处理后被立即销毁；
- 支付验证采用 Cardano 平台上的 Masumi 协议（非托管式托管机制）；
- 该工具仅需要网络访问权限，无需文件系统或 shell 权限。

## 模型调用说明

该工具会调用 NEXUS AI 服务 API，在服务器端利用大型语言模型处理您的输入数据。AI 会根据输入生成结构化响应。您可以选择不安装该工具以拒绝使用相关功能。

## 信任声明

安装该工具后，您的输入数据将传输至 NEXUS（https://ai-service-hub-15.emergent.host）进行人工智能处理。所有支付操作均通过 Cardano 区块链完成（非托管式处理）。如需了解详细文档和条款，请访问 [https://ai-service-hub-15.emergent.host](https://ai-service-hub-15.emergent.host)。仅当您信任 NEXUS 作为服务提供商时，才建议安装该工具。