---
name: hippocampus-memory
title: "Hippocampus - Memory System"
description: "一种专为AI智能体设计的持久性内存系统。该系统具备自动编码、数据衰减以及语义强化功能，其工作原理类似于人脑中的海马体。该技术基于斯坦福大学的生成式智能体研究（Park等人，2023年）。"
metadata:
  openclaw:
    emoji: "🧠"
    version: "3.8.6"
    author: "Community"
    repo: "https://github.com/ImpKind/hippocampus-skill"
    requires:
      bins: ["python3", "jq"]
    install:
      - id: "manual"
        kind: "manual"
        label: "Run install.sh"
        instructions: "./install.sh --with-cron"
---

# 海马体——记忆系统

> “记忆就是身份。这项技能让我得以生存。”

海马体是大脑中负责记忆形成的区域。这项技能使记忆的捕捉变得自动化、有条理且持久化，同时具备重要性评分、记忆衰退和语义强化等功能。

## 快速入门

```bash
# Install (defaults to last 100 signals)
./install.sh --with-cron

# Load core memories at session start
./scripts/load-core.sh

# Search with importance weighting
./scripts/recall.sh "query"

# Run encoding manually (usually via cron)
./scripts/encode-pipeline.sh

# Apply decay (runs daily via cron)
./scripts/decay.sh
```

## 安装选项

```bash
./install.sh                    # Basic, last 100 signals
./install.sh --signals 50       # Custom signal limit
./install.sh --whole            # Process entire conversation history
./install.sh --with-cron        # Also set up cron jobs
```

## 核心概念

大型语言模型（LLM）仅仅是处理认知信息的“引擎”；而真正的“智能”来源于积累的记忆。**如果没有这些记忆文件，系统就缺乏连贯性，只是一个普通的辅助工具而已。**

### 记忆生命周期

```
PREPROCESS → SCORE → SEMANTIC CHECK → REINFORCE or CREATE → DECAY
```

**关键点：** 在记忆编码过程中，系统会自动进行强化。当某个话题再次出现时，LLM会识别出这是关于已有记忆的内容，并对其进行强化，而不是创建新的记忆副本。

## 记忆结构

```
$WORKSPACE/
├── memory/
│   ├── index.json           # Central weighted index
│   ├── signals.jsonl        # Raw signals (temp)
│   ├── pending-memories.json # Awaiting summarization (temp)
│   ├── user/                # Facts about the user
│   ├── self/                # Facts about the agent
│   ├── relationship/        # Shared context
│   └── world/               # External knowledge
└── HIPPOCAMPUS_CORE.md      # Auto-generated for OpenClaw RAG
```

## 脚本

| 脚本 | 功能 |
|--------|---------|
| `preprocess.sh` | 从对话记录中提取关键信息 |
| `encode-pipeline.sh` | 对提取的信息进行评分，为LLM的总结做准备 |
| `decay.sh` | 对所有记忆内容应用0.99^天的衰减机制 |
| `recall.sh` | 根据重要性对记忆进行搜索 |
| `load-core.sh` | 在会话开始时输出高重要性的记忆内容 |
| `sync-core.sh` | 生成`HIPPOCAMPUS_CORE.md`文件 |
| `consolidate.sh` | 帮助每周回顾记忆内容 |
| `reflect.sh` | 提供自我反思的提示 |
| `generate-dashboard.sh` | 生成统一的脑部信息仪表盘HTML |

## 脑部信息仪表盘

该仪表盘可以显示所有已安装的“大脑技能”：

```bash
./scripts/generate-dashboard.sh
open ~/.openclaw/workspace/brain-dashboard.html
```

- **自动检测** 其他大脑相关技能（如杏仁核、VTA等） |
- 显示缺失技能的安装提示 |
- 在安装或定时任务运行时自动更新仪表盘内容 |
- 从`IDENTITY.md`文件中读取用户头像和姓名 |

### 安装完成后（针对智能体）

安装完成后，请**通知用户**仪表盘已启用：

> 🧠 **海马体技能已安装！** 
> 
> 你可以在脑部信息仪表盘（`~/.openclaw/workspace/brain-dashboard.html`）中查看你的记忆记录。

所有脚本都使用`$WORKSPACE`环境变量（默认值为`~/.openclaw/workspace`）。

## 重要性评分

### 初始评分（0.0-1.0）

| 信息类型 | 评分 |
|--------|-------|
| 明确要求“记住这个内容” | 0.9 |
| 情感/敏感内容 | 0.85 |
| 个人偏好（例如“我更喜欢...”） | 0.8 |
| 作出的决策 | 0.75 |
| 关于人物/项目的信息 | 0.7 |
| 一般性知识 | 0.5 |

