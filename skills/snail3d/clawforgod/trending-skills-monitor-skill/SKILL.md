---
name: trending-skills-monitor
description: 跟踪并发现来自ClawdHub的热门技能、新技能以及最近更新的技能。您可以根据兴趣（如3D打印、编程、自动化等）、类别或关键词进行筛选。还可以选择接收每日/每周的报告，或启用监控模式以实现持续关注。
---

# 流行技能监控器

发现Clawdbot技能生态系统中最新和最热门的技能。跟踪热门技能、新发布的技能以及最近的更新，并根据您的兴趣进行筛选。

## 快速入门

### 基本使用

```bash
# Check this week's trending skills
trending-skills-monitor

# Check last 14 days
trending-skills-monitor --days 14

# Filter by interests
trending-skills-monitor --interests "3D printing, coding, automation"

# Get top 10 trending
trending-skills-monitor --top 10

# Watch mode - check every hour
trending-skills-monitor --watch --interval 3600
```

### 输出示例

```
🔥 Trending Skills Report
============================================================
📅 2026-01-29T10:15:00.000000

✨ NEW RELEASES (Last 7 Days)
------------------------------------------------------------
  📦 webhook-listener
     Downloads: 342 | Listen for HTTP webhooks in Clawdbot... | Created: 2026-01-28

  📦 ocr-vision
     Downloads: 156 | Extract text from images using Claude vision... | Created: 2026-01-27

🔝 COMMUNITY FAVORITES (Most Installed)
------------------------------------------------------------
  🥇 #1. security-scanner
     📥 8,324 installs | ⭐ 4.8 | 📁 security

  🥈 #2. sentry-mode
     📥 7,891 installs | ⭐ 4.7 | 📁 surveillance

🔄 RECENT UPDATES
------------------------------------------------------------
  🆕 meshtastic-skill (v2.3.0)
     Updated: 2026-01-29 | Fixed GPS integration, added mesh network visualization

============================================================
📊 Total skills: 28
```

## 功能

### 1. 跟踪新技能
- 发现过去X天内发布的技能（可配置）
- 显示下载次数、描述和创建日期
- 帮助您随时了解最新发布的内容

### 2. 流行趋势分析
- 最受社区欢迎的安装/下载量最高的技能
- 按安装次数或下载次数排名
- 包含评分和类别信息
- 帮助您识别经过验证的、受欢迎的工具

### 3. 监控更新
- 跟踪最近更新的技能
- 查看版本变更和更新日志
- 知道您喜欢的技能何时得到了改进
- 避免错过重要的功能更新

### 4. 智能筛选
- 按兴趣筛选：`--interests "3D打印, 编程"`
- 按类别筛选：`--category "自动化"`
- 综合筛选以获得精确结果
- 对描述进行模糊关键词匹配

### 5. 监控模式
- 持续监控ClawdHub
- 可配置的检查间隔
- 新技能发现通知
- 帮助您尽早捕捉趋势

## 使用示例

### 示例1：每周趋势报告

```bash
trending-skills-monitor --days 7
```

获取过去7天的所有新技能、热门技能以及最近的更新。

### 示例2：关注您的兴趣

```bash
trending-skills-monitor \
  --interests "automation, data processing" \
  --days 14 \
  --format markdown
```

筛选出过去2周内与“自动化”或“数据处理”相关的技能，并以Markdown格式输出。

### 示例3：某个类别中的顶级技能

```bash
trending-skills-monitor \
  --category "iot" \
  --top 5 \
  --sort rating
```

显示按评分排序的前5个物联网（IoT）技能。

### 示例4：带有电子邮件报告的监控模式

```bash
# Run in background, check every 6 hours
trending-skills-monitor \
  --watch \
  --interval 21600 \
  --interests "3D printing" \
  --format markdown > /tmp/skills-report.txt

# Then pipe to email or Telegram
```

### 示例5：跟踪您喜欢的技能

创建一个配置文件并每天检查：

```bash
# config.json
{
  "interests": ["security", "automation", "data processing"],
  "days": 7,
  "category": "utility"
}

# Use it
trending-skills-monitor --config config.json --format json
```

## 命令参考

### 全局选项

```
--days N              Look back N days for new/updated skills (default: 7)
--interests STR       Comma-separated interests to filter by
--top N               Show top N trending skills (overrides --days)
--category STR        Filter by specific category
--sort FIELD          Sort by: downloads, installs, rating, updated, new (default: downloads)
--format FORMAT       Output format: text, json, markdown (default: text)
--watch               Enable watch mode (continuous monitoring)
--interval SECS       Check interval in seconds for watch mode (default: 3600)
--config FILE         Load settings from JSON config file
--verbose             Show debug output
--help                Show this help message
```

