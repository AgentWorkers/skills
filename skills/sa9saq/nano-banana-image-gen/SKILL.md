---
description: 使用 Google Gemini API 进行 AI 图像生成。可以创建支持日文文本的缩略图、横幅和图形。
---

# Nano Banana 图像生成工具

该工具利用 Google Gemini 2.0 Flash 的人工智能技术进行图像生成。

**适用场景**：生成图片、缩略图、横幅或图形。支持在图片中添加日文文本。

**使用命令**：`generate image`、`create thumbnail`、`make banner`、`画像生成`、`Nano Banana`

## 系统要求

- Python 3.10 及以上版本
- `google-genai` Python 包
- `GOOGLE.AI_API_KEY` 环境变量（Google AI Studio 的 API 密钥）

## 使用步骤

1. **设置 API 密钥**：
   ```bash
   export GOOGLE_AI_API_KEY=$(grep GOOGLE_AI_API_KEY ~/.openclaw/secrets.env | cut -d= -f2)
   ```

2. **生成图片**：
   ```bash
   python3 {skill_dir}/generate.py \
     --prompt "Description of the image you want" \
     --output "./output.png" \
     --aspect 16:9
   ```

3. **提示技巧**：
   - 请具体说明需求：例如：“日落时分的未来主义东京天际线，带有霓虹灯效果” > “Tokyo”
   - 指定风格：如 “水彩风格”、“写实风格”、“扁平插画”
   - 如需在图片中添加文本，请在提示中明确写出文本内容：`“带有文字的博客横幅：AI 的未来”`
   - 选择合适的氛围：如 “暖色调”、“极简风格”、“鲜艳多彩”

4. **将生成的图片保存到指定目录**：
   ```bash
   # Default output location
   --output /mnt/hdd/rey/images/YYYY-MM-DD_description.png
   ```

## 图像分辨率与比例

| 比例 | 适用场景 | 分辨率 |
|-------|----------|------------|
| 16:9 | YouTube 缩略图、博客标题栏 | 1792×1024 |
| 1:1 | Instagram 个人资料图片 | 1024×1024 |
| 9:16 | Instagram 的动态内容 | 1024×1792 |

## 应用场景

- **社交媒体缩略图**：用于 Twitter 或 note.com 的吸引眼球的图片
- **文章封面**：博客文章的专业化标题栏
- **横幅**：用于宣传的图形素材
- **演示文稿**：演示文稿中的视觉元素

## 注意事项

- **API 密钥未设置**：系统会提示认证错误。请检查 `~/.openclaw/secrets.env` 文件。
- **API 使用限制**：Google AI API 有每分钟的请求次数限制，请稍后重试。
- **日文文本渲染**：系统支持日文文本，但复杂布局可能需要调整。
- **不适宜的内容**：系统会拒绝包含不当内容的请求，请重新表述。
- **批量生成**：为避免超出限制，请在每次请求之间添加延迟。

## 安全提示

- 绝不要在输出结果中显示 API 密钥。
- 将 API 密钥保存在 `~/.openclaw/secrets.env` 文件中，并设置权限为 `chmod 600`；切勿将其放入代码或版本控制系统中。
- 生成的图片可能包含一些瑕疵，请在发布前仔细检查。