---
name: agent-memory
description: Full AI agent memory stack — Mem0 unified memory engine with vector search (Qdrant) and knowledge graph (Neo4j), plus SQLite for structured data. Complete setup script and tools. Give your OpenClaw agent a real brain with semantic recall, entity relationships, and structured storage.
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+, Docker (Qdrant + Neo4j), OpenRouter API key
metadata: {"openclaw": {"emoji": "\ud83e\udde0", "requires": {"env": ["OPENROUTER_API_KEY"]}, "primaryEnv": "OPENROUTER_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---

# 代理内存 🧠

完整的智能层包括：向量内存、知识图谱和结构化数据库。

## 使用场景

- 语义化地存储和检索信息（例如：“记住Abidi更喜欢...”）
- 管理结构化数据：项目、联系人、任务、书签
- 在容器重建后配置代理的内存结构
- 批量向内存中添加关键信息

## 使用方法

### 内存引擎（Mem0 — 向量 + 图谱）
```bash
# Store a fact
python3 {baseDir}/scripts/memory_engine.py add "Abidi's business focuses on Voice AI"

# Semantic recall
python3 {baseDir}/scripts/memory_engine.py search "what does Abidi's business do"

# List all memories
python3 {baseDir}/scripts/memory_engine.py get-all

# Test connections (Qdrant, Neo4j, Langfuse)
python3 {baseDir}/scripts/memory_engine.py test
```

### 结构化数据库（SQLite）
```bash
# List tables
python3 {baseDir}/scripts/structured_db.py tables

# Insert data
python3 {baseDir}/scripts/structured_db.py insert projects '{"name":"MyProject","status":"active"}'

# Query
python3 {baseDir}/scripts/structured_db.py query "SELECT * FROM projects"
```

### 设置与数据初始化
```bash
# Install Python deps after container rebuild
bash {baseDir}/scripts/setup_brain.sh

# Batch seed with key facts
python3 {baseDir}/scripts/seed_mem0.py
```

## 架构

- **Mem0**：统一的人工智能内存系统（自动提取信息、去重、多级检索功能）
- **Qdrant**：用于语义搜索的向量数据库
- **Neo4j**：用于存储实体及其关系的知识图谱
- **SQLite**：用于存储项目、联系人、任务、书签等结构化数据
- **Langfuse**：用于追踪所有操作的执行过程

## 致谢

由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) | [agxntsix.ai](https://www.agxntsix.ai) 开发  
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)  
该功能是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的企业配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)