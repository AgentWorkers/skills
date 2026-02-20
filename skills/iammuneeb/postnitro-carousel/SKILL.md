---
name: postnitro-carousel
description: 使用 PostNitro.ai 的 Embed API 生成专业的社交媒体轮播图。该 API 支持基于 AI 的内容生成，同时也支持手动导入内容，适用于 LinkedIn、Instagram、TikTok 和 X（Twitter）等平台的轮播图。当用户需要创建轮播图、社交媒体帖子、幻灯片集，或者将文本、文章、博客帖子等内容转换为轮播图时，都可以使用此功能。此外，当用户希望自动化社交媒体内容的生成过程时，该 API 也能派上用场。生成的文件格式为 PNG 图像或 PDF 文件，使用前需要提供 PostNitro 的 API 密钥。
metadata:
  openclaw:
    emoji: "🎠"
    requires:
      envs:
        - POSTNITRO_API_KEY
        - POSTNITRO_TEMPLATE_ID
        - POSTNITRO_BRAND_ID
        - POSTNITRO_PRESET_ID
---
# PostNitro轮播图生成器

通过PostNitro.ai的嵌入API来创建社交媒体轮播图。提供两种工作流程：

- **AI生成**：提供主题、文章或文本，让AI生成轮播图内容。
- **内容导入**：用户提供自己的幻灯片内容，并可完全控制内容，包括信息图。

## 前提条件

设置以下环境变量：

1. `POSTNITRO_API_KEY`：从PostNitro.ai账户的“嵌入”设置中获取。
2. `POSTNITRO TEMPLATE_ID`：用户PostNitro账户中的轮播图模板ID。
3. `POSTNITRO_BRAND_ID`：用户PostNitro账户中的品牌配置ID。
4. `POSTNITRO_PRESET_ID`：（用于AI生成）用户PostNitro账户中的AI预设ID。

如果用户没有这些信息，请引导他们访问https://postnitro.ai进行注册（免费计划：每月5个信用点）。

## API概述

**基础URL**：`https://embed-api.postnitro.ai`

**身份验证**：所有请求都需要包含`embed-api-key: $POSTNITRO_API_KEY`头部信息。

**Content-Type**：`application/json`（用于POST请求）。

### 异步工作流程

所有轮播图的生成都是异步的：

1. **初始化**：`POST /post/initiate/generate` 或 `POST /post/initiate/import` → 返回 `embedPostId`
2. **检查状态**：`GET /post/status/{embedPostId}` → 持续检查直到状态变为`"COMPLETED"`
3. **获取结果**：`GET /post/output/{embedPostId}` → 下载完成的轮播图文件

---

## 端点1：AI生成

`POST /post/initiate/generate`

当用户提供主题、文章URL或文本，并希望AI生成轮播图内容时使用此端点。

### 请求体

| 字段 | 类型 | 是否必填 | 描述 | 允许的值 |
|-------|------|----------|-------------|----------------|
| `postType` | string | 是 | 文章类型 | `"CAROUSEL"` |
| `requestorId` | string | 否 | 自定义跟踪标识符 | 任意字符串 |
| `templateId` | string | 是 | 模板ID | 有效的模板ID |
| `brandId` | string | 是 | 品牌配置ID | 有效的品牌ID |
| `presetId` | string | 是 | AI配置预设ID | 有效的预设ID |
| `responseType` | string | 否 | 输出格式（默认："PDF"） | `"PDF"`, `"PNG"` |
| `aiGeneration` | object | 是 | AI生成配置 | 见下文 |

### aiGeneration对象

| 字段 | 类型 | 是否必填 | 描述 | 允许的值 |
|-------|------|----------|-------------|----------------|
| `type` | string | 是 | AI生成类型 | `"text"`, `"article"`, `"x"` |
| `context` | string | 是 | 对于 `"text"`：文本内容；对于 `"article"`：文章URL；对于 `"x"`：X（Twitter）帖子/线程URL | 任意字符串 |
| `instructions` | string | 否 | 额外的样式/语气说明 | 任意字符串 |

**`aiGeneration.type` 的值：**
- `"text"`：根据用户提供的文本内容生成
- `"article"`：根据文章URL生成
- `"x"`：根据X（Twitter）帖子或线程URL生成

### 示例（基于文本）

```bash
curl -X POST 'https://embed-api.postnitro.ai/post/initiate/generate' \
  -H 'Content-Type: application/json' \
  -H "embed-api-key: $POSTNITRO_API_KEY" \
  -d '{
    "postType": "CAROUSEL",
    "requestorId": "user123",
    "templateId": "'"$POSTNITRO_TEMPLATE_ID"'",
    "brandId": "'"$POSTNITRO_BRAND_ID"'",
    "presetId": "'"$POSTNITRO_PRESET_ID"'",
    "responseType": "PNG",
    "aiGeneration": {
      "type": "text",
      "context": "Digital marketing tips for small businesses: 1. Focus on local SEO 2. Use social proof 3. Start email marketing early",
      "instructions": "Focus on actionable tips that can be implemented immediately"
    }
  }'
```

