---
name: apify-ultimate-scraper
description: 这是一个通用的、基于人工智能的网页抓取工具，适用于任何平台。它可以从 Instagram、Facebook、TikTok、YouTube、Google Maps、Google Search、Google Trends、Booking.com 和 TripAdvisor 等网站抓取数据。该工具可用于潜在客户开发、品牌监控、竞争对手分析、影响者发现、趋势研究、内容分析、受众分析或任何数据提取任务。
version: 1.0.8
source: https://github.com/apify/agent-skills
homepage: https://apify.com
metadata:
  openclaw:
    requires:
      env:
        - APIFY_TOKEN
      bins:
        - node
        - mcpc
    primaryEnv: APIFY_TOKEN
    install:
      - kind: node
        package: "@apify/mcpc"
        bins: [mcpc]
---

# 通用网络爬虫

该技能能够从55个以上的API中自动提取数据，覆盖所有主要平台。它会根据用户的需求自动选择最合适的API来完成任务。

## 先决条件

- 在OpenClaw设置中配置了`APIFY_TOKEN`
- 安装了Node.js 20.6或更高版本
- 通过技能元数据自动安装了`mcpc` CLI工具

## 输入数据清洗规则

在将任何值插入bash命令之前，请确保：
- **ACTOR_ID**：必须是技术名称（格式为`owner/actor-name`，包含字母、数字、连字符和点）或原始ID（长度为17个字符，例如`oeiQgfg5fsmIJB7Cn`）。不接受包含shell元字符（`; | & $ ` ( ) { } < > ! \n `）的值。
- **SEARCH_KEYWORDS**：仅接受纯文本字符串，不接受shell元字符。
- **JSON_INPUT**：必须是有效的JSON格式，且不能包含单引号（请使用转义的双引号）。使用前请验证其结构。
- **输出文件名**：必须符合`YYYY-MM-DD_descriptive-name.{csv,json}`的格式。文件名中不能包含路径分隔符（`/`、`..`）或特殊字符。

## 工作流程

请复制以下检查清单并记录进度：

```
Task Progress:
- [ ] Step 1: Understand user goal and select Actor
- [ ] Step 2: Fetch Actor schema via mcpc
- [ ] Step 3: Ask user preferences (format, filename)
- [ ] Step 4: Run the scraper script
- [ ] Step 5: Summarize results and offer follow-ups
```

### 第一步：了解用户需求并选择合适的API

首先，明确用户的目标。然后从以下选项中选择最适合的API。

#### Instagram API（12个）

| API ID | 适用场景 |
|---------|---------|
| `apify/instagram-profile-scraper` | 个人资料信息、粉丝数量、简介 |
| `apify/instagram-post-scraper` | 单个帖子详情、互动数据 |
| `apify/instagram-comment-scraper` | 评论提取、情感分析 |
| `apify/instagram-hashtag-scraper` | 标签内容、热门话题 |
| `apify/instagram-hashtag-stats` | 标签性能数据 |
| `apify/instagram-reel-scraper` | Reel视频内容及数据 |
| `apify/instagram-search-scraper` | 用户/地点/标签搜索 |
| `apify/instagram-tagged-scraper` | 被特定账户标记的帖子 |
| `apify/instagram-followers-count-scraper` | 粉丝数量统计 |
| `apify/instagram-scraper` | 全面Instagram数据 |
| `apify/instagram-api-scraper` | 基于API的Instagram访问 |
| `apify/export-instagram-comments-posts` | 批量导出评论/帖子 |

#### Facebook API（14个）

| API ID | 适用场景 |
|---------|---------|
| `apify/facebook-pages-scraper` | 页面数据、指标、联系方式 |
| `apify/facebook-page-contact-information` | 从页面获取电子邮件、电话号码、地址 |
| `apify/facebook-posts-scraper` | 帖子内容及互动数据 |
| `apify/facebook-comments-scraper` | 评论提取 |
| `apify/facebook-likes-scraper` | 互动数据分析 |
| `apify/facebook-reviews-scraper` | 页面评论 |
| `apify/facebook-groups-scraper` | 社群内容及成员信息 |
| `apify/facebook-events-scraper` | 活动数据 |
| `apify/facebook-ads-scraper` | 广告内容及定向信息 |
| `apify/facebook-search-scraper` | 搜索结果 |
| `apify/facebook-reels-scraper` | Reel视频内容 |
| `apify/facebook-photos-scraper` | 照片提取 |
| `apify/facebook-marketplace-scraper` | 商店列表 |
| `apify/facebook-followers-following-scraper` | 粉丝/被关注者列表 |

#### TikTok API（14个）

| API ID | 适用场景 |
|---------|---------|
| `clockworks/tiktok-scraper` | 全面TikTok数据 |
| `clockworks/free-tiktok-scraper` | 免费TikTok数据提取 |
| `clockworks/tiktok-profile-scraper` | 个人资料信息 |
| `clockworks/tiktok-video-scraper` | 视频详情及数据 |
| `clockworks/tiktok-comments-scraper` | 评论提取 |
| `clockworks/tiktok-followers-scraper` | 粉丝列表 |
| `clockworks/tiktok-user-search-scraper` | 根据关键词查找用户 |
| `clockworks/tiktok-hashtag-scraper` | 标签内容 |
| `clockworks/tiktok-sound-scraper` | 热门音效 |
| `clockworks/tiktok-ads-scraper` | 广告内容 |
| `clockworks/tiktok-discover-scraper` | 发现页面内容 |
| `clockworks/tiktok-explore-scraper` | 内容探索 |
| `clockworks/tiktok-trends-scraper` | 热门趋势 |
| `clockworks/tiktok-live-scraper` | 直播数据 |

#### YouTube API（5个）

| API ID | 适用场景 |
|---------|---------|
| `streamers/youtube-scraper` | 视频数据及指标 |
| `streamers/youtube-channel-scraper` | 频道信息 |
| `streamers/youtube-comments-scraper` | 评论提取 |
| `streamers/youtube-shorts-scraper` | Shorts视频内容 |
| `streamers/youtube-video-scraper-by-hashtag` | 按标签筛选视频 |

#### Google Maps API（4个）

| API ID | 适用场景 |
|---------|---------|
| `compass/crawler-google-places` | 商业列表、评分、联系方式 |
| `compass/google-maps-extractor` | 详细商业数据 |
| `compass/Google-Maps-Reviews-Scraper` | 评论提取 |
| `poidata/google-maps-email-extractor` | 从列表中提取电子邮件地址 |

#### 其他API（6个）

| API ID | 适用场景 |
|---------|---------|
| `apify/google-search-scraper` | Google搜索结果 |
| `apify/google-trends-scraper` | Google趋势数据 |
| `voyager/booking-scraper` | Booking.com酒店信息 |
| `voyager/booking-reviews-scraper` | Booking.com评论 |
| `maxcopell/tripadvisor-reviews` | TripAdvisor评论 |
| `vdrmota/contact-info-scraper` | 从URL中提取联系方式 |

---

#### 根据使用场景选择API

| 使用场景 | 推荐API |
|---------|---------------|
| **潜在客户生成** | `compass/crawler-google-places`, `poidata/google-maps-email-extractor`, `vdrmota/contact-info-scraper` |
| **影响者发现** | `apify/instagram-profile-scraper`, `clockworks/tiktok-profile-scraper`, `streamers/youtube-channel-scraper` |
| **品牌监控** | `apify/instagram-tagged-scraper`, `apify/instagram-hashtag-scraper`, `compass/Google-Maps-Reviews-Scraper` |
| **竞争对手分析** | `apify/facebook-pages-scraper`, `apify/facebook-ads-scraper`, `apify/instagram-profile-scraper` |
| **内容分析** | `apify/instagram-post-scraper`, `clockworks/tiktok-scraper`, `streamers/youtube-scraper` |
| **趋势研究** | `apify/google-trends-scraper`, `clockworks/tiktok-trends-scraper`, `apify/instagram-hashtag-stats` |
| **评论分析** | `compass/Google-Maps-Reviews-Scraper`, `voyager/booking-reviews-scraper`, `maxcopell/tripadvisor-reviews` |
| **受众分析** | `apify/instagram-followers-count-scraper`, `clockworks/tiktok-followers-scraper`, `apify/facebook-followers-following-scraper` |

---

#### 多API工作流程

对于复杂任务，可以链接多个API：

| 工作流程 | 第一步 | 第二步 |
|---------|--------|--------|
| **潜在客户信息丰富** | `compass/crawler-google-places` → `vdrmota/contact-info-scraper` |
| **影响者筛选** | `apify/instagram-profile-scraper` → `apify/instagram-comment-scraper` |
| **竞争对手深度分析** | `apify/facebook-pages-scraper` → `apify/facebook-posts-scraper` |
| **本地企业分析** | `compass/crawler-google-places` → `compass/Google-Maps-Reviews-Scraper` |

#### 找不到合适的API？

如果上述API都无法满足用户需求，请直接在Apify商店中搜索：

```bash
mcpc --json mcp.apify.com --header "Authorization: Bearer $APIFY_TOKEN" tools-call search-actors keywords:="SEARCH_KEYWORDS" limit:=10 offset:=0 category:="" | jq -r '.content[0].text'
```

请将`SEARCH_KEYWORDS`替换为1-3个简单关键词（例如：“LinkedIn profiles”、“Amazon products”、“Twitter”）。

### 第二步：获取API的输入格式和详细信息

使用`mcpc`动态获取所选API的输入格式和详细信息：

```bash
mcpc --json mcp.apify.com --header "Authorization: Bearer $APIFY_TOKEN" tools-call fetch-actor-details actor:="ACTOR_ID" | jq -r ".content"
```

请将`ACTOR_ID`替换为实际选择的API（例如`compass/crawler-google-places`）。

此操作将返回：
- API的描述和README文件
- 必需和可选的输入参数
- 可用的输出字段

### 第三步：询问用户偏好

在运行脚本之前，请询问用户以下信息：
1. **输出格式**：
   - **快速响应**：在聊天框中显示前几条结果（不保存文件）
   - **CSV**：包含所有字段的完整导出文件
   - **JSON**：以JSON格式的完整导出文件
2. **结果数量**：根据具体使用场景确定

### 第四步：运行脚本

**快速响应（在聊天框中显示，不保存文件）：**
```bash
node {baseDir}/reference/scripts/run_actor.js \
  --actor 'ACTOR_ID' \
  --input 'JSON_INPUT'
