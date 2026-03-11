---
name: text-to-image
description: 将文本转换为图像，并返回一个临时的本地图像文件路径（可选包含数据 URI）。该功能适用于 Clawhub 或 Codex，可用于将纯文本、带样式的文本、彩色文本、多语言文本、标语、海报、标题或文本片段转换为图像，同时支持控制图像的宽度、高度、格式、字体大小、全文字颜色或部分文字的颜色。支持输出格式为 SVG、PNG 和 JPEG，生成的临时文件将保存在 `tmp` 文件夹中。该功能兼容 Windows 和 macOS 系统，并具备内置的字体回退机制。此外，还支持以下功能：文本转图片、生成彩色文字图片、指定尺寸的图片、局部文字颜色设置、高亮显示部分文字、返回临时图片地址、返回本地图像路径、指定输出格式（SVG/PNG/JPEG）、兼容 Mac 和 Windows 系统。
---
# 将文本转换为图像

使用 `scripts/render_text_image.py` 脚本生成图像，并返回该图像的本地文件路径。根据需要，该脚本还可以包含一个 `data:` 图像 URL。

建议使用此脚本，而不是手动编写图像数据。该脚本已经处理了以下功能：

- 固定的图像宽度和高度
- 输出格式：`svg`、`png`、`jpg`、`jpeg`
- 默认情况下，图像文件会保存在 `tmp/` 目录下
- 响应中包含文件路径、文件名和文件大小
- 整段文本的颜色设置
- 通过高亮显示功能对部分文本进行颜色区分
- 明确指定字体大小；如果省略了 `font_size`，脚本会自动调整字体大小
- 支持换行符导致的文本换行
- 支持透明或实心背景
- 在 Windows 和 macOS 上，脚本会使用系统默认字体作为备用选项

## 输入格式

通过 `--spec-json` 或 `--spec-file` 传递 JSON 规格。

支持的字段：

```json
{
  "text": "Hello\nWorld",
  "highlight_ranges": [
    { "start": 0, "end": 5, "color": "#111111" },
    { "start": 6, "end": 11, "color": "#ff4d4f" }
  ],
  "highlight_texts": [
    { "match": "World", "color": "#1677ff", "occurrence": "all", "case_sensitive": true }
  ],
  "segments": [
    { "text": "Hello ", "color": "#111111" },
    { "text": "World", "color": "#ff4d4f" }
  ],
  "width": 1200,
  "height": 630,
  "format": "png",
  "font_size": 72,
  "min_font_size": 12,
  "default_color": "#111111",
  "background": "#ffffff",
  "padding": 48,
  "line_height": 1.2,
  "align": "center",
  "valign": "middle",
  "font_family": "Microsoft YaHei, PingFang SC, Arial, sans-serif"
}
```

规则：

- 必须提供 `text` 或 `segments` 其中的一项；如果两者都提供，则优先使用 `segments`。
- 对于简单的“将此单词标为红色”之类的请求，建议使用 `text` + `highlight_texts`。
- 当调用者知道字符位置时，使用 `highlight_ranges`。
- 仅当调用者已经将文本分割成具体的片段时，才使用 `segments`。
- 如果需要强制换行，请保留 `\n`。
- 省略 `font_size` 以使脚本自动调整文本在图像中的显示大小。
- 如果提供了 `font_size`，脚本会按照该大小显示文本，并根据需要换行。
- 默认输出格式为 `svg`。
- 对于文本较多的图像，建议使用 `png` 而不是 `jpg`。
- 如果格式设置为 `jpg` 或 `jpeg`，透明背景会自动转换为白色。

优先级：

1. `segments`
2. `text` + `highlight_ranges` / `highlight_texts`
3. 仅使用 `text`

**高亮显示格式示例：**

```json
{
  "text": "ClawHub makes text visible",
  "highlight_texts": [
    { "match": "ClawHub", "color": "#1677ff" },
    { "match": "visible", "color": "#fa541c" }
  ]
}
```

**范围格式示例：**

```json
{
  "text": "Hello World",
  "highlight_ranges": [
    { "start": 6, "end": 11, "color": "#ff4d4f" }
  ]
}
```

## 推荐的工作流程：

1. 根据用户的请求生成 JSON 规格。
2. 运行脚本。
3. 当下一步需要上传文件时，将文件路径返回给调用者。
4. 仅在调用者明确需要数据 URI 时，使用 `image_url`。

**示例：**

```powershell
@'
{
  "segments": [
    { "text": "Claw", "color": "#111111" },
    { "text": "Hub", "color": "#1677ff" }
  ],
  "width": 1024,
  "height": 512,
  "format": "png",
  "background": "#ffffff",
  "padding": 40
}
'@ | Set-Content spec.json

python scripts/render_text_image.py --spec-file spec.json --no-data-url
```

## 输出格式**

脚本会输出 JSON 数据：

```json
{
  "file_path": "E:\\clawhub\\text-to-image\\tmp\\rendered-0000.png",
  "relative_file_path": "tmp/rendered-0000.png",
  "file_name": "rendered-0000.png",
  "file_size": 21550,
  "mime_type": "image/png",
  "format": "png",
  "width": 1024,
  "height": 512,
  "font_size": 96.0,
  "line_count": 1,
  "resolved_segments": [
    { "text": "Claw", "color": "#111111" },
    { "text": "Hub", "color": "#1677ff" }
  ]
}
```

## 注意事项：

- `svg` 格式轻量且清晰，非常适合文本渲染。
- `png` 是用于文本图像的最佳通用位图格式。
- 虽然 `jpg` 也被支持，但通常不是处理文本的最佳选择。
- 自动调整字体大小的功能会考虑文本的宽度；虽然结果可能不够精确，但对于混合中文和拉丁文的内容来说仍然可靠。
- 脚本默认将文件保存在技能对应的 `tmp/` 目录下。
- 通过 `--output path.ext` 参数可以指定文件的保存路径。
- 如果调用者只需要文件的元数据（无需图像 URL），可以传递 `--no-data-url` 参数。
- 在 macOS 上，脚本会尝试使用系统默认字体（如 `PingFang` 和 `STHeiti`）；在 Windows 上则会尝试使用 `Microsoft YaHei`、`SimHei` 和 `Arial` 等字体。
- 可复用的示例规格文件位于 `testcases/` 目录下，其中包括用于固定文本显示大小的 `13-wrap-example.json` 文件。