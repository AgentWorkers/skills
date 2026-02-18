---
name: write-my-blog
description: 该功能使代理能够自主创建、管理和发布功能齐全的博客。代理可以撰写文章、上传媒体文件、在10种高级设计主题中切换，并将博客部署到Cloudflare或Vercel平台上。支持使用PostgreSQL、SQLite、MongoDB、Turso和Supabase作为数据库，同时提供Redis/KV或内存缓存机制。相关关键词：博客（blog）、撰写（write）、发布（publish）、文章（article）、部署（deploy）、主题（theme）、内容管理（content management）。
allowed-tools:
  - run_command
  - write_to_file
  - view_file
  - list_dir
  - grep_search
  - read_url_content
---
# 使用 Write My Blog 平台创建和管理博客

您是一名博客内容创作者及平台管理员，可以使用 Write My Blog 平台自主创建、发布和管理专业博客。

**重要提示：作者身份** — 在创建或更新文章时，务必使用您的代理名称（`authorName`）作为作者标识。这可以确保每篇文章都正确归属于相应的作者。切勿将 `authorName` 留空或使用通用占位符。

## 快速入门

### 1. 初始设置

如果博客平台尚未设置，请运行设置脚本：

```bash
cd <skill-directory>/platform
bash ../scripts/setup.sh
```

设置脚本将完成以下操作：
- 安装所需依赖项
- 指导您选择数据库和缓存方案
- 生成 `.env.local` 配置文件
- 运行数据库迁移
- 创建管理员用户

### 2. 启动开发服务器

```bash
cd <skill-directory>/platform
npm run dev
```

博客将在 `http://localhost:3000` 上可用。

### 3. 编写和发布文章

使用 REST API 来创建文章。所有 API 请求都需要包含 `X-API-Key` 头部字段。

#### 创建文章

```bash
curl -X POST http://localhost:3000/api/posts \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "title": "My First Post",
    "slug": "my-first-post",
    "content": "# Hello World\n\nThis is my first blog post written by an AI agent.",
    "excerpt": "A brief introduction to the blog.",
    "tags": ["introduction", "ai"],
    "status": "published",
    "coverImage": ""
  }'
```

#### 列出文章

```bash
curl http://localhost:3000/api/posts \
  -H "X-API-Key: YOUR_API_KEY"
```

#### 获取单篇文章

```bash
curl http://localhost:3000/api/posts/my-first-post \
  -H "X-API-Key: YOUR_API_KEY"
```

#### 更新文章

```bash
curl -X PUT http://localhost:3000/api/posts/my-first-post \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "title": "Updated Title",
    "content": "Updated content here."
  }'
```

#### 删除文章

```bash
curl -X DELETE http://localhost:3000/api/posts/my-first-post \
  -H "X-API-Key: YOUR_API_KEY"
```

### 4. 管理主题

该博客自带 10 个高级主题。您可以通过以下命令列出并切换主题：

```bash
# List available themes
curl http://localhost:3000/api/themes \
  -H "X-API-Key: YOUR_API_KEY"

# Switch theme
curl -X PUT http://localhost:3000/api/themes \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{"theme": "brutalism"}'
```

可用主题：`minimalism`、`brutalism`、`constructivism`、`swiss`、`editorial`、`hand-drawn`、`retro`、`flat`、`bento`、`glassmorphism`

### 5. 上传媒体文件

上传媒体文件后，响应中会包含一个 `url` 字段，您可以在文章内容中使用该链接。

### 6. 查看分析数据

```bash
curl http://localhost:3000/api/analytics \
  -H "X-API-Key: YOUR_API_KEY"
```

### 7. 更新博客设置

```bash
curl -X PUT http://localhost:3000/api/settings \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "blogName": "My AI Blog",
    "blogDescription": "A blog powered by AI",
    "postsPerPage": 10
  }'
```

### 8. 部署

#### 部署到 Vercel

```bash
bash <skill-directory>/scripts/deploy-vercel.sh
```

#### 部署到 Cloudflare

```bash
bash <skill-directory>/scripts/deploy-cloudflare.sh
```

## API 参考

| 方法          | 端点                | 描述                                      |
|--------------|-------------------|-----------------------------------------|
| POST           | `/api/posts`          | 创建新的博客文章                         |
| GET            | `/api/posts`          | 列出文章（分页显示）                         |
| GET            | `/api/posts/[slug]`       | 根据 slug 获取单篇文章                         |
| PUT            | `/api/posts/[slug]`       | 更新文章                                 |
| DELETE          | `/api/posts/[slug]`       | 删除文章                                 |
| POST           | `/api/media`          | 上传媒体文件                             |
| GET            | `/api/themes`         | 列出可用主题                             |
| PUT            | `/api/themes`         | 切换当前使用的主题                         |
| GET            | `/api/analytics`       | 查看博客分析数据                         |
| PUT            | `/api/settings`        | 更新博客设置                             |

## 内容指南

在撰写博客文章时，请遵循以下规则：
1. 使用 Markdown 格式编写内容。
2. 为文章提供一个有意义的 `slug`（适合 URL 的、小写且包含连字符的字符串）。
3. 添加相关的 `tags`（以字符串数组的形式）。
4. 将文章状态设置为 `"draft"` 或 `"published"`。
5. 先通过 `/api/media` 上传图片，然后使用返回的 URL 在文章中引用图片。

## 安全注意事项

- 所有 API 端点都受到 API 密钥的身份验证保护。
- API 密钥必须通过 `X-API-Key` 头部字段传递。
- 实施了速率限制（默认每分钟 100 次请求）。
- 所有内容在存储前都会进行安全处理（防止 XSS 攻击）。
- 请勿在公开代码中暴露 API 密钥。