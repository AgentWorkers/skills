---
name: vlmrun-cli-skill
description: "使用 VLM 运行命令行工具（`vlmrun`）与 Orion 视觉 AI 代理进行交互。该工具支持处理图像、视频和文档，并支持自然语言处理功能。可执行的操作包括：图像理解/生成、对象检测、光学字符识别（OCR）、视频摘要生成、文档内容提取、图像生成、视觉 AI 对话等。具体命令示例有：`generate an image/video`（生成图像/视频）、`analyze this image/video`（分析此图像/视频）、`extract text from`（从文件中提取文本）、`summarize this video`（生成视频摘要）、`process this PDF`（处理 PDF 文件）。"
---

# VLM Run CLI

通过 CLI 与 VLM Run 的 Orion 视觉 AI 代理进行交互。

## 设置
```bash
uv venv && source .venv/bin/activate
uv pip install "vlmrun[cli]"
```

## 环境变量

您需要将以下变量加载到您的环境中，以便 CLI 能够使用它们。您可以将 [./env](./env) 文件添加到您的环境中。

| 变量 | 类型 | 描述 |
|----------|------|-------------|
| `VLMRUN_API_KEY` | 必需 | 您的 VLM Run API 密钥（必需） |
| `VLMRUN_BASE_URL` | 可选 | 基础 URL（默认：`https://agent.vlm.run/v1`） |
| `VLMRUN_CACHE_DIR` | 可选 | 缓存目录（默认：`~/.vlmrun/cache/artifacts/`） |

## 命令
```bash
vlmrun chat "<prompt>" -i input.jpg [options]
```

## 选项

| 标志 | 描述 |
|------|-------------|
| `-p, --prompt` | 提示文本、文件路径或 `stdin` |
| `-i, --input` | 输入文件（图像、视频、文档）（可重复使用） |
| `-o, --output` | 生成结果的目录（默认：`~/.vlmrun/cache/artifacts/`） |
| `-m, --model` | `vlmrun-orion-1:fast`、`vlmrun-orion-1:auto`（默认）、`vlmrun-orion-1:pro` |
| `-s, --session` | 可选：用于继续之前的会话的会话 ID |
| `-j, --json` | 原始 JSON 输出 |
| `-ns, --no-stream` | 禁用流式传输 |
| `-nd, --no-download` | 跳过结果文件的下载 |

## 示例

### 图像处理
```bash
vlmrun chat "Describe what you see in this image in detail" -i photo.jpg
vlmrun chat "Detect and list all objects visible in this scene" -i scene.jpg
vlmrun chat "Extract all text and numbers from this document image" -i document.png
vlmrun chat "Compare these two images and describe the differences" -i before.jpg -i after.jpg
```

### 图像生成
```bash
vlmrun chat "Generate a photorealistic image of a cozy cabin in a snowy forest at sunset" -o ./generated
vlmrun chat "Remove the background from this product image and make it transparent" -i product.jpg -o ./output
```

### 视频处理
```bash
vlmrun chat "Summarize the key points discussed in this meeting video" -i meeting.mp4
vlmrun chat "Find the top 3 highlight moments and create short clips from them" -i sports.mp4
vlmrun chat "Transcribe this lecture with timestamps for each section" -i lecture.mp4 --json
```

### 视频生成
```bash
vlmrun chat "Generate a 5-second video of ocean waves crashing on a rocky beach at golden hour" -o ./videos
vlmrun chat "Create a smooth slow-motion video from this image" -i ocean.jpg -o ./output
```

### 文档处理
```bash
vlmrun chat "Extract the vendor name, line items, and total amount" -i invoice.pdf --json
vlmrun chat "Summarize the key terms and obligations in this contract" -i contract.pdf
```

### 提示输入源
```bash
# Direct prompt
vlmrun chat "What objects and people are visible in this image?" -i photo.jpg

# Prompt from file
vlmrun chat -p long_prompt.txt -i photo.jpg

# Prompt from stdin
echo "Describe this image in detail" | vlmrun chat - -i photo.jpg
```

### 继续之前的会话
如果您希望保留之前的对话和生成的结果文件，可以使用 `-s` 标志，并提供开始会话时生成的会话 ID 来继续会话。

```bash
# Start a new session of an image generation task where a new character is generated
vlmrun chat "Create an iconic scene of a ninja in a forest, practicing his skills with a katana?" -i photo.jpg

# Use the previous chat session in context to retain the same character and scene context (where the session ID is <session_id>)
vlmrun chat "Create a new scene with the same character meditating under a tree" -i photo.jpg -s <session_id>
```

### 跳过结果文件下载
如果您想跳过结果文件的下载，可以使用 `-nd` 标志。
```bash
vlmrun chat "What objects and people are visible in this image?" -i photo.jpg -nd
```

## 注意事项

- 使用 `-o ./<目录>` 可以将生成的结果文件（图像、视频）保存在当前工作目录的相对路径下。
- 如果不使用 `-o`，结果文件将保存在 `~/.vlmrun/cache/artifacts/<session_id>/` 目录下。
- 可以同时上传多个输入文件。