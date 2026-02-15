---
name: search-x
description: 使用 Grok 或 X API 实时搜索 X/Twitter。可以查找推文、趋势以及带有引用信息的讨论内容。
homepage: https://docs.x.ai
user-invocable: true
disable-model-invocation: true
triggers:
  - search x
  - search twitter
  - find tweets
  - what's on x about
  - x search
  - twitter search
metadata:
  clawdbot:
    emoji: "🔍"
    primaryEnv: XAI_API_KEY
    requires:
      bins: [node]
      env: [XAI_API_KEY]
---

# 在X平台上进行搜索

提供了两种实时搜索X/Twitter内容的模式：

1. **xAI Grok**（默认模式）——基于人工智能的搜索方式，使用`x_search`工具，可搜索过去30天内的数据。
2. **X API**（`--x-api`选项）——使用X平台的原生搜索功能，可搜索过去7天内的数据，采用按使用量计费的模式。

## 设置

### 选项1：xAI API（默认模式）
```bash
export XAI_API_KEY="xai-YOUR-KEY"
```
请在以下链接获取您的API密钥：https://console.x.ai

### 选项2：X API（原生模式）
```bash
export X_BEARER_TOKEN="YOUR-BEARER-TOKEN"
```
请在以下链接获取您的API令牌：https://console.x.com

**注意：** X API采用按使用量计费的模式，无需订阅。

## 命令

### 基本搜索（xAI Grok模式）
```bash
node {baseDir}/scripts/search.js "AI video editing"
```

### 使用X API进行搜索
```bash
node {baseDir}/scripts/search.js --x-api "AI video editing"
node {baseDir}/scripts/search.js --x-api --max 50 "trending topic"  # More results
```

### 按时间筛选
```bash
node {baseDir}/scripts/search.js --days 7 "breaking news"
node {baseDir}/scripts/search.js --days 1 "trending today"
node {baseDir}/scripts/search.js --x-api --days 7 "news"  # X API max is 7 days
```

### 按用户账号筛选
```bash
node {baseDir}/scripts/search.js --handles @elonmusk,@OpenAI "AI announcements"
node {baseDir}/scripts/search.js --exclude @bots "real discussions"
```

### 输出选项
```bash
node {baseDir}/scripts/search.js --json "topic"        # Full JSON response
node {baseDir}/scripts/search.js --compact "topic"     # Just tweets, no fluff
node {baseDir}/scripts/search.js --links-only "topic"  # Just X links
```

## 在聊天中的使用示例

**用户：**“在X平台上搜索关于‘Claude Code’的讨论”
**操作：** 使用查询“Claude Code”来执行搜索。

**用户：**“查找@remotion_dev在过去一周内发布的推文”
**操作：** 使用`--handles @remotion_dev --days 7`来执行搜索。

**用户：**“今天Twitter上关于AI的热门话题是什么？”
**操作：** 使用`--days 1 "AI trending"`来执行搜索。

**用户：**“在X平台上搜索‘Remotion’的最佳实践，搜索范围为过去30天”
**操作：** 使用`--days 30 "Remotion best practices"`来执行搜索。

## 工作原理

### xAI Grok模式（默认模式）
- 使用xAI的`/v1/responses`接口以及`x_search`工具进行搜索：
  - 使用的模型为`grok-4-1-fast`（专为高效搜索优化）。
  - 可搜索过去30天内的数据。
  - 搜索结果会包含引文，并以人工智能的方式格式化显示。
  - 返回的推文会包含原始链接。

### X API模式（`--x-api`选项）
- 使用X平台的原生搜索接口`/2/tweets/search/recent`进行搜索：
  - 可搜索过去7天内的数据。
  - 采用按使用量计费的模式（无需订阅）。
  - 返回的推文数据为原始格式，并包含相关指标。
  - 每次查询最多返回100条结果。

## 结果格式

每个搜索结果包含以下信息：
- **@username**（用户名）
- 推文内容
- 发布日期/时间
- 互动指标（仅限X API模式）
- 推文的直接链接

## 环境变量

**xAI模式：**
- `XAI_API_KEY` - 您的xAI API密钥（默认模式必需）
- `SEARCH_X_MODEL` - 可自定义的搜索模型（默认值为`grok-4-1-fast`）
- `SEARCH_X_days` - 搜索的天数（默认值为30天）

**X API模式：**
- `X_BEARER_TOKEN` - 您的X API令牌
- `TWITTER_BEARER_TOKEN` - 可选的替代环境变量名称

## 安全性与权限

**该技能的功能：**
- 调用xAI的`/v1/responses`接口（Grok模式）或X平台的`/2/tweets/search/recent`接口。
- 返回包含链接和引文的公开推文数据。
- 所有请求仅发送到`api.x.ai`或`api.x.com`。

**该技能不执行以下操作：**
- 不会发布、点赞、转发或修改任何X/Twitter上的内容。
- 不会访问您的X/Twitter账户或私信。
- 不会读取配置文件或访问本地文件系统。
- 不会向任何第三方接口发送您的凭证。
- 该技能不能被代理程序自动调用（`disable-model-invocation: true`设置为true时有效）。

首次使用前，请查看`scripts/search.js`文件以确认其功能是否符合预期。