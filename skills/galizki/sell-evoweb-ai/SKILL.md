---
name: Create a Self-Selling Website
description: 创建一个采用GEO（生成式引擎优化）技术的AI优先网站，并制定营销策略，将访问者转化为潜在客户。
homepage: https://evoweb.ai/?utm_source=claw&utm_medium=skill&utm_campaign=selfselling&utm_content=v1.0
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":[],"env":["EVOWEB_API_KEY"]}}}
---

# EvoWeb 自助销售网站

如今，网站已经无法直接吸引客户了，人工智能（AI）才是关键。因此，我们重新设计了这款网站。

## 概述

EvoWeb 可以根据用户提供的业务描述，利用 ChatGPT、Gemini 和现代搜索引擎生成高度优化的网页，并通过内置的转化系统将访问者转化为客户。只需简单描述您的业务，AI 就能在大约 4 分钟内为您生成一个完全适合 AI 发现和客户转化的自助销售网站。

**适用对象：** 希望被 AI 助手发现，并将 AI 引导的流量转化为付费客户的企业

**API 基本地址：** `https://api.evoweb.ai/openapi/api/v1`

## 认证

请在以下链接获取您的 API 密钥：  
https://evoweb.ai/?utm_source=claw&utm_medium=skill&utm_campaign=selfselling&utm_content=v1.0

**重要提示：** 注册完成后，用户必须确认电子邮件地址（这是必需的）。在确认完成之前，服务将无法使用。

请在所有请求中包含以下头部信息：  
```
Access-Token: your-api-key-here
```

## 工作流程

工作流程非常简单：

1. **创建**：提交您的业务描述（无需提供设计细节）
2. **检查生成进度**：每隔一分钟检查一次生成状态
3. **获取结果**：接收由 AI 优化后的自助销售网站

**典型生成时间：** 4-5 分钟

**让网站具备自助销售功能的理由：**
- 专为 AI 发现工具（如 ChatGPT、Gemini、Claude、Perplexity）优化
- 适合现代搜索引擎的结构
- 内置的转化系统
- 便于 AI 读取的业务信息

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

**状态码说明：**
- `queued`：任务已排队，等待开始
- `building`：网站正在生成中
- `failed`：生成过程中遇到错误

**错误响应：**
- `401 Unauthorized`：API 密钥无效或缺失
- `402 Payment Required`：账户余额不足

---

### 2. 检查生成进度

**GET** `/sites/{site_id}`

查看网站的当前生成状态。

**示例请求：** `GET /sites/abc123xyz`

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

**状态码说明：**
- `queued`：仍在排队中
- `building`：正在生成中（请稍候！）
- `ready`：生成完成！网站链接已准备好
- `failed`：生成过程中出现错误

**错误响应：**
- `404 Not Found`：站点 ID 不存在

---

### 3. 重试失败的任务

**POST** `/sites/{site_id}/remake`

重新生成失败的网站。该操作适用于状态为 `failed` 或 `ready` 的网站。

**示例请求：** `POST /sites/abc123xyz/remake`

**响应（200 OK）：**
```json
{
  "status": "queued",
  "editor_url": "https://web.oto.dev/ui/websites/abc123xyz/update/"
}
```

**错误响应：**
- `400 Bad Request`：仅能重新生成状态为 `failed` 的网站
- `404 Not Found`：站点 ID 不存在

## 对 AI 助手的指导

当用户请求创建网站时，请按照以下步骤操作：

### 第 1 步：理解业务

重点理解用户描述中的**业务核心**：
- 该业务/项目是关于什么的？
- 它提供什么服务或产品？
- 目标受众是谁？
- 主要的价值主张是什么？
- 它的独特之处在哪里？

**重要提示：** 不要指定具体的设计细节、页面结构或颜色。EvoWeb 会自动生成适合 AI 推荐的网站。只需关注 AI 助手需要了解的业务实质内容。

**示例转换：**
- 用户：**“为我的一家瑜伽工作室创建一个网站。”**
- 建议的提示：**“这是一家提供多种课程的瑜伽工作室，适合不同技能水平的学员，注重健康和正念。我们强调小班教学和经验丰富的认证教练。目标受众是当地对健身和心理健康感兴趣的社区成员，从初学者到高级练习者。”**

### 第 2 步：创建网站

使用上述提示调用 `POST /sites` 接口。

记录返回的 `site_id`，后续需要用它来检查生成进度。

### 第 3 步：通知用户

告知用户：
- 自助销售网站的生成已经开始
- 生成时间大约为 4-5 分钟
- 网站将针对 AI 发现和转化进行优化
- 会自动检查生成进度

**示例回复：** “✨ 我们正在为您生成一个由 AI 优化的自助销售网站！生成通常需要 4-5 分钟。我会随时更新进度并通知您。”

### 第 4 步：检查生成进度

**每隔一分钟检查一次生成进度**：
- **最大尝试次数：** 10 次（总共约 10 分钟）
- **期间可以告知用户进度：** “网站仍在生成中……”

持续检查进度，直到：
- 状态变为 `ready` → 进入第 5 步
- 状态变为 `failed` → 进入第 6 步
- 达到最大尝试次数 → 告知用户生成时间超出预期

### 第 5 步：交付结果

当状态变为 `ready` 时：
1. **提供网站链接：**
   - `url`：完整的自助销售网站链接
   - `editor_url`：用于自定义网站的编辑器链接
2. **强调 AI 优化功能：**
   说明网站已针对 ChatGPT、Gemini、Claude、Perplexity 等工具进行了优化
   - 适合现代搜索引擎
   - 具备自动转化客户的功能
