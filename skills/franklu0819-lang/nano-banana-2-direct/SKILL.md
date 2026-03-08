---
name: nano-banana-2-direct-direct
description: 使用 Gemini 3.1 的 Flash Image Preview（Nano Banana 2）功能生成或编辑图像。该功能支持直接通过 API 调用，无需依赖 `inference.sh` 脚本。适用于创建、修改图像的操作，包括文本转图像（Text-to-Image）和图像转图像（Image-to-Image）等任务。支持 1K、2K、4K 分辨率，可通过 `--input-image` 参数指定输入图像文件。
---
# Nano Banana 2 Direct - Gemini 3.1 Flash Image

使用 Google 的 Gemini 3.1 Flash Image Preview API 直接生成新图像或编辑现有图像（无需使用 `inference.sh`）。

## 使用方法

使用绝对路径运行脚本（请勿先进入 `skill` 目录）：

**生成新图像：**
```bash
uv run ~/.openclaw/workspace/skills/nano-banana-2-direct/scripts/generate_image.py --prompt "your image description" --filename "output-name.png" [--resolution 1K|2K|4K] [--api-key KEY]
```

**编辑现有图像：**
```bash
uv run ~/.openclaw/workspace/skills/nano-banana-2-direct/scripts/generate_image.py --prompt "editing instructions" --filename "output-name.png" --input-image "path/to/input.png" [--resolution 1K|2K|4K] [--api-key KEY]
```

**重要提示：** 请始终从用户当前的工作目录运行脚本，以确保图像保存在用户的工作文件夹中，而不是 `skill` 目录中。

## 默认工作流程（草图 → 迭代 → 最终版本）

目标：快速迭代，避免在 4K 分辨率上浪费时间，直到获得满意的图像效果。

- **草图阶段（1K 分辨率）**：快速获得反馈
  - `uv run ~/.openclaw/workspace/skills/nano-banana-2-direct/scripts/generate_image.py --prompt "<draftprompt>" --filename "yyyy-mm-dd-hh-mm-ss-draft.png" --resolution 1K`
- **迭代阶段**：通过微调提示内容进行修改；每次迭代时使用新的文件名
  - 如果在编辑图像，请确保每次迭代都使用相同的 `--input-image` 参数，直到达到满意的效果。
- **最终版本（4K 分辨率）**：仅在提示内容确定后使用
  - `uv run ~/.openclaw/workspace/skills/nano-banana-2-direct/scripts/generate_image.py --prompt "<finalprompt>" --filename "yyyy-mm-dd-hh-mm-ss-final.png" --resolution 4K`

## 分辨率选项

Gemini 3.1 Flash Image API 支持三种分辨率（分辨率值需为大写 K）：

- **1K**（默认）：约 1024 像素
- **2K**：约 2048 像素
- **4K**：约 4096 像素

用户请求与 API 参数的对应关系：
- 未指定分辨率时：使用 `1K`
- “低分辨率”、“1080”、“1080p”、“1K”：使用 `1K`
- “2K”、“2048”、“普通分辨率”、“中等分辨率”：使用 `2K`
- “高分辨率”、“高画质”、“超高分辨率”、“4K”、“超高清”：使用 `4K`

## API 密钥

脚本会按以下顺序检查 API 密钥：
1. `--api-key` 参数（如果用户在聊天中提供了密钥，则使用该参数）
2. `GEMINI_API_KEY` 环境变量

如果两者都不存在，脚本将输出错误信息并终止运行。

## 预检 + 常见问题及解决方法（快速修复）

- **预检步骤：**
  - 确保 `command -v uv` 命令存在
  - 运行 `test -n "$GEMINI_API_KEY"`（或通过 `--api-key` 参数传递密钥）
  - 如果正在编辑图像，请运行 `test -f "path/to/input.png"` 进行验证

- **常见错误：**
  - **错误：未提供 API 密钥。** → 请设置 `GEMINI_API_KEY` 或通过 `--api-key` 参数传递密钥
  - **错误：无法加载输入图像。** → 检查 `--input-image` 是否指向有效的图像文件
  - **API 错误（如 quota/permission/403）**：可能是密钥错误、无访问权限或超出使用限制；请尝试其他密钥或账户

## 文件名生成规则

文件名遵循以下格式：`yyyy-mm-dd-hh-mm-ss-name.png`

**格式说明：**
- `yyyy-mm-dd-hh-mm-ss`：当前日期和时间（24 小时格式）
- `name`：描述性的小写文本（通常包含 1-5 个单词）
- 描述性文本应简洁明了
- 可以根据用户的提示或对话内容来生成文件名
- 如果提示内容不明确，系统会自动生成随机标识符（例如 `x9k2`、`a7b3`）

**示例：**
- 提示：“一个宁静的日本花园” → `2025-11-23-14-23-05-japanese-garden.png`
- 提示：“山间的日落” → `2025-11-23-15-30-12-sunset-mountains.png`
- 提示：“生成一个机器人的图像” → `2025-11-23-16-45-33-robot.png`
- 如果提示内容不明确，系统会生成随机文件名（例如 `2025-11-23-17-12-48-x9k2.png`）

## 图像编辑

当用户需要修改现有图像时：
1. 确认用户是否提供了图像路径，或者指定了当前目录中的图像文件
2. 使用 `--input-image` 参数指定图像文件的路径
3. 提示中应包含编辑指令（例如：“让天空看起来更富有戏剧性”、“移除人物”、“转换为卡通风格”等）
- 常见的编辑操作包括：添加/删除元素、调整颜色、模糊背景等

## 提示处理方式

- **生成新图像时**：直接将用户的描述性文本传递给 `--prompt` 参数。只有在描述不够清晰时才进行修改。
- **编辑图像时**：在 `--prompt` 参数中明确说明编辑要求（例如：“在天空添加一道彩虹”、“将其调整为水彩画风格”）

在两种情况下，都要保留用户的创意意图。

## 提示模板（提高效率）

当用户描述模糊或需要精确编辑时，可以使用以下模板：

- **生成新图像的模板：**
  - “生成一幅 <主题> 的图像。风格：<风格>。构图：<构图方式>。光线效果：<光线效果>。背景：<背景类型>。色彩调色板：<色彩调色板>。避免使用：<需要避免的元素列表>。”

- **编辑图像的模板（保持其他设置不变）：**
  - “仅更改：<具体修改内容>。其他设置保持不变：主题、构图/裁剪、姿势、光线效果、色彩调色板、背景和整体风格。不要添加新元素。如果已有文字，请保持不变。”

## 输出结果

- 图像会保存为 PNG 格式，文件路径默认为当前目录；如果文件名中包含目录路径，则会保存在该目录下
- 脚本会输出生成的图像的完整路径
- **注意：** 脚本不会显示图像内容，仅向用户提供保存路径

**示例：**
- **生成新图像：**
```bash
uv run ~/.openclaw/workspace/skills/nano-banana-2-direct/scripts/generate_image.py --prompt "A serene Japanese garden with cherry blossoms" --filename "2025-11-23-14-23-05-japanese-garden.png" --resolution 4K
```

- **编辑现有图像：**
```bash
uv run ~/.openclaw/workspace/skills/nano-banana-2-direct/scripts/generate_image.py --prompt "make the sky more dramatic with storm clouds" --filename "2025-11-23-14-25-30-dramatic-sky.png" --input-image "original-photo.jpg" --resolution 2K
```