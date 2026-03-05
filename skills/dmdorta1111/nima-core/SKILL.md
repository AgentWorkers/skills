---
name: nima-core
description: "**Noosphere集成内存架构**——专为AI代理设计的完整认知系统：支持持久化存储、情感智能、梦境整合、群体思维、预知能力以及清晰的意识状态。该架构提供了4种数据嵌入方式，并采用LadybugDB图谱作为后端存储系统，支持零配置安装。  
**nima-core.ai**"
version: 3.2.0
metadata:
  {
    "openclaw": {
      "emoji": "🧠",
      "source": "https://github.com/lilubot/nima-core",
      "homepage": "https://nima-core.ai",
      "requires": { "bins": ["python3", "node"] },
      "install": [
        {
          "id": "shell",
          "kind": "shell",
          "script": "install.sh",
          "label": "Install NIMA Core (creates ~/.nima, pip-installs dependencies, copies OpenClaw hooks)"
        }
      ],
      "permissions": {
        "reads":   ["~/.nima/", "~/.openclaw/extensions/nima-*/"],
        "writes":  ["~/.nima/", "~/.openclaw/extensions/nima-*/"],
        "network": [
          "voyage.ai (only if NIMA_EMBEDDER=voyage)",
          "openai.com (only if NIMA_EMBEDDER=openai or ANTHROPIC_API_KEY set)",
          "anthropic.com (only if ANTHROPIC_API_KEY set — memory pruner)"
        ]
      },
      "optional_env": {
        "NIMA_DATA_DIR":         "Override default ~/.nima data directory",
        "NIMA_EMBEDDER":         "voyage|openai|ollama|local (default: local — zero external calls)",
        "VOYAGE_API_KEY":        "Required when NIMA_EMBEDDER=voyage",
        "OPENAI_API_KEY":        "Required when NIMA_EMBEDDER=openai",
        "NIMA_OLLAMA_MODEL":     "Model name when NIMA_EMBEDDER=ollama",
        "NIMA_VOICE_TRANSCRIBER":"whisper|local (for voice notes)",
        "WHISPER_MODEL":         "tiny|base|small|medium|large",
        "ANTHROPIC_API_KEY":     "For memory pruner LLM distillation (opt-in only)",
        "HIVE_ENABLED":          "1 to enable multi-agent memory sharing via shared DB",
        "HIVE_REDIS_URL":        "Redis URL for real-time hive pub/sub (optional, HIVE_ENABLED=1)"
      },
      "external_calls": "All external API calls are opt-in via explicit env vars. Default mode uses local embeddings with zero network calls. install.sh does pip install nima-core and optional real-ladybug; review before running in shared/production environments."
    }
  }
---
# NIMA Core 3.2

**Noosphere集成记忆架构** — 为AI代理提供了一套完整的认知功能：持久化记忆、情感智能、梦境整合、群体思维以及预知能力。

**官方网站：** https://nima-core.ai · **GitHub仓库：** https://github.com/lilubot/nima-core

## 快速入门

```bash
pip install nima-core && nima-core
```

您的机器人现在拥有了持久化记忆功能，无需任何额外配置。

## v3.0的新特性

### 完整的认知架构

NIMA已从一个简单的记忆插件发展成为一个全面的认知架构：

| 模块 | 功能 | 版本 |
|--------|-------------|---------|
| **记忆捕获** | 三层数据捕获（输入/思考/输出），四阶段噪声过滤 | v2.0 |
| **语义检索** | 向量与文本混合搜索，生态评分系统，token预算控制 | v2.0 |
| **动态情感** | 根据Panksepp理论划分的七种情感状态（寻求、愤怒、恐惧、欲望、关怀、恐慌、玩耍） | v2.1 |
| **VADER分析器** | 基于上下文的情感分析——包括情感强度提升、否定词处理、习语识别、程度修饰词分析 | v2.2 |
| **记忆修剪器** | 通过LLM对旧对话进行提炼，生成语义摘要，并设置30天的数据保留期限 | v2.3 |
| **梦境整合** | 每晚从情景记忆中提取洞察和模式 | v2.4 |
| **群体思维** | 多个代理通过共享数据库进行记忆共享（支持Redis发布/订阅机制） | v2.5 |
| **预知能力** | 通过分析时间模式来预加载记忆内容 | v2.5 |
| **清晰时刻** | 情感共鸣的记忆会自发浮现 | v2.5 |
| **达尔文式记忆** | 通过余弦相似度算法对相似记忆进行聚类，并通过LLM验证 | v3.0 |
| **安装工具** | 一键安装脚本（包括LadybugDB、钩子配置等） | v3.0 |