### 示例（基于文章URL）

```bash
curl -X POST 'https://embed-api.postnitro.ai/post/initiate/generate' \
  -H 'Content-Type: application/json' \
  -H "embed-api-key: $POSTNITRO_API_KEY" \
  -d '{
    "postType": "CAROUSEL",
    "requestorId": "user123",
    "templateId": "'"$POSTNITRO_TEMPLATE_ID"'",
    "brandId": "'"$POSTNITRO_BRAND_ID"'",
    "presetId": "'"$POSTNITRO_PRESET_ID"'",
    "responseType": "PNG",
    "aiGeneration": {
      "type": "article",
      "context": "https://example.com/blog/digital-marketing-tips",
      "instructions": "Focus on actionable tips for small businesses"
    }
  }'
```

### 响应

```json
{
  "success": true,
  "message": "CAROUSEL generation initiated",
  "data": {
    "embedPostId": "post123",
    "status": "PENDING"
  }
}
```

**费用**：每张幻灯片2个信用点。

---

## 端点2：内容导入

`POST /post/initiate/import`

当用户提供自己的幻灯片内容时使用此端点。

### 请求体

| 字段 | 类型 | 是否必填 | 描述 | 允许的值 |
|-------|------|----------|-------------|----------------|
| `postType` | string | 是 | 文章类型 | `"CAROUSEL"` |
| `requestorId` | string | 否 | 自定义跟踪标识符 | 任意字符串 |
| `templateId` | string | 是 | 模板ID | 有效的模板ID |
| `brandId` | string | 是 | 品牌配置ID | 有效的品牌ID |
| `responseType` | string | 否 | 输出格式（默认："PDF"） | `"PDF"`, `"PNG"` |
| `slides` | array | 是 | 幻灯片对象数组 | 见下文 |

### 幻灯片结构

| 字段 | 类型 | 是否必填 | 描述 | 允许的值 |
|-------|------|----------|-------------|----------------|
| `type` | string | 是 | 幻灯片类型 | `"starting_slide"`, `"body_slide"`, `"ending_slide"` |
| `heading` | string | 是 | 主标题文本 | 任意字符串 |
| `sub_heading` | string | 否 | 子标题文本 | 任意字符串 |
| `description` | string | 否 | 描述文本 | 任意字符串 |
| `image` | string | 否 | 背景图片URL | 有效的URL |
| `background_image` | string | 否 | 背景图片URL | 有效的URL |
| `cta_button` | string | 否 | 呼叫行动按钮文本 | 任意字符串 |
| `layoutType` | string | 否 | 幻灯片布局类型 | `"default"`, `"infographics"` |
| `layoutConfig` | object | 否 | 信息图配置 | 见下文 |

### 幻灯片规则

- 必须有1张`starting_slide`。
- 至少有1张`body_slide`。
- 必须有1张`ending_slide`。

### 信息图布局

在`body_slide`上将`layoutType`设置为`"infographic"`，以用结构化数据替换图片区域。

**layoutConfig对象：**

| 字段 | 类型 | 是否必填 | 描述 | 允许的值 |
|-------|------|----------|-------------|----------------|
| `columnCount` | number | 是 | 列数 | `1`, `2`, `3` |
| `columnDisplay` | string | 是 | 列显示模式 | `"cycle"`, `"grid"` |
| `displayCounterAs` | string | 是 | 计数器显示方式 | `"none"`, `"counter"` |
| `hasHeader` | boolean | 是 | 是否显示列标题 | `true`, `false` |
| `columnData` | array | 否 | 列内容 | 见下文 |

**columnData项：**

| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `header` | string | 是 | 列标题文本 |
| `content` | array | 是 | 列内容数组 | `{"title": "...", "description": "..."}` |

**信息图注意事项：**
- `layoutType: "infographic"` 会用信息图替换幻灯片中的图片。
- 列数不得超过3。
- 循环显示（`"cycle"`）仅使用第一列的数据。
- 网格显示（`"grid"`）使用所有列的数据。

### 示例（默认幻灯片）

