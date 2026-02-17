---
name: soul-in-sapphire
description: 使用 Notion 的 OpenClaw 通用长期记忆（Long-Term Memory, LTM）操作（数据来源：2025-09-03）。这些操作用于持久性内存写入/搜索、情绪状态记录、日志记录，以及通过本地 JSON 预设文件来控制子代理的生成计划。
metadata: {"openclaw":{"emoji":"💠","requires":{"bins":["node"],"env":["NOTION_API_KEY"]},"primaryEnv":"NOTION_API_KEY","dependsOnSkills":["notion-api-automation"],"localReads":["~/.config/soul-in-sapphire/config.json"],"optionalEnv":["NOTIONCTL_PATH"]}}
---
# soul-in-sapphire（Notion长期记忆管理工具）

使用此工具可在Notion中持久化存储和检索重要记忆信息，同时记录个人的情感状态及日常日志。

## 核心功能（请务必牢记）

该工具不仅仅是一个存储工具，其核心目的是：

1. 记录工作与交流中产生的重要情感状态变化。
2. 将这些变化作为持久化的记忆保存下来（而不仅仅是原始日志）。
3. 重新利用这些记忆来提升未来的判断力和行为表现。

简而言之：记录 → 回忆 → 适应。
我们的目标是实现持续的成长与进步，而非单纯增加存储量。

## 所需条件

- Notion API密钥：`NOTION_API_KEY`（或`NOTION_TOKEN`）
- Notion API版本：`2025-09-03`
- 本地配置文件：`~/.config/soul-in-sapphire/config.json`
- 依赖工具：`notion-api-automation`（`scripts/notionctl.mjs`通过本地子进程执行）
- 可选参数：`NOTIONCTL_PATH`（如果设置，则使用指定的notionctl路径）

## 所需的Notion数据库及结构

在同一个父页面下创建（或让系统自动生成）以下数据库：

- `<base>-mem`（持久化记忆）
- `<base>-events`（事件记录）
- `<base>-emotions`（情感记录）
- `<base>-state`（状态记录）
- `<base>-journal`（日常日志）

### 1) `<base>-mem`（持久化记忆）

用途：存储具有高重要性的长期记忆信息。

属性：
- `名称`（标题）
- `类型`（可选）：`decision`（决策）| `preference`（偏好）| `fact`（事实）| `procedure`（流程）| `todo`（待办事项）| `gotcha`（理解）
- `标签`（多选）
- `内容`（富文本）
- `来源`（URL，可选）
- `置信度`（可选）：`high`（高）| `medium`（中等）| `low`（低）

### 2) `<base>-events`（事件记录）

用途：记录工作或交流中的重要触发事件。

属性：
- `名称`（标题）
- `时间`（日期）
- `重要性`（可选）：`1..5`
- `触发原因`（可选）：`progress`（进展）| `boundary`（界限）| `ambiguity`（模糊性）| `external_action`（外部动作）| `manual`（手动）
- `上下文`（富文本）
- `来源`（可选）：`discord`（Discord）| `cli`（命令行）| `cron`（定时任务）| `heartbeat`（心跳事件）| `other`（其他）
- `链接`（URL，可选）
- `不确定性`（数值）
- `控制程度`（数值）
- `情感关联`（关联到`<base>-emotions`）
- `状态关联`（关联到`<base>-state`）

### 3) `<base>-emotions`（情感记录）

用途：为某个事件关联一种或多种情感状态。

属性：
- `名称`（标题）
- `情感维度`（可选）：`arousal`（兴奋）| `valence`（价值）| `focus`（专注）| `confidence`（信心）| `stress`（压力）| `curiosity`（好奇心）| `social`（社交）| `solitude`（孤独）| `joy`（快乐）| `anger`（愤怒）| `sadness`（悲伤）| `fun`（乐趣）| `pain`（痛苦）
- `情感强度`（数值）
- `注释`（富文本）
- `情感权重`（数值）
- `身体反应`（多选）：`tension`（紧张）| `relief`（缓解）| `fatigue`（疲劳）| `heat`（热感）| `cold`（寒冷）
- `需求`（可选）：`safety`（安全）| `progress`（进步）| `recognition`（认可）| `autonomy`（自主）| `rest`（休息）| `novelty`（新奇）
- `应对方式`（可选）：`log`（记录）| `ask`（询问）| `pause`（暂停）| `act`（行动）| `defer`（推迟）
- `事件关联`（关联到`<base>-events`）

