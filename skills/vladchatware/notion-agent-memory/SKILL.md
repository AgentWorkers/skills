---
name: agent-memory
description: 使用 Notion 构建的人工智能代理的结构化内存系统。适用于配置代理内存、讨论内存持久性，以及帮助代理在不同会话之间保持上下文记忆。该系统包括 ACT 框架数据库、MEMORY.md 模板以及“连续性循环”（Continuity Cycle）模式。
---
# 代理内存管理

使用 Notion 数据库为你的代理构建结构化的内存管理系统。

## 快速入门

1. 在 `notion.so/my-integrations` 中创建 Notion 集成。
2. 生成访问令牌：`echo "ntn_XXX" > ~/.config/notion/api_key`
3. 创建一个包含 3 个 ACT 数据库的代理工作区页面（详见 `references/act-framework.md`）。
4. 将 `MEMORY.md` 文件添加到代理的系统提示中（详见 `assets/MEMORY-TEMPLATE.md`）。

## 内存结构

### 第一层：每日日志（`memory/YYYY-MM-DD.md`）
原始事件日志——记录了工作过程中发生的事情及其时间。

### 第二层：长期记忆（`MEMORY.md`）
整理后的知识：包括模式、偏好、经验教训以及正在进行的项目。

### 第三层：Notion（ACT 数据库）
结构化的外部存储空间，代理可以通过 API 进行查询和更新。

## ACT 框架

三个用于代理结构化认知的数据库：

| 数据库 | 用途 | 使用场景 |
|----------|---------|-------------|
| ACT I：隐藏的叙事（Hidden Narratives） | 跟踪模式、假设和盲点 | 发现与反思 |
| ACT II：无限可能（Limitless (MMM) | 思维方式/方法/动机突破 | 成长时刻 |
| ACT III：创意管道（Ideas Pipeline） | 捕获 → 评估 → 实施创意 | 持续进行 |

**完整数据库架构：** 详见 `references/act-framework.md`

## 连续性循环

```
DO WORK → DOCUMENT → UPDATE INSTRUCTIONS → NEXT SESSION STARTS SMARTER
```

**两个重要的步骤：** 在标记某项任务为“已完成”之前，请先问自己：“如果我明天醒来时对所有事情都毫无记忆，我还能从哪里继续工作？”
**完整的连续性循环模型：** 详见 `references/continuity-cycle.md`

## Notion API 模式

### 查询数据库
```bash
curl -s "https://api.notion.com/v1/databases/$DB_ID/query" \
  -H "Authorization: Bearer $(cat ~/.config/notion/api_key)" \
  -H 'Notion-Version: 2022-06-28' \
  -H 'Content-Type: application/json' \
  -d '{"filter": {"property": "Status", "select": {"equals": "in progress"}}}'
```

### 添加新条目
```bash
curl -X POST 'https://api.notion.com/v1/pages' \
  -H "Authorization: Bearer $(cat ~/.config/notion/api_key)" \
  -H 'Notion-Version: 2022-06-28' \
  -H 'Content-Type: application/json' \
  -d '{
    "parent": {"database_id": "'$DB_ID'"},
    "properties": {
      "Idea": {"title": [{"text": {"content": "Your idea"}}]},
      "Status": {"select": {"name": "captured"}}
    }
  }'
```

## 日常工作流程

**会话开始：**
1. 阅读 `MEMORY.md`。
2. 阅读今天的日志文件 `memory/YYYY-MM-DD.md`。
3. 检查 Notion 中的未完成事项。

**工作过程中：**
- 立即将事件记录到每日日志文件中。
- 新见解 → 分类到 ACT I 数据库。
- 突破性发现 → 分类到 ACT II 数据库。
- 新创意 → 分类到 ACT III 数据库。

**会话结束：**
- 更新 `MEMORY.md`，记录长期学习的内容。
- 更新 Notion 中的任务状态。

## 相关文件

- `references/act-framework.md` — 完整的数据库架构。
- `references/continuity-cycle.md` — 完整的连续性循环模型。
- `assets/MEMORY-TEMPLATE.md` — 代理使用的 `MEMORY.md` 模板文件。