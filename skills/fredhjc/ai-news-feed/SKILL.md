---
name: ai-news-feed
description: 查询 AI 新闻推送 API，以获取来自 57 个精选的 Twitter/X 账号的实时 AI/ML 新闻。当用户询问有关 AI 的新闻、热门的 AI 主题、AI/ML 领域的最新动态，或希望开发基于新闻的功能时，可以使用此 API。该 API 通过 RapidAPI 提供预处理过的双语（英文/中文）摘要、新闻重要性评分以及相关主题标签。
---
# AI新闻推送API

该API可查询来自57个以上Twitter/X账户的、经过预聚合处理并添加了大型语言模型（LLM）分析的AI/机器学习（ML）相关新闻。数据每2小时更新一次。

## API访问与设置

**在发起任何API请求之前**，请确认用户是否已配置RapidAPI密钥。如果没有，请按照以下步骤操作：

1. 在<https://rapidapi.com>（免费）注册/登录。
2. 在<https://rapidapi.com/jiachenfred/api/twitter-ai-news-feed>订阅该API（提供免费 tier，无需信用卡）。
3. 订阅成功后，进入RapidAPI的“Endpoints”页面——“X-RapidAPI-Key”会自动填充到右侧的代码示例中，请将其复制下来。
4. 将密钥保存以供后续使用（例如，将其存储在环境变量`RAPIDAPI_KEY`中）。

**所有请求都必须包含以下请求头：**
```
X-RapidAPI-Key: <user's own key from step 3>
X-RapidAPI-Host: twitter-ai-news-feed.p.rapidapi.com
```

**基础URL**：`https://twitter-ai-news-feed.p.rapidapi.com`

**响应格式**：所有接口返回JSON格式的数据。完整的响应结构请参见[references/api-spec.md]。

## 接口详情

### 获取新闻推送 — `GET /v1/feed`

按发布时间排序的最新文章。

| 参数 | 类型 | 默认值 | 描述 |
|---|---|---|---|
| `lang` | `en` \| `zh` | `en` | 响应语言 |
| `limit` | 1-100 | 20 | 文章数量 |
| `offset` | int | 0 | 分页参数 |
| `tags` | string | — | 用逗号分隔的过滤条件：`paper`、`model_release`、`funding`、`product_launch`、`opinion`、`tutorial`、`benchmark`、`open_source`、`regulation`、`industry` |
| `min_importance` | 1-10 | — | 最小重要性得分 |
| `since` | unix ts | — | 该时间戳之后的文章 |

示例：`GET /v1/feed?lang=zh&limit=5&tags=model_release,paper&min_importance=7`

### 获取热门新闻 — `GET /v1/feed/trending`

按重要性排序的热门文章。

| 参数 | 类型 | 默认值 | 描述 |
|---|---|---|---|
| `lang` | `en` \| `zh` | `en` | 响应语言 |
| `limit` | 1-50 | 10 | 文章数量 |
| `hours` | 1-168 | 时间窗口（168 = 7天） |

示例：`GET /v1/feed/trending?lang=zh&hours=48&limit=10`

### 获取账户信息 — `GET /v1/accounts`

列出所有被监控的账户（共57个以上）。

| 参数 | 类型 | 描述 |
|---|---|---|
| `category` | `official` \| `researcher` \| `media` \| `kol` | 按类别过滤 |

### 获取账户发布的文章 — `GET /v1/accounts/{handle}/posts`

获取特定账户发布的文章（例如：`/v1/accounts/karpathy/posts`）。

| 参数 | 类型 | 默认值 | 描述 |
|---|---|---|---|
| `lang` | `en` \| `zh` | `en` | 响应语言 |
| `limit` | 1-100 | 20 | 文章数量 |
| `offset` | int | 0 | 分页参数 |

### 获取标签信息 — `GET /v1/tags`

显示所有标签及其对应的文章数量。无需其他参数。

### 健康检查 — `GET /health`

返回`{"status": "ok", "timestamp": "..."}`。

## 响应中的关键字段

每条新闻包含以下信息：

- `content` — 原始推文内容
- `summary` — 由大型语言模型生成的一句话摘要（语言取决于`lang`参数）
- `description` — 由大型语言模型生成的2-4句话详细分析（语言取决于`lang`参数）
- `tags` — 文章的主题标签数组
- `importance` | 重要性得分（1-10分，综合了大型语言模型的分析结果和用户互动数据）
- `metrics` | `{likes, retweets, replies, views}` | 文章的互动数据（点赞数、转发数、回复数、浏览量）
- `tweetUrl` | 原始推文的链接
- `tweetedAt` | 推文的发布时间（ISO 8601格式，显示前需转换为用户的本地时区）
- `account` | `{handle, name, category}` | 发布文章的账户信息（包括账号名称和所属类别）

完整的JSON结构请参见[references/api-spec.md]。

## 请求示例

以下是使用curl发起请求的示例（请将`YOUR_KEY`替换为用户的RapidAPI密钥）：
```bash
curl "https://twitter-ai-news-feed.p.rapidapi.com/v1/feed/trending?lang=zh&limit=5" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: twitter-ai-news-feed.p.rapidapi.com"
```

## 常见用法

1. **获取今日的热门AI新闻（中文）**：`GET /v1/feed/trending?lang=zh&hours=24&limit=10`
2. **查找新的模型发布信息**：`GET /v1/feed?tags=model_release&min_importance=5`
3. **跟踪特定研究人员**：`GET /v1/accounts/karpathy/posts?lang=zh`
4. **仅获取融资相关的新闻**：`GET /v1/feed?tags=funding&min_importance=6`
5. **每周新闻汇总**：`GET /v1/feed/trending?hours=168&limit=20&lang=en`

## 被监控的账户类别

- **官方机构**（23个）：OpenAI、Anthropic、Google AI、Meta AI、NVIDIA、Hugging Face、Mistral、xAI、Stability AI、Runway、Perplexity、ElevenLabs、Cursor、Replit等
- **研究人员**（13个）：Karpathy、Yann LeCun、Andrew Ng、Jeff Dean、Ilya Sutskever、Jim Fan、Demis Hassabis、Jeremy Howard等
- **KOL（关键意见领袖）**（12个）：Swyx、Simon Willison、Logan Kilpatrick、Emad Mostaque、Linus Ekenstam等
- **媒体机构**（9个）：MIT Tech Review、WIRED、The Verge、AI Breakfast、Ben's Bites、The Rundown AI等