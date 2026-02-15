---
name: nima-core
description: 神经集成内存架构（Neural Integrated Memory Architecture）：一种基于图的数据存储系统，结合了 LadybugDB 数据库、语义搜索功能以及动态情感分析（dynamic affect）和惰性数据检索（lazy recall）技术。该架构已准备好用于人工智能代理（AI agents）的实际应用。
version: 2.0.3
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "requires":
          {
            "bins": ["python3", "node"],
            "env": ["NIMA_EMBEDDER", "VOYAGE_API_KEY", "NIMA_DATA_DIR"],
          },
      },
  }
---
# NIMA Core 2.0

**Neural Integrated Memory Architecture** — 专为具备情感智能的AI代理设计的完整内存系统。

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
- **支持HNSW算法的向量搜索**（查询速度为18ms）  
- **数据库大小减少44%**（从91MB降至50MB）  
- **支持使用Cypher进行图谱遍历**  

### 安全性增强  
- **查询内容经过安全处理**（防止SQL注入等攻击）  
- **保护路径遍历安全**  
- **自动清理临时文件**  
- **全面优化错误处理机制**  

### 线程安全  
- **采用双重检查锁定机制实现线程安全**  
- **API超时设置**（Voyage为30秒，LadybugDB为10秒）  
- **支持连接池技术**  

### 测试与验证  
- **包含348项测试用例**  
- **确保线程安全性**  
- **覆盖所有边缘情况**  

## 架构概述  

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
| 向量搜索 | 需依赖外部库 | **18ms**（内置支持） |
| 数据库大小 | 91MB | **50MB**（减少44%） |
| 上下文信息存储量 | 约180条 | **约30条**（减少6倍） |

## API接口  

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
| `VOYAGE_API_KEY` | — | 使用Voyage API时必需 |
| `NIMA_LADYBUG` | `0` | 设置为`1`时使用LadybugDB后端 |

## 插件功能  

### nima-memory（数据捕获）  
- 在每个代理动作中捕获输入、处理过程及输出结果  
- 将数据存储至SQLite或LadybugDB  
- 计算并存储数据嵌入信息  

### nima-recall-live（信息检索）  
- 在代理启动前预加载相关记忆数据  
- 仅返回前N条结果  
- 通过上下文信息进行数据去重  

### nima-affect（情感处理）  
- 实时检测文本中的情感信息  
- 维护Panksepp提出的7种情感状态  
- 调节代理的响应方式  

## 安装说明  

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
| [README.md] | 系统使用指南 |
| [SETUP_GUIDE.md] | 安装步骤说明 |
| [docs/DATABASE_OPTIONS.md] | SQLite与LadybugDB的比较 |
| [docs/EMBEDDING_PROVIDERS.md] | 数据嵌入方式（Voyage、OpenAI、本地存储） |
| [MIGRATION_GUIDE.md] | 旧版本升级指南 |

## 安全性与隐私政策  

### 数据访问权限  
该插件会访问以下文件：  
- `~/.openclaw/agents/.../*.jsonl` — 会话记录文件（用于数据捕获）  
- `~/.nima/` — 本地内存数据库（SQLite或LadybugDB）  
- `~/.openclawextensions/` — 插件安装目录  

### 网络调用  
数据嵌入信息会发送至外部API：  
- **Voyage AI**（`api.voyageai.com`）—— 默认的嵌入服务提供商  
- **OpenAI**（`api.openai.com`）—— 可选嵌入服务提供商  
- **本地存储**—— 使用内置句子转换器时无需外部调用  

### 必需的环境变量  

| 变量 | 用途 | 是否必需 |
|----------|---------|----------|
| `NIMA_EMBEDDER` | 数据嵌入方式（`voyage`、`openai`或`local`） | 可选（默认：`voyage`） |
| `VOYAGE_API_KEY` | 使用Voyage API时需设置 |  
| `OPENAI_API_KEY` | 使用OpenAI API时需设置 |  
| `NIMA_DATA_DIR` | 内存存储路径 | 可选（默认：`~/.nima`） |
| `NIMA_LADYBUG` | 是否使用LadybugDB后端 | 可选（默认：`0`） |

### 安装脚本  
`install.sh`脚本会：  
1. 检查系统是否安装了Python 3和Node.js  
2. 创建`~/.nima/`目录  
3. 通过pip安装所需Python包  
4. 将插件文件复制至`~/.openclaw/extensions/`目录  

**无需额外下载任何外部组件。** 所有依赖包均来自PyPI。  

---

## 更新日志  

### v2.0.1  
- **线程安全改进**：采用双重检查锁定机制确保线程安全  
- **安全性增强**：明确API密钥的使用要求  
- **文档更新**：补充了关于API密钥安全性的说明  

### v2.0.0  
- **新增功能**：  
  - 引入LadybugDB后端及HNSW向量搜索功能  
  - 支持使用Cypher进行图谱遍历  
  - 提供`nima-query`命令行工具以统一管理查询操作  
- **安全性优化**：  
    - 防止SQL注入和FTS5攻击  
    - 加强路径遍历安全  
    - 自动清理临时文件  
- **其他改进**：  
    - 修复了线程安全相关的初始化问题  
    - 调整了API超时时间  
    - 测试通过348项测试用例  
    - 文本搜索速度提升3.4倍，数据库大小减少44%  

### v1.2.1  
- **新增意识系统相关功能**：  
  - 添加了8种意识状态模型（Φ、全局工作空间、自我意识等）  
  - 引入稀疏块存储技术（Sparse Block VSA）  
  - 统一了意识系统的接口设计  

### v1.1.9  
- **性能优化**：  
  - 修复了`nima-recall`插件在每次启动时创建新Python进程的问题  
  - 提高了信息检索效率（速度提升约50-250倍）  

### v1.2.0  
- **情感处理功能升级**：  
  - 新增了4层情感处理引擎  
  - 支持异步情感处理  
  - 增加了对Voyage AI嵌入服务的支持