### 示例

```bash
# New skills from last 30 days
trending-skills-monitor --days 30

# Top 20 most installed
trending-skills-monitor --top 20 --sort installs

# Filter to automation category
trending-skills-monitor --category automation

# Multiple interests
trending-skills-monitor --interests "coding, automation, data"

# JSON output for scripting
trending-skills-monitor --format json > report.json

# Watch mode: check every 2 hours
trending-skills-monitor --watch --interval 7200

# Combine filters
trending-skills-monitor \
  --days 14 \
  --interests "security" \
  --category "surveillance" \
  --sort rating
```

## 输出格式

### 文本格式（默认）

包含表情符号的纯文本，按章节组织：
- ✨ 新发布
- 🔝 社区热门技能
- 🔄 最新更新

非常适合在终端查看和快速浏览。

### Markdown格式

```bash
trending-skills-monitor --format markdown
```

输出：
```markdown
# 🔥 Trending Skills Report

*2026-01-29T10:15:00*

## ✨ New Releases

**webhook-listener** (v1.2.0) by author-name  
Listen for HTTP webhooks in Clawdbot...  
📥 345 installs | ⭐ 4.9 | 📊 1,234 downloads
```

适合编写文档、生成报告以及发布到渠道。

### JSON格式

```bash
trending-skills-monitor --format json
```

结构化数据，适用于程序化处理：

```json
{
  "timestamp": "2026-01-29T10:15:00.000000",
  "new_skills": [
    {
      "id": "webhook-listener",
      "name": "webhook-listener",
      "description": "...",
      "author": "...",
      "downloads": 342,
      "installs": 345,
      "rating": 4.9,
      "category": "communication",
      "version": "1.2.0",
      "created_at": "2026-01-28T...",
      "updated_at": "2026-01-29T...",
      "tags": ["http", "webhook", "event"]
    }
  ],
  "trending_skills": [...],
  "updated_skills": [...],
  "filters": {
    "days": 7,
    "interests": [],
    "category": null,
    "sort": "downloads"
  }
}
```

非常适合与其他工具和自动化系统集成。

## 配置文件

创建一个JSON配置文件来保存您的偏好设置：

```json
{
  "interests": [
    "3D printing",
    "coding",
    "automation"
  ],
  "days": 7,
  "category": null,
  "sort": "downloads",
  "top": 20,
  "format": "text"
}
```

使用方法：

```bash
trending-skills-monitor --config my-config.json
```

## 智能筛选

该工具使用智能关键词匹配功能：

### 兴趣匹配
- **精确匹配**：`coding` 与 `coding-tutorials` 匹配
- **子字符串匹配**：`3d` 与 `3d-printing` 或 `3d-model-viewer` 匹配
- **模糊匹配**：`3D printing` 与包含“3D打印”、“3d-printing”或“3d-print”关键词的技能匹配
- **描述搜索**：搜索技能的描述、标签和元数据

### 类别匹配
为常见术语提供了内置的类别别名：

```
automation      → "automate", "workflow", "robot", "task"
coding          → "code", "programming", "script", "dev"
3d-printing     → "3d", "cad", "model"
data            → "analytics", "machine-learning", "ml", "ai"
web             → "http", "api", "website", "web-scraping"
iot             → "sensors", "esp32", "arduino", "hardware"
communication   → "telegram", "slack", "email", "discord"
media           → "image", "video", "audio", "photo"
```

## 监控模式

持续监控ClawdHub上的新技能和热门技能：

```bash
# Check every 30 minutes
trending-skills-monitor --watch --interval 1800

# Check every 6 hours with interests
trending-skills-monitor \
  --watch \
  --interval 21600 \
  --interests "security, automation"
```

监控模式：
- 无限期运行，按指定间隔进行检查
- 与上一次检查结果进行比较以发现新技能
- 发现新技能时显示通知
- 适用于cron作业或systemd定时器

### 与通知系统的集成

将监控模式的结果发送到Telegram：

```bash
# Assuming you have a message utility
trending-skills-monitor --format markdown | \
  message send --channel "alerts" --text "$(cat -)"
```

## 集成示例

### 每日摘要脚本