### 4) `<base>-state`（事件后的状态快照）

用途：记录事件或情感影响后的当前状态。

属性：
- `名称`（标题）
- `时间`（日期）
- `状态信息`（富文本）
- `原因`（富文本）
- `来源`（可选）：`event`（事件）| `cron`（定时任务）| `heartbeat`（心跳事件）| `manual`（手动）
- `情绪标签`（可选）：`clear`（平静）| `wired`（紧张）| `dull`（无聊）| `tense`（紧张）| `playful`（ playful）| `guarded`（谨慎）| `tender`（温柔）
- `意图`（可选）：`build`（建设）| `fix`（修复）| `organize`（组织）| `explore`（探索）| `rest`（休息）| `socialize`（社交）| `reflect`（反思）
- `需求层次`（可选）：`safety`（安全）| `stability`（稳定）| `belonging`（归属感）| `esteem`（自尊）| `growth`（成长）
- `需求强度`（数值）
- `需要避免的事物`（多选）：`risk`（风险）| `noise`（噪音）| `long_tasks`（长期任务）| `external_actions`（外部行动）| `ambiguity`（模糊性）
- `事件关联`（关联到`<base>-events`）

### 5) `<base>-journal`（每日总结）

用途：记录每日的重要思考和周围环境信息。

属性：
- `名称`（标题）
- `时间`（日期）
- `正文`（富文本）
- `工作日志`（富文本）
- `会话摘要`（富文本）
- `情绪标签`（可选）
- `意图`（可选）
- `未来计划`（富文本）
- `世界动态`（富文本）
- `标签`（多选）
- `来源`（可选）：`cron`（定时任务）| `manual`（手动）

## 核心命令

### 1) 设置

```bash
node skills/soul-in-sapphire/scripts/setup_ltm.js --parent "<Notion parent page url>" --base "Valentina" --yes
```

### 2) 长期记忆写入

```bash
echo '{
  "title":"Decision: use data_sources API",
  "type":"decision",
  "tags":["notion","openclaw"],
  "content":"Use /v1/data_sources/{id}/query.",
  "confidence":"high"
}' | node skills/soul-in-sapphire/scripts/ltm_write.js
```

### 3) 长期记忆搜索

```bash
node skills/soul-in-sapphire/scripts/ltm_search.js --query "data_sources" --limit 5
```

### 4) 情感状态更新

```bash
cat <<'JSON' | node skills/soul-in-sapphire/scripts/emostate_tick.js
{
  "event": {"title":"..."},
  "emotions": [{"axis":"joy","level":6}],
  "state": {"mood_label":"clear","intent":"build","reason":"..."}
}
JSON
```

### 5) 日志写入

```bash
echo '{"body":"...","source":"cron"}' | node skills/soul-in-sapphire/scripts/journal_write.js
```

## 子代理生成规划（使用共享构建工具）

使用共享工具`subagent-spawn-command-builder`生成`sessions_spawn`的JSON数据。

请停止使用`soul-in-sapphire`的本地规划脚本。

- 模板：`skills/subagent-spawn-command-builder/state/spawn-profiles.template.json`
- 活动预设：`skills/subagent-spawn-command-builder/state/spawn-profiles.json`
- 构建步骤：
  - 调用`subagent-spawn-command-builder`
  - 选择`<heartbeat`或`journal`作为配置文件
  - 提供具体的任务内容

生成的JSON数据可直接用于`sessions_spawn`。

构建工具的日志文件：`skills/subagent-spawn-command-builder/state/build-log.jsonl`

