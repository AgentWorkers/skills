---
name: nano-gpt
description: >
  **使用说明：**  
  当任务需要通过本地 `nano-gpt` CLI 以及 OpenClaw 或 ClawHub 工作流程中的配套脚本来利用 NanoGPT API 进行文本、图像或视频生成时，请使用此技能。使用此技能前，您需要拥有一个 NanoGPT API 令牌。
---
# NanoGPT 技能

当需要通过本地终端环境调用 NanoGPT API 时，请使用此技能。NanoGPT 的官方文档将其描述为一个用于文本、图像和视频生成的 API，其文本生成功能通常符合 OpenAI 的标准。该仓库提供了该 API 的本地命令行界面（CLI）和技能封装脚本，而非通用的提示辅助工具。建议使用 `scripts/` 目录中的封装脚本，以确保 OpenClaw 和直接使用 CLI 时行为一致。

**官方文档：** <https://docs.nano-gpt.com/>

## 前提条件检查**

在调用此技能之前，请确保 CLI 可用：

```bash
./scripts/models.sh --json
```

如果由于本地 CLI 尚未构建而失败，请执行以下操作：

```bash
npm install
npm run build
```

如果本地没有该仓库，请先安装已发布的 CLI：

```bash
npm install -g nano-gpt-cli
```

**身份验证**：此技能需要一个 NanoGPT API 令牌。请将令牌设置到 `NANO_GPT_API_KEY` 变量中：

```bash
export NANO_GPT_API_KEY=YOUR_NANO_GPT_TOKEN
```

或者配置一次并将其存储在本地 `nano-gpt-cli` 用户配置文件中：

```bash
nano-gpt config set api-key YOUR_API_KEY
```

**可选的环境变量设置：**

```bash
export NANO_GPT_MODEL=moonshotai/kimi-k2.5
export NANO_GPT_IMAGE_MODEL=qwen-image
export NANO_GPT_VIDEO_MODEL=kling-video-v2
export NANO_GPT_BASE_URL=https://nano-gpt.com
export NANO_GPT_OUTPUT_FORMAT=text
```

## 快速入门**

- **文本提示：**  
  使用以下命令进行文本提示：  
  ```bash
./scripts/prompt.sh "Summarize the latest build logs."
```

- **流式多模态提示：**  
  使用以下命令进行流式多模态提示：  
  ```bash
./scripts/prompt.sh "Describe this image." --image ./assets/example.png
```

- **交互式聊天：**  
  使用以下命令进行交互式聊天：  
  ```bash
./scripts/chat.sh
```

- **图像生成：**  
  使用以下命令生成图像：  
  ```bash
./scripts/image.sh "A cinematic product shot of a silver mechanical keyboard" --output output/keyboard.png
```

- **图像到图像生成：**  
  使用以下命令生成图像到图像的转换结果：  
  ```bash
./scripts/image.sh "Turn this product photo into a watercolor ad" --image ./assets/product.png --output output/product-watercolor.png
```

- **视频生成：**  
  使用以下命令生成视频：  
  ```bash
./scripts/video.sh "A cinematic drone flyover of a neon coastal city at dusk" --duration 5 --output output/neon-city.mp4
```

## 工作流程**

1. 使用 `scripts/prompt.sh` 进行一次性文本或视觉提示。
2. 使用 `scripts/chat.sh` 进行交互式对话。
3. 使用 `scripts/image.sh` 进行文本到图像或图像到图像的转换。
4. 使用 `scripts/video.sh` 进行文本到视频或图像到视频的转换。
5. 当视频生成是异步的且需要后续状态检查时，使用 `nano-gpt video-status REQUEST_ID` 命令。
6. 当需要查询模型信息时，使用 `scripts/models.sh --json` 命令。
7. 尽量使用命令行参数而非直接修改脚本，以保持封装脚本的简洁性。

## 参考资料**

- **命令参考：** `references/cli.md`
- **常见的 OpenClaw 工作流程：** `references/workflows.md`

## 规范与限制：

- 建议优先使用封装脚本，而非直接调用 NanoGPT 的 HTTP API。
- 仅在用户需要调用 NanoGPT API 时使用此技能。
- 请勿在提示或日志中泄露敏感信息；使用配置文件或环境变量来存储 API 密钥。
- 仅上传用户明确提供的本地图像或视频文件；切勿自行搜索文件系统中的媒体文件。
- 将本地输入的 `--image` 和 `--video` 参数视为远程上传操作；除非用户明确要求，否则不要发送敏感的截图、导出文件或录音。
- 所有提示内容及提供的媒体文件都将发送到配置的 NanoGPT API 端点（默认为 `https://nano-gpt.com`）。
- 如果其他工具或代理需要解析输出结果，请使用 `--json` 参数。
- 在 `scripts/image.sh` 中使用 `--output` 参数来指定输出文件的路径；在 `scripts/video.sh` 中使用该参数来指定最终生成的 MP4 文件的保存路径。