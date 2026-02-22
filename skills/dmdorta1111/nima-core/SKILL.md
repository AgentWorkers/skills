---
name: nima-core
description: "**Noosphere集成内存架构**——专为AI代理设计的完整认知系统：支持持久化内存、情感智能、梦境整合、群体思维、预知能力以及清晰的意识状态。该架构提供了4种数据嵌入方式，采用LadybugDB图谱作为后端存储系统，并支持零配置安装。开发团队：nima-core.ai"
version: 3.0.3
metadata: {"openclaw":{"emoji":"🧠","requires":{"bins":["python3","node"],"env":["NIMA_DATA_DIR"]},"optional_env":{"NIMA_EMBEDDER":"voyage|openai|ollama|local (default: local)","VOYAGE_API_KEY":"Required when NIMA_EMBEDDER=voyage","OPENAI_API_KEY":"Required when NIMA_EMBEDDER=openai","NIMA_OLLAMA_MODEL":"Model name when NIMA_EMBEDDER=ollama","NIMA_VOICE_TRANSCRIBER":"whisper|local (for voice notes)","WHISPER_MODEL":"tiny|base|small|medium|large","ANTHROPIC_API_KEY":"For memory pruner LLM distillation"},"permissions":{"reads":["~/.openclaw/agents/*/sessions/*.jsonl"],"writes":["~/.nima/"],"network":["voyage.ai (conditional)","openai.com (conditional)"]}}}
---
# NIMA Core 3.0

**Noosphere集成记忆架构** — 为AI代理提供了一套完整的认知功能：持久性记忆、情感智能、梦境整合、群体思维以及预知能力。

**官方网站：** https://nima-core.ai · **GitHub仓库：** https://github.com/lilubot/nima-core

## 快速入门

```bash
pip install nima-core && nima-core
```

您的机器人现在具备了持久性记忆功能，无需任何额外配置。

## v3.0的新特性

### 完整的认知架构

NIMA已从一个简单的记忆插件发展成为一个全面的认知架构：

| 模块 | 功能 | 版本 |
|--------|-------------|---------|
| **记忆捕捉** | 三层数据捕捉（输入/思考/输出），四阶段噪声过滤 | v2.0 |
| **语义检索** | 向量与文本混合搜索，生态评分系统，token预算控制 | v2.0 |
| **动态情感** | 根据Panksepp模型划分的七种情感状态（寻求、愤怒、恐惧、欲望、关怀、恐慌、玩耍） | v2.1 |
| **VADER分析器** | 基于上下文的情感分析（包括情感强度、否定词、习语、程度修饰词） | v2.2 |
| **记忆筛选器** | 从旧对话中提取语义精华，对原始数据进行处理并设置30天的存储期限 | v2.3 |
| **梦境整合** | 每晚对记忆内容进行整合，提取其中的洞察和模式 | v2.4 |
| **群体思维** | 通过共享数据库实现多代理之间的记忆共享（支持Redis发布/订阅机制） | v2.5 |
| **预知能力** | 通过分析时间模式来实现记忆的预加载 | v2.5 |
| **清晰时刻** | 情感共鸣的记忆会自发浮现 | v2.5 |

### v3.0.2的修复问题
- **严重问题：** v3.0.0版本的ClawHub包中缺少`nima_core/cognition/`目录下的10个文件以及所有OpenClaw相关的钩子文件（问题源于`.clawhubignore`文件的错误配置）——现已修复 |
- 《README.md》文件已全面重写，所有版本信息已统一。

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

- ✅ 所有数据均存储在本地`~/.nima/`目录中 |
- ✅ 默认情况下：不进行任何外部数据调用 |
- ❌ 无NIMA服务器，无数据追踪，无数据分析 |
- 🔒 仅在使用Voyage或OpenAI时才会触发嵌入API调用（需用户选择启用）

**控制选项：**
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

| 提供商 | 设置方式 | 数据维度 | 成本 |
|----------|-------|------|------|
| **本地**（默认） | `NIMA_EMBEDDER=local` | 384维度 | 免费 |
| **Voyage AI** | `NIMA_EMBEDDER=voyage` + `VOYAGE_API_KEY` | 1024维度 | 每100万个token费用0.12美元 |
| **OpenAI** | `NIMA_EMBEDDER=openai` + `OPENAI_API_KEY` | 1536维度 | 每100万个token费用0.13美元 |
| **Ollama** | `NIMA_EMBEDDER=ollama` + `NIMA_OLLAMA_MODEL` | 768维度 | 免费 |

