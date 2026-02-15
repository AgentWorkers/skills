---
name: nano-banana-pro-openrouter
description: 使用 OpenRouter 通过 Nano Banana Pro 生成图像。当用户请求生成图像、提到 Nano Banana Pro、Gemini 3 Pro 图像或 OpenRouter 图像生成时，请使用此方法。
---

# Nano Banana Pro 图像生成

使用 OpenRouter 的 Nano Banana Pro（Gemini 3 Pro 图像预览功能）生成新的图像。

## 使用方法

使用绝对路径运行脚本（请勿先进入技能目录）：

生成新图像：
```bash
sh ~/.openclaw/workspace/skills/nano-banana-pro-openrouter/scripts/generate_image.sh --prompt "your image description" [--filename "output-name.png" | --filename auto] [--resolution 1K|2K|4K] [--api-key KEY]
```
注意：当前 shell 版本仅支持图像生成（不支持输入图像的编辑）。

重要提示：
- 图像始终保存在 `~/.openclaw/workspace/outputs/nano-banana-pro-openrouter` 目录下。
- 如果 `--filename` 参数包含路径，仅使用文件名（不含路径部分）。

## 默认工作流程（草图 -> 迭代 -> 最终版本）

目标：快速迭代，避免在生成 4K 图像时浪费时间，直到生成出正确的图像为止。

- **草图版本（1K 分辨率）**：快速获取反馈：
  ```bash
  sh ~/.openclaw/workspace/skills/nano-banana-pro-openrouter/scripts/generate_image.sh --prompt "<草图提示>" --filename auto --resolution 1K
  ```
- **迭代版本**：对提示进行微调；每次运行时都使用新的文件名。
- **最终版本（4K 分辨率）**：仅在提示内容确定后生成：
  ```bash
  sh ~/.openclaw/workspace/skills/nano-banana-pro-openrouter/scripts/generate_image.sh --prompt "<最终提示>" --filename auto --resolution 4K
  ```

## 分辨率选项

Gemini 3 Pro 图像 API 支持以下三种分辨率（分辨率值需以大写字母 K 表示）：
- 1K（默认）：约 1024 像素
- 2K：约 2048 像素
- 4K：约 4096 像素

用户请求与 API 参数的对应关系：
- 未指定分辨率时：使用 1K 分辨率
- “low resolution”、“1080”、“1080p”、“1K”：1K 分辨率
- “2K”、“2048”、“normal”、“medium resolution”：2K 分辨率
- “high resolution”、“high-res”、“hi-res”、“4K”、“ultra”：4K 分辨率

## API 密钥和基础 URL

脚本会按以下顺序查找 API 密钥：
1. `--api-key` 参数（如果用户在聊天中提供了密钥，则使用该参数）
2. `OPENROUTER_API_KEY` 环境变量

API 基础 URL 需要通过 `OPENROUTER_BASE_URL` 设置。请使用 OpenRouter 的完整聊天完成端点地址（例如：`https://openrouter.ai/api/v1/chat/completions`）。

脚本还会自动加载 `.env` 文件（如果存在）：
- 当前工作目录下的 `.env` 文件
- 技能目录下的 `.env` 文件

重要提示：如果存在 `.env` 文件，无需提前询问用户输入密钥。直接运行脚本；只有在脚本因“未提供 API 密钥”而报错时才需要用户输入密钥。

### OpenClaw 聊天执行规则

- OpenClaw 不会自动读取技能目录下的 `.env` 文件。
- 如果 `~/.openclaw/workspace/skills/nano-banana-pro-openrouter/.env` 文件存在：
  1. 使用 `read` 命令读取该文件。
  2. 提取 `OPENROUTER_API_KEY` 和 `OPENROUTER_BASE_URL`。
  3. 运行脚本时必须通过 `--api-key` 参数传递这些密钥。
- 仅在 `.env` 文件缺失或无法读取密钥时才询问用户。
- 如果用户请求带有时间戳的文件名，建议使用 `--filename auto` 选项（避免手动输入日期）。

## 预检查及常见故障（快速解决方法）

**预检查**：
- `command -v sh` 命令必须可用。
- `command -v curl` 命令必须可用。
- `command -v base64` 命令必须可用。

**常见故障**：
- **错误：未提供 API 密钥。**：读取 `.env` 文件后使用 `--api-key` 重新尝试；如果仍然失败，请让用户设置 `OPENROUTER_API_KEY`。
- **错误：未提供 API 基础 URL。**：确保 `OPENROUTER_BASE_URL` 设置为正确的聊天完成端点地址。
- **错误：无法加载输入图像。**：检查路径是否正确或文件是否可读；确认 `--input-image` 参数指向有效的图像文件。
- **API 错误（如 quota/permission/403）**：可能是密钥错误、无访问权限或超出使用限制；尝试使用其他密钥或账户。

## 文件名生成规则

生成的文件名遵循以下格式：`yyyy-mm-dd-hh-mm-ss-name.png`：
- **时间戳**：当前日期和时间（24 小时格式，例如 `2025-11-23-14-23-05`）。
- **文件名**：描述性的小写文本（通常包含 1-5 个单词）。
- **文件名生成方式**：使用用户提供的提示或对话内容；如果内容不明确，可以使用默认名称 “image”。
- **示例**：
  - 提示：“一个宁静的日本花园” → `2025-11-23-14-23-05-japanese-garden.png`
  - 提示：“山间的日落” → `2025-11-23-15-30-12-sunset-mountains.png`
  - 提示：“生成一个机器人的图像” → `2025-11-23-16-45-33-robot.png`
  - 如果提示内容不明确 → `2025-11-23-17-12-48-image.png`

**提示：**为避免时间戳错误，建议使用 `--filename auto` 选项，让脚本根据系统时间自动生成文件名。

## 图像编辑（Shell 版本不支持）

当前 shell 脚本仅支持生成新图像，不支持编辑输入图像。

## 提示处理

在生成图像时，直接将用户的描述性文本作为参数传递给 `--prompt`。只有在描述不够清晰时才需要重新调整。

## 提示模板（适用于高使用频率的场景）

当用户描述模糊或需要精确编辑时，可以使用以下模板：
```
生成一个 <主题> 的图像。风格：<风格>。构图：<构图方式>。光线：<光线效果>。背景：<背景类型>。颜色调色板：<调色板>。避免使用：<需要避免的元素列表>。
```

## 输出结果

- 生成的 PNG 图像保存在 `~/.openclaw/workspace/outputs/nano-banana-pro-openrouter` 目录下。
- 如果 `--filename` 参数包含路径，仅使用文件名部分。
- 脚本会输出图像的完整路径。
- 脚本还会为每张图像生成 `MEDIA_URL=file:///absolute/path` 的值。

### 在回复中显示图像

- 使用 `MEDIA_URL` 值将图像嵌入模型响应中。
- 在 OpenClaw 中，建议使用 `file://` 格式的 URL 来发送图像。
- 也可以在文本中附上文件的完整路径以供参考。

## 示例

生成新图像：
```bash
sh ~/.openclaw/workspace/skills/nano-banana-pro-openrouter/scripts/generate_image.sh --prompt "A serene Japanese garden with cherry blossoms" --filename auto --resolution 4K
```