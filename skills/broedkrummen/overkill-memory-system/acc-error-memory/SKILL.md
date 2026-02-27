---
name: acc-error-memory
description: "**AI代理的错误模式跟踪功能**：该功能能够检测错误并采取相应的纠正措施；对于反复出现的错误，系统会进行升级处理（即采取更高级别的应对策略）；同时，该系统还能学习如何有效减轻这些错误的影响。这是AI Brain系列中“Something’s Off”检测器（“有异常情况”检测器）的核心功能之一。"
metadata:
  openclaw:
    emoji: "⚡"
    version: "1.0.0"
    author: "ImpKind"
    repo: "https://github.com/ImpKind/acc-error-memory"
    requires:
      os: ["darwin", "linux"]
      bins: ["python3", "jq"]
    tags: ["memory", "monitoring", "ai-brain", "error-detection"]
---

# 前扣带回记忆功能 ⚡  
**用于AI代理的冲突检测与错误监控**。属于“AI大脑”系列技能之一。  

前扣带回皮层（Anterior Cingulate Cortex, ACC）负责监控错误和冲突。该功能使AI代理能够从错误中学习——通过长期追踪错误模式，在以往经常出问题的情境中变得更加谨慎。  

## 问题  
AI代理可能会犯以下错误：  
- 误解用户意图  
- 提供错误信息  
- 使用不当的语气  
- 忘记之前的对话内容  

若不进行错误追踪，同样的错误会不断重复。前扣带回皮层会检测并记录这些错误，从而在多次会话中保持对这些错误的认知。  

## 解决方案  
通过以下方式追踪错误模式：  
- **模式检测**：重复出现的错误类型会被标记为需要关注的问题  
- **严重程度分级**：正常（1次）、警告（2次）、严重（3次及以上）  
- **解决状态追踪**：如果某种错误在30天后仍未解决，则将其标记为“已解决”  
- **水印系统**：采用增量处理方式，避免重复分析同一数据  

## 配置  
### ACC_MODELS（模型无关）  
LLM（Large Language Model）的筛选和校准脚本与具体模型无关。只需将`ACC_MODELS`设置为任何可通过CLI访问的模型即可：  

```bash
# Default (Anthropic Claude via CLI)
export ACC_MODELS="claude --model haiku -p,claude --model sonnet -p"

# Ollama (local)
export ACC_MODELS="ollama run llama3,ollama run mistral"

# OpenAI
export ACC_MODELS="openai chat -m gpt-4o-mini,openai chat -m gpt-4o"

# Single model (no fallback)
export ACC_MODELS="claude --model haiku -p"
```  

**格式：** 以逗号分隔的CLI命令。每个命令的执行都需要在末尾加上相应的提示参数。系统会按顺序尝试不同的模型；如果第一个模型失败或超时（45秒），则会自动切换到下一个模型。  

**使用ACC_MODELS的脚本：**  
- `haiku-screen.sh`：通过LLM确认经过正则表达式过滤的错误候选项  
- `calibrate-patterns.sh`：通过LLM分类来校准错误模式  

## 快速入门  
### 1. 安装  
```bash
cd ~/.openclaw/workspace/skills/anterior-cingulate-memory
./install.sh --with-cron
```  
安装完成后：  
- 会创建一个名为`memory/acc-state.json`的文件，其中包含初始的空错误模式记录  
- 生成`ACC_STATE.md`文件，用于存储会话上下文信息  
- 设置定时任务，每天自动执行3次分析（凌晨4点、中午12点、晚上8点）  

### 2. 检查当前状态  
```bash
./scripts/load-state.sh
# ⚡ ACC State Loaded:
# Active patterns: 2
# - tone_mismatch: 2x (warning)
# - missed_context: 1x (normal)
```  

### 3. 手动记录错误  
```bash
./scripts/log-error.sh \
  --pattern "factual_error" \
  --context "Stated Python 3.9 was latest when it's 3.12" \
  --mitigation "Always web search for version numbers"
```  

### 4. 检查已解决的错误模式  
```bash
./scripts/resolve-check.sh
# Checks patterns not seen in 30+ days
```  

## 相关脚本  
| 脚本 | 功能 |  
|--------|---------|  
| `preprocess-errors.sh` | 提取自水印标记以来的用户与代理的交互记录  
| `encode-pipeline.sh` | 运行完整的预处理流程  
| `log-error.sh` | 记录包含错误模式、上下文及处理措施的日志  
| `load-state.sh` | 生成便于人类阅读的会话状态报告  
| `resolve-check.sh` | 检查哪些错误模式已解决（超过30天）  
| `update-watermark.sh` | 更新处理过程中的“水印”标记  
| `sync-state.sh` | 从`acc-state.json`生成`ACC_STATE.md`文件  
| `log-event.sh` | 记录用于分析的事件数据  

