---
name: nexus-regex-generator
description: "用简单的英语描述您想要匹配的内容，然后生成一个可用于实际开发的正则表达式。该正则表达式应包含命名捕获组，并提供相应的测试用例以及针对边缘情况的警告说明。支持 Python、JavaScript、Go、Java 等编程语言。"
version: 1.0.2
capabilities:
  - id: invoke-regex-generator
    description: "Describe what you want to match in plain English and get a production-ready regular expression with named capture groups, test cases, and edge case warnings. Supports Python, JavaScript, Go, Java, and"
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
# NEXUSRegex Forge

> 专为Cardano原生开发的AI服务，用于生成自动化代理程序 | NEXUS AaaS平台

## 使用场景

当您的代理程序需要生成、验证或调试正则表达式时，无需手动编写正则表达式模式，只需用自然语言描述匹配条件，即可获得经过测试且文档化的正则表达式模式。

## 产品优势

该服务不仅返回正则表达式本身，还提供一个完整的解决方案包：包含带有命名捕获组的正则表达式、5个以上的测试用例（包括匹配和不匹配的情况）、每个组件的英文说明，以及对常见问题的警告（如Unicode编码、换行符处理和贪婪匹配等）。

## 使用步骤

1. 将输入数据准备为JSON格式。
2. 使用`X-Payment-Proof`头部向NEXUS API发送POST请求。
3. 解析返回的结构化JSON响应。

### API调用示例

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/original-services/regex-generator \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: sandbox_test" \
  -d '{"description": "Match email addresses ending with .edu or .gov, capturing username and domain separately", "flavor": "python"}'
```

**端点：** `https://ai-service-hub-15.emergent.host/api/original-services/regex-generator`
**方法：** POST
**请求头：**
- `Content-Type: application/json`
- `X-Payment-Proof: <masumi_payment_id>` （免费沙箱环境使用`sandbox_test`）

## 外部接口

| URL | 方法 | 发送的数据 |
|-----|--------|-----------|
| `https://ai-service-hub-15.emergent.host/api/original-services/regex-generator` | POST | 以JSON格式发送输入参数 |

## 安全性与隐私保护

所有请求均通过HTTPS/TLS协议传输至`https://ai-service-hub-15.emergent.host`。数据不会被永久存储，仅在内存中处理后立即丢弃。支付验证通过Cardano的Masumi协议完成（非托管式支付方式）。无需任何文件系统或shell权限。

## 关于模型调用的说明

此功能会调用NEXUS AI服务API，该API利用大型语言模型在服务器端处理请求。您可以选择不安装此功能以规避相关风险。

## 信任声明

安装此功能后，输入数据将传输至NEXUS（https://ai-service-hub-15.emergent.host）进行AI处理。所有支付均通过Cardano的非托管方式完成。详情请访问https://ai-service-hub-15.emergent.host查看相关文档和条款。