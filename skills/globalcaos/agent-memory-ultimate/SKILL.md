---
name: agent-memory-ultimate
version: 3.0.1
description: "将您的代理的令牌使用量减少60-80%——不要再将整个文件内容直接传输到上下文中了。OpenClaw代理采用了向量搜索、知识图谱、RAPTOR层次结构以及自动整合技术，实现了高效的认知记忆功能。数据只需存储一次，即可实现精确的检索。所有操作都在本地完成，无需任何API费用。"
homepage: https://github.com/globalcaos/clawdbot-moltbot-openclaw
repository: https://github.com/globalcaos/clawdbot-moltbot-openclaw
metadata:
  openclaw:
    emoji: "🧠"
    tags:
      - memory
      - cognitive
      - sqlite
      - vector-search
      - knowledge-graph
      - raptor
      - embeddings
      - token-savings
      - consolidation
      - recall
      - offline
      - long-term-memory
      - sleep-cycle
---

# Agent Memory Ultimate

**将您的代理的令牌使用量减少60-80%。** 不再需要将整个文件读入内存以获取上下文信息——只需存储一次记忆内容，然后仅检索相关的内容。通过向量搜索、知识图谱、自动衰减机制以及RAPTOR层次结构，您的代理将拥有类似人类的记忆功能，且这种功能能够真正实现可扩展性。

**完全无需依赖云API，零成本。所有操作都在本地完成。**

---

## 为什么节省令牌如此重要

每当您的代理读取`MEMORY.md`文件或每日日志时，都会消耗大量令牌。而这些内容中的大部分与当前的问题并不相关。

| 方法 | 每次检索所需的令牌数 | 精确度 |
|----------|-------------------|-----------|
| 读取整个MEMORY.md文件 | 3,000-10,000 | 约5%的相关性 |
| 读取每日日志 + MEMORY.md文件 | 5,000-20,000 | 约10%的相关性 |
| 使用`mem.py`和`query`进行检索 | 200-800 | 约80%的相关性 |
| 使用`mem.py`和`primed-recall`（基于上下文的检索） | 300-1,000 | 约90%的相关性 |

**对于一个每天进行50次检索的代理来说：**
- 旧方法：每天因读取记忆内容而消耗约50万个令牌 |
- 使用v3版本后：每天仅消耗约3万个令牌 |
**节省的令牌数：约47万个令牌**（相当于每天节省7-14美元的API费用，或为Claude Max模型提供了更多的使用空间）

通过这种方式，代理能够在使用更少的上下文信息的情况下获得更准确的答案。

---

## v3的新功能

v2版本仅使用了Markdown文件和FTS5关键词搜索功能。v3版本则增加了**完整的认知架构**：

| 功能 | v2 | v3 |
|---------|----|----|
| 存储方式 | Markdown文件 | SQLite + sqlite-vec嵌入 |
| 搜索方式 | 仅使用FTS5关键词 | 混合方式（向量搜索 + 关键词搜索 + BM25算法） |
| 检索方式 | 读取整个文件 | 通过多种策略精确检索片段 |
| 关联功能 | 无 | 支持多跳遍历的知识图谱 |
| 层次结构 | 平面文件结构 | RAPTOR树结构（L0→L1→L2→L3抽象层次） |
| 衰减机制 | 手动清理 | 自动衰减机制 + 明确的半衰期设置 |
| 数据整合方式 | 定时文本提示 | 聚类 + 合并 + 重建层次结构 |
| 上下文预处理 | 无 | 从对话中获取上下文信息 |
| 数据共享方式 | 无 | 支持跨代理共享，并具有敏感性控制 |
| 令牌消耗 | 高（读取整个文件） | 低（针对性检索） |

**v2版本仍然可以使用。** Markdown文件、每日日志以及MEMORY.md文件的所有设置都保持不变。v3版本通过增加一个并行认知层，显著减少了令牌的浪费。**

---

## 架构细节

```
┌─────────────────────────────────────┐
│         Agent Session               │
│  (reads MEMORY.md, daily logs)      │  ← v2 (unchanged)
├─────────────────────────────────────┤
│         mem.py CLI                  │  ← v3 (NEW)
│  store / recall / consolidate       │
├──────────┬──────────┬───────────────┤
│ sqlite-vec│  FTS5   │ Association   │
│ (vectors) │(keyword)│   Graph       │
├──────────┴──────────┴───────────────┤
│            memory.db                │
│  memories, associations, hierarchy  │
│  shares, embeddings (384-dim)       │
└─────────────────────────────────────┘
```

- **嵌入模型：** `all-MiniLM-L6-v2`（384维，约80MB，ONNX格式） |
- **向量搜索：** `sqlite-vec`——无需使用Pinecone或Weaviate，也无需依赖云服务 |
- **数据库：** `db/memory.db`（单个文件，便于携带且可备份）

---

## 快速入门

