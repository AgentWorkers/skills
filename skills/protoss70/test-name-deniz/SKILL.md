---
name: apify-ultimate-scraper
description: 这是一个通用的、基于人工智能的网页抓取工具，适用于任何平台。它可以从 Instagram、Facebook、TikTok、YouTube、Google Maps、Google Search、Google Trends、Booking.com 和 TripAdvisor 等网站中抓取数据。该工具可用于潜在客户开发、品牌监控、竞争对手分析、影响者发现、趋势研究、内容分析、受众分析或任何数据提取任务。
---

# 通用网页爬虫

该工具能够从55个以上的数据源中自动提取数据，这些数据源覆盖了所有主流平台。它会根据用户的具体需求自动选择最合适的工具（Actor）来完成任务。

## 先决条件
（无需提前检查）

- 包含 `APIFY_TOKEN` 的 `.env` 文件
- Node.js 20.6 或更高版本（以支持 `--env-file` 参数）
- `mcpc` 命令行工具：`npm install -g @apify/mcpc`

## 工作流程

请复制以下清单并记录进度：

```
Task Progress:
- [ ] Step 1: Understand user goal and select Actor
- [ ] Step 2: Fetch Actor schema via mcpc
- [ ] Step 3: Ask user preferences (format, filename)
- [ ] Step 4: Run the scraper script
- [ ] Step 5: Summarize results and offer follow-ups
```

### 第一步：了解用户需求并选择合适的工具

首先，明确用户想要获取的信息。然后从以下选项中选择最适合的工具：

#### Instagram 工具（12个）

| 工具 ID | 适用场景 |
|---------|---------|
| `apify/instagram-profile-scraper` | 个人资料信息、粉丝数量、简介 |
| `apify/instagram-post-scraper` | 单个帖子详情、互动数据 |
| `apify/instagram-comment-scraper` | 评论提取、情感分析 |
| `apify/instagram-hashtag-scraper` | 标签内容、热门话题 |
| `apify/instagram-hashtag-stats` | 标签的互动数据 |
| `apify/instagram-reel-scraper` | Reel（短视频）内容及数据 |
| `apify/instagram-search-scraper` | 搜索用户、地点、标签 |
| `apify/instagram-tagged-scraper` | 被特定账户标记的帖子 |
| `apify/instagram-followers-count-scraper` | 跟随者数量统计 |
| `apify/instagram-scraper` | 全面的 Instagram 数据 |
| `apify/instagram-api-scraper` | 基于 API 的 Instagram 访问 |
| `apify/export-instagram-comments-posts` | 批量导出评论和帖子 |

#### Facebook 工具（14个）

| 工具 ID | 适用场景 |
|---------|---------|
| `apify/facebook-pages-scraper` | 页面数据、指标、联系方式 |
| `apify/facebook-page-contact-information` | 从页面获取电子邮件、电话号码、地址 |
| `apify/facebook-posts-scraper` | 帖子内容及互动数据 |
| `apify/facebook-comments-scraper` | 评论提取 |
| `apify/facebook-likes-scraper` | 点赞数据分析 |
| `apify/facebook-reviews-scraper` | 页面评论 |
| `apify/facebook-groups-scraper` | 群组内容及成员信息 |
| `apify/facebook-events-scraper` | 活动数据 |
| `apify/facebook-ads-scraper` | 广告内容及目标受众分析 |
| `apify/facebook-search-scraper` | 搜索结果 |
| `apify/facebook-reels-scraper` | Reel 内容 |
| `apify/facebook-photos-scraper` | 照片提取 |
| `apify/facebook-marketplace-scraper` | 商店列表 |
| `apify/facebook-followers-following-scraper` | 跟随者/被跟随者列表 |

#### TikTok 工具（14个）

| 工具 ID | 适用场景 |
|---------|---------|
| `clockworks/tiktok-scraper` | 全面的 TikTok 数据 |
| `clockworks/free-tiktok-scraper` | 免费提取 TikTok 数据 |
| `clockworks/tiktok-profile-scraper` | 个人资料信息 |
| `clockworks/tiktok-video-scraper` | 视频详情及数据 |
| `clockworks/tiktok-comments-scraper` | 评论提取 |
| `clockworks/tiktok-followers-scraper` | 跟随者列表 |
| `clockworks/tiktok-user-search-scraper` | 根据关键词查找用户 |
| `clockworks/tiktok-hashtag-scraper` | 标签内容 |
| `clockworks/tiktok-sound-scraper` | 热门音频 |
| `clockworks/tiktok-ads-scraper` | 广告内容 |
| `clockworks/tiktok-discover-scraper` | 发现页面内容 |
| `clockworks/tiktok-explore-scraper` | 探索内容 |
| `clockworks/tiktok-trends-scraper` | 热门趋势 |
| `clockworks/tiktok-live-scraper` | 直播数据 |

#### YouTube 工具（5个）

| 工具 ID | 适用场景 |
|---------|---------|
| `streamers/youtube-scraper` | 视频数据及指标 |
| `streamers/youtube-channel-scraper` | 频道信息 |
| `streamers/youtube-comments-scraper` | 评论提取 |
| `streamers/youtube-shorts-scraper` | Shorts 内容 |
| `streamers/youtube-video-scraper-by-hashtag` | 按标签筛选视频 |

#### Google 地图工具（4个）

| 工具 ID | 适用场景 |
|---------|---------|
| `compass/crawler-google-places` | 商业列表、评分、联系方式 |
| `compass/google-maps-extractor` | 详细商业数据 |
| `compass/Google-Maps-Reviews-Scraper` | 评论提取 |
| `poidata/google-maps-email-extractor` | 从列表中提取电子邮件 |

#### 其他工具（6个）

