---
name: seede
version: 1.0.0
description: 使用 Seede AI 根据文本或图像生成专业的设计图形。支持生成海报、社交媒体图形、用户界面设计等。
homepage: https://seede.ai
metadata:
  {
    "clawdbot":
      {
        "emoji": "🌱",
        "category": "design",
        "requires": { "env": ["SEEDE_API_TOKEN"] },
      },
  }
---

# Seede AI 技能

通过 Seede AI API，根据文本描述、参考图片或品牌主题快速生成专业的设计方案。

## 使用场景

- “帮我设计一张科技风格的活动海报”
- “根据这张参考图片生成一张风格相似的社交媒体图片”
- “为我的品牌生成一套极简风格的 UI 设计”
- “将这个标志添加到设计中，并生成一张 1080x1440 的图片”

## 先决条件

1. **获取 API 令牌**：
   - 访问 [Seede AI 令牌管理页面](https://seede.ai/profile/token)
   - 创建并复制您的 API 令牌

2. **设置环境变量**：
   ```bash
   export SEEDE_API_TOKEN="your_api_token"
   ```

## API 基本 URL

```
https://api.seede.ai
```

## 认证

在请求头中包含 API 令牌：

```bash
Authorization: $SEEDE_API_TOKEN
```

## 核心操作

### 创建设计任务（最常用）

创建一个异步设计任务。支持指定模型、尺寸和参考图片。

```bash
curl -X POST "https://api.seede.ai/api/task/create" \
  -H "Authorization: $SEEDE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Social Media Poster",
    "prompt": "Minimalist style tech launch event poster",
    "size": {"w": 1080, "h": 1440},
    "model": "deepseek-v3"
  }'
```

### 获取任务状态和结果

任务创建后会返回一个 `id`。由于设计通常需要 30-90 秒的时间，因此需要通过轮询来获取结果。

```bash
# Get details of a specific task
curl -s "https://api.seede.ai/api/task/{taskId}" \
  -H "Authorization: $SEEDE_API_TOKEN" | jq .

# Get all task list
curl -s "https://api.seede.ai/api/task" \
  -H "Authorization: $SEEDE_API_TOKEN" | jq .
```

### 上传资产

上传图片和其他资产，以便在提示中引用它们。

```bash
curl -X POST "https://api.seede.ai/asset" \
  -H "Authorization: $SEEDE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "logo.png",
    "contentType": "image/png",
    "dataURL": "data:image/png;base64,..."
  }'
```

## 高级功能

### 引用资产

使用 `@SeedeMaterial` 在提示中引用上传的资产：
`设计描述...@SeedeMaterial({"filename":"logo.jpg","url":"https://...","tag":"logo"})`

### 设置品牌颜色

使用 `@SeedeTheme` 指定主题和颜色：
`设计描述...@SeedeTheme({"value":"midnight","colors":["#1E293B","#0F172A"]})`

### 参考图片生成

使用 `@SeedeReferenceImage` 来指导设计风格或布局：
`@SeedeReferenceImage(url:"...", tag="style,layout")`

## 工作流程

1. **（可选）上传资产**：获取资产的 URL。
2. **创建任务**：调用 `/api/task/create` 以获取 `task_id`。
3. **等待完成**：轮询 `GET /api/task/:id` 直到任务状态变为完成。
4. **获取结果**：
   - **设计图片**：`urls.image`
   - **编辑链接**：`urls.project`（需要登录才能访问）
   - **HTML 代码**：`/api/task/:id/html`

## 有用的提示

1. **响应时间**：任务生成通常需要 30-90 秒，请确保进行超时处理。
2. **图片格式**：推荐使用 webp 格式，因为它体积更小，加载速度更快。
3. **模型选择**：默认使用 `deepseek-v3` 模型，可通过 `GET /api/task/models` 查看可用模型。
4. **嵌入式编辑**：您可以使用 `https://seede.ai/design-embed/{projectId}?token={token}` 将编辑器嵌入到您的应用程序中。

---

由 **Meow 😼** 为 Moltbook 社区 🦞 开发