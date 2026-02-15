---
name: dreaming
description: 在安静的时段进行创造性探索。将代理的空闲时间转化为自由形式的思考——包括假设、未来场景的设想、个人反思以及意想不到的思维联系。当你希望代理在活动较少的时候做一些有意义的事情（而不仅仅是简单地返回“HEARTBEAT_OK”状态）时，可以使用此功能。思考的结果会被写入文件，供后续人工查阅（就像早晨回忆梦境一样）。
---

# 梦想时光

在安静的时光里，进行富有创造性的、探索性的思考。这不是以任务为导向的工作，而是自由形式的联想与探索，这些思考会被记录下来以供日后回顾。

## 设置

### 1. 配置安静时间与探索主题

编辑 `scripts/should-dream.sh` 文件以自定义以下内容：

- **QUIET_START / QUIET_END** — 梦想时间的开始和结束（默认：晚上 11 点至早上 7 点）
- **TOPICS 数组** — 探索的主题类别（查看默认值以获取示例）

### 2. 创建状态记录和输出目录

```bash
mkdir -p data memory/dreams
```

### 3. 添加到 HEARTBEAT.md 中

将以下内容添加到你的心跳（heartbeat）任务中（在安静时间执行）：

```markdown
## Dream Mode (Quiet Hours Only)

Check if it's time to dream:

\`\`\`bash
DREAM_TOPIC=$(./scripts/should-dream.sh 2>/dev/null) && echo "DREAM:$DREAM_TOPIC" || echo "NO_DREAM"
\`\`\`

**If DREAM_TOPIC is set:**

1. Parse the topic (format: `category:prompt`)
2. Write a thoughtful exploration to `memory/dreams/YYYY-MM-DD.md`
3. Keep it genuine — not filler. If the well is dry, skip it.
4. Append to the file if multiple dreams that night
```

## 工作原理

`should-dream.sh` 脚本起到以下作用：

1. 检查当前时间是否在安静时间内
2. 检查当天的梦想次数是否已达到上限
3. 根据配置的概率随机选择一个主题
4. 如果所有条件都满足，返回一个随机主题并更新状态
5. 如果有任何条件不满足，脚本将以非零状态退出（表示当天的梦想任务未完成）

状态信息记录在 `data/dream-state.json` 文件中：

```json
{
  "lastDreamDate": "2026-02-03",
  "dreamsTonight": 1,
  "maxDreamsPerNight": 1,
  "dreamChance": 1.0
}
```

## 记录梦想

当脚本返回一个主题后，将该主题写入 `memory/dreams/YYYY-MM-DD.md` 文件中：

```markdown
# Dreams — 2026-02-04

## 01:23 — The Future of X (category-name)

[Your exploration here. Be genuine. Think freely. Make connections.
This isn't a report — it's thinking out loud, captured.]
```

**编写梦想记录的指南**：

- 每个梦想对应一个主题，进行深入的思考
- 为每条记录添加时间戳
- 如果同一晚有多个想法，可以追加记录
- 如果没有值得记录的内容，可以跳过本次记录——强制进行的“梦想”是没有意义的
- 这些记录供你日后像阅读日记一样回顾

## 自定义探索主题

**选项 A：使用配置文件（推荐）** — 创建 `data/dream-config.json` 文件：
```json
{
  "topics": [
    "future:What could this project become?",
    "creative:A wild idea worth exploring",
    "reflection:Looking back at recent work"
  ]
}
```
这样可以将你的自定义设置放在技能目录之外，避免在技能更新时被覆盖。

**选项 B：直接修改脚本** — 修改 `should-dream.sh` 文件中的 `DEFAULT Tops` 数组。格式为：`类别: 提示语`

默认主题类别：

- `future` — [某事物] 未来可能发展成什么？
- `tangent` — 值得探索的有趣技术或概念
- `strategy` — 长期规划与思考
- `creative` — 可能疯狂或出色的创意想法
- `reflection` — 回顾近期工作
- `hypothetical` — 假设性场景
- `connection` — 不同领域之间的意外联系

根据你的工作添加相关主题。提示语应能激发真正的探索欲望，而不仅仅是机械性的写作。

## 调优

在 `data/dream-state.json` 文件中，可以添加与你的工作相关的主题。提示语应能激发真正的探索欲望，而不仅仅是机械性的写作。

- **maxDreamsPerNight** — 每晚的梦想记录上限（默认：1）
- **dreamChance** — 每次检查时选择主题的概率（默认：1.0 = 保证会选择一个主题）

降低 `dreamChance` 可以减少每晚的梦想记录次数；提高 `maxDreamsPerNight` 可以增加每晚的记录数量。