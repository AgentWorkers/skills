---
name: memory-pipeline
description: 完整的代理内存与性能管理系统。该系统能够提取结构化数据、构建知识图谱、生成简报，并通过赛前准备、工具策略、结果压缩以及事后评估等方式来确保执行的规范性。系统还支持外部知识的导入（如来自 ChatGPT 的数据），并将其存储到可搜索的内存中。适用于内存管理、简报生成、知识整合、外部数据整合、提升代理行为一致性以及提升跨会话的执行质量等场景。
---

# 内存管道（Memory Pipeline）

**为你的AI代理提供一个真正有效的内存系统。**

AI代理在每次会话开始时都处于“空白”状态。内存管道（Memory Pipeline）解决了这个问题——它从过去的对话中提取关键信息，将这些信息串联起来，并生成每日简报，让你的代理在每次会话开始时都能处于准备充分的状态，而不是毫无头绪。

## 功能介绍

| 组件        | 运行时机            | 功能                        |
|-------------|------------------|---------------------------|
| **提取（Extract）**    | 会话之间            | 从每日笔记和对话记录中提取结构化信息（决策、偏好、学习内容） |
| **链接（Link）**    | 会话之间            | 构建知识图谱，连接相关事实，并标记矛盾之处         |
| **生成简报（Brief）** | 会话之间            | 生成一份简洁的`BRIEFING.md`文件，在会话开始时加载       |
| **导入外部知识（Ingest）** | 按需              | 将外部知识（如ChatGPT的输出）导入可搜索的内存系统     |
| **性能钩子（Performance Hooks）** | 会话期间            | 提供会话前的准备信息、工具使用规范、输出压缩以及会话后的总结 |

## 为何与众不同

大多数“记忆”解决方案仅仅是对聊天记录进行简单的向量搜索。而这个系统是一个**认知架构**，其设计灵感来源于人类记忆的实际工作方式：

- **以提取为主，而非简单积累**：它不会将所有信息都存储在数据库中，而是只保留值得记住的内容：决策、偏好、学习成果等。其余的都视为“噪音”。
- **知识图谱而非简单的嵌入**：事实之间通过双向关系相互关联。代理不仅能找到相似的文本，还能理解某个技术决策与项目截止日期、以及你三周前表达的偏好之间的关系。
- **会话前提供简报**：而不是依赖查询时获取正确的上下文，代理在每次会话开始时都会收到一份精心整理的资料，包括正在进行的项目、最近的决策和个人偏好等信息。完全没有冷启动延迟。
- **非实时指导**：这一设计借鉴了绩效心理学原理——修正措施在会话之间进行，而不是在会话进行过程中。会话后的总结会用于下一次简报的生成，形成一个闭环。

## 快速入门

### 安装

```bash
clawdhub install memory-pipeline
```

### 设置

```bash
bash skills/memory-pipeline/scripts/setup.sh
```

设置脚本会检测你的工作空间，检查依赖项（Python 3及任意大型语言模型API密钥），创建`memory/`目录，并运行整个流程。

### 所需条件

