---
name: GIF
slug: gif
version: 1.0.1
description: 查找、搜索并创建经过适当优化和具备良好可访问性的 GIF 文件。
changelog: Declare required binary (ffmpeg), document optional deps (gifsicle, API keys)
metadata: {"clawdbot":{"emoji":"🎞️","requires":{"bins":["ffmpeg"]},"os":["linux","darwin","win32"]}}
---
## 要求

**创建 GIF 图像所需工具：**
- `ffmpeg` — 用于将视频转换为 GIF 格式

**可选工具：**
- `gifsicle` — 用于后期优化（可减少文件大小 30-50%）
- `GIPHY_API_KEY` — 用于使用 Giphy 搜索 API
- `TENOR_API_KEY` — 用于使用 Tenor 搜索 API

## 获取 GIF 图像的来源

| 网站 | 适用场景 | 是否需要 API |
|------|----------|-----|
| **Giphy** | 通用视频、热门视频 | 需要 API 密钥 |
| **Tenor** | 适用于消息应用 | 需要 API 密钥 |
| **Imgur** | 病毒式传播的视频/社区内容 | 需要 API |
| **Reddit r/gifs** | 小众、独特的 GIF 图像 | 不需要 API |

## 使用 FFmpeg 创建 GIF 图像

**务必使用 `palettegen` 工具（否则颜色会显得失真）：**
```bash
ffmpeg -ss 0 -t 5 -i input.mp4 \
  -filter_complex "fps=10,scale=480:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse" \
  output.gif
```

| 设置 | 值 | 原因 |
|---------|-------|-----|
| fps | 8-12 | 帧率过高会导致文件体积过大 |
| scale | 320-480 | 1080p 分辨率的 GIF 文件体积非常大 |
| lanczos | 必须启用 | 最佳的图像缩放质量 |

## 后期优化

如果安装了 `gifsicle`：
```bash
gifsicle -O3 --lossy=80 --colors 128 input.gif -o output.gif
```

使用 `gifsicle` 可以在几乎不损失画质的情况下将 GIF 文件大小减少 30-50%。

## 使用视频代替 GIF 图像（适用于网页）

对于网页来说，使用视频代替大型 GIF 图像可以节省大量空间（通常文件大小可减少 80-90%）：
```html
<video autoplay muted loop playsinline>
  <source src="animation.webm" type="video/webm">
  <source src="animation.mp4" type="video/mp4">
</video>
```

## 可访问性建议

- **WCAG 2.2.2**：循环播放时间超过 5 秒的视频需要提供暂停功能 |
- **prefers-reduced-motion**：建议显示静态图片 |
- **Alt 文本**：为视频添加描述性文字（例如：“猫咪从桌子上跳下来”） |
- **闪光效果**：每秒闪光次数超过 3 次可能会对用户造成不适（尤其是对有癫痫史的用户） |

## 常见错误

- 未在 FFmpeg 中启用 `palettegen` 工具——会导致颜色显示异常 |
- 帧率（FPS）设置过高——虽然画面更流畅，但文件体积会急剧增加 |
- 网页上未实现懒加载功能——会导致页面加载缓慢 |
- 用大型 GIF 图像替代适合的视频文件——实际上这会浪费大量带宽，且文件体积更大（可能达到视频的 10 倍） |

## API 快速参考

**Giphy 搜索 API：**
```bash
curl "https://api.giphy.com/v1/gifs/search?api_key=$GIPHY_API_KEY&q=thumbs+up&limit=10"
```

**Tenor 搜索 API：**
```bash
curl "https://tenor.googleapis.com/v2/search?key=$TENOR_API_KEY&q=thumbs+up&limit=10"
```