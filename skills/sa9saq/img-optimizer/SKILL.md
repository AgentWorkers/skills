---
description: 使用 ImageMagick 对图像进行压缩、调整大小和转换。支持批量处理，并确保处理后的图像质量符合要求。
---

# 图像优化工具

通过压缩、调整大小和转换格式来优化图像。

**适用场景**：压缩图像、批量转换图像格式或调整图像大小以适应网页/社交媒体需求。

## 系统要求**

- ImageMagick 7.0 或更高版本（使用 `magick` 命令）；或 ImageMagick 6.0 或更高版本（使用 `convert` 命令）。
- 可选工具：`cwebp`（用于 WebP 格式转换）、`optipng`（用于 PNG 格式优化）、`jpegoptim`（用于 JPEG 格式优化）。
- 无需使用 API 密钥。

## 使用说明

1. **处理前检查图像信息**：
   ```bash
   magick identify -format "%f | %wx%h | %b | %m\n" image.png
   ```

2. **压缩** — 减小文件大小：
   ```bash
   # JPEG (80% quality is a good default)
   magick input.jpg -quality 80 -strip output.jpg

   # PNG (lossless optimization)
   optipng -o5 image.png          # in-place
   magick input.png -strip output.png

   # WebP (lossy, excellent compression)
   cwebp -q 80 input.png -o output.webp
   ```

3. **调整大小** — 将图像缩放到指定尺寸：
   ```bash
   # Exact dimensions (may distort)
   magick input.jpg -resize 800x600! output.jpg

   # Fit within bounds (preserve aspect ratio)
   magick input.jpg -resize 800x600 output.jpg

   # By percentage
   magick input.jpg -resize 50% output.jpg

   # Thumbnail (crop to fill)
   magick input.jpg -resize 300x300^ -gravity center -extent 300x300 thumb.jpg
   ```

4. **格式转换**：
   ```bash
   magick input.png output.webp    # PNG → WebP
   magick input.jpg output.avif    # JPEG → AVIF
   ```

5. **批量处理**：
   ```bash
   # Convert all PNGs to WebP in a directory
   for f in *.png; do magick "$f" -quality 80 "${f%.png}.webp"; done

   # Resize all images to max 1200px width
   for f in *.jpg; do magick "$f" -resize "1200>" "$f"; done
   ```

6. **输出结果**：
   ```
   ## 🖼️ Optimization Results
   | File | Original | Optimized | Savings |
   |------|----------|-----------|---------|
   | hero.jpg | 2.4 MB | 680 KB | 72% |
   | logo.png | 340 KB | 89 KB | 74% |
   **Total: 2.74 MB → 769 KB (72% reduction)**
   ```

## 预设尺寸

| 使用场景 | 尺寸 | 备注 |
|----------|-----------|-------|
| 网页头像 | 1920×1080 | 使用 JPEG q80 或 WebP 格式 |
| 缩略图 | 300×300 | 裁剪以适应显示区域 |
| 社交媒体（原始尺寸） | 1200×630 | 适用于 Facebook/Twitter 预览 |
| 个人资料图片 | 400×400 | 方形裁剪 |
| 电子邮件附件 | 宽度 600 像素 | 仅调整宽度 |

## 特殊情况处理

- **动画 GIF**：使用 `magick input.gif -coalesce -resize 50% output.gif` 命令（保留动画效果）。
- **EXIF 数据**：使用 `-strip` 命令删除包括 GPS 位置信息在内的元数据；使用 `-auto-orient -strip` 命令保持图像的旋转方向。
- **透明度**：将包含透明度的 PNG 图像转换为 JPEG 时，透明度会丢失。可以使用 `-background white -flatten` 命令进行修复。
- **超大文件**：分批处理以避免内存不足的问题。
- **已优化过的图像**：检查压缩后文件大小是否有所减少；如果变化微不足道，则可跳过优化步骤。

## 安全注意事项

- 处理前对文件名进行清理，以防止通过恶意文件名引发的安全风险（如 shell 注入攻击）。
- 使用 `magick` 命令而非 `convert` 命令，以避免与 Windows 系统中的 `convert.exe` 命令产生路径冲突。