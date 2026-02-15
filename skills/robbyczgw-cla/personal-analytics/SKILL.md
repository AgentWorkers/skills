---
name: personal-analytics
description: 分析对话模式、追踪工作效率，并揭示关于个人认知的见解。适用于用户希望了解自己的交流习惯（如聊天内容、讨论的主题、工作效率趋势以及情绪变化）的情况。提供每周/每月的报告、主题推荐以及基于时间的分析结果。该工具采用以隐私保护为核心的设计理念，所有分析数据均存储在本地。
---

# 个人分析工具

**了解自己，更高效地工作，发现那些你未曾察觉的规律。**

个人分析工具会分析你的对话模式，从而揭示关于你的工作方式、兴趣和效率的实用见解——同时确保你的数据完全保密且仅存储在本地。

## 核心功能

1. **会话分析** - 分析你的聊天时长及效率模式
2. **主题追踪** - 常被提及的主题及当前的热门兴趣
3. **情绪分析** - 随时间变化的情绪状态及压力指标
4. **效率洞察** - 你最有效的工作时段
5. **周/月度报告** - 以美观的形式呈现你的数据模式
6. **主题推荐** - 自动推荐值得主动研究的主题

## 首先考虑隐私

🔒 **所有分析都在本地进行，数据不会离开你的设备。**

- 原始对话 **从不** 被存储
- 仅保存汇总统计信息
- 需要用户主动启用功能
- 可随时删除数据
- 无外部API用于数据分析
- Git会忽略数据文件

## 快速入门

```bash
# Initialize
cp config.example.json config.json

# Enable tracking
python3 scripts/enable.py

# Analyze current sessions
python3 scripts/analyze.py

# Generate report
python3 scripts/report.py weekly

# Get topic recommendations
python3 scripts/recommend.py
```

## 被追踪的内容

### 会话元数据
- 时间戳（开始/结束）
- 会话时长
- 消息数量
- 主要讨论的主题
- 情绪（积极/中立/消极/混合）
- 效率标记（完成任务、做出决策）

### 汇总统计
- 每小时活动热图
- 主题频率随时间变化的情况
- 不同时间段的工作效率
- 情绪趋势

### 不被追踪的内容
- ❌ 原始消息内容
- ❌ 个人信息
- ❌ 敏感数据（密码、密钥等）
- ❌ 具体对话内容

## 配置

### config.json

```json
{
  "enabled": true,
  "tracking": {
    "sessions": true,
    "topics": true,
    "sentiment": true,
    "productivity": true
  },
  "privacy": {
    "min_aggregation_window_hours": 24,
    "auto_delete_after_days": 90,
    "exclude_patterns": ["password", "secret", "token", "key"]
  },
  "insights": {
    "productivity_markers": [
      "completed", "shipped", "fixed", "merged", "deployed"
    ],
    "stress_indicators": [
      "urgent", "asap", "critical", "broken", "emergency"
    ]
  },
  "reports": {
    "weekly_day": "sunday",
    "weekly_time": "20:00",
    "auto_send": false
  },
  "integrations": {
    "proactive_research": {
      "auto_suggest_topics": true,
      "suggestion_threshold": 3
    }
  }
}
```

## 脚本

### analyze.py

分析对话模式：

```bash
# Analyze all available data
python3 scripts/analyze.py

# Analyze specific time range
python3 scripts/analyze.py --since "2026-01-01" --until "2026-01-31"

# Analyze and show insights
python3 scripts/analyze.py --insights

# Verbose output
python3 scripts/analyze.py --verbose
```

**输出：**
```
📊 Personal Analytics Analysis

Period: Jan 1 - Jan 28, 2026 (28 days)

Session Summary:
  Total sessions: 145
  Total time: 18h 32m
  Avg session: 7m 40s
  Most active: Tuesday 10:00-11:00

Topics (Top 10):
  1. Python (32 sessions)
  2. FM26 (28 sessions)
  3. Dirac Live (15 sessions)
  4. ETH/crypto (12 sessions)
  5. Docker (11 sessions)
  ...

Productivity:
  High productivity: 09:00-12:00, 14:00-16:00
  Low productivity: Late night (after 22:00)
  Peak day: Wednesday
  
Sentiment:
  Positive: 62%
  Neutral: 28%
  Negative: 8%
  Mixed: 2%
```

