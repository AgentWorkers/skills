---
name: nima-core
description: "Noosphere集成内存架构——为AI代理提供完整的认知功能栈：持久化内存、情商、梦境整合、群体智能、预知能力以及清晰的思维状态。支持4种嵌入方式，采用LadybugDB图谱后端，支持零配置安装。nima-core.ai"
version: 3.0.9
metadata: {"openclaw":{"emoji":"🧠","source":"https://github.com/lilubot/nima-core","homepage":"https://nima-core.ai","requires":{"bins":["python3","node"],"env":[]},"optional_env":{"NIMA_DATA_DIR":"Override default ~/.nima data directory","NIMA_EMBEDDER":"voyage|openai|ollama|local (default: local — zero external calls)","VOYAGE_API_KEY":"Required when NIMA_EMBEDDER=voyage","OPENAI_API_KEY":"Required when NIMA_EMBEDDER=openai","NIMA_OLLAMA_MODEL":"Model name when NIMA_EMBEDDER=ollama","NIMA_VOICE_TRANSCRIBER":"whisper|local (for voice notes)","WHISPER_MODEL":"tiny|base|small|medium|large","ANTHROPIC_API_KEY":"For memory pruner LLM distillation (opt-in only)"},"permissions":{"reads":["~/.nima/"],"writes":["~/.nima/","~/.openclaw/extensions/nima-*/"],"network":["voyage.ai (only if NIMA_EMBEDDER=voyage)","openai.com (only if NIMA_EMBEDDER=openai)"]},"external_calls":"All external API calls are opt-in via explicit env vars. Default mode uses local embeddings with zero network calls."}}
---
# NIMA Core 3.0

**Noosphere集成记忆架构**——为AI代理提供了一套完整的认知功能：持久性记忆、情感智能、梦境整合、群体智慧以及预知能力。

**官方网站：** https://nima-core.ai · **GitHub仓库：** https://github.com/lilubot/nima-core

## 快速入门

```bash
pip install nima-core && nima-core
```

您的机器人现在拥有了持久性记忆功能，无需任何额外配置。

## v3.0的新特性

### 完整的认知架构

NIMA已从一个简单的记忆插件演变为一个全面的认知架构：

| 模块 | 功能 | 版本 |
|--------|-------------|---------|
| **记忆捕获** | 三层数据捕获（输入/思考/输出），四阶段噪声过滤 | v2.0 |
| **语义检索** | 向量与文本混合搜索，生态评分，token预算限制 | v2.0 |
| **动态情感** | 根据Panksepp理论划分的七种情感状态 | v2.1 |
| **VADER分析器** | 基于上下文的情感分析（包括否定词、习语、程度修饰词） | v2.2 |
| **记忆精简器** | 从旧对话中提取语义核心内容，30天内抑制无关信息 | v2.3 |
| **梦境整合** | 每晚合成梦境，从中提取洞察和模式 | v2.4 |
| **群体智慧** | 通过共享数据库实现多代理间记忆共享（可选使用Redis发布/订阅机制） | v2.5 |
| **预知能力** | 通过时间模式挖掘实现记忆预加载 | v2.5 |
| **清晰时刻** | 情感共鸣的记忆会自发浮现 | v2.5 |
| **达尔文式记忆** | 通过余弦相似度算法对记忆进行聚类，去除重复内容 | v3.0 |
| **安装工具** | 一键安装，支持配置LadybugDB、挂载点及嵌入器设置 | v3.0 |

### v3.0的主要亮点
- 所有认知模块整合到一个包中
- 提供安装脚本（`install.sh`），实现零摩擦安装
- 所有OpenClaw挂载点均已准备好直接使用
- 重新编写了README文档，所有版本信息统一更新至`3.0.4`

## 架构概述

```text
OPENCLAW HOOKS
├── nima-memory/          Capture hook (3-layer, 4-phase noise filter)
│   ├── index.js          Hook entry point
│   ├── ladybug_store.py  LadybugDB storage backend
│   ├── embeddings.py     Multi-provider embedding (Voyage/OpenAI/Ollama/local)
│   ├── backfill.py       Historical transcript import
│   └── health_check.py   DB integrity checks
├── nima-recall-live/     Recall hook (before_agent_start)
│   ├── lazy_recall.py    Current recall engine
│   └── ladybug_recall.py LadybugDB-native recall
├── nima-affect/          Affect hook (message_received)
│   ├── vader-affect.js   VADER sentiment analyzer
│   └── emotion-lexicon.js Emotion keyword lexicon
└── shared/               Resilient wrappers, error handling

PYTHON CORE (nima_core/)
├── cognition/
│   ├── dynamic_affect.py         Panksepp 7-affect system
│   ├── emotion_detection.py      Text emotion extraction
│   ├── affect_correlation.py     Cross-affect analysis
│   ├── affect_history.py         Temporal affect tracking
│   ├── affect_interactions.py    Affect coupling dynamics
│   ├── archetypes.py             Personality baselines (Guardian, Explorer, etc.)
│   ├── personality_profiles.py   JSON personality configs
│   └── response_modulator_v2.py  Affect → response modulation
├── dream_consolidation.py        Nightly memory synthesis engine
├── memory_pruner.py              Episodic distillation + suppression
├── hive_mind.py                  Multi-agent memory sharing
├── precognition.py               Temporal pattern mining
├── lucid_moments.py              Spontaneous memory surfacing
├── connection_pool.py            SQLite pool (WAL, thread-safe)
├── logging_config.py             Singleton logger
└── metrics.py                    Thread-safe counters/timings
```

