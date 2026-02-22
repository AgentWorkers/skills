---
name: nima-core
description: 神经集成内存架构（Neural Integrated Memory Architecture）——专为人工智能代理设计的持久性内存系统，具备情感智能和语义回忆功能。该架构包含内存优化工具（Memory Pruner）、情感分析引擎（VADER Affect）、五种嵌入模型生成工具（5 Embedding Providers），并且支持零配置安装。欲了解更多信息，请访问 nima-core.ai。
version: 2.5.0
metadata: {"openclaw":{"emoji":"🧠","requires":{"bins":["python3","node"],"env":["NIMA_DATA_DIR"]},"optional_env":{"NIMA_EMBEDDER":"voyage|openai|local (default: local)","VOYAGE_API_KEY":"Required when NIMA_EMBEDDER=voyage","OPENAI_API_KEY":"Required when NIMA_EMBEDDER=openai"},"permissions":{"reads":["~/.openclaw/agents/*/sessions/*.jsonl"],"writes":["~/.nima/"],"network":["voyage.ai (conditional)","openai.com (conditional)"]}}}
---
# NIMA Core 2.3

**Neural Integrated Memory Architecture** — 一种专为具有情感智能的AI代理设计的完整内存系统。

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

## 🔒 隐私与权限  

**数据访问：**  
- ✅ 从 `~/.openclaw/agents/*/sessions/*.jsonl` 读取会话记录  
- ✅ 将数据写入本地存储（`~/.nima/`，包括数据库、情感历史记录和嵌入数据）  

**网络调用（取决于所使用的嵌入器）：**  
- 🌐 **Voyage API** — 仅在 `NIMA_EMBEDDER=voyage` 时使用（用于发送文本以获取嵌入数据）  
- 🌐 **OpenAI API** — 仅在 `NIMA_EMBEDDER=openai` 时使用（用于发送文本以获取嵌入数据）  
- 🔒 **本地嵌入** — 默认设置（`NIMA_EMBEDDER=local`），不进行外部API调用  

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
- 排除子代理的会话记录  
- 过滤系统产生的噪音  
- 使用本地嵌入数据（不进行外部API调用）  
- 所有数据均存储在本地  

**如需禁用该插件，请从 `openclaw.json` 文件中的 `plugins.allow` 列表中移除 `nima-memory`。**  

## 2.1 版本的新功能  

### VADER 情感分析器  
- **上下文分析**：加强了大写字符的处理（效果提升1.5倍），突出标点符号，支持否定词和程度修饰词  
- **识别30多种习语**：能够理解“not bad”、“kind of”、“sort of”等短语  
- **Panksepp 7情感模型**：将VADER情感分析结果直接映射到“SEEKING”、“RAGE”、“FEAR”、“LUST”、“CARE”、“PANIC”、“PLAY”等情感状态  
- **情感调节机制**：根据用户情绪调整代理的行为（例如将用户的愤怒转化为代理的关心或关怀）  
- 替代了之前的基于词典的情感分析方法  

### 噪音处理（四阶段流程）  
1. **空值验证**：过滤掉空或无效的输入数据  
2. **心跳信号过滤**：排除系统产生的噪音（如心跳信号相关消息）  
3. **去重**：去除会话中的重复内容  
4. **性能监控**：跟踪数据捕获的质量和过滤效果  

### 性能提升：  
- **修复了LadybugDB后端的导入问题**  
- **增加令牌预算**：回忆功能的令牌预算从500个增加到3000个  
- **改进了连接管理**：优化了与LadybugDB后端的连接机制  

## 2.0 版本的新功能  

### LadybugDB后端  
- **文本搜索速度提升3.4倍**（从31ms缩短至9ms）  
- **支持HNSW算法的向量搜索**（搜索速度提升至18ms）  
- **数据库体积缩小44%**（从91MB降至50MB）  
- **支持使用Cypher进行图谱查询**  

### 安全性增强：  
- **查询数据清洗**：防止SQL注入等安全漏洞  
- **路径遍历保护**  
- **临时文件清理**  
- **全面的错误处理**  

### 线程安全性：  
- 采用双重检查锁定机制确保线程安全  
- **API超时设置**：Voyage API超时时间为30秒，LadybugDB API超时时间为10秒  
- **支持连接池**  

### 全面测试：  
- 完成了348项单元测试  
- 确保了线程安全性  
- 覆盖了所有可能的边缘情况  

## 架构概述  

```text
OPENCLAW HOOKS
├── nima-memory      — Three-layer capture with 4-phase noise remediation
├── nima-recall-live — Lazy recall injection (before_agent_start)
└── nima-affect      — VADER-based real-time affect analysis

PYTHON CORE
├── nima_core/cognition/
│   ├── dynamic_affect.py       — Panksepp 7-affect system
│   ├── personality_profiles.py — JSON personality configs
│   ├── vader_affect.py         — VADER sentiment analyzer (NEW v2.1)
│   └── archetypes.py           — Baseline affect profiles
└── scripts/
    ├── nima_ladybug_backend.py — LadybugDB CLI
    └── ladybug_parallel.py     — Parallel migration

DATABASE (SQLite or LadybugDB)
├── memory_nodes   — Messages with embeddings
├── memory_edges   — Graph relationships
└── memory_turns   — Conversation turns
```  

## 性能对比  

| 测试指标 | SQLite | LadybugDB |
|--------|--------|-----------|
| 文本搜索 | 31ms | **9ms**（快3.4倍） |
| 向量搜索 | 外部服务 | **18ms**（本地服务） |
| 上下文相关词汇数量 | 约180个 | **约30个**（数量减少6倍） |
| 回忆功能令牌预算 | 500个 | **3000个**（2.1版本后提升） |

