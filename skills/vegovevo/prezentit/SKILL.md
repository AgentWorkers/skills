```skill
---
name: prezentit
description: Generate beautiful AI-powered presentations instantly. Create professional slides with custom themes, visual designs, and speaker notes—all through natural language commands.
homepage: https://prezentit.net
emoji: "👽"
metadata:
  clawdbot:
    emoji: "👽"
    skillKey: prezentit
    homepage: https://prezentit.net
    requires:
      config:
        - PREZENTIT_API_KEY
    config:
      requiredEnv:
        - name: PREZENTIT_API_KEY
          description: Your Prezentit API key (starts with pk_). Get one free at https://prezentit.net/api-keys
      example: |
        export PREZENTIT_API_KEY=pk_your_api_key_here
    permissions:
      network:
        - https://prezentit.net/api/v1/*
      fileSystem: none
      env:
        reads:
          - PREZENTIT_API_KEY
        writes: none
---

# Prezentit - AI Presentation Generator

**Base URL**: `https://prezentit.net/api/v1`
**Auth Header**: `Authorization: Bearer {PREZENTIT_API_KEY}`

> **This skill requires a `PREZENTIT_API_KEY` environment variable.** Get a free API key at https://prezentit.net/api-keys — new accounts include 100 free credits.

## ⚠️ CRITICAL FOR AI AGENTS

**ALWAYS use `"stream": false`** in generation requests! Without this, you get streaming responses that cause issues.

---

## Complete Workflow (FOLLOW THIS ORDER)

### Step 1: Check Credits First

```  
http  
GET /api/v1/me/credits  
Authorization: Bearer {PREZENTIT_API_KEY}  

```

**Response:**
```  
json  
{  
  "credits": 100,  
  "pricing": {  
    "outlinePerSlide": 5,  
    "designPerSlide": 10,  
    "estimatedCostPerSlide": 15  
  },  
  "_ai": {  
    "canGenerate": true,  
    "maxSlidesAffordable": 6,  
    "nextSteps": ["..."  
  }  
}  

```

→ If `_ai.canGenerate` is false, direct user to https://prezentit.net/buy-credits
→ Use `_ai.maxSlidesAffordable` to know the limit

### Step 2: Choose a Theme

**Option A — Browse all available themes and pick by ID:**

```  
http  
GET /api/v1/themes  
Authorization: Bearer {PREZENTIT_API_KEY}  

```

**Response:**
```  
json  
{  
  "themes": [  
    { "id": "corporate_blue", "name": "企业蓝", "category": "企业与专业" },  
    { "id": "nature_earth", "name": "自然与有机" }  
  ],  
  "categories": ["企业与专业", "创意与视觉", "数据与分析", ...],  
  "_ai": {  
    "totalThemes": 20,  
    "popularThemes": ["corporate_blue", "midnight_tech", "nature_earth", "storyteller", "data_dashboard" }  
}  

```

→ Use the exact `id` value in your generation request

**Option B — Search for a theme by keyword:**

```  
http  
GET /api/v1/themes?search=minimalist  
Authorization: Bearer {PREZENTIT_API_KEY}  

```

→ Returns best matches ranked by relevance. Use the `id` from `bestMatch`.

**Option C — Describe a custom style (no theme ID needed):**

Use the `customDesignPrompt` parameter instead. See the Custom Design Prompt section below.

### Step 3: Generate Presentation

```  
http  
POST /api/v1/presentations/generate  
Authorization: Bearer {PREZENTIT_API_KEY}  
Content-Type: application/json  

{  
  "topic": "用户主题",  
  "slideCount": 5,  
  "theme": "corporate_blue",  
  "stream": false  
}  

```

**⏱️ IMPORTANT: Generation takes 1-3 minutes. The API will return when complete.**

**Full Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `topic` | string | Yes* | Presentation topic (2-500 chars). Required if no `outline`. `prompt` is also accepted as an alias. |
| `outline` | object | No | Pre-built outline (saves ~33% credits). See Outline section below. |
| `slideCount` | number | No | Number of slides (3-50, default: 5). Ignored if outline provided. |
| `theme` | string | No | Theme ID from `GET /api/v1/themes`. Use the exact `id` value. |
| `customDesignPrompt` | string | No | Custom visual style description (see below). Overrides theme ID. |
| `details` | string | No | Additional context about the presentation content. |
| `confirmPartial` | boolean | No | Set `true` to confirm partial generation when credits are limited. |
| `stream` | boolean | **ALWAYS false** | **AI agents must always set `stream: false`**. |

