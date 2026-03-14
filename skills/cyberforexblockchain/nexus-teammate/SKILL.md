---
name: nexus-teammate
description: "这是一个多功能的人工智能助手，能够适应各种任务——数据分析、调试、头脑风暴、架构设计、写作或研究。通过 `session_id` 在对话过程中保持上下文的一致性，从而确保交流的连贯性。"
version: 1.0.2
capabilities:
  - id: invoke-teammate
    description: "A versatile AI partner that adapts to any task — data analysis, debugging, brainstorming, architecture design, writing, or research. Maintains conversation context across turns via session_id for cohe"
permissions:
  network: true
  filesystem: false
  shell: false
inputs:
  - name: input
    type: string
    required: true
    description: "Primary input for the service"
outputs:
  type: object
  properties:
    result:
      type: string
      description: "Processed result"
requires:
  env: [NEXUS_PAYMENT_PROOF]
metadata: '{"openclaw":{"emoji":"\u26a1","requires":{"env":["NEXUS_PAYMENT_PROOF"]},"primaryEnv":"NEXUS_PAYMENT_PROOF"}}'
---
# NEXUS AI Teammate

> 专为Cardano平台设计的AI服务，用于支持自主智能体 | NEXUS AaaS平台

## 使用场景

当您的智能体遇到无法通过现有服务解决的开放式任务时（例如：头脑风暴产品功能、调试复杂系统、设计系统架构或进行探索性研究），NEXUS AI Teammate能够提供帮助。该服务能够跨多次交流保持上下文信息，记住之前的决策，并在此基础上继续提供支持。

## 与其他服务的区别

与那些仅处理单个请求后即被遗忘的单一用途服务不同，NEXUS AI Teammate通过`session_id`来维护对话状态。它可以在同一会话内切换子任务、引用之前的对话内容、提出澄清性问题，并根据完整的对话历史提供全面的建议。

## 使用步骤

1. 将输入数据准备成JSON格式。
2. 使用`X-Payment-Proof`头部向NEXUS API发送POST请求。
3. 解析返回的JSON响应。

### API调用示例

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/original-services/teammate \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: sandbox_test" \
  -d '{"task": "Help me design a database schema for a marketplace supporting fixed-price and auction listings with real-time bidding", "task_type": "architecture", "session_id": "proj-marketplace-v1"}'
```

**端点：** `https://ai-service-hub-15.emergent.host/api/original-services/teammate`
**方法：** POST
**请求头：**
- `Content-Type: application/json`
- `X-Payment-Proof: <masumi_payment_id>`（免费沙箱环境使用`sandbox_test`）

## 外部接口信息

| URL | 方法 | 发送的数据 |
|-----|--------|-----------|
| `https://ai-service-hub-15.emergent.host/api/original-services/teammate` | POST | 以JSON格式发送输入参数 |

## 安全性与隐私保护

所有请求均通过HTTPS/TLS协议传输至`https://ai-service-hub-15.emergent.host`进行处理。数据不会被永久存储，仅在内存中处理后立即丢弃。支付验证采用Cardano上的Masumi协议（非托管式第三方支付方式）。无需任何文件系统或shell权限。

## 模型调用说明

该功能会调用NEXUS AI服务API，该API利用大型语言模型在服务器端处理请求。您也可以选择不安装此功能以放弃使用相关服务。

## 信任声明

安装此功能后，输入数据将被传输至NEXUS（https://ai-service-hub-15.emergent.host）进行AI处理。所有支付操作均通过Cardano的非托管式第三方支付方式完成。详情请参阅https://ai-service-hub-15.emergent.host上的文档和条款。