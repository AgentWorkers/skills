```json
{
  "name": "twitter_operations",
  "description": "全面的Twitter/X平台自动化与管理工具",
  "version": "1.0.0",
  "category": "social_media",
  "enabled": true,
  "triggers": ["twitter", "tweet", "x.com", "social media", "twitter_api"],
  "capabilities": [
    "发布推文和话题",
    "安排推文发布时间以获得最佳互动效果",
    "回复提及和私信",
    "根据关键词、标签或用户搜索推文",
    "监控热门话题和标签",
    "分析推文的表现和互动数据",
    "根据条件关注/取消关注用户",
    "点赞和转发内容",
    "创建和管理Twitter列表",
    "跟踪粉丝增长和数据分析",
    "实现Twitter机器人功能",
    "抓取推文和用户信息",
    "生成带有合适标签的推文内容",
    "管理多个Twitter账户",
    "监控品牌提及和情感分析",
    "自动回复特定关键词或模式",
    "归档推文和用户数据",
    "创建Twitter投票",
    "上传和管理媒体（图片、视频、GIF）",
    "实施速率限制和API配额管理",
    "处理Twitter认证（OAuth 1.0a/2.0）",
    "解析和格式化推文元数据",
    "将分析数据导出为CSV/JSON",
    "实时推送推文",
    "检测并响应特定用户互动",
    "批量操作（批量关注/取消关注/屏蔽）",
    "监控和参与Twitter Spaces",
    "社区管理和审核",
    "跟踪标签的使用情况",
    "监控竞争对手账户"
  ],
  "parameters": {
    "api_version": "v2",
    "auth_type": "oauth2",
    "rate_limit_mode": "conservative",
    "max_tweets_per_request": 100,
    "default_tweet_count": 10,
    "retry_attempts": 3,
    "timeout_seconds": 30,
    "media_upload_max_size_mb": 5,
    "thread_delay_seconds": 2,
    "auto_hashtag_limit": 5,
    "sentiment_analysis": true,
    "enable_streaming": false,
    "archive_tweets": true
  },
  "dependencies": [
    "tweepy>=4.14.0",
    "python-twitter-v2>=0.9.0",
    "requests>=2.31.0",
    "requests-oauthlib>=1.3.1",
    "python-dotenv>=1.0.0",
    "pandas>=2.0.0",
    "beautifulsoup4>=4.12.0",
    "schedule>=1.2.0",
    "textblob>=0.17.1",
    "Pillow>=10.0.0"
  ],
  "configuration": {
    "credentials_file": "~/.openclaw/twitter_credentials.json",
    "cache_dir": "~/.openclaw/cache/twitter",
    "log_file": "~/.openclaw/logs/twitter.log",
    "archive_dir": "~/.openclaw/archives/twitter"
  },
  "api_endpoints": {
    "tweet": "/2/tweets",
    "search": "/2/tweets/search/recent",
    "users": "/2/users",
    "timeline": "/2/users/:id/tweets",
    "likes": "/2/users/:id/likes",
    "retweets": "/2/tweets/:id/retweets",
    "followers": "/2/users/:id/followers",
    "following": "/2/users/:id/following",
    "spaces": "/2/spaces",
    "lists": "/2/lists",
    "media": "/1.1/media/upload"
  },
  "examples": [
    {
      "action": "post_tweet",
      "description": "发布一条简单的推文",
      "command": "openclaw twitter post 'Hello from OpenClaw! #automation'"
    },
    {
      "action": "post_thread",
      "description": "发布一条Twitter话题",
      "command": "openclaw twitter thread 'Thread part 1' 'Thread part 2' 'Thread part 3'"
    },
    {
      "action": "search_tweets",
      "description": "搜索最近的推文",
      "command": "openclaw twitter search '#AI OR #MachineLearning' --count 50"
    },
    {
      "action": "get_trends",
      "description": "获取热门话题",
      "command": "openclaw twitter trends --location 'United States'"
    },
    {
      "action": "analyze_account",
      "description": "分析一个Twitter账户",
      "command": "openclaw twitter analyze @username --metrics engagement,growth"
    },
    {
      "action": "schedule_tweet",
      "description": "安排推文发布时间",
      "command": "openclaw twitter schedule 'My scheduled tweet' --time '2026-02-03 10:00'"
    },
    {
      "action": "auto_reply",
      "description": "设置自动回复机制",
      "command": "openclaw twitter auto-reply --keywords 'support,help' --message 'Thanks for reaching out!'"
    },
    {
      "action": "monitormentions",
      "description": "实时监控品牌提及",
      "command": "openclaw twitter monitor @brandname --alert-webhook https://hooks.example.com"
    },
    {
      "action": "export_analytics",
      "description": "导出推文分析数据",
      "command": "openclaw twitter analytics --days 30 --format csv --output ~/twitter_stats.csv"
    },
    {
      "action": "manage_followers",
      "description": "根据条件关注用户",
      "command": "openclaw twitter follow --search '#devops' --min-followers 100 --limit 20"
    }
  ],
  "error_handling": {
    "rate_limit_exceeded": "等待并使用指数级退避策略重试",
    "authentication_failed": "检查配置文件中的凭据",
    "invalid_tweet": "发布前验证推文内容和媒体",
    "network_error": "增加延迟后重试",
    "api_deprecated": "升级到最新API版本"
  },
  "best_practices": [
    "始终遵守Twitter的速率限制和服务条款",
    "将API凭据安全地存储在环境变量或加密文件中",
    "实施适当的错误处理和日志记录",
    "使用Webhook通知重要事件",
    "缓存频繁访问的数据以减少API调用",
    "发布前验证推文内容",
    "监控API使用情况以避免超出配额",
    "逐步增加自动化操作的频率",
    "定期备份重要的推文数据和分析结果"
  ],
  "security": {
    "credential_encryption": true,
    "api_key_rotation": "推荐",
    "oauth_token_refresh": "自动更新",
    "sensitive_data_filtering": true,
    "audit_logging": true
  }
}
```