## 隐私与权限设置

- ✅ 所有数据存储在`~/.nima/`目录下
- ✅ 默认情况下，数据不会发送到外部服务器
- ❌ 无NIMA服务器，无跟踪行为，无数据分析
- 🔒 仅在使用Voyage/OpenAI时才会触发嵌入API调用（可选择性开启）

## 安全性

### 安装内容

| 组件 | 安装位置 | 功能 |
|-----------|----------|---------|
| Python核心模块 (`nima_core/`) | `~/.nima/` | 负责记忆处理和情感分析 |
| OpenClaw挂载点 | `~/.openclaw/extensions/nima-*/` | 负责数据捕获和检索 |
| SQLite数据库 | `~/.nima/memory/graph.sqlite` | 用于持久化存储 |
| 日志文件 | `~/.nima/logs/` | 包含调试日志（可选） |

### 凭据管理

| 环境变量 | 是否必需 | 是否涉及网络请求 | 功能 |
|---------|-----------|----------------|---------|
| `NIMA_EMBEDDER=local` | 否 | ❌ | 默认设置，使用本地嵌入方式 |
| `VOYAGE_API_KEY` | 仅在使用Voyage时需要 | ✅ 用于访问voyage.ai的云服务 |
| `OPENAI_API_KEY` | 仅在使用OpenAI时需要 | ✅ 用于访问openai.com的云服务 |
| `ANTHROPIC_API_KEY` | 仅在使用记忆精简器时需要 | ✅ 用于访问anthropic.com的服务 |
| `NIMA_OLLAMA_MODEL` | 仅在使用Ollama时需要 | ❌ | 使用本地GPU进行嵌入 |

**建议：** 默认情况下使用`NIMA_EMBEDDER=local`。仅在需要更高质量的嵌入服务时启用云服务。

### 安全特性

- **输入过滤**：在数据捕获前会过滤系统消息、重复内容及无效数据 |
- **防止SQL注入**：通过参数化查询防止SQL注入攻击 |
- **路径安全**：所有文件路径都会经过安全处理 |
- **临时文件清理**：自动清理临时文件 |
- **API超时设置**：网络请求有合理的超时限制（Voyage服务30秒，本地系统10秒）

### 最佳实践

1. **安装前检查**：在安装前仔细阅读`install.sh`脚本及相关挂载点文件 |
2. **备份配置**：在添加挂载点之前备份`~/.openclaw/openclaw.json`文件 |
3. **勿以root权限运行**：安装过程会写入用户主目录 |
4. **使用容器化环境**：如有疑问，请先在虚拟机或容器环境中进行测试 |
5. **定期更换API密钥**：使用云服务时定期更新API密钥 |
6. **监控日志**：定期检查`~/.nima/logs/`目录中的异常活动

## 数据存储位置

```text
~/.nima/
├── memory/
│   ├── graph.sqlite       # SQLite backend (default)
│   ├── ladybug.lbug       # LadybugDB backend (optional)
│   ├── embedding_cache.db # Cached embeddings
│   └── embedding_index.npy# Vector index
├── affect/
│   └── affect_state.json  # Current emotional state
└── logs/                  # Debug logs (if enabled)

~/.openclaw/extensions/
├── nima-memory/           # Capture hook
├── nima-recall-live/     # Recall hook
└── nima-affect/          # Affect hook
```

**控制设置：**
```json
{
  "plugins": {
    "entries": {
      "nima-memory": {
        "skip_subagents": true,
        "skip_heartbeats": true,
        "noise_filtering": { "filter_system_noise": true }
      }
    }
  }
}
```

## 配置选项

### 嵌入服务提供商

| 服务提供商 | 设置方式 | 数据维度 | 成本 |
|----------|-------|------|------|
| **本地**（默认） | `NIMA_EMBEDDER=local` | 384维度 | 免费 |
| **Voyage AI** | `NIMA_EMBEDDER=voyage` + `VOYAGE_API_KEY` | 1024维度 | 每百万token费用0.12美元 |
| **OpenAI** | `NIMA_EMBEDDER=openai` + `OPENAI_API_KEY` | 1536维度 | 每百万token费用0.13美元 |
| **Ollama** | `NIMA_EMBEDDER=ollama` + `NIMA_OLLAMA_MODEL` | 768维度 | 免费 |

### 数据库后端

