---
name: image-utils
description: 使用 Python 的 Pillow 库进行经典的图像处理操作：调整图像大小、裁剪图像、合成图像、转换图像格式、添加水印、调整图像的亮度/对比度，以及优化图像以适应网页展示。该技能适用于对 AI 生成的图像进行后期处理、为网页展示准备图像、批量处理图像文件、创建响应式图像版本，或执行任何基于像素级别的图像操作。该工具既可以独立使用，也可以与 bria-ai 结合使用，以对生成的图像进行进一步处理。
license: MIT
metadata:
  author: Bria AI
  version: "1.2.5"
---
# 图像处理工具

基于Pillow的图像处理工具，支持精确到像素级别的图像操作，适用于调整大小、裁剪、合成、格式转换、添加水印等标准图像处理任务。

## 适用场景

- **AI生成图像的后处理**：对生成的图像进行裁剪、调整大小，以适应网页展示需求。
- **格式转换**：在保持质量的前提下，将图像在PNG、JPEG和WEBP格式之间进行转换。
- **图像合成**：将图像叠加到背景上，或将主体元素粘贴到背景中。
- **批量处理**：批量调整图像大小、添加水印等操作。
- **网页优化**：压缩图像并调整大小，以加快加载速度。
- **社交媒体适配**：根据不同平台的规格裁剪图像。

## 快速参考

| 操作            | 方法                | 描述                                      |
|------------------|------------------|-----------------------------------------|
| **加载图像**       | `load(source)`         | 从URL、文件路径、字节数据或Base64编码字符串加载图像           |
|                | `load_from_url(url)`       | 从指定URL下载图像                         |
| **保存图像**       | `save(image, path)`        | 自动检测格式后保存图像                         |
|                | `to_bytes(image, format)`      | 将图像转换为字节数据                         |
|                | `to_base64(image, format)`      | 将图像转换为Base64编码字符串                         |
| **调整大小**       | `resize(image, width, height)`     | 将图像调整为指定尺寸                         |
|                | `scale(image, factor)`       | 按指定比例缩放图像（0.5表示缩小一半）                   |
|                | `thumbnail(image, size)`      | 将图像裁剪为指定大小并保持纵横比                   |
| **裁剪图像**       | `crop(image, left, top, right, bottom)` | 从指定位置裁剪图像                         |
|                | `crop_center(image, width, height)` | 从图像中心裁剪                         |
|                | `crop_to_aspect(image, ratio)`     | 按指定纵横比裁剪图像                         |
| **图像合成**       | `paste(bg, fg, position)`     | 将背景图像和前景图像按照指定位置叠加                   |
|                | `composite(bg, fg, mask)`     | 使用遮罩效果合成图像                         |
|                | `fit_to_canvas(image, w, h)`     | 使图像适应指定画布尺寸                         |
| **添加边框/填充**     | `add_border(image, width, color)`    | 为图像添加固定宽度的边框或背景色                   |
| **图像变换**       | `rotate(image, angle)`      | 旋转图像                         |
|                | `flip_horizontal(image)`     | 水平翻转图像                         |
|                | `flip_vertical(image)`     | 垂直翻转图像                         |
| **添加水印**       | `add_text_watermark(image, text)`    | 在图像上添加文字水印                         |
|                | `add_image_watermark(image, logo)`    | 在图像上添加Logo水印                         |
| **图像调整**       | `adjust_brightness(image, factor)`    | 调整图像亮度                         |
|                | `adjust_contrast(image, factor)`    | 调整图像对比度                         |
|                | `adjust_saturation(image, factor)`    | 调整图像饱和度                         |
|                | `blur(image, radius)`      | 对图像应用高斯模糊效果                         |
| **网页优化**       | `optimize_for_web(image, max_size)` | 优化图像以适应网页加载需求                     |
| **获取信息**       | `get_info(image)`       | 获取图像的尺寸、格式和编码方式                         |

## 所需依赖库/模块

```bash
pip install Pillow requests
```

## 基本用法

```python
from image_utils import ImageUtils

# Load from URL
image = ImageUtils.load_from_url("https://example.com/image.jpg")

# Or load from various sources
image = ImageUtils.load("/path/to/image.png")         # File path
image = ImageUtils.load(image_bytes)                  # Bytes
image = ImageUtils.load("data:image/png;base64,...")  # Base64

# Resize and save
resized = ImageUtils.resize(image, width=800, height=600)
ImageUtils.save(resized, "output.webp", quality=90)

# Get image info
info = ImageUtils.get_info(image)
print(f"{info['width']}x{info['height']} {info['mode']}")
```

## 调整图像大小与比例

```python
# Resize to exact dimensions
resized = ImageUtils.resize(image, width=800, height=600)

# Resize maintaining aspect ratio (fit within bounds)
fitted = ImageUtils.resize(image, width=800, height=600, maintain_aspect=True)

# Resize by width only (height auto-calculated)
resized = ImageUtils.resize(image, width=800)

# Scale by factor
half = ImageUtils.scale(image, 0.5)    # 50% size
double = ImageUtils.scale(image, 2.0)  # 200% size

# Create thumbnail
thumb = ImageUtils.thumbnail(image, (150, 150))
```

## 裁剪图像