### 数据库后端

| | SQLite（默认） | LadybugDB（推荐） |
|--|-----------------|------------------------|
| 文本搜索 | 31毫秒 | LadybugDB：9毫秒（速度提升3.4倍） |
| 向量搜索 | 外部服务 | 使用OpenAI的HNSW算法（速度提升） |
| 图谱查询 | 支持SQL JOIN操作 | 使用Cypher语言 |
| 数据库大小 | 约91MB | LadybugDB：约50MB（体积减少44%） |

升级方式：`pip install real-ladybug && python -c "from nima_core.storage import migrate; migrate()"`

## 所有环境变量

```bash
# Embedding (default: local)
NIMA_EMBEDDER=local|voyage|openai|ollama
VOYAGE_API_KEY=pa-xxx
OPENAI_API_KEY=sk-xxx
NIMA_OLLAMA_MODEL=nomic-embed-text

# Data paths
NIMA_DATA_DIR=~/.nima/memory
NIMA_DB_PATH=~/.nima/memory/ladybug.lbug

# Memory pruner
NIMA_DISTILL_MODEL=claude-haiku-4-5
ANTHROPIC_API_KEY=sk-ant-xxx

# Logging
NIMA_LOG_LEVEL=INFO
NIMA_DEBUG_RECALL=1
```

## 钩子函数（Hooks）

| 钩子名称 | 触发条件 | 功能 |
|------|-------|------|
| `nima-memory` | 保存操作后 | 捕获三层记忆数据，过滤噪声，存储到图谱数据库中 |
| `nima-recall-live` | 在LLM模型使用前 | 搜索记忆内容，根据情感评分系统进行筛选，并将结果作为上下文信息注入（使用3000个token） |
| `nima-affect` | 接收到消息时 | 使用VADER模型分析情感状态，并根据Panksepp模型调整行为 |

## 安装说明

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
每晚对记忆内容进行整合，提取其中的洞察和模式：
```bash
python -m nima_core.dream_consolidation
# Or schedule via OpenClaw cron at 2 AM
```

### 记忆筛选器
将旧对话内容提炼成语义精华，过滤掉无关信息：
```bash
python -m nima_core.memory_pruner --min-age 14 --live
python -m nima_core.memory_pruner --restore 12345  # undo within 30 days
```

### 群体思维
支持多代理之间的记忆共享：
```python
from nima_core import HiveMind
hive = HiveMind(db_path="~/.nima/memory/ladybug.lbug")
context = hive.build_agent_context("research task", max_memories=8)
hive.capture_agent_result("agent-1", "result summary", "model-name")
```

### 预知能力
通过分析时间模式来实现记忆的预加载：
```python
from nima_core import NimaPrecognition
precog = NimaPrecognition(db_path="~/.nima/memory/ladybug.lbug")
precog.run_mining_cycle()
```

### 清晰时刻
情感共鸣的记忆会自发浮现（具备安全机制：过滤创伤性记忆，限定使用时间，每日使用次数有限）：
```python
from nima_core import LucidMoments
lucid = LucidMoments(db_path="~/.nima/memory/ladybug.lbug")
moment = lucid.surface_moment()
```

### 情感系统
基于Panksepp模型的七种情感状态及人格特征：
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
- **v3.0.2**（2026年2月22日）：修复ClawHub包中缺失的认知相关文件和钩子问题 |
- **v3.0.0**（2026年2月22日）：版本信息统一，包内容审核 |
- **v2.5.0**（2026年2月21日）：新增群体思维和预知功能 |
- **v2.4.0**（2026年2月20日）：改进梦境整合机制 |
- **v2.3.0**（2026年2月19日）：优化记忆筛选器，支持Ollama模型 |
- **v2.2.0**（2026年2月19日）：增强情感分析功能，改进噪声过滤机制 |
- **v2.0.0**（2026年2月13日）：采用LadybugDB作为数据库后端，加强安全性，通过348项测试验证系统稳定性 |

## 许可证

MIT许可证 — 适用于所有AI代理，无论是商业用途还是个人使用。