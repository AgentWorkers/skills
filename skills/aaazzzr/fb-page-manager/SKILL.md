---
name: fb-page-poster
description: 通过 Meta Graph API 将帖子发布到 Facebook 页面。适用于用户请求“发布到 Facebook”、“在 Facebook 上发帖”、“在粉丝专页上发文”、“在社群中发帖”、“帮我发帖”、“安排帖子发布时间”或提供内容后要求“发布此内容”的情况。支持仅文本、图片、链接到评论中的内容、定时发布的帖子，以及中英文之间的多语言翻译（发布前需进行审核）。
version: 1.0.0
metadata: {"openclaw": {"emoji": "📘", "requires": {"env": ["LONG_META_page_TOKEN", "META_PAGE_ID", "META_APP_SECRET"], "bins": ["node"]}, "primaryEnv": "LONG_META_page_TOKEN"}}
---
# Facebook页面海报发布

通过Meta Graph API将内容发布到Facebook页面。

## 环境变量

| 变量 | 用途 |
|---|---|
| `LONG_META_PAGE_TOKEN` | 持久有效的页面访问令牌，具有`pages_manage_posts`和`pages_read_engagement`权限 |
| `META_PAGE_ID` | 页面的数字ID |
| `META_APP_SECRET` | 用于appsecret_proof的Meta应用密钥 |

如果缺少任何变量，请引导用户参考`{baseDir}/references/token-setup-guide.md`。

## 工作流程

### 1. 解析请求

从用户消息中提取以下信息：
- **内容**：要发布的文本
- **语言方向**：ZH→EN、EN→ZH、ZH→ZH或EN→EN
- **帖子类型**：文本 | 图片 | 评论中的链接 | 定时发布（可组合）
- **语气**：自动判断——推广和活动使用积极/促销的语气；公告和企业内容使用正式/专业的语气。如有疑问，请询问用户。
- **图片**：本地文件路径或URL（如适用）
- **时间安排**：ISO 8601时间戳（如适用）
- **链接**：第一个评论的URL（如适用）

### 2. 草拟并翻译内容——务必先预览

**未经用户确认，切勿发布内容。**

如果源语言与目标语言不同，请按照以下规则进行翻译：
- 保持意义和意图的准确性，以及标签的使用
- 自然地调整习语，不要逐字翻译
- 品牌名称和专有名词保持原样
- 除非在目标语言中不自然，否则保留表情符号的使用

展示预览内容：

```
📋 Post Preview
─────────────────
[Post text here]

🔗 First comment: [URL or N/A]
🖼️ Image: [filename/URL or N/A]
⏰ Schedule: [time or "Publish immediately"]
─────────────────
Confirm? (yes / edit / cancel)
```

### 3. 发布内容

运行位于`{baseDir}/scripts/fb-post.js`的脚本：

```bash
# Text-only
node {baseDir}/scripts/fb-post.js --type text --message "content"

# Image (file)
node {baseDir}/scripts/fb-post.js --type image --message "content" --image-file /path/to/img.jpg

# Image (URL)
node {baseDir}/scripts/fb-post.js --type image --message "content" --image-url "https://..."

# Link in first comment
node {baseDir}/scripts/fb-post.js --type text --message "content" --comment-link "https://..."

# Scheduled (append to any above)
node {baseDir}/scripts/fb-post.js --type text --message "content" --schedule "2025-12-25T10:00:00+0800"
```

这些选项可以组合使用。例如：图片 + 评论中的链接 + 定时发布：

```bash
node {baseDir}/scripts/fb-post.js --type image --message "content" --image-url "https://..." --comment-link "https://..." --schedule "2025-12-25T10:00:00+0800"
```

### 4. 报告结果

- 显示帖子ID
- 确认评论是否已发布（如果使用了评论中的链接）
- 确认预定发布时间（如果设置了定时发布）
- 发生错误时，显示错误信息并提供解决方法

## 错误参考

| 错误类型 | 可能原因 | 解决方法 |
|---|---|---|
| OAuthException / 无效令牌 | 令牌过期 | 请根据`{baseDir}/references/token-setup-guide.md`刷新令牌 |
| 权限被拒绝 | 缺少`pages_manage_posts`权限 | 重新授权令牌并设置正确的权限范围 |
| 预定发布时间过早 | 预定时间必须在未来10分钟以上 | 调整时间戳 |
| 图片过大 | 图片大小超过10 MB | 压缩或调整图片大小 |
| 请求频率限制 | 请求次数过多 | 等待几分钟后再尝试 |