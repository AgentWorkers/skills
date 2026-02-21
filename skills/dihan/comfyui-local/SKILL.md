---
name: comfyui-local
description: 使用本地的 ComfyUI 实例生成高质量图像。适用于用户希望通过自己的硬件和自定义工作流程来实现私有、高效的图像生成需求的情况。前提是必须有一个正在运行的 ComfyUI 服务器，并且该服务器能够通过本地网络访问。
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

此技能允许 OpenClaw 通过连接到本地网络中运行的 ComfyUI 实例来生成图像。

## 设置

1. **服务器地址：** 将 `COMFYUI_SERVER_ADDRESS` 环境变量设置为你的 PC 的 IP 地址和端口（例如：`http://192.168.1.119:8189`）。
2. **API 模式：** 确保在 ComfyUI 的设置中开启了 **“启用开发者模式”**，以允许进行 API 交互。

## 使用方法

### 生成图像
运行内部生成脚本：
```bash
python3 {skillDir}/scripts/comfy_gen.py "your image prompt" $COMFYUI_SERVER_ADDRESS
```

### 使用自定义工作流程
将你的 API JSON 工作流程文件放入 `workflows/` 文件夹中，然后指定路径：
```bash
python3 {skillDir}/scripts/comfy_gen.py "your prompt" $COMFYUI_SERVER_ADDRESS --workflow {skillDir}/workflows/my_workflow.json
```

## 特性
- **默认使用 SDXL：** 默认使用高质量的 SDXL 工作流程（Juggernaut XL）。
- **自动备份：** 设计用于将生成的图像保存到 `image-gens/` 文件夹中，并可配置为同步到本地文档文件夹。
- **自定义工作流程：** 支持保存在 `workflows/` 文件夹中的外部 API JSON 工作流程。脚本会自动尝试将你的提示内容和随机种子值插入到工作流程中。

## 实现细节
该技能使用一个 Python 辅助程序（`scripts/comfy_gen.py`）来处理与 ComfyUI API 的 WebSocket/HTTP 通信、排队提示内容以及下载生成的图像。