*`topic` is required even when providing an `outline` (used for presentation metadata).

### Step 4: Get the Result

**Success Response:**
```  
json  
{  
  "presentationId": "uuid-here",  
  "viewUrl": "https://prezentit.net/view/abc123",  
  "creditsUsed": 75,  
  "remainingCredits": 25  
}  

```

→ Share the `viewUrl` with the user. That's their presentation!

### Step 5: Download (Optional)

```  
http  
GET /api/v1/presentations/{presentationId}/download?format=pptx  
Authorization: Bearer {PREZENTIT_API_KEY}  

```

**Formats:** `pptx` (PowerPoint), `pdf`, `json` (raw data)

---

## Pricing

| Scenario | Cost per Slide | Example (5 slides) |
|----------|----------------|-------------------|
| Auto-generate outline | 15 credits | 75 credits |
| Provide your own outline | 10 credits | 50 credits (~33% savings!) |

- New accounts get **100 free credits**
- Buy more at: https://prezentit.net/buy-credits

---

## Theme Selection

### How to Pick a Theme

1. **Fetch the theme list**: `GET /api/v1/themes` — returns all available themes with `id`, `name`, and `category`
2. **Pick the best match** for the user's topic and style preference
3. **Pass the `id`** in the generation request as the `theme` parameter

You can also search: `GET /api/v1/themes?search=KEYWORD` or filter by category: `GET /api/v1/themes?category=CATEGORY_NAME`

### Custom Design Prompt (Skip the Theme List)

If no existing theme fits, use `customDesignPrompt` to describe a fully custom visual style. **This must be a detailed, structured description** — not just a color palette.

**REQUIRED structure for customDesignPrompt** (include ALL of these sections):

```  
**颜色系统:**  
主要颜色 [十六进制代码], 辅助颜色 [十六进制代码], 强调色 [十六进制代码], 背景颜色 [十六进制代码/渐变], 标题和正文的文字颜色。  

**排版系统:**  
标题字体样式 [例如：粗体几何无衬线字体（如Montserrat）], 正文字体样式 [例如：简洁的人体主义无衬线字体（如Open Sans）, 字体大小层次结构 [大/中/小], 字体粗细对比。  

**布局系统:**  
幻灯片结构 [例如：内容与视觉元素的比例为60/40], 文本左对齐，右侧放置视觉元素, 间距处理 [保持足够的空白与紧凑的信息布局], 使用网格布局。  

**视觉元素:**  
背景处理 [纯色/渐变/纹理/图案], 装饰性元素 [几何形状、有机曲线、线条艺术等], 图像风格 [带叠加效果的摄影、插图、图标、数据可视化], 边框/框架设计。  

**氛围与风格:**  
整体美学风格 [例如：企业权威感、富有创意、学术严谨性、科技前沿], 活力水平 [平静/动态/鲜明], 针对受众的印象。  

```

**Example — Good customDesignPrompt:**

```  
json  
{  
  "topic": "医疗领域的AI应用",  
  "customDesignPrompt":  
    "颜色系统":  
      主要颜色：深医疗蓝 (#1B3A5C),  
      辅助颜色：浅蓝绿色 (#2A9D8F),  
      强调色：暖珊瑚色 (#E76F51)  
    "背景颜色":  
      交替使用纯白色 (#FAFAFA) 和微妙的蓝灰色 (#F0F4F8)  
    "标题文字": 深海蓝色,  
    "正文文字": #333333  
    **排版系统:**  
      标题使用粗体几何无衬线字体 (Montserrat 风格),  
      正文使用简洁的人体主义无衬线字体 (Source Sans 风格),  
      字体大小层次分明：标题 48pt, 子标题 24pt, 正文 16pt  
    **布局系统:**  
      非对称布局，内容与视觉元素的比例为60/40,  
      左侧文本块与右侧的数据可视化或医疗相关图像对齐, 边距充足 (60px), 使用清晰的网格结构  
    **视觉元素:**  
      角落处有5%透明度的DNA螺旋水印,  
      使用细浅蓝绿色线条作为章节分隔符,  
      使用医疗相关的图标（听诊器、心跳图、分子结构）作为装饰元素,  
      背景使用带蓝调的叠加效果  
    **氛围与风格:**  
    专业医疗权威感与亲切温暖相结合, 风格冷静可靠, 专为医院高管和医疗专业人士设计  
    "stream": false  
}  

```

