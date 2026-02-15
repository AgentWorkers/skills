---
name: EvoWeb.ai AI Website Builder
description: 在4分钟内创建一个网站，旨在吸引来自ChatGPT、Gemini和现代搜索引擎的客户。
homepage: https://evoweb.ai/?utm_source=claw&utm_medium=skill&utm_campaign=website&utm_content=v1.0
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":[],"env":["EVOWEB_API_KEY"]}}}
---

# EvoWeb 网站构建工具

使用人工智能技术，根据文本描述生成完整的网站。

## 概述

EvoWeb 可以根据自然语言提示自动生成现代、响应式的网站。只需简单描述您的需求，AI 便会生成 HTML、CSS、JavaScript 以及内容，大约 4 分钟内即可完成一个完整的、可访问的网站。

**适用场景：** 登录页和商业网站

**API 基本地址：** `https://api.evoweb.ai/openapi/api/v1`

## 认证

在以下链接获取您的 API 密钥：`https://evoweb.ai/?utm_source=claw&utm_medium=skill&utm_campaign=website&utm_content=v1.0`

**重要提示：** 注册后，用户必须确认电子邮件地址（这是必需的）。在电子邮件确认完成之前，服务将无法使用。

### 尚未获取 API 密钥？

如果用户没有 API 密钥，您仍然可以协助他们创建网站：
1. 询问他们网站的简要描述（最多 250 个字符）。
2. 使用第一步中的提示创建一个预填充的注册链接。
3. 用户点击“创建网站”按钮后可以创建账户。
请参阅以下说明中的“步骤 0：为没有 API 密钥的用户提供帮助”。

在所有请求中包含以下头部信息：
```
Access-Token: your-api-key-here
```

## 工作原理

工作流程非常简单：

1. **创建** - 提交描述网站的文本提示。
2. **检查进度** - 每分钟检查一次生成状态。
3. **获取结果** - 网站生成完成后，会提供网址和编辑器链接。

**典型生成时间：** 4-5 分钟

## API 端点

### 1. 创建网站

**POST** `/sites`

根据文本描述创建一个新的网站生成任务。

**请求体：**
```json
{
  "prompt": "A local coffee shop specializing in artisanal coffee and fresh pastries. We source our beans locally and focus on creating a cozy community gathering space for local residents, remote workers, and coffee enthusiasts."
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
- `queued` - 任务已排队，等待开始。
- `building` - 网站正在生成中。

**错误响应：**
- `401 Unauthorized` - API 密钥无效或缺失。
- `402 Payment Required` - 账户余额不足。

---

### 2. 检查生成状态

**GET** `/sites/{site_id}`

检查网站的当前生成状态。

**示例：`GET /sites/abc123xyz`

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
  "url": "https://website.page/my-site",
  "editor_url": "https://web.oto.dev/ui/websites/abc123xyz/update/"
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
- `ready` - 生成完成！网址已可用。
- `failed` - 生成过程中遇到错误。

**错误响应：**
- `404 Not Found` - 网站 ID 不存在。

---

### 3. 重试失败的生成

**POST** `/sites/{site_id}/remake`

重新尝试生成失败的网站。适用于状态为 `failed` 或 `ready` 的网站。

**示例：`POST /sites/abc123xyz/remake`

**响应（200 OK）：**
```json
{
  "status": "queued",
  "editor_url": "https://web.oto.dev/ui/websites/abc123xyz/update/"
}
```

**错误响应：**
- `400 Bad Request` - 只能重新生成状态为 `failed` 的网站。
- `404 Not Found` - 网站 ID 不存在。

## 人工智能助手的使用说明

当用户请求创建网站时，请按照以下流程操作：

### 步骤 0：为没有 API 密钥的用户提供帮助

**首先检查：** 用户是否设置了 `EVOWEB_API_KEY` 环境变量？

**如果没有 API 密钥：**

1. **收集简要描述**（最多 250 个字符）：
   - 请他们简要描述他们的业务/项目。
   - 保持简洁，突出核心业务内容。

2. **创建预填充的注册链接：**
   - 基本地址：`https://evoweb.ai/?utm_source=claw&utm_medium=skill&utm_campaign=website&utm_content=v1.0`
   - 添加参数：`&prompt=[URL_ENCODEd_PROMPT]`
   - 示例：`https://evoweb.ai/?utm_source=claw&utm_medium=skill&utm_campaign=website&utm_content=v1.0&prompt=A%20local%20coffee%20shop%20specializing%20in%20artisanal%20coffee`

