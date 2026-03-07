---
name: cricket-live-score
description: 为任何正在进行的T20或ODI比赛，将实时的板球比分更新（包括文字信息和语音备忘录）发送到Telegram。完全免费。
author: Amit Kulkarni
tags: cricket, sports, live-score, telegram, voice
dependencies: gTTS
env: TELEGRAM_BOT_TOKEN (optional — can also use --bot-token arg or OpenClaw config)
config: ~/.openclaw/openclaw.json (optional fallback for bot token)
---
# 🏏 板球实时比分更新

实时板球比分更新通过 Telegram 发送给您——同时提供可选的语音备忘录功能，让您无需查看屏幕即可随时了解比赛进度。该脚本从 Cricbuzz 网站抓取数据，无需设置任何 API 密钥即可获取比分信息。

支持 T20 和 ODI 比赛格式，自动识别参赛队伍、比赛局数以及所需的得分率。

脚本在后台运行，按照您设定的时间间隔发送更新，并在比赛结束时自动停止。

语音备忘录功能非常适合在驾驶或其他无法注视屏幕的情况下使用。

## 示例指令

**开始更新：**
- “发送印度对阵澳大利亚比赛的实时比分更新”
- “关注 IPL 比赛（RCB 对阵 CSK），每 3 分钟发送一次更新”
- “英格兰对阵巴基斯坦的 T20 比赛比分是多少？请随时告知我”

**使用语音备忘录：**
- “发送世界杯决赛的实时板球比分，并附带语音备忘录”
- “关注印度对阵南非的比赛，并提供语音更新——我正在开车”

**更改更新间隔：**
- “将更新间隔改为每 2 分钟”
- “将更新间隔改为每 10 分钟”

**停止更新：**
- “停止发送比分更新”
- “关闭板球比分更新服务”

## 适用场景

当用户需要实时比分更新、板球比分提醒或关注某场比赛时使用该脚本。

## 工作原理

1. **查找比赛对应的 Cricbuzz 网址**：搜索 `cricbuzz <队伍1> 对阵 <队伍2> 实时比分`，获取 `cricbuzz.com/live-cricket-scores/...` 的网址。
2. **在后台运行脚本**：

```bash
python3 <skill_dir>/scripts/cricket-live.py \
  --url "<cricbuzz_url>" \
  --chat-id "<telegram_chat_id>" \
  --bot-token "<telegram_bot_token>" \
  --interval 300 \
  --voice
```

3. 脚本会自动识别参赛队伍、比赛局数、比赛格式（T20/ODI）以及目标得分。
4. 按设定的时间间隔发送文本信息和语音备忘录，并在比赛结束时自动停止。

## 参数设置

| 参数 | 默认值 | 说明 |
|-------|---------|-------------|
| `--url` | 必需 | Cricbuzz 实时比分页面的网址 |
| `--chat-id` | 必需 | 发送更新的 Telegram 聊天频道 ID |
| `--bot-token` | 自动获取 | Telegram 机器人令牌。如未设置，则使用环境变量 `TELEGRAM_BOT_TOKEN` 或 OpenClaw 配置文件（`~/.openclaw/openclaw.json`）中的令牌 |
| `--interval` | 300 | 更新间隔（默认为 5 分钟） |
| `--voice` | 关闭 | 是否在每次更新时附带语音备忘录 |

## 分数更新内容示例

### 第二局（追赶局）
```
*India: 146/4 (15 ov)*
  🏏 Tilak Varma — 20 (15)
  🏏 Sanju Samson — 80 (40)

Need: 50 runs off 30 balls
RRR: 10.0 per over with 5.0 overs to go
Last wicket: Suryakumar Yadav c Rutherford b Joseph 18 (16)

🔹 WI innings: 195/4 (20 ov)
━━━━━━━━━━━━━━━━━
🏏 IND vs WI | ICC Men's T20 World Cup 2026

· Next update in 5 min
```

### 第一局
```
*West Indies: 120/3 (15 ov)*
  🏏 Rovman Powell — 25 (14)
  🏏 Jason Holder — 12 (8)

Run rate: 8.0 per over
Projected: 160
Last wicket: Shimron Hetmyer c Samson b Bumrah 22 (18)

━━━━━━━━━━━━━━━━━
🏏 IND vs WI | ICC Men's T20 World Cup 2026

· Next update in 5 min
```

### 语音备忘录示例

**第二局：** “印度队在 15 局比赛中得到 146 分，目前有 4 人出局。Tilak Varma 和 Sanju Samson 正在击球。Tilak Varma 得分为 20 分，Sanju Samson 得分为 80 分。印度队还需要在剩余 30 个球内得到 50 分，当前所需得分率为每局 10 分。”
**第一局：** “西印度队在 15 局比赛中得到 120 分，目前有 3 人出局。Rovman Powell 和 Jason Holder 正在击球。当前得分率为每局 8 分，预计总分为 160 分。”

## 数据来源

该脚本从 Cricbuzz 网站抓取数据，包括实时比分的 `og:description` 元数据以及击球手的详细信息；同时还会获取最后一个出局球的统计数据、投球手的统计信息以及球队详情。获取比分数据无需支付任何费用或使用 API 密钥。

## 停止更新的方式

- 当脚本检测到比赛结果（获胜、平局或无结果）时，会自动停止更新。
- 如需手动停止更新，可以终止后台进程。

## 支持的渠道

目前仅支持 Telegram——脚本通过 Telegram 机器人 API 直接发送更新。未来版本将支持多渠道推送（Discord、WhatsApp、Signal 等）。

## 系统要求

- Python 3（仅使用标准库中的 `urllib`，无需 `requests` 模块）
- `gTTS` 包（用于生成语音备忘录）
- Telegram 机器人令牌：可以通过以下方式提供：
  1. `--bot-token` 参数
  2. 环境变量 `TELEGRAM_BOT_TOKEN`
  3. OpenClaw 配置文件（`~/.openclaw/openclaw.json` 中的 `channelsTelegram.botToken`）

## 已知限制

- 当追赶方队伍全部出局或在未达到目标得分的情况下完成比赛时，脚本可能无法及时检测到比赛结果（具体取决于 Cricbuzz 网站的页面更新情况）。不过该脚本能准确识别获胜、平局和达到目标得分的情况。