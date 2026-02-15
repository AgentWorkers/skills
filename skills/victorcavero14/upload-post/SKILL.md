---
name: upload-post
description: "通过 Upload-Post API 将内容上传到社交媒体平台。适用于将视频、照片、文本或文档发布到 TikTok、Instagram、YouTube、LinkedIn、Facebook、X（Twitter）、Threads、Pinterest、Reddit 或 Bluesky。该 API 支持定时上传、数据分析、FFmpeg 处理以及上传历史记录的记录功能。"
---

# Upload-Post API

通过一个API调用，将内容发布到多个社交媒体平台。

## 文档说明

- 完整的API文档：https://docs.upload-post.com
- 适合大型语言模型（LLM）使用的文档：https://docs.upload-post.com/llm.txt

## 设置流程

1. 在 [upload-post.com](https://upload-post.com) 注册账户。
2. 连接您的社交媒体账户。
3. 创建一个 **个人资料**（例如：“mybrand”）——该资料将关联您的所有已连接的社交媒体账户。
4. 从控制面板生成一个 **API密钥**。
5. 在API调用中使用个人资料名称作为 `user` 参数。

## 认证

```
Authorization: Apikey YOUR_API_KEY
```

基础URL：`https://api.upload-post.com/api`

所有端点中的 `user` 参数指的是您的 **个人资料名称**（而非用户名），该名称决定了哪些已连接的社交媒体账户会接收内容。

## 端点参考

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/upload_videos` | POST | 上传视频 |
| `/upload_photos` | POST | 上传照片/轮播图 |
| `/upload_text` | POST | 仅上传文本的帖子 |
| `/upload_document` | POST | 上传文档（仅限LinkedIn） |
| `/uploadposts/status?request_id=X` | GET | 查看异步上传状态 |
| `/uploadposts/history` | GET | 查看上传历史记录 |
| `/uploadposts/schedule` | GET | 列出已安排的帖子 |
| `/uploadposts/schedule/<job_id>` | DELETE | 取消已安排的帖子 |
| `/uploadposts/schedule/<job_id>` | PATCH | 修改已安排的帖子 |
| `/uploadposts/me` | GET | 验证API密钥 |
| `/analytics/<profile>` | GET | 获取分析数据 |
| `/uploadposts/facebook/pages` | GET | 列出Facebook页面 |
| `/uploadposts/linkedin/pages` | GET | 列出LinkedIn页面 |
| `/uploadposts/pinterest/boards` | GET | 列出Pinterest板块 |
| `/uploadposts/reddit/detailed_posts` | GET | 获取包含媒体的Reddit帖子 |
| `/ffmpeg` | POST | 使用FFmpeg处理媒体文件 |

## 上传视频

```bash
curl -X POST "https://api.upload-post.com/api/upload_videos" \
  -H "Authorization: Apikey YOUR_KEY" \
  -F "user=profile_name" \
  -F "platform[]=instagram" \
  -F "platform[]=tiktok" \
  -F "video=@video.mp4" \
  -F "title=My caption"
```

关键参数：
- `user`：个人资料用户名（必填）
- `platform[]`：目标平台（必填）
- `video`：视频文件或URL（必填）
- `title`：标题（必填）
- `description`：详细描述 |
- `scheduled_date`：用于安排的ISO-8601格式日期 |
- `timezone`：IANA时区（例如：“Europe/Madrid”） |
- `async_upload`：设置为 `true` 以进行后台处理 |
- `first_comment`：自动发布第一条评论 |

## 上传照片

```bash
curl -X POST "https://api.upload-post.com/api/upload_photos" \
  -H "Authorization: Apikey YOUR_KEY" \
  -F "user=profile_name" \
  -F "platform[]=instagram" \
  -F "photos[]=@photo1.jpg" \
  -F "photos[]=@photo2.jpg" \
  -F "title=My caption"
```

Instagram和Threads支持混合轮播图（同一帖子中包含照片和视频）。

## 上传文本

```bash
curl -X POST "https://api.upload-post.com/api/upload_text" \
  -H "Authorization: Apikey YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user": "profile_name",
    "platform": ["x", "threads", "bluesky"],
    "title": "My text post"
  }'
```

支持的平台：X、LinkedIn、Facebook、Threads、Reddit、Bluesky。

## 上传文档（仅限LinkedIn）

可以上传PDF、PPT、DOC格式的文档，并以LinkedIn原生的文档形式发布（支持轮播图查看）。

```bash
curl -X POST "https://api.upload-post.com/api/upload_document" \
  -H "Authorization: Apikey YOUR_KEY" \
  -F "user=profile_name" \
  -F 'platform[]=linkedin' \
  -F "document=@presentation.pdf" \
  -F "title=Document Title" \
  -F "description=Post text above document"
