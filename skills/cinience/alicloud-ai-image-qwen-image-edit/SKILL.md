---
name: alicloud-ai-image-qwen-image-edit
description: 使用 Alibaba Cloud Model Studio 的 Qwen Image Edit 模型（qwen-image-edit、qwen-image-edit-plus、qwen-image-edit-max 以及 snapshot）来编辑图像。这些模型适用于修改现有图像（如修复瑕疵、替换图像内容、进行风格转换或进行局部编辑），同时能够保持图像中主体内容的一致性，并可用于记录图像编辑请求与响应之间的对应关系。
version: 1.0.0
---
**类别：provider**

# Model Studio Qwen 图像编辑

## 验证

```bash
mkdir -p output/alicloud-ai-image-qwen-image-edit
python -m py_compile skills/ai/image/alicloud-ai-image-qwen-image-edit/scripts/prepare_edit_request.py && echo "py_compile_ok" > output/alicloud-ai-image-qwen-image-edit/validate.txt
```

**通过条件：**命令以 0 的状态退出，并且生成了 `output/alicloud-ai-image-qwen-image-edit/validate.txt` 文件。

## 输出与证据

- 将编辑请求的数据、结果 URL 以及模型参数保存在 `output/alicloud-ai-image-qwen-image-edit/` 目录下。
- 保留一个请求/响应对以方便重现实验结果。

**使用说明：**  
使用 Qwen Image Edit 模型进行基于指令的图像编辑，而不是文本到图像的生成。

## 关键模型名称  

请使用以下模型名称之一：  
- `qwen-image-edit`  
- `qwen-image-edit-plus`  
- `qwen-image-edit-max`  
- `qwen-image-2.0`  
- `qwen-image-2.0-pro`  
- `qwen-image-edit-plus-2025-12-15`  
- `qwen-image-edit-max-2026-01-16`  

## 先决条件  

- 在虚拟环境中安装 SDK：  
```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```  
- 在您的环境中设置 `DASHSCOPE_API_KEY`，或者将 `dashscope_api_key` 添加到 `~/.alibabacloud/credentials` 文件中。  

## 标准化接口（image.edit）  

### 请求参数  
- `prompt`（字符串，必填）：编辑指令  
- `image`（字符串 | 字节，必填）：源图像的 URL、路径或字节数据  
- `mask`（字符串 | 字节，可选）：需要修复的区域掩码  
- `size`（字符串，可选）：例如 `1024*1024`  
- `seed`（整数，可选）：随机数种子  

### 响应参数  
- `image_url`（字符串）：编辑后的图像 URL  
- `seed`（整数）：随机数种子  
- `request_id`（字符串）：请求 ID  

## 操作指南  

- 编辑指令应明确指出需要修改的内容和需要保留的部分。  
- 使用掩码来实现精确的局部编辑。  
- 将编辑后的图像保存到对象存储中，并仅保留图像的 URL。  
- 为确保图像内容的一致性，请在指令中提供明确的约束条件。  

## 本地辅助脚本  

准备标准化的请求 JSON 数据，并验证响应格式：  
```bash
.venv/bin/python skills/ai/image/alicloud-ai-image-qwen-image-edit/scripts/prepare_edit_request.py \
  --prompt "Replace the sky with sunset, keep buildings unchanged" \
  --image "https://example.com/input.png"
```  

## 输出路径  

- 默认输出路径：`output/alicloud-ai-image-qwen-image-edit/images/`  
- 可通过设置 `OUTPUT_DIR` 变量来覆盖默认路径。  

## 工作流程  

1) 确认用户的操作意图、所在地区、使用的标识符，以及操作是只读还是修改操作。  
2) 首先执行一个最小的只读查询，以验证网络连接和权限。  
3) 使用指定的参数和范围执行目标操作。  
4) 验证结果并保存输出文件及相关证据。  

## 参考资料  
- `references/sources.md`