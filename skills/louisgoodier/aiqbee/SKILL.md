---
name: aiqbee
description: 通过 MCP 连接到您的 Aiqbee 知识图谱。在您的架构、产品组合以及数字战略系统中搜索、创建并链接神经元（即数据节点或功能模块）。
homepage: https://aiqbee.com
metadata: {"clawdbot":{"emoji":"🧠"}}
---
# Aiqbee 脑（Aiqbee Brain）

将您的 OpenClaw 助手连接到 [Aiqbee](https://aiqbee.com) 知识图谱中。通过自然语言对话，在您的架构、产品组合和数字战略管理中搜索、创建和关联知识。

## 设置（Setup）

### 选项 1：直接 MCP 配置（推荐）

在您的 `openclaw.json` 文件中添加以下配置：

```json
{
  "mcpServers": {
    "aiqbee": {
      "transport": "streamable-http",
      "url": "https://mcp.aiqbee.com/mcp"
    }
  }
}
```

系统会提示您使用 Aiqbee 账户登录（支持 OAuth 2.0，会打开浏览器）。

### 选项 2：通过 mcporter

如果您已安装了 mcporter，请在 `config/mcporter.json` 文件中添加相应的配置：

```json
{
  "mcpServers": {
    "aiqbee": {
      "baseUrl": "https://mcp.aiqbee.com/mcp",
      "description": "Aiqbee knowledge graph"
    }
  }
}
```

使用以下命令验证配置是否正确：

```bash
mcporter list aiqbee
```

## 认证（Authentication）

Aiqbee 使用 OAuth 2.0 进行身份验证。首次连接时，系统会打开浏览器页面让您登录。无需使用 API 密钥或环境变量，只需使用现有的 Aiqbee 账户登录即可。

## 可用工具（Available Tools, 12 个）

### 读取（Read）

| 工具 | 描述 |
|------|-------------|
| `aiqbee_search` | 在知识图谱中搜索神经元 |
| `aiqbee_fetch` | 获取神经元的完整内容和元数据 |
| `aiqbee_get_brain_info` | 获取大脑的元数据和统计信息 |
| `aiqbee_get_neuron_types` | 列出所有神经元类型及其数量 |
| `aiqbee_list_neurons` | 带有过滤功能的神经元列表（分页显示） |
| `aiqbee_get_relationships` | 获取某个神经元的输入/输出关系 |

### 写入（Write）

| 工具 | 描述 |
|------|-------------|
| `aiqbee_create_neuron` | 在知识图谱中创建新的神经元 |
| `aiqbee_update_neuron` | 更新现有的神经元 |
| `aiqbee_delete_neuron` | 删除神经元 |
| `aiqbee_create_relationship` | 在两个神经元之间创建关联 |
| `aiqbee_update_relationship` | 更新现有的关联 |
| `aiqbee_delete_relationship` | 删除关联 |

## 使用示例（Usage Examples）

### 在知识图谱中搜索

“在我的知识图谱中搜索与‘云迁移’相关的内容”

```bash
mcporter call 'aiqbee.aiqbee_search(query: "cloud migration")'
```

### 获取神经元的完整信息

“显示 API 网关神经元的详细信息”

```bash
mcporter call 'aiqbee.aiqbee_fetch(neuron_id: "neuron-uuid-here")'
```

### 创建新的神经元

首先调用 `aiqbee_get_neuron_types()` 获取有效的神经元类型 ID，然后创建新的神经元：

```bash
mcporter call 'aiqbee.aiqbee_create_neuron(
  neuron_type_id: "type-uuid-from-get-neuron-types",
  name: "gRPC for internal services",
  content: "We decided to use gRPC for all internal service-to-service communication."
)'
```

### 关联神经元

使用搜索或创建过程中返回的神经元 ID 来建立关联：

```bash
mcporter call 'aiqbee.aiqbee_create_relationship(
  source_neuron_id: "source-uuid",
  target_neuron_id: "target-uuid",
  link_description: "depends on"
)'
```

### 列出神经元类型

“我的知识图谱中有哪些类型的知识？”

```bash
mcporter call 'aiqbee.aiqbee_get_neuron_types()'
```

### 查看大脑概览

“提供我的架构管理系统的概览”

```bash
mcporter call 'aiqbee.aiqbee_get_brain_info()'
```

## 什么是 Aiqbee？

[Aiqbee](https://aiqbee.com) 是一个基于 Web 的架构管理、产品组合和数字战略管理平台。它将知识组织成由“神经元”通过“突触”连接的交互式知识图谱。

- **知识图谱（Knowledge Graphs）**：将想法组织成由“神经元”通过“突触”连接的结构。
- **架构管理（Architecture Management）**：记录和管理企业架构。
- **产品组合管理（Portfolio Management）**：跟踪产品、项目和数字资产。
- **智能搜索（AI-Powered Search）**：在知识库中快速查找所需内容。
- **协作（Collaboration）**：提供基于角色的团队工作空间。

## 资源（Resources）

- [Aiqbee 平台](https://app.aiqbee.com)
- [文档](https://app.aiqbee.com/help)
- [MCP 服务器](https://mcp.aiqbee.com/mcp)
- [GitHub 仓库](https://github.com/AIQBee/aiqbee-ai)