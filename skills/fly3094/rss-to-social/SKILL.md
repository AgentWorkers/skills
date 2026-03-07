---
name: rss-to-social
description: 自动监控 RSS 源，并将内容发布到社交媒体上。通过 AI 安排发布时间，生成帖子，并将它们发布到 Twitter/LinkedIn 上。
author: fly3094
version: 1.0.0
tags: [rss, social-media, automation, twitter, linkedin, scheduling, content]
metadata:
  clawdbot:
    emoji: 📰
    requires:
      bins:
        - python3
        - curl
      env:
        - RSS_FEED_URLS
        - SOCIAL_PLATFORMS
    config:
      env:
        RSS_FEED_URLS:
          description: Comma-separated RSS feed URLs to monitor
          required: true
          example: "https://example.com/feed.xml,https://news.com/rss"
        SOCIAL_PLATFORMS:
          description: Target platforms (twitter,linkedin,all)
          default: "twitter"
          required: false
        POST_INTERVAL_HOURS:
          description: Hours between posts
          default: "4"
          required: false
        AI_MODEL:
          description: AI model for content generation
          default: "default"
          required: false
        INCLUDE_HASHTAGS:
          description: Add hashtags to posts
          default: "true"
          required: false
---
# RSS到社交媒体的自动发布工具 📰

该工具可自动监控RSS源，利用人工智能生成吸引人的社交媒体帖子，并按预定时间进行发布。

## 功能介绍

- 📰 **RSS监控**：跟踪多个RSS源以获取新内容
- 🤖 **人工智能内容生成**：自动生成适合各平台的帖子
- ⏰ **定时发布**：在最佳时间发布（可配置间隔）
- 🔄 **多平台支持**：支持Twitter、LinkedIn或同时支持两者
- 📊 **智能去重**：避免重复发布相同内容
- 🔗 **自动添加链接**：包含原文链接

## 安装

```bash
clawhub install rss-to-social
```

## 配置

### 必需的环境变量

```bash
# RSS feeds to monitor (comma-separated)
export RSS_FEED_URLS="https://techcrunch.com/feed/,https://news.ycombinator.com/rss"

# Target platforms: twitter, linkedin, or all
export SOCIAL_PLATFORMS="twitter"

# Hours between posts (default: 4)
export POST_INTERVAL_HOURS="4"
```

### 可选的环境变量

```bash
# AI model for content generation
export AI_MODEL="default"

# Include hashtags (true/false)
export INCLUDE_HASHTAGS="true"

# Twitter-specific (if direct posting enabled)
export TWITTER_API_KEY="your_key"
export TWITTER_API_SECRET="your_secret"
export TWITTER_ACCESS_TOKEN="your_token"
export TWITTER_ACCESS_TOKEN_SECRET="your_token_secret"

# LinkedIn-specific (if direct posting enabled)
export LINKEDIN_ACCESS_TOKEN="your_token"
```

## 使用方法

### 单次发布
```
Check RSS feeds and post latest content to social media
```

### 启动持续监控
```
Start RSS monitoring and auto-posting every 4 hours
```

### 检查状态
```
Show RSS monitoring status and recent posts
```

### 停止监控
```
Stop RSS auto-posting
```

### 平台特定设置
```
Post to LinkedIn only from RSS feeds
```

## 输出示例

### Twitter帖子
```
🚀 New: OpenClaw Releases Major Update

Key features:
• New skill marketplace
• Improved browser automation  
• 50% performance boost

Read more: https://techcrunch.com/article

#OpenClaw #AI #Automation
```

### LinkedIn帖子
```
Exciting developments in AI automation!

OpenClaw just announced a major update with three game-changing features:

1️⃣ New skill marketplace with 100+ integrations
2️⃣ Improved browser automation for complex workflows
3️⃣ 50% performance improvement across all operations

This is a significant step forward for personal AI assistants.

What features are you most excited about?

Read the full announcement: https://techcrunch.com/article

#ArtificialIntelligence #Automation #Productivity #Tech
```

## 安排发布时间

### 使用OpenClaw调度器
```
Every 4 hours, check RSS and post new content
```

### 使用Cron任务
```bash
# Add to crontab (every 4 hours)
0 */4 * * * cd /path/to/workspace && openclaw run "Check RSS and post"
```

### 使用Systemd定时器
```ini
# /etc/systemd/system/rss-to-social.timer
[Unit]
Description=RSS to Social Auto-Poster

[Timer]
OnBootSec=5min
OnUnitActiveSec=4h
Unit=rss-to-social.service

[Install]
WantedBy=timers.target
```

## 特点

### 智能内容生成
- **引人注目的开头**：人工智能自动生成吸引读者的开头
- **平台适配**：根据平台调整内容长度和格式
- **标签建议**：根据内容推荐相关标签
- **链接缩短**：可选的URL缩短功能，使帖子更简洁

### 去重机制
- 记录已发布的URL到`.rss-to-social/posted.json`文件中
- 确保不重复发布相同内容
- 默认保留30天的发布记录

### 多源支持
- 可监控无限数量的RSS源
- 支持优先级排序（优先级最高的源优先发布）
- 支持按类别筛选内容

## 集成能力

- ✅ 与social-media-automator兼容（可触发该工具）
- ✅ 通过API与Buffer/Hootsuite集成
- ✅ 直接通过Twitter API发布
- ✅ 直接通过LinkedIn API发布
- ✅ 通过Telegram/WhatsApp进行发布前审核（可选）

### 审核流程（可选）
对于敏感账户，可启用发布前审核功能：

```
When new RSS content found, send to Telegram for approval before posting
```

## 常见问题及解决方法

### 未生成帖子
- 检查RSS_feed_URLS的格式（以逗号分隔的有效URL）
- 确保RSS源中有新内容
- 检查人工智能模型的可用性

### 发布失败
- 验证API凭证
- 检查API的使用频率限制
- 根据平台要求进行调整

### 重复发布
- 如有需要，清空`.rss-to-social/posted.json`文件
- 调整去重窗口设置

## 使用场景

- **科技新闻聚合**：监控科技博客，自动分享到Twitter以展示专业见解
- **行业动态**：跟踪行业RSS源，在LinkedIn上分享行业资讯
- **内容策划**：为特定领域打造精选新闻账号
- **个人品牌建设**：自动化管理社交账号内容，同时保持内容质量

## 商业化方案

该工具为LobsterLabs的内容自动化服务提供支持：
- **设置与配置**：一次性费用299美元
- **每月管理**：499美元/月（包含监控、优化和报告服务）
- **定制集成**：每小时150美元

联系方式：PayPal 492227637@qq.com

## 更新日志

### 1.0.0 (2026-03-07)
- 首次发布
- 支持RSS源监控
- 引入人工智能内容生成功能
- 支持Twitter和LinkedIn平台
- 实现去重机制
- 完善调度功能集成