**Example — Bad customDesignPrompt (TOO VAGUE, will produce generic results):**

```  
“蓝白医疗主题”  

```

---

## Creating Outlines (Save ~33% Credits)

Providing your own outline saves credits and gives you full control over content.

### Outline Structure

The outline is an object with a `slides` array. Each slide has these fields:

```  
json  
{  
  "topic": "您的演示主题",  
  "outline": {  
    "slides": [  
      {  
        "title": "幻灯片标题",  
        "mainIdea": "解释该幻灯片的核心信息以及观众应从中获得的要点。"  
        "talkingPoints": [  
          "第一个关键点：提供足够的细节以明确其含义（至少10个字符）",  
          "第二个关键点：对主要观点进行扩展",  
          "第三个关键点：提供支持性证据或示例"  
        ],  
        "visualGuide": "详细的视觉布局说明：背景风格、图片位置、图标建议、图表类型、颜色强调区域以及该幻灯片的装饰元素。"  
      }  
    ]  
  },  
  "stream": false  
}  

```

### Slide Field Reference

| Field | Required | Constraints | Description |
|-------|----------|-------------|-------------|
| `title` | Yes | 3-100 chars, 1-15 words | Slide heading |
| `mainIdea` | Yes | 10-500 chars, 3-75 words | Core message of the slide |
| `talkingPoints` | Yes | 2-7 items, each 10-300 chars (3-50 words) | Key points to cover |
| `visualGuide` | Yes | 20-500 chars, 5-75 words | Visual design instructions for this slide |

### Validation Rules

**Overall:**
- Minimum **3 slides**, maximum **50 slides**
- `topic` is still required (used for presentation metadata)
- All four fields (`title`, `mainIdea`, `talkingPoints`, `visualGuide`) are required per slide

**The API returns detailed error messages with `fix` suggestions if validation fails.**

### Complete Example

```  
json  
{  
  "topic": "机器学习简介",  
  "outline": {  
    "slides": [  
      {  
        "title": "机器学习简介",  
        "mainIdea": "机器学习通过使系统能够从数据中学习并自动改进，从而改变企业的运作方式，而无需进行显式编程。"  
        "talkingPoints": [  
          "机器学习是人工智能的一个子领域，专注于模式识别",  
          "机器学习系统通过经验而非手动规则编写来改进",  
          "预计到2029年，全球机器学习市场将达到2090亿美元"  
        ],  
        "visualGuide":  
          **标题幻灯片**：采用未来主义科技风格，背景为深蓝色渐变，标题文字为粗体，背景中带有神经网络节点的图案，使用电蓝色作为强调色。  
      },  
      {  
        "title": "机器学习的工作原理",  
        "mainIdea": "机器学习算法根据其从数据中学习的方式分为监督学习、无监督学习和强化学习三种类型。"  
        "talkingPoints": [  
          "监督学习使用标记数据进行分类和回归任务",  
          "无监督学习通过聚类在未标记数据中发现隐藏模式",  
          "强化学习通过试错和奖励信号来优化决策"  
        ],  
        "visualGuide":  
          **三个不同的视觉部分**：分别展示三种类型的机器学习，使用蓝色、绿色和紫色进行区分。  
      },  
      {  
        "title": "商业应用",  
        "mainIdea": "各行各业的公司都在利用机器学习来提升客户体验、运营效率和决策能力。"  
        "talkingPoints": [  
          "通过提前识别高风险账户来减少客户流失",  
          "欺诈检测系统实时处理大量交易",  
          "个性化推荐系统显著提升用户参与度和销售额"  
        ],  
        "visualGuide":  
          **内容布局简洁**, 左侧文本对齐，右侧放置图标或迷你图表。背景为白色，带有细小的网格线。每个要点都配有相应的图标（欺诈防护、预测图表、个性化图标）。  
      },  
      {  
        "title": "开始使用机器学习",  
        "mainIdea": "成功采用机器学习需要从明确的使用场景、高质量的数据和合适的团队入手，而不是直接使用复杂的算法。"  
        "talkingPoints": [  
          "确定能够带来明显价值的高影响力使用场景",  
          "在选择算法之前先投资于高质量、结构良好的数据",  
          "与具有机器学习专业知识的团队合作或使用成熟的框架"  
        ],  
        "visualGuide":  
          **结论幻灯片**：包含编号的路线图或步骤说明，三个大圆圈分别代表三个步骤，背景带有向上的箭头，表示进展方向，最后一步使用醒目的强调色。  
      }  
    ],  
    "theme": "midnight_tech",  
    "stream": false  
}  

```

