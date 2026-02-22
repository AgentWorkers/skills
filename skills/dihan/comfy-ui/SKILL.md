---
name: comfyui
description: 使用本地的 ComfyUI 实例生成高质量图像。适用于用户希望通过自己的硬件和自定义工作流程来执行私密、高效的图像生成操作的情况。前提是必须有一个正在运行的 ComfyUI 服务器，并且该服务器能够通过本地网络访问。
metadata:
  {
    "openclaw":
      {
        "emoji": "🎨",
        "requires": { "env": ["COMFYUI_SERVER_ADDRESS"] },
      },
  }
---
# ComfyUI 本地技能

该技能允许 OpenClaw 通过连接到本地网络中运行的 ComfyUI 实例来生成图像。

## 设置

1. **服务器地址：** 将 `COMFYUI_SERVER_ADDRESS` 环境变量设置为你的 PC 的 IP 地址和端口（例如：`http://192.168.1.119:8189`）。
2. **API 模式：** 确保在 ComfyUI 的设置中开启了 **“启用开发模式”**，以允许 API 交互。

## 使用方法

### 生成图像
运行内部生成脚本，并提供相应的提示：
```bash
python3 {skillDir}/scripts/comfy_gen.py "your image prompt" $COMFYUI_SERVER_ADDRESS
```

### 使用自定义工作流程
将你的 API JSON 工作流程文件放入 `workflows/` 文件夹中，然后指定文件路径：
```bash
python3 {skillDir}/scripts/comfy_gen.py "your prompt" $COMFYUI_SERVER_ADDRESS --workflow {skillDir}/workflows/my_workflow.json
```

## 特点
- **默认使用 SDXL 工作流程：** 默认使用高质量的 SDXL 工作流程（Juggernaut XL）。
- **自动备份：** 设计用于将生成的图像保存到 `image-gens/` 文件夹中，并可配置为同步到本地文档文件夹。
- **自定义工作流程：** 支持保存在 `workflows/` 文件夹中的外部 API JSON 工作流程。脚本会自动尝试将你的提示和随机种子插入到工作流程节点中。

## 实现细节
该技能使用一个 Python 辅助脚本（`scripts/comfy_gen.py`）来处理与 ComfyUI API 的 WebSocket/HTTP 通信、排队提示内容以及下载生成的图像。

## ComfyUI 图像生成注意事项：

1. **服务器地址：**
    * ComfyUI 服务器地址需要作为 `comfy_gen.py` 脚本的直接参数传递，而不仅仅是作为环境变量。
    * 例如：`python3 ... "你的提示" http://192.168.1.119:8189 ...`

2. **工作流程文件路径：**
    * 当指定的工作流程文件路径包含空格或特殊字符时，必须用单引号括起来，以便脚本能够正确解析。
    * 例如：`--workflow '/path/to/your/workflow file name.json'`

3. **Lora 权重控制：**
    * 目前的 `comfy_gen.py` 脚本没有直接用于控制 Lora 权重的参数（例如，将 'l1lly' Lora 设置为 0.90）。这可能需要在工作流程 JSON 文件中进行配置，或者对脚本本身进行修改。

4. **输出文件名：**
    * 生成的图像默认可能会使用临时文件名（例如：`ComfyUI_temp_...png`），而不是更具描述性的文件名。

5. **ComfyUI 设置：**
    * 确保在 ComfyUI 的设置中开启了 “启用开发模式”，以支持 API 交互。