---
name: ComfyUI
description: 通过 HTTP API 运行本地的 ComfyUI 工作流程。当用户请求运行 ComfyUI、根据文件路径/名称执行某个工作流程，或提供符合 API 格式的 JSON 数据时，可以使用此方法；系统支持随资产一起提供的默认工作流程。
read_when:
  - User asks to generate images with ComfyUI
  - User provides a workflow file or JSON to run
  - User describes an image to generate (subject, style, scene)
  - User pastes or sends a list of model weight URLs to download for ComfyUI
metadata: {"clawdbot":{"emoji":"🖼️","requires":{"bins":["python3"]}}}
---

# ComfyUI 运行器

## 概述
使用 API 格式的 JSON 在本地服务器（默认为 127.0.0.1:8188）上运行 ComfyUI 工作流程，并返回生成的图像。

## 在运行前编辑工作流程
运行脚本仅接受 `--workflow <路径>` 参数。在运行之前，你必须根据自己对 ComfyUI API 格式的了解，**检查并编辑工作流程 JSON 文件**。不要假设节点 ID、`class_type` 名称或 `_meta.title` 值是固定的——用户可能已经更新了默认的工作流程或提供了自定义的工作流程。

**对于每次运行（包括默认工作流程）：**
1. 读取工作流程 JSON 文件（默认路径为 `skills/comfyui/assets/default-workflow.json`，或用户提供的路径/文件）。
2. **识别与提示相关的节点**：查看节点图，找到包含主要文本提示的节点——例如 `PrimitiveStringMultiline`、`CLIPTextEncode`（用于生成正文本的节点），或任何具有 `_meta.title` 或 `class_type` 为 “Prompt” / “positive” / “text” 的节点。根据用户提供的信息（主题、风格、光照、质量等），更新相应的输入内容（例如 `inputs.value` 或编码器的文本输入）。如果用户没有要求自定义图像，可以保留现有的提示内容，或者仅在必要时进行微调。
3. **可选地识别风格/前缀相关的节点**——例如 `StringConcatenate` 节点，或用于设置风格的第二个字符串输入。如果用户指定了特定的风格或需要清除默认前缀，请设置这些节点。
4. **可选地设置新的随机种子值**：找到类似采样器的节点（例如 `KSampler`、`BasicGuider` 或任何具有 `seed` 输入的节点），并将 `seed` 设置为一个新的随机整数，以确保每次运行结果不同。
5. 将修改后的工作流程文件写入临时文件（例如 `skills/comfyui/assets/tmp-workflow.json`）。如果需要使用内嵌的 Python 代码，请使用 `~/ComfyUI/venv/bin/python`；不要直接使用 `python` 命令。
6. 运行命令：`comfyui_run.py --workflow <编辑后的 JSON 文件路径>`。

如果工作流程的结构不明确，或者你找不到提示/采样器节点，请直接运行脚本，并仅更改你能可靠识别的部分。对于用户提供的任意 JSON 文件，也采用相同的处理方式：先检查，然后根据你的知识进行编辑，最后再运行。

## 运行脚本（单一职责）
```bash
~/ComfyUI/venv/bin/python skills/comfyui/scripts/comfyui_run.py \
  --workflow <path-to-workflow.json>
```

该脚本仅负责将工作流程放入队列并等待其完成。它会输出包含 `prompt_id` 和 `images` 的 JSON 数据。所有与提示/风格/种子相关的更改都需你在 JSON 文件中预先完成。

## 如果服务器无法访问
如果运行脚本因连接错误（例如连接到 127.0.0.1:8188 时被拒绝或超时）而失败，可能是因为 ComfyUI 未安装或未运行。

**检查：** `~/ComfyUI` 目录是否存在，并且其中是否包含 `main.py` 文件？

- **如果未安装 ComfyUI：** 安装 ComfyUI（例如克隆仓库、创建虚拟环境、安装依赖项，然后启动服务器）。示例：
  ```bash
  git clone https://github.com/comfyanonymous/ComfyUI.git ~/ComfyUI
  cd ~/ComfyUI
  python3 -m venv venv
  ~/ComfyUI/venv/bin/pip install -r requirements.txt
  ```
  接着启动服务器（详见下方说明）。告知用户，根据工作流程的不同，他们可能还需要将模型权重文件安装到 `~/ComfyUI/models/` 目录中。

- **如果已安装但未运行：** 启动 ComfyUI 服务器，确保 API 在 8188 端口上可用。示例：
  ```bash
  ~/ComfyUI/venv/bin/python ~/ComfyUI/main.py --listen 127.0.0.1
  ```
  可以在后台或单独的终端中运行服务器，以确保其持续运行。之后再尝试运行工作流程。

在路径引用时，请使用 `~`（或用户的 home 目录）以确保脚本能在用户的机器上正常运行。

