---
name: x-extract
description: >
  **使用浏览器自动化从 x.com URL 中提取推文内容（无需认证）**  
  当用户请求“提取推文”、“下载 x.com 链接”或提供 x.com/twitter.com URL 以供内容提取时，可以使用该方法。该方法无需 Twitter API 认证即可正常工作。
---
# 从 x.com 提取推文信息

无需 Twitter/X 账户凭证，即可从 x.com 的 URL 中提取推文内容（文本、媒体、作者和元数据）。

## 工作原理

使用 OpenClaw 的浏览器工具加载推文页面，然后从渲染后的 HTML 中提取内容。

## 工作流程

### 1. 验证 URL

检查 URL 是否为有效的 x.com 或 twitter.com 推文链接：
- 必须包含 `x.com/*/status/` 或 `twitter.com/*/status/`
- 从 URL 模式中提取推文 ID：`/status/(\d+)`

### 2. 在浏览器中打开页面

```javascript
browser action=open profile=openclaw targetUrl=<x.com-url>
```

等待页面加载（返回 `targetId`）。

### 3. 捕获页面快照

```javascript
browser action=snapshot targetId=<TARGET_ID> snapshotFormat=aria
```

### 4. 提取内容

从页面快照中提取以下信息：

**必填字段：**
- **推文文本**：查找包含推文主要内容的部分（通常标记为 `role=article`）
- **作者**：查找作者名称/链接（通常采用 `@username` 格式）
- **时间戳**：查找时间戳元素（标记为 `role=time`）

**可选字段：**
- **媒体**：查找包含图片（`role=img`）或视频（`role=video`）的链接
- **互动信息**：点赞数、转发数、回复数（标记为 `role=group` 或 `role=button`）
- **推文线程信息**：如果推文属于某个线程，记录前一条/下一条推文的链接

### 5. 格式化输出

将提取到的信息以结构化的 Markdown 格式输出：

```markdown
# Tweet by @username

**Author:** Full Name (@handle)  
**Posted:** YYYY-MM-DD HH:MM  
**Source:** <original-url>

---

<Tweet text content here>

---

**Media:**
- ![Image 1](<media-url-1>)
- ![Image 2](<media-url-2>)

**Engagement:**
- 👍 Likes: 1,234
- 🔄 Retweets: 567
- 💬 Replies: 89

**Thread:** [Part 2/5] | [View full thread](<thread-url>)
```

### 6. 下载媒体（可选）

如果用户请求 `--download-media` 或 “下载图片”：
1. 从页面快照中提取所有媒体链接
2. 使用 `exec` 和 `curl` 或 `wget` 下载媒体文件：
   ```bash
   curl -L -o "tweet-{tweetId}-image-{n}.jpg" "<media-url>"
   ```
3. 显示已下载文件的路径

## 错误处理

**如果页面无法加载：**
- 检查 URL 是否有效
- 尝试使用 `twitter.com` 作为替代地址（仍然可行）
- 有些推文可能需要登录才能查看（存在争议或受年龄限制）——请告知用户

**如果内容提取失败：**
- x.com 的页面布局可能发生了变化——请参考 [references/selectors.md] 以获取最新的 CSS/ARIA 选择器
- 向用户提供原始的页面快照以便手动检查
- 报告哪些字段成功提取到了内容

## 常用选择器

详细的使用 CSS/ARIA 选择器的信息请参见 [references/selectors.md](references/selectors.md)（会随着页面布局的更新而更新）。

## 限制

- **无需凭证**：无法访问受保护的推文、私信或需要登录的内容
- **速率限制**：x.com 可能会限制过多的自动化请求
- **页面布局变化**：如果 x.com 修改了 HTML 结构，选择器可能失效
- **动态内容**：部分内容（如评论、推文线程）可能不会立即显示

## 示例

**提取单条推文：**
```
User: "Extract this tweet: https://x.com/vista8/status/2019651804062241077"
Agent: [Opens browser, captures snapshot, formats markdown output]
```

**提取包含媒体的推文并下载媒体：**
```
User: "Get the tweet text and download all images from https://x.com/user/status/123"
Agent: [Extracts content, downloads images to ./downloads/, reports paths]
```

**提取推文线程：**
```
User: "Extract this thread: https://x.com/user/status/456"
Agent: [Detects thread, extracts all tweets in sequence, formats as numbered list]
```