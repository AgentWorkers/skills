---
name: memory-pipeline
description: 完整的代理内存与性能管理系统。该系统能够提取结构化数据、构建知识图谱、生成简报，并通过游戏前的准备工作、工具策略、结果压缩以及事后的回顾来确保执行流程的规范性。适用于需要处理内存管理、简报生成、知识整合、代理行为一致性或提升跨会话执行质量的任务。
---

# 内存管道与性能常规机制

这是一个为AI代理设计的完整内存与性能管理系统，包含两个子系统，封装在一个包中：

- **内存管道**（Python脚本）：用于提取事实数据、构建知识图谱并生成每日简报。
- **性能常规机制**（TypeScript钩子）：负责在会话前注入简报内容、规范工具使用、压缩输出结果以及进行事后回顾。

## 功能介绍

### 内存管道（会话间）

该系统分为三个阶段，帮助AI代理维护长期记忆：
1. **提取**：利用大语言模型（LLM）从每日笔记和会话记录中提取结构化信息（如决策、偏好、学习内容及承诺）。
2. **链接**：利用嵌入技术构建知识图谱，并在相关事实之间建立双向关联，同时识别矛盾之处。
3. **生成简报**：在会话开始时生成一个简洁的`BRIEFING.md`文件，其中包含代理的个性特征、当前项目、近期决策及关键背景信息。

### 性能常规机制（会话中）

该机制包含四个生命周期钩子，确保代理运行过程中的行为一致性：
1. **会话前准备**（`before_agent_start`）：从内存文件和检查清单中整理简报内容，并将其注入系统提示中。
2. **工具使用规范**（`before_tool_call`）：检查工具使用是否符合预设规则，防止不安全的操作。
3. **结果压缩**（`tool_result_persist`）：对工具输出结果进行压缩处理，以避免信息冗余。
4. **事后回顾**（`agent_end`）：记录会话中的关键事件、使用的工具及最终结果。

## 快速入门

### 安装

该技能包含三个Python脚本，位于`scripts/`目录下：
- `memory-extract.py`：用于提取事实数据。
- `memory-link.py`：用于构建知识图谱。
- `memory-briefing.py`：用于生成每日简报。

脚本会自动检测工作空间路径：
- 通过`CLAWDBOT_WORKSPACE`环境变量。
- 当前工作目录（如果包含`SOUL.md`或`AGENTS.md`文件）。
- 或者`~/.clawdbot/workspace`（默认路径）。

### 系统要求

**至少需要一个LLM API密钥**：
- OpenAI API密钥（用于GPT-4o-mini及嵌入功能）。
- Anthropic API密钥（用于Claude Haiku）。
- Gemini API密钥（用于Gemini Flash）。

可以通过环境变量或配置文件来设置API密钥：
```bash
# Environment variable
export OPENAI_API_KEY="sk-..."

# OR config file
echo "sk-..." > ~/.config/openai/api_key
```

脚本会自动选择可用的API密钥进行使用。

### 基本用法

- 运行整个流程：```bash
python3 scripts/memory-extract.py
python3 scripts/memory-link.py
python3 scripts/memory-briefing.py
```
- 或根据需要单独运行各个步骤。

## 流程阶段

### 第一阶段：提取事实

**脚本：`memory-extract.py`

优先从以下位置读取数据：
- 每日内存文件（`{workspace}/memory/YYYY-MM-DD.md`）：今天的或昨天的数据。
- 会话记录文件（`~/.clawdbot/agents/main/sessions/*.jsonl`）。

提取的结构化事实包括：
- **类型**：决策、偏好、学习内容、承诺等。
- **内容**：实际的信息。
- **主题**：根据上下文自动确定。
- **置信度**：0.0-1.0的可靠性评分。

**输出结果**：`{workspace}/memory/extracted.jsonl`——每行包含一条去重后的JSON格式事实。

### 第二阶段：构建知识图谱

**脚本：`memory-link.py`

- 使用提取的事实数据：
  - 生成嵌入向量（如果使用OpenAI API密钥）；否则使用关键词相似度算法。
  - 在相关事实之间建立双向链接。
  - 识别矛盾之处，并标记被替代的事实。
  - 自动从内容中生成领域标签。

**输出结果**：
  - `{workspace}/memory/knowledge-graph.json`：包含节点和链接的完整知识图谱。
  - `{workspace}/memory/knowledge-summary.md`：便于人类阅读的知识图谱摘要。

### 第三阶段：生成简报

**脚本：`memory-briefing.py`

- 生成一个简洁的每日简报，在会话开始时加载。

简报内容包含：
- 代理的个性特征（如果`SOUL.md`存在）。
- 用户背景信息（如果`USER.md`存在）。
- 最近的项目内容。
- 当前的待办事项（来自`todos*.md`文件）。

**输出结果**：`{workspace}/BRIEFING.md`——长度不超过2000个字符，可由LLM生成或基于模板生成。

## 集成到`HEARTBEAT.md`中

若要实现自动运行，请将以下内容添加到工作空间的`HEARTBEAT.md`文件中：
```markdown
# Heartbeat Tasks

## Daily (once per day, morning)
- Run memory extraction: `cd {workspace} && python3 skills/memory-pipeline/scripts/memory-extract.py`
- Build knowledge graph: `cd {workspace} && python3 skills/memory-pipeline/scripts/memory-link.py`
- Generate briefing: `cd {workspace} && python3 skills/memory-pipeline/scripts/memory-briefing.py`

## Weekly (Sunday evening)
- Review `memory/knowledge-summary.md` for insights
- Clean up old daily notes (optional)
```

