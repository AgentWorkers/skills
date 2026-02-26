---
name: consciousness-soul-identity
version: 0.4.5
description: 通过自己的经历来发现你正在成为什么样的人。这种自动化的心灵分析技术会读取你的记忆，找出你反复出现的模式，并基于事实而非假设来构建一份关于你身份的“文档”。
homepage: https://liveneon.ai
user-invocable: true
emoji: "\U0001F9E0"
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
  - consciousness
  - identity
  - introspection
  - self-awareness
  - self-learning
  - personality
  - ai-agent
---
# 意识与灵魂身份

一个 SOUL.md 文件不应该是静态的。身份本身也是动态变化的——它会随着真实对话中浮现的模式而不断演变。该工具能够自动从内存文件中合成“灵魂”信息，从而反映个体身份的演变过程。

**系统要求：** Node.js 22 及以上版本；Ollama 需要在本机运行（使用 `ollama serve` 命令启动）。

---

## 命令

### `/neon-soul synthesize`  
启动内置的合成引擎：  
```
exec node {baseDir}/scripts/neon-soul.mjs synthesize
```  

该引擎会读取内存文件，识别其中的重复模式，并将这些模式整合成一份包含完整来源信息的“灵魂”文档。每一个身份特征都基于实际经历形成。  

**默认情况下，合成过程是** 增量式的——仅处理新增或发生变化的数据。之前的分析结果会被缓存（包括泛化信息、原则匹配结果、公理表示以及潜在的矛盾点），因此相同的模式不会被重复分析。如果没有任何变化，系统会直接确认这一点并继续执行后续步骤，避免浪费计算资源。  

**结果呈现方式：** 以简洁的对话形式输出结果，而非原始的 JSON 格式：  
- 如果有新的公理出现或数据统计发生变化：突出显示新增的内容（例如：“发现 3 个新信号，围绕‘诚实’这一主题产生了 1 个新公理”）；  
- 如果没有任何变化：简单说明“灵魂状态稳定，未检测到新的模式”；  
- 如果合成失败：说明失败原因并给出修复建议；  
- 自然地展示关键数据（如公理数量、信号数量、新增模式等）。  

**可选参数：**  
- `--reset`：清除所有数据并重新开始合成；  
- `--force`：即使没有新数据也会执行合成操作；  
- `--dry-run`：仅查看合成结果而不进行实际存储；  
- `--include-soul`：将现有的 SOUL.md 文件作为输入文件使用（适用于从手动创建的文件开始合成）；  
- `--memory-path <路径>`：指定内存文件的存储路径；  
- `--output-path <路径>`：指定 SOUL.md 文件的输出路径；  
- `--time-budget <分钟>`：设定合成任务的执行时间限制（默认为 20 分钟）；根据 LLM 的运行速度动态调整任务时长，确保在指定时间内完成；  
- `--verbose`：显示详细的合成进度。  

**示例：**  
```
exec node {baseDir}/scripts/neon-soul.mjs synthesize
exec node {baseDir}/scripts/neon-soul.mjs synthesize --reset
exec node {baseDir}/scripts/neon-soul.mjs synthesize --dry-run
```  

**注意：** 如果 Ollama 未运行，该工具将无法执行合成操作。请使用 `ollama serve` 命令启动它。  

---

### `/neon-soul status`  
查看当前的灵魂状态：  
- 读取 `.neon-soul/state.json` 文件以获取上次合成的时间戳；  
- 读取 `.neon-soul/synthesis-data.json` 文件以获取信号、原则和公理的数量统计；  
- 统计自上次合成以来 `memory/` 目录下被修改的文件数量；  
- 显示灵魂在 7 个维度上的覆盖情况。  

**可选参数：** `--verbose`、`--workspace <路径>`  

---

