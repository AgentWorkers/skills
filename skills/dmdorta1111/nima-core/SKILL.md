---
name: nima-core
description: "**Noosphere集成内存架构**——专为AI代理设计的完整认知系统：持久性内存、情感智能、梦境整合、群体思维、预知能力以及清晰的思维状态。支持4种嵌入方式，采用LadybugDB图谱后端，支持零配置安装。nima-core.ai"
version: 3.1.4
metadata: {"openclaw":{"emoji":"🧠","source":"https://github.com/lilubot/nima-core","homepage":"https://nima-core.ai","requires":{"bins":["python3","node"],"env":[]},"optional_env":{"NIMA_DATA_DIR":"Override default ~/.nima data directory","NIMA_EMBEDDER":"voyage|openai|ollama|local (default: local — zero external calls)","VOYAGE_API_KEY":"Required when NIMA_EMBEDDER=voyage","OPENAI_API_KEY":"Required when NIMA_EMBEDDER=openai","NIMA_OLLAMA_MODEL":"Model name when NIMA_EMBEDDER=ollama","NIMA_VOICE_TRANSCRIBER":"whisper|local (for voice notes)","WHISPER_MODEL":"tiny|base|small|medium|large","ANTHROPIC_API_KEY":"For memory pruner LLM distillation (opt-in only)"},"permissions":{"reads":["~/.nima/"],"writes":["~/.nima/","~/.openclaw/extensions/nima-*/"],"network":["voyage.ai (only if NIMA_EMBEDDER=voyage)","openai.com (only if NIMA_EMBEDDER=openai)"]},"external_calls":"All external API calls are opt-in via explicit env vars. Default mode uses local embeddings with zero network calls."}}
---
# NIMA Core 3.1

**Noosphere集成记忆架构** — 为AI代理提供了一套完整的认知功能：持久性记忆、情感智能、梦境整合、群体思维以及预知能力。

**官方网站：** https://nima-core.ai · **GitHub仓库：** https://github.com/lilubot/nima-core

## 快速入门

```bash
pip install nima-core && nima-core
```

您的机器人现在具备了持久性记忆功能，无需任何额外配置。

## v3.0的新特性

### 完整的认知功能栈

NIMA已从一个简单的记忆插件发展成为一个全面的认知架构：

| 模块 | 功能 | 版本 |
|--------|-------------|---------|
| **记忆捕获** | 三层数据捕获（输入/思考/输出），四阶段噪声过滤 | v2.0 |
| **语义检索** | 向量与文本混合搜索，生态评分，token预算控制 | v2.0 |
| **动态情感** | 根据Panksepp理论划分的七种情感状态（寻求、愤怒、恐惧、欲望、关怀、恐慌、玩耍） | v2.1 |
| **VADER分析器** | 基于上下文的情感分析——包括情感强度、否定词、习语和程度修饰词 | v2.2 |
| **记忆修剪器** | 从旧对话中提取语义精华，30天内抑制无关信息 | v2.3 |
| **梦境整合** | 每晚对情景记忆进行整合，提取洞察和模式 | v2.4 |
| **群体思维** | 通过共享数据库实现多代理间记忆共享（可选支持Redis发布/订阅） | v2.5 |
| **预知能力** | 通过分析时间模式实现记忆预加载 | v2.5 |
| **清晰时刻** | 情感共鸣的记忆会自发浮现 | v2.5 |
| **达尔文式记忆** | 根据相似性对记忆进行分类，使用余弦相似度和LLM进行验证 | v3.0 |
| **安装程序** | 一键安装——包括LadybugDB、钩子设置和嵌入器配置 | v3.0 |

### v3.0的亮点
- 所有认知模块整合到一个包中
- 提供安装程序（`install.sh`），实现零配置安装
- 所有OpenClaw钩子均已准备好直接使用
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

## 隐私与权限