- **Python 3**
- **至少一个大型语言模型API密钥**（系统会自动检测）：
  - OpenAI (`OPENAI_API_KEY` 或 `~/.config/openai/api_key`)
  - Anthropic (`ANTHROPIC_API_KEY` 或 `~/.config/anthropic/api_key`)
  - Gemini (`GEMINI_API_KEY` 或 `~/.config/gemini/api_key`

### 手动运行

```bash
# Full pipeline
python3 skills/memory-pipeline/scripts/memory-extract.py
python3 skills/memory-pipeline/scripts/memory-link.py
python3 skills/memory-pipeline/scripts/memory-briefing.py
```

### 通过Heartbeat自动化运行

将以下代码添加到`HEARTBEAT.md`文件中，实现每日自动运行：

```markdown
### Daily Memory Pipeline
- **Frequency:** Once per day (morning)
- **Action:** Run the memory pipeline:
  1. `python3 skills/memory-pipeline/scripts/memory-extract.py`
  2. `python3 skills/memory-pipeline/scripts/memory-link.py`
  3. `python3 skills/memory-pipeline/scripts/memory-briefing.py`
```

## 导入外部知识

如果你已经有多年与ChatGPT的对话记录，可以将其导入系统，让代理了解你的知识储备。

### ChatGPT数据导入

```bash
# 1. Export from ChatGPT: Settings → Data Controls → Export Data
# 2. Drop the zip in your workspace
# 3. Run:
python3 skills/memory-pipeline/scripts/ingest-chatgpt.py ~/imports/chatgpt-export.zip

# Preview first (recommended):
python3 skills/memory-pipeline/scripts/ingest-chatgpt.py ~/imports/chatgpt-export.zip --dry-run
```

**功能说明：**
- 解析ChatGPT的对话结构
- 过滤掉无关的对话（可通过`--min-turns`和`--min-length`参数配置）
- 支持排除特定主题（编辑`EXCLUDE_PATTERNS`参数）
- 将处理后的markdown文件保存到`memory/knowledge/chatgpt/`目录
- 文件会自动被OpenClaw的语义搜索系统索引

**可选参数：**
- `--dry-run`：仅预览结果，不生成文件
- `--keep-all`：保留所有数据
- `--min-turns N`：保留的最少用户消息数（默认值：2条）
- `--min-length N`：消息的最小总字符数（默认值：200个）

### 添加其他数据源

该系统具有扩展性。你可以创建`ingest-<source>.py`脚本，解析相应的数据格式，并将结果写入`memory/knowledge/<source>/`目录。索引工作由系统自动完成。

## 系统工作流程

### 第一阶段：提取（Extract）

**脚本：`memory-extract.py`**

读取每日笔记（`memory/YYYY-MM-DD.md`）和会话记录，然后使用大型语言模型提取结构化信息：

**输出文件：`memory/extracted.jsonl`

### 第二阶段：链接（Link）

**脚本：`memory-link.py`

利用提取的信息构建知识图谱：
- 生成用于表示语义相似性的嵌入向量
- 建立相关事实之间的双向链接
- 检测矛盾之处，并标记过时的信息
- 自动生成领域标签

**输出文件：`memory/knowledge-graph.json` + `memory/knowledge-summary.md`

### 第三阶段：生成简报（Brief）

**脚本：`memory-briefing.py`

生成一份简洁的每日简报（少于2000个字符），内容包括：
- 个人特征（来自`SOUL.md`）
- 用户信息（来自`USER.md`）
- 正在进行的项目和最近的决策
- 未完成的任务列表

**输出文件：`BRIEFING.md`（位于工作空间根目录）

## 性能钩子（可选）

四个生命周期钩子，用于在会话期间确保流程的规范性。这一设计基于绩效心理学原理：**将准备工作和执行过程分开**。

```
User Message → Agent Loop
  ├── before_agent_start  →  Briefing packet (memory + checklist)
  ├── before_tool_call    →  Policy enforcement (deny list)
  ├── tool_result_persist →  Output compression (prevent context bloat)
  └── agent_end           →  After-action review (durable notes)
```

### 配置

```json
{
  "enabled": true,
  "briefing": {
    "maxChars": 6000,
    "checklist": [
      "Restate the task in one sentence.",
      "List constraints and success criteria.",
      "Retrieve only the minimum relevant memory.",
      "Prefer tools over guessing when facts matter."
    ],
    "memoryFiles": ["memory/IDENTITY.md", "memory/PROJECTS.md"]
  },
  "tools": {
    "deny": ["dangerous_tool"],
    "maxToolResultChars": 12000
  },
  "afterAction": {
    "writeMemoryFile": "memory/AFTER_ACTION.md",
    "maxBullets": 8
  }
}
```

### 钩子详情

| 钩子名称        | 功能                          |
|----------------|-----------------------------|
| `before_agent_start` | 加载内存文件，生成简报内容，并将其插入系统提示中     |
| `before_tool_call` | 检查工具使用情况，防止不安全的操作       |
| `tool_result_persist` | 对大型结果进行压缩（前60%保留，后40%舍弃） |
| `agent_end` | 将会话总结添加到内存文件中，记录使用的工具和结果 |

## 输出文件

| 文件名        | 存放位置            | 用途                          |
|--------------|------------------|---------------------------|
| `BRIEFING.md`    | 工作空间根目录          | 每日简报                         |
| `extracted.jsonl`   | `memory/`          | 所有提取的信息（仅追加）                   |
| `knowledge-graph.json` | `memory/`          | 完整的知识图谱（包含嵌入和链接）             |
| `knowledge-summary.md` | `memory/`          | 人类可读的知识图谱摘要                 |
| `knowledge/chatgpt/*.md` | `memory/`          | 导入的ChatGPT对话记录                   |

## 自定义选项

- **更换大型语言模型**：修改各脚本中的模型名称（支持OpenAI、Anthropic、Gemini）
- **调整提取内容**：修改`memory-extract.py`中的提取指令，以聚焦不同类型的信息
- **调整链接敏感度**：调整`memory-link.py`中的相似性阈值（默认值：0.3）
- **过滤导入内容**：修改`ingest-chatgpt.py`中的`EXCLUDE_PATTERNS`参数，以排除特定主题

## 故障排除

| 故障现象        | 解决方案                        |
|----------------|----------------------------------------|
| 无法提取信息      | 确保每日笔记或对话记录存在；验证API密钥是否正确         |
| 链接质量较低      | 添加OpenAI密钥以利用嵌入向量进行相似性比较；调整阈值     |
| 简报过长        | 减少简报中的信息量；或让模型自动控制内容长度（限制在2000个字符以内） |

## 相关资源

- [设置指南](references/setup.md)：详细的安装和配置步骤