```bash
#!/bin/bash
# save as: /usr/local/bin/skills-digest.sh

trending-skills-monitor \
  --days 1 \
  --interests "automation, security" \
  --format markdown > /tmp/skills-today.md

# Send to Telegram, email, or store
cat /tmp/skills-today.md
```

通过cron每天运行：

```bash
# Add to crontab
0 9 * * * /usr/local/bin/skills-digest.sh
```

### Slack集成

```bash
#!/bin/bash
REPORT=$(trending-skills-monitor --format json)

curl -X POST https://hooks.slack.com/services/YOUR/WEBHOOK \
  -H 'Content-Type: application/json' \
  -d "{
    \"text\": \"🔥 New Skills This Week\",
    \"blocks\": [
      {
        \"type\": \"section\",
        \"text\": {
          \"type\": \"mrkdwn\",
          \"text\": \"$REPORT\"
        }
      }
    ]
  }"
```

### 筛选到仪表板

解析JSON输出并进行筛选：

```bash
# Get only highly-rated new skills
trending-skills-monitor --format json | \
  jq '.new_skills | map(select(.rating >= 4.5))'
```

## 架构

### 组件

**trending-skills-monitor**（CLI）
- 入口点，参数解析
- 路由到主监控脚本

**scripts/monitor.py**
- 主协调脚本
- 获取数据、应用筛选条件、格式化输出
- 处理监控模式逻辑

**scripts/clawdhub_api.py**
- 与ClawdHub API通信
- 测试时使用模拟数据作为备用
- 缓存响应

**scripts/filter_engine.py**
- 根据兴趣和类别进行智能筛选
- 模糊关键词匹配
- 类别别名映射

**scripts/formatter.py**
- 格式化输出（文本、JSON、Markdown）
- 提供不同的视图（排名、简洁版、详细版）

**scripts/cache.py**
- 简单的基于文件的缓存机制
- 可配置的缓存有效期（TTL）
- 监控模式状态跟踪

### 数据流

```
CLI args
  ↓
monitor.py (orchestrator)
  ↓
ClawdHubAPI → Fetch (new, trending, updated)
  ↓
FilterEngine → Apply interests/categories
  ↓
Formatter → Format output
  ↓
Print results
```

## 配置

### 环境变量

```bash
# ClawdHub API configuration
export CLAWDHUB_API_URL="https://hub.clawdbot.com/api/v1"
export CLAWDHUB_API_KEY="your-api-key-here"
```

### 缓存位置

缓存文件存储在：`~/.cache/trending-skills-monitor/`

清除缓存：

```bash
rm -rf ~/.cache/trending-skills-monitor/
```

## 需求

### 系统依赖
- Python 3.7及以上版本
- requests库（`pip install requests`）

### API要求
- 需要访问ClawdHub API（测试时可以使用模拟数据）
- 可选：用于身份验证的API密钥

### 网络
- 需要连接到ClawdHub
- 如果无法连接，则自动切换到模拟数据

## 故障排除

### 未返回结果

```bash
# Debug with verbose output
trending-skills-monitor --verbose

# Check if interests are matching
trending-skills-monitor --interests "automation" --verbose

# Try broader search
trending-skills-monitor --days 30
```

### API错误

如果您看到API错误但希望继续测试：

```bash
# Will use mock data
CLAWDHUB_API_URL="http://invalid" trending-skills-monitor
```

### 监控模式未检测到新技能

```bash
# Check cache status
ls ~/.cache/trending-skills-monitor/

# Clear cache
rm ~/.cache/trending-skills-monitor/*

# Restart watch mode
trending-skills-monitor --watch --verbose
```

## 未来改进计划

计划中的功能：
- [ ] Webhook通知（Telegram、Discord、Slack）
- [ ] 定期报告（每日/每周电子邮件）
- [ ] 基于已安装技能的技能推荐
- [ ] 技能对比功能（“类似于X的技能”）
- [ ] 用户评分/评论汇总
- [ ] 导出到日历（即将发布的技能）
- [ ] 基于AI的技能摘要
- [ ] 技能依赖关系跟踪

## 脚本参考

该工具包含以下Python脚本：

- **monitor.py** - 主协调脚本（10KB）
- **clawdhub_api.py** - API客户端（8KB）
- **filter_engine.py** - 筛选逻辑（6KB）
- **formatter.py** - 输出格式化脚本（6KB）
- **cache.py** - 缓存脚本（2KB）

## 许可证与支持

该工具属于Clawdbot生态系统的一部分。如有问题或建议，请查看ClawdHub仓库。

---

**最后更新时间：** 2026-01-29
**版本：** 1.0.0