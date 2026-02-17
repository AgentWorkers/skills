# 🏏 板球比分 v1.0.0

**OpenClaw 的实时板球比分、IPL 跟踪和比赛提醒功能。**

通过 OpenClaw 代理，您可以获取实时比分、即将进行的比赛日程、详细的比分卡以及 IPL 排名——所有数据均来自 [CricketData.org](https://cricketdata.org) 的 API（端点：`api.cricapi.com`）。

---

## ✨ 主要功能

- 🔴 **实时比分** — 所有正在进行的比赛的实时比分、局数和比赛状态
- 📋 **比赛详情** — 包含击球和投球统计的完整比分卡
- 📅 **即将进行的比赛** — 下周7天内安排的比赛，可按球队筛选
- ✅ **最近的比赛结果** — 过去3天内结束的比赛
- 🏆 **IPL 信息中心** — IPL 排名、即将进行的比赛、实时比分和比赛结果
- 🔍 **比赛搜索** — 可通过球队名称查找比赛（支持别名，如 "MI"、"CSK"、"AUS"）
- 🔔 **提醒** — 支持定时任务（Cron）的脚本，用于通知球门失守、球员达到百分或比赛结果
- 💾 **智能缓存** — 允许配置每个端点的缓存时间（TTL），以合理利用 API 配额
- 🇮🇳 **默认显示时间为印度标准时间（IST）**

---

## 🚀 快速入门

### 1. 获取免费 API 密钥
在 [cricketdata.org](https://cricketdata.org) 注册——免费 tier 每天提供 **100 次 API 请求**。（CricketData.org 的 API 通过 `api.cricapi.com` 提供——两者是同一服务。）

### 2. 设置环境变量
```bash
export CRICKET_API_KEY="your-api-key-here"
# Add to your shell profile or ~/.openclaw/.env for persistence
```

### 3. 运行任何脚本
```bash
bash scripts/live-scores.sh              # What's happening right now?
bash scripts/upcoming-matches.sh         # What's coming up?
bash scripts/ipl.sh standings            # IPL points table
```

---

## 📖 使用方法

### 实时比分
```bash
bash scripts/live-scores.sh
```
显示所有正在进行的比赛的比分、局数和比赛状态。

**示例输出：**
```
🏏 LIVE CRICKET SCORES
━━━━━━━━━━━━━━━━━━━━━

🔴 India vs England — 3rd Test, Day 2
🇮🇳 India: 285/6 (78.2 ov)
🏴 England: 312 (98.4 ov)
📊 India trail by 27 runs

🔴 Australia vs South Africa — 1st ODI
🇦🇺 Australia: 156/3 (28.1 ov)
📊 In Progress
```

### 即将进行的比赛
```bash
bash scripts/upcoming-matches.sh              # All upcoming
bash scripts/upcoming-matches.sh --team India  # Filter by team
bash scripts/upcoming-matches.sh MI            # Works with aliases
```

**示例输出：**
```
📅 UPCOMING MATCHES (Next 7 Days)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🇮🇳 India vs England — 4th Test
📍 Ranchi
🕐 16 Feb 2026, 09:30 AM IST

🏏 Mumbai Indians vs Chennai Super Kings — IPL 2026
📍 Wankhede Stadium, Mumbai
🕐 18 Feb 2026, 07:30 PM IST
```

### 最近的比赛结果
```bash
bash scripts/recent-results.sh
```

**示例输出：**
```
✅ RECENT RESULTS
━━━━━━━━━━━━━━━━━

🏆 India won by 5 wickets
India vs England — 2nd Test
📍 Visakhapatnam

🏆 Australia won by 73 runs
Australia vs Sri Lanka — 3rd ODI
📍 Melbourne
```

### IPL 信息中心
```bash
bash scripts/ipl.sh standings   # Points table
bash scripts/ipl.sh upcoming    # Upcoming IPL matches
bash scripts/ipl.sh live        # Live IPL scores
bash scripts/ipl.sh results     # Recent IPL results
```

### 比赛详情（比分卡）
```bash
bash scripts/match-details.sh <match-id>
```
可以从实时比分或搜索结果中获取比赛 ID。

### 搜索比赛
```bash
bash scripts/search-match.sh "India vs Australia"
bash scripts/search-match.sh "MI vs CSK"
```

### 板球提醒（Cron）
```bash
bash scripts/cricket-alert.sh
```
检测球门失守、球员达到百分或比赛结束的情况。仅在有重要事件发生时输出——非常适合用于定时任务。

---

## 🗣️ 语言映射

| 用户输入 | 脚本名称 |
|-----------|--------|
| “比分是多少？” / “显示比赛 X 的比分卡” | `live-scores.sh` |
| “显示比赛 X 的比分卡” | `match-details.sh <id>` |
| “即将进行的比赛” / “有什么比赛？” | `upcoming-matches.sh` |
| “最近的比赛结果” / “谁赢了？” | `recent-results.sh` |
| “IPL 排名” | `ipl.sh standings` |
| “今天的 IPL 比赛” | `ipl.sh live` |
| “印度对阵澳大利亚” | `search-match.sh "India vs Australia"` |

---

## ⚙️ 配置

### `config/cricket.yaml`
主要配置文件。API 密钥可以在这里设置，也可以通过 `CRICKET_API_KEY` 环境变量设置（环境变量优先级更高）。

```yaml
api_key: ""                    # Set via env var recommended
favorite_teams:                # Teams for alert filtering
  - India
  - Mumbai Indians
alert_events:                  # Events that trigger alerts
  - wicket
  - century
  - match_end
cache_dir: /tmp/cricket-cache  # Cache directory
cache_ttl:                     # Cache TTL in seconds per endpoint
  live: 120
  upcoming: 1800
  results: 1800
  series: 86400
  scorecard: 300
```

### `config/teams.yaml`
用于模糊匹配的球队名称别名。将简写名称（MI、CSK、IND、AUS）映射到官方的 API 名称。详情请参阅 `config/README.md`。

---

## ⏰ 定时任务集成
设置定期比赛提醒：

```bash
# Check for notable events every 5 minutes during match hours
*/5 9-23 * * * CRICKET_API_KEY="your-key" bash /path/to/skills/cricket-scores/scripts/cricket-alert.sh

# Or use OpenClaw cron:
# Schedule cricket-alert.sh to run during IPL match times (7-11 PM IST)
```

提醒脚本会跟踪 `/tmp/cricket-alert-state.json` 文件中的状态，并且仅在有新情况发生时（如球门失守、球员达到百分或比赛结果）才输出。

---

## 📊 API 配额管理

| 计费等级 | 每天请求次数 | 费用 |
|------|-----------|------|
| 免费 | 100 | $0 |
| 专业级 | 2,000 | $5.99/月 |

### 缓存的作用
所有脚本都会将 API 响应本地缓存到 `/tmp/cricket-cache/`：
- **实时比分**：缓存时间为 2 分钟（比赛期间保持最新）
- **即将进行的比赛/比赛结果**：缓存时间为 30 分钟
- **系列赛信息**：缓存时间为 24 小时
- **比分卡**：缓存时间为 5 分钟

### 比赛日的预算
大约 10 次列表请求 + 50 次比分检查 + 40 次临时请求 = **100 次请求**（符合免费 tier 的限制）

### 当配额用尽时
脚本会显示明确提示：*"API 配额已用尽（每天限制为 100 次请求）。请明天再试或升级。"*

---

## 📂 输出格式
所有输出都便于阅读：
- 不使用 Markdown 表格（适用于 WhatsApp、Discord、Telegram）
- 使用项目符号列表和表情符号
- 时间转换为印度标准时间（IST）
- 包含比赛 ID 以便进一步查询

---

## 📋 必备软件

- **bash** 4.0 或更高版本
- **curl**（通常已预装）
- **jq** — 可通过 `apt install jq` 或 `brew install jq` 安装
- **python3** — 用于辅助脚本和数据解析
- **CricketData.org API 密钥**（免费）——请在 [cricketdata.org](https://cricketdata.org) 注册

---

## 🔒 安全注意事项

- **API 密钥在 URL 查询参数中**：CricketData.org 的 API（`api.cricapi.com`）要求将 API 密钥作为 URL 查询参数传递（`?apikey=...`）。这意味着密钥可能会显示在 shell 历史记录、进程列表、服务器访问日志以及任何 HTTP 代理/检查日志中。应对措施：
  - 通过 `CRICKET_API_KEY` 环境变量设置密钥（不要硬编码在配置文件中）。
  - 使用 **免费 tier 的密钥**——其权限有限，且易于更换。
  - 避免在共享或多租户环境中运行脚本，以防进程参数被其他用户看到。
  - CricketData.org 的 API 不支持基于头部的身份验证，因此必须通过查询参数传递密钥。

---

## 📄 许可证

MIT 许可证 — 详情请参阅 [LICENSE](LICENSE)