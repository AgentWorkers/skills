---
name: prd
description: 创建和管理产品需求文档（Product Requirements Documents, PRDs）。使用场景包括：  
(1) 制定包含用户故事的结构化任务列表；  
(2) 明确各项功能的验收标准；  
(3) 为AI代理或人类开发者规划功能的实现细节。
author: Benjamin Jesuiter <bjesuiter@gmail.com>
metadata:
  clawdbot:
    emoji: "📋"
    os: ["darwin", "linux"]
---

# PRD 技能

用于创建和管理产品需求文档（PRD），以支持功能规划。

## 什么是 PRD？

**产品需求文档（PRD）** 是一种结构化的规范，它：

1. 将一个功能分解为多个**独立的用户故事**；
2. 为每个用户故事定义**可验证的验收标准**；
3. 根据任务的依赖关系来安排执行顺序（数据模型 → 后端 → 用户界面）。

## 快速入门

1. 在项目中创建/编辑 `agents/prd.json` 文件；
2. 定义用户故事及其验收标准；
3. 通过更新 `passes` 的值（从 `false` 更改为 `true`）来跟踪进度。

## prd.json 格式

```json
{
  "project": "MyApp",
  "branchName": "ralph/feature-name",
  "description": "Short description of the feature",
  "userStories": [
    {
      "id": "US-001",
      "title": "Add priority field to database",
      "description": "As a developer, I need to store task priority.",
      "acceptanceCriteria": [
        "Add priority column: 'high' | 'medium' | 'low'",
        "Generate and run migration",
        "Typecheck passes"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    }
  ]
}
```

### 字段说明

| 字段 | 说明 |
|-------|-------------|
| `project` | 项目名称，用于提供上下文信息 |
| `branchName` | 该功能的 Git 分支名（前缀为 `ralph/`） |
| `description` | 功能的简短概述 |
| `userStories` | 需要完成的用户故事列表 |
| `userStories[].id` | 用户故事的唯一标识符（例如：US-001, US-002） |
| `userStories[].title` | 用户故事的简短描述性标题 |
| `userStories[].description` | “作为[用户]，我需要[功能]，因为[好处]” |
| `userStories[].acceptanceCriteria` | 可验证的验收标准 |
| `userStories[].priority` | 执行顺序（数字越小，优先级越高） |
| `userStories[].passes` | 完成状态（`false` 表示未完成；`true` 表示已完成） |
| `userStories[].notes` | 代理添加的运行时备注 |

## 用户故事的规模

**每个用户故事都应在一个工作窗口内完成。**

### ✅ 合适的规模示例：
- 添加一个数据库列并进行数据迁移；
- 为现有页面添加一个用户界面组件；
- 用新的逻辑更新服务器操作；
- 为列表添加一个筛选下拉框。

### ❌ 太大的用户故事（需要拆分）：
- “构建整个仪表板” → 拆分为：数据模型、查询逻辑、用户界面、筛选功能；
- “添加身份验证” → 拆分为：数据模型、中间件、登录界面、会话管理。

## 用户故事的排序

用户故事按照优先级顺序执行。较早完成的用户故事不应依赖于后续的用户故事。

**正确的执行顺序：**
1. 数据模型/数据库变更（数据迁移）；
2. 服务器操作/后端逻辑；
3. 使用后端的用户界面组件；
4. 仪表板/汇总视图。

## 验收标准

验收标准必须是可以验证的，不能含糊不清。

### ✅ 合适的验收标准示例：
- “在任务表中添加一个 `status` 列，默认值为 ‘pending’”；
- “筛选下拉框应包含 ‘All’、‘Active’、‘Completed’ 三个选项”；
- “代码通过类型检查（typecheck）”。

### ❌ 不合适的验收标准示例：
- “功能能够正常运行”；
- “用户可以轻松地完成某项操作”。

**务必包含：** “代码通过类型检查（typecheck passes）”。

## 进度跟踪

当用户故事完成时，将 `passes` 的值更新为 `true`。可以使用 `notes` 字段记录运行时的观察结果：

```json
"notes": "Used IF NOT EXISTS for migrations"
```

## 快速参考

| 操作 | 命令 |
|--------|---------|
| 创建 PRD | 保存到 `agents/prd.json` 文件 |
| 查看状态 | `cat prd.json | jq '.userStories[] | {id, passes}'` |
| 查看未完成的任务 | `jq '.userStories[] | select(.passes == false)' prd.json` |

## 资源

有关详细文档，请参阅 `references/` 目录：
- `agent-usage.md` – 人工智能代理如何执行 PRD（Claude Code、OpenCode 等工具的使用方法）；
- `workflows.md` – 顺序工作流程模式；
- `output-patterns.md` – 模板和示例。