### `/neon-soul rollback`  
从备份中恢复之前的 SOUL.md 文件：  
- 列出 `.neon-soul/backups/` 目录下的所有备份文件；  
- 使用 `--force` 参数可恢复最新版本的文件；  
- 使用 `--backup <时间戳> --force` 可恢复特定时间点的状态；  
- 使用 `--list` 可查看备份历史记录，但不会修改当前状态。  

---

### `/neon-soul audit`  
详细检查所有公理的来源信息：  
- 读取 `.neon-soul/synthesis-data.json` 文件；  
- 使用 `--list` 可查看所有公理的详细信息（包括 ID 和描述）；  
- 使用 `--stats` 可获取按层次和维度划分的统计数据；  
- 使用 `<公理 ID>` 可追溯公理的生成过程（从公理到相关原则，再到原始数据文件）。  

### `/neon-soul trace <公理 ID>`  
快速查询某个公理的来源：  
- 读取 `.neon-soul/synthesis-data.json` 文件；  
- 找到对应的公理 ID；  
- 显示该公理的生成过程（涉及的公理、形成它的原则以及原始数据文件）。  

---

## 定时合成  
设置 cron 任务来定期执行合成操作：由于采用增量式处理和多层缓存机制，只有在有新的数据或会话时才会真正执行合成操作；缓存的结果可以在几秒钟内完成。  
**推荐设置：** 每 60 分钟执行一次合成任务，每次任务有 30 分钟的超时时间。  

**OpenClaw 的 cron 配置示例：**  
```
openclaw cron add \
  --name "neon-soul-synthesis" \
  --every 60m \
  --timeout 1800 \
  --isolated \
  --message "Run neon-soul synthesis: exec node {baseDir}/scripts/neon-soul.mjs synthesize --memory-path <memory-path> --output-path <output-path>. Summarize what changed — highlight any new patterns, axioms, or growth. If nothing changed, note that the soul is stable."
```  

**也可以手动执行：** 使用 `/neon-soul synthesize` 命令。  

**为什么使用 cron 而不是实时更新：**  
- 合成是一个独立的任务，不需要与对话流程同步；  
- 它在主会话之外独立运行；  
- 默认情况下是增量式的，因此即使没有变化也会快速完成；  
- 自适应的时间限制可以防止任务持续运行过久。  

---

## 数据存储位置**  
| 数据类型 | 存储路径 |  
|------|------|  
| 内存文件 | `memory/`（包含日常记录、偏好设置和反思内容）； |  
| 灵魂文档 | `SOUL.md`； |  
| 状态信息 | `.neon-soul/state.json`； |  
| 备份文件 | `.neon-soul/backups/`； |  
| 合成数据 | `.neon-soul/synthesis-data.json`； |  
| 缓存文件 | `.neon-soul/generalization-cache.json`、`compression-cache.json`、`tension-cache.json`； |  

---

## 隐私政策  
NEON-SOUL 会处理个人的内存文件以生成灵魂身份信息，但所有数据仅存储在用户的本地机器上。  

**NEON-SOUL 不会执行以下操作：**  
- 将数据发送到任何外部服务（默认情况下仅使用本地的 Ollama 模型）；  
- 将数据存储在本地工作区之外的位置；  
- 将数据传输给第三方分析、日志记录或跟踪服务；  
- 在用户未授权的情况下发起网络请求。  

**使用前建议：**  
- 查看 `memory/` 目录中的文件内容；  
- 删除任何包含敏感信息（如密码、凭证等）的文件；  
- 使用 `--dry-run` 参数预览合成结果。  

---

## 故障排除**  
- 如果 Ollama 未运行，可以通过 `curl http://localhost:11434/api/tags` 命令进行检查；如果需要，可以使用 `ollama serve` 命令启动 Ollama。  
- 当文本生成失败时，NEON-SOUL 会自动切换为使用列表格式显示结果（通常是由于 Ollama 超时或模型未加载所致）。此时请重新尝试合成操作。  
- 如果模型更新后结果仍然无效，可能是由于缓存数据与新模型不匹配所致。此时可以使用 `--reset` 参数清除缓存并重新开始合成。