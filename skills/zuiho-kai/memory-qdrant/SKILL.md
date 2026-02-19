---
name: memory-qdrant
description: 使用 Qdrant 和 Transformers.js 实现本地语义记忆功能：通过向量嵌入技术来存储、搜索和检索对话上下文（完全基于本地处理，无需使用 API 密钥）。
version: 1.0.10
author: zuiho-kai
homepage: https://github.com/zuiho-kai/openclaw-memory-qdrant
tags: [memory, semantic-search, qdrant, transformers, embeddings, local-ai, vector-db, context]
metadata:
  openclaw:
    requires:
      bins: [node, npm]
---
# memory-qdrant

**适用场景**：当你需要 OpenClaw 代理在多次对话中通过语义搜索来记住和检索信息时，可以使用此插件。

该插件基于 Qdrant 向量数据库和 Transformers.js 嵌入技术实现本地语义记忆功能。无需任何配置，完全在本地运行，也不需要 API 密钥。

## 主要特性

- 支持使用 Transformers.js 嵌入进行语义搜索
- 可选择使用内存存储（无需配置）或 Qdrant 持久化存储
- 可选自动捕获对话上下文（默认关闭）
- 具有上下文感知的记忆检索功能
- 完全在本地运行，无需依赖外部服务或 API 密钥

## 安装

```bash
clawhub install memory-qdrant
```

**首次安装说明**：首次运行时，该插件会从 Hugging Face 下载一个 25MB 大小的嵌入模型，可能还需要安装一些构建工具（如 sharp、onnxruntime）。详细安装要求请参阅 [README](https://github.com/zuiho-kai/openclaw-memory-qdrant#readme)。

## 配置方法

在 OpenClaw 配置文件中启用该插件：

```json
{
  "plugins": {
    "memory-qdrant": {
      "enabled": true
    }
  }
}
```

**可选配置参数**：
- `autoCapture`（默认值：`false`）：自动记录对话内容。注意：触发条件包含电子邮件/电话号码的正则表达式，因此启用此功能可能会捕获个人身份信息（PII）。
- `autoRecall`（默认值：`true`）：自动检索相关记忆内容。
- `qdrantUrl`（可选）：外部 Qdrant 服务器地址（留空表示使用内存存储）

## 使用方法

提供了以下三个工具：

- `memory_store`：用于保存信息
```javascript
memory_store({
  text: "User prefers Opus for complex tasks",
  category: "preference"
})
```

- `memory_search`：用于查找相关记忆内容
```javascript
memory_search({
  query: "workflow preferences",
  limit: 5
})
```

- `memory_forget`：用于删除记忆内容
```javascript
memory_forget({ memoryId: "uuid" })
// or
memory_forget({ query: "text to forget" })
```

## 隐私与安全设置

- **内存存储模式**（默认）：重启后数据会被清除。
- **Qdrant 存储模式**：数据会被发送到配置的服务器（仅使用可信赖的服务器）。
- **网络通信**：首次运行时会从 Hugging Face 下载约 25MB 大小的模型文件。
- **自动捕获功能**：出于隐私考虑，默认是关闭的。触发条件包括电子邮件和类似电话号码的字符串，因此启用此功能可能会捕获个人身份信息。

## 技术细节

- **数据库类型**：Qdrant（支持内存存储或外部存储）
- **嵌入模型**：Xenova/all-MiniLM-L6-v2（本地生成）
- **代码实现语言**：ES6，采用工厂函数（factory function）模式

## 链接

- GitHub 仓库：https://github.com/zuiho-kai/openclaw-memory-qdrant
- 问题反馈：https://github.com/zuiho-kai/openclaw-memory-qdrant/issues