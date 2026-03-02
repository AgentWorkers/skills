---
name: NEON-SOUL
version: 0.4.5
description: >
  **AI代理的自动化灵魂合成系统**  
  该系统能够从内存文件中提取代理的身份信息，将重复出现的模式提炼为公理（N≥3），并生成包含完整来源追踪信息的`SOUL.md`文件。整个处理过程由集成化的引擎完成，无需人工进行问答操作。
homepage: https://liveneon.ai
user-invocable: true
emoji: "\U0001F52E"
metadata:
  openclaw:
    config:
      stateDirs:
        - memory/
        - .neon-soul/
      writePaths:
        - SOUL.md
        - .neon-soul/backups/
    requires:
      node: ">=22.0.0"
      services:
        - name: ollama
          url: http://localhost:11434
          optional: false
tags:
  - soul
  - soul-synthesis
  - identity
  - self-learning
  - memory
  - provenance
  - compression
  - agent-soul
  - soul-document
  - ai-agent
---
# NEON-SOUL

这是一个用于AI代理的自动化灵魂合成工具。它能够读取内存文件，识别其中的重复模式，并生成包含来源追踪信息的SOUL.md文件。整个过程无需问卷调查或模板，用户的“灵魂”特征是通过真实的对话逐渐形成的。

**系统要求：** Node.js 22及以上版本；Ollama需要在本地运行（使用`ollama serve`命令）。

---

## 命令

### `/neon-soul synthesize`

执行内置的处理引擎。这是一个单次执行的命令：

```
exec node {baseDir}/scripts/neon-soul.mjs synthesize
```

默认情况下，合成过程是**增量式的**——仅处理新的或发生变化的内存文件和会话数据。现有数据会被保留并与新数据合并。之前的处理结果会被缓存（包括泛化信息、原则匹配结果、公理表示以及紧张度检测结果），因此相同的数据不会被重复处理。如果自上次运行以来没有变化，合成过程将自动跳过。

该脚本会自动检测Ollama的运行状态，读取内存文件，提取相关数据，生成新的公理，并最终生成SOUL.md文件。生成的结果将以JSON格式输出。

**结果展示方式：** 不要直接输出原始的JSON数据，而是提供简洁的文字总结：
- 如果有新的公理生成或数据数量发生变化：明确指出哪些内容发生了变化（例如：“3个新的信号被转化为公理——你的‘灵魂’正在不断深化”）
- 如果没有变化：只需简单说明“灵魂状态稳定，未检测到新的模式”
- 如果出现错误：详细说明问题所在并给出解决方法
- 自然地包含关键数据（如公理数量、信号数量），但无需列出所有字段
- 保持语言风格为反思性且亲切的——这是在描述用户的“灵魂”演变过程，而非构建日志

**可选参数：**
- `--reset`：清除所有合成数据和缓存，从头开始重新提取信息
- `--force`：即使没有检测到新的数据也会执行合成操作
- `--dry-run`：仅预览变化结果，不进行实际存储
- `--include-soul`：将现有的SOUL.md文件作为输入文件使用（适用于从手动制作的文件开始合成）
- `--memory-path <路径>`：指定内存文件的目录路径
- `--output-path <路径>`：指定SOUL.md文件的输出路径
- `--time-budget <分钟>`：指定合成操作的时间预算（默认为20分钟）。根据LLM的运行速度动态调整处理时间，以确保在预算内完成合成
- `--verbose`：显示详细的处理进度

**使用示例：**
```
exec node {baseDir}/scripts/neon-soul.mjs synthesize
exec node {baseDir}/scripts/neon-soul.mjs synthesize --reset
exec node {baseDir}/scripts/neon-soul.mjs synthesize --force
exec node {baseDir}/scripts/neon-soul.mjs synthesize --dry-run
```

**如果Ollama未运行**，脚本会输出错误提示。请用户先运行`ollama serve`命令。

---

### `/neon-soul status`