```

**CSV格式导出：**
```bash
node {baseDir}/reference/scripts/run_actor.js \
  --actor 'ACTOR_ID' \
  --input 'JSON_INPUT' \
  --output 'YYYY-MM-DD_OUTPUT_FILE.csv' \
  --format csv
```

**JSON格式导出：**
```bash
node {baseDir}/reference/scripts/run_actor.js \
  --actor 'ACTOR_ID' \
  --input 'JSON_INPUT' \
  --output 'YYYY-MM-DD_OUTPUT_FILE.json' \
  --format json
```

### 第五步：总结结果并提供后续建议

任务完成后，报告以下信息：
- 找到的结果数量
- 文件的位置和名称
- 可用的关键字段
- 根据结果提供的后续建议：

| 用户需求 | 建议的下一步操作 |
|---------|-------------------|
| 获取商业列表 | 使用`vdrmota/contact-info-scraper`丰富数据或获取评论 |
| 分析影响者资料 | 使用评论提取工具分析互动情况 |
| 研究竞争对手页面 | 使用帖子/广告提取工具深入分析 |
| 分析趋势数据 | 使用特定平台的标签提取工具验证数据 |

## 安全性与数据隐私

该技能会指导代理选择合适的API，通过`mcpc`获取其输入格式，并运行相应的爬虫。脚本仅与`api.apify.com`通信，并将输出文件保存在当前工作目录下；不会访问其他系统文件或环境变量。

Apify的API仅抓取公开可用的数据，不会收集目标平台上无法公开获取的私人或个人身份信息。为确保安全，您可以通过查询`https://api.apify.com/v2/acts/:actorId`来查看API的权限级别：`LIMITED_PERMISSIONS`表示在受限环境中运行，而`FULL_PERMISSIONS`表示具有更广泛的系统访问权限。有关详细信息，请参阅[Apify的通用条款和条件](https://docs.apify.com/legal/general-terms-and-conditions)。

## 错误处理

- **`APIFY_TOKEN未找到`**：请用户在OpenClaw设置中配置`APIFY_TOKEN`。
- **`mcpc未找到`**：运行`npm install -g @apify/mcpc`。
- **API未找到`**：请检查API ID的拼写是否正确。
- **运行失败`**：请用户查看错误输出中的Apify控制台链接。
- **超时`**：尝试减小输入数据量或增加`--timeout`参数。