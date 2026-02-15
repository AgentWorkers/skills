---
name: Twitter Command Center (Search + Monitor)
description: "实时搜索 Twitter 上的内容，监控趋势，提取帖子，并分析社交媒体数据——非常适合用于社交监听和情报收集。默认情况下，系统仅提供安全的只读操作功能。"
homepage: https://openclaw.ai
metadata: {"openclaw":{"emoji":"🐦","requires":{"bins":["curl","python3"],"env":["AISA_API_KEY"]},"primaryEnv":"AISA_API_KEY"}}
---

# OpenClaw Twitter 🐦

**用于自主代理的Twitter/X数据访问与自动化工具。由AIsa提供支持。**

只需一个API密钥，即可全面获取Twitter的各类信息。

---

## ⚠️ 重要安全提示

本工具提供两种类型的操作：

### ✅ 读取操作（安全 - 推荐给大多数用户）
- 用户资料、推文、搜索结果、热门话题、关注者
- **无需身份验证**
- **不传输任何凭证**
- **适合生产环境使用**

### ⚠️ 写入操作（高风险 - 仅限专用账户使用）
- 发布推文、点赞、转发推文
- **需要向第三方API传输电子邮件地址、密码和代理设置**
- **安全风险**：会授予`api.aisa.one`对账户的完全访问权限

**⚠️ 重要提示**：切勿使用您的主Twitter账户进行写入操作。请创建专门的自动化账户。

---

## 🔥 您能做什么？（安全的读取操作）

### 监控影响者
```
"Get Elon Musk's latest tweets and notify me of any AI-related posts"
```

### 跟踪热门话题
```
"What's trending on Twitter worldwide right now?"
```

### 社交监听
```
"Search for tweets mentioning our product and analyze sentiment"
```

### 竞争对手分析
```
"Monitor @anthropic and @GoogleAI - alert me on new announcements"
```

### 用户研究
```
"Find AI researchers in the Bay Area and show their recent work"
```

---

## 快速入门

```bash
export AISA_API_KEY="your-key"
```

请在[aisa.one](https://aisa.one)获取您的API密钥。

---

## 核心功能

### ✅ 读取操作（无需登录 - 安全）

所有读取操作都是安全的，仅需您的AIsa API密钥，无需提供Twitter凭证。

#### 获取用户信息
```bash
curl "https://api.aisa.one/apis/v1/twitter/user/info?userName=elonmusk" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

#### 获取用户的最新推文
```bash
curl "https://api.aisa.one/apis/v1/twitter/user/user_last_tweet?userName=elonmusk" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

#### 高级推文搜索
**注意**：必须指定`queryType`参数（如“Latest”或“Top”）
```bash
# Search latest tweets
curl "https://api.aisa.one/apis/v1/twitter/tweet/advanced_search?query=AI+agents&queryType=Latest" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Search top tweets
curl "https://api.aisa.one/apis/v1/twitter/tweet/advanced_search?query=AI+agents&queryType=Top" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

#### 获取热门话题
```bash
# Worldwide trends (woeid=1)
curl "https://api.aisa.one/apis/v1/twitter/trends?woeid=1" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

#### 搜索用户
```bash
curl "https://api.aisa.one/apis/v1/twitter/user/search_user?keyword=AI+researcher" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

#### 根据ID获取推文详情
```bash
curl "https://api.aisa.one/apis/v1/twitter/tweet/tweetById?tweet_ids=123456789" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

#### 获取用户的关注者
```bash
curl "https://api.aisa.one/apis/v1/twitter/user/user_followers?userName=elonmusk" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

#### 获取用户的关注对象
```bash
curl "https://api.aisa.one/apis/v1/twitter/user/user_followings?userName=elonmusk" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

---

## ⚠️ 写入操作（高风险 - 需要身份验证）

**🚨 重要安全警告**：
进行写入操作时，您需要将Twitter的电子邮件地址、密码和代理设置发送给`api.aisa.one`。
- **请务必信任该第三方服务**，因为它将获得对您账户的完全访问权限。
- **严禁在以下情况下使用这些操作：**
  - ❌ 您的主Twitter账户
  - ❌ 包含敏感数据的账户
  - ❌ 经过验证的高价值账户
  - ❌ 无法承受账户丢失风险的账户
- **仅允许在以下情况下使用：**
  - ✅ 专用测试/自动化账户
  - ✅ 未在其他地方使用的唯一密码
  - ✅ 专门为此目的创建的账户
  - ✅ 在仔细阅读AIsa的安全政策后使用

**使用写入操作时，您需自行承担所有风险。**

---

### 写入操作API参考

> ⚠️ **警告**：所有写入操作均需通过登录端点进行身份验证。

#### 第1步：账户登录（异步操作）
```bash
curl -X POST "https://api.aisa.one/apis/v1/twitter/user_login_v3" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "test_automation_account",
    "email": "test@example.com",
    "password": "unique_password_here",
    "proxy": "http://user:pass@proxy-ip:port"
  }'
```

**登录是异步的**——提交请求后请等待登录状态。

#### 第2步：检查登录状态
```bash
curl "https://api.aisa.one/apis/v1/twitter/get_my_x_account_detail_v3?user_name=test_automation_account" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

#### 发布推文
```bash
curl -X POST "https://api.aisa.one/apis/v1/twitter/send_tweet_v3" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "test_automation_account",
    "text": "Hello from OpenClaw!"
  }'
