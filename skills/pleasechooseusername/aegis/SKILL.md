---
name: aegis
description: "自动化紧急地缘政治情报系统——为冲突地区的平民提供实时威胁监测和安全警报。适用场景包括：  
(1) 为特定地区设置战区/危机安全监测机制；  
(2) 用户咨询安全状况或威胁等级；  
(3) 配置紧急警报的发送方式；  
(4) 生成安全简报；  
(5) 制定应急准备计划。"
homepage: "https://github.com/PleaseChooseUsername/aegis-openclaw-skill"
source: "https://github.com/PleaseChooseUsername/aegis-openclaw-skill"
requires:
  binaries:
    - curl
    - python3
  env: []
  optional_env:
    - AEGIS_DATA_DIR
    - AEGIS_BOT_TOKEN
    - AEGIS_CHANNEL_ID
  optional_config:
    - "api_keys.newsapi"
---
# AEGIS — 自动化紧急地缘政治情报系统

专为冲突地区的平民提供威胁情报服务。系统监控30多个信息源（RSS、网页、API、开源情报聚合器），并提供两种信息传递方式：

1. **仅紧急情况扫描**（每15分钟一次）——仅在人员生命受到直接威胁时发布警报。
2. **晨间/晚间简报**（当地时间上午8点/晚上8点）——由人工生成的局势报告，包含可操作的应对建议。

该系统基于**World Monitor**（实时地缘政治情报API）和**LiveUAMap**（经过验证的开源情报事件源）运行，并结合政府官方消息、主要新闻机构及航空数据。

**注意：**本系统并非用于引发恐慌的工具，而是提供冷静、基于事实的、以行动为导向的情报。所有信息均遵循政府官方指导。

## 系统要求

- **curl**——用于所有HTTP请求（RSS、网页、API）。大多数系统已预装此工具。
- **python3**（3.8及以上版本）——所有脚本均需在此环境下运行。无需额外安装pip包（仅依赖标准库）。
- **23个基础信息源无需API密钥**。如需扩展信息覆盖范围，可使用NewsAPI的免费 tier。

## 快速入门

### 首次设置（交互式）
```bash
python3 scripts/aegis_onboard.py
```
创建`~/.openclaw/aegis-config.json`文件，配置地理位置、语言和警报偏好设置。

### 手动配置
创建`~/.openclaw/aegis-config.json`文件：
```json
{
  "location": {
    "country": "AE",
    "country_code": "AE",
    "city": "Dubai",
    "timezone": "Asia/Dubai"
  },
  "language": "en",
  "alerts": { "critical_instant": true, "high_batch_minutes": 30, "medium_digest_hours": 6 },
  "briefings": { "morning": "07:00", "evening": "22:00" },
  "scan_interval_minutes": 15,
  "api_keys": {}
}
```

### 运行扫描
```bash
python3 scripts/aegis_scanner.py
```

### 设置定时扫描任务
```
# CRITICAL-only scan (every 15 min) — posts ONLY for imminent threats
openclaw cron add --every 15m --message "Run AEGIS scan: python3 <skill-dir>/scripts/aegis_cron.py"

# Morning briefing (adjust time for user timezone — example: 4:00 UTC = 8:00 Dubai)
openclaw cron add --cron "0 4 * * *" --tz UTC --message "Run AEGIS morning briefing: python3 <skill-dir>/scripts/aegis_briefing.py morning"

# Evening briefing (example: 16:00 UTC = 20:00 Dubai)
openclaw cron add --cron "0 16 * * *" --tz UTC --message "Run AEGIS evening briefing: python3 <skill-dir>/scripts/aegis_briefing.py evening"

# Optional: Live feed (every 5 min) — for high-tempo situations only, disable during calm periods
openclaw cron add --cron "*/5 * * * *" --message "Run AEGIS live feed: python3 <skill-dir>/scripts/aegis_feed.py" --disabled
```

### 可选：通过Telegram频道发送警报
设置环境变量以直接通过Telegram频道发布警报：
- `AEGIS_BOT_TOKEN` — Telegram机器人的访问令牌（需从BotFather获取）
- `AEGIS_CHANNEL_ID` — 目标Telegram频道ID

或通过配置文件进行设置：
```json
{
  "telegram": {
    "bot_token": "your-token",
    "channel_id": "-100xxxxxxxxxx"
  }
}
```

## 数据存储

AEGIS将扫描结果保存在`~/.openclaw/aegis-data/`文件夹中（若未指定，则使用`$AEGIS_DATA_DIR`）：
- `seen_hashes.json` — 扫描内容的去重哈希值（扫描结果保留48小时，信息源更新保留6小时）
- `pending_alerts.json` — 待批量发送的警报信息
- `scan_log.json` — 最近的扫描记录
- `last_scan.json` — 最新的扫描结果（用于生成简报）
- `feed_state.json` — 实时信息源的更新状态及最后一条消息的发布时间
- `last_alert_time.json` — 预警信息在频道发布的间隔时间
- `scan_history.log` — 扫描结果的滚动日志（记录最近500条记录）

所有数据均以JSON格式存储在本地，不会发送到`source-registry.json`中列出的任何外部服务器。

