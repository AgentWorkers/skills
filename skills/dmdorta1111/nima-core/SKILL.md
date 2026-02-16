---
name: nima-core
description: 神经集成内存架构（Neural Integrated Memory Architecture）：一种基于图的数据存储系统，结合了LadybugDB数据库、语义搜索功能以及动态情感分析（dynamic affect）和懒惰式数据检索（lazy recall）机制。该架构已具备量产能力，适用于人工智能代理（AI agents）的应用场景。
version: 2.0.5
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["python3","node"],"env":["NIMA_EMBEDDER","VOYAGE_API_KEY","NIMA_DATA_DIR"]}}}
---
# NIMA Core 2.0

**Neural Integrated Memory Architecture** — 专为具有情感智能的AI代理设计的完整内存系统。

**官方网站：** https://nima-core.ai  
**GitHub仓库：** https://github.com/lilubot/nima-core  

## 🚀 快速入门  

```bash
# Install
pip install nima-core

# Or with LadybugDB (recommended for production)
pip install nima-core[vector]

# Set embedding provider
export NIMA_EMBEDDER=voyage
export VOYAGE_API_KEY=your-key

# Install hooks
./install.sh --with-ladybug

# Restart OpenClaw
openclaw restart
```  

## 2.0的新功能  

### LadybugDB后端  
- **文本搜索速度提升3.4倍**（从31ms缩短至9ms）  
- **支持HNSW的向量搜索**（速度提升至18ms）  
- **数据库大小减少44%**（从91MB降至50MB）  
- **支持使用Cypher进行图谱遍历**  

### 安全性增强  
- **查询内容 sanitization（防止SQL注入等安全问题）**  
- **路径遍历保护**  
- **临时文件清理**  
- **全面的错误处理**  

### 线程安全  
- **采用双重检查锁定机制的单例模式**  
- **API超时设置**（Voyage：30秒；LadybugDB：10秒）  
- **支持连接池**  

### 348项测试  
- **全面的单元测试**  
- **线程安全性已验证**  
- **涵盖了各种边缘情况**  

## 架构  

```text
OPENCLAW HOOKS
├── nima-memory      — Three-layer capture (input/contemplation/output)
├── nima-recall-live — Lazy recall injection (before_agent_start)
└── nima-affect      — Real-time emotion detection

PYTHON CORE
├── nima_core/cognition/
│   ├── dynamic_affect.py     — Panksepp 7-affect system
│   ├── personality_profiles.py — JSON personality configs
│   ├── emotion_detection.py  — Lexicon-based emotion→affect mapping
│   └── archetypes.py         — Baseline affect profiles
└── scripts/
    ├── nima_ladybug_backend.py — LadybugDB CLI
    └── ladybug_parallel.py    — Parallel migration

DATABASE (SQLite or LadybugDB)
├── memory_nodes   — Messages with embeddings
├── memory_edges   — Graph relationships
└── memory_turns   — Conversation turns
```  

## 性能对比  

| 测量指标 | SQLite | LadybugDB |
|--------|--------|-----------|
| 文本搜索 | 31ms | **9ms**（快3.4倍） |
| 向量搜索 | 外部库 | **18ms**（原生支持） |
| 数据库大小 | 91MB | **50MB**（缩小44%） |
| 上下文令牌数量 | 约180个 | **约30个**（减少6倍） |

## API  

```python
from nima_core import DynamicAffectSystem, get_affect_system

# Get singleton instance (thread-safe)
affect = get_affect_system(identity_name="lilu")

# Process input and get affect state
state = affect.process_input("I'm so excited about this project!")
print(state.current)  # {"SEEKING": 0.72, "PLAY": 0.65, ...}

# Recall memories (via hooks - automatic)
# Or manually via CLI:
# nima-query who_search "David" --limit 5
# nima-query text_search "project" --limit 5
```  

## 配置参数  

| 参数 | 默认值 | 说明 |
|----------|---------|-------------|
| `NIMA_DATA_DIR` | `~/.nima` | 内存存储路径 |
| `NIMA_EMBEDDER` | `voyage` | 可选值：`voyage`、`openai`或`local` |
| `VOYAGE_API_KEY` | — | 使用Voyage API时必填 |
| `NIMA_LADYBUG` | `0` | 设置为`1`时使用LadybugDB后端 |

## 插件功能  

### nima-memory（捕获模块）  
- 在每个回合捕获输入、处理过程及输出结果  
- 将数据存储至SQLite或LadybugDB  
- 计算并存储嵌入向量  

