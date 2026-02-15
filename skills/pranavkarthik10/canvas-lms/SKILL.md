---
name: canvas-lms
description: 访问 Canvas LMS（Instructure）以获取课程数据、作业、成绩以及提交情况。该工具可用于查看截止日期、成绩、课程列表，或从 Canvas 下载课程材料。
---

# Canvas LMS 技能

通过 REST API 访问 Canvas LMS 的数据。

## 设置

1. 在 Canvas 中生成 API 令牌：账户 → 设置 → 新访问令牌
2. 将令牌存储在环境变量或 `.env` 文件中：
   ```bash
   export CANVAS_TOKEN="your_token_here"
   export CANVAS_URL="https://your-school.instructure.com"  # or canvas.yourschool.edu
   ```

## 认证

在所有请求中包含令牌：
```bash
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" "$CANVAS_URL/api/v1/..."
```

## 常用端点

### 课程与个人资料
```bash
# User profile
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" "$CANVAS_URL/api/v1/users/self/profile"

# Active courses
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" "$CANVAS_URL/api/v1/courses?enrollment_state=active&per_page=50"

# Dashboard cards (quick overview)
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" "$CANVAS_URL/api/v1/dashboard/dashboard_cards"
```

### 作业与截止日期
```bash
# To-do items (upcoming work)
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" "$CANVAS_URL/api/v1/users/self/todo"

# Upcoming events
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" "$CANVAS_URL/api/v1/users/self/upcoming_events"

# Missing/overdue submissions
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" "$CANVAS_URL/api/v1/users/self/missing_submissions"

# Course assignments
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" "$CANVAS_URL/api/v1/courses/{course_id}/assignments?per_page=50"

# Assignment details
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" "$CANVAS_URL/api/v1/courses/{course_id}/assignments/{id}"

# Submission status
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" "$CANVAS_URL/api/v1/courses/{course_id}/assignments/{id}/submissions/self"
```

### 成绩
```bash
# Enrollments with scores
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" "$CANVAS_URL/api/v1/users/self/enrollments?include[]=current_grading_period_scores&per_page=50"
```
获取成绩：`.grades.current_score`

### 课程内容
```bash
# Announcements
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" "$CANVAS_URL/api/v1/announcements?context_codes[]=course_{course_id}&per_page=20"

# Modules
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" "$CANVAS_URL/api/v1/courses/{course_id}/modules?include[]=items&per_page=50"

# Files
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" "$CANVAS_URL/api/v1/courses/{course_id}/files?per_page=50"

# Discussion topics
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" "$CANVAS_URL/api/v1/courses/{course_id}/discussion_topics?per_page=50"

# Inbox
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" "$CANVAS_URL/api/v1/conversations?per_page=20"
```

## 响应处理

- 列表端点返回数组
- 分页：检查 `Link` 头部的 `rel="next"` 字段
- 日期采用 ISO 8601 格式（UTC）
- 对于响应速度较慢的端点，可以使用 `--max-time 30` 参数

使用 jq 进行解析：
```bash
curl -s ... | jq '.[] | {name: .name, due: .due_at}'
```

如果无法使用 jq，也可以使用 Python 进行解析：
```bash
curl -s ... | python3 -c "import sys,json; data=json.load(sys.stdin); print(json.dumps(data, indent=2))"
```

## 提示

- 课程 ID 会出现在待办事项/作业的响应中
- 文件下载地址位于文件对象的 `url` 字段中
- 为获取更多结果，请始终添加 `per_page=50` 参数（默认值通常为 10）