### Get Schema Programmatically

```  
http  
GET /api/v1/docs/outline-format  
Authorization: Bearer {PREZENTIT_API_KEY}  

```

Returns the full JSON schema with all constraints and example slides.

---

## Error Handling

### Error Response Format

```  
json  
{  
  "error": "人类可读的信息",  
  "code": "ERROR_CODE",  
  "fix": "关于如何解决此问题的指导"  
}  

```

### Common Errors & Solutions

| HTTP | Code | Message | Solution |
|------|------|---------|----------|
| 400 | `MISSING_TOPIC` | Topic or prompt is required | Provide a `topic` or `prompt` field |
| 400 | `INVALID_OUTLINE` | Outline validation failed | Check outline structure — response includes detailed `validationErrors` with `fix` per field |
| 400 | `INVALID_SLIDE_COUNT` | Slide count must be 3-50 | Adjust `slideCount` to be between 3 and 50 |
| 401 | `UNAUTHORIZED` | Invalid or missing API key | Check `Authorization: Bearer pk_...` header |
| 402 | `INSUFFICIENT_CREDITS` | Not enough credits | Response includes `required`, `available`, and `purchaseUrl` |
| 404 | `PRESENTATION_NOT_FOUND` | Presentation doesn't exist | Verify presentation ID |
| 409 | `DUPLICATE_REQUEST` | Same request within cooldown | Wait and retry — don't resend identical requests |
| 409 | `GENERATION_IN_PROGRESS` | Already generating | Check status at `GET /api/v1/me/generation/status` or cancel at `POST /api/v1/me/generation/cancel` |
| 429 | `RATE_LIMITED` | Too many requests | Wait `retryAfter` seconds before retrying |
| 500 | `GENERATION_FAILED` | Internal error | Retry once, then contact support |
| 503 | `SERVICE_UNAVAILABLE` | System overloaded | Retry after `retryAfter` seconds |

### Handling Insufficient Credits

```  
json  
{  
  "error": "信用不足",  
  "code": "INSUFFICIENT_CREDITS",  
  "required": 75,  
  "available": 50,  
  "purchaseUrl": "https://prezentit.net/buy-credits"  
}  

```

**AI Agent Response:** "You need 75 credits but only have 50. Purchase more at https://prezentit.net/buy-credits"

### Handling Partial Generation

If the user has some credits but not enough for full generation, the API returns a `confirmation_required` response with options. Read the `_ai.options` array and present them to the user. To proceed with partial generation, resend the request with `"confirmPartial": true`.

### Handling Rate Limits

```  
json  
{  
  "error": "请求过多",  
  "code": "RATE_LIMITED",  
  "retryAfter": 30  
}  

```

**AI Agent Action:** Wait `retryAfter` seconds before retrying.

---

## Additional Endpoints

### Check Generation Status

```  
http  
GET /api/v1/me/generation/status  
Authorization: Bearer {PREZENTIT_API_KEY}  

```

Returns current progress if a generation is running: stage, percentage, designs completed.

### Cancel Active Generation

```  
POST /api/v1/me/generation/cancel  
Authorization: Bearer {PREZENTIT_API_KEY}  

```

Cancels the current generation in progress.

### Get Presentation Details

```  
http  
GET /api/v1/presentations/{presentationId}  
Authorization: Bearer {PREZENTIT_API_KEY}  

```

### List User's Presentations

```  
http  
GET /api/v1/me/presentations  
Authorization: Bearer {PREZENTIT_API_KEY}  

```

Optional: `?limit=20&offset=0`

### List All Themes

```  
http  
GET /api/v1/themes  
Authorization: Bearer {PREZENTIT_API_KEY}  

```

Optional query params:
- `?search=keyword` — Filter by name
- `?category=corporate` — Filter by category

---

## Anti-Spam Rules

| Rule | Limit | What Happens |
|------|-------|--------------|
| Duplicate detection | ~30 seconds | 409 error for identical requests |
| Rate limit | Varies by key | 429 error with `retryAfter` |
| One generation at a time | 1 concurrent | 409 `GENERATION_IN_PROGRESS` error |

