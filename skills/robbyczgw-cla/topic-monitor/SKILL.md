---
name: topic-monitor
version: 1.3.5
description: 监控感兴趣的主题，并在发生重要事件时主动发出警报。适用于用户希望自动监控特定主题的情况（例如产品发布、价格变动、新闻话题、技术更新等）。支持定时网页搜索、基于人工智能的重要性评分、智能警报功能以及每周汇总报告；同时具备内存优化机制，能够生成上下文相关的摘要信息。
metadata: {"openclaw":{"requires":{"bins":["python3"],"env":{"TOPIC_MONITOR_TELEGRAM_ID":"optional - Telegram chat ID for alerts","TOPIC_MONITOR_DATA_DIR":"optional - defaults to .data/ in skill dir","WEB_SEARCH_PLUS_PATH":"optional - defaults to relative path"},"note":"All env vars optional. Defaults work out of the box."}}}
---
# 主题监控器

**监控重要的内容。在重要事件发生时及时收到通知。**

主题监控器通过持续监控您关心的主题，并仅在真正有重要事项发生时智能地向您发送警报，将您的助手从被动响应式转变为主动式。

---

## ⚡ 快速启动（v1.2.0 新功能！）

**只需监控一个主题？只需一个命令：**

```bash
python3 scripts/quick.py "AI Model Releases"
```

就这样！系统会创建一个具有默认设置的主题：
- **查询**：根据主题名称自动生成
- **关键词**：从主题名称中提取
- **频率**：每日
- **重要性**：中等
- **渠道**：Telegram

### 快速启动选项

```bash
# Basic - just a topic name
python3 scripts/quick.py "Bitcoin Price"

# With keywords
python3 scripts/quick.py "Security CVEs" --keywords "CVE,vulnerability,critical"

# High priority, hourly checks
python3 scripts/quick.py "Production Alerts" --frequency hourly --importance high

# Custom query
python3 scripts/quick.py "Competitor News" --query "CompanyName product launch funding"

# Different channel
python3 scripts/quick.py "Team Updates" --channel discord
```

### 快速启动与完整设置对比

| 功能 | 快速启动 | 完整设置 |
|---------|-------------|------------|
| 速度 | ⚡ 一个命令 | 📝 向导 |
| 默认设置 | 智能 | 可自定义 |
| 使用场景 | 单个主题 | 多个主题 |
| 配置 | 最小化 | 完全控制 |

**快速启动后，您随时可以自定义设置：**
```bash
python3 scripts/manage_topics.py edit ai-model-releases --frequency hourly
```

---

## 核心功能

1. **主题配置** - 使用自定义参数定义监控主题
2. **定时监控** - 按可配置的间隔自动搜索
3. **AI 重要性评分** - 智能过滤：立即警报、摘要或忽略
4. **上下文摘要** - 不仅仅是链接，还包括有意义的上下文摘要
5. **每周摘要** - 将低优先级的发现整理成可读的报告
6. **记忆整合** - 参考您之前的对话和兴趣

---

## 完整设置（交互式向导）

要配置多个主题或高级选项，请使用以下步骤：

```bash
python3 scripts/setup.py
```

向导将引导您完成以下步骤：
1. **主题** - 您想要监控哪些主题？
2. **搜索查询** - 如何搜索每个主题
3. **关键词** - 哪些词表示相关性
4. **频率** - 每多久检查一次（每小时/每天/每周）
5. **重要性阈值** - 何时发送警报（低/中/高）
6. **每周摘要** - 将非紧急的发现整理成摘要

向导会创建一个 `config.json` 文件，保存您的偏好设置。您随时可以编辑它，或者使用 `manage_topics.py` 命令来添加/删除主题。

