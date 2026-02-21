---
name: nima-core
description: 神经集成内存架构（Neural Integrated Memory Architecture）——专为人工智能代理设计的持久性内存系统，具备情感智能和语义检索功能。该架构包含内存优化工具（Memory Pruner）、VADER情感分析引擎、以及五种嵌入模型提供者（Embedding Providers），支持零配置安装（zero-config installation）。欲了解更多信息，请访问 nima-core.ai。
version: 2.4.0
metadata: {"openclaw":{"emoji":"🧠","requires":{"bins":["python3","node"],"env":["NIMA_DATA_DIR"]},"optional_env":{"NIMA_EMBEDDER":"voyage|openai|local (default: local)","VOYAGE_API_KEY":"Required when NIMA_EMBEDDER=voyage","OPENAI_API_KEY":"Required when NIMA_EMBEDDER=openai"},"permissions":{"reads":["~/.openclaw/agents/*/sessions/*.jsonl"],"writes":["~/.nima/"],"network":["voyage.ai (conditional)","openai.com (conditional)"]}}}
---
# NIMA Core 2.3

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
- ✅ 从 `~/.openclaw/agents/*/sessions/*.jsonl` 文件中读取会话记录  
- ✅ 将数据写入本地存储目录 `~/.nima/`（包括数据库、情感历史记录和嵌入信息）  

**网络调用（取决于所使用的嵌入器）：**  
- 🌐 **Voyage API** — 仅当 `NIMA_EMBEDDER=voyage` 时使用（用于发送文本以获取嵌入信息）  
- 🌐 **OpenAI API** — 仅当 `NIMA_EMBEDDER=openai` 时使用（用于发送文本以获取嵌入信息）  
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
- 不包含子代理的会话记录  
- 过滤系统产生的噪音  
- 使用本地嵌入信息（不进行外部API调用）  
- 所有数据均存储在本地  

**如需禁用该插件，请在 `openclaw.json` 文件中的 `plugins.allow` 配置中移除 `nima-memory` 项。**  

## 2.1 版本的新功能  

### VADER情感分析器  
- **上下文分析**：加强了大写字符的处理（效果提升1.5倍），突出标点符号，支持否定词及程度修饰词  
- **识别30多种习语**：能够理解“not bad”（还不错）、“kind of”（有点）等短语  
- **Panksepp 7情感模型**：实现VADER情感与SEEKING（寻求）、RAGE（愤怒）、FEAR（恐惧）、LUST（欲望）、CARE（关心）、PANIC（恐慌）、PLAY（娱乐）等情感状态的直接映射  
- **用户情绪到代理行为的转化**：根据用户情绪调整代理的行为反应  

**噪音处理机制（共4个阶段）：**  
1. **空值验证**：过滤掉空或无效的输入信息  
2. **心跳检测**：排除系统产生的噪音（如心跳检测消息）  
3. **去重**：去除会话中的重复内容  
4. **性能监控**：记录处理效果并收集相关指标  

**性能优化：**  
- **修复了LadybugDB后端的导入问题**  
- **增加令牌预算**：检索令牌数量从500个增加到3000个  
- **改进了与LadybugDB后端的连接管理**  

## 2.0版本的新功能  

### LadybugDB后端  
- **文本搜索速度提升3.4倍**（从31ms缩短至9ms）  
- **支持HNSW算法的向量搜索**（搜索速度提升至18ms）  
- **数据库体积缩小44%**（从91MB降至50MB）  
- **支持使用Cypher进行图谱查询**  

**安全性增强：**  
- 对查询内容进行安全处理（防止SQL注入攻击）  
- 保护路径遍历过程  
- 清理临时文件  
- 全程加强错误处理  

**线程安全性：**  
- 采用双重检查锁定机制确保线程安全  
- API调用超时设置：Voyage API为30秒，LadybugDB为10秒  
- 支持连接池技术  

**全面测试：**  
- 完整通过了348项单元测试  
- 确保了线程安全性  
- 覆盖了所有边缘使用场景  

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
| 向量搜索 | 需依赖外部库 | **18ms**（本地实现） |
| 上下文相关词汇数量 | 约180个 | **约30个**（数据量减少6倍） |
| 召回令牌预算 | 500个 | **3000个**（2.1版本后提升） |

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

### nima-memory（数据捕获模块）  
- 在每个代理回合捕获输入、处理过程及输出结果  
- 采用四阶段噪音处理机制（空值验证、心跳检测、去重、性能监控）  
- 将数据存储至SQLite或LadybugDB  
- 计算并存储文本嵌入信息  

