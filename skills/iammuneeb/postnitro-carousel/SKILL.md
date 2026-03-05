---
name: postnitro-carousel
description: 使用 PostNitro.ai 的 Embed API 生成专业的社交媒体轮播图。该 API 支持基于 AI 的内容生成，同时也支持手动导入内容，适用于 LinkedIn、Instagram、TikTok 和 X（Twitter）等平台的轮播图。当用户需要创建轮播图、社交媒体帖子、幻灯片展示（用于社交媒体）、多页内容，或提及 PostNitro 时，都可以使用此功能。此外，当用户希望将文本、文章、博客文章或主题转换为轮播图，或者希望自动化社交媒体内容的生成时，也可以使用该 API。输出格式为 PNG 图像或 PDF 文件。使用此功能需要 PostNitro 的 API 密钥。
homepage: https://postnitro.ai
metadata: {"openclaw":{"emoji":"🎠","primaryEnv":"POSTNITRO_API_KEY","requires":{"env":["POSTNITRO_API_KEY","POSTNITRO_TEMPLATE_ID","POSTNITRO_BRAND_ID","POSTNITRO_PRESET_ID"]}}}
---
# PostNitro轮播图生成器

通过PostNitro.ai的嵌入API生成社交媒体轮播图。提供两种工作流程：**AI生成**（将文本、文章或X平台（Twitter）帖子转换为轮播图）和**内容导入**（使用用户自己的幻灯片，支持可选的信息图）。

## 设置

1. 在https://postnitro.ai注册（免费计划：每月5个信用点）。
2. 进入账户设置 → “嵌入” → 生成API密钥。
3. 在PostNitro控制台中设置模板、品牌和AI预设。
4. 设置环境变量：
   ```bash
   export POSTNITRO_API_KEY="your-api-key"
   export POSTNITRO_TEMPLATE_ID="your-template-id"
   export POSTNITRO_BRAND_ID="your-brand-id"
   export POSTNITRO_PRESET_ID="your-ai-preset-id"
   ```

基础URL：`https://embed-api.postnitro.ai`
认证头：`embed-api-key: $POSTNITRO_API_KEY`

## 核心工作流程

所有轮播图的生成都是异步的：**初始化 → 检查状态 → 获取结果**。

### 1. 使用AI生成轮播图

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
      "type": "text",
      "context": "5 tips for growing your LinkedIn audience in 2026",
      "instructions": "Professional tone, actionable advice"
    }
  }'
