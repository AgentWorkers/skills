---
name: mingli
description: "**Mingli（命理）——多系统每日运势预测：**  
包括西方占星术（出生星盘+行星运行）、八字/四柱命理、数字命理学以及《易经》的解读。数据来源于 Kerykeion 和 astronomyapi.com，通过 Telegram 平台发送。"
version: 2.0.0
---

# Mingli 命理

这是一个多系统占卜服务，结合了西方占星术（Placidus宫位系统及精确的星象相位分析）、八字/四柱命理学、数字命理学（LifePath+个人周期分析）以及易经（六十四卦解析）。服务内容通过 Telegram 的定时任务（cron）每日自动推送，或根据用户需求即时提供。

## 使用模式

| 模式 | 描述 | 触发方式 |
|------|-------------|---------|
| **设置** | 输入出生日期、出生时间、出生地点（经纬度及时区），注册 Telegram 账号，并选择推送时间 | 输入 “set up my horoscope” |
| **每日更新** | 每日自动根据预设时间表推送四系统占卜结果 | 通过 cron 定时任务 |
| **即时查询** | 立即获取当前占卜结果 | 输入 “my horoscope” 或 “horoscope now” |
| **易经解析** | 随机或手动解析易经六十四卦 | 输入 “cast I Ching” 或 “throw hexagram” |
| **管理** | 暂停/恢复占卜服务或更改推送时间 | 输入 “pause horoscope” 或 “change horoscope time” |

## 所用脚本

```bash
# Western natal chart (kerykeion — houses, aspects, nodes)
.claude/skills/.venv/bin/python3 .claude/skills/mingli/scripts/calculate-western-natal-chart-using-kerykeion.py \
  --date 2000-03-25 --time 12:00 --tz "Asia/Saigon" --lat 21.0245 --lon 105.84117 --name "User"

# Ba-Zi Four Pillars + Western zodiac
.claude/skills/.venv/bin/python3 .claude/skills/mingli/scripts/calculate-bazi.py \
  --date 1990-05-15 --time 14:30 --tz "Asia/Saigon"

# Planetary positions (astronomyapi.com fallback for transit data)
.claude/skills/.venv/bin/python3 .claude/skills/mingli/scripts/fetch-planetary-positions.py \
  --lat 10.8231 --lon 106.6297

# Numerology — LifePath, Birthday, Attitude, Challenges, Pinnacles, Personal cycles
.claude/skills/.venv/bin/python3 .claude/skills/mingli/scripts/calculate-numerology.py \
  --date 2000-03-25

# I Ching hexagram casting
.claude/skills/.venv/bin/python3 .claude/skills/mingli/scripts/cast-i-ching-hexagram.py --mode random
.claude/skills/.venv/bin/python3 .claude/skills/mingli/scripts/cast-i-ching-hexagram.py \
  --mode manual --upper Kan --lower Kun --moving 2,1
```

### 设置模式

1. 用户需提供：出生日期（YYYY-MM-DD）、出生时间（HH:MM）、出生地点（经纬度及时区）。
2. 提供 Telegram 账号以及希望接收占卜结果的時間和时区。
3. 运行所有相关计算脚本：生成出生星盘、八字命盘和数字命盘数据。
4. 将结果保存至 `~/clawd/memory/horoscope-users.md` 文件中（包含用户的经纬度和 LifePath 数值）。
5. 创建每日自动执行的 cron 任务。
6. 确认用户的星座、Ascendant（上升点）、八字命盘中的“日主”、LifePath 数值以及推送时间。

### 每日更新模式

Cron 任务会触发四个脚本，将生成的 JSON 数据发送给大型语言模型（LLM），模型会整合这些数据生成完整的占卜结果，并通过 Telegram 发送给用户。

详细的使用提示请参考 `references/horoscope-prompt-template.md`。

### 即时查询模式

用户可通过输入 “my horoscope”、“horoscope now” 或 “what’s my horoscope today” 来获取当前的占卜结果。该模式会立即生成并发送占卜内容，不涉及单独的会话。

### 易经解析模式

用户可通过输入 “cast I Ching”、“throw hexagram” 或 “que Kinh Dich” 来请求易经解析：
- **随机解析**：使用三枚硬币的随机方法生成卦象。
- **手动输入**：用户需提供上卦和下卦的卦象，以及变动的卦线。
- 输出内容包括：主卦、变动卦线、卦象的解析结果以及 SPARK（占卜补充信息）。

## 管理命令

| 命令 | 功能 |
|---------|--------|
| “pause horoscope” | 暂停占卜服务的 cron 任务 |
| “resume horoscope” | 恢复占卜服务的 cron 任务 |
| “change horoscope time to 7am” | 将占卜结果的推送时间设置为早上 7 点 |
| “remove horoscope” | 删除对应的 cron 任务及存储的数据记录 |

## Cron 任务配置

每个用户对应一个 cron 任务，任务名称格式为 `horoscope-daily-{username}`。

```json
{
  "name": "horoscope-daily-{username}",
  "enabled": true,
  "schedule": { "kind": "cron", "expr": "0 {hour} * * *", "tz": "{timezone}" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "[prompt from references/horoscope-prompt-template.md]",
    "model": "claude-sonnet-4-20250514",
    "timeoutSeconds": 180,
    "deliver": true,
    "channel": "telegram",
    "to": "{telegram_chat_id}"
  },
  "isolation": { "postToMainPrefix": "Horoscope delivered", "postToMainMode": "summary" }
}
```

### 状态跟踪

系统使用 `state/users.json` 文件来记录用户的用户名与对应的 cron 任务 ID 的关联关系。

## 错误处理机制

- 如果 `kerykeion` 库使用失败，系统会回退到基于 API 的 `fetch-planetary-positions.py` 来生成占卜结果（此时不包含宫位信息）。
- 如果 API 服务不可用，系统将仅使用黄道带相关知识来生成占卜结果。
- 如果系统内存中缺少数据，系统会提示用户先完成初始设置。
- 如果易经解析所需的数据缺失，系统会使用内置的算法来生成卦象。

## 参考资料

- `references/astronomyapi-reference.md`：API 认证及相关接口说明。
- `references/zodiac-reference.md`：西方与中式生肖表、干支信息。
- `references/horoscope-prompt-template.md`：用于生成每日占卜提示的模板。
- `references/i-ching-64-hexagrams.json`：包含六十四卦的中文/越南文名称对照表。

## 所需依赖库/服务

- `kerykeion`（通过 pip 安装）：用于生成出生星盘、宫位和星象相位信息。安装命令：`pip install kerykeion`。
- `astronomyapi.com`：提供 API 访问所需的配置参数（`ASTRONOMY_APP_ID`、`ASTRONOMY_APP_SECRET`）。
- 其他所有脚本均基于 Python 标准库实现。