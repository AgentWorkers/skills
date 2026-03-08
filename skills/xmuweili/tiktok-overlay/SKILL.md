---
name: tiktok-overlay
version: 1.1.0
description: 该功能可以为图片和视频添加类似TikTok风格的文字叠加效果，支持自定义字体、背景、描边效果以及定时动画。
user-invocable: true
metadata:
  {"openclaw": {"emoji": "🎵", "requires": {"bins": ["python3"]}, "install": [{"type": "uv", "packages": ["Pillow", "moviepy"]}]}}
---
# TikTok 文本叠加工具

这是一个模拟 TikTok 文本叠加功能的工具，可以将带样式的文本叠加到图片和视频上，呈现出与 TikTok 内置文本编辑器相同的外观和效果。

## 设置

所有用于文本叠加的脚本都位于 `{baseDir}` 目录下：

- `{baseDir}/tiktok_overlay.py` — 用于图片的文本叠加引擎
- `{baseDir}/tiktok_video_overlay.py` — 用于视频的文本叠加引擎（基于 moviepy 库实现）

在使用该工具之前，请确保已安装所有必要的依赖库：

```bash
pip3 install Pillow moviepy
```

## 可用的文本样式

| 样式             | 值            | 描述                                      |
|-----------------|-----------------|-----------------------------------------|
| Classic           | `classic`       | 简洁的粗体无衬线字体（Arial Bold）                   |
| Typewriter       | `typewriter`     | 等宽字体，模仿打字机的风格                     |
| Handwriting       | `handwriting`     | 休闲风格的手写体                             |
| Neon            | `neon`         | 圆角粗体字体，带有发光效果                     |
| Serif            | `serif`         | 传统的衬线字体（Georgia）                         |
| Strong           | `strong`        | 非常粗体的字体风格                         |
| Comic           | `comic`        | 轻松幽默的漫画字体                           |

## 背景样式

| 样式             | 值            | 描述                                      |
|-----------------|-----------------|-----------------------------------------|
| None             | `none`          | 无背景，仅显示文本                           |
| Highlight         | `highlight`       | 每行文字周围有圆形高光效果（TikTok 默认样式）           |
| Full BG           | `full_bg`        | 所有文字下方都有一个圆形背景框                   |
| Letter            | `letter`         | 每行文字周围有细小的高光效果                     |

## 图片文本叠加

使用 `{baseDir}/tiktok_overlay.py` 对图片应用文本叠加效果：

```python
import sys
sys.path.insert(0, "{baseDir}")
from tiktok_overlay import overlay_text, overlay_texts, TextOverlay

# Single text — save to file
overlay_text("input.jpg", "Your text here", "output.jpg",
    style="classic", font_size=48, stroke_width=5, bg_style="none")

# Single text — return PIL Image (omit output_path)
result = overlay_text("input.jpg", "Your text here",
    style="strong", font_size="large", text_color="coral")

# Multiple overlays — TextOverlay objects
overlay_texts("input.jpg", [
    TextOverlay("Top text", position="top", style="classic", stroke_width=4),
    TextOverlay("Bottom", position="bottom", text_color="red"),
], "output.jpg")

# Multiple overlays — dicts (no import needed)
overlay_texts("input.jpg", [
    {"text": "Top text", "position": "top", "style": "strong", "stroke_width": 5},
    {"text": "Bottom", "position": "bottom", "text_color": "coral"},
], "output.jpg")

# Multiple overlays — (text, kwargs) tuples
overlay_texts("input.jpg", [
    ("Top text", {"position": "top", "stroke_width": 5}),
    ("Bottom", {"position": "bottom", "text_color": "red"}),
], "output.jpg")
```

### 灵活的输入参数

所有参数都支持多种输入格式：

- **输入源**：文件路径、PIL 图像、numpy 数组或字节数据：
```python
overlay_text("photo.jpg", "Hello", "out.jpg")          # path
overlay_text(pil_image, "Hello", "out.jpg")             # PIL Image
overlay_text(numpy_array, "Hello", "out.jpg")           # numpy
overlay_text(image_bytes, "Hello", "out.jpg")           # bytes
```

- **输出结果**：保存文件的路径；如果不需要输出结果，可以设置为 `None`，此时函数会返回一个 PIL 图像：
```python
overlay_text("photo.jpg", "Hello", "out.jpg")           # saves file
result = overlay_text("photo.jpg", "Hello")             # returns PIL Image
```

- **颜色**：十六进制颜色代码、简写十六进制颜色代码、带有透明度的十六进制颜色代码、颜色名称、RGB 或 RGBA 元组：
```python
text_color="#FF0000"          # hex
text_color="#F00"             # short hex
text_color="#FF000080"        # hex with alpha
text_color="red"              # named (all CSS/PIL colors)
text_color=(255, 0, 0)        # RGB tuple
text_color=(255, 0, 0, 128)   # RGBA tuple
```

- **字体大小**：以像素为单位的整数、带有单位的字符串或预定义的字体大小：
```python
font_size=48                  # pixels
font_size="48px"              # string with unit
font_size="small"             # 32px
font_size="medium"            # 48px
font_size="large"             # 64px
font_size="xl"                # 80px
font_size="title"             # 72px
font_size="caption"           # 28px
```

