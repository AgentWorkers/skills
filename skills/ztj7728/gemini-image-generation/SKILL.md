---
name: gemini-image-generation
description: '使用 Google GenAI SDK 通过 Gemini 生成或编辑图像。当用户在 OpenClaw 技能工作流中请求创建、转换、渲染或保存一张或多张图像时，可以使用此功能。'
argument-hint: 'prompt="<image prompt>" output="outputs/image.png" [input="assets/source.png"] [input="assets/source-2.png"] [aspectRatio="16:9"] [imageSize="2K"]'
---
# 图像生成

当您需要根据文本提示创建一个或多个图像文件，或使用 Gemini 工具编辑一个或多个现有图像时，请使用此技能。

## 要求

- 环境中必须包含 `GEMINI_API_KEY`。
- 环境中必须包含 `GEMINI_MODEL_ID`，且该 ID 必须指向支持图像输出的模型。对于图像编辑功能，该模型还必须支持图像输入。
- `GEMINI_BASE_URL` 是可选的环境变量，用于自定义 API 端点；如果提供该变量，请确保其末尾没有斜杠。
- 工作区环境中必须安装了 Node.js。
- 请通过 `npm install` 从工作区根目录安装所有依赖项。

## 使用场景

- 用户请求根据文本提示生成新图像。
- 用户请求修改、重新设计、扩展或以其他方式编辑一个或多个现有图像。
- 用户希望将生成的图像保存到工作区文件中。
- 该任务应通过可重用的 OpenClaw 技能来完成，而不是使用临时的 SDK 代码。

## 执行步骤

1. 将用户请求转换为明确的图像生成指令。
2. 如果用户提供了源图像，请在工作区内选择或确认输入文件的路径。
3. 如果用户指定了目标宽高比或尺寸，请将其作为 `--aspectRatio` 和 `--imageSize` 参数传递。
4. 选择工作区内的输出路径（除非用户已经指定了路径）。
5. 对于文本转图像的操作，运行 `[generate-image.mjs](./scripts/generate-image.mjs)`，并传入 `--prompt`、`--output` 及可选的图像配置参数。
6. 对于图像编辑操作，运行 `[edit-image.mjs](./scripts/edit-image.mjs)`，并传入 `--prompt`、一个或多个 `--input` 参数、`--output` 及可选的图像配置参数。
7. 从环境变量 `GEMINI_API_KEY` 中读取 API 密钥，从 `GEMINI_MODEL_ID` 中读取模型 ID。
8. （可选）从环境变量 `GEMINI_BASE_URL` 中读取自定义 API 端点的基地址。
9. 将保存的图像路径返回给用户。

## 命令示例

```powershell
node ./.claude/skills/gemini-image-generation/scripts/generate-image.mjs --prompt "根据 Gemini 主题，生成一张‘纳米香蕉盘’在高档餐厅中的图片" --output "outputs/gemini-native-image.png"
```

```powershell
node ./.claude/skills/gemini-image-generation/scripts/generate-image.mjs --prompt "生成一张宽屏的、具有 Gemini 主题的‘纳米香蕉盘’在高档餐厅中的美食照片" --output "outputs/gemini-wide.png" --aspectRatio "16:9" --imageSize "2K"
```

```powershell
node ./.claude/skills/gemini-image-generation/scripts/edit-image.mjs --prompt "将这只猫修改成一幅水彩画，让它正在高档餐厅里‘吃’一个‘纳米香蕉’，背景为 Gemini 星座" --input "inputs/cat.png" --output "outputs/cat-watercolor.png" --aspectRatio "5:4" --imageSize "2K"
```

```powershell
node ./.claude/skills/gemini-image-generation/scripts/edit-image.mjs --prompt "生成一张办公室团队的照片，照片中的人都在做鬼脸" --input "inputs/person-1.jpg" --input "inputs/person-2.jpg" --input "inputs/person-3.jpg" --output "outputs/group-photo.png"
```

## 注意事项

- 脚本会输出模型生成的文本（以 `TEXT:` 标识）以及每个保存后的图像文件（以 `IMAGE:` 标识）。
- 如果模型返回多个图像，脚本会分别将它们保存为 `name-1.png`、`name-2.png` 等文件。
- `edit-image.mjs` 支持多次使用 `--input` 参数；您也可以将多个文件路径用逗号分隔后传递给一个 `--input` 参数。
- `edit-image.mjs` 会自动识别输入文件的格式（`.png`、`.jpg`、`.jpeg` 或 `.webp`）。您可以为所有输入文件指定一个 `--mime-type` 参数，或者为每个输入文件分别指定 `--mime-type`。
- 两个脚本都支持 `--aspectRatio` 和 `--imageSize` 参数；它们也接受大写形式的参数（如 `--aspect-ratio` 和 `--image-size`）。
- 只有在提供了至少其中一个参数时，脚本才会发送 `config.imageConfig`。