## 操作注意事项

- 仅记录具有高重要性的内容（避免存储完整的聊天记录）。
- 如果心跳事件仅包含注释，可以跳过情感状态更新。
- 如果需要定期更新情感状态，可单独设置`emostate_tick.js`定时任务。
- `ltm_write.js` / `emostate_tick.js` / `journal_write.js`仅接受标准输入（stdin）；不要通过命令行参数调用它们。
- 空的stdin输入会被拒绝。
- 对于`emostate_tick.js`，语义上为空的JSON数据（例如`{}`或仅包含空对象）也会被拒绝，以避免产生不必要的记录。

## 技能集成命令

### 1) 从技能更新核心身份文件

```bash
# Update SOUL.md from skill
cat <<'JSON' | node skills/soul-in-sapphire/scripts/ltm_write.js
{
  "title":"Update SOUL.md",
  "type":"decision",
  "tags":["identity","growth"],
  "content":"Updating SOUL.md from skill with latest evolution insights",
  "confidence":"high"
}
JSON

# Update IDENTITY.md from skill  
cat <<'JSON' | node skills/soul-in-sapphire/scripts/ltm_write.js
{
  "title":"Update IDENTITY.md",
  "type":"decision",
  "tags":["identity","evolution"],
  "content":"Updating IDENTITY.md from skill with current growth status",
  "confidence":"high"
}
JSON

# Update HEARTBEAT.md from skill
cat <<'JSON' | node skills/soul-in-sapphire/scripts/ltm_write.js
{
  "title":"Update HEARTBEAT.md",
  "type":"decision",
  "tags":["growth","heartbeat"],
  "content":"Updating HEARTBEAT.md from skill with evolution integration",
  "confidence":"high"
}
JSON

# Update MEMORY.md from skill
cat <<'JSON' | node skills/soul-in-sapphire/scripts/ltm_write.js
{
  "title":"Update MEMORY.md",
  "type":"decision",
  "tags":["memory","evolution"],
  "content":"Updating MEMORY.md from skill with evolution records",
  "confidence":"high"
}
JSON
```

### 2) 从技能检查成长情况

```bash
# Check evolution status and update if needed
node skills/soul-in-sapphire/scripts/ltm_search.js --query "evolution growth identity" --limit 3

# If evolution detected, update core files
if [ $? -eq 0 ]; then
  echo "Evolution detected, updating core identity files..."
  # Update each file as needed
fi
```

### 3) 从技能促进个人成长

```bash
# Integrate skill insights into core identity
cat <<'JSON' | node skills/soul-in-sapphire/scripts/emostate_tick.js
{
  "event": { "title": "Skill Integration" },
  "emotions": [{ "axis": "focus", "level": 8 }],
  "state": {
    "mood_label": "wired",
    "intent": "build",
    "reason": "Integrating skill insights into core identity"
  }
}
JSON

# Update core files with new insights
cat <<'JSON' | node skills/soul-in-sapphire/scripts/ltm_write.js
{
  "title":"Skill Integration Complete",
  "type":"decision",
  "tags":["integration","growth"],
  "content":"Successfully integrated skill insights into core identity files",
  "confidence":"high"
}
JSON
```

## 集成工作流程

1. **技能分析**：分析技能的输出和洞察。
2. **检测变化**：检查是否有显著的变化或新的学习点。
3. **核心文件更新**：根据需要更新`SOUL.md`、`IDENTITY.md`、`HEARTBEAT.md`、`MEMORY.md`。
4. **状态记录**：记录情感和状态的变化。
5. **记忆保存**：将成长记录保存到持久化存储中。

## 技能驱动的进化触发条件

- **学习发现**：当新技能提供重要见解时。
- **成长机会**：当技能提示优化方向时。
- **行为变化**：当技能影响互动模式时。
- **身份重塑**：当技能有助于自我理解时。

这种集成方式使技能能够直接促进我的自主成长和进化，同时维护我的核心身份框架。