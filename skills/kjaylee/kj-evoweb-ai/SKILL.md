---
name: EvoWeb.ai Website Builder
description: 创建一个网站，旨在将客户从 ChatGPT、Gemini 和现代搜索引擎引入该网站。
homepage: https://evoweb.ai/
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":[],"env":["EVOWEB_API_KEY"]}}}
---

# EvoWeb 网站构建工具

使用基于人工智能的生成技术，根据文本描述创建完整的网站。

## 概述

EvoWeb 可以根据自然语言提示自动生成现代化、响应式网站。只需简单描述您的需求，AI 就会生成 HTML、CSS、JavaScript 以及内容，大约 4 分钟内即可交付一个完整的、可在线使用的网站。

**适用场景：** 登录页、作品集、在线商店、博客、企业网站

**API 基本地址：** `https://api.web.oto.dev/openapi/api/v1`

## 认证

请从以下链接获取您的 API 密钥：https://evoweb.ai/

在所有请求中包含以下头部信息：
```
Access-Token: your-api-key-here
```

## 工作原理

工作流程非常简单：

1. **创建** - 提交一个描述您网站的文本提示。
2. **检查生成进度** - 每 15-20 秒检查一次生成状态。
3. **获取结果** - 网站生成完成后，您将收到网站的在线地址和编辑器链接。

**典型生成时间：** 2-5 分钟

## API 端点

### 1. 创建网站

**POST** `/sites`

根据文本描述创建一个新的网站生成任务。

**请求体：**
```json
{
  "prompt": "Create a modern landing page for a coffee shop with menu section, gallery of drinks, contact form, and location map. Use warm brown tones and inviting imagery."
}
```

**响应（200 OK）：**
```json
{
  "site_id": "abc123xyz",
  "status": "queued"
}
```

**状态值：**
- `queued` - 任务已加入队列，等待开始。
- `building` - 网站正在生成中。

**错误响应：**
- `401 Unauthorized` - API 密钥无效或缺失。
- `402 Payment Required` - 账户余额不足。

---

### 2. 检查生成进度

**GET** `/sites/{site_id}`

查看网站的当前生成状态。

**示例：** `GET /sites/abc123xyz`

**生成中时的响应：**
```json
{
  "status": "building"
}
```

**生成完成时的响应：**
```json
{
  "status": "ready",
  "url": "https://my-site.evoweb.ai",
  "editor_url": "https://editor.evoweb.ai/sites/abc123xyz"
}
```

**生成失败时的响应：**
```json
{
  "status": "failed",
  "error": "Generation failed: Invalid prompt structure"
}
```

**状态值：**
- `queued` - 在队列中等待。
- `building` - 正在生成中（请稍候！）
- `ready` - 生成完成！可获取网址。
- `failed` - 生成过程中遇到错误。

**错误响应：**
- `404 Not Found` - 网站 ID 不存在。

---

### 3. 重试失败的生成

**POST** `/sites/{site_id}/remake`

重新尝试生成失败的网站。仅适用于状态为 `failed` 的网站。

**示例：** `POST /sites/abc123xyz/remake`

**响应（200 OK）：**
```json
{
  "status": "queued",
  "editor_url": "https://editor.evoweb.ai/sites/abc123xyz"
}
```

**错误响应：**
- `400 Bad Request` - 只能重新生成状态为 `failed` 的网站。
- `404 Not Found` - 网站 ID 不存在。

## 与 AI 助手的沟通指南

当用户请求创建网站时，请按照以下步骤操作：

### 第 1 步：完善提示

将用户的请求转化为详细、结构化的提示，包括：
- 网站的目的和类型。
- 需要的具体页面（首页、关于我们、联系我们等）。
- 功能（表单、图库、价格表等）。
- 设计风格（现代、极简、优雅、专业等）。
- 颜色偏好。
- 目标受众。

**示例转换：**
- 用户：**为我的瑜伽工作室创建一个网站。**
- 完善后的提示：**为瑜伽工作室创建一个现代化的登录页，包含课程安排、会员等级的价格表、带照片的教练简介、咨询联系表以及嵌入地图的位置信息。使用柔和的蓝色和绿色作为主色调，并搭配自然元素。**

### 第 2 步：创建网站

使用完善后的提示调用 `POST /sites`。

保存返回的 `site_id`——您需要它来检查网站生成进度。

### 第 3 步：通知用户

告知用户：
- 网站生成已经开始。
- 生成过程大约需要 4 分钟。
- 我会自动检查进度并通知您。

**示例：** “✨ 正在为您创建网站！生成通常需要 3-5 分钟。我会随时检查进度并通知您。”

### 第 4 步：检查生成进度

调用 `GET /sites/{site_id}` 来检查进度：

- **检查间隔：** 每 17 秒（建议 15-20 秒）。
- **最大尝试次数：** 20 次（总共约 6 分钟）。
- **检查期间：** 可以向用户反馈生成进度（例如：“仍在生成中……”）。

持续检查进度，直到：
- 状态变为 `ready` → 进入第 5 步。
- 状态变为 `failed` → 进入第 6 步。
- 达到最大尝试次数 → 告知用户生成时间超过预期。

### 第 5 步：交付结果

当状态变为 `ready` 时：

1. **提供网址：**
   - `url` - 在线网站的地址。
   - `editor_url` - 编辑网站的链接。
