---
name: multi-platform-crosspost
description: **自动将博客内容跨发布到7个以上平台（LinkedIn、Dev.to、Hashnode、Twitter/X、Reddit、Substack、Pinterest）**，同时支持内容跟踪、去重以及针对每个平台的个性化格式化处理。该流程已通过生产环境测试。
tags: [cross-posting, content-distribution, seo, blog, linkedin, devto, hashnode, automation, marketing]
author: mhmalvi
version: 1.2.0
license: CC BY-NC-SA 4.0
metadata:
  clawdbot:
    emoji: "📡"
    requires:
      n8nCredentials: [google-sheets-oauth2, smtp, linkedin-oauth2]
    os: [linux, darwin, win32]
---
# 多平台跨发布管道 📡

只需一个命令，即可自动将您的博客内容分发到7个以上的平台。该工具专为Hugo博客设计，但也可适配任何静态站点生成器或内容管理系统（CMS）。

## 问题

您写了一篇很棒的文章，但每次都需要花费45分钟的时间手动将其发布到LinkedIn、Dev.to、Hashnode、Reddit、Substack和Twitter等平台上。

这个工具可以完全解决这个问题。

## 功能

1. 接收博客文章的标识符（slug）作为输入。
2. 从您的博客管理API获取文章的全部内容。
3. 根据每个平台的要求对内容进行格式化（如将HTML转换为Markdown、处理字符限制、处理图片等）。
4. 通过API自动将内容发布到支持API的平台（Dev.to、Hashnode、LinkedIn）。
5. 对不支持API的平台（Twitter、Reddit、Substack）通过电子邮件发送格式化后的内容。
6. 在Google Sheets中记录所有跨平台发布的操作（通过slug和来源信息进行去重）。
7. 处理身份验证、请求速率限制和错误恢复等问题。

## 支持的平台

| 平台 | 方法 | 自动化程度 |
|----------|--------|-----------------|
| LinkedIn | API（OAuth） | 完全自动化 |
| Dev.to | API（token） | 完全自动化 |
| Hashnode | API（token） | 完全自动化 |
| Pinterest | API | 完全自动化 |
| Twitter/X | 电子邮件摘要 | 内容格式化后手动发布 |
| Reddit | 电子邮件摘要 | 内容格式化后手动发布 |
| Substack | 电子邮件摘要 | 内容格式化后手动发布 |

## 架构

```
Blog Post Published
    │
    ▼
Webhook Trigger (n8n)
    │
    ├── Validate auth (_secret)
    ├── Fetch post content from blog-admin API
    ├── Parse frontmatter + body
    │
    ├──► IF LinkedIn enabled → Format + Post via API
    ├──► IF Dev.to enabled → Format + Post via API
    ├──► IF Hashnode enabled → Format + Post via API
    ├──► IF Pinterest enabled → Format + Pin via API
    ├──► IF Twitter enabled → Format + Email to owner
    ├──► IF Reddit enabled → Format + Email to owner
    └──► IF Substack enabled → Format + Email to owner
    │
    ▼
Google Sheets Tracker (appendOrUpdate, no duplicates)
```

## 所需的n8n凭证

在导入此工作流之前，您需要在n8n实例中创建以下凭证：

| 凭证类型 | 用途 | JSON中的占位符 |
|----------------|----------|---------------------|
| Google Sheets OAuth2 | 跨平台发布跟踪和去重 | `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID` |
| SMTP（Gmail或自定义） | 用于手动发送电子邮件的SMTP凭证 | `YOUR_SMTP_CREDENTIAL_ID` |
| LinkedIn OAuth2 | 自动发布到LinkedIn的凭证 | `YOUR_LINKEDIN_CREDENTIAL_ID` |
| OpenAI（可选） | 用于内容格式化的AI服务 | `YOUR_OPENAI_CREDENTIAL_ID` |

## 配置占位符

在部署工作流之前，请替换以下占位符：