## API接口  

```python
from nima_core import DynamicAffectSystem, get_affect_system
from nima_core.cognition.vader_affect import VaderAffectAnalyzer

# Get singleton instance (thread-safe)
affect = get_affect_system(identity_name="lilu")

# Process input and get affect state
state = affect.process_input("I'm so excited about this project!")
print(state.current)  # {"SEEKING": 0.72, "PLAY": 0.65, ...}

# Use VADER analyzer directly
analyzer = VaderAffectAnalyzer()
result = analyzer.analyze("This is AMAZING!!!")
print(result.affects)  # {'PLAY': 0.78, 'SEEKING': 0.71, ...}

# Recall memories (via hooks - automatic)
# Or manually via CLI:
# nima-query who_search "David" --limit 5
# nima-query text_search "project" --limit 5
```  

## 配置参数  

| 参数 | 默认值 | 说明 |
|----------|---------|-------------|
| `NIMA_DATA_DIR` | `~/.nima` | 内存存储路径 |
| `NIMA_EMBEDDER` | `voyage` | 可选值：`voyage`、`openai` 或 `local` |
| `VOYAGE_API_KEY` | — | 使用Voyage API时必填 |
| `NIMA_LADYBUG` | `0` | 使用LadybugDB后端时设置为1 |

## 插件功能说明  

### nima-memory（数据捕获）  
- 在每个代理操作环节捕获输入数据、处理过程及输出结果  
- 采用四阶段噪声处理机制（空值验证、心跳信号过滤、去重、性能监控）  
- 将数据存储至SQLite或LadybugDB  
- 计算并存储情感嵌入信息  

### nima-recall-live（回忆功能）  
- 在代理启动前注入相关记忆信息  
- 实现延迟加载机制（仅返回前N个结果）  
- 对输入数据进行去重处理  
- 令牌预算：3000个（相比2.1版本增加了2500个）  

### nima-affect（情感分析）  
- 基于VADER算法进行实时情感分析  
- 支持上下文相关分析（如大写字符、标点符号、否定词、程度修饰词）  
- 识别30多种习语  
- 维护Panksepp 7情感模型  
- 根据用户情绪调节代理行为  

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
| [README.md] | 全系统概述 |
| [SETUP_GUIDE.md] | 分步安装指南 |
| [docs/DATABASE_OPTIONS.md] | SQLite与LadybugDB的比较 |
| [docs/EMBEDDING_PROVIDERS.md] | 嵌入器选择指南（Voyage、OpenAI、本地） |
| [MIGRATION_GUIDE.md] | 旧版本迁移指南 |
| [CHANGELOG.md] | 版本更新记录 |

## 安全性与隐私政策  

### 数据访问权限：  
该插件会访问以下文件：  
- `~/.openclaw/agents/.../*.jsonl`：会话记录文件  
- `~/.nima/`：本地内存数据库（SQLite或LadybugDB）  
- `~/.openclaw/extensions/`：插件安装目录  

### 网络调用：**  
嵌入数据会发送至外部API：  
- **Voyage AI**（`api.voyageai.com`）：默认的嵌入服务提供商  
- **OpenAI**（`api.openai.com`）：可选的嵌入服务提供商  
- **本地模式**：使用内部转换器时不会进行外部API调用  

### 必需的环境变量：  
| 变量 | 用途 | 是否必填 |
|----------|---------|----------|
| `NIMA_EMBEDDER` | 选择嵌入服务提供商 | 可选（默认为`voyage`） |
| `VOYAGE_API_KEY` | 使用Voyage API时需设置 |  
| `OPENAI_API_KEY` | 使用OpenAI API时需设置 |  
| `NIMA_DATA_DIR` | 内存存储路径 | 可选（默认为`~/.nima`） |
| `NIMA_LADYBUG` | 是否使用LadybugDB后端 | 可选（默认为0） |

### 安装脚本：  
`install.sh`脚本会：  
1. 检查系统是否安装了Python 3和Node.js  
2. 创建`~/.nima/`目录  
3. 通过pip安装相关Python包  
4. 将插件文件复制至`~/.openclaw/extensions/`目录  

**所有依赖包均来自PyPI。**  

---

## 版本更新记录  

### v2.1.0（2026年2月17日）  
- **新增功能：** 基于VADER的情感分析器，替代了传统的基于词典的分析方法  
  - 强化上下文分析功能  
  - 支持更多习语识别  
  - 采用Panksepp 7情感模型  
  - 引入情感调节机制  
- **改进：** 噪音处理流程  
- **修复：** LadybugDB后端的导入问题  
- **调整：** 提高回忆功能的令牌预算  
- **优化：** 改进了与LadybugDB后端的连接管理  

### v2.0.3（2026年2月15日）  
- **安全性增强：** 修复了多个安全漏洞  
- **改进：** 提高了错误处理的透明度和效率  

### v2.0.1（2026年2月15日）  
- **线程安全性改进：** 采用双重检查锁定机制确保线程安全  
- **文档更新：** 明确了API密钥的使用要求  

### v2.0.0（2026年2月15日）  
- **新增功能：** 引入了LadybugDB后端及HNSW向量搜索技术  
- **优化：** 改进了数据库性能和安全性  

### 其他版本更新：  
- **v1.2.1**：新增了8种意识模型和稀疏块存储技术  
- **v1.1.9**：优化了插件性能  
- **v1.2.0**：增强了情感处理能力和API接口