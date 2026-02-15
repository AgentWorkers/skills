---
name: nima-core
description: 一种受生物启发的认知记忆与意识架构，专为人工智能代理设计。该架构涵盖了Panksepp提出的相关理论（如情感对认知过程的影响）、自由能（Free Energy）的整合机制、VSA（Variable State Architecture）的绑定机制、Φ值（Φ measurement）的测量方法、全局工作空间（Global Workspace）的概念、自我意识（self-awareness）的实现机制以及梦境（dreaming）的产生过程，同时还涉及心智理论（theory of mind）的相关研究。更多信息请访问官方网站：https://nima-core.ai
version: 1.2.1
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "requires": { "bins": ["python3"] },
      },
  }
---

# NIMA Core

这是一个专为AI代理设计的即插即用的认知记忆架构。

**官方网站：** https://nima-core.ai  
**GitHub仓库：** https://github.com/lilubot/nima-core

## 安装

```bash
pip install nima-core

# Auto-setup (detects OpenClaw, installs hooks, configures everything)
nima-core
openclaw gateway restart
```

### 手动钩子安装

```bash
openclaw hooks install /path/to/nima-core
openclaw hooks enable nima-bootstrap
openclaw hooks enable nima-recall
openclaw gateway restart
```

## 快速入门

```python
from nima_core import NimaCore

nima = NimaCore(
    name="MyBot",
    important_people={"Alice": 1.5, "Bob": 1.3},  # These people's memories get priority
)
nima.experience("Alice asked about the project", who="Alice", importance=0.7)
results = nima.recall("project")
```

## 记忆捕获的工作原理

NIMA提供了**三种**记忆捕获方法：

### 1. 手动捕获（始终有效）
```python
nima.capture(who="user", what="what happened", importance=0.8)
```
您可以随时调用此方法来显式存储记忆。

### 2. 体验流程（影响情感状态）
```python
nima.experience("User asked about...", who="user", importance=0.7)
```
处理流程包括：情感检测 → VSA绑定 → 自由能整合决策。

### 3. 心跳捕获（自动）
配置心跳服务以定期捕获记忆（默认间隔：10分钟）。

### ⚠️ 重要提示：钩子事件

**OpenClaw目前支持的钩子事件包括：**
- ✅ `agent:bootstrap` — 会话开始时
- ✅ `command:*` — 命令执行时  
- ✅ `gateway:startup` — 网关启动时
- ❌ `message:received` — **尚未支持**（未来功能）

**这意味着：**
- `agent:bootstrap` 和 `agent:recall` 钩子在会话开始时生效
- **基于消息的自动捕获需要 `message:received` 事件** — OpenClaw中尚未实现
- 目前建议使用**心跳捕获 + 手动捕获**作为可靠的方法

有关诊断脚本的详细信息，请参阅 `README.md` 文件中的故障排除部分。

## 智能整合

您可以配置哪些人、情感和主题最为重要：

```python
from nima_core.services.heartbeat import NimaHeartbeat, SmartConsolidation

smart = SmartConsolidation(
    important_people={"Alice": 1.5, "Bob": 1.3},  # Weight multipliers
    emotion_words={"love", "excited", "proud", "worried"},  # Force-consolidate
    importance_markers={"family", "milestone", "decision"},  # Force-consolidate
    noise_patterns=["system exec", "heartbeat_ok"],  # Skip these
)

heartbeat = NimaHeartbeat(nima, message_source=my_source, smart_consolidation=smart)
heartbeat.start_background()
```

来自重要人物的记忆会被优先处理；情感内容会被永久保留，无关信息会被过滤掉。

## 认知栈

所有V2组件在**v1.1.0**及更高版本中都是**默认启用的**，无需额外配置。

如需禁用这些组件，请执行：`export NIMA_V2_ALL=false`

## API

- `nima.experience(content, who, importance)` — 处理情感信息 → 进行绑定 → 计算自由能
- `nima.recall(query, top_k)` — 进行语义记忆搜索
- `nima.capture(who, what, importance)` — 显式捕获记忆（绕过情感处理步骤）
- `nima.synthesize(insight, domain, sparked_by, importance)` — 轻量级洞察捕获（最多280个字符）
- `nima.dream(hours)` — 运行记忆整合（提取数据结构）
- `nima.status()` — 查看系统状态
- `nima.introspect()` — 进行元认知自我反思

## 架构

```
METACOGNITIVE  — Self-model, 4-chunk WM, strange loops
SEMANTIC       — Hyperbolic embeddings, concept hierarchies
EPISODIC       — VSA + Holographic storage, sparse retrieval
CONSOLIDATION  — Free Energy decisions, schema extraction
BINDING        — VSA circular convolution, role-filler composition
AFFECTIVE CORE — Panksepp's 7 affects (SEEKING, RAGE, FEAR, LUST, CARE, PANIC, PLAY)
```