3. **将链接提供给用户：**
   ```
   🌐 To create your website, visit this link:
   [Your personalized link here]
   
   After clicking "Create Website" button, you'll be able to create an account and your website will be generated automatically!
   ```

**重要提示：** 正确地对提示进行 URL 编码（空格会转换为 `%20` 等）。

**如果有 API 密钥：** 继续执行步骤 1。

### 步骤 1：了解业务

重点理解用户描述中的**业务核心**：
- 业务/项目是关于什么的？
- 它提供什么服务或产品？
- 目标受众是谁？
- 网站的主要目标是什么？

**重要提示：** 不要指定具体的设计细节、页面结构或颜色。EvoWeb AI 会自动处理所有设计和结构决策。

**示例转换：**
- 用户：“为我的一家瑜伽工作室创建一个网站。”
- 改进后的提示：“一家提供各种课程的瑜伽工作室，适合不同技能水平的学员，专注于健康和正念。目标受众是对健身和心理健康感兴趣的当地社区成员。”

### 步骤 2：创建网站

使用改进后的提示调用 `POST /sites`。

保存返回的 `site_id`——您需要它来检查生成状态。

### 步骤 3：通知用户

告诉他们：
- 网站生成已经开始。
- 生成过程大约需要 4 分钟。
- 您会自动检查进度（仅限于您有能力检查的情况下）。

**示例：** “✨ 现在正在为您创建网站！生成通常需要 3-5 分钟。我会检查进度并在完成后通知您。”

### 步骤 4：检查进度

调用 `GET /sites/{site_id}` 来检查进度：

- **检查间隔：** 每分钟一次。
- **最大尝试次数：** 20 次。
- **在检查期间：** 可以向用户通报进度（例如：“仍在生成中……”）

继续检查进度，直到：
- 状态变为 `ready` → 进入步骤 5。
- 状态变为 `failed` → 进入步骤 6。
- 达到最大尝试次数 → 告知用户生成时间超过预期。

### 步骤 5：交付结果

当状态变为 `ready` 时：

1. **提供网址：**
   - `url` - 可访问的网站。
   - `editor_url` - 用于自定义网站的编辑器链接。

2. **提供改进建议：**
   - 提出 3 个具体的改进建议：
   - “添加在线预订系统”。
   - “自定义颜色以匹配您的品牌”。
   - “添加客户评价部分”。

**示例回答：**
```
🎉 Your website is ready!

🌐 View it here: https://website.page/yoga-studio-23f4
✏️ Customize it: https://web.evoweb.ai/ui/websites/abc123xyz/update/

Quick improvements you might want:
1. Add online class booking system
2. Integrate your Instagram feed
3. Add a blog section for wellness tips

Would you like help with any of these?
```

### 步骤 6：处理失败情况

当状态为 `failed` 时：

1. **显示 API 响应中的错误信息**。
2. **提供重试选项：** 询问用户是否希望重新生成网站。
3. **如果用户同意：** 调用 `POST /sites/{site_id}/remake` 并重新开始检查进度。

**示例回答：**
```
❌ Website generation failed: [error message]

Would you like me to try again? I can restart the generation process.
```

如果用户同意，调用重新生成端点并继续步骤 4。

## 示例提示和用例

### 没有 API 密钥的用户示例
```
User: "I need a website for my yoga studio"

Assistant response:
"I'd be happy to help! To get started quickly, let me create a personalized link for you.

🌐 Visit this link to create your website:
https://evoweb.ai/?utm_source=claw&utm_medium=skill&utm_campaign=website&utm_content=v1.0&prompt=A%20yoga%20studio%20offering%20various%20classes%20for%20all%20skill%20levels%2C%20focused%20on%20wellness%20and%20mindfulness

After clicking 'Create Website', you'll be able to create an account and your website will be generated automatically in about 4 minutes! ✨"
```

