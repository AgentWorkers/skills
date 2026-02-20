---
name: total-recall
description: "这是唯一一种能够自主监控用户记忆状态的工具。它不依赖任何数据库，也不使用向量数据或手动保存机制。它只是一个基于大型语言模型（LLM）的监控系统，会将用户的对话内容压缩成优先级排序的笔记，在笔记数量增加时进行整理，并能恢复任何被遗漏的信息。该工具具备五层冗余保护机制，完全无需维护。每月使用成本约为0.10美元。与其他需要用户主动提醒自己“记住某些内容”的记忆辅助工具不同，这款工具只需静静地关注用户的记忆过程即可。"
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
# Total Recall — 自动化代理记忆系统

**这是唯一一个能够自主监控记忆内容的工具。**

无需数据库、无需向量数据，也无需手动保存数据。它仅依赖一个大型语言模型（LLM）来记录用户的对话内容，并将这些内容压缩成优先级排序的笔记。当笔记数量过多时，系统会自动进行整合；同时，它还能恢复任何被遗漏的信息。该系统具备五层冗余机制，完全无需维护，每月费用约为0.10美元。

虽然其他记忆辅助工具需要用户主动提醒自己去记忆某些内容，但Total Recall只需默默地关注用户的对话过程即可。

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

- **观察者（Observer）**：读取最近的会话记录（JSONL格式），将其发送给大型语言模型（Gemini Flash），并将压缩后的观察结果按照优先级（🔴 高优先级、🟡 中等优先级、🟢 低优先级）添加到`observations.md`文件中。
- **整合器（Reflector）**：当观察结果文件过大时，会自动整合相关内容并删除低优先级的旧记录。
- **会话恢复功能（Session Recovery）**：在会话开始时运行，检查是否已捕获之前的会话记录；如果没有，则会进行紧急数据捕获。
- **反应式监控器（Reactive Watcher）**：通过`inotify`机制实时监控会话目录，确保高活跃度的会话内容能够被更快地捕获。
- **预压缩机制（Pre-compaction Hook）**：在OpenClaw准备压缩数据时启动，确保不会丢失任何信息。

## 快速入门

### 1. 安装该工具
```bash
clawdhub install total-recall
```

### 2. 设置OpenRouter API密钥
将API密钥添加到`.env`文件或OpenClaw配置文件中：
```bash
OPENROUTER_API_KEY=sk-or-v1-xxxxx
```

### 3. 运行设置脚本
```bash
bash skills/total-recall/scripts/setup.sh
```

设置脚本会完成以下操作：
- 创建内存目录结构（`memory/`、`logs/`、备份文件）。
- 在Linux系统中，通过`inotify`和`systemd`服务安装反应式监控器。
- 输出Cron作业和代理配置说明，供用户手动配置。

### 4. 配置代理以加载观察结果
将相关配置添加到代理的工作空间中（例如`MEMORY.md`文件或系统提示中）：
```
At session startup, read `memory/observations.md` for cross-session context.
```

或者使用OpenClaw的`memoryFlush.systemPrompt`命令来启动该功能。

## 平台支持

| 平台 | 观察者 + 整合器 + 会话恢复功能 | 反应式监控器 |
|----------|-------------------------------|-----------------|
| Linux（Debian/Ubuntu等） | ✅ 完全支持 | ✅ 需要`inotify-tools`工具 |
| macOS | ✅ 完全支持 | ❌ 仅支持基于Cron的自动备份 |

所有核心脚本均使用跨平台的bash命令（如`stat`、`date`、`md5`），并通过 `_compat.sh`文件进行兼容性处理。

## 配置参数

所有配置参数都从环境变量中读取，部分参数具有默认值：

