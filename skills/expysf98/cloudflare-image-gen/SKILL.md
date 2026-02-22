---
name: cloudflare-image-gen
description: 使用 Cloudflare Workers 的 AI flux-1-schnell 模型生成图像。当用户通过 Cloudflare Workers API 提出文本到图像的生成请求时，可以使用该模型。
---
# Cloudflare 图像生成

该技能使用 Cloudflare Workers AI 的 `@cf/black-forest-labs/flux-1-schnell` 模型来生成图像。

## 认证信息

- 账户 ID：`1e89d3ce76cbfef3b5c340e3984b7a52`
- 令牌：`aCTA2KaKa1n3ayFDL-LPmZ-JgUC0HHgA5Msy18Bk`
- 模型：`@cf/black-forest-labs/flux-1-schnell`

## 使用方法

可以直接运行脚本：

```bash
python3 /home/ubuntu/.openclaw/workspace/skills/cloudflare-image-gen/scripts/generate_image.py "your prompt here" -o output.png
```

或者使用 Python 函数：

```python
import sys
sys.path.insert(0, '/home/ubuntu/.openclaw/workspace/skills/cloudflare-image-gen/scripts')
from generate_image import generate_image

output_path = generate_image("a black horse")
```

## 输出结果

脚本会将生成的图像保存为 PNG 格式，并返回文件路径。您可以通过 Telegram 将图像发送给用户。