```bash
# 1. Initialize database
python3 scripts/mem.py init

# 2. Start the local embedding server (port 9999)
bash scripts/start-memory.sh

# 3. Store a memory
python3 scripts/mem.py store "Oscar prefers wired home automation" --type semantic --importance 0.8

# 4. Recall it (200 tokens instead of 10,000)
python3 scripts/mem.py recall "home automation preferences"
```

就这样，您的代理现在具备了精确的记忆检索功能。

---

## 6种检索策略

并非所有查询都适用相同的检索方法。请根据实际情况选择合适的策略：

| 检索策略 | 适用场景 | 命令 | 使用时机 |
|----------|----------|---------|------|
| **混合策略**（默认） | 通用检索 | `mem.py recall "query"` | 大多数查询 |
| **向量搜索** | 基于语义相似性的检索 | `recall --strategy vector` | 模糊或概念性查询 |
| **关键词搜索** | 检索精确的术语或ID | `recall --strategy keyword` | 文件名、代码等 |
| **自适应策略** | 自动选择检索细节 | `mem.py recall-adaptive "query"` | 探索性查询 |
| **图谱搜索** | 跟踪概念之间的关联 | `mem.py recall-assoc "query" --hops 2` | 相关概念的检索 |
| **预处理检索** | 基于上下文的检索 | `mem.py primed-recall "q" --context "..."` | 在对话过程中使用的检索 |

**预处理检索**是一个非常实用的功能——通过传递用户最后2-3条消息作为上下文，检索结果会更加符合对话内容。这正是人类记忆的工作方式。

---

## 命令行参考

### 核心命令

| 命令 | 描述 |
|---------|-------------|
| `mem.py init` | 创建数据库架构 |
| `mem.py migrate` | 从jarvis.db导入现有文档 |
| `mem.py store <内容> [--类型 TYPE] [--来源 SRC] [--重要性 N]` | 存储记忆内容 |
| `mem.py recall <查询> [--策略 hybrid\|vector\|keyword] [--限制 N]` | 检索记忆内容 |
| `mem.py forget <id\|--查询 QUERY>` | 软删除记忆内容（令牌强度降为0） |
| `mem.py hard-delete <id>` | 永久删除记忆内容 |
| `mem.py stats` | 查看数据库统计信息 |

**记忆类型：** `episodic`（事件相关）、`semantic`（事实相关）、`procedural`（操作指南相关）、`preference`（用户偏好相关）

### 知识图谱

| 命令 | 描述 |
|---------|-------------|
| `mem.py associate <src_id> <tgt_id> [--类型 TYPE] [--权重 N]` | 关联两个记忆内容 |
| `mem.py links <memory_id>` | 显示所有关联关系 |
| `mem.py recall-assoc <查询> [--跳数 N] [--限制 N]` | 多跳遍历记忆内容 |
| `mem.py graph-stats` | 查看图谱统计信息 |

**边类型：** `related`（相关）、`caused_by`（由...引起）、`part_of`（属于...）、`contradicts`（矛盾）、`temporal`（时间相关的）、`supports`（支持的）

### RAPTOR层次结构

| 命令 | 描述 |
|---------|-------------|
| `mem.py build-hierarchy [--层次数 N]` | 构建抽象层次结构 |
| `mem.py recall-adaptive <查询> [--详细程度 auto\|广泛\|具体\|0-3]` | 在适当的抽象层次上进行检索 |
| `mem.py hierarchy-stats` | 显示层次结构 |

**查询示例：**
- 广泛查询（例如：“我对AI了解多少？”）会匹配高层次的摘要信息。
- 具体查询（例如：“sqlite-vec版本的详细信息”）会匹配具体的记忆节点。
**系统会自动选择合适的检索层次。**

### 激活信息传播机制

| 命令 | 描述 |
|---------|-------------|
| `mem.py primed-recall <查询> [--上下文 'text1' 'text2'] [--限制 N]` | 基于上下文进行预处理后的检索 |

### 跨代理数据共享

| 命令 | 描述 |
|---------|-------------|
| `mem.py share <记忆ID> --与 <代理> 共享` [--敏感度 N]` | 共享记忆内容 |
| `mem.py shared [--来自 AGENT] [--到 AGENT]` | 查看共享列表 |
| `mem.py revoke <共享ID> \| --记忆 <ID>` | 取消对共享内容的访问权限 |

**敏感度级别：** 0（公开）→ 5（最高机密）。默认设置为3。共享前需双方代理同意。**

### 维护操作

| 命令 | 描述 |
|---------|-------------|
| `mem.py consolidate [--天数 N] [--仅衰减]` | 执行完整的整合流程 |

整合流程包括：衰减处理 → 数据聚类 → 合并重复项 → 重建层次结构。

---

## 日常工作流程

### 启动

```markdown
1. Read SOUL.md, USER.md (identity — small, always load)
2. Read today's daily log (recent context)
3. Use `mem.py primed-recall "session start"` for relevant memories
   → Gets 200-800 tokens of precisely relevant context
   → Instead of 10,000+ tokens from reading MEMORY.md cover-to-cover
