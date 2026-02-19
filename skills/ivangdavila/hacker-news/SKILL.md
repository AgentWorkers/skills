---
name: Hacker News
slug: hacker-news
version: 1.0.0
description: 通过 API 访问 Hacker News，您可以搜索和浏览文章、评论、用户以及招聘信息。
metadata: {"clawdbot":{"emoji":"🟠","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 快速参考

| 主题 | 文件 |
|-------|------|
| API 端点 | `api.md` |
| 搜索模式 | `search.md` |

## 核心规则

### 1. 提供两种 API
| API | 使用场景 | 基本 URL |
|-----|----------|----------|
| 官方 HN API | 单个项目，实时数据 | `https://hacker-news.firebaseio.com/v0` |
| Algolia 搜索 | 全文搜索，支持过滤 | `https://hn.algolia.com/api/v1` |

### 2. 官方 API 端点
- `/topstories.json` — 前 500 个故事 ID
- `/newstories.json` — 最新的 500 个故事 ID  
- `/beststories.json` — 最受欢迎的故事  
- `/askstories.json` — 提问 HN  
- `/showstories.json` — 显示 HN 内容  
- `/jobstories.json` — 招聘信息  
- `/item/{id}.json` — 故事/评论详情  
- `/user/{username}.json` — 用户个人资料  

### 3. Algolia 搜索语法
```
/search?query=TERM&tags=TAG&numericFilters=FILTER
```

**标签（可与其他标签使用 AND 进行组合）：**
- `story`、`comment`、`poll`、`job`、`ask_hn`、`show_hn`  
- `author_username` — 按用户筛选帖子  
- `story_ID` — 筛选特定故事下的评论  

**数值过滤器：**
- `created_at_i>TIMESTAMP` — 时间在指定日期之后  
- `points>N` — 分数大于指定值  
- `num_comments>N` — 评论数大于指定值  

### 4. 常见搜索模式
| 请求 | 端点 |
|---------|----------|
- 首页内容 | 官方 API：`/topstories.json`（获取前 30 个条目）  
- 搜索帖子 | Algolia：`/search?query=X&tags=story`  
- 用户的帖子 | Algolia：`/search?tags=author_username`  
- 哪里在招聘？ | Algolia：`/search?query=who is hiring&tags=story,author_whoishiring`  
- 故事评论 | Algolia：`/search?tags=comment,story_ID`  
- 本周热门内容 | Algolia：`/search?tags=story&numericFilters=created_at_i>WEEK_TS`  

### 5. 响应处理
- 官方 API 返回项目 ID — 需要批量获取数据（可并行处理）  
- Algolia 返回包含 `hits[]` 数组的完整对象  
- 故事对象：`id`、`title`、`url`、`score`、`by`、`time`、`descendants`（评论数量）  
- 评论对象：`id`、`text`、`by`、`parent`、`time`  

### 6. 请求限制
- 官方 API：无需认证，请求限制较为宽松  
- Algolia：每小时 10,000 次请求（无需密钥）  
- 处理大量结果时请使用分页（`page=N`、`hitsPerPage=N`）  

### 7. 注意事项
- 对于 `Ask HN` 和 `Show HN` 中的文本帖子，`url` 字段可能为空，此时应使用 `text` 字段  
- 系统中可能存在已删除或过时的数据，请在显示前进行验证  
- 时间戳以 Unix 秒为单位，而非毫秒  
- Algolia 的 `objectID` 与 HN 的 `id` 相同（以字符串形式表示）