| | 使用的数据库 | 推荐使用 | 性能对比 |
|--|-----------------|------------------------|
| 文本搜索 | SQLite | **9毫秒**（速度提升3.4倍） |
| 向量搜索 | 外部服务 | **原生HNSW算法（18毫秒） |
| 图谱查询 | SQL JOIN操作 | **原生Cypher查询语言** |
| 数据库大小 | 约91MB | **约50MB（体积减少44%） |

**升级建议：** `pip install real-ladybug && python -c "from nima_core.storage import migrate; migrate()"`

### 所有环境变量

```bash
# Embedding (default: local)
NIMA_EMBEDDER=local|voyage|openai|ollama
VOYAGE_API_KEY=pa-xxx
OPENAI_API_KEY=sk-xxx
NIMA_OLLAMA_MODEL=nomic-embed-text

# Data paths
NIMA_DATA_DIR=~/.nima
NIMA_DB_PATH=~/.nima/memory/ladybug.lbug

# Memory pruner
NIMA_DISTILL_MODEL=claude-haiku-4-5
ANTHROPIC_API_KEY=sk-ant-xxx

# Logging
NIMA_LOG_LEVEL=INFO
NIMA_DEBUG_RECALL=1
```

## 挂载点（Hook）功能

| 挂载点 | 触发条件 | 执行操作 |
|------|-------|------|
| `nima-memory` | 保存数据后 | 捕获三层数据，过滤噪声后存储到图谱数据库 |
| `nima-recall-live` | 在LLM模型使用前 | 搜索记忆内容，根据情感状态进行评分，并作为上下文信息注入（使用3000个token） |
| `nima-affect` | 收到消息时 | 使用VADER情感分析模型，判断情感状态，并调整行为模式 |

### 安装步骤

```bash
./install.sh
openclaw gateway restart
```

或手动安装方式：
```bash
cp -r openclaw_hooks/nima-memory ~/.openclaw/extensions/
cp -r openclaw_hooks/nima-recall-live ~/.openclaw/extensions/
cp -r openclaw_hooks/nima-affect ~/.openclaw/extensions/
```

## 高级功能

### 梦境整合
每晚从记忆中提取洞察和模式：
```bash
python -m nima_core.dream_consolidation
# Or schedule via OpenClaw cron at 2 AM
```

### 记忆精简器
将旧对话内容提炼成语义核心内容，去除冗余信息：
```bash
python -m nima_core.memory_pruner --min-age 14 --live
python -m nima_core.memory_pruner --restore 12345  # undo within 30 days
```

### 群体智慧
支持多代理间的记忆共享：
```python
from nima_core import HiveMind
hive = HiveMind(db_path="~/.nima/memory/ladybug.lbug")
context = hive.build_agent_context("research task", max_memories=8)
hive.capture_agent_result("agent-1", "result summary", "model-name")
```

### 预知能力
通过时间模式挖掘实现记忆预加载：
```python
from nima_core import NimaPrecognition
precog = NimaPrecognition(db_path="~/.nima/memory/ladybug.lbug")
precog.run_mining_cycle()
```

### 清晰时刻
情感共鸣的记忆会自发浮现（具备安全机制：过滤创伤性记忆，选择合适的时间点，每日使用次数有限）：
```python
from nima_core import LucidMoments
lucid = LucidMoments(db_path="~/.nima/memory/ladybug.lbug")
moment = lucid.surface_moment()
```

### 情感系统
基于Panksepp理论实现七种情感状态及个性特征：
```python
from nima_core import DynamicAffectSystem
affect = DynamicAffectSystem(identity_name="my_bot", baseline="guardian")
state = affect.process_input("I'm excited about this!")
# Archetypes: guardian, explorer, trickster, empath, sage
```

## API接口

```python
from nima_core import (
    DynamicAffectSystem,
    get_affect_system,
    HiveMind,
    NimaPrecognition,
    LucidMoments,
)

# Affect (thread-safe singleton)
affect = get_affect_system(identity_name="lilu")
state = affect.process_input("Hello!")

# Hive Mind
hive = HiveMind()
context = hive.build_agent_context("task description")

# Precognition
precog = NimaPrecognition()
precog.run_mining_cycle()

# Lucid Moments
lucid = LucidMoments()
moment = lucid.surface_moment()
```

## 版本历史

详细版本更新记录请参见[CHANGELOG.md](./CHANGELOG.md)。

### 最新版本
- **v3.0.4**（2026年2月23日）：新增达尔文式记忆引擎、新的命令行工具、修复漏洞 |
- **v2.5.0**（2026年2月21日）：加入群体智慧和预知功能 |
- **v2.4.0**（2026年2月20日）：改进梦境整合机制 |
- **v2.3.0**（2026年2月19日）：优化记忆精简器，支持Ollama模型 |
- **v2.2.0**（2026年2月19日）：增强情感分析功能，改进噪声过滤机制 |
- **v2.0.0**（2026年2月13日）：采用LadybugDB作为数据库后端，增强安全性，通过348项测试验证 |

## 许可证

NIMA采用MIT许可证——适用于所有AI代理，无论商业用途还是个人使用。