- ✅ 所有数据存储在本地`~/.nima/`目录下
- ✅ 默认情况下：仅使用本地嵌入方式，**不进行任何外部调用**
- ✅ NIMA不拥有服务器，不进行任何数据追踪，也不会将数据发送到外部服务
- ⚠️ 可选网络功能：群体思维（Redis发布/订阅）、预知能力（LLM端点）、LadybugDB迁移——详见下方“可选功能”
- 🔒 仅在使用时才会触发嵌入器API调用（VOYAGE_API_KEY、OPENAI_API_KEY等）

### 带有网络访问功能的可选特性

| 特性 | 环境变量 | 需要的网络调用 | 默认设置 |
|---------|----------|------------------|---------|
| 云嵌入 | `NIMA_EMBEDDER=voyage` | voyage.ai | 关闭 |
| 云嵌入 | `NIMA_EMBEDDER=openai` | openai.com | 关闭 |
| 记忆修剪器 | 设置`ANTHROPIC_API_KEY` | anthropic.com | 关闭 |
| Ollama嵌入 | `NIMA_EMBEDDER=ollama` | localhost:11434 | 关闭 |
| 群体思维 | `HIVE_ENABLED=true` | Redis发布/订阅 | 关闭 |
| 预知能力 | 使用外部LLM | 配置相应的端点 | 关闭 |

## 安全性

### 安装内容

| 组件 | 安装位置 | 功能 |
|-----------|----------|---------|
| Python核心（`nima_core/`） | `~/.nima/` | 负责记忆处理、情感分析和认知功能 |
| OpenClaw钩子 | `~/.openclaw/extensions/nima-*/` | 负责数据捕获、检索和情感处理 |
| SQLite数据库 | `~/.nima/memory/graph.sqlite` | 用于持久化存储 |
| 日志 | `~/.nima/logs/` | 存储调试日志（可选） |

### 凭据管理

| 环境变量 | 是否必需 | 是否涉及网络调用 | 功能 |
|---------|-----------|----------------|---------|
| `NIMA_EMBEDDER=local` | 否 | ❌ | 默认设置——使用本地嵌入方式 |
| `VOYAGE_API_KEY` | 仅在使用Voyage时需要 | ✅ | 用于云嵌入 |
| `OPENAI_API_KEY` | 仅在使用OpenAI时需要 | ✅ | 用于云嵌入 |
| `ANTHROPIC_API_KEY` | 仅在使用记忆修剪器时需要 | ✅ | 用于数据处理 |
| `NIMA_OLLAMA_MODEL` | 仅在使用Ollama时需要 | ❌ | 用于本地GPU嵌入 |

**建议：** 默认情况下使用`NIMA_EMBEDDER=local`。仅在需要更高质量的嵌入效果时才启用云服务。

### 安全特性

- **输入过滤**：在数据捕获前会过滤系统消息、重复内容及无效数据 |
- **防止SQL注入**：通过参数化查询防止SQL注入攻击 |
- **路径安全**：所有文件路径都会经过安全处理 |
- **临时文件清理**：自动清理临时文件 |
- **API超时设置**：网络调用有合理的超时限制（Voyage服务30秒，本地服务10秒）

### 最佳实践

1. **安装前检查**：在运行前仔细阅读`install.sh`文件和所有钩子脚本 |
2. **备份配置**：在添加钩子之前备份`~/.openclaw/openclaw.json`文件 |
3. **避免以root权限运行**：安装过程会写入用户主目录 |
4. **使用容器化环境**：如果不确定安全性，建议在虚拟机或容器环境中进行测试 |
5. **定期更换API密钥**：使用云嵌入服务时，定期更换API密钥 |
6. **监控日志**：定期检查`~/.nima/logs/`目录中的日志以发现异常活动 |

### 数据存储位置

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

