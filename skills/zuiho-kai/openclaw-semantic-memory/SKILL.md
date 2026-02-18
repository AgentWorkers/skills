---
name: semantic-memory
description: 本地语义记忆系统结合了向量搜索和Transformers.js技术，支持使用嵌入向量来存储、搜索和检索对话上下文（完全基于本地处理，无需API密钥）。
version: 1.0.0
author: zuiho-kai
homepage: https://github.com/zuiho-kai/openclaw-semantic-memory
tags: [memory, semantic-search, vector-search, transformers, embeddings, local-ai, context]
metadata:
  openclaw:
    requires:
      bins: [node, npm]
---
# 语义记忆（Semantic Memory）

**适用场景**：当您希望 OpenClaw 代理能够在多次对话中通过语义搜索来记住和检索信息时使用该插件。

⚠️ **隐私声明**：可选的 `autoCapture` 功能（默认禁用）在启用 `allowPIICapture` 时可能会捕获个人身份信息（如电子邮件和电话号码）。请仅在了解相关隐私影响后启用此功能。

该插件基于向量搜索和 Transformers.js 嵌入技术实现，完全本地化运行，无需任何 API 密钥。

## 主要特性

- 使用 Transformers.js 嵌入技术进行语义搜索
- 支持内存模式（无需配置）或持久化存储（使用 Qdrant 服务）
- 可选的自动对话内容捕获功能（默认禁用）
- 具有上下文感知的记忆检索能力
- 完全本地化运行，无需依赖外部服务或 API 密钥

## 安装

```bash
clawhub install semantic-memory
```

**首次安装**：首次运行时，该插件会从 Hugging Face 下载一个 25MB 大小的嵌入模型，并可能需要安装一些构建工具（如 sharp、onnxruntime）。详细安装要求请参阅 [README](https://github.com/zuiho-kai/openclaw-memory-qdrant#readme)。

## 配置

在 OpenClaw 配置文件中启用该插件：

```json
{
  "plugins": {
    "semantic-memory": {
      "enabled": true
    }
  }
}
```

**配置选项：**
- `persistToDisk`（默认值：true）：在内存模式下将记忆数据保存到磁盘。数据会保存在 `~/.openclaw-memory/` 目录中，重启后仍可保留。如需使用临时内存模式，请将此选项设置为 `false`。
- `storagePath`（可选）：自定义存储目录。默认值为 `~/.openclaw-memory/`。
- `autoCapture`（默认值：false）：自动记录对话内容。**默认开启隐私保护**：系统会自动跳过包含个人身份信息的文本。
- `allowPIICapture`（默认值：false）：在启用自动捕获功能时允许捕获个人身份信息。请仅在了解相关隐私影响后启用此选项。
- `autoRecall`（默认值：true）：自动检索相关记忆内容。
- `qdrantUrl`（可选）：外部 Qdrant 服务器地址。如使用内存存储模式，请留空。

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

## 隐私与安全

- **磁盘持久化**：记忆数据保存在 `~/.openclaw-memory/` 目录中，重启后仍可保留。如需使用临时内存模式，请将 `persistToDisk` 设置为 `false`。
- **内存模式**：当 `persistToDisk` 为 `false` 时，重启后数据会被清除。
- **Qdrant 模式**：数据会发送到配置的服务器（仅使用可信赖的服务器）。
- **网络资源**：首次运行时会从 Hugging Face 下载约 25MB 大小的模型文件。
- **个人身份信息保护**：默认情况下，自动捕获功能会跳过包含电子邮件或电话号码的文本。只有在了解相关隐私影响后才能启用 `allowPIICapture`。
- **自动捕获**：出于隐私考虑，默认情况下此功能是禁用的。启用后，系统仅捕获符合语义规则的文本（如偏好设置、决策内容、事实信息），并自动跳过个人身份信息。

## 技术细节

- 数据存储方式：使用向量数据库 Qdrant（支持内存存储或外部存储）。
- 嵌入模型：Xenova/all-MiniLM-L6-v2（本地部署）。
- 代码实现：基于 ES6 语言，采用工厂函数模式（factory function pattern）。

## 链接

- GitHub 仓库：https://github.com/zuiho-kai/openclaw-semantic-memory
- 问题报告：https://github.com/zuiho-kai/openclaw-semantic-memory/issues