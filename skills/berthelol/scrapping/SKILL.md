---
name: scrapping
description: 每当用户需要从社交媒体平台获取、检索或查找公开数据时（如个人资料、帖子、视频、评论、关注者、互动数据、文字记录、热门内容、标签或创作者信息），请使用此功能。这些平台包括 TikTok、Instagram、YouTube、Twitter/X、LinkedIn、Facebook、Reddit、Threads、Bluesky、Pinterest、Snapchat、Twitch、Kick、Truth Social，以及 Linktree、Komi、Pillar 等平台。该功能还支持广告库的查询（Meta、Google、LinkedIn、Reddit），以及 TikTok 商店的数据检索。无论用户输入“scrape”、“monitor”、“search”还是“check”等指令，该功能都会被触发。但请注意：该功能仅适用于直接从社交媒体平台获取数据的情况，不适用于开发应用程序、使用官方平台 SDK/API（如 PRAW、tweepy、YouTube Data API）、分析本地文件或创建数据仪表板等场景。
---
# ScrapeCreators API

ScrapeCreators 提供了 100 多个 REST 端点，用于从 20 多个社交媒体平台抓取公开数据。只需一个 API 密钥和一个请求头，即可通过简单的 curl 请求来获取数据。

## 快速入门

### 认证

每个请求都需要一个请求头：

```
x-api-key: YOUR_API_KEY
```

