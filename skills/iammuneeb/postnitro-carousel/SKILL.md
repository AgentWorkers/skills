---
name: postnitro-carousel
description: >
  Generate professional social media carousel posts using the PostNitro.ai Embed API.
  Supports AI-powered content generation and manual content import for LinkedIn, Instagram,
  TikTok, and X (Twitter) carousels. Use this skill whenever the user wants to create a
  carousel, social media post, slide deck for social media, multi-slide content, or
  mentions PostNitro. Also trigger when the user asks to turn text, articles, blog posts,
  or topics into carousel posts, or wants to automate social media content creation.
  Outputs PNG images or PDF files. Requires a PostNitro API key.
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

通过PostNitro.ai的嵌入API（Embed API）创建精美的社交媒体轮播图。支持两种工作流程：**人工智能生成**（提供主题，让AI生成内容）和**内容导入**（提供自己的幻灯片内容并完全控制生成过程）。

## 先决条件

用户必须设置以下环境变量：

1. `POSTNITRO_API_KEY` — 从PostNitro.ai账户的“嵌入”（Embed）设置中获取。
2. `POSTNITRO TEMPLATE_ID` — 从他们的PostNitro账户中选择的轮播图模板的ID。
3. `POSTNITRO_BRAND_ID` — 从他们的PostNitro账户中选择的品牌ID。
4. `POSTNITRO_PRESET_ID` — （用于人工智能生成）在PostNitro账户中配置的人工智能预设ID。

如果用户没有这些信息，请引导他们访问https://postnitro.ai进行注册（免费计划每月提供5个信用点）。

## API参考

**基础URL**：`https://embed-api.postnitro.ai`

**身份验证**：所有请求都需要包含`embed-api-key: $POSTNITRO_API_KEY`头部信息。

**Content-Type**：始终为`application/json`。

### 工作流程概述

所有轮播图的创建都是异步的：

1. **初始化** — 调用`/post/initiate/generate`或`/post/initiate/import` → 接收`embedPostId`。
2. **查询状态** — 使用`embedPostId`调用`/post/request-status`，直到状态显示为“完成”。
3. **获取结果** — 使用`embedPostId`调用`/post/output`下载生成的轮播图内容。

### 端点1：人工智能生成

`POST /post/initiate/generate`

当用户提供主题、文章URL或文本，并希望AI生成轮播图内容时使用此端点。

```json
{
  "postType": "CAROUSEL",
  "templateId": "<template-id>",
  "brandId": "<brand-id>",
  "presetId": "<ai-preset-id>",
  "responseType": "PNG",
  "aiGeneration": {
    "type": "<generation-type>",
    "context": "<topic, text, or article URL>",
    "instructions": "<optional style/tone instructions>"
  }
}
```

**`aiGeneration.type` 的取值：**
- `"text"` — 从用户提供的文本生成内容。
- `"article"` — 从文章URL或长篇内容生成内容。
- `"topic"` — 从主题描述生成内容。

**`responseType` 的取值：**
- `"PNG"` — 每张幻灯片为单独的图片（适合社交媒体发布）。
- `"PDF"` — 包含所有幻灯片的单个PDF文档。

**费用**：每张幻灯片2个信用点（人工智能生成）。

### 端点2：内容导入

`POST /post/initiate/import`

当用户提供自己的幻灯片内容（标题、描述、图片）时使用此端点。

```json
{
  "postType": "CAROUSEL",
  "templateId": "<template-id>",
  "brandId": "<brand-id>",
  "requestorId": "<optional-tracking-id>",
  "responseType": "PNG",
  "slides": [
    {
      "type": "starting_slide",
      "heading": "Title Text",
      "sub_heading": "Subtitle Text",
      "description": "Description text",
      "cta_button": "Call to Action",
      "image": "https://example.com/image.jpg",
      "background_image": "https://example.com/bg.jpg"
    },
    {
      "type": "body_slide",
      "heading": "Slide Heading",
      "description": "Slide body text",
      "image": "https://example.com/image.jpg"
    },
    {
      "type": "ending_slide",
      "heading": "Final Slide Title",
      "sub_heading": "Closing Subtitle",
      "description": "Closing message",
      "cta_button": "Take Action",
      "image": "https://example.com/logo.png",
      "background_image": "https://example.com/bg.jpg"
    }
  ]
}
```

**幻灯片类型：**
- `"starting_slide"` — 第一张幻灯片（标题/介绍）。支持：`heading`（标题）、`sub_heading`（子标题）、`description`（描述）、`cta_button`（呼叫行动按钮）、`image`（图片）、`background_image`（背景图片）。
- `"body_slide"` — 中间内容幻灯片。支持：`heading`（标题）、`description`（描述）、`image`（图片）。
- `"ending_slide"` — 最后一张幻灯片（呼叫行动按钮/结尾）。支持：`heading`（标题）、`sub_heading`（子标题）、`description`（描述）、`cta_button`（呼叫行动按钮）、`image`（图片）、`background_image`（背景图片）。

