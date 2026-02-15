---
name: proactive-research
description: 监控感兴趣的主题，并在发生重要事件时主动发出警报。适用于需要自动监控特定主题的场景（例如产品发布、价格变动、新闻话题、技术更新等）。支持定时网页搜索、基于人工智能的重要性评分机制、智能警报功能以及每周汇总报告；同时具备内存管理功能，能够生成与上下文相关的摘要信息。
---

# 主动研究（Proactive Research）

**监控重要的信息，及时接收通知。**

通过持续监控您关注的主题，并仅在真正重要的信息出现时智能地提醒您，Proactive Research 能将您的助手从被动响应型转变为主动型。

## 核心功能

1. **主题配置** - 使用自定义参数定义主题
2. **定时监控** - 按可配置的间隔自动搜索
3. **AI 重要性评分** - 智能过滤：立即提醒、汇总或忽略
4. **上下文摘要** - 不仅仅是链接，还包括有意义的上下文摘要
5. **每周摘要** - 将低优先级的发现整理成易读的报告
6. **记忆整合** - 参考您之前的对话和兴趣

## 快速入门

```bash
# Initialize config
cp config.example.json config.json

# Add a topic
python3 scripts/manage_topics.py add "Dirac Live updates" \
  --keywords "Dirac Live,room correction,audio" \
  --frequency daily \
  --importance medium

# Test monitoring (dry run)
python3 scripts/monitor.py --dry-run

# Set up cron for automatic monitoring
python3 scripts/setup_cron.py
```

## 主题配置

每个主题包含：

- **名称** - 显示名称（例如：“AI 模型发布”）
- **查询** - 搜索查询（例如：“新的 AI 模型发布公告”）
- **关键词** - 相关性过滤器（["GPT", "Claude", "Llama", "release"]）
- **频率** - `每小时`、`每天`、`每周`
- **重要性阈值** - `高`（立即提醒）、`中`（重要时提醒）、`低`（仅汇总）
- **渠道** - 提醒发送的位置（["Telegram", "Discord"]）
- **上下文** - 您关注的原因（用于生成 AI 上下文摘要）

### 示例 config.json

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

管理研究主题：

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

主要监控脚本（通过 cron 运行）：

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
1. 根据频率读取需要检查的主题
2. 使用 web-search-plus 或内置的 web_search 进行搜索
3. 用 AI 重要性评分器对每个结果进行评分
4. 高重要性 → 立即提醒
5. 中等重要性 → 保存以供汇总
6. 低重要性 → 忽略
7. 更新状态以避免重复提醒

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

配置自动监控：

```bash
# Interactive setup
python3 scripts/setup_cron.py

# Auto-setup with defaults
python3 scripts/setup_cron.py --auto

# Remove cron jobs
python3 scripts/setup_cron.py --remove
```

**创建 cron 条目：**
```cron
# Proactive Research - Hourly topics
0 * * * * cd /path/to/skills/proactive-research && python3 scripts/monitor.py --frequency hourly

# Proactive Research - Daily topics  
0 9 * * * cd /path/to/skills/proactive-research && python3 scripts/monitor.py --frequency daily

# Proactive Research - Weekly digest
0 18 * * 0 cd /path/to/skills/proactive-research && python3 scripts/digest.py --send
```

## AI 重要性评分

评分器使用多种信号来决定提醒的优先级：

### 评分信号

**高优先级（立即提醒）：**
- 重大突发新闻（通过新鲜度和关键词密度检测）
- 价格变化超过 10%（针对金融主题）
- 与您精确匹配的关键词的产品发布
- 您使用的工具中的安全漏洞
- 对您提出的具体问题的直接回答

**中等优先级（值得汇总）：**
- 相关新闻但不紧急
- 被跟踪产品的 minor 更新
- 您主题中的有趣发展
- 教程/指南的发布
- 社区讨论参与度高的内容

**低优先级（忽略）：**
- 重复的新闻（已经收到过提醒）
- 次要相关的内容
- 低质量的信息源
- 过时的信息
- 垃圾邮件/促销内容

### 学习模式

当启用 (`learning_enabled: true`) 时，系统：
1. 跟踪您互动的提醒
2. 根据您的行为调整评分权重
3. 建议主题优化
4. 自动调整重要性阈值