**示例流程：**
```
🔍 Topic Monitor - Setup Wizard

What topics do you want to monitor?
  > AI Model Releases
  > Security Vulnerabilities
  > 

--- Topic 1/2: AI Model Releases ---
  Search query for 'AI Model Releases' [AI Model Releases news updates]: new AI model release announcement
  Keywords to watch for in 'AI Model Releases'?
  > GPT, Claude, Llama, release

--- Topic 2/2: Security Vulnerabilities ---
  Search query for 'Security Vulnerabilities' [Security Vulnerabilities news updates]: CVE critical vulnerability patch
  Keywords to watch for in 'Security Vulnerabilities'?
  > CVE, vulnerability, critical, patch

How often should I check for updates?
  1. hourly
  2. daily *
  3. weekly

✅ Setup Complete!
```

## 快速启动

如果您已经知道如何操作，可以参考以下手动方法：

```bash
# Initialize config from template
cp config.example.json config.json

# Add a topic
python3 scripts/manage_topics.py add "Product Updates" \
  --keywords "release,update,patch" \
  --frequency daily \
  --importance medium

# Test monitoring (dry run)
python3 scripts/monitor.py --dry-run

# Set up cron for automatic monitoring
python3 scripts/setup_cron.py
```

## 主题配置

每个主题包含以下信息：
- **名称** - 显示名称（例如：“AI模型发布”
- **查询** - 搜索查询（例如：“新AI模型发布公告”
- **关键词** - 用于过滤相关内容的关键词（例如：“GPT”、“Claude”、“Llama”、“release”）
- **频率** - 每小时/每天/每周
- **重要性阈值** - 高（立即警报）、中等（重要时警报）、低（仅生成摘要）
- **渠道** - 发送警报的渠道（例如：“Telegram”、“Discord”）
- **上下文** - 您关注这些主题的原因（用于生成更有意义的摘要）

### 示例 config.json 文件

```json
{
  "topics": [
    {
      "id": "ai-models",
      "name": "AI Model Releases",
      "query": "new AI model release GPT Claude Llama",
      "keywords": ["GPT", "Claude", "Llama", "release", "announcement"],
      "frequency": "daily",
      "importance_threshold": "high",
      "channels": ["telegram"],
      "context": "Following AI developments for work",
      "alert_on": ["model_release", "major_update"]
    },
    {
      "id": "tech-news",
      "name": "Tech Industry News",
      "query": "technology startup funding acquisition",
      "keywords": ["startup", "funding", "Series A", "acquisition"],
      "frequency": "daily",
      "importance_threshold": "medium",
      "channels": ["telegram"],
      "context": "Staying informed on tech trends",
      "alert_on": ["major_funding", "acquisition"]
    },
    {
      "id": "security-alerts",
      "name": "Security Vulnerabilities",
      "query": "CVE critical vulnerability security patch",
      "keywords": ["CVE", "vulnerability", "security", "patch", "critical"],
      "frequency": "hourly",
      "importance_threshold": "high",
      "channels": ["telegram", "email"],
      "context": "DevOps security monitoring",
      "alert_on": ["critical_cve", "zero_day"]
    }
  ],
  "settings": {
    "digest_day": "sunday",
    "digest_time": "18:00",
    "max_alerts_per_day": 5,
    "deduplication_window_hours": 72,
    "learning_enabled": true
  }
}
```

## 脚本

### manage_topics.py

用于管理研究主题：

```bash
# Add topic
python3 scripts/manage_topics.py add "Topic Name" \
  --query "search query" \
  --keywords "word1,word2" \
  --frequency daily \
  --importance medium \
  --channels telegram

# List topics
python3 scripts/manage_topics.py list

# Edit topic
python3 scripts/manage_topics.py edit eth-price --frequency hourly

# Remove topic
python3 scripts/manage_topics.py remove eth-price

# Test topic (preview results without saving)
python3 scripts/manage_topics.py test eth-price
```

### monitor.py

主要监控脚本（通过 cron 任务运行）：

