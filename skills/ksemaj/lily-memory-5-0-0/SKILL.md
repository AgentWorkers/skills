---
name: lily-memory
description: OpenClaw代理的持久化内存插件：结合了SQLite FTS5的关键词搜索功能与Ollama的向量语义搜索技术，支持自动捕获、自动召回、故障检测以及内存优化功能。该插件完全不依赖于npm包。
metadata:
  openclaw:
    requires:
      bins: [node, sqlite3]
    primaryEnv: ""
---
# Lily Memory

这是一个为 OpenClaw 代理设计的持久化内存插件，可为代理提供长期存储能力，确保数据在会话重置、数据压缩或系统重启后仍然可用。

## 功能介绍

- **自动回忆**：在每次 LLM（大型语言模型）轮次开始前，将相关记忆内容注入到代理的上下文中。
- **自动捕获**：从对话中提取事实信息并自动存储。
- **混合搜索**：结合 SQLite 的 FTS5 关键词搜索技术与 Ollama 的向量相似度算法进行搜索。
- **陷入循环检测**：检测对话主题的重复性，并提示代理打破循环。
- **内存整合**：在系统启动时删除重复的数据条目。
- **动态实体管理**：通过配置文件管理允许添加的实体列表，并在运行时动态添加新实体。
- **优雅降级机制**：即使没有 Ollama 也能正常工作（仅支持基于关键词的搜索）。
- **无 npm 依赖**：仅使用 `sqlite3 CLI` 和原生的 `fetch` 功能进行数据交互。

## 系统要求

- Node.js 18 及以上版本（用于支持原生的 `fetch` 功能）。
- 安装了 SQLite 3.33 及更高版本（包含 FTS5 支持；在 macOS 上可通过 `apt install sqlite3` 安装，在 Linux 上同样可用）。
- 可选：如果需要语义搜索功能，需安装带有 `nomic-embed-text` 模型的 Ollama。

## 快速入门

1. 将插件安装到您的 `extensions` 目录中。
2. 在 `openclaw.json` 配置文件中添加以下配置：

```json
{
  "plugins": {
    "slots": { "memory": "lily-memory" },
    "entries": {
      "lily-memory": {
        "enabled": true,
        "config": {
          "dbPath": "~/.openclaw/memory/decisions.db",
          "entities": ["config", "system"]
        }
      }
    }
  }
}
```

3. 重启 OpenClaw 代理：`openclaw gateway restart`

## 可用工具

| 工具 | 功能描述 |
|------|-------------|
| `memory_search` | 对所有存储的事实信息进行 FTS5 关键词搜索 |
| `memory_entity` | 根据特定实体名称查询所有相关事实 |
| `memory_store` | 将事实信息保存到持久化内存中 |
| `memory_semantic_search` | 通过 Ollama 进行向量相似度搜索 |
| `memory_add_entity` | 在运行时注册新实体 |

## 配置选项

| 选项 | 类型 | 默认值 | 描述 |
|--------|------|---------|-------------|
| `dbPath` | 字符串 | `~/.openclaw/memory/decisions.db` | SQLite 数据库路径 |
| `autoRecall` | 布尔值 | `true` | 每次轮次开始前自动回忆记忆内容 |
| `autoCapture` | 布尔值 | `true` | 从响应中自动提取事实信息 |
| `maxRecallResults` | 整数 | `10` | 每次轮次可回忆的最大记忆条目数 |
| `maxCapturePerTurn` | 整数 | 每次响应最多捕获的事实数量 |
| `stuckDetection` | 布尔值 | `true` | 检测对话主题是否重复 |
| `vectorSearch` | 布尔值 | `true` | 使用 Ollama 进行语义搜索 |
| `ollamaUrl` | 字符串 | `http://localhost:11434` | Ollama 服务器地址 |
| `embeddingModel` | 字符串 | `nomic-embed-text` | 用于实体嵌入的模型 |
| `consolidation` | 布尔值 | `true` | 启动时删除重复数据 |
| `vectorSimilarityThreshold` | 数值 | `0.5` | 最小向量相似度阈值 |
| `entities` | 数组 | `[]` | 允许添加的实体名称列表 |

## 架构说明

- **回忆流程**：从消息中提取关键词 → 使用 FTS5 进行搜索 → 合并并删除重复数据 → 将结果注入代理的上下文中。
- **捕获流程**：使用正则表达式扫描包含 `entity: key = value` 模式的字符串 → 根据允许的实体列表验证实体 → 将数据存储到 SQLite 数据库中 → 通过 Ollama 进行异步嵌入。
- **陷入循环检测**：统计每次响应中出现频率最高的 5 个词汇 → 如果连续 3 次的词汇相似度超过 60%，则提示代理采取相应行动（例如“反思”）。

## 许可证

MIT 许可证。