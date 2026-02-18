---
name: nima-core
description: 神经集成内存架构（Neural Integrated Memory Architecture）：一种基于图谱的数据存储系统，采用了LadybugDB作为数据存储引擎，支持语义搜索功能，并具备动态数据管理及懒惰式数据检索（lazy recall）机制。该架构已完全准备好用于人工智能代理（AI agents）的应用。欲了解更多信息，请访问 nima-core.ai。
version: 2.0.12
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["python3","node"],"env":["NIMA_DATA_DIR"]},"optional_env":{"NIMA_EMBEDDER":"voyage|openai|local (default: local)","VOYAGE_API_KEY":"Required when NIMA_EMBEDDER=voyage","OPENAI_API_KEY":"Required when NIMA_EMBEDDER=openai"},"permissions":{"reads":["~/.openclaw/agents/*/sessions/*.jsonl"],"writes":["~/.nima/"],"network":["voyage.ai (conditional)","openai.com (conditional)"]}}}
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

## 🔒 隐私与权限设置  

**数据访问权限：**  
- ✅ 从 `~/.openclaw/agents/*/sessions/*.jsonl` 文件中读取会话记录。  
- ✅ 将数据写入 `~/.nima/` 目录（包括数据库、情感历史记录及嵌入信息）。  

**网络调用（取决于所使用的嵌入器）：**  
- 🌐 **Voyage API** — 仅当 `NIMA_EMBEDDER=voyage` 时使用（用于发送文本以生成嵌入信息）。  
- 🌐 **OpenAI API** — 仅当 `NIMA_EMBEDDER=openai` 时使用（用于发送文本以生成嵌入信息）。  
- 🔒 **本地嵌入** — 默认设置（`NIMA_EMBEDDER=local`），不进行外部API调用。  

**可选配置：**  
```json
// openclaw.json
{
  "plugins": {
    "entries": {
      "nima-memory": {
        "enabled": true,
        "skip_subagents": true,      // Exclude subagent sessions (default)
        "skip_heartbeats": true,      // Exclude heartbeat checks (default)
        "noise_filtering": {
          "filter_heartbeat_mechanics": true,
          "filter_system_noise": true
        }
      }
    }
  }
}
```  

**隐私默认设置：**  
- 不包含子代理的会话记录。  
- 过滤掉不必要的系统噪声。  
- 使用本地嵌入信息（不进行外部API调用）。  
- 所有数据均存储在本地。  

**如需禁用该插件，请在 `openclaw.json` 文件中的 `plugins.allow` 配置中移除 `nima-memory` 项。**  

## 2.0 版本的新功能  

### LadybugDB 后端  
- **文本搜索速度提升**：3.4倍（从31毫秒缩短至9毫秒）。  
- **支持HNSW算法的本地向量搜索**（搜索速度提升至18毫秒）。  
- **数据库大小缩减**：从91MB降至50MB（减少了44%）。  
- **支持使用Cypher查询进行图结构遍历》。  

### 安全性增强：**  
- 对查询内容进行安全处理（防止SQL注入攻击）。  
- 保护路径遍历行为。  
- 清理临时文件。  
- 全程优化错误处理机制。  

### 线程安全性：**  
- 采用双重检查锁定的单例模式确保线程安全。  
- API调用超时时间设置：Voyage API为30秒，LadybugDB为10秒。  
- 支持连接池技术。  

### 测试情况：**  
- 共完成348项单元测试。  
- 确保了线程安全性。  
- 覆盖了所有边缘使用场景。  

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

## 性能对比：**  
| 测试指标 | SQLite | LadybugDB |  
|--------|--------|-----------|  
| 文本搜索 | 31毫秒 | **9毫秒**（快3.4倍） |  
| 向量搜索 | 需依赖外部服务 | **18毫秒**（本地处理） |  
| 数据库大小 | 91MB | **50MB**（缩小44%） |  
| 上下文信息数量 | 约180条 | **约30条**（减少6倍） |  

## API接口：**  
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

## 配置参数：**  
| 参数 | 默认值 | 说明 |  
|----------|---------|-------------|  
| `NIMA_DATA_DIR` | `~/.nima` | 内存存储路径 |  
| `NIMA_EMBEDDER` | `voyage` | 可选值：`voyage`、`openai` 或 `local` |  
| `VOYAGE_API_KEY` | — | 使用Voyage API时必需的密钥 |  
| `NIMA_LADYBUG` | `0` | 使用LadybugDB后端时设置为1 |  

## 插件功能说明：  

### nima-memory（数据捕获模块）：**  
- 在每个代理动作中捕获输入、思考过程及输出结果。  
- 将数据存储至SQLite或LadybugDB数据库中。  
- 计算并存储相应的嵌入信息。  

