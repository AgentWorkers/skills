---
name: total-recall
description: "这是唯一一种能够自主监控用户记忆状态的工具。它不依赖任何数据库，也不使用任何向量数据结构，更不需要手动保存用户的信息。它只是一个基于大型语言模型（LLM）的监控工具，会将用户的对话内容压缩成优先级排序的笔记，当笔记数量过多时进行整理，并能恢复任何被遗漏的信息。该工具具备五层冗余保护机制，完全无需维护。每月使用成本仅约0.10美元。与其他需要用户主动提醒自己去记忆的工具不同，这个工具只需静静地“观察”用户的记忆过程即可。"
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: ["jq", "curl"]
    env:
      - key: OPENROUTER_API_KEY
        label: "OpenRouter API key (for LLM calls)"
        required: true
    config:
      memorySearch:
        description: "Enable memory search on observations.md for cross-session recall"
---
# Total Recall — 自主代理记忆系统

**这是唯一一个能够自主监控记忆内容的工具。**

无需数据库，无需向量数据，也无需手动保存数据。它只是一个基于大型语言模型（LLM）的观察者，会将你的对话内容压缩成优先级排序的笔记，在笔记数量过多时进行整合，并能恢复任何被遗漏的信息。系统具有五层冗余机制，完全无需维护，每月成本约为0.10美元。

虽然其他记忆辅助工具需要你主动去“记住某些事情”，但Total Recall只需默默地关注你的对话内容即可。

## 架构

```
Layer 1: Observer (cron, every 15-30 min)
    ↓ compresses recent messages → observations.md
Layer 2: Reflector (auto-triggered when observations > 8000 words)
    ↓ consolidates, removes superseded info → 40-60% reduction
Layer 3: Session Recovery (runs on every /new or /reset)
    ↓ catches any session the Observer missed
Layer 4: Reactive Watcher (inotify daemon, Linux only)
    ↓ triggers Observer after 40+ new JSONL writes, 5-min cooldown
Layer 5: Pre-compaction hook (memoryFlush)
    ↓ emergency capture before OpenClaw compacts context
```

## 功能介绍

- **观察者**：读取最近的会话记录（格式为JSONL），将其发送给LLM，并将压缩后的观察结果按照优先级（高、中、低）添加到`observations.md`文件中。
- **整合器**：当观察结果过多时启动，整合相关内容并删除低优先级的旧记录。
- **会话恢复**：在会话开始时运行，检查上一次会话是否已被记录；如果没有，则进行紧急备份。
- **反应式监控器**：使用`inotify`技术实时监控会话目录，确保高活跃度的会话内容能够更快地被捕获。
- **预压缩机制**：在OpenClaw准备压缩数据时启动，确保不会丢失任何信息。

## 快速入门

### 1. 安装该工具
```bash
clawdhub install total-recall
```

### 2. 设置API密钥
将API密钥添加到`.env`文件或OpenClaw配置文件中：
```bash
OPENROUTER_API_KEY=sk-or-v1-xxxxx
```

### 3. 运行设置脚本
```bash
bash skills/total-recall/scripts/setup.sh
```

该脚本将完成以下操作：
- 创建记忆数据目录结构（`memory/`、`logs/`、`backups`）。
- 在Linux系统中，通过`inotify`和`systemd`服务安装反应式监控器。
- 打印出Cron作业的配置信息，供你手动添加。

### 4. 配置代理以加载观察结果
将相关配置添加到代理的工作空间中（例如`MEMORY.md`文件或系统提示信息中）：
```
At session startup, read `memory/observations.md` for cross-session context.
```

或者使用OpenClaw的`memoryFlush.systemPrompt`命令来设置启动时的配置。

## 平台支持

| 平台 | 观察者 + 整合器 + 恢复机制 | 反应式监控器 |
|----------|-------------------------------|-----------------|
| Linux（Debian/Ubuntu等） | 完全支持 | 需要`inotify-tools`工具 |
| macOS | 完全支持 | 仅支持基于Cron的备份机制 |

所有核心脚本均使用跨平台的bash脚本。`stat`、`date`和`md5`命令通过 `_compat.sh` 文件实现跨平台兼容性。

## 配置参数

所有配置参数都从环境变量中读取，默认值如下：

| 参数 | 默认值 | 说明 |
|----------|---------|-------------|
| `OPENROUTER_API_KEY` | （必填） | 用于调用LLM的API密钥 |
| `MEMORY_DIR` | `$OPENCLAW_WORKSPACE/memory` | 存储观察结果的目录 |
| `SESSIONS_DIR` | `~/.openclaw/agents/main/sessions` | OpenClaw会话记录的存储路径 |
| `OBSERVER_MODEL` | `deepseek/deepseek-v3.2` | 主要压缩模型 |
| `OBSERVERFallback_MODEL` | `google/gemini-2.5-flash` | 备用压缩模型 |
| `OBSERVER_lookBACK_MIN` | `15` | 日间查看的记录时间（分钟） |
| `OBSERVER_MORNING_lookBACK_MIN` | `480` | 清晨8点之前的记录时间（分钟） |
| `OBSERVER_LINE_THRESHOLD` | `40` | 触发反应式监控的最低行数（Linux系统） |
| `OBSERVER_COOLDOWN_SECS` | `300` | 反应式监控之间的冷却时间（Linux系统） |
| `REFLECTORWORD_THRESHOLD` | `8000` | 触发整合器的最低单词数 |
| `OPENCLAW_WORKSPACE` | `~/your-workspace` | 代理工作空间路径 |

