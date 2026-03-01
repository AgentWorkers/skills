---  
**名称：facebook-page**  
**描述：** 通过 Meta Graph API 与 Facebook 页面的任何功能进行交互。当用户需要发布内容、安排发布时间、删除帖子、回复评论、查看收件箱、分析页面数据、管理事件、上传视频、审核评论或执行其他与 Facebook 页面相关的操作时，可以使用该技能。该技能不会局限于预设的命令，而是会根据用户的实际需求自动选择合适的 API 调用。如果缺少某些权限，系统会明确告知用户需要添加哪些权限以及在哪里添加这些权限。  
**元数据：**  
`{"openclaw":{"emoji":"[fb]"}`  

# **facebook-page** — 通用 Meta Graph API 技能  
该技能会根据用户的操作需求，直接构建并执行 Meta Graph API 调用，无需编写额外的脚本。  

**API 版本：** **v25.0**  
**基础 URL：** `https://graph.facebook.com/v25.0`  

---

## **步骤 1：加载凭据**  
凭据存储在 `~/.config/fb-page/credentials.json` 文件中。  
**（如果文件不存在，请指导用户完成设置。）**  
**所需字段：**  
| 字段 | 用途 |  
| --- | --- |  
| `FB_PAGE_TOKEN` | 永不过期的页面访问令牌，用于所有 API 调用 |  
| `FB_PAGE_ID` | Facebook 页面的数字 ID |  
| `FB_APP_ID` | Meta 应用程序 ID（仅在令牌交换时需要） |  
| `FB_APP_SECRET` | Meta 应用程序密钥（仅在令牌交换时需要） |  

**一次性令牌交换设置：**  
（具体步骤请参考相关文档。）  

**保存文件后，请立即限制对该文件的访问权限：**  
（具体操作请参考相关文档。）  

> ⚠️ 请勿将此文件提交到版本控制系统中，因为它包含长期有效的敏感信息。  
> 该技能仅向 `graph.facebook.com` 发送请求，不会将任何数据转发给第三方。  

---

## **步骤 2：确定 API 调用方式**  
### 常见 API 端点  
| 用户操作 | 方法 | 端点 |  
| --- | --- | --- |  
| 发布文本 | POST | `/$pageId/feed` — 请求体：`message` |  
| 发布带图片的帖子 | POST | `/$pageId/photos` — 多部分请求：`source` + `message` |  
| 发布带视频的帖子 | POST | `/$pageId/videos` — 多部分请求：`source` + `description` |  
| 发布带链接的帖子 | POST | `/$pageId/feed` — 请求体：`message` + `link` |  
| 删除帖子 | DELETE | `/{post-id}` |  
| 安排帖子发布时间 | POST | `/$pageId/feed` — 请求体：`message` + `published=false` + `scheduled_publish_time`（Unix 时间戳） |  
| 获取最新帖子 | GET | `/$pageId/published_posts?fields=id,message,created_time&limit=10` |  
| 获取页面信息 | GET | `/$pageId?fields=name,fan_count,followers_count,about` |  
| 点赞帖子 | POST | `/{post-id}/likes` |  
| 获取评论 | GET | `/{post-id}/comments?fields=message,from,created_time` |  
| 回复评论 | POST | `/{comment-id}/comments` — 请求体：`message` |  
| 隐藏评论 | POST | `/{comment-id}` — 请求体：`is_hidden=true` |  
| 删除评论 | DELETE | `/{comment-id}` |  
| 获取页面分析数据 | GET | `/$pageId/insights?metric=page_fans,page_impressions&period=day` |  
| 获取帖子分析数据 | GET | `/{post-id}/insights?metric=post_impressions,post_reactions_by_type_total` |  
| 列出事件 | GET | `/$pageId/events?fields=name,start_time,description` |  
| 创建事件 | POST | `/$pageId/events` — 请求体：`name`, `start_time`, `description` |  
| 列出相册 | GET | `/$pageId/albums?fields=name,count` |  
| 获取页面角色信息 | GET | `/$pageId/roles` |  
| 发布草稿帖子 | POST | `/{post-id}` — 请求体：`is_published=true` |  