```bash
# Normal run (alerts + saves state)
python3 scripts/monitor.py

# Dry run (no alerts, shows what would happen)
python3 scripts/monitor.py --dry-run

# Force check specific topic
python3 scripts/monitor.py --topic eth-price

# Verbose logging
python3 scripts/monitor.py --verbose
```

**工作原理：**
1. 根据设置的频率读取需要检查的主题
2. 使用 `web-search-plus` 或内置的搜索引擎进行搜索
3. 使用 AI 评分系统对每个搜索结果进行重要性评分
4. 重要性高的结果 → 立即警报
5. 重要性中等的结果 → 保存为摘要
6. 重要性低的结果 → 被忽略
7. 更新状态以避免重复警报

### digest.py

生成每周摘要：

```bash
# Generate digest for current week
python3 scripts/digest.py

# Generate and send
python3 scripts/digest.py --send

# Preview without sending
python3 scripts/digest.py --preview
```

**输出格式：**
```markdown
# Weekly Research Digest - [Date Range]

## 🔥 Highlights

- **AI Models**: Claude 4.5 released with improved reasoning
- **Security**: Critical CVE patched in popular framework

## 📊 By Topic

### AI Model Releases
- [3 findings this week]

### Security Vulnerabilities
- [1 finding this week]

## 💡 Recommendations

Based on your interests, you might want to monitor:
- "Kubernetes security" (mentioned 3x this week)
```

### setup_cron.py

配置自动监控任务：

```bash
# Interactive setup
python3 scripts/setup_cron.py

# Auto-setup with defaults
python3 scripts/setup_cron.py --auto

# Remove cron jobs
python3 scripts/setup_cron.py --remove
```

该脚本用于创建 cron 任务条目：
```cron
# Topic Monitor - Hourly topics
0 * * * * cd /path/to/skills/topic-monitor && python3 scripts/monitor.py --frequency hourly

# Topic Monitor - Daily topics  
0 9 * * * cd /path/to/skills/topic-monitor && python3 scripts/monitor.py --frequency daily

# Topic Monitor - Weekly digest
0 18 * * 0 cd /path/to/skills/topic-monitor && python3 scripts/digest.py --send
```

## AI 重要性评分

评分系统使用多种信号来确定警报的优先级：

### 评分标准

**高优先级（立即警报）：**
- 重大突发新闻（通过新鲜度和关键词密度判断）
- 价格变动超过 10%（针对金融主题）
- 与您关键词完全匹配的产品发布
- 您使用的工具中的安全漏洞
- 对您提出的具体问题的直接回答

**中等优先级（值得生成摘要）：**
- 相关新闻但非紧急
- 被跟踪产品的次要更新
- 您关注主题中的有趣发展
- 教程/指南的发布
- 社区中参与度高的讨论

**低优先级（忽略）：**
- 重复的新闻（已收到过警报）
- 间接相关的内容
- 低质量的信息源
- 过时的信息
- 垃圾信息/促销内容

### 学习模式

当启用学习模式（`learning_enabled: true`）时，系统会：
1. 记录您与哪些警报进行了互动
2. 根据您的行为调整评分权重
3. 建议优化主题设置
4. 自动调整重要性阈值

学习数据存储在 `.learning_data.json` 文件中（数据安全，不会被共享）。

## 记忆整合

主题监控器会关联您的对话历史：

**示例警报：**
> 🔔 **Dirac 实时更新**
> 
> 新版本 3.8 已发布，其中包含了您上周请求的房间校正改进。
> 
> **上下文：** 您提到在录音室中遇到低频响应的问题。此次更新包含新的低频优化措施。
> 
> [链接] | [详细信息]

**工作原理：**
1. 读取 `memory_hints.md` 文件（系统会自动生成此文件）
2. 扫描最近的对话记录（如果有的话）
3. 将搜索结果与之前的对话内容进行匹配
4. 生成个性化的摘要

### memory_hints.md（可选）

帮助 AI 理解您的需求：