### report.py

生成美观的报告：

```bash
# Weekly report
python3 scripts/report.py weekly

# Monthly report
python3 scripts/report.py monthly

# Custom range
python3 scripts/report.py custom --since "2026-01-01" --until "2026-01-31"

# Export to file
python3 scripts/report.py weekly --output report.md

# Send via Telegram
python3 scripts/report.py weekly --send
```

**报告格式：**

```markdown
# 📊 Weekly Analytics Report
**Jan 22 - Jan 28, 2026**

## 🎯 Highlights

- **Most productive day:** Wednesday (4 tasks completed)
- **Peak hours:** 09:00-11:00 (3h 45m focused work)
- **Emerging topic:** Rust (mentioned 12 times, +200% from last week)
- **Mood trend:** ↗️ Improving (78% positive, up from 65%)

## ⏰ Time Patterns

### Activity Heatmap
```
周一  ████░░░░░░░░░░░░░░░░░░░░  4小时
周二  ██████████░░░░░░░░░░░░ 6小时30分钟
周三  ████████████░░░░░░░░░░ 8小时15分钟  ← 高效时段
周四  ██████░░░░░░░░░░░░░ 5小时
周五  ████░░░░░░░░░░░░░░ 3小时45分钟
周六  ██░░░░░░░░░░░░░░░ 1小时30分钟
周日  ░░░░░░░░░░░░░░░ 45分钟
```

### Hourly Distribution
```
06-09: ██░░░░░░░░  (12%)
09-12: ████████░░  (38%)  ← 高效时段
12-14: ███░░░░░░  (15%)
14-17: █████░░░░  (24%)
17-22: ██░░░░░  (11%)
```

## 📚 Topic Insights

### Top Topics This Week
1. **Python Development** (32 sessions)
   - Focus: FastAPI, async, testing
   - Trend: Steady
   - Suggestion: Monitor "Python 3.13 features"

2. **FM26** (28 sessions)
   - Focus: Tactics, transfers, editor
   - Trend: ↗️ +15%
   - Suggestion: Already monitoring "FM26 patches" ✓

3. **Audio Engineering** (15 sessions)
   - Focus: Dirac Live, room correction, bass management
   - Trend: 🆕 New topic
   - Suggestion: Monitor "Dirac Live updates"

### Emerging Topics
- **Rust** (12 mentions, first appearance)
- **Kubernetes** (8 mentions, +300%)
- **Machine Learning** (6 mentions)

## 💡 Productivity Insights

### Task Completion
- Total tasks: 23 completed
- Success rate: 87%
- Best day: Wednesday (6 tasks)
- Best time: Morning (09:00-12:00)

### Focus Sessions
- Long sessions (>30m): 8
- Average focus time: 18m
- Longest session: 1h 42m (Wed 10:15)

### Problem-Solving Speed
- Quick wins (<15m): 14 problems
- Complex issues (>1h): 3 problems
- Average: 24m per problem

## 😊 Sentiment & Well-being

### Overall Mood
```
😊 积极情绪  ████████████████░  78%  (↑13%)
😐 中立情绪  ████░░░░░░░░ 18%
😟 消极情绪  ██░░░░░░ 4%
```

### Stress Indicators
- High stress: 3 sessions (down from 7)
- Urgent keywords: 5 (down from 12)
- Late-night work: 2 sessions (down from 8)

**Insight:** Stress levels decreasing. Good work-life balance this week! 🎉

## 🎯 Recommendations

### For Proactive Research
Based on your interests this week, consider monitoring:
1. **Rust language updates** (mentioned 12x, new interest)
2. **Dirac Live releases** (mentioned 15x, active problem-solving)
3. **Kubernetes security** (mentioned 8x, DevOps focus)

### Productivity Tips
- **Schedule deep work 09:00-11:00** (your peak productivity)
- **Batch meetings after lunch** (14:00-16:00 is secondary peak)
- **Avoid late-night sessions** (22% slower problem-solving)

### Topics to Explore
Based on your current interests, you might enjoy:
- Async Rust patterns (combines Rust + async focus)
- Kubernetes observability (combines K8s + monitoring)
- Audio DSP with Python (combines audio + Python)

---

_Generated by Personal Analytics • Privacy-first, locally processed_
```