### nima-recall-live（回忆模块）：**  
- 在代理启动前加载相关记忆信息。  
- 实现延迟加载机制，仅返回最相关的结果。  
- 通过注入上下文信息来消除数据重复。  

### nima-affect（情感处理模块）：**  
- 实时检测文本中的情感信息。  
- 维护Panksepp提出的七种情感状态。  
- 调节代理的响应方式。  

## 安装选项：**  
### SQLite（开发环境）：**  
```bash
pip install nima-core
./install.sh
```  

### LadybugDB（生产环境）：**  
```bash
pip install nima-core[vector]
./install.sh --with-ladybug
```  

## 文档资料：**  
- [README.md] — 全系统概述。  
- [SETUP_GUIDE.md] — 详细安装步骤。  
- [docs/DATABASE_OPTIONS.md] — SQLite与LadybugDB的比较。  
- [docs/EMBEDDING_PROVIDERS.md] — 支持的嵌入器类型（Voyage、OpenAI、本地）。  
- [MIGRATION_GUIDE.md] — 旧版本到新版本的迁移指南。  

## 安全性与隐私政策：**  
**数据访问权限：**  
该插件会访问以下路径：  
- `~/.openclaw/agents/.../*.jsonl` — 会话记录文件（用于数据捕获）。  
- `~/.nima/` — 本地内存数据库（存储方式：SQLite或LadybugDB）。  
- `~/.openclaw/extensions/` — 插件安装目录。  

**网络调用说明：**  
嵌入信息会发送至以下外部API：  
- **Voyage AI**（`api.voyageai.com`）—— 默认的嵌入服务提供商。  
- **OpenAI**（`api.openai.com`）—— 可选的嵌入服务提供商。  
- **本地处理**：使用内置的句子转换器时，不进行外部API调用。  

**必需的环境变量：**  
| 变量 | 用途 | 是否必需 |  
|----------|---------|----------|  
| `NIMA_EMBEDDER` | 选择嵌入服务（`voyage`、`openai` 或 `local`） | 否（默认为`voyage`） |  
| `VOYAGE_API_KEY` | 使用Voyage API时所需的认证密钥 | 是 |  
| `OPENAI_API_KEY` | 使用OpenAI API时所需的认证密钥 | 是 |  
| `NIMA_DATA_DIR` | 内存存储路径 | 否（默认为`~/.nima`） |  
| `NIMA_LADYBUG` | 是否使用LadybugDB后端 | 否（默认为0） |  

**安装说明：**  
`install.sh` 脚本会：  
1. 检查系统是否安装了Python 3和Node.js。  
2. 创建 `~/.nima/` 目录。  
3. 通过pip安装相关Python包。  
4. 将插件文件复制至 `~/.openclaw/extensions/` 目录。  

**注意：** 所有依赖包均来自PyPI。  

## 更新日志：**  
### v2.0.3（2026年2月15日）：**  
- **安全性增强：** 修复了 `affect_history.py` 中的路径遍历漏洞（严重级别）。  
- **安全性改进：** 修复了3个文件中的临时文件资源泄漏问题。  
- **代码优化：** 更正了错误处理逻辑（将通用异常处理替换为更具体的类型）。  
- **质量提升：** 提高了错误信息的可见性和调试效率。  

### v2.0.1：**  
- **线程安全性优化：** 采用双重检查锁定的单例模式确保线程安全。  
- **安全性增强：** 明确了元数据的使用要求（涉及Node.js和环境变量）。  
- **文档更新：** 添加了关于API密钥使用的安全说明。  

### v2.0.0：**  
- **新增功能：**  
  - 引入了支持HNSW算法的LadybugDB后端。  
  - 支持使用Cypher进行图结构遍历。  
  - 新增了 `nima-query` CLI工具，用于统一查询操作。  
- **安全性增强：** 防止SQL注入和FTS5攻击。  
  - 优化了路径遍历逻辑。  
  - 清理了临时文件。  
- **稳定性改进：** 修复了单例初始化过程中的问题。  
- **性能提升：** 文本搜索速度提升3.4倍，数据库大小缩减44%。  

### 其他版本更新：**  
- **v1.2.1：** 添加了8种意识系统模型（Φ、全局工作空间、自我意识相关功能）。  
- **新增：** 使用稀疏块存储技术优化内存管理。  
- **新增：** 统一的ConsciousnessCore接口。  

- **v1.1.9：** 优化了`nima-recall`模块的性能，减少了启动时的资源消耗。  
- **v1.2.0：** 引入了多层情感处理引擎，支持异步情感处理，并增强了与Voyage AI的集成。