## 信息源（30多个）

所有信息源的详细信息均存储在`references/source-registry.json`文件中。系统仅会访问该文件中列出的URL。

| 等级 | 类型 | 数量 | 示例 |
|------|------|-------|----------|
| 0 🏛️ | 政府及紧急信息源 | 7 | GDACS、NCEMA、阿联酋国防部、美国/英国大使馆、MOFAIC |
| 1 📰 | 主要新闻及RSS源 | 11 | 半岛电视台（Al Jazeera）、路透社（Reuters）、BBC、Gulf Business、Emirates 24/7、Gulf Today |
| 2 🔍 | 开源情报及冲突地图 | 5 | World Monitor API、LiveUAMap（覆盖3个地区） |
| 2 ✈️ | 航空信息源 | 2 | 美国联邦航空管理局（FAA）的NOTAM公告（DXB、AUH） |
| 3 📋 | 分析类信息源 | 2 | Crisis Group、War on the Rocks |
| 4 🔑 | 基于API的增强型信息源（可选） | 1+ | NewsAPI（免费 tier）、GDELT |

### 外部连接

系统仅会连接`references/source-registry.json`中列出的URL：
- RSS信息源
- 新闻网站
- 政府官方页面

此外，系统还会访问：
- `https://world-monitor.com/api/signal-markers`（World Monitor公共API）
- LiveUAMap的区域页面（例如：`https://iran.liveuamap.com`）
- 如果配置了Telegram频道发送功能，还会访问Telegram机器人的API（`https://apiTelegram.org/bot.../sendMessage`）

系统不记录使用情况数据，也不进行任何分析或主动报告系统状态。

## 警报分类

| 等级 | 含义 | 触发条件 |
|-------|---------|---------|
| 🔴 CRITICAL | 用户所在国家面临迫在眉睫的物理危险 | 导弹来袭、警报响起、要求民众避难、机场关闭、核生化威胁 |
| 🟠 HIGH | 地区性重大威胁 | 邻国遭受攻击、海峡交通中断、航班取消 |
| ℹ️ MEDIUM | 一般性局势变化 | 地区性军事行动、外交事件、油价波动、制裁措施 |

“CRITICAL”等级的警报表示“立即行动，您的生命可能处于危险之中”；“HIGH”等级的警报表示地区性重大事件。

### 防伪机制
- 等级0-1的信息源可以直接触发警报。
- 等级2及以上的信息源需要至少来自1个“CRITICAL”等级信息源的验证。
- 社交媒体信息完全不予考虑。
- 特殊或夸张的声明需要至少来自3个独立信息源的证实。

## 简报生成

晨间和晚间简报由人工生成，内容易于理解：

### 简报格式
每份简报包括：
- **摘要**——用通俗语言说明发生的情况及具体数据。
- **当前安全状况**——当前的安全级别及威胁详情。
- **应对措施**——平民应立即采取的4-6项具体行动。
- **日常影响**——航班、学校、工作、交通、医疗设施的现状。
- **未来展望**——未来12-24小时内的可能情况。
- **信息来源**——可查询更多信息的渠道。

## 信息传递方式
| 传递方式 | 发布频率 | 发布平台 |
|------|-----------|---------|
| **紧急情况扫描** | 每15分钟 | 仅在发生迫在眉睫的危险时（如导弹来袭、要求避难时） |
| **晨间简报** | 每天一次（当地时间上午8点） | 全面情况更新及夜间事件总结 |
| **晚间简报** | 每天一次（当地时间晚上8点） | 全面情况更新及白天事件总结 |
| **实时信息流** | 每5分钟一次（可选） | 来自LiveUAMap和World Monitor的经核实事件 |

### 防止垃圾信息
- **紧急情况扫描**：每次在频道发布警报前需等待60分钟。
- **实时信息流**：每5分钟批量发送一条消息，每次最多8条事件。
- **简报**：由人工生成后固定在频道上，每个周期发布一次。

## 国家资料

每个支持的国家在`references/country-profiles/`文件夹中都有对应的资料文件。资料内容包括：
- 紧急联系人和热线电话
- 邻国及相关地区信息（用于筛选信息源）
- 当地的威胁关键词模式
- 避难和疏散指南

目前支持的国家资料：**阿联酋**（`uae.json`）。如需添加其他国家，请复制 `_template.json`文件，填写详细信息后提交拉取请求。

## 应急准备资源

更多资源请参阅`references/preparedness/`：
- `go-bag-checklist.md` — 应急疏散所需物品清单
- `communication-plan.md` — 家庭沟通计划
- `shelter-guidance.md` — 居家避难指南
- `evacuation-guidance.md` — 疏散路线、交通信息及大使馆联系方式

## 配置参考

详细配置选项请参阅`references/config-reference.md`。

## 成本

- **基础配置（无需API密钥）**：使用Copilot或本地模型可免费使用；使用商业大型语言模型每日费用约为0.03-0.05美元。
- **包含所有23个信息源**：免费（RSS、网页抓取及公共API）。
- **可选的NewsAPI**：免费tier（每天100次请求）即可满足需求。