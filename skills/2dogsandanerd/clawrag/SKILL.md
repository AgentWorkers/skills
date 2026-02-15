# ClawRAG 连接器

**OpenClaw 的核心组件**——一个支持混合搜索的自托管 RAG（Retrieval, Association, and Generation）引擎。

> ⚠️ 本组件需要 Docker 来运行。它用于将 OpenClaw 与您的本地 ClawRAG 实例连接起来。

## 什么是 ClawRAG？

一个可用于生产环境的 RAG 架构，能够将数据存储在本地：
- 🔒 **隐私优先**：所有数据都存储在您的机器上
- 🔍 **混合搜索**：结合语义搜索和关键词搜索（使用 BM25 算法进行排名）
- 📄 **智能数据导入**：支持 PDF、Office 文档以及 Markdown 格式的文件导入（通过 Docling 工具）
- 🧠 **与 MCP（Memory-Based Computing Platform）无缝集成**：支持与 OpenClaw 的紧密协作

## 安装

### 第一步：启动 ClawRAG（使用 Docker）
```bash
git clone https://github.com/2dogsandanerd/ClawRag.git
cd ClawRag
cp .env.example .env
docker compose up -d
```

等待 `http://localhost:8080/health` 返回 “OK” 状态。

### 第二步：将 OpenClaw 与 ClawRAG 连接
```bash
openclaw mcp add --transport stdio clawrag npx -y @clawrag/mcp-server
```

### 验证
测试您的安装配置：
```bash
curl http://localhost:8080/api/v1/rag/collections
```

## 主要功能

| 功能            | 描述                                      |
|------------------|-----------------------------------------|
| 文档上传        | 支持通过 API 或文件夹上传 PDF、DOCX、TXT、MD 格式的文件           |
| 混合搜索        | 结合向量相似度和关键词匹配进行搜索                   |
| 引用功能        | 为所有搜索结果提供来源信息                         |
| 多集合管理      | 可按项目对知识内容进行分类和组织                   |

## 系统要求

- Docker 及 Docker Compose 工具
- 至少 4GB 的内存（推荐使用 8GB 内存以支持本地大语言模型）
- 或者：需要 OpenAI/Anthropic 的 API 密钥以使用云端大语言模型

## 架构概述
```
OpenClaw ◄──MCP──► @clawrag/mcp-server ◄──HTTP──► ClawRAG API (localhost:8080)
                                           │
                                           ▼
                                    ┌─────────────┐
                                    │  ChromaDB   │
                                    │  (vectors)  │
                                    └─────────────┘
```

## 相关链接

- 📚 官方文档：https://github.com/2dogsandanerd/ClawRag#readme
- 🔧 API 参考文档：http://localhost:8080/docs （在应用程序运行时访问）
- 🐛 问题反馈：https://github.com/2dogsandanerd/ClawRag/issues
- MCP 包：https://www.npmjs.com/package/@clawrag/mcp-server

## 标签

rag, vector, memory, search, documents, self-hosted, privacy, mcp, local-ai

---

## ClawHub 上传所需的元数据

| 字段            | 值                                      |
|------------------|-----------------------------------------|
| **slug**           | `clawrag`                                      |
| **显示名称**        | `ClawRAG - 自托管 RAG 与内存管理工具`                   |
| **版本**           | `1.2.0`                                      |
| **标签**           | `rag`, `vector`, `memory`, `search`, `documents`, `self-hosted`, `privacy`, `mcp`, `local-ai` |

## 版本 1.2.0 的更新日志

### 1.2.0 版本更新内容

- 新增了用于 OpenClaw 集成的连接器组件
- 支持 MCP 服务器（版本 @clawrag/mcp-server v1.1.0）
- 采用 Docker 作为主要部署方式
- 引入了混合搜索功能（结合向量相似度和 BM25 算法进行搜索）