```markdown
# Memory Hints for Topic Monitor

## AI Models
- Using Claude for coding assistance
- Interested in reasoning improvements
- Comparing models for different use cases

## Security
- Running production Kubernetes clusters
- Need to patch critical CVEs quickly
- Interested in zero-day disclosures

## Tech News
- Following startup ecosystem
- Interested in developer tools space
- Tracking potential acquisition targets
```

## 警报渠道

### Telegram

需要使用 OpenClaw 消息工具：

```json
{
  "channels": ["telegram"],
  "telegram_config": {
    "chat_id": "@your_username",
    "silent": false,
    "effects": {
      "high_importance": "🔥",
      "medium_importance": "📌"
    }
  }
}
```

### Discord

通过代理发送警报（技能配置中不使用 webhook）：

`monitor.py` 会生成 `DISCORD_ALERT` JSON 格式的警报，OpenClaw 通过消息工具发送这些警报。这种方式符合 Telegram 的警报流程（结构化输出，技能代码中不直接使用 HTTP）。

```json
{
  "channels": ["discord"]
}
```

### Email

支持 SMTP 或 API：

```json
{
  "channels": ["email"],
  "email_config": {
    "to": "you@example.com",
    "from": "research@yourdomain.com",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587
  }
}
```

## 高级功能

### 警报条件

您可以微调警报的触发条件：

```json
{
  "alert_on": [
    "price_change_10pct",
    "keyword_exact_match",
    "source_tier_1",
    "high_engagement"
  ],
  "ignore_sources": [
    "spam-site.com",
    "clickbait-news.io"
  ],
  "boost_sources": [
    "github.com",
    "arxiv.org",
    "official-site.com"
  ]
}
```

### 正则表达式模式

用于匹配特定的搜索模式：

```json
{
  "patterns": [
    "version \\d+\\.\\d+\\.\\d+",
    "\\$\\d{1,3}(,\\d{3})*",
    "CVE-\\d{4}-\\d+"
  ]
}
```

### 速率限制

防止频繁收到警报：

```json
{
  "settings": {
    "max_alerts_per_day": 5,
    "max_alerts_per_topic_per_day": 2,
    "quiet_hours": {
      "start": "22:00",
      "end": "08:00"
    }
  }
}
```

## 环境变量

通过配置以下环境变量来自定义主题监控器的行为：

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `TOPIC_MONITOR_TELEGRAM_ID` | — | 用于接收警报的 Telegram 聊天 ID |
| `TOPIC_MONITOR_DATA_DIR` | 技能目录下的 `.data/` | 用于存储状态和搜索结果 |
| `WEB SEARCH_plus_PATH` | 相对于技能目录的路径 | `web-search-plus` 搜索脚本的路径 |
| `SERPER_API_KEY` / `TAVILY_API_KEY` / `EXA_API_KEY` / `YOU_API_KEY` / `SEARXNG_INSTANCE_URL` / `WSP_CACHE_DIR` | 可选的搜索服务相关环境变量 |

**示例配置：**
```bash
# Add to ~/.bashrc or .env
export TOPIC_MONITOR_TELEGRAM_ID="123456789"
export TOPIC_MONITOR_DATA_DIR="/home/user/topic-monitor-data"
export WEB_SEARCH_PLUS_PATH="/path/to/skills/web-search-plus/scripts/search.py"
```

## 状态管理

### .research_state.json

文件存储在 `TOPIC_MONITOR_DATA_DIR` 目录下（默认为技能目录下的 `.data/`）。

记录以下信息：
- 每个主题的最后检查时间
- 已接收警报的 URL（去重处理）
- 重要性评分历史
- 学习数据（如果启用了学习模式）

