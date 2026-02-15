---
name: feishu-sticker
description: 将图片作为Feishu的原生贴纸发送。支持自动上传、缓存功能，以及GIF格式转换为WebP格式的功能。
tags: [feishu, lark, sticker, image, fun]
---

# Feishu Sticker Skill

该功能用于向 Feishu 用户或群组发送贴纸（图片）。系统会自动将图片上传至 Feishu（通过 MD5 哈希值进行缓存），并将 GIF 格式的图片转换为 WebP 格式以提高传输效率，同时支持智能搜索功能。

## 主要特性
- **自动上传**：根据需求将本地图片上传至 Feishu 的内容分发网络（CDN）。
- **缓存机制**：通过文件哈希值对图片进行缓存，避免重复上传。
- **优化处理**：自动使用 `ffmpeg-static` 将 GIF 格式的图片转换为 WebP 格式，并压缩大于 5MB 的图片。
- **智能搜索**：支持通过 `--query` 或 `--emotion` 参数进行贴纸搜索。

## 使用方法

```bash
# Send random sticker
node skills/feishu-sticker/send.js --target "ou_..."

# Send specific file
node skills/feishu-sticker/send.js --target "ou_..." --file "/path/to/image.jpg"

# Search and send
node skills/feishu-sticker/send.js --target "ou_..." --query "angry cat"
node skills/feishu-sticker/send.js --target "ou_..." --emotion "happy"
```

## 设置要求
1. 将贴纸文件保存在 `~/.openclaw/media/stickers/` 目录中（或通过 `STICKER_DIR` 配置路径）。
2. 安装所需依赖库：`npm install`（需要安装 `axios`、`commander`、`ffmpeg-static`、`form-data` 和 `dotenv`）。