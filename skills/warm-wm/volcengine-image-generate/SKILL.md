---
name: volcengine-image-generate
description: 使用 `volcengine/image_generate.py` 脚本生成图像时，需要提供清晰且具体的 `prompt`（提示信息）。
license: Complete terms in LICENSE.txt
---

# 图像生成

## 使用场景

当您需要根据文本描述生成图像时，可以使用此功能来调用 `image_generate` 函数。

## 操作步骤

1. 准备一个清晰且具体的 `prompt`（提示信息）。
2. 运行脚本 `python scripts/image_generate.py "<prompt>"`。运行前，请先进入相应的目录。
3. 脚本会返回生成的图像 URL。

## 认证与凭据

- 首先，脚本会尝试读取 `MODEL_IMAGE_API_KEY` 或 `ARK_API_KEY` 环境变量。
- 如果这些变量未配置，脚本会尝试使用 `VOLCENGINE_ACCESS_KEY` 和 `VOLCENGINE_SECRET_KEY` 来获取 Ark API 密钥。

## 输出格式

- 控制台会输出生成的图像 URL。
- 如果调用失败，脚本会打印错误信息。

## 示例

```bash
python scripts/image_generate.py "a cute cat"
```