### v3.0的主要亮点
- 所有认知模块整合到一个包中
- 提供了一键安装工具（`install.sh`），简化设置流程
- 所有的OpenClaw钩子都已打包好，可直接使用
- 重新编写了README文档，所有版本信息统一更新至`3.0.4`

## 架构

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

- ✅ 所有数据均存储在`~/.nima/`目录下
- ✅ 默认情况下，所有外部调用都被禁用
- ✅ NIMA不拥有任何服务器，不进行任何数据追踪，也不会将数据发送给外部服务
- ⚠️ 可选网络功能：群体思维（Redis发布/订阅）、预知能力（外部LLM端点）、LadybugDB迁移——详见“可选功能”部分
- 🔒 仅在使用时才会触发嵌入API调用（需要配置`VOYAGE_API_KEY`、`OPENAI_API_KEY`等）

### 带有网络访问功能的可选特性

| 特性 | 环境变量 | 需要的网络调用 | 默认状态 |
|---------|----------|------------------|---------|
| 云嵌入服务 | `NIMA_EMBEDDER=voyage` | voyage.ai | 关闭 |
| 云嵌入服务 | `NIMA_EMBEDDER=openai` | openai.com | 关闭 |
| 记忆修剪器 | `ANTHROPIC_API_KEY` | anthropic.com | 关闭 |
| Ollama嵌入服务 | `NIMA_EMBEDDER=ollama` | localhost:11434 | 关闭 |
| 群体思维 | `HIVE_ENABLED=true` | 使用Redis发布/订阅 | 关闭 |
| 预知能力 | 使用外部LLM时需要配置端点 | 关闭 |

## 安全性

### 安装内容

| 组件 | 安装位置 | 功能 |
|-----------|----------|---------|
| Python核心 | `~/.nima/` | 负责记忆处理、情感分析、认知功能 |
| OpenClaw钩子 | `~/.openclaw/extensions/nima-*/` | 负责数据捕获、检索、情感处理 |
| SQLite数据库 | `~/.nima/memory/graph.sqlite` | 用于持久化存储 |
| 日志文件 | `~/.nima/logs/` | 存储调试日志（可选） |

### 凭据管理

| 环境变量 | 是否必需 | 是否涉及网络调用 | 功能 |
|---------|-----------|----------------|---------|
| `NIMA_EMBEDDER=local` | 否 | ✌ | 默认情况下使用本地嵌入服务 |
| `VOYAGE_API_KEY` | 仅在使用Voyage服务时需要 | ✅ | 用于云嵌入服务 |
| `OPENAI_API_KEY` | 仅在使用OpenAI服务时需要 | ✅ | 用于云嵌入服务 |
| `ANTHROPIC_API_KEY` | 仅在使用记忆修剪器时需要 | ✅ | 用于处理嵌入数据 |
| `NIMA_OLLAMA_MODEL` | 仅在使用Ollama服务时需要 | ❌ | 用于本地GPU嵌入 |

**建议：** 默认情况下使用`NIMA_EMBEDDER=local`。仅在需要更高质量的嵌入服务时再启用云服务。

### 安全特性

- **输入过滤**：系统消息、心跳信号以及重复数据在捕获前会被过滤掉
- **防止SQL注入**：通过参数化查询防止SQL注入攻击
- **路径安全**：所有文件路径都会经过安全处理
- **临时文件清理**：自动清理临时文件
- **API超时设置**：网络调用有合理的超时限制（Voyage服务30秒，本地服务10秒）

### 最佳实践

1. **安装前检查**：在安装前请仔细阅读`install.sh`脚本和所有钩子文件
2. **备份配置**：在添加钩子之前，请备份`~/.openclaw/openclaw.json`文件
3. **避免以root用户身份运行**：安装过程会写入用户的主目录
4. **使用容器化环境**：如果不确定如何安装，建议在虚拟机或容器环境中进行测试
5. **定期更换API密钥**：使用云嵌入服务时，请定期更换API密钥
6. **监控日志**：定期检查`~/.nima/logs/`目录中的日志以检测异常活动

### 数据存储位置

**控制设置：**
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

## 配置选项

### 嵌入服务提供商

