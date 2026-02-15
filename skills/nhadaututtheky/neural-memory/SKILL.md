---
name: neural-memory
description: |
  Associative memory with spreading activation for persistent, intelligent recall.
  Use PROACTIVELY when:
  (1) You need to remember facts, decisions, errors, or context across sessions
  (2) User asks "do you remember..." or references past conversations
  (3) Starting a new task — inject relevant context from memory
  (4) After making decisions or encountering errors — store for future reference
  (5) User asks "why did X happen?" — trace causal chains through memory
  Zero LLM dependency. Neural graph with Hebbian learning, memory decay, contradiction detection, and temporal reasoning.
homepage: https://github.com/nhadaututtheky/neural-memory
metadata: {"openclaw":{"emoji":"brain","primaryEnv":"NEURALMEMORY_BRAIN","requires":{"bins":["python3"],"env":["NEURALMEMORY_BRAIN"]},"os":["darwin","linux","win32"],"install":[{"id":"pip","kind":"node","package":"neural-memory","bins":["nmem"],"label":"pip install neural-memory"}]}}
---

# NeuralMemory — 为AI代理设计的联想式记忆系统

这是一个受生物学启发的记忆系统，它采用“扩散激活”（spreading activation）机制，而非传统的关键词/向量搜索方式。记忆以神经图的形式存在，神经元通过20种不同类型的突触相互连接。频繁被访问的记忆会加强它们之间的连接（基于赫布学习原理，Hebbian learning），而过时的记忆会自然衰退。系统能够自动检测记忆之间的矛盾。

**为什么不用传统的向量搜索呢？**  
向量搜索只能找到与查询内容相似的文档，而NeuralMemory则通过遍历神经图来找到*概念上相关*的记忆——即使这些记忆之间没有关键词或嵌入信息的重叠。例如，当用户询问“我们关于授权问题做了什么决定？”时，系统会同时激活与时间、实体和概念相关的神经元，从而找到相关的记忆。

## 设置

### 1. 安装NeuralMemory

```bash
pip install neural-memory
nmem init
```

安装完成后，系统会在`~/.neuralmemory/`目录下创建一个默认的记忆结构，并自动配置MCP（Memory Control Protocol）。

### 2. 为OpenClaw配置MCP

将以下配置添加到OpenClaw的MCP配置文件（`~/.openclaw/mcp.json`或项目配置文件`openclaw.json`）中：

```json
{
  "mcpServers": {
    "neural-memory": {
      "command": "python3",
      "args": ["-m", "neural_memory.mcp"],
      "env": {
        "NEURALMEMORY_BRAIN": "default"
      }
    }
  }
}
```

### 3. 验证配置

```bash
nmem stats
```

此时，你应该能够看到系统的基本统计信息（包括神经元数量、突触数量等）。

## 工具参考

### 核心记忆工具

| 工具 | 功能 | 使用场景 |
|------|---------|-------------|
| `nmem_remember` | 存储记忆 | 在做出决策、遇到错误或需要记录事实、见解时使用 |
| `nmem_recall` | 查询记忆 | 在执行任务前，或用户需要回顾过去的信息时使用 |
| `nmem_context` | 获取最近的记忆 | 会话开始时，用于注入新的上下文信息 |
| `nmem_todo` | 创建有效期为30天的待办事项列表 | 用于任务管理 |

### 智能辅助工具

| 工具 | 功能 | 使用场景 |
|------|---------|-------------|
| `nmem_auto` | 从文本中自动提取记忆 | 在重要对话后，自动捕捉决策、错误和待办事项 |
| `nmem_recall`（深度=3） | 深度联想回忆 | 需要跨领域关联的复杂问题 |
| `nmem_habits` | 提供工作流程建议 | 当用户重复相似的操作序列时使用 |

### 管理工具

| 工具 | 功能 | 使用场景 |
|------|---------|-------------|
| `nmem_health` | 检查记忆系统的健康状况 | 定期检查系统性能，特别是在共享记忆之前 |
| `nmem_stats` | 查看记忆系统的统计信息 | 快速了解记忆的使用情况 |
| `nmem_version` | 创建记忆系统的快照并进行回滚 | 在执行高风险操作前，用于备份数据 |
| `nmem_transplant` | 在不同系统之间传输记忆 | 实现知识共享 |

