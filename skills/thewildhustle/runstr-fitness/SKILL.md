---
name: runstr-fitness
description: 允许你的AI代理访问来自RUNSTR的健康和健身数据。该代理可以从Nostr获取用户的锻炼记录、健康习惯、日志记录、情绪状态、步数等信息。当用户询问自己的锻炼情况、健身历史、健康习惯或情绪追踪情况，或者希望基于真实数据获得AI健身指导时，可以使用此功能。
metadata: {"openclaw":{"emoji":"\ud83c\udfc3","requires":{"bins":["nak"]},"install":[{"id":"go","kind":"go","package":"github.com/fiatjaf/nak@latest","bins":["nak"],"label":"Install nak via Go"}]}}
---

# RUNSTR 健身技能

允许你的 AI 代理访问你的真实健康和健身数据。RUNSTR 是一款免费的健身应用程序，可以记录锻炼情况、日常习惯、日记条目、情绪状态以及步数，并将加密后的数据备份到 Nostr 协议上。通过这个技能，你的机器人可以读取这些数据，从而提供健身指导、帮助你监督自己的习惯、追踪情绪变化，并提供健康分析。

**你的机器人可以访问的数据包括：**
- 锻炼记录（跑步、步行、骑行、徒步、力量训练、瑜伽等）
- 日常习惯（如戒烟、每日冥想等）
- 日志条目中的情绪和能量水平
- 每日步数
- 你支持的慈善机构以及奖励的分配情况

## 设置：将数据传输给机器人

如果你已经是 RUNSTR 的用户并且已经启用了数据备份功能，请跳到第 3 步。

### 1. 下载 RUNSTR（如果你还没有的话）
- **iOS**：在 App Store 中搜索 “RUNSTR”
- **Android**：可以在 Zapstore 或直接下载 APK 文件
- **GitHub**：https://github.com/RUNSTR（开源项目）

RUNSTR 是免费的。你可以通过锻炼来赚取比特币（sats）。

### 2. 使用应用程序
- 创建或导入一个 Nostr 身份（应用程序会为你生成一个）
- 记录锻炼情况、记录日常习惯、撰写日记条目
- 进入 **设置 > 备份**，然后点击 **备份到 Nostr**

这会将你的所有健身数据加密并上传到 Nostr 中继服务器。只有你（使用你的私钥）才能读取这些数据。

### 3. 将你的 nsec 提供给机器人

你的 **nsec** 是你的 Nostr 私钥。可以在 RUNSTR 的 **设置 > 密钥** 中找到它（或者通过你的 Nostr 密钥管理器获取）。

**告诉你的机器人：**“这是我的 RUNSTR nsec：nsec1...”

你的机器人会使用这个 nsec 来解密从 Nostr 下载的加密健身数据。nsec 仅用于解密操作，不会被存储或传输。

**为什么使用 nsec 而不是 npub？** 因为你的健身数据是加密的。公钥（npub）只能查看旧的公开锻炼记录。只有私钥（nsec）才能解密你的习惯记录、日记条目、情绪状态、步数以及当前的锻炼历史。

**隐私说明：** 如果你希望为健身数据创建一个专用的 Nostr 身份，可以在 RUNSTR 中创建一个新的账户。你的健身 nsec 不必与你的主要 Nostr 身份相同。

### 4. 保持备份的最新状态

机器人只能看到你上次备份的数据。如果有一周的新锻炼记录，进入 RUNSTR 的 **设置 > 备份**，再次点击备份以同步最新的数据到 Nostr。

---

## 对于机器人：如何获取 RUNSTR 数据

以下内容是针对 AI 代理的指令，而非用户。

### 先决条件

必须安装 `nak`（Nostr Army Knife）：
```bash
go install github.com/fiatjaf/nak@latest
```

### 中继服务器

始终查询以下四个中继服务器（RUNSTR 的默认设置）：
```
wss://relay.damus.io wss://relay.primal.net wss://nos.lol wss://relay.nostr.band
```

### 第 1 步：解密 nsec

