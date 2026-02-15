---
name: raindrop
description: 同步并处理来自 Raindrop.io 的书签。适用于获取新书签、分析已保存的内容或将书签同步到知识库的场景。该功能会在以下事件触发：`raindrop`、`bookmarks`、`sync bookmarks`、`new saves`。
---
# Raindrop 书签同步

从 Raindrop.io API 获取书签信息，并将其整合到知识库中。

## 设置

1. 从 [https://app.raindrop.io/settings/integrations](https://app.raindrop.io/settings/integrations) 获取 API 令牌。
2. 创建一个测试令牌（只读权限即可）。
3. 将令牌保存到 `.secrets/raindrop.env` 文件中：
   ```
   RAINDROP_TOKEN=your_token_here
   ```

## 使用方法

### 获取新书签
```bash
source .secrets/raindrop.env
python3 skills/raindrop/scripts/fetch.py --since 24h
```

### 从特定集合中获取书签
```bash
python3 skills/raindrop/scripts/fetch.py --collection 12345678
```

### 处理书签信息并添加到知识库
```bash
python3 skills/raindrop/scripts/fetch.py --since 24h --output /tmp/raindrop-new.json
# Then process each item with web_fetch and add to memory/knowledge-base.md
```

## API 参考

- **基础 URL：** `https://api.raindrop.io/rest/v1`
- **身份验证：** 在请求头中添加 Bearer 令牌。
- **请求速率限制：** 每分钟 120 次请求。

### 主要 API 端点
- `GET /raindrops/{collectionId}` — 获取书签列表（使用 `0` 可获取所有书签）。
- `GET /collections` — 获取集合列表。
- `GET /raindrop/{id}` — 获取单个书签的详细信息。

### 书签对象结构
```json
{
  "_id": 123456,
  "title": "Article Title",
  "link": "https://example.com/article",
  "excerpt": "Short description...",
  "tags": ["tag1", "tag2"],
  "created": "2026-02-15T10:00:00Z",
  "collection": {"$id": 12345678}
}
```

## 工作流程

1. **获取新书签**：获取自上次同步以来的新书签。
2. **过滤**：跳过已处理过的书签链接（检查 `memory/kb-index.json` 文件）。
3. **提取内容**：使用 `web_fetch` 函数提取书签内容。
4. **分析内容**：对书签内容进行总结并添加标签。
5. **存储书签信息**：将处理后的书签信息追加到 `memory/knowledge-base.md` 文件中。
6. **更新索引**：将书签的 URL 添加到 `memory/kb-index.json` 文件中。

## 定时同步

可以通过心跳任务或 Cron 作业实现自动同步：
```
每天检查一次 Raindrop 新书签，处理后存入知识库
```