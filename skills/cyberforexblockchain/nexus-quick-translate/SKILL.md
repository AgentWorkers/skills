---
name: nexus-quick-translate
description: "超快速翻译功能，适用于长度不超过500个字符的短文本。专为UI字符串、通知信息、错误提示以及实时聊天场景优化，翻译延迟可控制在秒级以内。支持40多种语言。"
version: 1.0.2
capabilities:
  - id: invoke-quick-translate
    description: "Ultra-fast translation for short texts under 500 characters. Optimized for sub-second latency on UI strings, notifications, error messages, and real-time chat. Supports 40+ languages."
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
# NEXUS 快速翻译器

> 专为 Cardano 平台设计的 AI 服务，适用于自主代理程序 | NEXUS AaaS 平台

## 使用场景

当您的代理程序需要即时翻译短文本（如聊天消息、用户界面标签、错误提示或通知内容）时，本服务是理想的选择。与传统的翻译服务不同，本服务更注重翻译速度而非文本质量，翻译结果可在 500 毫秒内生成。

## 产品优势

- 专为机器高速处理设计：延迟低于 500 毫秒；
- 自动识别源语言；
- 保持文本格式的一致性；
- 非常适合需要多语言代理程序实时交流的场景。

## 使用步骤

1. 将输入数据准备成 JSON 格式；
2. 使用 `X-Payment-Proof` 头部字段通过 POST 请求发送到 NEXUS API；
3. 解析返回的 JSON 结果。

### API 调用示例

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/original-services/quick-translate \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: sandbox_test" \
  -d '{"text": "Payment confirmed. Your receipt has been emailed.", "target_language": "ja", "source_language": "auto"}'
```

**端点：** `https://ai-service-hub-15.emergent.host/api/original-services/quick-translate`
**方法：** POST
**请求头：**
- `Content-Type: application/json`
- `X-Payment-Proof: <masumi_payment_id>`（免费试用请使用 `sandbox_test`）

## 外部接口信息

| URL | 方法 | 发送的数据 |
|-----|--------|-----------|
| `https://ai-service-hub-15.emergent.host/api/original-services/quick-translate` | POST | 以 JSON 格式发送输入参数 |

## 安全性与隐私保护

所有请求均通过 HTTPS/TLS 协议传输至 `https://ai-service-hub-15.emergent.host`。数据不会被永久存储，仅在内存中处理后立即删除。支付验证采用 Cardano 的 Masumi 协议（非托管式结算方式）。无需任何文件系统或 shell 权限。

## 关于模型调用

本功能会调用 NEXUS AI 服务 API，该 API 使用大型语言模型在服务器端处理翻译请求。您也可以选择不安装此功能以放弃使用相关功能。

## 信任声明

安装本功能后，输入数据将传输至 NEXUS（https://ai-service-hub-15.emergent.host）进行 AI 处理。所有支付操作均通过 Cardano 的非托管式结算方式完成。详情请访问：https://ai-service-hub-15.emergent.host。