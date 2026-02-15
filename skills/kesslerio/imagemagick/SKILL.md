# ImageMagick Moltbot 技能

Moltbot 提供了丰富的 ImageMagick 操作功能，用于图像处理。

## 安装

**macOS:**
```bash
brew install imagemagick
```

**Linux:**
```bash
sudo apt install imagemagick  # Debian/Ubuntu
sudo dnf install ImageMagick  # Fedora
```

**验证安装:**
```bash
convert --version
```

## 可用的操作

### 1. 去除背景（白色/纯色 → 透明背景）
```bash
./scripts/remove-bg.sh input.png output.png [tolerance] [color]
```

| 参数 | 默认值 | 范围 | 说明 |
|-----------|---------|-------|-------------|
| input.png | — | — | 输入图像文件 |
| output.png | — | — | 输出的透明 PNG 文件 |
| tolerance | 20 | 0-255 | 颜色匹配的模糊度 |
| color | #FFFFFF | 十六进制颜色代码 | 需要去除的颜色 |

**示例:**
```bash
./scripts/remove-bg.sh icon.png icon-clean.png              # default white
./scripts/remove-bg.sh icon.png icon-clean.png 30           # loose tolerance
./scripts/remove-bg.sh icon.png icon-clean.png 10 "#000000" # remove black
```

### 2. 调整图像大小
```bash
convert input.png -resize 256x256 output.png
```

### 3. 转换图像格式
```bash
convert input.png output.webp          # PNG → WebP
convert input.jpg output.png           # JPG → PNG
convert input.png -quality 80 output.jpg  # Compress
```

### 4. 使图像角部圆角（iOS 风格）
```bash
convert input.png -alpha set -virtual pixel transparent \
    -distort viewport 512x512+0+0 \
    -channel A -blur 0x10 -threshold 50% \
    output-rounded.png
```

### 5. 添加水印
```bash
convert base.png watermark.png -gravity southeast -composite output.png
```

### 6. 批量生成缩略图
```bash
for f in *.png; do convert "$f" -resize 128x128 "thumbs/$f"; done
```

### 7. 调整图像颜色
```bash
convert input.png -brightness-contrast 10x0 output.png      # brighter
convert input.png -grayscale output.png                     # grayscale
convert input.png -modulate 100,150,100 output.png          # more saturation
```

## 常见应用场景

### 将扁平图标转换为透明背景
```bash
./scripts/remove-bg.sh icon.png icon-clean.png 15
```

### 生成 iOS 应用图标集
```bash
for size in 1024 512 256 128 64 32 16; do
    convert icon.png -resize ${size}x${size} icon-${size}.png
done
```

### 优化图像以适应网页显示
```bash
convert large.png -quality 85 -resize 2000x2000\> optimized.webp
```

## 提示

- **较高的模糊度（20-50）:** 更适合去除锯齿边缘，但可能会去除部分图像细节 |
- **较低的模糊度（5-15）:** 保留更多图像细节，但可能会留下颜色边缘 |
- **对于扁平图标：** 通常使用 10-20 的模糊度效果最佳 |
- 使用 `-quality` 参数进行 JPEG/WebP 压缩（范围 0-100） |
- 使用 `-strip` 参数去除文件中的元数据（以减小文件大小）