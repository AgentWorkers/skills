---
name: trakt
description: 与 Trakt API 进行交互，以管理您的观看列表、收藏夹、评分，并发现新的内容。
metadata: {"openclaw": {"requires": {"env": ["TRAKT_CLIENT_ID", "TRAKT_CLIENT_SECRET", "TRAKT_ACCESS_TOKEN"]}, "primaryEnv": "TRAKT_ACCESS_TOKEN", "homepage": "https://trakt.tv"}}
---

# Trakt API集成

通过Trakt.tv来管理您的观看列表、追踪观看历史记录、维护您的收藏夹、对内容进行评分，以及发现新的电影和剧集。

## 认证

在使用此功能之前，您需要设置Trakt API的认证信息：

1. 在https://trakt.tv/oauth/applications创建一个Trakt应用程序。
2. 获取您的客户端ID（Client ID）和客户端密钥（Client Secret）。
3. 完成OAuth认证流程以获取访问令牌（access token）。
4. 在`~/.openclaw/openclaw.json`文件中设置环境变量：

```json
{
  "skills": {
    "entries": {
      "trakt": {
        "enabled": true,
        "env": {
          "TRAKT_CLIENT_ID": "your_client_id",
          "TRAKT_CLIENT_SECRET": "your_client_secret",
          "TRAKT_ACCESS_TOKEN": "your_access_token",
          "TRAKT_REFRESH_TOKEN": "your_refresh_token"
        }
      }
    }
  }
}
```

## 可用的命令

### 观看列表管理

**添加到观看列表：**
```bash
curl -X POST https://api.trakt.tv/sync/watchlist \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TRAKT_ACCESS_TOKEN" \
  -H "trakt-api-version: 2" \
  -H "trakt-api-key: $TRAKT_CLIENT_ID" \
  -d '{"movies":[{"title":"Inception","year":2010}]}'
```

**获取观看列表：**
```bash
curl https://api.trakt.tv/sync/watchlist/movies \
  -H "Authorization: Bearer $TRAKT_ACCESS_TOKEN" \
  -H "trakt-api-version: 2" \
  -H "trakt-api-key: $TRAKT_CLIENT_ID"
```

**从观看列表中删除：**
```bash
curl -X POST https://api.trakt.tv/sync/watchlist/remove \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TRAKT_ACCESS_TOKEN" \
  -H "trakt-api-version: 2" \
  -H "trakt-api-key: $TRAKT_CLIENT_ID" \
  -d '{"movies":[{"ids":{"trakt":12601}}]}'
```

### 搜索

**搜索电影：**
```bash
curl "https://api.trakt.tv/search/movie?query=inception" \
  -H "trakt-api-version: 2" \
  -H "trakt-api-key: $TRAKT_CLIENT_ID"
```

**搜索剧集：**
```bash
curl "https://api.trakt.tv/search/show?query=breaking+bad" \
  -H "trakt-api-version: 2" \
  -H "trakt-api-key: $TRAKT_CLIENT_ID"
```

### 历史记录

**获取观看历史记录：**
```bash
curl https://api.trakt.tv/sync/history \
  -H "Authorization: Bearer $TRAKT_ACCESS_TOKEN" \
  -H "trakt-api-version: 2" \
  -H "trakt-api-key: $TRAKT_CLIENT_ID"
```

**将内容添加到历史记录中（标记为已观看）：**
```bash
curl -X POST https://api.trakt.tv/sync/history \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TRAKT_ACCESS_TOKEN" \
  -H "trakt-api-version: 2" \
  -H "trakt-api-key: $TRAKT_CLIENT_ID" \
  -d '{"movies":[{"title":"The Matrix","year":1999,"watched_at":"2024-01-15T20:00:00.000Z"}]}'
```

### 收藏夹

**获取收藏夹：**
```bash
curl https://api.trakt.tv/sync/collection/movies \
  -H "Authorization: Bearer $TRAKT_ACCESS_TOKEN" \
  -H "trakt-api-version: 2" \
  -H "trakt-api-key: $TRAKT_CLIENT_ID"
```

**添加到收藏夹：**
```bash
curl -X POST https://api.trakt.tv/sync/collection \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TRAKT_ACCESS_TOKEN" \
  -H "trakt-api-version: 2" \
  -H "trakt-api-key: $TRAKT_CLIENT_ID" \
  -d '{"movies":[{"title":"Blade Runner 2049","year":2017,"collected_at":"2024-01-15T20:00:00.000Z","media_type":"bluray","resolution":"uhd_4k"}]}'
```

### 评分

**获取评分：**
```bash
curl https://api.trakt.tv/sync/ratings/movies \
  -H "Authorization: Bearer $TRAKT_ACCESS_TOKEN" \
  -H "trakt-api-version: 2" \
  -H "trakt-api-key: $TRAKT_CLIENT_ID"
```

**添加评分：**
```bash
curl -X POST https://api.trakt.tv/sync/ratings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TRAKT_ACCESS_TOKEN" \
  -H "trakt-api-version: 2" \
  -H "trakt-api-key: $TRAKT_CLIENT_ID" \
  -d '{"movies":[{"title":"The Shawshank Redemption","year":1994,"rating":10}]}'
```

### 推荐

**获取推荐内容：**
```bash
curl https://api.trakt.tv/recommendations/movies?limit=10 \
  -H "Authorization: Bearer $TRAKT_ACCESS_TOKEN" \
  -H "trakt-api-version: 2" \
  -H "trakt-api-key: $TRAKT_CLIENT_ID"
```

**获取热门内容：**
```bash
curl https://api.trakt.tv/movies/trending \
  -H "trakt-api-version: 2" \
  -H "trakt-api-key: $TRAKT_CLIENT_ID"
```