```

参数：
- `document`：PDF、PPT、PPTX、DOC、DOCX格式的文件（最大100MB，300页）
- `title`：文档标题（必填）
- `description`：帖子说明 |
- `visibility`：公开、仅限联系人查看、仅限登录用户查看、容器模式 |
- `target_linkedin_page_id`：目标LinkedIn页面ID

## 支持的平台

| 平台 | 视频 | 照片 | 文本 | 文档 |
|----------|--------|--------|------|-----------|
| TikTok | ✓ | ✓ | - | - |
| Instagram | ✓ | ✓ | - | - |
| YouTube | ✓ | - | - | - |
| LinkedIn | ✓ | ✓ | ✓ | ✓ |
| Facebook | ✓ | ✓ | ✓ | - |
| X（Twitter） | ✓ | ✓ | ✓ | - |
| Threads | ✓ | ✓ | ✓ | - |
| Pinterest | ✓ | ✓ | - | - |
| Reddit | - | ✓ | ✓ | - |
| Bluesky | ✓ | ✓ | ✓ | - |

## 查看上传历史记录

```bash
curl "https://api.upload-post.com/api/uploadposts/history?page=1&limit=20" \
  -H "Authorization: Apikey YOUR_KEY"
```

参数：
- `page`：页面编号（默认：1）
- `limit`：10、20、50或100（默认：10）

返回内容：上传时间戳、平台、上传状态、帖子链接以及错误信息。

## 安排上传

通过添加 `scheduled_date` 参数（ISO-8601格式）来安排上传：

```json
{
  "scheduled_date": "2026-02-01T10:00:00Z",
  "timezone": "Europe/Madrid"
}
```

响应中包含 `job_id`。可以通过以下接口进行管理：
- `GET /uploadposts/schedule` - 列出所有已安排的上传任务 |
- `DELETE /uploadposts/schedule/<job_id>` - 取消已安排的上传任务 |
- `PATCH /uploadposts/schedule/<job_id>` - 修改已安排的上传任务（日期、标题、描述等）

## 查看上传状态

对于异步上传或已安排的帖子，可以使用以下接口：

```bash
curl "https://api.upload-post.com/api/uploadposts/status?request_id=XXX" \
  -H "Authorization: Apikey YOUR_KEY"
```

或者使用 `job_id` 来查询已安排的帖子状态。

## 分析数据

```bash
curl "https://api.upload-post.com/api/analytics/profile_name?platforms=instagram,tiktok" \
  -H "Authorization: Apikey YOUR_KEY"
```

支持的平台：Instagram、TikTok、LinkedIn、Facebook、X、YouTube、Threads、Pinterest、Reddit、Bluesky。

返回数据：关注者数量、曝光次数、 reach量、个人资料浏览量以及时间序列数据。

## 获取页面/板块信息

```bash
# Facebook Pages
curl "https://api.upload-post.com/api/uploadposts/facebook/pages" \
  -H "Authorization: Apikey YOUR_KEY"

# LinkedIn Pages  
curl "https://api.upload-post.com/api/uploadposts/linkedin/pages" \
  -H "Authorization: Apikey YOUR_KEY"

# Pinterest Boards
curl "https://api.upload-post.com/api/uploadposts/pinterest/boards" \
  -H "Authorization: Apikey YOUR_KEY"
```

## 获取Reddit详细帖子信息

可以获取包含完整媒体信息的Reddit帖子：

```bash
curl "https://api.upload-post.com/api/uploadposts/reddit/detailed-posts?profile_username=myprofile" \
  -H "Authorization: Apikey YOUR_KEY"
```

返回最多2000条包含媒体链接、尺寸和缩略图的帖子。

## 使用FFmpeg编辑媒体文件

```bash
curl -X POST "https://api.upload-post.com/api/ffmpeg" \
  -H "Authorization: Apikey YOUR_KEY" \
  -F "file=@input.mp4" \
  -F "full_command=ffmpeg -y -i {input} -c:v libx264 -crf 23 {output}" \
  -F "output_extension=mp4"
```

- 使用 `{input}` 和 `{output}` 占位符来指定输入和输出文件路径。
- 监控任务状态，直到任务完成（状态变为 `FINISHED`）。
- 从 `/ffmpeg/job/<job_id>/download` 下载处理结果。
- 支持多个输入文件：`{input0}`、`{input1}` 等。

流量限制：
- 免费账户：每月30分钟；
- 基础账户：300分钟；
- 专业账户：1000分钟；
- 高级账户：3000分钟；
- 商业账户：10000分钟。

## 平台特定参数

详细平台参数请参阅 [references/platforms.md](references/platforms.md)。

## 媒体格式要求

具体媒体格式要求请参阅 [references/requirements.md](references/requirements.md)。

## 错误代码

| 代码 | 含义 |
|------|---------|
| 400 | 请求错误 / 缺少参数 |
| 401 | API密钥无效 |
| 404 | 资源未找到 |
| 429 | 超过流量限制 |
| 500 | 服务器错误 |

## 其他说明

- 如果视频处理时间超过59秒，系统会自动选择异步上传方式。
- 如果 `x_long_text_as_post` 参数设置为 `true`，长文本会以帖子形式发布。
- Facebook要求提供页面ID（个人资料无法使用此功能）。
- Instagram和Threads支持混合轮播图（照片和视频）。