---
name: microsoft-docs
description: 查询微软的官方文档，以了解相关概念、查找教程，并学习各项服务的工作原理。这些文档适用于 Azure、.NET、Microsoft 365、Windows、Power Platform 以及所有微软技术。您可以从 learn.microsoft.com 及其他微软官方网站获取准确、最新的信息，包括架构概述、快速入门指南、配置指南、使用限制以及最佳实践。
context: fork
compatibility: Requires Microsoft Learn MCP Server (https://learn.microsoft.com/api/mcp)
---

# Microsoft 文档

## 工具

| 工具 | 用途 |
|------|---------|
| `microsoft_docs_search` | 查找文档——包括概念、指南、教程和配置信息 |
| `microsoft_docs_fetch` | 获取完整页面内容（当搜索结果不足以满足需求时） |

## 适用场景

- **理解技术概念** — 例如：“Cosmos DB 的分区机制是如何工作的？”
- **学习某个服务** — 例如：“Azure Functions 的概述”、“容器应用程序的架构”
- **查找教程** — 例如：“快速入门”、“操作指南”、“分步说明”
- **查看配置选项** — 例如：“App Service 的配置设置”
- **了解限制和配额** — 例如：“Azure OpenAI 的使用频率限制”、“Service Bus 的配额”
- **了解最佳实践** — 例如：“Azure 的安全最佳实践”

## 查询效率

有效的查询应具有明确的目标：

```
# ❌ Too broad
"Azure Functions"

# ✅ Specific
"Azure Functions Python v2 programming model"
"Cosmos DB partition key design best practices"
"Container Apps scaling rules KEDA"
```

在查询时请提供以下上下文信息：
- **相关版本**（例如：`.NET 8`、`EF Core 8`）
- **查询目的**（例如：快速入门、教程、概述、限制信息）
- **目标平台**（例如：Linux、Windows）

## 何时获取完整页面内容

在以下情况下，建议获取完整页面内容：
- **需要详细教程** — 需要完整的操作步骤
- **需要查看配置指南** — 需要列出所有配置选项
- **需要深入了解某个功能** — 需要全面的说明
- **搜索结果被截断** — 需要查看完整的上下文信息

## 使用这些工具的原因

- **准确性** — 这些文档是实时更新的，而非可能过时的培训资料
- **完整性** — 教程提供了完整的操作步骤，而非零散的信息
- **权威性** — 这些文档来自微软官方