| 工具 ID | 适用场景 |
|---------|---------|
| `apify/google-search-scraper` | Google 搜索结果 |
| `apify/google-trends-scraper` | Google 流行趋势数据 |
| `voyager/booking-scraper` | Booking.com 酒店信息 |
| `voyager/booking-reviews-scraper` | Booking.com 评论 |
| `maxcopell/tripadvisor-reviews` | TripAdvisor 评论 |
| `vdrmota/contact-info-scraper` | 从 URL 中提取联系方式 |

---

#### 根据使用场景选择工具

| 使用场景 | 主要使用的工具 |
|---------|---------------|
| **潜在客户开发** | `compass/crawler-google-places`, `poidata/google-maps-email-extractor`, `vdrmota/contact-info-scraper` |
| **发现影响者** | `apify/instagram-profile-scraper`, `clockworks/tiktok-profile-scraper`, `streamers/youtube-channel-scraper` |
| **品牌监控** | `apify/instagram-tagged-scraper`, `apify/instagram-hashtag-scraper`, `compass/Google-Maps-Reviews-Scraper` |
| **竞争对手分析** | `apify/facebook-pages-scraper`, `apify/facebook-ads-scraper`, `apify/instagram-profile-scraper` |
| **内容分析** | `apify/instagram-post-scraper`, `clockworks/tiktok-scraper`, `streamers/youtube-scraper` |
| **趋势研究** | `apify/google-trends-scraper`, `clockworks/tiktok-trends-scraper`, `apify/instagram-hashtag-stats` |
| **评论分析** | `compass/Google-Maps-Reviews-Scraper`, `voyager/booking-reviews-scraper`, `maxcopell/tripadvisor-reviews` |
| **受众分析** | `apify/instagram-followers-count-scraper`, `clockworks/tiktok-followers-scraper`, `apify/facebook-followers-following-scraper` |

---

#### 多工具协同工作流程

对于复杂任务，可以串联使用多个工具：

| 工作流程 | 第一步 | 第二步 |
|---------|--------|--------|
| **潜在客户信息补充** | `compass/crawler-google-places` → `vdrmota/contact-info-scraper` |
| **影响者筛选** | `apify/instagram-profile-scraper` → `apify/instagram-comment-scraper` |
| **竞争对手深度分析** | `apify/facebook-pages-scraper` → `apify/facebook-posts-scraper` |
| **本地企业分析** | `compass/crawler-google-places` → `compass/Google-Maps-Reviews-Scraper` |

#### 找不到合适的工具？

如果上述工具都无法满足用户需求，请直接在 Apify 商店中搜索：

```bash
export $(grep APIFY_TOKEN .env | xargs) && mcpc --json mcp.apify.com --header "Authorization: Bearer $APIFY_TOKEN" tools-call search-actors keywords:="SEARCH_KEYWORDS" limit:=10 offset:=0 category:="" | jq -r '.content[0].text'
```

请将 `SEARCH_KEYWORDS` 替换为1-3个简单的关键词（例如：“LinkedIn 个人资料”、“Amazon 产品”、“Twitter”）。

### 第二步：获取工具的输入格式和详细信息

使用 `mcpc` 动态获取所选工具的输入格式和详细信息：

```bash
export $(grep APIFY_TOKEN .env | xargs) && mcpc --json mcp.apify.com --header "Authorization: Bearer $APIFY_TOKEN" tools-call fetch-actor-details actor:="ACTOR_ID" | jq -r ".content"
```

请将 `ACTOR_ID` 替换为实际选择的工具（例如：`compass/crawler-google-places`）。

这将返回：
- 工具的描述和 README 文件
- 必需和可选的输入参数
- 可用的输出字段

### 第三步：询问用户偏好

在运行之前，请询问用户以下信息：
1. **输出格式**：
   - **快速响应**：在聊天中显示前几条结果（不保存文件）
   - **CSV**：包含所有字段的完整导出文件
   - **JSON**：以 JSON 格式导出所有数据
2. **结果数量**：根据具体需求确定

### 第四步：运行脚本

**快速响应（在聊天中显示，不保存文件）：**
```bash
node --env-file=.env ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.js \
  --actor "ACTOR_ID" \
  --input 'JSON_INPUT'
```

**CSV 格式导出：**
```bash
node --env-file=.env ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.js \
  --actor "ACTOR_ID" \
  --input 'JSON_INPUT' \
  --output YYYY-MM-DD_OUTPUT_FILE.csv \
  --format csv
```

**JSON 格式导出：**
```bash
node --env-file=.env ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.js \
  --actor "ACTOR_ID" \
  --input 'JSON_INPUT' \
  --output YYYY-MM-DD_OUTPUT_FILE.json \
  --format json
```

### 第五步：总结结果并提供后续建议

完成后，报告以下信息：
- 找到的结果数量
- 文件的位置和名称
- 可用的关键字段
- 根据结果提供的后续建议：

| 用户需求 | 建议的下一步操作 |
|-------------|--------------|
| 获取商业列表 | 使用 `vdrmota/contact-info-scraper` 或获取评论数据 |
| 分析影响者资料 | 使用评论提取工具分析互动情况 |
| 分析竞争对手页面 | 使用帖子/广告提取工具进行深入分析 |
| 分析趋势数据 | 使用特定平台的标签提取工具进行验证 |

## 错误处理

- `APIFY_TOKEN 未找到`：请用户创建包含 `APIFY_TOKEN=your_token` 的 `.env` 文件
- `mcpc 未找到`：请用户安装 `npm install -g @apify/mcpc`
- 工具未找到`：请检查工具 ID 的拼写是否正确
- 运行失败`：请用户查看错误输出中的 Apify 控制台链接
- 超时`：尝试减少输入数据量或增加 `--timeout` 参数的值