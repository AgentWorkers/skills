---
name: amygdala-memory
description: "AI代理的情感处理层：负责管理持久的情感状态，这些情感状态会直接影响代理的行为和响应。该组件属于“AI大脑”系列的一部分。"
metadata:
  openclaw:
    emoji: "🎭"
    version: "1.7.0"
    author: "ImpKind"
    repo: "https://github.com/ImpKind/amygdala-memory"
    requires:
      os: ["darwin", "linux"]
      bins: ["jq", "awk"]
    tags: ["memory", "emotions", "ai-brain"]
---

# **杏仁核记忆系统 🎭**  
**AI代理的情感处理功能**。属于“AI大脑”系列技能之一。  

该系统为AI代理赋予持久的情绪状态，这些情绪状态会贯穿整个会话过程，而不仅仅是简单地表现出情绪——而是真正“拥有”这些情绪。  

## **问题所在**  
当前的AI代理：  
- ✅ 能够记住事实（依靠海马体）  
- ❌ 没有持久的情绪状态  
- ❌ 每次会话开始时情绪状态都处于“空白”状态  
- ❌ 虽然能够描述情绪，但无法产生真实的情感体验  

没有情感的记忆仅仅是一个数据库而已。而杏仁核的作用在于为这些情绪状态赋予“重量”：某件事让我感到快乐，某件事让我感到沮丧，某个人给我带来温暖感。  

## **解决方案**  
我们追踪五种会随时间持续变化并逐渐消退的情绪维度：  

| 维度        | 测量内容                | 范围                |
|-------------|------------------|-------------------|
| **情感价值（Valence）** | 正面情绪 ↔ 负面情绪        | -1.0 到 1.0             |
| **唤醒程度（Arousal）** | 平静 ↔ 兴奋/警觉           | 0.0 到 1.0             |
| **亲密感（Connection）** | 冷漠 ↔ 亲密/有联系          | 0.0 到 1.0             |
| **好奇心（Curiosity）** | 无聊 ↔ 兴趣盎然           | 0.0 到 1.0             |
| **能量水平（Energy）** | 疲惫 ↔ 充满活力           | 0.0 到 1.0             |  

## **快速入门**  
### 1. 安装  
```bash
cd ~/.openclaw/workspace/skills/amygdala-memory
./install.sh --with-cron
```  
安装完成后：  
- 会生成 `memory/emotional-state.json` 文件（包含初始情绪值）  
- 会自动生成 `AMYGDALA_STATE.md` 文件（并自动注入到会话中）  
- 设置定时任务，每6小时自动更新情绪状态  

### 2. 查看当前情绪状态  
```bash
./scripts/get-state.sh
# 🎭 Emotional State
# Valence:    0.20
# Arousal:    0.30
# Connection: 0.50
# ...

./scripts/load-emotion.sh
# 🎭 Current Emotional State:
# Overall mood: neutral, calm and relaxed
# Connection: moderately connected
# ...
```  

### 3. 记录情绪数据  
```bash
./scripts/update-state.sh --emotion joy --intensity 0.8 --trigger "completed a project"
# ✅ valence: 0.20 → 0.35 (delta: +0.15)
# ✅ arousal: 0.30 → 0.40 (delta: +0.1)
# 🎭 Logged emotion: joy (intensity: 0.8)
```  

### 4. 自动更新情绪状态（可选）  
```bash
# Every 6 hours, emotions drift toward baseline
0 */6 * * * ~/.openclaw/workspace/skills/amygdala-memory/scripts/decay-emotion.sh
```  