示例文件：```json
{
  "topics": {
    "eth-price": {
      "last_check": "2026-01-28T22:00:00Z",
      "last_alert": "2026-01-28T15:30:00Z",
      "alerted_urls": [
        "https://example.com/eth-news-1"
      ],
      "findings_count": 3,
      "alerts_today": 1
    }
  },
  "deduplication": {
    "url_hash_map": {
      "abc123": "2026-01-28T15:30:00Z"
    }
  }
}
```

### .findings/ 目录

用于存储值得生成摘要的搜索结果：

```
.findings/
├── 2026-01-22_eth-price.json
├── 2026-01-24_fm26-patches.json
└── 2026-01-27_ai-breakthroughs.json
```

## 最佳实践

1. **谨慎开始** - 初始时将 `importance_threshold` 设置为中等，根据警报质量进行调整
2. **使用上下文字段** - 有助于 AI 生成更准确的摘要
3. **优化关键词** - 添加负面关键词以过滤无关内容（例如：“keywords”: ["AI", "-clickbait", "-spam"]）
4. **启用学习模式** - 根据您的使用习惯逐步优化系统
5. **每周查看摘要** - 不要忽略摘要，它可以帮助您发现新的趋势
6. **结合个人分析** - 根据您的对话模式推荐相关主题

## 与其他技能的集成

### web-search-plus

自动选择合适的搜索服务：
- 产品/价格相关主题 → 使用 Serper
- 研究主题 → 使用 Tavily
- 公司/初创企业相关主题 → 使用 Exa

### personal-analytics

根据您的对话习惯推荐相关主题：
> “您本月已经询问了 12 次关于 Rust 的信息。是否希望我监控‘Rust 语言更新’？”

## 隐私与安全

- **所有数据均存储在本地** - 除了搜索 API 外，不使用任何外部服务
- **状态文件被 Git 管理** - 安全地存储在版本控制的工作环境中
- **记忆提示功能可选** - 您可以控制共享的上下文内容
- **学习数据仅保存在本地** - 不会发送到任何外部服务
- ** subprocess 环境变量限制** - 只允许传递 PATH/HOME/LANG/TERM 和搜索服务相关的环境变量
- **技能代码中不使用直接 HTTP 请求** - 警报以 JSON 格式发送给 OpenClaw

## 故障排除

**没有收到警报：**
- 检查 cron 任务是否正在运行：`crontab -l`
- 验证频道配置（Telegram 聊天 ID、Discord/Email 的频道列表）
- 使用 `--dry-run --verbose` 命令运行脚本以查看评分过程

**收到过多警报：**
- 提高 `importance_threshold` 值
- 设置速率限制
- 优化关键词（添加负面过滤条件）
- 启用学习模式

**错过重要新闻：**
- 降低 `importance_threshold` 值
- 增加检查频率
- 扩大关键词范围
- 检查 `.research_state.json` 文件中的去重情况

**摘要未生成：**
- 确保 `.findings/` 目录存在且有内容
- 检查每周摘要的生成计划
- 手动运行 `python3 scripts/digest.py --preview` 命令查看摘要

## 示例工作流程

### 监控产品发布

```bash
python3 scripts/manage_topics.py add "iPhone 17 Release" \
  --query "iPhone 17 announcement release date" \
  --keywords "iPhone 17,Apple event,September" \
  --frequency daily \
  --importance high \
  --channels telegram \
  --context "Planning to upgrade from iPhone 13"
```

### 监控竞争对手动态

```bash
python3 scripts/manage_topics.py add "Competitor Analysis" \
  --query "CompetitorCo product launch funding" \
  --keywords "CompetitorCo,product,launch,Series,funding" \
  --frequency weekly \
  --importance medium \
  --channels discord,email
```

### 研究主题

```bash
python3 scripts/manage_topics.py add "Quantum Computing Papers" \
  --query "quantum computing arxiv" \
  --keywords "quantum,qubit,arxiv" \
  --frequency weekly \
  --importance low \
  --channels email
```

## 致谢

该功能由 ClawHub 开发，使用了 `web-search-plus` 技能来实现智能的搜索路由。