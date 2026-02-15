---
name: ai-picture-book
description: 使用百度AI生成静态或动态的图画书视频
metadata: { "openclaw": { "emoji": "📔", "requires": { "bins": ["python3"], "env":["BAIDU_API_KEY"]},"primaryEnv":"BAIDU_API_KEY" } }
---

# 人工智能图画书

根据故事或描述生成图画书视频。

## 工作流程

1. **创建任务**：提交故事内容 → 获取任务ID
2. **查询任务状态**：每隔5-10秒查询一次任务状态，直到任务完成
3. **获取结果**：当任务状态变为“2”时，获取视频链接

## 图画书类型

| 类型 | 方法 | 描述 |
|------|--------|-------------|
| 静态 | 9 | 静态图画书 |
| 动态 | 10 | 动态图画书 |

**要求**：用户必须指定图画书类型（静态/9 或 动态/10）。如果未指定，系统会提示用户进行选择。

## 状态代码

| 代码 | 状态 | 处理方式 |
|-------|---------|---------|
| 0, 1, 3 | 进行中 | 继续查询任务状态 |
| 2 | 完成 | 返回结果 |
| 其他 | 失败 | 显示错误信息 |

## API

### 创建任务

**接口地址**：`POST /v2/tools/ai_picture_book/task_create`

**参数**：
- `method`（必填）：`9` 表示静态图画书；`10` 表示动态图画书
- `content`（必填）：故事内容或描述

**示例**：
```bash
python3 scripts/ai_picture_book_task_create.py 9 "A brave cat explores the world."
```

**响应**：
```json
{ "task_id": "uuid-string" }
```

### 查询任务状态

**接口地址**：`GET /v2/tools/ai_picture_book/query`

**参数**：
- `task_id`（必填）：通过创建任务接口获得的任务ID

**示例**：
```bash
python3 scripts/ai_picture_book_task_query.py "task-id-here"
```

**响应**（任务已完成）：
```json
{
  "status": 2,
  "video_bos_url": "https://...",
}
```

## 自动查询策略（推荐）

### 自动查询示例：
```bash
python3 scripts/ai_picture_book_poll.py <task_id> [max_attempts] [interval_seconds]
```

### 手动查询
1. 创建任务 → 存储任务ID
2. 每隔5-10秒查询一次任务状态，直到状态变为“2”
3. 如果超过2-3分钟仍未完成，则视为超时，建议稍后再试

## 错误处理

- 内容无效：`内容不能为空`
- 类型错误：`输入的类型无效。请使用 9（静态图画书）或 10（动态图画书）`
- 处理错误：`生成图画书时出现错误`
- 超时：`任务超时，请稍后再试`