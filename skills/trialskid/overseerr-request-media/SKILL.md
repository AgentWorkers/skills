# 使用Overseerr请求媒体资源

## 功能
允许用户通过Overseerr实例请求电影或电视剧。Overseerr会将请求转发给Sonarr/Radarr。

## 所需环境变量：
- `OVERSEERR_URL`（示例：`https://overseerr.yourdomain.com`）
- `OVERSEERR_API_KEY`

## 需要的认证信息：
- `X-Api-Key`: `$OVERSEERR_API_KEY`

Overseerr能够根据用户配置的Plex + Sonarr/Radarr连接，判断媒体资源是否已经存在或已被请求过。

## 该功能支持的操作示例：
- “请求《星际穿越》”
- “将《星际穿越》添加到Overseerr的收藏列表中”
- “请求《伸出手来》第二季”
- “请求《办公室》第2-4季”

## 必须遵循的工作流程：

### 1) 解析用户请求
- 提取以下信息：
  - 电影/电视剧的标题
  - 可选类型提示（movie或tv）
  - 可选的季数（如：`season 2`、`seasons 1-3`、`season 1 and 4`）

### 2) 向Overseerr发送搜索请求
使用以下URL发送GET请求：
```
$OVERSEERR_URL/api/v1/search?query=<url-encoded title>
```
示例：
```
curl -s -H "X-Api-Key: $OVERSEERR_API_KEY" \
 "$OVERSEERR_URL/api/v1/search?query=interstellar"
```

### 3) 确认搜索结果是否模糊（同名电影与电视剧）
如果搜索结果中同时包含：
- 一部电影
- 一部电视剧，
且它们的标题相同或非常相似，
则需要用户先进行选择。

最多显示2-4个选项，例如：
- 电影：标题（年份）
- 电视剧：标题（年份）

如果用户明确指定了类型（如“movie”、“show”、“tv”、“season 2”），则自动选择相应的类型。

### 4) 选择最合适的匹配结果
- 优先选择标题完全匹配的结果
- 在有多个结果时，优先选择人气最高的结果
- 如果用户提供了类型提示（movie或tv），则尊重用户的偏好

### 5) 检查媒体资源的状态
在创建请求之前，需要检查选中的资源是否已经存在或已被请求：
- 查看Overseerr返回的资源可用性/请求状态信息。
  - 如果资源已经在库中：
    - 不要再次请求
    - 回复：“资源已存在 ✅”
  - 如果资源已被请求（处于待处理、已批准或已请求状态）：
    - 不要再次请求
    - 回复：“资源已请求 ✅”
  - 如果API返回的状态不明确：
    - 继续创建请求
    - 如果由于重复请求导致POST请求失败，回复：“资源已请求 ✅”

### 6) 创建请求
使用以下URL发送POST请求：
```
$OVERSEERR_URL/api/v1/request
```
**电影请求的JSON格式：**
```json
{
  "mediaType": "movie",
  "mediaId": <tmdbId>
}
```
**电视剧（完整季数）的JSON格式：**
```json
{
  "mediaType": "tv",
  "mediaId": <tmdbId>
}
```
**电视剧（特定季数）的JSON格式：**
```json
{
  "mediaType": "tv",
  "mediaId": <tmdbId>,
  "seasons": [2, 3]
}
```
示例：
- 请求电影：
```bash
curl -s -X POST \
-H "X-Api-Key: $OVERSEERR_API_KEY" \
-H "Content-Type: application/json" \
"$OVERSEERR_URL/api/v1/request" \
-d '{"mediaType":"movie","mediaId":157336}'
```
- 请求完整季数的电视剧：
```bash
curl -s -X POST \
-H "X-Api-Key: $OVERSEERR_API_KEY" \
-H "Content-Type: application/json" \
"$OVERSEERR_URL/api/v1/request" \
-d '{"mediaType":"tv","mediaId":71912}'
```
- 请求《伸出手来》第二季：
```bash
curl -s -X POST \
-H "X-Api-Key: $OVERSEERR_API_KEY" \
-H "Content-Type: application/json" \
"$OVERSEERR_URL/api/v1/request" \
"$OVERSEERR_URL/api/v1/request" \
-d '{"mediaType":"tv","mediaId":71912,"seasons":[2]}'
```

### 7) 清晰地回复用户
- 确认用户请求的内容
  - 如果是电视剧请求，列出可选择的季数
  - 如果资源已存在或已被请求，告知用户
  - 如果没有找到结果，询问用户是否可以提供其他拼写或更多信息

## 回复格式：
- 简洁的确认信息：
  - “✅ 已请求：《星际穿越》（2014年）”
  - “✅ 已请求：《伸出手来》第二季”
  - “资源已存在 ✅”
  - “资源已请求 ✅”

## 错误处理：
- 如果搜索结果为空：
  - 询问用户是否可以提供其他标题或年份
- 如果有多个相似的结果：
  - 询问用户从2-4个选项中选择