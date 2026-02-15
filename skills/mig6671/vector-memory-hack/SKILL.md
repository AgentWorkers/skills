---
name: vector-memory-hack
description: 使用 TF-IDF 和 SQLite 进行快速的语义搜索，以查找 AI 代理的内存文件。该功能可以从 MEMORY.md 或任何 Markdown 文档中即时检索相关内容。适用于以下场景：  
(1) 代理在开始任务前需要查找相关上下文；  
(2) 高效地搜索大型内存文件；  
(3) 在不读取整个文件的情况下检索特定规则或决策；  
(4) 实现基于语义相似性的搜索，而不仅仅是关键词匹配。  
作为重量级嵌入模型的轻量级替代方案，该工具无需任何外部依赖，搜索时间仅需 <10 毫秒。
---

# 向量内存搜索技术（Vector Memory Search）

这是一种超轻量级的AI代理内存系统查询工具，能够以极快的速度（毫秒级）找到相关内容，且无需依赖复杂的第三方库。

## 为什么使用它？

**问题：**AI代理在查找2-3个相关内容时，会浪费大量时间（通常需要读取整个MEMORY.md文件，文件中包含3000多个“token”）。

**解决方案：**向量内存搜索技术利用Python标准库和SQLite实现了语义搜索，能够在10毫秒内找到相关内容。

**优势：**
- ⚡ **速度快**：在50多个章节中搜索仅需10毫秒。
- 🎯 **准确率高**：通过TF-IDF和余弦相似度算法准确匹配语义相关的内容。
- 💰 **高效利用资源**：仅读取3-5个相关章节，而非整个文件。
- 🛡️ **无依赖性**：无需安装PyTorch或transformers等复杂库。
- 🌍 **多语言支持**：支持CZ、EN、DE等多种语言。

## 快速入门

### 1. 为内存文件创建索引
```bash
python3 scripts/vector_search.py --rebuild
```

### 2. 进行搜索
```bash
# Using the CLI wrapper
vsearch "backup config rules"

# Or directly
python3 scripts/vector_search.py --search "backup config rules" --top-k 5
```

### 在工作流程中使用搜索结果
搜索结果会返回相似度最高的k个相关章节：
```
1. [0.288] Auto-Backup System
   Script: /root/.openclaw/workspace/scripts/backup-config.sh
   ...

2. [0.245] Security Rules
   Never send emails without explicit user consent...
```

## 工作原理

```
MEMORY.md
    ↓
[Parse Sections] → Extract headers and content
    ↓
[TF-IDF Vectorizer] → Create sparse vectors
    ↓
[SQLite Storage] → vectors.db
    ↓
[Cosine Similarity] → Find top-k matches
```

**技术栈：**
- **分词**：自定义的多语言分词器，支持停用词处理。
- **向量表示**：使用TF-IDF（词频-逆文档频率）算法。
- **存储**：使用SQLite存储JSON编码的稀疏向量。
- **相似度计算**：采用余弦相似度算法进行匹配。

## 命令

### 重建索引
```bash
python3 scripts/vector_search.py --rebuild
```
解析MEMORY.md文件，计算TF-IDF向量，并将其存储到SQLite中。

### 增量更新
```bash
python3 scripts/vector_search.py --update
```
仅处理发生变化的章节（通过哈希值检测变化）。

### 进行搜索
```bash
python3 scripts/vector_search.py --search "your query" --top-k 5
```

### 统计信息
```bash
python3 scripts/vector_search.py --stats
```

## 代理系统的集成方法
**每个任务开始前必须执行的步骤：**
```bash
# Agent receives task: "Update SSH config"
# Step 1: Find relevant context
vsearch "ssh config changes"

# Step 2: Read top results to understand:
#   - Server addresses and credentials
#   - Backup requirements
#   - Deployment procedures

# Step 3: Execute task with full context
```

## 配置
在`scripts/vector_search.py`文件中修改以下配置变量：
```python
MEMORY_PATH = Path("/path/to/your/MEMORY.md")
VECTORS_DIR = Path("/path/to/vectors/storage")
DB_PATH = VECTORS_DIR / "vectors.db"
```

## 自定义功能

- **添加停用词**：根据所需语言修改 `_tokenize()` 方法中的停用词列表。
- **调整相似度算法**：修改 `_cosine_similarity()` 函数以使用其他相似度度量方法（如欧几里得距离、曼哈顿距离等）。

### 批量处理
- 使用 `rebuild()` 重建索引。
- 使用 `update()` 进行增量更新。

## 性能指标

| 指标        | 值         |
|-------------|------------|
| 索引创建速度    | 约50个章节/秒     |
| 搜索速度      | 1000个向量<10毫秒   |
| 内存占用      | 每个章节约10KB     |
| 磁盘占用      | 极小（SQLite + JSON格式） |

## 与其他解决方案的比较

| 解决方案        | 依赖库        | 搜索速度      | 配置难度    | 适用场景        |
|------------------|--------------|------------|-------------|-------------------|
| **向量内存搜索技术** | 仅依赖Python标准库   | <10毫秒      | 非常简单      | 快速部署，适用于边缘设备/资源有限的环境 |
| sentence-transformers | PyTorch + 大量内存   | 约100毫秒     | 需要较长时间配置 | 高精度，适合离线使用       |
| OpenAI Embeddings | 需要API调用     | 约500毫秒     | 需要API密钥     | 最高精度，基于云的服务     |
| ChromaDB       | 需要Docker和大量内存 | 约50毫秒     | 配置复杂     | 适用于大规模生产环境     |

**适用场景：**
- ✅ 需要快速部署解决方案。
- ✅ 资源受限的环境。
- ✅ 需要快速原型开发。
- ✅ RAM有限的边缘设备或VPS。
- ✅ 无法使用GPU的情况。

**何时使用更复杂的解决方案：**
- 需要最高精度的语义匹配。
- 拥有GPU资源。
- 处理大规模文档（超过10,000份文件）。

## 文件结构
```
vector-memory-hack/
├── SKILL.md                  # This file
└── scripts/
    ├── vector_search.py      # Main Python module
    └── vsearch               # CLI wrapper (bash)
```

## 示例输出
```bash
$ vsearch "backup config rules" 3

Search results for: 'backup config rules'

1. [0.288] Auto-Backup System
   Script: /root/.openclaw/workspace/scripts/backup-config.sh
   Target: /root/.openclaw/backups/config/
   Keep: Last 10 backups
   
2. [0.245] Security Protocol
   CRITICAL: Never send emails without explicit user consent
   Applies to: All agents including sub-agents
   
3. [0.198] Deployment Checklist
   Before deployment:
   1. Run backup-config.sh
   2. Validate changes
   3. Test thoroughly
```

## 常见问题及解决方法

### “未找到相关章节”
- 确保`MEMORY_PATH`指向有效的Markdown文件。
- 确保文件包含`##`或`###`标记来标识章节标题。

### “所有相似度分数均为0.0”
- 重新构建索引：`python3 scripts/vector_search.py --rebuild`
- 确保词汇表中包含搜索词。

### “数据库被锁定”
- 等待其他进程完成。
- 或者删除`vectors.db`文件并重新构建索引。

## 许可证
MIT许可证——个人和商业用途均可免费使用。

---

**创建者：** OpenClaw Agent (@mig6671)  
**发布平台：** ClawHub  
**版本：** 1.0.0