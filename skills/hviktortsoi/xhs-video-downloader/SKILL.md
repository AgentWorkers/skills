---
name: xiaohongshu-downloader
description: 从小红书页面下载视频。适用于用户需要从 xiaohongshu.com 网址保存或下载视频的情况，或者当用户提到“小红书视频下载”、“保存小红书视频”等类似需求时使用。
---
# 小红书视频下载器

通过从页面中提取实际的CDN URL来下载小红书上的视频。

## 工作原理

小红书上的视频在浏览器中使用了特殊的 blob URL，这些 URL 无法直接下载。本工具通过以下步骤实现视频下载：

1. 使用浏览器自动化技术加载页面（这是渲染 JavaScript 内容所必需的）。
2. 从页面的 HTML 代码中提取实际的 CDN 视频 URL。
3. 使用正确的请求头（headers）下载视频。

## 方法 1：浏览器自动化（推荐）

使用浏览器工具提取视频 URL：

1. 访问小红书页面：
```
browser action=navigate targetUrl="https://www.xiaohongshu.com/explore/NOTE_ID"
```

2. 使用 JavaScript 提取视频 URL：
```javascript
(() => {
  const html = document.documentElement.outerHTML;
  const mp4Matches = html.match(/https?:\/\/[^"\s]+\.mp4[^"\s]*/g);
  if (mp4Matches) return [...new Set(mp4Matches)];
  return null;
})()
```

3. 使用 curl 命令下载视频：
```bash
curl -L -o output.mp4 "<VIDEO_URL>" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -H "Referer: https://www.xiaohongshu.com/"
```

## 方法 2：Python 脚本

对于不需要身份验证的页面，可以使用以下 Python 脚本进行下载：

```bash
python3 scripts/download_video.py "https://www.xiaohongshu.com/explore/NOTE_ID"
```

注意：由于以下原因，该 Python 脚本可能无法适用于所有页面：
- 需要 JavaScript 进行页面渲染。
- 需要用户身份验证或登录。
- 遭遇速率限制（rate limiting）。

## 注意事项：

- 视频通常托管在 `xhscdn.com` 这个 CDN 服务器上。
- 为了避免 403 错误，必须设置正确的 `User-Agent` 和 `Referer` 请求头。
- 下载视频的目录为：`~/Downloads/xiaohongshu/`。
- 视频 URL 的格式为：`https://sns-video-*.xhscdn.com/stream/.../*.mp4`