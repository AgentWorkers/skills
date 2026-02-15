---
name: fal-image-gen
description: "调用 fal.ai 模型的 API 进行图像生成（文本到图像和图像到图像）。当用户需要集成 fal、构建请求、运行作业、处理身份验证，或从 fal 模型 API 返回图像 URL 时，请使用这些 API。"
---

# Fal 图像生成

## 概述
使用此技能可以通过 fal 模型 API 实现文本到图像或图像到图像的转换功能。在调用之前，请务必查阅相关文档，确认所选模型所需的输入参数、输出格式以及认证要求，以确保操作的准确性。

## 快速入门
1. 从 fal 模型 API 文档中获取目标模型的 ID。
2. 从用户那里收集输入参数：
  - 文本到图像：`prompt`（提示语），可选 `negative_prompt`（负面提示语），`size/aspect`（尺寸/纵横比），`steps`（生成步骤数），`seed`（随机种子值），`safety`（安全设置）。
  - 图像到图像：源图像的 URL，`strength`（清晰度/去噪程度），以及上述的 `prompt` 和其他选项。
3. 选择合适的调用方式：
  - 如果用户偏好使用 SDK，提供 Python 或 JavaScript 的示例代码。
  - 如果用户偏好使用 REST，提供 curl 或 HTTP 请求的示例代码。
4. 执行请求，并从响应中获取图像的 URL。

## 工作流程：文本到图像
1. 确认模型的 ID 及其输入参数格式。
2. 查阅 fal 模型 API 文档，确认具体的输入字段和输出格式。
3. 验证输入参数：
  - 确保 `prompt` 不为空，并且输入的尺寸/纵横比符合模型的要求。
4. 构建请求：
  - 使用 SDK：调用 `run` 或 `submit` 方法，并传入包含输入参数的 `input` 对象。
  - 使用 REST：发送符合模型要求的 JSON 请求体到相应的 API 端点。
5. 执行请求并解析响应结果。
6. 从模型定义的响应字段中提取图像的 URL，并将其返回给用户。
7. 提供包含所有图像 URL 的列表，并附上用户请求的元数据（如随机种子值、尺寸等）。

## 工作流程：图像到图像
1. 确认模型的 ID 及其输入参数格式。
2. 验证输入参数：
  - 确保源图像可以通过 URL 访问，或者已经转换为模型所需的格式。
3. 根据文档确认所需的清晰度/去噪程度范围。
4. 构建请求：
  - 包含源图像、提示语以及模型要求的其他参数。
5. 执行请求并解析响应结果。
6. 从模型定义的响应字段中提取图像的 URL，并将其返回给用户。
7. 提供包含所有图像 URL 的列表。

## SDK 与 REST 的选择建议
- 对于简单的认证流程和重试机制，建议使用 SDK。
- 当用户需要原始的 HTTP 请求示例，或者在无法使用 SDK 的环境中运行时，建议使用 REST。
- 绝不要硬编码 API 密钥。请按照文档中的说明设置相应的环境变量或请求头。

## 最小示例（请根据文档填写具体内容）
以下示例仅供参考，请在查阅文档后替换占位符：

### Python（SDK）
```python
# Pseudocode: replace with the exact fal SDK import + call pattern from docs
import os
# from fal import client  # or the current SDK import

MODEL_ID = "<model-id-from-docs>"
input_data = {
    "prompt": "a cinematic photo of a red fox",
    # "image_url": "https://..."  # for image-to-image
    # "negative_prompt": "...",
    # "width": 1024,
    # "height": 1024,
}

# result = client.run(MODEL_ID, input=input_data)
# urls = extract_urls(result)
```

### JavaScript（SDK）
```javascript
// Pseudocode: replace with the exact fal SDK import + call pattern from docs
// import { client } from "@fal-ai/client";

const MODEL_ID = "<model-id-from-docs>";
const input = {
  prompt: "a cinematic photo of a red fox",
  // image_url: "https://..." // for image-to-image
};

// const result = await client.run(MODEL_ID, { input });
// const urls = extractUrls(result);
```

### REST（curl）
```bash
# Pseudocode: replace endpoint, headers, and payload schema from docs
curl -X POST "https://<fal-api-base>/<model-endpoint>" \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "a cinematic photo of a red fox"
  }'
```

## 参考资源
- `references/fal-model-api-checklist.md`：用于收集输入参数和验证响应的 checklist。
- `references/fal-model-examples.md`：包含文本到图像、图像到图像以及 REST 请求的示例模板。