```bash
curl -X POST 'https://embed-api.postnitro.ai/post/initiate/import' \
  -H 'Content-Type: application/json' \
  -H "embed-api-key: $POSTNITRO_API_KEY" \
  -d '{
    "postType": "CAROUSEL",
    "templateId": "'"$POSTNITRO_TEMPLATE_ID"'",
    "brandId": "'"$POSTNITRO_BRAND_ID"'",
    "responseType": "PNG",
    "slides": [
      {
        "type": "starting_slide",
        "sub_heading": "My Awesome Subtitle",
        "heading": "Welcome to the Carousel!",
        "description": "This is how you start with a bang.",
        "cta_button": "Swipe to learn more"
      },
      {
        "type": "body_slide",
        "heading": "Section 1: The Core Idea",
        "description": "Explain your first key point here."
      },
      {
        "type": "body_slide",
        "heading": "Section 2: Deeper Dive",
        "description": "More details for the second point."
      },
      {
        "type": "ending_slide",
        "heading": "Get Started Today!",
        "sub_heading": "Ready to Act?",
        "description": "A final encouraging message.",
        "cta_button": "Visit Our Website"
      }
    ]
  }'
```

### 示例（包含信息图）

```bash
curl -X POST 'https://embed-api.postnitro.ai/post/initiate/import' \
  -H 'Content-Type: application/json' \
  -H "embed-api-key: $POSTNITRO_API_KEY" \
  -d '{
    "postType": "CAROUSEL",
    "templateId": "'"$POSTNITRO_TEMPLATE_ID"'",
    "brandId": "'"$POSTNITRO_BRAND_ID"'",
    "responseType": "PNG",
    "slides": [
      {
        "type": "starting_slide",
        "heading": "PostNitro Infographics",
        "sub_heading": "Import API Feature",
        "description": "Create stunning visual carousels with structured data."
      },
      {
        "type": "body_slide",
        "heading": "Grid Layout",
        "description": "Display data in an organized grid format.",
        "layoutType": "infographic",
        "layoutConfig": {
          "columnCount": 2,
          "columnDisplay": "grid",
          "displayCounterAs": "counter",
          "hasHeader": true,
          "columnData": [
            {
              "header": "Features",
              "content": [
                {"title": "Grid Display", "description": "Organized columns for comparison."},
                {"title": "Counter Support", "description": "Numbered items for sequence."}
              ]
            },
            {
              "header": "Options",
              "content": [
                {"title": "Column Headers", "description": "Enable/disable per column."},
                {"title": "Flexible Columns", "description": "Choose 1, 2, or 3 columns."}
              ]
            }
          ]
        }
      },
      {
        "type": "ending_slide",
        "heading": "Try PostNitro Infographics",
        "sub_heading": "Start Creating Today",
        "cta_button": "Get Your API Key"
      }
    ]
  }'
```

### 响应

```json
{
  "success": true,
  "message": "CAROUSEL generation initiated",
  "data": {
    "embedPostId": "post123",
    "status": "PENDING"
  }
}
```

**费用**：每张幻灯片1个信用点。

---

## 端点3：检查帖子状态

`GET /post/status/{embedPostId}`

无需请求体。将`embedPostId`作为路径参数传递。

**头部信息：`embed-api-key: $POSTNITRO_API_KEY`（必填）

```bash
curl -X GET "https://embed-api.postnitro.ai/post/status/$EMBED_POST_ID" \
  -H "embed-api-key: $POSTNITRO_API_KEY"
```

### 响应

```json
{
  "success": true,
  "data": {
    "embedPostId": "post123",
    "embedPost": {
      "id": "post123",
      "postType": "CAROUSEL",
      "status": "COMPLETED",
      "createdAt": "2024-01-15T10:30:00Z",
      "updatedAt": "2024-01-15T10:35:00Z"
    },
    "logs": [
      {
        "id": "log1",
        "embedPostId": "post123",
        "step": "INITIATED",
        "status": "SUCCESS",
        "message": "Post generation initiated",
        "timestamp": "2024-01-15T10:30:00Z"
      },
      {
        "id": "log2",
        "embedPostId": "post123",
        "step": "PROCESSING",
        "status": "SUCCESS",
        "message": "Content generated successfully",
        "timestamp": "2024-01-15T10:32:00Z"
      },
      {
        "id": "log3",
        "embedPostId": "post123",
        "step": "COMPLETED",
        "status": "SUCCESS",
        "message": "Post generation completed",
        "timestamp": "2024-01-15T10:35:00Z"
      }
    ]
  }
}
```

每3-5秒检查一次状态。通过`data.embedPost.status`查看进度。`logs`数组提供详细的进度信息。

---

## 端点4：获取结果

`GET /post/output/{embedPostId}`

无需请求体。将`embedPostId`作为路径参数传递。

**头部信息：`embed-api-key: $POSTNITRO_API_KEY`（必填）

```bash
curl -X GET "https://embed-api.postnitro.ai/post/output/$EMBED_POST_ID" \
  -H "embed-api-key: $POSTNITRO_API_KEY"
```