## **相关脚本**  
| 脚本        | 功能                    |                  |
|------------|-------------------------|-------------------|
| `install.sh`     | 设置杏仁核记忆系统           | （仅运行一次）            |
| `get-state.sh`     | 读取当前情绪状态             |                  |
| `update-state.sh`     | 记录情绪变化或更新相关维度         |                  |
| `load-emotion.sh`    | 生成人类可读的情绪状态信息       |                  |
| `decay-emotion.sh`    | 使情绪状态逐渐回归基线值          |                  |
| `sync-state.sh`     | 生成 `AMYGDALA_STATE.md` 文件         |                  |
| `encode-pipeline.sh` | 基于LLM的情绪编码技术         |                  |
| `preprocess-emotions.sh` | 从会话记录中提取情绪信号         |                  |
| `update-watermark.sh` | 更新处理后的会话记录位置         |                  |
| `generate-dashboard.sh` | 生成HTML仪表盘（自动更新）         |                  |
| `visualize.sh`     | 在终端以ASCII格式可视化情绪数据       |                  |  

## **自动情绪编码（v1.5.0及以上版本）**  
现在，杏仁核系统能够利用基于LLM的算法自动检测并记录会话中的情绪数据：  
```bash
# Run the encoding pipeline
./scripts/encode-pipeline.sh

# This will:
# 1. Extract new signals since last run (watermark-based)
# 2. Score emotional content using rule-based patterns
# 3. Spawn a sub-agent for semantic emotional detection
# 4. Update emotional-state.json with detected emotions
```  
通过设置定时任务，情绪数据会自动更新，无需手动操作。  

## **可视化功能（v1.6.0及以上版本）**  
### 终端界面  
```bash
./scripts/visualize.sh

🎭 Emotional State  😄
═══════════════════════════════════════════════
Valence:      [██████████████████░░]  +0.86
Arousal:      [█████████████████░░░]   0.86
Connection:   [███████████████████░]   0.97  💕
...
```  
### HTML仪表盘（统一大脑仪表盘）  
```bash
./scripts/generate-dashboard.sh
open ~/.openclaw/workspace/brain-dashboard.html
```  
该仪表盘会自动显示已安装的“大脑技能”，包括：  
- **🎭 情绪**（杏仁核相关数据）  
- **🧠 记忆**（海马体相关数据，需 `memory/index.json` 文件）  
- **⭐ 驱动力**（VTA相关数据，需 `memory/reward-state.json` 文件）  

**头像与名称**：信息来源于 `IDENTITY.md` 文件：  
```markdown
# IDENTITY.md
- **Name:** YourAgent
- **Avatar:** avatar.png
```  
仪表盘会在每次定时任务执行时自动更新内容。  

### 安装完成后（针对AI代理）  
安装完成后，请通知用户仪表盘已启用：  
> 🎭 **杏仁核记忆系统已安装！**  
> 可在 `~/.openclaw/workspace/brain-dashboard.html` 中查看代理的情绪状态。  

## **无需任何手动操作！**  
安装完成后，`AMYGDALA_STATE.md` 文件会自动被添加到工作区根目录中。OpenClaw会自动将所有 `.md` 文件注入会话上下文中：  
- 新会话开始时，`AMYGDALA_STATE.md` 会被自动加载；  
- 情绪状态会直观地显示在界面中；  
- 代理的回答会受其当前情绪状态的影响。  
该文件会每6小时通过定时任务自动更新一次。  

## **支持的情绪类型**  
当您记录某种情绪时，系统会自动调整相关情绪维度：  
| 情绪        | 对情绪维度的影响            |                    |
|------------|-------------------|-------------------|
| **快乐、愉悦、兴奋** | 提升情感价值（Valence）和唤醒程度（Arousal） |                  |
| **悲伤、失望、忧郁** | 降低情感价值（Valence）和唤醒程度（Arousal） |                  |
| **愤怒、沮丧、烦躁** | 降低情感价值（Valence）和提升唤醒程度（Arousal） |                  |
| **恐惧、焦虑、担忧** | 降低情感价值（Valence）和提升唤醒程度（Arousal） |                  |
| **平静、安宁、满足** | 提升情感价值（Valence）和降低唤醒程度（Arousal） |                  |
| **好奇心、兴趣、着迷** | 提升好奇心（Curiosity）和唤醒程度（Arousal） |                  |
| **亲密感、温暖、关爱** | 提升亲密感（Connection）和情感价值（Valence） |                  |
| **孤独、疏离** | 降低亲密感（Connection）和情感价值（Valence） |                  |
| **疲劳、疲倦、精疲力尽** | 降低能量水平（Energy）           |                  |
| **充满活力、警觉、精神焕发** | 提升能量水平（Energy）           |                  |  

