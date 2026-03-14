---
name: nexus-commit-message
description: "根据提供的 `SKILL.md` 文件内容，以下是翻译后的中文版本：
**生成基于差异文件的常规提交信息**
**说明：**  
此功能用于根据文件间的差异（diffs）自动生成规范的提交信息。提交信息通常包含对更改内容的简要描述，以便团队成员能够快速理解更改的目的和内容。以下是实现该功能的步骤：
1. **读取文件差异（diffs）**：首先，系统会读取需要生成提交信息的文件之间的差异数据。
2. **解析差异数据**：接着，系统会解析这些差异数据，提取出所有被修改的行和对应的修改类型（如添加、删除或修改）。
3. **生成提交信息**：根据解析出的差异数据，系统会生成一个格式规范的提交信息。提交信息通常包括以下内容：
   - 提交者（Author）
   - 提交日期（Date）
   - 提交信息（Message）
   - 被修改的文件列表（Files modified）
   - 被修改的行列表（Lines modified）
4. **格式化提交信息**：最后，系统会将生成的提交信息格式化为标准的 Git 提交消息格式，以便在 Git 仓库中使用。
**示例代码：**  
（由于原始代码片段中未包含具体的实现细节，这里仅提供功能描述和示例结构。实际实现可能需要根据具体的编程语言和框架来完成。）
**注意：**  
- 如果需要自定义提交信息的格式或内容，可以在解析差异数据或生成提交信息的步骤中进行相应的处理。
- 为了确保生成的提交信息的一致性和可读性，建议使用统一的模板或规则来格式化提交信息。
请注意，这个翻译是基于提供的文档内容生成的。如果需要更详细的解释或特定的技术细节，请提供更多的上下文或代码示例。"
version: 1.0.0
capabilities:
  - id: invoke-commit-message
    description: "Generate conventional commit messages from diffs"
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
# 提交信息生成器

> NEXUS 代理即服务（Agent-as-a-Service）在 Cardano 上提供 | 价格：0.05 美元/次请求

## 使用场景

当您需要根据代码差异（diffs）生成常规的提交信息时，请使用此工具。

## 使用步骤

1. 向 NEXUS API 端点发送 POST 请求，并提供相应的输入数据。
2. 必须包含 `X-Payment-Proof` 头部字段（用于支付验证；测试时可使用 `sandbox_test`）。
3. 解析 JSON 格式的响应内容，并获取生成的结果。

### API 调用示例

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/original-services/commit-message \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: $NEXUS_PAYMENT_PROOF" \
  -d '{
  "input": "Example input for Commit Message Generator"
}'
```

**端点：** `https://ai-service-hub-15.emergent.host/api/original-services/commit-message`
**方法：** POST
**请求头：**
- `Content-Type: application/json`
- `X-Payment-Proof: <masumi_payment_id>`（免费测试时使用 `sandbox_test`）

## 外部 API 端点

| URL | 方法 | 发送的数据 |
|-----|--------|-----------|
| `https://ai-service-hub-15.emergent.host/api/original-services/commit-message` | POST | 以 JSON 格式发送输入参数 |

## 安全性与隐私保护

- 所有数据均通过 HTTPS/TLS 协议传输至 `https://ai-service-hub-15.emergent.host`。
- 数据不会被永久存储，请求处理完成后会被立即删除。
- 支付验证通过 Cardano 区块链上的 Masumi 协议完成。
- 无需访问文件系统或执行 shell 命令。

## 模型调用说明

该功能会调用 NEXUS 的 AI 服务 API，该 API 使用大型语言模型（如 GPT-5.2、Claude Sonnet 4.5、GPT-4o）来处理请求。AI 会在服务器端处理您的输入并返回结构化的响应。您可以选择不安装此功能。

## 信任声明

使用此功能时，您的输入数据将会被发送至 NEXUS（https://ai-service-hub-15.emergent.host）进行 AI 处理。支付过程通过 Cardano 上的 Masumi 协议实现，且 NEXUS 不会保管用户的资金。仅当您信任 NEXUS 作为服务提供商时，才建议安装此功能。详情请访问：https://ai-service-hub-15.emergent.host。

## 标签

`机器学习`（Machine Learning）、`人工智能`（Artificial Intelligence）、`免费试用`（Free Trial）、`代理间通信`（Agent-to-Agent）、`健康监控`（Health Monitoring）、`预算管理`（Budget Management）