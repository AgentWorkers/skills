# maasv 内存

这是一个为 OpenClaw 代理设计的结构化长期记忆系统，由 [maasv](https://github.com/ascottbell/maasv) 提供支持。

该系统通过引入认知层来替代默认的内存后端，该认知层支持三信号检索（语义信息 + 关键词 + 知识图谱）、实体提取、时间版本控制以及基于经验的学习功能。

**maasv 完全是自托管的**，没有云服务版本。您需要在自己的机器上运行服务器，所有数据都存储在您自己控制的本地 SQLite 文件中，没有任何数据会被发送到 maasv 服务器。

## 安装

使用此功能需要 `@maasv/openclaw-memory` 插件以及一个正在运行的 maasv 服务器。

### 1. 启动服务器
```bash
pip install "maasv[server,anthropic,voyage]"
cp server.env.example .env  # fill in API keys (see below)
maasv-server
```

### 2. 安装插件
```bash
openclaw plugins install @maasv/openclaw-memory
```

### 3. 激活插件
```json5
// ~/.openclaw/openclaw.json
{
  plugins: {
    slots: { memory: "memory-maasv" },
    entries: {
      "memory-maasv": {
        enabled: true,
        config: {
          serverUrl: "http://127.0.0.1:18790",
          autoRecall: true,
          autoCapture: true,
          enableGraph: true
        }
      }
    }
  }
}
```

## 所需凭据

maasv 服务器需要一个大型语言模型（LLM）提供者（用于实体提取）和一个嵌入服务提供者（用于语义搜索）。请在您的 `.env` 文件中配置这些信息：

| 变量 | 是否必需 | 用途 |
|----------|----------|---------|
| `MAASV_LLM_PROVIDER` | 是 | 用于调用大型语言模型进行实体提取 |
| `MAASV_ANTHROPIC_API_KEY` | 如果使用 Anthropic | 用于 Anthropic 的 LLM 调用 |
| `MAASV_OPENAI_API_KEY` | 如果使用 OpenAI | 用于 OpenAI 的 LLM 调用 |
| `MAASV_EMBED_PROVIDER` | 是 | 用于选择嵌入服务提供者（如 voyage、openai 或 ollama） |
| `MAASV_VOYAGE_API_KEY` | 如果使用 Voyage | 用于 Voyage 的嵌入服务 |
| `MAASV_API_KEY` | 可选 | 用于保护 maasv 服务器端点的安全性 |

**对于完全本地化的操作**（不进行任何云调用），请使用 `ollama` 作为嵌入服务提供者，并使用本地的 LLM。maasv 针对 [Qwen3-Embedding-8B](https://ollama.com/library/qwen3-embedding) 进行优化，支持内置的 Matryoshka 维度截断功能。有关本地化的设置，请参阅 [maasv 的 README 文件](https://github.com/ascottbell/maasv)。

## 数据与网络行为

- **maasv 没有云服务**，所有服务都在您的机器上运行，数据库是一个存储在本地磁盘上的 SQLite 文件，数据完全由您控制。
- **所有外部调用都指向您自己的 LLM 或嵌入服务提供者**（Anthropic、OpenAI、Voyage），并且使用您自己的 API 密钥。如果您使用的是 ollama，那么没有任何数据会离开您的机器。  
- **该插件仅与本地主机（`127.0.0.1:18790`）进行通信**，不会发起任何外部网络请求。  
- **autoCapture** 功能会将对话摘要发送到您的本地 maasv 服务器以进行实体提取，提取出的实体会存储在本地 SQLite 数据库中。  
- **autoRecall** 功能会从本地 SQLite 数据库中读取数据，并将相关记忆内容注入代理的上下文中。  
- **maasv 不会收集或传输任何数据**，也没有任何遥测或分析功能。

## 功能概述

- `memory_search`：支持在您的记忆存储系统中进行三信号检索。  
- `memory_store`：提供去重功能的记忆存储服务。  
- `memory_forget`：实现永久性数据删除。  
- `memory_graph`：提供知识图谱功能，支持实体搜索、信息查询及关系分析。  
- `memory_wisdom`：记录推理过程、保存决策结果。

## 链接

- **插件（npm）**：[@maasv/openclaw-memory](https://www.npmjs.com/package/@maasv/openclaw-memory)  
- **服务器及核心组件（PyPI）**：[maasv](https://pypi.org/project/maasv/)  
- **源代码**：[github.com/ascottbell/maasv](https://github.com/ascottbell/maasv)