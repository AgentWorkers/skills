---
name: renderkit
version: "1.3.5"
description: 使用 RenderKit API，将结构化数据渲染成美观的托管网页，并创建用于数据收集的托管表单。该功能适用于生成可视化页面、调查问卷、回复确认表单、反馈表单或任何其他结构化数据的应用场景。
metadata:
  openclaw:
    requires:
      env:
        - RENDERKIT_API_KEY
      bins:
        - curl
    primaryEnv: RENDERKIT_API_KEY
    homepage: https://renderkit.live
---

# RenderKit 技能

RenderKit 可将结构化数据渲染成美观的托管网页，并创建用于数据收集的托管表单。

## 设置

1. 在 [https://renderkit.live](https://renderkit.live) 注册以获取您的 API 密钥。
2. 设置您的环境变量：

```bash
export RENDERKIT_API_KEY="your-api-key"
```

## 使用方法

所有命令均通过 `curl` 发送到 RenderKit API。请选择正确的接口端点：

- **只读页面**（结果、摘要、对比、行程安排）→ `POST /v1/render`
- **数据收集**（表单、调查问卷、回复、注册、反馈）→ `POST /v1/forms`

### 创建页面

```bash
curl -s -X POST https://renderkit.live/v1/render \
  -H "Authorization: Bearer $RENDERKIT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "template": "freeform",
    "context": "brief description of what this content is",
    "data": {
      "title": "Page Title",
      "content": "your data here — markdown, structured objects, anything"
    }
  }'
```

返回 `url`、`slug` 和 `render_id`。模板选项：`freeform`（由 AI 自动选择布局）或 `travel_itinerary`。

### 更新页面

```bash
curl -s -X PATCH https://renderkit.live/v1/render/{render_id} \
  -H "Authorization: Bearer $RENDERKIT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "strategy": "merge",
    "context": "updated description",
    "data": { "content": "new or additional data" }
  }'
```

更新方式有两种：`merge`（添加新内容）或 `replace`（完全重写页面内容）。页面的 URL 保持不变。

### 检查页面状态

```bash
curl -s https://renderkit.live/v1/render/{render_id}/status \
  -H "Authorization: Bearer $RENDERKIT_API_KEY"
```

### 创建表单

```bash
curl -s -X POST https://renderkit.live/v1/forms \
  -H "Authorization: Bearer $RENDERKIT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Event RSVP",
    "prompt": "Create an RSVP form for a dinner party. Ask for name, email, dietary restrictions, and plus-one.",
    "multi_response": true,
    "expires_in": 604800
  }'
```

系统会返回一个可供受访者使用的 `url`。您也可以指定具体的 `fields`（表单字段）。

### 获取表单回复

```bash
curl -s https://renderkit.live/v1/forms/{form_id}/responses \
  -H "Authorization: Bearer $RENDERKIT_API_KEY"
```

### 关闭表单

```bash
curl -s -X DELETE https://renderkit.live/v1/forms/{form_id} \
  -H "Authorization: Bearer $RENDERKIT_API_KEY"
```

## 注意事项

- **严禁使用 `/v1/render` 来伪造表单**——该接口会生成无法收集回复的静态页面。
- 请在数据中直接嵌入页面 URL，因为这些 URL 会自动添加图片、评分和元数据。
- 可选参数：`"theme": { "mode": "dark", "palette": ["#color1", "#color2"] }` 用于设置页面主题。
- 更新操作（PATCH 请求）是免费的，且不会占用您的 API 使用量。
- 如果您之前已经生成了相关页面，后续修改建议使用 `PATCH` 而不是 `POST`。
- 完整的 API 文档请参阅：[https://renderkit.live/docs.md](https://renderkit.live/docs.md)

## 示例

```bash
# Create a travel itinerary page
curl -s -X POST https://renderkit.live/v1/render \
  -H "Authorization: Bearer $RENDERKIT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"template":"travel_itinerary","context":"3-day Paris trip","data":{"title":"Paris Weekend","content":"Day 1: Louvre, lunch at Loulou, Seine walk. Day 2: Montmartre, Sacré-Cœur."}}'

# Create a feedback survey
curl -s -X POST https://renderkit.live/v1/forms \
  -H "Authorization: Bearer $RENDERKIT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title":"Team Feedback","prompt":"Create a short feedback form with rating (1-5) and open comments","multi_response":true}'

# Check for new form submissions
curl -s https://renderkit.live/v1/forms/{form_id}/status \
  -H "Authorization: Bearer $RENDERKIT_API_KEY"
```