---
name: moviepilot
description: "**MoviePilot** 是一款媒体订阅与管理工具。用户可以使用它来：  
(1) 搜索电影或电视剧；  
(2) 订阅/关注某些电影或电视剧以实现自动下载；  
(3) 查看或管理现有的订阅内容；  
(4) 取消订阅；  
(5) 查看下载进度；  
(6) 浏览推荐内容（来自 Douban、TMDB、Bangumi 等平台）；  
以及执行与 MoviePilot 相关的任何其他操作。"
---
# MoviePilot

通过 MoviePilot API 进行电影/电视剧的搜索、订阅和管理操作。

## 前提条件

在使用前必须设置以下环境变量：
- `MOVIEPILOT_URL` - MoviePilot 服务器地址（例如：`http://127.0.0.1:3000`）
- `MOVIEPILOT_API_KEY` - 用于身份验证的 API 密钥（推荐使用）
- 或 `MOVIEPILOT_TOKEN` - 通过登录获得的令牌

如果未设置凭据，请让用户提供相应的信息。

## 核心工作流程

### 1. 订阅电影/电视剧

典型用户请求：**“帮我订阅《XXX》”** 或 **“订阅《XXX》”**

步骤：
1. 搜索媒体资源：`scripts/moviepilot_api.sh search "title"`
2. 解析搜索结果，并在有多个匹配项时与用户确认（显示剧名、年份、类型、评分等信息）
3. 从选中的结果中提取 `tmdb_id`（或 `douban_id`）、`type`、`title`、`year`
4. 创建订阅：
   ```bash
   scripts/moviepilot_api.sh sub_add '{"name":"Title","type":"电影","tmdbid":12345,"year":"2024"}'
   ```
   - 如果订阅特定季数，请在参数中添加 `"season": N`
   - `type` 必须为 `"电影"`（movie）或 `"电视剧"`（TV show）

### 2. 查看订阅信息

```bash
scripts/moviepilot_api.sh sub_list
```
以可读的列表形式显示订阅信息：名称、类型、年份、状态。

### 3. 取消订阅

- **按订阅 ID 取消订阅**：
   ```bash
scripts/moviepilot_api.sh sub_delete <subscribe_id>
```

- **按媒体 ID 取消订阅**：
   ```bash
scripts/moviepilot_api.sh sub_delete_media "tmdb:12345"
```

### 4. 检查下载状态

```bash
scripts/moviepilot_api.sh downloads
```

### 5. 浏览推荐内容

```bash
# Options: douban_movie_hot, douban_tv_hot, tmdb_trending, tmdb_movies, tmdb_tvs, bangumi_calendar
scripts/moviepilot_api.sh recommend douban_movie_hot
```

### 6. 搜索种子资源

```bash
scripts/moviepilot_api.sh search_resource "keyword"
```

## 重要说明

- 媒体 ID 采用前缀格式：`tmdb:12345`、`douban:12345`、`bangumi:12345`
- 在订阅之前，请务必先进行搜索以获取正确的媒体 ID
- 当搜索结果有多个时，需向用户展示结果供其选择
- `type` 字段的中文表示：`电影`（movie）、`电视剧`（TV show）
- 有关详细的 API 文档，请参阅 [references/api_reference.md](references/api_reference.md)

## 脚本参考

辅助脚本 `scripts/moviepilot_api.sh` 支持以下操作：

| 操作 | 描述 | 示例 |
|--------|-------------|---------|
| `login` | 获取认证令牌 | `login user pass` |
| `search` | 搜索媒体资源 | `search "流浪地球"` |
| `media_detail` | 查看媒体详情 | `media_detail "tmdb:12345"` |
| `sub_list` | 列出所有订阅项 | `sub_list` |
| `sub_add` | 添加订阅 | `sub_add '{"name":"...","type":"电影","tmdbid":123}'` |
| `sub_delete` | 按订阅 ID 删除订阅 | `sub_delete 5` |
| `sub_delete_media` | 按媒体 ID 删除订阅 | `sub_delete_media "tmdb:123"` |
| `sub_detail` | 查看订阅详情 | `sub_detail 5` |
| `sub_refresh` | 刷新所有订阅信息 | `sub_refresh` |
| `sub_history` | 查看订阅历史 | `sub_history movie` |
| `downloads` | 查看当前正在下载的资源 | `downloads` |
| `recommend` | 浏览推荐内容 | `recommend tmdb_trending` |
| `search_resource` | 搜索种子资源 | `search_resource "keyword"` |