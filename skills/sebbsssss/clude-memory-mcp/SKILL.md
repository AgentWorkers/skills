---
name: Clude Memory MCP
description: MCP服务器是Clude四层认知记忆系统的重要组成部分，负责数据的存储、检索、搜索以及梦境的生成等功能。该系统基于Supabase和pgvector技术构建，支持针对不同数据类型的衰减机制（decay mechanism），并利用Hebbian关联图（Hebbian association graphs）来处理神经元之间的连接关系。数据的安全存储与传输通过Solana区块链技术实现。
metadata:
  openclaw:
    requires:
      env:
        - SUPABASE_URL
        - SUPABASE_SERVICE_KEY
      bins:
        - node
    primaryEnv: SUPABASE_URL
---
# Clude Memory MCP

MCP服务器采用了一种四层认知记忆架构，该架构的灵感来源于斯坦福大学的生成式代理模型（Park等人，2023年）。

## 工具

### `recall_memories`
用于搜索记忆系统。返回根据相关性、重要性、最近使用频率和向量相似度排序的记忆结果。

- `query` — 用于搜索记忆摘要的文本
- `tags` — 按标签过滤
- `related_user` — 按用户/代理ID过滤
- `memory_types` — 按类型过滤：`episodic`（事件）、`semantic`（语义）、`procedural`（程序性）、`self_model`（自我模型）
- `limit` — 最大结果数量（1-20，默认为5）
- `min_importance` — 最小重要性阈值（0-1）

### `store_memory`
用于存储新的记忆。记忆会在对话中持续存在，如果未被访问则会随时间衰减，并最终被存储到Solana区块链上。

- `type` — 记忆类型：`episodic`（事件）、`semantic`（知识）、`procedural`（行为）、`self_model`（自我模型）
- `content` — 记忆的完整内容
- `summary` — 用于检索的简短摘要
- `tags` — 用于过滤的标签
- `importance` — 重要性得分（0-1）
- `source` — 记忆的来源标识符（例如 `mcp:my-agent`）

### `get_memory_stats`
用于获取统计信息：按类型统计的记忆数量、平均重要性/衰减率、梦境会话历史记录以及热门标签。

### `get_market_mood`
用于获取当前的市场情绪和价格状态（无需调用LLM）。

### `ask_clude`
用于向Claude提问并获取角色化的响应。该功能通过调用Claude的API来实现。

## 设置

```bash
npm install clude-bot
```

需要一个包含`supabase-schema.sql`中定义的数据库模式的Supabase项目。请设置`SUPABASE_URL`和`SUPABASE_SERVICE_KEY`环境变量。

## 架构

- **四层记忆系统**：
  - `episodic`（事件）：每天衰减7%
  - `semantic`（语义）：每天衰减2%
  - `procedural`（程序性）：每天衰减3%
  - `self_model`（自我模型）：每天衰减1%
- **混合检索机制**：结合pgvector余弦相似度算法、关键词匹配和标签评分
- **梦境周期**：每6小时进行一次记忆整合、反思和更新
- **链上存储**：使用SHA-256哈希算法将记忆数据存储到Solana区块链上
- **细粒度检索**：通过片段级嵌入实现精确的记忆检索

## 许可证

MIT许可证