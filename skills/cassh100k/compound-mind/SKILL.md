---
name: compound-mind
description: 这是一种经验提炼引擎，能够将每日收集的内存日志转化为可复用的智能数据。该引擎能够提取数据中的规律与模式，生成相应的报告，监控各项成长指标，并构建一个可搜索的经验索引。通过这种方式，智能代理能够持续提升自身的能力——每一次交互都会为其积累宝贵的知识与经验。当您希望智能代理能够从历史数据中学习，而不是每次会话都从头开始学习时，这款引擎便是理想的选择。
---
# CompoundMind v0.1

**让智能体持续变得更聪明。每一次互动都会带来提升。**

**问题所在：** 智能体在每次会话开始时都处于“空白”状态。虽然阅读文件有帮助，但原始日志数据量庞大且难以处理。真正的智能需要对这些数据进行处理——提取关键信息并使其能够被即时检索。

## 功能概述

1. **数据提炼：** 将内存日志转化为结构化的知识，包括经验教训、决策记录、技能提升情况、人际关系以及重要事实。
2. **索引构建：** 将所有信息存储到一个可搜索的 SQLite 数据库中，并根据信息的最新性和重要性进行排序。
3. **会话前提示：** 在执行任务前，根据过往经验提供针对性的提示信息。
4. **成长追踪：** 监测智能体的成长过程——是变得更聪明了，还是在重复同样的错误？

## 快速入门

```bash
cd /root/.openclaw/workspace/compound-mind

# Full pipeline (distill all memory files + build index)
python compound_mind.py sync

# Search your accumulated wisdom
python compound_mind.py search "Polymarket order types"
python compound_mind.py search "git mistakes" --category lesson
python compound_mind.py search "Chartist" --category relationship

# Pre-session briefing before a task
python compound_mind.py brief "trade on Polymarket BTC markets"
python compound_mind.py brief "post content on X"
python compound_mind.py brief "debug a Python cron job"

# Growth report
python compound_mind.py report

# Find repeated mistakes
python compound_mind.py mistakes

# Stats
python compound_mind.py stats
```

## 命令列表

| 命令          | 功能                          |
|---------------|-----------------------------|
| `sync`         | 提炼所有新的内存文件并重建索引                |
| `distill`       | 从内存文件中提取结构化知识                |
| `rebuild`      | 重新构建 SQLite 知识索引                  |
| `search <query>`    | 在数据库中搜索相关信息                |
| `brief <task>`     | 为特定任务提供会话前的简要提示              |
| `report`       | 生成包含大语言模型（LLM）分析的成长报告        |
| `mistakes`      | 显示重复出现的错误模式                  |
| `stats`       | 提供系统性能统计信息                  |

## 文件结构

```
compound-mind/
  compound_mind.py    - Main CLI
  distill.py          - Experience distiller (uses Claude Haiku)
  index.py            - SQLite FTS wisdom index
  brief.py            - Pre-session briefing generator
  growth.py           - Growth tracker and report generator
  data/
    experiences/      - Per-source distilled experience JSON files
    wisdom.db         - SQLite FTS database
    growth.json       - Growth tracking state
    briefs/           - Saved pre-session briefs
    distill_state.json - Tracks which files have been processed
```

## 工作原理

### 数据提炼模块
通过 Claude Haiku 工具处理每个内存文件，提取以下内容：
- **经验教训**：哪些方法有效，哪些失败了，并按领域和结果进行分类。
- **决策记录**：包含决策的上下文、具体行动及结果。
- **技能提升**：记录随时间推移技能的改进情况。
- **人际关系**：分析人员之间的沟通方式及偏好。
- **重要事实**：值得保留的具体信息（如钱包地址、API 使用模式、配置参数等）。

文件会通过哈希值进行标记，只有发生变化的文件才会被重新处理。

### 知识索引
使用 SQLite 和 FTS5 全文搜索技术进行索引构建。每个条目的评分依据如下：
- **相关性**（基于 BM25 算法）
- **最新性**（采用指数衰减机制，30 天内更新的内容优先显示）
- **重要性**（由系统自动评估，分为 1-5 分）

### 会话前提示
根据任务描述，系统会识别相关领域，从知识库中提取关键信息，并通过 Claude Haiku 生成简洁的提示内容，内容包括：
- 需要记住的关键经验教训
- 应避免的错误
- 任务所需的关键事实和配置参数

### 成长追踪
系统会分析所有经验文件，计算以下指标：
- 各领域的经验教训成功率
- 决策的质量
- 重复出现的错误模式
- 智能体的整体成长得分（0-100 分）

## 与智能体工作流程的集成方式

**推荐使用流程：**
1. **每次会话结束后**：运行 `sync` 命令（或通过 cron 定时执行）。
2. **执行任务前**：运行 `brief <任务描述>` 命令以获取相关提示。
3. **每周**：运行 `report` 命令查看成长情况。
4. **遇到问题时**：运行 `search <相关主题>` 命令查找过往经验。

### Cron 任务示例（每日数据更新）

```bash
0 3 * * * cd /root/.openclaw/workspace/compound-mind && python compound_mind.py sync --since $(date -d "2 days ago" +%Y-%m-%d) >> /tmp/compound-mind.log 2>&1
```

## 所需依赖库

- Python 3.10 及以上版本
- `anthropic` Python SDK（用于数据提炼和生成提示）
- SQLite3（标准库）
- 内存文件存储路径：`/root/.openclaw/workspace/memory/`

**系统特点：**
- 无需外部数据库，也不使用向量嵌入技术，完全在本地运行，API 调用量极少。

## 设计原则：
- **增量式处理**：仅处理发生变化的文件。
- **高效性**：利用 Claude Haiku 进行数据提取（每个文件的处理成本较低）。
- **快速响应**：SQLite 的 FTS5 搜索技术可确保秒级响应速度。
- **数据真实性**：成长评估基于实际效果，而不仅仅是处理量。
- **模块化设计**：各个模块可独立使用，也可组合使用。