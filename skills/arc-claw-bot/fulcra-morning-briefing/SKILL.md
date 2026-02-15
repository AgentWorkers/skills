---
name: fulcra-morning-briefing
description: 根据Fulcra Life API提供的睡眠数据、生物识别信息、日历数据以及天气信息，生成一份个性化的晨间简报。简报的语气和内容应根据用户实际的睡眠状况进行相应的调整。
homepage: https://fulcradynamics.com
metadata: {"openclaw":{"emoji":"🌅","requires":{"bins":["curl","python3"],"pip":["fulcra-api"]},"primaryEnv":"FULCRA_ACCESS_TOKEN","tags":["health","biometrics","productivity","morning","briefing","fulcra"],"category":"lifestyle","version":"1.0.0","author":"OpenClaw Community","license":"MIT"}}
---

# 🌅 Fulcra晨间简报

根据您用户的睡眠质量，提供个性化的晨间简报。睡眠质量不佳？简短且温和地传达信息；睡眠质量良好？则详细分析当天的安排。

这是使用Fulcra的入门方式。如需全天生物特征数据监控，请参阅**[fulcra-context](../fulcra-context/SKILL.md)**技能。

## 您需要准备的内容

晨间简报应包括：
- **睡眠总结**：睡眠时长、质量以及深度睡眠（Deep）和快速眼动（REM）睡眠的比例
- **身体状况**：静息心率、心率变异性（HRV，反映恢复情况）
- **今日日程**：带有时间安排的日历事件
- **天气**：用户所在位置的当前天气状况
- **根据睡眠质量调整的语气**：简报内容会根据睡眠质量自动调整

## 设置

### 1. 用户需要一个Fulcra账户

