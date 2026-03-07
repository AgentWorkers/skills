---
name: image-handler
description: Read, analyze, convert, and manipulate image files (PNG, JPG, GIF, WebP, TIFF, BMP, HEIC, SVG, ICO). Use when working with images: reading metadata, converting formats, resizing, rotating, compressing, or batch processing. Triggers on mentions of image files, file paths with image extensions, or requests to process/convert images.
---

# 图像处理工具

用于分析、转换和操作图像文件。

## 支持的格式

| 格式 | 扩展名 | 读取 | 转换 | 元数据 |
|--------|------------|------|---------|----------|
| PNG | .png | ✅ | ✅ | ✅ |
| JPEG | .jpg, .jpeg | ✅ | ✅ | ✅ |
| GIF | .gif | ✅ | ✅ | ✅ |
| WebP | .webp | ✅ | ✅ | ✅ |
| TIFF | .tiff, .tif | ✅ | ✅ | ✅ |
| BMP | .bmp | ✅ | ✅ | ✅ |
| HEIC | .heic, .heif | ✅ | ✅ | ✅ |
| SVG | .svg | ✅ | ✅ | - |
| ICO | .ico | ✅ | ✅ | ✅ |

## 快速命令

### 查看元数据（使用 macOS 内置的 `sips` 命令）

```bash
# Get all properties
sips -g all image.jpg

# Get specific properties
sips -g pixelWidth -g pixelHeight -g format -g dpiWidth -g dpiHeight image.jpg

# JSON-like output (parseable)
sips -g all image.jpg 2>&1 | tail +2
```

### 转换图像格式

```bash
# Convert to PNG
sips -s format png input.jpg --out output.png

# Convert to JPEG with quality
sips -s format jpeg -s formatOptions 85 input.png --out output.jpg

# Convert HEIC to JPEG
sips -s format jpeg input.heic --out output.jpg

# Batch convert (shell)
for f in *.heic; do sips -s format jpeg "$f" --out "${f%.heic}.jpg"; done
```

### 调整图像大小

```bash
# Resize to max dimensions (maintains aspect ratio)
sips --resampleWidth 1920 image.jpg --out resized.jpg
sips --resampleHeight 1080 image.jpg --out resized.jpg

# Resize to exact dimensions
sips --resampleWidth 1920 --resampleHeight 1080 image.jpg --out resized.jpg

# Scale by percentage
sips --resampleWidth 50% image.jpg --out half.jpg
```

### 旋转和翻转图像

```bash
# Rotate 90 degrees clockwise
sips --rotate 90 image.jpg --out rotated.jpg

# Rotate 180 degrees
sips --rotate 180 image.jpg --out rotated.jpg

# Flip horizontal
sips --flip horizontal image.jpg --out flipped.jpg

# Flip vertical
sips --flip vertical image.jpg --out flipped.jpg
```

### 裁剪图像

```bash
# Crop to specific pixels (x, y, width, height)
sips --cropToHeightWidth 500 500 image.jpg --out cropped.jpg

# Crop from center
sips --cropToHeightWidth 500 500 --cropOffset 100 100 image.jpg --out cropped.jpg
```

### 删除图像元数据

```bash
# Remove EXIF and all metadata
sips --deleteProperty all image.jpg --out clean.jpg
```

### 使用 `ffmpeg` 进行高级操作

```bash
# WebP to PNG
ffmpeg -i input.webp output.png

# Extract frames from GIF
ffmpeg -i animation.gif frame_%03d.png

# Create GIF from images
ffmpeg -framerate 10 -i frame_%03d.png output.gif

# Resize with ffmpeg
ffmpeg -i input.jpg -vf scale=1920:-1 output.jpg

# Convert video to GIF
ffmpeg -i video.mp4 -vf "fps=10,scale=480:-1" output.gif
```

## 脚本

### `image_info.sh`

获取图像的详细元数据。

```bash
~/Dropbox/jarvis/skills/image-handler/scripts/image_info.sh <image>
```

### `convert_image.sh`

根据需要转换图像格式。

```bash
~/Dropbox/jarvis/skills/image-handler/scripts/convert_image.sh <input> <output> [quality]
```

### `batch_convert.sh`

批量转换目录中的所有图像。

```bash
~/Dropbox/jarvis/skills/image-handler/scripts/batch_convert.sh <input_dir> <output_format> [output_dir]
```

## 工作流程

1. **获取信息** — 使用 `sips -g all` 命令获取图像的尺寸、格式和元数据。
2. **如有需要，进行转换** — 为了兼容性，可以转换图像格式。
3. **调整图像大小/优化** — 为了适应网页或分享需求，可以调整图像大小。
4. **删除元数据** — 为了保护隐私，可以删除图像的 EXIF 元数据。

## 注意事项

- `sips` 已经内置在 macOS 中，无需额外安装。
- `ffmpeg` 可以处理 WebP 格式、动画 GIF 文件以及将视频转换为图像。
- 对于 HEIC（iPhone 照片）格式，建议转换为 JPEG 格式以确保兼容性。
- SVG 格式是基于文本的，可以使用 `cat` 命令或其他文本处理工具进行操作。
- 如果需要对图像进行OCR（光学字符识别）处理，请使用专门的文档处理工具。