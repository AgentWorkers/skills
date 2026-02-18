# Macrocosmos SN13 API - 社交媒体数据技能

通过 Macrocosmos SN13 API，您可以使用关键词、用户名、日期范围和过滤器从 X（Twitter）和 Reddit 获取实时社交媒体数据，并获取相关的数据互动指标。该 API 运行在 Bittensor 平台上。

## 元数据

- **名称**: macrocosmos-social-data
- **版本**: 1.0.1
- **首页**: https://github.com/macrocosm-os/macrocosmos-mcp
- **来源**: https://github.com/macrocosm-os/macrocosmos-mcp
- **Pypi**: https://pypi.org/project/macrocosmos-mcp
- **子网**: Bittensor SN13（数据宇宙）
- **作者**: Macrocosmos AI
- **许可证**: MIT

## 所需的环境变量

| 变量 | 是否必需 | 类型 | 说明 |
|----------|----------|------|-------------|
| `MC_API` | 是 | **密钥** | Macrocosmos API 密钥。所有 API 请求都需要此密钥。您可以在 [https://app.macrocosmos.ai/account?tab=api-keys](https://app.macrocosmos.ai/account?tab=api-keys) 获取免费密钥 |

**设置说明**: `MC_API` 密钥必须设置为环境变量。在 REST 请求中，它作为 Bearer 令牌传递在 `Authorization` 标头中；或者直接提供给 Python SDK 客户端。

---

## API 端点

```
POST https://constellation.api.cloud.macrocosmos.ai/sn13.v1.Sn13Service/OnDemandData
```

### 请求头

```
Content-Type: application/json
Authorization: Bearer <YOUR_MC_API_KEY>
```

---

## 请求格式

```json
{
  "source": "X",
  "usernames": ["@elonmusk"],
  "keywords": ["AI", "bittensor"],
  "start_date": "2026-01-01",
  "end_date": "2026-02-10",
  "limit": 10,
  "keyword_mode": "any"
}
```

### 参数

| 参数 | 类型 | 是否必需 | 说明 |
|-----------|------|----------|-------------|
| `source` | 字符串 | 是 | `"X"` 或 `"REDDIT"`（区分大小写） |
| `usernames` | 数组 | 否 | 最多 5 个用户名。`@` 可选。**仅适用于 X（不适用于 Reddit）** |
| `keywords` | 数组 | 否 | 最多 5 个关键词/标签。对于 Reddit，使用子版块格式 `"r/subreddit"` |
| `start_date` | 字符串 | 否 | `YYYY-MM-DD` 或 ISO 格式。默认为 24 小时前 |
| `end_date` | 字符串 | 否 | `YYYY-MM-DD` 或 ISO 格式。默认为当前时间 |
| `limit` | 整数 | 否 | 结果数量范围：1-1000。默认值为 10 |
| `keyword_mode` | 字符串 | 否 | `"any"`（默认）匹配任意关键词；`all` 需要所有关键词 |

---

## 响应格式

```json
{
  "data": [
    {
      "datetime": "2026-02-10T17:30:58Z",
      "source": "x",
      "text": "Tweet content here",
      "uri": "https://x.com/username/status/123456",
      "user": {
        "username": "example_user",
        "display_name": "Example User",
        "followers_count": 1500,
        "following_count": 300,
        "user_description": "Bio text",
        "user_blue_verified": true,
        "profile_image_url": "https://pbs.twimg.com/..."
      },
      "tweet": {
        "id": "123456",
        "like_count": 42,
        "retweet_count": 10,
        "reply_count": 5,
        "quote_count": 2,
        "view_count": 5000,
        "bookmark_count": 3,
        "hashtags": ["#AI", "#bittensor"],
        "language": "en",
        "is_reply": false,
        "is_quote": false,
        "conversation_id": "123456"
      }
    }
  ]
}
```

---

## curl 示例

### 1. 在 X 上进行关键词搜索

```bash
curl -s -X POST https://constellation.api.cloud.macrocosmos.ai/sn13.v1.Sn13Service/OnDemandData \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "source": "X",
    "keywords": ["bittensor"],
    "start_date": "2026-01-01",
    "limit": 10
  }'
```

### 2. 获取特定用户的推文

```bash
curl -s -X POST https://constellation.api.cloud.macrocosmos.ai/sn13.v1.Sn13Service/OnDemandData \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "source": "X",
    "usernames": ["@MacrocosmosAI"],
    "start_date": "2026-01-01",
    "limit": 10
  }'
```

### 3. 多关键词 AND 搜索

```bash
curl -s -X POST https://constellation.api.cloud.macrocosmos.ai/sn13.v1.Sn13Service/OnDemandData \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "source": "X",
    "keywords": ["chutes", "bittensor"],
    "keyword_mode": "all",
    "start_date": "2026-01-01",
    "limit": 20
  }'
```

### 4. 在 Reddit 上进行搜索

```bash
curl -s -X POST https://constellation.api.cloud.macrocosmos.ai/sn13.v1.Sn13Service/OnDemandData \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "source": "REDDIT",
    "keywords": ["r/MachineLearning", "transformers"],
    "start_date": "2026-02-01",
    "limit": 50
  }'
```

### 5. 使用用户名和关键词进行过滤

```bash
curl -s -X POST https://constellation.api.cloud.macrocosmos.ai/sn13.v1.Sn13Service/OnDemandData \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "source": "X",
    "usernames": ["@opentensor"],
    "keywords": ["subnet"],
    "start_date": "2026-01-01",
    "limit": 20
  }'
```

---

## Python 示例

### 使用 `macrocosmos` SDK

```python
import asyncio
import macrocosmos as mc

async def search_tweets():
    client = mc.AsyncSn13Client(api_key="YOUR_API_KEY")

    response = await client.sn13.OnDemandData(
        source="X",
        keywords=["bittensor"],
        usernames=[],
        start_date="2026-01-01",
        end_date=None,
        limit=10,
        keyword_mode="any",
    )

    if hasattr(response, "model_dump"):
        data = response.model_dump()

    for tweet in data["data"]:
        print(f"@{tweet['user']['username']}: {tweet['text'][:100]}")
        print(f"  Likes: {tweet['tweet']['like_count']} | Views: {tweet['tweet']['view_count']}")

asyncio.run(search_tweets())
```

### 使用 `requests`（REST）

```python
import requests

url = "https://constellation.api.cloud.macrocosmos.ai/sn13.v1.Sn13Service/OnDemandData"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_API_KEY"
}
payload = {
    "source": "X",
    "keywords": ["bittensor"],
    "start_date": "2026-01-01",
    "limit": 10
}

response = requests.post(url, json=payload, headers=headers)
data = response.json()

for tweet in data["data"]:
    print(f"@{tweet['user']['username']}: {tweet['text'][:100]}")
```

---

## 提示与已知问题

### 可靠的操作方式：
- **高频率的关键词搜索**：像 “bittensor”、“AI”、“iran”、“lfg” 这样的热门词汇可以快速获取结果。
- **更宽的日期范围**：将 `start_date` 设置得更早（例如几周/几个月）可以改善搜索效果。
- **`keyword_mode: "all"`**：非常适合查找两个主题的交集（例如 “chutes” AND “bittensor”）。

### 可能出现的问题：
- **仅使用用户名的查询**：可能会超时（DEADLINE_EXCEEDED）。将 `start_date` 设置得更早有助于解决问题。
- **小众/低频关键词**：如果数据索引不足，非常具体的关键词可能会超时。
- **未设置 `start_date`**：默认为过去 24 小时，可能会遗漏数据；请明确设置以获得最佳结果。

### 对大型语言模型（LLM）代理的最佳实践：
1. **始终设置 `start_date`** —— 不要依赖默认的 24 小时范围。对于用户查询，至少使用过去 7 天的数据。
2. **优先使用关键词** —— 关键词搜索更为可靠。
3. **对于用户名查询，务必包含 `start_date`**，并设置几周/几个月前的时间范围。
4. **在结合主题和子主题时使用 `keyword_mode: "all"`**（例如 “bittensor” + “chutes”）。
5. **优雅地处理超时** —— 如果查询超时，尝试使用更宽的日期范围或切换到关键词搜索。
6. **解析互动指标** —— `view_count`、`like_count`、`retweet_count` 有助于判断结果的相关性。
7. **检查 `is_reply` 和 `is_quote`** —— 根据使用场景过滤原始推文和回复。

---

## Gravity API（大规模数据集）

对于结果数量超过 1000 的数据集，请使用 Gravity API：

### 创建任务
```
POST /gravity.v1.GravityService/CreateGravityTask
```
```json
{
  "gravity_tasks": [
    {"platform": "x", "topic": "#bittensor", "keyword": "dTAO"}
  ],
  "name": "Bittensor dTAO Collection"
}
```
**注意**：X 的主题必须以 `#` 或 `$` 开头。Reddit 的主题需要使用子版块格式。

### 检查状态
```
POST /gravity.v1.GravityService/GetGravityTasks
```
```json
{
  "gravity_task_id": "multicrawler-xxxx-xxxx",
  "include_crawlers": true
}
```

### 构建数据集
```
POST /gravity.v1.GravityService/BuildDataset
```
```json
{
  "crawler_id": "crawler-0-multicrawler-xxxx",
  "max_rows": 10000
}
```
**警告**：构建数据集会永久停止爬虫的运行。

### 下载数据集
```
POST /gravity.v1.GravityService/GetDataset
```
```json
{
  "dataset_id": "dataset-xxxx-xxxx"
}
```
完成构建后，会返回 Parquet 文件的下载链接。

---

## 工作流程总结

```
Quick Query (< 1000 results):
  OnDemandData → instant results

Large Collection (7-day crawl):
  CreateGravityTask → GetGravityTasks (monitor) → BuildDataset → GetDataset (download)
```

---

## 错误参考

| 错误 | 原因 | 解决方法 |
|-------|-------|-----|
| `401 Unauthorized` | API 密钥缺失或无效 | 检查 `Authorization: Bearer` 标头 |
| `500 Internal Server Error` | 服务器端问题（通常与 gRPC 认证有关） | 验证 API 密钥并重试 |
| `DEADLINE_EXCEEDED` | 查询超时 —— 数据提供者无法完成请求 | 使用更宽的日期范围或切换到关键词搜索 |
| `data` 数组为空 | 未找到匹配结果 | 扩大搜索范围或日期范围 |