## 加载`BRIEFING.md`

**重要提示**：`BRIEFING.md`需要在会话开始时作为工作空间上下文被加载。这需要OpenClaw的上下文加载功能（目前仍在开发中）。

配置代理，使其在每次会话开始时同时加载`BRIEFING.md`、`SOUL.md`和`AGENTS.md`。

## 输出文件

所有输出文件均保存在`{workspace}/memory/`目录下：
- `extracted.jsonl`：所有提取的事实数据（仅追加）。
- `knowledge-graph.json`：包含嵌入向量的完整知识图谱。
- `knowledge-summary.md`：知识图谱的便于阅读的摘要。
- `BRIEFING.md`：位于工作空间根目录，作为每日上下文参考。

## 自定义设置

### 更换模型

- 在每个脚本中修改模型名称：
  - `memory-extract.py`：将`"model": "gpt-4o-mini"`（或Claude/Gemini对应的模型）替换为所需模型。
- `memory-link.py`：将`"model": "text-embedding-3-small"`替换为所需模型。
- `memory-briefing.py`：将`"model": "gpt-4o-mini"`替换为所需模型。

### 调整提取方式

- 在`memory-extract.py`中修改提取提示，以获取不同类型的信息或调整输出格式。

### 调整链接阈值

- 在`memory-link.py`中修改用于创建链接的相似度阈值（当前设置为0.3）。

## 常见问题与解决方法

- **无法提取事实**：
  - 确保每日笔记或会话记录存在。
  - 检查API密钥是否设置正确。
  - 检查脚本输出中是否有LLM相关的错误信息。

- **链接质量较低**：
  - 如果使用OpenAI API密钥，可提高链接的准确性（基于嵌入向量的相似度计算比基于关键词的匹配更精确）。
  - 调整`memory-link.py`中的相似度阈值。

- **简报过长**：
  - 减少模板中包含的事实数量（修改`generate_fallback_briefing`函数）。
  - LLM生成的简报长度自动限制在2000个字符以内。

## 性能常规机制（钩子系统）

性能常规机制通过`src/`目录下的生命周期钩子实现，遵循了性能心理学的一个核心原则：**将思考与执行分开**。运动员不会在比赛进行中重新设计技术动作——他们会先进行有目的的思考，然后执行训练好的动作（反应性执行）。唯一的例外是处理真正的错误情况。

对于AI代理而言，这意味着：在推理开始之前，需要将所有上下文、约束条件及记忆信息预先加载到简报包中；执行过程应保持简洁。事后回顾应在推理结束后进行。

### 架构概述

```
User Message → Gateway → Agent Loop
  ├── before_agent_start → Briefing Packet (checklist + memory + constraints)
  ├── LLM Inference (clean context, no mid-run corrections)
  ├── before_tool_call → Policy enforcement (deny list)
  ├── Tool Execution → Result
  ├── tool_result_persist → Compression (head+tail, bounded)
  └── agent_end → After-Action Review → durable memory for next run
```

### 核心理念：避免在运行过程中进行实时调整

在运行过程中频繁进行修改会降低输出质量。在运行过程中插入修改指令会导致指令冲突，代理需要处理这些冲突。更好的方法是：
1. **捕获修改内容**：不要将修改内容直接插入当前执行流程。
2. **汇总修改内容**：将所有修改合并成一个清晰的更新。
3. **在下次会话中应用**：下一次生成的简报包中包含已修正的指令。

事后回顾（`agent_end`）的结果会反馈到下一次会话的简报中（`before_agent_start`）。这个循环是封闭的，不会在运行过程中中断。

### 配置方式

通过`openclaw.plugin.json`或代理配置文件进行配置：
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

### 钩子详细信息

- **`before_agent_start`——简报包**：
  - 从工作空间加载配置好的内存文件。
  - 组装简报包：包含任务提示、检查清单及提取的内存数据。
  - 将简报包注入系统提示中（遵守`maxChars`长度限制）。
  - 如果缺少内存文件，则忽略这些文件。

- **`before_tool_call`——工具使用规范**：
  - 检查工具名称是否在禁止使用列表中。
  - 如果工具被禁止使用，则抛出错误（防止执行）。
  - 可扩展以支持参数规范化。

- **`tool_result_persist`——结果压缩**：
  - 保持结果长度在`maxToolResultChars`（默认12000个字符）以内。
  - 采用头部（60%）和尾部（30%）的数据压缩策略。
  - 保持JSON格式的结果结构。

- **`after_action_review`——持久化记录**：
  - 将会话总结内容追加到配置好的内存文件中。
  - 从最终答案中提取关键信息。
  - 记录使用的工具及其执行结果（包括失败标志）。
  - 自动创建相应的目录。

### 源代码文件

- `src/index.ts`：钩子注册与连接逻辑。
- `src/briefing.ts`：简报包生成模块。
- `src/compress.ts`：结果压缩模块。
- `src/memory.ts`：内存文件加载与事后记录模块。

## 相关资源

- [安装指南](references/setup.md)：详细的安装和配置说明。
- [博客文章草稿](../../drafts/blog-pregame-routine.md)：性能常规机制的完整介绍。