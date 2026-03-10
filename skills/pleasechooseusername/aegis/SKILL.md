---
name: aegis
description: "自动化应急地缘政治情报系统——为冲突地区的平民提供实时威胁监控和安全警报。适用场景包括：  
(1) 为特定地区建立战区/危机安全监控机制；  
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

专为冲突地区的平民提供威胁情报服务。该系统监控28个以上的信息来源（包括RSS、网页、API和开源情报聚合器），并提供两种信息传递方式：

1. **仅限紧急情况的扫描**（每15分钟一次）—— 仅发布经过验证的、正在发生的紧急事件（需经过三阶段验证）。
2. **晨间/晚间简报**（当地时间上午8点/晚上8点）—— 由人工生成的局势报告，包含可操作的指导建议。

AEGIS基于**World Monitor**（实时地缘政治情报API）和**LiveUAMap**（经过验证的开源情报事件源）运行，同时还会参考政府官方消息来源、主要新闻机构和航空数据。

**注意：** 本系统并非用于引发恐慌的工具，而是提供冷静、基于事实的、以行动为导向的信息。所有内容均遵循政府官方指导。

## 系统要求

- **curl**—— 用于所有HTTP请求（获取RSS、网页内容及API数据）。大多数系统已预装该工具。
- **python3**（3.8及以上版本）—— 用于运行所有脚本。无需额外安装pip包（仅需要标准库）。
- **基础信息来源无需API密钥**。如需扩展信息覆盖范围，可使用NewsAPI的免费 tier。
- **大型语言模型（LLM，可选）**—— 通过语义验证提高紧急警报的准确性。详见[LLM验证](#llm-verification)部分。

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

### 设置定时任务监控
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
需设置以下环境变量以直接通过Telegram频道发送警报：
- `AEGIS_BOT_TOKEN` — Telegram机器人的访问令牌（从BotFather获取）
- `AEGIS_CHANNEL_ID` — Telegram频道ID

或直接在配置文件中添加这些信息：
```json
{
  "telegram": {
    "bot_token": "your-token",
    "channel_id": "-100xxxxxxxxxx"
  }
}
```

## 数据存储

AEGIS将扫描结果存储在`~/.openclaw/aegis-data/`目录中（如果设置了`$AEGIS_DATA_DIR`，则使用该目录）：
- `seen_hashes.json` — 扫描内容的去重哈希值（扫描结果保留48小时，信息源更新保留6小时）
- `pending_alerts.json` — 待批量发送的警报信息
- `scan_log.json` — 最新的扫描结果
- `last_scan.json` — 最最近的扫描输出（用于生成简报）
- `feed_state.json` — 实时信息源的更新状态及最后一条信息的发布时间
- `last_alert_time.json` — 预警信息在频道发布的间隔时间
- `scan_history.log` — 扫描结果的滚动日志（记录最近500条记录）

所有数据均为本地JSON格式，不会发送到`source-registry.json`中列出的任何外部服务器。

## 信息来源（30个以上）

所有信息来源均定义在`references/source-registry.json`文件中。系统仅会访问该文件中列出的URL。

| 来源等级 | 类型 | 数量 | 示例 |
|------|------|-------|----------|
| 0 🏛️ | 政府及紧急信息 | 7 | GDACS、NCEMA、阿联酋国防部、美国/英国大使馆、MOFAIC |
| 1 📰 | 主要新闻及RSS源 | 11 | 半岛电视台（Al Jazeera）、路透社（Reuters）、BBC、Gulf Business、Emirates 24/7、Gulf Today |
| 2 🔍 | 开源情报及冲突地图 | 5 | World Monitor API、LiveUAMap（覆盖3个地区） |
| 2 ✈️ | 航空信息 | 2 | 美国联邦航空管理局（FAA）的NOTAM公告（DXB、AUH机场） |
| 3 📋 | 分析类信息 | 2 | Crisis Group、War on the Rocks |
| 4 🔑 | 基于API的增强型信息（可选） | 1个以上 | NewsAPI（免费 tier）、GDELT |

### 外部连接

系统仅会访问`references/source-registry.json`中列出的URL：
- RSS信息源
- 新闻网站
- 政府官方网站

此外，系统还会连接以下外部服务：
- `https://world-monitor.com/api/signal-markers`（World Monitor公共API）
- LiveUAMap的区域页面（例如`https://iran.liveuamap.com`）
- Telegram机器人API（`https://apiTelegram.org/bot.../sendMessage`）（仅当配置了Telegram频道发送功能时使用）

系统不发送任何遥测数据，也不进行任何数据分析或主动上报系统状态。

## 警报分类

| 等级 | 含义 | 触发条件 |
|-------|---------|---------|
| 🔴 **紧急** | 用户所在国家面临迫在眉睫的物理危险 | 导弹来袭、警报响起、疏散命令、机场关闭、核生化威胁 |
| 🟠 **高风险** | 地区性重大威胁 | 邻国遭受攻击、海峡交通中断、航班取消 |
| ℹ️ **中等风险** | 需关注的区域动态 | 地区性军事行动、外交事件、油价波动、制裁措施 |

“紧急”等级用于表示“立即行动，生命可能受到威胁”的情况；“高风险”等级用于表示具有区域影响的重大事件。

### 紧急警报的验证流程（v3.2）

紧急警报需经过三阶段验证以排除误报：
1. **正则表达式预过滤** — 严格匹配正在发生的攻击、警报事件和疏散命令。
2. **否定模式过滤** — 排除过去发生的事件、体育赛事相关内容、分析性文章和猜测性信息。
3. **大型语言模型（LLM）验证**（可选） — 确认事件属于真实发生的紧急情况。

此外：
- **政府官方来源**（如NCEMA、政府机构）可免于LLM验证。
- **多源验证**：单一来源需等待4小时；多个来源需等待1小时。
- **安全机制** — 如果LLM不可用或被禁用，紧急警报仍会直接发送。

### LLM验证

LLM验证是可选的，但推荐使用。它可以通过语义分析帮助识别正则表达式可能遗漏的误报（例如，“由于战争导致板球比赛取消”这样的信息可能被误判为紧急事件）。

**验证方式有三种**（可在`aegis-config.json`的`"llm"`配置项中选择）：

| 方式 | 提供者 | 成本 | 准确率 | 设置要求 |
|------|----------|------|----------|-------|
| **本地Ollama模型** | `"ollama"` | 免费（在用户的GPU上运行） | 最准确 | 需安装[Ollama](https://ollama.ai)并下载模型 |
| **兼容OpenAI的API** | `"openai"` | 每次验证约0.001美元 | 最准确 | 任何支持OpenAI的API（如OpenRouter、Together、vLLM、LiteLLM等） |
| **不使用LLM** | `"none"` | 免费 | 通过正则表达式和否定模式过滤也能达到较高准确率 | 无需额外设置 |

**配置示例：**

```json
// Local Ollama (recommended if you have a GPU)
"llm": { "enabled": true, "provider": "ollama", "endpoint": "http://localhost:11434", "model": "qwen3:8b" }

// OpenRouter (cheap cloud API)
"llm": { "enabled": true, "provider": "openai", "endpoint": "https://openrouter.ai/api", "model": "meta-llama/llama-3-8b-instruct", "api_key": "sk-or-..." }

// No LLM (regex-only, no external calls)
"llm": { "enabled": false, "provider": "none" }
```

系统提供引导工具`aegis_onboard.py`，可帮助用户在设置过程中做出选择。

### 防伪机制
- **一级来源**：直接信任（政府或紧急机构发布的消息）。
- **二级及以上等级的紧急警报**：必须通过LLM的语义验证。
- **二级及以上等级的警报**：需要至少来自一个一级或二级来源的确认信息。
- **社交媒体内容**：完全排除在外。
- **极端或未经证实的声明**：需要来自三个独立来源的确认。

## 简报生成

晨间和晚间简报由人工生成，内容易于理解：

### 简报格式
每份简报包含：
- **摘要** — 用通俗语言说明发生了什么，附带具体数据。
- **当前安全状况** — 当前的安全等级及详细说明。
- **应对措施** — 平民应立即采取的4-6项具体行动。
- **日常影响** — 航班、学校、工作、交通、医院等方面的情况。
- **未来展望** — 接下来12-24小时内的可能情况。
- **信息来源** — 可以在哪里核实更多信息。

## 信息传递方式
| 传递方式 | 频率 | 发布平台 |
|------|-----------|---------|
| **紧急情况扫描** | 每15分钟 | 仅发布紧急事件（如导弹来袭、疏散命令） |
| **晨间简报** | 每日一次（当地时间上午8点） | 包括夜间发生的所有事件及总结 |
| **晚间简报** | 每日一次（当地时间晚上8点） | 包括白天发生的所有事件及总结 |
| **实时信息流** | 每5分钟一次（可选） | 来自LiveUAMap和World Monitor的经核实事件 |

### 防止信息垃圾邮件
- **紧急情况扫描**：单源信息需等待4小时才能再次发布；多源信息需等待1小时才能再次发布。
- **实时信息流**：每5分钟发布一次，每次最多发布8条事件。
- **简报**：由系统自动生成，通过Telegram频道发送。

## 国家资料

每个支持的国家都有对应的资料文件，位于`references/country-profiles/`目录下。资料文件包含：
- 紧急联系信息和热线电话
- 邻国及相关地区信息（用于过滤信息来源）
- 当地的威胁关键词模式
- 避难和疏散指南

目前支持的国家资料：**阿联酋**（`uae.json`）。如需添加其他国家资料，请复制 `_template.json`文件，填写详细信息后提交Pull Request。

## 应急准备资源

更多资源请参阅`references/preparedness/`目录：
- `go-bag-checklist.md` — 应急疏散时需要携带的物品清单
- `communication-plan.md` — 家庭沟通计划
- `shelter-guidance.md` — 居家避难指南
- `evacuation-guidance.md` — 疏散路线、交通信息及大使馆联系方式

## 配置参考

所有配置选项详见`references/config-reference.md`文件。

## 成本

- **信息来源（30个以上）**：免费（RSS、网页爬取和公共API）
- **LLM验证（可选）**：使用Ollama模型时免费；使用云API时每次验证约0.001美元；也可关闭该功能（仅使用正则表达式过滤）。
- **简报生成**：使用Copilot或本地模型时免费；使用商业LLM模型时每天费用约为0.03-0.05美元。
- **NewsAPI（可选）**：免费 tier每天允许100次请求。