您可以在 [https://scrapecreators.com](https://scrapecreators.com) 获取 API 密钥（注册即可获得 100 个免费信用点，无需信用卡）。将密钥存储在环境变量中，以避免其被包含在脚本中或出现在版本控制历史记录和聊天记录中：

```bash
export SCRAPECREATORS_API_KEY="your-key-here"
```

### 您的第一个请求

```bash
curl -s "https://api.scrapecreators.com/v1/tiktok/profile?handle=khaby.lame" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY" | jq .
```

所有端点的使用方式都相同：使用 `GET` 请求，加上查询参数和认证请求头。

## 基本 URL

```
https://api.scrapecreators.com
```

## 信用点的使用规则

- **大多数端点**：**1 个请求 = 1 个信用点**
- **部分特殊端点** 的费用更高（例如，获取受众人口统计信息需要 26 个信用点）
- 信用点永不过期，无需按月订阅
- 大多数响应中都会包含 `credits_remaining` 字段
- 请在 [文档](https://docs.scrapecreators.com) 中查看每个端点的信用点费用详情

## 常用参数

这些参数在大多数端点中都适用：

| 参数 | 说明 |
|-----------|-------------|
| `trim=true` | 返回精简后的响应内容——当您只需要名称、统计信息和 ID 等关键字段时，该参数可帮助保持响应结构的整洁性 |
| `cursor` | 上一次请求返回的分页游标——将其传递给后续请求以获取下一页内容。每页内容需要 1 个信用点，因此只有在需要更多结果时才进行分页 |
| `includeExtras=true` | 在 YouTube 端点中返回额外的字段（如视频数量、描述等）——如果不启用此参数，仅返回视频的标题和 ID |
| `sort_by` | 对结果进行排序——具体排序方式取决于端点（例如 `popular`、`relevance`、`total_impressions`、`recency`）。请参考相应平台的文档以获取有效的排序参数，否则会收到 400 错误 |

## 分页

许多端点会返回分页结果。操作步骤如下：

1. 首次请求时不传递游标。
2. 响应中会包含 `cursor`（或 `next_cursor`、`next_page_id`）字段。
3. 在后续请求中将该值作为 `?cursor=...` 参数传递。
4. 重复此过程，直到游标值为 `null` 或为空。

```bash
# First page
curl -s "https://api.scrapecreators.com/v1/tiktok/profile/videos?handle=khaby.lame" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY" | jq .

# Next page (using cursor from previous response)
curl -s "https://api.scrapecreators.com/v1/tiktok/profile/videos?handle=khaby.lame&cursor=CURSOR_VALUE" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY" | jq .
```

部分 v2 版本的端点需要手动分页——具体规则请参考相应平台的文档。

## 支持的平台和端点

每个平台都有详细的端点参考文件。请根据您的需求选择相应的文件：

| 平台 | 参考文件 | 主要端点 |
|----------|---------------|---------------|
| TikTok | `references/tiktok.md` | 个人资料、视频、评论、搜索、热门内容、商店、歌曲、字幕、直播、关注者/被关注者、受众人口统计 |
| Instagram | `references/instagram.md` | 个人资料、帖子、Reels（短视频）、评论、Reels 搜索、字幕、故事亮点、嵌入链接 |
| YouTube | `references/youtube.md` | 视频详情、频道信息、频道视频、Shorts（短视频）、搜索、字幕 |
| Twitter/X | `references/twitter.md` | 个人资料、社区动态、社区推文 |
| LinkedIn | `references/linkedin.md` | 个人资料、公司页面、公司帖子、帖子详情、广告库搜索、广告详情 |
| Facebook | `references/facebook.md` | 帖子、评论、Reels（短视频）、广告库、字幕、群组帖子、个人资料 |
| Reddit | `references/reddit.md` | 个人资料、子版块详情/帖子/搜索、帖子评论、搜索、广告库 |
| 其他平台 | `references/other-platforms.md` | Pinterest、Threads、Bluesky、Snapchat、Twitch、Kick、Truth Social、Google（广告+搜索）、链接分享平台（Linktree、Komi、Pillar、Linkbio、Linkme）、Amazon Shop |

## 发送请求的通用格式

所有请求都遵循相同的格式：

```bash
curl -s "https://api.scrapecreators.com/v1/{platform}/{endpoint}?{params}" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY"
```

可以使用 `jq` 对 JSON 数据进行格式化，或者使用 `jq '.some.field'` 来提取特定字段。使用 `jq` 非常重要，因为原始 API 响应通常是结构复杂的 JSON 数据——通过提取所需字段，可以使输出更易于阅读，并保持代码的整洁性。

### 连接多个请求

常见的操作顺序是先获取用户资料（确认账户存在并获取其 ID），然后再获取其具体内容：

```bash
# 1. Get profile
PROFILE=$(curl -s "https://api.scrapecreators.com/v1/tiktok/profile?handle=creator_name" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY")

# 2. Get their recent posts
POSTS=$(curl -s "https://api.scrapecreators.com/v1/tiktok/profile/videos?handle=creator_name" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY")

# 3. Get comments on a specific video (extract video ID from posts)
VIDEO_ID=$(echo "$POSTS" | jq -r '.aweme_list[0].aweme_id')
COMMENTS=$(curl -s "https://api.scrapecreators.com/v1/tiktok/video/comments?video_id=$VIDEO_ID" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY")
```

## 保存结果

```bash
# Save raw JSON
curl -s "https://api.scrapecreators.com/v1/instagram/profile?handle=natgeo" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY" > natgeo_profile.json

# Save as CSV (extract specific fields with jq)
curl -s "https://api.scrapecreators.com/v1/tiktok/profile/videos?handle=creator" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY" \
  | jq -r '.aweme_list[] | [.aweme_id, .desc, .statistics.play_count, .statistics.digg_count] | @csv' \
  > creator_posts.csv
```

## 处理和分析抓取的数据

获取数据后，可以采取以下常见的分析方法：

### 提取关键指标
```bash
# Get engagement stats from a profile
curl -s "https://api.scrapecreators.com/v1/tiktok/profile?handle=creator" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY" \
  | jq '{followers: .statsV2.followerCount, following: .statsV2.followingCount, likes: .statsV2.heartCount}'
```

### 汇总多条帖子的信息
```bash
# Average engagement across recent posts
curl -s "https://api.scrapecreators.com/v1/tiktok/profile/videos?handle=creator" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY" \
  | jq '[.aweme_list[] | .statistics.digg_count] | (add / length)'
```

### 获取视频字幕以进行分析
```bash
# Fetch transcript of a TikTok video
curl -s "https://api.scrapecreators.com/v1/tiktok/video/transcript?video_id=VIDEO_ID" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY" | jq -r '.data.transcript'
```

### 搜索和过滤
```bash
# Find TikTok creators by niche with audience filters
curl -s "https://api.scrapecreators.com/v1/tiktok/creators/popular?min_followers=100000&audience_country=US" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY" | jq '.data'
```

## 重要说明

- **仅抓取公开数据** — 该 API 仅抓取公开可用的信息，不会访问私人账户或私信。
- **无请求限制** — 可根据需要同时发送多个请求。
- **请求超时限制为 29 秒** — 超时请求将被终止（受 AWS Lambda 限制影响）。大多数请求在 3 秒内完成。
- **AI 字幕限制** — 长度超过 2 分钟的视频无法生成 AI 字幕。YouTube 的字幕有专门的获取接口，不受此限制影响。
- **v2 版本端点** — 部分端点（如 Instagram 的搜索 Reels、评论）支持 v2 版本，需要手动分页。自动分页的 v1 版本正在逐步被淘汰。
- **响应格式** — 所有响应均为 JSON 格式。如果只需要关键字段，可以使用 `trim=true` 来减少数据量。

## 错误处理

如果请求失败，请检查以下内容：
1. HTTP 状态码
2. 响应体中通常会包含错误信息
- 常见问题：API 密钥无效（401）、端点未找到（404）、请求超时（502/503）

```bash
# Check status code
curl -s -o response.json -w "%{http_code}" \
  "https://api.scrapecreators.com/v1/tiktok/profile?handle=creator" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY"
```

## 选择合适的端点

根据用户的需求，选择相应的平台和端点：

- **“获取创作者/账户的信息”** → `/{platform}/profile`
- **“获取他们的帖子/视频/内容”** → `/{platform}/profile/videos`（TikTok）或 `/{platform}/channel-videos`（YouTube）或 `/{platform}/user/posts`（Instagram）或 `/{platform}/posts`（Facebook）
- **“获取帖子的评论”** → `/{platform}/video/comments` 或 `/{platform}/post/comments`
- **“搜索关于 X 的内容”** → `/{platform}/search/keyword`（TikTok）或 `/{platform}/search`（其他平台）
- **“获取视频的字幕”** → `/{platform}/video/transcript`（TikTok/YouTube）或 `/v2/instagram/media/transcript`（Instagram）或 `/facebook/transcript`（Facebook）
- **“谁关注他们/他们关注谁”** → `/{platform}/user/followers` 或 `/following`
- **“当前热门内容”** → `/tiktok/videos/popular`、`/tiktok/get-trending-feed`、`/tiktok/hashtags/popular`
- **“查找公司的广告”** → `/facebook/adLibrary/search/ads`、`/linkedin/ads/search`、`/google/company/ads` 或 `/reddit/ads/search`
- **“获取 TikTok 商店的产品详情”** → `/tiktok/product`、`/tiktok/shop/search`

如有疑问，请查阅相应平台的参考文件以获取完整的端点列表。

## 完整的 API 文档

如需查看包含响应格式和示例的完整交互式文档，请访问：[https://docs.scrapecreators.com](https://docs.scrapecreators.com)