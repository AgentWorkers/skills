---
name: ai-notes-ofvideo
description: **从视频中生成由 AI 驱动的笔记（文档、大纲或图文格式）**
metadata: { "openclaw": { "emoji": "📺", "requires": { "bins": ["python3"], "env":["BAIDU_API_KEY"]},"primaryEnv":"BAIDU_API_KEY" } }
---

# AI 视频笔记

使用百度 AI 从视频 URL 生成结构化的笔记，支持三种笔记格式。

## 工作流程

1. **创建任务**：提交视频 URL → 获取任务 ID
2. **查询任务状态**：每 3-5 秒查询一次任务状态，直到任务完成
3. **获取结果**：当任务状态为 10002 时，获取生成的笔记

## 状态码

| 状态码 | 状态 | 操作 |
|-------|---------|---------|
| 10000 | 进行中 | 继续查询 |
| 10002 | 完成 | 返回结果 |
| 其他 | 失败 | 显示错误信息 |

## 笔记类型

| 类型 | 描述 |
|------|-------------|
| 1 | 文本笔记 |
| 2 | 大纲笔记 |
| 3 | 图文结合的笔记 |

## API

### 创建任务

**接口**：`POST /v2/tools/ai_note/task_create`

**参数**：
- `video_url`（必填）：公共视频 URL

**示例**：
```bash
python3 scripts/ai_notes_task_create.py 'https://example.com/video.mp4'
```

**响应**：
```json
{
  "task_id": "uuid-string"
}
```

### 查询任务

**接口**：`GET /v2/tools/ai_note/query`

**参数**：
- `task_id`（必填）：通过创建任务接口获得的任务 ID

**示例**：
```bash
python3 scripts/ai_notes_task_query.py "task-id-here"
```

**响应（任务完成时）**：
```json
{
  "status": 10002,
  "notes": [
    {
      "tpl_no": "1",
      "contents: ["Note content..."]
    }
  ]
}
```

## 查询策略

### 选项 1：手动查询
1. 创建任务 → 存储任务 ID
2. 每 3-5 秒查询一次任务状态：
   ```bash
   python3 scripts/ai_notes_task_query.py <task_id>
   ```
3. 显示进度更新：
   - 状态 10000：正在处理中...
   - 状态 10002：任务完成
4. 在 30-60 秒后停止查询（具体时间取决于视频长度）

### 选项 2：自动查询（推荐）
使用自动查询脚本来实时获取任务状态更新：

```bash
python3 scripts/ai_notes_poll.py <task_id> [max_attempts] [interval_seconds]
```

**示例**：
```bash
# Default: 20 attempts, 3-second intervals
python3 scripts/ai_notes_poll.py "task-id-here"

# Custom: 30 attempts, 5-second intervals
python3 scripts/ai_notes_poll.py "task-id-here" 30 5
```

**输出**：
- 显示实时进度：`[1/20] 正在处理中... 25%`
- 任务完成后自动停止
- 返回带有类型标签的格式化笔记

## 错误处理

- 无效的 URL：`视频 URL 无法访问`
- 处理错误：`无法解析视频文件`
- 超时：`视频文件过长，请稍后再试`