**获取热门剧集：**
```bash
curl https://api.trakt.tv/movies/popular \
  -H "trakt-api-version: 2" \
  -H "trakt-api-key: $TRAKT_CLIENT_ID"
```

## 数据格式

### 电影对象（Movie Object）
```json
{
  "title": "Inception",
  "year": 2010,
  "ids": {
    "trakt": 16662,
    "slug": "inception-2010",
    "imdb": "tt1375666",
    "tmdb": 27205
  }
}
```

### 剧集对象（Show Object）
```json
{
  "title": "Breaking Bad",
  "year": 2008,
  "ids": {
    "trakt": 1,
    "slug": "breaking-bad",
    "tvdb": 81189,
    "imdb": "tt0903747",
    "tmdb": 1396
  }
}
```

### 集数对象（Episode Object）
```json
{
  "season": 1,
  "number": 1,
  "title": "Pilot",
  "ids": {
    "trakt": 73482,
    "tvdb": 349232,
    "imdb": "tt0959621",
    "tmdb": 62085
  }
}
```

## 使用说明

当用户请求与Trakt交互时，请遵循以下步骤：

1. **始终使用curl**并设置正确的请求头，包括访问令牌。
2. 所有请求都必须包含以下请求头：
   - `trakt-api-version: 2`
   - `trakt-api-key: $TRAKT_CLIENT_ID`
   - `Authorization: Bearer $TRAKT_ACCESS_TOKEN`（已认证的请求）
   - `Content-Type: application/json`（POST/PUT/DELETE请求）

3. 使用电影标题和年份来识别项目；如果可用，也可以使用项目ID。
4. 根据操作类型选择相应的API端点：
   - 观看列表：`/sync/watchlist`（POST用于添加，/sync/watchlist/remove用于删除）
   - 历史记录：`/sync/history`（GET用于查看，POST用于添加）
   - 收藏夹：`/sync/collection`（GET用于查看，POST用于添加）
   - 评分：`/sync/ratings`（GET用于查看，POST用于添加）
   - 搜索：`/search/{type}?query={q}`（无需认证）
   - 热门内容：`/{type}/trending`（无需认证）
   - 热门剧集：`/{type}/popular`（无需认证）
   - 推荐内容：`/recommendations/{type}`（需要认证）

5. **正确处理响应**：
   - 成功：状态码200/201
   - 未找到：404
   - 未经授权：401（可能需要刷新令牌）
   - 评分限制：429

## 速率限制

- **已认证用户**：每5分钟1000个GET请求，每秒1个POST/PUT/DELETE请求。
- **未认证用户**：每5分钟1000个GET请求。

## 获取OAuth令牌

要获取访问令牌，请使用以下辅助脚本：

```bash
#!/bin/bash
# Save as get_trakt_token.sh

CLIENT_ID="your_client_id"
CLIENT_SECRET="your_client_secret"
REDIRECT_URI="urn:ietf:wg:oauth:2.0:oob"

echo "1. Open this URL in your browser:"
echo "https://trakt.tv/oauth/authorize?response_type=code&client_id=$CLIENT_ID&redirect_uri=$REDIRECT_URI"
echo ""
echo "2. Authorize the app and copy the code"
echo -n "3. Paste the code here: "
read CODE

echo ""
echo "Exchanging code for token..."

RESPONSE=$(curl -s -X POST https://api.trakt.tv/oauth/token \
  -H "Content-Type: application/json" \
  -d "{
    \"code\": \"$CODE\",
    \"client_id\": \"$CLIENT_ID\",
    \"client_secret\": \"$CLIENT_SECRET\",
    \"redirect_uri\": \"$REDIRECT_URI\",
    \"grant_type\": \"authorization_code\"
  }")

echo ""
echo "Response:"
echo "$RESPONSE" | jq .
echo ""
echo "Add these to your OpenClaw config:"
echo "TRAKT_ACCESS_TOKEN=$(echo $RESPONSE | jq -r .access_token)"
echo "TRAKT_REFRESH_TOKEN=$(echo $RESPONSE | jq -r .refresh_token)"
```

将其设置为可执行文件：`chmod +x get_trakt_token.sh`

## 示例

**用户**：“将《沙丘》添加到我的Trakt观看列表中。”

**助手**：我会将《沙丘》添加到您的Trakt观看列表中。

```bash
curl -X POST https://api.trakt.tv/sync/watchlist \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TRAKT_ACCESS_TOKEN" \
  -H "trakt-api-version: 2" \
  -H "trakt-api-key: $TRAKT_CLIENT_ID" \
  -d '{"movies":[{"title":"Dune","year":2021}]}'
```

---

**用户**：“Trakt上有哪些热门电影？”

**助手**：我正在查询Trakt上的热门电影。

```bash
curl "https://api.trakt.tv/movies/trending?limit=10" \
  -H "trakt-api-version: 2" \
  -H "trakt-api-key: $TRAKT_CLIENT_ID"
```

---

**用户**：“在Trakt上将《绝命毒师》的评分设置为10/10。”

**助手**：我已将《绝命毒师》的评分设置为10/10。

```bash
curl -X POST https://api.trakt.tv/sync/ratings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TRAKT_ACCESS_TOKEN" \
  -H "trakt-api-version: 2" \
  -H "trakt-api-key: $TRAKT_CLIENT_ID" \
  -d '{"shows":[{"title":"Breaking Bad","year":2008,"rating":10}]}'
```

## 注意事项

- 被标记为已观看的项目会自动从观看列表中删除。
- 为了提高准确性，您可以使用项目ID而不是标题或年份。
- 可以使用`?extended=full`参数来获取更多详细信息。
- 所有日期都应采用UTC ISO 8601格式。
- 该API支持批量操作——您可以在一个请求中添加多个项目。