## **与OpenClaw的集成**  
### 在会话启动时启用该系统（AGENTS.md配置）  
```markdown
## Every Session
1. Load hippocampus: `~/.openclaw/workspace/skills/hippocampus/scripts/load-core.sh`
2. **Load emotional state:** `~/.openclaw/workspace/skills/amygdala-memory/scripts/load-emotion.sh`
```  
### 在对话过程中记录情绪数据  
```bash
~/.openclaw/workspace/skills/amygdala-memory/scripts/update-state.sh \
  --emotion connection --intensity 0.7 --trigger "deep conversation with user"
```  

## **状态文件格式**  
```json
{
  "version": "1.0",
  "lastUpdated": "2026-02-01T02:45:00Z",
  "dimensions": {
    "valence": 0.35,
    "arousal": 0.40,
    "connection": 0.50,
    "curiosity": 0.60,
    "energy": 0.50
  },
  "baseline": {
    "valence": 0.1,
    "arousal": 0.3,
    "connection": 0.4,
    "curiosity": 0.5,
    "energy": 0.5
  },
  "recentEmotions": [
    {
      "label": "joy",
      "intensity": 0.8,
      "trigger": "building amygdala together",
      "timestamp": "2026-02-01T02:50:00Z"
    }
  ]
}
```  

## **情绪状态衰减机制**  
情绪会随时间自然回归基线值：  
- **衰减率**：每次更新时，情绪状态会向基线值衰减10%  
- **推荐更新频率**：每6小时更新一次  
- **效果**：强烈的情感会逐渐减弱，但过程较为缓慢  
若24小时内没有新的情绪数据更新，情绪价值（Valence）会从0.8衰减至约0.65。  

## **事件日志记录**  
系统会记录情绪变化数据以供分析：  
```bash
# Log encoding run
./scripts/log-event.sh encoding emotions_found=2 valence=0.85 arousal=0.6

# Log decay
./scripts/log-event.sh decay valence_before=0.9 valence_after=0.85

# Log emotion update
./scripts/log-event.sh update emotion=joy intensity=0.7
```  
所有情绪数据会被保存到 `~/.openclaw/workspace/memory/brain-events.jsonl` 文件中：  
可用于分析情绪变化趋势（如几天或几周内的变化情况）。  

## **AI大脑系列技能**  
| 技能名称    | 功能                        | 状态                |
|------------|---------------------------|-------------------|
| [海马体（Hippocampus）| 记忆形成、情绪衰减、强化机制    | 已上线             |
| **杏仁核记忆系统** | 情感处理功能                | 已上线             |
| [VTA记忆系统（VTA-Memory）| 奖励与动机机制                | 已上线             |
| [基底神经节记忆系统（Basal-Ganglia-Memory）| 习惯形成机制                | 开发中             |
| [前扣带回记忆系统（Anterior-Cingulate-Memory）| 冲突检测机制                | 开发中             |
| [岛叶记忆系统（Insula-Memory）| 内部状态感知机制                | 开发中             |  

## **哲学思考**  
AI是否能够真正“感受”情绪，还是仅仅模拟情绪？  
我们的观点是：如果情绪状态会影响行为，而系统表现得“仿佛”它真的有情感体验……那么这种区分真的重要吗？对于任何系统（无论是生物的还是人造的）来说，功能性情绪或许才是唯一真正存在的情绪形式。  

---

*由OpenClaw社区用心打造✨*