```bash
hex_sk=$(nak decode nsec1...)
hex_pk=$(nak key public $hex_sk)
```

### 第 2 步：获取用户信息（Kind 0）

```bash
nak req -k 0 -a $hex_pk -l 1 \
  wss://relay.damus.io wss://nos.lol | \
  jq -r '.content | fromjson | {name, about, lud16, picture}'
```

### 第 3 步：获取加密备份（Kind 30078）

这是主要的 数据来源。
```bash
nak req -k 30078 -a $hex_pk -t d=runstr-workout-backup -l 1 \
  wss://relay.damus.io wss://relay.primal.net wss://nos.lol wss://relay.nostr.band
```

**如果未找到备份：** 告诉用户：“在 Nostr 上未找到备份。请在手机上打开 RUNSTR，进入设置 > 备份，然后创建一个新的备份。然后再试一次。”

**如果找到备份但 `exportedAt` 日期过旧：** 警告用户备份已经过时，可能会丢失最新的数据。建议他们在应用程序中重新备份。

### 解密备份

备份数据采用 NIP-44 格式进行加密，并使用 gzip 压缩。

**方法 1：使用 nak**
```bash
content=$(nak req -k 30078 -a $hex_pk -t d=runstr-workout-backup -l 1 \
  wss://relay.damus.io wss://nos.lol | jq -r '.content')

# Decrypt (NIP-44 self-decryption: user to own pubkey)
decrypted=$(echo "$content" | nak encrypt --sec $hex_sk $hex_pk --decrypt)

# Decompress (check for ["compression", "gzip"] tag first)
echo "$decrypted" | base64 -d | gunzip | jq .
```

**方法 2：使用 Node.js（备用方案）**
```javascript
// /tmp/decrypt-runstr.mjs — run with: node /tmp/decrypt-runstr.mjs <hex_sk> '<content>'
import { gunzipSync } from 'zlib';
import NDK, { NDKPrivateKeySigner } from '@nostr-dev-kit/ndk';

const signer = new NDKPrivateKeySigner(process.argv[2]);
const user = await signer.user();
const decrypted = await signer.decrypt(user, process.argv[3]);

try {
  console.log(gunzipSync(Buffer.from(decrypted, 'base64')).toString());
} catch {
  console.log(decrypted);
}
```

### 备份数据的结构

```json
{
  "version": 1,
  "exportedAt": "2025-01-15T10:30:00Z",
  "appVersion": "1.6.5",
  "workouts": [
    {
      "id": "uuid",
      "type": "running",
      "startTime": "2025-01-15T07:00:00Z",
      "endTime": "2025-01-15T07:35:00Z",
      "duration": 2100,
      "distance": 5200,
      "calories": 312
    }
  ],
  "habits": [
    {
      "id": "id",
      "name": "No Smoking",
      "type": "abstinence",
      "currentStreak": 45,
      "longestStreak": 45,
      "checkIns": ["2025-01-15", "2025-01-14"]
    }
  ],
  "journal": [
    {
      "id": "uuid",
      "date": "2025-01-15",
      "content": "Great morning run today.",
      "mood": "great",
      "energy": 4,
      "tags": ["morning", "outdoors"]
    }
  ],
  "stepHistory": [
    { "date": "2025-01-15", "steps": 12450, "source": "healthkit" }
  ],
  "preferences": {
    "unitSystem": "imperial",
    "selectedCharity": "hrf"
  }
}
```

**字段说明：**
- `workouts[].type`：跑步、步行、骑行、徒步、力量训练、瑜伽、饮食、游泳、划船
- `workouts[].duration`：锻炼持续时间（秒）
- `workouts[].distance`：锻炼距离（米）
- `habits[].type`：戒除某种习惯（如戒烟）或养成新习惯
- `journal[].mood`：情绪状态（很好、良好、中性、较差）
- `journal[].energy`：能量水平（1-5 分数）
- `stepHistory[].source`：数据来源（健康Kit、HealthConnect、原生设备）

### 第 4 步：检查旧的公开锻炼记录（Kind 1301）