### nima-recall-live（回忆模块）  
- 在代理启动前注入相关记忆内容  
- 实现延迟加载机制（仅返回前N条结果）  
- 根据上下文对结果进行去重处理  
- 令牌预算：3000个（相比2.1版本增加）  

### nima-affect（情感分析模块）  
- 基于VADER算法进行实时情感分析  
- 支持上下文相关处理（如大写字符、标点符号、否定词等）  
- 识别30多种习语  
- 维护Panksepp 7情感模型状态  
- 根据用户情绪调整代理行为  

## 安装说明  

### SQLite版本（开发环境）  
```bash
pip install nima-core
./install.sh
```  

### LadybugDB版本（生产环境）  
```bash
pip install nima-core[vector]
./install.sh --with-ladybug
```  

## 文档资料  

| 文档名称 | 说明 |
|-------|-------------|
| [README.md] | 全系统使用指南 |
| [SETUP_GUIDE.md] | 安装步骤说明 |
| [docs/DATABASE_OPTIONS.md] | SQLite与LadybugDB的比较 |
| [docs/EMBEDDING_PROVIDERS.md] | 嵌入器选择指南（Voyage、OpenAI、本地方式） |
| [MIGRATION_GUIDE.md] | 旧版本迁移指南 |
| [CHANGELOG.md] | 版本更新记录 |

## 隐私与安全设置  

### 数据访问权限：**  
该插件会访问以下路径：  
- `~/.openclaw/agents/.../*.jsonl`：会话记录文件  
- `~/.nima/`：本地内存数据库（存储方式：SQLite或LadybugDB）  
- `~/.openclaw/extensions/`：插件安装目录  

**网络调用说明：**  
嵌入信息会发送至以下外部API：  
- **Voyage AI**（`api.voyageai.com`）：默认嵌入服务提供商  
- **OpenAI**（`api.openai.com`）：可选嵌入服务提供商  
- **本地模式**：使用内置的句子转换器时无需外部API调用  

**所需环境变量：**  
| 变量 | 用途 | 是否必填 |
|----------|---------|----------|
| `NIMA_EMBEDDER` | 选择嵌入服务提供商 | 可选（默认值：voyage） |
| `VOYAGE_API_KEY` | Voyage API认证密钥 | 使用Voyage API时必填 |
| `OPENAI_API_KEY` | OpenAI API认证密钥 | 使用OpenAI API时必填 |
| `NIMA_DATA_DIR` | 内存存储路径 | 可选（默认值：`~/.nima`） |
| `NIMA_LADYBUG` | 是否使用LadybugDB后端 | 可选（默认值：0） |

**安装脚本：**  
`install.sh` 脚本会：  
1. 检查系统是否安装了Python 3和Node.js  
2. 创建 `~/.nima/` 目录  
3. 通过pip安装所需Python包  
4. 将插件文件复制至 `~/.openclaw/extensions/` 目录  

**所有插件依赖包均来自PyPI。**  

## 版本更新记录  

### v2.1.0（2026年2月17日）  
- **新增功能：**  
  - 基于VADER的情感分析器，替代了传统的基于词典的情感检测机制  
    - 强化上下文分析功能  
    - 支持30多种习语识别  
    - 实现Panksepp 7情感模型  
    - 改进噪音处理机制  
  - 增加令牌预算  
  - 修复LadybugDB后端的导入问题  
  - 提升了数据库性能  

### v2.0.3（2026年2月15日）  
- **安全性增强：**  
  - 修复了`affect_history.py`中的路径遍历漏洞  
  - 修复了3个文件中的临时文件资源泄漏问题  
  - 优化了错误处理机制  
  - 提高了错误信息的可见性和可调试性  

### v2.0.1（2026年2月15日）  
- **线程安全性改进：**  
  - 采用双重检查锁定机制确保线程安全  
  - 明确了API密钥的使用要求  
  - 更新了相关文档  

### v2.0.0（2026年2月15日）  
- **新增功能：**  
  - 引入了LadybugDB后端及HNSW向量搜索功能  
  - 支持使用Cypher进行图谱查询  
  - 提供了统一的API查询工具（nima-query CLI）  
  - 加强了安全性防护（防止SQL注入和路径遍历攻击）  
  - 清理了临时文件  
  - 修复了线程安全相关问题  

### 其他版本更新：**  
- v1.2.1：增加了8种意识状态模型  
- v1.1.9：优化了插件性能  
- v1.2.0：增强了情感处理能力