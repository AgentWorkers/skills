---
name: nano-banana-pro
description: 使用 Nano Banana Pro（Gemini 3 Pro Image）生成/编辑图像。支持图像的创建、修改等操作，包括文本转图像（text-to-image）和图像转图像（image-to-image）功能；支持 1K、2K、4K 格式的图像处理；可通过 `--input-image` 参数指定输入图像文件。
---

# Nano Banana Pro 图像生成与编辑

使用 Google 的 Nano Banana Pro API（Gemini 3 Pro Image）来生成新图像或编辑现有图像。

## 使用方法

使用绝对路径运行脚本（请勿先进入技能目录）：

**生成新图像：**
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "your image description" --filename "output-name.png" [--resolution 1K|2K|4K] [--api-key KEY]
```

**编辑现有图像：**
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "editing instructions" --filename "output-name.png" --input-image "path/to/input.png" [--resolution 1K|2K|4K] [--api-key KEY]
```

**重要提示：** 请始终从用户当前的工作目录运行脚本，以确保图像保存在用户的工作目录中，而不是技能目录中。

## 默认工作流程（草图 → 迭代 → 最终版本）

目标：快速迭代，避免在 4K 分辨率上浪费时间，直到得到满意的结果。

- **草图阶段（1K 分辨率）**：快速获取反馈
  - `uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "<草图提示>" --filename "yyyy-mm-dd-hh-mm-ss-draft.png" --resolution 1K`
- **迭代阶段**：逐步调整提示内容；每次迭代时使用新的文件名
  - 如果正在进行编辑，请在每次迭代中保持 `--input-image` 参数不变，直到满意为止。
- **最终版本（4K 分辨率）**：仅在提示内容确定后使用
  - `uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "<最终提示>" --filename "yyyy-mm-dd-hh-mm-ss-final.png" --resolution 4K`

## 分辨率选项

Gemini 3 Pro Image API 支持三种分辨率（分辨率需以大写 K 表示）：

- **1K**（默认）：约 1024 像素
- **2K**：约 2048 像素
- **4K**：约 4096 像素

用户请求与 API 参数的对应关系如下：
- 未指定分辨率 → 使用 `1K`
- “低分辨率”、“1080”、“1080p”、“1K” → `1K`
- “2K”、“2048”、“中等分辨率”、“正常分辨率” → `2K`
- “高分辨率”、“高画质”、“超高分辨率”、“4K”、“超高清” → `4K`

## API 密钥

脚本会按以下顺序检查 API 密钥：
1. `--api-key` 参数（如果用户在聊天中提供了密钥，则使用该参数）
2. `GEMINI_API_KEY` 环境变量

如果两者都不存在，脚本将输出错误信息并终止运行。

## 预检与常见故障（快速解决方法）

- **预检步骤：**
  - `command -v uv`（必须存在）
  - `test -n "\"GEMINI_API_KEY\"`（或使用 `--api-key` 参数）
  - 如果正在编辑图像：`test -f \"path/to/input.png\"`

- **常见故障：**
  - **错误：未提供 API 密钥。** → 设置 `GEMINI_API_KEY` 或使用 `--api-key` 参数
  - **错误：无法加载输入图像。** → 检查路径是否正确，文件是否可读；确保 `--input-image` 指向有效的图像文件
  - **API 错误（如“配额/权限/403”）** → 密钥错误、无访问权限或超出配额；尝试使用其他密钥/账户

## 文件名生成规则

文件名遵循以下格式：`yyyy-mm-dd-hh-mm-ss-名称.png`

**格式说明：**
- **时间戳：** 当前日期和时间（24 小时格式，例如 `yyyy-mm-dd-hh-mm-ss`）
- **名称：** 用连字符连接的描述性文本（通常为 1-5 个单词）
- **描述性部分** 应简洁明了
- 可以使用用户提供的提示或对话内容作为名称的依据
- 如果内容不明确，系统会生成随机标识符（例如 `x9k2`、`a7b3`）

**示例：**
- 提示：“一个宁静的日本花园” → `2025-11-23-14-23-05-japanese-garden.png`
- 提示：“山上的日落” → `2025-11-23-15-30-12-sunset-mountains.png`
- 提示：“生成一个机器人的图像” → `2025-11-23-16-45-33-robot.png`
- 如果提示内容不明确 → `2025-11-23-17-12-48-x9k2.png`

## 图像编辑

当用户需要修改现有图像时：
1. 确认用户是否提供了图像路径，或指定了当前目录中的图像文件
2. 使用 `--input-image` 参数指定图像文件的路径
3. 提示中应包含编辑指令（例如：“让天空看起来更富有戏剧性”、“移除人物”、“改为卡通风格”）
- 常见的编辑操作包括：添加/删除元素、调整颜色、模糊背景等

## 提示处理方式

- **生成新图像时：** 直接将用户的描述性文本传递给 `--prompt` 参数。只有在描述不够清晰时才进行修改。
- **编辑图像时：** 在 `--prompt` 中提供具体的编辑指令（例如：“在天空添加一道彩虹”、“将其调整为水彩画风格”）
- 在两种情况下，都要保留用户的创意意图。

## 提示模板（提高效率）

当用户描述模糊或需要精确编辑时，可以使用以下模板：

- **生成新图像的模板：**
  - “生成一幅 <主题> 的图像。风格：<风格>。构图：<构图方式>。光线：<光线效果>。背景：<背景类型>。调色板：<调色板颜色>。避免使用：<需要避免的元素>。”

- **编辑图像的模板（保留其他设置）：**
  - “仅修改：<具体修改内容>。其他部分保持不变：主题、构图/裁剪、姿势、光线、调色板、背景和整体风格。不要添加新元素。如果已有文字，请保持不变。”

## 输出结果

- 图像会以 PNG 格式保存在当前目录中（如果文件名中包含路径，则保存到指定路径）
- 脚本会输出生成图像的完整路径
- **注意：** 脚本不会显示图像内容，仅向用户提供保存路径

## 示例

**生成新图像：**
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "A serene Japanese garden with cherry blossoms" --filename "2025-11-23-14-23-05-japanese-garden.png" --resolution 4K
```

**编辑现有图像：**
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "make the sky more dramatic with storm clouds" --filename "2025-11-23-14-25-30-dramatic-sky.png" --input-image "original-photo.jpg" --resolution 2K
```