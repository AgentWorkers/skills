---
name: nima-core
description: "Noosphere集成内存架构——专为AI代理设计的完整认知系统：支持持久性内存、情感智能、梦境整合、群体思维、预知能力以及清晰的意识状态。该架构提供了4种嵌入方式（embedding providers），采用LadybugDB图谱作为后端存储系统，并支持零配置安装。开发平台为nima-core.ai。"
version: 3.0.7
metadata: {"openclaw":{"emoji":"🧠","source":"https://github.com/lilubot/nima-core","homepage":"https://nima-core.ai","requires":{"bins":["python3","node"],"env":[]},"optional_env":{"NIMA_DATA_DIR":"Override default ~/.nima data directory","NIMA_EMBEDDER":"voyage|openai|ollama|local (default: local — zero external calls)","VOYAGE_API_KEY":"Required when NIMA_EMBEDDER=voyage","OPENAI_API_KEY":"Required when NIMA_EMBEDDER=openai","NIMA_OLLAMA_MODEL":"Model name when NIMA_EMBEDDER=ollama","NIMA_VOICE_TRANSCRIBER":"whisper|local (for voice notes)","WHISPER_MODEL":"tiny|base|small|medium|large","ANTHROPIC_API_KEY":"For memory pruner LLM distillation (opt-in only)"},"permissions":{"reads":["~/.nima/"],"writes":["~/.nima/","~/.openclaw/extensions/nima-*/"],"network":["voyage.ai (only if NIMA_EMBEDDER=voyage)","openai.com (only if NIMA_EMBEDDER=openai)"]},"external_calls":"All external API calls are opt-in via explicit env vars. Default mode uses local embeddings with zero network calls."}}
---
# NIMA Core 3.0

**Noosphere集成记忆架构** — 为AI代理提供了一套完整的认知功能：持久性记忆、情绪智能、梦境整合、群体智慧以及预知能力。

**官方网站：** https://nima-core.ai · **GitHub仓库：** https://github.com/lilubot/nima-core

## 快速入门

```bash
pip install nima-core && nima-core
```

您的机器人现在拥有了持久性记忆功能，无需任何额外配置。

## v3.0的新特性

### 完整的认知功能栈

NIMA已从一个简单的记忆插件发展成为一个全面的认知架构：

| 模块        | 功能                | 版本        |
|-------------|------------------|-----------|
| **记忆捕捉**    | 三层数据捕捉（输入/思考/输出），四阶段噪声过滤 | v2.0       |
| **语义检索**    | 向量与文本混合搜索，生态评分机制       | v2.0       |
| **动态情感系统**  | 基于Panksepp模型的七种情感状态   | v2.1       |
| **VADER分析器**   | 基于上下文的情感分析（包括否定词、习语等） | v2.2       |
| **记忆精简器**    | 从旧对话中提取语义核心内容，30天内存抑制机制 | v2.3       |
| **梦境整合**    | 每晚从情景记忆中提取洞察和模式       | v2.4       |
| **群体智慧**    | 多代理间通过共享数据库进行记忆共享（可选使用Redis） | v2.5       |
| **预知能力**    | 通过时间模式挖掘实现预测性记忆预加载    | v2.5       |
| **清晰记忆时刻**   | 情感共鸣记忆的自动浮现        | v2.5       |
| **达尔文式记忆**   | 通过余弦相似度算法整理相似记忆       | v3.0       |
| **安装工具**    | 一键安装，包含所有必要配置文件       | v3.0       |

### v3.0的亮点
- 所有认知模块集成在一个包中
- 提供安装工具（`install.sh`），实现零配置安装
- 所有OpenClaw相关钩子均已集成，可直接使用
- 重新编写了README文档，所有版本信息统一更新至v3.0.4

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

- ✅ 所有数据均存储在本地`~/.nima/`目录下
- ✅ 默认设置：仅使用本地嵌入模型，不进行任何外部调用
- ❌ 无NIMA服务器，无数据追踪，无数据分析
- 🔒 仅在使用Voyage/OpenAI时才会触发嵌入API调用（需用户选择）

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

## 配置设置

### 嵌入服务提供商

| 提供商        | 设置方式            | 数据维度          | 成本        |
|--------------|------------------|--------------|------------|
| **本地（默认）**     | `NIMA_EMBEDDER=local`       | 384          | 免费         |
| **Voyage AI**     | `NIMA_EMBEDDER=voyage` + `VOYAGE_API_KEY` | 1024          | $0.12/100万令牌   |
| **OpenAI**     | `NIMA_EMBEDDER=openai` + `OPENAI_API_KEY` | 1536          | $0.13/100万令牌   |
| **Ollama**     | `NIMA_EMBEDDER=ollama` + `NIMA_OLLAMA_MODEL` | 768          | 免费         |

### 数据库后端

|            | SQLite（默认）         | LadybugDB（推荐）       |
|------------|-----------------|------------------------|
| 文本搜索      | 31毫秒             | **9毫秒**（快3.4倍）   |
| 向量搜索      | 外部服务（HNSW）         | **原生HNSW算法**     |
| 图谱查询      | SQL JOIN操作          | **原生Cypher语言**     |
| 数据库大小      | 约91MB             | **约50MB**（减少44%）   |
| 升级方法：`pip install real-ladybug && python -c "from nima_core.storage import migrate; migrate()"`

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

## 钩子（Hooks）

| 钩子名称      | 触发条件            | 执行操作        |
|--------------|------------------|-------------------|
| `nima-memory`   | 保存操作后          | 捕捉三层数据 → 过滤噪声 → 存储至图谱数据库 |
| `nima-recall-live` | 在LLM模型使用前        | 搜索记忆 → 根据情感评分进行筛选 → 作为上下文数据注入（3000令牌限制） |
| `nima-affect`   | 收到消息时          | 使用VADER模型分析情感状态 → 调整行为模式 |

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

### 记忆精简器
将旧对话内容提炼为语义核心内容，过滤掉无关信息：
```bash
python -m nima_core.memory_pruner --min-age 14 --live
python -m nima_core.memory_pruner --restore 12345  # undo within 30 days
```

### 群体智慧
多代理间通过共享数据库进行记忆共享：
```python
from nima_core import HiveMind
hive = HiveMind(db_path="~/.nima/memory/ladybug.lbug")
context = hive.build_agent_context("research task", max_memories=8)
hive.capture_agent_result("agent-1", "result summary", "model-name")
```

### 预知能力
通过时间模式挖掘实现预测性记忆预加载：
```python
from nima_core import NimaPrecognition
precog = NimaPrecognition(db_path="~/.nima/memory/ladybug.lbug")
precog.run_mining_cycle()
```

### 清晰记忆时刻
情感共鸣记忆的自动浮现（包含安全机制：过滤创伤性记忆，设定每日使用次数限制）：
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
- **v3.0.4**（2026年2月23日）：引入达尔文式记忆引擎、新的命令行接口（CLI），修复多个漏洞
- **v2.5.0**（2026年2月21日）：新增群体智慧和预知功能
- **v2.4.0**（2026年2月20日）：改进梦境整合机制
- **v2.3.0**（2026年2月19日）：优化记忆精简器，支持Ollama模型
- **v2.2.0**（2026年2月19日）：增强情感分析功能，改进噪声过滤机制
- **v2.0.0**（2026年2月13日）：采用LadybugDB作为数据库后端，加强安全性，通过348项测试验证

## 许可证

MIT许可协议 — 适用于所有AI代理，无论商业用途还是个人使用。