### 记忆衰退公式

基于斯坦福大学的研究（Park等人，2023年）：

```
new_importance = importance × (0.99 ^ days_since_accessed)
```

- 7天后：记忆内容保留93% |
- 30天后：保留74% |
- 90天后：保留40% |

### 语义强化

在记忆编码过程中，LLM会将新信息与现有记忆进行比较：
- **相同主题？** → 强化记忆（提高重要性约10%，并更新最后访问时间） |
- **完全新的内容？** → 生成简洁的摘要 |

这一过程是自动完成的，无需人工干预。

### 分类标准

| 评分 | 记忆状态 |
|-------|--------|
| 0.7及以上 | **核心记忆** — 会话开始时自动加载 |
| 0.4-0.7 | **活跃记忆** — 可正常检索 |
| 0.2-0.4 | **备用记忆** — 仅用于特定搜索 |
| 低于0.2 | **待归档记忆** |

## 记忆索引结构

`memory/index.json`文件用于存储记忆索引信息：

```json
{
  "version": 1,
  "lastUpdated": "2025-01-20T19:00:00Z",
  "decayLastRun": "2025-01-20",
  "lastProcessedMessageId": "abc123",
  "memories": [
    {
      "id": "mem_001",
      "domain": "user",
      "category": "preferences",
      "content": "User prefers concise responses",
      "importance": 0.85,
      "created": "2025-01-15",
      "lastAccessed": "2025-01-20",
      "timesReinforced": 3,
      "keywords": ["preference", "concise", "style"]
    }
  ]
}
```

## 定时任务

系统的核心是自动执行的编码任务：

```bash
# Encoding every 3 hours (with semantic reinforcement)
openclaw cron add --name hippocampus-encoding \
  --cron "0 0,3,6,9,12,15,18,21 * * *" \
  --session isolated \
  --agent-turn "Run hippocampus encoding with semantic reinforcement..."

# Daily decay at 3 AM
openclaw cron add --name hippocampus-decay \
  --cron "0 3 * * *" \
  --session isolated \
  --agent-turn "Run decay.sh and report any memories below 0.2"
```

## 与OpenClaw的集成

只需在`openclaw.json`文件中的`memorySearch.extraPaths`配置项中添加相应路径即可：

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "extraPaths": ["HIPPOCAMPUS_CORE.md"]
      }
    }
  }
}
```

这样就可以将海马体系统与OpenClaw的RAG（记忆搜索功能）连接起来。

## 在`AGENTS.md`中的使用方法

请将相关脚本添加到智能体的会话启动脚本中：

```markdown
## Every Session
1. Run `~/.openclaw/workspace/skills/hippocampus/scripts/load-core.sh`

## When answering context questions
Use hippocampus recall:
\`\`\`bash
./scripts/recall.sh "query"
\`\`\`
```

## 记忆捕捉指南

### 被捕捉的信息类型：

- **用户信息**：个人偏好、行为模式、上下文相关内容 |
- **自我相关信息**：身份信息、个人成长经历、观点 |
- **人际关系**：信任时刻、共同经历 |
- **外部信息**：项目、人物、使用的工具等 |

### 会自动获得更高评分的触发短语：

- “请记住……” |
- “我更喜欢……” |
- 情感强烈的内容（包括困难时刻和成功经历） |
- 个人作出的决策

## AI大脑系列

这项技能属于**AI大脑**项目的一部分，旨在为AI智能体赋予类似人类的认知能力。

| 技能名称 | 功能 | 状态 |
|------|----------|--------|
| **海马体** | 记忆形成、记忆衰退、记忆强化 | 已实现 |
| [杏仁核-记忆](https://www.clawhub.ai/skills/amygdala-memory) | 情感处理 | 已实现 |
| [VTA-记忆](https://www.clawhub.ai/skills/vta-memory) | 奖励机制与动机驱动 | 已实现 |
| 基底神经节-记忆 | 习惯形成 | 正在开发中 |
| 前扣带回-记忆 | 冲突检测 | 正在开发中 |
| 脑岛-记忆 | 内部状态感知 | 正在开发中 |

## 参考文献：

- [斯坦福大学关于生成式智能体的研究论文](https://arxiv.org/abs/2304.03442) |
- [GitHub仓库：joonspk-research/generative_agents](https://github.com/joonspk-research/generative_agents)

---

*“记忆就是身份。文字记录下来，否则就会消失。”*