| 提供商 | 设置方式 | 数据维度 | 成本 |
|----------|-------|------|------|
| **本地**（默认） | `NIMA_EMBEDDER=local` | 384维度 | 免费 |
| **Voyage AI** | `NIMA_EMBEDDER=voyage` + `VOYAGE_API_KEY` | 1024维度 | 每100万个token费用0.12美元 |
| **OpenAI** | `NIMA_EMBEDDER=openai` + `OPENAI_API_KEY` | 1536维度 | 每100万个token费用0.13美元 |
| **Ollama** | `NIMA_EMBEDDER=ollama` + `NIMA_OLLAMA_MODEL` | 768维度 | 免费 |

### 数据库后端

| | 使用的数据库 | 推荐使用 | 性能对比 |
|--|-----------------|------------------------|
| 文本搜索 | SQLite | **9毫秒**（速度提升3.4倍） |
| 向量搜索 | 外部服务 | **原生HNSW算法（18毫秒） |
| 图谱查询 | SQL JOIN操作 | **原生Cypher查询** |
| 数据库大小 | 约91MB | **约50MB**（体积减少44%） |
| 升级建议：`pip install real-ladybug && python -c "from nima_core.storage import migrate; migrate()"`

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

## 钩子功能

| 钩子名称 | 触发条件 | 执行操作 |
|------|-------|------|
| `nima-memory` | 保存操作后 | 捕获三层数据 → 过滤噪声 → 存储到图谱数据库 |
| `nima-recall-live` | 在调用LLM之前 | 检索记忆 → 根据情感状态进行评分 → 以3000个token为预算注入到上下文中 |
| `nima-affect` | 接收到消息时 | 使用VADER情感分析 → 根据Panksepp理论划分情感状态 → 调整行为 |

### 安装步骤

```bash
./install.sh
openclaw gateway restart
```

或手动安装：
```bash
cp -r openclaw_hooks/nima-memory ~/.openclaw/extensions/
cp -r openclaw_hooks/nima-recall-live ~/.openclaw/extensions/
cp -r openclaw_hooks/nima-affect ~/.openclaw/extensions/
```

## 高级功能

### 梦境整合
每晚从情景记忆中提取洞察和模式：
```bash
python -m nima_core.dream_consolidation
# Or schedule via OpenClaw cron at 2 AM
```

### 记忆修剪器
对旧对话进行提炼，生成语义摘要，并过滤掉无关信息：
```bash
python -m nima_core.memory_pruner --min-age 14 --live
python -m nima_core.memory_pruner --restore 12345  # undo within 30 days
```

### 群体思维
支持多个代理之间的记忆共享：
```python
from nima_core import HiveMind
hive = HiveMind(db_path="~/.nima/memory/ladybug.lbug")
context = hive.build_agent_context("research task", max_memories=8)
hive.capture_agent_result("agent-1", "result summary", "model-name")
```

### 预知能力
通过分析时间模式来预加载记忆内容：
```python
from nima_core import NimaPrecognition
precog = NimaPrecognition(db_path="~/.nima/memory/ladybug.lbug")
precog.run_mining_cycle()
```

### 清晰时刻
情感共鸣的记忆会自发浮现（具备安全机制：过滤创伤性记忆，选择合适的时间节点，每日使用次数有限）：
```python
from nima_core import LucidMoments
lucid = LucidMoments(db_path="~/.nima/memory/ladybug.lbug")
moment = lucid.surface_moment()
```

### 情感系统
基于Panksepp理论划分的七种情感状态，并结合人格特征进行情感管理：
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

完整的版本历史请参阅[CHANGELOG.md](./CHANGELOG.md)。

### 最新版本更新
- **v3.0.4**（2026年2月23日）：引入了达尔文式记忆引擎、新的命令行接口（CLI），修复了多个漏洞
- **v2.5.0**（2026年2月21日）：新增了群体思维和预知功能
- **v2.4.0**（2026年2月20日）：优化了梦境整合功能
- **v2.3.0**（2026年2月19日）：改进了记忆修剪器，增加了对Ollama模型的支持
- **v2.2.0**（2026年2月19日）：增强了VADER情感分析功能，改进了噪声过滤机制，引入了生态评分系统
- **v2.0.0**（2026年2月13日）：更新了LadybugDB后端，加强了安全性，并进行了348项测试

## 许可证

NIMA采用MIT许可证——适用于所有AI代理，无论是商业用途还是个人使用。