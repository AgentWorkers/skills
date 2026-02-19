---
name: virlo
description: Virlo 社交媒体智能工具：提供病毒式视频分析、话题标签排名、趋势汇总功能，并支持在 YouTube、TikTok 和 Instagram 上进行社交监听。适用于内容策略制定、趋势发现、竞争分析以及细分市场监测。
license: MIT
metadata:
  {
    "openclaw":
      {
        "emoji": "☄️",
        "requires": { "bins": ["curl"], "env": ["VIRLO_API_KEY"] },
        "primaryEnv": "VIRLO_API_KEY",
        "homepage": "https://dev.virlo.ai",
        "source": "https://github.com/CalciferFriend/virlo-skill",
      },
  }
---
# Virlo

Virlo 是一款专注于分析短视频内容的社交媒体情报工具，类似于 Bloomberg 在病毒式内容（即短时间内迅速传播的内容）方面的服务。

**官网**: https://dev.virlo.ai  
**源代码**: https://github.com/CalciferFriend/virlo-skill  
**完整 API 文档**: https://dev.virlo.ai/docs  
**测试平台**: https://dev.virlo.ai/docs/playground  

## 配置  

设置 `VIRLO_API_KEY` 环境变量。你的 API 密钥格式为 `virlo_tkn_<your_key>`，可以从 [Virlo 仪表板](https://dev.virlo.ai/dashboard) 获取。  

## 功能概述  

Virlo API 提供跨平台的数据分析服务，支持 YouTube、TikTok 和 Instagram：  
- **标签**：超过 50 万个标签，按使用频率和总观看次数排序；  
- **趋势**：每日更新的流行话题（UTC 时间 1 点更新）；  
- **视频**：超过 200 万个病毒式视频的详细数据（观看次数、点赞数、分享次数、评论数）；  
- **Orbit**：基于关键词的社交内容监控服务，支持异步分析；  
- **Comet**：自动化的内容监测工具，可定期抓取相关数据。  

## API 访问  

所有 API 端点都使用基础 URL `https://api.virlo.ai/v1`，采用 `snake_case` 命名规则，并以 `{ "data": ... }` 的格式返回数据。  

### 发送请求  

使用 `curl` 命令，并传入 `VIRLO_API_KEY` 环境变量：  
```bash
# GET request
curl -s -X GET "https://api.virlo.ai<endpoint>" \
  -H "Authorization: Bearer ${VIRLO_API_KEY}" \
  -H "Content-Type: application/json"

# POST request with JSON body
curl -s -X POST "https://api.virlo.ai<endpoint>" \
  -H "Authorization: Bearer ${VIRLO_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '<json-body>'
```  

### 示例  

```bash
# List top hashtags
curl -s -X GET "https://api.virlo.ai/v1/hashtags" \
  -H "Authorization: Bearer ${VIRLO_API_KEY}" \
  -H "Content-Type: application/json"

# Top 10 viral videos
curl -s -X GET "https://api.virlo.ai/v1/videos?limit=10" \
  -H "Authorization: Bearer ${VIRLO_API_KEY}" \
  -H "Content-Type: application/json"

# Daily trend digest
curl -s -X GET "https://api.virlo.ai/v1/trends" \
  -H "Authorization: Bearer ${VIRLO_API_KEY}" \
  -H "Content-Type: application/json"

# Create an Orbit search
curl -s -X POST "https://api.virlo.ai/v1/orbit" \
  -H "Authorization: Bearer ${VIRLO_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"name":"AI research","keywords":["artificial intelligence","AI tools"]}'
```  

---

## API 参考  

### 身份验证  

所有请求都需要携带 Bearer 令牌。  

**注意**：切勿将 API 密钥提交到版本控制系统中。如果密钥被泄露，应立即从仪表板重新生成。  

### 响应格式  

所有响应都采用 `{ "data": ... }` 的格式。部分 API 端点还包含分页元数据：  
```json
{
  "data": {
    "total": 500,
    "limit": 50,
    "offset": 0,
    "items": [ ... ]
  }
}
```  

### 分页  

分页功能通过 `limit` 和 `page` 参数实现：  
| 参数 | 类型 | 默认值 | 描述                          |  
|------|------|-----------|-----------------------------|  
| `limit` | 整数 | 每页显示的条目数（1-100）                |  
| `page` | 整数 | 当前页码（从 1 开始计数）                |  

通过分页最多可获取 1000 条结果。  

### 常用查询参数  

许多与视频相关的 API 端点支持以下过滤条件：  
| 参数    | 类型    | 描述                                      |  
|---------|-------|-------------------------------------------------|  
| `min_views` | 整数 | 最小观看次数阈值                    |  
| `platforms` | 字符串 | 以逗号分隔的平台：`youtube`, `tiktok`, `instagram` |  
| `start_date` | 字符串 | ISO 8601 格式的日期过滤条件（最早发布日期）       |  
| `end_date` | 字符串 | ISO 8601 格式的日期过滤条件（最新发布日期）       |  
| `order_by` | 字符串 | 排序字段（因端点而异）                    |  
| `sort`   | 字符串 | 排序方向：`asc` 或 `desc`（默认：`desc`）           |  

### 支持的平台  

- `youtube`：YouTube Shorts 和普通视频  
- `tiktok`：TikTok 视频  
- `instagram`：Instagram Reels 视频  

---

### 标签  

Virlo 跟踪超过 50 万个标签，并按使用频率和总观看次数进行排序：  
#### 列出标签  

**请求方式**:  
```
GET /v1/hashtags
```  
**响应格式**:  
```json
{
  "data": [
    {
      "hashtag": "#shorts",
      "count": 10926,
      "total_views": 869912593
    }
  ]
}
```  
| 字段     | 类型    | 描述                                   |  
|---------|--------|---------------------------------------------|  
| `hashtag`   | 字符串   | 标签文本（可能包含 `#` 或不包含）             |  
| `count`    | 整数    | 使用该标签的视频数量                   |  
| `total_views` | 整数    | 所有包含该标签的视频的总观看次数             |  

---

### 趋势  

每日更新的流行话题（UTC 时间 1 点更新）：  
#### 列出趋势组  

**请求方式**:  
```
GET /v1/trends
```  
**响应格式**:  
```json
{
  "data": [
    {
      "id": "b88c0c23-8501-4975-a1e9-b7c1160c6342",
      "title": "Trends for Oct 15th",
      "trends": [
        {
          "id": "132ea402-804d-4515-b706-f3ff9c698c5e",
          "trend_id": "8ab75d1a-cb50-4885-b9b3-2e4ede2a3620",
          "trend_group_id": "b88c0c23-8501-4975-a1e9-b7c1160c6342",
          "ranking": 1,
          "trend": {
            "id": "8ab75d1a-cb50-4885-b9b3-2e4ede2a3620",
            "name": "NBA Season Opening Night",
            "description": "The 2025-26 NBA season officially tipped off...",
            "trend_type": "content"
          }
        }
      ]
    }
  ]
}
```  
| 字段    | 类型   | 描述                                      |  
|---------|--------|-----------------------------------------|  
| `id`     | 字符串   | 趋势组的唯一标识符                         |  
| `title`    | 字符串   | 显示标题（例如：“10 月 15 日的热门趋势”）             |  
| `trends` | 数组    | 排序后的趋势条目列表                   |  

趋势条目包含以下字段：`id`, `trend_id`, `trend_group_id`, `ranking`, `trend`（包含 `id`, `name`, `description`, `trend_type`）。  

---

### 视频  

涵盖 YouTube、TikTok 和 Instagram 上的病毒式视频：  
#### 列出热门视频（跨平台）  

**请求方式**:  
```
GET /v1/videos
```  
| 参数    | 类型    | 描述                                      |  
|---------|--------|-------------------------------------------------|  
| `limit`    | 整数    | 每页显示的条目数（1-100，默认 50）                |  
| `page`     | 整数    | 当前页码（从 1 开始计数）                |  
| `min_views` | 整数    | 最小观看次数阈值                    |  
| `platforms` | 字符串   | 以逗号分隔的平台：`youtube`, `tiktok`, `instagram`     |  
| `start_date` | 字符串   | ISO 8601 格式的最早发布日期                |  
| `end_date` | 字符串   | ISO 8601 格式的最新发布日期                |  
| `order_by` | 字符串   | 排序方式（`publish_date`, `views`, `created_at`）       |  
| `sort`    | 字符串   | 排序方向（`asc` 或 `desc`，默认：`desc`）           |  

#### 平台特定的 API 端点  

这些端点的参数和响应格式与 `/v1/videos` 相同，但仅针对特定平台：  
```
GET /v1/youtube-videos
GET /v1/tiktok-videos
GET /v1/instagram-videos
```  

#### 视频对象字段  

| 字段         | 类型       | 描述                                      |  
|-------------|------------|-----------------------------------------|  
| `id`        | 字符串     | Virlo 生成的唯一标识符                   |  
| `url`        | 字符串     | 视频的原始 URL                          |  
| `publish_date`   | 字符串     | 视频的发布时间戳（ISO 8601 格式）             |  
| `views`      | 整数       | 观看次数                          |  
| `number_of_likes` | 整数       | 点赞数                          |  
| `number_of_comments` | 整数       | 评论数                          |  
| `description`    | 字符串     | 视频描述                          |  
| `thumbnail_url`   | 字符串     | 缩略图 URL                         |  
| `hashtags`     | 字符串数组   | 提取的标签                        |  
| `type`       | 字符串     | 视频平台（`youtube`, `tiktok`, `instagram`）       |  
| `niche`      | 字符串     | 内容类型                          |  
| `author_id`    | 字符串     | 视频作者的唯一标识符                   |  
| `bookmarks`     | 整数       | 收藏/保存次数                        |  
| `external_id`    | 字符串     | 平台特定的视频 ID                     |  
| `region`     | 字符串/空    | 地理区域代码                        |  
| `duration`    | 整数       | 视频时长（秒）                        |  
| `transcript_raw` | 字符串/空    | 视频原始字幕（如有提供）                   |  

---

### Orbit — 社交内容监控  

Orbit 提供基于关键词的视频发现服务，支持异步分析、元数据广告收集和创作者异常检测：  
#### 创建搜索任务  

**请求方式**:  
```
POST /v1/orbit
```  
| 参数          | 类型       | 是否必填 | 描述                                      |  
|----------------|---------|----------------------------------|  
| `name`        | 字符串     | 搜索任务的描述性名称                        |  
| `keywords`     | 字符串数组   | 要搜索的关键词（1-10 个）                   |  
| `platforms`     | 字符串数组   | 是否必填 | 支持的平台（默认：全部）                   |  
| `min_views`     | 整数       | 最小观看次数阈值                    |  
| `time_period`    | 字符串     | 时间范围（`today`, `this_week`, `this_month`, `this_year`） |  
| `run_analysis`    | 布尔值     | 是否启用 AI 分析（默认：false）                |  
| `enable_meta_ads`    | 布尔值     | 是否启用元数据广告收集（默认：false）                |  
| `exclude_keywords`    | 字符串数组   | 需排除的关键词                        |  
| `exclude_keywords_strict` | 布尔值     | 是否同时检查字幕中的关键词（默认：false）           |  

#### 列出搜索任务  

**请求方式**:  
```
GET /v1/orbit
```  
支持标准的分页功能（`limit`/`page`）。  

#### 获取搜索结果  

**请求方式**:  
```
GET /v1/orbit/:orbit_id
```  
等待任务完成。如果 `run_analysis` 为 `true`，则返回包含 AI 分析结果的报告。  

查询参数：`order_by`（`views`, `likes`, `shares`, `comments`, `bookmarks`, `publish_date`, `author_followers`），`sort`（`asc`/`desc`）。  

#### 获取特定平台的视频结果  

**请求方式**:  
```
GET /v1/orbit/:orbit_id/videos
```  
支持分页，并可指定 `min_views`, `platforms`, `start_date`, `end_date`, `order_by`, `sort`。  

#### 获取元数据广告  

**请求方式**:  
```
GET /v1/orbit/:orbit_id/ads
```  
需要 `enable_meta_ads` 为 `true`。支持分页，并可指定 `order_by`（`created_at`, `page_like_count`）。  

#### 获取创作者异常数据  

**请求方式**:  
```
GET /v1/orbit/:orbit_id/creators/outliers
```  
显示表现超出粉丝数量的创作者。`outlier_ratio` 高表示内容传播范围远超粉丝基数。支持分页。  

---

### Comet — 自动化内容监测  

Comet 可自动发现特定类型的视频、广告和创作者：  
#### 创建内容监测配置  

**请求方式**:  
```
POST /v1/comet
```  
| 参数          | 类型       | 是否必填 | 描述                                      |  
|----------------|---------|----------------------------------|  
| `name`        | 字符串     | 监测任务的描述性名称                        |  
| `keywords`     | 字符串数组   | 要搜索的关键词（1-20 个）                   |  
| `platforms`     | 字符串数组   | 支持的平台（默认：全部）                   |  
| `cadence`      | 字符串     | 监测频率（`daily`, `weekly`, `monthly`, 或 cron 表达式）     |  
| `min_views`     | 整数       | 最小观看次数阈值                    |  
| `time_range`    | 字符串     | 时间范围（`today`, `this_week`, `this_month`, `this_year`）   |  
| `is_active`     | 布尔值     | 是否启用监控（默认：true）                   |  
| `meta_ads_enabled` | 布尔值     | 是否启用元数据广告收集（默认：false）                |  
| `exclude_keywords`     | 字符串数组   | 需排除的关键词                        |  
| `exclude_keywords_strict` | 布尔值     | 是否同时检查字幕中的关键词（默认：false）           |  

#### 列出内容监测配置  

**请求方式**:  
```
GET /v1/comet
```  
可添加 `?include_inactive=true` 以包含已停用的配置。  

#### 获取/更新/删除内容监测配置  

**请求方式**:  
```
GET /v1/comet/:id
PUT /v1/comet/:id       # Full replacement — all required fields must be provided
DELETE /v1/comet/:id     # Soft-delete, returns 204
```  

#### 获取内容监测结果  

**请求方式**:  
```
GET /v1/comet/:id/videos
```  
支持分页，并可指定 `min_views`, `platforms`, `start_date`, `end_date`, `order_by`, `sort`。  

#### 获取元数据广告结果  

**请求方式**:  
```
GET /v1/comet/:id/ads
```  
需要 `enable_meta_ads` 为 `true`。支持分页，并可指定 `order_by`（`created_at`, `page_like_count`）。  

#### 获取创作者异常数据  

**请求方式**:  
```
GET /v1/comet/:id/creators/outliers
```  
支持分页。  

---

### 错误处理  

| 状态码 | 描述                                      |  
|--------|-----------------------------------------|  
| 200     | 请求成功                        |  
| 201     | 资源已创建                        |  
| 202     | 异步任务已排队                    |  
| 204     | 未找到相关内容                    |  
| 400     | 请求参数无效                    |  
| 401     | 未经授权                      |  
| 403     | 权限不足                        |  
| 404     | 资源未找到                      |  
| 422     | 数据格式不正确                    |  
| 429     | 请求次数过多                      |  
| 500     | 服务器内部错误                    |  

**错误响应格式**:  
```json
{
  "error": {
    "type": "validation_error",
    "message": "keywords is required",
    "param": "keywords"
  }
}
```  

### 速率限制  

- 每次请求最多返回 100 条数据；  
- 每次查询最多返回 1,000 条结果；  
- 如果遇到错误代码 429，请等待 `retry_after` 时间后重试。