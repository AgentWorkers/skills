---
name: gemini-image-generation
description: '使用 Google GenAI SDK 通过 Gemini 生成或编辑图像。当用户在 OpenClaw 技能工作流中请求创建、转换、渲染或保存一张或多张图像时，可以使用此功能。'
argument-hint: 'prompt="<image prompt>" output="outputs/image.png" [input="assets/source.png"] [input="assets/source-2.png"] [aspectRatio="16:9"] [imageSize="2K"]'
metadata: {"openclaw":{"emoji":"🎨","requires":{"bins":["node"],"env":["GEMINI_API_KEY","GEMINI_MODEL_ID"]},"primaryEnv":"GEMINI_API_KEY","optionalEnv":"GEMINI_BASE_URL"}}
---
# 图像生成

当您需要根据文本提示创建一个或多个图像文件，或者使用 Gemini 工具编辑一个或多个现有图像时，请使用此技能。

## 前提条件

- 环境中必须包含 `GEMINI_API_KEY`。
- 环境中必须包含 `GEMINI_MODEL_ID`，并且该 ID 必须指向支持图像输出的模型。对于图像编辑功能，该模型还必须支持图像输入。
- `GEMINI_BASE_URL` 是可选的环境变量，用于自定义 API 端点；如果提供了该变量，请确保其后面没有斜杠（/）。
- 工作区环境中必须已安装 Node.js。
- 请从工作区根目录使用 `npm install` 命令安装所有依赖项。

## 使用场景

- 用户请求根据文本提示生成新的图像。
- 用户请求修改、重新设计、扩展或以其他方式编辑一个或多个现有图像。
- 用户希望将生成的图像保存到工作区文件中。
- 该任务应通过可重用的 OpenClaw 技能来完成，而不是使用临时的 SDK 代码。

## 执行步骤

1. 将用户的请求转换为一个明确的图像生成指令。
2. 如果用户提供了源图像，请在工作区内选择或确认输入文件的路径。
3. 如果用户指定了目标宽高比或尺寸，请通过 `--aspectRatio` 和 `--imageSize` 参数传递这些值。
4. 选择工作区内的输出路径（除非用户已经指定了路径）。
5. 对于文本转图像的操作，运行 [generate-image.mjs](./scripts/generate-image.mjs) 文件，并传入 `--prompt`、`--output` 以及可选的图像配置参数。
6. 对于图像编辑操作，运行 [edit-image.mjs](./scripts/edit-image.mjs) 文件，并传入 `--prompt`、一个或多个 `--input` 参数、`--output` 以及可选的图像配置参数。
7. 从环境变量 `GEMINI_API_KEY` 中读取 API 密钥，从 `GEMINI_MODEL_ID` 中读取模型 ID。
8. （可选）从环境变量 `GEMINI_BASE_URL` 中读取自定义 API 端点的基地址。
9. 将保存的图像路径返回给用户。

## 示例命令

```powershell
node ./.claude/skills/gemini-image-generation/scripts/generate-image.mjs --prompt "根据 Gemini 主题，生成一张精美的餐厅中‘纳米香蕉盘’的图片" --output "outputs/gemini-native-image.png"
```

```powershell
node ./.claude/skills/gemini-image-generation/scripts/generate-image.mjs --prompt "生成一张宽屏的电影风格食品图片，展示精美的餐厅中的‘纳米香蕉盘’，并设置宽高比为 16:9，图像大小为 2K" --output "outputs/gemini-wide.png" --aspectRatio "16:9" --imageSize "2K"
```

```powershell
node ./.claude/skills/gemini-image-generation/scripts/edit-image.mjs --prompt "将这张猫的图片修改成水彩插画，展示它在 Gemini 星座下的精美餐厅里吃‘纳米香蕉’" --input "inputs/cat.png" --output "outputs/cat-watercolor.png" --aspectRatio "5:4" --imageSize "2K"
```

```powershell
node ./.claude/skills/gemini-image-generation/scripts/edit-image.mjs --prompt "生成一张办公室团队的照片，照片中的人都在做鬼脸" --input "inputs/person-1.jpg" --input "inputs/person-2.jpg" --input "inputs/person-3.jpg" --output "outputs/group-photo.png"
```

## 注意事项

- 脚本会输出模型生成的文本内容（以 `TEXT:` 标签显示）以及每个保存后的图像文件的路径（以 `IMAGE:` 标签显示）。
- 最终的 JSON 结果仅包含生成的图像路径和可选的图像配置信息，因此提示内容、模型 ID 和源图像路径不会被记录在日志中。
- 如果模型返回多个图像，脚本会分别将它们保存为 `name-1.png`、`name-2.png` 等文件。
- `edit-image.mjs` 支持多次使用 `--input` 参数；您也可以将多个文件路径用逗号分隔后传递给单个 `--input` 参数。
- `edit-image.mjs` 会自动识别输入文件的格式（`.png`、`.jpg`、`.jpeg` 或 `.webp`），您可以为所有输入文件指定统一的 `--mime-type` 参数，或者为每个输入文件分别指定 `--mime-type`。
- 两个脚本都支持 `--aspectRatio` 和 `--imageSize` 参数；它们也接受 `--aspect-ratio` 和 `--image-size`（大小写不敏感的形式）。
- 只有在提供了至少其中一个参数时，脚本才会发送 `config.imageConfig` 数据。