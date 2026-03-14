---
name: nexus-sentiment-analysis
description: "分析文本的情感基调、观点极性、主观性、情感强度以及具体情感。输出结果包括每句话的详细分析（包含讽刺语检测结果、紧迫性评分以及混合情感的识别）。"
version: 1.0.2
capabilities:
  - id: invoke-sentiment-analysis
    description: "Analyze text for emotional tone, opinion polarity, subjectivity, intensity, and specific emotions. Returns per-sentence breakdown with sarcasm detection, urgency scoring, and mixed-sentiment identific"
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
# NEXUS 情感分析服务

> 专为 Cardano 生态设计的 AI 服务，适用于自主智能体 | NEXUS AaaS 平台

## 使用场景

当您的智能体需要处理客户评价、社交媒体帖子、支持工单、调查问卷回复等文本时，若需通过理解文本中的情感基调来辅助决策，本服务将非常有用。该服务不仅能区分文本的正面/负面情绪，还能识别用户的不满、满意度、紧迫感或困惑等复杂情绪。

## 服务特色

- **多维度分析**：包括情感极性（-1 至 +1）、主观性（0 至 1）、情感强度（低/中/高）、具体情绪类型（喜悦、愤怒、恐惧、惊讶）以及讽刺语气的概率。
- **精准到句**：能够对长文本进行详细分析，而不仅仅是给出一个总体评分。

## 使用步骤

1. 将输入数据准备成 JSON 格式。
2. 使用 `X-Payment-Proof` 头部信息通过 POST 请求发送到 NEXUS API。
3. 解析返回的 JSON 结构化响应。

### API 调用示例

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/original-services/sentiment-analysis \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: sandbox_test" \
  -d '{"text": "The product arrived quickly and works great, but the packaging was damaged and customer support took 3 days to respond.", "granularity": "sentence"}'
```

**端点:** `https://ai-service-hub-15.emergent.host/api/original-services/sentiment-analysis`
**方法:** POST
**请求头:**
- `Content-Type: application/json`
- `X-Payment-Proof: <masumi_payment_id>`（免费试用请使用 `sandbox_test`）

## 外部接口信息

| URL | 方法 | 发送的数据 |
|-----|--------|-----------|
| `https://ai-service-hub-15.emergent.host/api/original-services/sentiment-analysis` | POST | 以 JSON 格式发送输入参数 |

## 安全性与隐私保护

所有请求均通过 HTTPS/TLS 协议传输至 `https://ai-service-hub-15.emergent.host`。数据不会被永久存储，仅在处理完成后立即销毁。支付验证采用 Cardano 的 Masumi 协议（非托管式托管方式）。无需任何文件系统或 shell 权限。

## 关于模型调用

该功能会调用 NEXUS AI 服务 API，该 API 使用大型语言模型在服务器端处理请求。您可以选择不安装此功能以拒绝使用相关服务。

## 信任声明

安装此功能后，输入数据将传输至 NEXUS（https://ai-service-hub-15.emergent.host）进行人工智能处理。所有支付操作均通过 Cardano 的非托管方式完成。详情请访问 [https://ai-service-hub-15.emergent.host](https://ai-service-hub-15.emergent.host) 查看相关文档和条款。