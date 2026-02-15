---
name: alicloud-ai-image-zimage-turbo
description: 使用 Alibaba Cloud Model Studio Z-Image Turbo (z-image-turbo) 通过 DashScope 的多模态生成 API 生成图像。该 API 可用于创建文本到图像的输出结果，控制图像的大小、种子值以及提示信息（prompt_extend），同时可用于记录 Z-Image 的请求与响应映射关系。
---

**类别：provider**

# Model Studio Z-Image Turbo

使用 Z-Image Turbo 通过 DashScope 的多模态生成 API 快速实现文本到图像的转换。

## 关键模型名称

**仅使用以下精确的模型名称：**
- `z-image-turbo`

## 先决条件

- 在您的环境中设置 `DASHSCOPE_API_KEY`，或者将 `dashscope_api_key` 添加到 `~/.alibabacloud/credentials` 文件中（环境变量优先）。
- 选择区域端点（北京或新加坡）。如果不确定，请选择最合适的区域或询问用户。

## 标准化接口（`image.generate`）

### 请求参数
- `prompt`（字符串，必填）
- `size`（字符串，可选）例如：`1024*1024`
- `seed`（整数，可选）
- `prompt_extend`（布尔值，可选；默认为 `false`）
- `base_url`（字符串，可选）用于覆盖 API 端点

### 响应参数
- `image_url`（字符串）
- `width`（整数）
- `height`（整数）
- `prompt`（字符串）
- `rewritten_prompt`（字符串，可选）
- `reasoning`（字符串，可选）
- `request_id`（字符串）

## 快速启动（使用 curl）

```bash
curl -sS 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -d '{
    "model": "z-image-turbo",
    "input": {
      "messages": [
        {
          "role": "user",
          "content": [{"text": "A calm lake at dawn, a lone angler casting a line, cinematic lighting"}]
        }
      ]
    },
    "parameters": {
      "size": "1024*1024",
      "prompt_extend": false
    }
  }'
```

## 本地辅助脚本

```bash
python skills/ai/image/alicloud-ai-image-zimage-turbo/scripts/generate_image.py \
  --request '{"prompt":"a fishing scene at dawn, cinematic, realistic","size":"1024*1024"}' \
  --output output/ai-image-zimage-turbo/images/fishing.png \
  --print-response
```

## 关于尺寸的说明

- 总像素数必须在 `512*512` 到 `2048*2048` 之间。
- 建议使用常见的尺寸，如 `1024*1024`、`1280*720`、`1536*864`。

## 成本说明

- 当 `prompt_extend` 设置为 `true` 时，费用会比 `false` 高。仅在需要生成重写后的提示时启用此选项。

## 输出位置

- 默认输出路径：`output/ai-image-zimage-turbo/images/`
- 可通过 `OUTPUT_DIR` 变量覆盖默认输出目录。

## 参考资料

- `references/api_reference.md`：请求/响应格式及区域端点的详细信息。
- `references/sources.md`：官方文档。