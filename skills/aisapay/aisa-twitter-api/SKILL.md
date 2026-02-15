---
name: Twitter Command Center (Search + Post)
description: "实时搜索 X（Twitter）平台上的内容，提取相关帖子，并立即发布推文或回复——非常适合用于社交监听、用户互动以及快速的内容管理。"
homepage: https://openclaw.ai
metadata: {"openclaw":{"emoji":"🐦","requires":{"bins":["curl","python3"],"env":["AISA_API_KEY"]},"primaryEnv":"AISA_API_KEY"}}
---

# OpenClaw Twitter 🐦

**专为自主代理设计的Twitter/X数据访问与自动化工具。由AIsa提供支持。**

只需一个API密钥，即可全面获取Twitter的所有功能。

## 🔥 您能做什么？

### 监控影响者
```
"Get Elon Musk's latest tweets and notify me of any AI-related posts"
```

### 跟踪趋势
```
"What's trending on Twitter worldwide right now?"
```

### 社交监听
```
"Search for tweets mentioning our product and analyze sentiment"
```

### 自动互动
```
"Like and retweet posts from @OpenAI that mention GPT-5"
```

### 竞争对手分析
```
"Monitor @anthropic and @GoogleAI - alert me on new announcements"
```

## 快速入门

```bash
export AISA_API_KEY="your-key"
```

## 核心功能

### 读取数据（无需登录）
```bash
# Get user info
curl "https://api.aisa.one/apis/v1/twitter/user/info?userName=elonmusk" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Get user's latest tweets
curl "https://api.aisa.one/apis/v1/twitter/user/user_last_tweet?userName=elonmusk" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Advanced tweet search (queryType is required: Latest or Top)
curl "https://api.aisa.one/apis/v1/twitter/tweet/advanced_search?query=AI+agents&queryType=Latest" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Search top tweets
curl "https://api.aisa.one/apis/v1/twitter/tweet/advanced_search?query=AI+agents&queryType=Top" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Get trending topics (worldwide)
curl "https://api.aisa.one/apis/v1/twitter/trends?woeid=1" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Search users by keyword
curl "https://api.aisa.one/apis/v1/twitter/user/search_user?keyword=AI+researcher" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Get tweets by ID
curl "https://api.aisa.one/apis/v1/twitter/tweet/tweetById?tweet_ids=123456789" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Get user followers
curl "https://api.aisa.one/apis/v1/twitter/user/user_followers?userName=elonmusk" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Get user followings
curl "https://api.aisa.one/apis/v1/twitter/user/user_followings?userName=elonmusk" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### 写入数据（需要登录）
> ⚠️ **警告**：发布内容需要登录账户。请谨慎使用，以避免触发速率限制或导致账户被暂停。

```bash
# Step 1: Login first (async, check status after)
curl -X POST "https://api.aisa.one/apis/v1/twitter/user_login_v3" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_name":"myaccount","email":"me@example.com","password":"xxx","proxy":"http://user:pass@ip:port"}'

# Step 2: Check login status
curl "https://api.aisa.one/apis/v1/twitter/get_my_x_account_detail_v3?user_name=myaccount" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Send tweet
curl -X POST "https://api.aisa.one/apis/v1/twitter/send_tweet_v3" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_name":"myaccount","text":"Hello from OpenClaw!"}'

# Like a tweet
curl -X POST "https://api.aisa.one/apis/v1/twitter/like_tweet_v3" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_name":"myaccount","tweet_id":"1234567890"}'

# Retweet
curl -X POST "https://api.aisa.one/apis/v1/twitter/retweet_v3" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_name":"myaccount","tweet_id":"1234567890"}'

# Update profile
curl -X POST "https://api.aisa.one/apis/v1/twitter/update_profile_v3" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_name":"myaccount","name":"New Name","bio":"New bio"}'
```

## Python客户端
```bash
# User operations
python3 {baseDir}/scripts/twitter_client.py user-info --username elonmusk
python3 {baseDir}/scripts/twitter_client.py tweets --username elonmusk
python3 {baseDir}/scripts/twitter_client.py followers --username elonmusk
python3 {baseDir}/scripts/twitter_client.py followings --username elonmusk

# Search & Discovery
python3 {baseDir}/scripts/twitter_client.py search --query "AI agents"
python3 {baseDir}/scripts/twitter_client.py user-search --keyword "AI researcher"
python3 {baseDir}/scripts/twitter_client.py trends --woeid 1

# Post operations (requires login)
python3 {baseDir}/scripts/twitter_client.py login --username myaccount --email me@example.com --password xxx --proxy "http://user:pass@ip:port"
python3 {baseDir}/scripts/twitter_client.py post --username myaccount --text "Hello!"
python3 {baseDir}/scripts/twitter_client.py like --username myaccount --tweet-id 1234567890
python3 {baseDir}/scripts/twitter_client.py retweet --username myaccount --tweet-id 1234567890
```

## API端点参考

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/twitter/user/info` | GET | 获取用户信息 |
| `/twitter/user/user_last_tweet` | GET | 获取用户的最新推文 |
| `/twitter/user/user_followers` | GET | 获取用户的关注者 |
| `/twitter/user/user_followings` | GET | 获取用户关注的对象 |
| `/twitter/user/search_user` | GET | 通过关键词搜索用户 |
| `/twitter/tweet/advanced_search` | GET | 高级推文搜索 |
| `/twitter/tweet/tweetById` | GET | 通过ID获取推文 |
| `/twitter/trends` | GET | 获取热门话题 |
| `/twitter/user_login_v3` | POST | 登录账户 |
| `/twitter/send_tweet_v3` | POST | 发布推文 |
| `/twitter/like_tweet_v3` | POST | 点赞推文 |
| `/twitter/retweet_v3` | POST | 转发推文 |

## 价格

| API | 费用 |
|-----|------|
| Twitter数据读取 | 约0.0004美元 |
| Twitter内容发布/点赞/转发 | 约0.001美元 |

每个响应都会包含`usage.cost`和`usage.credits_remaining`信息。

## 开始使用

1. 在[aisa.one](https://aisa.one)注册账号。
2. 获取您的API密钥。
3. 购买相应的信用额度（按需付费）。
4. 设置环境变量：`export AISA_API_KEY="您的API密钥"`。

## 完整API参考

请访问[API参考文档](https://aisa.mintlify.app/api-reference/introduction)以获取完整的端点说明。