# Valence Memory

Valence Memory 是 OpenClaw 的一个持久化知识存储系统。它用带有置信度评分的信念、语义搜索、模式识别以及联邦化知识共享机制取代了传统的 flat-file 存储方式。

## 功能介绍

Valence 为你的智能体提供了“真正的记忆”功能——这不仅仅是对话记录，而是一个会随着时间推移而不断智能化的结构化知识库：

- **信念**：包含事实性陈述、维度置信度评分、领域分类以及来源追踪的信息。
- **自动回忆**：在智能体运行之前，系统会自动将相关的信念注入到对话上下文中，无需手动搜索。
- **自动捕获**：系统能自动从对话中提取有价值的见解并将其转化为信念。
- **模式识别**：能够检测出跨会话的重复行为和偏好模式。
- **实体管理**：能够追踪人物、工具、项目等实体，并记录它们之间的关系。
- **矛盾处理**：系统会揭示信念之间的矛盾，帮助用户解决这些问题。
- **会话跟踪**：完整记录对话的生命周期，并保存对话内容。
- **与 MEMORY.md 同步**：即使卸载 OpenClaw，该系统也能作为数据恢复的备用方案，确保你的知识不会丢失。

## 先决条件

使用 Valence 需要一台运行着 PostgreSQL 和 pgvector 的服务器：

```bash
# Install Valence
pip install ourochronos-valence

# Start PostgreSQL with pgvector (Docker is easiest)
docker run -d --name valence-db \
  -e POSTGRES_DB=valence \
  -e POSTGRES_USER=valence \
  -e POSTGRES_PASSWORD=valence \
  -p 5432:5432 \
  pgvector/pgvector:pg17

# Run migrations
valence-server migrate up

# Start the server
valence-server
```

默认情况下，服务器的地址为 `http://127.0.0.1:8420`。

## 安装插件

```bash
openclaw plugins install @ourochronos/memory-valence
```

## 配置

将以下配置添加到你的 OpenClaw 配置文件（`~/.openclaw/openclaw.json`）中：

```json
{
  "plugins": {
    "slots": {
      "memory": "memory-valence"
    },
    "entries": {
      "memory-valence": {
        "enabled": true,
        "config": {
          "serverUrl": "http://127.0.0.1:8420",
          "autoRecall": true,
          "autoCapture": true,
          "sessionTracking": true,
          "memoryMdSync": true
        }
      }
    }
  }
}
```

或者通过 OpenClaw 的控制界面进行配置。

### 配置选项

| 选项 | 默认值 | 说明 |
|--------|---------|-------------|
| `serverUrl` | `http://127.0.0.1:8420` | Valence 服务器的 URL |
| `authToken` | — | 令牌（或设置环境变量 `VALENCE_AUTH_TOKEN`） |
| `autoRecall` | `true` | 在智能体运行前自动插入相关信念 |
| `autoCapture` | `true` | 从对话中自动提取见解 |
| `sessionTracking` | `true` | 在 Valence 中跟踪 OpenClaw 会话 |
| `exchangeRecording` | `false` | 不记录单次对话的详细内容 |
| `memoryMdSync` | `true` | 将信念同步到 MEMORY.md 文件中（作为数据恢复的备用方案） |
| `recallMaxResults` | `10` | 自动回忆时最多插入的信念数量 |
| `recallMinScore` | `0.5` | 回忆所需的最低置信度评分（0-1） |

## 智能体工具

该插件提供了 58 个工具，按类别分类如下：

### 核心工具（使用频率最高）
- `belief_create` / `belief_query` / `belief_search` / `belief_get`：创建和查找信念。
- `belief_supersede`：在保留历史记录的情况下更新信念。
- `belief_archive`：归档信念（符合 GDPR 规范，保持信念之间的关联）。
- `confidence_explain`：解释信念的置信度评分依据。
- `entity_search` / `entity_get`：查找和检查实体。
- `tension_list` / `tension.resolve`：揭示并解决信念之间的矛盾。
- `insight_extract`：从对话中提取有价值的见解并将其转化为信念。
- `pattern_search` / `pattern_record` / `pattern_reinforce`：识别行为模式。
- `memory_search` / `memory_get`：搜索和读取 MEMORY.md 文件（作为数据恢复的备用方案）。

### 共享与联邦化
- 与可信的智能体共享信念，跨多个节点进行查询。
- 提供信任验证、声誉追踪和争议解决功能。
- 支持备份和导入，以便数据迁移。

### VKB（虚拟知识库）
- 管理会话的生命周期。
- 记录对话内容。
- 提供高级的模式识别和见解分析工具。

## 工作原理

1. **在每个智能体轮次中**，系统会自动从 Valence 中检索与当前对话相关的信念，并将其作为上下文信息注入。
2. **在对话过程中**，智能体会使用相关工具来记录决策、偏好和见解。
3. **对话结束后**，系统会自动提取未被记录的见解。
4. 随着时间的推移，信念通过相互印证而获得更高的置信度，重复出现的模式会被识别出来，智能体的理解能力也会逐渐加深。
5. `MEMORY.md` 文件作为可读的快照和安全保障被持续同步。

## 架构

```
OpenClaw Agent
    ↕ (plugin tools + hooks)
memory-valence plugin
    ↕ (REST API)
Valence Server (http://127.0.0.1:8420)
    ↕ (SQL + pgvector)
PostgreSQL + pgvector
```

该插件是一个轻量级的 REST 客户端。所有的智能处理逻辑都托管在 Valence 服务器上，包括嵌入模型、置信度评分、模式检测以及联邦化协议的处理。

## 链接

- **Valence**：[github.com/ourochronos/valence](https://github.com/ourochronos/valence) | [PyPI](https://pypi.org/project/ourochronos-valence/)
- **插件**：[github.com/ourochronos/valence-openclaw](https://github.com/ourochronos/valence-openclaw) | [npm](https://www.npmjs.com/package/@ourochronos/memory-valence)
- **问题反馈**：[github.com/ourochronos/valence/issues](https://github.com/ourochronos/valence/issues)