```python
# Crop to specific region
cropped = ImageUtils.crop(image, left=100, top=50, right=500, bottom=350)

# Crop from center
center = ImageUtils.crop_center(image, width=400, height=400)

# Crop to aspect ratio (for social media)
square = ImageUtils.crop_to_aspect(image, "1:1")      # Instagram
wide = ImageUtils.crop_to_aspect(image, "16:9")       # YouTube thumbnail
story = ImageUtils.crop_to_aspect(image, "9:16")      # Stories/Reels

# Control crop anchor
top_crop = ImageUtils.crop_to_aspect(image, "16:9", anchor="top")
bottom_crop = ImageUtils.crop_to_aspect(image, "16:9", anchor="bottom")
```

## 图像合成

```python
# Paste foreground onto background
result = ImageUtils.paste(background, foreground, position=(100, 50))

# Alpha composite (foreground must have transparency)
result = ImageUtils.composite(background, foreground)

# Fit image onto canvas with letterboxing
canvas = ImageUtils.fit_to_canvas(
    image,
    width=1200,
    height=800,
    background_color=(255, 255, 255, 255),  # White
    position="center"  # or "top", "bottom"
)
```

## 格式转换

```python
# Convert to different formats
png_bytes = ImageUtils.to_bytes(image, "PNG")
jpeg_bytes = ImageUtils.to_bytes(image, "JPEG", quality=85)
webp_bytes = ImageUtils.to_bytes(image, "WEBP", quality=90)

# Get base64 for data URLs
base64_str = ImageUtils.to_base64(image, "PNG")
data_url = ImageUtils.to_base64(image, "PNG", include_data_url=True)
# Returns: "data:image/png;base64,..."

# Save with format auto-detected from extension
ImageUtils.save(image, "output.png")
ImageUtils.save(image, "output.jpg", quality=85)
ImageUtils.save(image, "output.webp", quality=90)
```

## 添加水印

```python
# Text watermark
watermarked = ImageUtils.add_text_watermark(
    image,
    text="© 2024 My Company",
    position="bottom-right",  # bottom-left, top-right, top-left, center
    font_size=24,
    color=(255, 255, 255, 128),  # Semi-transparent white
    margin=20
)

# Logo/image watermark
logo = ImageUtils.load("logo.png")
watermarked = ImageUtils.add_image_watermark(
    image,
    watermark=logo,
    position="bottom-right",
    opacity=0.5,
    scale=0.15,  # 15% of image width
    margin=20
)
```

## 图像调整

```python
# Brightness (1.0 = original, <1 darker, >1 lighter)
bright = ImageUtils.adjust_brightness(image, 1.3)
dark = ImageUtils.adjust_brightness(image, 0.7)

# Contrast (1.0 = original)
high_contrast = ImageUtils.adjust_contrast(image, 1.5)

# Saturation (0 = grayscale, 1.0 = original, >1 more vivid)
vivid = ImageUtils.adjust_saturation(image, 1.3)
grayscale = ImageUtils.adjust_saturation(image, 0)

# Sharpness
sharp = ImageUtils.adjust_sharpness(image, 2.0)

# Blur
blurred = ImageUtils.blur(image, radius=5)
```

## 图像变换

```python
# Rotate (counter-clockwise, degrees)
rotated = ImageUtils.rotate(image, 45)
rotated = ImageUtils.rotate(image, 90, expand=False)  # Don't expand canvas

# Flip
mirrored = ImageUtils.flip_horizontal(image)
flipped = ImageUtils.flip_vertical(image)
```

## 添加边框与填充效果

```python
# Add solid border
bordered = ImageUtils.add_border(image, width=5, color=(0, 0, 0))

# Add padding (whitespace)
padded = ImageUtils.add_padding(image, padding=20)  # Uniform
padded = ImageUtils.add_padding(image, padding=(10, 20, 10, 20))  # left, top, right, bottom
```

## 优化图像以适应网页展示

```python
# Optimize for web delivery
optimized_bytes = ImageUtils.optimize_for_web(
    image,
    max_dimension=1920,  # Resize if larger
    format="WEBP",       # Best compression
    quality=85
)

# Save optimized
with open("optimized.webp", "wb") as f:
    f.write(optimized_bytes)
```

## 与AI图像生成工具集成

可与其他图像生成API（如Bria AI）配合使用：

```python
from bria_client import BriaClient
from image_utils import ImageUtils

client = BriaClient()

# Generate with AI
result = client.generate("product photo of headphones", aspect_ratio="1:1")
image_url = result['result']['image_url']

# Download and post-process
image = ImageUtils.load_from_url(image_url)

# Create multiple sizes for responsive images
sizes = {
    "large": ImageUtils.resize(image, width=1200),
    "medium": ImageUtils.resize(image, width=600),
    "thumb": ImageUtils.thumbnail(image, (150, 150))
}

# Save all as optimized WebP
for name, img in sizes.items():
    ImageUtils.save(img, f"product_{name}.webp", quality=85)
```

## 批量处理示例

```python
from pathlib import Path
from image_utils import ImageUtils

def process_catalog(input_dir, output_dir):
    """Process all images in a directory."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    for image_file in Path(input_dir).glob("*.{jpg,png,webp}"):
        image = ImageUtils.load(image_file)

        # Crop to square
        square = ImageUtils.crop_to_aspect(image, "1:1")

        # Resize to standard size
        resized = ImageUtils.resize(square, width=800, height=800)

        # Add watermark
        final = ImageUtils.add_text_watermark(resized, "© My Brand")

        # Save optimized
        output_file = output_path / f"{image_file.stem}.webp"
        ImageUtils.save(final, output_file, quality=85)

process_catalog("./raw_images", "./processed")
```

## API参考

详细实现及文档说明请参阅 [image_utils.py](./references/code-examples/image_utils.py)。