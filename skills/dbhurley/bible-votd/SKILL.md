---
name: bible
description: 获取 Bible.com 当日经文，并附有可分享的图片。
homepage: https://bible.com
metadata: {"clawdis":{"emoji":"📖","requires":{"bins":["python3"]}}}
---

# Bible.com 每日经文

从 Bible.com (YouVersion) 获取每日经文，并附带可分享的图片。

## 快速命令

### 获取每日经文（JSON格式）
```bash
python3 ~/clawd/skills/bible/votd.py
```

返回结果：
```json
{
  "reference": "Psalms 27:4",
  "text": "One thing I ask from the LORD...",
  "usfm": "PSA.27.4",
  "date": "2026-01-04T21:00:10.178Z",
  "image_url": "https://imageproxy.youversionapi.com/1280x1280/...",
  "attribution": "Bible.com / YouVersion"
}
```

### 获取每日经文及下载图片
```bash
python3 ~/clawd/skills/bible/votd.py --download /tmp/votd.jpg
```

将 1280x1280 像素的图片下载到指定路径。

## 分享每日经文

在分享每日经文时：
1. 使用 `image_url` 来显示或发送预先渲染好的图片
2. 必须包含经文引用（例如：“诗篇 27:4”）
3. 必须注明图片来源：“Bible.com / YouVersion”

## 图片详情

- 图片为 1280x1280 像素的高质量 JPG 格式
- 经文文本会叠加在精美的背景上
- 非常适合在社交媒体或消息应用中分享

## 注意事项

- 每日经文会根据 YouVersion 的安排更新
- 无需使用 API 密钥——直接从 Bible.com 的公开页面抓取数据
- 在分享时务必注明图片来源：“Bible.com / YouVersion”