### recommend.py

生成值得主动研究的主题推荐：

```bash
# Get recommendations
python3 scripts/recommend.py

# Show reasoning
python3 scripts/recommend.py --explain

# Auto-add to proactive-research
python3 scripts/recommend.py --auto-add

# Set threshold (minimum mentions)
python3 scripts/recommend.py --threshold 5
```

**输出：**
```
💡 Topic Recommendations for Proactive Research

Based on your conversation patterns:

1. Rust Language Updates
   Mentioned: 12 times this week (new topic)
   Reason: Emerging interest, high engagement
   Suggested query: "Rust language updates releases"
   Suggested frequency: weekly
   
2. Dirac Live Updates
   Mentioned: 15 times this week
   Reason: Active problem-solving, technical depth
   Suggested query: "Dirac Live update release"
   Suggested frequency: daily
   
3. FM26 Patches
   Mentioned: 28 times this week
   Reason: Consistent interest over time
   NOTE: Already monitoring! ✓

Would you like to add these topics to proactive-research? [y/N]
```

### session_tracker.py

跟踪由Moltbot调用的会话：

```bash
# Log session start
python3 scripts/session_tracker.py start --channel telegram

# Log session end
python3 scripts/session_tracker.py end --session-id <id>

# Log message (topics, sentiment)
python3 scripts/session_tracker.py message --session-id <id> \
  --topics "Python,Docker" \
  --sentiment positive
```

此脚本专为通过Moltbot的钩子调用设计，不可手动执行。

### enable.py / disable.py

管理数据追踪功能：

```bash
# Enable tracking
python3 scripts/enable.py

# Disable tracking
python3 scripts/disable.py

# Show status
python3 scripts/status.py
```

## 与Moltbot的集成

个人分析工具可以与Moltbot的会话生命周期集成：

### 钩子点

1. **会话开始** - 记录时间戳和频道
2. **会话结束** - 计算时长并保存统计信息
3. **收到消息** - 提取主题（简化处理）并检测情绪

### 推荐的设置方式

将相关配置添加到Moltbot的SOUL.md文件中：

```markdown
## Personal Analytics Integration

After each session ends, if personal-analytics is enabled:
1. Extract primary topics discussed (max 5)
2. Determine overall sentiment
3. Detect productivity markers (tasks completed)
4. Log to personal-analytics via session_tracker.py
```

## 数据存储

### .analytics_data.json

仅保存汇总统计信息：

```json
{
  "sessions": [
    {
      "id": "session_uuid",
      "start": "2026-01-28T10:00:00Z",
      "end": "2026-01-28T10:15:00Z",
      "duration_seconds": 900,
      "channel": "telegram",
      "topics": ["Python", "Docker"],
      "sentiment": "positive",
      "productivity_score": 0.8,
      "tasks_completed": 1
    }
  ],
  "topic_stats": {
    "Python": {
      "total_mentions": 145,
      "last_seen": "2026-01-28T10:15:00Z",
      "trend": "stable"
    }
  },
  "time_stats": {
    "hourly_distribution": {
      "09": 23, "10": 45, "11": 38, ...
    },
    "daily_distribution": {
      "monday": 120, "tuesday": 98, ...
    }
  },
  "sentiment_stats": {
    "positive": 145,
    "neutral": 62,
    "negative": 18,
    "mixed": 5
  }
}
```

### .topic_cache.json

主题提取缓存（临时文件）：

```json
{
  "hash_12345": ["Python", "FastAPI", "testing"],
  "hash_67890": ["FM26", "tactics"]
}
```