## 工作流程

### 会话开始时
1. 调用`nmem_context`将最近的记忆加载到用户的认知中。
2. 如果用户提到了某个特定主题，可以调用`nmem_recall`来检索与该主题相关的记忆。

### 对话过程中
- 当做出决策时：使用`nmem_remember`并指定记忆类型为“decision”。
- 当出现错误时：使用`nmem_remember`并指定记忆类型为“error”。
- 当用户表达偏好时：使用`nmem_remember`并指定记忆类型为“preference”。
- 当需要回顾过去的事件时：根据需要调用`nmem_recall`并设置适当的搜索深度。

### 会话结束时
1. 对于重要的对话内容，调用`nmem_auto`并指定操作类型为“process”，系统会自动提取相关的事实、决策和待办事项。

## 示例

### 记录一个决策
```
nmem_remember(
  content="Use PostgreSQL for production, SQLite for development",
  type="decision",
  tags=["database", "infrastructure"],
  priority=8
)
```

### 通过扩散激活机制进行回忆
```
nmem_recall(
  query="database configuration for production",
  depth=1,
  max_tokens=500
)
```
该机制通过遍历神经图来检索记忆，而不是依赖关键词匹配。即使没有共享的关键词，系统也能找到相关的记忆（例如：“部署任务使用了Docker，并进行了pg_dump备份”）。

### 追踪因果关系链
```
nmem_recall(
  query="why did the deployment fail last week?",
  depth=2
)
```
系统通过`CAUSED_BY`和`LEADS_TO`突触来追踪事件之间的因果关系。

### 从对话中自动提取信息
```
nmem_auto(
  action="process",
  text="We decided to switch from REST to GraphQL because the frontend needs flexible queries. The migration will take 2 sprints. TODO: update API docs."
)
```
系统会自动提取：1个决策、1个事实、1个待办事项。

## 主要特性

- **完全不依赖大型语言模型（LLM）**：完全基于算法实现，包括正则表达式处理、神经图遍历和赫布学习机制。
- **扩散激活**：通过神经图进行联想式回忆，而非关键词/向量搜索。
- **支持20种突触类型**：用于表示时间顺序（BEFORE/AFTER）、因果关系（CAUSED_BY/LEADS_TO）、语义关系（IS_A/HAS_PROPERTY）、情感状态（FELT/EVOKES）以及记忆的冲突（CONTRADICTS）。
- **记忆生命周期**：从短期记忆到长期记忆，再到具有艾宾浩斯遗忘规律的语义记忆。
- **自动检测矛盾**：系统能自动识别相互冲突的记忆，并优先处理过时的记忆。
- **赫布学习**：经常一起激活的神经元会形成更牢固的连接，从而提升记忆的稳定性。
- **时间推理**：支持因果链的追踪、事件序列的分析以及时间范围的查询。
- **记忆版本管理**：支持创建记忆快照和回滚功能，以便在不同版本间进行数据交换。
- **支持多语言**：同时支持越南语和英语，便于信息的提取和情感分析。

## 回忆深度

| 回忆深度 | 名称 | 处理速度 | 使用场景 |
|-------|------|-------|----------|
| 0 | 即时回忆 | <10毫秒 | 快速获取事实或最近的信息 |
| 1 | 基本回忆 | 约50毫秒 | 标准的回忆功能 |
| 2 | 工作流程建议 | 约200毫秒 | 用于模式匹配和工作流程建议 |
| 3 | 深度回忆 | 约500毫秒 | 支持跨领域的关联分析和因果关系链的追踪 |

## 注意事项

- 记忆数据存储在本地SQLite数据库（路径：`~/.neuralmemory/brains/<brain>.db`）中。
- 除非配置了外部嵌入服务，否则系统不会将数据发送到任何外部服务。
- 每个记忆系统都是独立的，不存在数据交叉污染的问题。
- `nmem_remember`会返回一个`fiber_id`，用于追踪记忆的来源。
- 记忆的优先级范围从0（最不重要）到10（最重要），默认值为5。
- 记忆类型包括：事实、决策、偏好、待办事项、见解、上下文、指令、错误、工作流程信息等。