所有幻灯片字段都是可选的。使用`image`设置前景图片，使用`background_image`设置幻灯片背景。图片链接必须是公开可访问的。

**费用**：每张幻灯片1个信用点（用户提供的内容）。

### 端点3：查询请求状态

`POST /post/request-status`

```json
{
  "embedPostId": "<post-id-from-initiate-response>"
}
```

每隔3–5秒查询一次此端点，直到收到请求完成的响应。

### 端点4：获取结果

`POST /post/output`

```json
{
  "embedPostId": "<post-id-from-initiate-response>"
}
```

返回生成的轮播图内容。对于PNG格式，返回一个包含所有幻灯片URL的数组；对于PDF格式，返回一个包含所有幻灯片的单个文档。

## 分步使用方法

### 创建人工智能生成的轮播图

1. 确认用户已设置`POSTNITRO_API_KEY`、`POSTNITRO TEMPLATE_ID`、`POSTNITRO_BRAND_ID`和`POSTNITRO_PRESET_ID`。
2. 询问用户所需的主题/内容及任何样式偏好。
3. 发送生成请求：
   ```bash
   curl -X POST 'https://embed-api.postnitro.ai/post/initiate/generate' \
     -H 'Content-Type: application/json' \
     -H "embed-api-key: $POSTNITRO_API_KEY" \
     -d '{
       "postType": "CAROUSEL",
       "templateId": "'"$POSTNITRO_TEMPLATE_ID"'",
       "brandId": "'"$POSTNITRO_BRAND_ID"'",
       "presetId": "'"$POSTNITRO_PRESET_ID"'",
       "responseType": "PNG",
       "aiGeneration": {
         "type": "topic",
         "context": "User topic here",
         "instructions": "User style instructions here"
       }
     }'
   ```
4. 从响应中提取`embedPostId`。
5. 持续查询状态，直到生成完成：
   ```bash
   curl -X POST 'https://embed-api.postnitro.ai/post/request-status' \
     -H 'Content-Type: application/json' \
     -H "embed-api-key: $POSTNITRO_API_KEY" \
     -d '{"embedPostId": "'"$EMBED_POST_ID"'"}'
   ```
6. 获取生成的轮播图内容：
   ```bash
   curl -X POST 'https://embed-api.postnitro.ai/post/output' \
     -H 'Content-Type: application/json' \
     -H "embed-api-key: $POSTNITRO_API_KEY" \
     -d '{"embedPostId": "'"$EMBED_POST_ID"'"}'
   ```

### 使用用户内容创建轮播图

1. 确认用户已设置`POSTNITRO_API_KEY`、`POSTNITRO TEMPLATE_ID`和`POSTNITRO_BRAND_ID`。
2. 从用户处收集幻灯片内容（或根据需求生成内容）。
3. 按照“starting_slide” → “body_slide”（多个中间幻灯片） → “ending_slide”的顺序组织幻灯片。
4. 发送导入请求，并按照上述流程查询状态和获取结果。

## 内容策略建议

在帮助用户制作轮播图内容时，请注意以下要点：

- **LinkedIn**：采用专业的语气，提供实用的见解，6–10张幻灯片，以明确的呼叫行动按钮结束。
- **Instagram**：以视觉内容为主，文字简洁，5–8张幻灯片，具有连贯的故事情节。
- **TikTok**：内容要时尚、简洁，4–7张幻灯片，第一张幻灯片要吸引注意力。
- **X（Twitter）**：以数据为基础，3–6张幻灯片，开头要有吸引力。

## 错误处理

- 如果API返回身份验证错误，请检查`POSTNITRO_API_KEY`是否正确以及账户是否处于活跃状态。
- 如果信用点用完，请通知用户。免费计划每月提供5个信用点；付费计划每月提供250个以上信用点。
- 如果状态查询显示失败，请在报告错误前重新尝试初始化请求一次。
- 所有端点的请求次数都受到API密钥的限制，请合理分配请求次数。

## 价格快速参考

| 计划        | 价格        | 每月信用点数      | 备注                          |
|-------------|------------|--------------|--------------------------------|
| 免费        | $0/month     | 5             | API密钥生成时默认使用此计划           |
| 月度计划     | $10/month     | 250+          | 可扩展（1–100个信用点）                 |
|            |             |                |                                  |

- 1个信用点 = 1张幻灯片（用户提供的内容）。
- 人工智能生成：每张幻灯片2个信用点。

## 链接

- 文档：https://postnitro.ai/docs/embed/api
- 获取API密钥：https://postnitro.ai/app/embed
- Postman集合：https://www.postman.com/postnitro/postnitro-embed-apis/overview
- 技术支持：support@postnitro.ai