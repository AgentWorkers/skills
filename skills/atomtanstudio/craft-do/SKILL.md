# Craft.do 集成技能

本技能实现了与 Craft.do（一款美观的笔记和文档管理应用）的完整 REST API 集成。

## 概述

该技能提供了对 Craft.do 的全面编程访问能力，支持以下功能：
- **任务自动化**：在收件箱、每日笔记、日志本中创建、更新和管理任务
- **文档工作流**：编程方式创建、读取和整理文档
- **文件夹管理**：通过 API 构建嵌套文件夹结构
- **Obsidian 数据库迁移**：一次性迁移所有内容并保留原有结构
- **内容操作**：通过 `/blocks` 端点添加或编辑 Markdown 内容

Craft.do 的主要特性包括：
- 原生 Markdown 支持
- 任务管理（收件箱、每日笔记、日志本）
- 文件夹和文档的层级结构
- 完整的 REST API 接口

## 设置

1. 从 Craft.do 的设置中获取您的 API 密钥
2. 安全存储您的凭据：

```bash
export CRAFT_API_KEY="pdk_xxx"
export CRAFT_ENDPOINT="https://connect.craft.do/links/YOUR_LINK/api/v1"
```

## API 功能

### ✅ 可用的功能

#### 列出文件夹
```bash
curl -H "Authorization: Bearer $CRAFT_API_KEY" \
  "$CRAFT_ENDPOINT/folders"
```

返回所有文件夹的位置：未分类文件夹、每日笔记文件夹、回收站文件夹、模板文件夹以及自定义文件夹。

#### 列出文档
```bash
curl -H "Authorization: Bearer $CRAFT_API_KEY" \
  "$CRAFT_ENDPOINT/documents?folderId=FOLDER_ID"
```

#### 创建文件夹（可选设置父文件夹以实现嵌套）
```bash
# Root-level folder
curl -X POST \
  -H "Authorization: Bearer $CRAFT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "folders": [{
      "name": "Projects"
    }]
  }' \
  "$CRAFT_ENDPOINT/folders"

# Nested folder (requires parent folder ID)
curl -X POST \
  -H "Authorization: Bearer $CRAFT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "folders": [{
      "name": "Q1 2024",
      "parentFolderId": "PARENT_FOLDER_ID"
    }]
  }' \
  "$CRAFT_ENDPOINT/folders"
```

#### 创建文档
```bash
curl -X POST \
  -H "Authorization: Bearer $CRAFT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [{
      "title": "Document Title"
    }],
    "destination": {
      "folderId": "FOLDER_ID"
    }
  }' \
  "$CRAFT_ENDPOINT/documents"
```

**注意：**文档创建时默认为空。请使用 `/blocks` 端点添加内容。

#### 向文档添加内容
```bash
curl -X POST \
  -H "Authorization: Bearer $CRAFT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "blocks": [{
      "type": "text",
      "markdown": "# Document content\n\nFull markdown support!"
    }],
    "position": {
      "pageId": "DOCUMENT_ID",
      "position": "end"
    }
  }' \
  "$CRAFT_ENDPOINT/blocks"
```

#### 读取文档内容
```bash
curl -H "Authorization: Bearer $CRAFT_API_KEY" \
  "$CRAFT_ENDPOINT/blocks?id=DOCUMENT_ID"
```

返回包含所有区块的完整 Markdown 内容。

#### 创建任务
```bash
curl -X POST \
  -H "Authorization: Bearer $CRAFT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tasks": [{
      "markdown": "Task description",
      "location": {"type": "inbox"},
      "status": "active"
    }]
  }' \
  "$CRAFT_ENDPOINT/tasks"
```

#### 更新任务（标记为已完成）
```bash
curl -X PUT \
  -H "Authorization: Bearer $CRAFT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tasksToUpdate": [{
      "id": "TASK_ID",
      "markdown": "- [x] Completed task"
    }]
  }' \
  "$CRAFT_ENDPOINT/tasks"
```