```

#### 点赞推文
```bash
curl -X POST "https://api.aisa.one/apis/v1/twitter/like_tweet_v3" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "test_automation_account",
    "tweet_id": "1234567890"
  }'
```

#### 转发推文
```bash
curl -X POST "https://api.aisa.one/apis/v1/twitter/retweet_v3" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "test_automation_account",
    "tweet_id": "1234567890"
  }'
```

#### 更新个人资料
```bash
curl -X POST "https://api.aisa.one/apis/v1/twitter/update_profile_v3" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "test_automation_account",
    "name": "New Name",
    "bio": "New bio"
  }'
```

---

## Python客户端

### 安全的读取操作
```bash
# User operations (safe)
python3 {baseDir}/scripts/twitter_client.py user-info --username elonmusk
python3 {baseDir}/scripts/twitter_client.py tweets --username elonmusk
python3 {baseDir}/scripts/twitter_client.py followers --username elonmusk
python3 {baseDir}/scripts/twitter_client.py followings --username elonmusk

# Search & Discovery (safe)
python3 {baseDir}/scripts/twitter_client.py search --query "AI agents"
python3 {baseDir}/scripts/twitter_client.py user-search --keyword "AI researcher"
python3 {baseDir}/scripts/twitter_client.py trends --woeid 1
```

### ⚠️ 写入操作（高风险）

**仅限专用测试账户使用：**
```bash
# Login (use test account only!)
python3 {baseDir}/scripts/twitter_client.py login \
  --username test_automation_account \
  --email test@example.com \
  --password unique_password \
  --proxy "http://user:pass@ip:port"

# Check account status
python3 {baseDir}/scripts/twitter_client.py account --username test_automation_account

# Post operations (after login)
python3 {baseDir}/scripts/twitter_client.py post \
  --username test_automation_account \
  --text "Test post"

python3 {baseDir}/scripts/twitter_client.py like \
  --username test_automation_account \
  --tweet-id 1234567890

python3 {baseDir}/scripts/twitter_client.py retweet \
  --username test_automation_account \
  --tweet-id 1234567890
```

---

## API端点参考

### 安全的读取操作

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/twitter/user/info` | GET | 获取用户资料 |
| `/twitter/user/user_last_tweet` | GET | 获取用户的最新推文 |
| `/twitter/user/user_followers` | GET | 获取用户的关注者 |
| `/twitter/user/user_followings` | GET | 获取用户的关注对象 |
| `/twitter/user/search_user` | GET | 根据关键词搜索用户 |
| `/twitter/tweet/advanced_search` | GET | 高级推文搜索 |
| `/twitter/tweet/tweetById` | GET | 根据ID获取推文 |
| `/twitter/trends` | GET | 获取热门话题 |

### 写入操作（高风险）

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/twitter/user_login_v3` | POST | 登录账户 ⚠️ |
| `/twitter/send_tweet_v3` | POST | 发布推文 ⚠️ |
| `/twitter/like_tweet_v3` | POST | 点赞推文 ⚠️ |
| `/twitter/retweet_v3` | POST | 转发推文 ⚠️ |

---

## 价格

| 操作类型 | 每次请求费用 |
|-----------|-----------------|
| 读取操作 | 约0.0004美元 |
| 写入操作 | 约0.001美元 |

每个API响应中都包含`usage.cost`和`usage.credits_remaining`字段。

---

## 开始使用

### 第1步：获取API密钥
在[aisa.one](https://aisa.one)注册并获取您的API密钥。

### 第2步：充值信用
AIsa采用按需付费的计费方式。请为您的账户充值信用。

### 第3步：设置环境变量
```bash
export AISA_API_KEY="your-key-here"
```

### 第4步：从读取操作开始
先从安全的读取操作开始，熟悉API接口。

**只有在有特定需求且拥有专用测试账户的情况下，才能进行写入操作。**

---

## 安全最佳实践

1. **默认设置为仅读取权限**——大多数使用场景不需要写入权限。
2. **使用专用账户**——切勿将自动化操作与个人账户混用。
3. **使用唯一凭证**——为自动化账户设置唯一的密码。
4. **使用环境变量**——切勿在脚本中硬编码凭证。
5. **监控活动**——定期查看AIsa的仪表板。
6. **定期更换API密钥**。
7. **最小化权限**——仅在必要时使用写入操作。
8. **彻底测试**——始终先在测试账户上进行测试。
9. **阅读服务条款**——了解Twitter和AIsa的服务条款。
10. **制定备用计划**——准备好应对账户被暂停的情况。

---

## 文档资料

- [完整API参考](https://aisa.mintlify.app/api-reference/introduction)
- [AIsa安全政策](https://aisa.one)
- [OpenClaw文档](https://openclaw.ai)
- [ClawHub包](https://www.clawhub.com/aisa-one/openclaw-twitter)

---

## 支持服务

- **API问题**：请联系AIsa的支持团队：[aisa.one](https://aisa.one)
- **工具相关问题**：在GitHub上提交问题。
- **安全问题**：请查阅AIsa的安全文档。

---

## 免责声明

本工具通过AIsa的API帮助您访问Twitter数据。写入操作需要向第三方服务传输凭证。用户需自行承担所有风险，包括账户被暂停、数据丢失或安全漏洞等问题。使用本工具时，请自行承担相关风险。