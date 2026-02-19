---
name: nano-banana-pro
description: 使用 Nano Banana Pro 通过 grsai.com API 生成/编辑图片。该 API 支持图片的创建、修改等操作，支持文本转图片（text-to-image）和图片转图片（image-to-image）的功能，支持 1K、2K、4K 格式的图片处理；可以使用 `--input-image` 参数指定输入图片文件。
---
# Nano Banana Pro 图像生成与编辑

使用 grsai.com 的 Nano Banana Pro API 生成新图像或编辑现有图像。

## 使用方法

使用绝对路径运行脚本（请勿先进入 `skill` 目录）：

**生成新图像：**
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "your image description" --filename "output-name.png" [--resolution 1K|2K|4K] [--api-key KEY]
```

**编辑现有图像：**
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "editing instructions" --filename "output-name.png" --input-image "path/to/input.png" [--resolution 1K|2K|4K] [--api-key KEY]
```

**重要提示：** 请始终从用户当前的工作目录运行脚本，以确保图像保存在用户的工作目录中，而不是 `skill` 目录中。

## 默认工作流程（草图 → 迭代 → 最终版本）

目标：快速迭代，避免在 4K 分辨率上浪费时间，直到生成出满意的图像。

- **草图阶段（1K 分辨率）**：快速获取反馈
  - `uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "<draftprompt>" --filename "yyyy-mm-dd-hh-mm-ss-draft.png" --resolution 1K`
- **迭代阶段**：逐步调整图像描述；每次迭代时使用新的文件名
  - 如果正在进行编辑，请在每次迭代时保持 `--input-image` 参数不变，直到满意为止。
- **最终版本（4K 分辨率）**：仅在图像描述确定后使用
  - `uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "<finalprompt>" --filename "yyyy-mm-dd-hh-mm-ss-final.png" --resolution 4K`

## 分辨率选项

- **1K**（默认）：约 1024 像素
- **2K**：约 2048 像素
- **4K**：约 4096 像素

用户请求与 API 参数的对应关系：
- 未指定分辨率时：使用 `1K`
- “低分辨率”、“1080”、“1080p”、“1K”：`1K`
- “2K”、“2048”、“普通分辨率”、“中等分辨率”：`2K`
- “高分辨率”、“高画质”、“4K”、“超高清”：`4K`

## 宽高比选项

通过 `--aspect-ratio` 参数设置宽高比。支持的值：`auto`（默认）、`1:1`、`16:9`、`9:16`、`4:3`、`3:4`、`3:2`、`2:3`、`5:4`、`4:5`、`21:9`

## API 密钥

脚本会按以下顺序检查 API 密钥：
1. `--api-key` 参数（如果用户在聊天中提供了密钥，则使用该参数）
2. `GRSAI_API_KEY` 环境变量

如果两者都不存在，脚本将输出错误信息并终止。

## 预检查 + 常见问题及解决方法

- **预检查**：
  - `command -v uv` 命令必须存在
  - `test -n "$GRSAI_API_KEY"`（或使用 `--api-key` 参数）
  - 如果正在编辑图像：`test -f "path/to/input.png"`
- **常见问题**：
  - **错误：未提供 API 密钥。** → 设置 `GRSAI_API_KEY` 或使用 `--api-key` 参数
  - **错误：无法加载输入图像。** → 文件路径错误或文件无法读取
  - **HTTP 401**：API 密钥错误或已过期
  - **生成失败。** → 内容审核问题或输入无效；请重新描述图像要求

## 文件名生成规则

文件名格式为：`yyyy-mm-dd-hh-mm-ss-name.png`

**格式说明：**
- `yyyy-mm-dd-hh-mm-ss`：当前日期和时间（24 小时格式）
- `name`：描述性的小写文本（通常包含 1-5 个单词）
- 保持描述部分的简洁性
- 可以使用用户提供的图像描述或对话内容作为文件名的一部分
- 如果描述不明确，系统会生成随机标识符（例如 `x9k2`、`a7b3`）

**示例：**
- 图像描述：“宁静的日本花园” → `2025-11-23-14-23-05-japanese-garden.png`
- 图像描述：“山间的日落” → `2025-11-23-15-30-12-sunset-mountains.png`
- 图像描述：“生成一个机器人的图像” → `2025-11-23-16-45-33-robot.png`
- 如果描述不明确，系统会生成随机文件名（例如 `2025-11-23-17-12-48-x9k2.png`

## 图像编辑

当用户需要编辑现有图像时：
1. 确认用户是否提供了图像路径，或者是否指定了当前目录中的图像文件
2. 使用 `--input-image` 参数指定图像文件路径
3. 图像描述中应包含编辑指令（例如：“让天空看起来更生动”、“移除人物”、“转换为卡通风格”）
- 常见的编辑操作包括：添加/删除元素、调整颜色、模糊背景等

## 图像描述的处理方式

- **生成新图像时**：直接将用户的描述传递给 `--prompt` 参数
- **编辑图像时**：在 `--prompt` 参数中提供具体的编辑指令（例如：“在天空添加彩虹”、“将其调整为水彩画风格”）
- 在两种情况下，都要尽量保留用户的创意意图

## 提示模板（提高生成效率）

当用户描述模糊或需要精确编辑时，可以使用以下模板：

- **生成图像模板：**
  - “生成一幅 <主题> 的图像。风格：<风格>。构图：<构图方式>。光线：<光线效果>。背景：<背景类型>。调色板：<调色板颜色>。避免使用：<需要避免的元素>。”
- **编辑图像模板（保留其他设置）：**
  - “仅修改：<具体修改内容>。保持以下内容不变：主题、构图/裁剪、姿势、光线、调色板、背景和整体风格。不要添加新元素。如果已有文字，请保持不变。”

## 输出结果

- 图像保存在当前目录中（如果文件名中包含目录路径，则保存在该目录下）
- 脚本会输出生成图像的完整路径
- **不显示图像内容**——仅向用户提供保存路径

## 示例

**生成新图像：**
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "A serene Japanese garden with cherry blossoms" --filename "2025-11-23-14-23-05-japanese-garden.png" --resolution 4K
```

**编辑现有图像：**
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "make the sky more dramatic with storm clouds" --filename "2025-11-23-14-25-30-dramatic-sky.png" --input-image "original-photo.jpg" --resolution 2K
```