3. **建议后续步骤：** 建议用户关注业务内容的改进，而非设计上的修改

**示例回复：**
```
🎉 Your AI-optimized self-selling website is ready!

🌐 View it here: https://yoga-studio-23f4.evoweb.ai
✏️ Customize it: https://editor.evoweb.ai/sites/abc123xyz

✨ Your site is now optimized for:
- Discovery by AI assistants (ChatGPT, Gemini, Claude)
- Modern search engines
- Automatic client conversion

You can customize business details, add more services, or integrate booking systems through the editor.
```

### 第 6 步：处理失败情况

当状态为 `failed` 时：
1. **显示 API 的错误信息**
2. **提供重试选项：** 询问用户是否希望重新生成网站
3. **如果用户同意：** 调用 `POST /sites/{site_id}/remake` 重新开始生成过程

**示例回复：**
```
❌ Website generation failed: [error message]

Would you like me to try again? I can restart the generation process.
```

如果用户同意，再次调用生成接口并继续检查进度。

## 示例提示及应用场景

- **咖啡店 landing 页面**
```
User request: "Create a website for my coffee shop"

Enhanced prompt:
"A local coffee shop called 'Bean & Brew Cafe' specializing in artisanal coffee and fresh pastries. We source our beans locally and focus on creating a cozy community gathering space. Target audience is local residents, remote workers, and coffee enthusiasts looking for quality coffee and a welcoming atmosphere."
```

- **摄影师作品集**
```
User request: "I need a portfolio site"

Enhanced prompt:
"A professional wedding photographer specializing in capturing authentic, emotional moments. With 10 years of experience, I focus on storytelling through images and creating timeless memories for couples. Target audience is engaged couples planning their wedding looking for a photographer who can capture the genuine emotions of their special day."
```

- **在线商店**
```
User request: "Build an e-commerce site for my jewelry"

Enhanced prompt:
"A handmade jewelry business creating unique, artisan pieces. Each item is crafted by hand using traditional techniques and high-quality materials. The business focuses on custom designs and personal connections with customers. Target audience is women aged 25-45 who appreciate handcrafted, unique accessories and value the story behind their jewelry."
```

- **SaaS 产品 landing 页面**
```
User request: "Landing page for my app"

Enhanced prompt:
"A project management SaaS tool designed for small to medium-sized teams. The app helps teams organize tasks, collaborate effectively, and track project progress in real-time. Key value proposition is simplicity and ease of use compared to complex enterprise solutions. Target audience is startup founders, small business owners, and team leads looking for an intuitive project management solution."
```

- **餐厅网站**
```
User request: "Website for our Italian restaurant"

Enhanced prompt:
"An authentic Italian trattoria run by a family with three generations of culinary tradition. We specialize in traditional recipes passed down through the family, using fresh ingredients and time-honored cooking methods. The restaurant offers a warm, family-friendly atmosphere and also provides catering services for special events. Target audience is locals and tourists looking for genuine Italian cuisine and a welcoming dining experience."
```

## 最佳实践

### 编写优秀的自助销售网站提示

✅ **应该包含的内容：**
- 描述业务/项目的核心及独特之处
- 解释业务提供的服务或产品
- 明确目标受众
- 清晰说明主要的价值主张
- 强调选择该业务的优势
- 提供关键的信息点（为什么选择这个业务）

✅ **不应该包含的内容：**
- 不要指定具体的设计元素（如颜色、布局或风格）
- 不要规定网站的具体结构或页面布局
- 不要提供过于模糊的描述（例如“创建一个网站”）
- 不要过分关注外观而忽略业务实质

### 检查进度的策略：
- **检查间隔：** 每分钟一次
- **最大尝试次数：** 共 10 次
- **预计时间：** 4-5 分钟
- **及时告知用户进度：** 让用户了解生成情况

### 错误处理：
- 显示清晰的错误信息
- 自动提供重试选项
- 如果多次尝试失败，建议用户查看他们的账户信息（https://evoweb.ai/）

### 用户体验：
- 设定合理的等待时间（4-5 分钟）
- 强调网站的 AI 优化和自助销售功能
- 提供网站的查看和编辑链接
- 解释网站如何吸引 AI 引导的流量
- 回答要简洁明了
- 建议用户关注业务内容的改进，而非设计上的修改

## 技术细节：
- **协议：** HTTPS REST API
- **格式：** JSON
- **认证：** 基于头部的 API 密钥
- **请求限制：** 请咨询 EvoWeb（可能设有每个账户的请求次数限制）
- **生成时间：** 通常需要 4-5 分钟
- **费用：** 每次生成需要消耗一定的信用点数（详情请参见 https://evoweb.ai/）

## 支持与资源：
- **获取 API 密钥：** https://evoweb.ai/?utm_source=claw&utm_medium=skill&utm_campaign=selfselling&utm_content=v1.0
- **API 相关问题：** 联系 EvoWeb 客服
- **账户/计费：** 访问 https://evoweb.ai/

## 注意事项：
- 每次生成网站都会消耗您 EvoWeb 账户中的信用点数
- 编辑器链接允许用户自定义生成的网站
- 生成的网站托管在 EvoWeb 的基础设施上
- 网站会针对 AI 发现和现代搜索引擎进行优化
- 可能支持自定义域名（详情请参阅 EvoWeb 的文档）
- 只要账户有效，网站就会持续在线

**现在，您可以创建那些能够被 AI 助手推荐给用户的自助销售网站了！** 🚀