---
name: twinfold
description: Control Twinfold — AI-powered social media content platform — from your agent. Create posts, generate images, adapt content for 10 platforms in 13 languages, manage autopilot, publish, and track analytics. Use when the user wants to create social media content, post to LinkedIn/Twitter/Instagram/etc., manage their content calendar, run autopilot content generation, check trends, or interact with their Twinfold account. Triggers on: post, publish, tweet, linkedin, social media, content, schedule, autopilot, twinfold, thread, adapt, trends, repurpose.
metadata:
  openclaw:
    requires:
      env:
        - TWINFOLD_API_KEY
    credentials:
      - name: TWINFOLD_API_KEY
        description: "Twinfold API key (starts with twf_). Get one at twinfold.app → Settings → API Keys."
        required: true
        prefix: "twf_"
---

# Twinfold Skill

您可以通过 [Twinfold](https://twinfold.app) 的 MCP API 来控制这个 AI 思维领导力平台。

## 设置

用户需要一个 Twinfold API 密钥。请检查环境变量 `TWINFOLD_API_KEY` 是否已设置。如果密钥缺失，请告知用户：
1. 访问 **twinfold.app → 设置 → API 密钥**  
2. 创建一个新的密钥（密钥名称以 `twf_` 开头）  
3. 将密钥设置为：`export TWINFOLD_API_KEY=twf_...`，或将其添加到 `.env` 文件中。

## API

**端点：** `POST https://twinfold.app/api/mcp/tools`  
**认证：** `Authorization: Bearer <TWINFOLD_API_KEY>`  
**请求体：** `{ "tool": "twinfold.<toolName>", "arguments": { ... } }`

所有请求在成功时返回 `{ "result": { ... }`，在失败时返回 `{ "error": "..." }`。

### 发现工具

```bash
curl https://twinfold.app/api/mcp/tools
```

该接口用于获取所有 34 个工具的详细信息（包括其使用方式）。无需进行身份验证。

## 工具快速参考

### 内容创建

| 工具 | 用途 |
|------|-----|
| `createPost` | 使用 AI 生成帖子，支持多语言、添加图片、生成首条评论，并自动适配不同平台格式后发布 |
| `createArticle` | 利用 Twin 的知识生成长篇文章 |
| `adaptContent` | 根据特定平台的文化和格式重新编写内容 |
| `generateHooks` | 生成 4 个具有互动效果的社交媒体帖子模板（附带互动数据） |
| `generateImage` | 生成 AI 图片并附在帖子上 |
| `repurposeContent` | 将任何文本转换为适用于多个平台的帖子草稿 |
| `planContent` | 生成包含多篇帖子的内容日程表 |

### 内容管理

| 工具 | 用途 |
|------|-----|
| `'post` | 读取单篇帖子的详细信息 |
| `listPosts` | 列出帖子（可按状态或平台筛选） |
| `updatePost` | 编辑帖子内容、平台设置、媒体文件及发布时间 |
| `deletePost` | 删除草稿或已安排的帖子 |
| `listArticles` | 列出所有文章 |

### 发布

| 工具 | 用途 |
|------|-----|
| `publishNow` | 立即将帖子发布到已连接的平台上 |
| `schedulePost` | 预定帖子的发布时间 |

### 自动化流程

| 工具 | 用途 |
|------|-----|
| `runAutopilot` | 启动完整的自动化流程（发现 → 创建 → 发布） |
| `getAutopilotQueue` | 查看待审核的帖子列表 |
| `approvePost` | 批准已安排的帖子发布 |
| `rejectPost` | 拒绝自动生成的帖子 |

### 智能辅助

| 工具 | 用途 |
|------|-----|
| `queryTwin` | 根据用户的专业知识向 AI 提出问题 |
| `addKnowledge` | 向 Twin 提供新知识 |
| `getTrends` | 获取按相关性排序的热门话题 |

### 品牌指南与品牌声音

| 工具 | 用途 |
|------|-----|
| `getBrandGuide` | 获取品牌指南的 Markdown 文件 |
| `setBrandGuide` | 更新品牌指南（免费，无需额外费用） |
| `generateBrandGuide` | 利用 Twin 的知识自动生成品牌指南（需 5 个信用点） |
| `listBrandVoices` | 列出所有品牌声音配置文件 |
| `createBrandVoice` | 手动创建品牌声音 |
| `updateBrandVoice` | 更新现有的品牌声音 |
| `deleteBrandVoice` | 删除品牌声音配置文件 |
| `generateBrandVoice` | 生成品牌声音分析报告（需 5 个信用点） |

### 通知

| 工具 | 用途 |
|------|-----|
| `getNotifications` | 查看未读通知（按类型分页显示） |
| `markNotificationRead` | 将一个或多个通知标记为已读 |
| `getNotificationPreferences` | 获取通知渠道偏好设置 |

### 账户

| 工具 | 用途 |
|------|-----|
| `listAccounts` | 查看已连接的社交账户及支持的语言 |
| `getCredits` | 查看信用点余额、计划及费用信息 |
| `getAnalytics` | 查看帖子统计和工作区分析数据 |

## 常见工作流程

有关工具的详细信息及工作流程示例，请参阅 [references/workflows.md](references/workflows.md)。

### 快速操作：创建并发布帖子

```
1. twinfold.createPost { topic, platforms, language, autoAdapt: true, autoPublish: true }
```

通过一次 API 调用即可完成内容生成、平台适配及发布。

### 快速操作：创建 → 审核 → 发布

```
1. twinfold.createPost { topic, platforms, language }  → postId
2. Show content to user, let them edit
3. twinfold.updatePost { postId, content: editedContent }
4. twinfold.publishNow { postId }
```

### 完整的自动化流程（包含图片和社交媒体帖子模板）

```
1. twinfold.generateHooks { topic }  → pick best hook
2. twinfold.createPost { topic, platforms, language, generateImage: true, generateFirstComment: true }  → postId
3. twinfold.getPost { postId }  → review
4. twinfold.publishNow { postId }
```

## 支持的平台

LinkedIn · Twitter/X · Instagram · Facebook · YouTube · TikTok · Pinterest · Threads · Reddit · Bluesky

## 支持的语言

英语 · 法语 · 魁北克法语（fr-CA）· 西班牙语 · 德语 · 葡萄牙语 · 巴西葡萄牙语 · 意大利语 · 荷兰语 · 日语 · 韩语 · 中文 · 阿拉伯语

您可以根据需要为每个社交账户或 API 调用设置相应的语言。内容会以原始语言生成（不会被翻译）。

## 信用点费用

| 操作 | 所需信用点 |
|-----------|---------|
| 发布帖子 | 10 |
| 创建文章 | 50 |
| 生成社交媒体帖子模板 | 5 |
| 生成图片 | 10 |
| 添加首条评论 | 2 |
| 向 Twin 提问 | 2 |
| 生成品牌指南 | 5 |
| 生成品牌声音 | 5 |

在进行大规模操作前，请务必查看 `twinfold.getCredits` 的余额。

## 错误处理

- `401` → API 密钥无效  
- `402` | 信用点不足（请使用 `getCredits` 检查余额）  
- `400` | 参数错误（错误信息会说明具体问题）  
- `429` | 请求次数达到限制（请稍后重试）

## 提示

- 在 `createPost` 中设置 `autoAdapt: true` 可自动优化帖子以适应不同平台  
- 设置 `language: "fr-CA"` 可生成纯正的魁北克法语内容  
- 结合使用 `getTrends` 和 `createPost` 可根据热门趋势生成内容  
- `repurposeContent` 可将博客文章、文本记录或笔记转换为适合社交媒体的格式  
- `planContent` 可一次性生成一周的内容草稿  
- 自动化流程每天运行一次——使用 `getAutopilotQueue` 和 `approvePost` 进行内容审核