### API 调用模式  
- **GET 请求：** （具体代码请参考相关文档。）  
- **POST 请求（请求体格式）：** （具体代码请参考相关文档。）  
- **DELETE 请求：** （具体代码请参考相关文档。）  
- **多部分数据上传（图片/视频）：** （具体代码请参考相关文档。）  
- **安排帖子发布时间（将本地时间转换为 Unix 时间戳）：** （具体代码请参考相关文档。）  

---

## **步骤 3：处理错误**  
**错误代码及含义及解决方法：**  
| 代码 | 子代码 | 含义 | 解决方案 |  
| --- | --- | --- | --- |  
| 100 | — | 参数无效 | 检查参数值是否正确。 |  
| 102 | — | 会话过期 | 重新运行设置以获取新的令牌。 |  
| 190 | 460 | 令牌过期 | 使用新的临时令牌重新运行设置。 |  
| 190 | 467 | 令牌无效 | 重新运行设置。 |  
| 200 | — | 权限被拒绝 | 在应用程序中添加 `error.message` 中列出的权限。 |  
| 10 | — | 权限被拒绝（针对特定页面） | 添加 `pages_read_engagement` 或 `pages_manage_posts` 权限。 |  
| 230 | — | 需要重新登录 | 重新运行设置。 |  
| 368 | — | 被暂时限制访问 | 等待片刻后重试；可能是由于频率限制。 |  

### 权限参考  
| 权限 | 所需操作 |  
| --- | --- | --- |  
| `pages_manage_posts` | 创建、删除、安排帖子发布 |  
| `pages_read_engagement` | 阅读帖子、点赞、评论、分析页面数据 |  
| `pages_show_list` | 列出你管理的页面 |  
| `pages_manage_metadata` | 更新页面设置 |  
| `pages_manage_comments` | 审核评论、回复评论 |  
| `pages_read_user_content` | 阅读访客发布的帖子和评论 |  
| `pages_manage_ads` | 管理页面上的广告活动 |  
| `pages_manage_instant_articles` | 管理 Instant Articles 内容 |  

**如果缺少权限：**  
1. 访问 [Meta for Developers](https://developers.facebook.com/apps/)  
2. 选择你的应用程序 → “权限和功能”  
3. 添加所需的权限  
4. 通过 [Graph API Explorer](https://developers.facebook.com/tools/explorer/) 生成新的令牌  
5. 使用新令牌重新运行设置。  

---

**代理规则：**  
- **始终先加载凭据。** 如果凭据缺失或不完整，指导用户完成设置。  
- **API 调用时仅使用 `FB_PAGE_TOKEN` 和 `FB_PAGE_ID`；`FB_APP_ID` 和 `FB_APP_SECRET` 仅用于令牌交换。**  
- **不要在凭据文件中写入额外的字段（如页面所有者 ID、会话 ID 或第三方密钥）。**  
- **令牌交换完成后，从 `credentials.json` 文件中删除 `FB_APP_SECRET`（因为 API 调用不再需要它）。**  
- **最小权限原则**：仅请求实际操作所需的权限。除非必要，否则不要请求 `pages_manage_ads` 或 `pages_manage_instant_articles`。  
- **定期通过 Graph API Explorer 更换 `FB_PAGE_TOKEN`；如果系统被入侵，立即更换令牌。**  
- **所有 API 调用仅通过 `graph.facebook.com` 发送，不得转发给第三方服务。**  
- **根据用户的操作需求直接构建 API 调用，不要依赖脚本文件。**  
- **遇到错误时**：解析 `error.code` 和 `error.error_subcode`，根据上述规则告知用户具体解决方法。  
- **如果缺少权限**：向用户说明具体权限名称，并提供 [Meta for Developers] 的相关链接，建议用户重新运行设置。