| 占位符 | 说明 |
|-------------|-------------|
| `YOUR_BLOG_ADMIN_API_KEY` | 博客管理面板的API密钥 |
| `YOUR_CROSSPOST_SECRET` | Webhook认证密钥 |
| `YOUR TRACKER_SHEET_ID` | 用于跨平台发布跟踪的Google Sheets ID |
| `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID` | n8n的Google Sheets凭证ID |
| `YOUR_SMTP_CREDENTIAL_ID` | n8n的SMTP凭证ID |
| `YOUR_LINKEDIN_CREDENTIAL_ID` | n8n的LinkedIn OAuth凭证ID |
| `YOUR_LINKEDIN_PERSON_ID` | 您的LinkedIn个人资料URL |
| `YOUR_OPENAI_CREDENTIAL_ID` | n8n的OpenAI凭证ID |
| `YOUR_BLOG_DOMAIN` | 您博客的公共URL |
| `YOUR_FROM_EMAIL` | 用于发送摘要邮件的发件人邮箱 |
| `YOUR_NOTIFICATION_EMAIL` | 发送跨平台发布摘要的邮箱地址 |
| `YOUR_BLOG_ADMIN_HOST:3000` | 博客管理主机的地址（Docker或URL） |

## 快速入门

### 1. 先决条件
- n8n实例（版本2.4及以上）
- 具有API端点的博客
- Google Sheets OAuth2凭证
- 至少一个平台的API密钥

### 2. 配置平台
在工作流的“Platform Config”节点中设置您的API凭证：

```json
{
  "devto_api_key": "your-dev-to-api-key",
  "hashnode_token": "your-hashnode-token",
  "hashnode_publication_id": "your-pub-id",
  "linkedin_credential_id": "your-linkedin-oauth-id"
}
```

### 3. 设置跟踪表格
创建一个Google Sheets表格，包含以下列：
- `slug`（文本）——文章标识符
- `source`（文本）——博客名称（支持多博客）
- `date`（文本）——跨平台发布日期
- `platforms`（文本）——用逗号分隔的发布平台列表
- `status`（文本）——发布状态（成功/部分成功/失败）

### 4. 触发工作流
```bash
# Via webhook
curl -X POST https://your-n8n.com/webhook/blog-crosspost \
  -H "Content-Type: application/json" \
  -d '{"slug": "my-article", "lang": "en", "platforms": "all", "_secret": "your-secret"}'

# Or via blog admin (auto-triggers on first publish)
```

## 平台特定的格式化规则

### Dev.to
- 将HTML转换为Markdown格式。
- 添加指向原文的链接。
- 将文章分类映射到Dev.to的标签（最多4个）。
- 在文章开头添加封面图片。

### Hashnode
- 使用Markdown格式，并添加前置内容（frontmatter）。
- 提供指向原文的链接。
- 将分类映射到Hashnode的标签。
- 实现平台特定的发布功能。

### LinkedIn
- 使用纯文本格式，保留换行符（不使用Markdown格式）。
- 将文章内容截断至3000个字符。
- 包含指向原文的链接。
- 从文章标签中提取并添加相关标签。

### Pinterest
- 创建包含特色图片的Pin。
- 使用文章标题作为Pin的标题。
- 使用文章的元描述作为描述。
- 提供指向原文的链接。

## 去重机制

跟踪工具使用Google Sheets的`appendOrUpdate`功能，并通过`slug`和`source`进行去重：
- 首次发布时创建新行。
- 同一slug的重复发布会更新现有行（避免重复）。
- 不同博客的相同slug会分别记录在不同的行中（通过`source`区分）。

## 多博客支持

通过设置不同的`source`值，可以同时处理多个博客的内容：
- 博客A：`source: "my-tech-blog"`
- 博客B：`source: "my-business-blog"`
每个博客的内容都会在同一个表格中分别被记录。

## 使用场景

1. **个人博主**——一次编写，多平台发布。
2. **内容机构**——管理多个客户博客的跨平台发布。
3. **SEO策略**——自动在7个平台上建立链接网络。
4. **新闻通讯推广**——每个平台都能吸引订阅者订阅您的新闻通讯。

## 所需条件

- n8n版本2.4及以上（自托管或云服务）。
- 至少一个平台的API密钥。
- Google Sheets的API凭证。
- 访问博客管理API或文件系统以获取文章内容。

## 提示

- 从Dev.to和LinkedIn开始使用（投资回报率最高，设置最简单）。
- 逐步添加更多平台。
- 定期检查跟踪表格，及时处理发布失败的情况。
- 使用规范的URL可以避免内容重复带来的惩罚。
- 将跨平台发布安排在原文发布后1-2小时进行，以提高互动率。