```

返回结果：`{"success": true, "data": { "embedPostId": "post123", "status": "PENDING" }`。保存`embedPostId`。

**`aiGeneration.type` 的取值：**
- `"text"`：输入的文本内容将被转换为轮播图。
- `"article"`：输入的文章URL将被提取并转换。
- `"x"`：输入的X平台（Twitter）帖子或话题链接。

参见[examples/generate-from-text.json](examples/generate-from-text.json)、[examples/generate-from-article.json]和[examples/generate-from-x-post.json]示例文件。

### 2. 导入用户自己的幻灯片内容

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
      { "type": "starting_slide", "heading": "Your Title", "description": "Intro text" },
      { "type": "body_slide", "heading": "Key Point", "description": "Details here" },
      { "type": "ending_slide", "heading": "Take Action!", "cta_button": "Learn More" }
    ]
  }'
```

返回与上述相同的响应格式，其中包含`embedPostId`。

**幻灯片规则：**
- 必须有1张**起始幻灯片**。
- 必须有至少1张**正文幻灯片**。
- 必须有1张**结束幻灯片**。
- 每张幻灯片都必须包含`heading`（标题）。

**幻灯片字段：**`heading`（标题）、`sub_heading`（副标题）、`description`（描述）、`image`（图片URL）、`background_image`（背景图片URL）、`cta_button`（呼叫行动按钮）、`layoutType`（布局类型）、`layoutConfig`（布局配置）。

对于信息图幻灯片，在正文幻灯片上设置`layoutType: "infographic"`——这将用结构化的数据列替换图片。详细信息请参阅[examples/import-infographics.json](examples/import-infographics.json)和[references/api-reference.md]。

### 3. 检查帖子状态

```bash
curl -X GET "https://embed-api.postnitro.ai/post/status/$EMBED_POST_ID" \
  -H "embed-api-key: $POSTNITRO_API_KEY"
```

每隔3–5秒检查一次状态，直到`data.embedPost.status`变为`"COMPLETED"`。`logs`数组会显示生成过程的详细步骤。

### 4. 获取结果

```bash
curl -X GET "https://embed-api.postnitro.ai/post/output/$EMBED_POST_ID" \
  -H "embed-api-key: $POSTNITRO_API_KEY"
```

在`data.result.data`中返回可下载的URL：
- **PNG格式**：每张幻灯片对应的URL列表。
- **PDF格式**：单个PDF文件链接。

详细响应格式请参阅[references/api-reference.md]。

## 常见用法示例

### 示例1：LinkedIn思想领导力轮播图

使用专业风格的内容生成LinkedIn轮播图：

```json
{
  "aiGeneration": {
    "type": "text",
    "context": "5 mistakes startups make with their LinkedIn strategy and how to fix each one",
    "instructions": "Professional but conversational tone. Each slide should have one clear takeaway."
  }
}
```

### 示例2：重新利用博客文章

将现有文章转换为轮播图：

```json
{
  "aiGeneration": {
    "type": "article",
    "context": "https://yourblog.com/posts/social-media-strategy-2026",
    "instructions": "Extract the 5 most actionable points. Keep slide text concise."
  }
}
```

### 示例3：重新利用X平台（Twitter）话题帖子

将热门的X平台话题帖子转换为视觉轮播图：

```json
{
  "aiGeneration": {
    "type": "x",
    "context": "https://x.com/username/status/1234567890",
    "instructions": "Maintain the original voice and key points"
  }
}
```

### 示例4：数据驱动的信息图轮播图

导入具有结构化布局的信息图幻灯片：

详细示例请参阅[examples/import-infographics.json]（包含网格和循环布局）。

## 内容策略建议

- **LinkedIn**：采用专业风格，提供可操作的见解，6–10张幻灯片，包含明确的呼叫行动按钮。
- **Instagram**：以视觉内容为主，文字简洁，5–8张幻灯片，具有故事情节。
- **TikTok**：内容时尚、简洁，4–7张幻灯片，第一张幻灯片要吸引观众注意力。
- **X平台（Twitter）**：以数据为基础，3–6张幻灯片，开头具有吸引力。

## 常见问题

1. **默认响应格式为PDF**——如果需要单独的幻灯片图片，请务必明确指定`"PNG"`。
2. **每张幻灯片都必须包含`heading`——缺少`heading`会导致错误。
3. **幻灯片结构严格**：必须有1张起始幻灯片、至少1张正文幻灯片和1张结束幻灯片。
- **文章类型需要URL**——`"article"`类型需要文章的URL作为输入内容，而不是纯文本。
- **X平台类型需要帖子链接**——`"x"`类型需要`https://x.com/...`或`https://twitter.com/...`形式的帖子链接。
- **信息图会替换图片**——设置`layoutType: "infographic"`后，该幻灯片上的图片将被信息图替代。
- **循环信息图仅使用第一列数据**——`columnDisplay: "cycle"`会忽略第二列及以后的数据。
- **最多3列**——信息图布局的`columnCount`不能超过3。
- **图片URL必须是公开的**——`image`和`background_image`字段需要可公开访问的URL。
- **费用因方法而异**：AI生成每张幻灯片费用为2个信用点，内容导入每张幻灯片费用为1个信用点。

## 费用与定价

| 计划 | 价格 | 每月信用点数 |
|------|-------|---------------|
| 免费 | $0 | 5 |
| 月度计划 | $10 | 250+（可扩展） |

- 内容导入：每张幻灯片1个信用点。
- AI生成：每张幻灯片2个信用点。

## 支持资源

**参考文档：**
- [references/api-reference.md] — 完整的API端点参考，包含请求/响应格式和信息图配置。

**现成的示例：**
- [examples/EXAMPLES.md] — 所有示例的索引。
- [examples/generate-from-text.json] — 从文本生成轮播图的示例。
- [examples/generate-from-article.json] — 从文章URL生成轮播图的示例。
- [examples/generate-from-x-post.json] — 从X平台帖子生成轮播图的示例。
- [examples/import-default.json] — 基本的幻灯片导入示例。
- [examples/import-infographics.json] — 使用信息图布局的导入示例。

## 快速参考

```
# Auth
Header: embed-api-key: $POSTNITRO_API_KEY

# AI generation
POST /post/initiate/generate  { postType, templateId, brandId, presetId, responseType?, requestorId?, aiGeneration: { type, context, instructions? } }

# Content import
POST /post/initiate/import  { postType, templateId, brandId, responseType?, requestorId?, slides: [{ type, heading, ... }] }

# Check status (poll until COMPLETED)
GET /post/status/{embedPostId}

# Get output (download URLs)
GET /post/output/{embedPostId}
```

## 给开发者的建议

- 在调用任何API端点之前，务必确认用户已设置`POSTNITRO_API_KEY`、`POSTNITRO_TEMPLATE_ID`和`POSTNITRO_BRAND_ID`。
- `POSTNITRO_PRESET_ID`仅用于AI生成，不适用于内容导入。
- 对于`"article"`类型，输入内容必须是URL，而不是文章文本；使用`"text"`类型即可。
- 对于`"x"`类型，输入内容必须是X平台或Twitter的帖子链接。
- 默认响应格式为`PDF`——如果用户需要单独的幻灯片图片，请指定`"PNG"`。
- 在导入幻灯片时，务必按照以下结构组织：1张起始幻灯片 → 1张或更多正文幻灯片 → 1张结束幻灯片。
- 对于数据量较大的内容，建议在正文幻灯片中使用信息图布局。
- 每3–5秒检查一次`GET /post/status/{embedPostId}`的状态。
- 获取结果后，将下载链接直接提供给用户。
- 如果用户未指定平台，建议使用LinkedIn（最常见的轮播图使用场景）。
- 提前告知用户费用情况：AI生成的成本是内容导入的两倍。