缓存文件会在7天后自动删除。

## 洞察与规律

### 基于时间的洞察

**按小时分析效率：**
- 分析每小时的任务完成率
- 确定高效工作时段
- 提供最佳工作安排建议

**每周工作模式：**
- 每天的活动水平
- 最适合深入工作的日子
- 会议较多与专注工作的日子对比

### 主题洞察

**主题聚类：**
- 将相关主题分组
- 发现新的兴趣点
- 检测主题趋势（上升/下降/稳定）

**深度分析：**
- 表面提及与深入讨论的区别
- 问题解决类主题与闲聊类主题的对比
- 技术类与非技术类主题的比例

### 情绪洞察

**情绪追踪：**
- 整体情绪趋势
- 与时间段的关联
- 压力指标的检测

**健康指标：**
- 深夜工作的频率
- 紧急/压力相关的关键词
- 工作与生活的平衡指标

## 隐私控制

### 敏感数据的排除

自动排除敏感数据：

```json
{
  "privacy": {
    "exclude_patterns": [
      "password", "token", "key", "secret",
      "credit card", "ssn", "api key"
    ]
  }
}
```

### 数据保留

自动删除旧数据：

```json
{
  "privacy": {
    "auto_delete_after_days": 90,
    "keep_aggregated_stats": true
  }
}
```

### 手动删除

```bash
# Delete all data
python3 scripts/delete_data.py --all

# Delete specific date range
python3 scripts/delete_data.py --since "2026-01-01" --until "2026-01-31"

# Delete specific topics
python3 scripts/delete_data.py --topics "topic1,topic2"
```

## 高级功能

### 定义效率标准

自定义“效率”的定义：

```json
{
  "insights": {
    "productivity_markers": [
      "completed", "shipped", "merged", "deployed",
      "fixed", "resolved", "closed", "published"
    ]
  }
}
```

### 主题推荐

根据以下条件自动推荐主题：
- 主题出现的频率（N次以上）
- 主题趋势（兴趣增长）
- 问题解决的模式（技术深度）
- 时间模式（频繁讨论的主题）

### 报告定制

```json
{
  "reports": {
    "include_sections": [
      "time_patterns",
      "topic_insights",
      "productivity",
      "sentiment",
      "recommendations"
    ],
    "exclude_topics": ["personal", "family"],
    "min_session_count": 5
  }
}
```

## 使用场景

### 🎯 优化工作安排
发现你的高效时段，并据此安排深度工作。

### 📚 跟踪学习过程
了解你关注的主题、关注程度以及知识缺口。

### 🧘 监控健康状况
追踪压力指标、深夜工作情况和情绪趋势。

### 🔍 发现规律
发现你未曾注意到的兴趣点。

### 🤝 提升协作效率
了解你最能响应的时间，并据此安排会议。

### 💡 生成内容灵感
你讨论最多的主题是宝贵的内容资源。

## 最佳实践

1. **每周生成报告** - 设置每周自动生成报告
2. **查看推荐主题** - 每月检查主题推荐
3. **调整隐私设置** - 从保守开始，根据需要逐步调整
4. **结合主动研究使用** - 将洞察转化为自动化监控
5. **不要过度优化** - 洞察是参考，而非绝对规则

## 故障排除

**未收集数据：**
- 确保已启用数据追踪：`python3 scripts/status.py`
- 检查Moltbot集成是否激活
- 执行手动分析：`python3 scripts/analyze.py --verbose`

**情绪分析不准确：**
- 情绪检测基于启发式方法
- 可在后续版本中进行调整

**主题缺失：**
- 主题提取依赖于关键词匹配
- 如果配置过于严格，可降低匹配阈值

**隐私问题：**
- 查看`.analytics_data.json`文件——仅保存汇总统计信息
- 可随时删除数据：`python3 scripts/delete_data.py --all`
- 禁用数据追踪：`python3 scripts/disable.py`

## 致谢

本工具专为ClawdHub开发，其隐私保护设计灵感来源于“量化自我”（Quantified Self）理念。