## LLM提供者配置

Total Recall支持任何与OpenAI兼容的聊天完成API。通过设置环境变量来切换提供者：

| 参数 | 默认值 | 说明 |
|----------|---------|-------------|
| `LLM_BASE_URL` | `https://openrouter.ai/api/v1` | API接口地址 |
| `LLM_API_KEY` | 使用`OPENROUTER_API_KEY`作为默认值 |
| `LLM_MODEL` | `deepseek/deepseek-v3.2` | 使用的模型 |

### 提供者示例

```bash
# OpenRouter (default)
export OPENROUTER_API_KEY="your-key"

# Ollama (local)
export LLM_BASE_URL="http://localhost:11434/v1"
export LLM_API_KEY="ollama"
export LLM_MODEL="llama3.1:8b"

# Groq
export LLM_BASE_URL="https://api.groq.com/openai/v1"
export LLM_API_KEY="your-groq-key"
export LLM_MODEL="llama-3.3-70b-versatile"
```

## 生成的文件

```
memory/
  observations.md          # The main observation log (loaded at startup)
  observation-backups/     # Reflector backups (last 10 kept)
  .observer-last-run       # Timestamp of last observer run
  .observer-last-hash      # Dedup hash of last processed messages
logs/
  observer.log
  reflector.log
  session-recovery.log
  observer-watcher.log
```

## Cron作业

设置脚本会创建以下Cron作业：

| 作业 | 定时任务 | 说明 |
|-----|----------|-------------|
| `memory-observer` | 每15分钟 | 压缩最近的对话记录 |
| `memory-reflector` | 每小时 | 整合过多的观察结果 |

## 反应式监控器（仅限Linux系统）

反应式监控器使用`inotifywait`来实时监控会话活动，从而比单独使用Cron更快地触发观察者任务。需要安装`inotify-tools`工具。

```bash
# Install inotify-tools (Debian/Ubuntu)
sudo apt install inotify-tools

# Check watcher status
systemctl --user status total-recall-watcher

# View logs
journalctl --user -u total-recall-watcher -f
```

## 成本

使用DeepSeek v3.2并通过OpenRouter服务时，每月成本约为0.03-0.10美元（包含观察者和整合器功能）。
每天大约会运行15-30次Cron作业，每次处理几百个对话记录。

## 工作原理（技术细节）

### 观察者
1. 查找最近修改的会话JSONL文件。
2. 过滤掉子代理或Cron任务生成的会话记录。
3. 从记录中提取用户和助手的对话内容。
4. 通过MD5哈希值进行去重处理。
5. 将处理后的数据发送给LLM，并根据优先级进行压缩。
6. 将压缩结果添加到`observations.md`文件中。
7. 如果记录内容超过预设的单词数量阈值，会触发整合器进行进一步处理。

### 整合器
1. 备份当前的观察结果。
2. 将所有记录发送给LLM，并附带整合指令。
3. 验证处理后的文件长度是否小于原始文件长度（确保数据完整）。
4. 用整合后的版本替换原始记录。
5. 清理旧的备份文件（仅保留最近的10份备份）。

### 会话恢复
1. 在每次会话开始时运行，检查上一次会话是否已被记录；如果没有，则进行紧急备份。
2. 对会话文件的最新内容进行哈希处理。
3. 与上次观察结果进行对比；如果不一致，则启动观察器进行恢复操作（最多查看4小时内的记录）。
4. 如果观察器失败，则手动提取原始对话内容。

### 反应式监控器
1. 使用`inotifywait`监控会话目录的更改。
2. 仅记录写入`main sessions`文件的JSONL文件。
3. 当检测到更改时（至少有40条新记录），触发观察器执行整合操作；每次触发之间有5分钟的冷却时间。
4. 当检测到Cron作业或外部观察器运行时，重置计数器。

## 自定义提示信息

观察者和整合器的提示信息存储在`prompts/`目录下：
- `prompts/observer-system.txt`：控制对话内容的压缩方式。
- `prompts/reflector-system.txt`：控制观察结果的整合方式。

你可以根据代理的特性和需求自定义这些提示信息。

---

## Dream Cycle（梦境循环）

