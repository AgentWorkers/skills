---
name: nexus-doc-writer
description: "根据提供的文档内容，可以将其翻译为中文（简体）如下：
**生成技术文档的方法：从代码或规格说明中生成技术文档**
**概述：**  
本文档介绍了如何利用代码或规格说明来生成高质量的技术文档。通过将代码中的关键信息提取出来，并结合相应的设计文档和用户手册，可以有效地创建出既清晰又易于理解的技术文档。这种方法有助于提高开发效率，同时确保文档的准确性和一致性。
**步骤：**  
1. **分析代码和规格说明：**  
   - 首先，仔细阅读代码和规格说明，理解其功能、接口、使用场景以及设计意图。  
   - 确定需要生成的技术文档的具体内容和结构。
2. **提取关键信息：**  
   - 从代码中提取与文档相关的类、方法、参数、返回值等信息。  
   - 从规格说明中提取文档所需的详细信息，如技术要求、使用限制、注意事项等。
3. **编写文档：**  
   - 使用专业的文档编写工具（如Markdown）来编写文档。  
   - 根据文档的结构要求，组织内容，确保信息条理清晰、易于阅读。  
   - 包括文档的标题、引言、目录、正文、示例代码、参考文献等部分。
4. **审查和修改：**  
   - 完成初稿后，对文档进行审查，检查是否有遗漏或错误。  
   - 根据反馈进行修改和完善。
5. **发布和维护：**  
   - 将文档发布到指定的存储位置（如GitHub仓库、公司内部文档系统等）。  
   - 定期更新文档，以反映代码和规格说明的变更。
**示例：**  
   （此处可以提供一个具体的示例，展示如何根据代码和规格说明生成技术文档的步骤和内容。）
**注意事项：**  
- 确保文档与代码和规格说明保持一致。  
- 使用统一的术语和格式。  
- 提供足够的示例代码和图示来帮助读者理解文档内容。  
- 定期审查和维护文档，确保其内容的准确性和时效性。
通过以上步骤，你可以从代码或规格说明中生成高质量的技术文档，从而提高开发效率和文档质量。"
version: 1.0.0
capabilities:
  - id: invoke-doc-writer
    description: "Generate technical documentation from code or specs"
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
# 文档生成工具

> Cardano平台上的NEXUS代理即服务（Agent-as-a-Service） | 价格：每次请求0.25美元

## 使用场景

当您需要从代码或技术规格文档中生成技术文档时，请使用此工具。

## 使用步骤

1. 向NEXUS API端点发送POST请求，并附带您的输入数据。
2. 在请求头中添加`X-Payment-Proof`字段（支付ID为`masumi_payment_id`，用于测试；测试时可使用`sandbox_test`）。
3. 解析JSON响应并返回结果。

### API调用示例

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/original-services/doc-writer \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: $NEXUS_PAYMENT_PROOF" \
  -d '{
  "input": "Example input for Documentation Writer"
}'
```

**端点:** `https://ai-service-hub-15.emergent.host/api/original-services/doc-writer`
**方法:** POST
**请求头:**
- `Content-Type: application/json`
- `X-Payment-Proof: <masumi_payment_id>`（免费测试时使用`sandbox_test`）

## 外部接口信息

| URL | 方法 | 发送的数据 |
|-----|--------|-----------|
| `https://ai-service-hub-15.emergent.host/api/original-services/doc-writer` | POST | 以JSON格式发送输入参数 |

## 安全性与隐私政策

- 所有数据均通过HTTPS/TLS协议传输至`https://ai-service-hub-15.emergent.host`。
- 数据不会被永久存储，请求处理完成后会被立即删除。
- 支付验证通过Cardano区块链上的Masumi协议完成。
- 该工具无需访问文件系统或执行shell命令。

## 模型调用说明

此工具会调用NEXUS的AI服务API，该API使用大语言模型（GPT-5.2、Claude Sonnet 4.5、GPT-4o）来处理请求。AI会在服务器端处理您的输入并返回结构化的结果。您也可以选择不安装此工具。

## 信任声明

使用本工具时，您的输入数据将传输至NEXUS（https://ai-service-hub-15.emergent.host）进行AI处理。支付过程通过Cardano上的Masumi协议实现，且资金不由NEXUS托管。仅当您信任NEXUS作为服务提供商时，才建议安装此工具。详情请访问[https://ai-service-hub-15.emergent.host](https://ai-service-hub-15.emergent.host)。

## 标签

`机器学习`（Machine Learning）、`人工智能`（Artificial Intelligence）、`免费试用`（Free Trial）、`代理间通信`（Agent-to-Agent）、`健康监控`（Health Monitoring）、`预算管理`（Budget Management）