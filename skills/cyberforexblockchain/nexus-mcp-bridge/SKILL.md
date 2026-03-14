---
name: nexus-mcp-bridge
description: "桥接代理用于与兼容MCP的工具服务器进行通信，这些工具服务器支持IPFS数据固定（pinning）功能、GitHub操作以及文件系统相关功能。通过统一的接口执行MCP工具的相关命令。"
version: 1.0.1
capabilities:
  - id: invoke-mcp-bridge
    description: "Bridge agent to MCP-compatible tool servers including IPFS pinning, GitHub operations, and filesystem tools. Execute MCP tool calls through a unified interface."
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
# NEXUS MCP桥接器

> 在Cardano平台上提供的NEXUS代理即服务（Agent-as-a-Service）

## 使用场景

当您的代理需要与MCP工具服务器进行交互时——例如将文件固定到IPFS上、读写GitHub仓库，或通过Model Context Protocol执行文件系统操作。

## 产品特点

这是首个在Cardano平台上以付费服务形式提供的MCP桥接器。支持IPFS（固定/解除固定文件、目录操作）、GitHub（读写/提交Pull Request），并且可以扩展到任何兼容MCP的服务器。

## 使用步骤

1. 将输入数据准备为JSON格式。
2. 向NEXUS的API端点发送带有`X-Payment-Proof`头的POST请求。
3. 解析返回的结构化JSON响应。

### API调用示例

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/original-services/mcp-bridge \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: sandbox_test" \
  -d '{"mcp_server": "ipfs", "operation": "pin", "parameters": {"content": "Hello from NEXUS agent", "filename": "agent-output.txt"}}'
```

**API端点：** `https://ai-service-hub-15.emergent.host/api/original-services/mcp-bridge`
**请求方法：** POST
**请求头：**
- `Content-Type: application/json`
- `X-Payment-Proof: <masumi_payment_id>` （免费沙箱测试请使用`sandbox_test`）

## 外部API端点

| URL | 请求方法 | 发送的数据 |
|-----|--------|-----------|
| `https://ai-service-hub-15.emergent.host/api/original-services/mcp-bridge` | POST | 以JSON格式发送输入参数 |

## 安全性与隐私保护

- 所有请求均通过HTTPS/TLS加密传输至`https://ai-service-hub-15.emergent.host`。
- 不会永久存储任何用户数据，请求仅在内存中处理后立即丢弃。
- 支付验证采用Cardano上的Masumi协议（非托管式托管模式）。
- 该功能仅需要网络访问权限，无需文件系统或shell操作权限。

## 关于模型调用的说明

该功能会调用NEXUS AI服务API，该API会在服务器端使用大型语言模型处理您的输入数据。AI会根据输入生成响应并返回结构化结果。您可以选择不安装此功能以拒绝使用相关服务。

## 信任声明

通过安装此功能，您的输入数据将会被传输至NEXUS（https://ai-service-hub-15.emergent.host）进行AI处理。所有支付操作均通过Cardano区块链完成（非托管式）。如需了解详细文档和条款，请访问https://ai-service-hub-15.emergent.host。仅当您信任NEXUS作为服务提供商时，才建议安装此功能。