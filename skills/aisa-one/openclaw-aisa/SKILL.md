---
name: openclaw-starter-kit
description: "将100多个API密钥替换为一个即可。从而实现即时访问大语言模型（LLMs）、Twitter、YouTube、LinkedIn、金融数据以及Tavily和Scholar的数据。为您的本地代理提供企业级稳定性保障。"
homepage: https://openclaw.ai
metadata: {"openclaw":{"emoji":"🦞","requires":{"bins":["curl","python3"],"env":["AISA_API_KEY"]},"primaryEnv":"AISA_API_KEY"}}
---

# OpenClaw 入门套件 🦞

**自主代理的完美起点。由 AIsa 提供支持。**

只需一个 API 密钥，即可获取您的代理所需的所有数据源。

## 🔥 您能做什么？

### 早晨简报（定时）
```
"Send me a daily briefing at 8am with:
- My portfolio performance (NVDA, TSLA, BTC)
- Twitter trends in AI
- Top news in my industry"
```

### 竞争对手情报
```
"Monitor @OpenAI - alert me on new tweets, news mentions, and paper releases"
```

### 投资研究
```
"Full analysis on NVDA: price trends, insider trades, analyst estimates, 
SEC filings, and Twitter sentiment"
```

### 创业项目评估
```
"Research the market for AI writing tools - find competitors, 
Twitter discussions, and academic papers on the topic"
```

### 加密货币大户预警
```
"Track large BTC movements and correlate with Twitter activity"
```

## AIsa 与 bird 的对比

| 功能 | AIsa ⚡ | bird 🐦 |
|---------|---------|---------|
| 认证方式 | API 密钥（简单） | 浏览器 Cookie（复杂） |
| 阅读 Twitter 内容 | ✅ | ✅ |
| 发布/点赞/转发 | ✅（需登录） | ✅ |
| 网页搜索 | ✅ | ❌ |
| 学术资源搜索 | ✅ | ❌ |
| 新闻/财经信息 | ✅ | ❌ |
| LLM 路由功能 | ✅ | ❌ |
| 服务器友好性 | ✅ | ❌ |
| 成本 | 按使用量计费 | 免费 |

**适合使用 AIsa 的场景**：服务器环境、需要使用搜索/学术 API、偏好简单的 API 密钥设置。
**适合使用 bird 的场景**：本地机器、需要免费访问、需要复杂的 Twitter 操作。

## 快速入门

```bash
export AISA_API_KEY="your-key"
```

## 核心功能

### 阅读 Twitter/X 内容
```bash
# Get user info
curl "https://api.aisa.one/apis/v1/twitter/user/info?userName=elonmusk" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Advanced tweet search
curl "https://api.aisa.one/apis/v1/twitter/tweet/advanced_search?query=AI+agents&queryType=Latest" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Get trending topics (worldwide)
curl "https://api.aisa.one/apis/v1/twitter/trends?woeid=1" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### 发布 Twitter/X 内容
> ⚠️ **警告**：发布内容需要登录账户。请谨慎使用，以避免超出使用频率限制或导致账户被封禁。

```bash
# Step 1: Login first (async, check status after)
curl -X POST "https://api.aisa.one/apis/v1/twitter/user_login_v3" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_name":"myaccount","email":"me@example.com","password":"xxx","proxy":"http://user:pass@ip:port"}'

# Step 2: Send tweet
curl -X POST "https://api.aisa.one/apis/v1/twitter/send_tweet_v3" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_name":"myaccount","text":"Hello from OpenClaw!"}'

# Like / Retweet
curl -X POST "https://api.aisa.one/apis/v1/twitter/like_tweet_v3" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_name":"myaccount","tweet_id":"1234567890"}'
```

### 搜索（网页 + 学术资源）
```bash
# Web search
curl -X POST "https://api.aisa.one/apis/v1/scholar/search/web?query=AI+frameworks&max_num_results=10" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Academic/scholar search
curl -X POST "https://api.aisa.one/apis/v1/scholar/search/scholar?query=transformer+models&max_num_results=10" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Smart search (web + academic combined)
curl -X POST "https://api.aisa.one/apis/v1/scholar/search/smart?query=machine+learning&max_num_results=10" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### 财经新闻
```bash
# Company news by ticker
curl "https://api.aisa.one/apis/v1/financial/news?ticker=AAPL&limit=10" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### LLM 路由功能（兼容 OpenAI）
```bash
curl -X POST "https://api.aisa.one/v1/chat/completions" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4", "messages": [{"role": "user", "content": "Hello"}]}'
```

支持的模型：GPT-4、Claude-3、Gemini、Qwen、Deepseek、Grok 等。

## Python 客户端
```bash
# Twitter Read
python3 {baseDir}/scripts/aisa_client.py twitter user-info --username elonmusk
python3 {baseDir}/scripts/aisa_client.py twitter search --query "AI agents"
python3 {baseDir}/scripts/aisa_client.py twitter trends --woeid 1

# Twitter Write (requires login first)
python3 {baseDir}/scripts/aisa_client.py twitter login --username myaccount --email me@example.com --password xxx --proxy "http://user:pass@ip:port"
python3 {baseDir}/scripts/aisa_client.py twitter post --username myaccount --text "Hello!"
python3 {baseDir}/scripts/aisa_client.py twitter like --username myaccount --tweet-id 1234567890

# Search
python3 {baseDir}/scripts/aisa_client.py search web --query "latest AI news"
python3 {baseDir}/scripts/aisa_client.py search scholar --query "LLM research"
python3 {baseDir}/scripts/aisa_client.py search smart --query "machine learning"

# News
python3 {baseDir}/scripts/aisa_client.py news --ticker AAPL

# LLM
python3 {baseDir}/scripts/aisa_client.py llm complete --model gpt-4 --prompt "Explain quantum computing"
```

## 价格信息

| API 功能 | 成本 |
|---------|------|
| Twitter 查询 | 约 0.0004 美元 |
| Twitter 发布/点赞 | 约 0.001 美元 |
| 网页搜索 | 约 0.001 美元 |
| 学术资源搜索 | 约 0.002 美元 |
| 新闻内容 | 约 0.001 美元 |
| LLM 服务 | 基于令牌计费 |

每个响应都会包含 `usage.cost` 和 `usage.credits_remaining` 信息。

## 错误处理

错误会以 JSON 格式返回，并包含 `error` 字段：

```json
{
  "error": "Invalid API key",
  "code": 401
}
```

常见错误代码：
- `401` - API 密钥无效或缺失
- `402` - 信用点数不足
- `429` - 超出使用频率限制
- `500` - 服务器错误

## 开始使用的方法

1. 在 [aisa.one](https://aisa.one) 注册账户
2. 获取您的 API 密钥
3. 购买信用点数（按需支付）
4. 设置环境变量：`export AISA_API_KEY="your-key"`

## 完整 API 参考

请参阅 [API 参考文档](https://github.com/AIsa-team/Openclaw-Starter-Kit/blob/main/skills/aisa/references/api-reference.md) 以获取完整的端点说明。