Dream Cycle是一个可选的夜间运行脚本，用于在非工作时间整理`observations.md`文件。它会归档过时的内容，并添加语义标签，确保有用的信息不会丢失。系统保持简洁性，所有内容仍然可以轻松查找。

### 功能介绍

- 根据内容的重要性和时效性（关键/高/中/低/最低）对记录进行分类。
- 归档超过时效阈值的记录。
- 为每个归档的记录添加语义标签（包含关键词和归档链接）。
- 如果出现问题，系统会自动验证并恢复数据。

### 主要特性

- **多路径检索**：每个归档记录提供4-5种不同的搜索方式。即使使用不同的关键词进行搜索，也能找到相关内容。
- **置信度评分**：每条记录都会被赋予置信度评分（0.0-1.0），并标明信息来源类型（明确/隐含/推理/不确定）。高置信度的记录会被保留更长时间；低置信度的记录会被更快归档。
- **记忆类型系统**：支持7种记忆类型，每种类型都有不同的保留期限：`event`（14天）、`fact`（90天）、`preference`（180天）、`goal`（365天）、`habit`（365天）、`rule`（永久保存）、`context`（30天）。这些信息以不可见的HTML元数据形式存储在`observations.md`文件中。
- **记录压缩**：将3条及以上相关的记录合并为一条摘要。原始记录会被归档，只保留摘要信息，从而实现高达75%的文件大小缩减。
- **重要性衰减**：每天根据类型调整记录的重要性评分。低于保留阈值的记录会被标记为删除对象。具体衰减速率如下：`event`（每天减少0.5），`fact`（每天减少0.1），`preference`（每天减少0.02），`rule`/`habit`/`goal`（不衰减）。
- **主题提取**：扫描最近的会话记录，找出重复出现的主题（需在3天以上出现3次）。将提取结果保存到`memory/dream-staging/`目录中，供人工审核。可以使用`staging-review.sh`脚本来查看、批准或拒绝这些提取结果。`context`类型的记录永远不会被自动归档。

### 设置方法

1. 运行`bash skills/total-recall/scripts/setup.sh`命令，自动创建Dream Cycle所需的目录。
2. 添加夜间运行的Cron作业：
   ```
   # Dream Cycle — nightly at 3am
   0 3 * * * OPENCLAW_WORKSPACE=~/your-workspace bash ~/your-workspace/skills/total-recall/scripts/dream-cycle.sh preflight
   ```

3. 使用`prompts/dream-cycle-prompt.md`作为代理的提示信息。推荐模型：`Claude Sonnet`用于分析决策，`DeepSeek v3.2`用于执行归档操作。
4. 在最初几晚将`READ_ONLY_MODE`设置为`true`以进行测试。每次运行后查看`memory/dream-logs/`目录，确认归档内容。
5. 确认效果后，将`READ_ONLY_MODE`设置为`false`。

### 配置参数

| 参数 | 默认值 | 说明 |
|----------|---------|-------------|
| `DREAM_TOKEN_TARGET` | `8000` | 归档后的记录最大长度（以单词计） |
| `READ_ONLY_MODE` | `false` | 设置为`true`以进行无写入的测试分析 |

## 相关文件

| 文件 | 说明 |
|------|-------------|
| `scripts/dream-cycle.sh` | 脚本工具：用于预处理、归档、更新记录、写入日志等操作 |
| `prompts/dream-cycle-prompt.md` | 夜间Dream Cycle运行的提示信息 |
| `dream-cycle/README.md` | Dream Cycle的快速使用指南 |
| `schemas/observation-format.md` | 扩展的观察记录元数据格式 |

## 监控和故障排除

**观察者未运行？**
- 查看`logs/observer.log`文件中的错误信息。
- 确保`OPENROUTER_API_KEY`已正确设置且有效。
- 确认Cron作业正在运行：`crontab -l`。

**会话开始时无法加载观察结果？**
- 确保代理的启动脚本包含读取`memory/observations.md`的指令。
- 检查`MEMORY_DIR`是否指向正确的路径。

**反应式监控器未触发？**
- 运行`systemctl --user status total-recall-watcher`命令。
- 确保安装了`inotify-tools`：`which inotifywait`。
- 查看监控器的日志：`journalctl --user -u total-recall-watcher -f`。

**Dream Cycle归档过于频繁？**
- 将`READ_ONLY_MODE`设置为`true`，并在正式上线前测试归档行为。
- 调高`DREAM_TOKEN_TARGET`值，减少每次的归档频率。

## 受启发来源

该系统的设计灵感来源于人类睡眠期间的记忆机制：海马体（观察者）负责捕捉记忆，而在睡眠期间的整合过程（整合器）会强化重要记忆，同时过滤掉无关信息。

阅读更多相关文章：[你的AI存在注意力问题](https://gavlahh.substack.com/p/your-ai-has-an-attention-problem)

*“让你的AI发挥作用吧。”*

---

（注：由于文本较长，部分内容在翻译时进行了适当压缩和简化。）