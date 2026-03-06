---
name: cricket-live-score
description: >
  **功能描述：**  
  以可配置的时间间隔，将实时板球比赛比分更新（包括文字信息和语音备忘录）发送到 Telegram。适用于用户请求任何正在进行的板球比赛的实时比分更新场景。支持 T20 和 ODI 比赛格式，自动识别参赛队伍、比赛目标以及当前进行的局数。  
  **技术细节：**  
  - **数据来源：** 可能通过 API 或其他数据服务获取实时板球比赛比分数据。  
  - **发送方式：** 使用 Telegram 的消息发送功能，同时包含文字信息和语音备忘录（如果需要）。  
  - **自动更新：** 根据用户设定的时间间隔，自动触发比分更新。  
  - **格式支持：** 无论是 T20 还是 ODI 比赛，系统都能正确显示比分信息。  
  - **团队/目标识别：** 系统会自动识别当前比赛的参赛队伍及比赛目标（如总得分）。  
  - **多局显示：** 对于 T20 比赛，系统会同时显示两局的比分情况。  
  **使用场景：**  
  - 当用户需要查看正在进行的板球比赛的实时比分时，可以使用该功能。  
  - 适用于板球赛事的直播、转播或相关应用程序。  
  **注意事项：**  
  - 请确保已正确配置 Telegram 账户并授权应用程序发送消息。  
  - 分数更新的数据来源可能需要根据实际情况进行适配或更换。  
  - 若需支持更多比赛格式或功能，可能需要进一步开发或调整代码。
author: Amit Kulkarni
tags: cricket, sports, live-score, telegram, voice
dependencies: gTTS, requests
config: Telegram bot token (via --bot-token, TELEGRAM_BOT_TOKEN env var, or OpenClaw config)
---
# 🏏 板球实时比分更新

实时板球比分更新通过 Telegram 发送给您——支持添加语音备忘录，让您无需查看屏幕即可随时了解比赛进度。

该脚本支持 T20 和 ODI 比赛格式，可自动识别参赛队伍、比赛阶段以及所需的得分率。

脚本在后台运行，按照您设定的时间间隔发送比分更新，并在比赛结束时自动停止。

语音备忘录非常适合在驾驶或其他无法注视屏幕的情况下使用。

## 示例指令

**开始更新：**
- “发送印度对阵澳大利亚比赛的实时比分更新”
- “关注 IPL 比赛（RCB 对阵 CSK），每 3 分钟发送一次更新”
- “英格兰对阵巴基斯坦的 T20 比赛比分是多少？请随时告知我”

**使用语音备忘录：**
- “发送世界杯决赛的实时板球比分，并附带语音备忘录”
- “关注印度对阵南非的比赛，同时提供语音更新——我正在开车”

**调整更新间隔：**
- “将更新间隔改为每 2 分钟”
- “将更新间隔改为每 10 分钟”

**停止更新：**
- “停止发送比分更新”
- “终止板球比分更新服务”

## 使用场景

当用户请求实时比分更新、板球比分提醒或想要关注某场比赛时，可以使用该脚本。

## 工作原理

1. **查找比赛对应的 Cricbuzz 网址**：搜索 `cricbuzz <team1> vs <team2> live score`，获取 `cricbuzz.com/live-cricket-scores/...` 的网址。
2. **在后台运行脚本**：
```bash
python3 <skill_dir>/scripts/cricket-live.py \
  --url "<cricbuzz_url>" \
  --chat-id "<telegram_chat_id>" \
  --bot-token "<telegram_bot_token>" \
  --interval 300 \
  --voice
```

3. 脚本会自动识别参赛队伍、比赛阶段（T20/ODI）以及比赛目标分数。
4. 按设定的时间间隔发送文本信息和语音备忘录，并在比赛结束时自动停止。

## 参数设置

| 参数 | 默认值 | 说明 |
|-------|---------|-------------|
| `--url` | 必需 | 板球比分更新页面的 Cricbuzz 网址 |
| `--chat-id` | 必需 | 分数更新要发送到的 Telegram 聊天频道 ID |
| `--bot-token` | 自动获取 | Telegram 机器人令牌。若未提供，则使用环境变量 `TELEGRAM_BOT_TOKEN` 或 OpenClaw 配置文件（`~/.openclaw/openclaw.json`）中的令牌 |
| `--interval` | 300 | 更新间隔（默认为 5 分钟） |
| `--voice` | 关闭 | 是否在每次更新时添加语音备忘录 |

## 分数更新内容示例

### 第二局比赛（追赶阶段）
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

### 第一局比赛
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

**第二局比赛：**“印度队在 15 局比赛中得到 146 分，目前有 4 人出局。Tilak Varma 和 Sanju Samson 正在击球。Tilak Varma 得分为 20 分，Sanju Samson 得分为 80 分。印度队还需要在 30 个球内得到 50 分，当前每局所需的得分率为 10.0 分。”
**第一局比赛：**“西印度队在 15 局比赛中得到 120 分，目前有 3 人出局。Rovman Powell 和 Jason Holder 正在击球。当前每局的得分率为 8.0 分，预计总分为 160 分。”

## 数据来源

该脚本从 Cricbuzz 网站获取实时比分数据：使用 `og:description` 元标签获取比分和击球手信息，并通过嵌入的 JSON 数据获取最后一个出局球员、投球手的数据以及球队信息。无需支付 API 费用或使用 API 密钥。

## 停止更新的方式

- 当脚本检测到比赛结果（获胜、平局或无结果）时，会自动停止更新。
- 如需手动停止更新，可以直接终止后台进程。

## 支持的渠道

目前仅支持 **Telegram**——脚本通过 Telegram 机器人 API 直接发送更新。未来版本将支持多渠道（Discord、WhatsApp、Signal 等）。

## 系统要求

- Python 3
- `gTTS` 包（用于生成语音备忘录）
- Telegram 机器人令牌：可以通过以下方式获取：
  1. 使用 `--bot-token` 参数
  2. 设置环境变量 `TELEGRAM_BOT_TOKEN`
  3. 从 OpenClaw 配置文件（`~/.openclaw/openclaw.json`）中读取 `channelsTelegram.botToken`

## 已知限制

- 如果追赶方队伍全部出局或在未达到目标分数的情况下完成所有局数，脚本可能无法及时检测到比赛结果（具体取决于 Cricbuzz 网站的更新情况）。不过该脚本能准确识别获胜、平局以及达到目标分数的情况。