## 从 URL 下载模型权重文件
当用户提供模型权重的 URL 列表（每行一个 URL，或用逗号分隔）时，将这些文件下载到 ComfyUI 安装目录中，以便后续的工作流程可以使用这些文件。

1. **规范列表格式**：确保每行只有一个 URL；删除空行和注释（以 `#` 开头的行）。
2. 使用 ComfyUI 的基础路径（默认为 `~/ComfyUI`）运行下载脚本。该脚本会使用 [pget](https://github.com/replicate/pget) 来进行并行下载；如果 `pget` 未安装在系统中，它会自动将其安装到 `~/.local/bin` 目录中（无需使用 `sudo`）。如果 `pget` 无法安装（例如由于操作系统或架构不支持），则会使用内置的下载工具。为了确保脚本正确运行，请使用 ComfyUI 的虚拟环境 Python：  
   ```bash
   ~/ComfyUI/venv/bin/python skills/comfyui/scripts/download_weights.py --base ~/ComfyUI
   ```
   可以将 URL 作为参数传递，或者将文件/列表通过标准输入（stdin）传递：
   ```bash
   echo "https://example.com/model.safetensors" | ~/ComfyUI/venv/bin/python skills/comfyui/scripts/download_weights.py --base ~/ComfyUI
   ```
   或者将用户提供的列表保存到临时文件中，然后运行脚本：
   ```bash
   ~/ComfyUI/venv/bin/python skills/comfyui/scripts/download_weights.py --base ~/ComfyUI < /tmp/weight_urls.txt
   ```
   如果需要使用内置下载工具（不使用 `pget`），请添加 `--no-pget` 参数。
3. **子文件夹**：脚本会根据 URL 或文件名自动推断 ComfyUI 模型的子文件夹（例如 `vae`、`clip`、`loras`、`checkpoints`、`text_encoders`、`controlnet`、`upscale_models`）。用户也可以在每行指定子文件夹，例如 `https://.../model.safetensors vae`。你也可以使用 `--subfolder loras` 参数设置默认子文件夹，这样所有相关文件都会被保存到 `models/loras/` 目录中。
4. **处理现有文件**：默认情况下，脚本会跳过磁盘上已存在的文件；如果需要覆盖现有文件，请使用 `--overwrite` 参数。
5. **文件路径**：文件会被保存在 `~/ComfyUI/models/<子文件夹>/` 目录下。请告知用户文件的保存位置，并告诉他们在 ComfyUI 服务器重新启动后可以再次运行工作流程。

支持的子文件夹（位于 `ComfyUI/models/` 目录下）：`checkpoints`、`clip`、`clip_vision`、`controlnet`、`diffusion_models`、`embeddings`、`loras`、`text_encoders`、`unet`、`vae`、`vae_approx`、`upscale_models` 等。如果自动推断的子文件夹不正确，可以使用 `--subfolder <名称>` 参数进行手动指定。

## 运行后的处理
生成的输出文件会被保存在 `ComfyUI/output/` 目录下。可以使用脚本输出中的 `images` 列表来定位文件的位置（文件名 + 子文件夹路径）。

### ⚠️ 必须将结果发送给用户
ComfyUI 运行成功后，**必须将生成的图像发送给用户**。不要仅回复文件名或直接返回 `NO_REPLY`。

1. 从脚本输出中解析 `images` 数据（每个图像包含 `filename`、`subfolder`、`type` 信息）。
2. 构建完整的文件路径：`ComfyUI/output/` + 子文件夹 + 文件名（例如 `ComfyUI/output/z-image_00007_.png`）。
3. 通过用户使用的通道将图像发送给他们（例如使用消息发送工具，并提供图像的完整路径）。如果需要，可以附上简短的说明文字（例如 “这是生成的图像。” 或 “东京街道场景。”）。

每次成功的运行都应确保用户能够收到生成的图像。切勿仅提供文件名而不进行任何交付。

## 资源

### 脚本：
- `comfyui_run.py`：负责将工作流程放入队列、等待完成，并输出 `prompt_id` 和 `images` 数据。无需参数——运行前你需要先编辑 JSON 文件。
- `download_weights.py`：将模型权重文件的 URL 下载到 `~/ComfyUI/models/<子文件夹>/` 目录中。该脚本会使用 [pget](https://github.com/replicate/pget) 来进行下载；如果 `pget` 未安装，会自动安装到 `~/.local/bin` 目录中。支持参数：`--base`、`--subfolder`、`--overwrite`、`--no-pget`。如果未指定子文件夹，脚本会根据 URL 或文件名自动推断。

### 资源文件：
- `default-workflow.json`：默认的工作流程文件。你可以复制并编辑其中的提示内容、风格设置和随机种子值，然后使用编辑后的文件路径运行工作流程；或者直接使用默认设置进行通用运行。