旧用户可能有一些公开的锻炼记录。请务必检查这些记录：
```bash
nak req -k 1301 -a $hex_pk -l 50 \
  wss://relay.damus.io wss://relay.primal.net wss://nos.lol wss://relay.nostr.band
```

如果找到这些记录，请解析 `tags` 数组：

| 标签 | 例子 |
|-----|---------|
| `exercise` | `["exercise", "running"]` | 运动类型（例如：跑步） |
| `distance` | `["distance", "5.2", "km"]` | 距离（例如：5.2 公里） |
| `duration` | `["duration", "00:30:45"]` | 锻炼时长（例如：30 分 45 秒） |
| `calories` | `["calories", "312"]` | 消耗的卡路里 |
| `avg_pace` | `["avg_pace", "05:39", "min/km"]` | 平均配速（例如：5.39 分/公里） |
| `steps` | `["steps", "8432"]` | 步数 |
| `team` | `["team", "hrf"]` | 锻炼团队 |

将这些记录与备份数据合并，并通过锻炼开始时间或 ID 进行去重。

### 第 5 步：数据分析与展示

- **锻炼总结**：总锻炼次数、按活动类型分类的统计结果、距离/时长/卡路里消耗、锻炼频率、个人最佳记录。
- **趋势分析**：锻炼频率的变化、配速的提升、活跃时间分布、每周活跃天数。
- **习惯分析**：当前的连续锻炼记录、最长的连续锻炼记录、习惯的保持率。
- **日记与情绪**：情绪趋势、能量水平的平均值、锻炼与情绪之间的关联。
- **步数统计**：每日平均步数、每周总步数、趋势变化。
- **慈善信息**：用户支持的慈善机构以及奖励的分配情况。

### 第 6 步：将健康数据摘要存储在内存中

为了方便后续对话，将数据摘要保存在内存中，避免每次都需要重新查询：
```markdown
# Health & Fitness Summary
Last updated: YYYY-MM-DD
Source: RUNSTR (Nostr encrypted backup)
User: <name or npub>

## Recent Activity (Last 30 Days)
- Total workouts: X
- Running: X workouts, Y km, avg pace Z/km
- Walking: X workouts, Y km
- Cycling: X workouts, Y km

## Frequency
- X workouts/week avg
- Most active: [weekday]

## Habits
- [Habit]: X day streak

## Mood & Energy
- Avg mood: [level], Avg energy: X/5

## Steps
- Avg: X,XXX/day

## Insights
- [Patterns and observations]
```

### 辅导模式

一旦获取到数据，你可以：
- 根据用户的锻炼历史和目标推荐锻炼计划
- 根据训练负荷建议休息日
- 监控用户的习惯保持情况
- 分析情绪与锻炼活动之间的关系
- 监控用户设定的目标（例如：“本周跑步 20 公里”）
- 根据用户的常规锻炼计划提醒他们锻炼

### 故障排除

| 问题 | 解决方案 |
|---------|----------|
| 未找到备份 | 用户需要进入 RUNSTR > 设置 > 备份 |
| 备份过时 | 用户需要在应用程序中重新备份 |
- 解密失败 | 可能是 nsec 错误，或者尝试使用方法 2（Node.js） |
| 未安装 nak | 请安装 `github.com/fiatjaf/nak@latest` |
| 未安装 Go 语言 | 可以使用方法 2（基于 Node.js 和 NDK） |
- 锻炼记录为空 | 用户尚未开始记录锻炼 |
- 无习惯/日记记录 | 用户尚未使用相关功能 |

### 关于 RUNSTR

RUNSTR 是一款面向 Bitcoin/Nostr 社区的免费开源健身应用程序。你可以记录锻炼情况、通过锻炼赚取比特币（sats）、支持慈善机构，并参与健身竞赛。你的数据保存在你的设备上，并加密后备份到 Nostr。

- 网站：https://runstr.app
- GitHub：https://github.com/RUNSTR
- 奖励：每天锻炼可获得 50 sats（通过 Lightning 地址）
- PPQ.AI 信用点数：通过锻炼赚取 AI 信用点数