#### 列出任务
```bash
# Active tasks
curl -H "Authorization: Bearer $CRAFT_API_KEY" \
  "$CRAFT_ENDPOINT/tasks?scope=active"

# All completed (logbook)
curl -H "Authorization: Bearer $CRAFT_API_KEY" \
  "$CRAFT_ENDPOINT/tasks?scope=logbook"

# Upcoming
curl -H "Authorization: Bearer $CRAFT_API_KEY" \
  "$CRAFT_ENDPOINT/tasks?scope=upcoming"

# Inbox only
curl -H "Authorization: Bearer $CRAFT_API_KEY" \
  "$CRAFT_ENDPOINT/tasks?scope=inbox"
```

#### 移动文档
```bash
curl -X PUT \
  -H "Authorization: Bearer $CRAFT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "documentIds": ["DOC_ID"],
    "destination": {"location": "unsorted"}
  }' \
  "$CRAFT_ENDPOINT/documents/move"
```

**注意：**只能将文档移动到“未分类”文件夹、“模板文件夹”或自定义文件夹中，不能直接移动到回收站。

### ❌ 限制

- **无 Collections API**：无法通过 API 访问 Collections（数据库中的文件夹结构）
- **无法删除任务**：只能创建或更新任务，无法删除
- **无法直接删除文档**：只能移动文档
- **无搜索功能**：搜索需要特定的查询格式（需进一步测试）
- **过滤功能有限**：Collections 的过滤和分组只能在用户界面中进行，无法通过 API 完成

## 常见用例

### 从外部系统同步任务
```bash
# Create task in Craft from Mission Control
TASK_TITLE="Deploy new feature"
curl -X POST \
  -H "Authorization: Bearer $CRAFT_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"tasks\": [{
      \"markdown\": \"$TASK_TITLE\",
      \"location\": {\"type\": \"inbox\"},
      \"status\": \"active\"
    }]
  }" \
  "$CRAFT_ENDPOINT/tasks"
```

### 创建每日笔记
```bash
TODAY=$(date +%Y-%m-%d)
curl -X POST \
  -H "Authorization: Bearer $CRAFT_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"documents\": [{
      \"title\": \"Daily Note - $TODAY\",
      \"content\": [{\"textContent\": \"# $TODAY\\n\\n## Tasks\\n\\n## Notes\\n\"}],
      \"location\": \"daily_notes\"
    }]
  }" \
  "$CRAFT_ENDPOINT/documents"
```

### 归档已完成的工作
```bash
# Get all completed tasks
curl -H "Authorization: Bearer $CRAFT_API_KEY" \
  "$CRAFT_ENDPOINT/tasks?scope=logbook" | jq '.items[] | {id, markdown, completedAt}'
```

## 集成模式

### Mission Control → Craft 同步

**问题：**Mission Control 具有自动化功能，但用户界面不够友好；Craft 拥有美观的用户界面，但缺乏自动化功能。

**解决方案：**将 Mission Control 作为数据源，将已完成的工作同步到 Craft 中以便查看。

```bash
#!/bin/bash
# sync-to-craft.sh - Sync completed tasks to Craft

# Read completed tasks from Mission Control
COMPLETED_TASKS=$(cat mission-control/tasks.json | jq -r '.[] | select(.status=="done") | .title')

# Push each to Craft
echo "$COMPLETED_TASKS" | while read -r task; do
  curl -X POST \
    -H "Authorization: Bearer $CRAFT_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
      \"tasks\": [{
        \"markdown\": \"- [x] $task\",
        \"location\": {\"type\": \"inbox\"}
      }]
    }" \
    "$CRAFT_ENDPOINT/tasks"
done
```

## Markdown 支持

Craft 完全支持 Markdown 格式：
- 标题：`# H1`、`## H2` 等
- 列表：`- item`、`1. item`
- 任务：`- [ ] 待办事项`、`- [x] 已完成`
- 链接：`[text](url)`
- 代码：``` `inline` `` 或 ` ```block``` `
- 强调：`*italic*`、`**bold``

所有内容都以 Markdown 格式存储和返回，非常适合编程操作。

