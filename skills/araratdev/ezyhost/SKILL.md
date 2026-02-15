# EzyHost — 代理技能

本文档介绍了AI代理如何通过编程方式与EzyHost进行交互。
如需了解人类用户的使用指南，请访问 [ezyhost.io](https://ezyhost.io)。

## 基本URL

```
https://ezyhost.io/api
```

## 认证

所有API请求都需要在请求头中传递API密钥：

```
x-api-key: YOUR_API_KEY
```

您可以在 `https://ezyhost.io/dashboard/api-keys` 生成您的API密钥。

**注意：** 使用API需要“Solo”计划或更高级别的计划。

---

## 端点

### 项目

#### 列出项目
```
GET /api/projects
```
返回：`{ projects: [{ id, name, slug, subdomain, customDomain, status, storageUsed, seoScore, deployedAt, _count: { files, analytics } }] }`

#### 创建项目
```
POST /api/projects
Content-Type: application/json
Body: { "name": "my-site", "subdomain": "my-site" }
```
返回：`{ project: { id, name, subdomain, s3Prefix, url, ... } }`

子域名必须由3个或更多字符组成，可以是小写字母、数字和连字符。您的网站将托管在 `https://{subdomain}.ezyhost.site` 上。

#### 获取项目信息
```
GET /api/projects/:id
```
返回：`{ project: { id, name, subdomain, customDomain, status, storageUsed, seoScore, files: [...], ... } }`

#### 更新项目
```
PATCH /api/projects/:id
Content-Type: application/json
Body: { "name": "new-name", "metaTitle": "...", "metaDescription": "..." }
```

#### 删除项目
```
DELETE /api/projects/:id
```
将项目及其所有关联文件从存储中删除。此操作不可撤销。

---

### 文件上传

#### 上传文件（ZIP格式或单个文件）
```
POST /api/upload/:projectId
Content-Type: multipart/form-data
Body: files (multipart)
```
返回：`{ message, filesUploaded, totalSize, project: { id, subdomain } }`

支持上传`.zip`压缩包（会自动解压）和单个文件。所有上传的文件都会经过恶意软件扫描（ClamAV + 魔术字节验证）。

**支持的文件类型：** HTML、CSS、JS、JSON、XML、SVG、图片（PNG、JPG、GIF、WebP、AVIF、ICO）、PDF、演示文稿（PPTX）、文档（DOCX、XLSX）、音频（MP3、WAV、OGG、FLAC、AAC）、视频（MP4、WebM、MOV）、字体（WOFF、WOFF2、TTF、OTF、EOT）、压缩包（ZIP）以及任何其他静态资源。

**禁止上传的文件类型：** 可执行文件（.exe、.dll、.bat、.sh、.php、.asp、.jar）。

#### 获取预签名的上传URL
```
POST /api/upload/:projectId/presign
Content-Type: application/json
Body: { "filename": "video.mp4", "contentType": "video/mp4" }
```
返回：`{ uploadUrl, s3Key }` — 用于直接将大文件上传到S3。

#### 删除文件
```
DELETE /api/upload/:projectId/files/:fileId
```

#### 批量删除文件
```
POST /api/upload/:projectId/files/bulk-delete
Content-Type: application/json
Body: { "fileIds": ["id1", "id2", "id3"] }
```

#### 重命名文件
```
PATCH /api/upload/:projectId/files/:fileId
Content-Type: application/json
Body: { "newPath": "assets/renamed-file.png" }
```

---

### SEO

#### 获取SEO报告
```
GET /api/seo/:projectId
```
返回：`{ score, suggestions: [{ id, type, severity, message, resolved }] }`

#### 运行SEO分析
```
POST /api/seo/:projectId/analyze
```
触发新的SEO扫描并返回更新后的建议。

#### 解决SEO问题
```
PATCH /api/seo/suggestion/:id/resolve
```

#### AI自动修复SEO问题
```
POST /api/seo/:projectId/ai-fix
Content-Type: application/json
Body: { "suggestionIds": ["id1", "id2"] }
```
使用AI自动修复HTML文件中的SEO问题。此操作会消耗AI生成次数。

---

### 分析

#### 获取分析数据
```
GET /api/analytics/:projectId?period=7d
```
可选时间周期：`24小时`、`7天`、`30天`、`90天`

返回：`{ totalVisits, visitsByDay: [{ date, visits }], topPages: [{ path, visits }], topReferrers: [{ referrer, visits }], topCountries: [{ country, visits }] }`

#### 跟踪事件（服务器端）
```
POST /api/analytics/track
Content-Type: application/json
Body: { "projectId": "...", "path": "/page", "referrer": "...", "userAgent": "..." }
```

---

### 域名

#### 添加自定义域名
```
POST /api/domains/:projectId
Content-Type: application/json
Body: { "domain": "example.com" }
```
返回：`{ dnsInstructions: { type, name, value } }` — 需要创建的DNS记录。

需要“Solo”计划或更高级别的计划。

#### 验证域名DNS
```
GET /api/domains/:projectId/verify
```
返回：`{ verified: true/false, dnsInstructions }`。在设置DNS记录后调用此接口。

#### 删除域名
```
DELETE /api/domains/:projectId
```

---

### AI构建器

#### 通过AI生成/编辑网站
```
POST /api/aibuilder/chat
Content-Type: application/json
Body: { "message": "build a portfolio site", "history": [], "currentFiles": [] }
```
返回**SSE流**，其中包含以下事件：
- `status` — 进度更新（例如：“生成HTML...”）
- `progress` — 完成百分比（0-100）
- `done` — 生成的文件列表（`{ files: [{ filename, content }] }`）
- `error` — 失败时的错误信息

此操作会消耗AI生成次数。

#### 部署AI生成的文件
```
POST /api/aibuilder/deploy/:projectId
Content-Type: application/json
Body: { "files": [{ "filename": "index.html", "content": "<!DOCTYPE html>..." }] }
```

#### 以ZIP格式下载
```
POST /api/aibuilder/download-zip
Content-Type: application/json
Body: { "files": [{ "filename": "index.html", "content": "..." }] }
```
提供ZIP文件的下载链接。

#### 模板
```
GET    /api/aibuilder/templates           — list saved templates
GET    /api/aibuilder/templates/:id       — get template details
POST   /api/aibuilder/templates           — save new template
PATCH  /api/aibuilder/templates/:id       — update template
DELETE /api/aibuilder/templates/:id       — delete template
```

模板示例：
```json
{
  "name": "我的模板",
  "description": "...",
  "messages": [...],
  "files": [...]
}
```

---

### API密钥

#### 获取当前密钥
```
GET /api/apikey
```
返回：`{ hasKey: true/false, apiKey: "ezy_****..." }` — 密钥部分被屏蔽。

#### 生成新密钥
```
POST /api/apikey/generate
```
返回：`{ apiKey: "ezy_..." }` — 新密钥仅显示一次，会撤销之前的密钥。

#### 撤销密钥
```
DELETE /api/apikey
```

---

### 计费

#### 获取计费信息
```
GET /api/billing
```
返回：`{ plan, subscription, aiCredits, usage }`

#### 获取AI使用情况
```
GET /api/billing/ai-usage
```
返回：`{ used, limit, remaining, resetsAt }`

---

## 计划限制

| 功能 | 免费 | Tiny（$5） | Solo（$13） | Pro（$31） | Pro Max（$74） |
|---------|------|-----------|------------|-----------|---------------|
| 项目数量 | 1 | 1 | 5 | 15 | 无限 |
| 存储空间 | 10 MB | 25 MB | 每个项目75 MB | 10 GB | 2 TB |
| 每月访问量 | 1K | 10K | 100K | 500K | 无限 |
| 支持的文件类型 | 基本类型 | 所有类型 | 所有类型 | 所有类型 | 所有类型 |
| 自定义域名 | 不支持 | 不支持 | 支持 | 支持 | 支持 |
| API访问 | 不支持 | 不支持 | 支持 | 支持 | 支持 |
| AI生成次数 | 每月3次 | 每月15次 | 每月50次 | 每月150次 | 每月500次 |
| 去除品牌标识 | 不支持 | 支持 | 支持 | 支持 | 支持 |

---

## 托管网站URL

网站托管地址：
- **免费子域名：** `https://{subdomain}.ezyhost.site`
- **自定义域名：** `https://{your-domain.com}`（仅限“Solo”及以上计划）

所有网站均提供HTTPS、CDN缓存以及针对非HTML项目的自动浏览器支持。

---

## 错误响应

所有错误都会以JSON格式返回：
```json
{ "error": "Description of the error" }
```

计划限制相关的错误会包含 `"upgrade": true`，表示需要升级到更高级别的计划。

常见的HTTP状态码：
- `400` — 请求错误/验证失败
- `401` — 未授权
- `403` — 达到计划限制
- `404` — 资源未找到
- `429` — 请求频率限制
- `500` — 服务器错误

---

## 请求频率限制

- **通用API：** 每个API密钥每15分钟300次请求
- **文件上传：** 每秒2次请求
- **AI构建器：** 受计划生成的次数限制

---

## 示例：部署静态网站
```bash
# 1. Create a project
curl -X POST https://ezyhost.io/api/projects \
  -H "x-api-key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-site", "subdomain": "my-site"}'

# 2. Upload files (ZIP)
curl -X POST https://ezyhost.io/api/upload/PROJECT_ID \
  -H "x-api-key: YOUR_KEY" \
  -F "files=@site.zip"

# 3. Check SEO
curl https://ezyhost.io/api/seo/PROJECT_ID \
  -H "x-api-key: YOUR_KEY"

# 4. Add custom domain (optional, Solo+)
curl -X POST https://ezyhost.io/api/domains/PROJECT_ID \
  -H "x-api-key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'
```

您的网站现已上线，地址为 `https://my-site.ezyhost.site`

## 示例：使用AI生成并部署网站
```bash
# 1. Generate a site with AI (SSE stream)
curl -N -X POST https://ezyhost.io/api/aibuilder/chat \
  -H "x-api-key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message": "build a modern portfolio with dark theme", "history": []}'

# 2. Deploy the generated files to a project
curl -X POST https://ezyhost.io/api/aibuilder/deploy/PROJECT_ID \
  -H "x-api-key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"files": [{"filename": "index.html", "content": "..."}]}'
```