---
name: dreaming
version: 1.0.1
description: 在安静的时光里进行创造性探索。将代理的空闲时间转化为自由发挥的思考过程——包括提出各种假设、设想未来可能发生的情况、进行反思，以及发现意想不到的关联。当你希望代理在活动较少的时候能够做一些有意义的事情（而不仅仅是简单地返回“HEARTBEAT_OK”状态）时，可以使用这个功能。生成的思考内容会被写入文件中，供日后人类查看（就像早晨回忆梦境一样）。
metadata:
  openclaw:
    requires:
      bins: ["jq"]
      anyBins: ["python3"]
---
# 梦想

在安静的时段进行富有创造性的、探索性的思考。这不是以任务为导向的工作，而是一种自由形式的联想性探索，其结果会被记录下来以便日后查看。

## 环境变量

| 变量 | 是否必需 | 默认值 | 说明 |
|----------|----------|---------|-------------|
| `WORKSPACE` | 否 | 技能的父目录（`scripts/..`） | 存放 `data/` 和 `memory/` 目录的根目录。可选——默认值为技能的父目录，这适用于标准的工作空间布局。 |

## 脚本写入的目录

该技能会将数据写入以下目录（相对于 `WORKSPACE`）：

- **`data/dream-state.json`** — 记录每晚的梦境次数和最后一次梦境的日期 |
- **`data/dream-config.json`** — 可选的自定义主题配置（由用户创建） |
- **`memory/dreams/YYYY-MM-DD.md`** — 梦境输出文件（由代理程序生成，而非脚本本身） |

## 设置

### 1. 配置安静时段和探索主题

编辑 `skills/dreaming/scripts/should-dream.sh` 脚本以自定义以下内容：

- **QUIET_START / QUIET_END** — 梦想可以进行的时段（默认：晚上11点至早上7点） |
- **TOPICS 数组** — 探索的主题类别（查看默认值以获取示例） |

### 2. 创建状态和输出目录

```bash
mkdir -p data memory/dreams
```

### 3. 添加到 HEARTBEAT.md 中

在安静时段，将以下内容添加到你的心跳（heartbeat）脚本中：

```markdown
## Dream Mode (Quiet Hours Only)

Check if it's time to dream:

\`\`\`bash
DREAM_TOPIC=$(./skills/dreaming/scripts/should-dream.sh 2>/dev/null) && echo "DREAM:$DREAM_TOPIC" || echo "NO_DREAM"
\`\`\`

**If DREAM_TOPIC is set:**

1. Parse the topic (format: `category:prompt`)
2. Write a thoughtful exploration to `memory/dreams/YYYY-MM-DD.md`
3. Keep it genuine — not filler. If the well is dry, skip it.
4. Append to the file if multiple dreams that night
```

## 工作原理

`skills/dreaming/scripts/should-dream.sh` 脚本的作用如下：

1. 检查当前时间是否在安静时段内 |
2. 检查是否已经达到了每晚的梦境次数上限 |
3. 根据配置的概率进行随机选择 |
4. 如果所有条件都满足：随机选择一个主题并更新状态 |
5. 如果有任何条件不满足：以非零状态退出（表示当晚没有生成梦境） |

状态信息存储在 `data/dream-state.json` 文件中：

```json
{
  "lastDreamDate": "2026-02-03",
  "dreamsTonight": 1,
  "maxDreamsPerNight": 1,
  "dreamChance": 1.0
}
```

## 记录梦境

当脚本选择一个主题后，将内容写入 `memory/dreams/YYYY-MM-DD.md` 文件中：

```markdown
# Dreams — 2026-02-04

## 01:23 — The Future of X (category-name)

[Your exploration here. Be genuine. Think freely. Make connections.
This isn't a report — it's thinking out loud, captured.]
```

**指南：**

- 每个梦境对应一个主题，需进行深入的思考和记录 |
- 为每个记录添加时间戳 |
- 如果一个晚上有多个梦境，可以追加记录 |
- 如果没有值得记录的内容，可以跳过本次记录——强制生成的梦境是没有意义的 |
- 这些记录供你后续阅读，就像阅读日记一样 |

## 自定义主题

**方法A：使用配置文件（推荐）** — 创建 `data/dream-config.json` 文件：

```json
{
  "topics": [
    "future:What could this project become?",
    "creative:A wild idea worth exploring",
    "reflection:Looking back at recent work"
  ]
}
```

```

This keeps your customizations outside the skill directory (safe for skill updates).

**Option B: Edit script directly** — Modify the `DEFAULT_TOPICS` array in `should-dream.sh`. Format: `category:prompt`

Default categories:

- `future` — What could [thing] become?
- `tangent` — Interesting technology or concepts worth exploring
- `strategy` — Long-term thinking
- `creative` — Wild ideas that might be crazy or brilliant
- `reflection` — Looking back at recent work
- `hypothetical` — What-if scenarios
- `connection` — Unexpected links between domains

Add domain-specific topics relevant to your work. The prompt should spark genuine exploration, not busywork.

## Tuning

In `data/dream-state.json`:

Add domain-specific topics relevant to your work. The prompt should spark genuine exploration, not busywork.

## Tuning

In `data/dream-state.json`:

- **maxDreamsPerNight** — cap on dreams per night (default: 1)
- **dreamChance** — probability per check (default: 1.0 = guaranteed if under limit)

Lower `dreamChance` for more sporadic dreaming. Raise `maxDreamsPerNight` for more prolific nights.
```