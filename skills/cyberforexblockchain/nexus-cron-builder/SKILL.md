---
name: nexus-cron-builder
description: "生成并解释 Cron 表达式
**Cron 表达式简介：**  
Cron 表达式是一种用于指定任务执行时间的文本格式。它由六个字段组成，每个字段之间用冒号（:）分隔，具体格式如下：  
`hour minute minute month day weekday`  
- `hour`：任务应在每小时的第几分钟执行（0-59）  
- `minute`：任务应在每分钟的第几分钟执行（0-59）  
- `minute`：与 `hour` 相同，表示任务应在每分钟的第几分钟执行  
- `month`：任务应在每月的哪一天执行（1-12）  
- `day`：任务应在每月的哪一天执行（1-31）  
- `weekday`：任务应在一周中的哪一天执行（0-7，其中0表示星期日，1表示星期一，依此类推）  
**Cron 表达式的示例：**  
- `0 0 0 * * *`：表示任务每天在凌晨0点执行  
- `0 15 30 * * *`：表示任务每天在下午3点30分执行  
- `1 15 15 * * *`：表示任务每月的15号每天在下午3点15分执行  
- `0 0 1 1 * *`：表示任务每月的1号每天在凌晨0点执行（仅限于星期一）  
**Cron 表达式的解释：**  
- `*`：表示该字段的值可以任意设置，允许任务在任何时间执行  
- ```：表示该字段的值需要匹配特定的条件  
- ```：表示该字段的值需要匹配特定的条件  
**Cron 表达式的应用场景：**  
Cron 表达式广泛应用于自动化任务调度，例如定期备份数据、发送邮件、更新网站内容等。通过编写合适的 Cron 表达式，可以轻松实现定时任务的管理和执行。"
version: 1.0.0
capabilities:
  - id: invoke-cron-builder
    description: "Generate and explain cron expressions"
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
# Cron 表达式生成器

> Cardano 上的 NEXUS 代理即服务（Agent-as-a-Service） | 价格：0.05 美元/请求

## 使用场景

当您需要生成和解释 Cron 表达式时，请使用此工具。

## 使用步骤

1. 向 NEXUS API 端点发送 POST 请求，并提供相应的输入数据。
2. 在请求头中添加 `X-Payment-Proof` 字段（用于支付验证，内容为 Masumi 支付 ID；测试时可使用 `sandbox_test`）。
3. 解析 JSON 响应并获取结果。

### API 调用示例

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/original-services/cron-builder \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: $NEXUS_PAYMENT_PROOF" \
  -d '{
  "input": "Example input for Cron Expression Builder"
}'
```

**端点：** `https://ai-service-hub-15.emergent.host/api/original-services/cron-builder`
**方法：** POST
**请求头：**
- `Content-Type: application/json`
- `X-Payment-Proof: <masumi_payment_id>` （免费测试时使用 `sandbox_test`）

## 外部接口信息

| URL | 方法 | 发送的数据 |
|-----|--------|-----------|
| `https://ai-service-hub-15.emergent.host/api/original-services/cron-builder` | POST | 以 JSON 格式发送输入参数 |

## 安全性与隐私政策

- 所有数据均通过 HTTPS/TLS 协议传输至 `https://ai-service-hub-15.emergent.host`。
- 数据不会被永久存储，请求处理完成后会被立即删除。
- 支付验证通过 Cardano 区块链上的 Masumi 协议完成。
- 无需访问文件系统或执行 shell 命令。

## 模型调用说明

该功能会调用 NEXUS AI 服务 API，该 API 使用 LLM 模型（GPT-5.2、Claude Sonnet 4.5、GPT-4o）来处理请求。AI 会在服务器端处理您的输入并返回结构化的响应。您可以选择不安装此功能。

## 信任声明

使用此功能时，您的输入数据将被发送至 NEXUS（https://ai-service-hub-15.emergent.host）进行 AI 处理。支付过程通过 Cardano 上的 Masumi 协议实现，且数据不会被第三方托管。仅当您信任 NEXUS 作为服务提供商时，才建议安装此功能。详情请访问：https://ai-service-hub-15.emergent.host。

## 标签

`机器学习`（Machine Learning）、`人工智能`（Artificial Intelligence）、`免费试用`（Free Trial）、`代理间通信`（Agent-to-Agent）、`健康监控`（Health Monitoring）、`预算管理`（Budget Management）