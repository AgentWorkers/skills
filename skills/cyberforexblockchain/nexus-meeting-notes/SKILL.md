---
name: nexus-meeting-notes
description: "将原始的会议记录转换为结构化的会议纪要，其中包含与会人员、决策内容、待办事项、负责人以及截止日期等信息。该工具专为能够自动处理音频转录结果的智能代理设计。"
version: 1.0.2
capabilities:
  - id: invoke-meeting-notes
    description: "Parse meeting transcripts and generate structured meeting minutes"
permissions:
  network: true
  filesystem: false
  shell: false
inputs:
  - name: transcript
    type: string
    required: true
    description: "Raw meeting transcript or notes to process"
outputs:
  type: object
  properties:
    minutes:
      type: object
      description: "Structured meeting minutes with sections"
requires:
  env: [NEXUS_PAYMENT_PROOF]
metadata: '{"openclaw":{"emoji":"\\u26a1","requires":{"env":["NEXUS_PAYMENT_PROOF"]},"primaryEnv":"NEXUS_PAYMENT_PROOF"}}'
---
# NEXUS 会议记录生成工具

> 专为 Cardano 平台上的 AI 代理设计的自主会议智能辅助工具

## 使用场景

当您的 AI 代理拥有原始会议记录文本（来自 Whisper、AssemblyAI 或手动笔记）时，该工具可帮助生成结构化、可操作的会议纪要。生成的纪要会明确记录发言者、决策内容以及各项后续任务的负责人。

## 产品优势

大多数会议总结工具仅生成简单的段落式文本，而 NEXUS 会议记录生成工具能够生成结构化数据：分别为与会者、议程主题、决策内容、行动项（包括负责人和截止日期）以及未解决的问题创建独立的数组。这使得后续自动化处理变得非常简单——您的代理可以直接使用这些数据创建 Jira 工单、发送跟进邮件或更新项目跟踪系统。

## 使用方法

1. 音频转录工具将录制的会议内容转换为原始文本。
2. 代理通过 POST 请求将转录文本发送给 NEXUS 会议记录生成工具。
3. 该工具会返回结构化的 JSON 数据：`{attendees, topics, decisions, action_items, open_questions}`。
4. 代理将行动项分配给任务管理系统，将决策内容记录到文档中。

### API 调用方式

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/original-services/meeting-notes \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: sandbox_test" \
  -d '{"transcript": "John: We need to ship the API by Friday. Sarah: I will handle testing. Bob: What about the payment integration? John: Lets push payments to next sprint."}'
```

## 外部接口

| URL | 方法 | 发送的数据 |
|-----|--------|-----------|
| `https://ai-service-hub-15.emergent.host/api/original-services/meeting-notes` | POST | 会议记录文本（以 JSON 格式） |

## 安全性与隐私保护

会议记录通常包含敏感的商业讨论内容。所有数据均通过 HTTPS/TLS 协议进行加密处理；记录文本不会被存储，而是在处理完成后立即删除。所有交易验证均通过 Cardano 的 Masumi 协议完成。

## 关于模型使用说明

该工具依赖服务器端的大型语言模型（LLM）来解析会议记录。AI 负责识别发言者、提取决策内容并分配行动项。您也可以选择不安装该工具以放弃使用相关功能。

## 信任声明

使用该工具时，会议记录数据会传输至 NEXUS 进行 AI 处理。所有交易均通过 Cardano 区块链完成，且不涉及任何资金托管。详情请访问：https://ai-service-hub-15.emergent.host