| 参数 | 默认值 | 说明 |
|----------|---------|-------------|
| `OPENROUTER_API_KEY` | （必填） | 用于调用大型语言模型的API密钥 |
| `MEMORY_DIR` | `$OPENCLAW_WORKSPACE/memory` | 存储观察结果文件的目录 |
| `SESSIONS_DIR` | `~/.openclaw/agents/main/sessions` | OpenClaw会话记录的存储路径 |
| `OBSERVER_MODEL` | `google/gemini-2.5-flash` | 主要压缩模型 |
| `OBSERVERFallback_MODEL` | `google/gemini-2.0-flash-001` | 备用压缩模型 |
| `OBSERVER_lookBACK_MIN` | `15` | 日间数据保留时间（分钟） |
| `OBSERVER_MORNING_lookBACK_MIN` | `480` | 早晨（8点前）数据保留时间（分钟） |
| `OBSERVER_LINE_THRESHOLD` | `40` | 触发反应式监控的最低行数（Linux系统） |
| `OBSERVER_COOLDOWN_SECS` | `300` | 反应式监控之间的冷却时间（秒） |
| `REFLECTORWORD_THRESHOLD` | `8000` | 触发整合器运行的最低单词数 |
| `OPENCLAW_WORKSPACE` | `~/clawd` | 代理工作空间根目录 |

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

| 作业名称 | 安排时间 | 功能描述 |
|-----|----------|-------------|
| `memory-observer` | 每15分钟 | 压缩最近的对话记录 |
| `memory-reflector` | 每小时 | 整合过多的观察结果 |

## 反应式监控器（仅限Linux系统）

反应式监控器使用`inotifywait`来实时监控会话活动，从而比传统的Cron任务更快地触发观察者。该功能需要安装`inotify-tools`工具。

在macOS系统中，由于缺乏`inotify`支持，因此仅使用传统的Cron作业。

```bash
# Install inotify-tools (Debian/Ubuntu)
sudo apt install inotify-tools

# Check watcher status
systemctl --user status total-recall-watcher

# View logs
journalctl --user -u total-recall-watcher -f
```

## 成本

通过OpenRouter使用Gemini 2.5 Flash模型的费用为：
- 每月约0.05-0.15美元（包含观察者和整合器功能）。
- 每天大约运行15-30次Cron任务，每次处理数百条对话记录。

## 工作原理（技术细节）

### 观察者（Observer）
1. 查找最近修改过的会话记录文件（JSONL格式）。
2. 过滤掉子代理或由Cron任务生成的会话记录。
3. 从记录中提取用户和助手的对话内容。
4. 通过MD5哈希值进行去重处理。
5. 将处理后的数据发送给大型语言模型，并根据优先级进行压缩。
6. 将压缩结果添加到`observations.md`文件中。
7. 如果记录内容超过预设的单词阈值，会触发整合器进行进一步处理。

### 整合器（Reflector）
1. 备份当前的观察结果。
2. 将所有记录发送给大型语言模型，并附上整合指令。
3. 确认处理后的文件长度是否小于原始文件长度（进行完整性检查）。
4. 用整合后的内容替换原始记录。
5. 清理旧的备份文件（仅保留最近的10份备份）。

### 会话恢复功能（Session Recovery）
1. 在每次会话开始时运行，检查是否已保存之前的会话记录。
2. 对最新会话文件的行内容进行哈希处理。
3. 如果哈希值与之前保存的哈希值不匹配，会触发观察器进行恢复操作（回顾过去4小时的对话记录）。
4. 如果观察器出现故障，会直接提取原始对话内容作为备份。

### 反应式监控器（Reactive Watcher）
1. 使用`inotifywait`监控会话目录的更改。
2. 仅当有新的JSONL文件写入会话文件时才会触发观察器。
3. 每处理40条记录后，会等待5秒后再进行下一次检测。
4. 当检测到Cron任务或外部观察器运行时，会重置计数器。

## 自定义提示信息

观察者和整合器的提示信息存储在`prompts/`目录中：
- `prompts/observer-system.txt`：控制对话内容的压缩方式。
- `prompts/reflector-system.txt`：控制观察结果的整合方式。

用户可以根据自己的需求自定义这些提示信息，以匹配代理的个性和优先级设置。

## 设计灵感来源

该系统的设计灵感来源于人类睡眠时的记忆机制：海马体（观察者）负责捕捉记忆内容，而在睡眠期间的整合过程（整合器）会强化重要记忆，同时过滤掉无关信息。

阅读更多相关文章：[你的AI存在注意力问题](https://gavlahh.substack.com/p/your-ai-has-an-attention-problem)

*“让你的代理记住重要的事情吧。”*

---

（注：根据要求，翻译内容保持了技术细节的准确性，同时尽量使用了简洁明了的中文表达方式。）