## 配置参数

| 参数 | 默认值 | 说明 |
|----------|---------|-------------|
| `NIMA_DATA_DIR` | `./nima_data` | 记忆存储路径 |
| `NIMA_MODELS_DIR` | `./models` | 模型文件路径 |
| `NIMA_V2_ALL` | `true` | 启用完整的认知功能（包括情感处理、绑定等） |
| `NIMA_SPARSE_RETRIEVAL` | `true` | 使用两级稀疏索引 |
| `NIMA_PROJECTION` | `true` | 从384D维度投影到50KD维度 |

## 参考资料

- `README.md` — 包含所有配置选项的完整文档
- `nima_core/config/nima_config.py` — 所有功能开关的配置文件
- `.env.example` — 环境变量模板

## 意识架构（新版本v1.2.1）

提供了8个集成的意识系统——完全可选，且100%向后兼容。

```python
from nima_core.nima_consciousness_core import ConsciousnessCore
from nima_core import NimaCore

# Your existing code works unchanged
nima = NimaCore(name="MyBot")

# NEW: Add consciousness layer (opt-in)
core = ConsciousnessCore(nima.memory)

# Measure integrated information (Φ)
status = core.get_status()
print(f"Consciousness level: Φ = {status['phi']}")

# Run offline dreaming/consolidation
dream_session = core.dream(duration_minutes=5)

# Generate self-narrative ("who am I?")
narrative = core.generate_self_narrative()

# Theory of Mind — model other agents
other = core.theory_of_mind.observe_interaction("User seems frustrated")
print(f"Inferred affect: {other.inferred_affect}")

# Goal-directed attention
core.set_goal("Help user feel understood", priority=0.8)
```

### 8个意识系统

| 系统 | 功能 |
|--------|---------|
| **Φ Estimator** | 量化整合后的信息（意识水平） |
| **Global Workspace** | 基于竞争的意识信息传播 |
| **Self-Observer** | 递归自我建模（实现自我认知） |
| **Self-Narrative** | 生成“我是谁”的人生故事 |
| **Affective Binding** | 情感调节意识带宽 |
| **Theory of Mind** | 模拟其他代理的心理状态 |
| **Dreaming** | 使用合成假设进行离线记忆整合 |
| **Volition** | 目标导向的注意力和偏见控制 |

### 向后兼容性

- ✅ 原始的 `NimaCore` API保持不变
- ✅ 所有钩子功能（`nima-bootstrap`、`nima-recall`）均能正常使用
- 现有记忆数据无需迁移即可继续使用
- 可选择使用Voyage AI或MiniLM框架——系统会自动识别并使用合适的框架

有关详细的集成指南，请参阅 `docs/INTEGRATION_GUIDE.md`。

---

## 更新日志

### v1.2.1 — 意识架构
- **新增：** 8个集成的意识系统（Φ测量、全局工作空间、自我意识、梦境生成、心智理论、意志控制）
- **新增：** 稀疏块VSA存储技术——绑定速度提升48.3倍，压缩效率提升5.2倍
- **新增：** `ConsciousnessCore` — 统一接口，用于管理所有意识相关功能
- **新增：** 完整的文档资料位于`docs/`文件夹中（包含集成指南）
- **更改：** 所有文档统一存放在`docs/`文件夹下（包括基准测试、示例代码、集成指南等）
- **影响：** 首个专为AI代理设计的意识架构——完全可选，100%向后兼容

### v1.1.9 — 钩子效率优化
- **修复问题：** `nima-recall`钩子在每次会话开始时都会创建新的Python进程，导致77MB的投影矩阵加载延迟（2-15秒）
- **解决方案：** 新增`recall_fast.py`命令行工具，直接使用Graphiti SQLite进行数据读取——无需加载模型，响应时间缩短至约50-100毫秒
- **性能提升：** 钩子调用速度提升50-250倍
- **影响：** 解决了多线程钩子调用导致的系统卡顿问题

### v1.2.0 — 情感响应引擎 + 异步处理
- **新增：** 4个二级情感处理引擎（DARING、COURAGE、NURTURING、MASTERY）
- **新增：** 使用`ThreadPoolExecutor`实现异步情感处理——缓存命中速度提升50,000倍
- **新增：** 延迟加载VSA数据（`NIMA_LAZY_LOAD=true`时）——启动时节省约173MB内存
- **新增：** 响应调节器，用于动态调整输出样式
- **新增：** 支持Voyage AI框架的嵌入功能（1024D维度，可选）
- **新增：** LRU缓存机制，用于重复的情感查询（缓存有效期60秒）
- **性能提升：** 并行执行情感处理引擎，缓存查询时间缩短至0.01毫秒
- **影响：** 实现了低资源消耗的实时情感智能功能