学习数据存储在 `.learning_data.json` 中（保护隐私，永不共享）。

## 记忆整合

Proactive Research 会关联您的对话历史：

**示例提醒：**
> 🔔 **Dirac Live 更新**
> 
> 发布了 3.8 版本，其中包含了您上周要求的房间校正改进。
> 
> **上下文：** 您提到在录音室中遇到低频响应的问题。此更新包含了新的低频优化。
> 
> [链接] | [完整详情]

**工作原理：**
1. 读取 `memory_hints.md` 文件（如果您创建了该文件）
2. 扫描最近的对话记录（如果有的话）
3. 将发现的内容与过去的上下文匹配
4. 生成个性化的摘要

### memory_hints.md（可选）

帮助 AI 理解您的需求：

```markdown
# Memory Hints for Proactive Research

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

## 提醒渠道

### Telegram

需要 OpenClaw 消息工具：

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

基于 Webhook 的提醒：

```json
{
  "channels": ["discord"],
  "discord_config": {
    "webhook_url": "https://discord.com/api/webhooks/...",
    "username": "Research Bot",
    "avatar_url": "https://..."
  }
}
```

### 电子邮件

通过 SMTP 或 API 发送：

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

### 提醒条件

微调提醒时机：

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

匹配特定模式：

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

防止提醒疲劳：

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

## 状态管理

### .research_state.json

记录：
- 每个主题的最后检查时间
- 已提醒的 URL（去重）
- 重要性评分历史
- 学习数据（如果启用）

示例：
```json
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

存储值得汇总的发现：

```
.findings/
├── 2026-01-22_eth-price.json
├── 2026-01-24_fm26-patches.json
└── 2026-01-27_ai-breakthroughs.json
```

## 最佳实践

1. **谨慎开始** - 初始设置 `importance_threshold: medium`，根据提醒的质量进行调整
2. **使用上下文字段** - 帮助 AI 生成更好的摘要
3. **优化关键词** - 添加负面关键词以过滤无关内容：`["AI", "-clickbait", "-spam"]`
4. **启用学习模式** - 根据您的行为逐步改进
5. **每周查看摘要** - 不要忽略摘要，它可以帮助您发现模式
6. **结合个人分析** - 根据您的聊天模式获取主题推荐

## 与其他技能的集成

### web-search-plus

自动使用智能路由：
- 产品/价格相关主题 → 使用 Serper
- 研究主题 → 使用 Tavily
- 公司/初创企业发现 → 使用 Exa

### personal-analytics

根据聊天模式推荐主题：
> “您本月已经询问了 Rust 12 次。是否希望我监控‘Rust 语言更新’？”

## 隐私与安全

- **所有数据均存储在本地** - 除了搜索 API 外，不使用任何外部服务
- **状态文件被 git 忽略** - 可以在版本控制的工作空间中安全使用
- **记忆提示可选** - 您可以控制共享的上下文
- **学习数据保留在本地** - 从不发送到 API

## 故障排除

**没有发送提醒：**
- 检查 cron 是否正在运行：`crontab -l`
- 验证渠道配置（Telegram 聊天 ID、Discord Webhook）
- 使用 `--dry-run --verbose` 运行脚本以查看评分过程

**提醒过多：**
- 提高 `importance_threshold`
- 添加速率限制
- 优化关键词（添加负面过滤器）
- 启用学习模式

**错过重要新闻：**
- 降低 `importance_threshold`
- 增加检查频率
- 扩大关键词范围
- 检查 `.research_state.json` 以查看去重问题

**摘要未生成：**
- 确认 `.findings/` 目录存在且有内容
- 检查摘要的 cron 计划
- 手动运行：`python3 scripts/digest.py --preview`

## 示例工作流程

### 跟踪产品发布

```bash
python3 scripts/manage_topics.py add "iPhone 17 Release" \
  --query "iPhone 17 announcement release date" \
  --keywords "iPhone 17,Apple event,September" \
  --frequency daily \
  --importance high \
  --channels telegram \
  --context "Planning to upgrade from iPhone 13"
```

### 监控竞争对手

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

该功能由 ClawHub 开发，使用 web-search-plus 技能进行智能搜索路由。