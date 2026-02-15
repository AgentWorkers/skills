---
name: soul-in-sapphire
description: 使用 Notion 的 OpenClaw 通用长期内存（LTM）操作（数据来源：2025-09-03）。这些操作用于持久化内存写入/搜索、情绪状态记录、日志写入，以及通过本地 JSON 预置文件实现模型控制的子代理生成计划。
metadata: {"openclaw":{"emoji":"💠","requires":{"bins":["node"],"env":["NOTION_API_KEY"]},"primaryEnv":"NOTION_API_KEY","dependsOnSkills":["notion-api-automation"],"localReads":["~/.config/soul-in-sapphire/config.json"],"optionalEnv":["NOTIONCTL_PATH"]}}
---

# soul-in-sapphire（Notion长期记忆管理工具）

使用此工具可在Notion中持久化存储和检索重要信息，并维护个人的情绪状态及日记记录。

## 核心功能（务必牢记）

该工具不仅仅是一个存储工具，其核心功能在于：

1. 记录工作中和交流中产生的重要情绪或状态变化。
2. 将这些变化作为持久化的记忆保存下来（而不仅仅是原始日志）。
3. 重新利用这些记忆来改进未来的判断和行为。

简而言之：记录 → 回忆 → 适应。其目标是实现持续性的成长，而非单纯增加存储量。

## 使用要求

- Notion访问令牌：`NOTION_API_KEY`（或`NOTION_TOKEN`）
- Notion API版本：`2025-09-03`
- 本地配置文件：`~/.config/soul-in-sapphire/config.json`
- 必需依赖的技能：`notion-api-automation`（`scripts/notionctl.mjs`通过本地子进程执行）
- 可选配置：`NOTIONCTL_PATH`（如果设置，则使用指定的notionctl路径，而非默认路径）

## 必需的Notion数据库及结构

在同一个父页面下创建（或让系统自动生成）以下数据库：

- `<base>-mem`（持久化记忆）
- `<base>-events`（工作/交流中的重要事件）
- `<base>-emotions`（产生的情绪）
- `<base>-state`（当前的情绪状态）
- `<base>-journal`（每日反思记录）

### 1) `<base>-mem`（持久化记忆）

用途：存储具有高重要性的长期记忆。

属性：
- `名称`（标题）
- `类型`（可选）：`decision`（决策）、`preference`（偏好）、`fact`（事实）、`procedure`（流程）、`todo`（待办事项）、`gotcha`（已理解的内容）
- `标签`（多选）
- `内容`（富文本）
- `来源`（URL，可选）
- `信心程度`（可选）：`high`（高）、`medium`（中等）、`low`（低）

### 2) `<base>-events`（重要事件）

用途：记录工作或交流中的关键触发点。

属性：
- `名称`（标题）
- `时间`（日期）
- `重要性`（可选）：`1..5`
- `触发原因`（可选）：`progress`（进展）、`boundary`（界限）、`ambiguity`（模糊性）、`external_action`（外部行动）、`manual`（手动触发）
- `上下文`（富文本）
- `来源`（可选）：`discord`（Discord）、`cli`（命令行）、`cron`（定时任务）、`heartbeat`（心跳事件）、`other`（其他）
- `链接`（URL，可选）
- `不确定性`（数值）
- `控制程度`（数值）
- `情绪关联`（关联到`<base>-emotions`数据库）
- `状态关联`（关联到`<base>-state`数据库）

### 3) `<base>-emotions`（情绪反应）

用途：为某个事件关联一种或多种情绪状态。

属性：
- `名称`（标题）
- `情绪维度`（可选）：`arousal`（兴奋）、`valence`（价值感）、`focus`（专注度）、`confidence`（信心）、`stress`（压力）、`curiosity`（好奇心）、`social`（社交需求）、`solitude`（孤独感）、`joy`（快乐）、`anger`（愤怒）、`sadness`（悲伤）、`fun`（乐趣）、`pain`（痛苦）
- `情绪强度`（数值）
- `备注`（富文本）
- `情绪权重`（数值）
- `身体反应`（多选）：`tension`（紧张）、`relief`（缓解）、`fatigue`（疲劳）、`heat`（热度）、`cold`（寒冷）
- `需求`（可选）：`safety`（安全需求）、`progress`（进步需求）、`recognition`（认可需求）、`autonomy`（自主需求）、`rest`（休息需求）、`novelty`（新奇需求）
- `应对方式`（可选）：`log`（记录）、`ask`（询问）、`pause`（暂停）、`act`（行动）、`defer`（推迟）
- `事件关联`（关联到`<base>-events`数据库）

### 4) `<base>-state`（事件后的状态快照）

用途：保存事件或情绪影响后的当前状态。

属性：
- `名称`（标题）
- `时间`（日期）
- `状态信息`（富文本）
- `原因`（富文本）
- `来源`（可选）：`event`（事件）、`cron`（定时任务）、`heartbeat`（心跳事件）、`manual`（手动触发）
- `情绪标签`（可选）：`clear`（平静）、`wired`（紧张）、`dull`（无聊）、`tense`（紧张）、`playful`（轻松）、`guarded`（谨慎）、`tender`（温柔）
- `意图`（可选）：`build`（建设）、`fix`（修复）、`organize`（整理）、`explore`（探索）、`rest`（休息）、`socialize`（社交）、`reflect`（反思）
- `需求层次`（数值）
- `需要避免的事物`（多选）：`risk`（风险）、`noise`（噪音）、`long_tasks`（长期任务）、`external_actions`（外部行动）、`ambiguity`（模糊性）
- `事件关联`（关联到`<base>-events`数据库）

### 5) `<base>-journal`（每日总结）

用途：记录每日的重要反思和周围环境信息。

属性：
- `名称`（标题）
- `时间`（日期）
- `正文`（富文本）
- `工作日志`（工作内容）
- `会议总结`（会议记录）
- `情绪标签`（可选）
- `意图`（可选）
- `未来计划`（未来目标）
- `世界动态`（周围新闻）
- `标签`（多选）
- `来源`（可选）：`cron`（定时任务）、`manual`（手动记录）

## 核心命令

### 1) 初始化设置

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

### 4) 情绪状态更新

```bash
cat <<'JSON' | node skills/soul-in-sapphire/scripts/emostate_tick.js
{
  "event": {"title":"..."},
  "emotions": [{"axis":"joy","level":6}],
  "state": {"mood_label":"clear","intent":"build","reason":"..."}
}
JSON
```

### 5) 日记记录

```bash
echo '{"body":"...","source":"cron"}' | node skills/soul-in-sapphire/scripts/journal_write.js
```

## 子代理生成计划（使用共享构建工具）

使用共享工具`subagent-spawn-command-builder`生成`sessions_spawn`所需的JSON数据。
请停止使用`soul-in-sapphire`的本地生成脚本。

- 模板：`skills/subagent-spawn-command-builder/state/spawn-profiles.template.json`
- 活动预设配置：`skills/subagent-spawn-command-builder/state/spawn-profiles.json`
- 使用方法：
  - 调用`subagent-spawn-command-builder`
  - 选择`heartbeat`或`journal`作为模板配置
  - 提供具体的任务内容

生成的JSON数据可直接用于`sessions_spawn`功能。

构建工具的日志文件：`skills/subagent-spawn-command-builder/state/build-log.jsonl`

## 运行注意事项：

- 仅记录具有高重要性的内容（避免保存完整的聊天记录）。
- 如果心跳事件仅包含评论信息，可以跳过情绪状态更新。
- 如果无论心跳事件如何都需要定期更新情绪状态，可以单独设置`emostate_tick.js`定时任务。