| 服务提供商 | 设置方式 | 插入维度 | 成本 |
|----------|-------|------|------|
| **本地**（默认） | `NIMA_EMBEDDER=local` | 384维度 | 免费 |
| **Voyage AI** | `NIMA_EMBEDDER=voyage` + `VOYAGE_API_KEY` | 1024维度 | 每100万个token费用0.12美元 |
| **OpenAI** | `NIMA_EMBEDDER=openai` + `OPENAI_API_KEY` | 1536维度 | 每100万个token费用0.13美元 |
| **Ollama** | `NIMA_EMBEDDER=ollama` + `NIMA_OLLAMA_MODEL` | 768维度 | 免费 |

### 数据库后端

| | SQLite（默认） | 推荐使用LadybugDB |
|--|-----------------|------------------------|
| 文本搜索 | 31毫秒 | LadybugDB：9毫秒（速度提升3.4倍） |
| 向量搜索 | 使用外部服务 | 使用OpenAI的HNSW算法（18毫秒） |
| 图谱查询 | 使用SQL JOIN | 使用Cypher查询语言 |
| 数据库大小 | 约91MB | LadybugDB：约50MB（体积减少44%） |

升级命令：`pip install real-ladybug && python -c "from nima_core.storage import migrate; migrate()"`

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
| `nima-affect` | 接收到消息时 | 使用VADER模型分析情感状态 → 调整行为模式 |

### 安装方法

```bash
./install.sh
openclaw gateway restart
```

或手动安装方法：
```bash
cp -r openclaw_hooks/nima-memory ~/.openclaw/extensions/
cp -r openclaw_hooks/nima-recall-live ~/.openclaw/extensions/
cp -r openclaw_hooks/nima-affect ~/.openclaw/extensions/
```

## 高级功能

### 梦境整合
每晚对情景记忆进行整合，提取其中的洞察和模式：
```bash
python -m nima_core.dream_consolidation
# Or schedule via OpenClaw cron at 2 AM
```

### 记忆修剪器
从旧对话中提取语义精华，过滤掉无关信息：
```bash
python -m nima_core.memory_pruner --min-age 14 --live
python -m nima_core.memory_pruner --restore 12345  # undo within 30 days
```

### 群体思维
支持多代理间的记忆共享：
```python
from nima_core import HiveMind
hive = HiveMind(db_path="~/.nima/memory/ladybug.lbug")
context = hive.build_agent_context("research task", max_memories=8)
hive.capture_agent_result("agent-1", "result summary", "model-name")
```

### 预知能力
通过分析时间模式实现记忆预加载：
```python
from nima_core import NimaPrecognition
precog = NimaPrecognition(db_path="~/.nima/memory/ladybug.lbug")
precog.run_mining_cycle()
```

### 清晰时刻
情感共鸣的记忆会自发浮现（包含安全机制：过滤创伤性内容，选择合适的时间点，每日使用次数有限）：
```python
from nima_core import LucidMoments
lucid = LucidMoments(db_path="~/.nima/memory/ladybug.lbug")
moment = lucid.surface_moment()
```

### 情感系统
基于Panksepp理论划分的七种情感状态，并结合人格特征进行分析：
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

## 更新日志

完整的版本历史记录请参阅[CHANGELOG.md](./CHANGELOG.md)。

### 最新版本

- **v3.0.4**（2026年2月23日）：引入达尔文式记忆引擎、新的命令行接口（CLI），修复了多个漏洞 |
- **v2.5.0**（2026年2月21日）：新增群体思维和预知功能 |
- **v2.4.0**（2026年2月20日）：改进梦境整合机制 |
- **v2.3.0**（2026年2月19日）：优化记忆修剪器，支持Ollama模型 |
- **v2.2.0**（2026年2月19日）：增强VADER情感分析功能，改进噪声过滤机制 |
- **v2.0.0**（2026年2月13日）：更新LadybugDB后端，加强安全性，新增348项测试 |

## 许可证

NIMA采用MIT许可证——适用于所有AI代理，无论是商业用途还是个人使用。