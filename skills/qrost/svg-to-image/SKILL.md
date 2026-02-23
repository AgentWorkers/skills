---
name: svg-to-image
version: 1.1.1
description: 将 SVG 文件转换为 PNG 或 JPG 格式，以便快速分享（例如通过 Telegram）或打印。
author: qrost
permissions:
  - shell:exec
---
# 将 SVG 文件转换为图片（PNG 或 JPG）

该功能用于将 SVG 文件转换为 PNG 或 JPG 格式的图片。当你拥有矢量图形（例如从地图抓取工具、图表工具或设计软件中获得的图形）时，这种转换非常实用，因为你可以将这些图片用于聊天或文档中。

## 所需依赖库

- `cairosvg`（用于 SVG 的渲染）
- `Pillow`（仅用于生成 JPG 格式的图片）

**安装说明：** OpenClaw 本身不会自动安装 Python 包。安装此功能后，请运行以下命令：`pip install -r requirements.txt`（该命令位于技能对应的文件夹中）。在 Linux（如 Ubuntu/Debian）系统中，需要先安装 Cairo 库：`sudo apt install libcairo2`。如果脚本在执行过程中出现 `ModuleNotFoundError` 或与 Cairo 库相关的问题，请安装缺失的包或系统库。

## 使用方法

### 将 SVG 文件转换为 PNG 或 JPG

**参数：**
- `input`：SVG 文件的路径。
- `-o`, `--output`：输出文件的路径（默认值为输入文件名加上 `.png` 或 `.jpg` 扩展名）。
- `-f`, `--format`：输出格式（默认为 `png`，也可设置为 `jpg`）。
- `--width`, `--height`：可选的输出图片尺寸（以像素为单位）；如果只指定其中一个参数，系统会保持图片的宽高比。
- `--dpi`：图片的分辨率（默认值为 96）。

```bash
# SVG to PNG (default)
python3 scripts/convert_svg.py drawing.svg -o drawing.png

# SVG to JPG
python3 scripts/convert_svg.py drawing.svg -f jpg -o drawing.jpg

# Fixed width 800px (height auto)
python3 scripts/convert_svg.py map.svg -o map.png --width 800
```

## 将图片发送到 Telegram

你可以通过 OpenClaw 的 Telegram 对话功能来使用该功能。运行脚本时，使用 `-o <文件路径>.png` 或 `-o <文件路径>.jpg` 选项生成图片文件，然后通过 OpenClaw 的消息/媒体工具将图片发送给用户。

**OpenClaw 允许的文件路径：** OpenClaw 的消息工具仅允许从以下目录发送文件：`~/.openclaw/media/`, `~/.openclaw/agents/`, 或 `/tmp`。例如，可以使用 `-o ~/.openclaw/media/out.png` 或 `-o /tmp/out.png`；请勿使用技能安装目录，否则发送操作会失败。

**代理程序的行为：** 当用户请求将 SVG 文件转换为 PNG 或 JPG 格式，或者请求“以图片形式发送”时，代理程序会直接运行 `convert_svg.py <svg_path> -o <输出文件路径>.png`（或 `-f jpg`）命令来生成图片，并将生成的图片发送给用户。无需用户确认，程序会自动执行并发送图片。

## 示例：

**用户：** “请将这个 SVG 文件转换为 PNG 格式，以便我可以通过 Telegram 发送。”
**操作：** 运行 `convert_svg.py <svg_path> -o /tmp/out.png`，然后将生成的 PNG 文件发送给用户。

**用户：** “请将 `map.svg` 文件转换为宽度为 1200 像素的 JPG 文件。”
**操作：** 运行 `convert_svg.py -f jpg -o /tmp/map.jpg --width 1200`，然后将生成的 JPG 文件发送给用户。