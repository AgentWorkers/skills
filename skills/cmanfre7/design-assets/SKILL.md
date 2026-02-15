# design-assets

用于创建和编辑图形设计资源：图标、网站图标（favicon）、图片以及颜色系统。

## 工具选择

| 任务 | 工具 | 选择理由 |
|------|------|-----|
| AI 图像生成 | nano-banana-pro | 可根据文本提示生成图片 |
| 图片缩放/转换 | sips | macOS 自带工具，速度快，无需额外依赖 |
| 高级图像处理 | ImageMagick | 支持图像合成、效果处理及批量处理 |
| 图标与徽标设计 | SVG | 可缩放，文件体积小，易于编辑 |
| 屏幕截图 | screencapture | macOS 自带工具 |

## 应用图标生成

从单个 1024x1024 的源图标生成所有所需的图标尺寸。

### iOS / macOS 图标尺寸
```bash
#!/bin/bash
# generate-app-icons.sh <source-1024.png> <output-dir>
SOURCE="$1"
OUTDIR="${2:-.}"
mkdir -p "$OUTDIR"

SIZES=(16 20 29 32 40 48 58 60 64 76 80 87 120 128 152 167 180 256 512 1024)
for SIZE in "${SIZES[@]}"; do
  sips -z $SIZE $SIZE "$SOURCE" --out "$OUTDIR/icon-${SIZE}x${SIZE}.png" 2>/dev/null
done
echo "Generated ${#SIZES[@]} icon sizes in $OUTDIR"
```

### Android 图标尺寸
```bash
# Android adaptive icon sizes
declare -A ANDROID_SIZES=(
  ["mdpi"]=48 ["hdpi"]=72 ["xhdpi"]=96
  ["xxhdpi"]=144 ["xxxhdpi"]=192
)
for DENSITY in "${!ANDROID_SIZES[@]}"; do
  SIZE=${ANDROID_SIZES[$DENSITY]}
  mkdir -p "res/mipmap-$DENSITY"
  sips -z $SIZE $SIZE "$SOURCE" --out "res/mipmap-$DENSITY/ic_launcher.png"
done
```

## 网站图标（favicon）生成

```bash
#!/bin/bash
# generate-favicons.sh <source.png> <output-dir>
SOURCE="$1"
OUTDIR="${2:-.}"
mkdir -p "$OUTDIR"

# Standard web favicons
sips -z 16 16 "$SOURCE" --out "$OUTDIR/favicon-16x16.png"
sips -z 32 32 "$SOURCE" --out "$OUTDIR/favicon-32x32.png"
sips -z 180 180 "$SOURCE" --out "$OUTDIR/apple-touch-icon.png"
sips -z 192 192 "$SOURCE" --out "$OUTDIR/android-chrome-192x192.png"
sips -z 512 512 "$SOURCE" --out "$OUTDIR/android-chrome-512x512.png"

# ICO file (requires ImageMagick)
magick "$OUTDIR/favicon-16x16.png" "$OUTDIR/favicon-32x32.png" "$OUTDIR/favicon.ico"

echo "Favicons generated in $OUTDIR"
```

### HTML 元标签设置
```html
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
```

### site.webmanifest 文件生成
```json
{
  "name": "My App",
  "short_name": "App",
  "icons": [
    { "src": "/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png" }
  ],
  "theme_color": "#ffffff",
  "background_color": "#ffffff",
  "display": "standalone"
}
```

## 颜色调色板生成

根据指定的主色调生成完整的颜色调色板：

```javascript
// HSL-based palette generation
function generatePalette(hue, saturation = 70) {
  return {
    50:  `hsl(${hue}, ${saturation}%, 97%)`,
    100: `hsl(${hue}, ${saturation}%, 94%)`,
    200: `hsl(${hue}, ${saturation}%, 86%)`,
    300: `hsl(${hue}, ${saturation}%, 74%)`,
    400: `hsl(${hue}, ${saturation}%, 62%)`,
    500: `hsl(${hue}, ${saturation}%, 50%)`,  // Primary
    600: `hsl(${hue}, ${saturation}%, 42%)`,
    700: `hsl(${hue}, ${saturation}%, 34%)`,
    800: `hsl(${hue}, ${saturation}%, 26%)`,
    900: `hsl(${hue}, ${saturation}%, 18%)`,
    950: `hsl(${hue}, ${saturation}%, 10%)`,
  };
}
```

## ImageMagick 快速参考

```bash
# Resize
magick input.png -resize 800x600 output.png

# Convert format
magick input.png output.webp

# Add border
magick input.png -border 10 -bordercolor "#333" output.png

# Round corners (with transparency)
magick input.png \( +clone -alpha extract -draw "roundrectangle 0,0,%[w],%[h],20,20" \) -alpha off -compose CopyOpacity -composite output.png

# Composite / overlay
magick base.png overlay.png -gravity center -composite output.png

# Batch resize all PNGs
magick mogrify -resize 50% *.png

# Create solid color image
magick -size 1200x630 xc:"#1a1a2e" output.png

# Add text to image
magick input.png -gravity south -pointsize 24 -fill white -annotate +0+20 "Caption" output.png
```

## sips 快速参考（macOS 版本）
```bash
# Resize (maintain aspect ratio)
sips --resampleWidth 800 input.png --out output.png

# Exact resize
sips -z 600 800 input.png --out output.png

# Convert format
sips -s format jpeg input.png --out output.jpg

# Get image info
sips -g all input.png

# Rotate
sips --rotate 90 input.png --out output.png
```