- **文本样式**：字符串或枚举类型：
```python
style="classic"               # string
style="strong"
from tiktok_overlay import TikTokStyle
style=TikTokStyle.CLASSIC     # enum
```

- **文本位置**：可以使用预定义的名称、复合格式、像素坐标、百分比值或字典来指定位置：
```python
position="top"                # named
position="bottom-left"        # compound
position=(100, 200)           # pixel coordinates
position=("50%", "80%")       # percentage of image size
position={"x": "10%", "y": "top"}  # dict with mixed
```

- **透明度**：浮点数、整数或百分比字符串：
```python
bg_opacity=0.6                # float 0-1
bg_opacity=153                # int 0-255
bg_opacity="60%"              # percentage string
```

- **最大文本宽度比例**：浮点数或百分比字符串：
```python
max_width_ratio=0.85          # float
max_width_ratio="85%"         # percentage string
```

### 命令行接口（CLI）

```bash
python3 {baseDir}/tiktok_overlay.py <input_image> "<text>" [output_image] [style]
```

输出路径是可选的，默认值为 `input_overlay.ext`。

## 视频文本叠加

使用 `{baseDir}/tiktok_video_overlay.py` 对视频应用文本叠加效果。支持设置文本的显示时间以及文本的淡入/淡出效果：

```python
import sys
sys.path.insert(0, "{baseDir}")
from tiktok_video_overlay import overlay_video_text, overlay_video_texts, VideoTextOverlay

# Single text on entire video
overlay_video_text("input.mp4", "Hello!", "output.mp4",
    style="classic", font_size=52, stroke_width=5)

# Multiple timed texts
overlay_video_texts("input.mp4", [
    VideoTextOverlay("Appears 0-3s", t_start=0, t_end=3,
        fade_in=0.5, fade_out=0.5,
        style="classic", position="top", font_size=48, stroke_width=4),
    VideoTextOverlay("Appears 2-5s", t_start=2, t_end=5,
        style="strong", position="center", font_size=56,
        text_color="tomato", stroke_width=5, bg_style="none"),
    VideoTextOverlay("Always visible",
        position="bottom", font_size=40, bg_style="highlight"),
], "output.mp4")
```

### 命令行接口（CLI）

```bash
python3 {baseDir}/tiktok_video_overlay.py <input_video> "<text>" <output_video> [style]
```

## 主要参数

| 参数                | 接受的输入类型                | 默认值            | 描述                                      |
|------------------|------------------|-----------------------------------------|
| `input_source`       | 文件路径、PIL 图像、numpy 数组或字节数据 |                  | 要叠加的图像                               |
| `text`            | 字符串                     |                  | 要叠加的文本                                 |
| `output_path`       | 文件路径（可选）                |                  | 输出文件的路径；`None` 表示返回 PIL 图像           |
| `style`            | 字符串或 `TikTokStyle` 枚举类型    | `classic`           | 文本字体样式                               |
| `font_size`         | 整数或字符串（例如 `"48px"`、`"large"`）    |                  | 字体大小                                   |
| `text_color`        | 十六进制颜色代码、颜色名称或 RGB/RGBA 元组    | `#FFFFFF`           | 文本颜色                                 |
| `bg_style`          | 字符串                     |                  | 背景样式                                   |
| `bg_color`         | 十六进制颜色代码、颜色名称或 RGB/RGBA 元组    | `#000000`           | 背景颜色                                 |
| `bg_opacity`         | 浮点数（0-1）或百分比字符串       |                  | 背景透明度                               |
| `position`         | 字符串、坐标值或位置字典            | `center`           | 文本位置                                 |
| `alignment`        | 字符串                     |                  | 文本对齐方式（left/center/right）                   |
| `stroke_width`       | 整数                     |                  | 文本边框宽度（TikTok 风格建议使用 4-6）                |
| `stroke_color`        | 十六进制颜色代码、颜色名称或 RGB/RGBA 元组    | `#000000`           | 文本边框颜色                               |
| `max_width_ratio`     | 浮点数或百分比字符串           |                  | 文本最大宽度与图片宽度的比例                         |

### 仅适用于视频的参数

| 参数                | 类型                         | 默认值            | 描述                                      |
|------------------|------------------|-----------------------------------------|
| `t_start`           | 浮点数或 `None`                |                  | 文本显示的开始时间（秒）                         |
| `t_end`           | 浮点数或 `None`                |                  | 文本显示的结束时间（秒）                         |
| `fade_in`          | 浮点数                     |                  | 文本淡入的持续时间（秒）                         |
| `fade_out`          | 浮点数                     |                  | 文本淡出的持续时间（秒）                         |

## 使用技巧

- 要获得经典的 TikTok 文本边框效果，设置 `bg_style="none"` 并设置 `stroke_width=5`。
- 要获得 TikTok 风格的高光效果，设置 `bg_style="highlight"` 并设置 `bg_opacity=0.6`。
- 系统会自动根据 `max_width_ratio` 参数进行文本换行。
- 支持复合位置格式，例如 `"top-left"` 和 `"bottom-right"`。
- 支持所有常见的 CSS 和 PIL 颜色名称（例如 `"red"`、`coral"`、`dodgerblue"`、`gold` 等）。
- 该工具会使用 macOS 系统自带的字体来实现 TikTok 风格，因此在 macOS 上无需额外配置即可正常使用。