## 工作原理  
### 1. 预处理流程  
`encode-pipeline.sh`从会话记录中提取交互内容：  
**输出结果：`pending-errors.json`文件，其中包含用户与代理的交互记录**  
```json
[
  {
    "assistant_text": "The latest Python version is 3.9",
    "user_text": "Actually it's 3.12 now",
    "timestamp": "2026-02-11T10:00:00Z"
  }
]
```  

### 2. 错误分析（通过Cron任务）  
配置好的LLM（通过`ACC_MODELS`指定）会分析每次交互，判断是否存在以下情况：  
- 直接的纠正反馈（如“不”、“错了”）  
- 隐性的纠正表达（如“实际上……”）  
- 表示用户困惑的信号  
- 由代理行为引起的用户困惑  

### 3. 模式追踪  
错误会按照出现频率被分类记录：  
- **1次** → 正常（标记为“需要注意”）  
- **2次** → 警告（需特别关注）  
- **3次及以上** → 严重（应主动避免）  

### 4. 错误解决  
如果某种错误在30天内未被解决，它会被标记为“已解决”：  
```bash
./scripts/resolve-check.sh
# ✓ Resolved: version_numbers (32 days clear)
```  

## 定时任务安排  
默认设置：每天自动执行3次分析，以加快反馈循环速度：  
```bash
# Add to cron
openclaw cron add --name acc-analysis \
  --cron "0 4,12,20 * * *" \
  --session isolated \
  --agent-turn "Run ACC analysis pipeline..."
```  

## 状态文件格式  
```json
{
  "version": "2.0",
  "lastUpdated": "2026-02-11T12:00:00Z",
  "activePatterns": {
    "factual_error": {
      "count": 3,
      "severity": "critical",
      "firstSeen": "2026-02-01T10:00:00Z",
      "lastSeen": "2026-02-10T15:00:00Z",
      "context": "Stated outdated version numbers",
      "mitigation": "Always verify versions with web search"
    }
  },
  "resolved": {
    "tone_mismatch": {
      "count": 2,
      "resolvedAt": "2026-02-11T04:00:00Z",
      "daysClear": 32
    }
  },
  "stats": {
    "totalErrorsLogged": 15
  }
}
```  

## 事件日志  
系统会持续记录前扣带回皮层的活动情况：  
**事件数据会被保存到`~/.openclaw/workspace/memory/brain-events.jsonl`文件中**  
```json
{"ts":"2026-02-11T12:00:00Z","type":"acc","event":"analysis","errors_found":2,"patterns_active":3}
```  

## 与OpenClaw的集成  
**方法：在代理启动脚本（AGENTS.md）中添加相关配置**  
```markdown
## Every Session
1. Load hippocampus: `./scripts/load-core.sh`
2. Load emotional state: `./scripts/load-emotion.sh`
3. **Load error patterns:** `~/.openclaw/workspace/skills/anterior-cingulate-memory/scripts/load-state.sh`
```  

## 行为指南  
当发现前扣带回皮层中的错误模式时：  
- 🔴 **严重错误（3次及以上）**：在回应前务必仔细核实  
- ⚠️ **警告错误（2次）**：需格外小心  
- ✅ **问题已解决**：记住经验教训，避免再次犯错  

## 未来计划：与杏仁核的集成  
**计划中：** 将前扣带回皮层与杏仁核连接起来，让错误影响代理的情绪状态：  
- 错误会导致情绪低落、警觉性提高  
- 顺利解决问题的情况会提升代理的积极情绪  
- 错误的解决会带来成就感  

## “AI大脑”系列技能  
| 技能名称 | 功能 | 开发状态 |  
|------|----------|--------|  
| [海马体](https://www.clawhub.ai/skills/hippocampus) | 记忆形成、衰退与强化 | 已上线 |  
| [杏仁核记忆](https://www.clawhub.ai/skills/amygdala-memory) | 情绪处理 | 已上线 |  
| [VTA记忆](https://www.clawhub.ai/skills/vta-memory) | 奖励机制与动机驱动 | 已上线 |  
| **前扣带回记忆** | 冲突检测与错误监控 | 已上线 |  
| [基底神经节记忆](https://www.clawhub.ai/skills/basal-ganglia-memory) | 习惯形成 | 正在开发中 |  
| [岛叶记忆](https://www.clawhub.ai/skills/insula-memory) | 内部状态感知 | 正在开发中 |  

## 设计理念  
人类大脑中的前扣带回皮层会让人产生“出错”的感觉——这是一种潜意识的错误感知。该功能让AI代理也具备类似的自我认知能力，能够持续关注错误模式并据此调整行为。  

**由OpenClaw社区共同开发 🚡**