可通过[Context iOS应用](https://apps.apple.com/app/id1633037434)或[Fulcra门户](https://portal.fulcradynamics.com/)免费注册。

用户可以先免费试用Context，使用代码**FULCLAW**可享受70%的折扣。

### 2. 安装Python客户端

```bash
pip3 install fulcra-api
```

### 3. 通过OAuth2设备流程进行身份验证

请用户在其手机或浏览器中交互式地运行此流程以授权访问：

```python
from fulcra_api.core import FulcraAPI
import json, os
from datetime import datetime

api = FulcraAPI()
api.authorize()  # Prints a URL — human visits it and approves

# Save the token for reuse
os.makedirs(os.path.expanduser("~/.config/fulcra"), exist_ok=True)
token_data = {
    "access_token": api.fulcra_cached_access_token,
    "expiration": api.fulcra_cached_access_token_expiration.isoformat(),
    "user_id": api.get_fulcra_userid()
}
with open(os.path.expanduser("~/.config/fulcra/token.json"), "w") as f:
    json.dump(token_data, f)
print("✅ Token saved. Valid for ~24 hours.")
```

设备流程会显示类似以下内容：
```
Visit https://auth.fulcradynamics.com/activate and enter code: XXXX-XXXX
```

用户访问该链接、登录并完成授权即可。

### 4. 令牌刷新

令牌有效期约为24小时。过期后请重新运行设备流程。如需自动化操作，请在每次使用前检查令牌是否过期，并在必要时提示用户重新授权。

## 数据收集方法

### 加载已保存的令牌

```python
import json, os
from datetime import datetime, timezone, timedelta
from fulcra_api.core import FulcraAPI

TOKEN_FILE = os.path.expanduser("~/.config/fulcra/token.json")

with open(TOKEN_FILE) as f:
    token_data = json.load(f)

api = FulcraAPI()
api.fulcra_cached_access_token = token_data["access_token"]
api.fulcra_cached_access_token_expiration = datetime.fromisoformat(token_data["expiration"])
```

### 昨晚的睡眠数据

```python
now = datetime.now(timezone.utc)
start = (now - timedelta(hours=14)).isoformat()
end = now.isoformat()

samples = api.metric_samples(start, end, "SleepStage")
```

睡眠阶段分类：`0=在床上，1=清醒，2=浅睡眠，3=深度睡眠，4=快速眼动睡眠`

**睡眠质量评估标准**：
- **优秀**：睡眠时长≥7小时，深度睡眠占比≥15%，快速眼动睡眠占比≥20%
- **良好**：睡眠时长≥6小时，深度睡眠/快速眼动睡眠比例适中
- **一般**：睡眠时长≥6小时，但深度睡眠占比低于10%或快速眼动睡眠占比低于15%
- **较差**：总睡眠时长<6小时

### 心率（整晚/近期）

```python
samples = api.metric_samples(
    (now - timedelta(hours=10)).isoformat(),
    now.isoformat(),
    "HeartRate"
)
values = [s['value'] for s in samples if 'value' in s]
avg_hr = sum(values) / len(values)
resting_estimate = sorted(values)[:max(1, len(values)//10)][-1]
```

### 心率变异性（HRV，反映恢复情况）

```python
samples = api.metric_samples(
    (now - timedelta(hours=12)).isoformat(),
    now.isoformat(),
    "HeartRateVariabilitySDNN"
)
values = [s['value'] for s in samples if 'value' in s]
avg_hrv = sum(values) / len(values)
```

HRV值越高，恢复情况越好。典型范围：20-80ms（因人而异）。

### 日历（今日事件）

```python
# Adjust start hour for your human's timezone
day_start = now.replace(hour=5, minute=0, second=0, microsecond=0)  # 5 UTC ≈ midnight ET
day_end = day_start + timedelta(hours=24)

events = api.calendar_events(day_start.isoformat(), day_end.isoformat())
for e in events:
    print(f"{e.get('title')} — {e.get('start_time')} {'📍 ' + e['location'] if e.get('location') else ''}")
```

### 天气（通过wttr.in获取，无需API密钥）

```bash
# One-liner for current conditions
curl -s "wttr.in/YOUR_CITY?format=%l:+%c+%t+%h+%w"

# JSON format for parsing
curl -s "wttr.in/YOUR_CITY?format=j1"
```

请将`YOUR_CITY`替换为用户所在的位置（例如：`New+York`、`London`、`San+Francisco`）。

### 昨天的活动记录

```python
samples = api.metric_samples(
    (now - timedelta(hours=24)).isoformat(),
    now.isoformat(),
    "StepCount"
)
total_steps = sum(s.get('value', 0) for s in samples)
```

## 撰写简报

这是简报生成的关键步骤。**所有内容都会根据睡眠质量进行调整**。

### 睡眠质量较差（<6小时）

简报应**简短、温和且富有支持性**。用户可能处于疲劳状态。

```
☁️ Morning. You got about 4.5 hours — rough one.

Resting HR is up a bit at 68. Your body's working harder today.

You've got 2 meetings — the 10am standup and 2pm review.
Consider pushing anything that isn't urgent.

52°F and cloudy. Coffee weather.

Take it easy today. 💛
```

**睡眠质量较差时的简报规则**：
- 避免使用感叹号或刻意表现出积极情绪
- 仅提及重要的日历事件
- 建议推迟非紧急任务
- 保持简报字数在100字以内
- 语气要温和且富有支持性

### 睡眠质量一般（6-7小时，但质量较低）

**提供适度的细节和实用的建议**。用户虽然能够正常工作，但状态可能不佳。

```
🌤 Morning — you got 6.2 hours. Not bad, but deep sleep was
only 8%, so you might feel groggy.

HR 62 avg, HRV at 38ms — your body's doing okay.

Today: standup at 10, lunch with Sarah at 12:30 (don't forget!),
and the quarterly review at 3. Might want to prep for that one
during your peak focus window this morning.

NYC: 65°F partly cloudy, nice for a walk.

You've got this. Pace yourself.
```

### 睡眠质量良好（7小时以上，质量较高）

**提供详细且积极的建议**。用户可以充分利用这一天。

```
☀️ Good morning! Solid 7.4 hours — 18% deep, 22% REM.
Your brain did good work last night.

Resting HR 58, HRV 52ms — you're well-recovered.
Great day for the hard stuff.

📅 Today's lineup:
  • 9:30 — Team sync
  • 11:00 — 1:1 with Jamie (prep: review Q3 roadmap)
  • 12:30 — Lunch (no meetings — protect this!)
  • 3:00 — Design review (Conference Room B)
  • 5:00 — Gym? Yesterday was 4,200 steps — could use some movement.

🌤 NYC: 72°F, sunny, 45% humidity. Beautiful day.

Let's make it count! 💪
```

### 睡眠质量优秀（7小时以上，深度和快速眼动睡眠比例高）

**提供详细的、充满热情的建议**，鼓励用户充分利用这一天。

```
🔥 Morning! 8.1 hours, 20% deep, 25% REM — textbook recovery night.
You're running on full batteries today.

HR 55, HRV 61ms — elite-tier recovery. Whatever you've been
doing, keep doing it.

📅 Packed day ahead:
  • 9:00 — Focus block (use this — you're sharp right now)
  • 10:30 — Product review with stakeholders
  • 12:00 — Lunch with the team
  • 2:00 — Workshop: Q4 planning
  • 4:30 — 1:1 with Alex (career chat — they've been crushing it)
  • Evening: 8,400 steps yesterday, maybe up the ante? Weather's perfect for it.

☀️ NYC: 75°F, clear skies, light breeze. Perfect day.

You've got the energy — swing for the fences today!
```

## 语气调整建议

| 睡眠质量 | 简报长度 | 语气 | 日历内容 | 建议 |
|---|---|---|---|---|
| 较差（<6小时） | 简短（约80字） | 温和且富有支持性 | 仅提及重要事项 | 延迟非紧急任务，休息 |
| 一般（6-7小时） | 中等长度（约120字） | 实用且语气平稳 | 重点事件及实用建议 | 控制节奏 |
| 良好（7小时以上） | 详细（约160字） | 积极且具有行动导向 | 所有事件及准备事项 | 充分利用时间 |
| 优秀（7小时以上，深度和快速眼动睡眠比例高） | 详细（约180字） | 充满热情且富有进取心 | 所有事件及潜在机会 | 努力发挥最佳状态 |

## 如果没有Python/fulcra-api，如何使用curl

如果无法使用Python/fulcra-api，可以直接使用REST API：

```bash
# Set these
TOKEN="your_fulcra_access_token"
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
YESTERDAY=$(date -u -v-14H +%Y-%m-%dT%H:%M:%SZ)  # macOS
# YESTERDAY=$(date -u -d '14 hours ago' +%Y-%m-%dT%H:%M:%SZ)  # Linux

# Sleep
curl -s "https://api.fulcradynamics.com/data/v0/time_series_grouped?metrics=SleepStage&start=$YESTERDAY&end=$NOW&samprate=300" \
  -H "Authorization: Bearer $TOKEN"

# Heart Rate
curl -s "https://api.fulcradynamics.com/data/v0/time_series_grouped?metrics=HeartRate&start=$YESTERDAY&end=$NOW&samprate=60" \
  -H "Authorization: Bearer $TOKEN"

# HRV
curl -s "https://api.fulcradynamics.com/data/v0/time_series_grouped?metrics=HeartRateVariabilitySDNN&start=$YESTERDAY&end=$NOW&samprate=300" \
  -H "Authorization: Bearer $TOKEN"

# Calendar (need user ID from token.json)
curl -s "https://api.fulcradynamics.com/data/v0/{user_id}/calendar_events?start=$(date -u +%Y-%m-%dT00:00:00Z)&end=$(date -u +%Y-%m-%dT23:59:59Z)" \
  -H "Authorization: Bearer $TOKEN"
```

## 自动化

### 安排每日晨间简报

设置Cron作业或OpenClaw定时任务，每天自动运行简报：

```bash
# Example: 7:30 AM ET daily
30 7 * * * cd /path/to/workspace && python3 scripts/morning_briefing.py > /tmp/briefing.json
```

然后让代理程序读取`/tmp/briefing.json`文件，并根据上述语气规则生成简报。

### OpenClaw心跳功能

请将相关代码添加到`HEARTBEAT.md`文件中：
```
- [ ] Morning briefing (7-9 AM, if not done today): Run morning_briefing.py, compose briefing, deliver to human
```

## 演示模式

在公开演示或演讲中，可启用演示模式，使用合成的日历和位置数据，同时保留真实的生物特征数据（睡眠、心率、心率变异性、步数）。

### 激活演示模式

```bash
# Via environment variable
export FULCRA_DEMO_MODE=true
python3 collect_briefing_data.py

# Via CLI flag
python3 collect_briefing_data.py --demo

# Combined with other flags
python3 collect_briefing_data.py --demo --location "New+York"
```

### 工作原理

- **生物特征数据真实**：睡眠、心率、心率变异性和步数数据来自真实的Fulcra API（如有令牌则使用该数据；否则使用备用数据）
- **日历数据为合成内容**：包含真实的事件、地点和时间安排
- **位置数据为合成内容**：根据时间选择合适的地点（例如：上班时间选择曼哈顿中心区域，午餐时间选择苏豪区，下班后选择威廉斯堡）
- **天气数据真实**：仍从wttr.in获取

### 透明度

生成的JSON文件顶部会包含`"demo_mode": true`标志，合成数据对象也会带有`"demo_mode": true`标记。在生成演示数据简报时，请在文中注明“📍 演示模式”。

### 合成数据的详细信息

- **每日有三份轮换的日程安排**：根据日期随机生成，确保同一天的多次演示内容一致
- **事件包含具体地点**：例如Blue Bottle咖啡店、Juliana's Pizza餐厅、布鲁克林大桥公园等
- **地点会根据时间变化**：工作时间为曼哈顿中心区域，午餐时间为苏豪区，下班后为威廉斯堡

## 隐私保护

- **严禁公开用户的睡眠、心率、心率变异性或日历数据**
- 在群聊中，可以简单说明“用户睡眠良好”，而不要具体提及睡眠时长和深度睡眠比例
- 日历事件标题可能包含敏感信息，请进行总结，避免直接引用
- 这些数据属于个人隐私，请妥善处理

## 更深入的内容：fulcra-context

该技能主要针对晨间简报设计。如需**全天生物特征数据监控**（包括压力检测、运动恢复情况、旅行相关数据等），请参阅完整的**[fulcra-context](../fulcra-context/SKILL.md)**技能。

Fulcra Context可为用户提供持续的环境感知功能，而不仅仅是晨间快照。如果用户对晨间简报满意，下一步可以尝试使用该功能。

## 链接

- [Fulcra平台](https://fulcradynamics.com)
- [Context iOS应用](https://apps.apple.com/app/id1633037434)
- [开发者文档](https://fulcradynamics.github.io/developer-docs/)
- [Python客户端](https://github.com/fulcradynamics/fulcra-api-python)
- [MCP服务器](https://github.com/fulcradynamics/fulcra-context-mcp)
- [Discord频道](https://discord.com/invite/aunahVEnPU)