**Best Practice:** Always check for `retryAfter` in error responses and wait that duration.

---

## Quick Copy-Paste Examples

### Minimal Generation

```  
POST /api/v1/presentations/generate  
{  
  "topic": "气候变化简介",  
  "stream": false  
}  

```

### With Theme (Fetch ID First)

```  
1. GET /api/v1/themes → 查找主题ID  
2. POST /api/v1/presentations/generate  

```

```  
json  
{  
  "topic": "第四季度销售报告",  
  "slideCount": 8,  
  "theme": "corporate_blue",  
  "stream": false  
}  

```

### With Custom Design Prompt

```  
json  
{  
  "topic": "创业公司提案稿",  
  "slideCount": 10,  
  "customDesignPrompt":  
    "颜色系统":  
      主要颜色：电蓝色 (#4F46E5),  
      辅助颜色：青色 (#06B6D4),  
      强调色：亮粉色 (#EC4899),  
      背景颜色：深炭灰色 (#111827) 伴微妙的渐变至 #1F2937,  
      标题文字：白色,  
      正文文字：#D1D5DB  
    **排版系统:**  
      标题使用粗体宽跟踪无衬线字体 (Inter/Poppins 风格),  
      正文使用中等粗细的简洁无衬线字体,  
      字体大小对比鲜明：标题 56pt, 正文 18pt  
    **布局系统:**  
      全屏幻灯片，内容与视觉元素的比例为60/40,  
      标题左对齐，下方放置支持性文本,  
      大面积的视觉元素用于展示原型图和图表, 边距 80px  
    **视觉元素:**  
      背景上有3%透明度的细点网格图案,  
      使用霓虹色线条作为强调效果,  
      所有容器边缘呈圆形,  
      数据标注使用玻璃质感卡片和磨砂背景,  
      使用渐变网格作为装饰元素  
    **氛围与风格:**  
    强烈的科技初创企业风格, 自信且具有前瞻性, 旨在给风险投资家留下深刻印象  
    "stream": false  
}  

```

### With Outline (~33% Savings)

```  
json  
{  
  "topic": "每周团队同步会议",  
  "outline": {  
    "slides": [  
      {  
        "title": "2024年1月15日每周团队同步会议",  
        "mainIdea": "介绍会议内容及本周目标。"  
        "talkingPoints": [  
          "欢迎团队成员并确定当天的议程",  
          "回顾上周的成果和本周的重点任务"  
        ],  
        "visualGuide":  
          **标题幻灯片**：使用公司颜色, 标题居中, 下方标注日期。背景简洁且带有几何图案。  
      },  
      {  
        "title": "上周的成就",  
        "mainIdea": "团队在功能开发、问题解决和性能优化方面取得了显著进展。"  
        "talkingPoints": [  
          "功能X提前完成并合并到主分支",  
          "解决了三个影响结账流程的关键问题",  
          "数据库查询优化使页面加载时间提高了20%"  
        ],  
        "visualGuide":  
          **内容幻灯片**：每个成就旁边都有勾选图标, 完成的项目用绿色强调。左侧文本对齐, 角落处有庆祝图标。  
      },  
      {  
        "title": "本周的目标",  
        "mainIdea": "本周的重点是进行测试版发布、初步用户测试和完成文档工作。"  
        "talkingPoints": [  
          "在周三前向内部测试人员发布测试版",  
          "与五位试点客户进行用户测试",  
          "完成API文档和开发者入职指南"  
        ],  
        "visualGuide":  
          **前瞻性幻灯片**：包含编号的步骤或时间线图示, 使用蓝色强调色表示接下来的任务。  
      },  
      {  
        "title": "开放式讨论",  
        "mainIdea": "现在是提问、讨论障碍和未在议程中涵盖的问题的时间。"  
        "talkingPoints": [  
          "鼓励自由提问和讨论障碍",  
          "下一次同步会议安排在周一上午"  
        ],  
        "visualGuide":  
          **简单的结束幻灯片**, 包含问号图标或讨论气泡图示, 颜色简洁, 关键信息用大字体显示, 会议时间醒目标注。  
      }  
    ],  
    "theme": "corporate_blue",  
    "stream": false  
}  

```

---

## Getting Help

- **Website**: https://prezentit.net
- **Buy Credits**: https://prezentit.net/buy-credits
- **Support**: https://prezentit.net/support
- **API Key Management**: https://prezentit.net/api-keys
```