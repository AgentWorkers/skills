---
name: image-hosting
description: >
  Upload images to img402.dev and get a public URL. Free tier: 1MB max, 7-day
  retention, no auth. Use when the agent needs a hosted image URL — for sharing
  in messages, embedding in documents, posting to social platforms, or any
  context that requires a public link to an image file.
metadata:
  openclaw:
    requires:
      bins:
        - curl
---

# 图像托管 — img402

将图片上传到 img402.dev 并获取一个公共 URL。无需注册账户、API 密钥或配置文件。

## 快速参考

```bash
# Upload (multipart)
curl -s -X POST https://img402.dev/api/free -F image=@/path/to/image.png

# Response
# {"url":"https://i.img402.dev/aBcDeFgHiJ.png","id":"aBcDeFgHiJ","contentType":"image/png","sizeBytes":182400,"expiresAt":"2026-02-17T..."}
```

## 工作流程

1. **获取图片**：使用现有的文件，或生成/下载一张图片。
2. **检查文件大小**：文件大小必须小于 1MB。如果超过 1MB，请调整图片大小：
   ```bash
   sips -Z 1600 /path/to/image.png    # macOS — scale longest edge to 1200px
   convert /path/to/image.png -resize 1600x1600 /path/to/image.png  # ImageMagick
   ```
3. **上传图片**：
   ```bash
   curl -s -X POST https://img402.dev/api/free -F image=@/path/to/image.png
   ```
4. **使用 URL**：响应中的 `url` 字段是一个公共 CDN 链接。您可以根据需要将其嵌入到任何地方。

## 限制条件

- **最大文件大小**：1MB
- **保留时间**：7 天
- **支持的格式**：PNG、JPEG、GIF、WebP
- **每日免费上传次数**：1,000 次（全球范围内）
- **无需身份验证**

## 支付选项

对于需要长期保存的图片（最长 1 年，最大文件大小 5MB），请使用 x402 支付接口（费用为 0.01 美元 USD），具体信息请参见：https://img402.dev/blog/paying-x402-apis