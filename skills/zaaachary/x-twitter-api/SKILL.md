---
name: x-twitter
description: X（Twitter）API客户端，用于搜索推文、获取文章内容以及检索热门话题。支持Bearer Token（仅限应用程序使用）和OAuth 2.0两种认证方式。
homepage: https://developer.x.com
metadata: { "openclaw": { "emoji": "𝕏", "requires": { "bins": ["python3"] }, "env": ["X_BEARER_TOKEN"], "primaryEnv": "X_BEARER_TOKEN" } }
---

# X（Twitter）API

用于搜索推文、获取文章内容以及从X（Twitter）获取热门话题。

## 功能

- **搜索推文**：使用高级查询操作符搜索最近7天内的推文。
- **获取文章内容**：通过URL或ID检索推文和文章的详细信息。
- **热门话题**：获取热门话题（需要Basic级别或更高级别的账户）。
- **用户信息**：获取用户资料和推文历史记录。

## 设置

```bash
# Set environment variable
export X_BEARER_TOKEN="your_bearer_token_here"

# Or temporarily for this session
X_BEARER_TOKEN="your_token" python3 scripts/search_tweets.py
```

**获取API令牌：**
1. 访问 https://developer.x.com
2. 创建一个项目和应用程序。
3. 在“Keys and Tokens”选项卡中生成Bearer令牌。
4. 设置环境变量。

## 使用方法

### 搜索推文
```bash
# Basic search
python3 scripts/search_tweets.py --query "AI OR 人工智能"

# Advanced search (Chinese original tweets only)
python3 scripts/search_tweets.py --query "AI -is:retweet lang:zh" --count 10

# Search by user
python3 scripts/search_tweets.py --query "from:elonmusk" --count 5

# Search hashtags
python3 scripts/search_tweets.py --query "#Crypto OR #Blockchain"
```

**查询操作符：**
- `-is:retweet`：仅显示原创推文。
- `lang:zh`：中文语言的推文。
- `from:username`：特定用户的推文。
- `has:links`：包含链接的推文。
- `is:verified`：仅显示已认证用户的推文。

### 获取文章/推文内容
```bash
# By URL (article or tweet)
python3 scripts/get_article.py --url "https://x.com/username/article/123456789"

# By Tweet ID
python3 scripts/get_article.py --id "123456789"
```

### 获取热门话题
```bash
# Global trends
python3 scripts/get_trends.py

# Trends by WOEID (Yahoo Where On Earth ID)
python3 scripts/get_trends.py --woeid 1  # Global
python3 scripts/get_trends.py --woeid 23424977  # USA
```

## API限制

| 级别 | 费用 | 每月推文数量 | 备注 |
|------|------|--------------|-------|
| 免费 | $0 | 500 | 每天1次请求，仅限测试使用 |
| Basic | $200 | 500,000 | 最低生产级别 |
| Pro | $5,000 | 2,000,000+ | 支持实时流式数据 |

**免费级别限制：**
- 每月500条推文（约每天16-17条）。
- 每个端点每天1次请求。
- 不支持发布或点赞功能。
- 仅适用于开发测试。

## 输出格式

- **JSON**：包含所有字段的结构化数据。
- **Pretty**：人类可读的格式化文本。
- **Save**：可选的文件导出格式（JSON/Markdown）。

## 错误处理

脚本自动处理以下错误：
- 速率限制（429错误）
- 无效令牌（401错误）
- 网络错误（包含重试逻辑）
- 缺少必要参数

## 示例

### 示例1：搜索与AI相关的推文
```bash
python3 scripts/search_tweets.py --query "AI OR 人工智能 -is:retweet" --count 5 --output pretty
```

### 示例2：监控特定用户
```bash
python3 scripts/search_tweets.py --query "from:username" --count 10 --save output.json
```

### 示例3：获取文章并进行分析
```bash
python3 scripts/get_article.py --url "https://x.com/user/article/id" --output markdown --save article.md
```