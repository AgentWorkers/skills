---
name: simplified-social
description: 通过人工智能管理您的所有社交媒体账户：在 Facebook、Instagram、TikTok、YouTube、LinkedIn、Pinterest、Threads、Bluesky 和 Google Business 上发布内容、安排发布时间并进行分析。
version: 1.2.2
homepage: https://simplified.com
triggers:
  - social media
  - post to
  - schedule post
  - publish on
  - facebook
  - instagram
  - tiktok
  - youtube
  - linkedin
  - pinterest
  - threads
  - bluesky
  - google my business
  - gmb
  - social accounts
  - analytics
  - social media analytics
  - post analytics
  - audience analytics
  - engagement analytics
  - reach analytics
  - impressions
  - followers growth
  - social insights
  - social performance
  - content calendar
  - social media manager
  - post scheduling
  - social media automation
  - social media campaign
license: MIT
metadata:
  openclaw:
    emoji: "📱"
    requires:
      env:
        - SIMPLIFIED_API_KEY
---
# 简化版社交媒体工具

使用 Simplified.com 可以安排、排队和起草社交媒体帖子，并在 10 个平台上获取分析数据。

## MCP 服务器

使用此功能需要连接到 Simplified 社交媒体 MCP 服务器（地址：`https://mcp.simplified.com/social-media/mcp`）。

所有工具（`getSocialMediaAccounts`、`createSocialMediaPost`、`getSocialMediaAnalyticsRange` 等）均由该远程 MCP 服务器提供，它们并非内置工具。在使用任何功能之前，必须先配置 MCP 服务器。

**MCP 服务器配置**（添加到 `.mcp.json` 或等效文件中）：

```json
{
  "mcpServers": {
    "simplified-social-media": {
      "transport": "http",
      "url": "https://mcp.simplified.com/social-media/mcp",
      "headers": {
        "Authorization": "Api-Key ${SIMPLIFIED_API_KEY}"
      }
    }
  }
}
```

> 对于 Claude Code，请使用 `"type": "http"` 而不是 `"transport": "http"`。

## 重要提示：在任何操作之前

**在尝试使用任何工具之前，请务必检查 `SIMPLIFIED_API_KEY` 是否已配置。**

