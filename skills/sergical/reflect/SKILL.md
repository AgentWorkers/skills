---
name: reflect
description: 将内容添加到每日笔记中，并在 Reflect 中创建新的笔记。这些笔记可用于记录想法、待办事项，或将信息同步到你的知识图谱中。
homepage: https://reflect.app
---

# Reflect笔记功能

Reflect是一款基于网络的笔记应用。所有笔记都采用端到端（E2E）加密技术，因此其API仅支持**追加操作**——我们只能添加内容，无法读取笔记内容。

## 设置

1. 在 [https://reflect.app/developer/oauth](https://reflect.app/developer/oauth) 创建OAuth凭证。
2. 通过该接口生成访问令牌。
3. 设置环境变量：
   ```bash
   export REFLECT_TOKEN="your-access-token"
   export REFLECT_GRAPH_ID="your-graph-id"  # Find via: curl -H "Authorization: Bearer $REFLECT_TOKEN" https://reflect.app/api/graphs
   ```

或者将访问令牌存储在1Password中，并更新`scripts/reflect.sh`文件中的凭证路径。

## 功能概述

1. **追加到每日笔记**：将新内容添加到当天的笔记中（或指定日期的笔记中）。
2. **创建新笔记**：创建包含主题和Markdown内容的独立笔记。
3. **创建链接**：保存带有高亮标记的书签。
4. **获取链接/书籍**：检索已保存的链接和笔记内容。

## API参考

基础URL：`https://reflect.app/api`
认证方式：`Authorization: Bearer <access_token>`

### 追加到每日笔记

```bash
curl -X PUT "https://reflect.app/api/graphs/$REFLECT_GRAPH_ID/daily-notes" \
  -H "Authorization: Bearer $REFLECT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your text here",
    "transform_type": "list-append",
    "date": "2026-01-25",          # optional, defaults to today
    "list_name": "[[List Name]]"   # optional, append to specific list
  }'
```

### 创建新笔记

```bash
curl -X POST "https://reflect.app/api/graphs/$REFLECT_GRAPH_ID/notes" \
  -H "Authorization: Bearer $REFLECT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Note Title",
    "content_markdown": "# Heading\n\nContent here...",
    "pinned": false
  }'
```

### 创建链接

```bash
curl -X POST "https://reflect.app/api/graphs/$REFLECT_GRAPH_ID/links" \
  -H "Authorization: Bearer $REFLECT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "title": "Page Title",
    "description": "Optional description",
    "highlights": ["Quote 1", "Quote 2"]
  }'
```

### 获取链接

```bash
curl "https://reflect.app/api/graphs/$REFLECT_GRAPH_ID/links" \
  -H "Authorization: Bearer $REFLECT_TOKEN"
```

## 辅助脚本

使用`scripts/reflect.sh`执行常见操作：

```bash
# Append to daily note
./scripts/reflect.sh daily "Remember to review PR #6"

# Append to specific list in daily note  
./scripts/reflect.sh daily "Buy milk" "[[Shopping]]"

# Create a new note
./scripts/reflect.sh note "Meeting Notes" "# Standup\n\n- Discussed X\n- Action item: Y"

# Save a link
./scripts/reflect.sh link "https://example.com" "Example Site" "Great resource"
```

## 使用场景

- **将聊天中的待办事项捕获并追加到每日笔记中**。
- **保存对话中提到的有趣链接**。
- **创建会议笔记或总结**。
- **将提醒同步到Reflect中进行持久化存储**。
- **为列表（如`[[Ideas]]`或`[[Project Name]]`）创建超链接**。

## 限制

- **无法读取笔记内容**（采用端到端加密）。
- **仅支持追加操作**——无法编辑或删除现有内容。
- **无搜索功能**——无法查询现有笔记。