2. **提供改进建议：**
   - 提出 3 个具体的改进建议：
     - “添加在线预订系统。”
     - “调整颜色以匹配您的品牌。”
     - “添加客户评价部分。”
3. **回答要简洁且具有操作性。**

**示例响应：**
```
🎉 Your website is ready!

🌐 View it here: https://yoga-studio-23f4.evoweb.ai
✏️ Customize it: https://editor.evoweb.ai/sites/abc123xyz

Quick improvements you might want:
1. Add online class booking system
2. Integrate your Instagram feed
3. Add a blog section for wellness tips

Would you like help with any of these?
```

### 第 6 步：处理失败情况

当状态为 `failed` 时：

1. **显示 API 响应中的错误信息。**
2. **提供重试选项：** 询问用户是否希望重新生成网站。
3. **如果用户同意：** 调用 `POST /sites/{site_id}/remake` 并重新开始检查进度。

**示例响应：**
```
❌ Website generation failed: [error message]

Would you like me to try again? I can restart the generation process.
```

如果用户同意，重新调用生成端点并继续第 4 步的操作。

## 示例提示及使用场景

### 咖啡店登录页
```
User request: "Create a website for my coffee shop"

Enhanced prompt:
"Create a modern landing page for 'Bean & Brew Cafe' with:
- Hero section featuring coffee and cozy atmosphere
- Menu section with drinks and pastries (with prices)
- About section highlighting locally sourced beans
- Hours and location with map
- Contact form for catering inquiries
- Instagram feed integration
Use warm brown and cream colors with inviting photography style"
```

### 摄影师作品集
```
User request: "I need a portfolio site"

Enhanced prompt:
"Create a professional portfolio website for a wedding photographer with:
- Stunning hero image showcasing best work
- Project gallery organized by wedding collections
- About page with photographer bio and experience
- Services and pricing packages
- Contact form for booking inquiries
- Testimonials from happy couples
Use clean, elegant design with white space, black and white aesthetic, and large image displays"
```

### 在线商店
```
User request: "Build an e-commerce site for my jewelry"

Enhanced prompt:
"Create an online store for handmade jewelry with:
- Product catalog with filtering by category (necklaces, earrings, rings, bracelets)
- Individual product pages with multiple photos and descriptions
- Shopping cart functionality
- Checkout form with shipping options
- About the artisan section
- Custom order inquiry form
Use elegant design with soft rose gold accents and luxury feel"
```

### SaaS 产品登录页
```
User request: "Landing page for my app"

Enhanced prompt:
"Create a SaaS landing page for a project management tool with:
- Value proposition above the fold with app screenshot
- Feature showcase with icons (task tracking, team collaboration, reporting)
- Pricing table with 3 tiers (Free, Pro, Enterprise)
- Customer testimonials with logos
- Free trial CTA buttons throughout
- FAQ section
Use modern, professional design with blue primary color and clean interface"
```

### 餐厅网站
```
User request: "Website for our Italian restaurant"

Enhanced prompt:
"Create a restaurant website for an authentic Italian trattoria with:
- Rotating hero images of signature dishes
- Full menu with appetizers, pasta, entrees, desserts, wine list
- Online reservation system
- About section telling family story and traditions
- Location with map and parking info
- Photo gallery of dining room and dishes
- Catering services page
Use warm, inviting design with red and green accents, rustic Italian aesthetic"
```

## 最佳实践

### 撰写有效的提示

✅ **应该做到：**
- 明确指定页面和功能。
- 提及设计风格和整体风格。
- 包括颜色偏好。
- 明确网站的目的和目标受众。
- 列出所需的关键页面。

❌ **不应该这样做：**
- 提示过于模糊（例如“创建一个网站”）。
- 省略重要细节。
- 假设 AI 会自动理解您的需求。

### 检查进度的策略

- **检查间隔：** 每 15-20 秒（建议 17 秒）。
- **最大尝试次数：** 总共 20 次。
- **典型时间：** 3-5 分钟（大约 8-15 次检查）。
- **通知用户：** 告知他们您正在检查进度。

### 错误处理

- 显示清晰的错误信息。
- 自动提供重试选项。
- 如果多次尝试失败，建议用户登录 https://evoweb.ai/ 检查账户信息。

### 用户体验

- 设定合理的等待时间（4 分钟）。
- 提供网站的在线查看和编辑链接。
- 提出具体的改进建议。
- 回答要简洁明了。
- 每次回复都要提供下一步的操作指南。

## 技术细节

- **协议：** HTTPS REST API
- **格式：** JSON
- **认证：** 基于头部的 API 密钥。
- **速率限制：** 请咨询 EvoWeb（可能设有每个账户的使用限制）。
- **生成时间：** 通常需要 2-5 分钟。
- **费用：** 每次生成需要消耗一定的信用点数（详见 https://evoweb.ai/ 的价格信息）。

## 支持与资源

- **获取 API 密钥：** https://evoweb.ai/
- **API 相关问题：** 联系 EvoWeb 客服。
- **账户/计费：** 访问 https://evoweb.ai/。

## 注意事项

- 每次生成都会消耗您 EvoWeb 账户中的信用点数。
- 编辑器链接允许用户自定义生成的网站。
- 生成的网站托管在 EvoWeb 的基础设施上。
- 可能支持自定义域名（请参阅 EvoWeb 的文档）。
- 只要账户有效，网站就会保持在线状态。

---

**只需提供文本描述，即可创建令人惊叹的网站！** 🚀