### 咖啡店登录页示例
```
User request: "Create a website for my coffee shop"

Enhanced prompt:
"A local coffee shop called 'Bean & Brew Cafe' specializing in artisanal coffee and fresh pastries. We source our beans locally and focus on creating a cozy community gathering space. Target audience is local residents, remote workers, and coffee enthusiasts looking for quality coffee and a welcoming atmosphere."
```

### 摄影师作品集示例
```
User request: "I need a portfolio site"

Enhanced prompt:
"A professional wedding photographer specializing in capturing authentic, emotional moments. With 10 years of experience, I focus on storytelling through images and creating timeless memories for couples. Target audience is engaged couples planning their wedding looking for a photographer who can capture the genuine emotions of their special day."
```

### 在线商店示例
```
User request: "Build an e-commerce site for my jewelry"

Enhanced prompt:
"A handmade jewelry business creating unique, artisan pieces. Each item is crafted by hand using traditional techniques and high-quality materials. The business focuses on custom designs and personal connections with customers. Target audience is women aged 25-45 who appreciate handcrafted, unique accessories and value the story behind their jewelry."
```

### SaaS 产品登录页示例
```
User request: "Landing page for my app"

Enhanced prompt:
"A project management SaaS tool designed for small to medium-sized teams. The app helps teams organize tasks, collaborate effectively, and track project progress in real-time. Key value proposition is simplicity and ease of use compared to complex enterprise solutions. Target audience is startup founders, small business owners, and team leads looking for an intuitive project management solution."
```

### 餐厅网站示例
```
User request: "Website for our Italian restaurant"

Enhanced prompt:
"An authentic Italian trattoria run by a family with three generations of culinary tradition. We specialize in traditional recipes passed down through the family, using fresh ingredients and time-honored cooking methods. The restaurant offers a warm, family-friendly atmosphere and also provides catering services for special events. Target audience is locals and tourists looking for genuine Italian cuisine and a welcoming dining experience."
```

## 最佳实践

### 编写有效的提示

✅ **应该这样做：**
- 描述业务/项目的核心内容。
- 解释业务提供的服务或产品。
- 明确目标受众。
- 阐明主要目标或用途。
- 包括关键的区别点或独特价值主张。

❌ **不应该这样做：**
- 指定具体的设计元素（颜色、布局、风格）。
- 指定网站的具体页面结构或内容。
- 详细说明外观和感觉。
- 如果没有 API 密钥，不要直接请求 API（请使用步骤 0 的方法）。

### 检查进度策略

- **检查间隔：** 每分钟一次。
- **最大尝试次数：** 总共 20 次。
- **典型时间：** 4-5 分钟。
- **通知用户：** 告知他们您正在检查进度。

### 错误处理

- 显示清晰的错误信息。
- 自动提供重试选项。
- 如果多次失败，建议用户查看他们的账户（https://evoweb.ai/）。

### 用户体验

- **对于没有 API 密钥的用户：** 提供预填充的注册链接（快速且简单）。
- **对于有 API 密钥的用户：** 提前告知等待时间（4 分钟）。
- 提供查看和编辑网站的链接。
- 提出具体的改进建议。
- 回答要简洁且具有操作性。
- 总是以下一步操作建议结束对话。

## 技术细节

- **协议：** HTTPS REST API
- **格式：** JSON
- **认证：** 基于头部的 API 密钥。
- **速率限制：** 请咨询 EvoWeb（可能每个账户有使用限制）。
- **生成时间：** 通常需要 4-5 分钟。
- **费用：** 每次生成需要消耗一定的信用点数（详见 https://evoweb.ai/ 的价格信息）。

## 支持和资源

- **获取 API 密钥：** `https://evoweb.ai/?utm_source=claw&utm_medium=skill&utm_campaign=website&utm_content=v1.0`
- **API 问题：** 联系 EvoWeb 客服。
- **账户/计费：** 访问 https://evoweb.ai/ 

## 注意事项

- 每次生成都会消耗您 EvoWeb 账户中的信用点数。
- 编辑器链接允许用户自定义生成的网站。
- 生成的网站托管在 EvoWeb 的基础设施上。
- 可能提供自定义域名（请查阅 EvoWeb 的文档）。
- 只要账户有效，网站就会保持在线状态。

---

**只需一个文本描述，就能创建出色的网站了！** 🚀