查看当前的灵魂状态。脚本会读取以下文件并生成报告：
1. 从`.neon-soul/state.json`中获取上次合成的时间戳
2. 从`.neon-soul/synthesis-data.json`中获取信号、原则和公理的数量
3. 统计自上次合成以来`memory/`目录下被修改的文件数量
4. 报告灵魂特征的覆盖范围（7个SoulCraft维度）

**可选参数：** `--verbose`, `--workspace <路径>`

---

### `/neon-soul rollback`

从备份中恢复之前的SOUL.md文件：
1. 在`.neon-soul/backups/`目录下查看所有备份文件
- 使用`--force`选项：恢复最近的备份
- 使用`--backup <时间戳> --force`选项：恢复指定的备份文件
- 使用`--list`选项：仅列出可用的备份文件，不进行恢复操作

---

### `/neon-soul audit`

查询所有公理的来源信息：
1. 读取`.neon-soul/synthesis-data.json`文件
- 使用`--list`选项：显示所有公理的ID和描述
- 使用`--stats`选项：按层次和维度展示统计信息
- 使用`<公理ID>`选项：查看完整的来源路径（公理 -> 原则 -> 信号 -> 源文件）

---

### `/neon-soul trace <公理ID>`

快速查询单个公理的来源信息：
1. 读取`.neon-soul/synthesis-data.json`文件
- 找到对应的`<公理ID>`
- 显示公理内容、参与生成它的原则以及对应的源文件行号

---

## 定时合成

可以设置cron任务来自动执行合成操作。由于采用增量式处理和多层缓存机制，只有在有新的内存数据或会话时才会真正执行合成操作——缓存后的任务可以在几秒钟内完成。

**推荐设置：** 每60分钟执行一次合成，每次合成之间有30分钟的延迟时间。

**OpenClaw的cron配置示例：**
```
openclaw cron add \
  --name "neon-soul-synthesis" \
  --every 60m \
  --timeout 1800 \
  --isolated \
  --message "Run neon-soul synthesis: exec node {baseDir}/scripts/neon-soul.mjs synthesize --memory-path <memory-path> --output-path <output-path>. Share a brief, warm summary of what changed — highlight any new patterns, axioms, or growth. If nothing changed, just a calm one-liner."
```

**也可以手动执行：** `./neon-soul synthesize`

**为什么使用cron而不是心跳检测？**
- 合成操作是独立运行的，不需要与主会话交互
- 默认为增量式处理，因此在数据无变化时缓存后的任务可以快速完成
- 自适应的时间控制可以防止任务持续运行过久

---

## 数据存储位置

| 数据类型 | 存储路径 |
|------|------|
| 内存文件 | `memory/`（包含日常记录、偏好设置和思考内容） |
| SOUL输出文件 | `SOUL.md` |
| 状态信息 | `.neon-soul/state.json` |
| 备份文件 | `.neon-soul/backups/` |
| 合成数据 | `.neon-soul/synthesis-data.json` |
| 缓存文件 | `.neon-soul/generalization-cache.json`, `compression-cache.json`, `tension-cache.json` |

---

## 隐私政策

NEON-SOUL会处理用户的个人内存文件以生成灵魂特征文件。所有数据仅存储在用户的本地机器上。

**NEON-SOUL不会做什么：**
- 将数据发送到任何外部服务（默认仅使用本地的Ollama模型）
- 将数据存储在用户的工作区之外
- 不会将数据传输给第三方分析、日志记录或跟踪服务
- 所有的网络请求都独立于用户的代理进程进行

**使用前建议：**
1. 查看`memory/`目录中的文件内容
2. 删除所有包含敏感信息（如密码、凭证等）的文件
3. 使用`--dry-run`选项预览处理内容

---

## 故障排除**

- 如果Ollama未运行：通过`curl http://localhost:11434/api/tags`检查其状态。请先运行`ollama serve`命令。
- 如果文本生成失败，NEON-SOUL会自动切换到使用列表格式显示结果。这通常表示Ollama超时或模型未加载。此时可以重新尝试合成操作。
- 如果模型更新后结果仍然无效：由于缓存是基于模型ID来管理的，因此需要使用`--reset`选项清除缓存并重新开始合成。