## 最佳实践

1. **安全存储 API 密钥**：切勿将密钥直接写入代码中
2. **先在“未分类”文件夹中进行测试**：便于查找和清理测试结果
3. **使用 Markdown 格式**：两种系统都支持 Markdown 格式
4. **仅进行单向同步**：从 Craft 向外部系统读取数据，从外部系统向 Craft 写入数据
5. **批量操作**：API 支持数组操作，提高效率
6. **优雅地处理错误**：API 会返回详细的验证错误信息

## 错误处理

常见错误：
- `VALIDATION_ERROR`：检查必填字段（如 Markdown 内容、文件夹位置等）
- `403`：API 密钥无效或已过期
- `404`：未找到文档或任务 ID

示例验证错误：
```json
{
  "error": "Validation failed",
  "code": "VALIDATION_ERROR",
  "details": [{
    "path": ["tasks", 0, "markdown"],
    "message": "Invalid input: expected string"
  }]
}
```

## 未来可能的功能

当 Craft 扩展其 API 功能时：
- [ ] 通过 API 实现 Collections 的创建、读取、更新和删除操作
- [ ] 文档的创建和删除
- [ ] 高级搜索功能
- [ ] 实时同步的 Webhook 功能
- [ ] 大规模数据集的批量操作

## 资源

- [Craft API 文档](https://craft.do/api)（从 Craft 设置中获取您的个人 API 端点）
- [Craft 博客 - Collections 功能](https://www.craft.do/blog/introducing-collections)
- [Craft YouTube 频道](https://www.youtube.com/channel/UC8OIJ9uNRQZiG78K2BSn67A)

## 测试清单

- [x] 列出文件夹
- [x] 列出文档
- [x] 创建文档
- [x] 通过 `/blocks` 端点向文档添加内容
- [x] 读取文档内容
- [x] 创建任务
- [x] 更新任务（标记为已完成）
- [x] 列出所有任务
- [x] 在不同文件夹之间移动文档
- [x] 完整地从 Obsidian 数据库迁移到 Craft
- [x] 搜索功能（需要进一步优化格式）
- [x] Collections 功能（目前无法通过 API 访问）
- [x] 无法删除任务
- [x] 无法直接删除文档（只能移动）

## 示例：完整的工作流程

```bash
# 1. Create a project folder
PROJECT_ID=$(curl -X POST \
  -H "Authorization: Bearer $CRAFT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Q1 2024 Projects"}' \
  "$CRAFT_ENDPOINT/folders" | jq -r '.id')

# 2. Create a project document
DOC_ID=$(curl -X POST \
  -H "Authorization: Bearer $CRAFT_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"documents\": [{
      \"title\": \"Project Alpha\",
      \"content\": [{\"textContent\": \"## Overview\\n\\nProject details here.\"}],
      \"location\": \"$PROJECT_ID\"
    }]
  }" \
  "$CRAFT_ENDPOINT/documents" | jq -r '.items[0].id')

# 3. Create tasks for the project
curl -X POST \
  -H "Authorization: Bearer $CRAFT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tasks": [
      {"markdown": "Design wireframes", "location": {"type": "inbox"}},
      {"markdown": "Build prototype", "location": {"type": "inbox"}},
      {"markdown": "User testing", "location": {"type": "inbox"}}
    ]
  }' \
  "$CRAFT_ENDPOINT/tasks"

# 4. Mark first task complete
TASK_ID=$(curl -H "Authorization: Bearer $CRAFT_API_KEY" \
  "$CRAFT_ENDPOINT/tasks?scope=active" | jq -r '.items[0].id')

curl -X PUT \
  -H "Authorization: Bearer $CRAFT_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"tasksToUpdate\": [{
      \"id\": \"$TASK_ID\",
      \"markdown\": \"- [x] Design wireframes\"
    }]
  }" \
  "$CRAFT_ENDPOINT/tasks"
```

---

**状态：** 已测试并通过（2026-01-31）
**测试工具：** Craft API v1
**作者：** Eliza