### nima-recall-live（回忆模块）  
- 在代理启动前注入相关记忆  
- **延迟加载**（仅返回前N个结果）  
- **通过上下文信息消除重复数据**  

### nima-affect（情感模块）  
- 从文本中实时检测情感  
- 维护Panksepp提出的7种情感状态  
- 调节代理的响应方式  

## 安装选项  

### SQLite（开发环境）  
```bash
pip install nima-core
./install.sh
```  

### LadybugDB（生产环境）  
```bash
pip install nima-core[vector]
./install.sh --with-ladybug
```  

## 文档资料  

| 文档名称 | 说明 |
|-------|-------------|
| [README.md] | 系统概述 |
| [SETUP_GUIDE.md] | 安装指南 |
| [docs/DATABASE_OPTIONS.md] | SQLite与LadybugDB的比较 |
| [docs/EMBEDDING_PROVIDERS.md] | 推荐的嵌入服务提供商（Voyage、OpenAI、本地） |
| [MIGRATION_GUIDE.md] | 旧版本到新版本的迁移指南 |

## 安全性与隐私  

### 数据访问权限  
该插件会访问以下文件：  
- `~/.openclaw/agents/.../*.jsonl` — 会话记录（用于数据捕获）  
- `~/.nima/` — 本地内存数据库（SQLite或LadybugDB）  
- `~/.openclaw/extensions/` — 插件安装目录  

### 网络调用  
嵌入向量会发送至外部API：  
- **Voyage AI**（`api.voyageai.com`）—— 默认的嵌入服务提供商  
- **OpenAI**（`api.openai.com`）—— 可选嵌入服务提供商  
- **本地模式**—— 使用`sentence-transformers`时无需外部调用  

### 必需的环境变量  

| 变量 | 用途 | 是否必填 |
|----------|---------|----------|
| `NIMA_EMBEDDER` | 插件类型（`voyage`、`openai`或`local`） | 可选 |
| `VOYAGE_API_KEY` | 使用Voyage API时需要 |  
| `OPENAI_API_KEY` | 使用OpenAI API时需要 |  
| `NIMA_DATA_DIR` | 内存存储路径 | 可选（默认：`~/.nima`） |
| `NIMA_LADYBUG` | 是否使用LadybugDB后端 | 可选（默认：0） |

### 安装脚本  
`install.sh`脚本会：  
1. 检查Python 3和Node.js是否已安装  
2. 创建`~/.nima/`目录  
3. 通过pip安装Python包  
4. 将插件文件复制至`~/.openclaw/extensions/`  

**无需额外下载**。所有依赖包均来自PyPI。  

---

## 更新日志  

### v2.0.3（2026年2月15日）  
- **安全性增强**：  
  - 修复`affect_history.py`中的路径遍历漏洞（严重级别）  
  - 修复3个文件中的临时文件资源泄漏问题  
  - 修正了`json.JSONEncodeError`导致的错误类型（从`TypeError`更正为`ValueError`）  
  - 改进了异常处理机制（将通用异常处理替换为更具体的类型）  
  - 提高了错误信息的可见性和调试效率  

### v2.0.1（线程安全与元数据改进）  
- **线程安全**：采用双重检查锁定机制实现单例模式  
- **安全性**：明确了元数据的使用要求（涉及Node.js和环境变量）  
- **文档更新**：增加了关于API密钥使用的安全说明  

### v2.0.0（新增LadybugDB功能）  
- **新增**：支持HNSW算法的向量搜索  
- **新增**：支持使用Cypher进行图谱遍历  
- **新增**：提供`nima-query` CLI工具以统一查询操作  
- **安全性**：加强了SQL/FTS5注入防护  
- **安全性**：改进了路径遍历保护机制  
- **安全性**：优化了临时文件的清理流程  
- **稳定性**：修复了单例初始化的相关问题  
- **性能提升**：文本搜索速度提升3.4倍，数据库大小减少44%  

### v1.2.1（意识架构改进）  
- **新增**：8种意识状态（Φ、全局工作区、自我意识相关功能）  
- **新增**：稀疏块VSA内存模型  
- **新增**：统一的意识处理接口  

### v1.1.9（插件效率优化）  
- **修复**：`nima-recall`插件在每次启动时创建新Python进程的问题  
- **性能提升**：回忆功能的速度提高了约50至250倍  

### v1.2.0（情感响应引擎）  
- **新增**：4层情感处理引擎  
- **新增**：异步情感处理功能  
- **新增**：支持与Voyage AI的嵌入服务集成