---
name: alicloud-ai-image-qwen-image-edit
description: 使用阿里云模型工作室的 Qwen Image Edit Max (qwen-image-edit-max) 对图像进行编辑。该工具适用于修改现有图像（如修补、替换、风格迁移、局部编辑等），同时能够保持图像中主体内容的一致性，也可用于记录图像编辑请求与响应之间的对应关系。
---

**类别：提供者（Provider）**  
# Model Studio Qwen 图像编辑（Model Studio Qwen Image Edit）  

使用 Qwen 图像编辑模型进行基于指令的图像编辑，而非文本到图像的生成。  

## 关键模型名称（Critical Model Names）  
使用以下模型名称之一：  
- `qwen-image-edit-max`  
- `qwen-image-edit-max-2026-01-16`  

## 先决条件（Prerequisites）  
- 在虚拟环境中安装 SDK：  
```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```  
- 在您的环境中设置 `DASHSCOPE_API_KEY`，或将 `dashscope_api_key` 添加到 `~/.alibabacloud/credentials` 文件中。  

## 标准化接口（Normalized Interface, image.edit）  

### 请求（Request）  
- `prompt`（字符串，必填）：编辑指令。  
- `image`（字符串 | 字节，必填）：源图像的 URL、路径或字节数据。  
- `mask`（字符串 | 字节，可选）：需要修复的图像区域掩码。  
- `size`（字符串，可选）：例如 `1024*1024`。  
- `seed`（整数，可选）：用于图像生成的随机种子值。  

### 响应（Response）  
- `image_url`（字符串）：编辑后的图像 URL。  
- `seed`（整数）：用于生成图像的随机种子值。  
- `request_id`（字符串）：请求的唯一标识符。  

## 操作指南（Operational Guidance）  
- 编辑指令应明确指出需要修改的内容和需要保留的部分。  
- 使用掩码来实现精确的局部图像修复。  
- 将处理后的图像文件保存到对象存储中，并仅保留其 URL。  
- 为确保图像内容的一致性，请在编辑指令中提供明确的约束条件。  

## 本地辅助脚本（Local Helper Script）  
准备一个符合标准的请求 JSON 数据，并验证响应格式。  
```bash
.venv/bin/python skills/ai/image/alicloud-ai-image-qwen-image-edit/scripts/prepare_edit_request.py \
  --prompt "Replace the sky with sunset, keep buildings unchanged" \
  --image "https://example.com/input.png"
```  

## 输出路径（Output Location）  
- 默认输出路径：`output/ai-image-qwen-image-edit/images/`  
- 可通过设置 `OUTPUT_DIR` 变量来覆盖默认路径。  

## 参考资料（References）  
- `references/sources.md`