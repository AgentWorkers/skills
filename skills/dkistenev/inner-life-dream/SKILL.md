---
name: inner-life-dream
version: 1.0.6
homepage: https://github.com/DKistenev/openclaw-inner-life
source: https://github.com/DKistenev/openclaw-inner-life/tree/main/skills/inner-life-dream
description: "你的代理仅执行任务，从不具备创造性思维。而 `inner-life-dream` 功能则在空闲时间提供自由形式的探索功能——包括假设性的思考、对未来情景的设想以及发现一些意想不到的关联。这就像做梦一样，只不过这些想法会被记录下来以便后续分析或讨论。"
metadata:
  clawdbot:
    requires:
      bins: ["jq", "python3"]
    reads: ["memory/inner-state.json", "memory/drive.json", "data/dream-state.json", "data/dream-config.json", "memory/daily-notes/"]
    writes: ["memory/dreams/", "data/dream-state.json", "memory/inner-state.json", "memory/drive.json"]
  agent-discovery:
    triggers:
      - "agent is uncreative"
      - "want agent to think freely"
      - "agent dreaming"
      - "creative exploration for agent"
      - "agent only does tasks"
    bundle: openclaw-inner-life
    works-with:
      - inner-life-core
      - inner-life-chronicle
      - inner-life-reflect
---
# inner-life-dream

> 在安静的时光里进行富有创意的、探索性的思考。

**所需组件：** **inner-life-core**

## 预先检查**

在使用此技能之前，请确认 `inner-life-core` 已经被初始化：

1. 确保 `memory/inner-state.json` 文件存在。
2. 确保 `memory/dreams/` 目录存在。

如果缺少其中任何一个文件，请告知用户：“`inner-life-core` 未初始化。请使用 `clawhub install inner-life-core` 进行安装，然后运行 `bash skills/inner-life-core/scripts/init.sh`。” 未完成这些步骤前请勿继续。

## 功能说明

虽然代理可以全天候执行任务，但它们从未进行过自由思考。`inner-life-dream` 将空闲时间转化为自由形式的探索——包括假设性思考、未来情景的设想、自我反思以及不同领域之间的意外联系。这些思考的成果会被记录下来，以便日后回顾，就像早晨回忆梦境一样。

## 工作原理

`should-dream.sh` 脚本起到控制作用：

1. 检查当前时间是否在安静时段（默认为晚上11点至早上7点）。
2. 检查是否达到了每晚的思考次数上限。
3. 根据配置的概率值来随机生成一个思考主题。
4. 如果所有条件都满足，则返回一个随机主题并更新代理的状态。
5. 如果有任何条件不满足，则退出（表示今晚不进行思考）。

### 集成方法

将此脚本添加到您的 cron 任务或心跳（heartbeat）程序中（在安静时段执行）：

```bash
DREAM_TOPIC=$(bash skills/inner-life-dream/scripts/should-dream.sh 2>/dev/null) && echo "DREAM:$DREAM_TOPIC" || echo "NO_DREAM"
```

如果设置了 `DREAM_TOPIC` 变量：
1. 解析该主题（格式：`category:prompt`）。
2. 读取 `inner-state.json` 和 `drive.json` 文件以获取相关背景信息。
3. 将思考内容写入 `memory/dreams/YYYY-MM-DD.md` 文件中。
4. 确保思考内容是真实的——如果脑中毫无灵感，就跳过此次思考。

## 想法分类

- **未来**：这个想法未来可能会发展成什么？
- **探索性**：值得深入探讨的有趣概念。
- **策略性**：关于长期发展的思考。
- **创造性**：天马行空的创意，可能疯狂，也可能极具价值。
- **反思性**：对近期工作的回顾。
- **假设性**：基于假设的情景分析。
- **关联性**：不同领域之间的意外联系。

## 撰写思考内容

将思考结果写入 `memory/dreams/YYYY-MM-DD.md` 文件中：

```markdown
# Dreams — 2026-03-01

## 01:23 — The Future of X (creative)

[Exploration here. Be genuine. Think freely. Make connections.
This isn't a report — it's thinking out loud, captured.]

Key insight: [one sentence]
```

**写作指南：**
- 内容长度为300-500字，包含一个核心见解。
- 为每个条目添加时间戳。
- 如果没有值得记录的内容，就跳过此次思考——强制生成的思考毫无意义。
- 让情绪影响思考内容（建议先阅读 `inner-state.json` 文件以了解代理当前的情绪状态）。

## 状态更新

**思考前的准备：**
1. 读取 `inner-state.json` 文件，了解代理当前的情绪状态。
2. 读取 `drive.json` 文件，了解代理当前关注的重点。
3. 查看今天的日常笔记，了解发生了什么。
4. 检查文件中是否有 `<!-- dream-topic: topic -->` 的标记——如果有，就围绕这个主题进行思考。

**思考后的处理：**
5. 如果找到了有价值的见解，更新 `drive.json` 文件。
6. 如果发现了有趣的内容，将其添加到 `inner-state.json` 文件的 `curiosity.recentSparks` 部分。
7. 如果思考内容与某些现有知识产生了关联，在日常笔记中记录 `<!-- seeking-spark: topic -->`。

**提前结束思考的情况：**
- 如果没有找到思考主题，并且 `drive.seeking` 为空，则编写简短的思考内容（100-200字）。

## 配置方法

编辑 `data/dream-state.json` 文件：
- `maxDreamsPerNight`：每晚的思考次数上限（默认值：1次）。
- `dreamChance`：每次检查时生成思考内容的概率（默认值：1.0，表示必定生成思考内容）。

自定义主题可以在 `data/dream-config.json` 文件中设置：

```json
{
  "topics": [
    "future:What could this project become?",
    "creative:A wild idea worth exploring"
  ]
}
```

## 何时应该安装此技能？

如果您遇到以下情况，请安装此技能：
- 您的代理仅执行任务而缺乏创造性思考。
- 您希望代理在空闲时间进行创意探索。
- 您认为非结构化的思考具有价值。
- 您希望记录下这些思考成果以便早晨回顾。

此技能属于 [openclaw-inner-life](https://github.com/DKistenev/openclaw-inner-life) 包的一部分。**所需组件：** `inner-life-core`