### 响应（PNG格式）

```json
{
  "success": true,
  "data": {
    "embedPost": {
      "id": "post123",
      "postType": "CAROUSEL",
      "responseType": "PNG",
      "status": "COMPLETED",
      "credits": 4,
      "createdAt": "2026-02-19T21:11:50.115Z",
      "updatedAt": "2026-02-19T21:12:08.333Z"
    },
    "result": {
      "id": "result123",
      "name": "Welcome to the Carousel!",
      "size": {
        "id": "4:5",
        "dimensions": { "width": 1080, "height": 1350 }
      },
      "type": "png",
      "mimeType": "image/png",
      "data": [
        "https://...supabase.co/.../slide_0.png",
        "https://...supabase.co/.../slide_1.png"
      ]
    }
  }
}
```

### 响应（PDF格式）

```json
{
  "success": true,
  "data": {
    "embedPost": {
      "id": "post123",
      "postType": "CAROUSEL",
      "responseType": "PDF",
      "status": "COMPLETED",
      "credits": 10,
      "createdAt": "2026-02-19T21:11:50.115Z",
      "updatedAt": "2026-02-19T21:12:08.333Z"
    },
    "result": {
      "id": "result123",
      "name": "Welcome to the Carousel!",
      "size": {
        "id": "4:5",
        "dimensions": { "width": 1080, "height": 1350 }
      },
      "type": "pdf",
      "mimeType": "application/pdf",
      "data": "https://...supabase.co/.../output.pdf"
    }
  }
}
```

### 结果对象

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `id` | string | 唯一的结果标识符 |
| `name` | string | 设计名称（来自模板或“Untitled”） |
| `size` | object | `{ "id": "4:5", "dimensions": { "width": 1080, "height": 1350 } }` |
| `type` | string | 文件类型（`"png"` 或 `"pdf"`） |
| `mimeType` | string | MIME类型（`"image/png"` 或 `"application/pdf"`） |
| `data` | string 或 array | **PNG**：幻灯片URL数组；**PDF**：单个URL |

直接下载这些URL以保存轮播图文件。

---

## 分步使用方法

### AI生成的轮播图

1. 确保已设置`POSTNITRO_API_KEY`、`POSTNITRO TEMPLATE_ID`、`POSTNITRO_BRAND_ID`和`POSTNITRO_PRESET_ID`。
2. 询问用户所需的生成类型（`text`、`article`或`x`），以及相应的内容（文本、文章URL或X帖子URL）和任何样式要求。
3. 向`POST /post/initiate/generate`发送生成请求。
4. 从响应中提取`embedPostId`。
5. 每3-5秒检查一次`GET /post/status/{embedPostId}`，直到状态变为`"COMPLETED"`。
6. 调用`GET /post/output/{embedPostId}`获取结果，并从`data`中下载URL以保存文件。

### 自定义内容轮播图

1. 确保已设置`POSTNITRO_API_KEY`、`POSTNITRO TEMPLATE_ID`和`POSTNITRO_BRAND_ID`。
2. 收集用户的幻灯片内容。结构应为：1张`starting_slide` → 多张`body_slide` → 1张`ending_slide`。
3. 对于包含大量数据的幻灯片，使用`layoutType: "infographic"`并设置`layoutConfig`对象。
4. 向`POST /post/initiate/import`发送导入请求。
5. 按照相同的流程检查状态并获取结果。

## 内容策略建议

- **LinkedIn**：专业风格，提供可操作的见解，6-10张幻灯片，清晰的呼叫行动按钮。
- **Instagram**：以视觉内容为主，简洁的文字，5-8张幻灯片，具有故事情节。
- **TikTok**：时尚、简洁，4-7张幻灯片，第一张幻灯片要吸引注意力。
- **X（Twitter）**：以数据驱动，3-6张幻灯片，开头要有吸引力。

## 错误处理

- 如果API返回身份验证错误，请确认`POSTNITRO_API_KEY`是否正确以及账户是否处于活跃状态。
- 如果信用点用完，请通知用户。免费计划：每月5个信用点。付费计划：每月250个以上信用点（每月10美元）。
- 如果状态检查显示失败，请在报告错误前重试一次初始化操作。
- 所有端点都受到API密钥的速率限制——请适当控制请求频率。
- 默认的`responseType`是`"PDF"`。如果需要单独的幻灯片图片，请明确指定`"PNG"`。

## 链接

- 文档：https://postnitro.ai/docs/embed/api
- 获取API密钥：https://postnitro.ai/app/embed
- Postman集合：https://www.postman.com/postnitro/postnitro-embed-apis/overview
- 支持：support@postnitro.ai