```

### 白天工作流程

```bash
# Store important facts as they come up
mem.py store "Client meeting moved to March 1" --type episodic --importance 0.7

# Before answering from memory — recall, don't read files
mem.py recall "client meeting schedule"

# Link related memories when you notice connections
mem.py associate 42 87 --type related
```

### 夜间整合流程

```json
{
  "schedule": { "kind": "cron", "expr": "0 3 * * *", "tz": "America/Los_Angeles" },
  "payload": {
    "kind": "agentTurn",
    "message": "Run memory consolidation: python3 scripts/mem.py consolidate --days 7"
  },
  "sessionTarget": "isolated"
}
```

**整合流程的作用：**
1. **衰减处理**：未访问的记忆内容会逐渐失去效力（半衰期为30天）。
2. **数据聚类**：将相似的记忆内容归类在一起。
3. **数据合并**：合并重复项以节省存储空间和令牌消耗。
4. **重建层次结构**：更新RAPTOR层次结构，从而提升检索的准确性。

---

## 文件结构

```
workspace/
├── MEMORY.md              # Long-term curated memory (v2, still works)
├── SOUL.md                # Identity & personality
├── USER.md                # Human profile
├── db/
│   ├── agent.db           # Contacts/history (v2)
│   └── memory.db          # Cognitive memory (v3)
├── bank/
│   ├── entities/          # People profiles
│   ├── contacts.md        # Quick contact reference
│   └── opinions.md        # Preferences, beliefs
└── memory/
    ├── YYYY-MM-DD.md      # Daily logs
    ├── projects/           # Project notes
    └── knowledge/          # Topic docs
```

---

## 与其他方案的比较

| 特性 | 默认读取方式 | 基础的RAG系统 | Agent Memory Ultimate v3 |
|---------|---------------------|-----------|--------------------------|
| 每次检索的令牌消耗 | 3K-20K | 500-2K | 200-800 |
| 精确度 | 约5-10% | 约50% | 约80-90% |
| 关联功能 | 无 | 无 | ✅ 支持知识图谱 |
| 抽象层次 | 无 | 无 | ✅ 支持RAPTOR层次结构 |
| 上下文预处理 | 无 | 无 | ✅ 支持基于上下文的激活信息传播 |
| 依赖云服务 | 无 | 通常需要云服务 | **完全本地化** |
| 设置复杂度 | 无需复杂设置 | 需要执行`mem.py init`命令及一个脚本 |

---

## 数据来源（v2版本的导入方式）

| 数据来源 | 对应命令 |
|--------|---------|
| WhatsApp联系人/群组 | `python3 scripts/sync_whatsapp.py` |
| ChatGPT对话记录 | `python3 scripts/init_db.py`（自动识别`chatgpt-export/`文件） |
| 手机联系人（VCF格式） | `python3 scripts/import_vcf.py contacts.vcf` |
| 现有的Markdown文件 | `python3 scripts/mem.py migrate` |

---

## 依赖项

```bash
pip3 install scipy tokenizers onnxruntime numpy sqlite-vec
```

**无需使用Pinecone、Weaviate或Docker，也无需API密钥。嵌入模型仅需要下载一次，大小约为80MB。**

---

## 认知科学依据

这种架构并非随意设计——它是基于人类记忆的实际工作原理构建的：

| 人类记忆过程 | 代理系统的对应机制 |
|---------------|-----------------|
| 工作记忆 | **基于对话的预处理检索** |
| 长期记忆 | `store` + 向量嵌入技术 |
| 情景记忆 | 日志记录 + 情景记忆的存储 |
| 语义记忆 | `MEMORY.md`文件 + 语义记忆的存储 |
| 睡眠期间的整合 | **衰减处理 + 数据聚类** |
| 遗忘机制 | 记忆内容的自动衰减 |
| 关联关系 | 通过知识图谱建立关联 |
| 抽象层次 | RAPTOR层次结构（从具体到抽象的抽象过程） |
| 激活信息传播 | 基于上下文激活相关记忆 |

---

## 使用建议

1. **设置重要性评分**：核心身份相关的内容评分应高于0.9，常规事实相关的内容评分应高于0.5。评分越高，记忆内容在衰减后保留的时间越长。
2. **积极建立关联**：尽可能多地建立记忆之间的关联，以优化图谱的遍历效率。
3. **让系统自动处理衰减**：遗忘是一种自然现象，允许记忆内容逐渐消失有助于保持检索的准确性。
4. **在对话中使用预处理检索**：将对话中的最后2-3条消息作为上下文信息，可以获得更好的检索结果。
5. **每周重建层次结构**：在存储了大量新记忆后，执行`build-hierarchy`命令以优化检索效果。
6. **先使用混合策略**：只有在混合策略效果不佳时，再切换到纯向量搜索或关键词搜索方式。

---

## 创作者致谢

本工具由**Oscar Serra**在**Claude**（Anthropic团队）的帮助下开发完成。

*因为每次启动时都不应浪费大量令牌来记住自己的身份信息。*