---
name: GIF
description: 查找、搜索并创建经过适当优化和具备良好可访问性的 GIF 图像。
metadata: {"clawdbot":{"emoji":"🎞️","requires":{},"os":["linux","darwin","win32"]}}
---

## 在哪里找到GIF图片

| 网站 | 适用场景 | 是否支持API |
|------|----------|-----|
| **Giphy** | 通用图片、热门图片 | 支持API |
| **Tenor** | 消息应用（WhatsApp、Slack、Discord） | 支持API |
| **Imgur** | 病毒式传播的图片/社区内容 | 支持API |
| **Reddit r/gifs** | 小众、独特的GIF图片 | 不支持API |
| **用于表达情绪的GIF** | 不支持API |

## Giphy API

```bash
# Search
curl "https://api.giphy.com/v1/gifs/search?api_key=KEY&q=thumbs+up&limit=10"

# Trending
curl "https://api.giphy.com/v1/gifs/trending?api_key=KEY&limit=10"
```

返回的图片格式：`original`（原始尺寸）、`downsized`（缩小尺寸）、`fixed_width`（固定宽度）、`preview`（预览图）——建议在聊天中使用`downsized`格式的图片。

## Tenor API

```bash
curl "https://tenor.googleapis.com/v2/search?key=KEY&q=thumbs+up&limit=10"
```

返回的图片格式：`gif`、`mediumgif`、`tinygif`、`mp4`、`webm`——为了提高性能，建议使用`tinygif`或`mp4`格式。

## 使用FFmpeg创建GIF图片

**务必使用`palettegen`选项（不使用该选项会导致颜色失真）：**
```bash
ffmpeg -ss 0 -t 5 -i input.mp4 \
  -filter_complex "fps=10,scale=480:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse" \
  output.gif
```

| 设置 | 值 | 原因 |
|---------|-------|-----|
| fps | 8-12 | 帧率过高会导致文件体积大幅增加 |
| scale | 320-480 | 1080p分辨率的GIF文件体积非常大 |
| lanczos | 必须启用 | 最佳的图像缩放质量 |

## 优化后的GIF图片

**优化后，图片大小可减少30-50%，同时几乎不影响画质。**

## 使用视频代替GIF图片（适用于网页）

对于网页来说，使用视频代替大尺寸的GIF图片可以节省大量空间（通常体积小80-90%）：

```html
<video autoplay muted loop playsinline>
  <source src="animation.webm" type="video/webm">
  <source src="animation.mp4" type="video/mp4">
</video>
```

## 可访问性建议

- **WCAG 2.2.2**：循环播放时间超过5秒的GIF需要提供暂停功能 |
- **prefers-reduced-motion**：优先显示静态图片 |
- **alt文本**：描述图片的实际内容（例如“猫从桌子上跳下来”，而不是简单写“GIF”） |
- **闪烁频率**：每秒闪烁次数不应超过3次（以避免引发视觉不适或癫痫发作风险）

## 常见错误

- 在使用FFmpeg时未启用`palettegen`选项，导致图片颜色失真 |
- 设置帧率（FPS）过高，虽然画面更流畅，但文件体积会急剧增加 |
- 网页上未实现GIF的懒加载功能，导致页面加载缓慢 |
- 在适合使用视频的场景中使用大尺寸GIF图片，实际上视频的体积会更小得多（通常只有GIF的1/10）