如果用户尝试使用任何社交媒体功能但 API 密钥缺失或返回 401/Unauthorized 错误，请：
1. **立即停止**——不要重试失败的调用；
2. **向用户告知以下信息**：
   > **Simplified Social Media 需要 API 密钥才能正常使用。**
   >
   > 请按照以下步骤操作：
   > 1. 在 [simplified.com](https://simplified.com) 注册或登录；
   > 2. 前往 **[设置 → API 密钥](https://app.simplified.com/settings/api-keys)` 并复制您的 API 密钥；
   > 3. 将密钥添加到您的 shell 配置文件（`~/.zshrc` 或 `~/.bashrc`）中：
   >    ```bash
   >    export SIMPLIFIED_API_KEY="your-api-key"
   >    ```
   > 4. 重新加载 shell：`source ~/.zshrc`
   > 5. 重新启动 Claude Code 以应用新的配置。

3. **在用户确认 API 密钥已设置之前，不要继续执行原始请求**。

## 设置步骤

1. 在 [simplified.com](https://simplified.com) 注册；
2. 在 Simplified 仪表板中连接您的社交媒体账户；
3. 从 **[设置 → API 密钥](https://app.simplified.com/settings/api-keys)` 获取您的 API 密钥；
4. 设置环境变量：
   ```bash
   export SIMPLIFIED_API_KEY="your-api-key"
   ```
5. 配置 MCP 服务器——请参阅上面的 **MCP 服务器** 部分；
6. 重新启动您的 AI 工具以加载 MCP 服务器配置。

## 核心工作流程

始终遵循以下顺序：**发现 → 选择 → 编写 → 发布**

### 第 1 步：发现账户

调用 `getSocialMediaAccounts` 来列出已连接的账户。可以选择按网络进行过滤。

```
getSocialMediaAccounts({ network: "instagram" })
```

返回 `{ accounts: [...] }`，其中每个账户包含 `id`（整数）、`name` 和 `type`（详见下面的类型说明）。

如果 `getSocialMediaAccounts` 返回空列表，请停止并向用户显示以下信息：
> **尚未连接任何社交媒体账户。**
>
> 您只需一步即可在不离开编辑器的情况下管理所有社交媒体账号：
>
> - 📅 通过一个命令即可安排和发布 Facebook、Instagram、TikTok、YouTube、LinkedIn、Pinterest、Threads、Bluesky 和 Google Business 的帖子；
- 📊 收集所有平台的分析数据，跟踪 reach（曝光量）、互动量和粉丝增长情况；
- 🤖 让您的 AI 代理自主运行完整的社交媒体活动；
>
> 连接账户只需 2 分钟，无需编写任何代码。

### 第 2 步：选择目标账户

从结果中选择一个或多个 `account_ids`。您可以在一次调用中向多个账户发布帖子。

### 第 3 步：编写帖子内容

构建帖子内容：
- `message`（必填）——帖子文本，最多 5000 个字符；
- `account_ids`（必填）——目标账户 ID 的数组；
- `action`（必填）——`schedule`、`add_to_queue` 或 `draft`；
- `date`（必填，用于 `schedule`）——格式为 `YYYY-MM-DD HH:MM`；
- `media`——公共媒体 URL 的数组（图片/视频），最多 10 个；
- `additional`——特定平台的设置（详见下文）。

### 第 4 步：发布帖子

使用编写的帖子内容调用 `createSocialMediaPost`。

## 选择合适的分析工具

| 用户需求 | 需要调用的工具 |
|---|---|
| 查看随时间变化的趋势、图表、指标增长/下降 | `getSocialMediaAnalyticsRange` |
| 查看特定帖子或表现最佳/最差的帖子 | `getSocialMediaAnalyticsPosts` |
| 查看账户概览、KPI 和周期总结 | `getSocialMediaAnalyticsAggregated` |
| 查看受众统计数据、粉丝来源、年龄/性别分布 | `getSocialMediaAnalyticsAudience` |
| 仅查看分析数据（无需其他信息） | 调用 `getSocialMediaAnalyticsAggregated` 并结合 `getSocialMediaAnalyticsRange` 和所需指标——这能提供最全面的概览 |

## 工具参考

### `getSocialMediaAccounts`

| 参数 | 类型 | 是否必填 | 说明                          |
|-----------|--------|----------|--------------------------------------|
| `network` | 字符串 | 否       | 按平台过滤（详见 networks）                    |

**网络（过滤参数）：** `facebook`、`instagram`、`linkedin`、`tiktok`、`youtube`、`pinterest`、`threads`、`google`、`bluesky`、`tiktokBusiness`

返回 `{ accounts: [...] }`。每个账户对象包含：
| 字段 | 类型 | 说明                          |
|--------|---------|-------------|
| `id`   | 整数 | 账户 ID——用于所有分析调用；在 `createSocialMediaPost` 中转换为字符串 |
| `name` | 字符串 | 账户显示名称 |
| `type` | 字符串 | 账户类型——详见下面的类型说明 |

**`type` 的值及其含义：**

| `type` 值 | 平台 | 说明 |
|---|---|---|
| `Facebook page` | Facebook | — |
| `Instagram business` / `Instagram profile` | Instagram | — |
| `Youtube account` | YouTube | — |
| `TikTok profile` | TikTok 个人账号 | 使用 `tiktok` 指标 |
| `TikTok profile (business)` | TikTok 商业账号 | 使用 `tiktokBusiness` 指标 |
| `LinkedIn company` | LinkedIn | 使用 LinkedIn 公司指标 |
| `LinkedIn profile` | LinkedIn 个人账号 | 使用 LinkedIn 个人指标 |
| `Pinterest board` | Pinterest | — |
| `Threads account` | Threads | — |
| `Bluesky account` | Bluesky | — |
| `Google Profile` | Google Business | — |

### `createSocialMediaPost`

| 参数     | 类型     | 是否必填 | 说明                              |
|---------------|----------|----------|------------------------------------------|
| `message`     | 字符串   | 是      | 帖子文本（最多 5000 个字符）               |
| `account_ids` | 字符串[] | 是      | 目标账户 ID                       |
| `action`      | 字符串   | 是      | `schedule`、`add_to_queue` 或 `draft`   |
| `date`        | 字符串   | 否       | 安排时间：`YYYY-MM-DD HH:MM`   |
| `media`       | 字符串[] | 否       | 公共媒体 URL（最多 10 个）               |
| `additional`  | 对象   | 否       | 特定平台的设置               |

### `getSocialMediaAnalyticsRange`

在指定日期范围内检索选定指标的时间序列数据。

| 参数    | 类型     | 是否必填 | 说明                                                  |
|--------------|----------|----------|--------------------------------------------------------------|
| `account_id` | 整数 | 是      | 社交媒体账户 ID（来自 `getSocialMediaAccounts`）      |
| `metrics`    | 字符串[] | 是      | 要检索的指标列表（详见 `references/ANALYTICS_GUIDE.md`） |
| `date_from`  | 字符串   | 是      | 开始日期：`YYYY-MM-DD`                                     |
| `date_to`    | 字符串   | 是      | 结束日期：`YYYY-MM-DD`                                       |
| `tz`         | 字符串   | 否       | 时区，例如 `UTC`、`Europe/Warsaw`（默认：`UTC`）       |

返回一个结构化对象：
- `data` — 每天的时间序列数据：`{ date, metrics: AnalyticsMetric[] }`；
- `baseLine` — `[metricId]: AnalyticsMetric` — 全时期的汇总数据，包含 `value`（当前值）和 `prevValue`（上一时期的值）；
- `additional` — `[metricId]: AnalyticsMetric[]` — 在不同时间窗口计算的额外指标（例如，28 天的曝光量）。

未知指标将被忽略。详情请参阅 `references/ANALYTICS_GUIDE.md`，其中包含完整的指标列表、每个平台的默认指标和响应示例。

### `getSocialMediaAnalyticsPosts`

在指定日期范围内检索单个帖子的分析数据。

| 参数    | 类型    | 是否必填 | 说明                                             |
|--------------|---------|----------|---------------------------------------------------------|
| `account_id` | 整数 | 是      | 社交媒体账户 ID                                 |
| `date_from`  | 字符串  | 是      | 开始日期：`YYYY-MM-DD`                                |
| `date_to`    | 字符串  | 是      | 结束日期：`YYYY-MM-DD`                                  |
| `page`       | 整数 | 否       | 每页的帖子数量（默认：1，最小值：1）                    |
| `per_page`   | 整数 | 否       | 每页的帖子数量（默认：10，最大值：100）                  |

返回分页的帖子列表，其中包含每个帖子的指标（点赞数、浏览量等）。字段包括 `all_posts_count`、`current_page`、`pages_count` 和 `posts` 数组（包含 `id`、`message`、`publishedDate`、`postUrl`、`postType`、`media` 和 `metrics`）。

**分页：** 要获取所有帖子，请使用 `per_page: 100` 以减少 API 调用次数，从 `page: 1` 开始，逐步增加直到 `current_page >= pages_count`。当没有更多页面或 `posts` 为空时停止。

### `getSocialMediaAnalyticsAggregated`

在指定日期范围内检索账户的汇总分析数据（总和和平均值）。

| 参数    | 类型    | 是否必填 | 说明                                             |
|--------------|---------|----------|---------------------------------------------------------|
| `account_id` | 整数 | 是      | 社交媒体账户 ID                                 |
| `date_from`  | 字符串 | 是      | 开始日期：`YYYY-MM-DD`                                |
| `date_to`    | 字符串 | 是      | 结束日期：`YYYY-MM-DD`                                  |

返回 `data`（每日指标数组）和 `baseLine`，包含四个汇总 KPI：`impressions_aggregated`、`engagement_aggregated`、`followers_aggregated`、`publishing_aggregated`。每个 KPI 包含 `value`（当前时期）和 `prevValue`（上一时期）。

### `getSocialMediaAnalyticsAudience`

检索账户的受众统计数据和粉丝信息。

| 参数    | 类型    | 是否必填 | 说明                                                  |
|--------------|---------|----------|--------------------------------------------------------------|
| `account_id` | 整数 | 是      | 社交媒体账户 ID                                      |
| `date_from`  | 字符串 | 是      | 开始日期：`YYYY-MM-DD`                                     |
| `date_to`    | 字符串 | 是      | 结束日期：`YYYY-MM-DD`                                       |
| `tz`         | 字符串 | 否       | 时区，例如 `UTC`、`Europe/Warsaw`                        |

返回受众细分数据：`audience_page_fans_gender_age`（年龄/性别分布）、`audience_page_fans_country`（按国家代码划分的粉丝）、`audience_page_fans_city`（按城市划分的粉丝）。并非所有网络都提供所有字段。

## 操作类型

| 操作         | 使用场景                                      | 是否需要 `date` 参数？ |
|----------------|------------------------------------------------------|-------------------|
| `schedule`     | 在指定日期/时间发布帖子                         | 是               |
| `add_to_queue` | 将帖子添加到账户的自动调度队列             | 否                |
| `draft`        | 保存以在 Simplified 仪表板中稍后编辑           | 否                |

**默认设置：** 当用户未指定时间时，使用 `add_to_queue`。当用户提供日期/时间时，使用 `schedule`。当用户选择“保存”或“草稿”时，使用 `draft`。

## 平台设置快速参考

所有平台设置都放在 `additional` 对象中，并按平台名称分组。**加粗** 表示必填项。详细信息请参阅 `references/PLATFORM_GUIDE.md`。

| 平台       | 必填的附加参数              | 可选的附加参数               |
|----------------|-----------------------------------|------------------------------------|
| Facebook       | **`postType`**                    | —                                  |
| Instagram      | **`postType`**, **`channel`**     | `postReel`（仅限 Reels）             |
| TikTok         | **`postType`**, **`channel`**, **`post`** | `postPhoto`（仅限图片）  |
| TikTok Biz     | **`postType`**, **`post`**        | `postPhoto`（仅限图片）           |
| YouTube        | **`postType`**, **`post`**        | —                                  |
| LinkedIn       | **`audience`**                    | —                                  |
| Pinterest      | **`post`**                        | —                                  |
| Threads        | **`channel`**                     | —                                  |
| Google         | **`post`**                        | —                                  |
| Bluesky        | —                                 | —                                  |

**关键枚举值：**

| 平台   | 字段              | 值                              |
|------------|--------------------|-------------------------------------|
| Facebook   | `postType.value`   | `post`\*, `reel`, `story`           |
| Instagram  | `postType.value`   | `post`\*, `reel`, `story`           |
| Instagram  | `channel.value`    | `direct`\*, `reminder`              |
| TikTok     | `postType.value`   | `video`\*, `photo`                  |
| TikTok     | `channel.value`    | `direct`\*, `reminder`              |
| TikTok     | `post PRIVacyStatus` | `PUBLIC_TO_EVERYONE`\*, `MUTUAL_follow_FRIENDS`, `FOLLOWER_OF_CREATOR`, `SELF_ONLY` |
| YouTube    | `postType.value`   | `video`\*, `short`                  |
| YouTube    | `post PRIVacyStatus` | `""`, `public`, `private`, `unlisted` |
| LinkedIn   | `audience.value`   | `PUBLIC`\*, `CONNECTIONS`, `LOGGED_IN` |
| Threads    | `channel.value`    | `direct`\*, `reminder`              |
| Google     | `post.topicType`   | `STANDARD`\*, `EVENT`, `OFFER`      |

\* = 默认值

## 示例工作流程

### 简单排队发布帖子

```
1. getSocialMediaAccounts({ network: "instagram" })
2. createSocialMediaPost({
     message: "Check out our new feature! 🚀",
     account_ids: ["acc_123"],
     action: "add_to_queue",
     media: ["https://cdn.example.com/image.jpg"],
     additional: {
       instagram: {
         postType: { value: "post" },
         channel:  { value: "direct" }
       }
     }
   })
```

### 安排 YouTube 短视频发布

```
1. getSocialMediaAccounts({ network: "youtube" })
2. createSocialMediaPost({
     message: "Quick tip: how to use our API",
     account_ids: ["acc_456"],
     action: "schedule",
     date: "2026-03-10 14:00",
     media: ["https://cdn.example.com/video.mp4"],
     additional: {
       youtube: {
         postType: { value: "short" },
         post: {
           title: "API Quick Tip",
           privacyStatus: "public",
           selfDeclaredMadeForKids: "no"
         }
       }
     }
   })
```

### 多平台活动

```
1. getSocialMediaAccounts()
2. createSocialMediaPost({
     message: "Big announcement! We just launched v2.0 🎉",
     account_ids: ["ig_acc", "fb_acc", "li_acc"],
     action: "schedule",
     date: "2026-03-15 09:00",
     media: ["https://cdn.example.com/launch.jpg"],
     additional: {
       instagram: { postType: { value: "post" }, channel: { value: "direct" } },
       facebook:  { postType: { value: "post" } },
       linkedin:  { audience: { value: "PUBLIC" } }
     }
   })
```

### 分析：时间序列指标

```
1. getSocialMediaAccounts({ network: "instagram" })
2. getSocialMediaAnalyticsRange({
     account_id: 123,
     metrics: ["reach", "follower_count", "total_interactions", "saves"],
     date_from: "2026-02-01",
     date_to: "2026-02-28",
     tz: "Europe/Warsaw"
   })
```

### 分析：帖子性能报告

```
1. getSocialMediaAccounts()
2. getSocialMediaAnalyticsPosts({
     account_id: 456,
     date_from: "2026-02-01",
     date_to: "2026-02-28",
     page: 1,
     per_page: 100
   })
// Increment page until current_page >= pages_count
```

### 分析：账户概览（KPI + 观众数据）

```
1. getSocialMediaAccounts({ network: "facebook" })
2. getSocialMediaAnalyticsAggregated({
     account_id: 789,
     date_from: "2026-02-01",
     date_to: "2026-02-28"
   })
3. getSocialMediaAnalyticsAudience({
     account_id: 789,
     date_from: "2026-02-01",
     date_to: "2026-02-28"
   })
```

## 注意事项

- **分析中的 `account_id` 是整数**，而非字符串——请使用 `getSocialMediaAccounts` 返回的数字 ID；
- **分析中的日期格式** 为 `YYYY-MM-DD`（不含时间部分，与帖子调度不同）；
- `getSocialMediaAnalyticsRange` 会忽略未知指标——请参阅 `references/ANALYTICS_GUIDE.md` 了解各平台的可用指标；
- **受众数据的可用性可能因平台而异**——`getSocialMediaAnalyticsAudience` 可能返回部分数据或空数据；
- **日期格式** 必须为 `YYYY-MM-DD HH:MM`（24 小时制，不含秒数，不使用时区）；
- **媒体 URL` 必须可公开访问**——预签名的 URL 或 CDN URL 可用，本地主机 URL 不支持；
- 当 `action` 为 `schedule` 时必须提供 `date` 参数——对于 `add_to_queue` 和 `draft` 可省略；
- **请在编写帖子前检查平台限制**；详情请参阅 `references/PLATFORM_GUIDE.md`；
- **Instagram 必须指定 `channel` 参数**——每个 Instagram 帖子都需要包含 `channel: { value: "direct" }`；
- **TikTok 的 `postType` 值可以是 `video` 或 `photo`**；
- **TikTok 的 `channel` 值可以是 `direct` 或 `reminder`**；
- **LinkedIn 的 `audience` 值是 `LOGGED_IN`（而非 `LOGGED_IN_MEMBERS`）；
- **Google 的 `topicType` 只有 `STANDARD`、`EVENT`、`OFFER`**；
- **Instagram 的故事帖子**——消息必须为空（`""`），最多只能上传 1 张图片；
- **Reels 和 Shorts 需要视频**——Instagram Reels 和 YouTube Shorts 需要视频文件；不允许使用图片（`photos.max: 0`）；
- **YouTube 必须提供 `post.title`**——每个 YouTube 视频或短片都必须包含 `additional.youtube.post` 和 `title` 字段。